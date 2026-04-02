---
layout: post
title: "Pluggable Belief Systems in Drools 6.0"
date: 2013-09-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2013/09/pluggable-belief-systems-in-drools-6-0.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Pluggable Belief Systems in Drools 6.0](<https://blog.kie.org/2013/09/pluggable-belief-systems-in-drools-6-0.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 22, 2013  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Drools has supported simple truth maintenance for a long time, and followed a similar approach as that in Jess and Clips.

In 6.0 we abstracted the TMS system to allow for pluggable belief systems. This allows a sub system to control what the main working memory can see; i.e. what is inserted for the user to write rules to join against.

There are two interfaces for this the BeliefSystem and the BeliefSet. The BeliefSystem is global to the engine and provides the handling for logical inserts or deletes. It also has a constructor method to provide the LogicalDependency instance; this allows BeliefSystem to have it’s own implementation.  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/beliefsystem/BeliefSystem.java>

The BeliefSet is the set of “equals” beliefs; i.e. logical insertions. If you remember in 5.x a TMS system a belief is a one or more logical insertions; but only one will ever be visible in the system. Logical means they have a supported rule, which is tracked by a counter. Only when there are no supporters and that counter is zero, is the belief deleted. We’ve extended this so a logical insertion have an additional value associated with it; which becomes useful in our JTMS implementation, that I’ll cover in a moment. Further the BeliefSystem provides control over what is or is not propagated into the main engine – it could be one of the logical inserted items from the set, or even a derived value determined from the set.

We have a “simple” implementation, that emulates what we had in 5.x, and is still the default.  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/beliefsystem/simple/SimpleBeliefSystem.java>  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/beliefsystem/simple/SimpleBeliefSet.java>

We’ve added am experimental JTMS implementation, which allows a logical insertion to have a positive or a negative label. This allows for contradiction handling. A logical insertion will only exist in the main working memory, as long as there is no conflict in the labelling – i.e. it must be one or more positive labels, and no minus label.  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/beliefsystem/jtms/JTMSBeliefSystem.java>  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/beliefsystem/jtms/JTMSBeliefSetImpl.java>

I’ve covered the bus pass system before, [here](<http://blog.athico.com/2009/11/what-is-inference-and-how-does-it.html>). The code is still the same, the only difference now with the JTMS plugin is that each logical insertion defaults to a positive label.

rule “IsChild” when  
p : Person( age < 16 )  
then  
logicalInsert( new IsChild( p ) )  
end  
  
  
rule “IsAdult” when  
p : Person( age >= 16 )  
then  
logicalInsert( new IsAdult( p ) )  
end

rule “Issue Child Bus Pass” when  
p : Person( )  
IsChild( person == p )  
then  
logicalInsert(new ChildBusPass( p ) );  
end  
  
rule “Issue Adult Bus Pass” when  
p : Person() IsAdult( person == p )  
then  
logicalInsert(new AdultBusPass( p ) );  
end

In the case of someone who is a child, it results in a tree that looks like below.

[![](/legacy/assets/images/2013/09/c3a1a6ae3e11-jtms_plus.png)](<http://3.bp.blogspot.com/-IANlHtsK-_o/Uj8LWpbggbI/AAAAAAAAA8w/SkUFm1VJ4vE/s1600/jtms_plus.png>)

These are called your “default” rules. Now what happens if you want to add an exception, that contradicts the default rule. JTMS allows a negative insertion for a fact, doing this causes a conflict an the fact will be held in limbo, and not available in the working memory, until the conflict is resolved. For instance we might want an exception rule, that does not allow a bus pass to be issued to someone who is banned.

rule “Do not issue to banned people” when  
p : Person( )  
Banned( person == p )  
then  
logicalInsert( new ChildBusPass( p ) , “neg” );  
end

If the person is banned, it results in a tree with one positive and one negative label. The belief system is incremental and cascading, so at any time the exception rule can become true which would result in a cascading undo operation.

[![](/legacy/assets/images/2013/09/6112bdf4047b-jtms_pos_neg.png)](<http://4.bp.blogspot.com/-ao5g8cR0qdE/Uj8MveblqwI/AAAAAAAAA88/uqONDIssCfA/s1600/jtms_pos_neg.png>)

We’ve also added another experimental implementation for [Defeasible logic](<http://www.defeasible.net/>). Interestingly it turned out that Defeasible logic can be derived from the JTMS implementation, using the same BeliefSystem implementation but a custom BeliefSet implementation. The DefeasibleSet can be found here, clearly it is a lot more complicated than the JTMS one. We use mask operations to try and keep it optimal. We haven’t added tracking for recursion yet, that is a TODO, and ideally done at compile time.  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/beliefsystem/defeasible/DefeasibleBeliefSet.java>

Defeasible augments the JTMS with annotations to provide declarative resolving of conflicts.

  * @Strict // rule cannot be defeated
  * @Defeasible // rule can be defeated
  * @Defeater // rule can defeat other rules, but it’s result is not propagated into the working memory
  * @Defeats // takes list of rules it defeats

rule “Do not issue to banned people” @Defeasible when  
p : Person( ) Banned( person == p )  
then  
logicalInsert(new ChildBusPass( p ) , “neg” );  
end  
  
rule “Exception for children with minor offences” @Defeats(“Do not issue to banned people”) when  
p : Person( )  
IsChild( person == p )  
Banned( person == p, offence == “minor” )  
then  
logicalInsert(new ChildBusPass( p ) );  
end

In defeasible logic the exception rule here is called a counter argument, and it is possible for another rule to rebut the counter-arguents, creating an argumentation chain, that rebuttal can also be rebutted. A good presentation on this can be found [here](<http://cs.uns.edu.ar/~grs/Publications/DeLP-ICLP-Color.pdf>).

We are currently working on other Belief System implementations. One is based on the [Belief Logic Programming](<http://130.203.133.150/viewdoc/summary;jsessionid=162A8F40668AEADD8607F9766BDA8296?doi=10.1.1.212.4006>) idea, which uses the concepts of belief combination functions as inspired by Dempster-Shafer. This will allow each logical insertion to have a degree of belief, and the BeliefSystem will be able to process those chains of logical insertions, applying the combination functions.

The other idea we are working on is Bayesian network integration. The BeliefSystem can back onto a Bayesian network, which can control which facts are inserted, or not inserted, into the engine. As the data changes over time, the sub system can add or remove what the main engine sees.

If you find this interesting, and what to have a go at implementing your own and need some help, then don’t hesitate to drop onto irc and ask:  
<http://www.jboss.org/drools/irc>

While the system is pluggable, the registration process is currently hard coded into an Enum, which you’ll need to update with your implementation:  
<https://github.com/droolsjbpm/drools/blob/master/drools-core/src/main/java/org/drools/core/BeliefSystemType.java>

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F09%2Fpluggable-belief-systems-in-drools-6-0.html&linkname=Pluggable%20Belief%20Systems%20in%20Drools%206.0> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F09%2Fpluggable-belief-systems-in-drools-6-0.html&linkname=Pluggable%20Belief%20Systems%20in%20Drools%206.0> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F09%2Fpluggable-belief-systems-in-drools-6-0.html&linkname=Pluggable%20Belief%20Systems%20in%20Drools%206.0> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F09%2Fpluggable-belief-systems-in-drools-6-0.html&linkname=Pluggable%20Belief%20Systems%20in%20Drools%206.0> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F09%2Fpluggable-belief-systems-in-drools-6-0.html&linkname=Pluggable%20Belief%20Systems%20in%20Drools%206.0> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F09%2Fpluggable-belief-systems-in-drools-6-0.html&linkname=Pluggable%20Belief%20Systems%20in%20Drools%206.0> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F09%2Fpluggable-belief-systems-in-drools-6-0.html&linkname=Pluggable%20Belief%20Systems%20in%20Drools%206.0> "Email")
  *[]: 2010-05-25T16:11:00+02:00