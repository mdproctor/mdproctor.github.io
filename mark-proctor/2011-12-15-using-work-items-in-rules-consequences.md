---
layout: post
title: "Using Work Items in rules' consequences"
date: 2011-12-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/12/using-work-items-in-rules-consequences.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Using Work Items in rules’ consequences](<https://blog.kie.org/2011/12/using-work-items-in-rules-consequences.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- December 15, 2011  
[Process](<https://blog.kie.org/category/process>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Recently I [added](<http://blog.athico.com/2011/11/guvnor-using-jbpm-work-items-in.html>) the ability to use Work Items as function calls in the guided decision table editor in Guvnor. This highlighted that Work Items have always been available as function calls in DRL but this has not been well documented; leaving users to make the connection.

Various Work Item handlers are available “out of the (jBPM) box” in the org.jbpm.process.workitem package that may prove useful to rule authors. In addition Work Item Handlers providing bespoke services for all domain areas can be easily authored and plugged in.

I have added a couple of examples to drools-examples (in the master branch on [github](<https://github.com/droolsjbpm/drools/tree/master/drools-examples/src/main/java/org/drools/examples/workitemconsequence>) and to be included 5.4.0.beta1) that illustrate how to use Work Item handlers from the right-hand side of a rule: one simulates sending an email and the other provides a greeting service; the code for both residing in custom Work Item handlers.

I hope they provide a catalyst to encourage the use of Work Items in rules.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fusing-work-items-in-rules-consequences.html&linkname=Using%20Work%20Items%20in%20rules%E2%80%99%20consequences> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fusing-work-items-in-rules-consequences.html&linkname=Using%20Work%20Items%20in%20rules%E2%80%99%20consequences> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fusing-work-items-in-rules-consequences.html&linkname=Using%20Work%20Items%20in%20rules%E2%80%99%20consequences> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fusing-work-items-in-rules-consequences.html&linkname=Using%20Work%20Items%20in%20rules%E2%80%99%20consequences> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fusing-work-items-in-rules-consequences.html&linkname=Using%20Work%20Items%20in%20rules%E2%80%99%20consequences> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fusing-work-items-in-rules-consequences.html&linkname=Using%20Work%20Items%20in%20rules%E2%80%99%20consequences> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F12%2Fusing-work-items-in-rules-consequences.html&linkname=Using%20Work%20Items%20in%20rules%E2%80%99%20consequences> "Email")
  *[]: 2010-05-25T16:11:00+02:00