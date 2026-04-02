---
layout: post
title: "Drools Solver"
date: 2007-09-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/09/drools-solver.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Solver](<https://blog.kie.org/2007/09/drools-solver.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 23, 2007  
[Optimization](<https://blog.kie.org/category/optimization>) [Article](<https://blog.kie.org/content_type/article>)

Geoffrey De Smet has been busy working on the Drools Solver module, which will hopefully be part of the next major Drools release. Drools solver aims to efficiently solve search based problems finding a valid solution from large search areas. It currently provides implementations for Tabu, simulated annealing and Local search. I personally hope to expand the system for Genetic Algorithms in the future, I’ll have a good look at jgap too see if we can provide true value over existing systems.

Geoffrey has started to flesh out the manual and is looking for feedback, it focuses on explaining the engine via solving the N-Queens problems.

[Drools Solver Manual](<http://users.telenet.be/geoffrey/tmp/solver/manual/html_single/>)

Drools Solver provides a framework for searching and uses Drools to provide the scoring, moves themselves are still done in Java code. I know that Geoffrey long term is hoping to have the move instructions also as part of the DRL.

[![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)![](https://users.telenet.be/geoffrey/tmp/solver/manual/shared/images/Chapter-Solver/screenshotSolvedNQueens8.png)](<http://users.telenet.be/geoffrey/tmp/solver/manual/shared/images/Chapter-Solver/screenshotSolvedNQueens8.png>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-solver.html&linkname=Drools%20Solver> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-solver.html&linkname=Drools%20Solver> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-solver.html&linkname=Drools%20Solver> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-solver.html&linkname=Drools%20Solver> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-solver.html&linkname=Drools%20Solver> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-solver.html&linkname=Drools%20Solver> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fdrools-solver.html&linkname=Drools%20Solver> "Email")