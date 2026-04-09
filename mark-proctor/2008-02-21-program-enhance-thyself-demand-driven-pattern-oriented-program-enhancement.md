---
layout: post
title: "“Program, Enhance Thyself!” – Demand-Driven Pattern-Oriented Program Enhancement"
date: 2008-02-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/02/program-enhance-thyself-demand-driven-pattern-oriented-program-enhancement.html
---

Godmar Back has been relentless in the mailing list recently diving deep into Drools and shining a bright light on obscure bugs. Good work Godmar, keep it up – that which does not kill us, can only make us stronger :)

I’d also like to bring this paper written in collaboration by Dr. Eli Tilevich and Dr. Godmar Backto everyone’s attention. It’s a very interesting read on how Drools can be used to dynamically enhance classes using rules and aop (aspectj). I’ve taken the liberty of pasting the abstract and a section with some examples in it. enjoy.

[“Program, Enhance Thyself!” – Demand-Driven Pattern-Oriented Program Enhancement](<http://people.cs.vt.edu/~gback/papers/autoenhance-aosd2008.pdf>)

Program enhancement refers to adding new functionality to an existing program. We argue that repetitive program enhancement tasks can be expressed as patterns, and that the application of such enhancement patterns can be automated. This paper presents a novel approach to pattern-oriented automated enhancement of object-oriented programs. Our approach augments the capabilities of an aspect compiler to capture the programmer’s intent to enhance a program. In response to the programmer referencing a piece of functionality that is non-existent, our approach automatically synthesizes aspect code to supply the required functionality transparently. To improve flexibility and facilitate reuse, the synthesis and application of the new functionality is guided by declarative whenthen rules, concisely expressed using a rule base. Our extensible automated program enhancement system, called DRIVEL, extends the AspectJ compiler with aspect generating capabilities. The generation is controlled using the DROOLS rules engine. To validate our approach and automated tool, we have created a collection of enhancement libraries and used DRIVEL to apply them to the LibX Edition Builder, a large-scale, widely-used Web application. DRIVEL automatically enhanced the LibX Edition Builder’s XML processing modules with structural navigation capabilities and caching, eliminating the need to implement this functionality by hand.  
…  
…  
Below, the variable ’m’ is bound to any encountered ’InvalidMethod’ facts meeting the condition that the name of the missing method is “toStringLong.” AddToStringLong(m) returns an enhancement object, and the insert method adds it as a new fact into the working memory.

```drl
rule "Provide a toStringLong() aspect"
when
m : InvalidMethod ( methodName == "toStringLong" )
then
insert (Enhancements.AddToStringLong(m));
end
```

A second example shows how rules can be triggered even in the absence of compile time errors using annotations. The annotation @NaturalOrdering triggers an enhancement that adds a natural ordering to a class, allowing it to be used in java.util.* containers without requiring the use of a comparator.

```drl
rule "Provide a natural ordering"
when
t : Clazz ( annotations[’NaturalOrdering’] != null ) not ( Enhancements.HaveNaturalOrdering ( clazz == t ) )
then
insert (Enhancements.AddNaturalOrdering(t));
end
```

The ’not HaveNaturalOrdering’ construct prevents the application  
of this rule if the class already defines a natural ordering. Applying  
the enhancement will assert a “HaveNaturalOrdering” fact for the  
class that is being enhanced. If the class already provides a natural  
ordering via a compareTo method, a rule can add this fact as  
follows:

```drl
rule "Disallow natural ordering annotation if compareTo() is present."
salience 10when m : Method (name == "compareTo", signature == "(Ljava/lang/Object;)I")
then
insert(new Enhancements.HaveNaturalOrdering (m.getClazz()));
end
```

The ’salience 10’ argument gives this rule higher priority than the “Provide a natural ordering” rule, thereby ensuring that its antecedent is falsified before it fires, preventing the accidental application of the enhancement (which would result in a compile error).