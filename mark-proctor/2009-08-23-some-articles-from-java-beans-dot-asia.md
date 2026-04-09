---
layout: post
title: "Some articles from Java Beans dot Asia"
date: 2009-08-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/08/some-articles-from-java-beans-dot-asia.html
---

[Java Beans dot Asia](<http://javabeans.asia/>) is building up a nice set of Drools articles, so I thought I’d list them here, quoting opening paragraph from each article. I notice a few could do with updating to Drools 5.0, so I’m looking forward to the updates – keep up the good work.

[Drools – writing DSL for DRL rule](<http://javabeans.asia/2009/08/22/drools_writing_dsl_for_drl_rule.html>)  
“One of the blog readers, who posted a comment in my previous post [Drools – tutorial on writing DSL template](<http://javabeans.asia/2008/10/24/drools_tutorial_on_writing_dsl_template.html>) asked to me to help him with creating DSL for the following rule, so I decided to use his example as a small case study:”

```drl
Brainteaser Drools: Testing Objects
Question(s):
Which of the two rules does valid comparison of the two Customer instances?
Which of the two rules is invalid? Why?
```

[Drools – tutorial on writing DSL template](<http://javabeans.asia/2008/10/24/drools_tutorial_on_writing_dsl_template.html> "Drools - tutorial on writing DSL template")  
Few months ago I wrote a [post](<http://javabeans.asia/2008/05/11/drools_working_with_stateless_session.html>) that describes an example that uses source DRL in conjunction with DSL template. In the current post, I want to describe and show with few examples how to write DSL template – whats allowed and whats not.

[Drools – Stop executing current agenda group and all rules](<http://javabeans.asia/2008/06/09/drools_stop_executing_current_agenda_group_and_all_rules.html> "Drools - Stop executing current agenda group and all rules")  
Sometimes, depends on your business rules in your application, there is a need to stop current agenda group or all rules from continuing to execute. It wont help setting a focus to another agenda group, since previous agenda will still remain in a stack. So in this post I want to show how to prevent rules in a particular agenda group from continuing to execute by clearing the agenda and also how to stop all rules totally.

[Drools – working with Stateless session](<http://javabeans.asia/2008/05/11/drools_working_with_stateless_session.html> "Drools - working with Stateless session")  
Drools (now it is also called JBoss Rules) is an amazing open source framework which allows you to create business rules management system for your application. I got introduced to Drools while working on a project at my current company.