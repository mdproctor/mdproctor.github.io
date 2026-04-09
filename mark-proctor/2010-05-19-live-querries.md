---
layout: post
title: "Live Querries"
date: 2010-05-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/05/live-querries.html
---

Drools has always had query support, but the result was returned as an iterable set; this makes it hard to monitor changes over time.

I did a little hacking this weekend and we have now complimented this with Live Querries, which has a listener attached instead of returning an iterable result set. These live querries stay open creating a view and publish change events for the contents of this view.

So now you can execute your query, with parameters and listen to changes in the resulting view.

There are many applications for this, but already I’m thinking about [Glazed List](<http://publicobject.com/glazedlists/>) integration, so it can be used to provide advanced filtering for table displays.

Hopefully this unit test is self explanatory, for those interested, the main part is the creating of the listener and the opening of the live query.

```java
String str = "";
str += "package org.drools.test  n";
str += "import org.drools.Cheese n";
str += "query cheeses(String $type1, String $type2) n";
str += "    stilton : Cheese(type == $type1, $price : price) n";
str += "    cheddar : Cheese(type == $type2, price == stilton.price) n";
str += "endn";

KnowledgeBuilder kbuilder = KnowledgeBuilderFactory.newKnowledgeBuilder();
kbuilder.add( ResourceFactory.newByteArrayResource( str.getBytes() ),
              ResourceType.DRL );

if ( kbuilder.hasErrors() ) {
    fail( kbuilder.getErrors().toString() );
}

KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase();
kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );

StatefulKnowledgeSession ksession = kbase.newStatefulKnowledgeSession();
Cheese stilton1 = new Cheese( "stilton", 1 );
Cheese cheddar1 = new Cheese( "cheddar", 1 );
Cheese stilton2 = new Cheese( "stilton", 2 );
Cheese cheddar2 = new Cheese( "cheddar", 2 );
Cheese stilton3 = new Cheese( "stilton", 3 );
Cheese cheddar3 = new Cheese( "cheddar", 3 );

org.drools.runtime.rule.FactHandle s1Fh = ksession.insert( stilton1 );
ksession.insert( stilton2 );
ksession.insert( stilton3 );
ksession.insert( cheddar1 );
ksession.insert( cheddar2 );
org.drools.runtime.rule.FactHandle c3Fh = ksession.insert( cheddar3 );

final List updated = new ArrayList();
final List removed = new ArrayList();
final List added = new ArrayList();

ViewChangedEventListener listener = new ViewChangedEventListener() {            
 public void rowUpdated(Row row) {
  updated.add( row.get( "$price" ) );
 }
 
 public void rowRemoved(Row row) {
  removed.add( row.get( "$price" ) );
 }
 
 public void rowAdded(Row row) {
  added.add( row.get( "$price" ) );
 }
};        

// Open the LiveQuery
LiveQuery query = ksession.openLiveQuery( "cheeses", 
                                          new Object[] { "cheddar", "stilton" },
                                          listener );

// Assert that on opening we have three rows added
assertEquals( 3, added.size() );
assertEquals( 0, removed.size() );
assertEquals( 0, updated.size() );

// And that we have correct values from those rows
assertEquals( 1, added.get( 0 ) );
assertEquals( 2, added.get( 1 ) );
assertEquals( 3, added.get( 2 ) );

// Do an update that causes a match to become untrue, thus triggering a removed
cheddar3.setPrice( 4 );
ksession.update(  c3Fh, cheddar3 );

assertEquals( 3, added.size() );
assertEquals( 1, removed.size() );
assertEquals( 0, updated.size() );

assertEquals( 4, removed.get( 0 ) );
  
// Now make that partial true again, and thus another added
cheddar3.setPrice( 3 );
ksession.update(  c3Fh, cheddar3 );

assertEquals( 4, added.size() );
assertEquals( 1, removed.size() );
assertEquals( 0, updated.size() );  

assertEquals( 3, added.get( 3 ) );        

// check a standard update
cheddar3.setOldPrice( 0 );
ksession.update(  c3Fh, cheddar3 ); 

assertEquals( 4, added.size() );
assertEquals( 1, removed.size() );
assertEquals( 1, updated.size() );         

assertEquals( 3, updated.get( 0 ) );      

// Check a standard retract
ksession.retract( s1Fh );
  
assertEquals( 4, added.size() );
assertEquals( 2, removed.size() );
assertEquals( 1, updated.size() );    

assertEquals( 1, removed.get( 1 ) );          

// Close the query, we should get removed events for each row
query.close();

assertEquals( 4, added.size() );
assertEquals( 4, removed.size() );
assertEquals( 1, updated.size() );         

assertEquals( 2, removed.get( 2 ) );
assertEquals( 3, removed.get( 3 ) );

// Check that updates no longer have any impact.
ksession.update(  c3Fh, cheddar3 ); 
assertEquals( 4, added.size() );
assertEquals( 4, removed.size() );
assertEquals( 1, updated.size() );
```