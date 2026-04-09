---
layout: post
title: "OOPath - Reactive XPath like functionality for Drools"
date: 2015-11-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/11/__trashed-8.html
---

### OOPath – Reactive XPath like functionality for Drools

Back in august I wrote a blog providing an update on our work around OOPath, it included links to unit tests a 26min presentation on the subject.  
<http://blog.athico.com/2015/08/ruleml2015-hybrid-reactive-relational.html>

This work provides a way to work with your Java models in Drools without having to flatten them, providing full reactivity over that graph of pojos. It also provides a more compact syntax, modelled on XPath.

Finally this work is now available in master and our nightly builds for you to try. It requires code instrumentation, so for now it is only available within our internal drl type declares. We are going to write a maven module that will instrument existing pojos.

We’ve added a simple example now, that you can checkout and run here.  
https://github.com/mariofusco/drools/blob/oopath/drools-examples-api/reactive-kiesession/