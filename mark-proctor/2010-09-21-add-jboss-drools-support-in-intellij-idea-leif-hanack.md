---
layout: post
title: "Add JBoss Drools Support In IntelliJ IDEA (leif.hanack)"
date: 2010-09-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/09/add-jboss-drools-support-in-intellij-idea-leif-hanack.html
---

<http://blog.strug.de/2010/09/add-jboss-drools-support-in-intellij-idea/> (leif.hanack)

Do you use Drools, a very popular rule engine? Do you use IntelliJ IDEA? Then this post might be interesting for you!

Peter Gromov showed me the power of [custom file types](<http://blogs.jetbrains.com/idea/2010/09/custom-file-types-in-intellij-idea/>). Another secret I discovered in the world’s greatest Java IDE.

I followed his advice and created a custom file type for DRL files.

[![](/legacy/assets/images/2010/09/9a20a505c5f6-idea-drl-support.png)](<http://blog.strug.de/wp-content/uploads/idea-drl-support.png>)

Nice, isn’t it? Besides the coloring you get:

  * basic code completion (all configured keywords)
  * support braces, brackets, parens, string escapes
  * 4 different keyword sets (4 different colorings)
  * Comment/Uncomment lines (Mac: Command-/)
  * Block-Comment/Uncomment (Mac: Control-?)

You can easily import this [IDEA drl file type](<http://blog.strug.de/wp-content/uploads/idea-drl-file-type.zip>) with _File > Import Settings.._. I didn’t tried to import them, so back up your settings please.

You want more? Go and vote for [IDEA-24348](<http://youtrack.jetbrains.net/issue/IDEA-24348>).