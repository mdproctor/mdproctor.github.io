---
layout: post
title: "Truth Maintenance over Directed Graphs using Reactive Derivation Queries"
date: 2011-06-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/06/truth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Truth Maintenance over Directed Graphs using Reactive Derivation Queries](<https://blog.kie.org/2011/06/truth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 21, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Drools 5.2 is almost done and we have something very cool added. As previous blogs have mentioned, we recently added [positoinal syntax and prolog like derivation query based backward chaining](<http://blog.athico.com/2011/04/backward-chaining-emerges-in-drools.html>). However those queries were pull only and didn’t support the recently added live [“open queries”](<http://blog.athico.com/2010/05/live-querries.html>). It also had the problem that it was method recursion based, so could blow the method stack if it was too deep.

5.2 is now stack based and supports “open queries”, you just miss of the ‘?’. So what this means is you can have TMS over reactive derivation queries. If I have a key in an envelop on a desk in an office I can add a TMS justifcation that will only exist while the key remains in the office.

This should have some very interesting use cases and I look forward to seeing what people come up with. For instance you could create a rule to monitor a project’s maven dependencies and transititive depdencies and receive an alert if ASL/MIT/BSD project has a GPL dependency added via a transititive dependency.

It’s a bit abstract, but here is the unit test showing it working:
[code]
    package org.drools.test    
    import java.util.List  
    import java.util.ArrayList  
    import org.drools.Person  
      
    global List list  
      
    dialect "mvel"  
      
    declare Location  
        thing : String   
        location : String   
    end  
      
    query isContainedIn( String x, String y )   
        Location(x, y;)  
        or   
        ( Location(z, y;) and isContainedIn(x, z;) )  
    end  
      
    rule look when   
        Person( $l : likes )   
        isContainedIn( $l, 'office'; )  
    then  
       insertLogical( 'blah' );  
    end  
      
    rule existsBlah when   
        exists String( this == 'blah')   
    then  
       list.add( 'exists blah' );  
    end  
      
    rule notBlah when   
        not String( this == 'blah')   
    then  
       list.add( 'not blah' );  
    end  
      
    rule init when  
    then  
        insert( new Location("apple", "kitchen") );  
        insert( new Location("desk", "office") );  
        insert( new Location("flashlight", "desk") );  
        insert( new Location("envelope", "desk") );  
        insert( new Location("key", "envelope") );  
        insert( new Location("washing machine", "cellar") );  
        insert( new Location("nani", "washing machine") );  
        insert( new Location("broccoli", "kitchen") );  
        insert( new Location("crackers", "kitchen") );  
        insert( new Location("computer", "office") );  
    end  
      
    rule go1 when   
        String( this == 'go1')   
    then  
        list.add( rule.getName() );   
        insert( new Location('lamp', 'desk') );  
    end  
      
    rule go2 when   
        String( this == 'go2')   
        $l : Location('lamp', 'desk'; )  
    then  
        list.add( rule.getName() );   
        retract( $l );  
    end  
      
    rule go3 when   
        String( this == 'go3')   
    then  
        list.add( rule.getName() );   
        insert( new Location('lamp', 'desk') );  
    end  
      
    rule go4 when   
        String( this == 'go4')   
        $l : Location('lamp', 'desk'; )  
    then  
        list.add( rule.getName() );   
        modify( $l ) { thing = 'book' };  
    end  
      
    rule go5 when   
        String( this == 'go5')   
        $l : Location('book', 'desk'; )  
    then  
        list.add( rule.getName() );   
        modify( $l ) { thing = 'lamp' };  
    end  
      
    rule go6 when   
        String( this == 'go6')   
        $l : Location( 'lamp', 'desk'; )  
    then  
        list.add( rule.getName() );   
        modify( $l ) { thing = 'book' };  
    end  
      
    rule go7 when   
        String( this == 'go7')   
        $p : Person( likes == 'lamp' )   
    then  
        list.add( rule.getName() );   
        modify( $p ) { likes = 'key' };  
    end  
      
    -----  
      
    [go1, exists blah, go2, not blah, go3, exists blah, go4, not blah, go5, exists blah, go6, not blah, go7, exists blah]  
      
    -----  
      
    Person p = new Person();  
    p.setLikes( "lamp" );  
    FactHandle handle = ksession.insert(  p  );  
    ksession.fireAllRules();  
      
    list.clear();  
      
    FactHandle fh = ksession.insert( "go1" );  
    ksession.fireAllRules();  
    ksession.retract( fh );          
    assertEquals( "go1", list.get(0));  
    assertEquals( "exists blah", list.get(1));  
      
    fh = ksession.insert( "go2" );  
    ksession.fireAllRules();  
    ksession.retract( fh );  
    assertEquals( "go2", list.get(2));  
    assertEquals( "not blah", list.get(3));  
      
    fh = ksession.insert( "go3" );  
    ksession.fireAllRules();  
    ksession.retract( fh );  
    assertEquals( "go3", list.get(4));  
    assertEquals( "exists blah", list.get(5));          
      
    fh = ksession.insert( "go4" );  
    ksession.fireAllRules();  
    ksession.retract( fh );  
    assertEquals( "go4", list.get(6));  
    assertEquals( "not blah", list.get(7));            
      
    fh = ksession.insert( "go5" );  
    ksession.fireAllRules();  
    ksession.retract( fh );  
    assertEquals( "go5", list.get(8));  
    assertEquals( "exists blah", list.get(9));  
      
    // This simulates a modify of the root DroolsQuery object, but first we break it  
    fh = ksession.insert( "go6" );  
    ksession.fireAllRules();  
    ksession.retract( fh );  
    assertEquals( "go6", list.get(10));  
    assertEquals( "not blah", list.get(11));    
      
    // now fix it  
    fh = ksession.insert( "go7" );  
    ksession.fireAllRules();  
    ksession.retract( fh );  
    assertEquals( "go7", list.get(12));  
    assertEquals( "exists blah", list.get(13));            
      
    System.out.println( list );
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Ftruth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html&linkname=Truth%20Maintenance%20over%20Directed%20Graphs%20using%20Reactive%20Derivation%20Queries> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Ftruth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html&linkname=Truth%20Maintenance%20over%20Directed%20Graphs%20using%20Reactive%20Derivation%20Queries> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Ftruth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html&linkname=Truth%20Maintenance%20over%20Directed%20Graphs%20using%20Reactive%20Derivation%20Queries> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Ftruth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html&linkname=Truth%20Maintenance%20over%20Directed%20Graphs%20using%20Reactive%20Derivation%20Queries> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Ftruth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html&linkname=Truth%20Maintenance%20over%20Directed%20Graphs%20using%20Reactive%20Derivation%20Queries> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Ftruth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html&linkname=Truth%20Maintenance%20over%20Directed%20Graphs%20using%20Reactive%20Derivation%20Queries> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F06%2Ftruth-maintenance-over-directed-graphs-using-reactive-derivation-queries.html&linkname=Truth%20Maintenance%20over%20Directed%20Graphs%20using%20Reactive%20Derivation%20Queries> "Email")
  *[]: 2010-05-25T16:11:00+02:00