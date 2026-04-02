---
layout: post
title: "Drools Inference and Truth Maintenance for good rule design and maintenance"
date: 2010-01-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/01/drools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Inference and Truth Maintenance for good rule design and maintenance](<https://blog.kie.org/2010/01/drools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 22, 2010  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Back in November I did a blog on inference and how it can be useful for rule authoring.  
[What is inference and how does it facilitate good rule design and maintenance](<http://blog.athico.com/2009/11/what-is-inference-and-how-does-it.html>)

The summary of this was:

  * De-couple knowledge responsibilities
  * Encapsulate knowledge
  * Provide semantic abstractions for those encapsulations

For my JUG in Lille I extended this example by including truth maintenance, to demonstrate self maintaining systems.

The previous example was issuing ID cards to over 18s, in this example we now issue bus passes, either a child or adult pass.
[code]
    rule "Issue Child Bus Pass" when  
      $p : Person( age then  
      insert(new ChildBusPass( $p ) );  
    end  
      
    rule "Issue Adult Bus Pass" when  
      $p : Person( age >= 16 )  
    then  
      insert(new AdultBusPass( $p ) );  
    end
[/code]

As before the above example is considered monolithic, leaky and providing poor separation of concerns.

As before we can provide a more robust application with a separation of concerns using inference. Notice this time we don’t just insert the inferred object, we use “logicalInsert”:
[code]
    rule "Infer Child" when  
      $p : Person( age then  
        logicalInsert( new IsChild( $p ) )  
    end  
    rule "Infer Adult" when  
      $p : Person( age >= 16 )  
    then  
        logicalInsert( new IsAdult( $p ) )  
    end
[/code]

A “logicalInsert” is part of the Drools Truth Maintenance System (TMS). Here the fact is logically inserted, this fact is dependant on the truth of the “when” clause. It means that when the rule becomes false the fact is automatically retracted. This works particularly well as the two rules are mutually exclusive. So in the above rules if the person is under 16 it inserts an IsChild fact, once the person is 16 or over the IsChild fact is automatically retracted and the IsAdult fact inserted.

We can now bring back in the code to issue the passes, these two can also be logically inserted, as the TMS supports chaining of logical insertions for a cascading set of retracts.
[code]
    rule "Issue Child Bus Pass" when  
      $p : Person( )  
           IsChild( person =$p )  
    then  
      logicalInsert(new ChildBusPass( $p ) );  
    end  
      
    rule "Issue Adult Bus Pass" when  
      $p : Person( age >= 16 )  
           IsAdult( person =$p )  
    then  
      logicalInsert(new AdultBusPass( $p ) );  
    end
[/code]

Now when the person changes from being 15 to 16, not only is the IsChild fact automatically retracted, so is the person’s ChildBusPass fact. For bonus points we can combine this with the ‘not’ conditional element to handle notifications, in this situation a request for the returning of the pass. So when the TMS automatically retracts the ChildBusPass object, this rule triggers and sends a request to the person:
[code]
    rule "Return ChildBusPass Request "when  
      $p : Person( )  
           not( ChildBusPass( person == $p ) )  
    then  
        requestChildBusPass( $p );  
    end
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F01%2Fdrools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html&linkname=Drools%20Inference%20and%20Truth%20Maintenance%20for%20good%20rule%20design%20and%20maintenance> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F01%2Fdrools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html&linkname=Drools%20Inference%20and%20Truth%20Maintenance%20for%20good%20rule%20design%20and%20maintenance> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F01%2Fdrools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html&linkname=Drools%20Inference%20and%20Truth%20Maintenance%20for%20good%20rule%20design%20and%20maintenance> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F01%2Fdrools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html&linkname=Drools%20Inference%20and%20Truth%20Maintenance%20for%20good%20rule%20design%20and%20maintenance> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F01%2Fdrools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html&linkname=Drools%20Inference%20and%20Truth%20Maintenance%20for%20good%20rule%20design%20and%20maintenance> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F01%2Fdrools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html&linkname=Drools%20Inference%20and%20Truth%20Maintenance%20for%20good%20rule%20design%20and%20maintenance> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F01%2Fdrools-inference-and-truth-maintenance-for-good-rule-design-and-maintenance.html&linkname=Drools%20Inference%20and%20Truth%20Maintenance%20for%20good%20rule%20design%20and%20maintenance> "Email")