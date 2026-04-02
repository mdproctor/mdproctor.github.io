---
layout: post
title: "JBoss Drools 4.0 Released"
date: 2007-07-25
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/jboss-drools-4-0-released.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [JBoss Drools 4.0 Released](<https://blog.kie.org/2007/07/jboss-drools-4-0-released.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 25, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Release](<https://blog.kie.org/content_type/release>)

JBoss Drools 4.0 has just been released :) We are really proud of what we have done here. We believe that we now have the best and most powerful declarative rule language, bar none; commercial or open source. The Rule Flow is excellent and I really enjoyed updating the Conway’s Game of Life to Rule Flow; sub Rule Flows and milestone support will be coming in a point release soon. The BRMS has long been requested and we put a lot of effort into the ajax based design. The Eclipse improvements for the debug points and guided editor should help reduce learning curves, opening us to new audiences. Of course performance is now much better, especially for complex rules and the new Sequential Mode should be very popular with decision services.

Boss Drools 4.0 can be summarised as:  
* More expressiveness.  
* More powerful declarative keywords.  
* Hibernate ready, with ‘from’ keyword for evaluating external data.  
* Pluggable dialects, with new MVEL dialect.  
* New Rule Flow and Eclipse modeller.  
* Better Performance.  
* IDE Improvements.  
* Enterprise Ready with Web 2.0 Business Rules Management Studio.

Resources:  
* Presentation from Skills Matter http://wiki.jboss.org/wiki/attach?page=JBossRules%2FSkillsMatter20070711.pdf  
* What’s new in JBoss Rules 4.0 http://wiki.jboss.org/wiki/attach?page=JBossRules%2Fwhats_new_in_jbossrules_4.0.pdf

Enjoy :)  
The Drools Team  
Mark Proctor, Michael Neale, Edson Tirelli, Kris Verlaenen, Fernando Meyer  
[http://blog.athico.com](<http://blog.athico.com/>)

Here is a more detailed enhancements list:  
Language Expressiveness Enhancements  
* New Conditional Elements: from(hibernate ready), collect, accumulate and forall  
* New Field Constraint operators: not matches, not contains, in, not in, memberOf, not memberOf  
* New Implicit Self Reference field: this  
* Full support to Conditional Elements nesting, for First Order Logic completeness.  
* Support to multi-restrictions and constraint connectives && and ||  
* Parser improvements to remove previous language limitations, like character escaping and keyword conflicts  
* Support to pluggable dialects and built-in support to Java and MVEL  
* Complete rewrite of DSL engine, allowing for full l10n  
* Fact attributes auto-vivification for return value restrictions and inline-eval constraints  
* Support to nested accessors, property navigation and simplified collection, arrays and maps syntax  
* Improved support to XML rules  
* Experimental Clips parser support

Core Engine Enhancements  
* Native support to primitive types, avoiding constant autoboxing  
* Transparent optional Shadow Facts  
* Rete Network performance improvements for complex rules  
* Rule-Flow  
* Stateful and Stateless working memories (rule engine sessions)  
* Support for Asynchronous Working Memory actions  
* Rules Engine Agent for hot deployment and BRMS integration  
* Pluggeable dialects and and full support to MVEL scripting language  
* Dynamic salience for rules conflict resolution  
* Parameterized Queries  
* halt command  
* Sequential execution mode, faster performance and uses less memory  
* Pluggable global variable resolver

IDE Enhancements  
* Support for rule break-points on debugging  
* WYSIWYG support to rule-flows  
* New guided editor for rules authoring  
* Upgrade to support all new engine features

Business Rules Management System – BRMS  
* User friendly web interface with nice WEB 2.0 ajax features (GWT)  
* Package configuration  
* Rule Authoring easy to edit rules both with guided editor ( drop-down menus ) and text editor  
* Package compilation and deployment  
* Easy deployment with Rule Agent  
* Easy to organize with categories and search assets  
* Versioning enabled, you can easily replace yours assets with previously saved  
* JCR compliant rule assets repository

Miscellaneous Enhancements  
* Slimmed down dependencies and smaller memory footprint

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-4-0-released.html&linkname=JBoss%20Drools%204.0%20Released> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-4-0-released.html&linkname=JBoss%20Drools%204.0%20Released> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-4-0-released.html&linkname=JBoss%20Drools%204.0%20Released> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-4-0-released.html&linkname=JBoss%20Drools%204.0%20Released> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-4-0-released.html&linkname=JBoss%20Drools%204.0%20Released> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-4-0-released.html&linkname=JBoss%20Drools%204.0%20Released> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-4-0-released.html&linkname=JBoss%20Drools%204.0%20Released> "Email")