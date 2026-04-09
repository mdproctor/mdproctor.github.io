---
layout: post
title: "Guvnor - Using jBPM Work Items in decision tables"
date: 2011-11-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/11/guvnor-using-jbpm-work-items-in-decision-tables.html
---

### Guvnor – Using jBPM Work Items in decision tables

Work is now complete for 5.4.0.beta1 to use jBPM Work Items in the guided decision table.

[![](/legacy/assets/images/2011/11/f34169330bbe-dtable.png)](</assets/images/2011/11/3633fb8ec208-dtable.png>)

New Actions have been added to perform the following:-

  * Call a Work Item. Parameters can be either literal values, or bound to a Fact or Fact Field.

  * Set the value of a field on an existing Fact to the value of a Work Item result.

  * Set the value of a field on a new Fact to the value of a Work Item result.

[![](/legacy/assets/images/2011/11/ae6ffdd9d138-actions.png)](</assets/images/2011/11/c6d0a94ff0e0-actions.png>)

Significantly, to maximize the usefulness of using Work Items in actions, is the ability to define bindings for Fact field values. This allows Facts’ fields to be passed to Work Items.

Bound fields can also be used in predicate and formula Condition definitions too; which opens a world of further possibility which up until now has been unavailable.

[![](/legacy/assets/images/2011/11/068c4a4ba99f-binding.png)](</assets/images/2011/11/f60360b39f90-binding.png>)

Work Item definitions can either be defined as assets in Guvnor or included in a workitem-definitions.xml the format of which follows the normal jBPM Work Item definition.

A short video [here](<http://vimeo.com/31693827>) demonstrates using Work Items in a decision table and a short example of how the feature can be leveraged from a Java application.

Unrelated to Work Items, but a welcome addition, is the ability to define an action to retract Facts.