---
layout: post
title: "Mario Fusco to join as core Drools engine developer"
date: 2011-07-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/07/mario-fusco-to-join-as-core-drools-engine-developer.html
---

It gives me great pleasure to announce that Mario Fusco will be joining the Drools team to work on the core engine in August.

[![](/legacy/assets/images/2011/07/13ca96b8b34c-MarioFusco.jpg)](</assets/images/2011/07/b60bcf5485e8-MarioFusco.jpg>)

Mario is the author of OSS Lambdaj which brings functional programming and closures to java, and the Hammurabi Scala rule engine.

Lambdaj  
<http://code.google.com/p/lambdaj/>  
<http://today.java.net/pub/a/today/2009/08/08/J1-2009-MarioFusco-Lambdaj.html> (JavaOne Audio podcast)

Hammurabi  
<http://code.google.com/p/hammurabi/>  
<http://java.dzone.com/articles/hammurabi-scala-rule-engine>

Mario initially will be focusing on improving the end user experience of the core engine, specifically in authoring DRL. Below is a list of areas he’ll be responsible for, during his first 6 months. Of course he isn’t limited to just those :)

  * Improved syntax error reporting
  * Killing all parser bugs and also expression and action evaluation bugs.
  * Better masking of the underlying execution engine (MVEL leaks too much)
  * Helping us move to a single language (no more dialects).
  * Micro benchmarking so we can better track performance and memory regressions
  * ASM bytecode compilation so we can reduce our dependency on JDT over time, which is too heavy. ASM will allow a more runtime JIT approach to expressions and actions.
  * Maintaining the Eclipse DRL editor.
  * Help with future DRL design discussions especially on functional programming.

More importantly this allows core maintenance to be spread across more people, which gives Edson and myself more time to do research so we can innovate faster.