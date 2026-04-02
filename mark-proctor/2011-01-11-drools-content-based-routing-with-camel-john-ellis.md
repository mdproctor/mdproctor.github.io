---
layout: post
title: "Drools Content Based Routing with Camel (John Ellis)"
date: 2011-01-11
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/01/drools-content-based-routing-with-camel-john-ellis.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Content Based Routing with Camel (John Ellis)](<https://blog.kie.org/2011/01/drools-content-based-routing-with-camel-john-ellis.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 11, 2011  
[General](<https://blog.kie.org/category/general>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

John Ellis has done a nice writeup of his work on improving Drools to work with Camel for CBR. You’ll need to use the latest version of Drools from trunk, which can be found in the maven repository that’s 5.2.0-SNAPSHOT, <https://repository.jboss.org/nexus/content/groups/public/org/drools/>.

For bonus points I’d love to see a further Drools and Camel tutorial around OSGi’s EventAdmin, <http://camel.apache.org/eventadmin.html>.

— (John Ellis) —  
One of Camel’s greatest strengths is the explicit support for [Enterprise Integration Patterns](<http://www.eaipatterns.com/toc.html>). Drools itself is particularly well suited to work alongside Camel to implement two commonly used integration patterns: the Content Based Router and the Dynamic Router. Both patterns leverage the ability of a Drools Endpoint to rapidly evaluate properties of a message, while the Dynamic Router can also integrate the Drools Policy as a dynamic rule based on feedback from a control channel.

The Camel routes required for message routing do not differ much from the previous Drools Endpoint example. You may even be able to omit the Drools Policy if you wish to inspect only the headers of messages being routed instead of interrogating the body of each message. For example, a DRL could be defined that takes action on inbound messages such as:
[code]
    import org.apache.camel.Message;  
    rule "WriteOperations"  
    when  
     $message : Message(headers["OPERATION"] == "WRITE");  
    then  
     $message.setHeader("routingSlip", "activemq:queue:op.write");  
    end  
      
    rule "ReadOperations"  
    when  
     $message : Message(headers["OPERATION"] == "READ");  
    then  
     $message.setHeader("routingSlip", "activemq:queue:op.read");  
    end
[/code]

Example 1: DRL for Routing Based on Message Headers

Here the custom header “OPERATION” is evaluated to see if it is set to the value “WRITE” or “READ.” Depending on the value of this header, a routing slip is defined for the message. The Routing Slip is another Enterprise Integration Pattern supported by Camel that may contain one or more URIs. The message is then sequentially sent to each URI defined.

The Camel routing itself is simply defined as:
[code]
    <route>  
     <from uri="activemq:queue:router"/>  
     <to uri="drools:brokerNode/cbrKSession?action=insertMessage"/>  
     <routingSlip uriDelimiter="#">  
         <header>routingSlip</header>  
     </routingSlip>  
    </route>
[/code]

Example 2: Camel Routes for Content Based Routing

Here we explicitly inform Camel that routing slips are defined as values within the “routingSlip” header and each URI is delimited by a # character. The headers set within the DRL are then interpreted as each message exits the Drools endpoint.

Content based routing with a Drools Endpoint offers several advantages over Camel’s default implementation. The DRL format itself allows routing to be specified more succinctly than Sprint DSLs or Camel RouteBuilders. Conditional operations are also evaluated more efficiently within Drools and are thread-safe, allowing a high volume of messages to be routed concurrently.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Fdrools-content-based-routing-with-camel-john-ellis.html&linkname=Drools%20Content%20Based%20Routing%20with%20Camel%20%28John%20Ellis%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Fdrools-content-based-routing-with-camel-john-ellis.html&linkname=Drools%20Content%20Based%20Routing%20with%20Camel%20%28John%20Ellis%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Fdrools-content-based-routing-with-camel-john-ellis.html&linkname=Drools%20Content%20Based%20Routing%20with%20Camel%20%28John%20Ellis%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Fdrools-content-based-routing-with-camel-john-ellis.html&linkname=Drools%20Content%20Based%20Routing%20with%20Camel%20%28John%20Ellis%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Fdrools-content-based-routing-with-camel-john-ellis.html&linkname=Drools%20Content%20Based%20Routing%20with%20Camel%20%28John%20Ellis%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Fdrools-content-based-routing-with-camel-john-ellis.html&linkname=Drools%20Content%20Based%20Routing%20with%20Camel%20%28John%20Ellis%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Fdrools-content-based-routing-with-camel-john-ellis.html&linkname=Drools%20Content%20Based%20Routing%20with%20Camel%20%28John%20Ellis%29> "Email")
  *[]: 2010-05-25T16:11:00+02:00