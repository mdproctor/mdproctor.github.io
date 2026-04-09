---
layout: post
title: "Declarative agenda and control rules"
date: 2011-08-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/08/declarative-agenda-and-control-rules.html
---

From the thread here:  
<http://drools.46999.n3.nabble.com/Declarative-Agenda-td3232818.html>

I just got a first cut working for “declarative agenda”. The idea here is rules can control which rule can or cannot fire. Because this is highly experimental it is off by default and users must explicitely enable it, it will stay this way until we are happy with the solution. My hope is that it will provide a more declarative approach to execution control; which will enable more readable and maintainable rules compared to using magic salience values and in some circumstances control objects.

```
KnowledgeBaseConfiguration kconf = KnowledgeBaseFactory.newKnowledgeBaseConfiguration();
kconf.setOption( DeclarativeAgendaOption.ENABLED );
KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase(  kconf );
```

The basic idea is:

  * All matched rule’s Activations are inserted into WorkingMemory as facts. So you can now match against an Activation the rules metadata and declarations are available as fields on the Activation object.
  * You can use the kcontext.block( $a ) for the current rule to block the selected activation. Only when that rule becomes false will the activation be elegible for firing. If it is already elebible for firing and is later blocked, it will be removed from the agenda until it is unblocked.
  * An activation may have multiple blockers, all blockers must became false, so they are removed to enable the activation to fire
  * kcontext.unblockAll( $a ) is an over-ride rule that will remove all blockers regardless
  * @activationListener(‘direct’) allows a rule to fire as soon as it’s matched, this is to be used for rules that block/unblock activations, it is not desirable for these rules to have side effects that impact else where. The name may change later, this is actually part of the pluggable terminal node handlers I made, which is an “internal” feature for the moment.

I should be committing this later today, and will send a follow up email once it hits HEAD, but here is a unit test. It uses a control role to stop all rules with metadata declaring the rules to be in the “sales” department. Only when that control rule becomes false can they fire.

```drl
package org.domain.testimport org.drools.runtime.
rule.Activationglobal java.util.List listdialect 'mvel'
rule rule1 @department('sales')
when
$s : String( this == 'go1' )
then
list.add( kcontext.
rule.name + ':' + $s );endrule rule2 @department('sales')
when
$s : String( this == 'go1' )
then
list.add( kcontext.
rule.name + ':' + $s );endrule rule3 @department('sales')
when
$s : String( this == 'go1' )
then
list.add( kcontext.
rule.name + ':' + $s );endrule blockerAllSalesRules @activationListener('direct')
when
$s : String( this == 'go2' )  $i : Activation( department == 'sales' )
then
list.add( $i.
rule.name + ':' + $s  ); kcontext.block( $i );
end
```

```java
KnowledgeBaseConfiguration kconf =  KnowledgeBaseFactory.newKnowledgeBaseConfiguration();kconf.setOption( DeclarativeAgendaOption.ENABLED );KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase( kconf );kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );StatefulKnowledgeSession ksession = kbase.newStatefulKnowledgeSession();List list = new ArrayList();ksession.setGlobal( "list", list);ksession.insert(  "go1" );FactHandle go2 = ksession.insert(  "go2" );ksession.fireAllRules();assertEquals( 3, list.size() ); // none of the rules 1-3 fire, as they  are blocked.assertTrue( list.contains( "rule1:go2" ));assertTrue( list.contains( "rule2:go2" ));assertTrue( list.contains( "rule3:go2" ));list.clear();ksession.retract( go2 ); // the blocker
rule is nolonger true, so rules  1-3 can now fire.ksession.fireAllRules();assertEquals( 3, list.size() );assertTrue( list.contains( "rule1:go1" ));assertTrue( list.contains( "rule2:go1" ));assertTrue( list.contains( "rule3:go1" ));ksession.dispose();UpdateI have now committed this work to master and you can checkout the comphensive tests to see how it works here: https://github.com/droolsjbpm/drools/blob/master/drools-compiler/src/test/java/org/drools/integrationtests/DeclarativeAgendaTest.java
```