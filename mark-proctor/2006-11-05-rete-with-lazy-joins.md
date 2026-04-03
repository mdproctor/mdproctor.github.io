---
layout: post
title: "Rete with Lazy Joins"
date: 2006-11-05
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/11/rete-with-lazy-joins.html
---

I’ve just spent the last four weeks stuck in front jProfiler taking JBoss Rules performance to the next level and the results have been great and well beyond what I hoped. To achieve this I wrote custom collections, unrolled loops and cached variables that are used repeatedly for join attempts. I really feel I’ve taken traditional Rete implementations with the following well known performance enhancements node sharing, alpha node hashing and beta node hashing to the limit. Yet I’m still way off OPSJ levels of performance for manners128 and waltz50.

My initial thought was that OPSJ must be doing some kinda of compile time/static agenda, like JRules attempts. This idea was slated for investigation when I next tackle performance again. The idea with compile time/static agenda’s is that you arrange the nodes and their memories so that propagations and joins occur in such a way that they mimick the results of a simple lifo style agenda and thus they can fire as soon as they hit the terminal node. You gain speed as you are no longer determining all cross products and conflict sets, this is kind of a cross between Rete and Leaps.

I have recently had the pleasure of exchanging a few emails with Charles Forgy, Earnest Friedman-Hill and a few others where ofcourse I just had to take the opportunity to quiz Charles Forgy on this. Here was his reply “OPSJ does not do compile-time static analysis to avoid computing conflict sets. It computes complete conflict sets, and it applies full MEA analysis to the conflict set (not some less-expensive composite pseudo-MEA)”. I was gob smacked and straight away went to off to verify this:

![Missing: Waltz on OPSJ benchmark results](/legacy/assets/images/missing-image.svg)📷 Waltz on OPSJ — benchmark chart (image unavailable)

Waltz on OPSJ (results given to me):  
Added To Agenda: 29,910  
Fired : 14,067

![Missing: Waltz on JBoss Rules benchmark results](/legacy/assets/images/missing-image.svg)📷 Waltz on JBoss Rules — benchmark chart (image unavailable)

Waltz on JBoss Rules:  
Added To Agenda: 31,841  
Fired : 14064

The differences are most likely due to my “less-expensive composite pseudo-MEA” conflict resolution strategy. These results proved Charles’ statement true and after having spent four weeks taking true Rete to what I thought was the limit it left me feeling like the twelve year old kid who thought he could play football with the adults.

Anyway not to be detered I went back to racking my brains again. One of the great things about systems like OPSJ and Jess is they give you something to aim for, without those markers I would probably have given up on trying to improve Rete long ago and opted for a compile time/static agenda like JRules has done. So here goes my next attempt at double guessing OPSJ :)

In my latest drools code my hashing system does two things, firstly it allows for indexing of composite fields and secondly it returns a bucket where it guarantees that all iterated values are already true for the indexed fields, you do not need to test them again – only further non “==” fields for that join node. Inside a join node I return this bucket and join and propagate for each iterated value. However imagine if instead of iterating over that bucket you simple give a reference from the incoming token to that bucket and propagate forward – so by the time it reaches the Agenda there have been no joins but it has references to all the buckets that contain potential successful joins – I use the term “potential” as the bucket may contain un-indexed fields due to field constraints with non “==” operators. The joining process is then delayed right until the activation is finally fired. Obviously there are still a huge number of details to work out and I’m still not totally sure if this would work, especially if a join node refers to variable constraints that are in a buckets that contains non “==” operators, as you cannot be sure that you should be testing and joining those.

For Manners i’m pretty sure this works as the “find_seating” rule as two ‘not’ nodes with only “==” constraints. For waltz it’s more difficult as all joins also have “!=” in them. Still I have enough of an idea now that I can start messing with code to try and do a proof of concept.