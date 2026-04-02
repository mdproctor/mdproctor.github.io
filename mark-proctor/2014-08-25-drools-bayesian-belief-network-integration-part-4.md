---
layout: post
title: "Drools - Bayesian Belief Network Integration Part 4"
date: 2014-08-25
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/08/drools-bayesian-belief-network-integration-part-4.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools – Bayesian Belief Network Integration Part 4](<https://blog.kie.org/2014/08/drools-bayesian-belief-network-integration-part-4.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- August 25, 2014  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

This follows my earlier [Part 3](<http://blog.athico.com/2014/05/drools-bayesian-belief-network.html>) posting in May.  
  
I have integrated the Bayesian System into the Truth Maintenance System, with a first end to end test. It’s still very raw, but it demonstrates how the TMS can be used to provide evidence via logical insertions.   
  
The BBN variables are mapped to fields on the Garden class. Evidence is applied as a logical insert, using a property reference – indicating it’s evidence for the variable mapped to that property. If there is conflict evidence for the same field, then the fact becomes undecided.   
  
The rules are added via a String, while the BBN is added from a file. This code uses the new pluggable knowledge types, which allow pluggable parsers, builders and runtimes. This is how the Bayesian stuff is added cleanly, without touching the core – but I’ll blog about those another time.
[code]
    String drlString = "package org.drools.bayes; " +
    "import " + Garden.class.getCanonicalName() + "; n"  +
    "import " + PropertyReference.class.getCanonicalName() + "; n"  +
    "global " +  BayesBeliefFactory.class.getCanonicalName() + " bsFactory; n" +
    "dialect 'mvel'; n" +
    " " +
    "rule rule1 when " +
    "        String( this == 'rule1') n" +
    "    g : Garden()" +
    "then " +
    "    System.out.println("rule 1"); n" +
    "    insertLogical( new PropertyReference(g, 'cloudy'), bsFactory.create( new double[] {1.0,0.0} ) ); n " +
    "end " +
    "rule rule2 when " +
    "        String( this == 'rule2') n" +
    "    g : Garden()" +
    "then " +
    "    System.out.println("rule2"); n" +
    "    insertLogical( new PropertyReference(g, 'sprinkler'), bsFactory.create( new double[] {1.0,0.0} ) ); n " +
    "end " +
    "rule rule3 when " +
    "        String( this == 'rule3') n" +
    "    g : Garden()" +
    "then " +
    "    System.out.println("rule3"); n" +
    "    insertLogical( new PropertyReference(g, 'sprinkler'), bsFactory.create( new double[] {1.0,0.0} ) ); n " +
    "end " +
    "rule rule4 when " +
    "        String( this == 'rule4') n" +
    "    g : Garden()" +
    "then " +
    "    System.out.println("rule4"); n" +
    "    insertLogical( new PropertyReference(g, 'sprinkler'), bsFactory.create( new double[] {0.0,1.0} ) ); n " +
    "end " +
    "n";
    KnowledgeBuilder kBuilder = KnowledgeBuilderFactory.newKnowledgeBuilder();
    kBuilder.add( ResourceFactory.newByteArrayResource(drlString.getBytes()),
    ResourceType.DRL );
    kBuilder.add( ResourceFactory.newClassPathResource("Garden.xmlbif", AssemblerTest.class), ResourceType.BAYES );
    KnowledgeBase kBase = KnowledgeBaseFactory.newKnowledgeBase();
    kBase.addKnowledgePackages( kBuilder.getKnowledgePackages() );
    StatefulKnowledgeSession kSession = kBase.newStatefulKnowledgeSession();
    NamedEntryPoint ep = (NamedEntryPoint) ksession.getEntryPoint(EntryPointId.DEFAULT.getEntryPointId());
    BayesBeliefSystem bayesBeliefSystem = new BayesBeliefSystem( ep, ep.getTruthMaintenanceSystem());
    BayesBeliefFactoryImpl bayesBeliefValueFactory = new BayesBeliefFactoryImpl(bayesBeliefSystem);
    ksession.setGlobal( "bsFactory", bayesBeliefValueFactory);
    BayesRuntime bayesRuntime = ksession.getKieRuntime(BayesRuntime.class);
    BayesInstance&amp;lt;Garden&amp;gt; instance = bayesRuntime.createInstance(Garden.class);
    assertNotNull(  instance );
    assertTrue(instance.isDecided());
    instance.globalUpdate();
    Garden garden = instance.marginalize();
    assertTrue( garden.isWetGrass() );
    FactHandle fh = ksession.insert( garden );
    FactHandle fh1 = ksession.insert( "rule1" );
    ksession.fireAllRules();
    assertTrue(instance.isDecided());
    instance.globalUpdate(); // rule1 has added evidence, update the bayes network
    garden = instance.marginalize();
    assertTrue(garden.isWetGrass());  // grass was wet before rule1 and continues to be wet
    FactHandle fh2 = ksession.insert( "rule2" ); // applies 2 logical insertions
    ksession.fireAllRules();
    assertTrue(instance.isDecided());
    instance.globalUpdate();
    garden = instance.marginalize();
    assertFalse(garden.isWetGrass() );  // new evidence means grass is no longer wet
    FactHandle fh3 = ksession.insert( "rule3" ); // adds an additional support for the sprinkler, belief set of 2
    ksession.fireAllRules();
    assertTrue(instance.isDecided());
    instance.globalUpdate();
    garden = instance.marginalize();
    assertFalse(garden.isWetGrass() ); // nothing has changed
    FactHandle fh4 = ksession.insert( "rule4" ); // rule4 introduces a conflict, and the BayesFact becomes undecided
    ksession.fireAllRules();
    assertFalse(instance.isDecided());
    try {
    instance.globalUpdate();
    fail( "The BayesFact is undecided, it should throw an exception, as it cannot be updated." );
    } catch ( Exception e ) {
    // this should fail
    }
    ksession.delete( fh4 ); // the conflict is resolved, so it should be decided again
    ksession.fireAllRules();
    assertTrue(instance.isDecided());
    instance.globalUpdate();
    garden = instance.marginalize();
    assertFalse(garden.isWetGrass() );// back to grass is not wet
    ksession.delete( fh2 ); // takes the sprinkler belief set back to 1
    ksession.fireAllRules();
    instance.globalUpdate();
    garden = instance.marginalize();
    assertFalse(garden.isWetGrass() ); // still grass is not wet
    ksession.delete( fh3 ); // no sprinkler support now
    ksession.fireAllRules();
    instance.globalUpdate();
    garden = instance.marginalize();
    assertTrue(garden.isWetGrass()); // grass is wet again
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fdrools-bayesian-belief-network-integration-part-4.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%204> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fdrools-bayesian-belief-network-integration-part-4.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%204> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fdrools-bayesian-belief-network-integration-part-4.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%204> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fdrools-bayesian-belief-network-integration-part-4.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%204> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fdrools-bayesian-belief-network-integration-part-4.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%204> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fdrools-bayesian-belief-network-integration-part-4.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%204> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fdrools-bayesian-belief-network-integration-part-4.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%204> "Email")
  *[]: 2010-05-25T16:11:00+02:00