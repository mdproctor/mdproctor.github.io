---
layout: post
title: "Drools Pipeline for Smooks, JAXB/XSD, jXLS (Excel) and XStream"
date: 2009-01-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/01/drools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Pipeline for Smooks, JAXB/XSD, jXLS (Excel) and XStream](<https://blog.kie.org/2009/01/drools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 21, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

The Drools pipeline helps with the automation of getting information into and out of Drools, especially when using services, such as JMS, and non pojo data sources. Transformers for Smooks, JAXB, Xstream and Jxls are povided. Smooks is an ETL tooling and can work with a variety of data sources, JAXB is a Java standard aimed at working with XSDs, while XStream is a simple and fast xml serialisation framework and finally Jxls allows for loading of pojos from an excel decision table.

Pipeline is not meant as a replacement for products like the more powerful Camel, but is aimed as a complimentary framework that ultimately can be integrated into more powerful pipeline frameworks. Instead it is a simple framework aimed at the specific Drools use cases.

In Drools a pipeline is a series of stages that operate on and propagate a given payload. Typically this starts with a Pipeline instance which is responsible for taking the payload, creating a PipelineContext for it and propagating that to the first Receiver stage. Two types of Pipelines are provided, both requiring a different PipelineContexts. StatefulKnowledgeSessionPipeline and StatelessKnowledgeSessionPipeline. Notice that both factory methods take the relevant session as an argument.
[code]
    Pipeline pipeline = PipelineFactory.newStatefulKnowledgeSessionPipeline( ksession );  
    pipeline.setReceiver( receiver );  
    
[/code]

A pipeline is then made up of a chain of Stages that can implement both the Emitter and the Receiver interfaces. The Emitter interface means the stage can propagate a payload and the Receiver interface means it can receive a payload. This is why the Pipeline interface only implements Emitter and Stage and not Receiver, as it is the first instance in the chain. The Stage interface allows a custom exception handler to be set on the stage.
[code]
    Transformer transformer = PipelineFactory.newXStreamFromXmlTransformer( xstream );  
    transformer.setStageExceptionHandler( new StageExceptionHandler() { .... } );  
    
[/code]

The Transformer interface above extends both Stage, Emitter and Receiver, other than providing those interface methods as a single type, it’s other role is that of a marker interface that indicates the role of the instance that implements it. We have several other marker interfaces such as Expression and Action, both of which also extend Stage, Emitter and Receiver. One of the stages should be responsible for setting a result value on the PipelineContext. It is the role of the ResultHandler interface, that the user implements that is responsible for executing on these results or simply setting them an object that the user can retrieve them from.
[code]
    ResultHandler resultHandler = new ResultHandlerImpl();  
    pipeline.insert( factHandle, resultHandler );   
    System.out.println( resultHandler );  
    ...  
    public class ResultHandlerImpl implements ResultHandler {  
       Object result;  
      
       public void handleResult(Object result) {  
           this.result = result;  
       }  
      
       public Object getResult() {  
           return this.result;  
       }  
    }    
    
[/code]

while the above example shows a simple handler that simply assigns the result to a field that the user can access, it could do more complex work  
like sending the object as a message.

Pipeline is provides an adapter to insert the payload and internally create the correct PipelineContext. Two types of Pipelines are provided, both requiring a different PipelineContext. StatefulKnowledgeSessionPipeline and StatelessKnowledgeSessionPipeline. Pipeline itself implements both Stage and Emitter, this means it’s a Stage in a pipeline and emits the payload to a receiver. It does not implement Receiver itself, as it the start adapter for the pipeline. PipelineFactory provides methods to create both of the two Pipeline. StatefulKnowledgeSessionPipeline is constructed as below, with the receiver set

In general it easier to construct the pipelines in reverse, for example the following one handles loading xml data from disk, transforming it with xstream and then inserting the object:
[code]
    // Make the results, in this case the FactHandles, available to the user  
    Action executeResultHandler = PipelineFactory.newExecuteResultHandler();  
      
    // Insert the transformed object into the session associated with the PipelineContext  
    KnowledgeRuntimeCommand insertStage = PipelineFactory.newStatefulKnowledgeSessionInsert();  
    insertStage.setReceiver( executeResultHandler );  
          
    // Create the transformer instance and create the Transformer stage, where we are going from Xml to Pojo.  
    XStream xstream = new XStream();  
    Transformer transformer = PipelineFactory.newXStreamFromXmlTransformer( xstream );  
    transformer.setReceiver( insertStage );  
      
    // Create the start adapter Pipeline for StatefulKnowledgeSessions  
    Pipeline pipeline = PipelineFactory.newStatefulKnowledgeSessionPipeline( ksession );  
    pipeline.setReceiver( transformer );  
      
    // Instantiate a simple result handler and load and insert the XML  
    ResultHandlerImpl resultHandler = new ResultHandlerImpl();  
    pipeline.insert( ResourceFactory.newClassPathResource( "path/facts.xml", getClass() ),  
                    resultHandler );  
    
[/code]

See StatefullKnowledgeSessionPipeline, StatelessKnowledgeSessionPipeline for more specific information and capabilities on these pipelines.

While the above example is for loading a resource from disk it is also possible to work from a running messaging service. Drools currently provides a single Service for JMS, called JmsMessenger. Support for other Services will be added later. Below shows part of a unit test which illustrates part of the JmsMessenger in action:
[code]
    // as this is a service, it's more likely the results will be logged or sent as a return message  
    Action resultHandlerStage = PipelineFactory.newExecuteResultHandler();  
      
    // Insert the transformed object into the session associated with the PipelineContext  
    KnowledgeRuntimeCommand insertStage = PipelineFactory.newStatefulKnowledgeSessionInsert();  
    insertStage.setReceiver( resultHandlerStage );  
      
    // Create the transformer instance and create the Transformer stage, where we are going from Xml to Pojo. Jaxb needs an array of the available classes  
    JAXBContext jaxbCtx = KnowledgeBuilderHelper.newJAXBContext( classNames,  
                                                                kbase );  
    Unmarshaller unmarshaller = jaxbCtx.createUnmarshaller();  
    Transformer transformer = PipelineFactory.newJaxbFromXmlTransformer( unmarshaller );  
    transformer.setReceiver( insertStage );  
      
    // payloads for JMS arrive in a Message wrapper, we need to unwrap this object  
    Action unwrapObjectStage = PipelineFactory.newJmsUnwrapMessageObject();  
    unwrapObjectStage.setReceiver( transformer );  
      
    // Create the start adapter Pipeline for StatefulKnowledgeSessions  
    Pipeline pipeline = PipelineFactory.newStatefulKnowledgeSessionPipeline( ksession );  
    pipeline.setReceiver( unwrapObjectStage );  
      
    // Services, like JmsMessenger take a ResultHandlerFactory implementation, this is because a result handler must be created for each incoming message.  
    ResultHandleFactoryImpl factory = new ResultHandleFactoryImpl();  
    Service messenger = PipelineFactory.newJmsMessenger( pipeline,  
                                                        props,  
                                                        destinationName,  
                                                        factory );  
    messenger.start();  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html&linkname=Drools%20Pipeline%20for%20Smooks%2C%20JAXB%2FXSD%2C%20jXLS%20%28Excel%29%20and%20XStream> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html&linkname=Drools%20Pipeline%20for%20Smooks%2C%20JAXB%2FXSD%2C%20jXLS%20%28Excel%29%20and%20XStream> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html&linkname=Drools%20Pipeline%20for%20Smooks%2C%20JAXB%2FXSD%2C%20jXLS%20%28Excel%29%20and%20XStream> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html&linkname=Drools%20Pipeline%20for%20Smooks%2C%20JAXB%2FXSD%2C%20jXLS%20%28Excel%29%20and%20XStream> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html&linkname=Drools%20Pipeline%20for%20Smooks%2C%20JAXB%2FXSD%2C%20jXLS%20%28Excel%29%20and%20XStream> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html&linkname=Drools%20Pipeline%20for%20Smooks%2C%20JAXB%2FXSD%2C%20jXLS%20%28Excel%29%20and%20XStream> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-pipeline-for-smooks-jaxb-xsd-jxls-excel-and-xstream.html&linkname=Drools%20Pipeline%20for%20Smooks%2C%20JAXB%2FXSD%2C%20jXLS%20%28Excel%29%20and%20XStream> "Email")