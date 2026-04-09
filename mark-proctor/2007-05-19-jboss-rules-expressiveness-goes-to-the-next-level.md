---
layout: post
title: "JBoss Rules expressiveness goes to the next level"
date: 2007-05-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/jboss-rules-expressiveness-goes-to-the-next-level.html
---

Edson has been doing great work on the expressiveness of rules, it’s now possible to use && and || on field values and between fields themselves inside of a Pattern:
```
Person( age > 30 && &lt 40 || hair =="black" )
```
Note the || here is different than the ‘or’ conditional element, which works on patterns and results in subrule generation, where each logical outcome is generated as a rule.

As part of Milestone Release 2 we already have autovivification of the field names inside of predicates and return value statemets to reduce the number of field variable declarations, which causes clutter in rules.

```
Cheese( oldPrice : oldPrice, newPrice == ( oldPrice * 1.10 ) )
```

Can now be written as:

```
Cheese( newPrice == ( oldPrice * 1.10 ) )
```

Next we are reducing created declarations for variable bindings by allowing direct access to the properties on a pattern binding declaration, note this does not include nested properties or the direct properties of a field declaration, this should further help with the readabilty of rules:

```
p : Person(personId : id)
i : Item(id == personId, value > 100 )
```

Will soon be able to write as:

```
p : Person()
i : Item(id == p.id, value > 100 )
```

The final change we hope to do in time for 4.0, which is our most requested feature, is to allow nested properties, array and hashmap access to be expressed as field constraints rather than as predicates, return value or evals. I should mention at this stage that there are a number of complications and issues with regards to nested properties, arrays and hashmaps in rule engines that many users are not aware of; the issue is similar to hashmap keys where the hashcode or fields are changed making the key and its object irretrievable and thus causing memory leaks. Internally what will really happen is that we will rewrite these expressions as an eval and execute using [MVEL](<http://mvel.codehaus.org/>).

```
Person($pets:pets)
eval($pets['rover'].type == "dog")
```

Will soon be able to write as:

```
Person( pets['rover'].type == "dog" )
```

This puts JBoss Rules firmly on the road to being one of the most expressive rule engines :)