---
layout: post
title: "Project Idea: Debug Helper"
date: 2012-01-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/01/project-idea-debug-helper.html
---

Have a great project for any intrepid rule exlorers. The project itself is not too difficult and will make it really easy for people to get an idea for what is going on inside of the engine. The below is an early concept idea sketched out, don’t take it as a spec to be rigidly followed :) You know where to find us if you want mentoring on this task:  
<http://www.jboss.org/drools/irc>

While the rule itself is named, patterns are not. By allowing patterns themselves to take on ids, we can specify capture points. This is already possible for rule terminal nodes via listeners for rule activation, but users would still need to write their own handlers. The proposal here is to write a utility that will capture propagations during a given start/stop period that users can later inspect for both activations and join attempts. This will allow users to know exactly what is happening underneath.

Blow shows a rule with 3 potential capture points:

```
package pkg1

rule r1 when then
   Person( name == "xxx" ) @id(p1)
   Location( name == "xxx" ) @id(l1)
then
end
```

1) The terminal node, via the rule name.  
2) p1  
2) l1

The idea is to be able to turn on monitor, that has a start(), stop() and clear() methods. When started it will capture the insert, update, retract propagations. Further it should be possible to write assertion utility to assert on the state of the captured information.

When capture is turned on for a given capture point it will record a List of instances. As different nodes have different data, there is a base node and a child node. Every time a propagation happens an instance is created and added to the montior representing the current state.

```text
BaseCapture
   NodeType nodeType       // enum for join, exists, not etc to allow  for casting to correct node
   String nodeName           // enum for join, exists, not etc
   Collection
 rules   // Rules is a collection, as the node  might be shared
   Activation activation      // Activation at the root of the WM  operation (may be null, if the acion came from outside of the wm).
   FactHandle[] f                // fact at the root of the working  memory operation
   FactHandle[] fh              // fact[] that entered the node

JoinCaptire extends BaseCapture
   Direction direction              // Left/Right enum
   FactHandle[] successJoins // the opposite fact handles that were  successfully joined with, during this montioring session
   FactHandle[] failedJoins    // the opposite fact handles that were  unsuccessfully joined with, during this monitoring session.
                                                //Note if the  propagation was from the left the join arrays will all be an length of 1.
RulePropagation extends BasePropagation
   RuleStatus status        // Matched, UnMatched, Fired
```

For example lets say I want to monitor the propagations on l1 and r1, that happens during two working memory actions. I can do the following:

```text
ksession.insert( new Person("darth"));
fh = ksession.insert( new Location("death star));
NodeMonitor l1monitor = ksession.getMonitor("pkg1/r1/l1")
NodeMonitor r1monitor = ksession.getMonitor("pkg1/r1")
l1monitor.start();
r1monitor.start();
ksession.insert( new Person("yoda));
ksession.retract( fh );
l2monitor.start();
r2monitor.start();

List props = l1monitor.getResults(JoinCapture.class);
List props = r1monitor.getResults(RuleCapture.class);
```

l1monitor will show left propagation for yoda and a successful join for death star  
r1 will have two entries. It will show a match (activation creation) but it will also show an unmatch, due to the retract.