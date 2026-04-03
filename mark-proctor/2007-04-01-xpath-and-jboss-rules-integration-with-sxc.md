---
layout: post
title: "XPath and JBoss Rules integration with SXC"
date: 2007-04-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/04/xpath-and-jboss-rules-integration-with-sxc.html
---

SXC (Simple XML Compiler)  
SXC has just been released and is a must have for any SOA project – <http://sxc.codehaus.org/> – best of all it comes with JBoss Rules integration :) SXC is a pluggeable XML compiler that provides a high performance streaming XPath parser with JBoss Rules integration. It allows you to specify XPath querries in your rules, as the XML is parsed those rules are then applied, you do not need to write additional XPath statements else where.

```drl
rule "AddresTest"when    event : XPathEvent( expression == "/order/address[@country]" );then    System.out.println("Success! - " + drools.getRule().getName());end
```