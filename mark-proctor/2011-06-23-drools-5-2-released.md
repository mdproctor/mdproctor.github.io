---
layout: post
title: "Drools 5.2 released"
date: 2011-06-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/06/drools-5-2-released.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools 5.2 released](<https://blog.kie.org/2011/06/drools-5-2-released.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 23, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Release](<https://blog.kie.org/content_type/release>)

We’re pleased to announce**the release of Drools (Expert, Fusion, Planner, Guvnor) 5.2.0.Final**.

This is quite an exciting release as Drools has now become a hybrid chaining engine, capable of executing both the reactive forward chaining rules and now prolog style backward chaining rules for derivation queries. We’ve added a lot more depth and maturity to the business rules authoring with top notch decision tables and rule templates

At the same time[ jBPM5.1](<http://kverlaen.blogspot.com/2011/06/jbpm-510-released.html>) has also been release, with full details [here](<http://kverlaen.blogspot.com/2011/06/jbpm-510-released.html>):

We’ve closed a huge number of issues in JIRA:  
Drools 286  
Guvnor 270

[![](/legacy/assets/images/2011/06/81cadf80181c-dtable-merged.png)](<http://4.bp.blogspot.com/-wUrb1xdL0r8/TgOPLpeA_0I/AAAAAAAAAfo/vO8iasdjYIQ/s1600/dtable-merged.png>)

  * Download the zips from [the drools download page](<http://www.jboss.org/drools/downloads>).
  * See the JBoss Maven repository for [a list of all released artifacts](<https://repository.jboss.org/nexus/index.html#nexus-search;gav~org.drools*~~5.2.0.Final~~>).
    * Note: if you’re coming from 5.1.0, some artifacts have a [new artifactId](<http://docs.jboss.org/drools/release/5.2.0.Final/droolsjbpm-introduction-docs/html/ch02.html#d0e397>).

# New and Noteworthy

## Core

  * MVEL
The MVEL dialect has been improved. All variable lookups have been moved to new indexed factories, which should allow faster execution, as well as being simpler code. The build process for MVEL has been reviewed to streamline it to avoid wasteless object creation so that the build time is faster. The ParserConfiguration is now shared which will make each MVEL compilation unit faster to initalise. Configurable type-safety has also been added.
  * Classloader
The Classloader has been improved to use a CompositeClassLoader instead of the previous hierarchical “parent” classloader to better support use of Drools within OSGi containers.

See [here](<http://docs.jboss.org/drools/release/5.2.0.Final/droolsjbpm-introduction-docs/html/ch02.html#d0e50>) for details.

## Drools Expert and Fusion

  * Lazy Truth Maintenance
You no longer need to enable or disable truth maintenance, via the kbase configuration. It is now handled automatically and turned on only when needed.
  * Multi-function Accumulates
The accumulate CE now supports multiple functions.
  * Parameterized constructors for declared types
Generate constructors with parameters for declared types.
  * Type Declaration ‘extends’
Type declarations now support ‘extends’ keyword for inheritance.
  * Free Form expressions in Constraints (New Parser)
The parser has been rewritten. We had reached the limitations of what we could achieve in pure ANTLR and moved to a hybrid parser, that adds flexibility to the language. The main benefit with the new parser is that the language now supports free form expressions for constraints and ‘from’ statements.
  * Rule API
A fluent API was created to allow programmatic creation of rules as an alternative to the previously suggested method of template creation.
  * Positional Arguments
Patterns now support positional arguments on type declarations.
  * Backward Chaining
Drools now provides Prolog style derivation queries, as an experimental feature.
  * Non Typesafe Classes
Annotation @typesafe( ) has been added to type declarations allowing for the configuration of type-safe evaluation of constraints.
  * Session Reports
An experimental framework to inspect a session and generate a report, either based on a predefined template or with a user created template, has been added.
  * Improved Camel integration
Camel integration using the Drools EndPoint was improved with the creation of both DroolsConsumer and DroolsProducer components.

See [here](<http://docs.jboss.org/drools/release/5.2.0.Final/droolsjbpm-introduction-docs/html/ch02.html#d0e72>) for details.

## Guvnor

  * Guvnor Look & Feel; moving closer to native GWT
We have removed GWT-Ext from Guvnor and now only use GWT.
  * Embed Guvnor Editors
We have added the ability to embed Guvnor Editor’s in external applications.
  * Annotations come to Declarative Models
The ability to add annotations in Guvnor to declarative models has been added.
  * Support for Complex Event Processing in the guided editors
The guided editors have been enhanced to allow full use of Drools Fusion’s Complex Event Processing operators, sliding windows and entry-points.
  * New guided decision table
The existing Guided Decision Table has been replaced to provide a foundation on which to build our future guided Decision Table toolset. The initial release largely provides an equivalent feature-set to the obsolete Guided Decision Table with a few improvements, as listed below.

  1. Cell Merging
  2. Merged Decision Table
  3. Typed-columns
  4. Improved header
  5. Fixed header when scrolling
  6. Negation of Fact patterns
  7. Negation of rules
  8. Support for “otherwise”

* Enhanced Package’s Report
Templates Rules and Decision Tables rules are now included in the package’s report.
* Spring Context Editor
Now it is possible to create and mange Spring Context files inside Guvnor.
* Configuring Multiple Guvnor Instances In a Jackrabbit
We added a new task in drools-ant which helps with configuring multiple Guvnor instances to be able to share their Jackrabbit content.
* Configuring Guvnor to use an external RDBMS made easier
We added a new section under the “Administration” tab called “Repository Configuration” which helps generate the repository.xml configuration file for a number of databases.

See [here](<http://docs.jboss.org/drools/release/5.2.0.Final/droolsjbpm-introduction-docs/html/ch02.html#d0e218>) for details.

## Eclipse

  * Removal of BRL Guided Editor
The BRL Guided Editor has been removed due to lack of interest and it falling behind.
See [here](<http://docs.jboss.org/drools/release/5.2.0.Final/droolsjbpm-introduction-docs/html/ch02.html#d0e389>) for details.

# Thank you

We would like to thank all the drools community members who helped made this release possible. [The Drools team](<http://www.jboss.org/drools/team>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Fdrools-5-2-released.html&linkname=Drools%205.2%20released> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Fdrools-5-2-released.html&linkname=Drools%205.2%20released> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Fdrools-5-2-released.html&linkname=Drools%205.2%20released> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Fdrools-5-2-released.html&linkname=Drools%205.2%20released> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Fdrools-5-2-released.html&linkname=Drools%205.2%20released> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Fdrools-5-2-released.html&linkname=Drools%205.2%20released> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Fdrools-5-2-released.html&linkname=Drools%205.2%20released> "Email")
  *[]: 2010-05-25T16:11:00+02:00