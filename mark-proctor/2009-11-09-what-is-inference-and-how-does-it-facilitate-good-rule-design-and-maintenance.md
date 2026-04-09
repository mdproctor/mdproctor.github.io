---
layout: post
title: "What is inference and how does it facilitate good rule design and maintenance"
date: 2009-11-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/11/what-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html
---

Inference has a bad names these days, as something not relevant to business use cases and just too complicated to be useful. It is true that contrived and complicated examples occur with inference, but that should not detract from the fact that simple and useful ones exist too. But more than this, correct use of inference can crate more agile and less error prone businesses with easier to maintain software.

So what is inference? Something is inferred when we gain knowledge of something from using previous knowledge. For example given a Person fact with an age field and a rule that provides age policy control, we can infer whether a Person is an adult or a child and act on this.

```drl
rule "Infer Adult"
when
$p : Person( age >= 18 )
then
insert( new IsAdult( $p ) )
end
```

So in the above every Person who is 18 or over will have an instance of IsAdult inserted for them. This fact is special in that it is known as a relation. We can use this inferred relation in any rule:

```
$p : Person()
  IsAdult( person == $p )
```

In the future we hope to improve our language so you can have special handling of known relation facts, so you can just do following and the join is implicit:

```
Person() IsAdult( )
```

So now we know what inference is, and have a basic example, how does this facilitate good rule design and maintenance?

Let’s take a government department that are responsible for issuing ID cards when children become adults, hence forth referred to as ID department. They might have a decision table that includes logic like this, which says when an adult living in london is 18 or over, issue the card:  
[![](/legacy/assets/images/2009/11/3f7f7b6e04cb-monolithic.png)](</assets/images/2009/11/a71c833dee76-monolithic.png>)

However the ID department does not set the policy on who an adult is. That’s done at a central government level. If the central government where to change that age to 21 there is a change management process. Someone has to liaise with the ID department and make sure their systems are updated, in time for the law going live.

This change management process and communication between departments is not ideal for an agile environment and change become costly and error prone. Also the card department is managing more information than it needs to be aware of with its “monolothic” approach to rules management which is “leaking” information better placed else where. By this I mean that it doesn’t care what explicit “age >= 18” information determines whether someone is an adult, only that they are an adult.

Instead what if we were to split (de-couple) the authoring responsibility, so the central government maintains its rules and the ID department maintains its.

So its the central governments job to determine who is an adult and if they change the law they just update their central repository with the new rules, which others use:  
[![](/legacy/assets/images/2009/11/df4ad387836c-InferIsAdult.png)](</assets/images/2009/11/827be3f38cad-InferIsAdult.png>)

The IsAdult fact, as discussed previously, is inferred from the policy rules. It encapsulates the seemingly arbitrary piece of logic “age >= 18” and provides semantic abstractions for it’s meaning. Now if anyone uses the above rules, they no longer need to be aware of explicit information that determines whether someone is an adult or not. They can just use the inferred fact:  
[![](/legacy/assets/images/2009/11/36d1d3619a6c-IssueIdCard.png)](</assets/images/2009/11/8da9e0847894-IssueIdCard.png>)

While the example is very minimal and trivial it illustrates some important points. We started with a monolithic and leaky approach to our knowledge engineering. We create a single decision table that had all possible information in it that leaks information from central government that the ID department did not care about and did not want to manage.

We first de-coupled the knowledge process so each department was responsible for only what it needed to know. We then encapsulated this leaky knowledge using an inferred fact IsAdult. The use of the term IsAdult also gave a semantic abstraction to the previously arbitrary logic “age >= 18”.

So a general rule or thumb when doing your knowledge engineering is:

Bad

  * Monolithic
  * Leaky

Good

  * De-couple knowledge responsibilities
  * Encapsulate knowledge
  * Provide semantic abstractions for those encapsulations