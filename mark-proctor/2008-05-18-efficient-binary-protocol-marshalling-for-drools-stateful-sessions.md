---
layout: post
title: "Efficient Binary Protocol Marshalling for Drools Stateful Sessions"
date: 2008-05-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/05/efficient-binary-protocol-marshalling-for-drools-stateful-sessions.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Efficient Binary Protocol Marshalling for Drools Stateful Sessions](<https://blog.kie.org/2008/05/efficient-binary-protocol-marshalling-for-drools-stateful-sessions.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 18, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

New code has been added, in trunk for a highly efficient binary protocol marshalling for stateful sessions. While Drools 4 supported standard serialisation of Working Memories, it used the default serialisation, this is both very slow and memory bloating. It also has the problem that it just serialises the user objects with it.

The new marshalling implementation allows for a strategy approach when handling the marshalling of user objects. You register different strategies for different name spaces. Currently we have two strategies, Serialised and Identity. Serialised just writes the user object to the stream via standard readObject/writeObject methods. Identity assigns the user object an id, from an int counter, and places it in a map and writes the id to the stream. Reading in uses that map to lookup the user object. Identity strategy is thus stateful, the write method can only be called once but read can be called repeatedly. Other strategies will be added, such as hibernate place holder support. Users can of course write there own.

So what does this give?

  * Session pause/resume, ideal for moving a session to a new server or restarting an existing server.
  * General snap shotting, backup. You could do a poor man’s high availability by snap shotting the session at the end of each transaction. Later we will be extending this binary protocol to support journalling and also replication via clustering.
  * Pre-loaded session templates. If you repeatedly create stateful sessions with the same base set of data and the insertion time is annoying, now you can just populate the session once and write out to a byte[] and use that as a template for further session creations.
  * Long term persistence, needed for our process integration work.

You can see the [MarshallingTest ](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-compiler/src/test/java/org/drools/integrationtests/MarshallingTest.java?r=HEAD>)to look at the integration tests in place at the moment.

In integrationtests’ [SerializationHelper ](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-compiler/src/test/java/org/drools/integrationtests/SerializationHelper.java?r=HEAD>)you can see the helper methods there demonstrating how it all works.

The [DefaultMarshalling ](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-core/src/main/java/org/drools/marshalling/DefaultMarshaller.java?r=HEAD>)class uses the Identity strategy if it is not passed a strategy factory. The Identity strategy is used throughout the tests.

The read/write marshalling is maintained in two files [InputMarshaller ](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-core/src/main/java/org/drools/marshalling/InputMarshaller.java?r=HEAD>)and [OutputMarshaller](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-core/src/main/java/org/drools/marshalling/OutputMarshaller.java?r=HEAD>), this will allow better handling of backwards compatiblity in the future.

It’s still very alphaware, but please do start trying it. I need to tidy up the debug output and will do that soon, I’ll probably make each read/write method take a String which will be written to the log when debug is on. It currently sorts a number of map/set data structures, this is for debugging so that testing can round trip for data loss, I will make sure that it can be disabled for production. The following types don’t yet marshall, not sure how to handle date/time stuff at the moment:  
Temporal Sessions do not marshall  
Scheduled rules, duration attribution do not marhsall

Implementations have not been added for accumulate, collect, from and rightinputadapter.

We are just hooking up the process marshalling into this at the moment.

Mark

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F05%2Fefficient-binary-protocol-marshalling-for-drools-stateful-sessions.html&linkname=Efficient%20Binary%20Protocol%20Marshalling%20for%20Drools%20Stateful%20Sessions> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F05%2Fefficient-binary-protocol-marshalling-for-drools-stateful-sessions.html&linkname=Efficient%20Binary%20Protocol%20Marshalling%20for%20Drools%20Stateful%20Sessions> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F05%2Fefficient-binary-protocol-marshalling-for-drools-stateful-sessions.html&linkname=Efficient%20Binary%20Protocol%20Marshalling%20for%20Drools%20Stateful%20Sessions> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F05%2Fefficient-binary-protocol-marshalling-for-drools-stateful-sessions.html&linkname=Efficient%20Binary%20Protocol%20Marshalling%20for%20Drools%20Stateful%20Sessions> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F05%2Fefficient-binary-protocol-marshalling-for-drools-stateful-sessions.html&linkname=Efficient%20Binary%20Protocol%20Marshalling%20for%20Drools%20Stateful%20Sessions> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F05%2Fefficient-binary-protocol-marshalling-for-drools-stateful-sessions.html&linkname=Efficient%20Binary%20Protocol%20Marshalling%20for%20Drools%20Stateful%20Sessions> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F05%2Fefficient-binary-protocol-marshalling-for-drools-stateful-sessions.html&linkname=Efficient%20Binary%20Protocol%20Marshalling%20for%20Drools%20Stateful%20Sessions> "Email")