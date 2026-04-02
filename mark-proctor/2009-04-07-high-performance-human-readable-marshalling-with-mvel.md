---
layout: post
title: "High performance human readable marshalling with MVEL"
date: 2009-04-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/04/high-performance-human-readable-marshalling-with-mvel.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [High performance human readable marshalling with MVEL](<https://blog.kie.org/2009/04/high-performance-human-readable-marshalling-with-mvel.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- April 7, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Thought I’d re-print this email to me from Mike Brock, the MVEL author:

This weekend, myself and Dhanji Prasanna from Google have firmed up an initial prototype implementation of MVBus; a new high-efficiency serialization framework built around MVEL, that is at least 4 times faster than XStream in the worst of scenarios.

It’s a very impressive framework, inspired by an an idea by Mark Proctor.

It consists of an encoding engine with modular type plug-ins, that allows any Java object to be translated in compact MVEL code, which can then be executed natively by the MVEL interpreter to be turned back into a real object.

Here’s an example of how it works:
[code]
    // Create a simple POJO object  
    Person p = new Person("Mike", 30, new String[] { "Dorkus", "Jerkhead"});  
    p.setActive(true);  
      
    // Create another...  
    Person mother = new Person("Sarah", 50, new String[] { "Mommy", "Mom"});  
    mother.setActive(false);  
      
    // And another  
    Person father = new Person("John", 55, new String[] { "Dad", "Daddy"});  
    mother.setActive(false);  
      
    // Stick them together to make a somewhat complex graph  
    p.setMother(mother);  
    p.setFather(father);  
      
    // Create an MVBus encoding bus  
    MVBus bus = MVBus.createBus();  
      
    // Encode it!  
    String marshalled = bus.encode(p);
[/code]

And here’s what that ‘marshalled’ variable contains
[code]
    org.mvbus.decode.MVBUSDecoder.instantiate(org.mvbus.tests.resources.Person).{name="Mike",age=30,nicknames=new java.lang.String[] {"Dorkus","Jerkhead"},mother=org.mvbus.decode.MVBUSDecoder.instantiate(org.mvbus.tests.resources.Person).{name="Sarah",age=50,nicknames=new java.lang.String[] {"Mommy","Mom"},active=false},father=org.mvbus.decode.MVBUSDecoder.instantiate(org.mvbus.tests.resources.Person).{name="John",age=55,nicknames=new java.lang.String[] {"Dad","Daddy"},active=false},active=true}
[/code]

This is completely native MVEL code that can be turned back into an Object simply by passing it to MVEL.eval(). And it’s very fast. However, if this isn’t pretty enough for you, the encoder has a nice pretty printer that can be turned on like so:
[code]
    MVBus bus = MVBus.createBus(PrintStyle.PRETTY);    
      
    String marshalled = bus.encode(p);
[/code]

Which produces
[code]
    org.mvbus.decode.MVBUSDecoder.instantiate(org.mvbus.tests.resources.Person).{  
            name = "Mike",  
            age = 30,  
            nicknames = new java.lang.String[] {  
                    "Dorkus","Jerkhead"  
            },  
            mother = org.mvbus.decode.MVBUSDecoder.instantiate(org.mvbus.tests.resources.Person).{  
                    name = "Sarah",  
                    age = 50,  
                    nicknames = new java.lang.String[] {  
                            "Mommy","Mom"  
                    },  
                    active = false  
            },  
            father = org.mvbus.decode.MVBUSDecoder.instantiate(org.mvbus.tests.resources.Person).{  
                    name = "John",  
                    age = 55,  
                    nicknames = new java.lang.String[] {  
                            "Dad","Daddy"  
                    },  
                    active = false  
            },  
            active = true  
    }
[/code]

… in all it’s MVEL-ly glory.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fhigh-performance-human-readable-marshalling-with-mvel.html&linkname=High%20performance%20human%20readable%20marshalling%20with%20MVEL> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fhigh-performance-human-readable-marshalling-with-mvel.html&linkname=High%20performance%20human%20readable%20marshalling%20with%20MVEL> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fhigh-performance-human-readable-marshalling-with-mvel.html&linkname=High%20performance%20human%20readable%20marshalling%20with%20MVEL> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fhigh-performance-human-readable-marshalling-with-mvel.html&linkname=High%20performance%20human%20readable%20marshalling%20with%20MVEL> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fhigh-performance-human-readable-marshalling-with-mvel.html&linkname=High%20performance%20human%20readable%20marshalling%20with%20MVEL> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fhigh-performance-human-readable-marshalling-with-mvel.html&linkname=High%20performance%20human%20readable%20marshalling%20with%20MVEL> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fhigh-performance-human-readable-marshalling-with-mvel.html&linkname=High%20performance%20human%20readable%20marshalling%20with%20MVEL> "Email")