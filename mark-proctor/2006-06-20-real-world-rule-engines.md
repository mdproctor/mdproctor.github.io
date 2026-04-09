---
layout: post
title: "Real World Rule Engines"
date: 2006-06-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/06/real-world-rule-engines.html
---

### Real World Rule Engines

Here is an excellent article, introduction reproduced below, from our very own mailing list mentor Geoffrey Wiseman:  
<http://www.infoq.com/articles/Rule-Engines>

For many developers, rule engines are buzzwords, or black boxes on an architectural diagram: something to be feared or admired from afar, but not understood. Coming to terms with this, is one of the catch-22s of technology:

  * It’s difficult to know when to use a technology or how to apply it well until you’ve had some first-hand, real-world experience.
  * The most common way to gain that experience is to use an unknown technology in a real project.
  * Getting first-hand experience using a new technology in a production environment is an invaluable experience for future work but can be a major risk for the work at hand.

Over the course of this article, I’ll be sharing my practical experience with rule engines and with Drools in particular to support in-market solutions for financial services, in order to help you understand where rule engines are useful and how to apply them best to the problems you face.

## Why Should I Care?

Some of you will have already considered using a rule engine and will be looking for practical advice on how to use it well: patterns and anti-patterns, best practices and rat-holes.

Others haven’t considered using a rule engine, and aren’t sure how this is applicable to the work you’re doing, or have considered rule engines and discarded the idea. Rule engines can be a powerful way to externalize business logic, empower business users, and solve complicated problems wherein large numbers of fine-grained business rules and facts interact.

If you’ve ever taken a series of conditional statements, tried to evaluate the combinations, and found yourself writing deep nested logic to solve a problem, these are just the sorts of entanglements that a rule engine can help you unravel.

Some of our more complicated financial services work, when rephrased in a rule approach, began to look markedly more comprehensible. Each step in converting procedural conditional logic to Drools business rules seemed to expose both more simplicity and more power at once.

Finally, if you’re not convinced by the above, consider this: rule engines are a tool, another way to approach software development. Tools have their strengths and weaknesses, and even if you aren’t making immediate use of this one, it’s helpful to understand the tradeoffs so that you can assess and communicate applicability in the future.