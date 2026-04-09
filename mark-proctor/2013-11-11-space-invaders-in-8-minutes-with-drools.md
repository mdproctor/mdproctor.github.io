---
layout: post
title: "Space Invaders in 8 minutes with Drools"
date: 2013-11-11
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2013/11/space-invaders-in-8-minutes-with-drools.html
---

Following in the same fashion of [Pong](<http://www.youtube.com/watch?v=Omj4PR3v-nI>) and [Wumpus World](<http://www.youtube.com/watch?v=4CvjKqUOEzM>), I’ve written a simplified Space Invaders game. I’ve uploaded it to youtube, make sure you watch it in high quality and full screen, to avoid blur text:  
<http://www.youtube.com/watch?v=wORlAZoxttA>

It’s not the complete game, but in it’s current form is simpler than Pong or Wumpus World; so it’s a better place to start learning. I’ve written it, with re-use in mind, such as the configuration classes and key rules, to be re-used in other games; although they will need refactoring first. For Invaders I’ve committed each stage of the game, as separate files, so it’s easy to see the stages for yourself.

The model classes and the 6 mains are here:  
<https://github.com/droolsjbpm/drools/tree/master/drools-examples/src/main/java/org/drools/games/invaders>

The 6 drl folders for each of the mains are here:  
<https://github.com/droolsjbpm/drools/tree/master/drools-examples/src/main/resources/org/drools/games>

This embed could not be captured in the archive. Original source: unknown source