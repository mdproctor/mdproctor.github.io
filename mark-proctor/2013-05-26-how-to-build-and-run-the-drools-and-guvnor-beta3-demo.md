---
layout: post
title: "How to build and run the Drools and Guvnor Beta3 Demo"
date: 2013-05-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2013/05/how-to-build-and-run-the-drools-and-guvnor-beta3-demo.html
---

After the release of the Drools and Guvnor beta3 video see [here](<http://blog.athico.com/2013/05/drools-and-guvnor-beta3-video.html>), I’m being asked how people can build and run it themselves. Luckily it’s very easy, so here are some quick instructions :)

  * Make sure you set your MAVEN_OPTS:
    * MAVEN_OPTS=”-Xms512m -Xmx1024m -XX:MaxPermSize=128m”
  * Git clone:
    * https://github.com/droolsjbpm/guvnor
  * From clone root, built the main application:
    * mvn clean install -DskipTests
  * Change to the WAR module:
    * cd drools-wb/drools-wb-distribution-wars
  * Build the WAR
    * mvn clean install -DskipTests
    * Builds Tomcat and JBoss AS WARs, with the firefox profile.
      * WAR only works with Firefox, but quick to compile, for testing.
  * Download unzip and start JBoss AS7.1
    * http://download.jboss.org/jbossas/7.1/jboss-as-7.1.1.Final/jboss-as-7.1.1.Final.zip
    * ./standalone.sh
    * Once started, don’t forget to create a management user with add-user.sh
  * Install the WAR via the AS web console
    * Find the WAR and upload it, AS automatically installs it
    * drools-workbench-6.0.0-SNAPSHOT-jboss-as7.0.war
  * Go to URL and login
    * http://localhost:8080/drools-workbench-6.0.0-SNAPSHOT-jboss-as7.0
    * login/pass admin/admin
    * Must use fireFox, as maven build defaults to reduced number of profile sets, for fast building. 
      * Use -PfullProfile with mvn install, to build all profiles, with longer build times.
  * There is a sample repo, but mostly has rubbish in it, stick to the uberfire playground.

Things to notice, or try:

  * Maven POM editor, when the file explorer is inside a maven project
  * As per my video, try building and installing the poject, and viewing in the maven manager
  * Clone some external projects, see if you can build and deploy them
  * Have a play with some of the custom editors, especially the guided editors and decision tables.