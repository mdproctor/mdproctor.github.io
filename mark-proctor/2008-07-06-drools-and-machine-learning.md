---
layout: post
title: "Drools and Machine Learning"
date: 2008-07-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/drools-and-machine-learning.html
---

```drl
I’m Gizil. I am doing my master thesis in Drools project. I’m working on decision trees. I have made an ID3, C4.5 implementation with rule generation. I’m investigating bagging and boosting algorithm in order to produce better rules.I am using Annotations on object fields to be able to process extra information on the attributes of the objects. I’m generating the rules out of the trees by parsing the trees using depth first search and compiling with PackageBuilder before adding to the RuleBase. In the future I consider using MVEL for templating to generate the rules from the trees.Target Attribute or Class LabelSince I implement a Supervised learning algorithm the class labels of the target class has to be given by the user. There are two ways to input the labels. The first and easy way is specifying one of the fields related to the target class as the label by the Annotation on that field. The second way is writing a getter function on the object class and specifiying by its Annotation. Attribute DomainsThe most common domain types are categorical and quantitative. Moreover, the decision trees need to deal with complex domains which are not simple primitive object types. Categorical (discrete) domain is commonly constructed by a set of String values. There has to be a finite number of discrete values. The attributes are assumed to be categorical by default. Only if there is an annotation saying the opposite then the domain is treated as quantitative. The target attribute has to be categorical since it is not a regression tree implementation.Quantitative (continuous) domain: Commonly, subset of real numbers, where there is a measurable difference between the possible values. Integers are usually treated as continuous in practical problems. This type of domain has to be discretized by defining a various number of thresholds (intervals) for each possible class. My implementation can discretize numerical attributes which are a set of real numbers and have quantitative domain.   For example: age 15 20 Literal attributes which are set of Strings and have a continuous domain can also be discretized by defining a various number of sets for each possible class.For example: letter element of {a, e, i, o, u} as vowel letter not element of {a, e, i, o, u} as consonantComplex domain implements a domain of an attribute that belongs to another object class. This type of domain needs more care because there are many possibilities such as Collections or references to the object class, itself.Quinlan’s C4.5 AlgorithmComparing to the ID3 the C4.5 learning algorithm can tackle with harder domains that contain many number of possible values.C4.5 deals with the numeric (integer or real) and continuous attributes using a discretization technic based on entropy.Continuous Attribute DiscretizationThere are mainly two approaches of discretizing the continuous attributes. One approach is using a global discretization algorithm, which results in a smaller decision tree. A global discretization algorithm would ignore the relation of the continuous attribute with the other attributes. The other approach is at any node of tree dicretizing the continuous attribute on the current set of instances that means applying the global discretization algorithm during the training of the decision tree.I implemented the Fayyad and Irani’s the Minimum descriptive length method to discretize the numerical domains which is also used by the WEKA project. Fayyad and Irani used information gain approach while evaluating the effectiveness of the discretization. I also tried the Quinlan’s gain ratio approach as an MDL method which is presented as a bit more fair evaluation of the domains due the normalization of the information gain by the information of the current data set based on the domain attribute. Moreover, there are some other approaches such as gini coefficient, or chi-squared test that need to be tested. For example:  Using the 15 Golf instances with 4 attributes (1 boolean, 1 literal and 2 numerical = 2 Categorical and 2 Quantitative) and Boolean target attribute I get a rule saying that the decision should be to play golf outside if the outlook attribute of the Golf object is “overcast”. This rule’s rank is 0.2858 which means that the rule is classifiying 28.58 % of the given Golf objects.rule “#0 decision= Play  classifying 4.0 num of facts with rank:0.2858” when$golf_0 : Golf(outlook == “overcast”, $target_label : decision )thenSystem.out.println(“[decision] Expected value (” + $target_label + “), Classified as (Play )”);end  Comments are closed. ✕KIEBlogKogitoDroolsjBPMOptaPlanner Featured posts All posts  ×  Archive   Feed Type  Article (1434)  Event (89)  News (79)  Presentation (62)  Release (111)  Video (40)Authors  Mark Proctor (578)  Kris Verlaenen (228)  Maciej Swiderski (105)  Geoffrey De Smet (94)  Edson Tirelli (72)  Michael Neale (59)  Tihomir Surdilovic (45)  Salaboy (42)  Cristiano Nicolai (37)  Eder Ignatowicz (37)  William Siqueira (34)  Geoffrey De Smet (32)  Matteo Mortari (23)  Manaswini Das (19)  Marian Buenosayres (18)  Karina Varela (18)  Mario Fusco (15)  Guilherme Carreiro (14)  Luiz Motta (14)  Paulo Martins (12)  Guilherme Caponetto (11)  Edoardo Vacchi (10)  Sotty (9)  Toni Rikkola (8)  Francisco Javier Tirado Sarti (8)  Gonzalo Muñoz Fernández (8)  Gabriele Cardosi (7)  Toshiya Kobayashi (7)  Sadhana Nandakumar (7)  paul browne (6)  rsynek (6)  Tiago Bento (6)  Saravana Balaji Srinivasan (5)  Tommaso Teofili (5)  Jacopo Rota (5)  Alessandro Costa (5)  Ricardo Zanini (5)  Tiago Dolphine (4)  Michael Anstis (4)  Fabrizio Antonangeli (4)  Ajay Jaganathan (4)  Daniel José dos Santos (4)  Ruben Romero Montes (3)  Rui Vieira (3)  triceo (3)  Luca Molteni (3)  Valentino Pellegrino (3)  Yeser Amer (3)  Helber Belmiro (3)  Jozef Marko (3)  wmedvede (3)  Christopher-Chianelli (3)  Diego Torres Fuerte (2)  Jaime Enriquez Parada (2)  Rob Geada (2)  Kirill Gaevskii (2)  Adriel Paredes (2)  Thiago Lugli (2)  MusaTalluzi (2)  Rishiraj Anand (2)  Rebecca Whitworth (2)  Archana Krishnan (2)  Wagner Lemos (2)  Enrique Mingorance Cano (2)  Paolo Bizzarri (1)  Christopher Chianelli (1)  Trevor Royer (1)  Reinhold Engelbrecht (1)  Nicole Prentzas (1)  Dmitrii Tikhomirov (1)  Ashley Ying (1)  Christoph Deppisch (1)  Jan Stastny (1)  Nikhil Dewoolkar (1)  Filippe Spolti (1)  tdavid (1)  Leonardo Gomes (1)  Jaroslaw Kijanowski (1)  Andrew Waterman (1)  Joe White (1)  Roberto Emanuel (1)  sudheerchekka (1)  jgoldsmith613 (1)  mariofusco (1)  mcimbora (1)  oskopek (1)  Handrey Cunha (1)  Hao Wu (1)  Jiri Locker (1)  Donato Marrazzo (1)  Lubo Terifaj (1)  michaltomco (1)  Abhishek Kumar (1)  Roger Martinez (1)  pauljamesbrown (1)  Jeff Taylor (1)  Michael Perez (1)See more  AI RulesAll other Processing CloudEvents with Drools
 Groupby – a new way to accumulate facts in D...
 Toward a reliable and fully recoverable Drools sta...
 Integrate Excel with Drools on OpenShift with Knat...
 Simplify Kubernetes debugging with declarative log...
 CloudEvents labeling and classification with Drool...
 First Virtual Technical Exploration for IBM Busine...
 Smarter Decision Tables Generation through Data...
 Exceptional rules, with Drools and Kogito
 Drools Reactive Messaging processing
 Drools 8 Final – toward a modular and cloud ...
 Drools trouble-shooting : Memory issues
 Transparent ML, integrating Drools with AIX360
 a DMN FEEL handbook
 Kogito Rules (Drools) with Java Inheritance
 Serverless Drools in 3 steps: Kogito, Quarkus, Kub...
 Explaining Drools with TrustyAI
 Refactoring the Drools Compiler
 Upgrade Drools version
 DMN Types from Java Classes
 Integrating Drools DMN Engine with IBM Open Predic...
 DEFEASIBLE REASONING, DROOLS AND TRUTH MAINTENANCE...
 Using JavaScript and Power Fx with DMN
 Content Based Routing with Quarkus and Kogito
 Prototypes and Live Queries: A Sneak Peek Into The...
 Event-driven predictions with Kogito
 Calling Java from DMN
 Data enrichment use-case with DMN and BPMN
 Event-driven rules with Kogito
 The Road Towards a Public API (part 2)
 All posts →
```