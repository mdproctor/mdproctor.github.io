---
layout: post
title: "Parallel Drools is coming - 12 core machine benchmark results"
date: 2016-06-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2016/06/parallel-drools-is-coming-12-core-machine-benchmark-results.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Parallel Drools is coming – 12 core machine benchmark results](<https://blog.kie.org/2016/06/parallel-drools-is-coming-12-core-machine-benchmark-results.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 1, 2016  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

We are working on a number of different usage patterns for multi-core processing. Our first attempt is at fireAllRules batch processing (no rule chaining) of 1000 facts against increasing 12, 48, 192, and 768 rules – one join per rule. The break even point is around 48 rules. Below 48 rules the running time was less than 100ms and the thread co-ordination costs starts to cancel out the advantage. But after 48 rules, things get better, much faster.

[![](/legacy/assets/images/2016/06/bc99b8b1c4e1-tzqAh1.jpg)![](/legacy/assets/images/2016/06/c4b344f24be2-tzqAh1.jpg)](<https://snag.gy/tzqAh1.jpg>)

Smaller is better (ms/op)

The running machine is 12 cores, which we put into 12 partitions and rules are evenly split across partitions. This is all organised by the engine, and not end user code. There are still a lot more improvements we can do, to get more optimal rule to partition assignment and to avoid sending all data to all partitions.

Next we’ll be turning out attention to long running fireUntilHalt stream use cases.

We don’t have any code yet that others can run, as it’s still a bit of hack. But as we progress, we’ll tidy things up and try and get it so others can try it.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2016%2F06%2Fparallel-drools-is-coming-12-core-machine-benchmark-results.html&linkname=Parallel%20Drools%20is%20coming%20%E2%80%93%2012%20core%20machine%20%20benchmark%20results> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2016%2F06%2Fparallel-drools-is-coming-12-core-machine-benchmark-results.html&linkname=Parallel%20Drools%20is%20coming%20%E2%80%93%2012%20core%20machine%20%20benchmark%20results> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2016%2F06%2Fparallel-drools-is-coming-12-core-machine-benchmark-results.html&linkname=Parallel%20Drools%20is%20coming%20%E2%80%93%2012%20core%20machine%20%20benchmark%20results> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2016%2F06%2Fparallel-drools-is-coming-12-core-machine-benchmark-results.html&linkname=Parallel%20Drools%20is%20coming%20%E2%80%93%2012%20core%20machine%20%20benchmark%20results> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2016%2F06%2Fparallel-drools-is-coming-12-core-machine-benchmark-results.html&linkname=Parallel%20Drools%20is%20coming%20%E2%80%93%2012%20core%20machine%20%20benchmark%20results> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2016%2F06%2Fparallel-drools-is-coming-12-core-machine-benchmark-results.html&linkname=Parallel%20Drools%20is%20coming%20%E2%80%93%2012%20core%20machine%20%20benchmark%20results> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2016%2F06%2Fparallel-drools-is-coming-12-core-machine-benchmark-results.html&linkname=Parallel%20Drools%20is%20coming%20%E2%80%93%2012%20core%20machine%20%20benchmark%20results> "Email")
  *[]: 2010-05-25T16:11:00+02:00