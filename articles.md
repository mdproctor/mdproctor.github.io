---
layout: page
title: Articles
permalink: /articles/
---

{% assign series_articles = site.articles | where_exp: "a", "a.order" | sort: 'order' %}
{% assign standalone = site.articles | where_exp: "a", "a.order == nil" | sort: 'date' | reverse %}
{% assign notes = series_articles | concat: standalone %}
{% include note-list.html notes=notes %}
