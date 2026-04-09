---
layout: post
title: "XText and Attempto for Controlled Natural Language"
date: 2011-10-05
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/10/xtext-and-attempto-for-controlled-natural-language.html
---

Drools has always been independant of the parser. DRL is just a general purpose technical language for logic programming. We’ve always been big proponents of the conceptual idea of DSLs.

An early hack for our “DSL” was a simple string interpolation framework, for sentence templating. We always hoped to do more, as this was unstructured, but DSL’s need tooling to fulfill their potential and this was beyond the resources we had.

I’ve been following [XText](<http://www.eclipse.org/Xtext/>) for some time now and I think it now offers a real alternative to our DSLs, for domain specific structured content authoring. Version 2.0 is looking particularly sexy.  
[![](/legacy/assets/images/2011/10/e9eb8c707877-xtext.png)](</assets/images/2011/10/a8108c187865-xtext.png>)  
A recent blog [“Using Xbase for Home Automation Rules “](<http://kaikreuzer.blogspot.com/2011/09/using-xbase-for-home-automation-rules.html>) by Kai Kreuzer confirms that Xtext has a lot of potential here. I’ve suggested to Kai that he can use XText to drive our fluent descr api, which is what Antlr uses. Examples of the descr api for programmatic rule generation can be seen in this unit test:  
<https://github.com/droolsjbpm/drools/blob/master/drools-compiler/src/test/java/org/drools/lang/api/DescrBuilderTest.java>

In essence I think a number of examples can be done to develop best practices, as well as fleshing our helper classes and abstract classes to make it quicker to developer DSLs in XText for Drools.

This started to make me think about how XText can be leveraged for natural language rule authoring.

[Attempto](<http://attempto.ifi.uzh.ch/site/>) is a project for controlled natural language. You provide mappings from your classes and fields to nouns, verbs and adjectives and it’s parser will then allow you to author rules via controlled natural language. However there is no IDE for this.

Enter [XText](<http://www.eclipse.org/Xtext/>), a rising star in the Eclipse world. Xtext provides complete tooling, code completion, refactoring, outlines, based on an antlr like grammar.

Using the class and field mappings and the techniques in the Attempto parser, it should be possibe to generate an XText grammar. This would allow for controlled natural language rule authoring.

I think this is a fantastic project idea and XText really is catalyst for making this easy to realise it’s potential. Any takers?

If you’re interested, you know where to find us:  
<http://www.jboss.org/drools/irc.html>

Mark