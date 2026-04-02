---
layout: post
title: "Drools - Bayesian Belief Network Integration Part 3"
date: 2014-05-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/05/drools-bayesian-belief-network-integration-part-3.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools – Bayesian Belief Network Integration Part 3](<https://blog.kie.org/2014/05/drools-bayesian-belief-network-integration-part-3.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 7, 2014  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

This follows my earlier [Part 2](<http://blog.athico.com/2014/04/drools-bayesian-belief-network.html>) posting in April,

Things now work end to end, and I have a clean separation from the Creation of the JunctionTree and initialisation of all state, and the state that change after evidence insertion. This separation ensures that multiple instances of the same bayesian network can be created cheaply.

I’m now working on integrating this into the belief system. One issue I have is that I can automate the update of the bayesian network as soon as the evidence changes. The reason for this is updating of the network is expensive, if you insert three pieces of evidence, you only want it to update one not three times. So for now I will add a dirty check, and allow users to call update. For best practice I will recommend people separate reasoning of the results of bayesian and entering new evidence, so that it becomes clearer when it’s efficient to call update.

For now I’m only dealing with hard evidence. We will be using superiority rules to resolve conflict evidence for a variable. Any unresolved conflicts will leave a variable marked as “Undecided”. Handling of soft or virtual evidence would be nice, this would add way to resolve conflicted evidence statistically; but for now this is out of scope. There is a paper [here](<http://www.csee.umbc.edu/~ypeng/Publications/2006/ICTAI06-RongPan.pdf>) on who to do it, if anyone wants to help me :)

I’ll be committing this to github in a few days, for now if anyone is interested, [here](<https://www.dropbox.com/s/rwb11rue1y4l06x/drools-beliefs.zip>) is the jar in a zip form from dropbox.

–update–  
The XMLBIF parser provided by Horacio Antar is now integrated and tested. I’m just working on refactoring Drools for pluggable knowledge types, to fully integrate Bayesian as a new type of knowledge.
[code]
    Graph&amp;lt;BayesVariable&amp;gt; graph = new BayesNetwork();
    GraphNode&amp;lt;BayesVariable&amp;gt; burglaryNode   = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; earthquakeNode = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; alarmNode      = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; johnCallsNode  = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; maryCallsNode  = graph.addNode();
    BayesVariable burglary   = new BayesVariable&amp;lt;String&amp;gt;("Burglary", burglaryNode.getId(), new String[]{"true", "false"}, new double[][]{{0.001, 0.999}});
    BayesVariable earthquake = new BayesVariable&amp;lt;String&amp;gt;("Earthquake", earthquakeNode.getId(), new String[]{"true", "false"}, new double[][]{{0.002, 0.998}});
    BayesVariable alarm      = new BayesVariable&amp;lt;String&amp;gt;("Alarm", alarmNode.getId(), new String[]{"true", "false"}, new double[][]{{0.95, 0.05}, {0.94, 0.06}, {0.29, 0.71}, {0.001, 0.999}});
    BayesVariable johnCalls  = new BayesVariable&amp;lt;String&amp;gt;("JohnCalls", johnCallsNode.getId(), new String[]{"true", "false"}, new double[][]{{0.90, 0.1}, {0.05, 0.95}});
    BayesVariable maryCalls  = new BayesVariable&amp;lt;String&amp;gt;("MaryCalls", maryCallsNode.getId(), new String[]{"true", "false"}, new double[][]{{0.7, 0.3}, {0.01, 0.99}});
    BayesVariableState burglaryState;
    BayesVariableState earthquakeState;
    BayesVariableState alarmState;
    BayesVariableState johnCallsState;
    BayesVariableState maryCallsState;
    JunctionTreeNode jtNode1;
    JunctionTreeNode jtNode2;
    JunctionTreeNode jtNode3;
    JunctionTree jTree;
    BayesEngine engine;
    @Before
    public void setUp() {
        connectParentToChildren(burglaryNode, alarmNode);
        connectParentToChildren(earthquakeNode, alarmNode);
        connectParentToChildren(alarmNode, johnCallsNode, maryCallsNode);
        burglaryNode.setContent(burglary);
        earthquakeNode.setContent(earthquake);
        alarmNode.setContent(alarm);
        johnCallsNode.setContent(johnCalls);
        maryCallsNode.setContent(maryCalls);
        JunctionTreeBuilder jtBuilder = new JunctionTreeBuilder(graph);
        jTree = jtBuilder.build();
        jTree.initialize();
        jtNode1 = jTree.getRoot();
        jtNode2 = jtNode1.getChildren().get(0).getChild();
        jtNode3 = jtNode1.getChildren().get(1).getChild();
        engine = new BayesEngine(jTree);
        burglaryState = engine.getVarStates()[burglary.getId()];
        earthquakeState = engine.getVarStates()[earthquake.getId()];
        alarmState = engine.getVarStates()[alarm.getId()];
        johnCallsState = engine.getVarStates()[johnCalls.getId()];
        maryCallsState = engine.getVarStates()[maryCalls.getId()];
    }
    @Test
    public void testInitialize() {
        // johnCalls
        assertArray(new double[]{0.90, 0.1, 0.05, 0.95}, scaleDouble( 3, jtNode1.getPotentials() ));
    
        // maryCalls
        assertArray( new double[]{ 0.7, 0.3, 0.01, 0.99 }, scaleDouble( 3, jtNode2.getPotentials() ));
        // burglary, earthquake, alarm
        assertArray( new double[]{0.0000019, 0.0000001, 0.0009381, 0.0000599, 0.0005794, 0.0014186, 0.0009970, 0.9960050 },
                     scaleDouble( 7, jtNode3.getPotentials() ));
    }
    @Test
    public void testNoEvidence() {
        engine.globalUpdate();
        assertArray( new double[]{0.052139, 0.947861},  scaleDouble(6, engine.marginalize("JohnCalls").getDistribution()) );
        assertArray( new double[]{0.011736, 0.988264 },  scaleDouble( 6, engine.marginalize("MaryCalls").getDistribution() ) );
        assertArray( new double[]{0.001, 0.999},  scaleDouble(3, engine.marginalize("Burglary").getDistribution()) );
        assertArray( new double[]{ 0.002, 0.998},  scaleDouble( 3, engine.marginalize("Earthquake").getDistribution() ) );
        assertArray( new double[]{0.002516, 0.997484},   scaleDouble(6, engine.marginalize("Alarm").getDistribution()) );
    }
    @Test
    public void testAlarmEvidence() {
        BayesEngine nue = new BayesEngine(jTree);
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode3,  alarmNode, new double[] { 1.0, 0.0 }) );
        nue.globalUpdate();
        assertArray( new double[]{0.9, 0.1}, scaleDouble( 6, nue.marginalize("JohnCalls").getDistribution() ) );
        assertArray( new double[]{0.7, 0.3 }, scaleDouble( 6, nue.marginalize("MaryCalls").getDistribution() ) );
        assertArray( new double[]{0.374, 0.626}, scaleDouble( 3, nue.marginalize("Burglary").getDistribution() ) );
        assertArray( new double[]{ 0.231, 0.769}, scaleDouble( 3, nue.marginalize("Earthquake").getDistribution() ) );
        assertArray( new double[]{1.0, 0.0}, scaleDouble( 6, nue.marginalize("Alarm").getDistribution() ) ); }
    @Test
    public void testEathQuakeEvidence() {
        BayesEngine nue = new BayesEngine(jTree);
        nue.setLikelyhood(new BayesLikelyhood(graph, jtNode3, earthquakeNode, new double[]{1.0, 0.0}));
        nue.globalUpdate();
        assertArray( new double[]{0.297, 0.703}, scaleDouble( 6, nue.marginalize("JohnCalls").getDistribution() ) );
        assertArray( new double[]{0.211, 0.789 }, scaleDouble( 6, nue.marginalize("MaryCalls").getDistribution() ) );
        assertArray( new double[]{.001, 0.999}, scaleDouble( 3, nue.marginalize("Burglary").getDistribution() ) );
        assertArray( new double[]{1.0, 0.0}, scaleDouble( 3, nue.marginalize("Earthquake").getDistribution() ) );
        assertArray( new double[]{0.291, 0.709}, scaleDouble( 6, nue.marginalize("Alarm").getDistribution() ) );
    }
    @Test
    public void testJoinCallsEvidence() {
        BayesEngine nue = new BayesEngine(jTree);
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode1,  johnCallsNode, new double[] { 1.0, 0.0 }) );
        nue.globalUpdate();
        assertArray( new double[]{1.0, 0.0}, scaleDouble( 6, nue.marginalize("JohnCalls").getDistribution() ) );
        assertArray( new double[]{0.04, 0.96 }, scaleDouble( 6, nue.marginalize("MaryCalls").getDistribution() ) );
        assertArray( new double[]{0.016, 0.984}, scaleDouble( 3, nue.marginalize("Burglary").getDistribution() ) );
        assertArray( new double[]{0.011, 0.989}, scaleDouble( 3, nue.marginalize("Earthquake").getDistribution() ) );
        assertArray( new double[]{0.043, 0.957}, scaleDouble( 6, nue.marginalize("Alarm").getDistribution() ) );
    }
    @Test
    public void testEarthquakeAndJohnCallsEvidence() {
        BayesEngine nue = new BayesEngine(jTree);
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode1,  johnCallsNode, new double[] { 1.0, 0.0 }) );
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode3,  earthquakeNode, new double[] { 1.0, 0.0 }) );
        nue.globalUpdate();
        assertArray( new double[]{1.0, 0.0}, scaleDouble( 6, nue.marginalize("JohnCalls").getDistribution() ) );
        assertArray( new double[]{0.618, 0.382 }, scaleDouble( 6, nue.marginalize("MaryCalls").getDistribution() ) );
        assertArray( new double[]{0.003, 0.997}, scaleDouble( 3, nue.marginalize("Burglary").getDistribution() ) );
        assertArray( new double[]{ 1.0, 0.0}, scaleDouble( 3, nue.marginalize("Earthquake").getDistribution() ) );
        assertArray( new double[]{0.881, 0.119}, scaleDouble( 6, nue.marginalize("Alarm").getDistribution() ) );
    }
    
[/code]
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F05%2Fdrools-bayesian-belief-network-integration-part-3.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%203> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F05%2Fdrools-bayesian-belief-network-integration-part-3.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%203> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F05%2Fdrools-bayesian-belief-network-integration-part-3.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%203> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F05%2Fdrools-bayesian-belief-network-integration-part-3.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%203> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F05%2Fdrools-bayesian-belief-network-integration-part-3.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%203> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F05%2Fdrools-bayesian-belief-network-integration-part-3.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%203> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F05%2Fdrools-bayesian-belief-network-integration-part-3.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%203> "Email")
  *[]: 2010-05-25T16:11:00+02:00