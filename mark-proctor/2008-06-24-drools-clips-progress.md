---
layout: post
title: "Drools Clips progress"
date: 2008-06-24
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/06/drools-clips-progress.html
---

Made some progress over the weekend with Drools Clips, which will provide a Clips like language for Drools. Deftemplates are now working and I did some work on PackageBuilder so that it’s now able to handle multiple namespaces and have a RuleBase attached to provide a more “shell” like environment suitable for Clips. Michael Neale also got a basic command line shell working. So what does it support?

  * deftemplate
  * defrule
  * deffuction
  * and/or/not/exists/test Conditional Elements
  * Literal, Variable, Return Value and Predicate field constraints

You can look at the [ClipsShellTest](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-clips/src/test/java/org/drools/clips/ClipsShellTest.java?r=HEAD>) and [LhsClipsParserTest](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-clips/src/test/java/org/drools/clips/LhsClpParserTest.java?r=HEAD>) get an idea of the full support. It’s still early stages and it’s very rough in places, especially on error handling and feedback as well as no view commands to display data. For a little fun here is a screenshot of the shell in action:

[![](/legacy/assets/images/2008/07/6a54a64d5d96-shell.png)(click to enlarge)](</assets/images/2008/06/6407840fcbaa-shell.png>)

> **📷 Missing image** — _(click to enlarge)_

The screen shot is a contrived example but it does show a shell environment cleanly mixing deftemplates and pojos – note that Drools 5.0 does not require shadow facts, due to the new asymmetrical Rete algorithm. It also shows deffunction in use. This will be part of Milestone1, that I’m hoping to tag tomorrow.