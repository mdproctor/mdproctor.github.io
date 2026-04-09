---
layout: post
title: "Drools Puzzle"
date: 2007-08-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/08/drools-puzzle.html
---

(updated on June 01, 2008)

Drools Puzzle is a periodic puzzle-solving contest. Anybody can compete in a round except the puzzle poster himself. Time for problem-solving cycle is adapted to the difficulty of the puzzle, varies from two weeks to several months. Puzzles are chosen by the winner of last round or the organizer. A participator can post her solution to

droolspuzzle@gmail.com

for evaluation. If the solution has very big size, you can upload it to any FTP server and post the download link to the email address above.

The evaluator must evaluate all submissions within two days of the submission deadline and post the result report within three days after the evaluation. All solutions should be evaluated on a same computer, under the same software configuration.

Every participator gets accumulated scores, even if she does not win. After each ten rounds, the top one on the score list will earn a “Drools Puzzle Cracker” award and there will be materialized prize from the Drools team too. Since the score is accumulated, it’s possible for a person to win this award if she participates in every round but never really won. The evaluator(s) should try their best to quantify the quality of the submissions as reasonable and analytical as possible.

If any bug in the Drools framework is caught during your solving of the Drools Puzzle, please report it and you will get a T-shirt from the Drools team.

**Rule for participation:**

  * The solution (the core algorithm) must be written in Drools. Eligible Drools version changes over the time and should be decided by the puzzle poster. For now, it’s recommended for all participators to write rules against Drools 4.0.0, so that there is much less work for the evaluator. Employment of any component in the Drools project is allowed. For example, the use of drools-solver is welcome.
  * In the rule definition file, any dialect of the expression language is allowed. You can declare rules in Java, MVEL, … and even mix them in a single rules definition file. Any DSL is allowed but you have to provide the language adapter.
  * Any kind of user interface is allowed. You can even submit a .ear file or .war file. Evaluators know how to measure the performance for your core algorithm. Any overhead for fancy UI rendering in your program will be ignored.
  * The solution program should be as easy to test as possible. Testability also counts in the evaluation.
  * Please provide a readme file with instructions about how to run your program. It is especially important if you submit a .war file or .ear file, you must tell the evaluator which web container to use and how to deploy it.
  * _Please do not paste your code in the email body_ , package your program files and the readme file and attach it in your email.
  * In principle, this contest is for native droolers. However, if you are really interested in the puzzle and want to send in solutions in, let’s say, CLIPS, or Lisp, or Prolog, or C/C++, or Ruby, yes, your solution will be evaluated and commented, since compilers and runtime of all the above languages are not difficult to get. But please add one line or two in your readme file about how to run your program.

**The purposes of this contest** :

  * To learn from each other in the Drools community. Improve our programming skill and learn good algorithms and good implementations.
  * To encourage people to explore features of Drools.
  * For fun.

**Guideline for winnders** :

  * Please consider a proper difficult level for the puzzle you are going to post. It should neither be too difficult nor too easy, and it should be easy for yourself to test the solutions. Puzzles like “Please prove that integrating and configuring software components using Drools is better than using xxxx-ESB” might be doable conceptually but you will need a whole suite of existing components and a whole stack of complex use cases to test the solutions.
  * The puzzles do not have to be backward-tracking-driven (goal-driven) logic puzzles. You may well post a forward-tracking-driven (data-driven) problem and provide an initial data configuration.

That’s it for now. Constructive advice and suggestion about this contest from the community will be taken here.

List of past rounds (including current one)

  1. [Round 1: Ages of the Sons (With result report)](<http://blog.athico.com/2007/08/drools-puzzle-round-1-ages-of-sons.html>)
  2. [Round 2: The Family Puzzl  
](<http://blog.athico.com/2007/08/drools-puzzle-round-2-familiy-puzzle.html>), and [the result report](<http://ningning.org/blog2/2008/05/25/drools-puzzles-result-round-2-the-familiy-puzzle>).