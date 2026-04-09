---
layout: post
title: "Drools Solver"
date: 2007-09-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/09/drools-solver.html
---

Geoffrey De Smet has been busy working on the Drools Solver module, which will hopefully be part of the next major Drools release. Drools solver aims to efficiently solve search based problems finding a valid solution from large search areas. It currently provides implementations for Tabu, simulated annealing and Local search. I personally hope to expand the system for Genetic Algorithms in the future, I’ll have a good look at jgap too see if we can provide true value over existing systems.

Geoffrey has started to flesh out the manual and is looking for feedback, it focuses on explaining the engine via solving the N-Queens problems.

[Drools Solver Manual](<http://users.telenet.be/geoffrey/tmp/solver/manual/html_single/>)

Drools Solver provides a framework for searching and uses Drools to provide the scoring, moves themselves are still done in Java code. I know that Geoffrey long term is hoping to have the move instructions also as part of the DRL.

> **📷 Missing image** — _screenshotSolvedNQueens8_