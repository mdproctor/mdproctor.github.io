---
layout: post
title: "JBoss Rules expressiveness goes to the next level"
date: 2007-05-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/jboss-rules-expressiveness-goes-to-the-next-level.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [JBoss Rules expressiveness goes to the next level](<https://blog.kie.org/2007/05/jboss-rules-expressiveness-goes-to-the-next-level.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 19, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Edson has been doing great work on the expressiveness of rules, it’s now possible to use && and || on field values and between fields themselves inside of a Pattern:
[code]
      
    Person( age > 30 && &lt 40 || hair =="black" ) 
[/code]

Note the || here is different than the ‘or’ conditional element, which works on patterns and results in subrule generation, where each logical outcome is generated as a rule.

As part of Milestone Release 2 we already have autovivification of the field names inside of predicates and return value statemets to reduce the number of field variable declarations, which causes clutter in rules.
[code]
      
    Cheese( oldPrice : oldPrice, newPrice == ( oldPrice * 1.10 ) )
[/code]

Can now be written as:
[code]
      
    Cheese( newPrice == ( oldPrice * 1.10 ) )
[/code]

Next we are reducing created declarations for variable bindings by allowing direct access to the properties on a pattern binding declaration, note this does not include nested properties or the direct properties of a field declaration, this should further help with the readabilty of rules:
[code]
      
    p : Person(personId : id)  
    i : Item(id == personId, value > 100 )
[/code]

Will soon be able to write as:
[code]
      
    p : Person()  
    i : Item(id == p.id, value > 100 )
[/code]

The final change we hope to do in time for 4.0, which is our most requested feature, is to allow nested properties, array and hashmap access to be expressed as field constraints rather than as predicates, return value or evals. I should mention at this stage that there are a number of complications and issues with regards to nested properties, arrays and hashmaps in rule engines that many users are not aware of; the issue is similar to hashmap keys where the hashcode or fields are changed making the key and its object irretrievable and thus causing memory leaks. Internally what will really happen is that we will rewrite these expressions as an eval and execute using [MVEL](<http://mvel.codehaus.org/>).
[code]
      
    Person($pets:pets)  
    eval($pets['rover'].type == "dog")
[/code]

Will soon be able to write as:
[code]
    Person( pets['rover'].type == "dog" )
[/code]

This puts JBoss Rules firmly on the road to being one of the most expressive rule engines :)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fjboss-rules-expressiveness-goes-to-the-next-level.html&linkname=JBoss%20Rules%20expressiveness%20goes%20to%20the%20next%20level> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fjboss-rules-expressiveness-goes-to-the-next-level.html&linkname=JBoss%20Rules%20expressiveness%20goes%20to%20the%20next%20level> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fjboss-rules-expressiveness-goes-to-the-next-level.html&linkname=JBoss%20Rules%20expressiveness%20goes%20to%20the%20next%20level> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fjboss-rules-expressiveness-goes-to-the-next-level.html&linkname=JBoss%20Rules%20expressiveness%20goes%20to%20the%20next%20level> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fjboss-rules-expressiveness-goes-to-the-next-level.html&linkname=JBoss%20Rules%20expressiveness%20goes%20to%20the%20next%20level> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fjboss-rules-expressiveness-goes-to-the-next-level.html&linkname=JBoss%20Rules%20expressiveness%20goes%20to%20the%20next%20level> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fjboss-rules-expressiveness-goes-to-the-next-level.html&linkname=JBoss%20Rules%20expressiveness%20goes%20to%20the%20next%20level> "Email")