---
layout: post
title: "Rete DSL testing harness"
date: 2009-11-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/11/rete-dsl-testing-harness.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Rete DSL testing harness](<https://blog.kie.org/2009/11/rete-dsl-testing-harness.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- November 15, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

As our Rete implementation gets more complicated we need to find easier and more maintainable ways to test our node implementations. Currently we have unit tests for all our nodes done in pure java, setting these up is laborious and because of the amount of java code involved makes it hard to read the intention. I’m finding that we are relying more on higher level integration tests, which is lazy and not as good as catching the problems earlier and in a more isolated manner. Take for example the JoinNode, this is the sample code necessary to setup a node for testing and apply some assertion tests:
[code]
       public void setUp() {  
           // create mock objects  
           constraint = mockery.mock( BetaNodeFieldConstraint.class );  
           final ContextEntry c = mockery.mock( ContextEntry.class );  
      
           // set mock objects expectations  
           mockery.checking( new Expectations() {  
               {  
                   // allowed calls and return values  
                   allowing( constraint ).createContextEntry();  
                   will( returnValue( c ) );  
      
                   allowing( c ).updateFromFactHandle( with( any( InternalWorkingMemory.class ) ),  
                                                       with( any( InternalFactHandle.class ) ) );  
                   allowing( c ).updateFromTuple( with( any( InternalWorkingMemory.class ) ),  
                                                  with( any( LeftTuple.class ) ) );  
                   allowing( c ).resetTuple();  
                   allowing( c ).resetFactHandle();  
               }  
           } );  
      
           this.rule = new Rule( "test-rule" );  
           this.context = new PropagationContextImpl( 0,  
                                                      PropagationContext.ASSERTION,  
                                                      null,  
                                                      null,  
                                                      null );  
           this.workingMemory = new ReteooWorkingMemory( 1,  
                                                         (ReteooRuleBase) RuleBaseFactory.newRuleBase() );  
      
           this.tupleSource = new MockTupleSource( 4 );  
           this.objectSource = new MockObjectSource( 4 );  
           this.sink = new MockLeftTupleSink();  
      
           final RuleBaseConfiguration configuration = new RuleBaseConfiguration();  
      
           ReteooRuleBase ruleBase = (ReteooRuleBase) RuleBaseFactory.newRuleBase();  
           BuildContext buildContext = new BuildContext( ruleBase,  
                                                         ruleBase.getReteooBuilder().getIdGenerator() );  
      
           this.node = new JoinNode( 15,  
                                     this.tupleSource,  
                                     this.objectSource,  
                                     new DefaultBetaConstraints( new BetaNodeFieldConstraint[]{this.constraint},  
                                                                 configuration ),  
                                     Behavior.EMPTY_BEHAVIOR_LIST,  
                                     buildContext );  
      
           this.node.addTupleSink( this.sink );  
      
           this.memory = (BetaMemory) this.workingMemory.getNodeMemory( this.node );  
      
           // check memories are empty  
           assertEquals( 0,  
                         this.memory.getLeftTupleMemory().size() );  
           assertEquals( 0,  
                         this.memory.getRightTupleMemory().size() );  
      
       }  
      
       public void testRetractTuple() throws Exception {  
           // set mock objects expectations  
           mockery.checking( new Expectations() {  
               {  
                   // allowed calls and return values  
                   allowing( constraint ).isAllowedCachedLeft( with( any( ContextEntry.class ) ),  
                                                               with( any( InternalFactHandle.class ) ) );  
                   will( returnValue( true ) );  
                   allowing( constraint ).isAllowedCachedRight( with( any( LeftTuple.class ) ),  
                                                                with( any( ContextEntry.class ) ) );  
                   will( returnValue( true ) );  
               }  
           } );  
      
           // setup 2 tuples 3 fact handles  
           final DefaultFactHandle f0 = (DefaultFactHandle) this.workingMemory.insert( "test0" );  
           this.node.assertObject( f0,  
                                   this.context,  
                                   this.workingMemory );  
      
           final DefaultFactHandle f1 = (DefaultFactHandle) this.workingMemory.insert( "test1" );  
           final LeftTuple tuple1 = new LeftTuple( f1,  
                                                   this.node,  
                                                   true );  
           this.node.assertLeftTuple( tuple1,  
                                      this.context,  
                                      this.workingMemory );  
      
           final DefaultFactHandle f2 = (DefaultFactHandle) this.workingMemory.insert( "test2" );  
           final LeftTuple tuple2 = new LeftTuple( f2,  
                                                   this.node,  
                                                   true );  
           this.node.assertLeftTuple( tuple2,  
                                      this.context,  
                                      this.workingMemory );  
      
           final DefaultFactHandle f3 = (DefaultFactHandle) this.workingMemory.insert( "test3" );  
           this.node.assertObject( f3,  
                                   this.context,  
                                   this.workingMemory );  
      
           final DefaultFactHandle f4 = (DefaultFactHandle) this.workingMemory.insert( "test4" );  
           this.node.assertObject( f4,  
                                   this.context,  
                                   this.workingMemory );  
      
           assertLength( 6,  
                         this.sink.getAsserted() );  
      
           // Double check the item is in memory  
           final BetaMemory memory = (BetaMemory) this.workingMemory.getNodeMemory( this.node );  
           assertTrue( memory.getRightTupleMemory().contains( f0.getFirstRightTuple() ) );  
      
           // Retract an object, check propagations  and memory  
           this.node.retractRightTuple( f0.getFirstRightTuple(),  
                                        this.context,  
                                        this.workingMemory );  
           assertLength( 2,  
                         this.sink.getRetracted() );  
      
           List tuples = new ArrayList();  
           tuples.add( ((Object[]) this.sink.getRetracted().get( 0 ))[0] );  
           tuples.add( ((Object[]) this.sink.getRetracted().get( 1 ))[0] );  
      
           assertTrue( tuples.contains( new LeftTuple( tuple1,  
                                                       f0.getFirstRightTuple(),  
                                                       this.sink,  
                                                       true ) ) );  
           assertTrue( tuples.contains( new LeftTuple( tuple1,  
                                                       f0.getFirstRightTuple(),  
                                                       this.sink,  
                                                       true ) ) );  
      
           // Now check the item  is no longer in memory  
           assertFalse( memory.getRightTupleMemory().contains( f0.getFirstRightTuple() ) );  
      
           this.node.retractLeftTuple( tuple2,  
                                       this.context,  
                                       this.workingMemory );  
           assertEquals( 4,  
                         this.sink.getRetracted().size() );  
      
           tuples = new ArrayList();  
           tuples.add( ((Object[]) this.sink.getRetracted().get( 2 ))[0] );  
           tuples.add( ((Object[]) this.sink.getRetracted().get( 3 ))[0] );  
      
           assertTrue( tuples.contains( new LeftTuple( tuple2,  
                                                       f3.getFirstRightTuple(),  
                                                       this.sink,  
                                                       true ) ) );  
           assertTrue( tuples.contains( new LeftTuple( tuple2,  
                                                       f4.getFirstRightTuple(),  
                                                       this.sink,  
                                                       true ) ) );  
       }
[/code]

I think everyone agrees that’s a lot of code and hard for anyone, especially noobies, to understand it’s intent.

This means that developers can be apathetic when adding more similar tests for edge cases and we have a long term maintenance problem when bringing new developers on board.

Enter the “Rete DSL testing harness”. This is an indentation based DSL for setting up and testing nodes. My plan is next to have it working with JUnit4 with a customised test suite. Hopefully everyone can understand what this is doing, which is actually doing and testing more than the above java code.
[code]
    // setup the nodes  
    ObjectTypeNode  
       otn1, java.lang.Integer  
    LeftInputAdapterNode  
       lian0, otn1  
    ObjectTypeNode  
       otn2, java.lang.Integer  
    ObjectTypeNode  
       otn3, java.lang.Integer         
      
    // creating a binding to be used in the JoinNode creation  
    Binding  
        p1, 0, java.lang.Integer, intValue  
      
    JoinNode  
       join1, lian0, otn2  
       intValue, !=, p1  
    JoinNode  
       join2, join1, otn3  
       intValue, !=, p1  
      
    //insert some facts, this returns and stores an array called "h"        
    Facts  
       0, 1, 2, 3, 4  
      
    // hd+ is used for compactness (not too many brackets) but is internally rewritten  
    // as h[d+] and evaluated with MVEL against a "h"  
    assert  
       otn1 [h1, h3]         
       otn2 [h0, h2]  
       otn3 [h4]   
      
    // we can now test some memories, memory order is deterministic       
    join1  
       leftMemory [[h1], [h3]] // matches with only one fact  
       rightMemory [h0, h2]  
    join2  
       leftMemory [[h1, h0], [h3, h0],  
                   [h1, h2], [h3, h2]] // matches with two chained facts  
       rightMemory [h4]         
    retract  
       otn1 [h1]         
       otn2 [h2];  
    join1  
       leftMemory [ [h3] ]  
       rightMemory [h0]       
    join2  
       leftMemory  [[h3, h0]]  
       rightMemory [h4]   
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Frete-dsl-testing-harness.html&linkname=Rete%20DSL%20testing%20harness> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Frete-dsl-testing-harness.html&linkname=Rete%20DSL%20testing%20harness> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Frete-dsl-testing-harness.html&linkname=Rete%20DSL%20testing%20harness> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Frete-dsl-testing-harness.html&linkname=Rete%20DSL%20testing%20harness> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Frete-dsl-testing-harness.html&linkname=Rete%20DSL%20testing%20harness> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Frete-dsl-testing-harness.html&linkname=Rete%20DSL%20testing%20harness> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F11%2Frete-dsl-testing-harness.html&linkname=Rete%20DSL%20testing%20harness> "Email")