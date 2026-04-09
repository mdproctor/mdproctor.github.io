---
layout: post
title: "Lazily Enabled Truth Maintenace"
date: 2010-09-14
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/09/lazily-enabled-truth-maintenace.html
---

Three weeks ago I posted the project idea for [“Left and Right Unlinking”](<http://blog.athico.com/2010/08/left-and-right-unlinking-community.html>). So far there are no takers, so if you are interested let me know :)

In the meantime I tried to think of a simpler enhancement that we would like to see done.

At the moment Drools has a user setting “MaintainTMSOption” which can be true or false. It’s a small optimisation that when turned off avoids using the equality hashmap that is maintained for all inserted objects.

It would be a much better idea to remove this configuration setting, thus simplifying things for end users and have TMS lazily enabled on demand.

For each object type there is an “ObjectTypeConf” configuration object that is retrieved every time a working memory action, such as insert, is executed. The enabledTMS boolean should be moved there, so there is one per object type, by default it is false.

When a working memory action occurs, like insert, it retrieved the ObjectTypeConf and checks the maintainTms boolean there, instead of the current engine scoped configuration. When a logical insertion occurs and the ObjectTypeConf is retrieved if maintainTms is false it sets the value to true and then iterates the associated ObjectTypeNode memory lazily adding all the objects to the TMS equality map. From then on for that ObjectType all inserted objects are added to that equality map.

With this you now have the advantage of TMS being laziy enabled, so the minor hashmap operation is no longer used and likewise a small memory saving from not populating the map. There is a further advantage that this is now fine grained and when enabled only impacts for that specific object type.

A further enhancement could use a int counter, instead of a boolean. Each logical insertion for that object type increases the counter, each retraction decreases the counter; even if automatically retracted if the truth is broken for that logical assertion. When the counter reaches zero, TMS for that OTN can be disabled. We do not however remove the objects from the equality map, as this would cause “churn” if TMS is continuously enabled and disabled. Instead when TMS is disabled record the current fact counter id. Then if TMS is disabled on a retraction but there is a counter id, we can check that counter id to see if the fact is prior to TMS being disabled and thus would need to be retracted from the equality map.