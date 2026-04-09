---
layout: post
title: "Drools Flow Overview and Previous Relevant Articles"
date: 2010-05-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/05/drools-flow-overview-and-previous-relevant-articles.html
---

InfoQ recently did an article on [Activi and BPMN 2.0](<http://www.infoq.com/news/2010/05/ActivitiBPM>), so I thought it was worth collecting some of the previous releveant Drools Flow articles, including ones on BPMN 2.0. So that people can get a better idea of what’s available in the OSS landscape.

Drools Flow is embeddable with small jar sizes, minimal dependencies and under the Apache Software License.

In 5.0 we had our own xml format, as BPMN2 was not ready. About a year ago we moved 5.1.0.SNAPSHOT to BPMN2 as the default.  
<http://blog.athico.com/2009/07/drools-flow-and-bpmn2.html>

We also have commitment to other standards such as our WS-HumanTask implementation, which we have had for some time.  
<http://blog.athico.com/2008/09/drools-and-ws-humantask.html>

Drools Flow comes fully integrated with our rules (Drools Expert) and cep (Drools Fusion) technology. This allows for built in declarative monitoring and interceptors, an important part of building both a dynamic and adaptive platform.  
<http://blog.athico.com/2009/11/monitoring-your-drools-flow-processes.html>

We also provide easy extension points for domain specific workflows, we call these “Work Items”. We provide example ones, such as google calendar integration, file listings, ftp, command line execution, email etc:  
<http://blog.athico.com/2009/02/drools-flow-work-items.html>

Video’s of Drools Flow in action:  
<http://blog.athico.com/2009/12/screencasts-on-some-faq.html>  
<http://blog.athico.com/2009/08/drools-flow-videos.html>

Rules and Processes share so much as declarative languages, and the Drools platform makes this a very natural fit, you can read more about things like common life cycle here:  
<http://people.redhat.com/kverlaen/BPM/>

We are just about to release M2, where the fruits of this work can be seen, and GA should follow very shortly. Follow the blog for latest release news:  
<http://www.jboss.org/drools/downloads.html>

Going forward Drools Flow will be incorporated into jBPM, with additional feedback from the jBPM community as part of jBPM5.  
[http://kverlaen.blogspot.com/2010/05/proposal-for-jbpm5-roadmap.htm](<http://kverlaen.blogspot.com/2010/05/proposal-for-jbpm5-roadmap.html>)[l](<http://kverlaen.blogspot.com/2010/05/proposal-for-jbpm5-roadmap.html>)