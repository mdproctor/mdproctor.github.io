---
layout: post
title: "Creating a DSL for WS-HumanTask and when not to use a Rule Engine"
date: 2008-09-24
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/09/creating-a-dsl-for-ws-humantask-and-when-not-to-use-a-rule-engine.html
---

As [previous discussed](<http://blog.athico.com/2008/09/drools-and-ws-humantask.html>) Drools is building a task system based on [oasis](<http://www.oasis-open.org/home/index.php>) spec [WS-HumtanTask (WSHT)](<http://download.boulder.ibm.com/ibmdl/pub/software/dw/specs/ws-bpel4people/WS-HumanTask_v1.pdf>). The spec has a number of operations to control the status of the task for a defined life cycle, where only certain people execute an operation based on given permissions. For a quick recap WSHT supplies the following:

A Task can be in one of the following states:  
Created, Ready, Reserved, In Progress, Completed

And supports the following main actions:  
Create, Claim, Start, Stop, Release, Suspend, Skip, Resume, Delegate, Forward, Complete, Fail.

WSHT supports the following role types, which it refers to as People Assignments:  
Task Initiator, Task Owner, Potential Owners, Business Administrators, Excluded Owners, Recipients, Task Stakeholders.

Already it’s obvious that we have rules and flow involved here. To give you an idea of the business logic involved lets look over some of them now – obviously the spec [pdf](<http://download.boulder.ibm.com/ibmdl/pub/software/dw/specs/ws-bpel4people/WS-HumanTask_v1.pdf>) has the complete set of business logic. The task starts off as Created and then moves to Ready where it can transition to Reserved or InProgress depending if the operation is claim or start. Only potential owners or business administrators may claim or start a task. Once in progress only the owner can fail or complete it. Potential owners can only forward a task if it has a status of Ready, once Reserved or In Progress only the owner or business administrator can forward it, further to that the person forwarding must be specified explicitly in the permission and not implicitly as part of some group.

The first thing that came to mind was “great we can model this with rules and flow using Drools” and after some thought I decided that Flow was a bit over kill for this as the flow was quite basic. Also flow diagrams can obscure the business logic, making you need to inspect each node to get a full understanding of the logic; if the flow is simple I think I’d prefer something that made the business logic more obvious. So I decided to defined a DSL that would define both the flow and the rules in a single way, that was also “self documenting” and that made it obvious what could be done where. I decided to use [MVEL](<http://mvel.codehaus.org/>) to model the DSL, as it allows for compact and minimal syntax when creating large graph objects. So lets look at what this DSL would look like.

We know that we first have an operation command (claim, start, stop, etc) and that those operations are only valid when the task is in given status, someone can only claim a task that is in the status Ready. Further to that we have allowed permissions, who can execute that task for the given status, only potential owners or business administrators may claim a task and then we have the resulting new status, which in this case would be Reserved, and the owner of the task must be set to the new user.

I first create the enum Operation which has entries for each possible operations (claim, start, stop, etc). I also create an enum Allowed which lists the different types of people/groups that may have permission for the operation (owner potential owner, business administrator). Then I create an OperationCommand object that will encapsulate the desired business logic in a declarative manner. As a start that OperationCommand would have the following fields:

```java
public class OperationCommand
List status;
List allowed;
Status newStatus;
boolean setNewOwnerToUser;
```

So using the above we can use MVEL to declare the first entry for our DSL:

```
[   Operation.Claim
    : [ new OperationCommand().{
            status = [ Status.Ready ],
            allowed = [ Allowed.PotentialOwner, Allowed.BusinessAdministrator ],
            setNewOwnerToUser = true,       
            newStatus = Status.Reserved
        } ]
]
```

Notice MVEL uses the “.” suffix to allow in-line “with” field accessors for very compact syntax. What the above says is that we have a Map of possible operations and each key has an array of possible OperationCommands. In the above case there is only one possible status Claim can execute on and that is Ready.

Now we know that Start can be called while the task is in status Ready or Reserved, so lets look at that DSL entry:

```
[    Operation.Start
    : [ new OperationCommand().{
            status = [ Status.Ready ],
            allowed = [ Allowed.PotentialOwner ],
            setNewOwnerToUser = true,          
            newStatus = Status.InProgress
        },
        new OperationCommand().{
            status = [ Status.Reserved ],
            allowed = [ Allowed.Owner ],      
            newStatus = Status.InProgress
        } ]
]
```

See the difference? Any potential owner can start a Ready task, where as only the owner can start a Reserved task. So what we have here is a self documenting DSL that is easy to understand and easy to administer. In reality WSHT gets a little more complex than there, where operations suspend and resume need to track previous status and as mentioned previously forwarding has an extra permissions check, and delegating will need to execute an additional command to also then Claim the task in the delegates name. The following links are for the full source code for [OperationCommand](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-process/drools-process-task/src/main/java/org/drools/task/service/OperationCommand.java?r=HEAD>) and the [operations-dsl.mvel](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-process/drools-process-task/src/main/resources/org/drools/task/service/operations-dsl.mvel?r=HEAD>).

Having written the DSL, forgoing Flow, the next question was – how do I write my rules to process the DSL. Given some more thought I realised that the rules where not large nor complex and the domain was known, in that they will not change often. further to this the data used with those rules is minimal – do I really need a rule engine for this? The obvious answer is no, I can hand crank some minimal Java code to process this DSL.

Java retrieved the list OperationCommands based on the requested operation the following java snippet shows how to iterate over the list of commands – note actually it processes the status and the previousStatus fields, but this is just for status:

```
for ( OperationCommand command : commands ) {
        // first find out if we have a matching status
        if ( command.getStatus() != null ) {
            for ( Status status : command.getStatus() ) {
                if ( taskData.getStatus() == status ) {
                    statusMatched = true;

                    // next find out if the user can execute this operation            
                    if ( !isAllowed( command,
                                     task,
                                     user,
                                     targetEntity ) ) {
                        return new TaskError( "User '" + user + "' does not have permissions to execution operation '" + operation + "' on task id " + task.getId() );

                    }

                    commands( command,
                              task,
                              user,
                              targetEntity );
                    return null;
                }
            }
        }
        ...
```

So in the case of “Start” we would have two OperationCommands and it would find the one that matches the current status of the Task. It then checks if the user has the correct permissions, which is encapsulated in the isAllowed(…) method. If the user has permissions it will then execute the commands, a java snippet for the commands method is below:

```java
private void commands(OperationCommand command,
                      Task task,
                      User user,
                      OrganizationalEntity targetEntity) {
    PeopleAssignments people = task.getPeopleAssignments();
    TaskData taskData = task.getTaskData();

    if ( command.getNewStatus() != null ) {
        taskData.setStatus( command.getNewStatus() );
    } else if ( command.isSetToPreviousStatus() ) {
        taskData.setStatus( taskData.getPreviousStatus() );
    }

    if ( command.isAddTargetEntityToPotentialOwners() && !people.getPotentialOwners().contains( targetEntity ) ) {
        people.getPotentialOwners().add( targetEntity );
    }

    if ( command.isRemoveUserFromPotentialOwners() ) {
        people.getPotentialOwners().remove( user );
    }

    if ( command.isSetNewOwnerToUser() ) {
        taskData.setActualOwner( (User) user );
    }

    if ( command.isSetNewOwnerToNull() ) {
        taskData.setActualOwner( null );
    }
    ...
```

The full DSL processing code can be found in the [TaskServiceSession](<http://fisheye.jboss.org/browse/JBossRules/trunk/drools-process/drools-process-task/src/main/java/org/drools/task/service/TaskServiceSession.java?r=HEAD>) source code.

So what can we take away from this?

  1. When the problem domain is well defined and known, try and design a self documenting DSL to represent the problem domain.
  2. We don’t always have to use XML, you do have a choice. Typically the dsl is going to be authored through a custom GUI, or just edited by the develop by hand. So why not keep it simple with a nice compact syntax, which will help with the “self documenting” benefits of the DSL.
  3. If the Flow is simple, we don’t have to use BPM software. Some times a DSL can be less verbose and provide more upfront visual information. Further to that a DSL encapsulates the flow and the rules in a single format.
  4. If their are a small number of non-complex rules that don’t change often and don’t require dynamic deployment with a small data set that won’t benefit from indexing or from optimising of data changes over time, maybe we should just write a few hundred lines of java code with good unit testing.