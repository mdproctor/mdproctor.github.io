---
layout: post
title: "Drools - OSGi Ready!"
date: 2010-01-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/01/drools-osgi-ready.html
---

### Drools – OSGi Ready!

I’ve spent some time getting Drools OSGi ready, which was harder than I expected, especially as OSGi is new to me. Last night I finally got OSGi Declarative Services working with Drools. When you combine this with our Spring work, <http://blog.athico.com/2009/12/drools-spring-improvements.html>, it’s great timing for the recent Spring DM announcement, <http://blog.springsource.com/2010/01/12/dm-server-project-moves-to-eclipse-org>.

For those that don’t know. OSGi is a dynamic module system for declarative services. So what does that mean? Each jar in OSGi is called a bundle and has it’s own Classloader. Each bundle specifies the packages it exports (makes publicly available) and which packages it imports (external dependencies). OSGi will use this information to wire the classloaders of different bundles together; the key distinction is you don’t specify what bundle you depend on, or have a single monolithic classpath, instead you specify your package import and version and OSGi attempts to satisfy this from available bundles.

It also supports side by side versioning, so you can have multiple versions of a bundle installed and it’ll wire up the correct one. Further to this Bundles can register services for other bundles to use. These services need initialisation, which can cause ordering problems – how do you make sure you don’t consume a service before its registered?

OSGi has a number of features to help with service composition and ordering. The two main ones are the programmatic ServiceTracker and the xml based Declarative Services. There are also other projects that help with this; [Spring DM](<http://www.springsource.org/osgi>), [iPOJO](<http://felix.apache.org/site/apache-felix-ipojo.html>), [Gravity](<http://gravity.sourceforge.net/servicebinder/>).

Each of the Drools factories is now also available as a FactoryService interface. You can either have OSGi inject those into a pojo, or retrieve them yourself from OSGi. I’ll cover injection here. The below example injects the KnowledgeBuilderFacotryService, KnowledgeBaseFactoryService and ResourecFactoryService into the TestComponent pojo.

```xml
<scr:component xmlns:scr="http://www.osgi.org/xmlns/scr/v1.1.0">
  <implementation class="testosgi.TestComponent"/>
  <reference bind="setKnowledgeBaseFactoryService" unbind="unsetKnowledgeBaseFactoryService" interface="org.drools.KnowledgeBaseFactoryService"/>
   
  <reference bind="setResourceFactoryService" unbind="unsetResourceFactoryService" interface="org.drools.io.ResourceFactoryService"/>
              
  <reference bind="setKnowledgeBuilderFactoryService" unbind="unsetKnowledgeBuilderFactoryService" interface="org.drools.builder.KnowledgeBuilderFactoryService" target="(org.drools.compiler.DecisionTableProvider=true)"/>
             
</scr:component>
```

The TestComponent will only be activated when all of the referenced services are available and injected into the pojo. You’ll also notice the “target” attribute for the KnowledgeBuilderFactoryService. The reason for this is that OSGi DS has no built in way to declaratively say which optional services must be present to satisfy your component. As a work around I made any Drools service that has optional services set a property if/when the optional service is available. Filters can then be applied, via the target attribute, to make sure the Service is in a desired state before consuming it. And that is pretty much it :)

Getting there wasn’t so easy. The first step was in automating the build and packaging. To automate the build I used Peter Krien’s [BND](<http://www.aqute.biz/Code/Bnd>) tool. I found that BND would only automate the maven transitive dependencies by embedding them, so I did this first. This built a single Drools jar with all Drools jars and dependencies inside it. This straight away triggered ClassLoader issue, forcing me to rework how the Drools ClassLoader framework is configured. The issue here was that Drools uses the ClassLoader that you provide it when compiling DRLs, that means any runtime class loading is resolved against the ClassLoader the user provides. Because of the way OSGi works if the user was to provide a ClassLoader from their bundle, that ClassLoader would not be able to see internal classes to Drools itself. This meant I’d have the Drools bundles giving me ClassNotFoundExceptions for classes in it’s own Bundle. The answer was to make a CompositeClassLoader that takes the provided user ClassLoader and combines it with the ClassLoaders of the Drools bundle’s.

With that now working the next issue was the monolithic bundle we now had. I first tried to separate drools-api, to give real api separation. This then triggered “split packages”. This is one of those things that you wish the OSGi people would shout from the roof tops about to anyone hoping to be OSGi compatible in the future, as I had them all over the place. A split package is where you have the same package namespace used in different jars. drools-api and drools-core both have classes in the “org.drools” namespace. There is very little documentation on resolving split packages and the solution proposed in BND didn’t seem to do anything for me. I read that I can use a “mandatory” setting with my exports, which should make my imports work, but I couldn’t get that working either. Instead I moved away from “Package-Import” to “DynamicPackage-Import *” and “Require-Bundle”, where I tied the Drools impl bundles to the api bundle and re-exported interfaces. This seemed to do the job, although the later are frowned upon, see [here](<http://www.osgi.org/blog/2006/04/misconceptions-about-osgi-headers.html>). “Require-Bundle” couples your bundle to a specific version, which means you aren’t making the most of the more declarative nature of OSGi and “DynamicPackage-Import *” just sucks everything in, which apparently can lead to inefficiencies in OSGi, something called a “fan out”. I have to admit this gets too low level for me, so if anyone wants to add more light on this in the comments, please do and I’ll paste it into the end of this blog.

The next step was to split up my monolithic Drools bundles back to their original jars and not to embed their dependencies. Variations on the following for the Drools modules seemed to work for me:

```xml
<configuration>
     
  <manifestLocation>META-INF</manifestLocation>
     
  <instructions>
           
    <_removeheaders>Ignore-Package</_removeheaders>
                              
    <Require-Bundle>org.drools.api;visibility:=reexport;bundle-version="${pom.version}"</Require-Bundle>
           
    <Import-Package>!org.drools.*, *</Import-Package>
           
    <Export-Package>org.drools.*</Export-Package>
               
    <DynamicImport-Package>*</DynamicImport-Package>
           
    <Bundle-Activator>org.drools.osgi.core.Activator</Bundle-Activator>
       
  </instructions>
</configuration>
```

Because many of the Drools dependencies are not OSGi ready I turned to the Spring [repository](<http://www.springsource.com/repository/app/>), which repackages many projects with OSGi ready manifests in a Maven consumerable repository.

The Activator element specifies the class to be called when each Bundle is loaded in OSGi. The Activator registers services and where optional services need to be tracked configures a ServiceTracker that updates the properties that the target attribute can filter on. This is the programmatic way to setup services in OSGi, compared to DS.

I’m now in the process of OSGi-ifying the other Drools modules and trying to make it more robust. Thanks to Peter Kriens and the people on the #eclipse and #osgi irc channels for their patience with my questions.