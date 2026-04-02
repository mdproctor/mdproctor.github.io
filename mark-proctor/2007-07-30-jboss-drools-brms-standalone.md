---
layout: post
title: "JBoss Drools BRMS Standalone"
date: 2007-07-30
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/jboss-drools-brms-standalone.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [JBoss Drools BRMS Standalone](<https://blog.kie.org/2007/07/jboss-drools-brms-standalone.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 30, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

Now you can download BRMS standalone version, this distribution comes with a built-in Tomcat 5.5.20 web server and the [insurance example](<http://blog.athico.com/2007/07/discount-insurance-brokers-example-for.html>) as demo repository, so it runs out the box. If you want to test BRMS and don’t have enough time to deploy, just follow to downloads page <http://labs.jboss.com/drools/downloads>

Brief install guide 

1\. Install a Java Development Kit (JDK) from[ http://java.sun.com/javase/downloads/index.jsp](<http://java.sun.com/javase/downloads/index.jsp>) (avoid JREs, Java EEs, Netbeans, etc. on that page – you just want a JDK).

2\. Set the JAVA_HOME variable to where you installed Java. Windows installers may do this for you.

3\. Run bin/startup.sh (*nix) or binstartup.bat (Windows). Check that there are no errors on the console. See below for troubleshooting advice.

4\. Point your browser at http://localhost/ You should see brms’s login box.

Problem 

A common startup problem is when another program has claimed port 80, which BRMS is configured to run on by default. To avoid this port conflict, BRMS’s port can be changed in conf/server.xml.

If you have installation (or other) problems, ask on the mailing lists or irc.

<http://labs.jboss.com/drools/lists.html>  
<http://labs.jboss.com/drools/irc.html>

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-brms-standalone.html&linkname=JBoss%20Drools%20BRMS%20Standalone> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-brms-standalone.html&linkname=JBoss%20Drools%20BRMS%20Standalone> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-brms-standalone.html&linkname=JBoss%20Drools%20BRMS%20Standalone> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-brms-standalone.html&linkname=JBoss%20Drools%20BRMS%20Standalone> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-brms-standalone.html&linkname=JBoss%20Drools%20BRMS%20Standalone> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-brms-standalone.html&linkname=JBoss%20Drools%20BRMS%20Standalone> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fjboss-drools-brms-standalone.html&linkname=JBoss%20Drools%20BRMS%20Standalone> "Email")