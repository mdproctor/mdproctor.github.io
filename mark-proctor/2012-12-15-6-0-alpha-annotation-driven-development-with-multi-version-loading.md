---
layout: post
title: "6.0 Alpha - Annotation Driven development with Multi Version Loading"
date: 2012-12-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/12/6-0-alpha-annotation-driven-development-with-multi-version-loading.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [6.0 Alpha – Annotation Driven development with Multi Version Loading](<https://blog.kie.org/2012/12/6-0-alpha-annotation-driven-development-with-multi-version-loading.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- December 15, 2012  
[Process](<https://blog.kie.org/category/process>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Drools & jBPM 6.0 alpha should be out end of next week. 6.0 introduces convention based projects that remove the need for boiler plate code – literally just drop in the drl or bpmn2 and get going. Further we now allow rules and processes to be published as maven artifacts, in maven repositories. These artifacts can either be resolve via the classpath or downloaded dynamically on the fly. We even support out of the box side by side version loading, via the maven ReleaseId conventions.

As a little taster here is a new screenshot showing the annotation driven development. The lines below are all that’s needed to dynamically load a module from a local or remote maven repository and start working with it. KieSession is the new, shorter name, for StatefulKnowlegeSession. Kie is an acronym for “Knowledge Is Everything”, but I’ll talk about Kie in another blog, expect to start hearing a lot about it soon :)

[![](/legacy/assets/images/2012/12/04574c5e2a4f-KSessionVersions.png)](<http://1.bp.blogspot.com/-GPSxpYUDTmA/UMw66cJUhLI/AAAAAAAAA3M/CgfqaZ7bbZg/s1600/KSessionVersions.png>)

And here is a complete example screen shot. Create the drl, define the kmodule and start using them.

[![](/legacy/assets/images/2012/12/7f2c7f5cc006-HelloDave.png)](<http://1.bp.blogspot.com/-Vzf25nGjhmo/UMw7ytp2e0I/AAAAAAAAA3U/LtXNonbQGFA/s1600/HelloDave.png>)

(click image to enlarge)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F12%2F6-0-alpha-annotation-driven-development-with-multi-version-loading.html&linkname=6.0%20Alpha%20%E2%80%93%20Annotation%20Driven%20development%20with%20Multi%20Version%20Loading> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F12%2F6-0-alpha-annotation-driven-development-with-multi-version-loading.html&linkname=6.0%20Alpha%20%E2%80%93%20Annotation%20Driven%20development%20with%20Multi%20Version%20Loading> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F12%2F6-0-alpha-annotation-driven-development-with-multi-version-loading.html&linkname=6.0%20Alpha%20%E2%80%93%20Annotation%20Driven%20development%20with%20Multi%20Version%20Loading> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F12%2F6-0-alpha-annotation-driven-development-with-multi-version-loading.html&linkname=6.0%20Alpha%20%E2%80%93%20Annotation%20Driven%20development%20with%20Multi%20Version%20Loading> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F12%2F6-0-alpha-annotation-driven-development-with-multi-version-loading.html&linkname=6.0%20Alpha%20%E2%80%93%20Annotation%20Driven%20development%20with%20Multi%20Version%20Loading> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F12%2F6-0-alpha-annotation-driven-development-with-multi-version-loading.html&linkname=6.0%20Alpha%20%E2%80%93%20Annotation%20Driven%20development%20with%20Multi%20Version%20Loading> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F12%2F6-0-alpha-annotation-driven-development-with-multi-version-loading.html&linkname=6.0%20Alpha%20%E2%80%93%20Annotation%20Driven%20development%20with%20Multi%20Version%20Loading> "Email")
  *[]: 2010-05-25T16:11:00+02:00