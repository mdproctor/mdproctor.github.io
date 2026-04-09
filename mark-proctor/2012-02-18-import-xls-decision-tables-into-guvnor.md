---
layout: post
title: "Import XLS decision tables into Guvnor"
date: 2012-02-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/02/import-xls-decision-tables-into-guvnor.html
---

Work has been completed to enable users to upload their XLS based Decision Tables into Guvnor! Checkout this new feature in the master branch (or wait for the arrival of 5.4.CR1 when it becomes available…)

Checkout a demo [here](<https://vimeo.com/37033081>).

Uploading a XLS decision table results in the creation of numerous new assets, including (obviously) web-guided Decision Tables, functions, declarative types and modifications to package globals and imports etc (Queries are not converted, although supported in the XLS form, as Guvnor doesn’t support them [yet](<https://issues.jboss.org/browse/GUVNOR-1532>)).

XLS decision table

[![](/legacy/assets/images/2012/02/0201a0229f32-dtable-xls.png)](</assets/images/2012/02/080123978dd7-dtable-xls.png>)

Guided decision table

[![](/legacy/assets/images/2012/02/2fa0c506c3ef-dtable-converted.png)](</assets/images/2012/02/1532aa2ab3bf-dtable-converted.png>)

This is the first stage of “round-tripping” decision tables. We still need to add the ability to export a guided decision table back to XLS, plus we’d like to add tighter integration of updated XLS assets to their original converted cousins – so if a new version of the XLS decision table is uploaded the related assets’ versions are updated (rather than creating new) upon conversion.

This is a powerful enhancement and as such your feedback is critical to ensure we implement the feature as you’d like it to operate. Check it out, feedback your opinions and help guide the future work :)