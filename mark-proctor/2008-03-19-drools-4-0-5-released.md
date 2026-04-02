---
layout: post
title: "Drools 4.0.5 Released"
date: 2008-03-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/03/drools-4-0-5-released.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools 4.0.5 Released](<https://blog.kie.org/2008/03/drools-4-0-5-released.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 19, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Release](<https://blog.kie.org/content_type/release>)

We just released Drools v4.0.5. This is a minor release with a few improvements on existing features and some bug fixes.

Release Notes – JBoss Drools – Version 4.0.5

We would like to really thanks all the contributors that helped on getting this release out. From those contributing patches and docs, to those testing and reporting bugs and providing feedback. The list is a bit long to post all names here and I may incur in a mistake forgetting someone, so our open public thank you to you all!

Follows the release notes.

Release Notes – JBoss Drools – Version 4.0.5

## Bug

  * [[JBRULES-1286](<http://jira.jboss.com/jira/browse/JBRULES-1286>)] – Incorrect information in section 2.5.7.3. Agenda Filters
  * [[JBRULES-1315](<http://jira.jboss.com/jira/browse/JBRULES-1315>)] – Rule that uses a ‘collect’ and ‘from’ clause together causes problem
  * [[JBRULES-1327](<http://jira.jboss.com/jira/browse/JBRULES-1327>)] – drools-ant task and java.lang.ClassCastException: org.drools.reteoo.ReteooRuleBase
  * [[JBRULES-1329](<http://jira.jboss.com/jira/browse/JBRULES-1329>)] – RuleBase.removeRule() prevents other rules from being applied
  * [[JBRULES-1330](<http://jira.jboss.com/jira/browse/JBRULES-1330>)] – Using RuleBase in multithread application server environment
  * [[JBRULES-1357](<http://jira.jboss.com/jira/browse/JBRULES-1357>)] – RuleBuildContext does not initialize package of rule
  * [[JBRULES-1388](<http://jira.jboss.com/jira/browse/JBRULES-1388>)] – Eval error when using multiple declarations
  * [[JBRULES-1389](<http://jira.jboss.com/jira/browse/JBRULES-1389>)] – using eval after using or causes ClassCastException
  * [[JBRULES-1392](<http://jira.jboss.com/jira/browse/JBRULES-1392>)] – Rules behave incorrectly (randomly) in multi-threaded environment
  * [[JBRULES-1414](<http://jira.jboss.com/jira/browse/JBRULES-1414>)] – Cannot build from source — missing directory or pom file
  * [[JBRULES-1415](<http://jira.jboss.com/jira/browse/JBRULES-1415>)] – Certain uses of from causes NullPointerException in WorkingMemoryLogger
  * [[JBRULES-1423](<http://jira.jboss.com/jira/browse/JBRULES-1423>)] – ObjectFactory$ObjectEqualsComparator.equals throws NPE if second arg is null
  * [[JBRULES-1426](<http://jira.jboss.com/jira/browse/JBRULES-1426>)] – NPE in ObjectFactory$ObjectEqualsComparator
  * [[JBRULES-1428](<http://jira.jboss.com/jira/browse/JBRULES-1428>)] – ClassCastException when comparing BigDecimal fields
  * [[JBRULES-1429](<http://jira.jboss.com/jira/browse/JBRULES-1429>)] – NPE in ObjectEqualsComparator
  * [[JBRULES-1435](<http://jira.jboss.com/jira/browse/JBRULES-1435>)] – NPE if rule checks a Long field for null, and a fact is passed in with Long field that is NOT null.
  * [[JBRULES-1436](<http://jira.jboss.com/jira/browse/JBRULES-1436>)] – Filescanner throws NPE when there’s a compile error.
  * [[JBRULES-1446](<http://jira.jboss.com/jira/browse/JBRULES-1446>)] – ClassCastException when iterating over an array using “from”
  * [[JBRULES-1447](<http://jira.jboss.com/jira/browse/JBRULES-1447>)] – Parser error when using keyword operators
  * [[JBRULES-1448](<http://jira.jboss.com/jira/browse/JBRULES-1448>)] – MVELDataProver throws nullpointer on null return value from expression
  * [[JBRULES-1451](<http://jira.jboss.com/jira/browse/JBRULES-1451>)] – LHS expression comparing a Boolean to a String does not fail but always returns true
  * [[JBRULES-1456](<http://jira.jboss.com/jira/browse/JBRULES-1456>)] – Or using DSL language
  * [[JBRULES-1459](<http://jira.jboss.com/jira/browse/JBRULES-1459>)] – parser/scanner bug: “unterminated literal”
  * [[JBRULES-1464](<http://jira.jboss.com/jira/browse/JBRULES-1464>)] – Comilation error : ‘Syntax error on token “,”, delete this token’ when referencing a global in an accumulate block
  * [[JBRULES-1467](<http://jira.jboss.com/jira/browse/JBRULES-1467>)] – Concurrency errors when parsing strings to dates in rules
  * [[JBRULES-1472](<http://jira.jboss.com/jira/browse/JBRULES-1472>)] – Problem when mixing alpha and beta constraints in a composite constraint
  * [[JBRULES-1477](<http://jira.jboss.com/jira/browse/JBRULES-1477>)] – User exception thrown from inside a rule always causes a stackTrace to console
  * [[JBRULES-1479](<http://jira.jboss.com/jira/browse/JBRULES-1479>)] – Exception compiling rules
  * [[JBRULES-1480](<http://jira.jboss.com/jira/browse/JBRULES-1480>)] – Potential multithreaded problem in MVELClassFieldExtractor
  * [[JBRULES-1481](<http://jira.jboss.com/jira/browse/JBRULES-1481>)] – Stop actionQueue recursion in working memory
  * [[JBRULES-1482](<http://jira.jboss.com/jira/browse/JBRULES-1482>)] – Bug with ReeteoRuleBase and merged package
  * [[JBRULES-1487](<http://jira.jboss.com/jira/browse/JBRULES-1487>)] – access to store property in MapBackedClassLoader should be synchronized
  * [[JBRULES-1489](<http://jira.jboss.com/jira/browse/JBRULES-1489>)] – Working Memory deserialization causes NPE
  * [[JBRULES-1490](<http://jira.jboss.com/jira/browse/JBRULES-1490>)] – org.drools.util.AbstractHashTable$SingleIndex is not serializable
  * [[JBRULES-1491](<http://jira.jboss.com/jira/browse/JBRULES-1491>)] – java.io.NotSerializableException: org.drools.util.AbstractHashTable$SingleIndex
  * [[JBRULES-1492](<http://jira.jboss.com/jira/browse/JBRULES-1492>)] – NPE caused by non-shadowed deep object access
  * [[JBRULES-1501](<http://jira.jboss.com/jira/browse/JBRULES-1501>)] – Multiples modify causes variable duplication exception
  * [[JBRULES-1503](<http://jira.jboss.com/jira/browse/JBRULES-1503>)] – Errors on rulebase serialization scenarios
  * [[JBRULES-1505](<http://jira.jboss.com/jira/browse/JBRULES-1505>)] – Fix CCE when using nested accessors to compare Date values
  * [[JBRULES-1506](<http://jira.jboss.com/jira/browse/JBRULES-1506>)] – RuleAgent will not read binary packages from Apache HTTP Server
  * [[JBRULES-1507](<http://jira.jboss.com/jira/browse/JBRULES-1507>)] – Objenesis too heavily used
  * [[JBRULES-1508](<http://jira.jboss.com/jira/browse/JBRULES-1508>)] – NPE in MVELDataProvider
  * [[JBRULES-1510](<http://jira.jboss.com/jira/browse/JBRULES-1510>)] – ObejnesisFactory.getStaticObjenesis() doesn’t set OBJENESIS_INSTANCE

## Feature Request

  * [[JBRULES-1307](<http://jira.jboss.com/jira/browse/JBRULES-1307>)] – Update and expand documentation for decision tables to show actual uses for all keywords
  * [[JBRULES-1338](<http://jira.jboss.com/jira/browse/JBRULES-1338>)] – DirectoryScanner should only take into account relevant files
  * [[JBRULES-1473](<http://jira.jboss.com/jira/browse/JBRULES-1473>)] – Add a configuration parameter to allow Drools to dump all generated java source code

## Patch

  * [[JBRULES-1452](<http://jira.jboss.com/jira/browse/JBRULES-1452>)] – Improved NullPointerException messages
  * [[JBRULES-1485](<http://jira.jboss.com/jira/browse/JBRULES-1485>)] – Fixes to the documentation

## Quality Risk

  * [[JBRULES-1475](<http://jira.jboss.com/jira/browse/JBRULES-1475>)] – Teensy spelling error in drools project template

## Task

  * [[JBRULES-1502](<http://jira.jboss.com/jira/browse/JBRULES-1502>)] – update example to use modify block as default

Happy Drooling  
Drools Team

Release Notes – JBoss Drools – Version 4.0.5

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-4-0-5-released.html&linkname=Drools%204.0.5%20Released> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-4-0-5-released.html&linkname=Drools%204.0.5%20Released> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-4-0-5-released.html&linkname=Drools%204.0.5%20Released> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-4-0-5-released.html&linkname=Drools%204.0.5%20Released> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-4-0-5-released.html&linkname=Drools%204.0.5%20Released> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-4-0-5-released.html&linkname=Drools%204.0.5%20Released> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-4-0-5-released.html&linkname=Drools%204.0.5%20Released> "Email")