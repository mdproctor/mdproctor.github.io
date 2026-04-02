---
layout: post
title: "update - Drools adds Clips parser"
date: 2007-03-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/03/update-drools-adds-clips-parser.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [update – Drools adds Clips parser](<https://blog.kie.org/2007/03/update-drools-adds-clips-parser.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 6, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Progress is going well with the Clips parser I now have the full LHS working, exception functions. That includes the ‘and’, ‘or’, ‘not and exists conditional elements, with full nesting, including ‘and’ and ‘or’ inside the ‘not’ and ‘exists’. Patterns work with literals, bound variables, predicates and return values. I’m now working on functions at which point we should be able to execute Clips rules inside the JBoss Rules engine. Probably the hardest part with functions is finding a sane way to deal with primitives in functions, especially built in Math functions. After that we’ll look at mapping our ‘accumulate’, ‘collect’, ‘forall’ and ‘from’ implementations.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fupdate-drools-adds-clips-parser.html&linkname=update%20%E2%80%93%20Drools%20adds%20Clips%20parser> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fupdate-drools-adds-clips-parser.html&linkname=update%20%E2%80%93%20Drools%20adds%20Clips%20parser> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fupdate-drools-adds-clips-parser.html&linkname=update%20%E2%80%93%20Drools%20adds%20Clips%20parser> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fupdate-drools-adds-clips-parser.html&linkname=update%20%E2%80%93%20Drools%20adds%20Clips%20parser> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fupdate-drools-adds-clips-parser.html&linkname=update%20%E2%80%93%20Drools%20adds%20Clips%20parser> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fupdate-drools-adds-clips-parser.html&linkname=update%20%E2%80%93%20Drools%20adds%20Clips%20parser> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fupdate-drools-adds-clips-parser.html&linkname=update%20%E2%80%93%20Drools%20adds%20Clips%20parser> "Email")