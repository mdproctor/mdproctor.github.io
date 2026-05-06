---
layout: page
title: Notes | Hortara
permalink: /notes/hortara/
---

{% assign notes = site.notes | where_exp: "n", "n.projects contains 'hortara'" | sort: 'date' | reverse %}
{% include note-list.html notes=notes %}
