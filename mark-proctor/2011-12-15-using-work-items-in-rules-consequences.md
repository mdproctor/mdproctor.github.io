---
layout: post
title: "Using Work Items in rules' consequences"
date: 2011-12-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/12/using-work-items-in-rules-consequences.html
---

Recently I [added](<http://blog.athico.com/2011/11/guvnor-using-jbpm-work-items-in.html>) the ability to use Work Items as function calls in the guided decision table editor in Guvnor. This highlighted that Work Items have always been available as function calls in DRL but this has not been well documented; leaving users to make the connection.

Various Work Item handlers are available “out of the (jBPM) box” in the org.jbpm.process.workitem package that may prove useful to rule authors. In addition Work Item Handlers providing bespoke services for all domain areas can be easily authored and plugged in.

I have added a couple of examples to drools-examples (in the master branch on [github](<https://github.com/droolsjbpm/drools/tree/master/drools-examples/src/main/java/org/drools/examples/workitemconsequence>) and to be included 5.4.0.beta1) that illustrate how to use Work Item handlers from the right-hand side of a rule: one simulates sending an email and the other provides a greeting service; the code for both residing in custom Work Item handlers.

I hope they provide a catalyst to encourage the use of Work Items in rules.