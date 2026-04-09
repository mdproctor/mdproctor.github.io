---
layout: post
title: "OpenRules Rule Compressor"
date: 2008-02-29
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/02/openrules-rule-compressor.html
---

The people over at [OpenRules](<http://openrules.com/>) have developed some very cool technology with their [Rule Compressor](<http://openrules.com/RuleCompressor.htm>). Given any decision table the compressor looks for redundant rule combinations and removes them.

If I have two rows in the decision table that look like this:  
if age > 50 then decrease price by 10%  
if age > 65 then decrease price by 10%

We have redundancy there and it can be combined into a single rule:  
if age > 50 then decrease price by 10%

This is obviously a very simple case and the Rule Compressor can do much more complex combinations. I’ve taken the liberty of taking a screen shot from a section showing an example from their [Rule Compressor](<http://openrules.com/RuleCompressor.htm>) explanation page:

![](/legacy/assets/images/2008/02/55b095d5a4d8-RuleCompressor.png)