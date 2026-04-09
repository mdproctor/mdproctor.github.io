---
layout: post
title: "Life Beyond Rete - R.I.P Rete 2013 :)"
date: 2013-01-02
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2013/01/life-beyond-rete-r-i-p-rete-2013.html
---

I’m just putting the final touches onto my new algorithm. It merges concepts from [Leaps](<http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.8595>), [Collection Oriented Match](<http://teamcore.usc.edu/papers/1993/cikm-final.pdf>) and [Left/Right unlinking](<http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.6246>), as well as a few ideas of my own. The code is committed, but I’m just getting accumulate to work and writting some more tests. I’ll do a full blog in a week or so, writting about it in more detail, hopefully accompanied with an alpha for people to play with.

The algorithm addresses the greedy and wasteful nature of Rete. This will make it suitable for more constrained environments, such as mobile devices, or browsers if we do a JS port with GWT. Further it’s been designed with multi-core utilisation in mind – although I haven’t implemented that yet.

For those with an understanding of the terminologies, here is a bullet point list of what I’ve done so far.

**Rule unlinking**

  * With segments to preserve sharing. Bit masks used for right input and segments, for efficient checking.
  * A Segment has it’s bit set, when all right inputs have their bit set.
  * A rule is linked in, when each segment has it’s bit set.
  * No beta evaluation happens until a rule is both fully linked in an popped of the agenda (see lazy rule evaluation) 
  * A linked rule can be unlinked, when any of right inputs has no data
    * All full and partial join data is preserved.
      * avoids re-calculation when rule is re-linked
      * Stops further wasted join attempts until the rule is likely to fire
    * GC algorithm is needed, so joins can be removed from memory if not used for some time.
  * I suspect we could use arc consistency to further delay when a bit is set, rather than simple the existing of a right input

**Lazy rule evaluation**

  * Rule’s beta network is not evaluated when linked. Instead it’s added to the priority queue, only when it pops do we evaluate it’s beta network

**Set Oriented propagations**

  * All insert, update and deletes are staged for the right inputs, until rule is evaluated. 
  * Beta network evaluation starts at the root 
    * All inset/update/delete’s are processed together resulting in a set of tuples to be propagated to the next node 
    * The set of tuples has separate lists for inserted, updated, deleted tuples. 
  * Ensures course grained node evaluation, ideal for multi-core scheduling.
  * Single pass propagation, instead of typical Rete which depth search thrashes the network. 
  * Note we do not yet do collection oriented match, which collapses the match space in a node.
    * While we borrowed the collection propagation concept, the defragmentation process of collection oriented match needs a lot more thought, as it has downsides. 
    * While not done yet, we will now be able to support set oriented executions, as well as propagations. Ideas for this are outlined here, <https://community.jboss.org/wiki/RuleExecutionSemantics>, inspired by [DADO](<http://academiccommons.columbia.edu/catalog/ac%3A145022>).

**Modify in place/Differential Update**

  * Modifies are real, instead of a retract + assert 
  * Allows for compensation “undo” actions, as we know what really was deleted and what was updated. 
  * Preserves objects, to avoid GC hit.

**Property Reactive**

  * Patterns can listen and react to specific property changes
    * Think of it as a property change listener, rather than the current class change listener
    * Defaults to listen to constrained fields, users may override what they do or don’t listen to.
    * Uses bit masks to keep it efficient

**Tree based graphs**

  * Retracts simply need to iterate the graph 
  * Allows for efficient “modify in place”

**Subnetwork support**

  * not, exists, accumulates can supported nested groups and patterns 
  * Is supported as part of the single pass network evaluation 
    * Our tuple set reaches the left input, and then recursively evaluates the subetnworks(s). This then eventually results in a single set of tuples again, which is applied to our current node, resulting in a single set to propagate to the child.

While not complete, here are some TODO items I can think of, to give an idea of near and longer term ideas:

**More efficient sub-networking**

  * The new design allows for more efficient execution within subnetworks, but we have yet to take advantage of this.

**GC Joins**

  * Allow joins to be GC’d after a period of time, if they are not used, but also must support recreation while not invalidating the execution sequence of rules (i.e. a rule must not fire again, if it’s already fired)

**Different network topologies**

  * Rete network’s always join from left to right, this is not always efficient. [Treat](<http://www.aaai.org/Papers/AAAI/1987/AAAI87-008.pdf>) and [Gator](<http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.35.140>) networks look at how different topologies can reduce the number of join attempts, it can also improve sharing with our new segmentation based network.

**Multi-core work**

  * The design now is already queued based, and supports coarse grained units of work. We now need to start creating the thread model and better isolating and separating the alpha network propagation process. This involves refactoring our existing locking model.
  * Efficient testing of overlapping rules is needed – i.e does one rule share segment with another rule. This will allow us to evaluate rules, without sync points.

**Intelligent Linking**

  * At the moment linking is done by setting a bit, when a right input receives a single fact. Arc consistency can be used to further delay this linking process, only linking in a rule segment and also a rule, when arc consistency is achieved.

**MVCC and Transactions**

  * The propagation model should support Multi-Version Concurrent Control. This will be necessary to get better multi-core support, and it will enable transactions support.

**R.I.P.**

**RETE 2013 :)**