---
layout: post
title: "Drools 5.5, 6.0 and The Future"
date: 2012-07-04
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/07/drools-5-5-6-0-and-the-future.html
---

Some time soon we will branch master. The current master will be branched to 5.5 and then master will become 6.0.

We will develop 5.5 and 6.0 in parallel. In general we will try to apply as many bug fixes and stable features to both branches, for as long as it’s practically possible. At some point 6.0 will diverge too much and the cost will become too high.

I hope we can release a 5.5 within the next 4-5 months; this may very depending on the impact of other commitments.

6.0 will be a longer term effort, and will involve the most drastic changes at both the engine and language level to date. The engine algorithm will be almost completely new, and will no longer be considered a Rete implementation. Instead it will be a lazy collection oriented matching algorithm, that will support adaptive network topologies. First we’ll deliver the lazy matching algorithm and then shift to collection oriented. The adaptive network topologies will take more time and may deliver after 6.0. These engine changes will lay the ground work for exploiting multi-cpu architectures, and durable backing stores (Active Databases). I also hope we can integrate our engine with a tableaux algorithm, to provide seamless description logic capabilities for semantic ontologies; but that’s still a very open research area, with many unknowns.

6.0 will most likely retain api comparability (no current plans to break it), however the DRL syntax will be broken. DRL has been backwards compatible, excluding bugs and regressions, for almost 7 years now. We plan to take this opportunity to revamp DRL, as we fully embrace becoming a hybrid reasoning engine. We will fully explore passive, reactive, relational and functional programming styles. The hope is we can create a declarative language system, more flexible and more suitable for a wider range of solutions. I also really want to address some of the usability problems associated with rule execution control, particularly around salience and the various rule groups (agenda-groups, ruleflow-groups, activation-groups). Relative salience and a single concept around a flexible RuleModule will hopefully make this possible. We have to start making things easier, simpler and more consistent.

We are just starting to flesh out our designs, figuring out what works and what doesn’t. All are at the very early stages, much has not yet been added, and everything is open to debate.

General rule syntax

<https://community.jboss.org/wiki/Drools60>

The event sequencing draft can be found here:

<https://community.jboss.org/wiki/EventSequencing>

The functional programming aspects are still being explored on this wiki page:

<https://community.jboss.org/wiki/FunctionalProgrammingInDrools>

We will eventually roll the later two back in the Drools60 document, to provide a single document that covers the 6.0 language specific.

The web based tooling is also under going a revamp. It will offer a more flexible workbench like experience where all panels are plugins, with support for perspectives. This will allow us to build a consistent and unified approach to our web tooling efforts across Drools&jBPM. We also have a mechanism now that will allow our web based components, such as decision tables and guided editors to be used in Eclipse – to create a consistent experience between the two environments. We have back ported the java7 vfs api and have a Git implementation for this, we will also continue provide a JCR implementation. So far Git is looking extremely scalable and easy to use. JGit provides a full java implementation, making out of the box use easy. Stay tuned for more news. Hopefully in less then 2 months we will have some early proof of concepts to show, for the web based efforts.

If you want to help make history happen, joins us on irc (real time chat). You can also leave comments on the wiki pages or the mailing lists (developer list).

<http://www.jboss.org/drools/irc>

<http://www.jboss.org/drools/lists>

Here goes nothing!!!

Mark