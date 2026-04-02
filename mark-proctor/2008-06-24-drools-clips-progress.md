---
layout: post
title: "Drools Clips progress"
date: 2008-06-24
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/06/drools-clips-progress.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Clips progress](<https://blog.kie.org/2008/06/drools-clips-progress.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 24, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Made some progress over the weekend with Drools Clips, which will provide a Clips like language for Drools. Deftemplates are now working and I did some work on PackageBuilder so that it’s now able to handle multiple namespaces and have a RuleBase attached to provide a more “shell” like environment suitable for Clips. Michael Neale also got a basic command line shell working. So what does it support?

  * deftemplate
  * defrule
  * deffuction
  * and/or/not/exists/test Conditional Elements
  * Literal, Variable, Return Value and Predicate field constraints

You can look at the [ClipsShellTest](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-clips/src/test/java/org/drools/clips/ClipsShellTest.java?r=HEAD>) and [LhsClipsParserTest](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-clips/src/test/java/org/drools/clips/LhsClpParserTest.java?r=HEAD>) get an idea of the full support. It’s still early stages and it’s very rough in places, especially on error handling and feedback as well as no view commands to display data. For a little fun here is a screenshot of the shell in action:

[![](/legacy/assets/images/2008/07/6a54a64d5d96-shell.png)(click to enlarge)](<http://bp0.blogger.com/_Jrhwx8X9P7g/SGRYc5qz-KI/AAAAAAAAAIw/xefELIYMRCo/s1600-h/shell.png>)

The screen shot is a contrived example but it does show a shell environment cleanly mixing deftemplates and pojos – note that Drools 5.0 does not require shadow facts, due to the new asymmetrical Rete algorithm. It also shows deffunction in use. This will be part of Milestone1, that I’m hoping to tag tomorrow.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-clips-progress.html&linkname=Drools%20Clips%20progress> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-clips-progress.html&linkname=Drools%20Clips%20progress> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-clips-progress.html&linkname=Drools%20Clips%20progress> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-clips-progress.html&linkname=Drools%20Clips%20progress> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-clips-progress.html&linkname=Drools%20Clips%20progress> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-clips-progress.html&linkname=Drools%20Clips%20progress> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-clips-progress.html&linkname=Drools%20Clips%20progress> "Email")