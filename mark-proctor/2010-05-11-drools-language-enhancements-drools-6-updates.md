---
layout: post
title: "Drools Language Enhancements (Drools 6) updates"
date: 2010-05-11
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/05/drools-language-enhancements-drools-6-updates.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Language Enhancements (Drools 6) updates](<https://blog.kie.org/2010/05/drools-language-enhancements-drools-6-updates.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 11, 2010  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Davide has been working on the new parser for Drools 6, he’s updated the language guide with some more ideas. Don’t worry, core developers are still focusing on 5.1. The full language guide, aimed to provide the Drools 6.0 drl syntax can be found here:  
<http://community.jboss.org/wiki/DroolsLanguageEnhancements>

The parts Davide has updated are:  
Pipes – Pass through Filters  
Unit support  
Rising / Falling edges

Pipes – Pass through Filters

While accumulate performs map and fold operations it returns a derived result. Pipes allow us to filter a set of Tuple chains, that represent the actual join partial match results. In 5.0.x we had “over” as a temporal pass through filter, Person() over win:time(30s). We feel this concept should be more generalised to allow any pluggable filters, and for those filters to work on single Patterns of a group of patterns:
[code]
    Person() | win:time(30s)
[/code]

These pipes can be combined, so we only allow the Persons for the last 10 minuts to propagate forward (retracting anyone who existed more than 10 mins ago) but we throttle the network updates to every 30s:
[code]
    Person() | win:time(10m) | throttle(30s)
[/code]

This is important for combination with say accumulates, where we don’t want every single change to be aggregated and the result propagated:
[code]
    acc( Bus( $t: takings) | win:time(1h) | throttle(5m),  
         $avgTakings : avg( $t ) )
[/code]

So th above calculates the average takings for the last hour, continously, but it only updates the results every 5 minutes. Throttle is just currently a proposed filter name, we might come up with something different for that behaviour later.

Pipes don’t just work on single Patterns, they can work on multiple patterns. So for instance we could provide a “unique” filter that remove ambiguous cross product joins; which Charles Forgy mentioned at ORF09. In the following example if we instead insert 3 As we would get 1 resulting match, not 9.
[code]
    (A() A() A()) | unique
[/code]

Unit support

Groovy added unit support, based around leveraging JScience and JSR275. http://groovy.dzone.com/news/domain-specific-language-unit-. The dot notation is a bit too ambigous for Drools, but we already use # to cast patterns, so we can do the same for units.
[code]
    3#km + 5#m
[/code]

We can cast existing units to other units. So we can declare something as 3km, but have it returned as feet.
[code]
    3#km#feet
[/code]

If a unit is combined with a normal literal, then it’s just a operator on that literal value, for instance the following is 6k, it is not executed in the same way as 3km * 2km would do.
[code]
    3#km * 2
[/code]

# can be used with methods and functions. If the method returns a literal, then it’s the same as saying 3km. If the method returns a unit, then it’s like a caste:
[code]
    returnInt()#km  
    returnKm()#feet
[/code]

This works for strings too, and can be used to provide date/time formatting:
[code]
    "2012 12 04"#myDateFormat
[/code]

Rising / Falling edges

Grindworks supports the idea of executing actions on the rising or falling edges of a rule. While we could do this on the actions too, we think initially this would be better on the LHS, as a special conditinal element.
[code]
    when  
       rising Person( age == 30 )  
      
    when  
       falling Person( age == 30 )
[/code]

Clealry rising is the default behaviour for a pattern. Whether we allow it’s inclusion, for readability intent, or only support falling, is to be decided.

We could combine this with a branch
[code]
    when  
       ...  
       branch( rising Person(....),  
               [b1] falling Person(....)
[/code]

This also has some ramifications for Logical Closures, as it solves some of the same problems.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F05%2Fdrools-language-enhancements-drools-6-updates.html&linkname=Drools%20Language%20Enhancements%20%28Drools%206%29%20updates> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F05%2Fdrools-language-enhancements-drools-6-updates.html&linkname=Drools%20Language%20Enhancements%20%28Drools%206%29%20updates> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F05%2Fdrools-language-enhancements-drools-6-updates.html&linkname=Drools%20Language%20Enhancements%20%28Drools%206%29%20updates> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F05%2Fdrools-language-enhancements-drools-6-updates.html&linkname=Drools%20Language%20Enhancements%20%28Drools%206%29%20updates> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F05%2Fdrools-language-enhancements-drools-6-updates.html&linkname=Drools%20Language%20Enhancements%20%28Drools%206%29%20updates> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F05%2Fdrools-language-enhancements-drools-6-updates.html&linkname=Drools%20Language%20Enhancements%20%28Drools%206%29%20updates> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F05%2Fdrools-language-enhancements-drools-6-updates.html&linkname=Drools%20Language%20Enhancements%20%28Drools%206%29%20updates> "Email")