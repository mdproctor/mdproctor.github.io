---
layout: post
title: "Glazed Lists examples for Drools Live Querries"
date: 2010-07-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/07/glazed-lists-examples-for-drools-live-querries.html
---

A while back I talked about the new features with Drools for Live querries:  
<http://blog.athico.com/2010/05/live-querries.html>

Where you could open a query in Drools and receive event notifications for added, deleted and upated rows. I mentioned this could be used with [Glazed Lists](<http://sites.google.com/site/glazedlists/>) for filtering, sorting and transformation.

I just added a unit test to Drools, which people can use as a template for their own Drools integration with Glazed Lists. The test is based on the one in [QueryTest.testOpenQuery()](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-compiler/src/test/java/org/drools/integrationtests/QueryTest.java?r=HEAD>):  
[DroolsEventList](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-compiler/src/test/java/org/drools/integrationtests/DroolsEventList.java?r=HEAD>)  
[DroolsEventListTest](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-compiler/src/test/java/org/drools/integrationtests/DroolsEventListTest.java?r=HEAD>)

The EventList implemention itself is very simple. At the moment it backs onto an ArrayList and uses linear searches for the updates and removes. Because Drools is likely to have a high volume of changes it should probably be backed by a HashMap or something for constant levels of performance for those lookups.

```java
public class DroolsEventList extends AbstractEventList implements ViewChangedEventListener {
    List data = new ArrayList();
    
    public Row get(int index) {
        return this.data.get( index );
    }

    public int size() {
        return this.data.size();
    }

    public void rowAdded(Row row) {
        int index = size();
        updates.beginEvent();
        updates.elementInserted(index, row);
        boolean result = data.add(row);
        updates.commitEvent();
    }

    public void rowRemoved(Row row) {
        int index = this.data.indexOf( row );
        updates.beginEvent();
        Row removed = data.remove( index );
        updates.elementDeleted(index, removed);        
        updates.commitEvent();
    }

    public void rowUpdated(Row row) {
        int index = this.data.indexOf( row );    
        updates.beginEvent();
        updates.elementUpdated(index, row, row);
        updates.commitEvent();
    }
}
```

Creating and using the EventList is also trivial, here is a snippet from the test using the SortedEventList:

```java
DroolsEventList list = new DroolsEventList();
        // Open the LiveQuery
        LiveQuery query = ksession.openLiveQuery( "cheeses", new Object[] { "cheddar", "stilton" } , list );
        
        SortedList sorted = new SortedList( list, new Comparator() {

            public int compare(Row r1,
                               Row r2) {
                Cheese c1 = ( Cheese ) r1.get( "stilton" );
                Cheese c2 = ( Cheese ) r2.get( "stilton" );
                return c1.getPrice() - c2.getPrice();
            }
        });

        
        assertEquals( 3, sorted.size() );
        assertEquals( 1, ((Cheese)sorted.get( 0 ).get( "stilton" )).getPrice() );
        assertEquals( 2, ((Cheese)sorted.get( 1 ).get( "stilton" )).getPrice() );
        assertEquals( 3, ((Cheese)sorted.get( 2 ).get( "stilton" )).getPrice() );
```