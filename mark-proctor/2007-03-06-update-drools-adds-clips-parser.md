---
layout: post
title: "update - Drools adds Clips parser"
date: 2007-03-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/03/update-drools-adds-clips-parser.html
---

### [update – Drools adds Clips parser](<https://blog.kie.org/2007/03/update-drools-adds-clips-parser.html>)

Progress is going well with the Clips parser I now have the full LHS working, exception functions. That includes the ‘and’, ‘or’, ‘not and exists conditional elements, with full nesting, including ‘and’ and ‘or’ inside the ‘not’ and ‘exists’. Patterns work with literals, bound variables, predicates and return values. I’m now working on functions at which point we should be able to execute Clips rules inside the JBoss Rules engine. Probably the hardest part with functions is finding a sane way to deal with primitives in functions, especially built in Math functions. After that we’ll look at mapping our ‘accumulate’, ‘collect’, ‘forall’ and ‘from’ implementations.