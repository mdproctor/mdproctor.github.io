---
layout: page
title: Notes | Sparge
permalink: /notes/sparge/
---

{% assign notes = site.notes | where_exp: "n", "n.projects contains 'sparge'" | sort: 'date' | reverse %}
{% include note-list.html notes=notes %}
