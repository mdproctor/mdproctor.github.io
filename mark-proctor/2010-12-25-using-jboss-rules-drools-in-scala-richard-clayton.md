---
layout: post
title: "Using JBoss Rules (Drools) in Scala (Richard Clayton)"
date: 2010-12-25
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/12/using-jboss-rules-drools-in-scala-richard-clayton.html
---

<http://gettingcirrius.blogspot.com/2010/12/using-jboss-rules-drools-in-scala.html>

extract:

[![](/legacy/assets/images/2010/12/10a308835c82-droolsExpertLogo.png)![](/legacy/assets/images/2010/12/10a308835c82-droolsExpertLogo.png)](<http://downloads.jboss.com/drools/docs/5.1.1.34858.FINAL/drools-expert/html_single/images/droolsExpertLogo.png>)

The JBoss Rules Framework, more often referred to as “Drools”, is an excellent tool for combining Rules, Workflow, and Events into what the framework authors call “the Business Logic Integration Platform” (BLIP) [1]. We use Drools extensively on our project; the framework enabled us to quickly construct a rich Event Driven Architecture (SOA 2.0) in a very short time frame. In fact, we like Drools so much, we’ve been considering using it in the realm of NLP as a way for applying rules to Entity Extraction and Resolution (I should mention this was originally John’s idea).

The downside to Drools is that the framework is written in Java. Sure, Mark Proctor and gang have put a lot effort in making the platform accessible to other languages through web services, but this is far from the level of integration I would enjoy (like a C# version). I think I should take the time an caveat the fact that I consider myself to be a Java programmer (first and foremost) and then a C# developer, but after a couple of solid weeks in .NET, I find it difficult to go back. The one thing I do love about Java (more than anything else) is the language’s amazing Open Source community. So instead of embracing the “Dark Side” and becoming a Microsoft evangelist, I have decided to look into the newer languages written for the JVM.

[![](/legacy/assets/images/2010/12/3657cac9a6dd-Scala_logo.png)](<http://upload.wikimedia.org/wikipedia/en/8/85/Scala_logo.png>)The two JVM languages I find the most intriguing are Clojure and Scala.