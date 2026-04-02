---
layout: post
title: "Washington Rules !"
date: 2006-11-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/11/washington-rules.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Washington Rules !](<https://blog.kie.org/2006/11/washington-rules.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- November 15, 2006  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

— Michael Neale  
Both Mark and myself recently returned from the highly informative [Business Rules Forum (in Washington DC).](<http://www.businessrulesforum.com/>)

The business rules industry seems to be in quite good shape, and there was a strong showing from all the vendors. I thought I would start with some summaries in general of what we saw, and what I thought.

The engine performance panel  
James Owen – an industry commentator and rule practitioner and evangelist of many years experience, kindly hosted a panel on performance challenges for rule engines (for the geeks). It was a real whos-who of rule engine core tech.

Take a look at the panel of braniacs below (James Owen is missing, he was talking).

From left to right (Dr. Ernest Friedman (Jess), Dr. Charles Forgey (Fair Isaac, inventor of RETE), Rev. Daniel Selman (ILog JRules product manager), Rabbi Mark Proctor (some bloke, JBoss Rules), Pedram Abrari (CTO Corticon)

[![](/legacy/assets/images/2006/11/7513ae7eb22d-100_3454.jpg)](<http://photos1.blogger.com/x/blogger2/3954/716/1600/527128/100_3454.jpg>)

Innovations I found interesting

There were strong offerings from all the vendors on rule management/editing/higher level tools, and an understanding that a lot of the core tech is being commoditised. Nevertheless, there were many different approaches. Here is an outline of the products/companies that tickled my fancy:  

  * Rule Burst
    * I love these guys as they are Australian ;) (same as me for those who don’t know). Their approach is rules capture and management inside Word documents, with a strong natural language engine. They used to be called “Softlaw” and specialise in turning complex legistlation into executable rules by marking up the actual legal documentation !
    * I also like them as they are solving hard problems for important customers which really shows the power of inference engines and rule management systems. They have been around for quite some time (> 15 years) and got their start with Prolog ! They tooling is also impressive, and they have a fairly unique way of allowing “backwards” chaining rules to ask questions and automatically generate questionnaires based on the rules.
  * Corticon
    * These guys are really approaching the problem from a different angle. They call it “rule modelling” and their Workbench/IDE/Environment is very impressive, and allows people to quickly model facts (vocabulary I think they call it), rules, and test/verify/analyse/find logic faults and gaps all in in the one desk top tool, and deploy it (for example) as a web service. Their CEO is also a MD (Medical Doctor) and he got his start as he saw the potential of rule based systems in medical diagnosis.
  * Pega Systems
    * Pega weren’t so much focusing on rules but also on process management, but even more so as whole new way of building apps “in place” – as in you take a web applications user interface, and switch in to design mode and you can modify the process/rules/fields that are “behind” the screen. Impressive, they have been really going hard with R&D, and it shows. Rules are just one part of their vision.
  * ILog
    * They didn’t participate in the “product derby” (kind of an Uber demo that gets shown while we are eating lunch) this year, but I did attend a session or two with Daniel Selman, the JRules Product Manager. I was particularly impressed with his presentation on “Mission Critical applications” and how it applies to rule engines. ILog JRules is clearly used everywhere in really sensitive applications, and Daniel did a great job outlining the real world challenges of maintaining complex applications and evolving them AND THE OBJECT MODEL over time (the JRules “Business Object Model” approach really shines for this, and now supports re factoring etc). ILog have impressive credentials in this space.
  * Haley
    * One of the benefits of this conference is that we get to speak with real world rule practitioners, and I heard great feedback about Haley’s implementation of NLP and NLU (Natural Language Processing and Natural Language Understanding) – which is an area that greatly interest me. On the one hand I view NLP as a little like voice recognition (annoying) or handwriting recognition (we all remember *that* version of the Apple newton) – ie hard to get right (and near enough is NOT good enough). But Haley seemed to have made this work for rules – so well done !

So it was an impressive showing from the Vendors. I am sure I missed some out, but this is all I had time to write notes on.

SOA and rules  
The “rule service” approach (stateless rule services exposed nominally via WSDL) seems to have become popular, and certainly seems applicable for a large class of rule problems (business decisioning, single point of truth etc.). 

Future challenges  
No one seemed to agree on a single way forward for modelling facts, some were talking MDA (MDA was a strong theme), some were purely WSDL/Web Service, and utilising OWL was even mentioned a few times (personally over the long term, I think OWL ontology’s may be The Way, but I am only new to them so I shouldn’t show my ignorance just yet). Modelling facts is a real challenge, and very few people were also thinking about how to cope with model evolution over time (as no one will get it right first go).

Rule standards are another major challenge, I am not expecting anything concrete for some months, perhaps a year. It was great to meet Said Tabet (of RuleML fame) and hear his opinions, and its also great to see vendors like ILog take RIF from W3C very seriously.  
  
Truth, Justice and the American way  
I found the US to be surprisingly familiar in every way, more so then Britain. The “tipping” culture took a while to get used to, I felt embarrassed as I had to ask people when to tip or not tip, how much etc. A feature of this seams to be to deliberately cause conflict. On the flip side, the service for everything was excellent. It was a hoot hanging around with James Owen, the ultimate Texan ! From my sampling of several Texan acquaintances over the years, I can say that I like Texans !  
  
Pretty Washington  
[![](/legacy/assets/images/2006/11/b51def859ed1-100_3441_283_29.jpg)](<http://photos1.blogger.com/x/blogger2/3954/716/1600/441306/100_3441%283%29.jpg>)The hotel was fantastic, and I was impressed by the array of Autumn colours (Autumn seems to be taking its time in the UK).  
  
Next  
Next week we will be in Berlin for JBoss World (I am arriving a little early to do the tourist thing, as a native to the Land Down Under, there is plenty over this side of the globe I have not yet seen – its all good !). If you are there, make sure you find Mark Proctor or myself, we have t shirts to give away !

[Post Comment](<https://beta.blogger.com/comment.g?blogID=5869426&postID=4656024316924088968>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fwashington-rules.html&linkname=Washington%20Rules%20%21> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fwashington-rules.html&linkname=Washington%20Rules%20%21> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fwashington-rules.html&linkname=Washington%20Rules%20%21> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fwashington-rules.html&linkname=Washington%20Rules%20%21> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fwashington-rules.html&linkname=Washington%20Rules%20%21> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fwashington-rules.html&linkname=Washington%20Rules%20%21> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fwashington-rules.html&linkname=Washington%20Rules%20%21> "Email")