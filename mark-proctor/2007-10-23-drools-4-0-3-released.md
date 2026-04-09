---
layout: post
title: "Drools 4.0.3 Released"
date: 2007-10-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/10/drools-4-0-3-released.html
---

We just [released Drools v4.0.3](<http://labs.jboss.com/drools/downloads.html>). This is a minor release with a few improvements on existing features and some bug fixes.

Release Notes – JBoss Drools – Version 4.0.3

We would like to really thanks all the contributors that helped on getting this release out. From those contributing patches and docs, to those testing and reporting bugs and providing feedback. The list is a bit long to post all names here and I may incur in a mistake forgetting someone, so our open public thank you to you all!

Follows the release notes.

Happy Drooling  
Drools Team

## Bug

  * [[JBRULES-1264](<http://jira.jboss.com/jira/browse/JBRULES-1264>)] – NPE at BaseObjectClassFieldExtractor.getLongValue with null fields
  * [[JBRULES-1266](<http://jira.jboss.com/jira/browse/JBRULES-1266>)] – Composite facts types (OR, AND) not rendering correctly
  * [[JBRULES-1272](<http://jira.jboss.com/jira/browse/JBRULES-1272>)] – DSL : String index out of range: -1
  * [[JBRULES-1279](<http://jira.jboss.com/jira/browse/JBRULES-1279>)] – Memory leak in release 4.0.2
  * [[JBRULES-1281](<http://jira.jboss.com/jira/browse/JBRULES-1281>)] – ExecutorService cannot be shared
  * [[JBRULES-1282](<http://jira.jboss.com/jira/browse/JBRULES-1282>)] – Problems uploading models etc. into the BRMS
  * [[JBRULES-1283](<http://jira.jboss.com/jira/browse/JBRULES-1283>)] – Unable to serialize rule base ( NotSerializableException: org.drools.base.FireAllRulesRuleBaseUpdateListener)
  * [[JBRULES-1295](<http://jira.jboss.com/jira/browse/JBRULES-1295>)] – DSL Mapping files does not support comments and empty lines

## Feature Request

  * [[JBRULES-1252](<http://jira.jboss.com/jira/browse/JBRULES-1252>)] – DrlDumper does not dump import functions

## Task

  * [[JBRULES-1293](<http://jira.jboss.com/jira/browse/JBRULES-1293>)] – Backport for Eclipse 3.3
  * [[JBRULES-1294](<http://jira.jboss.com/jira/browse/JBRULES-1294>)] – Upgrade to MVEL 1.2.10