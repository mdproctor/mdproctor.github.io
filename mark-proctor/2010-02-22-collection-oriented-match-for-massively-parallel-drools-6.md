---
layout: post
title: "Collection-oriented Match for massively parallel Drools 6"
date: 2010-02-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/02/collection-oriented-match-for-massively-parallel-drools-6.html
---

With multi-cores becoming ever cheaper the desire to push Drools into parallel processing is increasing. We’ve already added rulebase partitioning, which helps throughput for CEP type problems, but that doesn’t solve the parallel matching.

I’ve followed [ParaOPS5](<http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.612>), but wasn’t comfortable enough that the design would deliver universal speed improvements compared to the complexity it brings. With ParaOPS5 each partial match when propagated to a node for evaluation was submitted to a queue for evaluation as a “task”. This produces something that is very fine grained, and as a node, or potentially the index in a node is a locking point, there is a lot of waiting around for very small units of work.

A while back I stumbled across this paper [“Collection-Oriented Match by Anurag Acharya and Milind Tambe”](<http://teamcore.usc.edu/papers/1993/cikm-final.pdf>). The paper is well written and relatively easy to understand. Here it proposes instead of propagating the partial match once it’s created, it instead stays in the node and produce all partial matches which are stored in a collection, it’s this collection we then propagate. This propagated collection is submitted as a “task” to the queue. This allows for larger units of work, as more is done in the node itself. The approach is not without it’s problems, particularly around left indexing, as partial matches in the same propagated collection could be in different indexes for the node.

However we feel that this shows a lot of promise and have decided to explore this as the underlying algorithm for Drools 6. We’ll hopefully have a basic prototype working this summer, and then we’ll have some ideas on advantages and disadvantages.