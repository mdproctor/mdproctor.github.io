---
layout: post
title: "Making decisions with Rule Flow and more wonderful screenshots :)"
date: 2007-05-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/making-decisions-with-rule-flow-and-more-wonderful-screenshots.html
---

Kris has worked his magic again and it’s now possible to make decisions on ‘split’ and ‘join’ nodes in Rule Flow. ‘split’ nodes now support ‘and’, ‘or’ and ‘xor’ type decisions while ‘join’ supports ‘and’ and ‘or’. The beautiful part of this is its fully tooled and the decisions are specialised rules, so you can leverage the facts in the working memory and our powerful rule language.

The first screenshot (click to enlarge) shows the Constraint Editor on a ‘split’ node with an entry for each branch. At the bottom you will see the standard properties editor with the properties for the ‘split’ node, the node type is ‘xor’ and if you click the dotted builder icon on the constraints property it opens the Constraint Editor.  
[![](/legacy/assets/images/2007/05/283a1e455037-rulflow1.PNG)](</assets/images/2007/05/04faff9fae27-rulflow1.PNG>)  
This screenshot (click to enlarge) shows the form used while editing the constraints for a particular branch. Note how you can use standard left hand side (LHS) language statements. We still have to get context assist and code highlighting into the editor, but that will be coming soon, I just have to persuade Kris to give up sleep this weekend :)  
[![](/legacy/assets/images/2007/05/36ca9934a932-rulflow2.PNG)](</assets/images/2007/05/753c17247c73-rulflow2.PNG>)