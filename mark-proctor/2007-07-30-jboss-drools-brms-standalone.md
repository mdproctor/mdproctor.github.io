---
layout: post
title: "JBoss Drools BRMS Standalone"
date: 2007-07-30
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/jboss-drools-brms-standalone.html
---

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