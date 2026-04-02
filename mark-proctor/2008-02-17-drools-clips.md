---
layout: post
title: "Drools Clips"
date: 2008-02-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/02/drools-clips.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Clips](<https://blog.kie.org/2008/02/drools-clips.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 17, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’ve done some more work on Drools Clips in the last few weeks and it’s starting to take shape now and the basic shell is working and we should have something useful as part of the next Drools milestone release in a few weeks. You can see the unit tests here:  
http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/drools-clips/src/test/java/org/drools/clips/ShellTest.java

Below you can see two of the unit tests demonstrating deffunctions and rules:
[code]
      
    public void testRuleCallDeftemplate() {  
        String function = "(deffunction max (?a ?b) (if (> ?a ?b) then (return ?a) else (return ?b) ) )";  
        this.shell.eval( function );  
          
        this.shell.eval( "(import org.drools.*)" );  
        this.shell.eval( "(defrule testRule (Person (age ?age) ) => (printout t hello)  
                          (printout t " " (max 3 ?age) ) )" );  
        this.shell.eval( "(assert (Person (name mark) (age 32) ) )" );  
        this.shell.eval( "(run)" );  
        assertEquals( "hello 32",  
                      new String( this.baos.toByteArray() ) );          
    }  
      
    public void testTwoSimpleRulesWithModify() {  
        this.shell.eval( "(import org.drools.*)" );  
        this.shell.eval( "(defrule testRule ?p   
                          (printout t hello) (printout t " " ?name) (modify ?p (name bob) ) )" );  
        this.shell.eval( "(defrule testRule (Person (name ?name&bob) ) => (printout t  
                           hello) (printout t " " ?name))" );  
        this.shell.eval( "(assert (Person (name mark) ) )" );  
        this.shell.eval( "(run)" );  
        assertEquals( "hello markhello bob",  
                      new String( this.baos.toByteArray() ) );  
    }  
    
[/code]

We have support for a large set of the Clips LHS rule syntax and functions are easy to add. As Drools DRL also has support for the Jess 7.0 style infix notation we will add support for that too. The goal is to support the full LHS syntax for Jess and Clips. For now we will be missing out logical assertions, Jess slot specific and Clips COOL. Our logical assertion approaches are slightly different, so it’s easier to leave that out, and we currently have no way to support slot specific which is also the behaviour of Clips COOL. As we have full support for Java pojos and their approach to OO we have less need for COOL at this stage. It would be nice to add slot specific support soon and I hope to do it some time this year.

We do not yet support deftemplates but the rules will reason directly over pojo classes, as our DRL already does. I will add support for those soon.

One of the cool things about this is that it doesn’t just allow you to execute Jess and Clips rules but that it also provides you with a migration path. Using DrlDumper you can now load Jess/Clips rules via drools-clips and have the DrlDumper dump them to the more modern Drools DRL syntax.

I’ve actually changed my design approach for this. Originally I was building my own Lisp execution engine and then realised that I was creating much of the infrastructure that we already had put into MVEL. As Lisp really is just an abstract syntax tree you can actually take any Lisp statement and dump it to MVEL for execution. So I gave up on my own Lisp execution engine and instead did a Lisp to MVEL converter. This is only a stop gap though as Mike Brock has promised to eventually do a direct S-Expression lexer and parser for MVEL. It’s trivial to add new built-in functions to drools-clips by simply creating an MVEL language dumper. You can look at the existing functions like the ‘if’ function in the link below to see how simple this is:  
http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/drools-clips/src/main/java/org/drools/clips/functions/IfFunction.java

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fdrools-clips.html&linkname=Drools%20Clips> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fdrools-clips.html&linkname=Drools%20Clips> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fdrools-clips.html&linkname=Drools%20Clips> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fdrools-clips.html&linkname=Drools%20Clips> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fdrools-clips.html&linkname=Drools%20Clips> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fdrools-clips.html&linkname=Drools%20Clips> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F02%2Fdrools-clips.html&linkname=Drools%20Clips> "Email")