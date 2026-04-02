---
layout: post
title: "Drools Backward Chaining Unification Syntax Discussion - Rebellion in the ranks"
date: 2011-04-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/04/drools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Backward Chaining Unification Syntax Discussion – Rebellion in the ranks](<https://blog.kie.org/2011/04/drools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- April 22, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

We are having some lively [debate ](<http://drools.46999.n3.nabble.com/Backwards-chaining-the-difference-between-input-and-output-variables-td2842155.html>)on the unification syntax for Drools backward chaining. I want to make sure we get the widest possible input on this, so blogging it some more.

At the simplest level people have seen this:
[code]
    Location(t : thing, l : location)  
    Edible(t : thing)
[/code]

And said why do this, if the behaviour is the same as ‘==’ (see below), why introduce something new.
[code]
    Location(t : thing, l : location)  
    Edible(thing == t)
[/code]

Lets move from ground facts to a query, defined as:
[code]
    query niceFood( String t, String l )  
    Location(t : thing, l : location)  
    Edible(t : thing)  
    end
[/code]

Query parameter behaviour on whether the parameter is an in our an out variable is defined by the caller, not the defintition itself. That means we have no idea of the behaviour for t or l at compile time, i.e. in or out, bound or unbound. So using ‘==’ (see below) for those patterns wouldn’t make sense if the caller left t or l unbound, especially so if that query called another query passing that unbound variable down. You would in essence be using ‘==’ to pass down an unbound value to a nested query.
[code]
    query niceFood( String t, String l )  
    Location( thing == t, location == l)  
    Edible( thing == t )  
    end
[/code]

For this reason when dealing with queries we need to think in terms of unification across variables, which is bi-directional, and not filters on a field value. Remember as well that the unification process can span to nested patterns and queries.
[code]
    query niceFood( String t, String l )  
    Location( t : thing, l : location)  
    Edible( t : thing )  
    end
[/code]

Here is a recursive query, where a query calls itself. Again at compile time we have no way of knowing whether x or y is an in or an out var, that all depends on how the query is called at runtime. So we use the unification binding symbol, instead of the ‘==’ symbol.
[code]
    query isContainedIn( String x, String y )  
    Location( x : thing, y : location)  
    or  
    ( Location(z : thing, location y) and ?isContainedIn( x : x, z : y) )  
    end
[/code]

The unification symbol in essence means the value, once bound, will be the same across all locations.

If it’s still not clear what unification is, please read Adventures in Prolog.[ http://www.amzi.com/AdventureInProlog/a1start.php](<http://www.amzi.com/AdventureInProlog/a1start.php>) especially <http://www.amzi.com/AdventureInProlog/a5rules.php>. There is a wealth of explanations on how a prolog engine works for unification on the web. You could also try the [Mandarax manual](<https://docs.google.com/document/d/1ZbRxh_QMgb1-3uWGqW5woCE798c7t6vPcUMFevLXcZM/edit?hl=en#heading=h.i2m6diq77oxe>) that also executes derivation queries with Java objects.

The main complaint with this is that it introduces potential spelling mistakes. If I unify in 3 places for a rule and one of those misses a letter, the rule will not execute correctly. Prolog provides warnings when a unification only appears once, which catches the most trivial cases, but not all. The reverse is also true that someone might use a variable name for a binding not realising it was already a binding, again with the rule not executing as expected.

From the one or two emails I’ve had it’s been suggested the sky will fall in and we’ll all be going to hell in a hand basket.

So I’d please invite you all to discuss alternatives. Don’t just email me telling me that if I do this the world is gonna end and I’ve destroyed Drools and everyone’s reputation, that doesn’t help and it makes the debate emotional and awkward. Work with me through alternative suggestions based on levels of merit, discussing the pros and cons. Make sure you actually understand what unification is, so that you extrapalate through any suggestions. Another aspect to consider when proposing any alternatives is that we need to keep things regular across the positional syntax too.

  * Regular.
  * Introduces no new syntax, and thus no new symbols.
  * Natural and logical extended behaviour to our existing binding syntax and behaviour.
  * Backwards compatible.
  * People can ignore it if they wish, they never need know it exists.
    * Caveat it does introduce the spelling mistake issue to them.

I’d be very interested to see if there have ever been any proposals in the prolog world to address this.

As a way to get people’s mind thinking, lets work through one possible suggestion:

As alternatives we could leave ‘:’ for it’s traditional role as a single binding and instead introduce a new symbol purely for unification. POSL uses ‘->’ for slot fillers so lets use that. http://ruleml.org/submission/ruleml-shortation.html
[code]
    query niceFood( String t, String l )  
    Location( thing -> t, location -> l)  
    Edible( thing -> t)  
    end
[/code]

This however doesn’t solve the problem, you can still get spelling mistakes, the only difference is the problem has shifted to only those using unification and not those using normal ‘:’ bindings and constraints. In essence we’ve introduced a new symbol, not to remove the problem, but shift onto other people. This does nothing for positional though, where the problem will remain.

We could introduce a “var” prefix, that says if the identifier is not defined in the query parameters it must have a “var” prefix before it the first time it is unified against. That would ensure that no spelling mistakes occur. I’ll introduce a new query for this, where “location” is determine by the Here fact. Now location is no longer query argument, but determined by unifying against Here. As ‘l’ was not declared in th query parameters we had to prefix it with ‘var’, so that later uses can unify against it.
[code]
    query niceFood( String t, String l )  
    Location( thing -> t, location -> l)  
    Edible( thing -> t)  
    end  
      
    query getCurrentFood(String food)  
    Here(var location -> l)  
    ?niceFood( t -> food, location -> l)  
    end
[/code]

This solution seems to solve the problem, but we have introduced a new symbol and a new prefix. Also does this work for positionl? lets try:
[code]
    query niceFood( String t, String l )  
    Location( t, l)  
    Edible( t)  
    end  
      
    query getCurrentFood(String food)  
    Here( var l; )  
    ?niceFood( food, l; )  
    end
[/code]

I believe it does, although we’ll need to check that the parser can handle “var l” for positional without creating ambiguity. There is the issue though that it is possible to unify on patterns themselves:
[code]
    var p <- Person()  
    p <- Person()  
    
[/code]

So the <\- would need to work in place of : on the pattern bindings, and ‘var’ would also be needed. I reversed it to show that Person is unifying into p. Another aspect to consider is that a unification variable, once bound can be treated like a normal field constraint, which may cause confusion as effectively you have two ways of defining variables. This means people can use -> as a complete replacement, depending on their personal preferences – that may not be a good idea….

  * Regular.
  * Introduces new syntax and new symbols.
  * Existing ‘:’ is preserved, at the expense of introducing new concepts to learn.
  * Backwards compatible
  * People can ignore it if they wish, they never need know it exists.
  * People may end up using -> as a replacement for : for simple cases, confusing people.

What do people think about this as an alternative? Another suggestion has been to add “out” as a prefix on a query parameter, to enforce that a parameter can only be used for passing stuff out, and not bi-directional. Please keep the alternative suggestions coming, but remember there are no points for being dramatic.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fdrools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html&linkname=Drools%20Backward%20Chaining%20Unification%20Syntax%20Discussion%20%E2%80%93%20Rebellion%20in%20the%20ranks> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fdrools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html&linkname=Drools%20Backward%20Chaining%20Unification%20Syntax%20Discussion%20%E2%80%93%20Rebellion%20in%20the%20ranks> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fdrools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html&linkname=Drools%20Backward%20Chaining%20Unification%20Syntax%20Discussion%20%E2%80%93%20Rebellion%20in%20the%20ranks> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fdrools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html&linkname=Drools%20Backward%20Chaining%20Unification%20Syntax%20Discussion%20%E2%80%93%20Rebellion%20in%20the%20ranks> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fdrools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html&linkname=Drools%20Backward%20Chaining%20Unification%20Syntax%20Discussion%20%E2%80%93%20Rebellion%20in%20the%20ranks> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fdrools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html&linkname=Drools%20Backward%20Chaining%20Unification%20Syntax%20Discussion%20%E2%80%93%20Rebellion%20in%20the%20ranks> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F04%2Fdrools-backward-chaining-unification-syntax-discussion-rebellion-in-the-ranks.html&linkname=Drools%20Backward%20Chaining%20Unification%20Syntax%20Discussion%20%E2%80%93%20Rebellion%20in%20the%20ranks> "Email")
  *[]: 2010-05-25T16:11:00+02:00