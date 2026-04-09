---
layout: post
title: "Chained 'from', 'accumulate' and 'collect'"
date: 2007-06-29
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/chained-from-accumulate-and-collect.html
---

### Chained ‘from’, ‘accumulate’ and ‘collect’

In Drools 4.0 we introduced the ‘from’ keyword, this allows you to declare a source for a pattern to reason over. This allows the engine to reason over data not in the Working Memory. This could be a sub-field on a bound variable or the results of a method call; the later provides us with hibernate integration where named queries can be called and Drools will unify the pattern against the returned results. Please excuse the lack of indentation, I can’t figure out how to get Blogspot to preserve the white spacing and didn’t have to time put all the in by hand :(

Here is a simple example of reasoning and binding on sub-field:

```drl
Person( personAddress : address )
address : Address( zc : zipcode == "23920W") from personAddress
```

With all the flexibility from the new expressiveness in the Drools engine you can slice and dice this problem many ways. This is the same but shows how you can use a graph notation with the ‘from’:

```drl
p : Person( )
address : Address( zc : zipcode == "23920W") from p.address
```

Of course we can also do this our new flexible expressive language extensions:

```drl
Person( zc : address.zipCode == "2392OW")
```

The next example shows how we can reason over the results of a hibernate query, the Restaurant pattern will reason over and bind with each result in turn.

```drl
p : Person( )
  Restaurant( food == p.favouriteFood )
                from hs.getNamedQuery( "list restaurants by postcode" )
                     .setProperties( [ "postcode" : p.address.zipcode ] )
                     .list()
```

‘collect’ and ‘accumulate’ both result in a returned object, as such a pattern can specify either of those as its ‘from’ source. ‘collect’ allows cardinality reasoning (when there are more than 7 red buses) and returns a List object. ‘accumulate’ allows you to execute actions on each item of data in a set of data, matching a given pattern and execute a result action to return an object of the users choice – typically used to sum or total data, but of course can do a lot more complex work.

This example chains two ‘from’s together. It finds customers who have bought items all of which are priced over 10, where the items are a field and not asserted into the working memory:

```drl
c : Customer()
items : List( size == c.items.size ) 
      from collect( Item( price > 10 ) from c.items )
```

If the items where not a field, but instead asserted into the working memory, we could use a correlated ‘collect’ pattern:

```drl
p : Person()
list : List()
      from collect( Item( owner : p ) )
items : List(size == list.size)
      from collect( Item( price > 10 ) from list )
```

Here is how to achieve the same using ‘accumulate’ and its built in function ‘count’; although this doesn’t illustrate chained ‘from’, I added it for completeness:

```drl
p : Person()
count : Number()
      from accumulate( i : Item( owner == p ), count( i ) )
list : List( size == count )
      from collect( Item( owner == p, price > 10 ) )
```

For a more complex, and thus contrite but illustrative, example of chained ‘from’ we can look at the following example. For each store where the Person has an account we retrieve all the Items for that store and check if those items have an average price over 50

```drl
p : Person()
s : Store( accountOwner == p )
a : Number( intValue > 50 )
  from accumulate( item : Item( )
                   from collect( Item( store == s )
                                 from hs.getNamedQuery( "get user items in store" )
                                        .setProperties( [ "store" : s.name, "owner" : p.name ] )
                                        .list() ),
                   average( item.price ) )
```

So for all those that say Rete can’t handle collections and nested or out of working memory data very well, I hope this shuts you up :)

NB. We would like to thank Jess for pushing the ‘accumulate’ CE, which is what ours is based on with the addition of accumulate functions. Likewise ILog JRules for the ‘collect’ CE, which is a specialised version of ‘accumulate’.

— update 29/06/2007 17.44 —  
Dave Reynolds pointed me to a paper written in 1991 that described how to do collect/accumulate like extensions to Rete:  
<http://citeseer.ist.psu.edu/477215.html>

Francois Bois pointed me to Xcerpt that describes the problem with existing languages and web based reasoning, from the site it seems our work with chained and nested ‘from’ along with ‘collect’ and ‘accumulate’ help satisfy much of this problem:  
http://www.mulberrytech.com/Extreme/Proceedings/html/2004/Schaffert01/EML2004Schaffert01-toc.html