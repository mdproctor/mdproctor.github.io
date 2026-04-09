---
layout: post
title: "NExpert Review (MacTech)"
date: 2009-08-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/08/nexpert-review-mactech.html
---

A while back James Owen did a blog on [“full opportunistic backward chaining”](<http://javarules.blogspot.com/2008/10/full-opportunistic-backward-chaining.html>). I’ve since found this old NExpert Object article, entitled [“PROGRAMMING IN NEXPERT”](<http://www.mactech.com/articles/mactech/Vol.02/02.03/ExpertSystems/>) that gives quite a nice overview including an explanation of NOTKNOWN and UKNOWN for opportunistic backward chaining in NEXPERT.

[“PROGRAMMING IN NEXPERT](<http://www.mactech.com/articles/mactech/Vol.02/02.03/ExpertSystems/>)  
…

[![](/legacy/assets/images/2009/08/60b425828079-nexpert.gif)](</assets/images/2009/08/a1de8c8057b4-nexpert.gif>)

…  
NEXPERT has two basic values that any datum may have: NOTKNOWN and UNKNOWN. NEXPERT uses UNKNOWN as the “reset” value. Whenever a datum’s value is needed and it is currently UNKNOWN, then NEXPERT will switch to backward chaining to attempt to establish a value from the data already available. If this is unsuccessful then the user is queried, via the Question Window, for a value. NOTKNOWN on the other hand, is used to mean that the user has been questioned and does not know the answer. NOTKNOWN allows default reasoning to be done and prevents NEXPERT from continuing to ask for a value that the user does not know.  
…  
Once the system reaches a rule that has some UNKNOWN datum in it, the user will be prompted for a value (see the example in Figure 3 below). At this point the user can access the multi-level Explanation Facility (via the WHY? and HOW? Buttons ), which is automatically built from the static forward and backward chains already in the rule-base.”