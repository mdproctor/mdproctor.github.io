---
layout: page
title: Notes
permalink: /notes/
---

{% assign ch = site.notes | where_exp: "n", "n.projects contains 'casehub'" | sort: 'date' | reverse %}
<div class="notes-project-block">
  <h3>CaseHub</h3>
  <div class="notes-sub-chips">
    <a href="/notes/casehub/engine/">Engine</a>
    <a href="/notes/casehub/ledger/">Ledger</a>
    <a href="/notes/casehub/qhorus/">Qhorus</a>
    <a href="/notes/casehub/work/">Work</a>
    <a href="/notes/casehub/claudony/">Claudony</a>
    <a href="/notes/casehub/parent/">Parent</a>
  </div>
  {% for note in ch limit: 3 %}
  <div class="notes-post-row"><a href="{{ note.url }}">{{ note.title }}</a><span class="date">{{ note.date | date: "%b %-d" }}</span></div>
  {% endfor %}
  <a class="notes-section-header see-all" href="/notes/casehub/" style="display:inline-block;margin-top:8px;">See all CaseHub notes →</a>
</div>

<hr class="notes-divider">

{% assign qm = site.notes | where_exp: "n", "n.projects contains 'quarkmind'" | sort: 'date' | reverse %}
<div class="notes-project-block">
  <h3>QuarkMind</h3>
  {% for note in qm limit: 3 %}
  <div class="notes-post-row"><a href="{{ note.url }}">{{ note.title }}</a><span class="date">{{ note.date | date: "%b %-d" }}</span></div>
  {% endfor %}
  <a class="notes-section-header see-all" href="/notes/quarkmind/" style="display:inline-block;margin-top:8px;">See all QuarkMind notes →</a>
</div>

<hr class="notes-divider">

{% assign pm = site.notes | where_exp: "n", "n.projects contains 'permuplate'" | sort: 'date' | reverse %}
<div class="notes-project-block">
  <h3>Permuplate</h3>
  {% for note in pm limit: 3 %}
  <div class="notes-post-row"><a href="{{ note.url }}">{{ note.title }}</a><span class="date">{{ note.date | date: "%b %-d" }}</span></div>
  {% endfor %}
  <a class="notes-section-header see-all" href="/notes/permuplate/" style="display:inline-block;margin-top:8px;">See all Permuplate notes →</a>
</div>

<hr class="notes-divider">

{% assign hm = site.notes | where_exp: "n", "n.projects contains 'hortara'" | sort: 'date' | reverse %}
<div class="notes-project-block">
  <h3>Hortara</h3>
  {% for note in hm limit: 3 %}
  <div class="notes-post-row"><a href="{{ note.url }}">{{ note.title }}</a><span class="date">{{ note.date | date: "%b %-d" }}</span></div>
  {% endfor %}
  <a class="notes-section-header see-all" href="/notes/hortara/" style="display:inline-block;margin-top:8px;">See all Hortara notes →</a>
</div>

<hr class="notes-divider">
<div class="notes-project-block"><h3>Sparge</h3><div class="notes-coming">Coming soon.</div></div>
