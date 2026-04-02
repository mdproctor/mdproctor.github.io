---
layout: post
title: "A Vision for Unified Rules and Processes"
date: 2007-11-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/11/a-vision-for-unified-rules-and-processes.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [A Vision for Unified Rules and Processes](<https://blog.kie.org/2007/11/a-vision-for-unified-rules-and-processes.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- November 19, 2007  
[Process](<https://blog.kie.org/category/process>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Since Drools 4.0 I’ve been demonstrating our ruleflow stuff, which includes a graphical designer and basic rules and process integration for stateful rule orchestration. What is ruleflow? Ruleflow is the integration of rules and processes, which can predominantly be used to orchestrate the execution of rules. Additionally what 4.0 also provides is a prototype to prove that we don’t need to have a process oriented or a rule oriented view of the world. I believe that any company that isn’t able to truly unify rules and processes into a single modelling system, how PegaSystems have done, will not be in a suitable position for the future – actually Microsoft get this too with their Workflow Foundations offering, although their rule offering is still very weak. Typically the market has a strong process company with weak rules, or strong rules with weak processes – rules and processes must exist as first class citizens within the modelling and execution environment. The current “modus operandi” for the rule industry is a focus on stateless decision services, where the separate workflow engine at some point calls out to the separate stateless rule engine to assist in some decision making – after 30 years of research and development is that the best we have to offer, multi-million pound license deals that effectively boil down to glorified spreadsheets called via a stateless web services from some workflow engine. Not to mock this model, as it is actually quite useful, but this level of integration is superficial at most and we need to make sure that we unify these models and allow it to go to much greater depths. Once rules and processes are fully integrated that modelling environment will benefit from any other declarative systems added, such as our plans to add Complex Event Processing (CEP) to the engine and language – this means we can have rules monitoring streams of data and triggering process milestones.

[![](/legacy/assets/images/2007/11/cdeffe71ba87-clinical-pathway.png)](<http://bp3.blogger.com/_Jrhwx8X9P7g/R0HGHfGnhsI/AAAAAAAAAG8/tpj95IV8NA8/s1600-h/clinical-pathway.png>)  
Drools 4.0 ruleflow diagram

Partly the reason for the rule industry flocking to this model of stateless decision services is their existing tech is hard to understand and implement and thus more difficult to sell, decision services are simple to understand and thus easier toimplement and sell – it’s the rule engine industry’s stab at trying to grow their measly market share, compared to the workflow industry.

The jBPM team have put out their vision of the “[Process Virtial Machine](<http://docs.jboss.com/jbpm/pvm/>)” (PVM), but it is a process centric vision. The PVM was a term used by Tom Baeyens, in the linked paper, to present the idea of a generic engine for executing different process models, the “virtual machine” term may not be totally appropriate, and already irks some purists, but we have continued with this terminology for mean while – so we can get apples to oranges comparisons, instead of apples to giraffes :) Mike Brock suggests that Virtual Process Engine, or Generic Process Engine – I prefer something away from the terms process and rules, to something that focuses on the unified modelling concepts, so hopefully someone out there can put in an argument for something more appropriate :)

What we lay out here is what we have started to put in place with Drools, our vision of a PVM+ with rules and processes as first class citizens, tightly integrated modelling GUIs, single unified engine and apis for compilation/building, deployment and runtime execution.

So with the base PVM in place what we are working on now? We’ll we still have a lot to do, I’ve found our compilation framework is too coupled to rules, so I’m busy trying to refactor this so it can compile and build both rules and actions. The engine variables are currently only scoped at two levels, globals and rules; we need to make sure that we can scope variables by both process and sub process, and have the rules executed in those processes also scoped to that level. I need to extend our concept of a rule “duration”, which is basically a simple timer, to allow for cron type definitions and allow rules to execute each time, if its still true – this will allow for rich conditional timers. I have plans for stateful high availability, via JBoss Cache, and also I need to put in an optimal framework for persistence and restoring – ideally I want all this done, and more by Q1 :) We do not plan to do the BPEL, BPM etc layers and instead hope the jBPM team will become consumers of our tech, and also core developers (a joining of the two teams), and work on these parts of the domain.

The rest of this blog is a small paper put together by our ruleflow lead Kris Verlaenen, but exemplifies the whole Drool’s team vision and commitment to declarative programming, via multiple modelling paradigms – no one tool fits all solutions.

The Process Virtual Machine (PVM)  
This is an attempt to clarify our vision on an integrated approach for modelling business logic using rules and processes on top of the Drools Platform. It is intended to serve as a glossary, to create a common set of terms that might help in simplifying future discussions and creating a combined vision regarding this matter.

Figure 1 shows an overview of our approach to unify rules and processes by integrating a powerful process virtual machine (PVM+) into the Drools Platform. This allows us to support the execution of rules as well as the execution of processes based on this PVM+ within the Drools Platform. We believe that creating a unified approach for handling rules and processes (for the end user) will result in a much more powerful business logic system than what can be achieved by simply linking separate rules and workflow products. It will also allow us to create a lot of additional services on top of this unified platform (IDE, web-based management system, etc.), which can then be applied easily for both rules and processes, giving a much more unified experience for the end users of the platform. Each of the terms used in the figure will be explained in more detail in the subsequent sections.

[![](/legacy/assets/images/2007/11/09aeaeb55a59-pvm.png)](<http://bp0.blogger.com/_Jrhwx8X9P7g/R0G2kvGnhrI/AAAAAAAAAG0/lWWRbIKCARk/s1600-h/pvm.png>)Figure 1

PVM  
The Process Virtual Machine defines a common model that supports multiple process models. It is the basis for implementing workflow process models, and their implementation. It represents a state machine that can be embedded into any software application. Therefore it defines:

  * A process (definition) model: Defines concepts like a process, variables, nodes, connections, work definitions, etc.
  * A runtime model: Runtime instances corresponding to each of the elements in the process model, like process instance, variable instance, node instance, work item, etc.
  * API: Process instances can be started, aborted, suspended, the value of variable instances can be retrieved, work items can be completed or aborted, etc.
  * Services: The PVM also implements (non-functional) services which are useful for most process language implementations, like persistence, transaction management, asynchronous continuations, etc. These services should all be pluggable (do not have to be used, minimal overhead if not used) and configurable (different strategies could be used for each of these services, this should be configurable and extensible so people can plug in their own implementation).

On top of this process model, the PVM also defines/shows how to use the concepts of process (instance), node (instance), connection, etc. to implement common workflow patterns (in control flow, data, resource, exceptions) like a sequence of nodes, parallelism, choice, synchronization, state, subprocess, scoped variables, etc. These node implementations can be used as a basis for implementing different process languages.

PVM+  
Extends the PVM and integrates it into the Drools Platform. This allows:

  * Integration of rules and processes: Processes can include (the power of) rules in their process model whenever appropriate, e.g. split decisions, assignment of actors to work items, rules as expression language, etc. vice-versa, rules can start processes during their execution.
  * Processes and rules share one common data contextl, no need to integrate two (or more) different systems, continuously pass information between those two systems, synchronize data, etc.
  * Processes (and rules) can use other functionality that is offered by the Drools Platform: a unified audit system, unified API to start processes / rules, single build and deployment infrastructure etc.
  * One engine session can execute multiple different process instances in parallel, where each process can interact with the other processes and rules via changes to the shared variable context.

This PVM+ also defines additional node implementations that show the power of integrating rules and processes and how that power can be used inside a process model, e.g. choice using rules to evaluate conditions, milestones (a state where rules decide when to progress to the next state), timers with built in conditionals, actions supporting pluggable dialects, etc.

Specific workflow languages  
On top of the PVM+, different (domain-)specific workflow languages can be implemented:

  * jPDL: the general purpose, expressive workflow language for the Java developer
  * PageFlow: workflow language for specifying the control flow in web pages
  * RuleFlow: a workflow language for specifying the order in which large rule sets should be
  * evaluated
  * WS-BPEL: an implementation of the WS-BPEL standard for web service orchestration
  * …

These languages each define a process model and implementation for each of their nodes. These  
implementations will be based in a lot of cases on (a combination of) common node implementations of the PVM(+).

Pluggability: New node implementations can be added to existing process languages, existing  
process languages can be extended with new functionality (e.g. time constraints), or entirley new process languages can be plugged in into the PVM+.

Work Definitions  
All communication with the external world is handled by using work items, which are an abstract representation of a unit of work that should be executed. Work item handlers are then responsible for executing these work items whenever necessary during the execution of a process instance. This approach has the following advantages:

  * A much more declarative way of programming, where you only define what should executed (using an abstract work item), not how (no code)
  * Hides implementation details
  * Different handlers can be used in different contexts:
    * A workflow can be reused without modifications in different runtime execution contexts (e.g. different companies or different hospitals in the context of clinical workflow) by creating custom handlers for each of these settings
    * A workflow can behave differently depending on its stage in the life cycle. For example, for testing, handlers that do not actually do anything but simply test the execution of the workflow could be registered. For simulation, some visualization of the work items that should be executed, and the possibility for the person doing the simulation to complete/abort these work items is possible.
  * Work item definitions and handler implementations can be reused across nodes, across  
processes, and even across process models.

The different work items that are available in a specific workflow languages should be defined (by defining a unique id for that type of work item, and parameters for that work item). Different sets of work definitions can be defined:

  * Generic work definitions (and their handler implementation) can be defined for common  
task that might be useful in different workflow languages, e.g. related to communication  
(sending a mail, SMS, etc.), invoking a web service, logging a message, etc.
  * People can define their own domain-specific work items (and their handler implementation), which can then be used for modeling processes in that domain. For example, a clinical workflow language could define work items like “nursing order”, “medication order”, “contact general practitioner”, etc.

Extensions  
When a unified approach to processes and rules is used, as part of the Drools Platform, extensions on top of these concepts and APIs can easily be reused for all rules and process  
languages:

  * Eclipse-based IDE supports developing applications on top of the Drools Platform  
supporting the use of rules and processes. This IDE includes
    * a graphical workflow editor
    * unified error handling
    * integrated debugging
    * unified simulation
    * pluggability of process languages, custom property panels, etc.
    * …
  * B(R)MS: Business (Rules) Management System, a web-based application that serves as the repository for all business knowledge. Supports unified packaging, versioning, management, quality assurance, etc.
  * Security management: who is allowed to perform which operations on the Drools Platform.
  * (Human) task list management component that can be shared across rules and process  
languages, for integrating human tasks.
  * Reasoning on business logic, which is a combination of all rules and processes of a business.

[![](/legacy/assets/images/2007/11/58e0d9444a2b-pluggeable-work-items.png)](<http://bp1.blogger.com/_Jrhwx8X9P7g/R0HPu_GnhtI/AAAAAAAAAHE/bOH-mHZr078/s1600-h/pluggeable-work-items.png>)  
Pluggable work items (currently in svn trunk)

I’ll be at [Javapolis ](<http://www.javapolis.com/>)this year presenting a BOF on the concepts of [Declarative Programming with Rules, Processes and CEP](<http://www.javapolis.com/confluence/display/JP07/Declarative+programming+with+rules%2C+processes+and+cep>) which will cover most of this blog and more. The BOF is on Monday 10th from 21:00 to 22:00. So please do come along, if you want to talk about this in more detail.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F11%2Fa-vision-for-unified-rules-and-processes.html&linkname=A%20Vision%20for%20Unified%20Rules%20and%20Processes> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F11%2Fa-vision-for-unified-rules-and-processes.html&linkname=A%20Vision%20for%20Unified%20Rules%20and%20Processes> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F11%2Fa-vision-for-unified-rules-and-processes.html&linkname=A%20Vision%20for%20Unified%20Rules%20and%20Processes> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F11%2Fa-vision-for-unified-rules-and-processes.html&linkname=A%20Vision%20for%20Unified%20Rules%20and%20Processes> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F11%2Fa-vision-for-unified-rules-and-processes.html&linkname=A%20Vision%20for%20Unified%20Rules%20and%20Processes> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F11%2Fa-vision-for-unified-rules-and-processes.html&linkname=A%20Vision%20for%20Unified%20Rules%20and%20Processes> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F11%2Fa-vision-for-unified-rules-and-processes.html&linkname=A%20Vision%20for%20Unified%20Rules%20and%20Processes> "Email")