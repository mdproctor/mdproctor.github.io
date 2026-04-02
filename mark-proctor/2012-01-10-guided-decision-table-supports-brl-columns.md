---
layout: post
title: "Guided Decision Table supports BRL columns"
date: 2012-01-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/01/guided-decision-table-supports-brl-columns.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Guided Decision Table supports BRL columns](<https://blog.kie.org/2012/01/guided-decision-table-supports-brl-columns.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 10, 2012  
[Rules](<https://blog.kie.org/category/rules>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

Work has been completed to allow BRL fragments to be used as both (or either) Condition and Action columns in the Guided Decision Table within Guvnor.

You can see the feature in action [here](<http://vimeo.com/34842725>) and read more about it below.

Adding a BRL column

[![](/legacy/assets/images/2012/01/e9051b9e1f3c-dtable-advanced-columns.png)](<http://3.bp.blogspot.com/-vrqKuxyL2kU/TwyN5U4PLzI/AAAAAAAAAfA/KnT5quUcX9c/s1600/dtable-advanced-columns.png>)

A BRL fragment is a section of a rule created using Guvnor’s (BRL) Guided Rule Editor: Condition columns permit the definition of “WHEN” sections and Action columns the definition of “THEN” sections. Fields defined therein as “Template Keys” become columns in the decision table.

A Condition BRL fragment

[![](/legacy/assets/images/2012/01/0de4816c23e1-dtable-brl-condition.png)](<http://3.bp.blogspot.com/-QWjuLzpYiUc/TwyNcTk7YjI/AAAAAAAAAeo/aU3tXatA4FI/s1600/dtable-brl-condition.png>)

An Action BRL fragment

[![](/legacy/assets/images/2012/01/d33a7f4c085f-dtable-brl-action.png)](<http://2.bp.blogspot.com/-2EPf4u-QF1A/TwyNo-bw9aI/AAAAAAAAAe0/KHcWh7kucAA/s1600/dtable-brl-action.png>)

Consequently any rule that could be defined with the (BRL) Guided Rule Editor can now be defined with a decision table; including free-format DRL and DSL Sentences.

BRL fragments are fully integrated with other columns in the decision table, so that a Pattern or field defined in a regular column can be referenced in the BRL fragments and vice-versa.

A decision table with BRL fragments and regular columns  
  
[![](/legacy/assets/images/2012/01/1ab0c45dd065-dtable-brl-columns.png)](<http://2.bp.blogspot.com/-nQWun61E70g/TwxNvqVV4iI/AAAAAAAAAeQ/8WCH9394sOs/s1600/dtable-brl-columns.png>)

Source from BRL fragments

[![](/legacy/assets/images/2012/01/81d7dd84b5bb-dtable-brl-source.png)](<http://1.bp.blogspot.com/-S3GYrPfWKwY/TwxN_ggQRBI/AAAAAAAAAec/KWK69juiPGE/s1600/dtable-brl-source.png>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F01%2Fguided-decision-table-supports-brl-columns.html&linkname=Guided%20Decision%20Table%20supports%20BRL%20columns> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F01%2Fguided-decision-table-supports-brl-columns.html&linkname=Guided%20Decision%20Table%20supports%20BRL%20columns> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F01%2Fguided-decision-table-supports-brl-columns.html&linkname=Guided%20Decision%20Table%20supports%20BRL%20columns> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F01%2Fguided-decision-table-supports-brl-columns.html&linkname=Guided%20Decision%20Table%20supports%20BRL%20columns> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F01%2Fguided-decision-table-supports-brl-columns.html&linkname=Guided%20Decision%20Table%20supports%20BRL%20columns> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F01%2Fguided-decision-table-supports-brl-columns.html&linkname=Guided%20Decision%20Table%20supports%20BRL%20columns> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F01%2Fguided-decision-table-supports-brl-columns.html&linkname=Guided%20Decision%20Table%20supports%20BRL%20columns> "Email")
  *[]: 2010-05-25T16:11:00+02:00