---
layout: post
title: "Spring integration for Drools has landed."
date: 2009-10-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/10/spring-integration-for-drools-has-landed.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Spring integration for Drools has landed.](<https://blog.kie.org/2009/10/spring-integration-for-drools-has-landed.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- October 23, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’ve just committed the first end to end working Spring integration for Drools. There is still lots more to do, but it at least now allows for end to end working examples. The latest build that includes this work can be found from hudson here:  
<https://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/trunk/target/>

So how does it work. Lets look at the unit test for more details. The [beans.xml](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-container/drools-spring/src/test/resources/org/drools/container/spring/beans.xml?r=29780>) provides a configuration for KnowledgeBases, StatefulKnowledgeSession, StatelessKnowledgeSession and the ServiceManager. KnowledgeBases can be confired from a list of resources, that work in the same way that changeset xml does. This allows resources to be pulled from any URL resolveble location, be it classpath, localdisk or from artifacts published from Guvnor:
[code]
    <drools:kbase id="kbase1">  
    <drools:resource source="classpath:org/drools/container/spring/testSpring.drl" type="DRL"/>  
    <drools:resource source="classpath:org/drools/container/spring/IntegrationExampleTest.xls" type="DTABLE">  
      <drools:decisiontable-conf input-type="XLS" worksheet-name="Tables_2"/>  
    </drools:resource>  
    </drools:kbase>
[/code]

The above xml shows a KnowledgeBase configured from a DRL and a XLS, remember we could have added DRFs if we wanted workflow in there too.

That KnowledgeBase is now a bean that can be referenced via the id “kbase1”. From that bean we can now create sessions. The “type” attribute specifies whether the session is stateful or stateless:
[code]
    <drools:ksession id="ksession1" type="stateless" kbase="kbase1"/>  
    <drools:ksession id="ksession2" type="stateful" kbase="kbase1"/>
[/code]

Those sessions are now beans and can be injected into your own classes using Spring annotations, or used to configure up a Drools ServiceManager.
[code]
    <drools:serviceManager id="sm1">  
    <drools:register name="stateless1" ref="ksession1"/>  
    <drools:register ref="ksession2"/>  
    </drools:serviceManager>
[/code]

The ServiceManager is a new class that I haven’t mentioned before that will be in the upcoming Drools 5.1. The ServiceManager can be worked with both locally and remotely. It allows sessions to be created and registered all seamlessly, whether it’s local or remote and those sessions are also exposed both locally and remotely. This ties in with the [Camel ](<http://camel.apache.org/>)work we are doing to make it easy to work with Drools out of the box in a service and remoting environment and should hopefully provide the ultimate in event driven architectures. I’ll blog more on those pieces as they fall into place.

The XSD can be found here: [spring-drools.xsd](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-container/drools-spring/src/main/resources/drools-spring.xsd?r=29780>)

Once the xml is in place, using it with Spring is a doddle and you can look at the [two unit tests](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-container/drools-spring/src/test/java/org/drools/container/spring/SpringDroolsTest.java?r=29780>) to see this in action:
[code]
        public void test1() throws Exception {  
         ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext( "org/drools/container/spring/beans.xml" );  
      
         List list = new ArrayList();  
         StatelessKnowledgeSession kstateless = (StatelessKnowledgeSession) context.getBean( "ksession1" );  
         kstateless.setGlobal( "list", list );  
         kstateless.execute( new Person( "Darth", "Cheddar", 50 ) );  
         assertEquals( 2, list.size() );  
      
         list = new ArrayList();  
         StatefulKnowledgeSession kstateful = (StatefulKnowledgeSession) ((StatefulKnowledgeSession) context.getBean( "ksession2" ));  
         kstateful.setGlobal( "list", list );  
         kstateful.insert( new Person( "Darth", "Cheddar", 50 ) );  
         kstateful.fireAllRules();  
         assertEquals( 2, list.size() );  
     }  
      
     public void test2() {  
         ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext( "org/drools/container/spring/beans.xml" );  
      
         ServiceManager sm = (ServiceManager) context.getBean( "sm1" );  
      
         List list = new ArrayList();  
         StatelessKnowledgeSession kstateless = (StatelessKnowledgeSession) sm.lookup( "stateless1" );  
         kstateless.setGlobal( "list", list );  
         kstateless.execute( new Person( "Darth", "Cheddar", 50 ) );  
         assertEquals( 2, list.size() );  
      
         list = new ArrayList();  
         StatefulKnowledgeSession kstateful = (StatefulKnowledgeSession) sm.lookup( "ksession2" );  
         kstateful.setGlobal( "list" list );  
         kstateful.insert( new Person( "Darth", "Cheddar", 50 ) );  
         kstateful.fireAllRules();  
         assertEquals( 2, list.size() );  
     }
[/code]

There is still lots more to do, especially around exposing actual configuration information (JPA etc) and initial setup data (globals, inserted facts) along with extending this to work with Camel. So if you want to help, you know where to find us :)  
[IRC](<http://labs.jboss.org/drools/irc.html>)  
[Mailing Lists](<http://labs.jboss.org/drools/lists.html>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F10%2Fspring-integration-for-drools-has-landed.html&linkname=Spring%20integration%20for%20Drools%20has%20landed.> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F10%2Fspring-integration-for-drools-has-landed.html&linkname=Spring%20integration%20for%20Drools%20has%20landed.> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F10%2Fspring-integration-for-drools-has-landed.html&linkname=Spring%20integration%20for%20Drools%20has%20landed.> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F10%2Fspring-integration-for-drools-has-landed.html&linkname=Spring%20integration%20for%20Drools%20has%20landed.> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F10%2Fspring-integration-for-drools-has-landed.html&linkname=Spring%20integration%20for%20Drools%20has%20landed.> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F10%2Fspring-integration-for-drools-has-landed.html&linkname=Spring%20integration%20for%20Drools%20has%20landed.> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F10%2Fspring-integration-for-drools-has-landed.html&linkname=Spring%20integration%20for%20Drools%20has%20landed.> "Email")