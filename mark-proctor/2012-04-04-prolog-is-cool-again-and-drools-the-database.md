---
layout: post
title: "Prolog is Cool Again and Drools the DataBase"
date: 2012-04-04
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/04/prolog-is-cool-again-and-drools-the-database.html
---

Rich Hickey has just done a interview at InfoQ on Datomic  
<http://www.infoq.com/interviews/hickey-datomic>

In his talk he highlights their adoption of DataLog for their query format, and a transition away from an SQL approach to a rule based approach. DataLog is a Prolog derivitive, <http://en.wikipedia.org/wiki/Datalog>. It’s great to see Prolog and rule based systems for query capabilities getting more attention again.

We added Prolog like capabilities to Drools earlier this year, that provides both queries but also reactive materialised views:  
<http://blog.athico.com/2011/04/backward-chaining-emerges-in-drools.html>

We are currently working on some proof of concepts around transactions and persistent data structures in Drools, along with OrientDB integration. So I hope we can see Drools the DataBase, via OrientBD integration before end of this summer.