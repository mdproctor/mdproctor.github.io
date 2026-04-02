---
layout: post
title: "What is a Rule Engine"
date: 2006-05-31
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/05/what-is-a-rule-engine.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [What is a Rule Engine](<https://blog.kie.org/2006/05/what-is-a-rule-engine.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 31, 2006  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Drools is a [Rule Engine](<http://en.wikipedia.org/wiki/Rule_engine>) but it is more correctly classified as a [Production Rule System](<http://www.dbmi.columbia.edu/homepages/wandong/KR/krproductionrule.html>). The term “Production Rule” originates from [formal grammer](<http://en.wikipedia.org/wiki/Formal_grammar>) – where it is described as “an abstract structure that describes a formal language precisely, i.e., a set of rules that mathematically delineates a (usually infinite) set of finite-length strings over a (usually finite) alphabet”. Production Rules is a Rule Based approach to implementing an Expert System and is considered “applied artificial intilligence”.

The term Rule Engine is quite ambiguous in that it can be any system that uses rules, in any form, that can be applied to data to produce outcomes; which includes simple systems like form validation and dynamic expression engines: “How to Build a Business Rules Engine (2004)” by Malcolm Chisholm exemplifies this ambiguity. The book is actually about how to build and alter a database schema to hold validation rules which it then shows how to generate VB code from those validation rules to validate data entry – while a very valid and useful topic for some, it caused quite a suprise to this author, unaware at the time in the subtleties of Rules Engines differences, who was hoping to find some hidden secrets to help improve the Drools engine. jBPM uses expressions and delegates in its Decision nodes; which controls the transitions in a Workflow. At each node it evaluates a rule that dicates the transition to undertake – this is also a Rule Engine. While a Production Rule System is a kind of Rule Engine and also Expert System, the validation and expression evaluation Rule Engines mention previously are not Expert Systems.

A Production Rule System is [turing complete](<http://en.wikipedia.org/wiki/Turing_complete>) with a focus on [knowledge representation](<http://en.wikipedia.org/wiki/Knowledge_representation>) to expression [propositional](<http://en.wikipedia.org/wiki/Propositional_logic>) and [first order logic](<http://en.wikipedia.org/wiki/First_order_logic>) in a concise, non ambigious and declarative manner. The brain of a Production Rules System is an [Inference Engine](<http://en.wikipedia.org/wiki/Inference_engine>) that is able to scale to a large number of rules and facts; the engine is able to schedule many rules that are elegible for execution at the same time through the use of a “conflict resolution” strategy. There are [two methods of execution for Rule-Based Systems](<http://ai-depot.com/Tutorial/RuleBased-Methods.html>) – [Forward Chaining](<http://en.wikipedia.org/wiki/Forward_chaining>) and [Backward Chaining](<http://en.wikipedia.org/wiki/Backward_chaining>); systems that implement both are called Hybrid Production Rule Systems. Understanding these two modes of operation are key to understanding why a Production Rule System is different.

Forward Chaining is ‘data-driven’ and thus reactionary – facts are asserted into the working memory which results in rules firing – we start with a fact, it propagates and we end with multiple elegible Rules which are scheduled for execution. Drools is a forward chaining engine. Backward Chaining is ‘goal-driven’, we start with a conclusion which the engine tries to satisfy. If it can’t it searches for conclusions, ‘sub goals’, that help satisfy an unknown part fo the current goal – it continues this process until either the initial conclusion is proven or there are no more sub goals. Prolog is an example of a Backward Chaining engine; Drools will adding support for Backward Chaining in its next major release.

The [Rete](<http://en.wikipedia.org/wiki/Rete_algorithm>) algorithm by [Charles Forgy](<http://en.wikipedia.org/wiki/Charles_Forgy>) is a popular approach to Forward Chaining, [Leaps](<http://www.cs.utexas.edu/users/miranker/papers/1990>) is another approach. Drools has implementations for both Rete and Leaps. The Drools Rete implementation is called ReteOO signifying that Drools has an enhanced and optimised implementation of the Rete algorithm for Object Oriented systems. Other Rete based engines also have marketing terms for their proprietary enhancements to Rete, like RetePlus and Rete III. It is important to understand that names like Rete III are purely marketing where, unlike the original published Rete Algorithm, no details of implementation are published; thus asking a question like “Does Drools implement Rete III?” is nonsensical. The most common enhancements are covered in [“Production Matching for Large Learning Systems (Rete/UL)” (1995)](<http://portal.acm.org/citation.cfm?coll=GUIDE&dl=GUIDE&id=220593>) by Robert B. Doorenbos

[Business Rule Management Systems](<http://en.wikipedia.org/wiki/BRMS>) build value on top of an Rule Engine providing systems for rule management, deployment, collaboration, analysis and end user tools for business users. Further to this the [Business Rules Approach](<http://en.wikipedia.org/wiki/Business_rules_approach>) is a fast evolving and popular methodology helping to formalise the role of Rule Engines in the enterprise.

For more information read the following two chapters from the manual:  
[Introduction and Background](<http://labs.jboss.com/file-access/default/members/jbossrules/freezone/docs/3.0.1/html_single/index.html#d0e48>)  
[Knowledge Representation](<http://labs.jboss.com/file-access/default/members/jbossrules/freezone/docs/3.0.1/html_single/index.html#d0e268>)

[Post Comment](<https://beta.blogger.com/comment.g?blogID=5869426&postID=4199780704071383892>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F05%2Fwhat-is-a-rule-engine.html&linkname=What%20is%20a%20Rule%20Engine> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F05%2Fwhat-is-a-rule-engine.html&linkname=What%20is%20a%20Rule%20Engine> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F05%2Fwhat-is-a-rule-engine.html&linkname=What%20is%20a%20Rule%20Engine> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F05%2Fwhat-is-a-rule-engine.html&linkname=What%20is%20a%20Rule%20Engine> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F05%2Fwhat-is-a-rule-engine.html&linkname=What%20is%20a%20Rule%20Engine> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F05%2Fwhat-is-a-rule-engine.html&linkname=What%20is%20a%20Rule%20Engine> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F05%2Fwhat-is-a-rule-engine.html&linkname=What%20is%20a%20Rule%20Engine> "Email")