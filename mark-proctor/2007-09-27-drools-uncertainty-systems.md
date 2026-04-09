---
layout: post
title: "Drools - Uncertainty Systems"
date: 2007-09-27
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/09/drools-uncertainty-systems.html
---

### Drools – Uncertainty Systems

Davide Sottara has been working on the foundations for a Drools partial data reasoning, for his Phd, with Uncertainty Systems to express truth degrees. He’s made a small screenshot for us along with the proposed syntax. The idea is that different uncertainty systems can be configured to handle different evaluators for a given object type and field name – making it seamless to the rule language, beyond the notation shown.

[![](/legacy/assets/images/2007/09/130ce2640b10-uncertainty.png)](</assets/images/2007/09/6ff471628685-uncertainty.png>)

  * Traditional Pattern
    * Shower( temperature == “hot” )
  * Pattern with uncertainty evaluator
    * Shower( temperature == ~“hot” )
  * Pattern with uncertainty evaluator and parameters
    * Shower( temperature == ~(10, $x, 15, $y) “hot” )