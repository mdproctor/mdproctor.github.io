---
layout: post
title: "Sequential Rete"
date: 2007-07-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/sequential-rete.html
---

Stateless and Stateful Sessions

With Rete you have a stateful session where objects can be asserted and modified over time, rules can also be added and removed. Now what happens if we assume a stateless session, where after the initial data set no more data can be asserted or modified (no rule re-evaluations) and rules cannot be added or removed? This means we can start to make assumptions to minimise what work the engine has to do.

Algorithm  

  1. Order the Rules by salience and position in the ruleset (just sets a sequence attribute on the rule terminal node).
  2. Create an array, one element for each possible rule activation; element position indicates firing order.
  3. Turn off all node memories, except the right-input Object memory.
  4. Disconnect the LeftInputAdapterNode propagation, and have the Object plus the Node referenced in a Command object, which is added to a list on the WorkingMemory for later execution.
  5. Assert all objects, when all assertions are finished and thus right-input node memories are populated check the Command list and execute each in turn.
  6. All resulting Activations should be placed in the array, based upon the determined sequence number of the Rule. Record the first and last populated elements, to reduce the iteration range.
  7. Iterate the array of Activations, executing populated element in turn.
  8. If we have a maximum number of allowed rule executions, we can exit our network evaluations early to fire all the rules in the array.

The LeftInputAdapterNode no longer creates a Tuple, adding the Object, and then propagate the Tuple – instead a Command Object is created and added to a list in the Working Memory. This Command Object holds a reference to the LeftInputAdapterNode and the propagated Object. This stops any left-input propagations at assertion time, so that we know that a right-input propagation will never need to attempt a join with the left-inputs (removing the need for left-input memory). All nodes have their memory turned off, including the left-input Tuple memory but excluding the right-input Object memory – i.e. The only node that remembers an assertion propagation is the right-input Object memory. Once all the assertions are finished, and all right-input memories populated, we can then iterate the list of LeftInputAdatperNode Command objects calling each in turn; they will propagate down the network attempting to join with the right-input objects; not being remembered in the left input, as we know there will be no further object assertions and thus propagations into the right-input memory.

There is no longer an Agenda, with a priority queue to schedule the Tuples, instead there is simply an array for the number of rules. The sequence number of the RuleTerminalNode indicates the element with the array to place the Activation. Once all Command Objects have finished we can iterate our array checking each element in turn and firing the Activations if they exist. To improve performance in the array we remember record the first and last populated cells.

The network is constructed where each RuleTerminalNode is given a sequence number, based on a salience number and its order of being added to the network.

Data Structures  
Typically the right-input node memories are HashMaps, for fast Object retraction, as we know there will be no Object retractions, we can use a list when the values of the Object are not indexed. For larger numbers of Objects indexed HashMaps provide a performance increase; if we know an Object type has a low number of instances then indexing is probably not of an advantage and an Object list can be used.

Everything to the above paragraph is in JBoss Rules 4.0, the following sections are idea for the future, and thus still a bit vague at the moment.

If there is a huge number of rules a indexed paged direct address table can be used in place of the array that holds the resulting Activations. Here we create pages of arrays, we create further index points to pages at regular points in the range. The page can indicate if any of its elements are populated or not, allow us to skip iterations of those elements.

Collapsing Nodes, Code Generation and Node Ordering  
Stateful Rete can have nodes added and removed, for this reason to maximum node sharing we tend to have an AlphaNode per literal constraint. However as we know we will not have any more rules added we can collapse shared nodes into a single evaluation. If we have a chain of 3 AlphaNodes A, B and C. where A and B are shared and C isn’t. We can collapse A and B into a single node and generate code to do the multiple evaluations natively. Node ordering can be changed to maximise sharing and thus the impact of Collapsing them. There may also be some level of beta node collapsing we can do, but I have’nt given that side much thought yet.

Exploiting Multi-Threading  
In normal Rete exploiting multiple threads is hard, as you never know if a Tuple is going to enter the left-input or an Object is going to enter the right-input – i.e. reads and writes can happy simultaneously, the effect of adding locks to control this is expensive and past research has shown the costs are more than using lock free single thread approach. However with our sequential approach we know that the writes will always happen at different time to the reads. All writes happen during the first stage where objects are propagated to the right input nodes. All reads happen during Tuple propagation from the LeftInputAdapterNode. We can exploit this to execute parallel threads for each stage; using concurrent collection structures. We only have handle the synchronisation of the two stages – i.e. knowing when the all the Object propagations are finished and knowing when all the Tuple propagations are finished. Executing the actual rules in parallel is a little harder as we cannot easily know the user intention of the sequence. An attribute can be used to execute groups of rules that can be executed in parallel; those rules and groups must be specified in chronological order. i.e. If group A is to fire before group B, then all the rules for group A must be specified first. Or the execution order for the groups can be specified seperately, allowing rules to be more free formly tagged with the attributes.