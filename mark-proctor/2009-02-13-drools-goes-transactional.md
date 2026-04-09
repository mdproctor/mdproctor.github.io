---
layout: post
title: "Drools goes Transactional"
date: 2009-02-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/02/drools-goes-transactional.html
---

The last bit of work for Drools 5.0 is almost in place, where units of work can now be made transactionally. Here is a quick unit test that shows two transactions, the later with a rollback, notice the rolled back insertion does not have any affect. Statements executed outside of the user defined transaction block grab a transaction just for that single command, which is what happens with the fireAllRules(). This work was necessary so that we can combine rules and flow together but make sure those state changes are transactional. The rules side is quite heavy, but it should be fine for a small number of facts, where network latency of the DB will be the bottleneck.

```drl
rule addInteger
when
 $i : Integer( intValue > 1 )
then
 list.add( $i );
end
```

```text
KnowledgeBuilder kbuilder = KnowledgeBuilderFactory.newKnowledgeBuilder();
kbuilder.add( ResourceFactory.newByteArrayResource( str.getBytes() ),
           ResourceType.DRL );
KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase();

if ( kbuilder.hasErrors() ) {
 fail( kbuilder.getErrors().toString() );
}

kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );

StatefulKnowledgeSession ksession = kbase.newStatefulKnowledgeSession( conf );

List list = new ArrayList();
UserTransaction ut = (UserTransaction) new InitialContext().lookup( "java:comp/UserTransaction"
ut.begin();
ksession.setGlobal( "list",
                  list );
ksession.insert( 1 );
ksession.insert( 2 );
ut.commit();

ut.begin();
ksession.insert( 3 );
ut.rollback();

ksession.fireAllRules();

assertEquals( 2,
           list.size() );
```