---
layout: post
title: "Dynamic Salience Expressions"
date: 2007-05-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/dynamic-salience-expressions.html
---

The other week in the mailing list someone was asking about whether it’s possible to have the salience’s value derived from the matched facts. Which got me thinking as I haven’t seen that in any other rule engines – I only know a few engines, so someone with more experience care to verify that?

Anyway a few weeks later and a bored friday night dynamic salience expressions are born :) The salience value can now be derived from an expression that has full access to the variables bindings, ofcourse integer values can still be specified. Before, during conflict resolution, the salience value was read directly from the rule on each comparison, now when the Activation is created the salience value is determined once and stored in the Activation for comparison during conflict resolution. So now you can write things like have rules with the highest priced items combined with the shoppers bonus rating fire first:

```drl
rule "high value fires first"
salience (person.bonus * item.price)
when
person : Person()    item : Item()
then
...
end
```

MVEL is used for the salience expressions, as part of the pluggeable dialect system we have just built – I’ll blog on pluggeable dialects and parsers next week.

Update — Thanks to Johan Lindberg, who has pointed out that Clips and Jess allow the salience to be set via function calls in Jess/Clips.