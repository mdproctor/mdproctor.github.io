---
layout: post
title: "Rule Analytics - Looking at the AST (Toni Rikkola)"
date: 2007-06-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/rule-analytics-looking-at-the-ast-toni-rikkola.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Rule Analytics – Looking at the AST (Toni Rikkola)](<https://blog.kie.org/2007/06/rule-analytics-looking-at-the-ast-toni-rikkola.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 15, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I spent last weekend testing JRuby. I found out that some things would be easier using JRuby some things using Java, this was of course to be expected.

First days of this week I used to design a model that would help me to test rules.

JBoss Rules forms an abstract syntax tree (AST) from the rules it gets from rule base. This AST is done using Java, so the problem is that rule engines do not support object-oriented model that well, and as I am mainly using JBoss Rules to find conflicts I need to find another way. So Michael Neale told me to think about relations like the ones used in SQL databases, using this advise I added an identifier to all my objects and information of parent objects so that the relations could be solved. After this I could test small cases that were under And or Or descriptions, but this is not enough, because I would need to form loops to check for conflicts in the entire rule. Loops would be too messy to use, so I needed an other solution.

After some brain work, I realized that if I can get a list of all of the simpler clauses that can be formed from one rule, I can use those clauses to test conflicts inside this rule. Lets look at how this looks in the Rules drl file:

**rule** “Rule that causes warning”  
**when**  
Foo(bar == “baz” && ( xyz ==“123” || bar != “baz” ) )**  
then**  
# Do something**  
end**

This rule looks for Foo objects from working memory, if object Foo has parameters that match the definitions set inside the brackets it does something.  
So all the simpler clauses for definitions inside object Foo would be:

> bar == “baz” && xyz == “123”  
> bar == “baz” && bar != “baz”

This rule has an error because obviously parameter bar can not be equal to “baz” and at the same time be unequal to “baz”. On these kind of situations the RAM could check the rules and inform the user that he or she has a rule that can be true, but has an condition that can never be true. Other warnings are for example: Foo( x > 42 || x < 42 ) this would give a warning that possibility x == 42 is not taken care of. Only problem now is that how can I form all the possible clauses from the AST.

Yesterday and today I’ll be looking at how the feed back from rule checks should work. Michael Neale said that the feed back would be in XML and it could then be transformed to for example HTML. Proctor and Neale also suggested some books that could help, so last Tuesday I got Expert Systems: Principles and Programming by Joseph Giarratano and Gary D. Riley, I’ll be reading that on next weekend.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Frule-analytics-looking-at-the-ast-toni-rikkola.html&linkname=Rule%20Analytics%20%E2%80%93%20Looking%20at%20the%20AST%20%28Toni%20Rikkola%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Frule-analytics-looking-at-the-ast-toni-rikkola.html&linkname=Rule%20Analytics%20%E2%80%93%20Looking%20at%20the%20AST%20%28Toni%20Rikkola%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Frule-analytics-looking-at-the-ast-toni-rikkola.html&linkname=Rule%20Analytics%20%E2%80%93%20Looking%20at%20the%20AST%20%28Toni%20Rikkola%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Frule-analytics-looking-at-the-ast-toni-rikkola.html&linkname=Rule%20Analytics%20%E2%80%93%20Looking%20at%20the%20AST%20%28Toni%20Rikkola%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Frule-analytics-looking-at-the-ast-toni-rikkola.html&linkname=Rule%20Analytics%20%E2%80%93%20Looking%20at%20the%20AST%20%28Toni%20Rikkola%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Frule-analytics-looking-at-the-ast-toni-rikkola.html&linkname=Rule%20Analytics%20%E2%80%93%20Looking%20at%20the%20AST%20%28Toni%20Rikkola%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Frule-analytics-looking-at-the-ast-toni-rikkola.html&linkname=Rule%20Analytics%20%E2%80%93%20Looking%20at%20the%20AST%20%28Toni%20Rikkola%29> "Email")