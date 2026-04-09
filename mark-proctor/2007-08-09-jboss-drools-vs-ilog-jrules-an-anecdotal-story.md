---
layout: post
title: "JBoss Drools vs ILog JRules - an anecdotal story"
date: 2007-08-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/08/jboss-drools-vs-ilog-jrules-an-anecdotal-story.html
---

A user recently contacted me to share their experience with ILog JRules and investigations into a possible Drools migration. I’ve pasted part of the conversation below (with permission), and it makes nice anecdotal reading, I’ve removed a lot of the more ranting criticism of JRules, many of which surprised me, just to avoid this becoming too controversial :)

You can also read my previous blog article to see more user success stories [Drools Success Stories – quotes from the mailing list](<http://blog.athico.com/2007/07/drools-success-stories-quotes-from.html>)

Snippets pasted from user email  
X is one of the largest ILOG users, paying millions for license fees …snip… We are satisfied about the rules engine (JRules) performance, but disappointed about the quality of rules management platform and their support …snip… I have been on the user email (Drools) list for a while, and am very impressed at the energy and expertise you and other core team members demonstrated.  
…snip…  
I reviewed Drools 4.0.0 right before the GA release, and created a benchmark to test the engine. The rules used in the benchmark were translated from one of the most critical ILOG rule set in production, about 1,300 rules. I was also pleased to find that the declarative DRL in the new release was so rich that it made converting IRL to DRL a relatively easy task. The same data set used in ILOG benchmark were used in this benchmark, and as I expressed in the previous message, the initial result was very good …snip… I would say that the benchmarks were very close to “Apple to Apple”.  
…snip…  
I look at open source offering such as Drools as the perfect fit for us. We did a lot of reverse engineering trying to understand how JRules works and used many of the un-documented API’s for some special business and technical requirements. It would be much easier if the source code were available.