---
layout: post
title: "Drools 3.1 Milestone 1"
date: 2007-02-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/02/drools-3-1-milestone-1.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools 3.1 Milestone 1](<https://blog.kie.org/2007/02/drools-3-1-milestone-1.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 19, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Release](<https://blog.kie.org/content_type/release>)

3.1-M1 is now avaliable.

[Release Notes](<http://wiki.jboss.org/wiki/Wiki.jsp?page=3.1M1ReleaseNotes>)  
[Downloads](<http://labs.jboss.com/portal/jbossrules/downloads>)

Drools 3.1 is the development cycle for the eventually JBoss Rules 3.2 stable release, although the current feature set is looking like this might become 4.0. 3.1-M1 is the first milestone release, which provides an unstable snapshot of the features to date. The documentation will not be updated until the end of the development cycle. The BRMS is not quite ready yet, but should be included in an upcoming milestone release.

New language features

  * ‘collect’
    * Reasoning over sets of data, i.e. when you have atleast 6 red buses
  * ‘accumulate’
    * Reason and execute actions of sets of data, .i.e allows for summations, averages or other set based calculations.
  * ‘forall’
    * The pattern is true for all facts in the working memory
  * ‘from’
    * allows for reasoning over facts not in the working memory, this works with globals to pull data locally from services, such as a hibernate session.
  * multi restriction connective field constraints with & and |
    * & and | can now be used on fields inside a Pattern, Person(hair == “blue” | == “brown” )
  * Nested Conditional Elements
    * ‘and’ and ‘or’ can now be nested inside ‘not’ and ‘exists’
  * Keyword conflicts resolved
  * Primitive support
    * Primitives are no longer autoboxed
  * FactTemplates
    * Facts can be declared inside the DRL, with no need for a corresponding pojos.
  * Shadow Facts
    * asserted pojos have their values shadowed to ensure the integrity of the working memory against changes made to facts outside of the working memory.

New IDE features

  * Breakpoints in consequences and functions
  * Context assist for all new language features
  * Outline Filtering
  * New GEF based Rete viewer

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F02%2Fdrools-3-1-milestone-1.html&linkname=Drools%203.1%20Milestone%201> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F02%2Fdrools-3-1-milestone-1.html&linkname=Drools%203.1%20Milestone%201> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F02%2Fdrools-3-1-milestone-1.html&linkname=Drools%203.1%20Milestone%201> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F02%2Fdrools-3-1-milestone-1.html&linkname=Drools%203.1%20Milestone%201> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F02%2Fdrools-3-1-milestone-1.html&linkname=Drools%203.1%20Milestone%201> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F02%2Fdrools-3-1-milestone-1.html&linkname=Drools%203.1%20Milestone%201> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F02%2Fdrools-3-1-milestone-1.html&linkname=Drools%203.1%20Milestone%201> "Email")