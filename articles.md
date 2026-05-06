---
layout: page
title: Articles
permalink: /articles/
---

{% assign by_order = site.articles | sort: 'order' %}
{% assign notes = by_order | sort: 'date' | reverse %}
{% include note-list.html notes=notes %}
