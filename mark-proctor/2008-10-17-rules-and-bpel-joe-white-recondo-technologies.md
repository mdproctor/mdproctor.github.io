---
layout: post
title: "Rules and BPEL (Joe White @ Recondo Technologies)"
date: 2008-10-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/10/rules-and-bpel-joe-white-recondo-technologies.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Rules and BPEL (Joe White @ Recondo Technologies)](<https://blog.kie.org/2008/10/rules-and-bpel-joe-white-recondo-technologies.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- October 17, 2008  
[Process](<https://blog.kie.org/category/process>) [Article](<https://blog.kie.org/content_type/article>)

Joe is here with us in Texas for the Drools Boot Camp, his company is a big BPEL user and he’s been sharing his pain with us. They turned to BPEL, having drunk the koolaid, with the aim to simplify the management of a collection of services and their input and output of data. He tells us the result is a fairly complex system, that lives in Speghetti hell, that is difficult to manage on its own. Joe has been kind enough to share a screen shot and his own thoughts (all pasted below) on where he’d like to go with his company to better address this issue in the future, with the hope that Drools can help.

The image below is a graphical representation of a business process in BPEL. The boxes and circles along the right are services, the lines running to those services are invocations, and the boxes in the middle are steps in the BPEL process (assign, invoke, copy etc.)

Spaghetti BPEL, welcome to hell!!!

[![](/legacy/assets/images/2008/10/5c27a9b7f16f-rules_and_bpel.png)](<http://1.bp.blogspot.com/_Jrhwx8X9P7g/SPjNwmt8aXI/AAAAAAAAAOY/xOVGlQ6xQ0Y/s1600-h/rules+and+bpel.png>)(click to enlarge)

An alternative is to use rules to manage your business process. A purely rules based approach would use a rule set as a content based router and every decision point becomes an evaluation of your business routing rules. In addition, rules can manage service invocation by making the service invocation the consequence of firing into another rule set. Coupled with a BRMS like Guvnor the rules based process orchestration of services becomes accessible by business users in a managed environment. Coupled with a workflow or integration engine like Drools-Flow or Apache Camel the rules based business process management will allow for the management of complex long running business processes without some of the complexity and development overhead introduced by BPEL. The rules manage the decision points and the workflow engine helps manage the progression through your business process. The rules based approach won’t provide everything that you get with BPEL. For example state management, persistence, and ease of integration with WSDL are all advantages that BPEL provides that you wouldn’t get for free with a rules driven approach. In the end a rules based approach to business process orchestration should provide simplicity, modularity, and ease of development. As an architect it is worth considering a rules driven approach to business process management.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Frules-and-bpel-joe-white-recondo-technologies.html&linkname=Rules%20and%20BPEL%20%28Joe%20White%20%40%20Recondo%20Technologies%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Frules-and-bpel-joe-white-recondo-technologies.html&linkname=Rules%20and%20BPEL%20%28Joe%20White%20%40%20Recondo%20Technologies%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Frules-and-bpel-joe-white-recondo-technologies.html&linkname=Rules%20and%20BPEL%20%28Joe%20White%20%40%20Recondo%20Technologies%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Frules-and-bpel-joe-white-recondo-technologies.html&linkname=Rules%20and%20BPEL%20%28Joe%20White%20%40%20Recondo%20Technologies%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Frules-and-bpel-joe-white-recondo-technologies.html&linkname=Rules%20and%20BPEL%20%28Joe%20White%20%40%20Recondo%20Technologies%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Frules-and-bpel-joe-white-recondo-technologies.html&linkname=Rules%20and%20BPEL%20%28Joe%20White%20%40%20Recondo%20Technologies%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Frules-and-bpel-joe-white-recondo-technologies.html&linkname=Rules%20and%20BPEL%20%28Joe%20White%20%40%20Recondo%20Technologies%29> "Email")