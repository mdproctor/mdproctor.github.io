---
layout: post
title: "RuleFlow Constraint Editor and Code Completion (includes screenshots)"
date: 2007-06-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/ruleflow-constraint-editor-and-code-completion-includes-screenshots.html
---

Code completion has just been added to the constraint editor for ruleflow ‘splits’ and ‘joins. ‘and’, ‘or and ‘xor’ type logic can be applied and the constraint used for each branch. The same constraint language is used as the left hand side (LHS) ‘when’ part of a rule, and that constraint monitors the Working Memory. When the ruleflow enters the ‘split’ or ‘join’ it is only true if that LHS for the Working Memory is true. This provides extremely powerful Ruleflow modelling, bring the true power of rules to workflow, in a fully integrated fashion.

Simple Ruleflow showing the Code Completion for a constraint

[![](/legacy/assets/images/2007/06/486d42caf89f-ruleflow1.PNG)](</assets/images/2007/06/66b22ca54f61-ruleflow1.PNG>)

Code Completion showing the available fields

[![](/legacy/assets/images/2007/06/cb785e217b17-ruleflow2.PNG)](</assets/images/2007/06/67fb8b37a195-ruleflow2.PNG>)

Code Completion showing the valid operators for the “message” field.

[![](/legacy/assets/images/2007/06/5827e8d1c13d-ruleflow3.PNG)](</assets/images/2007/06/0b713f389a3b-ruleflow3.PNG>)

The end result, of course mode complex constraints can be built.

[![](/legacy/assets/images/2007/06/f72492923106-ruleflow4.PNG)](</assets/images/2007/06/5692f090105c-ruleflow4.PNG>)