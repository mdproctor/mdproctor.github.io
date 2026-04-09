---
layout: post
title: "Drools and WS-HumanTask"
date: 2008-09-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/09/drools-and-ws-humantask.html
---

I’ve previously blogged about how Drools is becoming a Business Logic integration Platform that unifies rules, work flow and event processing. An important aspect of work flow is human task management, which to date has been missing in our efforts. Kris Verlaenen, the Drools Flow lead and general evil genius, did a review of the various specs and other non-standard implementations. As it turns out the WS-Humantask (WSHT) spec is pretty decent and comprehensive, the pdf can be found [here](<http://download.boulder.ibm.com/ibmdl/pub/software/dw/specs/ws-bpel4people/WS-HumanTask_v1.pdf>), so when thinking about implementing this feature for Drools it made sense to base it on WSHT rather than a proprietary implementation such as the one found in jBPM. WSHT has become an oasis standard, which InfoQ covered back in january [“BPEL4People and WS-HumanTask Head To OASIS”](<http://www.infoq.com/news/2008/01/bpel4people-oasis>).

Kris has been busy working away on a implementation of WSHT and it’s almost at a usable stage, for now he has taken a more practical approach to this to deliver something that we can use for Drools, rather than just aiming for WSHT compliance. Although we do hope to eventually make this fully WSHT compliant, hopefully someone from the community can help us from that side.

The class model, which is made persistable through EJB3, is close to complete and able to represent the whole of WSHT – except for the presentation elements, which I have left off for now, these can be easily added later but we don’t have much use for them yet.

For now we have chosen to do ignore the WS aspect and focus on a [apache mina](<http://mina.apache.org/>) based client/server architecture this allows us to create a simpler and lower latency implementation for integration with our runtime and tooling, easily supports p2p and is more easily embeddable as mina is just a small JAR. The last one is important as the WSHT server needs to message events to running clients, who are typically in a wait state.

The spec does not specify anything about iCalendar notifications, so kris has added this anyway. So now when someone claims a task they get two iCalendar emails one for the first start date and one for the last start date. iCalendar VEvents was chosen over the more symantically correct VTodo as there doesn’t seem to be much support for the later – neither gmail or zimbra can detect a VTodo sent via an email. Maybe over time we can make this configurable and users can specify whether they want events or todos.

Typically a Task has a start by date and an end by date, WSHT allows for multiple start deadlines and multiple end deadlines. Each deadline can have zero or more escalations that result in a re-assignment or a notification. WSHT doesn’t specificy what form the notification takes place, this is one of their extension points. We have hooked up the notification system to integrate with our existing “work items” framework, initially with the email work item. Work items are pre made units of re-usable code, typically with GUI configuration in the flow editor, for executing actions. Later we could include a JMS or WS notification, leveraging any pre-made work items we have made.

A Task can be in one of the following states:  
Created, Ready, Reserved, In Progress, Completed

And supports the following main actions:  
Create, Claim, Start, Stop, Release, Suspend, Skip, Resume, Delegate, Forward, Complete, Fail.

WSHT supports the following role types, which it refers to as People Assignments:  
Task Initiator, Task Owner, Potential Owners, Business Administrators, Excluded Owners, Recipients, Task Stakeholders.

To get an understanding of how the WSHT life cycle works with the various allowed operations the spec [pdf](<http://download.boulder.ibm.com/ibmdl/pub/software/dw/specs/ws-bpel4people/WS-HumanTask_v1.pdf>) provides this state transition diagram which hopefully makes it all clear.

[![](/legacy/assets/images/2008/09/6a77f05f10ee-WSHT-lifecycle.png)](</assets/images/2008/09/c3d54bc88997-WSHT-lifecycle.png>)WSHT Lifecycle from spec [PDF](<http://download.boulder.ibm.com/ibmdl/pub/software/dw/specs/ws-bpel4people/WS-HumanTask_v1.pdf>)

The Drools Task code currently lives [here,](<http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/drools-process/drools-process-task/>) while the WSHT client/server implementation is close to complete the tooling integration will be minimal for 5.0 due to time constriants. We hope to quickly crank that up to make the tooling in eclipse and the Guvnor BRMS feature full. This is a great project for anyone wanting to get involved as it’s relatively self contained and thus straight forward and no complex algorithms :) Things to do include full WSHT compliance, improved tooling including various extensions like inbox style views that support task labelling and also “read” status.

For now here is a simple screenshot showing some of the minimal Task tooling integration into Eclipse.

[![](/legacy/assets/images/2008/09/dbb1fb52df5d-TaskView.png)](</assets/images/2008/09/6d078b5dc2da-TaskView.png>)