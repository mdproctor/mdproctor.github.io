---
layout: post
title: "JBoss Drools - What a difference two years make"
date: 2007-09-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/09/jboss-drools-what-a-difference-two-years-make.html
---

I’m just updating the Fibonacci example as we overhaul and start to document drools-examples. For a bit of nostolgia I thought I’d show how Fibonacci looked 2 years ago with Drools 2.0 and how it looks now with Drools 4.0 and the new MVEL dialect.

Drools 4.0

```drl
package org.drools.examplesimport org.drools.examples.FibonacciExample.Fibonacci;
dialect "mvel"
rule Recurse
salience 10
when
f : Fibonacci ( value == -1 )       not ( Fibonacci ( sequence == 1 ) )
then
insert( new Fibonacci( f.sequence - 1 ) );       System.out.println( "recurse for " + f.sequence );endrule Bootstrap
when
f : Fibonacci( sequence == 1 || == 2, value == -1 ) // this is a multi-restriction || on a single field
then
modify ( f ){ value = 1 };       System.out.println( f.sequence + " == " + f.value );endrule Calculate
when
f1 : Fibonacci( s1 : sequence, value != -1 ) // here we bind sequence       f2 : Fibonacci( sequence == (s1 + 1 ), value != -1 ) // here we don't, just to demonstrate the different way bindings can be used       f3 : Fibonacci( s3 : sequence == (f2.sequence + 1 ), value == -1 )
then
modify ( f3 ) { value = f1.value + f2.value };       System.out.println( s3 + " == " + f3.value ); // see how you can access pattern and field  bindingsend
```

Drools 2.0

```xml
<rule-set xmlns="http://drools.org/rules" xmlns:java="http://drools.org/semantics/java" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" name="fibonacci" xs:schemaLocation="http://drools.org/rules rules.xsd                             http://drools.org/semantics/java java.xsd">
    
  <import>org.drools.examples.fibonacci.Fibonacci</import>
    
  <rule name="Bootstrap 1" salience="20">
        
    <parameter identifier="f">
            
      <class>Fibonacci</class>
          
    </parameter>
        
    <java:condition>f.getSequence() == 1</java:condition>
        
    <java:condition>f.getValue() == -1</java:condition>
        
    <java:consequence>      f.setValue( 1 );      System.err.println( f.getSequence() + " == " + f.getValue() );      drools.modifyObject( f );    </java:consequence>
      
  </rule>
    
  <rule name="Bootstrap 2">
        
    <parameter identifier="f">
            
      <class>Fibonacci</class>
          
    </parameter>
        
    <java:condition>f.getSequence() == 2</java:condition>
        
    <java:condition>f.getValue() == -1</java:condition>
        
    <java:consequence>      f.setValue( 1 );      System.err.println( f.getSequence() + " == " + f.getValue() );      drools.modifyObject( f );    </java:consequence>
      
  </rule>
    
  <rule name="Recurse" salience="10">
        
    <parameter identifier="f">
            
      <class>Fibonacci</class>
          
    </parameter>
        
    <java:condition>f.getValue() == -1</java:condition>
        
    <java:consequence>      System.err.println( "recurse for " + f.getSequence() );      drools.assertObject( new Fibonacci( f.getSequence() - 1 ) );    </java:consequence>
      
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
        
    <java:consequence>      f3.setValue( f1.getValue() + f2.getValue() );      System.err.println( f3.getSequence() + " == " + f3.getValue() );      drools.modifyObject( f3 );      drools.retractObject( f1 );    </java:consequence>
      
  </rule>
</rule-set>
```