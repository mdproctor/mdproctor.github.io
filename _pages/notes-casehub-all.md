---
layout: page
title: CaseHub — All Notes
permalink: /notes/casehub/all/
---
{% include casehub-subnav.html %}

{% assign sub_names = "casehub-engine:Engine,casehub-ledger:Ledger,casehub-qhorus:Qhorus,casehub-work:Work,claudony:Claudony,casehub-parent:Parent" | split: "," %}
{% assign notes = site.notes | where_exp: "n", "n.projects contains 'casehub'" | sort: 'date' | reverse %}
{% for note in notes %}
<div class="notes-full-post">
  <a class="title" href="{{ note.url }}">{{ note.title }}
  {% for pair in sub_names %}
    {% assign kv = pair | split: ":" %}
    {% if note.projects contains kv[0] %}<span class="sub-tag">{{ kv[1] }}</span>{% break %}{% endif %}
  {% endfor %}
  </a>
  {% if note.excerpt %}<div class="excerpt">{{ note.excerpt | strip_html | truncate: 180 }}</div>{% endif %}
  <div class="meta">{{ note.date | date: "%b %-d, %Y" }}</div>
</div>
{% endfor %}
