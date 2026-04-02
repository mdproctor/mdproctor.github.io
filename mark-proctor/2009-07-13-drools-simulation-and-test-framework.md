---
layout: post
title: "Drools Simulation and Test framework"
date: 2009-07-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/07/drools-simulation-and-test-framework.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Simulation and Test framework](<https://blog.kie.org/2009/07/drools-simulation-and-test-framework.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 13, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’ve just got the initial Simulation and Testing framework working with JUnit integration :) Although still lots to do.

It allows Simulations to be run, with tests, for complex apps that involve rules, workflow and event processing all working together over time. This really shows of the Business Logic integration Platform (BLiP) concept and why people should be thinking about using Drools. Rather than the more traditional three different standalone engines with poor integration and totally different approaches, forcing you into a “process oriented” or “rules oriented” world.

[![](/legacy/assets/images/2009/07/39bd31e85331-simulation.jpg)](<http://2.bp.blogspot.com/_Jrhwx8X9P7g/SlqsjbXAxtI/AAAAAAAAAW0/JN9LdxlRqJc/s1600-h/simulation.jpg>)

When testing your business logic unit tests are not ideal. What you really want to be doing is testing the behaviour of your business logic, to do this you need to execute it in a Simulation environment. Drools 5.0 already has basic simulation and testing in the Guvnor QA tab, however it is not time aware and is specific to rules. By time aware I mean that it creates a session, inserts the facts and just lets it run and then checks the results at the end. For simulation we need to be able to execute specific actions at specific points of time while being able to assert on the engine data (inserted objects, globals and process variables, etc) or the engine state itself (agenda, process instances, etc) at given points in time.

The Simulator runs the Simulation. The Simulation is your scenario definition. The Simulation consists of 1 to n Paths, you can think of a Path as a sort of Thread. The Path is a chronological line on which Steps are specified at given temporal distances from the start. You don’t specify a time unit for the Step, say 12:00am, instead it is always a relative time distance from the start of the Simulation. Each Step contains one or more Commands, i.e. create a StatefulKnowledgeSession or insert an object or start a process.
[code]
    1..1 Simulation  
         1..n Paths  
                 1..n Steps  
                        1..n Commands
[/code]

All the steps, from all paths, are added to a priority queue which is ordered by the temporal distance, and allows us to incrementally execute the engine using a time slicing approach. The simulator pops of the steps from the queue in turn. For each Step it increments the engine clock and then executes all the Step’s Commands.

Example Command (notice it uses the same Commands as used by the CommandExecutor):
[code]
    new InsertObjectCommand( new Person( "darth", 97 ) )
[/code]

Commands can be grouped together, especially Assertion commands, via test groups. The test groups are mapped to JUnit “test methods”, so as they pass or fail using a specialised JUnit Runner the Eclipse GUI is updated – as illustrated in the above image, showing two passed test groups named “test1” and “test2”.

Using the JUnit integration is trivial. Just annotate the class with @RunWith(JUnitSimulationRunner.class). Then any method that is annotated with @Test and returns a Simulation instance will be invoked executing the returned Simulation instance in the Simulator. As test groups are executed the JUnit GUI is updated.

To make a Simulation more flexible Contexts are used, which provide key/value pair lookups. Each Path has it’s own Context, which inherits from a root “global” Context. Commands are executed against given Context identifiers. This allows a Simulation to have a number of ksessions or kbases for maximum flexibility, and Command adapter is used to make the Commands aware. I apologise in advance for the long name used in the adapter class, couldn’t think of a shorter name at the time and will refactor later :)

Creates a KnowledgeBase and assigns it to the the identifier “kbase” in the Context for “path1”:
[code]
    cmds.add( new SetVariableCommand( "path1",  
                                    "kbase",  
                                     new NewKnowledgeBaseCommand( null ) ) );
[/code]

Creates a StatefulKnowledgeSession and assigns it to the identifier “ksession” in the Context for “path1”. The KnowledgeContextResolveFromContextCommand adapts the targeted Command telling it that the KnowledgeBase to be used for the command can be retrieved from the Context using the identifier “kbase”. The null arguments could be used to specify a KnowledgeBuilder of StatefulKnowledgeSession if the Command required it:
[code]
    cmds.add( new SetVariableCommand( "path1",  
                                    "ksession",  
                                    new KnowledgeContextResolveFromContextCommand(  
      new NewStatefulKnowledgeSessionCommand( ksessionConf ),  
      null,  
      "kbase",  
      null ) ) );
[/code]

Now that we have the StatefulKnowledgeSession assigned to the “ksession” identifier we can insert objects into it. Again we used the adapter command to tell it to execute the InsertObjectCommand using the “ksession” instance – the null arguments are the positions used to specify a Knowledgebuilder or KnowledgeBase if the Command required it:
[code]
    cmds.add( new KnowledgeContextResolveFromContextCommand(  
                new InsertObjectCommand( new Person( "yoda", 98 ) ),  
                null,  
                null,  
                "ksession" ) );
[/code]

While the identifier manipulation Commands and Command adapters add a fair amount of verbosity to the api, they also create a very flexible Simulation environment. Tooling will be added that will hide this verbosity and reduce complexity, making it much more palatable.

While it all now works from an API perspective and JUnit integration, building a Simulation programmatically can be a bit verbose. So my next task is to update the existing Command XML, as discussed [here](<http://blog.athico.com/2009/04/batchexecutor.html>), to support the simulation, so that simulations can be defined purely in XML. At the same time we are working on an excel/open office front end to allow simulations to be defined with a Tabular metaphor which I hope should prove very popular.

What’s great about this is that it starts to show off the value of the foundations we have built, for rules, workflow and event processing as part of our Business Logic integration Platform (BLiP) concept. Starting first with the unified clock. Drools has single clock for time and scheduling that is pluggable. By default it’s a realtime clock based off the JVM system clock. The simulation however switches this to the pseudo clock, allowing programmatic control of time. This allows the Simulator to control the time increments, as based in the Simulation definition. Imagine trying to do this across three different engines. You’d have to hope they had pluggable clock strategies and supported programmatic control before you even started writing 3 different pieces of code to try and correlate the time increases across the engines. Then we have the Command sets that we had already written for interacting with Drools as a service via a “scripting approach – these Commands where especially written to allow the control and mapping of return data and work with rules, workflow and event processing. We can re-use and build on these Commands, and their XML representation, as the foundations of our instruction set for the Simulation definition. Finally there is our general philosophy of rules, workflow and event processing as first class citizens with a seamless and unified approach which ensures we always think about how these technologies work together to give the best possible user experience. As always Drools allows you to do more, by doing less

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F07%2Fdrools-simulation-and-test-framework.html&linkname=Drools%20Simulation%20and%20Test%20framework> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F07%2Fdrools-simulation-and-test-framework.html&linkname=Drools%20Simulation%20and%20Test%20framework> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F07%2Fdrools-simulation-and-test-framework.html&linkname=Drools%20Simulation%20and%20Test%20framework> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F07%2Fdrools-simulation-and-test-framework.html&linkname=Drools%20Simulation%20and%20Test%20framework> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F07%2Fdrools-simulation-and-test-framework.html&linkname=Drools%20Simulation%20and%20Test%20framework> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F07%2Fdrools-simulation-and-test-framework.html&linkname=Drools%20Simulation%20and%20Test%20framework> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F07%2Fdrools-simulation-and-test-framework.html&linkname=Drools%20Simulation%20and%20Test%20framework> "Email")