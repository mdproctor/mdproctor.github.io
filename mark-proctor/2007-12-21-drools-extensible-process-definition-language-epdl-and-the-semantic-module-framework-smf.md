---
layout: post
title: "Drools Extensible Process Definition Language (ePDL) and the Semantic Module Framework (SMF)"
date: 2007-12-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/12/drools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Extensible Process Definition Language (ePDL) and the Semantic Module Framework (SMF)](<https://blog.kie.org/2007/12/drools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- December 21, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Old school Drools 2.x users might remember the [Semantic Module Framework](<http://legacy.drools.codehaus.org/Semantics+Module+Framework>) and how it would allow for domain specific XML representations, such as the [House Example DSL](<http://legacy.drools.codehaus.org/House+Example>).

One of the issues with the SMF in Drools 2.0 was that rules are too hard to build programmatically, so the complexity was great. In contrast process nodes are trivial to build and wire together, so I have decided to resurrect the SMF for our process language; actually I have done this for rules too so they both using the same framwork, but I’m not expecting users to extend the rules side. I have forward ported the XML framework from Drools 2.0 and simplified it.

The parser creates DOM like fragments which are processed by builder handlers. The parser also maintains a parent hierarchy back to the root node. The SemanticModule is a configuration of handlers for elements in a given namespace (uri). We keep a registry called SemanticModules, with the uri as a key for each SematnicModule. The code to retrieve a SemanticModule is:
[code]
    public SemanticModule getSemanticModule(String uri) {  
     return this.modules.get( uri );  
    }
[/code]

The SemanticModules can be built programmaticaly and/or via discovered configuration files. The default process model handlers are already in the SemanticModules registry, via concrete implementations RulesSemanticModule and ProcessSemanticModule, discovered modules are wired together using the DefaultSemanticModule class.

For each xml element the parsers reads in it looks up the Handler, by first getting the SemanticModule for the namespace and then retrieving the handler from the SemanticModule with the getHandler(…) method:
[code]
    public Handler getHandler(String name) {  
     return this.handlers.get( name );  
    }
[/code]

So how does a Handler work? It has two methods, start(…) and end(…), called when the parsers enters and exits the element; inbetween which a DOM like fragment is built. The start method has access to the element attributes and the end method has access to the DOM like fragment that was built.

The start method initialises the DOM fragment build process using the startConfiguration() method:
[code]
    reader.startConfiguration( localName, attrs );
[/code]

The end method finalises the returns the DOM fragment using the endConfiguration() method:
[code]
    Configuration config = reader.endConfiguration();
[/code]

Lets look at a complete start method now for an ActionNode:
[code]
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
[/code]

Above you can see we start the configuration for the DOM fragment and create an ActionNode setting its properties; note we don’t yet set the content body, as we don’t have that information yet, this is created end the end method:
[code]
    public Object end(String uri, String localName,  
                      ExtensibleXmlParser reader) throws SAXException {  
     Configuration config = reader.endConfiguration();  
     RuleFlowProcessImpl  process = ( RuleFlowProcessImpl ) reader.getParent();  
     ActionNodeImpl actionNode = ( ActionNodeImpl ) xmlPackageReader.getCurrent();      
     actionNode.setAction( "logger.Warn(" + config.getText() + ")") );       
     return actionNode;  
    }
[/code]

Both properties files and programmatic apis can be used to register handlers for a SemanticModule. For instance if we wanted to programmatically register a logger handler we would do it as follows:
[code]
    SemanticModule module = new DefaultSemanticModule( "http://domain/org/mydsl" );  
    module.addHandler( "logger", new LoggerHandler() );
[/code]

Or we can do it via properties file:
[code]
    uri=http://domain/org/mydsl  
    store=org.drools.xml.StoreHandler
[/code]

Note to use a properties file the PackageBuilderConfiguration needs to be told about these configurations:
[code]
    semanticModules = mydsl.conf
[/code]

So the above LoggerHandler and its registration allows for domain specific XML like below:
[code]
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
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F12%2Fdrools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html&linkname=Drools%20Extensible%20Process%20Definition%20Language%20%28ePDL%29%20and%20the%20Semantic%20Module%20Framework%20%28SMF%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F12%2Fdrools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html&linkname=Drools%20Extensible%20Process%20Definition%20Language%20%28ePDL%29%20and%20the%20Semantic%20Module%20Framework%20%28SMF%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F12%2Fdrools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html&linkname=Drools%20Extensible%20Process%20Definition%20Language%20%28ePDL%29%20and%20the%20Semantic%20Module%20Framework%20%28SMF%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F12%2Fdrools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html&linkname=Drools%20Extensible%20Process%20Definition%20Language%20%28ePDL%29%20and%20the%20Semantic%20Module%20Framework%20%28SMF%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F12%2Fdrools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html&linkname=Drools%20Extensible%20Process%20Definition%20Language%20%28ePDL%29%20and%20the%20Semantic%20Module%20Framework%20%28SMF%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F12%2Fdrools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html&linkname=Drools%20Extensible%20Process%20Definition%20Language%20%28ePDL%29%20and%20the%20Semantic%20Module%20Framework%20%28SMF%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F12%2Fdrools-extensible-process-definition-language-epdl-and-the-semantic-module-framework-smf.html&linkname=Drools%20Extensible%20Process%20Definition%20Language%20%28ePDL%29%20and%20the%20Semantic%20Module%20Framework%20%28SMF%29> "Email")