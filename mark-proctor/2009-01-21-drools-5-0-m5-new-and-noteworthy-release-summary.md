---
layout: post
title: "Drools 5.0 M5 New and Noteworthy Release Summary"
date: 2009-01-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/01/drools-5-0-m5-new-and-noteworthy-release-summary.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools 5.0 M5 New and Noteworthy Release Summary](<https://blog.kie.org/2009/01/drools-5-0-m5-new-and-noteworthy-release-summary.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 21, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Release](<https://blog.kie.org/content_type/release>)

Previous New and Noteworth release summary notes:  
[M1](<http://blog.athico.com/2008/07/drools-50-m1-new-and-noteworthy.html>)  
[M2](<http://blog.athico.com/2008/10/drools-50-m2-new-and-noteworthy-summary.html>)  
[M3/M4  
](<http://blog.athico.com/2008/12/drools5-m3-release-notes.html>)

## Drools Guvnor

Most of the work has been bug fixes and small visual improvements.

  * It is possible to add objects to global collections.

  * Jamming asset lists are fixed. They were causing problems with some locales and date formats.

  * To allow faster rule opening, loading of some widgets have been deferred. For example the images show how assets meta data can be reviewed. Image on the right shows the default view and the left one shows detailed view.

[![](/legacy/assets/images/2009/01/dcae53a046dd-deferred_widget.png)](<http://3.bp.blogspot.com/_hmyqKKjBjB8/SXdkjyV-ntI/AAAAAAAAAA0/xy-I8F0n2uA/s1600-h/deferred_widget.png>)

  * There is now a “About” selection under Admin panel to show the Guvnor version and svn revision. This will help with bug reporting and support.  

## [![](/legacy/assets/images/2009/01/f5823a2743f2-version.png)](<http://3.bp.blogspot.com/_hmyqKKjBjB8/SXdk3Jr1IoI/AAAAAAAAAA8/qc39C0SUQtQ/s1600-h/version.png>)

## Drools Expert

But Fixes  
lots of bug fixes, see JIRA for M5 for details.

Pipeline  
The Drools pipeline helps with the automation of getting information into and out of Drools, especially when using services, such as JMS, and non pojo data sources. Transformers for Smooks, JAXB, Xstream and Jxls are povided. Smooks is an ETL tooling and can work with a variety of data sources, JAXB is a Java standard aimed at working with XSDs, while XStream is a simple and fast xml serialisation framework and finally Jxls allows for loading of pojos from an excel decision table. See the Javadocs PipelineFactory for documentation. Below shows part of a unit test which illustrates part of the JmsMessenger in action:
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

## Drools Flow

The biggest improvement by far is improvement of the documentation. We’re not there yet, but we’ve added sections on getting started, human task management, persistence, etc. The latest Flow documentation can be found here:

<https://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/trunk/target/docs/index.html>

Some features have also been extended, including:

  * The history log – that keeps the history of all executed process instances in a database – has been extended so it is now caable of storing more detailed information for one specfic process instance. It is now possible to find out exactly which nodes were triggered during the execution of the process instance.

  * A new type of join has been added, one that will wait until n of its m incoming connections have been completed. This n could either be hardcoded in the process or based on the value of a variable in the process.

  * Improvements have been made to make persistence easier to configure. The persistence approach is based on a command service that makes sure that all the client invocations are executed inside a transaction and that the state is stored in the database after successful execution of the command. While this was already possible in M4 using the commands directly, we have extended this so that people can simply use the normal StatefulKnowledgeSession interface but simply can configure the persistence using configuration files. For more details, check out the chapter on persistence in the Drools Flow documentation.

## Eclipse IDE

Some small bug fixes were added to make the IDE more stable.

## Drools Fusion

Support to event expiration policy  
added the ability to define a per-type event expiration policy. In the example bellow, the StockTick events will expire 10 minutes after they enter the system:  
declare StockTick  @role( event ) @expires( 10m ) end  
  
Support to temporal operations over arbitrary dates.  
added the ability for point-in-time operators (before, after and coincides) to be used with any arbitrary date field:  
rule “Allow access”   
when   
WorkHours( $s : start, $e : end )  
LogIn( time after $s, time before $e )  
then  
// allow access   
end

Bug Fixes  
lots of bug fixes, see JIRA for M5 for details.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-5-0-m5-new-and-noteworthy-release-summary.html&linkname=Drools%205.0%20M5%20New%20and%20Noteworthy%20Release%20Summary> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-5-0-m5-new-and-noteworthy-release-summary.html&linkname=Drools%205.0%20M5%20New%20and%20Noteworthy%20Release%20Summary> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-5-0-m5-new-and-noteworthy-release-summary.html&linkname=Drools%205.0%20M5%20New%20and%20Noteworthy%20Release%20Summary> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-5-0-m5-new-and-noteworthy-release-summary.html&linkname=Drools%205.0%20M5%20New%20and%20Noteworthy%20Release%20Summary> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-5-0-m5-new-and-noteworthy-release-summary.html&linkname=Drools%205.0%20M5%20New%20and%20Noteworthy%20Release%20Summary> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-5-0-m5-new-and-noteworthy-release-summary.html&linkname=Drools%205.0%20M5%20New%20and%20Noteworthy%20Release%20Summary> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-5-0-m5-new-and-noteworthy-release-summary.html&linkname=Drools%205.0%20M5%20New%20and%20Noteworthy%20Release%20Summary> "Email")