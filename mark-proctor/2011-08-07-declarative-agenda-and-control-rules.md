---
layout: post
title: "Declarative agenda and control rules"
date: 2011-08-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/08/declarative-agenda-and-control-rules.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Declarative agenda and control rules](<https://blog.kie.org/2011/08/declarative-agenda-and-control-rules.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- August 7, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

From the thread here:  
<http://drools.46999.n3.nabble.com/Declarative-Agenda-td3232818.html>

I just got a first cut working for “declarative agenda”. The idea here is rules can control which rule can or cannot fire. Because this is highly experimental it is off by default and users must explicitely enable it, it will stay this way until we are happy with the solution. My hope is that it will provide a more declarative approach to execution control; which will enable more readable and maintainable rules compared to using magic salience values and in some circumstances control objects.
[code]
    KnowledgeBaseConfiguration kconf = KnowledgeBaseFactory.newKnowledgeBaseConfiguration();  
    kconf.setOption( DeclarativeAgendaOption.ENABLED );  
    KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase(  kconf );
[/code]

The basic idea is:

  * All matched rule’s Activations are inserted into WorkingMemory as facts. So you can now match against an Activation the rules metadata and declarations are available as fields on the Activation object.
  * You can use the kcontext.block( $a ) for the current rule to block the selected activation. Only when that rule becomes false will the activation be elegible for firing. If it is already elebible for firing and is later blocked, it will be removed from the agenda until it is unblocked.
  * An activation may have multiple blockers, all blockers must became false, so they are removed to enable the activation to fire
  * kcontext.unblockAll( $a ) is an over-ride rule that will remove all blockers regardless
  * @activationListener(‘direct’) allows a rule to fire as soon as it’s matched, this is to be used for rules that block/unblock activations, it is not desirable for these rules to have side effects that impact else where. The name may change later, this is actually part of the pluggable terminal node handlers I made, which is an “internal” feature for the moment.

I should be committing this later today, and will send a follow up email once it hits HEAD, but here is a unit test. It uses a control role to stop all rules with metadata declaring the rules to be in the “sales” department. Only when that control rule becomes false can they fire.
[code]
    package org.domain.test  
    import org.drools.runtime.rule.Activation  
    global java.util.List list  
    dialect 'mvel'  
      
    rule rule1 @department('sales')  
    when  
      $s : String( this == 'go1' )  
    then  
     list.add( kcontext.rule.name + ':' + $s );  
    end  
    rule rule2 @department('sales')  
    when  
      $s : String( this == 'go1' )  
    then  
     list.add( kcontext.rule.name + ':' + $s );  
    end  
    rule rule3 @department('sales')  
    when  
      $s : String( this == 'go1' )  
    then  
     list.add( kcontext.rule.name + ':' + $s );  
    end  
    rule blockerAllSalesRules @activationListener('direct')  
    when  
      $s : String( this == 'go2' )  
      $i : Activation( department == 'sales' )  
    then  
     list.add( $i.rule.name + ':' + $s  );  
     kcontext.block( $i );  
    end
[/code]
[code]
    KnowledgeBaseConfiguration kconf =  KnowledgeBaseFactory.newKnowledgeBaseConfiguration();  
    kconf.setOption( DeclarativeAgendaOption.ENABLED );  
    KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase( kconf );  
    kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );  
    StatefulKnowledgeSession ksession = kbase.newStatefulKnowledgeSession();  
      
    List list = new ArrayList();  
    ksession.setGlobal( "list", list);  
    ksession.insert(  "go1" );  
      
    FactHandle go2 = ksession.insert(  "go2" );  
    ksession.fireAllRules();  
    assertEquals( 3, list.size() ); // none of the rules 1-3 fire, as they  are blocked.  
    assertTrue( list.contains( "rule1:go2" ));  
    assertTrue( list.contains( "rule2:go2" ));  
    assertTrue( list.contains( "rule3:go2" ));  
      
    list.clear();  
      
    ksession.retract( go2 ); // the blocker rule is nolonger true, so rules  1-3 can now fire.  
    ksession.fireAllRules();  
      
    assertEquals( 3, list.size() );  
    assertTrue( list.contains( "rule1:go1" ));  
    assertTrue( list.contains( "rule2:go1" ));  
    assertTrue( list.contains( "rule3:go1" ));  
      
    ksession.dispose();  
      
    Update  
    I have now committed this work to master and you can checkout the comphensive tests to see how it works here:   
    <https://github.com/droolsjbpm/drools/blob/master/drools-compiler/src/test/java/org/drools/integrationtests/DeclarativeAgendaTest.java>  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fdeclarative-agenda-and-control-rules.html&linkname=Declarative%20agenda%20and%20control%20rules> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fdeclarative-agenda-and-control-rules.html&linkname=Declarative%20agenda%20and%20control%20rules> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fdeclarative-agenda-and-control-rules.html&linkname=Declarative%20agenda%20and%20control%20rules> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fdeclarative-agenda-and-control-rules.html&linkname=Declarative%20agenda%20and%20control%20rules> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fdeclarative-agenda-and-control-rules.html&linkname=Declarative%20agenda%20and%20control%20rules> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fdeclarative-agenda-and-control-rules.html&linkname=Declarative%20agenda%20and%20control%20rules> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fdeclarative-agenda-and-control-rules.html&linkname=Declarative%20agenda%20and%20control%20rules> "Email")
  *[]: 2010-05-25T16:11:00+02:00