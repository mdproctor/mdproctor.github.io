---
layout: post
title: "Drools Flow and OSWorkflow Migration"
date: 2009-01-27
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/01/drools-flow-and-osworkflow-migration.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Flow and OSWorkflow Migration](<https://blog.kie.org/2009/01/drools-flow-and-osworkflow-migration.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 27, 2009  
[Process](<https://blog.kie.org/category/process>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Hi, my name is Miguel Fossati, I am a developer at Synapsis Argentina, and I am working with Chief Enterprise Architect Diego Naya (author of [Using OSWorkflow in your Application”](<http://www.infoq.com/articles/naya-lazo-osworkflow>)), Maurticio Salatino (A.K.A. Salaboy) and the Drools team in improving Drools Flow. We work together on projects for Argentina’s biggest healthcare provider, who are big OSWorkflow users. However with Drools offering a much more powerful and complete framework, that integrates rules, processes and event processing there is now a desire to move to this as the standard. As part of this effort we need a migration path for al the legacy OSWorkflow applications.

OSWorkflow is an open source workflow tool developed by OpenSymphony, widely used in open source, commercial systems and third party tools (like Jira, and others).

Since Drools Flow, part of up coming Drools 5 release, supports a pluggable node framework for process definitions it’s possible for us to implement other execution models. We are developing a tool to migrate OSWorkFlows processes into Drools Flow process format. This now makes it possible to migrate OSWorkflow processes and definitions to Drools. We expect this tool to be very useful for developers and users that want to migrate their existing OSWorkflow based systems, to take advantage of the Drools Flow process capabilities.

We have extended the underlying nodes framework adding a Step node to fully support OSWorkflow’s step concept. In OSWorkflow a Step node is a kind of a wait state that have some actions to take and move to another step. It supports conditional actions that implements OSWorkflow’s Condition contract, and execution of functions via the FunctionProvider interface. It also supports Split and Join nodes using the native RuleFlow Split and Join nodes.

Lets see an example, starting with this simple OSWorkflow definition:
[code]
    &LT;workflow&GT;  
        &LT;initial-actions&GT;  
            &LT;action id="1" name="Start Workflow"&GT;  
                &LT;results&GT;  
                    &LT;unconditional-result old-status="Finished"  
                        status="Queued" step="1" /&GT;  
                &LT;/results&GT;  
            &LT;/action&GT;  
        &LT;/initial-actions&GT;  
        &LT;steps&GT;  
            &LT;step id="1" name="First Draft"&GT;  
                &LT;actions&GT;  
                    &LT;action id="2" name="Start First Draft"&GT;  
                        &LT;restrict-to&GT;  
                            &LT;conditions&GT;  
                                &LT;condition type="class"&GT;  
                                    &LT;arg name="class.name"&GT;  
                                        com.opensymphony.workflow.util.StatusCondition  
                                    &LT;/arg&GT;  
                                    &LT;arg name="status"&GT;Queued&LT;/arg&GT;  
                                &LT;/condition&GT;  
                            &LT;/conditions&GT;  
                        &LT;/restrict-to&GT;  
                        &LT;pre-functions&GT;  
                            &LT;function type="class"&GT;  
                                &LT;arg name="class.name"&GT;  
                                    com.opensymphony.workflow.util.Caller  
                                &LT;/arg&GT;  
                            &LT;/function&GT;  
                            &LT;function type="beanshell"&GT;  
                                &LT;arg name="script"&GT;  
                                    System.out.println("Before executing actionid 2");  
                                &LT;/arg&GT;  
                            &LT;/function&GT;  
                        &LT;/pre-functions&GT;  
                        &LT;results&GT;  
                            &LT;unconditional-result old-status="Finished"  
                                status="Underway" step="1" owner="${caller}" /&GT;  
                        &LT;/results&GT;  
                    &LT;/action&GT;  
                    &LT;action id="3" name="Finish First Draft"&GT;  
                        &LT;restrict-to&GT;  
                            &LT;conditions type="AND"&GT;  
                                &LT;condition type="class"&GT;  
                                    &LT;arg name="class.name"&GT;  
                                        com.opensymphony.workflow.util.StatusCondition  
                                    &LT;/arg&GT;  
                                    &LT;arg name="status"&GT;Underway&LT;/arg&GT;  
                                &LT;/condition&GT;  
                                &LT;condition type="class"&GT;  
                                    &LT;arg name="class.name"&GT;  
                                        com.opensymphony.workflow.util.AllowOwnerOnlyCondition  
                                    &LT;/arg&GT;  
                                &LT;/condition&GT;  
                            &LT;/conditions&GT;  
                        &LT;/restrict-to&GT;  
                        &LT;results&GT;  
                            &LT;unconditional-result old-status="Finished"  
                                status="Queued" step="2" /&GT;  
                        &LT;/results&GT;  
                    &LT;/action&GT;  
                &LT;/actions&GT;  
            &LT;/step&GT;  
            &LT;step id="2" name="finished" /&GT;  
        &LT;/steps&GT;  
    &LT;/workflow&GT;
[/code]

Our Drools Flow definition matching the above would be like this:
[code]
    &LT;process xmlns="http://drools.org/drools-4.0/osworkflow"  
             xmlns:xs="http://www.w3.org/2001/XMLSchema-instance"  
             xs:schemaLocation="http://drools.org/drools-4.0/osworkflow drools-osworkflow-4.0.xsd"  
             type="OSWorkflow" name="simple" id="simple" package-name="org.drools.osworkflow" &GT;  
      
      &LT;header&GT;  
          &LT;initial-actions&GT;  
            &LT;action id="1" name="Start Workflow"&GT;  
                &LT;results&GT;  
                    &LT;unconditional-result old-status="Finished"  
                        status="Queued" step="1" /&GT;  
                &LT;/results&GT;  
            &LT;/action&GT;  
        &LT;/initial-actions&GT;  
      &LT;/header&GT;  
         
      &LT;nodes&GT;  
        &LT;step id="1" name="First Draft" &GT;  
          &LT;action id="2" name="Start First Draft"&GT;  
            &LT;restrict-to&GT;  
              &LT;conditions&GT;  
                &LT;condition type="class"&GT;  
                  &LT;arg name="class.name"&GT;  
                                        com.opensymphony.workflow.util.StatusCondition  
                                    &LT;/arg&GT;  
                  &LT;arg name="status"&GT;Queued&LT;/arg&GT;  
                &LT;/condition&GT;  
              &LT;/conditions&GT;  
            &LT;/restrict-to&GT;  
            &LT;pre-functions&GT;  
              &LT;function type="class"&GT;  
                &LT;arg name="class.name"&GT;  
                                    com.opensymphony.workflow.util.Caller  
                                &LT;/arg&GT;  
              &LT;/function&GT;  
              &LT;function type="beanshell"&GT;  
                &LT;arg name="script"&GT;&LT;![CDATA[  
                                    System.out.println("Before executing actionid 2");  
                                ]]&GT;&LT;/arg&GT;  
              &LT;/function&GT;  
            &LT;/pre-functions&GT;  
            &LT;results&GT;  
              &LT;unconditional-result old-status="Finished" status="Underway" step="1" owner="${caller}"/&GT;  
            &LT;/results&GT;  
          &LT;/action&GT;  
          &LT;action id="3" name="Finish First Draft"&GT;  
            &LT;restrict-to&GT;  
              &LT;conditions type="AND"&GT;  
                &LT;condition type="class"&GT;  
                  &LT;arg name="class.name"&GT;  
                                        com.opensymphony.workflow.util.StatusCondition  
                                    &LT;/arg&GT;  
                  &LT;arg name="status"&GT;Underway&LT;/arg&GT;  
                &LT;/condition&GT;  
                &LT;condition type="class"&GT;  
                  &LT;arg name="class.name"&GT;  
                                        com.opensymphony.workflow.util.AllowOwnerOnlyCondition  
                                    &LT;/arg&GT;  
                &LT;/condition&GT;  
              &LT;/conditions&GT;  
            &LT;/restrict-to&GT;  
            &LT;results&GT;  
              &LT;unconditional-result old-status="Finished" status="Queued" step="2"/&GT;  
            &LT;/results&GT;  
          &LT;/action&GT;  
        &LT;/step&GT;  
            &LT;step id="2" name="finished" &GT;  
        &LT;/step&GT;  
      &LT;/nodes&GT;  
      &LT;connections&GT;  
        &LT;connection from="1" fromType="3" to="2" toType="Queued" /&GT;  
      &LT;/connections&GT;  
    &LT;/process&GT;
[/code]

Persistence is currently managed by a mix of JPA and a Serialization process that store the status of the process inside a relational schema that is updated every time the process reach a wait state, taking out of memory the current processInstance until someone else interacts with the process. This persistence strategy is beeing extended but at the moment you can use it with the SingleCommandSessionService.

To run our process, we first build our knowledge base, as any native Drools flow:
[code]
                // create a builder  
                PackageBuilder builder = new PackageBuilder();  
                // load the process  
                Reader source = new InputStreamReader(this.getClass().getResourceAsStream(resourceName));  
                builder.addProcessFromXml(source);  
                // create the knowledge base  
                Package pkg = builder.getPackage();  
                RuleBase ruleBase = RuleBaseFactory.newRuleBase();  
                ruleBase.addPackage(pkg);  
    
[/code]

As you can see here we load our process in the working memory, exactly in the same way that we load a RuleFlow process.

When we want to interact with the process we must use the SingleSessionCommandService to execute commands that influence our process to jump from one step to another.  
This SingleSessionCommandService is configured with a JPA session that store the status of process when it reachs a wait state.

Here we start an instance of our process using the ID of the process, in this case “simple”, this will execute the OSWorkflow initial actions and point the execution of the process to the first step node called “First Draft”.
[code]
            SingleSessionCommandService service = new SingleSessionCommandService(ruleBase);  
            StartProcessCommand startProcessCommand = new StartProcessCommand();  
            startProcessCommand.setProcessId("simple");  
            ProcessInstance processInstance = (ProcessInstance) service.execute(startProcessCommand);  
            System.out.println("Started process instance " + processInstance.getId());  
      
            service = new SingleSessionCommandService(ruleBase);  
            GetProcessInstanceCommand getProcessInstanceCommand = new GetProcessInstanceCommand();  
            getProcessInstanceCommand.setProcessInstanceId(processInstance.getId());  
            processInstance = (ProcessInstance) service.execute(getProcessInstanceCommand);  
            System.out.println("Now working with processInstance " + processInstance.getId());
[/code]
[code]
               Now we want to execute an action to move to another step node in the workflow, so we use the command DoActionCommand to tell the process that we want to move to the next node. In this stage, the process will be retrieved from the database and a deserialization process of the processInstance status will take place. After this deserialization the action will be executed and the execution of the process will reach the next step. When the execution enter in the new step the process waits until someone execute another action, so the process will be persisted again.<pre>        service = new SingleSessionCommandService(ruleBase);<br />        DoActionCommand doActionCmd = new DoActionCommand();<br />        doActionCmd.setProcessInstanceId(processInstance.getId());<br />        doActionCmd.setActionId(2); //Action to be executed at current step<br />        service.execute(doActionCmd);      <br /></pre>Please, feel free to test this tool, and provide feedback that will help us improve it. This work is currently in a branch and will be merged into Drools trunk this week, we will announce in the blog once that merge is complete and ready for testing.
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-flow-and-osworkflow-migration.html&linkname=Drools%20Flow%20and%20OSWorkflow%20Migration> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-flow-and-osworkflow-migration.html&linkname=Drools%20Flow%20and%20OSWorkflow%20Migration> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-flow-and-osworkflow-migration.html&linkname=Drools%20Flow%20and%20OSWorkflow%20Migration> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-flow-and-osworkflow-migration.html&linkname=Drools%20Flow%20and%20OSWorkflow%20Migration> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-flow-and-osworkflow-migration.html&linkname=Drools%20Flow%20and%20OSWorkflow%20Migration> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-flow-and-osworkflow-migration.html&linkname=Drools%20Flow%20and%20OSWorkflow%20Migration> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F01%2Fdrools-flow-and-osworkflow-migration.html&linkname=Drools%20Flow%20and%20OSWorkflow%20Migration> "Email")