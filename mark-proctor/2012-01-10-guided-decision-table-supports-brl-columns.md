---
layout: post
title: "Guided Decision Table supports BRL columns"
date: 2012-01-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/01/guided-decision-table-supports-brl-columns.html
---

Work has been completed to allow BRL fragments to be used as both (or either) Condition and Action columns in the Guided Decision Table within Guvnor.

You can see the feature in action [here](<http://vimeo.com/34842725>) and read more about it below.

Adding a BRL column

[![](/legacy/assets/images/2012/01/e9051b9e1f3c-dtable-advanced-columns.png)](</assets/images/2012/01/3d5cad1b96f6-dtable-advanced-columns.png>)

A BRL fragment is a section of a rule created using Guvnor’s (BRL) Guided Rule Editor: Condition columns permit the definition of “WHEN” sections and Action columns the definition of “THEN” sections. Fields defined therein as “Template Keys” become columns in the decision table.

A Condition BRL fragment

[![](/legacy/assets/images/2012/01/0de4816c23e1-dtable-brl-condition.png)](</assets/images/2012/01/55e81e6fd866-dtable-brl-condition.png>)

An Action BRL fragment

[![](/legacy/assets/images/2012/01/d33a7f4c085f-dtable-brl-action.png)](</assets/images/2012/01/1c5074c460db-dtable-brl-action.png>)

Consequently any rule that could be defined with the (BRL) Guided Rule Editor can now be defined with a decision table; including free-format DRL and DSL Sentences.

BRL fragments are fully integrated with other columns in the decision table, so that a Pattern or field defined in a regular column can be referenced in the BRL fragments and vice-versa.

A decision table with BRL fragments and regular columns  
[![](/legacy/assets/images/2012/01/1ab0c45dd065-dtable-brl-columns.png)](</assets/images/2012/01/d35e108406c7-dtable-brl-columns.png>)

Source from BRL fragments

[![](/legacy/assets/images/2012/01/81d7dd84b5bb-dtable-brl-source.png)](</assets/images/2012/01/2e7a19c37207-dtable-brl-source.png>)