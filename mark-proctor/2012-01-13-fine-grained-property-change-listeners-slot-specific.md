---
layout: post
title: "Fine Grained Property Change Listeners (Slot Specific)"
date: 2012-01-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/01/fine-grained-property-change-listeners-slot-specific.html
---

Mario just got a first cut working for fine grained property change listeners. Previously when you call update() it will trigger revaluation of all Patterns of the matching object type in the knowledeg base.

As some have found this can be a problem, forcing you to split up your objects into smaller 1 to 1 objects, to avoid unwanted evaluation of objects – i.e. recursion or excessive evaluation problems.

The new approach now means the pattern’s will only react to fields constrained or bound inside of the pattern. This will help with performance and recursion and avoid artificial object splitting. We previously discussed this here:  
<http://blog.athico.com/2010/07/slot-specific-and-refraction.html>  
You can see the unit test here:  
<https://github.com/droolsjbpm/drools/blob/ca55c78429cbc0f14167c604c413cdc3faaf6988/drools-compiler/src/test/java/org/drools/integrationtests/MiscTest.java>

The implementation is bit mask based, so very efficient. When the engine executes a modify statement it uses a bit mask of fields being changed, the pattern will only respond if it has an overlapping bit mask. This does not work for update(), and is one of the reason why we promote modify() as it encapsulates the field changes within the statement. You can follow Mario’s chain of work on this at his github activity feed:  
<https://github.com/mariofusco.atom>

The adventerous amoung you can pick this up from hudson, or from maven, and start playing now. My hope is that this will make drools much easier to use:  
<https://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/drools-distribution/target/>  
Btw we are after a name. Drools is not a frame based system, so “slot specific” doesn’t seem appropropriate. Property Specific seems a bit of a mouth full. I’m quite liking High Fidelity Change Listeners :) any other suggestions?

slot-specific is the name used by Jess for this feature, . It’s also the standard way that Clips COOL works, which is the Clips OO module. Although that’s partly a side effect of the triple representation of properties used in COOL, and the modifications are triple based. I don’t know what mechanism Jess is using to enable this.

Mark