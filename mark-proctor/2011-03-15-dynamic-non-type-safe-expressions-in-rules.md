---
layout: post
title: "Dynamic (non type safe) Expressions in Rules"
date: 2011-03-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/03/dynamic-non-type-safe-expressions-in-rules.html
---

Drools is a statically typed language, which means it has to know the types of all fields up front. Sometimes, like in Collections, this just isn’t possible.

Previously we hacked this such as if you used a map or array accessor in an expression it would switch dynamic execution in MVEL for this.

We have now cleaned up this feature and made it generally available. Using type declarations you can now declare a type as un-typesafe. That then means it will not validate the expressions or their types at compile time and it will execute those expressions in dynamic (non-strict type) mvel mode.

Here is the unit test for those that want to see it in action:

```drl
@Test    public void testNoneTypeSafeDeclarations() {        // same namespace        String str = "
package org.droolsn" +            "
global java.util.List listn" +            "
declare Personn" +            "    @typesafe(false)n" +            "endn" +            "
rule testTypeSafen
dialect "mvel" whenn" +            "   $p : Person( object.street == 's1' )n" +            "thenn" +            "   list.add( $p );n" +            "endn";         executeTypeSafeDeclarations( str, true );            // different namespace with
import        str = "
package org.drools.testn" +            "
import org.drools.Personn" +            "
global java.util.List listn" +            "
declare Personn" +            "    @typesafe(false)n" +            "endn" +            "
rule testTypeSafen
dialect "mvel" whenn" +            "   $p : Person( object.street == 's1' )n" +            "thenn" +            "   list.add( $p );n" +            "endn";                    executeTypeSafeDeclarations( str, true );           // different namespace without
import using qualified name        str = "
package org.drools.testn" +            "
global java.util.List listn" +            "
declare org.drools.Personn" +            "    @typesafe(false)n" +            "endn" +            "
rule testTypeSafen
dialect "mvel" whenn" +            "   $p : org.drools.Person( object.street == 's1' )n" +            "thenn" +            "   list.add( $p );n" +            "endn";                executeTypeSafeDeclarations( str, true );           // this should fail as it's not declared non typesafe         str = "
package org.drools.testn" +            "
global java.util.List listn" +            "
declare org.drools.Personn" +            "    @typesafe(true)n" +            "endn" +            "
rule testTypeSafen
dialect "mvel" whenn" +            "   $p : org.drools.Person( object.street == 's1' )n" +            "thenn" +            "   list.add( $p );n" +            "endn";                executeTypeSafeDeclarations( str, false );                }         private void executeTypeSafeDeclarations(String str, boolean mustSucceed) {                    KnowledgeBuilder kbuilder = KnowledgeBuilderFactory.newKnowledgeBuilder();        kbuilder.add( ResourceFactory.newByteArrayResource( str.getBytes() ),                      ResourceType.DRL );        if ( kbuilder.hasErrors() ) {            if ( mustSucceed ) {                fail( kbuilder.getErrors().toString() );            } else {                return;            }        }         KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase();        kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );        StatefulKnowledgeSession ksession = kbase.newStatefulKnowledgeSession();        List list = new ArrayList();        ksession.setGlobal( "list",                            list );        Address a = new Address("s1" );        Person p = new Person( "yoda" );        p.setObject( a );         ksession.insert( p );        ksession.fireAllRules();        assertEquals( p, list.get(0));            }
```