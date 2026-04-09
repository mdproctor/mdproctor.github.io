---
layout: post
title: "Expert System in a Gaming Enviroment"
date: 2011-04-04
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/04/expert-system-in-a-gaming-enviroment.html
---

Found this blog on expert systems for game environments, thought others might like it:  
<http://wiki.bath.ac.uk/display/BISAI/Expert+System+in+a+Gaming+Enviroment>

Intro paragraph snippet:  
“Following on from the research this section will explain how an expert system function works within the gaming environment. The goal of this expert system is to select which weapon to use during game play, of which this depends on a number of different variables that are changing every frame, therefore the expert system will make a decision. This page will explain through the following:

  * Analysis of the gaming environment, listing variables, expert knowledge and static data.
  * Assumptions made in the creation of the expert system e.g. **confidence factor, forward chaining**
  * How the facts are derived from game play itself.
  * How the inference engine decides which rules to run using data from **working memory** and **knowledge base**.
  * Weapon Selection example using the expert system

Depicting the diagram shown in [Types of gaming AI](<http://wiki.bath.ac.uk/display/BISAI/Research+-+Types+of+AI> "Research - Types of AI") under expert system, there are a few requirements into developing a weapon selection AI system, and they are as follows:

  * From game play what are the input variables, or changing environmental data, i.e. target range, target type, weapon range.
  * What is the system going to output and why? i.e. type of weapon, why choose a specific weapon, what are the weapon characteristics.

The answers to these questions are derived from the **game expert** , in this case the makers of this coursework. Therefore the **known facts** are weapon characteristics (highlighted in the table 1 below ), format of target range weapon range, and which weapon is best for achieving its goal i.e to eradicate the target.

The main reason for developing an AI is to satisfy the [objectives](<http://wiki.bath.ac.uk/display/BISAI/Objectives> "Objectives") and as the gaming environment constantly changes, the bot will constantly have to re-evaluate the situation much like a human player. Creation of an AI will improve game play and provide a challenge with the bot making its own decisions on weapon selection.”