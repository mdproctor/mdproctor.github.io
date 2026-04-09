---
layout: post
title: "Parallel Drools is coming - 12 core machine benchmark results"
date: 2016-06-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2016/06/parallel-drools-is-coming-12-core-machine-benchmark-results.html
---

We are working on a number of different usage patterns for multi-core processing. Our first attempt is at fireAllRules batch processing (no rule chaining) of 1000 facts against increasing 12, 48, 192, and 768 rules – one join per rule. The break even point is around 48 rules. Below 48 rules the running time was less than 100ms and the thread co-ordination costs starts to cancel out the advantage. But after 48 rules, things get better, much faster.

[![](/legacy/assets/images/2016/06/bc99b8b1c4e1-tzqAh1.jpg)![](/legacy/assets/images/2016/06/c4b344f24be2-tzqAh1.jpg)](<https://snag.gy/tzqAh1.jpg>)

Smaller is better (ms/op)

The running machine is 12 cores, which we put into 12 partitions and rules are evenly split across partitions. This is all organised by the engine, and not end user code. There are still a lot more improvements we can do, to get more optimal rule to partition assignment and to avoid sending all data to all partitions.

Next we’ll be turning out attention to long running fireUntilHalt stream use cases.

We don’t have any code yet that others can run, as it’s still a bit of hack. But as we progress, we’ll tidy things up and try and get it so others can try it.