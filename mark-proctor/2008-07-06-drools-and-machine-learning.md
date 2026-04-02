---
layout: post
title: "Drools and Machine Learning"
date: 2008-07-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/drools-and-machine-learning.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools and Machine Learning](<https://blog.kie.org/2008/07/drools-and-machine-learning.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 6, 2008  
[AI](<https://blog.kie.org/category/ai>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’m Gizil. I am doing my master thesis in Drools project. I’m working on decision trees. I have made an ID3, C4.5 implementation with rule generation. I’m investigating bagging and boosting algorithm in order to produce better rules.

I am using Annotations on object fields to be able to process extra information on the attributes of the objects. I’m generating the rules out of the trees by parsing the trees using depth first search and compiling with PackageBuilder before adding to the RuleBase. In the future I consider using MVEL for templating to generate the rules from the trees.

Target Attribute or Class Label

Since I implement a Supervised learning algorithm the class labels of the target class has to be given by the user. There are two ways to input the labels. The first and easy way is specifying one of the fields related to the target class as the label by the Annotation on that field. The second way is writing a getter function on the object class and specifiying by its Annotation. 

Attribute Domains

The most common domain types are categorical and quantitative. Moreover, the decision trees need to deal with complex domains which are not simple primitive object types. 

  1. Categorical (discrete) domain is commonly constructed by a set of String values. There has to be a finite number of discrete values. The attributes are assumed to be categorical by default. Only if there is an annotation saying the opposite then the domain is treated as quantitative. The target attribute has to be categorical since it is not a regression tree implementation.

  2. Quantitative (continuous) domain: Commonly, subset of real numbers, where there is a measurable difference between the possible values. Integers are usually treated as continuous in practical problems. This type of domain has to be discretized by defining a various number of thresholds (intervals) for each possible class. My implementation can discretize numerical attributes which are a set of real numbers and have quantitative domain. 

For example: age 

15 

20 

Literal attributes which are set of Strings and have a continuous domain can also be discretized by defining a various number of sets for each possible class.

For example: letter element of {a, e, i, o, u} as vowel

letter not element of {a, e, i, o, u} as consonant

  3. Complex domain implements a domain of an attribute that belongs to another object class. This type of domain needs more care because there are many possibilities such as Collections or references to the object class, itself.

Quinlan’s C4.5 Algorithm

Comparing to the ID3 the C4.5 learning algorithm can tackle with harder domains that contain many number of possible values.

C4.5 deals with the numeric (integer or real) and continuous attributes using a discretization technic based on entropy.

Continuous Attribute Discretization

There are mainly two approaches of discretizing the continuous attributes. One approach is using a global discretization algorithm, which results in a smaller decision tree. A global discretization algorithm would ignore the relation of the continuous attribute with the other attributes. The other approach is at any node of tree dicretizing the continuous attribute on the current set of instances that means applying the global discretization algorithm during the training of the decision tree.

I implemented the Fayyad and Irani’s the Minimum descriptive length method to discretize the numerical domains which is also used by the WEKA project. Fayyad and Irani used information gain approach while evaluating the effectiveness of the discretization. I also tried the Quinlan’s gain ratio approach as an MDL method which is presented as a bit more fair evaluation of the domains due the normalization of the information gain by the information of the current data set based on the domain attribute. Moreover, there are some other approaches such as gini coefficient, or chi-squared test that need to be tested. 

For example: Using the 15 Golf instances with 4 attributes (1 boolean, 1 literal and 2 numerical = 2 Categorical and 2 Quantitative) and Boolean target attribute I get a rule saying that the decision should be to play golf outside if the outlook attribute of the Golf object is “overcast”. This rule’s rank is 0.2858 which means that the rule is classifiying 28.58 % of the given Golf objects.

rule “#0 decision= Play classifying 4.0 num of facts with rank:0.2858” 

when

$golf_0 : Golf(outlook == “overcast”, $target_label : decision )

then

System.out.println(“[decision] Expected value (” + $target_label + “), Classified as (Play )”);

end

## Author

     * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-and-machine-learning.html&linkname=Drools%20and%20Machine%20Learning> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-and-machine-learning.html&linkname=Drools%20and%20Machine%20Learning> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-and-machine-learning.html&linkname=Drools%20and%20Machine%20Learning> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-and-machine-learning.html&linkname=Drools%20and%20Machine%20Learning> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-and-machine-learning.html&linkname=Drools%20and%20Machine%20Learning> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-and-machine-learning.html&linkname=Drools%20and%20Machine%20Learning> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-and-machine-learning.html&linkname=Drools%20and%20Machine%20Learning> "Email")

Comments are closed.

✕

#### KIE

  * [Blog](<https://blog.kie.org/>)
  * [Kogito](<http://kogito.kie.org/>)
  * [Drools](<http://drools.org/>)
  * [jBPM](<http://jbpm.org/>)
  * [OptaPlanner](<http://OptaPlanner.org/>)

[Featured posts](</featured/all>) All posts

[×](<https://blog.kie.org/2008/07/drools-and-machine-learning.html>)

#####  [ Archive ](</archive>)

#####  [ Feed ](</category/all/feed>)

##### Type

Article (1434)

Event (89)

News (79)

Presentation (62)

Release (111)

Video (40)

##### Authors

Mark Proctor (578)

Kris Verlaenen (228)

Maciej Swiderski (105)

Geoffrey De Smet (94)

Edson Tirelli (72)

Michael Neale (59)

Tihomir Surdilovic (45)

Salaboy (42)

Cristiano Nicolai (37)

Eder Ignatowicz (37)

William Siqueira (34)

Geoffrey De Smet (32)

Matteo Mortari (23)

Manaswini Das (19)

Marian Buenosayres (18)

Karina Varela (18)

Mario Fusco (15)

Guilherme Carreiro (14)

Luiz Motta (14)

Paulo Martins (12)

Guilherme Caponetto (11)

Edoardo Vacchi (10)

Sotty (9)

Toni Rikkola (8)

Francisco Javier Tirado Sarti (8)

Gonzalo Muñoz Fernández (8)

Gabriele Cardosi (7)

Toshiya Kobayashi (7)

Sadhana Nandakumar (7)

paul browne (6)

rsynek (6)

Tiago Bento (6)

Saravana Balaji Srinivasan (5)

Tommaso Teofili (5)

Jacopo Rota (5)

Alessandro Costa (5)

Ricardo Zanini (5)

Tiago Dolphine (4)

Michael Anstis (4)

Fabrizio Antonangeli (4)

Ajay Jaganathan (4)

Daniel José dos Santos (4)

Ruben Romero Montes (3)

Rui Vieira (3)

triceo (3)

Luca Molteni (3)

Valentino Pellegrino (3)

Yeser Amer (3)

Helber Belmiro (3)

Jozef Marko (3)

wmedvede (3)

Christopher-Chianelli (3)

Diego Torres Fuerte (2)

Jaime Enriquez Parada (2)

Rob Geada (2)

Kirill Gaevskii (2)

Adriel Paredes (2)

Thiago Lugli (2)

MusaTalluzi (2)

Rishiraj Anand (2)

Rebecca Whitworth (2)

Archana Krishnan (2)

Wagner Lemos (2)

Enrique Mingorance Cano (2)

Paolo Bizzarri (1)

Christopher Chianelli (1)

Trevor Royer (1)

Reinhold Engelbrecht (1)

Nicole Prentzas (1)

Dmitrii Tikhomirov (1)

Ashley Ying (1)

Christoph Deppisch (1)

Jan Stastny (1)

Nikhil Dewoolkar (1)

Filippe Spolti (1)

tdavid (1)

Leonardo Gomes (1)

Jaroslaw Kijanowski (1)

Andrew Waterman (1)

Joe White (1)

Roberto Emanuel (1)

sudheerchekka (1)

jgoldsmith613 (1)

mariofusco (1)

mcimbora (1)

oskopek (1)

Handrey Cunha (1)

Hao Wu (1)

Jiri Locker (1)

Donato Marrazzo (1)

Lubo Terifaj (1)

michaltomco (1)

Abhishek Kumar (1)

Roger Martinez (1)

pauljamesbrown (1)

Jeff Taylor (1)

Michael Perez (1)

See more

[AI](<https://blog.kie.org/category/ai>) [Rules](<https://blog.kie.org/category/rules>)

### All other

######  [Processing CloudEvents with Drools](<https://blog.kie.org/2024/05/processing-cloudevents-with-drools.html>)  
by [Toshiya Kobayashi](<https://blog.kie.org/category/all?search_authors=261>)

######  [Groupby – a new way to accumulate facts in D...](<https://blog.kie.org/2023/07/groupby-a-new-way-to-accumulate-facts-in-drl.html>)  
by [Christopher Chianelli](<https://blog.kie.org/category/all?search_authors=315>)

######  [Toward a reliable and fully recoverable Drools sta...](<https://blog.kie.org/2023/05/toward-a-reliable-and-fully-recoverable-drools-stateful-session.html>)  
by [Mario Fusco](<https://blog.kie.org/category/all?search_authors=38>)

######  [Integrate Excel with Drools on OpenShift with Knat...](<https://blog.kie.org/2023/05/integrate-excel-with-drools-on-openshift-with-knative-and-quarkus.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [Simplify Kubernetes debugging with declarative log...](<https://blog.kie.org/2023/03/simplify-kubernetes-debugging-with-declarative-logic.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [CloudEvents labeling and classification with Drool...](<https://blog.kie.org/2023/02/cloudevents-labeling-and-classification-with-drools.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [First Virtual Technical Exploration for IBM Busine...](<https://blog.kie.org/2023/01/first-virtual-technical-exploration-for-ibm-business-automation-manager-open-edition-on-february-8-emea-time-zone.html>)  
by [Reinhold Engelbrecht](<https://blog.kie.org/category/all?search_authors=310>)

######  [Smarter Decision Tables Generation through Data...](<https://blog.kie.org/2023/01/automatically-generating-decision-tables-in-dmn.html>)  
by [Jozef Marko](<https://blog.kie.org/category/all?search_authors=308>)

######  [Exceptional rules, with Drools and Kogito](<https://blog.kie.org/2023/01/exceptional-rules-with-drools-and-kogito.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [Drools Reactive Messaging processing](<https://blog.kie.org/2022/11/drools-reactive-messaging-processing.html>)  
by [Toshiya Kobayashi](<https://blog.kie.org/category/all?search_authors=261>)

######  [Drools 8 Final – toward a modular and cloud ...](<https://blog.kie.org/2022/10/drools-8-final-toward-a-modular-and-cloud-native-rule-engine.html>)  
by [Mario Fusco](<https://blog.kie.org/category/all?search_authors=38>)

######  [Drools trouble-shooting : Memory issues](<https://blog.kie.org/2022/09/drools-trouble-shooting-memory-issues.html>)  
by [Toshiya Kobayashi](<https://blog.kie.org/category/all?search_authors=261>)

######  [Transparent ML, integrating Drools with AIX360](<https://blog.kie.org/2022/09/transparent-ml-integrating-drools-with-aix360.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [a DMN FEEL handbook](<https://blog.kie.org/2022/08/a-dmn-feel-handbook.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [Kogito Rules (Drools) with Java Inheritance](<https://blog.kie.org/2022/08/kogito-rules-drools-with-java-inheritance.html>)  
by [Jeff Taylor](<https://blog.kie.org/category/all?search_authors=258>)

######  [Serverless Drools in 3 steps: Kogito, Quarkus, Kub...](<https://blog.kie.org/2022/08/serverless-drools-in-3-steps-kogito-quarkus-kubernetes-and-knative.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [Explaining Drools with TrustyAI](<https://blog.kie.org/2022/07/explaining-drools-trustyai.html>)  
by [Rob Geada](<https://blog.kie.org/category/all?search_authors=281>)

######  [Refactoring the Drools Compiler](<https://blog.kie.org/2022/07/refactoring-the-drools-compiler.html>)  
by [Edoardo Vacchi](<https://blog.kie.org/category/all?search_authors=32>)

######  [Upgrade Drools version](<https://blog.kie.org/2022/05/upgrade-drools-version.html>)  
by [Toshiya Kobayashi](<https://blog.kie.org/category/all?search_authors=261>)

######  [DMN Types from Java Classes](<https://blog.kie.org/2022/05/dmn-types-from-java-classes.html>)  
by [Yeser Amer](<https://blog.kie.org/category/all?search_authors=238>)

######  [Integrating Drools DMN Engine with IBM Open Predic...](<https://blog.kie.org/2022/04/integrating-drools-dmn-engine-with-ibm-open-prediction-service.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [DEFEASIBLE REASONING, DROOLS AND TRUTH MAINTENANCE...](<https://blog.kie.org/2022/04/defeasible-reasoning-drools-and-truth-maintenance-system.html>)  
by [Nicole Prentzas](<https://blog.kie.org/category/all?search_authors=287>)

######  [Using JavaScript and Power Fx with DMN](<https://blog.kie.org/2022/03/using-javascript-and-power-fx-with-dmn.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [Content Based Routing with Quarkus and Kogito](<https://blog.kie.org/2022/03/content-based-routing-with-quarkus-and-kogito.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [Prototypes and Live Queries: A Sneak Peek Into The...](<https://blog.kie.org/2022/03/prototypes-and-live-queries-a-sneak-peek-into-the-future-of-drools-featuring-debezium-and-apache-calcite.html>)  
by [Mario Fusco](<https://blog.kie.org/category/all?search_authors=38>)

######  [Event-driven predictions with Kogito](<https://blog.kie.org/2022/01/event-driven-predictions-with-kogito.html>)  
by [Alessandro Costa](<https://blog.kie.org/category/all?search_authors=74>)

######  [Calling Java from DMN](<https://blog.kie.org/2022/01/dmn-calls-java.html>)  
by [Donato Marrazzo](<https://blog.kie.org/category/all?search_authors=242>)

######  [Data enrichment use-case with DMN and BPMN](<https://blog.kie.org/2022/01/data-enrichment-use-case-with-dmn-and-bpmn.html>)  
by [Matteo Mortari](<https://blog.kie.org/category/all?search_authors=36>)

######  [Event-driven rules with Kogito](<https://blog.kie.org/2022/01/event-driven-rules-with-kogito.html>)  
by [Alessandro Costa](<https://blog.kie.org/category/all?search_authors=74>)

######  [The Road Towards a Public API (part 2)](<https://blog.kie.org/2021/12/the-road-towards-a-public-api-part-2.html>)  
by [Edoardo Vacchi](<https://blog.kie.org/category/all?search_authors=32>)

[All posts →](<https://blog.kie.org>)