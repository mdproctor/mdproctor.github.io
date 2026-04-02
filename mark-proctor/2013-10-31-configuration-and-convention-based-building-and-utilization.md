---
layout: post
title: "Configuration and Convention based Building and Utilization"
date: 2013-10-31
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2013/10/configuration-and-convention-based-building-and-utilization.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Configuration and Convention based Building and Utilization](<https://blog.kie.org/2013/10/configuration-and-convention-based-building-and-utilization.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- October 31, 2013  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

Sneak peak at some of the 6.0 documentation we are writing. This introduces, via examples, the new ways to work with DRL and BPM2 files – without needing to programmatically create a builder, load resources.

Enjoy  
—  
6.0 introduces a new configuration and convention approach to building knowledge bases, instead of the using the programmatic builder approach in 5.x. Atlhough a builder is still available to fall back on, as it’s used for the tooling integration.  
Building now uses Maven, and aligns with Maven practices. A KIE projcet or module is simply a Maven java project or module; with an additional meta data file META-INF/kmodule.xml. The kmodule.xml file is the descriptor that selects resources to knowledge bases and configures those knowledge bases and sessions. There is also alternative xml support via Spring and OSGi BluePrints.  
While standard Maven can build and package KIE resources, it will not provide validation at build time. There is a Maven plugin which is recommend to use to get build time validation. The plugin also pre-genenerates many classes, making the runtime loading faster too.

Maven can either ‘mvn install’ to deploy a KieModule to the local machine, where all other applications on the local machine use it. Or it can ‘mvn ‘deploy’ to push the KieModule to a remote Maven repository. Building the Application wil pull in the KieModule, popualting it’s local Maven repository, as it does so.

Jars can be deployed in one of two ways. Either added to the classpath, like any other jar in a Maven dependency listing, or they can be dynamically loaded at runtime. KIE will scan the classpath to find all the jars with a kmodule.xml in it. Each found jar is represented by the KieModule interface. The term Classpath KieModules and dynamic KieModule is used to refer to the two loading approaches. While dynamic modules supports side by side versioning, classpath modules do not. Further once module is on the classpath, no other version may be loaded dynamically.  
Detailed referencs for the api are included in the next sections, the impatiant can jump straight to the examples section, which is fairly intuitive for the different use cases.

[The best way to learn the new build system is by example. The source project “drools-examples-api” contains a number of examples, and can be found at github:](<http://blog.athico.com/>)  
<https://github.com/droolsjbpm/drools/tree/6.0.x/drools-examples-api>  
Each example is described below, the order starts with the simplest and most default working it’s way up to more complex use cases.  
The Deploy use cases here all involve `mvn install`. Remote deployment of jars in Maven is well covered is Maven literature. Utilize refers to the initial act loading the resources and providing access to the KIE runtimes. Where as Run refers to the act of interacting with those runtimes.

#### [Default KieSession](<http://blog.athico.com/>)

  * [Project: default-kesession.](<http://blog.athico.com/>)

  * [Summary: Empty kmodule.xml KieModule on the classpath that includes all resources in a single default KieBase . The example shows the retrieval of the default KieSession from the classpath.](<http://blog.athico.com/>)

[An empty kmodule.xml will produce a single KieBase that includes all files found under resources path, be it DRL, BPMN2, XLS etc. That single KieBase is the default and also includes a single default KieSession. Default means they can be created without knowing their names.](<http://blog.athico.com/>)

[**Example 2.34. Author – kmodule.xml**
[code]
    <kmodule xmlns="http://jboss.org/kie/6.0.0/kmodule"> </kmodule>
      
    
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.35. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
ks.getKieClasspathContainer() returns the KieContainer that contains the KieBases deployed onto the environment classpath. kContainer.newKieSession() creates the default KieSession. Notice you no longer need to look up the KieBase, in orde to create the KieSession. The KieSession knows which KieBase it’s assocaited with, and ues that, which in this case is the default KieBase.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.36. Utilize and Run – Java**
[code]
    KieServices ks = KieServices.Factory.get();
    KieContainer kContainer = ks.getKieClasspathContainer();
    
    KieSession kSession = kContainer.newKieSession();
    kSession.setGlobal("out", out);
    kSession.insert(new Message("Dave", "Hello, HAL. Do you read me, HAL?"));
    kSession.fireAllRules();                
          
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
](<http://blog.athico.com/>)

#### [Named KieSession](<http://blog.athico.com/>)

  * [Project: named-kiesession.](<http://blog.athico.com/>)

  * [Summary: kmodule.xml that has one named KieBase and one named KieSession. The examples shows the retrieval of the named KieSession from the classpath.](<http://blog.athico.com/>)

[kmodule.xml will produce a single named KieBase, ‘kbase1’ that includes all files found under resources path, be it DRL, BPMN2, XLS etc. KieSession ‘ksession1’ is associated with that KieBase and can be created by name.](<http://blog.athico.com/>)

[**Example 2.37. Author – kmodule.xml**
[code]
     <kmodule xmlns="http://jboss.org/kie/6.0.0/kmodule">
        <kbase name="kbase1">
            <ksession name="ksession1"/>
        </kbase>
    </kmodule>
    
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.38. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
ks.getKieClasspathContainer() returns the KieContainer that contains the KieBases deployed onto the environment classpath. This time the KieSession uses the name ‘ksession1’. You do not need to lookup the KieBase first, as it knows which KieBase ‘ksession1’ is assocaited with.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.39. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    KieContainer kContainer = ks.getKieClasspathContainer();
    
    KieSession kSession = kContainer.newKieSession("ksession1");
    kSession.setGlobal("out", out);
    kSession.insert(new Message("Dave", "Hello, HAL. Do you read me, HAL?"));
    kSession.fireAllRules();
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [KieBase Inheritence](<http://blog.athico.com/>)

  * [Project: kiebase-inclusion.](<http://blog.athico.com/>)

  * [Summary: ‘kmodule.xml’ demonstrate that one KieBase can include the resources from another KieBase, from another KieModule. In this case it inherits the named KieBase from the ‘name-kiesession’ example. The included KieBase can be from the current KieModule or any other KieModule that is in the pom.xml dependency list.](<http://blog.athico.com/>)

[kmodule.xml will produce a single named KieBase, ‘kbase2’ that includes all files found under resources path, be it DRL, BPMN2, XLS etc. Further it will include all the resources found from the KieBase ‘kbase1’, due to the use of the ‘includes’ attribute. KieSession ‘ksession2’ is associated with that KieBase and can be created by name.](<http://blog.athico.com/>)

[**Example 2.40. Author – kmodule.xml**
[code]
     <kbase name="kbase2" includes="kbase1">
        <ksession name="ksession2"/>
    </kbase>
    
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
This example requires that the previous example, ‘named-kiesession’, is built and installed to the local Maven repository first. Once installed it can be included as a dependency, using the standard Maven  element.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.41. Author – pom.xml**
[code]
     <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
      <modelVersion>4.0.0</modelVersion>
      <parent>
        <groupId>org.drools</groupId>
        <artifactId>drools-examples-api</artifactId>
        <version>6.0.0/version>
      </parent>
    
      <artifactId>kiebase-inclusion</artifactId>
      <name>Drools API examples - KieBase Inclusion</name>
    
      <dependencies>
        <dependency>
          <groupId>org.drools</groupId>
          <artifactId>drools-compiler</artifactId>
        </dependency>
        <dependency>
          <groupId>org.drools</groupId>
          <artifactId>named-kiesession</artifactId>
          <version>6.0.0</version>
        </dependency>
      </dependencies>
    
    </project>
    
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
Once ‘named-kiesession’ is built and installed this example can be built and installed as normal. Again the act of installing, will force the unit tests to run, demonstrating the use case.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.42. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
ks.getKieClasspathContainer() returns the KieContainer that contains the KieBases deployed onto the environment classpath. This time the KieSession uses the name ‘ksession2’. You do not need to lookup the KieBase first, as it knows which KieBase ‘ksession1’ is assocaited with. Notice two rules fire this time, showing that KieBase ‘kbase2’ has included the resources from the dependency KieBase ‘kbase1’.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.43. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    KieContainer kContainer = ks.getKieClasspathContainer();
    KieSession kSession = kContainer.newKieSession("ksession2");
    kSession.setGlobal("out", out);
    
    kSession.insert(new Message("Dave", "Hello, HAL. Do you read me, HAL?"));
    kSession.fireAllRules();
    
    kSession.insert(new Message("Dave", "Open the pod bay doors, HAL."));
    kSession.fireAllRules();
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [Multiple KieBases](<http://blog.athico.com/>)

  * [Project: ‘multiple-kbases.](<http://blog.athico.com/>)

  * [Summary: Demonstrates that the ‘kmodule.xml’ can contain any number of KieBase or KieSession declarations. Introduces the ‘packages’ attribute to select the folders for the resources to be included inthe .](<http://blog.athico.com/>)

[kmodule.xml produces 6 different named KieBases. ‘kbase1’ includes all resources from the KieModule. The other KieBases include resources from other selected folders, via the ‘packages’ attribute. Note the use wildcard ‘*’ use, to select this package and all packages below it.](<http://blog.athico.com/>)

[**Example 2.44. Author – kmodule.xml**
[code]
     <kmodule xmlns="http://jboss.org/kie/6.0.0/kmodule">
    
      <kbase name="kbase1">
        <ksession name="ksession1"/>
      </kbase>
    
      <kbase name="kbase2" packages="org.some.pkg">
        <ksession name="ksession2"/>
      </kbase>
    
      <kbase name="kbase3" includes="kbase2" packages="org.some.pkg2">
        <ksession name="ksession3"/>
      </kbase>
    
      <kbase name="kbase4" packages="org.some.pkg, org.other.pkg">
        <ksession name="ksession4"/>
      </kbase>
    
      <kbase name="kbase5" packages="org.*">
        <ksession name="ksession5"/>
      </kbase>
    
      <kbase name="kbase6" packages="org.some.*">
        <ksession name="ksession6"/>
      </kbase>
    </kmodule>
    
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.45. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
Only part of the example is included below, as there is a test method per KieSession, but each one is a repetitino of the other, with just different list expectations.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.46. Utilize and Run – Java**
[code]
     @Test
    public void testSimpleKieBase() {
        List<Integer> list = useKieSession("ksession1");
        // no packages imported means import everything
        assertEquals(4, list.size());
        assertTrue( list.containsAll( asList(0, 1, 2, 3) ) );
    }
    
    //.. other tests for ksession2 to ksession6 here
    
    private List<Integer> useKieSession(String name) {
        KieServices ks = KieServices.Factory.get();
        KieContainer kContainer = ks.getKieClasspathContainer();
        KieSession kSession = kContainer.newKieSession(name);
    
        List<Integer> list = new ArrayList<Integer>();
        kSession.setGlobal("list", list);
        kSession.insert(1);
        kSession.fireAllRules();
    
        return list;
    }
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [KieContainer from KieRepository](<http://blog.athico.com/>)

  * [Project: kcontainer-from-repository](<http://blog.athico.com/>)

  * [Summary: The project does not contain a kmodule.xml, nor does the pom.xml have any dependencies for other KieModules. Instead the Java code demonstrates the loading of a dynamic KieModule from a maven repository.](<http://blog.athico.com/>)

[The pom.xml must include kie-ci as a depdency, to ensure Maven is available at runtime. As this uses Maven under the hood you can also use the standard Maven settings.xml file.](<http://blog.athico.com/>)

[**Example 2.47. Author – pom.xml**
[code]
     <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
      <modelVersion>4.0.0</modelVersion>
      <parent>
        <groupId>org.drools</groupId>
        <artifactId>drools-examples-api</artifactId>
        <version>6.0.0</version>
      </parent>
    
      <artifactId>kiecontainer-from-kierepo</artifactId>
      <name>Drools API examples - KieContainer from KieRepo</name>
    
      <dependencies>
        <dependency>
          <groupId>org.kie</groupId>
          <artifactId>kie-ci</artifactId>
        </dependency>
      </dependencies>
    
    </project>
    
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.48. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
In the previous examples the classpath KieContainer used. This example creates a dynamic KieContainer as specified by the ReleaseId. The ReleaseId uses Maven conventions for group id, artifact id and version. It also obey’s LATEST and SNAPSHOT for versions.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.49. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    
    // Install example1 in the local maven repo before to do this
    KieContainer kContainer = ks.newKieContainer(ks.newReleaseId("org.drools", "named-kiesession", "6.0.0-SNAPSHOT"));
    
    KieSession kSession = kContainer.newKieSession("ksession1");
    kSession.setGlobal("out", out);
    
    Object msg1 = createMessage(kContainer, "Dave", "Hello, HAL. Do you read me, HAL?");
    kSession.insert(msg1);
    kSession.fireAllRules();
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [Default KieSession from File](<http://blog.athico.com/>)

  * [Project: default-kiesession-from-file](<http://blog.athico.com/>)

  * [Summary: Dynamic KieModules can also be loaded from any Resource location. The loaded KieModule provides default KieBase and KieSession definitions.](<http://blog.athico.com/>)

[No kmodue.xml file exists. The project ‘default-kiesession’ must be built first, so that the resulting jar, in the target folder, be be reference as a File.](<http://blog.athico.com/>)

[**Example 2.50. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
Any KieModule can be loaded from a Resource location and added to the KieRepository. Once in the KieRepository it can be resolved via it’s ReleaseId. Note neither Maven or kie-ci are needed here. It will not setup a transitive dependency parent classloader.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.51. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    KieRepository kr = ks.getRepository();
    
    KieModule kModule = kr.addKieModule(ks.getResources().newFileSystemResource(getFile("default-kiesession")));
    
    KieContainer kContainer = ks.newKieContainer(kModule.getReleaseId());
    
    KieSession kSession = kContainer.newKieSession();
    kSession.setGlobal("out", out);
    
    Object msg1 = createMessage(kContainer, "Dave", "Hello, HAL. Do you read me, HAL?");
    kSession.insert(msg1);
    kSession.fireAllRules();
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [Named KieSession from File](<http://blog.athico.com/>)

  * [Project: named-kiesession-from-file](<http://blog.athico.com/>)

  * [Summary: Dynamic KieModules can also be loaded from any Resource location. The loaded KieModule provides named KieBase and KieSession definitions.](<http://blog.athico.com/>)

[No kmodue.xml file exists. The project ‘named-kiesession’ must be built first, so that the resulting jar, in the target folder, be be reference as a File.](<http://blog.athico.com/>)

[**Example 2.52. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
Any KieModule can be loaded from a Resource location and added to the KieRepository. Once in the KieRepository it can be resolved via it’s ReleaseId. Note neither Maven or kie-ci are needed here. It will not setup a transitive dependency parent classloader.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.53. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    KieRepository kr = ks.getRepository();
    
    KieModule kModule = kr.addKieModule(ks.getResources().newFileSystemResource(getFile("named-kiesession")));
    
    KieContainer kContainer = ks.newKieContainer(kModule.getReleaseId());
    
    KieSession kSession = kContainer.newKieSession("ksession1");
    kSession.setGlobal("out", out);
    
    Object msg1 = createMessage(kContainer, "Dave", "Hello, HAL. Do you read me, HAL?");
    kSession.insert(msg1);
    kSession.fireAllRules();
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [KieModule with Dependant KieModule](<http://blog.athico.com/>)

  * [Project: kie-module-form-multiple-files](<http://blog.athico.com/>)

  * [Summary: Programmatically provide the list of dependant KieModules, without any Maven to resolve anything.](<http://blog.athico.com/>)

[No kmodue.xml file exists. The projects ‘named-kiesession’ and ‘kiebase-include’ must be built first, so that the resulting jars, in the target folders, be be reference as Files.](<http://blog.athico.com/>)

[**Example 2.54. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
Creates two resources. One is for the main KieModule ‘exRes1’ the other is for the dependency ‘exRes2’. Even though kie-ci is not present and thus Maven is not there to resolve the dependencies, this shows how you can manually specify the dependency KieModuels, for the vararg.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.55. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    KieRepository kr = ks.getRepository();
    
    Resource ex1Res = ks.getResources().newFileSystemResource(getFile("kiebase-inclusion"));
    Resource ex2Res = ks.getResources().newFileSystemResource(getFile("named-kiesession"));
    
    KieModule kModule = kr.addKieModule(ex1Res, ex2Res);
    KieContainer kContainer = ks.newKieContainer(kModule.getReleaseId());
    
    KieSession kSession = kContainer.newKieSession("ksession2");
    kSession.setGlobal("out", out);
    
    Object msg1 = createMessage(kContainer, "Dave", "Hello, HAL. Do you read me, HAL?");
    kSession.insert(msg1);
    kSession.fireAllRules();
    
    Object msg2 = createMessage(kContainer, "Dave", "Open the pod bay doors, HAL.");
    kSession.insert(msg2);
    kSession.fireAllRules();
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [Programaticaly build a Simple KieModule with Defaults](<http://blog.athico.com/>)

  * [Project: kiemoduelmodel-example](<http://blog.athico.com/>)

  * [Summary: Programmaticaly buid a KieModule from just a single file. The pom and models are all defaulted. This is the quickest out of the box approach, but should not be added to a Maven repository.](<http://blog.athico.com/>)

[**Example 2.56. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
This programmatically builds a KieModule. It populates the model that represents the ReleaseId and kmodule.xml, as well as added the resources tht. A pom.xml is generated from the ReleaseId.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.57. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    KieRepository kr = ks.getRepository();
    KieFileSystem kfs = ks.newKieFileSystem();
    
    kfs.write("src/main/resources/org/kie/example5/HAL5.drl", getRule());
    
    KieBuilder kb = ks.newKieBuilder(kfs);
    
    kb.buildAll(); // kieModule is automatically deployed to KieRepository if successfully built.
    if (kb.getResults().hasMessages(Level.ERROR)) {
        throw new RuntimeException("Build Errors:n" + kb.getResults().toString());
    }
    
    KieContainer kContainer = ks.newKieContainer(kr.getDefaultReleaseId());
    
    KieSession kSession = kContainer.newKieSession();
    kSession.setGlobal("out", out);
    
    kSession.insert(new Message("Dave", "Hello, HAL. Do you read me, HAL?"));
    kSession.fireAllRules();
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

#### [Programaticaly build a KieModule using Meta Models](<http://blog.athico.com/>)

  * [Project: kiemoduelmodel-example](<http://blog.athico.com/>)

  * [Summary: Programmaticaly buid a KieModule, by creating it’s kmodule.xml meta models resources..](<http://blog.athico.com/>)

[**Example 2.58. Build and Install – Maven**
[code]
    mvn install
[/code]](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[  
This programmatically builds a KieModule. It populates the model that represents the ReleaseId and kmodule.xml, as well as added the resources tht. A pom.xml is generated from the ReleaseId.](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)[**Example 2.59. Utilize and Run – Java**
[code]
     KieServices ks = KieServices.Factory.get();
    KieFileSystem kfs = ks.newKieFileSystem();
    
    Resource ex1Res = ks.getResources().newFileSystemResource(getFile("named-kiesession"));
    Resource ex2Res = ks.getResources().newFileSystemResource(getFile("kiebase-inclusion"));
    
    ReleaseId rid = ks.newReleaseId("org.drools", "kiemodulemodel-example", "6.0.0-SNAPSHOT");
    kfs.generateAndWritePomXML(rid);
    
    KieModuleModel kModuleModel = ks.newKieModuleModel();
    kModuleModel.newKieBaseModel("kiemodulemodel")
                .addInclude("kiebase1")
                .addInclude("kiebase2")
                .newKieSessionModel("ksession6");
    
    kfs.writeKModuleXML(kModuleModel.toXML());
    kfs.write("src/main/resources/kiemodulemodel/HAL6.drl", getRule());
    
    KieBuilder kb = ks.newKieBuilder(kfs);
    kb.setDependencies(ex1Res, ex2Res);
    kb.buildAll(); // kieModule is automatically deployed to KieRepository if successfully built.
    if (kb.getResults().hasMessages(Level.ERROR)) {
        throw new RuntimeException("Build Errors:n" + kb.getResults().toString());
    }
    
    KieContainer kContainer = ks.newKieContainer(rid);
    
    KieSession kSession = kContainer.newKieSession("ksession6");
    kSession.setGlobal("out", out);
    
    Object msg1 = createMessage(kContainer, "Dave", "Hello, HAL. Do you read me, HAL?");
    kSession.insert(msg1);
    kSession.fireAllRules();
    
    Object msg2 = createMessage(kContainer, "Dave", "Open the pod bay doors, HAL.");
    kSession.insert(msg2);
    kSession.fireAllRules();
    
    Object msg3 = createMessage(kContainer, "Dave", "What's the problem?");
    kSession.insert(msg3);
    kSession.fireAllRules();
[/code]

  
](<http://blog.athico.com/>)[](<http://blog.athico.com/>)

[](<http://blog.athico.com/>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F10%2Fconfiguration-and-convention-based-building-and-utilization.html&linkname=Configuration%20and%20Convention%20based%20Building%20and%20Utilization> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F10%2Fconfiguration-and-convention-based-building-and-utilization.html&linkname=Configuration%20and%20Convention%20based%20Building%20and%20Utilization> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F10%2Fconfiguration-and-convention-based-building-and-utilization.html&linkname=Configuration%20and%20Convention%20based%20Building%20and%20Utilization> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F10%2Fconfiguration-and-convention-based-building-and-utilization.html&linkname=Configuration%20and%20Convention%20based%20Building%20and%20Utilization> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F10%2Fconfiguration-and-convention-based-building-and-utilization.html&linkname=Configuration%20and%20Convention%20based%20Building%20and%20Utilization> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F10%2Fconfiguration-and-convention-based-building-and-utilization.html&linkname=Configuration%20and%20Convention%20based%20Building%20and%20Utilization> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F10%2Fconfiguration-and-convention-based-building-and-utilization.html&linkname=Configuration%20and%20Convention%20based%20Building%20and%20Utilization> "Email")
  *[]: 2010-05-25T16:11:00+02:00