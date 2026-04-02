---
layout: post
title: "Collection-oriented Match for massively parallel Drools 6"
date: 2010-02-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/02/collection-oriented-match-for-massively-parallel-drools-6.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Collection-oriented Match for massively parallel Drools 6](<https://blog.kie.org/2010/02/collection-oriented-match-for-massively-parallel-drools-6.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 22, 2010  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

With multi-cores becoming ever cheaper the desire to push Drools into parallel processing is increasing. We’ve already added rulebase partitioning, which helps throughput for CEP type problems, but that doesn’t solve the parallel matching.

I’ve followed [ParaOPS5](<http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.612>), but wasn’t comfortable enough that the design would deliver universal speed improvements compared to the complexity it brings. With ParaOPS5 each partial match when propagated to a node for evaluation was submitted to a queue for evaluation as a “task”. This produces something that is very fine grained, and as a node, or potentially the index in a node is a locking point, there is a lot of waiting around for very small units of work.

A while back I stumbled across this paper [“Collection-Oriented Match by Anurag Acharya and Milind Tambe”](<http://teamcore.usc.edu/papers/1993/cikm-final.pdf>). The paper is well written and relatively easy to understand. Here it proposes instead of propagating the partial match once it’s created, it instead stays in the node and produce all partial matches which are stored in a collection, it’s this collection we then propagate. This propagated collection is submitted as a “task” to the queue. This allows for larger units of work, as more is done in the node itself. The approach is not without it’s problems, particularly around left indexing, as partial matches in the same propagated collection could be in different indexes for the node.

However we feel that this shows a lot of promise and have decided to explore this as the underlying algorithm for Drools 6. We’ll hopefully have a basic prototype working this summer, and then we’ll have some ideas on advantages and disadvantages.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fcollection-oriented-match-for-massively-parallel-drools-6.html&linkname=Collection-oriented%20Match%20for%20massively%20parallel%20Drools%206> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fcollection-oriented-match-for-massively-parallel-drools-6.html&linkname=Collection-oriented%20Match%20for%20massively%20parallel%20Drools%206> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fcollection-oriented-match-for-massively-parallel-drools-6.html&linkname=Collection-oriented%20Match%20for%20massively%20parallel%20Drools%206> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fcollection-oriented-match-for-massively-parallel-drools-6.html&linkname=Collection-oriented%20Match%20for%20massively%20parallel%20Drools%206> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fcollection-oriented-match-for-massively-parallel-drools-6.html&linkname=Collection-oriented%20Match%20for%20massively%20parallel%20Drools%206> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fcollection-oriented-match-for-massively-parallel-drools-6.html&linkname=Collection-oriented%20Match%20for%20massively%20parallel%20Drools%206> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fcollection-oriented-match-for-massively-parallel-drools-6.html&linkname=Collection-oriented%20Match%20for%20massively%20parallel%20Drools%206> "Email")