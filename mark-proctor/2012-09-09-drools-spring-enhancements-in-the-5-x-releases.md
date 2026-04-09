---
layout: post
title: "Drools Spring Enhancements in the 5.x releases"
date: 2012-09-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/09/drools-spring-enhancements-in-the-5-x-releases.html
---

Version 5.3 of Drools introduced the ability to declare Knowledge Listeners via the Spring XML. You could declare 3 types of listeners to be added to the _KnowledgeSessions – AgendaListener,_ _WorkingMemoryListener, ProcessEventListener_.

The drools-spring module allowed configuration of these listeners to KnowledgeSessions using XML tags. These tags have identical names as the actual listener interfaces i.e., _< drools:agendaEventListener….>, _< drools:workingMemoryEventListener….>_ and <drools:processEventListener….>_.

<http://docs.jboss.org/drools/release/5.3.0.Final/droolsjbpm-integration-docs/html/ch02.html#d0e509>

The upcoming 5.5.0.Beta1 would include the following enhancements to the drools-spring module

**Support declarative configuration for knowledge runtime loggers (console, file, threaded-file)**  
With this addition, all the requisite loggers can be defined declaratively and attached to the Knowledge Sessions. All the logger types supported by Drools Expert can be configured via XML.

```
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
```

You can find more information on the options and the corresponding Java Code here: <https://github.com/droolsjbpm/droolsjbpm-integration/blob/master/drools-container/drools-spring/src/test/resources/org/drools/container/spring/loggers.xml>  
<https://github.com/droolsjbpm/droolsjbpm-integration/blob/master/drools-container/drools-spring/src/test/java/org/drools/container/spring/SpringDroolsLoggersTest.java>

**Defining an environment (org.drools.runtime.Environment)**

```
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
```

You can find more information on the configuration options and the corresponding Java Code here: <https://github.com/droolsjbpm/droolsjbpm-integration/blob/master/drools-container/drools-spring/src/test/resources/org/drools/container/spring/environment.xml>