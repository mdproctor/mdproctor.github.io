---
layout: post
title: "IJTC and new Production Rule (Rete) explanation in slides"
date: 2007-11-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/11/ijtc-and-new-production-rule-rete-explanation-in-slides.html
---

Just got back from the [Irish Java Technology Conference](<http://ijtc.firstport.ie/>), for this presentation I had another go at trying to explain how a production rule engine works – the behaviour, not the algorithm. As I’ve mentioned in the past I’m finding it easier to talk about SQL to begin with, to frame people’s minds. If you jump into an example, straight away they are thinking, or asking, “how is this different from an ‘if’ statement in java”. By taking the SQL approach you hopefully break that problem.

The presentation takes 3 tables with data and shows the resulting rows for 2 different views, and how data might change if we had triggers on those views. So it gets people thinking in terms of cross products and rows of data (tuples). I then show the same data against rules and the resulting rows, which is identical to the views. Showing that basically a rule is a view on data, resulting in rows (tuples) of matched facts. The consequence is executed for each resulting row. This concept is taken further to say that if each rule is a view then the agenda is just an aggregate view of all the rule views. As you insert, retract and update data, rows are added and removed from the “agenda view”. I then introduce the idea of conflict resolution and salience, along with two phase execution, as a way to determine which of the rows in the agenda view have their consequences fired first; a new simple rule with a salience is added, along with the resulting agenda view tables show the impact of this. The presentation then goes on to touch first order logic, specifically ‘not’ and ‘accumulate’ and details our ruleflow work, the normal screen shots are supplied for explaining the rest of the capabilities of the system. I also did a populated BRMs demo at the end.

Do give me feedback on my approach to helping people understand production rule systems, via the sql and views analogy, I’d certainly like to try and improve the slides to help explain this better.

You can get the slides [here](<http://wiki.jboss.org/wiki/attach?page=JBossRules%2Fijtc.pdf>)