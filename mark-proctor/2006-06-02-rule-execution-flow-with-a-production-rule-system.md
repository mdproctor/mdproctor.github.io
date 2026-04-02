---
layout: post
title: "Rule Execution Flow with a Production Rule System"
date: 2006-06-02
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/06/rule-execution-flow-with-a-production-rule-system.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Rule Execution Flow with a Production Rule System](<https://blog.kie.org/2006/06/rule-execution-flow-with-a-production-rule-system.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 2, 2006  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Some times workflow is nothing but a decision tree, a series of questions with yes/no answers to determine a final answer. This can be modelled far better with a Production Rule System, and is already on the Drools road map.

For the other situations we can use a specialised implementation of Agenda Groups to model “stages” in rule engine execution. Agenda Groups are currently stacked, like Jess and Clips modules. But imagine instead if you could model linear Agenda Group execution – this is something I have been thinking about for a while to allow powerful and flexible modelling of processes in a Production Rule System. A successful implementation has clear advantages over two separate engines – as there is an impedance mismatch between the two. While there is little issue using a rule engine with workflow, using workflow to control linear execution of a rule engine will very suboptimal – this means we must seek a single optimal solution for performance sensitive applications.

Let’s start by calling these special Agenda Groups “nodes”, to indicate they are part of a linear graph execution process.

Start rules don’t need to be in a node and resulting target nodes will detach and evaluate once this rule has finished:
[code]
      
    rule "start rule"  
        target-node "<transition>" "<name>"       
      when  
        eval(true)  
      then  
         // assert some data  
    end       
    
[/code]

The start rule and the nodes can specify multiple target nodes and additional constraints for those target nodes; which is explained later. The start rule can fire on initialisation, using eval(true), or it could have some other constraints that fire the start rule at any time during the working memory life time. A Rule Base can have any number of start rules, allowing multiple workflows to be defined and executed.

The start rule dictates the next valid target-nodes – only activated rules in these nodes can fire as a result of the current assertions. While the activated rules in other nodes will not be able to fire, standard rules and Agenda Groups will react, activate and fire as normal to changes in data.

A node rule looks like a normal rule, except it declares the node it’s in. As mentioned previously a node can contain multiple rules; but only the rules with full matches to the LHS will be legible for firing:
[code]
      
    rule "rule name"  
        node "<name>"     
      when  
        <LHS>  
      then  
         // assert some data  
    end    
    
[/code]

There is an additional node structure, which the rules are associated with, and specifies the resulting targets:
[code]
      
    node "node name"  
        target-node "<transition>" "<name>"       
    end    
    
[/code]

Target nodes are only allowed to evaluate their activated rules once the previous start rule has finished or the previous node is empty because it has fired all its rules. Once a node is ready to be evaluated, we “detach” it and then spin it off into its own thread for rule firing, all resulting working memory actions will be “queued” and assert at safe points, so Rete is still a single process. Once a node is detached the contained rules can no longer be cancelled, they must all fire – further to this no further rules can be added. All our data structures are serialisable so suspension/persistence is simply a matter of calling a command to persist the detached node off to somewhere.

As well as a rule specifying the LHS constraints for it to activate, the previous node can specify additional constraints. A rule can be in multiple nodes, so if two incoming nodes specify additional constraints they are exclusive to each other – in that the additional constraints of the non current incoming node will have no effect:
[code]
      
    node "node name"  
        target-node "<transition>" "<name>" when  
            <additional constraints>  
        end  
    end    
    
[/code]

Further to this a node can specify multiple targets each with its own optinonal additional constraints. Sample formats are showing below:
[code]
      
    node "node name"  
        target-node "<transition>" "<name>"  
      
        target-node "<transition>" "<name>" when  
        end  
      
        target-nodes "<transition>" "<name>"   
                     "<transition>" "<name>"  
                     "<transition>" "<name>"  
       
        target-nodes "<transition>" "<name>"   
                     "<transition>" "<name>"  
                     "<transition>" "<name>" when  
        end  
    end    
    
[/code]

Further to this we need additional controls to implement “join nodes” and to also allow reasoning to work with both the transition name as well as the node name.

This highlights the basics for linearly controlled execution of rules within a Production Rule system. It also means we can model any BPM process, as it’s now a simplified subset, but allow it to be done in a highly scalable way that integrates into very demanding tasks. Further to this we can still have standard agenda groups and rules that fire as a result of data changes. This provides for a very powerful solution that is far more powerful than the simple subset that most workflow solutions provide.

[Post Comment](<https://beta.blogger.com/comment.g?blogID=5869426&postID=5144409847188936008>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F06%2Frule-execution-flow-with-a-production-rule-system.html&linkname=Rule%20Execution%20Flow%20with%20a%20Production%20Rule%20System> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F06%2Frule-execution-flow-with-a-production-rule-system.html&linkname=Rule%20Execution%20Flow%20with%20a%20Production%20Rule%20System> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F06%2Frule-execution-flow-with-a-production-rule-system.html&linkname=Rule%20Execution%20Flow%20with%20a%20Production%20Rule%20System> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F06%2Frule-execution-flow-with-a-production-rule-system.html&linkname=Rule%20Execution%20Flow%20with%20a%20Production%20Rule%20System> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F06%2Frule-execution-flow-with-a-production-rule-system.html&linkname=Rule%20Execution%20Flow%20with%20a%20Production%20Rule%20System> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F06%2Frule-execution-flow-with-a-production-rule-system.html&linkname=Rule%20Execution%20Flow%20with%20a%20Production%20Rule%20System> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F06%2Frule-execution-flow-with-a-production-rule-system.html&linkname=Rule%20Execution%20Flow%20with%20a%20Production%20Rule%20System> "Email")