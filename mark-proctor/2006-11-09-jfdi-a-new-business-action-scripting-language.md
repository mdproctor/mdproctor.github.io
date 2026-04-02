---
layout: post
title: "JFDI a new Business Action Scripting Language"
date: 2006-11-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/11/jfdi-a-new-business-action-scripting-language.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [JFDI a new Business Action Scripting Language](<https://blog.kie.org/2006/11/jfdi-a-new-business-action-scripting-language.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- November 9, 2006  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

We are working on a new non-imperative conseqeuence language for JBoss Ruless, called [JFDI](<http://xircles.codehaus.org/projects/jfdi>) which is a sort of business action scripting language. We have placed this project over at Codehaus as we are hoping that it will get taken up by other declarative systems, whether they are rule or process engines.

When we first thought about doing this we got a deluge of emails like “have you looked at groovy, rhino, judoscript etc” – the answer was obviously “yes”. The last thing wanted to do was yet another language and we looked hard into using those languages, but they all fell short. Not short in features, but short becuase they did too much!!! Here was the main feature set:  
1) A rule consequence should be “when this then that”, not “when this maybe that”, its quite simply a list of actions to be performed when this situation occurs. Therefor it should not contain any imperative code, no “if”, “switch” statements, its purely focused on expressions, method/function calls and we will allow a foreach loop. If someone needs to do some imperative code it should be encapsulated within a method or a function which is then called from the consequence.

2) The language should not be ambiguous and thus should be typed, although we may eventually allow type inference. Support for refactoring is definitely a long term goal.

3) A rule base may have thousands of rules, currently with JBoss Rules you end up with a minimum of two classes per rule and then a further class for each function, predicate, return value or ‘eval’ used. This large number of classes can cause a number of problems from perm gen issues to slowing down the system’s classloader. Therefore it must be able to run interpreted, no bytecode generation. A consequence can be serialised to disk and lazy loaded on first use. While this is interpreted, as much as possible is done at “compile” time with no runtime introspection, so it’s a tree of cached java.lang.reflect.Method calls. Although eventually we would like optional bytecode generation optimisations, but generally it is not the execution of the consequence that is the bottleneck.

4) A simple groovy/ruby like expression syntax. We need non-verbose ways to reference sub fields and to declare and reference maps and arrays, with support for inline anonymous maps and arrays. We would like further support for variable interpolation and <<EOF type stream writing.

5) The traditional way to “inject” variables into a scripting language is to put each key/value pair into a dictionary or context. We use to do this before drools-2.0-beta-14, it is not performant, instead we need to allow the application to determine at compile time how to resolve those external variables.

6) We need to be able to decorate a variable, at compile time, with additional methods – this way in a consequence a user can do “myVar.getFactHandle()” even if the variable itself does not support that method.

7) Native support for more complex types like BigInteger, BigDecimal and currency types is needed – so we need more control over that.

8) In-built support for FactTemplates (a better DynaBean) so they can be used as if they were real classes.

9) A less verbose way to set setters “instance(field1=z, field2=42)”. Ability to call a constructor and set fields in a single statement “new BarBaz(field1 = “val”, field2 = “x”)”.

10) The dependancy must be small, a few hundred kb.

Bob McWhirter has been busy beavering away on this and the project is getting to an almost useable state; although there is no content on the website you can start to look over the unit tests to get an idea of how the language is turning out.  
<http://svn.codehaus.org/jfdi/trunk/test/org/codehaus/jfdi/interpreter/>  
<http://svn.codehaus.org/jfdi/trunk/test/org/codehaus/jfdi/>

A quick look at the language itself:
[code]
      
    //fields  
    instance.field = value;  
    instance(field1=z, field2=42)  
    instance.map["key"] = value;  
    instance.array[0] = value;  
      
    // method call with an inline map and array   
    instance.method( [1, 2,"z", var], {"a" => 2, "b"   
    // standard constructor  
    bar = new BarBaz("x", 42)  
      
    // calls default constructor, THEN setters   
    bar = new BarBaz(field1 = "val", field2 = "x")  
    
[/code]

We are still trying to decide on the for each loop syntax. Bob wants to offer both the crappy java5 syntax (otherwise people will complain) and something more readable:
[code]
      
    foreach item in collection {  
     func(item)  
     func2(index) # index available automatically as a counter?  
    }  
      
    For ( item : collection  ) {  
     func(item)  
     func2(index) # index available automatically as a counter?  
    }  
    
[/code]

We don’t just plan to use this language for consequences, it will also be used from predicates, return values and ‘eval’s as well as the upcoming ‘accumulate’ and ‘from’ conditional elements.
[code]
      
    $cheese : Cheese( /* additional field constraints go here */ )   
              from session.getNamedQuery("thename").setProperties( {"key1" => "value1", "key2" => "value2" }).list()  
    
[/code]

So if you like what you see why not roll up your sleaves and get involved. A free T-Shirt to the first person that hassles bob to apply some patches :)

[Post Comment](<https://beta.blogger.com/comment.g?blogID=5869426&postID=4038874689439260478>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fjfdi-a-new-business-action-scripting-language.html&linkname=JFDI%20a%20new%20Business%20Action%20Scripting%20Language> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fjfdi-a-new-business-action-scripting-language.html&linkname=JFDI%20a%20new%20Business%20Action%20Scripting%20Language> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fjfdi-a-new-business-action-scripting-language.html&linkname=JFDI%20a%20new%20Business%20Action%20Scripting%20Language> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fjfdi-a-new-business-action-scripting-language.html&linkname=JFDI%20a%20new%20Business%20Action%20Scripting%20Language> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fjfdi-a-new-business-action-scripting-language.html&linkname=JFDI%20a%20new%20Business%20Action%20Scripting%20Language> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fjfdi-a-new-business-action-scripting-language.html&linkname=JFDI%20a%20new%20Business%20Action%20Scripting%20Language> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F11%2Fjfdi-a-new-business-action-scripting-language.html&linkname=JFDI%20a%20new%20Business%20Action%20Scripting%20Language> "Email")