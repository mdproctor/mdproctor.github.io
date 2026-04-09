---
layout: post
title: "Pre-installed Drools development environment for VirtualBox"
date: 2009-06-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/06/pre-installed-drools-development-environment-for-virtualbox.html
---

For the [Drools Boot Camp SF09](<http://blog.athico.com/2009/03/drools-boot-camp-san-francisco-june.html>) I made up pre-installed Drools development environments for Sun’s [VirtualBox](<http://www.virtualbox.org/>). This environment has everything you need to start development of drools.

[![](/legacy/assets/images/2009/06/98fd21fc9257-virtualbox_repoman.png)](</assets/images/2009/06/36dee2111508-virtualbox_repoman.png>)  
  
What’s in the box?

  * Fedora 10
  * Java 1.6 JDK
  * Maven 2.0.9
  * Ant 1.7.1
  * gwt-linux-1.5.2
  * JProfiler 5.2 (With Drools community license, only to be used with Drools)
  * Eclipse 3.4 (with GEF, Subclipse, Drools and JProfiler plugins pre-installed, and Drools runtime configured)
  * All environment variables correctly set
  * Full Drools SVN checkout
  * Maven repository populated with all Drools dependencies
  * Initial Eclipse workspace created, with basic modules already checked in
  * Documentation already built and set as FireFox home page
  * Full build already done, including the eclipse plugin which downloads eclipse to build itself, and JBoss AS for the guvnor-standalone.zip which is in drools-guvnor.

The VirtualBox 2.2 image is exported and zipped and available here:  
<https://docs.jboss.org/drools/virtualbox/dvbox-20090615.zip> (2.6GB)

username : repoman  
password : password

If anyone wants to improve on this image – preinstalled Netbeans, IntelliJ (with community license) or any other ideas, please feel free and let me know where I can download it from so I can make it available to others.