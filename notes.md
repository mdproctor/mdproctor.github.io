---
layout: page
title: Notes
permalink: /notes/
---

{% assign sorted_notes = site.notes | sort: 'date' | reverse %}
{% for note in sorted_notes %}
### [{{ note.title }}]({{ note.url }})
*{{ note.date | date: "%B %-d, %Y" }}*{% if note.projects %} · {{ note.projects | join: ", " }}{% endif %}{% if note.tags %} · {{ note.tags | join: ", " }}{% endif %}

{{ note.excerpt | markdownify | strip_html | truncate: 250 }}

---
{% endfor %}
