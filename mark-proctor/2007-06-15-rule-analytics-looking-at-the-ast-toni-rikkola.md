---
layout: post
title: "Rule Analytics - Looking at the AST (Toni Rikkola)"
date: 2007-06-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/rule-analytics-looking-at-the-ast-toni-rikkola.html
---

I spent last weekend testing JRuby. I found out that some things would be easier using JRuby some things using Java, this was of course to be expected.

First days of this week I used to design a model that would help me to test rules.

JBoss Rules forms an abstract syntax tree (AST) from the rules it gets from rule base. This AST is done using Java, so the problem is that rule engines do not support object-oriented model that well, and as I am mainly using JBoss Rules to find conflicts I need to find another way. So Michael Neale told me to think about relations like the ones used in SQL databases, using this advise I added an identifier to all my objects and information of parent objects so that the relations could be solved. After this I could test small cases that were under And or Or descriptions, but this is not enough, because I would need to form loops to check for conflicts in the entire rule. Loops would be too messy to use, so I needed an other solution.

After some brain work, I realized that if I can get a list of all of the simpler clauses that can be formed from one rule, I can use those clauses to test conflicts inside this rule. Lets look at how this looks in the Rules drl file:

```drl
rule “Rule that causes warning”
 when
 Foo(bar == “baz” && ( xyz ==“123” || bar != “baz” ) )
 then
 # Do something
end
```
This rule looks for Foo objects from working memory, if object Foo has parameters that match the definitions set inside the brackets it does something.  
So all the simpler clauses for definitions inside object Foo would be:
```java
bar == “baz” && xyz == “123”
bar == “baz” && bar != “baz”
```

This rule has an error because obviously parameter bar can not be equal to “baz” and at the same time be unequal to “baz”. On these kind of situations the RAM could check the rules and inform the user that he or she has a rule that can be true, but has an condition that can never be true. Other warnings are for example: Foo( x > 42 || x < 42 ) this would give a warning that possibility x == 42 is not taken care of. Only problem now is that how can I form all the possible clauses from the AST.

Yesterday and today I’ll be looking at how the feed back from rule checks should work. Michael Neale said that the feed back would be in XML and it could then be transformed to for example HTML. Proctor and Neale also suggested some books that could help, so last Tuesday I got Expert Systems: Principles and Programming by Joseph Giarratano and Gary D. Riley, I’ll be reading that on next weekend.