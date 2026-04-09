---
layout: post
title: "Drools Content Based Routing with Camel (John Ellis)"
date: 2011-01-11
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/01/drools-content-based-routing-with-camel-john-ellis.html
---

John Ellis has done a nice writeup of his work on improving Drools to work with Camel for CBR. You’ll need to use the latest version of Drools from trunk, which can be found in the maven repository that’s 5.2.0-SNAPSHOT, <https://repository.jboss.org/nexus/content/groups/public/org/drools/>.

For bonus points I’d love to see a further Drools and Camel tutorial around OSGi’s EventAdmin, <http://camel.apache.org/eventadmin.html>.

— (John Ellis) —  
One of Camel’s greatest strengths is the explicit support for [Enterprise Integration Patterns](<http://www.eaipatterns.com/toc.html>). Drools itself is particularly well suited to work alongside Camel to implement two commonly used integration patterns: the Content Based Router and the Dynamic Router. Both patterns leverage the ability of a Drools Endpoint to rapidly evaluate properties of a message, while the Dynamic Router can also integrate the Drools Policy as a dynamic rule based on feedback from a control channel.

The Camel routes required for message routing do not differ much from the previous Drools Endpoint example. You may even be able to omit the Drools Policy if you wish to inspect only the headers of messages being routed instead of interrogating the body of each message. For example, a DRL could be defined that takes action on inbound messages such as:

```drl
import org.apache.camel.Message;
rule "WriteOperations"
when
$message : Message(headers["OPERATION"] == "WRITE");
then
$message.setHeader("routingSlip", "activemq:queue:op.write");endrule "ReadOperations"
when
$message : Message(headers["OPERATION"] == "READ");
then
$message.setHeader("routingSlip", "activemq:queue:op.read");
end
```

Example 1: DRL for Routing Based on Message Headers

Here the custom header “OPERATION” is evaluated to see if it is set to the value “WRITE” or “READ.” Depending on the value of this header, a routing slip is defined for the message. The Routing Slip is another Enterprise Integration Pattern supported by Camel that may contain one or more URIs. The message is then sequentially sent to each URI defined.

The Camel routing itself is simply defined as:

```xml
<route>
   
  <from uri="activemq:queue:router"/>
   
  <to uri="drools:brokerNode/cbrKSession?action=insertMessage"/>
   
  <routingSlip uriDelimiter="#">
         
    <header>routingSlip</header>
     
  </routingSlip>
</route>
```

Example 2: Camel Routes for Content Based Routing

Here we explicitly inform Camel that routing slips are defined as values within the “routingSlip” header and each URI is delimited by a # character. The headers set within the DRL are then interpreted as each message exits the Drools endpoint.

Content based routing with a Drools Endpoint offers several advantages over Camel’s default implementation. The DRL format itself allows routing to be specified more succinctly than Sprint DSLs or Camel RouteBuilders. Conditional operations are also evaluated more efficiently within Drools and are thread-safe, allowing a high volume of messages to be routed concurrently.