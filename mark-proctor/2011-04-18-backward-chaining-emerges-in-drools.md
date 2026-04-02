---
layout: post
title: "Backward Chaining emerges in Drools"
date: 2011-04-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/04/backward-chaining-emerges-in-drools.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Backward Chaining emerges in Drools](<https://blog.kie.org/2011/04/backward-chaining-emerges-in-drools.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- April 18, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

We have a first cut of Prolog style derivation queries working. We have adopted the RuleML’s [POSL](<http://ruleml.org/submission/ruleml-shortation.html>) (Positional Slotted Language) approach to mixing positional terms and OO named arg arguments. This allows you to work fully in OO named arguments or fully in prolog positional terms or mix in between. The best of both worlds :) Note again this all works directly of java Pojos. We introduce an @Position annotation for fields, to allow positional mapping in rules.

Just to explain positional arguments are ones where you don’t need to specify the field name, as the position maps to a known named field. i.e. Person( name == “mark” ) can be rewritten as Person( “mark”; ). The ; is important so that we know when that everything before it is a positional argument. Otherwise we might assume it was a boolean expression, which is how it could be interpretted after the ;

If I had the following query:
[code]
    query niceFood( String thing, String location )  
         Location(thing, location)   // Location and Edible are ground facts  
         Edible(thing)  
    end
[/code]

I could invoke it in the following ways:
[code]
      
    //$food is positional output variable and "kitchen" an input literal  
    ?niceFood($food, "kitchen";)   
      
    // both are output variables  
    ?niceFood($food, $place;)   
      
    // Named arguments. Argument food is bound to output variable $food.   
    // Argument place is bound to input literal "kitchen"  
    ?niceFood($food : food, place : "kitchen" )   
      
    // Mixed, first argument is positional, second argument is named  
    ?niceFood($food; place : "kitchen" )
[/code]

The ? symbpol is necessary to tell Drools that is a pull based query. This will also (TBD) allow you to pull against ground fact patterns, instead of always being reactive to their changes. Drools is a reactive engine and data can be pushed (reactive) or pulled (queried). We don’t yet support it but eventually we will allow “open” derivation queries, where if you do not include the ?, it will continue to propagate new results as they appear in underlying query results.

A variable is considered an output variable if it has not been previous declared.

So let’s look at what Nani’ Search looks like in Drools. Nani Search is an example adventure program from [“Adventure’s in Prolog”](<http://www.amzi.com/AdventureInProlog/>). Here is a sample of queries and rules from the example. I’ve added a reactive rule to output what can be seen when Here is updated.
[code]
    query niceFood( String thing, String location )   
        Location(thing, location)  
        Edible(thing)  
    end  
      
    query connect( String x, String y )   
        Door(x, y;)  
        or   
        Door(y, x;)  
    end  
      
    query look(String place, List things, List food, List exits)   
        things : List() from accumulate( Location(thing, place;) ,                                      
                                      collectList( thing ) )  
        food : List() from accumulate( ?niceFood(thing, place;) ,                                      
                                    collectList( thing ) )            
        exits : List() from accumulate( ?connect(place, exit;) ,                                       
                                     collectList( exit ) )  
    end  
      
    rule reactiveLook when  
        Here( place : location)   
        ?look(place, things, food, exits;)  
    then         
        System.out.println( "  You are in the " + place );  
        System.out.println( "  You can see " + things );  
        System.out.println( "  You can eat" + food );  
        System.out.println( "  You can go to " + exits );  
    end  
    
[/code]

This gives the output:
[code]
    -----Output----  
       You are in the kitchen  
          You can see [crackers, broccoli, apple]  
          You can eat[crackers, apple]  
          You can go to [[kitchen, dining room], [kitchen, cellar]]
[/code]

Recursion is an important part of derivation queries and allows for search of trees:
[code]
    query isContainedIn( String x, String y )   
        Location(x, y;)  
        or   
        ( Location(z, y;) and ?isContainedIn(x, z;) )  
    end
[/code]

If you insert the following objects, you can determine that the key is located in the envelope, which is located on the desk and the desk is located in the office.
[code]
        insert( new Location("apple", "kitchen") );  
       insert( new Location("desk", "office") );  
       insert( new Location("flashlight", "desk") );  
       insert( new Location("envelope", "desk") );  
       insert( new Location("key", "envelope") );
[/code]

There is still lots more to do. The basics are now in place and usable and we’llpublish missing features in the mailing list soon. Note that this is not opportunistic backward chaining, which is still planned. You can think of opportunistic BC as lazy object creation or field initialisation.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fbackward-chaining-emerges-in-drools.html&linkname=Backward%20Chaining%20emerges%20in%20Drools> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fbackward-chaining-emerges-in-drools.html&linkname=Backward%20Chaining%20emerges%20in%20Drools> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fbackward-chaining-emerges-in-drools.html&linkname=Backward%20Chaining%20emerges%20in%20Drools> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fbackward-chaining-emerges-in-drools.html&linkname=Backward%20Chaining%20emerges%20in%20Drools> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fbackward-chaining-emerges-in-drools.html&linkname=Backward%20Chaining%20emerges%20in%20Drools> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fbackward-chaining-emerges-in-drools.html&linkname=Backward%20Chaining%20emerges%20in%20Drools> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fbackward-chaining-emerges-in-drools.html&linkname=Backward%20Chaining%20emerges%20in%20Drools> "Email")
  *[]: 2010-05-25T16:11:00+02:00