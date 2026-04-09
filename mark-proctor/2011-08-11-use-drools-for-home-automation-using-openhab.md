---
layout: post
title: "Use Drools for Home Automation using OpenHAB"
date: 2011-08-11
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/08/use-drools-for-home-automation-using-openhab.html
---

<http://code.google.com/p/openhab/wiki/Drools>  

## “Introduction

The open Home Automation Bus (openHAB) project aims at providing a universal integration platform for all things around home automation.

It is designed to be absolutely vendor-neutral as well as hardware/protocol-agnostic. openHAB brings together different bus systems, hardware devices and interface protocols by dedicated bindings. These bindings send and receive commands and status updates on the openHAB event bus. This concept allows designing user interfaces with a unique look&feel, but with the possibility to operate devices based on a big number of different technologies. Besides the user interfaces, it also brings the power of automation logics across different system boundaries.”

…

## “Defining the When clause (LHS)

The when clause (LHS) of a rule should contain conditions based on the objects in the working memory, i.e. items and events.

Here is an example of a when clause: 

```
$event :StateEvent(itemName=="Rain", changed==true)

        $window  :Item(name=="Window", state==OpenClosedType.OPEN)
```