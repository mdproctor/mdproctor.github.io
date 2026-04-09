---
layout: post
title: "Reactive Incremental Graph Reasoning with Drools"
date: 2015-03-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/03/reactive-incremental-graph-reasoning-with-drools.html
---

Today Mario got a first working version for incremental reactive graphs with Drools. This means people no longer need to flatten their models to a purely relational representation to get reactivity. It provides a hybrid language and engine for both relational and graph based reasoning. To differentiate between relational joins and reference traversal a new XPath-like was introduced, that can be used inside of patterns. Like XPath it supports collection iteration.

Here is a simple example, that finds all men in the working memory:  
Man( $toy: /wife/children[age > 10]/toys )

For each man it navigates the wife reference then the children reference; the children reference is a list. For each child in the list that is over ten it will navigate to its toy’s list. With the XPath notation if the leaf property is collection it will iterate it, and the variable binds to each iteration value. If there are two children over the age of 10, who have 3 toys each, it would execute 6 times.

As it traverses each reference a hook is injected to support incremental reactivity. If a new child is added or removed, or if an age changes, it will propagate the incremental changes. The incremental nature means these hooks are added and removed as needed, which keeps it efficient and light.

You can follow some of the unit tests here:  
<https://github.com/mariofusco/drools/blob/xpath/drools-compiler/src/test/java/org/drools/compiler/xpath/XpathTest.java>

It’s still very early pre-alpha stuff, but I think this is exciting stuff.