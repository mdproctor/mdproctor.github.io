---
layout: post
title: "Fine Grained Property Change Listeners (Slot Specific) (Mario Fusco)"
date: 2012-01-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/01/fine-grained-property-change-listeners-slot-specific-mario-fusco.html
---

Just a quick recap of what I did until now to check if we are all on the same page and also agree with the naming convention I used.

The property specific feature is off by default in order to make the behavior of the rule engine backward compatible with the former releases. If you want to activate it on a specific bean you have to annotate it with @propSpecific. This annotation works both on drl type declarations:

```drl
declare Person
 @propSpecific
 firstName : String
 lastName : String
end
```

and on Java classes:

@PropSpecific  
public static class Person {  
private String firstName;  
private String lastName;  
}

Moreover on Java classes you can also annotate any method to say that its invocation actually modifies other properties. For instance in the former Person class you could have a method like:

@Modifies( “firstName, lastName” )  
public void setName(String name) {  
String[] names = name.split(“\s”);  
this.firstName = names[0];  
this.lastName = names[1];  
}

That means that if a rule has a RHS like the following:

modify($person) { setName(“Mario Fusco”) }

it will correctly recognize that both the firstName and lastName have been modified and act accordingly. Of course the @Modifies annotation on a method has no effect if the declaring class isn’t annotated with @PropSpecific.

The third annotation I have introduced is on patterns and allows you to modify the inferred set of properties “listened” by it. So, for example, you can annotate a pattern in the LHS of a rule like:

Person( firstName == $expectedFirstName ) @watch( lastName ) // –> listens for changes on both firstName (inferred) and lastName  
Person( firstName == $expectedFirstName ) @watch( * ) // –> listens for all the properties of the Person bean  
Person( firstName == $expectedFirstName ) @watch( lastName, !firstName ) // –> listens for changes on lastName and explicitly exclude firstName  
Person( firstName == $expectedFirstName ) @watch( *, !age ) // –> listens for changes on all the properties except the age one

Once again this annotation has no effect if the corresponding pattern’s type hasn’t been annotated with @PropSpecific.

I’ve almost finished with the development of this feature (at the moment I am missing the compile-time check of the properties named in the @watch annotation together with some more exhaustive tests), so if you think that I misunderstood something or there is room for any improvement (or you just don’t like the annotation’s names I chose) please let me know as soon as possible.

Mario