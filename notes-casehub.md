---
layout: page
title: CaseHub Notes
permalink: /notes/casehub/
---
{% include casehub-subnav.html %}

{% assign sub_projects = "casehub-engine,casehub-ledger,casehub-qhorus,casehub-work,claudony,casehub-parent" | split: "," %}
{% assign display_names = "Engine,Ledger,Qhorus,Work,Claudony,Parent" | split: "," %}

{% for i in (0..5) %}
{% assign sub = sub_projects[i] %}
{% assign name = display_names[i] %}
{% assign sub_notes = site.notes | where_exp: "n", "n.projects contains sub" | sort: 'date' | reverse %}
{% if sub_notes.size > 0 %}
{% unless forloop.first %}<hr class="notes-divider">{% endunless %}
<div class="notes-section-header">
  <h3>{{ name }}</h3>
  <span class="count">{{ sub_notes.size }} notes</span>
  <a class="see-all" href="/notes/casehub/{{ name | downcase }}/">See all →</a>
</div>
{% for note in sub_notes limit: 3 %}
<div class="notes-post-row"><a href="{{ note.url }}">{{ note.title }}</a><span class="date">{{ note.date | date: "%b %-d" }}</span></div>
{% endfor %}
{% endif %}
{% endfor %}
