---
layout: post
title: "OpenRules Rule Compressor"
date: 2008-02-29
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/02/openrules-rule-compressor.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [OpenRules Rule Compressor](<https://blog.kie.org/2008/02/openrules-rule-compressor.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 29, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

The people over at [OpenRules ](<http://openrules.com/>)have developed some very cool technology with their [Rule Compressor](<http://openrules.com/RuleCompressor.htm>). Given any decision table the compressor looks for redundant rule combinations and removes them.

If I have two rows in the decision table that look like this:  
if age > 50 then decrease price by 10%  
if age > 65 then decrease price by 10%

We have redundancy there and it can be combined into a single rule:  
if age > 50 then decrease price by 10%

This is obviously a very simple case and the Rule Compressor can do much more complex combinations. I’ve taken the liberty of taking a screen shot from a section showing an example from their [Rule Compressor](<http://openrules.com/RuleCompressor.htm>) explanation page:

![](/legacy/assets/images/2008/02/55b095d5a4d8-RuleCompressor.png)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fopenrules-rule-compressor.html&linkname=OpenRules%20Rule%20Compressor> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fopenrules-rule-compressor.html&linkname=OpenRules%20Rule%20Compressor> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fopenrules-rule-compressor.html&linkname=OpenRules%20Rule%20Compressor> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fopenrules-rule-compressor.html&linkname=OpenRules%20Rule%20Compressor> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fopenrules-rule-compressor.html&linkname=OpenRules%20Rule%20Compressor> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fopenrules-rule-compressor.html&linkname=OpenRules%20Rule%20Compressor> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fopenrules-rule-compressor.html&linkname=OpenRules%20Rule%20Compressor> "Email")