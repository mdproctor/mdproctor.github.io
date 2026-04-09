---
layout: post
title: "Complex Event Processing (CEP) - The industry that never should have happened (Part 2)"
date: 2009-11-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/11/complex-event-processing-cep-the-industry-that-never-should-have-happened-part-2.html
---

Part 2

Part 1 was a tongue in cheek look at the CEP industry with the hypothesis that “CEP is the industry that never should have happened”, with ILog being the market leader and CEP being just another rule engine feature, such as truth maintenance or rule flow. In part 2 I go deeper with a more technical discussion on how we extended Drools easily, cleanly and orthogonally for event processing, which allowed Drools to enter the CEP market.

Three years ago I was at BRF2006 and we had just released Drools 3.0. My experience and research then was still focused on the more classical rule engine features, as found in Clips from NASA. I met up with Charles Forgy, the father of Rete based rule engines, and he told me about his work in “Data Fusion” that he was doing for the military. He was building a system able to receive a million objects a second and reason over them for up to 5 seconds, thus a total of 5 million objects at any one time. Inspired by Charles and already aware of the ILog’s event management capabilities I decided to direct our research into extending Drools with CEP capabilities. When I first pitched “CEP” to management, back in 2006, the general response was “what’s that?”. At the time I wasn’t quite aware of how quickly the industry would grow and how perfect the timing was for “Drools Fusion” as part of Drools 5.

Another big motivation for myself is the concept of declaratives behavioural modelling, which I hope to make the subject for a later article. That is building a system that is able to more completely model your problem thinking at a behaviour level, rather than an imperative implementation level. Software systems are often far to isolated, you go to one vendor for your rules, another for your event processing and another for your workflow. These along with business semantics, more commonly known as ontologies, form the most important foundations for business software development at a behavioural level. The isolated vendor approach provides for minimal integration and the end user spends as much time writing glue code to bring them together, as they do solving their actual business problem; meaning that these technologies as a whole never reach their true potential. By recognising these technologies as the important foundations and treating each one as a first class citizen to provide a seamless and fully integrated environment we create a more holistic approach that is far richer than today’s isolated software. This is a major motivator for why we took the efforts to naturally extend both our engine and rule language, rather than building a dedicated engine and language, which would have been far simpler. While the problems of extending Drools and the Rete algorithm are hard, they are not insurmountable and we believe the results to be clearly worth this extra effort.

Introduction to Patterns  
Without going into too much detail on rules engine theory I thought it would help to just go over the very basics of Patterns, which form the heart of a rules engine, and filter insert objects. Applying these filters to the data is called Pattern Matching.

Production Rules systems use the concept of a Pattern to filter data:

```drl
$c : Customer( type == “VIP”)
```

This is a bit like saying in SQL:

```drl
select * from Customer where type == “VIP”
```

Although rule engine language’s have the added power of allowing variable references to both the Classes (tables) and the fields (columns). ‘$c’ is the variable binding, the ‘$’ is just a best practice that helps to visually differentiate it from normal field names. These patterns are chained together to create a filtration network, called a discrimination network, with the leaf node of each chain resulting in a set of actions to execute. What this means is that data is inserted into the running engine and propagated to the first filter in the chain, if the filter of the pattern is true, the data is propagated to the next filter in the chain, this process repeats until the leaf node is met and the actions are executed against that data.

In this example we have two patterns that are joined, using the variable binding ‘$c’:

```drl
$c : Customer( )
$boe : BuyOrderEvent( customer == $c )
```

In SQL this is the equivalent of:

```drl
select * from Customer c, BuyOrderEvent boe where boe.customer == c
```

As an example, it is easy to understand that while it might be possible to insert all the ZipCode’s of the USA into the working memory, it would not be feasible to insert all the Buses. Instead, the engine can call an external service that finds the buses for a given zipCode – note that none of the Buses are inserted into the Working Memory itself and the filtration is local to that Pattern:

```drl
$zipCode : ZipCode()
Bus( color == “red” ) from webService.findBuses( $zipCode )
```

Limitations of the Rete Algorithm  
Now into the meat of the problems that we faced, and how we solved them, as we we decided to look into how to extend Drools for CEP. Now that we have an understanding of the basics for Pattern Matching, it should provide enough foundations to understand the various limitations of traditional Rete based engines. We identified the following limitations when first starting our research:

  1. Single point of entry with synchronized access and single threaded execution
  2. Manual life-cycle management (time stamping and retraction) of events.
  3. No temporal reasoning.
  4. Checking for absence of events.
  5. No aggregation capabilities.
  6. No Sliding or Tumbling (batch) windows.
  7. No sophisticated clock management.

```drl
$c : Customer( type == “VIP” )
BuyOrderEvent( customer == $c )
```

However this means that we have a single point of entry, that is synchronized. If we have multiple streams, from say a JMS feeder, we can potentially end up with a bottleneck. Furthermore all patterns see all inserted objects. The solution is to allow the Working Memory to have named partitions, called entry points. Typically each stream will have it’s own partition and a thread pool is used to allow each partition to execute in parallel.

Patterns can then filter directly against those entry points. Joins across partitions, and thus across threads, are safely handled. Such as the join from the default Working Memory entry point and the “Home Broker Stream” entry point – both of which are executing in their own Thread:

```drl
$c : Customer( type == “VIP” )
BuyOrderEvent( customer == $c ) from entry-point “Home Broker Stream”
```

Notice the use of the ‘from’ keyword to indicate the source of the Pattern to be filtered, in this case an entry point stream.

Manual life-cycle management (time stamping and retraction) of events  
In rule engine’s all inserted objects, also referred to as facts, must be retracted when no longer needed, otherwise you face potentially running out of memory. Events, a special type of fact, are constantly being inserted, normally via a stream, so this can be very cumbersome; especially as often the application does not know when the event is no longer applicable.

To first allow the engine to assume responsibility for the events life cycle we must declare the fact role as an “event”. In this example we tell the engine that the StockTicker class, in our domain model, is an event:

```drl
declare StockTicker  @role( event )end
```

When the engine manages the life cycle for a class, all rules are analysed to determinewhen the event is no longer relevant and can be automatically disposed.

However it is possible to have the engine automatically detect when an event is no longer relevant, an explicit expiration policy can also be specified. The following case shows an example where the event expires one hour and thirty minutes after being created:

```drl
declare StockTicker
  @role( event )
  @expires( 1h30m )
end
```

It’s also essential that engines provide for flexible time stamping of the event. The time of the event could be specified at the point of insertion based on a central reasoning clock (called session clock), or or it could be specified by a field on the instance; among other possibilities. We can declare the field to be used with:

```drl
declare StockTicker
  @role( event )
  @expires( 1h30m )
  @timestamp( dateTimeStampField )
end
```

Events can also specify a duration, which is needed for operators such as overlaps, again this duration can be specified by a field on the event instance:

```drl
declare StockTicker
  @role( event )
  @expires( 1h30m )
  @timestamp( dateTimeStampField )
  @duration( durationField )
end
```

While all the above is used to declare information on an existing class in our classpath, it is also possible to specify the fields so the engine will generate a pojo that is local to the engine only. This allows for different engines to be loaded at the same time with different versions of a class.

```drl
declare StockTicker
  @role( event )
  @expires( 1h30m )
  @timestamp( dateTimeStampField )
  @duration( durationField )

  companySymbol : String
  stockPrice : double
  dateTimeStampField : Date
  durationField : long
end
```

No temporal reasoning  
Temporal operators allow for comparisons with the time information on an event. There are 13 temporal operators that allow all known situations to be modelled:coincides, before, after, meets, metby, overlaps, overlappedby, during, inludes, starts, startedby, finishes, finishedby.

The following chart provides a visualization for the relationship between some of these operators.

[![](/legacy/assets/images/2009/11/f7a62dc8de3d-operators.png)](</assets/images/2009/11/c073cd31343a-operators.png>)  
Usage of these operators is trival:

```drl
$c  : Custumer( type == “VIP” )
$oe : BuyOrderEvent( customer == $c )  from entry-point “Home Broker Stream”
 BuyAckEvent( relatedEvent == $oe.id,
              this after[1s, 10s] $oe ) from entry-point “Stock Trader Stream”
```

The above correlates two streams for a given customer making sure the BuyAckEvent is received between 1 second and 10 seconds after the time of BuyOrderEvent.

Checking for absence of events.  
While the example used to check that a BuyAckEvent occurs, its actually often more important to know when something doesn’t occur. In this case the functionality is provided by the already existing ‘not’ functionality:

```drl
$c  : Custumer( type == “VIP” )
$oe : BuyOrderEvent( customer == $c )  from entry-point “Home Broker Stream”
 not BuyAckEvent( relatedEvent == $oe.id,
                  this after[1s, 10s] $oe ) from entry-point “Stock Trader Stream”
```

No aggregation capabilities.  
Rule engines typically need to write multiple rules with staged areas to do aggregations, which isn’t very performant and loses it’s declarative benefits. Jess was the first mainstream engine to introduce a new keyword called ‘accumulate’, which we’ve adopted and improved on in Drools. ‘accumulate’ allows you to use our standard pattern matching language to select a set of objects and then to perform an aggregate calculation on them, returning a result. The result is returned from the accumulate and can be constrained against using another Pattern. The example below sums the takings for all the red buses and is true if the sum is greater than 100:

```drl
Number( intValue > 100 ) from
   accumulate( Bus( $takings : takings, color == “red” ),
               sum( $takings ) )
```

Drools provides a number of functions out of the box and users can easily add their own. Fedex have done some very interesting things with statistical and geo-spatial accumulate functions, as part of their situational awareness technology.

No Sliding or Tumbling (batch) windows.  
A key part of event stream processing is to be able to analyse streams of data over time. We can achieve this by combing the accumulate with an extension to Patterns we call Behaviours. Typically as soon as object enters a pattern to be filtered, if all the constraints are true the object is propagated to the next pattern. Behaviours allow us to alter this behaviour of the pattern, two Behaviours are currently supported; window:time and window:length. Others will be supported in the future such as distinct:

```drl
Number( intValue > 100 ) from
      accumulate( StockTicker( $price : price,
                               ticker == “RHT” ) over window:time( 1m30s ),
                  avg( $price ) )
```

There two main types of windows – sliding and tumbling, also sometimes known as batch. Drools currently provides a sliding window and tumbling windows are planned. Both approaches are useful and important to know when you need one or the other. A tumbling window says starting now, the start of our window, reason over the events for the next n seconds, at the end of n seconds we have reached the end of our window. At any time if our aggregation logic is true the result is propagated. This could be used to sample the average stock price every 250ms and if the price has changed since the last sample then propagate the results. A sliding window has no specific start, instead it’s parameters are continuously applied. For instance if we said if the average price of a stock falls below 10 for any 1 minute window then do something, there are obvious problems with the tumbling approach. If when I start the window and finish it the average price may not have fallen below our threshold, however should it have had started the window 15 seconds later it would have done. A sliding time window solves this, it analyses the stream for any 1 minute window when the average falls below 10, no matter when that window starts.

No sophisticated clock management.  
Reasoning over time requires a reference clock. Just to mention one example, if a rule reasons over the average price of a given stock over the last 60 minutes, how the engine knows what stock price changes happened over the last 60 minutes in order to calculate the average? The obvious response is: by comparing the timestamp of the events with the “current time”. How the engine knows what time is now? Just looking at the hardware system clock isn’t good enough. Instead we introduce the concept of a Session clock.

The session clock implements a strategy pattern, allowing different types of clocks to be plugged and used by the engine. This is very important because the engine may be running in an array of different scenarios that may require different clock implementations. Just to mention a few:

  * Rules testing: testing always requires a controlled environment, and when the tests include rules with temporal constraints, it is necessary to not only control the input rules and facts, but also the flow of time.
  * Regular execution: usually, when running rules in production, the application will require a real time clock that allows the rules engine to react immediately to the time progression.
  * Special environments: specific environments may have specific requirements on time control. Cluster environments may require clock synchronization through heart beats, or JEE environments may require the use of an AppServer provided clock, etc.
  * Internationalization: different engines running on the same JVM may need to run in different time zones.
  * Rules replay or simulation: to replay scenarios or simulate scenarios it is necessary that the application also controls the flow of time.

Drools supplies 2 clock implementations out of the box. The default real time clock, based on the system clock, and an optional pseudo clock, controlled by the application. Others will be introduced in the future. As drools is a unified architecture for rules, processes and event processing all these environments share the same session clock, and all have job scheduling/timers based on this session clock. This makes building simulation/testing tools across these domains trivial, and ensures at runtime that the three domains are running in sync. This is one of the many advantages gained by taking an integrated approach, as discussed at the start of this article.

Conclusion  
“ CEP is the industry that never should have happened” is our original hypothesis. If you first consider that ILog showed that CEP can be done on a Rete based rule engine over 10 years ago, way before the existence of a CEP market. Then look at the further extensions Drools has done to Rete to show that a rule engine can compete with dedicated CEP engines. I believe it shows there is no reason for two separate industries and separate engines and separate language. CEP statements are rules, they belong in the rule engine. Now imagine if ILog had done all these extensions and more over 10 years ago, as part of their existing engine, as just another rule engine feature. Things may have turned out differently. The features in Drools just touch on the necessary basics of what’s possible and needed in a CEP system, but it clearly shows a Rete based engine can be cleanly extended to support such logic. While the syntax we have chosen is a clean, natural and orthogonal extension to the existing rule language, if a Streaming SQL standard emerges Drools can and will support that.

There is however a huge amount of work to do both on features and performance and the far more interesting stuff is to come. Such as an Event Processing Network and being capable of dealing with composite events, causality and event sequencing. We also have some very interesting research in the pipeline on imperfect reasoning; which involves things like fuzzy logic, probability and Bayesian networks.