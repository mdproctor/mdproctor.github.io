---
layout: post
title: "What is inference and how does it facilitate good rule design and maintenance"
date: 2009-11-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/11/what-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [What is inference and how does it facilitate good rule design and maintenance](<https://blog.kie.org/2009/11/what-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- November 9, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Inference has a bad names these days, as something not relevant to business use cases and just too complicated to be useful. It is true that contrived and complicated examples occur with inference, but that should not detract from the fact that simple and useful ones exist too. But more than this, correct use of inference can crate more agile and less error prone businesses with easier to maintain software.

So what is inference? Something is inferred when we gain knowledge of something from using previous knowledge. For example given a Person fact with an age field and a rule that provides age policy control, we can infer whether a Person is an adult or a child and act on this.
[code]
    rule "Infer Adult"  
    when  
      $p : Person( age >= 18 )  
    then  
      insert( new IsAdult( $p ) )  
    end  
    
[/code]

So in the above every Person who is 18 or over will have an instance of IsAdult inserted for them. This fact is special in that it is known as a relation. We can use this inferred relation in any rule:
[code]
        $p : Person()  
      IsAdult( person == $p )  
    
[/code]

In the future we hope to improve our language so you can have special handling of known relation facts, so you can just do following and the join is implicit:
[code]
      
      Person() IsAdult( )  
    
[/code]

So now we know what inference is, and have a basic example, how does this facilitate good rule design and maintenance?

Let’s take a government department that are responsible for issuing ID cards when children become adults, hence forth referred to as ID department. They might have a decision table that includes logic like this, which says when an adult living in london is 18 or over, issue the card:  
[![](/legacy/assets/images/2009/11/3f7f7b6e04cb-monolithic.png)](<http://1.bp.blogspot.com/_Jrhwx8X9P7g/Svi99ksQCaI/AAAAAAAAAX0/ldGiFCWXJSk/s1600-h/monolithic.png>)

However the ID department does not set the policy on who an adult is. That’s done at a central government level. If the central government where to change that age to 21 there is a change management process. Someone has to liaise with the ID department and make sure their systems are updated, in time for the law going live.

This change management process and communication between departments is not ideal for an agile environment and change become costly and error prone. Also the card department is managing more information than it needs to be aware of with its “monolothic” approach to rules management which is “leaking” information better placed else where. By this I mean that it doesn’t care what explicit “age >= 18” information determines whether someone is an adult, only that they are an adult.

Instead what if we were to split (de-couple) the authoring responsibility, so the central government maintains its rules and the ID department maintains its.

So its the central governments job to determine who is an adult and if they change the law they just update their central repository with the new rules, which others use:  
[![](/legacy/assets/images/2009/11/df4ad387836c-InferIsAdult.png)](<http://1.bp.blogspot.com/_Jrhwx8X9P7g/Svi99_5D-8I/AAAAAAAAAX8/47ySxmNG4Jc/s1600-h/InferIsAdult.png>)

The IsAdult fact, as discussed previously, is inferred from the policy rules. It encapsulates the seemingly arbitrary piece of logic “age >= 18” and provides semantic abstractions for it’s meaning. Now if anyone uses the above rules, they no longer need to be aware of explicit information that determines whether someone is an adult or not. They can just use the inferred fact:  
[![](/legacy/assets/images/2009/11/36d1d3619a6c-IssueIdCard.png)](<http://4.bp.blogspot.com/_Jrhwx8X9P7g/Svi9-FNxjbI/AAAAAAAAAYE/6PxlwbiE4kw/s1600-h/IssueIdCard.png>)

While the example is very minimal and trivial it illustrates some important points. We started with a monolithic and leaky approach to our knowledge engineering. We create a single decision table that had all possible information in it that leaks information from central government that the ID department did not care about and did not want to manage.

We first de-coupled the knowledge process so each department was responsible for only what it needed to know. We then encapsulated this leaky knowledge using an inferred fact IsAdult. The use of the term IsAdult also gave a semantic abstraction to the previously arbitrary logic “age >= 18”.

So a general rule or thumb when doing your knowledge engineering is:

Bad

  * Monolithic
  * Leaky

Good

  * De-couple knowledge responsibilities
  * Encapsulate knowledge
  * Provide semantic abstractions for those encapsulations

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Fwhat-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html&linkname=What%20is%20inference%20and%20how%20does%20it%20facilitate%20good%20rule%20design%20and%20maintenance> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Fwhat-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html&linkname=What%20is%20inference%20and%20how%20does%20it%20facilitate%20good%20rule%20design%20and%20maintenance> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Fwhat-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html&linkname=What%20is%20inference%20and%20how%20does%20it%20facilitate%20good%20rule%20design%20and%20maintenance> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Fwhat-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html&linkname=What%20is%20inference%20and%20how%20does%20it%20facilitate%20good%20rule%20design%20and%20maintenance> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Fwhat-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html&linkname=What%20is%20inference%20and%20how%20does%20it%20facilitate%20good%20rule%20design%20and%20maintenance> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Fwhat-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html&linkname=What%20is%20inference%20and%20how%20does%20it%20facilitate%20good%20rule%20design%20and%20maintenance> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Fwhat-is-inference-and-how-does-it-facilitate-good-rule-design-and-maintenance.html&linkname=What%20is%20inference%20and%20how%20does%20it%20facilitate%20good%20rule%20design%20and%20maintenance> "Email")