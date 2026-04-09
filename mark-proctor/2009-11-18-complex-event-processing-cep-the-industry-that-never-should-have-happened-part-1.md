---
layout: post
title: "Complex Event Processing (CEP) - The industry that never should have happened (Part 1)"
date: 2009-11-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/11/complex-event-processing-cep-the-industry-that-never-should-have-happened-part-1.html
---

PART 1

CEP is all the rage these days, everyone has to have one. I’m going to be lazy and just quote Wikipedia as to what CEP is, so I can quickly head into the meat of this article:  
“ _Complex Event Processing, or CEP, is primarily an event processing concept that deals with the task of processing multiple events with the goal of identifying the meaningful events within the event cloud._

CEP employs techniques such as detection of complex patterns of many events, event correlation and abstraction, event hierarchies, and relationships between events such as causality, membership, and timing, and event-driven processes.” (Wikipedia)

Some CEP examples:

  * When the average price of a stock falls below $25 over any 5 minute period, then sell.
  * When 2 transactions happen on an account from radically different geographic locations within a certain time window then report as potential fraud.
  * When a gold customer’s trouble ticket is not resolved within 1 hour, then escalate.
  * When a team meeting request overlaps with my lunch break, then deny the team meeting and demote the meeting organizer.

When talking to people about CEP the second question they ask is, “aren’t CEP statements just rules?” The first being “What’s CEP?”. They struggle to understand why we have two separate industries and approaches to what appears on the surface to be the same – i.e. when some scenario/situation in your data is detected, do something.

The reason for this is simple… they are right. Let me explain why <tongue in cheek>CEP is the industry that never should have happened</tongue in cheek>.

[![](/legacy/assets/images/2009/11/d53124eaeee1-powerofevents.png)](</assets/images/2009/11/e676d902d623-powerofevents.png>)While CEP has become the adopted term for this industry, there is some general concern about it’s inappropriateness, just google for “Tim Bass” and you’ll see plenty of comments on this. CEP is in actuality a huge research area and many CEP products, including Drools, only touch a fraction of what is possible. David Luckham’s book “The Power of Events: An Introduction to Complex Event Processing in Distributed Enterprise Systems” is considered the “bible” on this subject and shows how indeed we are only just scratching the surface. I had the luck to be at RuleML2008 where David was a keynote speaker, which was very inspirational.

Most of the engines in the market currently focus on what is actually event stream processing (ESP), which many consider to be a subset of CEP. Again Wikipedia to the rescue:

“ESP deals with the task of processing multiple streams of event data with the goal of identifying the meaningful events within those streams, employing techniques such as detection of complex patterns of many events, event correlation and abstraction, event hierarchies, and relationships between events such as causality, membership, and timing, and event-driven processes.”

(Wikipedia)

Tim Bass has a nice presentation on this subject [“Mythbusters: Event Stream Processing v. Complex Event Processing”](<http://www.slideshare.net/TimBassCEP/mythbusters-event-stream-processing-v-complex-event-processing-presentation>). While most of the industry is actually ESP, for continuity I’ll continue to refer to it as CEP throughout this article.

So now back to the subject “CEP is the industry that never should have happened”. Over ten years ago ILog introduced the event management and alarms capability into their flagship rule engine product, and things where good, this really was cutting edge stuff for a mainstream product at that time. This allowed for temporal event correlation, as a natural extension to their existing rule language, with fully managed life cycles; so the user didn’t have to worry about retracting all their objects and the engine memory blowing up. This wasn’t a separate engine, it was an integral part of their existing engine. The same way that truth maintenance or other advanced features are part of the engine. ILog had some high profile customers and rapid growth in the telecoms market, which was the target market for this functionality. At the same time they also had a whole host of really interesting products as the result of ongoing artificial intelligence (AI) research.

At the Business Rules Forum 2008 (BRF08) I had the pleasure of spending some time with the ILog guys – it’s great when we can put the marketing and competition to one side, and just chat as engineers. We talked about all the really cool things that ILog R&D had produced, but have had to trim back, or put on hold, over the last 15 years, as business focuses changed. It was all fascinating stuff. So what happened? Two things. The AI winter happened where some of the hype cooled, as reality hit. It became obvious that while interesting some of these things only worked well in a very narrow scope, making it hard to build a growing business around. While event management did have a strong and broad benefit the AI winter was shortly followed by the telecoms downturn and spending on research and new IT projects was vastly reduced. As the telecoms downturn set in, Business Rules started to emerge and a change in company focus happened as they realized the financial potential. Rather than pushing for more AI features, the push was more for simplification aimed at something business analysts can use for business automation and decision management. Slowly the advanced AI features were put on pause, slimmed down or removed. Apparently many cool features are still retained in the capabilities of the engine today, but just not exposed to the end user. The event management was put into maintenance and while it’s still in the product today, it is no longer the cutting edge of technology that it once was.

Fast forward to 2009 and CEP is now everywhere, everyone understands it, wants and needs it. A whole new industry has grown out of this with companies such as TIBCO, StreamBase and EsperTech. Many of the CEP companies denounce rule engines, and the Rete algorithm especially, as out dated technologies and not suitable for CEP, promoting their own specialist algorithms. These systems tend to be based around an extended SQL, called “Streaming SQL” that detects event patterns in streams and executes actions. These tools do not tend to offer inferencing or provide capabilities for reasoning over sets of data, such as that found in a decision table. TIBCO, one of the main players on the field, unlike many of their rivals do implement their technology on an enhanced Rete algorithm and able to offer full rule engine capabilities, beyond just event processing.

At BRF08, to the ILog engineer’s, I hypothesised that had ILog stayed the course and continued to develop and promote their event management capabilities, the CEP industry as standalone from rule engines may have never occurred. Ilog could have have emerged the leader, being the early entrant and market creator. I had great fun pointing this out to the ILog engineer’s and joking that CEP is the industry that never should have happened. :)

Part 2 of this article will be a lot more technical showing how Drools, originally a Rete based rules engine, was easily, cleanly and orthogonally extended as a platform for (complex) event processing.