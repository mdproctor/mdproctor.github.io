---
layout: page
title: Notes | QuarkMind
permalink: /notes/quarkmind/
---

{% assign notes = site.notes | where_exp: "n", "n.projects contains 'quarkmind'" | sort: 'date' | reverse %}
{% include note-list.html notes=notes %}
