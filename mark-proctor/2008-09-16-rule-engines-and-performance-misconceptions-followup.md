---
layout: post
title: "Rule Engines and Performance Misconceptions - Followup"
date: 2008-09-16
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/09/rule-engines-and-performance-misconceptions-followup.html
---

My previous posting [“Rule Engines and Performance Misconceptions”](<http://blog.athico.com/2008/09/rule-engines-and-performance.html>) proved very popular with a lot of page hits and interesting comments, as the comments aren’t syndicated or shown on the main page I thought I’d repaste them as a blog entry for more exposure.

Adam Warski said…  
The same argument applies in many places. For example: C vs. Java – the same programs written in C (or directly in ASM ;)) can run faster than Java programs.

But the layer of abstraction Java provides makes it possible to write more maintainable code, in a reasonable amount of time etc.

So when somebody asks you again why he should choose Drools instead of a custom Java solution, ask him why he uses Java instead of C – after all, C is faster :)

Edson Tirelli said…  
That is the problem with micro benchmarks. They usually don’t take into account volumes that is also a very important non-functional requirement. Getting a fast hand coded algorithm for like 10 rules that will not change over time is feasible, but try to do the same for 100 rules, or rules that change frequently, and things will start to look very different.

Adam, BTW, :) your analogy is very informative.

old-skool rule hacker said…  
Mark is right that rules can make it easier to deal with evolving complexity. This is true where the declarative aspects of the rule base provide a clear and succinct formalism for capturing constraints in the application domain. Of course, how well they cope and will continue to cope over time depends upon the nature of the problem and the way in which it changes. You will always have to pick and choose your problem if you have already decided that rules are the solution and you may not always get that right. But the same is true for any programming language or toolkit.

What Mark did not mention was the F-word, “flexibility”. So, even where the complexity of an application does not grow over time, rules can still be of great use when changes to requirements or even just changes to the data model alter the constraints which govern the application’s behaviour. Rewriting a large body of code is rarely a problem-free task. When a rule formalism models the application domain well then rewriting is often a lot quicker and simpler than it would be for, say, rewriting a C or Java program.

It’s also often a lot easier for someone who is an application domain expert to check and verify the assumptions coded into a rule base than it is to verify the assumptions coded into a C or Java program. This is critical when an application’s remit is subject to change, especially if a quick response is required. In many cases rules can _directly_ encode aspects of an application. It is not always possible for an application domain expert to directly verify a rule base. But it’s often a lot easier for an expert’s understanding to be correctly and _verifiably_ translated into declarative rules than into algorithms. That’s what declarative programming is all about — providing a clear and minimal specification of what needs to be done in terms which directly display the application requirements.

Algorithmic solutions, by contrast, tend to cloak invariants which need to be maintained during execution for the program to correctly model the application’s requirements. Different choices of algorithms can impose arbitrary and often unnecessary sequential orderings on operations; yet, at the same time this fails to make clear the true order dependencies required by the application.

Algorithmic languages are also mostly tied to a Von-Neumann state model (aka a poke and peek data model). This opens up all sorts of possibilities for data model dependencies to be coded in to programs in obscure ways — and then accidentally get coded out when the code base is changed. It is easy for the effect of a change in one piece of code only to be felt at a distance in some other piece of code. Scoping models such as APIs and object oriented programming help deal with this problem but do not eliminate it.

Greg Barton said…  
There are some instances where efficient algorithms are easier to code up in rules. One example I give is dynamic programming. This is because rule based systems are particularly adept at both 1) complex recursion on subproblems, and 2) storage of subproblems in a generic yet accessible (i.e. change indexed) manner.

Anonymous said…  
Good praises for rule engines.  
But speaking of performance of rule engines, which use cases do you know where hand crafted java code is a better way than rule engines? Or, which main business use cases do you know where performance of rule engines is not “good enough”?  
(I have seen some “old” rule engines that were not good enough, but I can change my mind if I know the limits).

woolfel said…  
There’s no simple answer to the question of “when a rule engine is better”.

The reality is you have to try both and weigh the trade-offs. Obviously, that’s prohibitive from a cost perspective, so the best a developer can do is take an educated guess.

For me, if the rules are simple and capture a linear process, using Java is probably going to be a better choice.

On the other hand, if you have complex rules that modify facts, create new facts, derive partial results and produce a final result, using rule engine “could” be a better solution. Really, only way to tell is to do a proof of concept and put it in front of the business user.

Greg Barton said…  
Anonymous, I can give you a concrete example of a time when rules were ill advised for performance reasons. It’s along the lines of woolfel’s thoughts.

I worked on a project for a large American telco which shall remain nameless. They were moving into the long distance business and were using rules (ILOG JRules) to process the several hundred gigs of data they gathered each night. The thing is, by design, they did not want to process the data in a non-monotonic manner and also had few joins between working memory objects. In other words, data was processed (mainly validated) once, then never touched again by this particular system.

Using a rules based system was unnecessary in that case. The system, by initializing the rete network, was effectively preparing for nonmonotonic work, but it was never being done. CPU cycles were being burned in preparation for work that, by design, would never happen: the very definition of waste.

However, I’m pretty sure this was before JRules had a sequential mode, so it might have made the system perform better. But barring that, rules were not the best solution. They scuttled the project, firing upwards of 60 developers, and shelving two years of work. I hear they eventually switched to PL/SQL. The efficiency of the private sector at it’s best. :) It wasn’t the fault of the rules based approach, though. It was just bad management and a lack of technical due diligence.

nheron said…  
Hello,  
We use drools in many projects for company in the retail area . When the java class are well-defined (real business classes and not just database tables badly representing the business) and the rete algorithm well understood, there are no performance issues. The main problem is to understand what facts are and how to use them well. Most people when starting programming rules use the facts as a “if” and put most business code in the “then” place. But when using the facts to get the good rule to apply, performance is there.  
In one project with complex business rules for a purchase department that was previously using an excell file with macros, the new software using drools was 3 times quickler and really implemented all business rules.

woolfel said…  
Here is a concrete example where using a rule engine is “better” in my mind.

In the past, I worked on an order management system and had to support complex compliance rules. The rules had to check the “risk” of the portfolio and determine if a trade would violate any of the rules. The tricky part is this. The authors of the rules are portfolio managers and compliance officers. The other big requirement is deploying new rules without goind through a full development cycle. By that I mean write a bunch of code, compile, unit test, UAT, sign-off and then deploy.

I know many olders compliance systems commercial and home grown go with the code approach. The problem is those systems can’t handle real-time pre-trade compliance validation, nor could they add new rules on the fly. Large institutions like fidelity, putnam, wellington and state street normally schedule new releases on a quarterly basis. This means writing compliance rules with code isn’t feasible. I know many compliance system use an interpreted approach, but they can only handle post-trade compliance in overnight batch processes.

In the case of compliance, it’s difficult for a developer to implement those rules correctly because they’re largely arbitrary, and complex. Using a normal development process, it would take a month or more to implement those rules. Using an business rule engine like jrules, jess, clips and drools means the rule engine can handle the complexity and make life easier for the developers. That doesn’t mean a BRE can solve all the problems, but it can make it much easier, as well as provide real-time capability that would be difficult to implement in a custom rule engine. For the record, if a developer was an expert on rule engines and pattern matching, they could build a custom engine that out performs jrules, jess, clips or drools, but those individuals are few and hard to find.