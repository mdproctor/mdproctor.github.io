---
layout: post
title: "Drools Extensible Process Definition Language (ePDL) and the Semantic Module Framework (SMF)"
date: 2007-12-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/12/drools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html
---

Old school Drools 2.x users might remember the [Semantic Module Framework](<http://legacy.drools.codehaus.org/Semantics+Module+Framework>) and how it would allow for domain specific XML representations, such as the [House Example DSL](<http://legacy.drools.codehaus.org/House+Example>).

One of the issues with the SMF in Drools 2.0 was that rules are too hard to build programmatically, so the complexity was great. In contrast process nodes are trivial to build and wire together, so I have decided to resurrect the SMF for our process language; actually I have done this for rules too so they both using the same framwork, but I’m not expecting users to extend the rules side. I have forward ported the XML framework from Drools 2.0 and simplified it.

The parser creates DOM like fragments which are processed by builder handlers. The parser also maintains a parent hierarchy back to the root node. The SemanticModule is a configuration of handlers for elements in a given namespace (uri). We keep a registry called SemanticModules, with the uri as a key for each SematnicModule. The code to retrieve a SemanticModule is:

```java
public SemanticModule getSemanticModule(String uri) {
 return this.modules.get( uri );
}
```

The SemanticModules can be built programmaticaly and/or via discovered configuration files. The default process model handlers are already in the SemanticModules registry, via concrete implementations RulesSemanticModule and ProcessSemanticModule, discovered modules are wired together using the DefaultSemanticModule class.

For each xml element the parsers reads in it looks up the Handler, by first getting the SemanticModule for the namespace and then retrieving the handler from the SemanticModule with the getHandler(…) method:

```java
public Handler getHandler(String name) {
 return this.handlers.get( name );
}
```

So how does a Handler work? It has two methods, start(…) and end(…), called when the parsers enters and exits the element; inbetween which a DOM like fragment is built. The start method has access to the element attributes and the end method has access to the DOM like fragment that was built.

The start method initialises the DOM fragment build process using the startConfiguration() method:

```java
reader.startConfiguration( localName, attrs );
```

The end method finalises the returns the DOM fragment using the endConfiguration() method:

```java
Configuration config = reader.endConfiguration();
```

Lets look at a complete start method now for an ActionNode:

```java
public Object start(String uri, String localName,
                    Attributes attrs, ExtensibleXmlParser reader) throws SAXException {
 xmlPackageReader.startConfiguration( localName, attrs );     
 RuleFlowProcessImpl  process = ( RuleFlowProcessImpl) reader.getParent();
 ActionNodeImpl actionNode = new ActionNodeImpl();     
 actionNode.setName( attrs.getValue( "name" ) );     
 process.addNode( actionNode );
 ((ProcessBuildData)reader.getData()).addNode( actionNode );     
 return actionNode;
}
```

Above you can see we start the configuration for the DOM fragment and create an ActionNode setting its properties; note we don’t yet set the content body, as we don’t have that information yet, this is created end the end method:

```java
public Object end(String uri, String localName,
                  ExtensibleXmlParser reader) throws SAXException {
 Configuration config = reader.endConfiguration();
 RuleFlowProcessImpl  process = ( RuleFlowProcessImpl ) reader.getParent();
 ActionNodeImpl actionNode = ( ActionNodeImpl ) xmlPackageReader.getCurrent();    
 actionNode.setAction( "logger.Warn(" + config.getText() + ")") );     
 return actionNode;
}
```

Both properties files and programmatic apis can be used to register handlers for a SemanticModule. For instance if we wanted to programmatically register a logger handler we would do it as follows:

```java
SemanticModule module = new DefaultSemanticModule( "http://domain/org/mydsl" );
module.addHandler( "logger", new LoggerHandler() );
```

Or we can do it via properties file:

```text
uri=http://domain/org/mydsl
store=org.drools.xml.StoreHandler
```

Note to use a properties file the PackageBuilderConfiguration needs to be told about these configurations:

```text
semanticModules = mydsl.conf
```

So the above LoggerHandler and its registration allows for domain specific XML like below:

```xml
<process  name="process name" id="process name" package-name="org.domain"
          xmlns="http://drools.org/drools-4.0/process"
          xmlns:mydsl="http://domain/org/mydsl"
          xmlns:xs="http://www.w3.org/2001/XMLSchema-instance"
          xs:schemaLocation="http://drools.org/drools-4.0/process drools-processes-4.0.xsd" >
          
 <nodes>           
     <start name="start node" />
     
     <action name="action node" dialect="java">
         list.add( "action node was here" );             
     </action>
     
     <mydsl:logger name="test logger" type="warn">
         This is my message         
     <mydsl:logger>
     
     <end name="end node" />
 </nodes>

 <connections>
     <connection from="start node" to="action node" />
     <connection from="action node" to="test logger" />
     <connection from="test logger" to="end node" />
 </connections>

</process>
```