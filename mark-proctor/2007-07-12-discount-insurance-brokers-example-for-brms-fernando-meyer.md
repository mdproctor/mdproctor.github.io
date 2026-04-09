---
layout: post
title: "Discount insurance brokers example for BRMS (Fernando Meyer)"
date: 2007-07-12
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/discount-insurance-brokers-example-for-brms-fernando-meyer.html
---

[![](/legacy/assets/images/2007/07/04574f08e866-BRMSFeatures.png)](</assets/images/2007/07/3fdd7f02a3bd-BRMSFeatures.png>)There is a new BRMS example available. It is written up in the manual as a tutorial, but the information is repeated here. We are having some issues with our build server – so the docs available in the snapshots are probably not as up to date as the source is.

————-  
Fernando runs a dodgy fly by night insurance operation in Sao Paulo, Brasil. These are his rules – would you buy insurance from him ? (I wouldn’t).

This example takes you through the key steps in using the BRMS with an example respository, and using rules in a very very simple application (which you can use as a basis for your applications).

  * Download the latest version of BRMS from <http://cruisecontrol.jboss.com/cc/artifacts/jboss-rules>
  * Deploy BRMS WAR file into JBoss4.2 AS or JBossWeb, other containers can be used as well (possibly with some tweaking of dependencies).
  * Check you can access and run the BRMS.
  * Check out the demo project from the Drools subversion repository (this will be included in future distributions): <http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/drools-examples/drools-examples-brms/>
  * Import the demo business rules insurance repository file into BRMS, the compressed can be found at “files” folder in the demo project.
    * To do this, open the “files” directory, unzip the file there locally, and then go to the “Admin” section and “Manage backups” of the BRMS, select the file, and press “Import” – follow instructions.
  * Navigate through the BRMS web application to see how things are placed and organized and try to create some rules.
  * Go to the “Packages” feature and build the package (you should see no errors).
  * Now go to the “Deployment” feature, when you click on the package, it will show you one snapshot (which was part of the import, you can create more if you like from the previous step).
    * Open a snapshot.
    * Copy the snapshot url that is displayed.
    * Locate the file brmsdeployedrules.properties
    * Place the copied URL in the brmsdeployedrules.properties file.
    * OPTIONAL: To use a file or directory deployment in the rule agent just update brmsdeployedrules.properties according the documentation.
  * Import the example project into eclipse and execute the MainClass. The program will show the following trace (and away you go !):

RuleAgent(insuranceconfig) INFO (Thu Jul 12 20:06:02 BRT 2007): Configuring with newInstance=true, secondsToRefresh=30

RuleAgent(insuranceconfig) INFO (Thu Jul 12 20:06:02 BRT 2007): Configuring package provider : URLScanner monitoring URLs: http://localhost:8080/drools-jbrms/org.drools.brms.JBRMS/package/org.acme.insurance/fmeyer With local cache dir of /Users/fernandomeyer/projects/jbossrules/drools-examples/drools-examples-brms/cache

RuleAgent(insuranceconfig) INFO (Thu Jul 12 20:06:02 BRT 2007): Applying changes to the rulebase. RuleAgent(insuranceconfig) INFO (Thu Jul 12 20:06:02 BRT 2007): Creating a new rulebase as per settings.

RuleAgent(insuranceconfig) INFO (Thu Jul 12 20:06:02 BRT 2007): Adding package called org.acme.insurance

APPROVED: due to no objections.  
APPROVED: Driver is safe and mature.  
APPROVED: due to no objections.  
REJECTED: Too many accidents

The Rule Agent will pick up any changes that happen automatically – as soon as you create a new snapshot of the rules you want to deploy.