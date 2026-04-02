---
layout: post
title: "Drools - Bayesian Belief Network Integration Part 2"
date: 2014-04-08
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/04/drools-bayesian-belief-network-integration-part-2.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools – Bayesian Belief Network Integration Part 2](<https://blog.kie.org/2014/04/drools-bayesian-belief-network-integration-part-2.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- April 8, 2014  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

A while back I mentioned I was working on Bayesian Belief Network integration, and I outlined the work I was doing around Junction Tree building, and ensuring we had good unit testing.  
<http://blog.athico.com/2014/02/drools-bayesian-belief-network.html>

Today I finally got everything working end to end, including the the addition of hard evidence. The next stage is to integrate this into our [Pluggable Belief System](<http://blog.athico.com/2013/09/pluggable-belief-systems-in-drools-60.html>). One of the things we hope to do is use Defeasible style superiority rules as a way to resolving conflicting evidence.

For those interested, here is the fruits of my labours, showing end to end unit testing of the Eathquake example, as covered [here](<http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.135.7921&rep=rep1&type=pdf>).

[![](/legacy/assets/images/2014/04/b8125bfe34f2-eathquake.png)](<http://3.bp.blogspot.com/-99wV62AIUgw/U0NCR_XothI/AAAAAAAABJI/m-ZSjVaALkI/s3200/eathquake.png>)
[code]
    Graph&amp;lt;BayesVariable&amp;gt; graph = new BayesNetwork();
    GraphNode&amp;lt;BayesVariable&amp;gt; burglaryNode    = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; earthquakeNode = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; alarmNode      = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; johnCallsNode  = graph.addNode();
    GraphNode&amp;lt;BayesVariable&amp;gt; maryCallsNode  = graph.addNode();
    BayesVariable burglary    = new BayesVariable&amp;lt;String&amp;gt;("Burglary", burglaryNode.getId(), new String[]{"true", "false"}, new double[][]{{0.001, 0.999}});
    BayesVariable earthquake = new BayesVariable&amp;lt;String&amp;gt;("Earthquake", earthquakeNode.getId(), new String[]{"true", "false"}, new double[][]{{0.002, 0.998}});
    BayesVariable alarm      = new BayesVariable&amp;lt;String&amp;gt;("Alarm", alarmNode.getId(), new String[]{"true", "false"}, new double[][]{{0.95, 0.05}, {0.94, 0.06}, {0.29, 0.71}, {0.001, 0.999}});
    BayesVariable johnCalls  = new BayesVariable&amp;lt;String&amp;gt;("JohnCalls", johnCallsNode.getId(), new String[]{"true", "false"}, new double[][]{{0.90, 0.1}, {0.05, 0.95}});
    BayesVariable maryCalls  = new BayesVariable&amp;lt;String&amp;gt;("MaryCalls", maryCallsNode.getId(), new String[]{"true", "false"}, new double[][]{{0.7, 0.3}, {0.01, 0.99}});
    JunctionTree jTree;
    @Before
    public void setUp() {
        connectParentToChildren( burglaryNode, alarmNode);
        connectParentToChildren( earthquakeNode, alarmNode);
        connectParentToChildren( alarmNode, johnCallsNode, maryCallsNode);
        burglaryNode.setContent(burglary);
        earthquakeNode.setContent(earthquake);
        alarmNode.setContent( alarm );
        johnCallsNode.setContent( johnCalls );
        maryCallsNode.setContent( maryCalls );
        JunctionTreeBuilder jtBuilder = new JunctionTreeBuilder( graph );
        jTree = jtBuilder.build();
        jTree.initialize();
    }
    @Test
    public void testInitialize() {
        JunctionTreeNode jtNode = jTree.getRoot();
        // johnCalls
        assertArray(new double[]{0.90, 0.1, 0.05, 0.95}, scaleDouble( 3, jtNode.getPotentials() ));
    
        // burglary, earthquake, alarm
        jtNode = jTree.getRoot().getChildren().get(0).getChild();
        assertArray( new double[]{0.0000019, 0.0000001, 0.0009381, 0.0000599, 0.0005794, 0.0014186, 0.0009970, 0.9960050 },
                     scaleDouble( 7, jtNode.getPotentials() ));
        // maryCalls
        jtNode = jTree.getRoot().getChildren().get(1).getChild();
        assertArray( new double[]{ 0.7, 0.3, 0.01, 0.99 }, scaleDouble( 3, jtNode.getPotentials() ));
    }
    @Test
    public void testNoEvidence() {
        NetworkUpdateEngine nue = new NetworkUpdateEngine(graph, jTree);
        nue.globalUpdate();
        JunctionTreeNode jtNode = jTree.getRoot();
        marginalize(johnCalls, jtNode);
        assertArray( new double[]{0.052139, 0.947861},  scaleDouble( 6, johnCalls.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(0).getChild();
        marginalize(burglary, jtNode);
        assertArray( new double[]{0.001, 0.999},  scaleDouble( 3, burglary.getDistribution() ) );
        marginalize(earthquake, jtNode);
        assertArray( new double[]{ 0.002, 0.998},  scaleDouble( 3, earthquake.getDistribution() ) );
        marginalize(alarm, jtNode);
        assertArray( new double[]{0.002516, 0.997484},  scaleDouble( 6, alarm.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(1).getChild();
        marginalize(maryCalls, jtNode);
        assertArray( new double[]{0.011736, 0.988264 },  scaleDouble( 6, maryCalls.getDistribution() ) );
    }
    @Test
    public void testAlarmEvidence() {
        NetworkUpdateEngine nue = new NetworkUpdateEngine(graph, jTree);
        JunctionTreeNode jtNode = jTree.getJunctionTreeNodes( )[alarm.getFamily()];
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode,  alarmNode, new double[] { 1.0, 0.0 }) );
        nue.globalUpdate();
        jtNode = jTree.getRoot();
        marginalize(johnCalls, jtNode);
        assertArray( new double[]{0.9, 0.1},  scaleDouble( 6, johnCalls.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(0).getChild();
        marginalize(burglary, jtNode);
        assertArray( new double[]{.374, 0.626},  scaleDouble( 3, burglary.getDistribution() ) );
        marginalize(earthquake, jtNode);
        assertArray( new double[]{ 0.231, 0.769},  scaleDouble( 3, earthquake.getDistribution() ) );
        marginalize(alarm, jtNode);
        assertArray( new double[]{1.0, 0.0},  scaleDouble( 6, alarm.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(1).getChild();
        marginalize(maryCalls, jtNode);
        assertArray( new double[]{0.7, 0.3 },  scaleDouble( 6, maryCalls.getDistribution() ) );
    }
    @Test
    public void testEathQuakeEvidence() {
        NetworkUpdateEngine nue = new NetworkUpdateEngine(graph, jTree);
        JunctionTreeNode jtNode = jTree.getJunctionTreeNodes( )[earthquake.getFamily()];
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode,  earthquakeNode, new double[] { 1.0, 0.0 }) );
        nue.globalUpdate();
        jtNode = jTree.getRoot();
        marginalize(johnCalls, jtNode);
        assertArray( new double[]{0.297, 0.703},  scaleDouble( 3, johnCalls.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(0).getChild();
        marginalize(burglary, jtNode);
        assertArray( new double[]{.001, 0.999},  scaleDouble( 3, burglary.getDistribution() ) );
        marginalize(earthquake, jtNode);
        assertArray( new double[]{ 1.0, 0.0},  scaleDouble( 3, earthquake.getDistribution() ) );
        marginalize(alarm, jtNode);
        assertArray( new double[]{0.291, 0.709},  scaleDouble( 3, alarm.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(1).getChild();
        marginalize(maryCalls, jtNode);
        assertArray( new double[]{0.211, 0.789 },  scaleDouble( 3, maryCalls.getDistribution() ) );
    }
    @Test
    public void testJoinCallsEvidence() {
        NetworkUpdateEngine nue = new NetworkUpdateEngine(graph, jTree);
        JunctionTreeNode jtNode = jTree.getJunctionTreeNodes( )[johnCalls.getFamily()];
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode,  johnCallsNode, new double[] { 1.0, 0.0 }) );
        nue.globalUpdate();
        jtNode = jTree.getRoot();
        marginalize(johnCalls, jtNode);
        assertArray( new double[]{1.0, 0.0},  scaleDouble( 2, johnCalls.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(0).getChild();
        marginalize(burglary, jtNode);
        assertArray( new double[]{0.016, 0.984},  scaleDouble( 3, burglary.getDistribution() ) );
        marginalize(earthquake, jtNode);
        assertArray( new double[]{ 0.011, 0.989},  scaleDouble( 3, earthquake.getDistribution() ) );
        marginalize(alarm, jtNode);
        assertArray( new double[]{0.043, 0.957},  scaleDouble( 3, alarm.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(1).getChild();
        marginalize(maryCalls, jtNode);
        assertArray( new double[]{0.04, 0.96 },  scaleDouble( 3, maryCalls.getDistribution() ) );
    }
    @Test
    public void testEathquakeAndJohnCallsEvidence() {
        JunctionTreeBuilder jtBuilder = new JunctionTreeBuilder( graph );
        JunctionTree jTree = jtBuilder.build();
        jTree.initialize();
        NetworkUpdateEngine nue = new NetworkUpdateEngine(graph, jTree);
        JunctionTreeNode jtNode = jTree.getJunctionTreeNodes( )[johnCalls.getFamily()];
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode,  johnCallsNode, new double[] { 1.0, 0.0 }) );
        jtNode = jTree.getJunctionTreeNodes( )[earthquake.getFamily()];
        nue.setLikelyhood( new BayesLikelyhood( graph, jtNode,  earthquakeNode, new double[] { 1.0, 0.0 }) );
        nue.globalUpdate();
        jtNode = jTree.getRoot();
        marginalize(johnCalls, jtNode);
        assertArray( new double[]{1.0, 0.0},  scaleDouble( 2, johnCalls.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(0).getChild();
        marginalize(burglary, jtNode);
        assertArray( new double[]{0.003, 0.997},  scaleDouble( 3, burglary.getDistribution() ) );
        marginalize(earthquake, jtNode);
        assertArray( new double[]{ 1.0, 0.0},  scaleDouble( 3, earthquake.getDistribution() ) );
        marginalize(alarm, jtNode);
        assertArray( new double[]{0.881, 0.119},  scaleDouble( 3, alarm.getDistribution() ) );
        jtNode = jTree.getRoot().getChildren().get(1).getChild();
        marginalize(maryCalls, jtNode);
        assertArray( new double[]{0.618, 0.382 },  scaleDouble( 3, maryCalls.getDistribution() ) );
    }
    
[/code]
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F04%2Fdrools-bayesian-belief-network-integration-part-2.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%202> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F04%2Fdrools-bayesian-belief-network-integration-part-2.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%202> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F04%2Fdrools-bayesian-belief-network-integration-part-2.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%202> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F04%2Fdrools-bayesian-belief-network-integration-part-2.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%202> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F04%2Fdrools-bayesian-belief-network-integration-part-2.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%202> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F04%2Fdrools-bayesian-belief-network-integration-part-2.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%202> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F04%2Fdrools-bayesian-belief-network-integration-part-2.html&linkname=Drools%20%E2%80%93%20Bayesian%20Belief%20Network%20Integration%20Part%202> "Email")
  *[]: 2010-05-25T16:11:00+02:00