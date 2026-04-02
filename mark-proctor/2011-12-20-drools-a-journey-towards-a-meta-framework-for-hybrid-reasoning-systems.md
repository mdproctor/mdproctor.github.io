---
layout: post
title: "Drools : A Journey towards a Meta Framework for Hybrid Reasoning Systems"
date: 2011-12-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/12/drools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools : A Journey towards a Meta Framework for Hybrid Reasoning Systems](<https://blog.kie.org/2011/12/drools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- December 20, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

## Introduction

Recent versions of Drools have started to show our direction towards a hybrid reasoning system, going beyond production rule systems. In 2011 we introduced prolog style derivation trees, with reactive materialised views, we also introduced traits. In 2012 we’ll continue to build out more of the prolog like functionality and traits will expand to description logic for semantic reasoning.

To make further progress I feel we need to smash apart our current infrustructure that is hard coded for the rigid way PRD systems where designed 30 years ago. In that time the structure of PRD systems hasn’t change that much. In essence they have an agenda + conflict resolution strategy. Simple “groups” have been added by various systems be it a single push/pop stacks or rufeflows. Further execution control has been hard coded via attributes.

If we could break Drools down into smaller components, each with life cycles, event models, hook points and designed for compositability – what would this look like? This would provide more of a meta framework, so the author can define how it’s execution should behave and open up Drools to a wider variety of research and problem solving.

Existing PRD behaviour can be easily provided as an “out of the box meta configuration”, however it is hoped via “macro’s” power users can implement other useful types of behaviours and provide those to end users as fully encapsulated macro’s.

By opening up the way that Drools components can be easily brought together we hope to make it easier for people to try out different research ideas – without having to develop yet another engine. This will allow ideas to go beyond that conceived by the core development team.

I hope the introduction of a macro concept for rules will allow for a more pattern oriented approach to rule engine development.

When reading this document please cast aside preconcieved ideas of what a rule engine is or how it works. The document is conceptual in nature and at this stage I would like conceptual input on how to progress the ideas, and not spend 95% of the time argueing over which symbols or keywords to use, or whether it’s needed (see [http://www.bikeshed.com](<http://www.bikeshed.com/>)). Expect many rough sketches, incomplete syntax etc, it is conceptual brain storming and not an implementation spec.

Continuous updates to this article can be found [here](<http://community.jboss.org/wiki/DroolsModule/>).

## Module

Additional ideas on modules for rules can be read as part of the research on Venus:  
[Venus: An Object-Oriented Extension of Rule-Based Programming (1998) ](<http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.6958>)  
[An Overview of the VenusDB Active Multidatabase System (1996) ](<http://citeseer.ist.psu.edu/viewdoc/similar?doi=10.1.1.21.8486&type=ab>)

The module concept can be introduced as generic container for rules. The module consists of a name and arguments. Parenthesis can be ommitted if no arguments are specified. There are also further member variables, internal to the module. A module supports attributes. A module can specify a single parent module, there is a MAIN module which is the default parent of all modules. A module may optional extend other modules
[code]
    <@attribute(....)>*  
    module <module_name> ( <arguments>*)  
     <parent module_name>?   
     <extends <module_name>+>*   
     <variables plus optional initialisation>*
[/code]

A DRL can have multiple modules specified. Within the DRL file all rules that come after that module name are associated with the module.
[code]
    module A  
     rule r1....  
     end   
      
     rule r2...  
     end  
      
    module B(String s, Person p)   
     var Book b    
      
     rule r3...   
     end    
      
     rule r4...   
     end
[/code]

NOTE) Can modules span namespaces? What does a namespce mean for a module, does it live within the namespace or is it global? For now assuming scoped to namespace.:

A module can be called like a java Runnable, the caller’s method signature must match the specified arguments or a runtime exception is thrown
[code]
    Module m = kruntime.packages["org.domain"].modules["A"]  
    ModuleHandle bhA = m.run()  
      
    m = kruntime.packages["org.domain"].modules["B"]  
    ModuleHandle mhB =m.run( "S", new Person("darth") );
[/code]

The parameter variables are available to the rules inside of the module, in a similar manner that globals are. An array pattern referencing the arguments is injected as the root pattern to each rule. This not only makes the variables available but acts as a control object for when rules can fire with those variables. The ModuleHandle has a “stop” method that results in that array element being retracted, and thus the rule cannot fire any more for those variables. Even rules associated with that module that do not depend on those variables has the root control fact injected.
[code]
    mhB.stop()
[/code]

Note that a module can be called multple times with different arguments, each results in a different ModuleHandle. Should a module be called with existing arguments the previous ModuleHandle is returned. So you can consider a module instance module + variables.

Passed module arguments may or may not be facts, if they are facts they may be modified (unlike globals) and patterns will respect and react to that change as normal. The module’s called signature is updated.

The role of member variables is for scoped data avaliable to events, such as counters or intermediary objects.

(NOTE) If we want to make member variables available to rules, we will need to think carefuly about the behaviour, as they have more potentially more complications than globals. Currently they are only available as fields on events, see the activation-group variance.

## Match

A Match is the same as the traditional Activation concept in PRD systems. It has an array of FactHandle’s for the matched objects. But we recognise the Match can be active or dormant, and use a boolean to represent this, and that even information on dormant matches can be useful in reasoning systems. A Match is considered active if it is ellible for for foring and has not yet done so.
[code]
    Match   
     FactHandle[] facts   
     boolean active
[/code]

(NOTE) Maybe instead of “boolean active” we should have an enum, and possible also including “running” as a state. ACTIVE, RUNNING, DORMANT.

(NOTE) It’s possible for a rule + facts to fire multiple times without relaxing (made false). We should optional keep a counter for the number of times fired, and even each execution can be time stamped.

## Module Properties
[code]
    Module Properties  
    activeSize // number of active Matches, queries can be used for more complex cases using rule attributes  
    dormantSize // number of dormant Matches, queries can be used for more complex cases using rule attributes  
    activeMatches // Collection of active Matches  
    dormantMatches // Collection of dormant Matches
[/code]

(NOTE) The size and and collection properties only contain relevance for eager matching algorithms that compute an entire cross product for each WME change. Future versions of Drools may optionally implement some lazy matching and in those situations the user’s understanding of those properties may be a problem.

## Module Methods
[code]
    Module Methods  
     cancel() // all active matches are made dormant  
     cancel( Match ) // cancels a match, i.e. sets it dormant, if already dormant this method does nothing.  
     refresh() // all dormant activates are made active, however filters such as calendars, enabled etc are still obeyed  
     refresh( Match ) // refreshes a match, i.e. sets it active if it's dormant, if it's already active it is ignored  
     halt() // The state of the module is preserved, but no  
     continue() //  
     addListener() // type inference adds the listener implementation to the correct list(s).                    
                   // Listener composition for  single instance is allowed, meaning it is added to multiple listener lists.  
     start(Object[] args)  
     stop() 
[/code]

## Module Events and Lifecycle

A Module has a life cycle to which listeners may be added.
[code]
    Module Events  
    onEnter // when a module is called  
    onExit  // when a module is stopped  
    onMatch // when a rule is matched  
    onRematch // when a rule is matched and is matched again, without relaxing first (via update)  
    onUnmatch // when a rule stops being matched  
    onBeforeFire // before a rule for this module fires  
    onAfterFire // after a rule for this module fires  
    onHalt // tells the listener halt has been callled  
    onResume // tells the listeners resume ahs been called  
    onEmpty // when the size == 0, all Matches are dormant -- other potential events --  
    onBeforeRuleEvaluation // before a wme insert/update/delete for this module  
    onAfterRuleEvaluation// after a wme insert/update/delete for this module
[/code]

onEmpty will only be triggered after the first rule evaluation phase. i.e. it does not fire after onEnter, before the rule evaluation phase has had a chance to execute.

(NOTE) Other potential events are before/after rule evaluation. Each WME insert/modify/update causes a rule evaluation, and could be listend to via onBeforeRuleEvaluation and OnAfterRuleEvaluation. This poses problems with concurrency where potentially multiple insertions/updates/modifies could be happening at the same time. So at best it’s a listener scoped to a fact, we cannot guarantee the resutling matches are assocated with this event, unless serial rule evaluation is enforced – which may be a possible configuration for a module.

DRL will support the ability to declare literal functions attached to these listeners, the exact syntax for this is TBD. But the keyword will probaby be “on.”. We will support .Net style delegate operators for = and += when adding or setting listeners.
[code]
    on.Enter += {  
    }
[/code]

Those listeners can also be added from java code.

## Simulation the Agenda

A Module itself doesn’t do anything other than obey the life cycle of the prescribed events, it doesn’t even fire a rule, making it dormant. The only thing the Module does is maintain the list of active and dormant matches.

However this then allows a much more flexible system to which the end user can customise the behaviour. For instance the traditional agenda+conflict resolution strategy can be implemented via the onMatch/onRematch/onUnmatch listeners.
[code]
    class Agenda implements onMatch, onUnmatch, onRematch {   
     ....  
    }
[/code]

The above class implements a composition of event listener interfaces, but it only needs to be added to the module once
[code]
    module.addListener( new Agenda() );
[/code]

This means each module may have it’s own conflict resolution strategy. Some may want more traditional lifo execution, but anything else is possible. Such as rule definition order, or async execution. Listeners can be combined, but that means that order IS important. Some listeners may want to preevent a rule from firing, others may want to prever other rules from firing after the current rule has fired.

## Async rule execution

Fire each match asyncronously as it matches.
[code]
    onMatch + { asyncFire( match ); }  
    
[/code]

## Manual Interaction Agenda

Because the listeners are now fully pluggable and whether a rule fires or does not, or is cancelled is fully pragmatic it is possible to just expose the Module via an interactive GUI and the end user can see the conflict set and specify which rule(s) to fire.

As WME actions occur the users GUI will be updated showing the active matches, however none will fire without user selection. This means the user can interrogate the state of each Match and the fact it contains to select whch rules to fire. The user can also see dormant matches and “refresh” them so they can become available for firing again.

This could be taken a step further where a user sees a dash board of modules and all are inactive and the user can manually activate modules they wish to see evaluated.

## Simulating existing rule execution behviours

## activation-group plus variance

Other rule attribute behaviours can be implemented by combining listeners, although listener order is obviously important. For instance this listener can be added AFTER the agenda listener, and it simulates the existing “activation-group” behaviour, such that only the first activation fires for a conflict.  
activation-group
[code]
    onMatch += {   
     module.cancel(); // cancels all other matches  
    }
[/code]

We could do a variance on this that fires the first 3 activations, and cancels the rest
[code]
    onEnter += { count = 0 } // count is a module member variable  
    onMatch += {   
     if ( count++ == 3 ) {        
          module.cancel(); // cancels all other matches    ]  
     }  
    }
[/code]

## ruleflow-group

ruleflow-group behaviour is very simple to simulate. jBPM injects a trigger member variable, that on exit calls telling jBPM to trigger the next nodes in the flow, which may be ruleflow-group nodes or other jBPM nodes
[code]
    onEmpty { module.stop() } // stopping the module causes onExit to fire  
    onExit + {  
     node.triggerCompleted()  
    }  
    
[/code]

## agenda-groups

agenda-groups implement a push/pop stack behaviour. Only the stack tip executes, the others are considered “halted”. To acehive this the consequence of any rule needs to call the following three methods:
[code]
    module1.halt();  
    module2.onExit += { module1.resume() };  
    module2.call();  
    
[/code]

So that halts the current module and executes “pushes” the next module, when that module finishes “pops” the caller is resumed.

Simulating agenda-filters  
If a match is cancelled, and made dormant it is not propagated to the next listener in the onMatch event.
[code]
    onMatch += {  
     if ( <boolean expr> ) {  
         module.cancel( match );  
     }  
    }
[/code]

## Events as facts

Events are also inserted as facts, so can be matched in rules too. Member variables are fields on the events
[code]
    rule  activationGroupVariance when   
     m : OnMatch( count < 3 )  
    then   
    m.count++  
    end  
    
[/code]

## Parent Modules and Module Scoping

Modules can contain sub modules, they can ony be called from within the scope of the parent module.Sub modules will have access othe parent modules member variables and parameter variables.

## Module Reuse and Extension

A module can extend other modules. The exact semantics of this will need a lot more extensive though, but i’ll outline something to get started. When a module extends another module it effectively copies the definitions of all the contained rules.However those rules will match and fire completely indepedantly of the source.

## Macro’s to abstract module configuration

All this manual configuration would become very cumbersome to the end user, and potentially far too complex. The idea is that all the above complexity is for power users, this is then encapsulated via macro’s for end users. I don’t intend to outline a Macro system for Drools yet, as that is a different subject in itself and will need a lot of though. For now I’ll use <macro “name”>, pontentially these can be listed. But how macro’s are defined and applied are completely open to debate. These macro’s are then expanded at complie time to provide all the required listener behaviour:
[code]
    Module xxxx   
    macro activationGroup( "g1" )  
      
    module xxx   
    macro agenda module xxx   
    macro agenda activationGroup( "g1 )  
      
    module xxx   
    macro default
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fdrools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html&linkname=Drools%20%3A%20A%20Journey%20towards%20a%20Meta%20Framework%20for%20Hybrid%20Reasoning%20Systems> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fdrools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html&linkname=Drools%20%3A%20A%20Journey%20towards%20a%20Meta%20Framework%20for%20Hybrid%20Reasoning%20Systems> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fdrools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html&linkname=Drools%20%3A%20A%20Journey%20towards%20a%20Meta%20Framework%20for%20Hybrid%20Reasoning%20Systems> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fdrools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html&linkname=Drools%20%3A%20A%20Journey%20towards%20a%20Meta%20Framework%20for%20Hybrid%20Reasoning%20Systems> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fdrools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html&linkname=Drools%20%3A%20A%20Journey%20towards%20a%20Meta%20Framework%20for%20Hybrid%20Reasoning%20Systems> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fdrools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html&linkname=Drools%20%3A%20A%20Journey%20towards%20a%20Meta%20Framework%20for%20Hybrid%20Reasoning%20Systems> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fdrools-a-journey-towards-a-meta-framework-for-hybrid-reasoning-systems.html&linkname=Drools%20%3A%20A%20Journey%20towards%20a%20Meta%20Framework%20for%20Hybrid%20Reasoning%20Systems> "Email")
  *[]: 2010-05-25T16:11:00+02:00