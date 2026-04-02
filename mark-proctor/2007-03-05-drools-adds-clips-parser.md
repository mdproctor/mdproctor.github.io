---
layout: post
title: "Drools adds Clips parser"
date: 2007-03-05
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/03/drools-adds-clips-parser.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools adds Clips parser](<https://blog.kie.org/2007/03/drools-adds-clips-parser.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 5, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

We have often stated that the Drools rule engine is fully language independant, but to date it’s only had two parsers – XML and DRL. For a bit of fun this weekend, hey I’m a willd type of guy, I went ahead and started on an experimental Clips grammar with ANTLR, although its still a long way from being finished. I hope It should eventually provide a migration path for Clips users as well as demonstrate how people can build their own grammars for the Drools rule engine using ANTLR, you don’t have to use ANTLR, but its our parser of choice. Clients who use other vendor products and want to migrate, but worried about the investment in the authored rules, can now write parsers for those products targetting JBoss Rules; obviously there are other things to consider like feature parity and execution models. We also support “dumpers”, via the visitor design patter, making round tripping possible – i.e. currently you can load an xml and dump drl, and vice versa, we will try and make the same possible with Clips.

So far it’s parsing multiple rules with multiple patterns, it supports literal, bound variable, predicate and return value field constraints as well as & and | field constraint connectives. I don’t yet have it working with functions, so I’ve just put text into the predicate and return value for now, for the purposes of testing. The next stage is to get nested Conditional Elements working including ‘and’, ‘or’, ‘not’ and ‘exists’. The really adventerous can help make ‘accumulate’, ‘collect’ and ‘from’ available :)

Clips/Lisp is a fairly simple grammar so this is a great learning project for anyone that wants to learn ANTLR and how to write custom parsers for the Drools Rule Engine; so if you want to help out why not pop onto codehause IRC [#drools,](<http://labs.jboss.com/portal/jbossrules/irc.html>) or subscribe to our developer mailing list, and we’ll help you get started.

The Clips ANTLR grammar is here <http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/drools-compiler/src/main/resources/org/drools/clp/CLP.g>

And for those interested here is the current unit test. This demonstrates the intermediate AST we use to build a language agnostic view of a grammar. This AST is “dumb” and we call it Descr, short for Description, this is because everything at this stage is held in a String format; little or not validation has been done, it’s just a pure string based tree representing the rules, this is then pass to the PackageBuider which validates the descr tree and builds the resulting rule AST.
[code]
        
      public void testRule() throws Exception {  
           RuleDescr rule = parse(  
           "(defrule xxx ?b <- (person (name "yyy"&?bf|~"zzz"|~=(ppp)&:(ooo)) )   
                         ?c <- (hobby (type ?bf2&~iii) (rating fivestar) )").rule();  
            
           assertEquals( "xxx", rule.getName() );  
            
           AndDescr lhs = rule.getLhs();  
           List lhsList = lhs.getDescrs();  
           assertEquals(2, lhsList.size());  
            
           // Parse the first column  
           ColumnDescr col = ( ColumnDescr ) lhsList.get( 0 );  
           assertEquals("?b", col.getIdentifier() );  
           assertEquals("person", col.getObjectType() );  
            
           List colList = col.getDescrs();  
           assertEquals(2, colList.size());  
           FieldConstraintDescr fieldConstraintDescr = ( FieldConstraintDescr ) colList.get( 0 );  
           List restrictionList = fieldConstraintDescr.getRestrictions();  
            
           assertEquals("name", fieldConstraintDescr.getFieldName() );         
           // @todo the 7th one has no constraint, as its a predicate, have to figure out how to handle this  
           assertEquals(8, restrictionList.size());  
                    
            
           LiteralRestrictionDescr litDescr = ( LiteralRestrictionDescr ) restrictionList.get( 0 );  
           assertEquals("==", litDescr.getEvaluator() );  
           assertEquals("yyy", litDescr.getText() );  
      
           RestrictionConnectiveDescr connDescr = ( RestrictionConnectiveDescr ) restrictionList.get( 1 );  
           assertEquals(RestrictionConnectiveDescr.AND, connDescr.getConnective() );  
            
           VariableRestrictionDescr varDescr = ( VariableRestrictionDescr ) restrictionList.get( 2 );  
           assertEquals("==", varDescr.getEvaluator() );  
           assertEquals("?bf", varDescr.getIdentifier() );         
            
           connDescr = ( RestrictionConnectiveDescr ) restrictionList.get( 3 );  
           assertEquals(RestrictionConnectiveDescr.OR, connDescr.getConnective() );  
            
           litDescr = ( LiteralRestrictionDescr ) restrictionList.get( 4 );  
           assertEquals("!=", litDescr.getEvaluator() );  
           assertEquals("zzz", litDescr.getText() );  
            
           connDescr = ( RestrictionConnectiveDescr ) restrictionList.get( 5 );  
           assertEquals(RestrictionConnectiveDescr.OR, connDescr.getConnective() );  
            
           ReturnValueRestrictionDescr retDescr = ( ReturnValueRestrictionDescr ) restrictionList.get( 6 );  
           assertEquals("!=", retDescr.getEvaluator() );  
           assertEquals("ppp", retDescr.getText() );  
            
           PredicateDescr predicateDescr = ( PredicateDescr ) colList.get( 1 );  
           assertEquals( "ooo", predicateDescr.getText() );  
            
            
           // Parse the second column  
           col = ( ColumnDescr ) lhsList.get( 1 );  
           assertEquals("?c", col.getIdentifier() );  
           assertEquals("hobby", col.getObjectType() );    
      
           colList = col.getDescrs();  
           assertEquals(2, colList.size());  
           fieldConstraintDescr = ( FieldConstraintDescr ) colList.get( 0 );  
           restrictionList = fieldConstraintDescr.getRestrictions();  
            
           assertEquals("type", fieldConstraintDescr.getFieldName() );         
            
           varDescr = ( VariableRestrictionDescr ) restrictionList.get( 0 );  
           assertEquals("==", varDescr.getEvaluator() );  
           assertEquals("?bf2", varDescr.getIdentifier() );   
            
           connDescr = ( RestrictionConnectiveDescr ) restrictionList.get( 1 );  
           assertEquals(RestrictionConnectiveDescr.AND, connDescr.getConnective() );  
            
           litDescr = ( LiteralRestrictionDescr ) restrictionList.get( 2 );  
           assertEquals("!=", litDescr.getEvaluator() );  
           assertEquals("iii", litDescr.getText() );  
            
           fieldConstraintDescr = ( FieldConstraintDescr ) colList.get( 1 );  
           restrictionList = fieldConstraintDescr.getRestrictions();         
            
           assertEquals("rating", fieldConstraintDescr.getFieldName() );  
            
           litDescr = ( LiteralRestrictionDescr ) restrictionList.get( 0 );  
           assertEquals("==", litDescr.getEvaluator() );  
           assertEquals("fivestar", litDescr.getText() );         
       }  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fdrools-adds-clips-parser.html&linkname=Drools%20adds%20Clips%20parser> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fdrools-adds-clips-parser.html&linkname=Drools%20adds%20Clips%20parser> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fdrools-adds-clips-parser.html&linkname=Drools%20adds%20Clips%20parser> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fdrools-adds-clips-parser.html&linkname=Drools%20adds%20Clips%20parser> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fdrools-adds-clips-parser.html&linkname=Drools%20adds%20Clips%20parser> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fdrools-adds-clips-parser.html&linkname=Drools%20adds%20Clips%20parser> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F03%2Fdrools-adds-clips-parser.html&linkname=Drools%20adds%20Clips%20parser> "Email")