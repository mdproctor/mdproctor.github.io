---
layout: post
title: "Drools : PHREAK Stack Based Evaluations and Backward Chaining"
date: 2014-01-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/01/drools-phreak-stack-based-evaluations-and-backward-chaining.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools : PHREAK Stack Based Evaluations and Backward Chaining](<https://blog.kie.org/2014/01/drools-phreak-stack-based-evaluations-and-backward-chaining.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 23, 2014  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

A while back I wrote a blog on our new algorithm.  
<http://blog.athico.com/2013/11/rip-rete-time-to-get-phreaky.html>  
Someone asked me about the new stack based system, and how backward chaining works. I replied to them in an email, but I thought others might find it useful, so have pasted it below. It’s written straight from my brain onto the page, so it’ a bit raw in places.; but I hope some find it useful, regardless.

—–

When a rule is evaluated, it evaluates from root to tip.

For each node it evaluates all possible joins and produces a tuple set. That child tuple set is then passed to the child node. The tuple set that is passed in is refered as the srcTupleSet (for variable name) then all the children are placed into the trgTupleSet. The trgTupleSet is passed to the child node, where it becomes the srcTupleSet.

Line 245 shows this loop  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/RuleNetworkEvaluator.java#L245>
[code]
    srcTuples = trgTuples; // previous target, is now the source
[/code]

When a node is entered it has a number of variables that are necessary to evaluate the node. The node id, the node memory, the segment memory, the srcTupleSet the trgTupleSet. Any node can be paused and resumed (evaluate at a later point in time) by creating a StackEntry that references these values. The StackEntry is placed onto the stack. Here is the StackEntry class:  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/StackEntry.java>

This is needed for 2 reasons, backward chaining and sub networks. Backward chaining is done via the query node.

When the propagation reaches a query node it needs to suspend the evaluation of the current rule – so it creates a StackEntry and places it on the stack.  
line 459 :[ https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/RuleNetworkEvaluator.java#L459](<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/RuleNetworkEvaluator.java#L459>)

A query is just a rule with no RHS, no consequence. It collects all the results that reach the terminal node and returns them to the caller. The query node allows a rule to invoke a query, passing in arguments. Invoking a query is done by inserting a DroolsQuery object, which matches the root pattern and triggers a propagation:  
see line 67; <https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/PhreakQueryNode.java>
[code]
    LeftInputAdapterNode.doInsertObject(handle, pCtx, lian, wm, lm, false, dquery.isOpen());
[/code]

Like prolog, arguments can be bound or unbound. A bound argument is an in-variable, and unbound argument is an out-variable. Implementation wise we do not apply constraints to unbound arguments. This allows for the classic prolog “transitive closure” type query. And while a rule can call a query, a query can also call a query (we don’t have tabling to detect infinite cycles).
[code]
    query isContainedIn( String x, String y )
      Location( x, y; )
      or
      ( Location( z, y; ) and isContainedIn( x, z; ) )
    end
[/code]

Note drools supports positional and slotted arguments in patterns. This is done by mapping all positions to a slot.

A step by step tutorial showing the above query in action, for reactive and non-reactive transitive closures, can be found here:  
<https://www.youtube.com/watch?v=fCjIRVSRFvA>

For the evaluating query, when the trgTulupleSet reaches the terminal node, it iterates and adds each tuple to the “collector”.  
see line 65: <https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/PhreakQueryTerminalNode.java#L65>

The collector creates a special child tuple, that can be added into the calling parent.  
see line 343: <https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/reteoo/QueryElementNode.java#L343>

Once the query has finished evaluating, it returns. The process of retuning then allows the execution to visit the stack, where it pops the StackEntry and resumes the evaluation – but now the query results are available.  
see lines 166 and 173: <https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/RuleNetworkEvaluator.java>

A query can be invoked reactively and non-reactively. Non reactively means there is no left memory and the query is not left open. Reactively means there is left memory and the query is left open. The reactive query is fully incremental and supports updates and deletes:  
see line 143 and 169: <https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/PhreakQueryNode.java#L143>

The data structures we use for tuples and “nested” (query result) tuples is efficient and “copy free” and “search free” – it’s all double linked lists. This was necessary to make incremental queries efficient.

Sub networks use a similar technique. At the point a subnetwork is reached, the outer rule is suspended (placed on the stack) and the inner network evaluation is created.  
see lines 593 and 604:  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/RuleNetworkEvaluator.java>

Once the subnetwork is finished, the outer rule resumes and places the results into the right input of the outer child node:  
line 662: <https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/phreak/RuleNetworkEvaluator.java#L662>

As previous mentioned currently we provide lazy rule evaluation, but not incremental rule evaluation. Once a rule evaluation starts, all tuples are produced. However as a stack entry can paused and resumed in any node, it could be used to provide incremental rule evaluation too – although we don’t do this now. In effect you “take” X number of objects on the right input – which could be 1 or 5 or 25 or 100. The number allows you to tune latency vs throughput. After a take if there are still un-evaluated right inputs, you create a StackEntry that forces re-evaluation of this node after the current propagation has finished.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F01%2Fdrools-phreak-stack-based-evaluations-and-backward-chaining.html&linkname=Drools%20%3A%20PHREAK%20Stack%20Based%20Evaluations%20and%20Backward%20Chaining> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F01%2Fdrools-phreak-stack-based-evaluations-and-backward-chaining.html&linkname=Drools%20%3A%20PHREAK%20Stack%20Based%20Evaluations%20and%20Backward%20Chaining> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F01%2Fdrools-phreak-stack-based-evaluations-and-backward-chaining.html&linkname=Drools%20%3A%20PHREAK%20Stack%20Based%20Evaluations%20and%20Backward%20Chaining> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F01%2Fdrools-phreak-stack-based-evaluations-and-backward-chaining.html&linkname=Drools%20%3A%20PHREAK%20Stack%20Based%20Evaluations%20and%20Backward%20Chaining> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F01%2Fdrools-phreak-stack-based-evaluations-and-backward-chaining.html&linkname=Drools%20%3A%20PHREAK%20Stack%20Based%20Evaluations%20and%20Backward%20Chaining> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F01%2Fdrools-phreak-stack-based-evaluations-and-backward-chaining.html&linkname=Drools%20%3A%20PHREAK%20Stack%20Based%20Evaluations%20and%20Backward%20Chaining> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F01%2Fdrools-phreak-stack-based-evaluations-and-backward-chaining.html&linkname=Drools%20%3A%20PHREAK%20Stack%20Based%20Evaluations%20and%20Backward%20Chaining> "Email")
  *[]: 2010-05-25T16:11:00+02:00