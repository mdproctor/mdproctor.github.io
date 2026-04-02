---
layout: post
title: "Reactive Incremental Graph Reasoning with Drools"
date: 2015-03-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/03/reactive-incremental-graph-reasoning-with-drools.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Reactive Incremental Graph Reasoning with Drools](<https://blog.kie.org/2015/03/reactive-incremental-graph-reasoning-with-drools.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 13, 2015  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Today Mario got a first working version for incremental reactive graphs with Drools. This means people no longer need to flatten their models to a purely relational representation to get reactivity. It provides a hybrid language and engine for both relational and graph based reasoning. To differentiate between relational joins and reference traversal a new XPath-like was introduced, that can be used inside of patterns. Like XPath it supports collection iteration.

Here is a simple example, that finds all men in the working memory:  
Man( $toy: /wife/children[age > 10]/toys )

For each man it navigates the wife reference then the children reference; the children reference is a list. For each child in the list that is over ten it will navigate to its toy’s list. With the XPath notation if the leaf property is collection it will iterate it, and the variable binds to each iteration value. If there are two children over the age of 10, who have 3 toys each, it would execute 6 times.

As it traverses each reference a hook is injected to support incremental reactivity. If a new child is added or removed, or if an age changes, it will propagate the incremental changes. The incremental nature means these hooks are added and removed as needed, which keeps it efficient and light.

You can follow some of the unit tests here:  
<https://github.com/mariofusco/drools/blob/xpath/drools-compiler/src/test/java/org/drools/compiler/xpath/XpathTest.java>

It’s still very early pre-alpha stuff, but I think this is exciting stuff.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Freactive-incremental-graph-reasoning-with-drools.html&linkname=Reactive%20Incremental%20Graph%20Reasoning%20with%20Drools> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Freactive-incremental-graph-reasoning-with-drools.html&linkname=Reactive%20Incremental%20Graph%20Reasoning%20with%20Drools> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Freactive-incremental-graph-reasoning-with-drools.html&linkname=Reactive%20Incremental%20Graph%20Reasoning%20with%20Drools> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Freactive-incremental-graph-reasoning-with-drools.html&linkname=Reactive%20Incremental%20Graph%20Reasoning%20with%20Drools> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Freactive-incremental-graph-reasoning-with-drools.html&linkname=Reactive%20Incremental%20Graph%20Reasoning%20with%20Drools> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Freactive-incremental-graph-reasoning-with-drools.html&linkname=Reactive%20Incremental%20Graph%20Reasoning%20with%20Drools> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Freactive-incremental-graph-reasoning-with-drools.html&linkname=Reactive%20Incremental%20Graph%20Reasoning%20with%20Drools> "Email")
  *[]: 2010-05-25T16:11:00+02:00