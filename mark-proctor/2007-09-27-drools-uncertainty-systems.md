---
layout: post
title: "Drools - Uncertainty Systems"
date: 2007-09-27
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/09/drools-uncertainty-systems.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools – Uncertainty Systems](<https://blog.kie.org/2007/09/drools-uncertainty-systems.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 27, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Davide Sottara has been working on the foundations for a Drools partial data reasoning, for his Phd, with Uncertainty Systems to express truth degrees. He’s made a small screenshot for us along with the proposed syntax. The idea is that different uncertainty systems can be configured to handle different evaluators for a given object type and field name – making it seamless to the rule language, beyond the notation shown.

[![](/legacy/assets/images/2007/09/130ce2640b10-uncertainty.png)](<http://bp2.blogger.com/_Jrhwx8X9P7g/RvtBAvhjg9I/AAAAAAAAAGM/b0cqcaEvknQ/s1600-h/uncertainty.png>)

  * Traditional Pattern
    * Shower( temperature == “hot” )
  * Pattern with uncertainty evaluator
    * Shower( temperature == ~“hot” )
  * Pattern with uncertainty evaluator and parameters
    * Shower( temperature == ~(10, $x, 15, $y) “hot” )

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-uncertainty-systems.html&linkname=Drools%20%E2%80%93%20Uncertainty%20Systems> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-uncertainty-systems.html&linkname=Drools%20%E2%80%93%20Uncertainty%20Systems> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-uncertainty-systems.html&linkname=Drools%20%E2%80%93%20Uncertainty%20Systems> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-uncertainty-systems.html&linkname=Drools%20%E2%80%93%20Uncertainty%20Systems> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-uncertainty-systems.html&linkname=Drools%20%E2%80%93%20Uncertainty%20Systems> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-uncertainty-systems.html&linkname=Drools%20%E2%80%93%20Uncertainty%20Systems> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-uncertainty-systems.html&linkname=Drools%20%E2%80%93%20Uncertainty%20Systems> "Email")