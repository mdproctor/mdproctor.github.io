---
layout: post
title: "Truth Maintenance over Directed Graphs using Reactive Derivation Queries"
date: 2011-06-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/06/truth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html
---

Drools 5.2 is almost done and we have something very cool added. As previous blogs have mentioned, we recently added [positoinal syntax and prolog like derivation query based backward chaining](<http://blog.athico.com/2011/04/backward-chaining-emerges-in-drools.html>). However those queries were pull only and didn’t support the recently added live [“open queries”](<http://blog.athico.com/2010/05/live-querries.html>). It also had the problem that it was method recursion based, so could blow the method stack if it was too deep.

5.2 is now stack based and supports “open queries”, you just miss of the ‘?’. So what this means is you can have TMS over reactive derivation queries. If I have a key in an envelop on a desk in an office I can add a TMS justifcation that will only exist while the key remains in the office.

This should have some very interesting use cases and I look forward to seeing what people come up with. For instance you could create a rule to monitor a project’s maven dependencies and transititive depdencies and receive an alert if ASL/MIT/BSD project has a GPL dependency added via a transititive dependency.

It’s a bit abstract, but here is the unit test showing it working:

```drl
package org.drools.test
import java.util.Listimport java.util.ArrayListimport org.drools.Personglobal List listdialect "mvel"
declare Location    thing : String     location : String endquery isContainedIn( String x, String y )     Location(x, y;)    or     ( Location(z, y;) and isContainedIn(x, z;) )endrule look
when
Person( $l : likes )     isContainedIn( $l, 'office'; )
then
insertLogical( 'blah' );endrule existsBlah
when
exists String( this == 'blah')
then
list.add( 'exists blah' );endrule notBlah
when
not String( this == 'blah')
then
list.add( 'not blah' );endrule init whenthen    insert( new Location("apple", "kitchen") );    insert( new Location("desk", "office") );    insert( new Location("flashlight", "desk") );    insert( new Location("envelope", "desk") );    insert( new Location("key", "envelope") );    insert( new Location("washing machine", "cellar") );    insert( new Location("nani", "washing machine") );    insert( new Location("broccoli", "kitchen") );    insert( new Location("crackers", "kitchen") );    insert( new Location("computer", "office") );endrule go1
when
String( this == 'go1')
then
list.add(
rule.getName() );     insert( new Location('lamp', 'desk') );endrule go2
when
String( this == 'go2')     $l : Location('lamp', 'desk'; )
then
list.add(
rule.getName() );     retract( $l );endrule go3
when
String( this == 'go3')
then
list.add(
rule.getName() );     insert( new Location('lamp', 'desk') );endrule go4
when
String( this == 'go4')     $l : Location('lamp', 'desk'; )
then
list.add(
rule.getName() );     modify( $l ) { thing = 'book' };endrule go5
when
String( this == 'go5')     $l : Location('book', 'desk'; )
then
list.add(
rule.getName() );     modify( $l ) { thing = 'lamp' };endrule go6
when
String( this == 'go6')     $l : Location( 'lamp', 'desk'; )
then
list.add(
rule.getName() );     modify( $l ) { thing = 'book' };endrule go7
when
String( this == 'go7')     $p : Person( likes == 'lamp' )
then
list.add(
rule.getName() );     modify( $p ) { likes = 'key' };
end
-----[go1, exists blah, go2, not blah, go3, exists blah, go4, not blah, go5, exists blah, go6, not blah, go7, exists blah]-----Person p = new Person();p.setLikes( "lamp" );FactHandle handle = ksession.insert(  p  );ksession.fireAllRules();list.clear();FactHandle fh = ksession.insert( "go1" );ksession.fireAllRules();ksession.retract( fh );        assertEquals( "go1", list.get(0));assertEquals( "exists blah", list.get(1));fh = ksession.insert( "go2" );ksession.fireAllRules();ksession.retract( fh );assertEquals( "go2", list.get(2));assertEquals( "not blah", list.get(3));fh = ksession.insert( "go3" );ksession.fireAllRules();ksession.retract( fh );assertEquals( "go3", list.get(4));assertEquals( "exists blah", list.get(5));        fh = ksession.insert( "go4" );ksession.fireAllRules();ksession.retract( fh );assertEquals( "go4", list.get(6));assertEquals( "not blah", list.get(7));          fh = ksession.insert( "go5" );ksession.fireAllRules();ksession.retract( fh );assertEquals( "go5", list.get(8));assertEquals( "exists blah", list.get(9));// This simulates a modify of the root DroolsQuery object, but first we break itfh = ksession.insert( "go6" );ksession.fireAllRules();ksession.retract( fh );assertEquals( "go6", list.get(10));assertEquals( "not blah", list.get(11));  // now fix itfh = ksession.insert( "go7" );ksession.fireAllRules();ksession.retract( fh );assertEquals( "go7", list.get(12));assertEquals( "exists blah", list.get(13));          System.out.println( list );
```