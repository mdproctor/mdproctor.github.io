---
layout: post
title: "Scorecards and PMML4.1 support for Drools 5.5"
date: 2012-10-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/10/scorecards-and-pmml4-1-support-for-drools-5-5.html
---

Thanks to our super star community contributor, Vinod Kiran, score cards are coming to Drools 5.5. Initially the PMML4.1 standard is embedded for the Scorecards module. We have a full standalone PMML implementation coming for 6.0, being worked on by Dr Davide Sottara. I hope that Vinod will write a full tutorial in this blog soon, explaining the feature in more detail.

If you don’t know what a Scorecard is, here is a tutorial I found on google:  
<http://www.primatek.ca/blog/2010/08/16/a-quick-introduction-to-scorecards/>

Below is a text and image excerpt from the New and Noteworthy docs for the up coming Drools 5.5 release:

_A scorecard is a graphical representation of a formula used to calculate an overall score. A scorecard can be used to predict the likelihood or probability of a certain outcome. Drools now supports additive scorecards. An additive scorecard calculates an overall score by adding all partial scores assigned to individual rule conditions._  
_  
_  
_Additionally, Drools Scorecards will allows for reason codes to be set, which help in identifying the specific rules (buckets) that have contributed to the overall score. Drools Scorecards will be based on the PMML 4.1 Standard._   

[![](/legacy/assets/images/2012/10/a4886cb6734a-scorecard_asset_webeditor.png)](</assets/images/2012/10/97e3ec3bbc4a-scorecard_asset_webeditor.png>)