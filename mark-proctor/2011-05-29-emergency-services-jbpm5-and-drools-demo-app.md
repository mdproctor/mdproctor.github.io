---
layout: post
title: "Emergency Services - jBPM5 and Drools Demo App"
date: 2011-05-29
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/05/emergency-services-jbpm5-and-drools-demo-app.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Emergency Services – jBPM5 and Drools Demo App](<https://blog.kie.org/2011/05/emergency-services-jbpm5-and-drools-demo-app.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 29, 2011  
[Process](<https://blog.kie.org/category/process>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’m proud to release the second version of the [Emergency Services jBPM5 and Drools](<https://github.com/Salaboy/emergency-service-drools-app>) demo application. We ([@ilesteban](<http://www.twitter.com/ilesteban>) and I [@salaboy](<http://www.twitter.com/salaboy>)) spend a fair amount of time creating the second version that helps us to show some best practices about how to build applications on top of the Drools & jBPM5 platform. We are advertising this application as a jBPM5 and Drools blueprint that shows one of the possible architectures that can be used to build robust applications mixing Business Processes, Business Rules and Complex Event Processing. I’m also happy to announce that a new dev has join us ([@calcacuervo](<http://www.twitter.com/calcacuervo>)) in this effort to share best practices and an end to end application that shows. We are waiting for your feedback and contributions, feel free to join us there are tons of things to do!

This version was already presented in a couple of events like:[ JUDCon](<http://www.jboss.org/events/JUDCon/agenda.html>) and a some [bootcamps in the US](<http://blog.athico.com/2011/04/drools-jbpm-workshops-may-new-york-and.html>), where we receive awesome feedback and that really motivate us to keep going and improving what we got. We were very happy to see that some Red Hat’s solution architects were using the application to show their customers how the jBPM5 and Drools project can be used to build smarter applications.

# New Features / Improvements

The focus of this second version was a complete refactoring to the old code base that was messy and cannot be reused, improved or extended. We decouple the monolithic project into separated modules that interacts using asynchronous messages (HornetQ/JMS).  
Taking advantage of these decouple architecture we also include Drools Grid that enables the application to run in a distributed cluster of virtual/physical machines. The application now has the availability of create knowledge based services in different remote nodes being able to distribute the load between different machines.  
The use case that is currently supported it’s the same as the one implemented in the version 1 of the application. But the current implementation allows us to easily extend and add more use cases that involve collaboration between different entities inside the city. The new set of decoupled components have a well defined scope and responsibility that it’s described in the following section. We also create a new Emergency Dashboard to show in real time what’s happening in a specific emergency and how many emergencies we are handling in a specific moment in time.

Finally we open a [wiki that can be found here](<https://github.com/Salaboy/emergency-service-drools-app/wiki>), to help the new comers that are interested to play with the application to download it and play with it.

# Application Structure / Modules

The current version of the application contains the following modules:

  * emergency-service-model

  * emergency-service-core

  * emergency-service-world-ui-slick

  * emergency-service-tasklists-ui-swing

  * emergency-service-tasklist-ui-web

  * emergency-service-sensor

In order to understand how the application works and how all these modules interacts we need to understand the scope and responsibility of each of them. The following sections explains the scope and how the functionality was separated in order to support the use cases.

## Emergency Service Model

This simple Java (JAR) project includes all the Domain POJOs definitions. Inside this project we define all the classes that represent the data structures that will be used by the rest of the modules and are related to our domain. In this case because we are modeling and Emergency Services Company like 911 we will have some POJOS like: Emergency, Call, Vehicle, Ambulance, etc. You will find also a couple of utility classes and Drools/JBPM5 artifacts that were included here for simplicity. This JAR package needs to be shared by all the different processes that are created for this application to work. Because the new design was conceived for a distributed environment we need to provide a package (or a set of packages) that contains all the domain specific dependencies that will be needed by the different runtimes that will be dynamically spawned by the application.

## Emergency Service Core

The core project now contains a set of services that encapsulate the logic required by the application. The current defined services are all knowledge based services. This means that all of them are using rules, processes and events. But the main idea is to be able to plug any type of service. For future release will make sense to split this module to be able to manage one or a group of services together. You can browse the currently defined services here: <https://github.com/Salaboy/emergency-service-drools-app/tree/master/emergency-service-core/src/main/java/com/wordpress/salaboy/services>

You will notice that we have a service that it’s in charge of dynamically create new services instances based on the situation that we are trying to solve, allowing us to plug new procedures without the need of modifying how the procedures are started.

This project is also containing the processes and rules assets inside the src/main/resources directory. For future versions of the project the assets should be placed inside the Knowledge Repository (Guvnor) and use a knowledge agent to retrieve these assets when they are needed.

## Emergency Service World UI

Right now the application has only one implementation of the World UI component. We are using a library called slick: <http://slick.cokeandcode.com/>. The main responsibility of this module is to show what it’s happening in the city. In real application we don’t have a representation of what’s happening, but for this demo we want to show and let you interact with the real world to simulate different situations. It’s important for us to show what it’s happening, but you need to remember that from inside the company, where all the employees are working, they will receive only notifications about the external world.

[![](/legacy/assets/images/2011/05/b3ad7ca0dad3-citymap.png)](<http://salaboy.files.wordpress.com/2011/05/citymap.png>)

## Emergency Service Task Lists UI

The application right now provides two different implementations for the task lists user interfaces. Remember that the Task Lists UIs will represent the software that will be used by the companies employees. The tasks will be created by business processes and also business rules when are required. The users will automatically receive the created tasks in their task lists. Both implementations are using a project called smart-tasks to improve how the task lists and task form are defined and configured. The web version uses some more advanced features of smart tasks to demonstrate how the project can be used to quickly build task list oriented front ends to interact with the human activities created by our business knowledge. You can find more about the smart tasks project here: [https://github.com/Salaboy/smart-tasks.](<https://github.com/Salaboy/smart-tasks>)

[![](/legacy/assets/images/2011/05/68b349eaa926-taskform.png)](<http://salaboy.files.wordpress.com/2011/05/taskform.png>)

## Emergency Service Sensor

This module contains the different adaptors to support external sources of events that can be used to represent real life information that it’s coming into our system. The first version of this application was working only with a [Nintentdo Wii Remote Control ](<http://en.wikipedia.org/wiki/Wii_Remote>)(WiiMote), but the new version supports also the accelerometer of the IPhone. You should only install a free application called [AccSim](<http://itunes.apple.com/app/accelerometer-simulator/id336476721?mt=8>) in your phone to send the accelerometer events. We use these accelerometers to simulate the patients heart beats when we have a heart attack situation.  
We are thinking to provide an extra module to support Android devices as well, but it’s still under development at the moment.

# Roadmap

The roadmap at this point for V3 is to improve the way to execute and extend the application. We will fight to include more complex use cases using the current architecture. We will be targeting the V3 for Rules Fest (October 24-27), and this version will include more dynamic mechanisms to discover the procedures that needs to be executed in order to solve more complex scenarios. For that reason we will be implementing multiple procedures that involves different entities like the police department and the fire department. The real fun begins when we want to solve situations that involves more than one entity to be coordinated. We are looking forward to implement some graphical aids to be able to show alerts inside the map in real time as they happen.

One minor refactor that we will be doing is creating a separate module for the Real Time Dashboard project, because right now it is included inside the Task Lists UI Swing application, but it doesn’t belong there.

[![](/legacy/assets/images/2011/05/49f090236d27-emergencydashboard.png)](<http://salaboy.files.wordpress.com/2011/05/emergencydashboard.png>)

I will be writing a more detailed post about the architecture of the application and logic that it’s being executed by each service inside the application soon. Also a detailed roadmap will be created based on the feedback. Please don’t post commands about THE MONSTER! we will be adding that use case as well :)

[![](/legacy/assets/images/2011/05/7c49d1baebd6-screen-shot-2011-05-27-at-9-19-05-pm.png)](<http://salaboy.files.wordpress.com/2011/05/screen-shot-2011-05-27-at-9-19-05-pm.png>)

If you want to see something in particular implemented here, please write a comment.

# Notes

We want to notify to all the people that its downloading the application and want to start playing with it a couple of things:

  1. We are not creating tags/branches to keep the stable versions. We don’t have a tag/branch for Version 1 and Version 2. We strongly believe that there are a lot of things that needs to be improved in order to create what we think is a stable version. If you check out the current code please remember that you are getting the latest code that it’s under continuous refactoring and improvement. Write us if you are having troubles, we will be here to help you.

  2. If you want to play with the application take a look at the wiki for the documentation and how to’s to set up and run the application in different operating systems. If you have troubles, please report them sending me an email: (salaboy AT gmail DOT com – esteban DOT aliverti AT gmail DOT com) or add a comment to the project. If you solve a problem related with your platform, please send us the information and we will include that in the wiki pages.

  3. We are mentoring and helping people to get involved. If you want to show or demonstrate how these projects like Drools, jBPM, HornetQ and Inifinispan works and how they can be used in your applications please contribute with this project. We build a generic architecture that can be adapted to almost every application domain. Everyone can benefit for the features that we are adding here in this application. For creating your own domain specific application then you can copy and paste the mechanisms and adapt the processes, rules and events sources to work for your domain.

Original Post: <http://salaboy.wordpress.com/2011/05/28/emergency-services-v2-jbpm5-and-drools-blueprint/>

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F05%2Femergency-services-jbpm5-and-drools-demo-app.html&linkname=Emergency%20Services%20%E2%80%93%20jBPM5%20and%20Drools%20Demo%20App> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F05%2Femergency-services-jbpm5-and-drools-demo-app.html&linkname=Emergency%20Services%20%E2%80%93%20jBPM5%20and%20Drools%20Demo%20App> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F05%2Femergency-services-jbpm5-and-drools-demo-app.html&linkname=Emergency%20Services%20%E2%80%93%20jBPM5%20and%20Drools%20Demo%20App> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F05%2Femergency-services-jbpm5-and-drools-demo-app.html&linkname=Emergency%20Services%20%E2%80%93%20jBPM5%20and%20Drools%20Demo%20App> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F05%2Femergency-services-jbpm5-and-drools-demo-app.html&linkname=Emergency%20Services%20%E2%80%93%20jBPM5%20and%20Drools%20Demo%20App> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F05%2Femergency-services-jbpm5-and-drools-demo-app.html&linkname=Emergency%20Services%20%E2%80%93%20jBPM5%20and%20Drools%20Demo%20App> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F05%2Femergency-services-jbpm5-and-drools-demo-app.html&linkname=Emergency%20Services%20%E2%80%93%20jBPM5%20and%20Drools%20Demo%20App> "Email")
  *[]: 2010-05-25T16:11:00+02:00