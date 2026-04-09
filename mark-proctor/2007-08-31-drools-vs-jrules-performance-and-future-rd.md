---
layout: post
title: "Drools vs JRules Performance and Future R&D"
date: 2007-08-31
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/08/drools-vs-jrules-performance-and-future-rd.html
---

We have had fantastic feedback on Drools 4.0.1, showing that we have real enterprise class performance.

One user just [reported](<http://www.mail-archive.com/rules-users@lists.jboss.org/msg02830.html>) on the mailing list that their application, that uses large number of field constraints (more than 4) in a pattern, is over 200x faster in Drools 4.0.1 than in 4.0.0 :)

Some of you may remember my previous blog titled [“JBoss Drools vs ILog JRules – an anecdotal story”](<http://blog.athico.com/2007/08/jboss-drools-vs-ilog-jrules.html>); where the user had 1300 rules executing in an high volume transaction environment. I’ve since had further feedback that even after guidance on optimising their JRules implementation, trying both “optimised” and”sequential” modes, that Drools out of the box using the same rules and data is 4 times faster than JRules’ best efforts. They have sent me the following results:

Summary  
---  
| Sequential| Rete  
Jrules| Drools| Jrules| Drools  
Average| 16.45| 3.53| 14.53| 3.71  
| | | |   
Difference  
Jrules/Drools| 5| 4  
  
Timings were based on making 1000 rule execution calls.

  * There are 5 data set, randomly selected for each rule execution call.
  * Each data set contains about 100 elements.
  * For each execution call, up to 100 rules would fire.
  * Same rule set containing 1219 rules (simple rules) was used for all execution calls.
  * For JRules, the same instance of IlrContext was used and reset after each call. For Drools, a stateless session was created from the same RuleBase and was discarded after each call.
  * I am using JRules 6.6.1, with JIT enabled and calling IlrRuleSet().optimize with hasherGeneration set and wmModifiedByCode unset.

Prior to “optimised” mode our standard Rete was 27 times faster than their standard Rete. JRules “optimised” mode optimises the network, where possible, to execute sequential and with a static agenda – it does not allow dynamic runtime rule additions to the rulebase.

Sequential (seconds)| | Drools  
---|---|---  
Jrules| Drools| | Jrules| Drools  
16.04| 3.44| | 95.85| 3.5  
| | | |   
16.035/3.440 = 5| | 95.852/3.500 = 27  
  
I must stress that this is just one users story and the information is provided anonymously, thus making it anecdotal, and other users mileage may vary :) But I tell you the story as is, engineer to engineer, with no slight of hand and we have done nothing to help them “tweak” Drools further than any other user gets out of the box. The academic, open and transparent nature to Drools ensures an openness in these sorts of discussions. To be balanced the author said Drools consumed a lot more memory during rule serialisation of rules than JRules. This is due to our reliance on Java serialisation which is not very efficient with graphs and storing byte[]s for class generation in memory, we will address this in the future. We did however consume less memory during runtime execution. Further to that Drools’ management system needs to mature more, before a completion transition:  
“The top reasons for us to select Drools over JRules is not performance: the #1 is the open API’s that allows us to do what is required, #2 is the active community and the support. Exceptional performance is #3, but may gain more weight when time to convert existing projects. I believe both will exist in our company for the near future until Drools’ management system matures.”

To wet everyone’s appetite I have detailed our future performance R&D to show that we are not done yet.  
  
Lazy latch nodes  
Parent nodes do not propagate unless there is something to join against in the child node. For small systems this has little impact, but for large, wide, systems it can save memory and provide an increase in performance.

Network disconnection for RuleFlow Groups and Agenda Groups  
When data is asserted into the network all patterns for all rules are evaluated, regardless of whether that rule is able to fire. If a rule is not in a ruleflow-group or agenda-group that is currently in focus and active it should be disconnected from the network at the attachment points where there is no node sharing. For truly large systems it should also be possibly to page those detached rules to disk, until their ruleflow-group and/or agenda-group has the focus and is active.

Partial Network Paging to Disk  
For really large networks it may be desirable not to have the entire network in memory. Instead the network can be paged to disk, and will only page into memory when data attempts to propagate to that part of the network. This can be applied to the “Network Disconnection” optimisation to page out entire ruleflow-groups and agenda-groups when they are not in-focus and not active. Java serialisation is not very efficient, especially for graphs, so this would need to be combined with a custom wire protocol for marshalling.  
Lazy Latch Querries  
For queries with no parameters we can add the DroolsQuery pattern to the end of the network for that Rule, instead of the beginning. We then find either the last unshared node or the root beta node and put in a “block” semaphore, that means no data will propagate that is specific to the query rule. When the DroolsQuery object is propagated to the JoinNode it signals the “block” semaphore to propagate all its data. This allows queries to share with existing rule data.

No Memory storage for Querries  
As querries are effectively stateless we do not need to store any left input memory for the join nodes. The root part of the query should mark the Tuple as not requiring left input memory storage, so that left memory is not used during propagation. This increases query performance and uses less memory. We may even be able to modify sequential mode so that they both use the same technique to avoid left memory storage.

Isolation and Sharing of the Right Input for a BetaNode  
Currently we either share, or or do not share, a whole beta node dependant on whether the entire parent chain is identical. If we can isolate the right input a little more we can, in some situations, allow sharing of that right input. Those situations would be where there is either no indexing, or the indexing is the same, for the beta node. Further to this, for situations with no indexing, we could probably look to just use the parent node as also the right input node. This reduces memory usage and slightly less needed network propagations.

Composite index Alpha Node Hashing  
We already have composite index hashing for beta nodes, to a maximum depth of three columns. currently alpha node indexing only works on the a single literal value, composite would allow us to index multiple literal constraints combinations, again a maximum depth would need to be provided to avoid this becomes too expensive. Further to this there may be times when single indexing is preferably, as this is based on literals whether to composite or single should be deterministic at compile time, based on some level of cost analysis.  
Node Collapsing  
Currently each alpha node constraint is in it’s own node, this is needed for dynamic rulebases where rules can be attached at a later date. If we know the rulebase is not going to change, like with stateless sessions, we can collapse similar shared node groups into single execution units; most likely with optional bytecode JIT. For standard Rete execution we will need a property, or method call, for the user to state the rulebase will not change so we can apply this optimisation.

Alpha Node Reordering  
Alpha nodes can be re-ordered to maximise node sharing, this will make “Node Collapsing” optimisations even more efficient. Again we would need some indicator that the RuleBase building is complete and that the optimisation can now be applied.  
Closed World Assumptions  
Allow some data to be marked as “closed world”. This means the data will only ever be created inside of the working memory. This way we can analyse the rules and handle the life cycle of the data and allow us to auto-unpropagate it back to the object type node when we know it will have no further impact on resulting conflict sets. This reduces the size of the working memory network and the number of wasteful cross product attempts.

Network Re-Writing via Analysis  
I haven’t put too much thought into this one, but it must be possible to recognise some patterns where the network can be re-organised to provide better execution, by failing the propagation earlier on. This is similar to network eager-filtering, where we can stop certain facts propagating at an earlier stage in the network, than the join later in the network dictates.

Sub-System threading  
While this won’t address parallel execution and evaluation of a rule engine (which I consider a very large R&D effort and out of scope for this blog, which focuses on low hanging fruit), it should be possible to identify some sub systems that would benefit from execution in their own thread, without too much complexity – the Agenda sub system is an idea candidate for this.

Whole Bucket Joining  
I’m not entirely sure how or if this would work, but the basic idea is instead of joining each tuple with each fact on the right input to form a new tuple, the tuple instead just references the bucket for the matching index for the constraints. The actual tuple joining is delayed until we reach the terminal node, where those buckets are evaluated. We may only be able to apply this to some limited situations, but it will avoid a lot of wasted cross product join attempts if we can make it work.

Indexing for Number Ranges  
Indexing number ranges is really only useful for environments where the data doesn’t change that often, otherwise the re-balancing of the data structure can outweigh the benefits of indexing. For this reason it will probably need to be combined with some ability to annotate field constraints with the desire to apply the indexing for number ranges.

Reduce the Number of Generated Classes  
For the Java dialect we currently generate a single Class for all the expressions and blocks in that rule. However, due to the need to use interfaces in the engine, we generate an Invoker Class for each expression and block, to allow the engine to call that expression or block via the interface. We can instead provide an integer index value per expression and block and allow that integer to be passed via the invoker interface. This means we can generate a single class that implements all expression and block interfaces using the integer value to determine which expression or block we actually call. A single switch statement can be used to determine this, which should have no noticeable impact on execution. This should also mean faster building times as less classes have to be resolved.