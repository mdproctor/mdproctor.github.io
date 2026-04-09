---
layout: post
title: "My rules don't work as expected. What can I do?"
date: 2007-07-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/my-rules-dont-work-as-expected-what-can-i-do.html
---

A good blog [entry](<http://rbs.gernotstarke.de/faq/faq/faq-devel.html>) from Dr. Gernot Starke, I love the opening paragraph, which can’t be said enough :)  
“Welcome to real life. Don’t ever believe that rules can and will be written by business-people only.”

Another useful titbit is to use an Agenda Filter with a Stateless Session. You use the AgendaFilter to isolate the rule(s) you wish to test. The Agenda Filter can be setup just once on the session and then collections of data can be executed against the session. You can then change the Agenda Filter when you wish to test a different rule.

```java
StatelessSession session = ruleBase.newStatelessSesssion();session.setAgendaFilter( new RuleNameMatches("<regexp to your rule name here>") );List data = new ArrayList();... // create your test data here (probably built from some external file)StatelessSessionResult result == session.executeWithResults( data );// check your results here.
```