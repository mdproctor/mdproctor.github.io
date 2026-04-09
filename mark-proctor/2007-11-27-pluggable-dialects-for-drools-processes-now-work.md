---
layout: post
title: "Pluggable Dialects for Drools Processes now work :)"
date: 2007-11-27
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/11/pluggable-dialects-for-drools-processes-now-work.html
---

Many of you would have read my [blog](<http://blog.athico.com/2007/11/vision-for-unified-rules-and-processes.html>) on unifying rules and processes, which was also featured at [infoq](<http://www.infoq.com/news/2007/11/rulesprocess>). Unifying these technologies is not just about the modelling paradigm it’s also about the infrastructure overlaps. Today I just finished my first end to end test for dialectable actions in a processes definition – which we call ruleflow, indicating its a melding of the power of processes and rules – so what does this mean?

Pluggable Dialects has been apart of the Drools framework for a while now, what it means is that any eval conditions and the consequence of the rule and can be written in any language; we currently support Java and [MVEL](<http://blog.athico.com/search/label/MVEL>) as dialect plugins.

One of the extra bits of plumbing that makes this worth while is that a Dialect, at compile time, returns the identifiers that it needs – i.e. none local variables – this allows us to do variable inject in compiled languages like Java, which means no manually retrieving and assignment variables from a context :)

Scripting language plugins like MVEL are very easy to integrate although compiled languages like Java add extra levels of complexity – this is because we want to compile all our consequences, and now actions, in a single pass. The compilation is at a later date than when the rule/action itself was built and thus we need an additional wiring process to hook the compiled code back up to the rule/action.

As we’ve already built all this for the rules framework with a bit of tweaking the process framework gets it for free – and thus we start to see the value of a unified core.

The image below (click to enlarge) shows a screenshot from our ruleflow editor in Eclipse. It contains just two actions, but of different dialects, one Action is MVEL the other in Java – both populate a String value in the List. The displayed Action is of the Java dialect, notice it has variable inject, so you don’t need to do assign the variables manually from a context, i.e.:  
List list = (List) context.getVariable(“list”);

[![](/legacy/assets/images/2007/11/4a51decf286b-ruleflowdialects1.png)](</assets/images/2007/11/0f85cd6acee9-ruleflowdialects1.png>)  
A Java Dialect Action in Ruleflow

Notice as well how the rules and process apis are complimentary to each other. The image below is from the unit test for the process definition in the above screenshot.

![](/legacy/assets/images/2007/11/4a51decf286b-ruleflowdialects1.png)![](/legacy/assets/images/2007/11/566e73c5a285-ruleflowdialects2.png)  
Dialect Unit Test for Ruleflow