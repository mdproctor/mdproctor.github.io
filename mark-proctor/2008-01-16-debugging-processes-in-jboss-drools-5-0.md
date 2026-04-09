---
layout: post
title: "Debugging processes in JBoss Drools 5.0"
date: 2008-01-16
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/01/debugging-processes-in-jboss-drools-5-0.html
---

It’s been quiet over the Christmas period and we haven’t shown you too much about the cool stuff we are doing. Never fret this blog will more than make up for it :) Kris Verlaenen has been working his magic again and we now have graphical debug tool for Drools processes, which will be part of the Drools 5.0 release at the end of Q1.

_**The processes**_

Our RuleBase contains 2 processes and some rules (used inside the ruleflow groups):

  * The main process contains some of the most common nodes: a start and end node (obviously), two ruleflow groups, an action (that simply prints a string to the default output), a milestone (a wait state that is trigger when a specific Event is inserted in the working memory) and a subprocess.

![](/legacy/assets/images/2008/01/82b8417e91ad-process_debug_html_77b1dab7.gif)![](/legacy/assets/images/2008/01/82b8417e91ad-process_debug_html_77b1dab7.gif)

  * The SubProcess simply contains a milestone that also waits for (another) specific Event in the working memory.

  * There are only two rules (one for each ruleflow group) that simply print out either a hello world or goodbye world to default output.

I will simulate the execution of this process by starting the process, firing all rules (resulting in the executing of the hello rule), then adding the specific milestone events for both the milestones (in the main process and in the subprocess) and finally by firing all rules again (resulting in the executing of the goodbye rule). The console will look something like this:  
Hello World  
Executing action  
Goodbye cruel world

_**Debugging the process**_

I added four breakpoints during the execution of the process (in the order in which they will be encountered):

  * At the start of the consequence of the hello rule

  * Before inserting the triggering event for the milestone in the main process

  * Before inserting the triggering event for the milestone in the subprocess

  * At the start of the consequence of the goodbye rule

When debugging the application, one can use the following debug views to track the execution of the process:

  * The working memory view, showing the contents (data) in the working memory.

  * The agenda view, showing all activations in the agenda.

  * The global data view, showing the globals.

  * The default Java Debug views, showing the current line and the value of the known variables, and this both for normal Java code _as for rules_.

  * NEW! The process instances view, showing all running processes (and their state).

  * The audit view, showing the audit log.

![](/assets/images/2008/01/582e6306f0cd-process_debug_html_3a85adef.gif)

_Figure: The process instances view, showing that there is currently one running process (instance), currently executing one node (instance), i.e. RuleSet node._

When double-clicking a process instance, the process instance viewer will graphically show the progress of the process instance. At each of the breakpoints, this will look like:

  * At the start of the consequence of the hello rule, only the hello ruleflow group is active, waiting on the execution of the hello rule:

![](/assets/images/2008/01/220d3e475973-process_debug_html_114fa092.gif)

  * Once that rule has been executed, the action, the milestone and the subprocess will be triggered. The action will be executed immediately, triggering the join (which will simply wait until all incomming connections have been triggered). The subprocess will wait at the milestone. So, before inserting the triggering event for the milestone in the main process, there now are two process instances, looking like this:  

![](/assets/images/2008/01/6f9b22d99014-process_debug_html_6fc7e616.gif)![](/assets/images/2008/01/34ed36f439fe-process_debug_html_m7dc9e323.gif)

  * When triggering the event for the milestone in the main process, this will also trigger the join (which will simply wait until all incomming connections have been triggered). So at that point (before inserting the triggering event for the milestone in the subprocess), the processes will look like this:  

> **📷 Missing image** — _process_debug_html_m3ab49a1.gif_

![](/assets/images/2008/01/34ed36f439fe-process_debug_html_m7dc9e323.gif)

  * When triggering the event for the milestone in the subprocess, this process instance will be completed and this will also trigger the join, which will then continue and trigger the goodbye ruleflow group, as all its incomming connections have been triggered. Firing all the rules will trigger the breakpoint in the goodbye rule. At that point, the situation looks like this:  

![](/assets/images/2008/01/77cd15096f33-process_debug_html_m318ba1e2.gif)

After executing the goodbye rule, the main process will also be completed and the execution will have reached the end.

For those who want to look at the result in the audit view, this will look something like this _[Note: the object insertion events might seem a little out of place, which is caused by the fact that they are only logged after (and never before) they are inserted, making it difficult to exactly pinpoint their location_

  

![](/assets/images/2008/01/10dfea1aaaaf-process_debug_html_46539117.gif)