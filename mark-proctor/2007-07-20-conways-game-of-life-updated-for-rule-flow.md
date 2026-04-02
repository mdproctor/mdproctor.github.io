---
layout: post
title: "Conways Game of Life updated for Rule Flow"
date: 2007-07-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/conways-game-of-life-updated-for-rule-flow.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Conways Game of Life updated for Rule Flow](<https://blog.kie.org/2007/07/conways-game-of-life-updated-for-rule-flow.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 20, 2007  
[Process](<https://blog.kie.org/category/process>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

As promised I finally got round to updating the popular Conways Game of Life example so it can be executed with both agenda-groups and ruleflows for execution control. So now people have a good example to study when trying to learn the two concepts. (click to enlarge images).

With agenda-groups we specify the stack execution order for each group, in the java code.  
[![](/legacy/assets/images/2007/07/5dc24f3cb8d5-agendagroupNextGeneration.PNG)](<http://bp2.blogger.com/_Jrhwx8X9P7g/RqAmKLDoz2I/AAAAAAAAAEM/YicZyJD_6II/s1600-h/agendagroupNextGeneration.PNG>)  
With ruleflow we instead specify the process id of the ruleflow:  
[![](/legacy/assets/images/2007/07/6388630f2781-ruleflowNextGeneration.PNG)](<http://bp1.blogger.com/_Jrhwx8X9P7g/RqAnI7Doz3I/AAAAAAAAAEU/XJairGbjUGU/s1600-h/ruleflowNextGeneration.PNG>)  
Here you can see the ruleflow for the above process id, notice how “birth” and “kill” are executed in parallel:  
[![](/legacy/assets/images/2007/07/6dd9b6779478-conwayRuleFlow.PNG)](<http://bp1.blogger.com/_Jrhwx8X9P7g/RqAna7Doz4I/AAAAAAAAAEc/2EM7CDuiYOo/s1600-h/conwayRuleFlow.PNG>)  
This code is in trunk, and will be part of the next release for drools-examples.

From working on this example what has become obvious is we need support for sub ruleflows, so that we can have a parent ruleflow choreographing all the ruleflows in the application, which is currently being done from java code.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fconways-game-of-life-updated-for-rule-flow.html&linkname=Conways%20Game%20of%20Life%20updated%20for%20Rule%20Flow> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fconways-game-of-life-updated-for-rule-flow.html&linkname=Conways%20Game%20of%20Life%20updated%20for%20Rule%20Flow> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fconways-game-of-life-updated-for-rule-flow.html&linkname=Conways%20Game%20of%20Life%20updated%20for%20Rule%20Flow> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fconways-game-of-life-updated-for-rule-flow.html&linkname=Conways%20Game%20of%20Life%20updated%20for%20Rule%20Flow> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fconways-game-of-life-updated-for-rule-flow.html&linkname=Conways%20Game%20of%20Life%20updated%20for%20Rule%20Flow> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fconways-game-of-life-updated-for-rule-flow.html&linkname=Conways%20Game%20of%20Life%20updated%20for%20Rule%20Flow> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fconways-game-of-life-updated-for-rule-flow.html&linkname=Conways%20Game%20of%20Life%20updated%20for%20Rule%20Flow> "Email")