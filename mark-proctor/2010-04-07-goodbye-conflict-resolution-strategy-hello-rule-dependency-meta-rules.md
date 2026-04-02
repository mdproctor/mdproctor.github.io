---
layout: post
title: "Goodbye Conflict Resolution Strategy, Hello Rule Dependency Meta Rules"
date: 2010-04-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/04/goodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Goodbye Conflict Resolution Strategy, Hello Rule Dependency Meta Rules](<https://blog.kie.org/2010/04/goodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- April 7, 2010  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’ve added a new section to the [Drools Language Enhancement](<http://community.jboss.org/wiki/DroolsLanguageEnhancements>) ideas wiki page discussing meta-rules to help declaratively control rule ordering. Here is what I have so far, feedback welcome, you can find the original content [here](<http://community.jboss.org/wiki/DroolsLanguageEnhancements#Field_Versioning>).

## Rule Dependency Meta-Rule Language

When a terminal node is matched instead of adding the Activation to the agenda it inserts it into the WorkingMemory. We have a special builder that allows easy access to the contents.

All declarations are typed fields for the Activation fact, based on the “name” field. So the name field is mandatory. All FactHandles are available via an array accessor, which has type inference for the element being used. We also all bindings on the Activation fact to work this way too. Act is used for compactness, we’ll allow that to be optionally user defined:  
act1 : Act( someDeclaration == X, fact[0] == Y )  
act2 : Act( someDeclaration.value > act1.someDeclaration.value )

Normal facts can also be matched. The RHS of the rule is side effect free, you cannot modify or insert facts; this allows the RHS to execute as soon as it’s matched. What you can do is setup rule dependencies – where one rule blocks another:  
act1.blockedBy( act2 ).until( Fired )  
act1.blockedBy( act2 ).until( IsFalse )

We can even allow facts to block:  
act1.blockedBy( someFact )

This means the act1 activation is blocked until a rule executes:  
act1.unblockedBy( someFact )

We can probably add an override, something like:  
act1.unblockAll()

Only when an Activation is no longer blocked will it be placed on the Agenda as normal.

If an activation on the agenda has not yet fired and something attempts to block it, it will be removed from the agenda until it is no longer blocked.

For this to be effective, especially for large systems, it will need to be combined with design time authoring help.

This work will be eventually be combined with further enhancements to help with parallel execution, in resulting conflicts, see the “Parellel Meta-Rule Language” heading.

<

p style=”min-height: 8pt; height: 8pt; padding: 0px;”>

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F04%2Fgoodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html&linkname=Goodbye%20Conflict%20Resolution%20Strategy%2C%20Hello%20Rule%20Dependency%20Meta%20Rules> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F04%2Fgoodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html&linkname=Goodbye%20Conflict%20Resolution%20Strategy%2C%20Hello%20Rule%20Dependency%20Meta%20Rules> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F04%2Fgoodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html&linkname=Goodbye%20Conflict%20Resolution%20Strategy%2C%20Hello%20Rule%20Dependency%20Meta%20Rules> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F04%2Fgoodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html&linkname=Goodbye%20Conflict%20Resolution%20Strategy%2C%20Hello%20Rule%20Dependency%20Meta%20Rules> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F04%2Fgoodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html&linkname=Goodbye%20Conflict%20Resolution%20Strategy%2C%20Hello%20Rule%20Dependency%20Meta%20Rules> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F04%2Fgoodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html&linkname=Goodbye%20Conflict%20Resolution%20Strategy%2C%20Hello%20Rule%20Dependency%20Meta%20Rules> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F04%2Fgoodbye-conflict-resolution-strategy-hello-rule-dependency-meta-rules.html&linkname=Goodbye%20Conflict%20Resolution%20Strategy%2C%20Hello%20Rule%20Dependency%20Meta%20Rules> "Email")