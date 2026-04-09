---
layout: post
title: "Drools halves memory use with new \"True Modify\" algorithm"
date: 2010-03-30
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/03/drools-halves-memory-use-with-new-true-modify-algorithm.html
---

Edson and I finally merged in our latest Rete algorithm improvements and fixed the last bugs; with a herculean effort by Edson to isolate the memory leak issue highlighted to us by Geoffrey De Smet using his Planner example. The initial results show the work was definitely worth while.

The original motivation for this change was from our high end users running large and intensive stateful engines. They found Drools, while favourable compared to our competition, in these large environments was still using large amount of memory and having garbage collection issues; where the GC could not keep up with the rate of allocation and usage and exhibiting very high peaks and troughs.

The latest change introduces something we dubbed “true modify”, although we need a better technical name for it, maybe “tree preserving updates”, so that it matches the previous Drools 5.0.x algorithm change “tree based removal” for retractions. I previously explained “true modify” in more detail [here](<http://blog.athico.com/2010/01/rete-and-true-modify.html>). The gist of it is that previously an update in the Rete algorithm would pass through the network twice with a retract and then an assert. This meant the network of partial matches that form the Rete tree would be blown away and rebuilt. In cases where only a small amount of the tree genuinely changed it was quite a waste, because it recreated what already existed. True modify performs a single pass through the network and attempts to preserve and re-use partial matches where they where true before and continue to be true now.

Less intensive applications won’t see much difference, for instance Manners and Waltz are unchanged, but applications with a large number of objects with repeated modifications should benefit. Using the Drools Planner example as our initial test case for the new algorithm changes we found a 35% speed gain, but more importantly we managed a 50% peak memory reduction with a resulting much smoother curve. We recorded the 5.0.x and trunk graphs and you can see the results for yourself below. I’m hoping our users running truly large, close to 8GB, systems might even receive greater gains; I’ll post any results fed back to us.

[![](/legacy/assets/images/2010/03/59223bc39c27-telemetry_2.png)](</assets/images/2010/03/f1016dc32e33-telemetry_2.png>)  
[5.0.x (click to enlarge))](</assets/images/2010/03/f1016dc32e33-telemetry_2.png>)

[![](/legacy/assets/images/2010/03/ea31da89f696-telemetry.png)](</assets/images/2010/03/faffd5ac4b52-telemetry.png>)  
[trunk (click to enlarge)](</assets/images/2010/03/faffd5ac4b52-telemetry.png>)

> **📷 Missing image** — _trunk (click to enlarge)_