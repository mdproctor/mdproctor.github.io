---
layout: post
title: "Drools - Bayesian Belief Network Integration"
date: 2014-02-03
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/02/drools-bayesian-belief-network-integration.html
---

### Drools – Bayesian Belief Network Integration

I’ve been working on the next stages for the [pluggable belief system](<http://blog.athico.com/2013/09/pluggable-belief-systems-in-drools-60.html>), integration of a bayesian network sub system. I wanted to ensure I really understood what was going on, so I have been writing my own implementation.

I’ve been working through this excellent tutorial:  
<http://www.mathcs.emory.edu/~whalen/Papers/BNs/Intros/BayesianNetworksTutorial.pdf>

And this tutorial too:  
[http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.135.7921&rep=rep1&type=pdf](<http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.135.7921&rep=rep1&type=pdf>)

I now have a fairly efficient algorithm that can produce optimal [junction trees](<http://en.wikipedia.org/wiki/Tree_decomposition>), from a given graph. It first moralises and then triangulates before producing the final junction tree. The junction tree algorithm transforms a graph into a tree, so that the network propagations at runtime are no longer NP -hard.

I’ve written a lot of low level unit tests, for all the small working parts – as I really want to be sure I’m building something solid, and it’s not enough to simply test the final transformation results. To get an idea of how it looks, I’ve created unit tests for the examples in the two tutorials above. Notice it uses BitSets to encode cliques, for efficiency. Only the first main bayesian network is represented as a graph of objects, after that all transformation work is done via an adjacency matrix – which keeps it light and fast.

Horacio has been working on a UI for bayesian networks. It’s early stages yet, but it can parse the bayesian XMLBIF standard and display the nodes. Next he’ll be adding the connectors and then we’ll start the work on making it editable. You can see a video here:  
<http://vimeo.com/85732009>

Next I’m going to work on the message propagation. I’m hoping to have this fully integrated and usable in the pluggable belief system, in 4 to 6 weeks. I’ll blog my progress.

**Example 1**

[![](/legacy/assets/images/2014/02/a9143443600b-junctiontree1.png)](</assets/images/2014/02/cb9a779ee683-junctiontree1.png>)

```java
@Test
public void testFullExample1() {
    // from "Bayesian Belief Network Propagation Engine In Java"
    // the result here is slightly different, due to ordering, but it's still correct.
    // http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.135.7921&amp;amp;amp;rep=rep1&amp;amp;amp;type=pdf
    Graph&amp;amp;lt;BayesVariable&amp;amp;gt; graph = new GraphImpl&amp;amp;lt;BayesVariable&amp;amp;gt;();
    Vertex xa = addVertex( graph );
    Vertex xb = addVertex( graph );
    Vertex xc = addVertex( graph );
    Vertex xd = addVertex( graph );
    Vertex xe = addVertex( graph );
    Vertex xf = addVertex( graph );
    Vertex xg = addVertex( graph );
    Vertex xh = addVertex( graph );
    connectParentToChildren(xa, xb, xc);
    connectParentToChildren(xb, xd);
    connectParentToChildren(xc, xe, xg);
    connectParentToChildren(xd, xf);
    connectParentToChildren(xe, xf, xh);
    connectParentToChildren(xg, xh);

    BitSet clique1 = bitSet("00000111"); // a, b, c
    BitSet clique2 = bitSet("00001110"); // b, c, d
    BitSet clique3 = bitSet("00011100"); // c, d, e
    BitSet clique4 = bitSet("01010100"); // c, e, g
    BitSet clique5 = bitSet("11010000"); // e, g, h
    BitSet clique6 = bitSet("00111000"); // d, e, f

    BitSet clique1And2 = bitSet("00000110"); // b, c
    BitSet clique2And3 = bitSet("00001100"); // c, d
    BitSet clique3And4 = bitSet("00010100"); // c, e
    BitSet clique4And5 = bitSet("01010000"); // e, g
    BitSet clique3And6 = bitSet("00011000"); // d, e
    // clique1
    JunctionTreeBuilder jtBuilder = new JunctionTreeBuilder( graph );
    JunctionTreeNode&amp;amp;lt;BayesVariable&amp;amp;gt; root = jtBuilder.build();
    assertEquals( clique1, root.getBitSet() );

    // clique2
    assertEquals(1, root.getSeparators().size());
    JunctionTreeSeparator sep =  root.getSeparators().get(0);
    assertEquals( clique1And2, sep.getBitSet() );
    JunctionTreeNode&amp;amp;lt;BayesVariable&amp;amp;gt; jtNode2 =sep.getNode2();
    assertEquals( clique1, sep.getNode1().getBitSet() );
    assertEquals( clique2, jtNode2.getBitSet() );
    assertEquals(2, jtNode2.getSeparators().size());
    // clique3
    assertSame( sep, jtNode2.getSeparators().get(0));
    sep =  jtNode2.getSeparators().get(1);
    assertEquals( clique2And3, sep.getBitSet() );
    JunctionTreeNode&amp;amp;lt;BayesVariable&amp;amp;gt;  jtNode3 =sep.getNode2();
    assertEquals( clique2, sep.getNode1().getBitSet() );
    assertEquals( clique3, jtNode3.getBitSet() );
    assertEquals( 3, jtNode3.getSeparators().size());
    // clique4
    assertSame( sep, jtNode3.getSeparators().get(0));
    sep =  jtNode3.getSeparators().get(1);
    assertEquals( clique3And4, sep.getBitSet() );
    JunctionTreeNode&amp;amp;lt;BayesVariable&amp;amp;gt; jtNode4 = sep.getNode1();
    assertEquals( clique3, sep.getNode2().getBitSet() );
    assertEquals( clique4, jtNode4.getBitSet() );
    assertEquals( 2, jtNode4.getSeparators().size());
    // clique5
    assertSame( sep, jtNode4.getSeparators().get(0));
    sep =  jtNode4.getSeparators().get(1);
    assertEquals( clique4And5, sep.getBitSet() );
    JunctionTreeNode&amp;amp;lt;BayesVariable&amp;amp;gt; jtNode5 = sep.getNode1();
    assertEquals( clique4, sep.getNode2().getBitSet() );
    assertEquals( clique5, jtNode5.getBitSet() );
    assertEquals( 1, jtNode5.getSeparators().size());
    //clique 6
    sep =  jtNode3.getSeparators().get(2);
    assertEquals( clique3And6, sep.getBitSet() );
    JunctionTreeNode&amp;amp;lt;BayesVariable&amp;amp;gt; jtNode6 = sep.getNode1();
    assertEquals( clique3, sep.getNode2().getBitSet() );
    assertEquals( clique6, jtNode6.getBitSet() );
    assertEquals( 1, jtNode6.getSeparators().size());
}
Example 2
@Test
public void testFullExample2() {
    // Bayesian Networks -  A Self-contained introduction with implementation remarks
    // http://www.mathcs.emory.edu/~whalen/Papers/BNs/Intros/BayesianNetworksTutorial.pdf
    Graph&amp;lt;BayesVariable&amp;gt; graph = new GraphImpl&amp;lt;BayesVariable&amp;gt;();
    Vertex xElectricity = addVertex( graph );   // 0
    Vertex xTelecom = addVertex( graph );       // 1
    Vertex xRail = addVertex( graph );          // 2
    Vertex xAirTravel = addVertex( graph );     // 3
    Vertex xTransportation = addVertex( graph );// 4
    Vertex xUtilities = addVertex( graph );     // 5
    Vertex xUSBanks = addVertex( graph );       // 6
    Vertex xUSStocks = addVertex( graph );      // 7
    connectParentToChildren( xElectricity, xRail, xAirTravel, xUtilities, xTelecom );
    connectParentToChildren( xTelecom, xUtilities, xUSBanks );
    connectParentToChildren( xRail, xTransportation );
    connectParentToChildren( xAirTravel, xTransportation );
    connectParentToChildren( xUtilities, xUSStocks );
    connectParentToChildren( xUSBanks, xUSStocks );
    connectParentToChildren( xTransportation, xUSStocks );

    BitSet clique1 = bitSet("11110000"); // Utilities, Transportation, USBanks, UStocks
    BitSet clique2 = bitSet("01110001"); // Electricity, Transportation, Utilities, USBanks
    BitSet clique3 = bitSet("01100011"); // Electricity, Telecom, Utilities, USBanks
    BitSet clique4 = bitSet("00011101"); // Electricity, Rail, AirTravel, Transportation
    BitSet clique1And2 = bitSet("01110000"); // Utilities, Transportation, USBanks
    BitSet clique2And3 = bitSet("01100001"); // Electricity, Utilities, USBanks
    BitSet clique2And4 = bitSet("00010001"); // Electricity, Transportation

    xElectricity.setContent(new BayesVariable("Electricity", xElectricity.getId(),
                                              new Object[]{"Working", "Reduced", "NotWorking"}, new double[][]{{0.6, 0.3, 0.099}}));
    xTelecom.setContent(new BayesVariable("Telecom", xTelecom.getId(),
                                          new Object[]{"Working", "Reduced", "NotWorking"}, new double[][]{{0.544, 0.304, 0.151}}));
    xRail.setContent(new BayesVariable("Rail", xRail.getId(),
                                       new Object[]{"Working", "Reduced", "NotWorking"}, new double[][]{{0.579, 0.230, 0.190}}));
    xAirTravel.setContent(new BayesVariable("AirTravel", xAirTravel.getId(),
                                            new Object[]{"Working", "Reduced", "NotWorking"}, new double[][]{{0.449, 0.330, 0.219}}));
    xTransportation.setContent(new BayesVariable("Transportation", xTransportation.getId(),
                                                 new Object[]{"Working", "Moderate", "Severe", "Failure"}, new double[][]{{0.658, 0.167, 0.097, 0.077}}));
    xUtilities.setContent(new BayesVariable("Utilities", xUtilities.getId(),
                                             new Object[]{"Working", "Moderate", "Severe", "Failure"}, new double[][]{{0.541, 0.272, 0.097, 0.088}}));
    xUSBanks.setContent(new BayesVariable("USBanks", xUSBanks.getId(),
                                          new Object[]{"Working", "Reduced", "NotWorking"}, new double[][]{{0.488, 0.370, 0.141}}));
    xUSStocks.setContent(new BayesVariable("USStocks", xUSStocks.getId(),
                                          new Object[]{"Up", "Down", "Crash"}, new double[][]{{0.433, 0.386, 0.179}}));
    JunctionTreeBuilder jtBuilder = new JunctionTreeBuilder( graph );
    JunctionTreeNode&amp;lt;BayesVariable&amp;gt; root = jtBuilder.build();

    // clique1
    assertEquals( clique1, root.getBitSet() );
    assertEquals( 1, root.getSeparators().size() );
    // clique2
    JunctionTreeSeparator sep =  root.getSeparators().get(0);
    assertEquals( clique1And2, sep.getBitSet() );
    JunctionTreeNode&amp;lt;BayesVariable&amp;gt; jtNode2 = sep.getNode2();
    assertEquals( clique1, sep.getNode1().getBitSet() );
    assertEquals( clique2, jtNode2.getBitSet() );
    assertEquals(3, jtNode2.getSeparators().size());
    // clique3
    assertSame( sep, jtNode2.getSeparators().get(0) );
    sep =  jtNode2.getSeparators().get(1);
    assertEquals( clique2And3, sep.getBitSet() );
    JunctionTreeNode&amp;lt;BayesVariable&amp;gt; jtNode3 = sep.getNode1();
    assertEquals( clique2, sep.getNode2().getBitSet() );
    assertEquals( clique3, jtNode3.getBitSet() );
    assertEquals(1, jtNode3.getSeparators().size());
    // clique4
    sep =  jtNode2.getSeparators().get(2);
    assertEquals( clique2And4, sep.getBitSet() );
    JunctionTreeNode&amp;lt;BayesVariable&amp;gt; jtNode4 = sep.getNode1();
    assertEquals( clique2, sep.getNode2().getBitSet() );
    assertEquals( clique4, jtNode4.getBitSet() );
    assertEquals(1, jtNode4.getSeparators().size());
}
```