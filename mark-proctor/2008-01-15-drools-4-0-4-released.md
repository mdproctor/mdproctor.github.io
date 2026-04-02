---
layout: post
title: "Drools 4.0.4 Released"
date: 2008-01-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/01/drools-4-0-4-released.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools 4.0.4 Released](<https://blog.kie.org/2008/01/drools-4-0-4-released.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 15, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Release](<https://blog.kie.org/content_type/release>)

We just [released Drools v4.0.4](<http://labs.jboss.com/drools/downloads.html>). This is a minor release with a few improvements on existing features and some bug fixes.

Release Notes – JBoss Drools – Version 4.0.4

We would like to really thanks all the contributors that helped on getting this release out. From those contributing patches and docs, to those testing and reporting bugs and providing feedback. The list is a bit long to post all names here and I may incur in a mistake forgetting someone, so our open public thank you to you all!

Follows the release notes.

Happy Drooling  
Drools Team

Release Notes – JBoss Drools – Version 4.0.4

## Bug

  * [[JBRULES-1243](<http://jira.jboss.com/jira/browse/JBRULES-1243>)] – Pattern matching does not allow spaces

  * [[JBRULES-1274](<http://jira.jboss.com/jira/browse/JBRULES-1274>)] – NPE when using reserved word “action” as a bound variable, or omitting rule title

  * [[JBRULES-1284](<http://jira.jboss.com/jira/browse/JBRULES-1284>)] – ClassCastException when using “

  * [[JBRULES-1310](<http://jira.jboss.com/jira/browse/JBRULES-1310>)] – java.lang.NullPointerException at org.drools.rule.builder.dialect.java.JavaConsequenceBuilder.build(JavaConsequenceBuilder.java:54)

  * [[JBRULES-1311](<http://jira.jboss.com/jira/browse/JBRULES-1311>)] – NPE when compiling rule consequences

  * [[JBRULES-1313](<http://jira.jboss.com/jira/browse/JBRULES-1313>)] – NullPointerException at JavaConsequenceBuilder.java:54 on RHS for simplest of consequences

  * [[JBRULES-1314](<http://jira.jboss.com/jira/browse/JBRULES-1314>)] – Error parsing rule that is written in a single line

  * [[JBRULES-1316](<http://jira.jboss.com/jira/browse/JBRULES-1316>)] – Serialising Both the RuleBase and WorkingMemory throws null pointer

  * [[JBRULES-1317](<http://jira.jboss.com/jira/browse/JBRULES-1317>)] – Rule Execution Very Slow on Subsequent Session Using the Same Packages

  * [[JBRULES-1321](<http://jira.jboss.com/jira/browse/JBRULES-1321>)] – org.drools.compiler.DroolsParserException: Unknown error while parsing.  
org.drools.compiler.DroolsParserException: Unknown error while parsing.

  * [[JBRULES-1325](<http://jira.jboss.com/jira/browse/JBRULES-1325>)] – OutOfMemory with the use of WorkingMemoryFileLogger

  * [[JBRULES-1336](<http://jira.jboss.com/jira/browse/JBRULES-1336>)] – Typo in RuleBaseConfiguration(ClassLoader classLoder, Properties properties) — the ClassLoader specified in the constructor args is not used

  * [[JBRULES-1337](<http://jira.jboss.com/jira/browse/JBRULES-1337>)] – ‘or’ with predicate/return val/inline eval with property issue

  * [[JBRULES-1339](<http://jira.jboss.com/jira/browse/JBRULES-1339>)] – Debugging: Breakpoints are only considered for code with variables

  * [[JBRULES-1340](<http://jira.jboss.com/jira/browse/JBRULES-1340>)] – JBRMS – Admin – Manage Archived Assets – Open item icon not opening item

  * [[JBRULES-1348](<http://jira.jboss.com/jira/browse/JBRULES-1348>)] – Incorrect hash code calculation for character attributes in alpha hashing optimization

  * [[JBRULES-1354](<http://jira.jboss.com/jira/browse/JBRULES-1354>)] – Duplicate parameter error while trying to use pattern bound variables or globals in accumulate function

  * [[JBRULES-1364](<http://jira.jboss.com/jira/browse/JBRULES-1364>)] – Drl parser ‘or’

  * [[JBRULES-1387](<http://jira.jboss.com/jira/browse/JBRULES-1387>)] – Drools doesn’t build with fresh maven2 installation and no repository

  * [[JBRULES-1397](<http://jira.jboss.com/jira/browse/JBRULES-1397>)] – org.mvel.CompileException: variable already defined within scope

  * [[JBRULES-1410](<http://jira.jboss.com/jira/browse/JBRULES-1410>)] – Rules with Collect / Accumulate CEs not working correctly when dinamically added to a rulebase

  * [[JBRULES-1412](<http://jira.jboss.com/jira/browse/JBRULES-1412>)] – ContextEntries should have cache nulled

  * [[JBRULES-1413](<http://jira.jboss.com/jira/browse/JBRULES-1413>)] – KnowledgeHelper should have cache reset before use.

  * [[JBRULES-1416](<http://jira.jboss.com/jira/browse/JBRULES-1416>)] – The use of HashKey is not thread safe in CompositeObjectSinkAdapter

## Feature Request

  * [[JBRULES-1308](<http://jira.jboss.com/jira/browse/JBRULES-1308>)] – getFactHandle with equality-based assert behavior

  * [[JBRULES-1349](<http://jira.jboss.com/jira/browse/JBRULES-1349>)] – NotNode and Exists Improvements

  * [[JBRULES-1395](<http://jira.jboss.com/jira/browse/JBRULES-1395>)] – Add support to modify() block in java dialect consequences

## Patch

  * [[JBRULES-1323](<http://jira.jboss.com/jira/browse/JBRULES-1323>)] – Add caching to the Objenesis instance and move instance to the RuleBase level

## Task

  * [[JBRULES-1421](<http://jira.jboss.com/jira/browse/JBRULES-1421>)] – Update mvel version to 1.2.21 and update mvel templates

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F01%2Fdrools-4-0-4-released.html&linkname=Drools%204.0.4%20Released> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F01%2Fdrools-4-0-4-released.html&linkname=Drools%204.0.4%20Released> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F01%2Fdrools-4-0-4-released.html&linkname=Drools%204.0.4%20Released> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F01%2Fdrools-4-0-4-released.html&linkname=Drools%204.0.4%20Released> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F01%2Fdrools-4-0-4-released.html&linkname=Drools%204.0.4%20Released> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F01%2Fdrools-4-0-4-released.html&linkname=Drools%204.0.4%20Released> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F01%2Fdrools-4-0-4-released.html&linkname=Drools%204.0.4%20Released> "Email")