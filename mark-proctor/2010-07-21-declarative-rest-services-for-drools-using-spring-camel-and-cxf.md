---
layout: post
title: "Declarative REST Services for Drools using Spring, Camel and CXF"
date: 2010-07-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/07/declarative-rest-services-for-drools-using-spring-camel-and-cxf.html
---

5.1CR1 has just been tagged and is being released, while that’s happening I thought I’d blog the new declarative services for drools-server.

For those wanting to just dive in, download this .war and just unzip into TomCat.  
<https://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/trunk/target/drools-5.1.0.SNAPSHOT-server.war>

Once that’s unzipped you should be able to look at and run the [test.jsp](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-server/src/main/webapp/test.jsp?r=HEAD>) to see it working. This example just executes a simple “echo” type application. It sends a message to the rule server that pre-appends the word “echo” to the front and sends it back. By default the message is “Hello World”, different messages can be passed using the url parameter msg – test.jsp?msg=”My Custom Message”.

Under the hood the jsp invokes the [Test.java](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-server/src/main/java/org/drools/server/Test.java?r=HEAD>) class, this then calls out to Camel which is where the meet happens. The [camel-client.xml](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-server/src/main/resources/camel-client.xml?r=HEAD>) defines the client with just a few lines of xml:

```xml
<camelContext xmlns="http://camel.apache.org/schema/spring" id="camel">
          
  <route>
          
    <from uri="direct://kservice"/>
          
    <policy ref="droolsPolicy">
               
      <to uri="cxfrs://http://localhost:8080/drools-server-app/kservice/rest"/>
            
    </policy>
       
  </route>
            
</camelContext>
```

“direct://kservice” is just a named hook, allowing java to grab a reference and push data into it. In this example the data is already in xml, so we don’t need to add any DataFormat’s to do the marshalling. The DroolsPolicy adds some smarts to the route and you’ll see it used on the server side too. If JAXB or XStream were used, it would inject custom paths and converters, it can also set the classloader too on the server side, on the client side it automatically unwrapes the Response object.

Configuring a Rest server with Spring and Camel is just a few lines of xml:

```xml
<cxf:rsServer id="rsServer"  
              address="/kservice/rest"
              serviceClass="org.drools.jax.rs.CommandExecutorImpl">
   <cxf:providers>
      <bean class="org.drools.jax.rs.CommandMessageBodyReader"/>
   </cxf:providers>
</cxf:rsServer>
```

With the server configured we can now set up our Camel route using Spring, this will unmarshall incoming payloads using xstream before executing against the drools runtime named “ksession1”. The policy augments the XStream converter with some custom converters for Drools objects, as well as setting the ClassLoader to the one used by the ksession.

```xml
<bean id="droolsPolicy" class="org.drools.camel.component.DroolsPolicy" />  
   
<camelContext id="camel" xmlns="http://camel.apache.org/schema/spring">        
   <route>
      <from uri="cxfrs://bean://rsServer"/>
      <policy ref="droolsPolicy">
         <unmarshal ref="xstream" />       
         <to uri="drools:node1/ksession1" />
         <marshal ref="xstream" />
      </policy>
   </route>           
</camelContext>
```

The final but is the declaration of the Drools services themselves:

```
<drools:execution-node id="node1" />
 
<drools:kbase id="kbase1" node="node1">
   <drools:resources>
      <drools:resource  type="DRL" source="classpath:test.drl"/>
   </drools:resources>                                             
</drools:kbase>
        
<drools:ksession id="ksession1" type="stateless" kbase="kbase1" node="node1"/>
```

The execution-node is optional and could have been left out, it’s role is to provide a context to store multiple ksessions. It then allows one rest endpoint to execute against those named ksessions, based on the given name; either in the header or attribute in the root element.

The rule itself can be found here: [test.drl](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-server/src/main/resources/test.drl?r=HEAD>). Notice the type Message is declared part of the drl and is thus not present on the Classpath.

```drl
declare Message
   text : String
end
   
 
rule "echo" dialect "mvel"
when
   $m : Message();
then
   $m.text = "echo:" + $m.text;
end
```

Lucaz has also done a write up of the new Drools Server, <http://lucazamador.wordpress.com/2010/07/20/drools-server-configuration-updated/>.