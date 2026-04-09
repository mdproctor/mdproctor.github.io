---
layout: post
title: "Drools a reflection on 5 years."
date: 2009-06-28
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/06/drools-a-reflection-on-5-years.html
---

5 years ago, when I first started to promote rule engines to the mainstream java developer market the questions I most often received where “What is a rule engine?” and “Why is this different/better to an ‘if’ statement”. In a room of 25 developers maybe only 3 or 4 would have heard of Jess, JRules or Prolog and only 1 or 2 would have any actual experience.

It was a long hard slog of repeating the same information over and over and over and over again to get the message out.

5 years later and the picture is very different. I’m no longer asked what a rule engine is or having to explain the benefits and everyone has heard of Drools. My personally feeling is that 2009 has become the tipping point for Drools, our “coming of age” year.

Could we have had the October Rules Festival 5 years ago and filled the room with over 100 people, the bulk of which where Java developers? Could I have had a [Boot Camp](<http://blog.athico.com/2009/03/drools-boot-camp-san-francisco-june.html>) backed with A-list names such as Wells Fargo, Boing, Fedex, Lockheed Martin, Sony, HP, Sun.

Reflecting on this made me feel immensely proud of what the Drools team (Michael Neale, Edson Tirelli, Krisv Verlaenen, Toni Rikkola and in the early years Bob McWhirter) and myself had achieved. We where actually responsible for making a whole mainstream market for Rule Engine technology. No other OSS engine has had any real market penetration and the commercial engines still do not target the mainstream Java developers – i.e. you don’t see JRules or Blaze Advisor at JavaOne or Devoxx(JavaPolis) or other similar events.

Drools was first established in 2001 by Bob McWhirter, there was no Drools 1.0 release. For those that remember the very early versions of Drools used Jelly (that xml scripting framework) and didn’t even compile on windows without cygwin as it required bash shell scripts – Bob’s handy work ;) A little later I got involved in Drools and together Bob, myself and others from the community finally managed to push out Drools 2.0, the first release, in June 2005, you can see the TSS announcement [here](<http://www.theserverside.com/news/thread.tss?thread_id=34277>) . Drools 2.0 was a simple xml scripting language, that was a partial rete “like” impl.

It was at this point that I become project lead, replacing Bob McWhirter who by then had become interested in other things, although he still remained involed in Drools, just to a lesser extent. When I first became involved in Drools I had zero background in rule engine technology, although I had an AI background in search space technology, specifically genetic algorithms.

Exactly 1 year later Drools 3.0 was released in June 2006, TSS announcement [here](<http://www.theserverside.com/news/thread.tss?thread_id=40802>). Drools 3.0 was a fully Rete implementation aimed at the Jess market.

Just over 1 year from that in July 2007 Drools 4.0 was released, TSS announcement [here](<http://www.theserverside.com/news/thread.tss?thread_id=46334>). Drools 4.0 moved up the food chain and was aimed at the JRules BRE market.

It took two full years to finally release Drools 5.0, TSS announcement [here](<http://www.theserverside.com/news/thread.tss?thread_id=54698>). Drools 5.0 has no target market and innovates beyond what traditional rule engines do to become what we refer to as a Business Logic integration Platform (BLiP). Drools 5.0 integrates and unifies rules, workflow and event processing. Drools 5.0 also includes Drools Solver, which is lead by community member Geoffrey De Smet. Probably the only comparable system now is Tibco Business Events, which is going in a similar direction.

For a bit of fun I thought I’d paste an old IRC entry from my early days (my handle is conan) with Drools, when Bob McWhirter was my mentor – Unfortunately my entries prior to 2004 are lost :( This paste provides a comical reference to where I’d told my employers that an unreleased piece of software was stable “as granite” and production ready in my efforts to sell Drools, only to find out otherwise. Should hopefully be encouraging for people to see me in my more “clue free” days, showing that if i can do it, anyone can :)

[2004-02-09 19:23:38] <conan> supposed to be getting the rules running at cisco this week, if drools is broken – I’m going to have a serious confidence problem with management.  
[2004-02-09 19:24:16] <topping> yes, caveats are good when pushing unreleased software to managment :-)  
[2004-02-09 19:25:03] <conan> topping: yeah I’ve been telling them its stable as granite!!!  
[2004-02-09 19:52:12] <conan> I’m thinking it might just be easier to stick in as an example for now in drools-examples  
[2004-02-09 19:52:21] <topping> i dunno, what problem are you having?  
[2004-02-09 19:53:29] <conan> I add two “request” objects which have states. on reset even which is fired when one request state = “Q” and any other request state != “N” can end up with request1 and requet2 being the same.  
[2004-02-09 19:53:35] <conan> which is fine  
[2004-02-09 19:53:53] <conan> I then retract the object, but its seems to recurse around still, even though there should be no data.  
2004-02-09 19:56:05] <bob> howdy  
[2004-02-09 19:56:16] <bob> if you’ve got a rule firing against a previously retracted object, then definitely a drools bug  
[2004-02-09 19:56:20] <bob> probably in the Agenda management  
[2004-02-09 19:56:39] <bob> Agenda isn’t dropping rule activations that involve retracted objects  
[2004-02-09 19:56:42] <bob> (just guessing)  
[2004-02-09 19:57:10] <conan> could this be beause the object is referenced by two parameters?  
[2004-02-09 19:57:13] <bob> nope  
[2004-02-09 19:57:22] <bob> an object either is or is-not in the working-memory  
[2004-02-09 19:57:31] <bob> if you take it out of the memory and it’s still in a rule activation, then bug  
[2004-02-09 19:57:44] <conan> bob: I’m going to knock up an example then and probe this.  
[2004-02-09 19:57:51] <bob> entirely possible I broke this in beta-12  
[2004-02-09 19:58:04] <bob> bad idea saying drools is “stable as granite” :)  
[2004-02-09 19:58:13] <conan> bob: yeah I know :)

Things would be remiss if I didn’t take this opportunity to thank many of the wonderful community contributors (in no particular order beyond old and new school) that helped make Drools what it is. Please if I missed off your name, then do let me know and I’ll add it.  
  
Old School:  
Alexander Saint Croix (nalex), Thomas Deisler, Doug Bryant (doug), Brain Topping (topping), Peter Royal (proyal), Simon Harris (sharris), Peter Lin (woolfel), David Cramer, Roger F. Gay, Barry Kaplan (memelet), Andy Barnett (dbarnett), Matt Ho (savaki), Martin Hold (mhald), Pete Kazmier (kaz), Alexander Bagerman (bagerman), Michael Frandsen.

New School:  
David Sinclair (stampy88), Ming Jin (ming), Ellen Zhao (ellen), Ben Truit, Wolfgang Laun (Laune) , Matthias Groch, Matt Geis, Joe White (joe), Michael Rhoden (mrhoden), Geoffrey De Smet (Ge0ffrey), Alexandre Porcelli (porcelli), Ahti Kitsik (Ahti), Tihomir Surdilovic, Salatino Mauricio (salaboy), Davide Sottara (sotty).