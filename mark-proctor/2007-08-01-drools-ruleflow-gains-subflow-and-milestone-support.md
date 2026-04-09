---
layout: post
title: "Drools RuleFlow gains subflow and milestone support"
date: 2007-08-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/08/drools-ruleflow-gains-subflow-and-milestone-support.html
---

Drools 4.0.1 will include SubFlow and Milestone support, below shows a screenshot of the new pallet. For more information on WorkFlow patterns see [http://workflowpatterns.com](<http://workflowpatterns.com/>).

[![](/legacy/assets/images/2007/08/cf5aebb19618-ruleflowpallete.PNG)](</assets/images/2007/08/507f1c02a01c-ruleflowpallete.PNG>)Drools 4.0.1 will also include a new Number Guess example that shows a recursive rule flow.

[![](/legacy/assets/images/2007/08/cbe1ee6fcb84-numberguess.PNG)](</assets/images/2007/08/c8043cec2b22-numberguess.PNG>)Here you can see the Rule Flow branch constraint editor with context assist. As mentioned before our constraint editor gives you full access to the Drools “when” conditional language and that constraint lives as an actual rule reasoning over the Working Memory, allowing for very powerful constraints to be expressed.

[![](/legacy/assets/images/2007/08/9264e46eb35c-ruleflowcosntraint1.PNG)](</assets/images/2007/08/af670370672d-ruleflowcosntraint1.PNG>)  
[![](/legacy/assets/images/2007/08/49e31e2de789-ruleflowcosntraint2.PNG)](</assets/images/2007/08/36d3c81d37fe-ruleflowcosntraint2.PNG>)Finally here you can see how easy it is to add rules in the drl to a ruleflow-group, its just a simple attribute. Complex process behavioural modelling has never been so easy :)

[![](/legacy/assets/images/2007/08/374eae8f4154-RuleFlowDRLExample.PNG)](</assets/images/2007/08/9ebb02a9118b-RuleFlowDRLExample.PNG>)