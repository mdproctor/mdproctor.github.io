---
layout: post
title: "How to build and run the Drools and Guvnor Beta3 Demo"
date: 2013-05-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2013/05/how-to-build-and-run-the-drools-and-guvnor-beta3-demo.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [How to build and run the Drools and Guvnor Beta3 Demo](<https://blog.kie.org/2013/05/how-to-build-and-run-the-drools-and-guvnor-beta3-demo.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 26, 2013  
[Rules](<https://blog.kie.org/category/rules>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

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
    *     * http://localhost:8080/drools-workbench-6.0.0-SNAPSHOT-jboss-as7.0
    * login/pass admin/admin
    * Must use fireFox, as maven build defaults to reduced number of profile sets, for fast building. 
      * Use -PfullProfile with mvn install, to build all profiles, with longer build times.
  * There is a sample repo, but mostly has rubbish in it, stick to the uberfire playground.

Things to notice, or try:

  * Maven POM editor, when the file explorer is inside a maven project
  * As per my video, try building and installing the poject, and viewing in the maven manager
  * Clone some external projects, see if you can build and deploy them
  * Have a play with some of the custom editors, especially the guided editors and decision tables.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F05%2Fhow-to-build-and-run-the-drools-and-guvnor-beta3-demo.html&linkname=How%20to%20build%20and%20run%20the%20Drools%20and%20Guvnor%20Beta3%20Demo> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F05%2Fhow-to-build-and-run-the-drools-and-guvnor-beta3-demo.html&linkname=How%20to%20build%20and%20run%20the%20Drools%20and%20Guvnor%20Beta3%20Demo> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F05%2Fhow-to-build-and-run-the-drools-and-guvnor-beta3-demo.html&linkname=How%20to%20build%20and%20run%20the%20Drools%20and%20Guvnor%20Beta3%20Demo> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F05%2Fhow-to-build-and-run-the-drools-and-guvnor-beta3-demo.html&linkname=How%20to%20build%20and%20run%20the%20Drools%20and%20Guvnor%20Beta3%20Demo> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F05%2Fhow-to-build-and-run-the-drools-and-guvnor-beta3-demo.html&linkname=How%20to%20build%20and%20run%20the%20Drools%20and%20Guvnor%20Beta3%20Demo> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F05%2Fhow-to-build-and-run-the-drools-and-guvnor-beta3-demo.html&linkname=How%20to%20build%20and%20run%20the%20Drools%20and%20Guvnor%20Beta3%20Demo> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2013%2F05%2Fhow-to-build-and-run-the-drools-and-guvnor-beta3-demo.html&linkname=How%20to%20build%20and%20run%20the%20Drools%20and%20Guvnor%20Beta3%20Demo> "Email")
  *[]: 2010-05-25T16:11:00+02:00