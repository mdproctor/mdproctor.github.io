---
layout: post
title: "Drools 5.4: Artificial Intelligence, A Little History"
date: 2012-05-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/05/drools-5-4-artificial-intelligence-a-little-history.html
---

If you like the article, please vote up ad dzone:  
<http://www.dzone.com/links/r/drools_54_artificial_intelligence_a_little_history.html>

As part of the 5.4 release, going out the door as we speak, I updated the intro docs. I have tried to give a wider understanding of the field and scope of work. Here is a copy. I’ll try and improve the sections over future releases, I ran out of time and the later sections are little rushed and thin. I’m not the best of writers, so please have patience, all contributions welcome :)

###  **A Little History**

Over the last few decades artificial intelligence (AI) became an unpopular term, with the well know [“AI Winter”](<http://en.wikipedia.org/wiki/AI_winter>). There were large boasts from scientists and engineers looking for funding, that never lived up to expectations along with many failed projects. [Thinking Machines Corporation](<http://en.wikipedia.org/wiki/Thinking_Machines_Corporation>) and the [5th Generation Computer](<http://en.wikipedia.org/wiki/Fifth-generation_computer>) (5GP) project probably exemplify best the problems at the time.

Thinking Machines Corporation was one of the leading AI firms in 1990, it had sales of nearly $65 million. Here is quote from it’s brochure:  
“Some day we will build a thinking machine. It will be a truly intelligent machine. One that can see and hear and speak. A machine that will be proud of us.”

Yet 5 years later it filed for Chapter 11. inc.com has a fascinating article titled [“The Rise and Fall of Thinking Machines”](<http://www.inc.com/magazine/19950915/2622.html>). The article covers the growth of the industry and how a cosy relationship with Thinking Machines and [DARPA](<http://en.wikipedia.org/wiki/DARPA>) over heated the market, to the point of collapse. It explains how and why commerce moved away from AI and towards more practical number crunching super computers.

The 5th Generation Computer project was a 400mill USD project in Japan to build a next generation computer. Valves was first, transistors was second, integrated circuits was third and finally microprocessors was fourth. This project spurred an “arms” race with the UK and USA, that caused much of the AI bubble. The 5GP would provide massive multi-cpu parallel processing hardware along with powerful knowledge representation and reasoning software via Prolog; a type of expert system. By 1992 the project was considered a failure and cancelled. It was the largest and most visible commercial venture for Prolog, and many of the failures are pinned on the problems trying to run a logic based programming language concurrently on multi cpu hardware with effective results. Some believe that the failure of the 5GP project tainted Prolog and resigned it academia, see [“Whatever Happened to Prolog”](<http://www.dvorak.org/blog/whatever-happened-to-prolog/>) by John C. Dvorak.

However while research funding dried up and the term AI became less used, many green shoots where planted and continued more quietly under discipline specific names: cognitive systems, machine learning, intelligent systems, knowledge representation and reasoning. Offshoots of these then made their way into commercial systems, such as expert systems in the Business Rules Management System (BRMS) market.

Imperative, system based languages, languages such as C, C++, Java and .Net have dominated the last 20 years. Enabled by the practicality of the languages and ability to run with good performance on commodity hardware. However many believe there is renaissance undergoing in the field of AI, spurred by advances in hardware capabilities and AI research. In 2005 Heather Havenstein authored [“Spring comes to AI winter”](<http://www.computerworld.com/s/article/99691/Spring_comes_to_AI_winter>) which outlines a case for this resurgence, which she refers to as a spring. Norvig and Russel dedicate several pages to what factors allowed the industry to over come it’s problems and the research that came about as a result:

“Recent years have seen a revolution in both the content and the methodology of work in artificial intelligence. It is now more common to build on existing theories than to propose brand-new ones, to base claims on rigorous theorems or hard experimental evidence rather than on intuition, and to show relevance to real-world applications rather than toy examples.” (Artificial Intelligence : A Modern Approach.)

Computer vision, neural networks, machine learning and knowledge representation and reasoning (KRR) have made great strides in become practical in commercial environments. For example vision based systems can now fully map out and navigate their environments with strong recognition skills, as a result we now have self driving cars about to enter the commercial market. Ontological research, based around description logic, has provided very rich semantics to represent our world. Algorithms such as the tableaux algorithm have made it possible to effectively use those rich semantics in large complex ontologies. Early KRR systems, like Prolog in 5GP, were dogged by the limited semantic capabilities and memory restrictions on the size of those ontologies.

###  **Knowledge Representation and Reasoning**

In A Little History talks about AI as a broader subject and touches on Knowledge Representation and Reasoning (KRR) and also Expert Systems, I’ll come back to Expert Systems later.  
KRR is about how we represent our knowledge in symbolic form, i.e. how we describe something. Reasoning is about how we go about the act of thinking using this knowledge. System based languages, like Java or C+, have classification systems, called Classes, to be able to describe things, in Java we calls these things beans or instances. However those classification systems are limited to ensure computational efficiency. Over the years researchers have developed increasingly sophisticated ways to represent our world, many of you may already have heard of OWL (Web Ontology Language). Although there is always a gap between what we can be theoretically represented and what can be used computationally in practically timely manner, which is why OWL has different sub languages from Lite to Full. It is not believed that any reasoning system can support OWL Full. Although Each year algorithmic advances try and narrow that gap and improve expressiveness available to reasoning engines.

There are also many approaches to how these systems go about thinking. You may have heard of discussions comparing the merits of forward chaining, which is reactive and data driven, or backward chaining, which is passive and query driven. Many other types of reasoning techniques exists, each of which enlarges the scope of the problems we can tackle declaratively. To list just a few: imperfect reasoning (fuzzy logic, certainty factors), defeasible logic, belief systems, temporal reasoning and correlation. Don’t worry if some of those words look alien to you, they aren’t needed to understand Drools and are just there to give an idea of the range of scope of research topics; which is actually far more extensive than this small list and continues to grow as researches push new boundaries.

KRR is often refereed as the core of Artificial Intelligence Even when using biological approaches like neural networks, which model the brain and are more about pattern recognition than thinking, they still build on KRR theory. My first endeavours with Drools were engineering oriented, as I had no formal training or understanding of KRR. Learning KRR has allowed me to get a much wider theoretical background. Allowing me to better understand both what I’ve done and where I’m going, as it underpins nearly all of the theoretical side to our Drools R&D. It really is a vast and fascinating subject that will pay dividends for those that take the time learn, I know it did and still does for me. Bracham and Levesque have written a seminal piece of work, called “Knowledge Representation and Reasoning” that for anyone wanting to build strong foundations is a must read. I would also recommend the Russel and Norvig book “Artificial Intelligence, a modern approach” which also covers KRR.

###  **Rule Engines and Production Rule Systems**

We’ve now covered a brief history of AI and learnt that the core of AI is formed around KRR. We’ve shown than KRR is vast and fascinating subject which forms the bulk of the theory driving Drools R&D.  
The rule engine is the computer program that delivers KRR functionality to the developer. At a high level it has three components:

  * Ontology
  * Rules
  * Data

As previous mentioned the ontology is the representation model we use for our “things”. It could be a simple records or Java classes or full blown OWL based ontologies. The Rules do the reasoning and facilitate thinking. The distinction between rules and ontologies blurs a little with OWL based ontologies, who’s richness is rule based.

The term rule engine is quite ambiguous in that it can be any system that uses rules, in any form, that can be applied to data to produce outcomes. This includes simple systems like form validation and dynamic expression engines. The book “How to Build a Business Rules Engine (2004)” by Malcolm Chisholm exemplifies this ambiguity. The book is actually about how to build and alter a database schema to hold validation rules. The book then shows how to generate VB code from those validation rules to validate data entry. Which while very valid, it is very different to what we talking about so far.

Drools started life as a specific type of rule engine called a production rule system (PRS) and was based around the Rete algorithm. The Rete algorithm, developed by Charles Forgey in 1979, forms the brain of a Production Rules System and is able to scale to a large number of rules and facts. A Production Rule is a two-part structure: the engine matches facts and data against Production Rules – also called Productions or just Rules – to infer conclusions which result in actions.

```xml
when    <conditions>then    <actions>;
```

The process of matching the new or existing facts against Production Rules is called pattern matching, which is performed by the inference engine. Actions execute in response to changes in data, like a database trigger; we say this is a data driven approach to reasoning. The actions themselves can change data, which in turn could match against other rules causing them to fire; this is referred to asforward chaining

Drools implements and extends the Rete algorithm;. The Drools Rete implementation is called ReteOO, signifying that Drools has an enhanced and optimized implementation of the Rete algorithm for object oriented systems. Our more recent work goes well beyond Rete. Other Rete based engines also have marketing terms for their proprietary enhancements to Rete, like RetePlus and Rete III. Th e most common enhancements are covered in “Production Matching for Large Learning Systems (Rete/UL)” (1995) by Robert B. Doorenbos. Leaps used to be provided but was retired as it became unmaintained, the good news is our research is close to producing an algorithm that merges the benefits of Leaps with Rete.

The Rules are stored in the Production Memory and the facts that the Inference Engine matches against are kept in the Working Memory. Facts are asserted into the Working Memory where they may then be modified or retracted. A system with a large number of rules and facts may result in many rules being true for the same fact assertion; these rules are said to be in conflict. The Agenda manages the execution order of these conflicting rules using a Conflict Resolution strategy.

[![](/legacy/assets/images/2012/05/853cb93d21a4-rule-engine-inkscape.png)](</assets/images/2012/05/4a4811108242-rule-engine-inkscape.png>)

###  **Hybrid Reasoning Systems**

You may have read discussions comparing the merits of forward chaining (reactive and data driven) or backward chaining(passive query). Here is a quick explanation of these two main types of reasoning.

Forward chaining is “data-driven” and thus reactionary, with facts being asserted into working memory, which results in one or more rules being concurrently true and scheduled for execution by the Agenda. In short, we start with a fact, it propagates and we end in a conclusion.

[![](/legacy/assets/images/2012/05/8ba27e407fe5-Forward_Chaining.png)](</assets/images/2012/05/6187440e0c8d-Forward_Chaining.png>)

Backward chaining is “goal-driven”, meaning that we start with a conclusion which the engine tries to satisfy. If it can’t it then searches for conclusions that it can satisfy; these are known as subgoals, that will help satisfy some unknown part of the current goal. It continues this process until either the initial conclusion is proven or there are no more subgoals. Prolog is an example of a Backward Chaining engine. Drools can also do backward chaining, which we refer to as derivation queries.

[![](/legacy/assets/images/2012/05/b7f06dbbd5c1-Backward_Chaining.png)](</assets/images/2012/05/4351c59a67de-Backward_Chaining.png>)

Historically you would have to make a choice between systems like OPS5 (forward) or Prolog (backward). Now many modern systems provide both types of reasoning capabilities. There are also many other types of reasoning techniques, each of which enlarges the scope of the problems we can tackle declaratively. To list just a few: imperfect reasoning (fuzzy logic, certainty factors), defeasible logic, belief systems, temporal reasoning and correlation. Modern systems are merging these capabilities, and others not listed, to create hybrid reasoning systems (HRS).

While Drools started out as a PRS, 5.x introduced Prolog style backward chaining reasoning as well as some functional programming styles. For this reason HRS is now the preferred term when referring to Drools, and what it is.

Drools current provides crisp reasoning, but imperfect reasoning is almost ready. Initially this will be imperfect reasoning with fuzzy logic, later we’ll add support for other types of uncertainty. Work is also under way to bring OWL based ontological reasoning, which will integrate with our traits system. We also continue to improve our functional programming capabilities.

**Expert Systems**

You will often hear the terms expert systems used to refer to production rule systems or Prolog like systems. While this is normally acceptable, it’s technically wrong as these are frameworks to build expert systems with, and not actually expert systems themselves. It becomes an expert system once there is an ontological model to represent the domain and there are facilities for knowledge acquisition and explanation.

Mycin is the most famous expert system, built during the 70s. It is still heavily covered in academic literature, such as the recommended book “Expert Systems” by Peter Jackson.

[![](/legacy/assets/images/2012/05/a36f7e6fe9e2-expertsytem_history.png)](</assets/images/2012/05/0ad45139344e-expertsytem_history.png>)

###  **Recommended Reading**

####  **General AI, KRR and Expert System Books**

For those wanting to get a strong theoretical background in KRR and expert systems, I’d strongly recommend the following books. “Artificial Intelligence: A Modern Approach” is must have, for anyone’s bookshelf.

  * Introduction to Expert Systems

    * Peter Jackson

  * Expert Systems: Principles and Programming

    * Joseph C. Giarratano, Gary D. Riley

  * Knowledge Representation and Reasoning

    * Ronald J. Brachman, Hector J. Levesque

  * Artificial Intelligence : A Modern Approach.

    * Stuart Russell and Peter Norvig

[![](/legacy/assets/images/2012/05/3cd248ba2e38-book_recommendations.png)](</assets/images/2012/05/71d98f536063-book_recommendations.png>)

#### 

**Papers**

Here are some recommended papers that cover some interesting areas in rule engine research.

  * Production Matching for Large Learning Systems : Rete/UL (1993)

    * Robert B. Doorenbos

  * Advances In Rete Pattern Matching

    * Marshall Schor, Timothy P. Daly, Ho Soo Lee, Beth R. Tibbitts (AAAI 1986)

  * Collection-Oriented Match

    * Anurag Acharya and Milind Tambe (1993)

  * The Leaps Algorithm (1990)

    * Don Battery

  * Gator: An Optimized Discrimination Network for Active Database Rule Condition Testing (1993)

    * Eric Hanson , Mohammed S. Hasan

#### 

**Drools Books**

There are currently three Drools books, all from Packt Publishing.

  * JBoss Drools Business Rules

    * Paul Brown

  * Drools JBoss Rules 5.0 Developers Guide

    * Michali Bali

  * Drools Developer’s Cookbook

    * Lucas Amador

[![](/legacy/assets/images/2012/05/c26ccbd079b0-drools_book_recommendations.png)](</assets/images/2012/05/39cd94c5b360-drools_book_recommendations.png>)

If you like the article, please vote up ad dzone:  
<http://www.dzone.com/links/r/drools_54_artificial_intelligence_a_little_history.html>