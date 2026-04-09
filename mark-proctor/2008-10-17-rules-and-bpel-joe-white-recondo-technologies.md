---
layout: post
title: "Rules and BPEL (Joe White @ Recondo Technologies)"
date: 2008-10-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/10/rules-and-bpel-joe-white-recondo-technologies.html
---

Joe is here with us in Texas for the Drools Boot Camp, his company is a big BPEL user and he’s been sharing his pain with us. They turned to BPEL, having drunk the koolaid, with the aim to simplify the management of a collection of services and their input and output of data. He tells us the result is a fairly complex system, that lives in Speghetti hell, that is difficult to manage on its own. Joe has been kind enough to share a screen shot and his own thoughts (all pasted below) on where he’d like to go with his company to better address this issue in the future, with the hope that Drools can help.

The image below is a graphical representation of a business process in BPEL. The boxes and circles along the right are services, the lines running to those services are invocations, and the boxes in the middle are steps in the BPEL process (assign, invoke, copy etc.)

Spaghetti BPEL, welcome to hell!!!

[![](/legacy/assets/images/2008/10/5c27a9b7f16f-rules_and_bpel.png)](</assets/images/2008/10/18403e0ab3ea-rules_and_bpel.png>)(click to enlarge)

> **📷 Missing image** — _(click to enlarge)_

An alternative is to use rules to manage your business process. A purely rules based approach would use a rule set as a content based router and every decision point becomes an evaluation of your business routing rules. In addition, rules can manage service invocation by making the service invocation the consequence of firing into another rule set. Coupled with a BRMS like Guvnor the rules based process orchestration of services becomes accessible by business users in a managed environment. Coupled with a workflow or integration engine like Drools-Flow or Apache Camel the rules based business process management will allow for the management of complex long running business processes without some of the complexity and development overhead introduced by BPEL. The rules manage the decision points and the workflow engine helps manage the progression through your business process. The rules based approach won’t provide everything that you get with BPEL. For example state management, persistence, and ease of integration with WSDL are all advantages that BPEL provides that you wouldn’t get for free with a rules driven approach. In the end a rules based approach to business process orchestration should provide simplicity, modularity, and ease of development. As an architect it is worth considering a rules driven approach to business process management.