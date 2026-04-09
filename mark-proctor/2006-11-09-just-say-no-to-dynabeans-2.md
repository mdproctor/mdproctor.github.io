---
layout: post
title: "Just say no to DynaBeans"
date: 2006-11-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/11/just-say-no-to-dynabeans-2.html
---

### Just say no to DynaBeans

The subject of DynaBeans just came up on the mailing list, and it is one I’ve been asked about before – so I thought I would do a blog my answer.

Dynabeans was written as a solution for Struts back in 2000, they are not JavaBean compliant – thus they have no value outside of that provided with commons BeanUtils, thus coupling your enterprise system to BeanUtils forever – no other apps are aware of them, or able to script them like they can JavaBeans. They cannot be used with any database schema mapping tools, so you cannot easily leverage db schema generation tools. JBRules 3.0 has no support for mapping utilities thus you’ll only be able to script those from within evals. If you only use evals you will have crippled the engine to work like a simple chain of command scripting engine – under no circumstances do I recommend this. Evals are a worst use case for conditions that cannot be expressed in field constraints, as field constraints and conditional elements become more powerful the dependency of evals is reduced. Further more DynaBeans are backed by a map, each read or write results in a hashmap read or write – this is not a scalable solution.

A much better solution that works now for JBRules 3.0 is to have runtime class generation. See this blog entry here: <http://sixlegs.com/blog/java/death-to-dynabeans.html>

Tools like cglib make this trivial now:

```
BeanGenerator bg = new BeanGenerator();
bg.addProperty("foo", Double.TYPE);
bg.addProperty("bar", String.class);
Object bean = bg.create();
```

That produced bean can have hibernate mappings generated at runtime, so you’ll get runtime hibernate support. JBRules can compile drls at runtime using the classloader those beans where generated with thus providing full field constraint use of them and pojo like access in the consequence – much nicer :)

For JBRules 3.2 we will provide a feature called FactTemplates – this is akin to jess/clips DefTemplates. These allow people to define Facts without the need for a compiled class, which is preferable to some who want complete encapsulation of their rules and business objects within the drl. FactTemplates are backed by an array and thus read/writes are much faster. FactTemplates support both named and int values to specify the field for the value; named set/get result in a HashMap lookup so have similar performance to DynaBean. However JBRules provides compile time optimisation of those named fields and swaps them to int lookups – we will have support for this in the JFDI language too, which we also hope will be support in jBPM. FactTemplates will also provide mapping facilities which means they can be mapped to any underlying structure – be it JavaBean, a Hashmap or a DynaBean.