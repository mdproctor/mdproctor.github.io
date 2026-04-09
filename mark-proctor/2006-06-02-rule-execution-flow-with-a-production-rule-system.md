---
layout: post
title: "Rule Execution Flow with a Production Rule System"
date: 2006-06-02
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/06/rule-execution-flow-with-a-production-rule-system.html
---

Some times workflow is nothing but a decision tree, a series of questions with yes/no answers to determine a final answer. This can be modelled far better with a Production Rule System, and is already on the Drools road map.

For the other situations we can use a specialised implementation of Agenda Groups to model “stages” in rule engine execution. Agenda Groups are currently stacked, like Jess and Clips modules. But imagine instead if you could model linear Agenda Group execution – this is something I have been thinking about for a while to allow powerful and flexible modelling of processes in a Production Rule System. A successful implementation has clear advantages over two separate engines – as there is an impedance mismatch between the two. While there is little issue using a rule engine with workflow, using workflow to control linear execution of a rule engine will very suboptimal – this means we must seek a single optimal solution for performance sensitive applications.

Let’s start by calling these special Agenda Groups “nodes”, to indicate they are part of a linear graph execution process.

Start rules don’t need to be in a node and resulting target nodes will detach and evaluate once this rule has finished:

```drl
rule "start rule"
    target-node "<transition>" "<name>"     
  when
    eval(true)
  then
     // assert some data
end
```

The start rule and the nodes can specify multiple target nodes and additional constraints for those target nodes; which is explained later. The start rule can fire on initialisation, using eval(true), or it could have some other constraints that fire the start rule at any time during the working memory life time. A Rule Base can have any number of start rules, allowing multiple workflows to be defined and executed.

The start rule dictates the next valid target-nodes – only activated rules in these nodes can fire as a result of the current assertions. While the activated rules in other nodes will not be able to fire, standard rules and Agenda Groups will react, activate and fire as normal to changes in data.

A node rule looks like a normal rule, except it declares the node it’s in. As mentioned previously a node can contain multiple rules; but only the rules with full matches to the LHS will be legible for firing:

```drl
rule "rule name"
    node "<name>"   
  when
    <LHS>
  then
     // assert some data
end
```

There is an additional node structure, which the rules are associated with, and specifies the resulting targets:

```drl
node "node name"
    target-node "<transition>" "<name>"     
end
```

Target nodes are only allowed to evaluate their activated rules once the previous start rule has finished or the previous node is empty because it has fired all its rules. Once a node is ready to be evaluated, we “detach” it and then spin it off into its own thread for rule firing, all resulting working memory actions will be “queued” and assert at safe points, so Rete is still a single process. Once a node is detached the contained rules can no longer be cancelled, they must all fire – further to this no further rules can be added. All our data structures are serialisable so suspension/persistence is simply a matter of calling a command to persist the detached node off to somewhere.

As well as a rule specifying the LHS constraints for it to activate, the previous node can specify additional constraints. A rule can be in multiple nodes, so if two incoming nodes specify additional constraints they are exclusive to each other – in that the additional constraints of the non current incoming node will have no effect:

```xml
node "node name"
    target-node "<transition>" "<name>" when
        <additional constraints>
    end
end
```

Further to this a node can specify multiple targets each with its own optinonal additional constraints. Sample formats are showing below:

```xml
node "node name"
    target-node "<transition>" "<name>"

    target-node "<transition>" "<name>" when
    end

    target-nodes "<transition>" "<name>" 
                 "<transition>" "<name>"
                 "<transition>" "<name>"
 
    target-nodes "<transition>" "<name>" 
                 "<transition>" "<name>"
                 "<transition>" "<name>" when
    end
end
```

Further to this we need additional controls to implement “join nodes” and to also allow reasoning to work with both the transition name as well as the node name.

This highlights the basics for linearly controlled execution of rules within a Production Rule system. It also means we can model any BPM process, as it’s now a simplified subset, but allow it to be done in a highly scalable way that integrates into very demanding tasks. Further to this we can still have standard agenda groups and rules that fire as a result of data changes. This provides for a very powerful solution that is far more powerful than the simple subset that most workflow solutions provide.