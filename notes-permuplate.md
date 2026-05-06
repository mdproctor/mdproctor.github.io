---
layout: page
title: Notes | Permuplate
permalink: /notes/permuplate/
---

{% assign notes = site.notes | where_exp: "n", "n.projects contains 'permuplate'" | sort: 'date' | reverse %}
{% include note-list.html notes=notes %}
