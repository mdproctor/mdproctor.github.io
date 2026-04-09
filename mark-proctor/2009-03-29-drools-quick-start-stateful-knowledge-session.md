---
layout: post
title: "Drools Quick Start - Stateful Knowledge Session"
date: 2009-03-29
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/03/drools-quick-start-stateful-knowledge-session.html
---

Here is an extract from the quick start guide I just writing on using stateful sessions:

Stateful sessions are longer lived and allow iterative changes over time. Some common use cases for stateful sessions are, but not limited to:

  * Monitoring
    * Stock market monitorig and analysis for semi-automatic buying
  * Diagnostics
    * fault finding, medical diagnostics
  * Logistics
    * parcel tracking and delivery provisioning
  * Compliance
    * Validation of legality for market trades.

Unlike a stateless session the dispose() method must be called afterwards to ensure there are no memory leaks, as the KnowledgeBase containes references to StatefulKnowledgeSessions when they are created. StatefulKnowledgeSession also supports the BatchExecutor interface like StatelessKnowledgeSession, the only difference is that when used with stateful the FireAllRules command is not automatically called at the end.

We can use a fire alarm example to explore the monitoring use case. The simple example has just 4 classes. We are monitoring the rooms in a house, each room has one sprinkler. If a fire starts in a room, we represent that with a single Fire instance.

```java
public class Room {
   private String name;
   // getter and setter methods here
}

public classs Sprinkler {
   private Room room;
   private boolean on;
   // getter and setter methods here
}

public class Fire {
   private Room room;
   // getter and setter methods here
}

public class Alarm {
}
```

In the previous section on stateless sessions the concepts of inserting and matching against data was introduced. That example assumed only a single instance of each object type was ever inserted and thus only used literal constraints. However a house has many rooms, so rules have the need to express joins that constraint to the desired objects, this can be done using a binding as a variable constraint in a pattern. This join process results in what is called cross products, which are covered in the next section.

When a fire occurs an instance of the Fire class is created, for that room, and insert it. The rule uses a binding on the room field of the Fire to constrain to the Sprinkler for that room, which is currently off. When this rule fires and the consequence is executed the sprinkler is turned on

```drl
rule "When there is a fire turn on the sprinkler"
when
Fire($room : room)   $sprinkler : Sprinkler( room == $room, on == false )
then
modify( $sprinkler ) { setOn( true ) };   System.out.println( "Turn on the sprinkler for room " + $room.getName() );
end
```

Where as the stateless session used standard java syntax to modify a field, in the above rule we use the modify keyword, which acts as a sort of with statement, that contains a series of comma separated java expressions. Stateless sessions typically do not use inference, which can be explicitly turned off by using the “sequential mode”, so the engine does not need to be aware of changes to data, however a stateful session does. The modify keyword allows the setters to modify the data, while make the engine aware of those changes so it can reason over them, this process is called inference.

So far we have rules that tell us when matching data exists, but what about when it doesn’t exist? What about when there stops being a Fire? Previously the constraints have been propositional logic where the engine is constraining against individual intances, Drools also has support for first order logic that allows you to look at sets of data. The ‘not’ keyword matches when something does not exist. So for a Room with a Sprinkler that is on when the Fire for that room stops existing we can turn off the sprinkler.

```drl
rule "When the fire is gone turn off the sprinkler"
when
$room : Room( )   $sprinkler : Sprinkler( room == $room, on == true )   not Fire( room == $room )
then
modify( $sprinkler ) { setOn( false ) };   System.out.println( "Turn off the sprinkler for room " + $room.getName() );
end
```

While there is a Sprinkler per room, there is just a single Alarm for the building. An Alarm is created when a Fire is occurs, but only one Alarm is needed for the entire building, no matter how many Fires occur. Previously ‘not’ was introduced, the compliment to ths is ‘exists’ which matches for one or more of something.

```drl
rule "Raise the alarm
when
we have one or more fires"
when
exists Fire()
then
insert( new Alarm() );   System.out.println( "Raise the alarm" );
end
```

Likewise when there are no Fires we want to remove the alarm, so the ‘not’ keyword can be used again.

```drl
rule "Lower the alarm
when
all the fires have gone"
when
not Fire()   $alarm : Alarm()
then
retract( $alarm );   System.out.println( "Lower the alarm" );
end
```

Finally there is a general health status message, that is printed when the application first starts and after the Alarm is removed and all Sprinklers have been turned off.

```drl
rule "Status output
when
things are ok"
when
not Alarm()   not Sprinkler( on === true )
then
System.out.println( "Everything is ok" );
end
```

The above rules should be placed in a single drl file and saved to the classpath using the file name “fireAlarm.drl”, as per the stateless session example. We can then build a KnowledgeBase as before, just using the new name “fireAlarm.drl”. The difference is this time we create a stateful session from the kbase, where as before we created a stateless session.

```
KnowledgeBuilder kbuilder = KnowledgeBuilderFactory.newKnowledgeBuilder();
kbuilder.add( ResourceFactory.newClasspathResource( "fireAlarm.drl", getClass() ),
             ResourceType.DRL );
if ( kbuilder.hasErrors() ) {
   System.err.println( builder.getErrors().toString() );
}
StatefulKnowledgeSession ksession = kbase.newStatefulKnowledgeSession();
```

With the session created it is now possible to iteratvely work with it over time. Four Rooms are created and inserted, a Sprinkler for each room is also inserted. At this point the engine has done all it’s matching, but no rules have fired. calling “fireAllRules” on the ksession allows the matched rules to fire, currently that is just the health message.

```text
Room kitchen = new Room( "kitchen" );
Room bedroom = new Room( "bedroom" );
Room office = new Room( "office" );
Room livingRoom = new Room( "livingroom" );

ksession.insert( kitchen );
ksession.insert( bedroom );
ksession.insert( office );
ksession.insert( livingRoom );

Sprinkler kitchenSprinkler = new Sprinkler( kitchen );
Sprinkler bedroomSprinkler = new Sprinkler( bedroom );
Sprinkler officeSprinkler = new Sprinkler( office );
Sprinkler livingRoomSprinkler = new Sprinkler( livingRoom );

ksession.insert( kitchenSprinkler );
ksession.insert( bedroomSprinkler );
ksession.insert( officeSprinkler );
ksession.insert( livingRoomSprinkler );

ksession.fireAllRules()

> Everything is ok
```

We now create two fires and insert them, this time a referenced is kept for the returned FactHandle. The FactHandle is an internal engine reference to the inserted instance and allows that instance to be retracted or modified at a later point in time. With the Fires now in the engine, once “fireAllRules” is called, the Alarm is raised and the respectively Sprinklers are turned on.

```text
Fire kitchenFire = new Fire( kitchen );
Fire officeFire = new Fire( office );

FactHandle kitchenFireHandle = ksession.insert( kitchenFire );
FactHandle officeFireHandle = ksession.insert( officeFire );

ksession.fireAllRules();

> Raise the alarm
> Turn on the sprinkler for room kitchen
> Turn on the sprinkler for room office
```

After a while the fires will be put out and the Fire intances are retracted. This results in the Sprinklers being turned off, the Alarm being lowered and eventually the health message is printed again.

```
ksession.retract( kitchenFireHandle );
ksession.retract( officeFireHandle );

ksession.fireAllRules();

> Turn on the sprinkler for room office
> Turn on the sprinkler for room kitchen
> Lower the alarm
> Everything is ok
```

Every one still with me? That wasn’t so hard and already I’m hoping you can start to see the value and power of a declarative rule system.