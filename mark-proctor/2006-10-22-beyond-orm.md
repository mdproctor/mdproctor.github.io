---
layout: post
title: "Beyond ORM"
date: 2006-10-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/10/beyond-orm.html
---

### Beyond ORM

A rule has many similarities to a query. It contains one or more propositional and first order logic statements organised into a network to filter data additions and changes – we call this a “discrimitation network” as it discrimates against data that does not match its statements. Any data that successfully matches all statements for a rule arrives at a Terminal Node; at this point we can either execute a series of actions (ignoring the role of the Agenda, for the moment) on that “row” of data or return it as part of a query request.

Like a database we index our data to provide high performance. There are two types of indexing – Alpha Node hashing and Beta Node indexing. Alpha Node hashing is used to index literal constriants, so that we only propagate the data to the rules that match that literal value. Beta Node indexing is used to index data used in joins – we have two facts, person and cheese, we record who owns which cheese and there is a rule that says “when the person’s cheeses are out of date then email that person” we have a join between the person and the cheeses, so we index each cheese against its owner. We also attempt to share indexes, so if rules use the same literals or joins where possible we try and share those indexes – this reduces memory consumption and also avoids duplicate constraint evaluations.

However a Production Rule system provides many features beyond a traditional database. Many of the features, marked with a * are planed for JBoss Rules releases next year.  

* Efficient First Order Logic with ‘exists’, ‘not’ and ‘forall’* quantifiers as well as cardinality qualifiers with ‘accumulate’* and ‘collect’ _._
* Abilitity to mix reasoning of data inside and both outside of the Working Memory using ‘from’.
* Object Validation* so only objects that are valid can exist. “name length must be less than 30”.
* Backward Chaining* for complex inferencing.
* Ontology* support for rich Object Models, probably via some Semantic Web OWL support.
* Efficient Truth Maintenance. Truth relationships can be set in place to ensure the Working Memory never breaks this statement.A “Red Alert” object can only exist while there are 3 or more emergencies.
* Event Stream Processing(ESP)* can analyse sets of data over time windows. “Determine the average stock ticker price in the last 30 seconds”.
* Event Correlation Processing(CEP)* can analyse data sets with temporal comparisons between object.

  
Firstly, before ORM advocates try and organise a public lynching, let me just state that “Beyond ORM” does not mean to replace ORM, there are clearly many applications where ORM is preferable – particularly when dealing with truly massive datasets or where you want to be able to represent relational data in differing form. However there are situations which can benefit from a richer and better integrated solution with features as described above. There is still a lot of work to achieve all of the above and we then need to consider how to cluster working memories to provide fault tolerance and some way to also make working memories transactional. If we can solve those problems we can look to integrate JBoss Cache, JBoss Rules and JBoss ESB for a next generation Data Centre. This is is a long term R&D proposal, but I thought I would sketch down the basic ideas in the diagram below.

[![](/legacy/assets/images/2006/10/c9ef55c535c3-Beyond_ORM.png)](</assets/images/2006/10/0a1aee1142df-Beyond_ORM.png>)