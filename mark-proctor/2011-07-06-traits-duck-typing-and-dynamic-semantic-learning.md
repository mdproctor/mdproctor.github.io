---
layout: post
title: "Traits, Duck Typing and Dynamic Semantic Learning"
date: 2011-07-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/07/traits-duck-typing-and-dynamic-semantic-learning.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Traits, Duck Typing and Dynamic Semantic Learning](<https://blog.kie.org/2011/07/traits-duck-typing-and-dynamic-semantic-learning.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 6, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Duck typing is the ability to say that something implements an interface. In this article I’ll focus on triples (sets of key value pairs) such as Maps in Java or Dictionaries in other languages – <Map-instance, key-obj, value-obj>. I will outline how the concepts of traits could be used in Drools to infer semantic abstractions over sets of triples, which allows for dynamic semantic learning over time. The terms map and triple set will be used interchangeably.

Duck Typing: <http://en.wikipedia.org/wiki/Duck_typing>  
  
“When I see a bird that walks like a duck and swims like a duck and quacks like a duck, I call that bird a duck.”

Triples: <http://en.wikipedia.org/wiki/Resource_Description_Framework>  
  
“the form of subject-predicate-object expressions. These expressions are known as triples in RDF terminology. The subject denotes the resource, and the predicate denotes traits or aspects of the resource and expresses a relationship between the subject and the object. For example, one way to represent the notion “The sky has the color blue” in RDF is as the triple: a subject denoting “the sky”, a predicate denoting “has the color”, and an object denoting “blue”.”

Duck typing over triples is the ability to say that the instance that represents the set of triples can be treated like an instance of a interface. This allows static type safe access to dynamic triple structures, it also allows abstraction through semantic representation of what that thing is; i.e. it’s not just a set of arbitrary triples, it is a Student. MVEL does not yet support the “dons”, as in “wears” keyword, so please take this as illustrative. The keyword may change eventually but it was proposed by Davide Sottara, who is POCing this idea.

I’ll use MVEL like syntax to demonstrate:
[code]
    bean = [ name : "Zod", age : 150 ]
      
    bean dons Human
      
    assertEquals( "Zod", bean.name )
      
    assertEquals( 150, bean.age)
[/code]

Without the don’s keyword to duck type the map to the interface this would not compile as the compiler would report a static typing error of unknown fields for “name” and “age”.

Now that we know duck typing can be used to allow static type safety access to map. What else can we do? In a rule based system if we used triples to represent facts (which is what semantic ontologies do) we can’t declare up front what interfaces a map wears, and those interfaces might change over time too. So we can use special rules to dynamically apply traits to a triple set.
[code]
    rule Human when
      
       $tp : Map( this contains [ "name" : String, "age" : int ] )
      
    then
      
       $tp dons Human// that $tp instance is now recognised by all other rules that match on Human
      
    end
      
    
      
    rule HelloWorld when
      
       $s : Human() // this will actually match against the Map "donned" to Human
      
    then
      
       println( "hello " + $s.name );
      
    end
[/code]

We can see the rule that applies the trait can probably have a first class representation for it’s use case. Which makes the rules intent far more obvious thus increasing the readability and maintainability of the system.
[code]
    trait Human( String name, int age ) when
      
    end
[/code]

In the above, “trait” is a new keyword and Human is the trait name. We pass all the fields and their type as arguments. The triple set must contain at least those keys, but of course it may contain more. Notice we have an empty “when” block. The reason for this is we can apply different logic as to when a trait is applied, beyond just matching known keys to fields.

For instance if someone is Human and is also 18 years of age or younger we can apply a further abstraction and say the are not just Human but also a Student. We use the “dons” keyword after the arguments to say the existing traits the Map must already wear, i.e. abstractions we already know about the thing.
[code]
    trait Student( String name, int age ) dons Human  when
      
       age( < 18; ) end
[/code]

The proposed syntax would allow argument names to be used as the pattern head and the type is inferred. We could also allow operators to be used in the positional syntax. This is to give compact sugar for “Integer( this < 18 ) from age”.

So now we have a system to detect and recognise sets of triples and declare what traits they have; what abstractions we infer for them. As the system learns new things keys may be added to the map and new abstractions can be inferred by declaring more traits,which in turn allows further reasoning. Keys may also be removed which results in traits being removed.

One of the problems of a purely tripled based approach is performance, both in terms of execution speed but more important memory usage. If “name” and “age” both have to be represented as objects the system is going to bloat fast. What we want is to allow a mixed type system of static and dynamic relations. The relations are what we refer to for each of the key/value pairs in the triple set, i.e. a property (bean getter and setter pair, normally on a member field) is a relation on a class.

When a normal bean is inserted we will know it don’s all the interfaces it implements and thus all the properties those interfaces declares. When accessing those properties we will do so via the standard getter or setters. This means properties we know up front and that don’t change, can be declare using standard java fields with getter and setters. Allowing quick access and low memory utilisation. However we will allow further relations (triples) to be associated with the instance, as “dynamic” properties.

The specialised ‘trait’ rules will uniformly detect existing static properties or dynamically added properties. It’s important to remember that a trait is a runtime applied interface to given instance, and just that instance. Bean instances of the same concrete type can wear different traits at any given time. Except of course for the statically declare interfaces on the concrete implementation.

Lets work through a complete example now. Human is a type declaration which is generated as an actual class from which beans can be initiated, “name”, “age” and “gender” are static relations. Young, Boy and FussyEater are all interfaces. Human extends TripleSet so that we know that further dynamic relations can be added and traits applied. We detect the bean instance is “< 18” and thus the trait Young is applied and that if the gender is M the trait Boy is applied. Further if a property exists, either static or dynamic (the two are seamless in the syntax) called “dislikes” with a value of “carrots” we apply the FussyEater trait.
[code]
    declare Human extends TripleSet
      
       String name;
      
       int age;
      
       Gender gender; // M/F enum
      
    end  
      
    
      
    trait Young(int age) dons Human when     
      
       age( < 18; ) 
      
    end  
      
    
      
    trait Boy(Gender gender) dons Young when     
      
       Gender( Gender.M; ) 
      
    end  
      
    
      
    trait FussyEater(String dislikes) dons Boy when     
      
       dislikes( “carrots”; ) 
      
    end
[/code]

Now that we have a system that can detect and declare fussy eaters, lets use it. First declare a person who is 16, that will be an actual bean instance. Then add the dynamic property “dislikes”. Finally insert a new command to give that person some ice cream.
[code]
    // Lets declare a new triple for a given bean instance that we instantiated from Human
      
    Human human = new Human( “Zod”, 16 )
      
    human.add(  [dislikes : “carrots”]  )
      
    insert ( human )
      
    insert( new GiveIceCream( human ) );
[/code]

We can now have a single rule that disallows fussy eaters from getting ice cream. How cool is that :)
[code]
    rule “Don't give icecream to boys who are fussy eaters”
      
        $f : FussyEater()
      
        $d : GiveIceCream( $f; )
      
    then
      
      retract ( $d )  
      
    end
[/code]

Because traits can be applied conditional on facts and facts can be logically inserted to be maintained by the truth maintenance system, that means we can have traits who existence is dependant on those logical insertions. When the series of premesis that creates the chain of logical insertiosn breaks the trait depending on it will be un-applied to the instance. See this previous blog for more details on TMS [“Drools Inference and Truth Maintenance for good rule design and maintenance”](<http://blog.athico.com/2010/01/drools-inference-and-truth-maintenance.html>).

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Ftraits-duck-typing-and-dynamic-semantic-learning.html&linkname=Traits%2C%20Duck%20Typing%20and%20Dynamic%20Semantic%20Learning> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Ftraits-duck-typing-and-dynamic-semantic-learning.html&linkname=Traits%2C%20Duck%20Typing%20and%20Dynamic%20Semantic%20Learning> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Ftraits-duck-typing-and-dynamic-semantic-learning.html&linkname=Traits%2C%20Duck%20Typing%20and%20Dynamic%20Semantic%20Learning> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Ftraits-duck-typing-and-dynamic-semantic-learning.html&linkname=Traits%2C%20Duck%20Typing%20and%20Dynamic%20Semantic%20Learning> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Ftraits-duck-typing-and-dynamic-semantic-learning.html&linkname=Traits%2C%20Duck%20Typing%20and%20Dynamic%20Semantic%20Learning> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Ftraits-duck-typing-and-dynamic-semantic-learning.html&linkname=Traits%2C%20Duck%20Typing%20and%20Dynamic%20Semantic%20Learning> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Ftraits-duck-typing-and-dynamic-semantic-learning.html&linkname=Traits%2C%20Duck%20Typing%20and%20Dynamic%20Semantic%20Learning> "Email")
  *[]: 2010-05-25T16:11:00+02:00