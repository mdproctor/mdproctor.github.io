---
layout: post
title: "Drools: A detailed description of internal code cleanups for fireAllRules, fireUntilHalt and Timers."
date: 2015-12-03
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/12/drools-a-detailed-description-of-internal-code-cleanups-for-fireallrules-fireuntilhalt-and-timers.html
---

In [June](<http://blog.athico.com/2015/06/improved-multi-threading-behaviour-with.html>) we blogged about a new internal state machine to manage the interaction of User, Timer and Engine threads. We’ve now done another big internal clean up of this code, to make it easier to read and easier to understand.

As previous mentioned all actions (insert, update, delete etc) are now placed into a thread safe propagation queue. The user thread, when executing those actions, never touches the engine any more, not even the alpha network. This gives improved thread safety. Instead when the engine starts it first drains and evaluates this queue, which can result in alpha network evaluations, before doing rule evaluation and firings.

As well as User and Engine thread separation the other aim of the state machine was to co-ordinate the Timer thread. When a timer kicks off the engine may be INACTIVE or it may be running. If the engine is active the Timer should just submit an entry into the propagation queue and let the current executing thread handle the job. If the engine is not active and the timer rule is async the timer thread should take care of the evaluating and firing, via the executeTask method. The state machine is designed to minimise sync’s and locks to keep contention minimal.

The engine now has 5 possible states it can be in. INACTIVE is the starting state.

[![](/legacy/assets/images/2015/12/2af3fd9af67a-8dDvaLZ.png)](</assets/images/2015/12/21696e15738a-8dDvaLZ.png>)

Engine evaluation and rule firing has three potential entry points fireAllRules, fireUntilHalt and async timer rules – the later is done through the executeTask part. We have unified fireAllRules and fireUntilHalt into a single fireLoop method, that uses a strategy class, passed as an argument, to handle the potential rest state of the loop. The engine is considered at rest when there are no rules firing, when there are no more agenda group to evaluate and when the queue is empty.

FireAllRules all rules will then set the engine to INACTIVE and the loop will exit. FireUntilHalt will make the current thread wait, until more work comes into the queue for processing. Work has been done here to make sure there are no gaps, and loss of executions, during those state transitions.

When a thread wants to transition to FIRE_ALL_RULES or FIRE_UNTIL_HALT or EXECUTE_TASK, it must go through waitAndEnterExecutionState. If the engine is INACTIVE it can transition straight away, if not it’ll go into a wait state until the current executing thread has finished and returned the engine back to INACTIVE:

```java
private void waitAndEnterExecutionState( ExecutionState newState ) {
    if (currentState != ExecutionState.INACTIVE) {
        try {
            stateMachineLock.wait();
        } catch (InterruptedException e) {
            throw new RuntimeException( e );
        }
    }
    setCurrentState( newState );
}
```

Let’s look at how fireAllRules() uses this. Note firstly that if the engine is already running, because fireAllRules or fireUntilHalt have been previous called and still running, it will simply exit. Second note it only holds the sync point long enough to either exit or make the desired transition. Once the engine is in FIRE_ALL_RULES state it can let go of the sync block and the state machine will stop anything from interfering with it.

```
public int fireAllRules(AgendaFilter agendaFilter,
                        int fireLimit) {
    synchronized (stateMachineLock) {
        if (currentState.isFiring()) {
            return 0;
        }
        waitAndEnterExecutionState( ExecutionState.FIRING_ALL_RULES );
    }

   int fireCount = fireLoop(agendaFilter, fireLimit, RestHandler.FIRE_ALL_RULES);

   return fireCount;
}
```

The fireLoop is now generic and used by both fireAllRules and fireUntilHalt, with the use of the RestHandler strategy to handle the logic for when the engine comes to a rest point.

```
private int fireLoop(AgendaFilter agendaFilter,
                     int fireLimit,
                     RestHandler restHandler) {
```

```java
// The engine comes to potential rest (inside the loop) when there are no propagations and no rule firings.        // It's potentially at rest, because we cannot guarantee it is at rest.        // This is because external async actions (timer rules) can populate the queue that must be executed immediately.        // A final takeAll within the sync point determines if it can safely come to rest.        // if takeAll returns null, the engine is now safely at rest. If it returns something        // the engine is not at rest and the loop continues.        //        // When FireUntilHalt comes to a safe rest, the thread is put into a wait state,        // when the queue is populated the thread is notified and the loop begins again.        //        // When FireAllRules comes to a safe rest it will put the engine into an INACTIVE state        // and the loop can exit.        //        // When a halt() command is added to the propagation queue and that queue is flushed        // the engine is put into a HALTING state. At this point isFiring returns false and        // no more rules can fire and the loop exits.
int fireCount = 0; try {         PropagationEntry head = workingMemory.takeAllPropagations(); int returnedFireCount = 0; boolean limitReached = fireLimit == 0; // -1 or > 0 will return false. No reason for user to give 0, just handled for completeness. boolean loop = true; while ( isFiring()  )  { if ( head != null ) { // it is possible that there are no action propagations, but there are rules to fire. this.workingMemory.flushPropagations(head);                 head = null;             } // a halt may have occurred during the flushPropagations, // which changes the isFiring state. So a second isFiring guard is needed if (!isFiring()) { break;             }              evaluateEagerList();             InternalAgendaGroup group = getNextFocus(); if ( group != null && !limitReached ) { // only fire rules while the limit has not reached. returnedFireCount = fireNextItem( agendaFilter, fireCount, fireLimit, group );                 fireCount += returnedFireCount;                  limitReached = ( fireLimit > 0 && fireCount >= fireLimit );                 head = workingMemory.takeAllPropagations();             } else {                 returnedFireCount = 0; // no rules fired this iteration, so we know this is 0 group = null; // set the group to null in case the fire limit has been reached } if ( returnedFireCount == 0 && head == null && ( group == null || !group.isAutoDeactivate() ) ) { // if true, the engine is now considered potentially at rest head = restHandler.handleRest( workingMemory, this );             }         } if ( this.focusStack.size() == 1 && getMainAgendaGroup().isEmpty() ) { // the root MAIN agenda group is empty, reset active to false, so it can receive more activations. getMainAgendaGroup().setActive( false );         }     } finally { // makes sure the engine is inactive, if an exception is thrown. // if it safely returns, then the engine should already be inactive        // it also notifies the state machine, so that another thread can take over        immediateHalt();
    }
    return fireCount;
}The fire loop goes through a single sync point when it does a takeAll() which is simple operation to return the current head instance, while also nulling member head field so that the queue is empty.  During this takeAll() it means that any user or timer operations will be waiting on the sync to release, before they can add into the queue. After that the rest of method, evaluating the returned list of items and evaluating the network and firing rules can happen without ever needing to go through another sync or lock.The rest handlers are both two very simple pieces of code:interface RestHandler {
    RestHandler FIRE_ALL_RULES = new FireAllRulesRestHandler();
    RestHandler FIRE_UNTIL_HALT = new FireUntilHaltRestHandler();

    PropagationEntry handleRest(InternalWorkingMemory wm, DefaultAgenda agenda);

    class FireAllRulesRestHandler implements RestHandler {
        @Override        public PropagationEntry handleRest(InternalWorkingMemory wm, DefaultAgenda agenda) {
            synchronized (agenda.stateMachineLock) {
                PropagationEntry head = wm.takeAllPropagations();
                if (head == null) {
                    agenda.halt();
                }
                return head;
            }
        }
    }

    class FireUntilHaltRestHandler  implements RestHandler {
        @Override        public PropagationEntry handleRest(InternalWorkingMemory wm, DefaultAgenda agenda) {
            return wm.handleRestOnFireUntilHalt( agenda.currentState );
        }
    }
}
@Overridepublic PropagationEntry handleRestOnFireUntilHalt(DefaultAgenda.ExecutionState currentState) {
    // this must use the same sync target as takeAllPropagations, to ensure this entire block is atomic, up to the point of wait    synchronized (propagationList) {
        PropagationEntry head = takeAllPropagations();

        // if halt() has called, the thread should not be put into a wait state        // instead this is just a safe way to make sure the queue is flushed before exiting the loop        if (head == null && currentState == DefaultAgenda.ExecutionState.FIRING_UNTIL_HALT) {
            propagationList.waitOnRest();
            head = takeAllPropagations();
        }
        return head;
    }
}Notice that the FireAllRulesRestHandler must get the stateMachineLock while it does final takeAll, before it can know it’s truly safe to return. This is due to timers which may be placed onto the queue, that need immediate firing. If engine was to return, the timer would not fire straight away – this is what we refer to as a “gap” in behaviour, that is now avoided.The FireUntilHalt gets a lock on the propagation queue, because as well as doing a takeAll it must perform the null check and the wait operation, all atomically. Again if the null check was not within the sync point, we’d end up with another potential gap in behaviour, that is now avoided.The final part of the puzzle is executeTask. This allows async operations to happen, typically a timer task, in an optimal way. If the engine is already running, due to FireAllRules or FireUntilHalt, then simply submit the task to the queue and let the current running thread handle it. If not then enter the EXECUTING_TASK state and execute it within the current thread.@Overridepublic void executeTask( ExecutableEntry executable ) {
    synchronized (stateMachineLock) {
        // state is never changed outside of a sync block, so this is safe.        if (isFiring()) {
            executable.enqueue();
            return;
        } else if (currentState != ExecutionState.EXECUTING_TASK) {
            waitAndEnterExecutionState( ExecutionState.EXECUTING_TASK );
        }
    }

    try {
        executable.execute();
    } finally {
        immediateHalt();
    }
}I should add that halt() is now submitted as a command, and evaluated as part of the standard queue drain. When executing, it will changing the engine into a HALTING, inside of a sync block. This will allow the outer loop to exit:public void halt() {
    synchronized (stateMachineLock) {
        if (currentState.isFiring()) {
            setCurrentState( ExecutionState.HALTING );
        }
    }
}So we now have really robust code for handling User, Timer and Engine thread interactions, in a way which has understandable behaviour. We’ve put a lot of effort into the cleanup, so that the code and behaviour can hopefully be understood by everyone.There is one final part of the engine that would still be considered unsafe. This is where a user invokes a setter of an inserted fact on one thread, while the engine is running. This can obviously end in tears. What we plan to allow is for users to submit tasks to this queue, so they can be executed with the same thread as the running engine. This will allow users to submit pojo updates from another thread outside of engine, as tasks, to execute safely.
```