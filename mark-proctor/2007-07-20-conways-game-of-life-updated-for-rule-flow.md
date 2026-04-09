---
layout: post
title: "Conways Game of Life updated for Rule Flow"
date: 2007-07-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/conways-game-of-life-updated-for-rule-flow.html
---

As promised I finally got round to updating the popular Conways Game of Life example so it can be executed with both agenda-groups and ruleflows for execution control. So now people have a good example to study when trying to learn the two concepts. (click to enlarge images).

With agenda-groups we specify the stack execution order for each group, in the java code.  
[![](/legacy/assets/images/2007/07/5dc24f3cb8d5-agendagroupNextGeneration.PNG)](</assets/images/2007/07/ab1d896873a3-agendagroupNextGeneration.PNG>)  
With ruleflow we instead specify the process id of the ruleflow:  
[![](/legacy/assets/images/2007/07/6388630f2781-ruleflowNextGeneration.PNG)](</assets/images/2007/07/a2f9712a5f7b-ruleflowNextGeneration.PNG>)  
Here you can see the ruleflow for the above process id, notice how “birth” and “kill” are executed in parallel:  
[![](/legacy/assets/images/2007/07/6dd9b6779478-conwayRuleFlow.PNG)](</assets/images/2007/07/be0b6a8bd559-conwayRuleFlow.PNG>)  
This code is in trunk, and will be part of the next release for drools-examples.

From working on this example what has become obvious is we need support for sub ruleflows, so that we can have a parent ruleflow choreographing all the ruleflows in the application, which is currently being done from java code.