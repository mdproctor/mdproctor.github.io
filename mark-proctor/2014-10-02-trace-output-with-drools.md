---
layout: post
title: "Trace output with Drools"
date: 2014-10-02
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/10/trace-output-with-drools.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Trace output with Drools](<https://blog.kie.org/2014/10/trace-output-with-drools.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- October 2, 2014  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Drools 6 includes a trace output that can help get an idea of what is going on in your system, and how often things are getting executed, and with how much data.

It can also help to understand that Drools 6 is now a goal based algorithm, using a linking mechanism to link in rules for evaluation. More details on that here:  
<http://blog.athico.com/2013/11/rip-rete-time-to-get-phreaky.html>

The first thing to do is set your slf4j logger to trace mode:
[code]
    <appender name="consoleAppender" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
          <!-- %l lowers performance -->
          <!--<pattern>%d [%t] %-5p %l%n  %m%n</pattern>-->
          <pattern>%d [%t] %-5p %m%n</pattern>
        </encoder>
      </appender>
      <logger name="org.drools" level="trace"/>
      <root level="info"><!-- TODO We probably want to set default level to warn instead -->
        <appender-ref ref="consoleAppender" />
      </root>
    </configuration>
[/code]

Let’s take the shopping example, you can find the Java and Drl files for this here:  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/shopping/Shopping.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/java/org/drools/examples/shopping/ShoppingExample.java>

Running the example will give output a very detailed and long log of execution. Initially you’ll see objects being inserted, which causes linking. Linking of nodes and rules is explained in the Drools 6 algorithm link. In summary 1..n nodes link in a segment, when object are are inserted.
[code]
    2014-10-02 02:35:09,009 [main] TRACE Insert [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac]
    2014-10-02 02:35:09,020 [main] TRACE LinkNode notify=false nmask=1 smask=1 spos=0 rules=
[/code]

Then 1..n segments link in a rule. When a Rule is linked in it’s schedule on the agenda for evaluation.
[code]
    2014-10-02 02:35:09,043 [main] TRACE  LinkRule name=Discount removed notification
    2014-10-02 02:35:09,043 [main] TRACE Queue RuleAgendaItem [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,043 [main] TRACE Queue Added 1 [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    
[/code]

When it eventually evaluates a rule it will indent as it visits each node, as it evaluate from root to tip. Each node will attempt to tell you how much data is being inserted, updated or deleted at that point.
[code]
    2014-10-02 02:35:09,046 [main] TRACE Rule[name=Apply 10% discount if total purchases is over 100] segments=2 TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,047 [main] TRACE      1 [ AccumulateNode(12) ] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,047 [main] TRACE      Segment 1
    2014-10-02 02:35:09,047 [main] TRACE      1 [ AccumulateNode(12) ] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,047 [main] TRACE      rightTuples TupleSets[insertSize=2, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,056 [main] TRACE        2 [RuleTerminalNode(13): rule=Apply 10% discount if total purchases is over 100] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
[/code]

You can use this information to see how often rules evaluate, how much linking and unlinking happens, how much data propagates and more important how much wasted work is done. Here is the full log:
[code]
    2014-10-02 02:35:08,889 [main] DEBUG Starting Engine in PHREAK mode
    2014-10-02 02:35:08,927 [main] TRACE Adding Rule Purchase notification
    2014-10-02 02:35:08,929 [main] TRACE Adding Rule Discount removed notification
    2014-10-02 02:35:08,931 [main] TRACE Adding Rule Discount awarded notification
    2014-10-02 02:35:08,933 [main] TRACE Adding Rule Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,009 [main] TRACE Insert [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac]
    2014-10-02 02:35:09,020 [main] TRACE LinkNode notify=false nmask=1 smask=1 spos=0 rules=
    2014-10-02 02:35:09,020 [main] TRACE   LinkSegment smask=2 rmask=2 name=Discount removed notification
    2014-10-02 02:35:09,025 [main] TRACE   LinkSegment smask=2 rmask=2 name=Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,028 [main] TRACE LinkNode notify=true nmask=1 smask=1 spos=0 rules=[RuleMem Purchase notification], [RuleMem Discount removed notification], [RuleMem Discount awarded notification], [RuleMem Apply 10% discount if total purchases is over 100]
    2014-10-02 02:35:09,028 [main] TRACE   LinkSegment smask=1 rmask=1 name=Purchase notification
    2014-10-02 02:35:09,028 [main] TRACE   LinkSegment smask=1 rmask=3 name=Discount removed notification
    2014-10-02 02:35:09,043 [main] TRACE  LinkRule name=Discount removed notification
    2014-10-02 02:35:09,043 [main] TRACE Queue RuleAgendaItem [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,043 [main] TRACE Queue Added 1 [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,043 [main] TRACE   LinkSegment smask=1 rmask=1 name=Discount awarded notification
    2014-10-02 02:35:09,043 [main] TRACE   LinkSegment smask=1 rmask=3 name=Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,043 [main] TRACE  LinkRule name=Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,043 [main] TRACE Queue RuleAgendaItem [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
    2014-10-02 02:35:09,043 [main] TRACE Queue Added 2 [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
    2014-10-02 02:35:09,043 [main] TRACE Added Apply 10% discount if total purchases is over 100 to eager evaluation list.
    2014-10-02 02:35:09,044 [main] TRACE Insert [fact 0:2:14633842:14633842:2:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Product@df4b72]
    2014-10-02 02:35:09,044 [main] TRACE Insert [fact 0:3:732189840:732189840:3:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Product@2ba45490]
    2014-10-02 02:35:09,044 [main] TRACE Insert [fact 0:4:939475028:939475028:4:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Purchase@37ff4054]
    2014-10-02 02:35:09,045 [main] TRACE BetaNode insert=1 stagedInsertWasEmpty=true
    2014-10-02 02:35:09,045 [main] TRACE LinkNode notify=true nmask=1 smask=1 spos=1 rules=[RuleMem Purchase notification]
    2014-10-02 02:35:09,045 [main] TRACE   LinkSegment smask=2 rmask=3 name=Purchase notification
    2014-10-02 02:35:09,045 [main] TRACE  LinkRule name=Purchase notification
    2014-10-02 02:35:09,046 [main] TRACE Queue RuleAgendaItem [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,046 [main] TRACE Queue Added 1 [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,046 [main] TRACE BetaNode insert=1 stagedInsertWasEmpty=true
    2014-10-02 02:35:09,046 [main] TRACE LinkNode notify=true nmask=1 smask=1 spos=1 rules=[RuleMem Apply 10% discount if total purchases is over 100]
    2014-10-02 02:35:09,046 [main] TRACE   LinkSegment smask=2 rmask=3 name=Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,046 [main] TRACE  LinkRule name=Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,046 [main] TRACE Added Apply 10% discount if total purchases is over 100 to eager evaluation list.
    2014-10-02 02:35:09,046 [main] TRACE Insert [fact 0:5:8996952:8996952:5:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Purchase@894858]
    2014-10-02 02:35:09,046 [main] TRACE BetaNode insert=2 stagedInsertWasEmpty=false
    2014-10-02 02:35:09,046 [main] TRACE BetaNode insert=2 stagedInsertWasEmpty=false
    2014-10-02 02:35:09,046 [main] TRACE Rule[name=Apply 10% discount if total purchases is over 100] segments=2 TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,047 [main] TRACE      1 [ AccumulateNode(12) ] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,047 [main] TRACE      Segment 1
    2014-10-02 02:35:09,047 [main] TRACE      1 [ AccumulateNode(12) ] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,047 [main] TRACE      rightTuples TupleSets[insertSize=2, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,056 [main] TRACE        2 [RuleTerminalNode(13): rule=Apply 10% discount if total purchases is over 100] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,057 [main] TRACE        Segment 1
    2014-10-02 02:35:09,057 [main] TRACE        2 [RuleTerminalNode(13): rule=Apply 10% discount if total purchases is over 100] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,057 [main] TRACE Rule[name=Apply 10% discount if total purchases is over 100] segments=2 TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,057 [main] TRACE      3 [ AccumulateNode(12) ] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,057 [main] TRACE Rule[name=Purchase notification] segments=2 TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,057 [main] TRACE      4 [JoinNode(5) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Purchase]] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,057 [main] TRACE      Segment 1
    2014-10-02 02:35:09,057 [main] TRACE      4 [JoinNode(5) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Purchase]] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,058 [main] TRACE      rightTuples TupleSets[insertSize=2, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,058 [main] TRACE        5 [RuleTerminalNode(6): rule=Purchase notification] TupleSets[insertSize=2, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,058 [main] TRACE        Segment 1
    2014-10-02 02:35:09,058 [main] TRACE        5 [RuleTerminalNode(6): rule=Purchase notification] TupleSets[insertSize=2, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,058 [main] TRACE Fire "Purchase notification" 
    [[ Purchase notification active=false ] [ [fact 0:4:939475028:939475028:4:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Purchase@37ff4054]
    [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac] ] ]
    Customer mark just purchased shoes
    2014-10-02 02:35:09,060 [main] TRACE Fire "Purchase notification" 
    [[ Purchase notification active=false ] [ [fact 0:5:8996952:8996952:5:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Purchase@894858]
    [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac] ] ]
    Customer mark just purchased hat
    2014-10-02 02:35:09,061 [main] TRACE Removing RuleAgendaItem [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,061 [main] TRACE Queue Removed 1 [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,061 [main] TRACE Rule[name=Discount removed notification] segments=2 TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,061 [main] TRACE      6 [NotNode(8) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,061 [main] TRACE      Segment 1
    2014-10-02 02:35:09,061 [main] TRACE      6 [NotNode(8) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,061 [main] TRACE      rightTuples TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,061 [main] TRACE        7 [RuleTerminalNode(9): rule=Discount removed notification] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,061 [main] TRACE        Segment 1
    2014-10-02 02:35:09,061 [main] TRACE        7 [RuleTerminalNode(9): rule=Discount removed notification] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,061 [main] TRACE Fire "Discount removed notification" 
    [[ Discount removed notification active=false ] [ null
    [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac] ] ]
    Customer mark now has a discount of 0
    2014-10-02 02:35:09,063 [main] TRACE Removing RuleAgendaItem [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,063 [main] TRACE Queue Removed 1 [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,063 [main] TRACE Fire "Apply 10% discount if total purchases is over 100" 
    [[ Apply 10% discount if total purchases is over 100 active=false ] [ [fact 0:6:2063009760:1079902208:6:null:NON_TRAIT:120.0]
    [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac] ] ]
    2014-10-02 02:35:09,071 [main] TRACE Insert [fact 0:7:874153561:874153561:7:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Discount@341a8659]
    2014-10-02 02:35:09,071 [main] TRACE   LinkSegment smask=2 rmask=3 name=Discount removed notification
    2014-10-02 02:35:09,071 [main] TRACE  LinkRule name=Discount removed notification
    2014-10-02 02:35:09,071 [main] TRACE Queue RuleAgendaItem [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,071 [main] TRACE Queue Added 1 [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,071 [main] TRACE BetaNode insert=1 stagedInsertWasEmpty=true
    2014-10-02 02:35:09,071 [main] TRACE LinkNode notify=true nmask=1 smask=1 spos=1 rules=[RuleMem Discount awarded notification]
    2014-10-02 02:35:09,071 [main] TRACE   LinkSegment smask=2 rmask=3 name=Discount awarded notification
    2014-10-02 02:35:09,071 [main] TRACE  LinkRule name=Discount awarded notification
    2014-10-02 02:35:09,071 [main] TRACE Queue RuleAgendaItem [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    2014-10-02 02:35:09,071 [main] TRACE Queue Added 3 [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    Customer mark now has a shopping total of 120.0
    2014-10-02 02:35:09,071 [main] TRACE Removing RuleAgendaItem [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
    2014-10-02 02:35:09,071 [main] TRACE Queue Removed 2 [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
    2014-10-02 02:35:09,071 [main] TRACE Rule[name=Discount removed notification] segments=2 TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,072 [main] TRACE      8 [NotNode(8) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,072 [main] TRACE      Segment 1
    2014-10-02 02:35:09,072 [main] TRACE      8 [NotNode(8) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,072 [main] TRACE      rightTuples TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,073 [main] TRACE        9 [RuleTerminalNode(9): rule=Discount removed notification] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,073 [main] TRACE        Segment 1
    2014-10-02 02:35:09,073 [main] TRACE        9 [RuleTerminalNode(9): rule=Discount removed notification] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,073 [main] TRACE Removing RuleAgendaItem [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,073 [main] TRACE Queue Removed 1 [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,073 [main] TRACE Rule[name=Discount awarded notification] segments=2 TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,073 [main] TRACE      10 [JoinNode(10) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,073 [main] TRACE      Segment 1
    2014-10-02 02:35:09,073 [main] TRACE      10 [JoinNode(10) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,074 [main] TRACE      rightTuples TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,074 [main] TRACE        11 [RuleTerminalNode(11): rule=Discount awarded notification] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,074 [main] TRACE        Segment 1
    2014-10-02 02:35:09,074 [main] TRACE        11 [RuleTerminalNode(11): rule=Discount awarded notification] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,074 [main] TRACE Fire "Discount awarded notification" 
    [[ Discount awarded notification active=false ] [ [fact 0:7:874153561:874153561:7:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Discount@341a8659]
    [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac] ] ]
    Customer mark now has a discount of 10
    2014-10-02 02:35:09,074 [main] TRACE Removing RuleAgendaItem [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    2014-10-02 02:35:09,074 [main] TRACE Queue Removed 1 [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    2014-10-02 02:35:09,074 [main] TRACE Delete [fact 0:5:8996952:8996952:5:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Purchase@894858]
    2014-10-02 02:35:09,074 [main] TRACE   LinkSegment smask=2 rmask=3 name=Purchase notification
    2014-10-02 02:35:09,074 [main] TRACE  LinkRule name=Purchase notification
    2014-10-02 02:35:09,074 [main] TRACE Queue RuleAgendaItem [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,074 [main] TRACE Queue Added 1 [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,075 [main] TRACE   LinkSegment smask=2 rmask=3 name=Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,075 [main] TRACE  LinkRule name=Apply 10% discount if total purchases is over 100
    2014-10-02 02:35:09,075 [main] TRACE Queue RuleAgendaItem [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
    2014-10-02 02:35:09,075 [main] TRACE Queue Added 2 [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
    2014-10-02 02:35:09,075 [main] TRACE Added Apply 10% discount if total purchases is over 100 to eager evaluation list.
    Customer mark has returned the hat
    2014-10-02 02:35:09,075 [main] TRACE Rule[name=Apply 10% discount if total purchases is over 100] segments=2 TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,075 [main] TRACE      12 [ AccumulateNode(12) ] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,075 [main] TRACE      Segment 1
    2014-10-02 02:35:09,075 [main] TRACE      12 [ AccumulateNode(12) ] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,075 [main] TRACE      rightTuples TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,075 [main] TRACE        13 [RuleTerminalNode(13): rule=Apply 10% discount if total purchases is over 100] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,075 [main] TRACE        Segment 1
    2014-10-02 02:35:09,075 [main] TRACE        13 [RuleTerminalNode(13): rule=Apply 10% discount if total purchases is over 100] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,075 [main] TRACE Delete [fact 0:7:874153561:874153561:7:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Discount@341a8659]
    2014-10-02 02:35:09,075 [main] TRACE   LinkSegment smask=2 rmask=3 name=Discount removed notification
    2014-10-02 02:35:09,075 [main] TRACE  LinkRule name=Discount removed notification
    2014-10-02 02:35:09,075 [main] TRACE Queue RuleAgendaItem [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,075 [main] TRACE Queue Added 3 [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,075 [main] TRACE UnlinkNode notify=true nmask=1 smask=0 spos=1 rules=[RuleMem Discount awarded notification]
    2014-10-02 02:35:09,076 [main] TRACE   UnlinkSegment smask=2 rmask=1 name=[RuleMem Discount awarded notification]
    2014-10-02 02:35:09,076 [main] TRACE     UnlinkRule name=Discount awarded notification
    2014-10-02 02:35:09,076 [main] TRACE Queue RuleAgendaItem [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    2014-10-02 02:35:09,076 [main] TRACE Queue Added 2 [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    2014-10-02 02:35:09,076 [main] TRACE Rule[name=Purchase notification] segments=2 TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE      14 [JoinNode(5) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Purchase]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE      Segment 1
    2014-10-02 02:35:09,076 [main] TRACE      14 [JoinNode(5) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Purchase]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE      rightTuples TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE        15 [RuleTerminalNode(6): rule=Purchase notification] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE        Segment 1
    2014-10-02 02:35:09,076 [main] TRACE        15 [RuleTerminalNode(6): rule=Purchase notification] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE Removing RuleAgendaItem [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,076 [main] TRACE Queue Removed 1 [Activation rule=Purchase notification, act#=2, salience=10, tuple=null]
    2014-10-02 02:35:09,076 [main] TRACE Rule[name=Discount removed notification] segments=2 TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE      16 [NotNode(8) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE      Segment 1
    2014-10-02 02:35:09,076 [main] TRACE      16 [NotNode(8) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,076 [main] TRACE      rightTuples TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE        17 [RuleTerminalNode(9): rule=Discount removed notification] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE        Segment 1
    2014-10-02 02:35:09,077 [main] TRACE        17 [RuleTerminalNode(9): rule=Discount removed notification] TupleSets[insertSize=1, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE Fire "Discount removed notification" 
    [[ Discount removed notification active=false ] [ null
    [fact 0:1:1455177644:1455177644:1:DEFAULT:NON_TRAIT:org.drools.examples.shopping.ShoppingExample$Customer@56bc3fac] ] ]
    Customer mark now has a discount of 0
    2014-10-02 02:35:09,077 [main] TRACE Removing RuleAgendaItem [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,077 [main] TRACE Queue Removed 1 [Activation rule=Discount removed notification, act#=0, salience=0, tuple=null]
    2014-10-02 02:35:09,077 [main] TRACE Rule[name=Discount awarded notification] segments=2 TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE      18 [JoinNode(10) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE      Segment 1
    2014-10-02 02:35:09,077 [main] TRACE      18 [JoinNode(10) - [ClassObjectType class=org.drools.examples.shopping.ShoppingExample$Discount]] TupleSets[insertSize=0, deleteSize=0, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE      rightTuples TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE        19 [RuleTerminalNode(11): rule=Discount awarded notification] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE        Segment 1
    2014-10-02 02:35:09,077 [main] TRACE        19 [RuleTerminalNode(11): rule=Discount awarded notification] TupleSets[insertSize=0, deleteSize=1, updateSize=0]
    2014-10-02 02:35:09,077 [main] TRACE Removing RuleAgendaItem [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    2014-10-02 02:35:09,077 [main] TRACE Queue Removed 1 [Activation rule=Discount awarded notification, act#=7, salience=0, tuple=null]
    2014-10-02 02:35:09,077 [main] TRACE Removing RuleAgendaItem [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
    2014-10-02 02:35:09,077 [main] TRACE Queue Removed 1 [Activation rule=Apply 10% discount if total purchases is over 100, act#=1, salience=0, tuple=null]
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F10%2Ftrace-output-with-drools.html&linkname=Trace%20output%20with%20Drools> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F10%2Ftrace-output-with-drools.html&linkname=Trace%20output%20with%20Drools> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F10%2Ftrace-output-with-drools.html&linkname=Trace%20output%20with%20Drools> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F10%2Ftrace-output-with-drools.html&linkname=Trace%20output%20with%20Drools> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F10%2Ftrace-output-with-drools.html&linkname=Trace%20output%20with%20Drools> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F10%2Ftrace-output-with-drools.html&linkname=Trace%20output%20with%20Drools> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F10%2Ftrace-output-with-drools.html&linkname=Trace%20output%20with%20Drools> "Email")
  *[]: 2010-05-25T16:11:00+02:00