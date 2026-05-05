---
layout: page
title: CaseHub — uparent Notes
permalink: /notes/casehub/parent/
---
{% include casehub-subnav.html %}

{% assign notes = site.notes | where_exp: "n", "n.projects contains ''" | sort: 'date' | reverse %}
{% for note in notes %}
<div class="notes-full-post">
  <a class="title" href="{{ note.url }}">{{ note.title }}</a>
  {% if note.excerpt %}<div class="excerpt">{{ note.excerpt | strip_html | truncate: 180 }}</div>{% endif %}
  <div class="meta">{{ note.date | date: "%b %-d, %Y" }}</div>
</div>
{% endfor %}
