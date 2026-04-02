---
layout: post
title: "JBoss Drools - What a difference two years make"
date: 2007-09-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/09/jboss-drools-what-a-difference-two-years-make.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [JBoss Drools – What a difference two years make](<https://blog.kie.org/2007/09/jboss-drools-what-a-difference-two-years-make.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 13, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’m just updating the Fibonacci example as we overhaul and start to document drools-examples. For a bit of nostolgia I thought I’d show how Fibonacci looked 2 years ago with Drools 2.0 and how it looks now with Drools 4.0 and the new MVEL dialect.

Drools 4.0
[code]
    package org.drools.examples  
      
    import org.drools.examples.FibonacciExample.Fibonacci;  
      
    dialect "mvel"  
      
    rule Recurse  
       salience 10  
       when  
           f : Fibonacci ( value == -1 )  
           not ( Fibonacci ( sequence == 1 ) )  
       then  
           insert( new Fibonacci( f.sequence - 1 ) );  
           System.out.println( "recurse for " + f.sequence );  
    end  
      
    rule Bootstrap  
       when  
           f : Fibonacci( sequence == 1 || == 2, value == -1 ) // this is a multi-restriction || on a single field  
       then  
           modify ( f ){ value = 1 };  
           System.out.println( f.sequence + " == " + f.value );  
    end  
      
    rule Calculate  
       when  
           f1 : Fibonacci( s1 : sequence, value != -1 ) // here we bind sequence  
           f2 : Fibonacci( sequence == (s1 + 1 ), value != -1 ) // here we don't, just to demonstrate the different way bindings can be used  
           f3 : Fibonacci( s3 : sequence == (f2.sequence + 1 ), value == -1 )              
       then    
           modify ( f3 ) { value = f1.value + f2.value };  
           System.out.println( s3 + " == " + f3.value ); // see how you can access pattern and field  bindings  
    end  
    
[/code]

Drools 2.0
[code]
    <rule-set name="fibonacci"  
              xmlns="http://drools.org/rules"  
              xmlns:java="http://drools.org/semantics/java"  
              xmlns:xs="http://www.w3.org/2001/XMLSchema-instance"  
              xs:schemaLocation="http://drools.org/rules rules.xsd  
                                 http://drools.org/semantics/java java.xsd">  
      
      <import>org.drools.examples.fibonacci.Fibonacci</import>  
      
      <rule name="Bootstrap 1" salience="20">  
        <parameter identifier="f">  
          <class>Fibonacci</class>  
        </parameter>  
      
        <java:condition>f.getSequence() == 1</java:condition>  
        <java:condition>f.getValue() == -1</java:condition>  
        <java:consequence>  
          f.setValue( 1 );  
          System.err.println( f.getSequence() + " == " + f.getValue() );  
          drools.modifyObject( f );  
        </java:consequence>  
      </rule>  
      
      <rule name="Bootstrap 2">  
        <parameter identifier="f">  
          <class>Fibonacci</class>  
        </parameter>  
        <java:condition>f.getSequence() == 2</java:condition>  
        <java:condition>f.getValue() == -1</java:condition>  
        <java:consequence>  
          f.setValue( 1 );  
          System.err.println( f.getSequence() + " == " + f.getValue() );  
          drools.modifyObject( f );  
        </java:consequence>  
      </rule>  
      
      <rule name="Recurse" salience="10">  
        <parameter identifier="f">  
          <class>Fibonacci</class>  
        </parameter>  
        <java:condition>f.getValue() == -1</java:condition>  
        <java:consequence>  
          System.err.println( "recurse for " + f.getSequence() );  
          drools.assertObject( new Fibonacci( f.getSequence() - 1 ) );  
        </java:consequence>  
      </rule>  
      
      <rule name="Calculate">  
        <parameter identifier="f1">  
          <class>Fibonacci</class>  
        </parameter>  
        <parameter identifier="f2">  
          <class>Fibonacci</class>  
        </parameter>  
        <parameter identifier="f3">  
          <class>Fibonacci</class>  
        </parameter>  
        <java:condition>f2.getSequence() == (f1.getSequence() + 1)</java:condition>  
        <java:condition>f3.getSequence() == (f2.getSequence() + 1)</java:condition>  
        <java:condition>f1.getValue() != -1</java:condition>  
        <java:condition>f2.getValue() != -1</java:condition>  
        <java:condition>f3.getValue() == -1</java:condition>  
        <java:consequence>  
          f3.setValue( f1.getValue() + f2.getValue() );  
          System.err.println( f3.getSequence() + " == " + f3.getValue() );  
          drools.modifyObject( f3 );  
          drools.retractObject( f1 );  
        </java:consequence>  
      </rule>  
      
    </rule-set>  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fjboss-drools-what-a-difference-two-years-make.html&linkname=JBoss%20Drools%20%E2%80%93%20What%20a%20difference%20two%20years%20make> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fjboss-drools-what-a-difference-two-years-make.html&linkname=JBoss%20Drools%20%E2%80%93%20What%20a%20difference%20two%20years%20make> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fjboss-drools-what-a-difference-two-years-make.html&linkname=JBoss%20Drools%20%E2%80%93%20What%20a%20difference%20two%20years%20make> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fjboss-drools-what-a-difference-two-years-make.html&linkname=JBoss%20Drools%20%E2%80%93%20What%20a%20difference%20two%20years%20make> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fjboss-drools-what-a-difference-two-years-make.html&linkname=JBoss%20Drools%20%E2%80%93%20What%20a%20difference%20two%20years%20make> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fjboss-drools-what-a-difference-two-years-make.html&linkname=JBoss%20Drools%20%E2%80%93%20What%20a%20difference%20two%20years%20make> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F09%2Fjboss-drools-what-a-difference-two-years-make.html&linkname=JBoss%20Drools%20%E2%80%93%20What%20a%20difference%20two%20years%20make> "Email")