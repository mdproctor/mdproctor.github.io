---
layout: post
title: "Drools Inference and Truth Maintenance for good rule design and maintenance"
date: 2010-01-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/01/drools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html
---

Back in November I did a blog on inference and how it can be useful for rule authoring.  
[What is inference and how does it facilitate good rule design and maintenance](<http://blog.athico.com/2009/11/what-is-inference-and-how-does-it.html>)

The summary of this was:

  * De-couple knowledge responsibilities
  * Encapsulate knowledge
  * Provide semantic abstractions for those encapsulations

For my JUG in Lille I extended this example by including truth maintenance, to demonstrate self maintaining systems.

The previous example was issuing ID cards to over 18s, in this example we now issue bus passes, either a child or adult pass.

```drl
rule "Issue Child Bus Pass"
when
$p : Person( age
then
insert(new ChildBusPass( $p ) );endrule "Issue Adult Bus Pass"
when
$p : Person( age >= 16 )
then
insert(new AdultBusPass( $p ) );
end
```

As before the above example is considered monolithic, leaky and providing poor separation of concerns.

As before we can provide a more robust application with a separation of concerns using inference. Notice this time we don’t just insert the inferred object, we use “logicalInsert”:

```drl
rule "Infer Child"
when
$p : Person( age
then
logicalInsert( new IsChild( $p ) )endrule "Infer Adult"
when
$p : Person( age >= 16 )
then
logicalInsert( new IsAdult( $p ) )
end
```

A “logicalInsert” is part of the Drools Truth Maintenance System (TMS). Here the fact is logically inserted, this fact is dependant on the truth of the “when” clause. It means that when the rule becomes false the fact is automatically retracted. This works particularly well as the two rules are mutually exclusive. So in the above rules if the person is under 16 it inserts an IsChild fact, once the person is 16 or over the IsChild fact is automatically retracted and the IsAdult fact inserted.

We can now bring back in the code to issue the passes, these two can also be logically inserted, as the TMS supports chaining of logical insertions for a cascading set of retracts.

```drl
rule "Issue Child Bus Pass"
when
$p : Person( )       IsChild( person =$p )
then
logicalInsert(new ChildBusPass( $p ) );endrule "Issue Adult Bus Pass"
when
$p : Person( age >= 16 )       IsAdult( person =$p )
then
logicalInsert(new AdultBusPass( $p ) );
end
```

Now when the person changes from being 15 to 16, not only is the IsChild fact automatically retracted, so is the person’s ChildBusPass fact. For bonus points we can combine this with the ‘not’ conditional element to handle notifications, in this situation a request for the returning of the pass. So when the TMS automatically retracts the ChildBusPass object, this rule triggers and sends a request to the person:

```drl
rule "Return ChildBusPass Request "
when
$p : Person( )       not( ChildBusPass( person == $p ) )
then
requestChildBusPass( $p );
end
```