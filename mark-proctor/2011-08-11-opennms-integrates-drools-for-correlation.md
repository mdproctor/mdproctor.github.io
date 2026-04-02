---
layout: post
title: "OpenNMS integrates Drools for Correlation"
date: 2011-08-11
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/08/opennms-integrates-drools-for-correlation.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [OpenNMS integrates Drools for Correlation](<https://blog.kie.org/2011/08/opennms-integrates-drools-for-correlation.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- August 11, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

<http://www.opennms.com/twio-drooling-all-over-your-network/>  

# “Meet the New Drools, Same as the Old Drools

For a long time now, OpenNMS has had a little-known feature for doing event correlation, using the open-source [Drools](<http://www.jboss.org/drools>) business logic engine. It is little-known because we have gone out of our way not to tell people about it — somewhere in the transition from OpenNMS 1.2 to 1.6, it broke because of a complicated chain of dependencies. Thanks to the work of the enigmatic Seth, Jetty and Drools are once again in agreement on their dependencies, and I’ve confirmed that it’s working as of this morning’s code (which should be available in tomorrow’s nightly snapshots).

The correlation engine lets you do complex workflows and event processing (including detection of flapping). We have a couple of examples of what can be done in the $OPENNMS_HOME/etc/examples/ directory. If you’d like to try them out, just copy the following files into your etc directory:

correlation-engine.xml
    Configures the correlation engine daemon. Since the OpenNMS correlation engine is a generic API that could potentially be implemented using multiple business logic implementations, this configuration tells OpenNMS which engines are available. Currently, the only implementation is the Drools engine.
drools-engine.xml
    Configures the Drools correlation engine. This file contains the Drools-specific configuration for event correlation. In it you define  tags which refer to the code, events, and other variables that are relevant.
LocationMonitorRules.drl
    An example Drools correlation rule which can detect flapping outages from remote pollers.
NodeParentRules.drl
    An example Drools correlation rule which can do root cause analysis on node outages based on a node parent outage.
nodeParentRules-context.xml
    A spring configuration file to provide extra resources to the “node parent” Drools rule.

Then, edit your $OPENNMS_HOME/etc/service-configuration.xml and uncomment the service named “OpenNMS:Name=Correlator” and restart OpenNMS.

Other than that, using Drools is not very well documented yet, but if you are a Java developer, you should be able to work out what’s going on looking at the rules and configuration files.”  

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fopennms-integrates-drools-for-correlation.html&linkname=OpenNMS%20integrates%20Drools%20for%20Correlation> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fopennms-integrates-drools-for-correlation.html&linkname=OpenNMS%20integrates%20Drools%20for%20Correlation> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fopennms-integrates-drools-for-correlation.html&linkname=OpenNMS%20integrates%20Drools%20for%20Correlation> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fopennms-integrates-drools-for-correlation.html&linkname=OpenNMS%20integrates%20Drools%20for%20Correlation> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fopennms-integrates-drools-for-correlation.html&linkname=OpenNMS%20integrates%20Drools%20for%20Correlation> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fopennms-integrates-drools-for-correlation.html&linkname=OpenNMS%20integrates%20Drools%20for%20Correlation> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fopennms-integrates-drools-for-correlation.html&linkname=OpenNMS%20integrates%20Drools%20for%20Correlation> "Email")
  *[]: 2010-05-25T16:11:00+02:00