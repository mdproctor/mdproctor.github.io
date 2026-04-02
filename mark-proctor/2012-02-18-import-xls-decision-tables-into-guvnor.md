---
layout: post
title: "Import XLS decision tables into Guvnor"
date: 2012-02-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/02/import-xls-decision-tables-into-guvnor.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Import XLS decision tables into Guvnor](<https://blog.kie.org/2012/02/import-xls-decision-tables-into-guvnor.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 18, 2012  
[Rules](<https://blog.kie.org/category/rules>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

Work has been completed to enable users to upload their XLS based Decision Tables into Guvnor! Checkout this new feature in the master branch (or wait for the arrival of 5.4.CR1 when it becomes available…)

Checkout a demo [here](<https://vimeo.com/37033081>).

Uploading a XLS decision table results in the creation of numerous new assets, including (obviously) web-guided Decision Tables, functions, declarative types and modifications to package globals and imports etc (Queries are not converted, although supported in the XLS form, as Guvnor doesn’t support them [yet](<https://issues.jboss.org/browse/GUVNOR-1532>)).

XLS decision table

[![](/legacy/assets/images/2012/02/0201a0229f32-dtable-xls.png)](<http://2.bp.blogspot.com/-7hqYVif8QYg/T0AqlQz-vmI/AAAAAAAAAiY/OKbymXwjgLg/s1600/dtable-xls.png>)

Guided decision table

[![](/legacy/assets/images/2012/02/2fa0c506c3ef-dtable-converted.png)](<http://1.bp.blogspot.com/-7zYvU-1lvlI/T0AqsBUmoVI/AAAAAAAAAik/ep4B2NSCCrI/s1600/dtable-converted.png>)

This is the first stage of “round-tripping” decision tables. We still need to add the ability to export a guided decision table back to XLS, plus we’d like to add tighter integration of updated XLS assets to their original converted cousins – so if a new version of the XLS decision table is uploaded the related assets’ versions are updated (rather than creating new) upon conversion.

This is a powerful enhancement and as such your feedback is critical to ensure we implement the feature as you’d like it to operate. Check it out, feedback your opinions and help guide the future work :)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fimport-xls-decision-tables-into-guvnor.html&linkname=Import%20XLS%20decision%20tables%20into%20Guvnor> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fimport-xls-decision-tables-into-guvnor.html&linkname=Import%20XLS%20decision%20tables%20into%20Guvnor> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fimport-xls-decision-tables-into-guvnor.html&linkname=Import%20XLS%20decision%20tables%20into%20Guvnor> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fimport-xls-decision-tables-into-guvnor.html&linkname=Import%20XLS%20decision%20tables%20into%20Guvnor> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fimport-xls-decision-tables-into-guvnor.html&linkname=Import%20XLS%20decision%20tables%20into%20Guvnor> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fimport-xls-decision-tables-into-guvnor.html&linkname=Import%20XLS%20decision%20tables%20into%20Guvnor> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fimport-xls-decision-tables-into-guvnor.html&linkname=Import%20XLS%20decision%20tables%20into%20Guvnor> "Email")
  *[]: 2010-05-25T16:11:00+02:00