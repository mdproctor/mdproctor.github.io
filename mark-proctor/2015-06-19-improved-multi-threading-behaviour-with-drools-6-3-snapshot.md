---
layout: post
title: "Improved multi-threading behaviour with Drools 6.3 SNAPSHOT"
date: 2015-06-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/06/improved-multi-threading-behaviour-with-drools-6-3-snapshot.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Improved multi-threading behaviour with Drools 6.3 SNAPSHOT](<https://blog.kie.org/2015/06/improved-multi-threading-behaviour-with-drools-6-3-snapshot.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 19, 2015  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

We’ve rewritten the internal parts of our code that deal with multi-threading to remove a large number of synchronisation points and to improve stability and predictability. We believe that what we have done is now far more robust for the interaction of the User, Timer and Engine threads. Our initial benchmarking is showing that this has led to mild performance improvements too. We’d really like to get this hardened, before we do 6.3 final, so if you have an application that users Timers or Time Windows, especially when using FireUntilHalt, could you give it a good hammering? Especially those using the [TimedRuleExecutionFilter](<http://docs.jboss.org/drools/release/6.2.0.Final/drools-docs/html/ch02.html#d0e1164>), which allows a timer to fire reactively when the engine is in passive mode (not fireUntilHalt).

For this iteration we just focused on the engine internals, we have not yet touched the outer lock and sync points, i.e. the ksession and kbase locks that threads go through when they do an insert/update/delete action. These apparently can create contention for lots of small lived ksessions. We believe with the latest work we’ve been doing we can soon improve this area too.

You should find all this work in the latest snapshot, for drools-core and drools-compiler.  
<https://repository.jboss.org/nexus/content/repositories/snapshots/org/drools/drools-core/6.3.0-SNAPSHOT/>  
<https://repository.jboss.org/nexus/content/repositories/snapshots/org/drools/drools-compiler/6.3.0-SNAPSHOT/>

For those interest, we have done two things. The first part was to properly separate the User insert/update/delete thread actions with he Engine network evaluations thread. The second part is to remove most of the internal sync points and replace with a state machine.

The User/Engine thread separation has been made possible by our move away from [Rete to Phreak](<http://blog.athico.com/2013/11/rip-rete-time-to-get-phreaky.html>). With Rete the network evaluation is done during the User insert/update/delete action, meaning each user action locks the entire engine. With phreak the insert/update/delete is separated and network evaluation happens when fireAllRules or fireUntilHalt is called. We’ve added a queue, [SynchronizedPropagationList](<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/SynchronizedPropagationList.java>), that stores up the user actions as commands, in a thread safe queue. The engine thread then takes all the entries on each of its iterations. We found our custom queue outperformed the JDK concurrent queues, but I think that is due to our specialist implementation. Instead of the engine taking just the HEAD entry, it does a takeAll and the processes that returned linked list as a batch. This reduces the amount of times the Engine thread hits the queue for each of the elements it processes. We can also efficiently handle when to park and when to notify the engine to spin up again, which was alway a bit hit and miss before. Now it simply parks when takeAll returns null, and it notifies if a Timer or User adds work be done and the engine is known to be parked.

The second part introduces a state machine for the User, Timer and Engine thread interactions. This now provides us with a system that we can ca be documented, due to it’s simplification, and also this will help explain the various thread interactions and behaviours. This was missing before, and understanding the behaviour could be a be bit confusing for users. It also means we now have a better behaviour for the interactions of calling fireAllRules and fireUntilHalt and when they overlap, or are called twice. i..e what happens if you call fireUntilHalt while fireAllRules is currently operating? or you call fireAllRules twice, or fall fireAllRules when fireUntilHalt is operating? Our state machine now more cleanly handles this with describable behaviour.

The bulk of the work is contained within the DefaultAgenda:  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/common/DefaultAgenda.java>

There are three threads that can interact. A User thread doing an insert/update/delete, the Timer thread, for timers and time windows and the engine thread for network evaluations. We have now changed this so that the timer thread no longer does network evaluations, blocking other threads, instead it submits a job and notifies the Engine thread (if it’s not already running) to process it. You can see this in [PhreakTimerNode](<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/PhreakTimerNode.java>). When the Timer now triggers it’ll submit a job tot he queue that I introduced in the previous paragraph.
[code]
    public void execute(JobContext ctx) {  
        TimerNodeJobContext timerJobCtx = (TimerNodeJobContext) ctx;  
        InternalWorkingMemory wm = timerJobCtx.getWorkingMemory();  
        wm.addPropagation( new TimerAction( timerJobCtx ) );  
    }
[/code]

When a timer thread is kicked off it has no idea if the engine thread is evaluating or parked. It could be parked because fireAllRules has returned and it’s waiting for the next fireAllRules. Or it could be parked because fireUntilHalt currently has no work to do. If for instance the engine is parked in fireUntilHalt it needs to notify the engine thread to unpark and process the timer work. If however engine thread is working (be it fireUntilRules or fireUntilHalt) it should just put it into the queue for the engine thread to process and not do the notification. These interactions are subtle, but they must be solid and avoid contention or excessing syncing. The behaviour is complicated further by the [TimedRuleExecutionFilter](<http://docs.jboss.org/drools/release/6.2.0.Final/drools-docs/html/ch02.html#d0e1164>).

To handle this we introduced the following enum to represent the available states of the engine:
[code]
    private enum ExecutionState {  // fireAllRule | fireUntilHalt | executeTask -->    INACTIVE( false ),         // fire        | fire          | exec    FIRING_ALL_RULES( true ),  // do nothing  | wait + fire   | enqueue    FIRING_UNTIL_HALT( true ), // do nothing  | do nothing    | enqueue    REST_HALTING( false ),     // wait + fire | wait + fire   | enqueue    FORCE_HALTING( false ),    // wait + fire | wait + fire   | wait + exec    EXECUTING_TASK( false );   // wait + fire | wait + fire   | wait + exec  
        private final boolean firing;  
      
        ExecutionState( boolean firing ) {  
            this.firing = firing;  
        }  
      
        public boolean isFiring() {  
            return firing;  
        }  
    }
[/code]

You can now see this state machine being used by fireAllRules and fireUntilHalt. Notice the new method waitAndEnterExecutionState. This allows threads to either park or return straight away – i.e. if you call fireAllRules and fireUntilHalt is running, just return straight away. If you call fireUntilHalt while fireAllRules is running, wait until fireAllRules finishes, then start fireUntilHalt.
[code]
    public int fireAllRules(AgendaFilter agendaFilter,  
                            int fireLimit) {  
        synchronized (this) {  
            if (currentState.isFiring()) {  
                return 0;  
            }  
            waitAndEnterExecutionState( ExecutionState.FIRING_ALL_RULES );  
        }
[/code]
[code]
    public void fireUntilHalt(final AgendaFilter agendaFilter) {  
        synchronized (this) {  
            if (currentState == ExecutionState.FIRING_UNTIL_HALT) {  
                return;  
            }  
            waitAndEnterExecutionState( ExecutionState.FIRING_UNTIL_HALT );  
        }
[/code]
[code]
    private void waitAndEnterExecutionState( ExecutionState newState ) {  
        if (currentState != ExecutionState.INACTIVE) {  
            try {  
                wait();  
            } catch (InterruptedException e) {  
                throw new RuntimeException( e );  
            }  
        }  
        currentState = newState;  
    }
[/code]

Previously you saw the Timer thread submitted a job into a queue, this is also handled by the state machine.
[code]
    public void executeTask( ExecutableEntry executable ) {  
        synchronized (this) {  
            if (isFiring() || currentState == ExecutionState.REST_HALTING) {  
                executable.enqueue();  
                return;  
            }  
            waitAndEnterExecutionState( ExecutionState.EXECUTING_TASK );  
        }  
      
        try {  
            executable.execute();  
        } finally {  
            immediateHalt();  
        }  
    }
[/code]

A key aspect we had to support here was what if a Timer thread triggers some work while the Engine thread is just returning. You end up with gaps, so that’s work that doesn’t fire, that the user was expecting. This is a problem people have seen in previous Drools releases. The combination of this task system halting statuses, allow the engine to restart again before properly halting. You can think of it as a two phase halting system. You an see that with the main do loop and then the second while loop, ensuring we get a clean shut down – i.e. the engine cannot park, unless there are no timer actions, before it returns and sets the state machine to INACTIVE.
[code]
    this.workingMemory.flushPropagations();  
    int returnedFireCount;  
    do {  
        returnedFireCount = fireNextItem( agendaFilter, fireCount, fireLimit );  
        fireCount += returnedFireCount;  
        this.workingMemory.flushPropagations();  
    } while ( ( isFiring() && returnedFireCount != 0 && (fireLimit == -1 || fireCount < fireLimit) ) );  
      
    PropagationEntry head = tryHalt();  
    while (head != null) {  
        fireCount += fireNextItem( agendaFilter, fireCount, fireLimit );  
        SynchronizedPropagationList.flush(workingMemory, head);  
        head = workingMemory.takeAllPropagations();  
    }
[/code]
[code]
    private PropagationEntry tryHalt() {  
        synchronized (this) {  
            PropagationEntry head = workingMemory.takeAllPropagations();  
            if (head == null) {  
                currentState = ExecutionState.INACTIVE;  
                notify();  
            } else if (currentState != ExecutionState.FORCE_HALTING) {  
                currentState = ExecutionState.REST_HALTING;  
            }  
            return head;  
        }  
    }
[/code]

One of the key aspects here is the takeAll action. We can use this to atomically both check if there is work to do, and return that work within a sync point. But process the work outside of the sync point. So you can see it it will only finally halt, if takeAll returns null. Note the Timer thread would have to go through this sync point to add more work – ensuring there are no gaps.

There is a lot to take in here, and it’s a bit of a brain dump. But I hope it proves useful to those wanting to understand how we are improving our engine, and how the prior work we did with the Phreak algorithm has enabled this.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F06%2Fimproved-multi-threading-behaviour-with-drools-6-3-snapshot.html&linkname=Improved%20multi-threading%20behaviour%20with%20Drools%206.3%20SNAPSHOT> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F06%2Fimproved-multi-threading-behaviour-with-drools-6-3-snapshot.html&linkname=Improved%20multi-threading%20behaviour%20with%20Drools%206.3%20SNAPSHOT> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F06%2Fimproved-multi-threading-behaviour-with-drools-6-3-snapshot.html&linkname=Improved%20multi-threading%20behaviour%20with%20Drools%206.3%20SNAPSHOT> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F06%2Fimproved-multi-threading-behaviour-with-drools-6-3-snapshot.html&linkname=Improved%20multi-threading%20behaviour%20with%20Drools%206.3%20SNAPSHOT> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F06%2Fimproved-multi-threading-behaviour-with-drools-6-3-snapshot.html&linkname=Improved%20multi-threading%20behaviour%20with%20Drools%206.3%20SNAPSHOT> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F06%2Fimproved-multi-threading-behaviour-with-drools-6-3-snapshot.html&linkname=Improved%20multi-threading%20behaviour%20with%20Drools%206.3%20SNAPSHOT> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F06%2Fimproved-multi-threading-behaviour-with-drools-6-3-snapshot.html&linkname=Improved%20multi-threading%20behaviour%20with%20Drools%206.3%20SNAPSHOT> "Email")
  *[]: 2010-05-25T16:11:00+02:00