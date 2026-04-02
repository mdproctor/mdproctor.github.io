---
layout: post
title: "What is a \"sequential\" Rule Engine"
date: 2007-06-24
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/what-is-a-sequential-rule-engine.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [What is a “sequential” Rule Engine](<https://blog.kie.org/2007/06/what-is-a-sequential-rule-engine.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 24, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

It’s very hard to find a public definition of what a “sequential” rule engine is, someone needs to update Wikipedia. My knowledge in this area is also limited so I’ve decided to write up what I know, in the hope that others can correct and add to this, so we can get a full public definition. Maybe the results can go up onto Wikipedia :)

Sequential engines are used in stateless execution environments; i.e. you cannot assert more data and call fireAllRules rules a second time. Modifying asserted data does not result in rule re-evaluation.

A Method is generated per rule in java code. The engine takes the asserted data and creates a list of the possible cross product combinations for the provided data and rules.

It then iterates over the rules, calling each in turn with the possible cross product matches from the list. The order is determined by salience and/or the order of rules in the file. When all ‘if’ statements are are true it fires straight away, there is no agenda.

If asserted data is not modified it can cache tests, which improves performance. If data is changed, you cannot cache, and further rule evaluations may not fire for the modified values.

It is the conflict set combined with data modifications that seems unclear to me, you modify data but the already checked/fired rules will never be re-evaluated for this changed data. It seems ideally sequential modes should not modify asserted data and benefit from tooling to aid in the authoring of rules so they do not result in conflicts for given sets of data, i.e. only one rule will fire.

I also don’t see how sequential will be faster if caching has to be turned off due to data modifications and you have a large number of rules.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fwhat-is-a-sequential-rule-engine.html&linkname=What%20is%20a%20%E2%80%9Csequential%E2%80%9D%20Rule%20Engine> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fwhat-is-a-sequential-rule-engine.html&linkname=What%20is%20a%20%E2%80%9Csequential%E2%80%9D%20Rule%20Engine> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fwhat-is-a-sequential-rule-engine.html&linkname=What%20is%20a%20%E2%80%9Csequential%E2%80%9D%20Rule%20Engine> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fwhat-is-a-sequential-rule-engine.html&linkname=What%20is%20a%20%E2%80%9Csequential%E2%80%9D%20Rule%20Engine> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fwhat-is-a-sequential-rule-engine.html&linkname=What%20is%20a%20%E2%80%9Csequential%E2%80%9D%20Rule%20Engine> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fwhat-is-a-sequential-rule-engine.html&linkname=What%20is%20a%20%E2%80%9Csequential%E2%80%9D%20Rule%20Engine> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fwhat-is-a-sequential-rule-engine.html&linkname=What%20is%20a%20%E2%80%9Csequential%E2%80%9D%20Rule%20Engine> "Email")