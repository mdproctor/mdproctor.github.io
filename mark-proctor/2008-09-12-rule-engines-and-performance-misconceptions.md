---
layout: post
title: "Rule Engines and Performance Misconceptions"
date: 2008-09-12
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/09/rule-engines-and-performance-misconceptions.html
---

I’m starting to see a misconception between users on rule engine performance. They seem to struggle on why you can hand craft some java code and get better performance than a rule engine, and then wonder what the value of a rule engine is. For most veterans this is obvious, it’s always possible for an experience developer to write faster code if you write a custom algorithm with all the correct data structures and indexes, some times order of magnitudes, as you know exactly which bits to optimise. The same is also true for work flow. At the more basic level a “for” loop in java is always going to outperform a ReteOO network representation of a “for” loop (although ReteOO bytecode generation and flattening will help here).

ReteOO, our enhanced implementation of Rete, is a generic algorithm with generic optimisations further to that it is interpreted to easily support dynamic rules at runtime. Hand crafted algorithms will always outperform generic algorithms. The point of a rule engine is it provides “good enough” performance while giving you the added benefits of declarative programming and the various authoring metaphors, improved maintenance, ability to grow in complexity in a sane way, enterprise management. You may also find that your hand crafted engine might start to scale poorly, compared to a rule engine, after 3 different developers have slapped on their enhancements over the years.

Simply put, you aren’t going to write a video codec in a rule engine. But if you are going to write a business or a monitoring problem who’s complexity is going to grow over time then the idea of maintaining spaghetti java code over the years might not appeal to you, and the rule engine performance will be “good enough” that the performance side is no longer the main consideration in your solution.

Drools performance at the moment is “good enough” in most cases where users have performance issues the matter can be dealt with by a change in approach. That said there is still a lot we can do to get increased performance, and we will continue to improve over time. For example we can flatten a ReteOO network down into bytecode methods to get native level java performance (for those that don’t care about dynamic capabilities), we can add indexing for literals and variables on !=, <, >, <= and >=. Those two alone, when we do them, should provide a robust increase in performance. But we also need to start targeting memory usage, looking at disk paging solutions to assist.

Something else I always tell people is that if you have a large application written in Drools that you can make public we can look over it and see what optimisations that can be done to Drools to improve it’s performance. We’d rather have user driven performance enhancements than blindly adding benchmark/academic driven enhancements.