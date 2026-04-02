---
layout: post
title: "Drools goes Transactional"
date: 2009-02-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/02/drools-goes-transactional.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools goes Transactional](<https://blog.kie.org/2009/02/drools-goes-transactional.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 13, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

The last bit of work for Drools 5.0 is almost in place, where units of work can now be made transactionally. Here is a quick unit test that shows two transactions, the later with a rollback, notice the rolled back insertion does not have any affect. Statements executed outside of the user defined transaction block grab a transaction just for that single command, which is what happens with the fireAllRules(). This work was necessary so that we can combine rules and flow together but make sure those state changes are transactional. The rules side is quite heavy, but it should be fine for a small number of facts, where network latency of the DB will be the bottleneck.
[code]
      
    rule addInteger  
    when  
     $i : Integer( intValue > 1 )  
    then  
     list.add( $i );  
    end  
    
[/code]
[code]
      
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
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F02%2Fdrools-goes-transactional.html&linkname=Drools%20goes%20Transactional> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F02%2Fdrools-goes-transactional.html&linkname=Drools%20goes%20Transactional> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F02%2Fdrools-goes-transactional.html&linkname=Drools%20goes%20Transactional> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F02%2Fdrools-goes-transactional.html&linkname=Drools%20goes%20Transactional> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F02%2Fdrools-goes-transactional.html&linkname=Drools%20goes%20Transactional> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F02%2Fdrools-goes-transactional.html&linkname=Drools%20goes%20Transactional> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F02%2Fdrools-goes-transactional.html&linkname=Drools%20goes%20Transactional> "Email")