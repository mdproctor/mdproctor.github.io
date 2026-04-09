---
layout: post
title: "Slot Specific and Refraction"
date: 2010-07-31
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/07/slot-specific-and-refraction.html
---

Slot Specific and Refraction are two techniques to help with recursive loop problems when writting rules. Drools currently implements neither.

Refraction  
Refraction has been around a long time and was part of the original LEX and MEA conflict resolution strategies. When a rule + fact[] fires the set of facts that make up the rule continue to be true. When the fields for an existing set of facts are changed any rules that fact[] have previously fired against are not re-added to the agenda for firing. Simply put a rule cannot refire for any give set of data regardless of whether the set of data is modified by the current rule or other rules. However if a modification to the fact[] stops it being true for a given rule and then later the fact[] becomes true again for that rule it can now be refired.  
The OPS5 manual on refraction:

http://www.math-cs.gordon.edu/courses/cs323/OPS5/ops5.html

```sql
REFRACTION        This term comes from the neurobiological observation of a refractory       period for a neuron, which means that the neuron is not able to fire       immediately without first going through a relaxation process.  In a       similar way, OPS5 will not allow the same instantiation in the conflict       set from firing twice in a row.  This prevents the inference engine from       entering into an infinite loop.
```

Refraction is supported in OPSJ and JRules, however it is not supported in Drools, Clips or Jess (please correct me if i’m wrong).

Slot Specific  
Jess also recently introduced “slot-specific” as an alternative way of dealing with recursive looping. You can read a thread here on “slot-specific” and refraction in Jess, <http://www.mail-archive.com/jess-users@sandia.gov/msg05488.html>. Slot specific means a pattern will only propagated facts for fields that are changed which it constrains on. This means you can modify a value in the consequence and if the rule does not constrain on that field it will not refire. Clips COOL (Clips Object Oriented Language) has this feature (but not deftemplates) as default for all fields of an Object. However “slot-specific” is not implemented in Drools, JRules or OPSJ (please correct me if i’m wrong).

Refraction + Slot-Specific + onChange  
I think there are advantages and disadvantages to each idea and I’ve been trying to think of better ways to deal with recursion in Drools and realised the two can be used together.

In Drools 6.0 I propose refraction to be the default behaviour for the engine, so no rules that have fired and still true can be reactived from a modify without first being made false. However “slot-specific” can override this allowing a pattern to react to changes on specific fields. With “Differential Diff”, previous called “True modify” refraction is trivial to support. A performant slot specific implementation will not be trivial, especially with our support for nested accessors.  
<http://blog.athico.com/2010/03/drools-halves-memory-use-with-new-true.html>  
<http://blog.athico.com/2010/01/rete-and-true-modify.html>

I propose “onChange” property listeners as a mechanism to specify which slots can receive modification updates. “onChange” would be a magical field supported in patterns that specifies whether a pattern listens to and propagates changes, “onChange” would give us “slot-specific” type semantics but with more user control and flexability. It takes an array of field names, here are example semantics:

Person( onChange == [name]) // listen to any “name” property changes, if “name” is changed then propagate, other property changes will not be propagated.  
// Notice we don’t need quotes as property names never have spaces

Person( onChange == [name, age, location]) // listens and propagates “name”, “age” and “location” changes.

Person( onChange == [*] ) // listen to all properties and propagates, this is the behaviour of current Drools.

Person( onChange == [!name, *]) // listen to all properties except “name”.

Person( onChange == [name, *]) // is allowed but obviously redundant

Person( onChange == [name, !name, *]) // is not allowed

All in all onChange allows the user to take advantage of slot-specific and refraction qualities, while not locking the user into either. I’ve also previously discussed constraining on previous values of a field, which would give even more fine grained control.  
Field Versioning  
There are times when you need to compare between current and previous values of a field, users can do this now by intermediary facts; i.e. inserting an Event to represent the before and after value for a field change, but it’s a little clunky. Intead we can provide built in support for this into the language, using an @ver(int) attribute. The idea is that Drools would store previous values, only on demand, so you only pay the cost if you use this feature. The value for @ver is an effective “diff” value counting backwards starting from 0, which is now. So @ver(0) is the current field value, @ver(-1) is the previous field value @ver(-2) is the value 2 versions ago.

SomeFact( fieldName != fieldName @ver( -1 ) )

So any field with no @ver is effectively, and you could write it as such, @ver(0)  
SomeFact( @ver(0) fieldName != fieldName @ver( -1 ) )

We can allow bindings to previous versions:  
SomeFact( $var : @ver(-2) fieldName )  
OtherFact( field == $var )

We should also support the ability to add a range of values to a list, for processing with accumulate:  
SomeFact $list : @var(0….-5) fieldName )