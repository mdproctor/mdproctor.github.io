---
layout: page
title: Articles
permalink: /articles/
---

{% assign sorted_articles = site.articles | sort: 'date' | reverse %}
{% for article in sorted_articles %}
### [{{ article.title }}]({{ article.url }})
*{{ article.date | date: "%B %-d, %Y" }}*{% if article.tags %} · {{ article.tags | join: ", " }}{% endif %}

{{ article.excerpt | markdownify | strip_html | truncate: 250 }}

---
{% endfor %}
