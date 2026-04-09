---
layout: post
title: "Drools 3.1 milestone 1 is comming"
date: 2006-11-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/11/drools-3-1-milestone-1-is-comming.html
---

As some of you already know, Drools 3.1m1 will be out of the door any minute now. The Drools name is used for project development releases, which are also unsupported – eventually the code is hardened and released to production as JBoss Rules 3.2. This new release is a a big improvement over the 3.0.x production branch in many ways and it will be intersting to see where we will go from there.

For those curious about it, I will briefly talk about the major changes one expect to see when moving to it, from a core/compiler perspective.

Performance 

After about 5-6 weeks of struggling led by Mark himself, most of the anchors slowing down JBRules 3.0 were simply left behind. By this I mean, no more internal structures for remembering matches, no more reference linking hell, no more overuse of array copies. Core was basically streamlined with a huge reduction on memory consumption and a significant performance boost. Benchmarks like manners, that stress the engine pattern matching algorithm are seeing improvements in the order of 300%, while memory comsuption is down to 20% of the original.  
Does that means that 3.0 performance was bad? I would say not at all! Performance was actually good on 3.0, specially when compared with previous drools versions and other open source engines. But no big improvement was possible in the 3.1 version without breaking some paradigms we had before. And Mark did an amazing job pushing every little aspect to the limit to find exactly what we needed to change.  
Does that mean real world applications will see improvements like that? Probably not in that order of magnitude, as benchmarks are designed to stress engines to its maximum, consequently generating extreme cases. Real world applications will certanly see great improvements, specially in the memory consumption side, but not in that order of magnitude. Actually I’m quite curious to test it in real use cases and see what will be the improvements.

Mark has provided a quick summary of the main enhancements:

  * Unrolled loops for constraint evaluation
  * High performance custom collections implementation
  * Tuple is now the entry, avoid Entry object creation.
  * Tuple, a wrapper for FactHandle[] during propagations, now uses a linked list as per Jess from [“Implementing A High-Performance Symbolic Reasoning Engine In Java”](<http://aaaprod.gsfc.nasa.gov/teas/Jess/JessUMBC/JessUMBC.PPT>)
  * Composite key indexing for left and right memory
  * Left and right value caching for join nodes, to avoid repeated value retrieval
  * Improved alpha node hashing
  * Extensive use of Single/Composite design to avoid setting up a for loop when there is only 1 child
  * Primitive support, avoids continuous primitive wrapping

Primitive type support

As users know, JBRules 3.0 automatically wraps any primitive types he needs to work with in its respective Object Wrappers. That was a limitation that was causing 2 undesired side effects:

  1. Performance really suffers when one needs to wrap/unwrap primitives.
  2. Code using primitive wrappers is much more verbose and cluttered.

Example:

```drl
rule "return value"
when
$person1 : Person( $age1 : age ) person2 : Person( age == ( new Integer( $age1.intValue() + 2 ) ) )
then
...
end
```

As you can see in the above example, the rule’s writer needs to be aware and keep wrapping/unwrapping primitive values to work with the engine.

JBRules 3.1m1 has now full support to primitive types, not only helping it to perform better and consume less memory but also making rules much more clear. Look at the same rule in 3.1m1:

```drl
rule "return value"
when
$person1 : Person( $age1 : age ) person2 : Person( age == ( $age1 + 2 ) )
then
...
end
```

It is now clear and straight forward to understand what the rule writer wanted his rule to do.

Shadow Facts support

As it is well known, JBRules uses POJO as its first and preferred fact representation structure. We design the engine targeting it to perform most efficiently on beans, as we understand that this is the most simple and productive way of integrating a rules engine in real world applications: work with user’s own business objects model. Although, this kind of integration demands a carefull planing on the engine side to avoid collateral effects, as the engine do not own the beans. The application or the user can change any bean property on the fly and not notify the engine.  
So it is mandatory that the engine implements some kind of control over the values being used for reasoning, keeping the whole engine state consistent. This is implemented by Shadow Facts, that are shallow copies (cache) of the bean values while reasoning over it, allowing updates only on safe points.  
Shadow Facts are implemented in JBRules 3.1m1 as dynamic proxies and besides being mandatory to have from an engine perspective, they are almost invisible for the engine users. I say almost, because being dynamic proxies, there is only one requirement users need to meet: a nonarg default constructor for the classes asserted into the engine. Besides that, users don’t have to worry about it. Only to know, their facts are being taken care appropriatelly. The proxy is not exposed to users, not even in consequence block.

New nodes

Evolving the engine also requires support to some new conditional expression elements. Three new CEs are included in 3.1m1, being them:

FROM: allows reasoning over facts not previously asserted into the engine. Specially useful for retrieval of facts on the fly from database tables or any other external source. Example:

```drl
rule "From"
when
$cheese : Cheese(type == "stilton" ) from cheesery.getCheeses()
then
// do stuffend
```

COLLECT: allows reasoning over collections of objects from working memory. Example:

```drl
rule "Collect"
when
$cheeseList  : ArrayList(size > 2) from collect( Cheese( price < 30 ) ) ;
then
// do stuffend
```

ACCUMULATE: a more flexible and customizable version of Collect, allows to iterate and calculate values from a set of facts in the working memory. Example:

```drl
rule "Accumulate"
when
$person      : Person( $likes : likes ) $cheesery    : Cheesery( totalAmount > 100 )                          from accumulate( $cheese : Cheese( type == $likes ),                                           init( Cheesery cheesery = new Cheesery(); ),                                           action( cheesery.addCheese( $cheese ); ),                                           result( cheesery ) );
then
// do stuffend
```

Conclusion

These are the main features you will se in this milestone from a core/compiler perspective. New milestones will bring even more news, specially related to the Rule Server under development as described in a previous post.

So, stay tunned, enjoy, and please provide us your feedback.

Edson