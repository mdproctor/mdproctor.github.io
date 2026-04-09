---
layout: post
title: "Goodbye Conflict Resolution Strategy, Hello Rule Dependency Meta Rules"
date: 2010-04-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/04/goodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html
---

I’ve added a new section to the [Drools Language Enhancement](<http://community.jboss.org/wiki/DroolsLanguageEnhancements>) ideas wiki page discussing meta-rules to help declaratively control rule ordering. Here is what I have so far, feedback welcome, you can find the original content [here](<http://community.jboss.org/wiki/DroolsLanguageEnhancements#Field_Versioning>).

## Rule Dependency Meta-Rule Language

When a terminal node is matched instead of adding the Activation to the agenda it inserts it into the WorkingMemory. We have a special builder that allows easy access to the contents.

All declarations are typed fields for the Activation fact, based on the “name” field. So the name field is mandatory. All FactHandles are available via an array accessor, which has type inference for the element being used. We also all bindings on the Activation fact to work this way too. Act is used for compactness, we’ll allow that to be optionally user defined:  
act1 : Act( someDeclaration == X, fact[0] == Y )  
act2 : Act( someDeclaration.value > act1.someDeclaration.value )

Normal facts can also be matched. The RHS of the rule is side effect free, you cannot modify or insert facts; this allows the RHS to execute as soon as it’s matched. What you can do is setup rule dependencies – where one rule blocks another:  
act1.blockedBy( act2 ).until( Fired )  
act1.blockedBy( act2 ).until( IsFalse )

We can even allow facts to block:  
act1.blockedBy( someFact )

This means the act1 activation is blocked until a rule executes:  
act1.unblockedBy( someFact )

We can probably add an override, something like:  
act1.unblockAll()

Only when an Activation is no longer blocked will it be placed on the Agenda as normal.

If an activation on the agenda has not yet fired and something attempts to block it, it will be removed from the agenda until it is no longer blocked.

For this to be effective, especially for large systems, it will need to be combined with design time authoring help.

This work will be eventually be combined with further enhancements to help with parallel execution, in resulting conflicts, see the “Parellel Meta-Rule Language” heading.

<

p style=”min-height: 8pt; height: 8pt; padding: 0px;”>