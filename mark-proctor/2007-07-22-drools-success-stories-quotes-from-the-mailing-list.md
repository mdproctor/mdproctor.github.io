---
layout: post
title: "Drools Success Stories - quotes from the mailing list"
date: 2007-07-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/drools-success-stories-quotes-from-the-mailing-list.html
---

“We are using Drools VERY succesfuly around 3 years (We started with version 2.x). And it has being so usefull that now we have a very big system running on more than one customer in telecom market.  
…  
Currently we do have a server running around 300 rules, where we assert millions of facts at once. The objective is to guide and rate telecom usage events. We are able to apply those 300 rules over 20 Milion facts and get results (Guided and Rated) around 1 hour(Note: First we have to read many binary files, perform a charset conversion on data, load it in our object model, assert objects in working memory, apply around 200 rules to enrich the data, assert again in a new working memory, and rate the events accessing external RDBMS databases – caching results of course).”

“We tested several deployment and architecture variants (esp. for batch processing), with <100 Rules and <10 facts for each data-row within our batches, but a few million rows. Worked out fine.”

“We deployed a Drools based solution to a client in the pharmaceutical distribution world (Fortune 100 company :-). We used Drools to power the decisions an interactive voice ordering system. A small number of rules initially but growing constantly based on user metrics. System has been running for a couple of years now.”