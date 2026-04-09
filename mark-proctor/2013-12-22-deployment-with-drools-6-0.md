---
layout: post
title: "Deployment with Drools 6.0"
date: 2013-12-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2013/12/deployment-with-drools-6-0.html
---

**KieScanner**   
The 6.0 KieScanner replaces the 5.x KnowledgeAgent. It uses embedded Maven to allow the resolving and retrieving of jars at runtime. 6.0 applications can now easily support dependencies and transitive dependencies; using well known Maven semantics for versioning. It allows for deployment on the class path and also dynamically at runtime. Currently it supports manual “scanNow” and interval polling, remoting will be added in the future. A KieScanner can be registered on a KieContainer as in the following example: 

```
KieServices kieServices = KieServices.Factory.get();
ReleaseId releaseId = kieServices.newReleaseId( "org.acme", "myartifact", "1.0-SNAPSHOT" );
KieContainer kContainer = kieServices.newKieContainer( releaseId );
KieScanner kScanner = kieServices.newKieScanner( kContainer );
// Start the KieScanner polling the Maven repository every 10 seconds
kScanner.start( 10000L );
```

In this example the KieScanner is configured to run with a fixed time interval, but it is also possible to run it on demand by invoking the scanNow() method on it. If the KieScanner finds in the Maven repository an updated version of the Kie project used by that KieContainer it automatically downloads the new version and triggers an incremental build of the new project. From this moment all the new KieBases and KieSessions created from that KieContainer will use the new project version. 

**Installation**

[![](/legacy/assets/images/2013/12/46a69ac40e1b-cheatsheet1.png)](</assets/images/2013/12/65ebd94d7e1e-cheatsheet1.png>)

**Deployment**

[![](/legacy/assets/images/2013/12/182b57378891-cheatsheet2.png)](</assets/images/2013/12/77a1e12a5320-cheatsheet2.png>)

**Settings.xml and Remote Repository Setup**   
The maven settings.xml is used to configure Maven execution. Detailed instructions can be found at the Maven website: http://maven.apache.org/settings.html The settings.xml file can be located in 3 locations, the actual settings used is a merge of those 3 locations. 

  * The Maven install: $M2_HOME/conf/settings.xml 
  * A user’s install: ${user.home}/.m2/settings.xml 
  * Folder location specified by the system propert kie.maven.settings.custom 

The settings.xml is used to specify the location of remote repositories. It is important that you activate the profile that specifies the remote repository, typically this can be done using “activeByDefault”: 

```xml
<profiles>
  <profile>
    <id>profile-1</id>
    <activation>
      <activeByDefault>true</activeByDefault>
    </activation>
    ...
  </profile>
</profiles>
```

  
**Maven Versions and Dependencies** Maven supports a number of mechanisms to manage versioning and dependencies within applications. Modules can be published with specific version numbers, or they can use the SNAPSHOT suffix. Dependencies can specify version ranges to consume, or take avantage of SNAPSHOT mechanism. 

StackOverflow provides a very good description for this, which is reproduced below. <http://stackoverflow.com/questions/30571/how-do-i-tell-maven-to-use-the-latest-version-of-a-dependency>

If you always want to use the newest version, Maven has two keywords you can use as an alternative to version ranges. You should use these options with care as you are no longer in control of the plugins/dependencies you are using. 

When you depend on a plugin or a dependency, you can use the a version value of LATEST or RELEASE. LATEST refers to the latest released or snapshot version of a particular artifact, the most recently deployed artifact in a particular repository. RELEASE refers to the last non-snapshot release in the repository. In general, it is not a best practice to design software which depends on a non-specific version of an artifact. If you are developing software, you might want to use RELEASE or LATEST as a convenience so that you don’t have to update version numbers when a new release of a third-party library is released. When you release software, you should always make sure that your project depends on specific versions to reduce the chances of your build or your project being affected by a software release not under your control. Use LATEST and RELEASE with caution, if at all. 

See the POM Syntax section of the Maven book for more details. 

<http://books.sonatype.com/mvnref-book/reference/pom-relationships-sect-pom-syntax.html>   
<http://books.sonatype.com/mvnref-book/reference/pom-relationships-sect-project-dependencies.html>

Here’s an example illustrating the various options. In the Maven repository, com.foo:my-foo has the following metadata: 

```xml
<metadata>
  <groupId>com.foo</groupId>
  <artifactId>my-foo</artifactId>
  <version>2.0.0</version>
  <versioning>
    <release>1.1.1</release>
    <versions>
      <version>1.0</version>
      <version>1.0.1</version>
      <version>1.1</version>
      <version>1.1.1</version>
      <version>2.0.0</version>
    </versions>
    <lastUpdated>20090722140000</lastUpdated>
  </versioning>
</metadata>
```

If a dependency on that artifact is required, you have the following options (other version ranges can be specified of course, just showing the relevant ones here): Declare an exact version (will always resolve to 1.0.1): 

```xml
<version>[1.0.1]</version>
```

Declare an explicit version (will always resolve to 1.0.1 unless a collision occurs, when Maven will select a matching version): 

```xml
<version>1.0.1</version>
```

Declare a version range for all 1.x (will currently resolve to 1.1.1): 

```xml
<version>[1.0.0,2.0.0)</version>
```

Declare an open-ended version range (will resolve to 2.0.0): 

```xml
<version>[1.0.0,)</version>
```

Declare the version as LATEST (will resolve to 2.0.0): 

```xml
<version>LATEST</version>
```

Declare the version as RELEASE (will resolve to 1.1.1): 

```xml
<version>RELEASE</version>
```

Note that by default your own deployments will update the “latest” entry in the Maven metadata, but to update the “release” entry, you need to activate the “release-profile” from the Maven super POM. You can do this with either “-Prelease-profile” or “-DperformRelease=true”