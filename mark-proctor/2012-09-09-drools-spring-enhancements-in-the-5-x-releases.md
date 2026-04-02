---
layout: post
title: "Drools Spring Enhancements in the 5.x releases"
date: 2012-09-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/09/drools-spring-enhancements-in-the-5-x-releases.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Spring Enhancements in the 5.x releases](<https://blog.kie.org/2012/09/drools-spring-enhancements-in-the-5-x-releases.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 9, 2012  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Version 5.3 of Drools introduced the ability to declare Knowledge Listeners via the Spring XML. You could declare 3 types of listeners to be added to the _KnowledgeSessions – AgendaListener,_ _WorkingMemoryListener, ProcessEventListener_.

The drools-spring module allowed configuration of these listeners to KnowledgeSessions using XML tags. These tags have identical names as the actual listener interfaces i.e., _< drools:agendaEventListener….>, _< drools:workingMemoryEventListener….>_ and <drools:processEventListener….>_.

<http://docs.jboss.org/drools/release/5.3.0.Final/droolsjbpm-integration-docs/html/ch02.html#d0e509>

The upcoming 5.5.0.Beta1 would include the following enhancements to the drools-spring module

**Support declarative configuration for knowledge runtime loggers (console, file, threaded-file)**  
With this addition, all the requisite loggers can be defined declaratively and attached to the Knowledge Sessions. All the logger types supported by Drools Expert can be configured via XML.
[code]
       <drools:ksession id="…" type="…" kbase="…">  
            <drools:consoleLogger/>  
     …  
        </drools:ksession>  
      
        <drools:ksession id="…" type="…" kbase="…">  
            <drools:fileLogger id="…" file="[path]"/>  
        </drools:ksession>  
      
        <drools:ksession id="…" type="…" kbase="…">  
            <drools:fileLogger id="…" file="[path]" threaded="true" interval="5"/>  
        </drools:ksession>  
    
[/code]

You can find more information on the options and the corresponding Java Code here: <https://github.com/droolsjbpm/droolsjbpm-integration/blob/master/drools-container/drools-spring/src/test/resources/org/drools/container/spring/loggers.xml>  
<https://github.com/droolsjbpm/droolsjbpm-integration/blob/master/drools-container/drools-spring/src/test/java/org/drools/container/spring/SpringDroolsLoggersTest.java>

**Defining an environment (org.drools.runtime.Environment)**
[code]
     <drools:environment id="drools-env">  
        <drools:entity-manager-factory ref="myEmf"/>  
        <drools:transaction-manager ref="txManager"/>  
        <drools:globals ref="my-globals"/>  
        <drools:date-formats ref="my-date-formats"/>  
        <drools:calendars ref="my-calendars"/>  
      
        <drools:object-marshalling-strategies>  
          <drools:serializable-placeholder-resolver-strategy strategy-acceptor-ref=".."/>  
          <drools:identity-placeholder-resolver-strategy strategy-acceptor-ref=".."/>  
          <drools:jpa-placeholder-resolver-strategy env-ref=".." />  
          <drools:process-instance-resolver-strategy/>  
        </drools:object-marshalling-strategies>  
      
       <!--  
            <drools:scoped-entity-manager scope="app" >  
            </drools:scoped-entity-manager>  
        -->  
    
[/code]

You can find more information on the configuration options and the corresponding Java Code here: <https://github.com/droolsjbpm/droolsjbpm-integration/blob/master/drools-container/drools-spring/src/test/resources/org/drools/container/spring/environment.xml>

<https://github.com/droolsjbpm/droolsjbpm-integration/blob/master/drools-container/drools-spring/src/test/java/org/drools/container/spring/EnvironmentTest.java>  
**  
****Author**  
Vinod Kiran  
BRMS Practice Lead with [ValueMomentum Software Services Pvt. Ltd](<http://www.valuemomentum.com/>)  
<http://www.linkedin.com/in/vinodkiran>

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fdrools-spring-enhancements-in-the-5-x-releases.html&linkname=Drools%20Spring%20Enhancements%20in%20the%205.x%20releases> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fdrools-spring-enhancements-in-the-5-x-releases.html&linkname=Drools%20Spring%20Enhancements%20in%20the%205.x%20releases> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fdrools-spring-enhancements-in-the-5-x-releases.html&linkname=Drools%20Spring%20Enhancements%20in%20the%205.x%20releases> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fdrools-spring-enhancements-in-the-5-x-releases.html&linkname=Drools%20Spring%20Enhancements%20in%20the%205.x%20releases> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fdrools-spring-enhancements-in-the-5-x-releases.html&linkname=Drools%20Spring%20Enhancements%20in%20the%205.x%20releases> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fdrools-spring-enhancements-in-the-5-x-releases.html&linkname=Drools%20Spring%20Enhancements%20in%20the%205.x%20releases> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fdrools-spring-enhancements-in-the-5-x-releases.html&linkname=Drools%20Spring%20Enhancements%20in%20the%205.x%20releases> "Email")
  *[]: 2010-05-25T16:11:00+02:00