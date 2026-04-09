---
layout: post
title: "The Decision Model IP Trap - Part Drei"
date: 2012-01-04
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/01/the-decision-model-ip-trap-part-drei.html
---

[part 1](<http://blog.athico.com/2011/11/decision-model-ip-trap.html>) [part 2](<http://blog.athico.com/2011/12/decision-model-ip-trap-part-deux.html>) [part 3](<http://blog.athico.com/2012/01/decision-model-ip-trap-part-drei.html>)

Recently Mr Suleiman Shehu wrote a [misleading rebuttal](<http://www.azintablog.com/2011/12/24/the-decision-model-ip-trap-rebuttal/>) on my blog posts [“The Decision Model IP Trap”](<http://blog.athico.com/2011/11/decision-model-ip-trap.html>) and [“The Decision Model IP Trap – Part Deux “](<http://blog.athico.com/2011/12/decision-model-ip-trap-part-deux.html>). He took great pains to declare that his article was balanced and impartial.

On a side note, interesting [post](<http://games.slashdot.org/comments.pl?sid=151312&cid=12701745>) by the famous John Carmack from ID Software on patents – “Yes, it is a legal tool that may help you against your competitors, but I’ll have no part of it. Its basically mugging someone.” [Carmack]

Mr Suleiman Shehu attempts to argue that patents and open source do mix, and mix regularly, in an effort to highlight my unreasonableness for not considering TDM within Drools. He cites patents owned by Oracle for Java and the recent Oracle and Google court case of those patents as the basis for those arguments. Further he tries to explain that the KPI usage policy is perfectly acceptable for any Open Source project.

Each and every fact he uses to form the basis of his argument is provably incorrect and shows he has no understanding of licensing within Open Source, or the different factions in Open Source, which admittedly is not a simple topic, but that is no excuse. You cannot bundle all of Open Source under a single umbrella argument, each license has different restrictions and guarantees. Having built his rebuttal on misguided, misunderstood and false assumption (points 1 to 4) he then slides to conjecture on my beliefs and motives for which he has no evidence (points 5 to 7). This completely nullifies any claims he has for impartiality, balance or integrity.

I have kept an original copy of his article [here](<http://www.athico.com/TDM/tdm-rebuttal.html>). For brevity purposes I have abridged his points, in a way I feel encapsulates his intent. In the original copy I created two columns, where the first column shows the section numbers that correspond with the points in the main document, which is in the second column. This is to show the source for the abridged version in this article.

It was not so long ago that Open Source Systems (OSS) came with a lot of uncertainty. Providing certainty was a large part that allowed mass OSS adoption of both developers and users. Patents create legal uncertainties.

Licenses like (but not limited to) the GPL and Apache License bring certainty, over the years they have built up strong brand recognition that creates instantly known commodities for social charters and usage restrictions of a project. These are catalysts allowing for OSS communities of developers and users to thrive. The licenses do what they say on the tin, you don’t need expensive lawyers to hunt down potential additional restrictions. As a leader of an OSS project I value the certainty these bring. I won’t stand quietly by, while others seek to dilute those certainties and to muddy the water of respected OSS brands that many have worked hard to establish.

Bearing this in mind, here are the main points:

1) There is no reasonable reason why Drools cannot embrace TDM – WRONG.

1.1) Legally this cannot happen. The Apache license forbids contributions which are covered by patents not made available under the terms guaranteed by the Apache license. The license is crystal clear on this. The same is true for the GPL.

1.2) This actually rebuts his entire article, and is probably the end of the discussion. But for completeness I will falsify each and every fact that Mr Suleiman Shehu uses.

2) Drools is written in Java. Java is patented, your world is already using patents, so what’s your problem – WRONG.

2.1) There are no patents for the Java language specification. The term Java is trademarked and you must pass certification to use it. Java can be used to refer to the platform, which is the language specification + libraries + virtual machine. Oracle has patents for its virtual machine, the JVM.

2.2) The Java language specification has no patents. It is possible to implement a VM that can execute Java which does not infringe upon Oracle’s patents; see Kaffe: <http://www.kaffe.org/>. The Java specification provides a safe buffer from possible infringement of patents, from the perspective of developers targeting the Java language.

2.3) This is why patenting of methodologies, specifications and business practices is actually far more dangerous that patents for implementations, where alternative implementation techniques can nearly always be found. If the Java language specification was patented, it would be impossible to do an implementation that does not infringe – in such a situation Java would not have taken off in OSS.

2.4) Illustrating this argument further, Drools DRL is derivative of Ilog’s IRL, while IBM may hold patents for the execution of IRL, that has no bearing on our derivative implementation for the IRL language. If however IRL was patented, that would be much more chilling. So it is important to understand the difference in patenting of a specification, which is absolute, and implementationswhich can be worked around.

3) Oracle granted OpenJDK exceptions for those patents, as long as you obey its specification. Why is that different to KPI granting OSS exceptions. If its good enough for them (OpenJDK), why isn’t it for you – WRONG.

3.1) When Sun placed its JVM implementation under the GPL license all its patents were also made available under terms of the GPL license. While the Apache license explicitly gives universal and perpetual usage of patented contributions, the GPL has similar implicit terminology. The patent licensing under certification is something completely different and is considered an additional guarantee.  
<http://en.swpat.org/wiki/Java_and_patents>

“OpenJDK is has been distributed by Oracle under GPLv2.[1] GPLv2 includes two implicit patent licences, so users of OpenJDK should be safe, and modified versions of OpenJDK should also be safe (even if they’re heavily modified).

“The protections in the GPL are unconditional. The software doesn’t have to comply with any specifications in order to benefit from these protections.”

3.2) KPI could better clarify its OSS exception. The use of the term “Open Source” creates ambiguity as each license brings different issues that need to be tackled. For this they need a better understanding of OSS licensing – GPL/MIT/BSD/ASL. As stated above for either Apache or GPL, you either provide universal and perpetual access to those patents or you don’t. A project cannot be under the terms of GPL if it contains additional restrictions. If there are restrictions on usage, then it’s not GPL. Also be aware that providing access to patents for GPL projects does not make them available to Apache licensed projects – see 4.

4) Java is patented, you are safe if you certify – see 3. Which is why Oracle is suing Google. So if those people can work with patents, why can’t you – WRONG.

4.1) As stated in point 3, OpenJDK is not “licensing” patents under restrictive terms based on certification. Those grants are universal and perpetual within the GPL eco-system. So using 4’s for the “if it’s good enough for them, why isn’t it for you” is broken. This is further falsified by point 2 where Drools targets a language specification that is not patent encumbered. Oracle is not suing Google for making something that executes Java like code, the Java language specification is not patented. It believes the Google VM infringes its patents. As stated in point 2 it is possible to implement Java while not infringing patents, Google certainly believes they don’t infringe on those patents. Even if Google is found to infringe on some Oracle patents, that does not distract from the fact that Java, the language spec, is not patented and all OpenJDK patents are available under the terms of the GPL.

4.2) Google’s issue is related to different OSS eco-systems, which is an entirely different subject and out of scope. In short Google’s VM is licensed under the Apache License while OpenJDK is under the GPL. Those perpetual and universal grants are restricted to those eco-systems they were placed under. GPL v ASL is a subject completely out of scope. So again, it has got nothing to do with one OSS project using patents under restrictive “certification” terms, see point 3. If Google had placed its VM under the GPL, Oracle would not be able to sue them.

——-

Having shown that each and every fact he uses to support the basis of his argument is completely wrong lets now turn to the darker sides of his blog, where he misappropriates someone’s comment and slides to conjecture on my beliefs and motives, for which he has no evidence. This completely nullifies any claims he has for impartiality, balance or integrity.

5) Jacob Feldman, from Open Rules, as an Open Source vendor has endorsed the TDM patent position. “If KPI TDM patent usage rights statement appears to be acceptable to Jacob at OpenRules – an open source decision management company www.openrules.com ) what is there to prevent you from using TDM within Drools?” – MISAPPROPRIATION

5.1) Before you misquote someone whose comment was intended to be amicable simply to avoid conflict, you should probably check with them first before you use them as a full blown endorsement. I have known Jacob personally for many years and have already spoken to him on the matter. And I think I’ve already answered well enough, time after time, why even legally this is prevented.

6) “The only people who have the moral right to own patents are open source software companies who will naturally use their patents defensively.” – CONJECTURE

6.1) That is complete conjecture with no basis of evidence. I have never and will never claim any arguments based on morality. Yes, I believe that patents hinder innovation in software. Yes, I believe that patents restrict the potential of Open Source, as it cannot license patents (as proven in points 1 to 4). This has nothing to do with morality. I am invested in Open Source, I have every right to protect my interests and my employers interests and attempt (within the law) to limit those that might negatively impact on said interests. In the same way any individual or company has every right to hold patents to protect their interest. Morality has nothing to do with it.  
  
7) “Mark believes that this TDM patent should be made available to the wider community on an Apache licence because I believe (but I cannot prove this belief) that Mark would have liked to integrate TDM with Drools in some way and therefore argues that an open source project should not be encumbered with any software patents.” – CONJECTURE

7.1) This is so bad in so many ways that I don’t even know where to begin. It borders on being libellous. You are trying to claim that I wish to appropriate someone else’s property because I wish to use their ideas.

7.2) I’ve repeatedly said, in almost every thread on this subject, that I consider the research projects Prologa and XTT2 to be far more extensive, and that I will be using those. That alone falsifies any conjecture you are trying to make. Shame on you.

7.3) I think I made it clear in point 6 that my motives are simply about protecting my interests. I’m invested in Open Source, I believe patents restrict the potential of Open Source and I have every right to execute in a way to negate those restrictions.

7.4) I have never said I believe that they “should be made available”. That’s a very strong statement, insinuating I believe in the appropriation of someone else’s property based on arguments of morality. Larry came to me and asked if we would use TDM within Drools, I cannot legally do so under the terms of the Apache license. If they wish for Drools to incorporate TDM, they need to license it under those terms – the choice is theirs and theirs alone. “Should” doesn’t come into it.

7.5) Patents create a ‘walled garden’, Drools cannot license those patents under restrictive terms. Thus wider adoption of TDM is not in my employer’s commercial interests, as we cannot provide implementations for those potential customers who want TDM. I have every right to protect my employer’s commercial interests by communicating this issue to potential TDM adopters, to ensure they do not become excluded from from Open Source.

Mark  
Disclaimer: This post is made in a personal capacity. Nothing written above should be construed as Red Hat’s corporate position.