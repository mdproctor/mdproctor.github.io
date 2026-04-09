---
layout: post
title: "Rule Constraints and Code Constraints now works for Splits"
date: 2007-12-05
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/12/rule-constraints-and-code-constraints-now-works-for-splits.html
---

Recently I got the Drools dialect system working for processes, as discussed in [this](<http://blog.athico.com/2007/11/pluggable-dialects-for-drools-processes.html>) previous blog article. The dialect system is a pluggable framework to allow code to be written with different languages. Previously Split constraints would only work with rules, so the next stage was naturally to allow for constraints to work with code, like traditional process engines – ofcourse the code constraint would also work with the dialect system. Below is a screenshot of a Split node with both MVEL and Java code constraints and MVEL and Java rule constraints.

[![](/legacy/assets/images/2007/12/4df25d254580-splitnodes.png)](</assets/images/2007/12/09e2a5082fcb-splitnodes.png>)