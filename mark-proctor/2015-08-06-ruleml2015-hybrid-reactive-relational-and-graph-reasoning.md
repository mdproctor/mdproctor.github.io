---
layout: post
title: "RuleML2015 : Hybrid Reactive Relational and Graph Reasoning"
date: 2015-08-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/08/ruleml2015-hybrid-reactive-relational-and-graph-reasoning.html
---

Here are the slides and presentation for my RuleML submission “Building a Hybrid Reactive Rule Engine for Relational and Graph Reasoning”. In this we propose a syntax extensions inspired by XPath, called OOPath, for Drools along with engine extensions and domain integration for reactive pojo graphs. We are hoping this new syntax and approach will make rule engines much easier to use for java developers. This work is already at an early prototype stage, and exists in master. You can follow the unit tests here:  
<https://github.com/droolsjbpm/drools/blob/master/drools-compiler/src/test/java/org/drools/compiler/xpath/XpathTest.java>

The first screenshot shows three rules. R1 is a reactive relational rule. R2 uses a ‘from’ which has access to the full graph information, but is not reactive. R3 uses OOPath statement, which is succinct and reactive. The second and third screenshots show more advanced syntax.

[![](/legacy/assets/images/2015/08/d6cd1a84e81f-TI9hUqV.png)](</assets/images/2015/08/b862f642e128-TI9hUqV.png>)

[(click to enlarge)](</assets/images/2015/08/b862f642e128-TI9hUqV.png>)

[![](/legacy/assets/images/2015/08/ad645e9c28e9-gCF0ZRD.png)](</assets/images/2015/08/f5a5dbdbcf8d-gCF0ZRD.png>)

[(click to enlarge)](</assets/images/2015/08/f5a5dbdbcf8d-gCF0ZRD.png>)

[![](/legacy/assets/images/2015/08/690f76ff0081-E8Kauit.png)](</assets/images/2015/08/f153afc6119a-E8Kauit.png>)

[(click to enlarge)](</assets/images/2015/08/f153afc6119a-E8Kauit.png>)

> **📷 Missing image** — _(click to enlarge)_

The Slides and video:  
slides : <http://www.slideshare.net/MarkProctor/ruleml2015-hybrid-relational-and-graph-reasoning>  
video : <https://www.youtube.com/watch?v=8NpJ845kg_Q>

[![YouTube video: 8NpJ845kg_Q](/legacy/assets/images/youtube/8NpJ845kg_Q.jpg)  
▶ Watch on YouTube](<https://www.youtube.com/watch?v=8NpJ845kg_Q>)