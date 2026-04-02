---
layout: post
title: "BatchExecutor"
date: 2009-04-03
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/04/batchexecutor.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [BatchExecutor](<https://blog.kie.org/2009/04/batchexecutor.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- April 3, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

One of the APIs that I really like in Drools 5.0 is the Command api and BatchExecutor combined with the Pipeline. Rule engines often have the concept of stateful or stateless sessions. Where stateful is the standard working memory that can be worked with iteratively over time. Stateless is a one off execution of a working memory with a provided data set and optionally returning some results with the session disposed at the end, prohibiting further iterative interactions. You can think of stateless as treating a rule engine like a function call with optional return results.

In Drools 4 we supported these two paradigms but the way the user interacted with them was different. StatelessSession used an execute(…) method which would insert a collection of objects as facts. StatefulSession didn’t have this method and insert used the more traditional insert(…) method. The other issue was the StatelessSession did not return any results, the user was expected to map globals themselves to get results, and it wasn’t possible to do anything else other than insert objects, users could not start processes or execute querries. Early versions of Drools 5 tried to address the results issue using the more traditional in/out parameters that others adopted, but still did not address starting processes or executing querries.

Finally with Drools 5.0 I managed to come up with an approach I was happy with that addressed all of these issues and more. The foundations for this is the BatchExecutor interface:
[code]
    public interface BatchExecutor {  
      BatchExecutionResults execute(Command cmd);  
    }  
      
    public interface BatchExecutionResults {  
      Collection getIdentifiers();  
       
      Object getValue(String identifier);  
    }
[/code]

Both the StatelessKnowledgeSession and StatefulKnowledgeSession implement this interface, creating consistency. The CommandFactory allows for commands to be executed on those sessions, only only difference being the StatelessKnowledgeSession executes fireAllRules() at the end before disposing the session. The current supported commands are:

  * FireAllRules
  * GetGlobal
  * SetGlobal
  * InsertObject
  * InsertElements
  * Query
  * StartProcess
  * BatchExecution

InsertObject will insert a single object while InsertElements will iterate an Iterable inserting each of the elements. What this means is that StatelessKnowledgeSession are no longer limited to just inserting objects, they can now start processes or execute querries. What you say, the method only allows for a single Command? That’s Where the BatchExecution comes in, this is a composite command that takes a list of Commands and will iterate and execute each Command in turn. This means you can insert some objects, start a process, call fireAllRules and execute a query all in a single execute(…) call – much more powerful.

As mentioned the StatelessKnowledgeSession by default will execute fireAllRules() automatically at the end. However the keen eyed reader probably has already noticed the FireAllRules command and wondering how that works with a StatelessKnowledgeSession. The FireAllRules command is allowed and using it will disable the automatic execution at the end, think of using it as a sort of manual override.

So this is great, we’ve brought consistency to how StatelessKnowledgeSession and StatefullKnowledgeSession work and also brought in support for more than just inserting objects. What about result handling? Rather than using parameters, like my first attempt which always bugged me, these commands support out identifiers. Any command that has an out identifier set on it will add it’s results to the BatchExecutionResults. Let’s look at a simple example to see how this works:
[code]
    StatelessKnowledgeSession ksession = kbase.newStatelessKnowledgeSession();  
      
    List cmds = new ArrayList();          
    cmds.add( CommandFactory.newInsertObject( new Cheese( "stilton", 1), "stilton") );  
    cmds.add( CommandFactory.newStartProcess( "process cheeses" ) );  
    cmds.add( CommandFactory.newQuery( "cheeses" ) );  
    BatchExecutionResults bresults = ksession.execute( CommandFactory.newBatchExecution( cmds ) );  
    QueryResults qresults = ( QueryResults ) bresults.getValue( "cheeses" );  
    Cheese stilton = ( Cheese ) bresults.getValue( "silton" );  
    
[/code]

So in the above example you saw how multiple commands where executed two of which populate the BatchExecutionResults. The query command defaults to use the same identifier as the query name, but it can also be mapped to a different identifier.

So now we have consistency across stateless and stateful sessions, ability to execute a variety of commands and an elegant way to deal with results. Does it get better than this? Absolutely we’ve built a custom XStream marshaller that can be used with the Drools Pipeline to get XML scripting, which is perfect for services.

I’ve mentioned the pipeline previously, it allows for a series of stages to be used together to help with getting data into and out of sessions. There is a stage that supports the BatchExecutor interface and allows the pipeline to script either a stateful or stateless session. The pipeline setup is trivial:
[code]
    Action executeResultHandler = PipelineFactory.newExecuteResultHandler();  
      
    Action assignResult = PipelineFactory.newAssignObjectAsResult();  
    assignResult.setReceiver( executeResultHandler );  
      
    Transformer outTransformer = PipelineFactory.newXStreamToXmlTransformer( BatchExecutionHelper.newXStreamMarshaller() );  
    outTransformer.setReceiver( assignResult );  
      
    KnowledgeRuntimeCommand batchExecution = PipelineFactory.newBatchExecutor();  
    batchExecution.setReceiver( outTransformer );  
      
    Transformer inTransformer = PipelineFactory.newXStreamFromXmlTransformer( BatchExecutionHelper.newXStreamMarshaller() );  
    inTransformer.setReceiver( batchExecution );  
      
    Pipeline pipeline = PipelineFactory.newStatelessKnowledgeSessionPipeline( ksession );  
    pipeline.setReceiver( inTransformer );
[/code]

The key thing here to note is the use of the BatchExecutionHelper to provide a specially configured XStream with custom converters for our Commands and the new BatchExecutor stage.

The above java code to create the BatchExecution is converted to java below, for added fun I’ve added parameters to the query.
[code]
    <batch-execution>  
      <insert out-identifier="stilton">  
        <org.drools.Cheese>  
          <type>stilton</type>  
          <price>1</price>  
        </org.drools.Cheese>  
      </insert>  
      <query out-identifier='cheeses2' name='cheesesWithParams'>  
        <string>stilton</string>  
        <string>cheddar</string>  
      </query>  
    </batch-execution>
[/code]

Executing is as simple as inserting the XML into the pipeline:
[code]
    insert( inXml, resultHandler );
[/code]

The pipeline also handles the results and marshalling back into XML:
[code]
    String outXml = (String) resultHandler.getObject();  
    
[/code]

With the XML results looking something like:
[code]
    <batch-execution-results>  
      <result identifier="stilton">  
        <org.drools.Cheese>  
          <type>stilton</type>  
          <price>2</price>  
        </org.drools.Cheese>  
      </result>          
      <result identifier='cheeses'>  
        <query-results>  
          <identifiers>  
            <identifier>stilton</identifier>  
            <identifier>cheddar</identifier>  
          </identifiers>  
          <row>  
            <org.drools.Cheese>  
              <type>cheddar</type>  
              <price>2</price>  
              <oldPrice>0</oldPrice>  
            </org.drools.Cheese>  
          </row>  
          <row>  
            <org.drools.Cheese>  
              <type>cheddar</type>  
              <price>1</price>  
              <oldPrice>0</oldPrice>  
            </org.drools.Cheese>  
          </row>  
        </query-results>  
      </result>  
    </batch-execution-results>  
    
[/code]

Pretty cool eh, so we’ve aligned a messaging format to our api and made it service friendly by integrating that with our pipeline.

Hopefully by now you can see why I’m so happy with this and glad I thought of doing this in time before releasing Drools 5.0, instead of using the parameters api. We will extend the CommandFactory to support all the methods for a StatefulknowledgeSession, all with XML marshalling using XStream. This will then form the foundations for rest/ws services in future releases of Drools.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fbatchexecutor.html&linkname=BatchExecutor> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fbatchexecutor.html&linkname=BatchExecutor> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fbatchexecutor.html&linkname=BatchExecutor> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fbatchexecutor.html&linkname=BatchExecutor> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fbatchexecutor.html&linkname=BatchExecutor> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fbatchexecutor.html&linkname=BatchExecutor> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F04%2Fbatchexecutor.html&linkname=BatchExecutor> "Email")