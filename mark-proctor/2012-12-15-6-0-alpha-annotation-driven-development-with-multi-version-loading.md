---
layout: post
title: "6.0 Alpha - Annotation Driven development with Multi Version Loading"
date: 2012-12-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/12/6-0-alpha-annotation-driven-development-with-multi-version-loading.html
---

### 6.0 Alpha – Annotation Driven development with Multi Version Loading

Drools & jBPM 6.0 alpha should be out end of next week. 6.0 introduces convention based projects that remove the need for boiler plate code – literally just drop in the drl or bpmn2 and get going. Further we now allow rules and processes to be published as maven artifacts, in maven repositories. These artifacts can either be resolve via the classpath or downloaded dynamically on the fly. We even support out of the box side by side version loading, via the maven ReleaseId conventions.

As a little taster here is a new screenshot showing the annotation driven development. The lines below are all that’s needed to dynamically load a module from a local or remote maven repository and start working with it. KieSession is the new, shorter name, for StatefulKnowlegeSession. Kie is an acronym for “Knowledge Is Everything”, but I’ll talk about Kie in another blog, expect to start hearing a lot about it soon :)

[![](/legacy/assets/images/2012/12/04574c5e2a4f-KSessionVersions.png)](</assets/images/2012/12/2ed88220ac65-KSessionVersions.png>)

And here is a complete example screen shot. Create the drl, define the kmodule and start using them.

[![](/legacy/assets/images/2012/12/7f2c7f5cc006-HelloDave.png)](</assets/images/2012/12/48dcc4f324e4-HelloDave.png>)

(click image to enlarge)