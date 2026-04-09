---
layout: post
title: "UF Dashbuilder - Activity monitoring in jBPM"
date: 2015-03-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/03/uf-dashbuilder-activity-monitoring-in-jbpm.html
---

syndicated from <http://dashbuilder.blogspot.com.es/2015/03/uf-dashbuilder-in-jbpm-for-activity.html>

Last week, the jBPM team announced the 6.2.0.Final release (announcement [here](<http://blog.athico.com/2015/03/jbpm-620final-released.html>)). In this release (like in previous ones) you can author processes, rules, data models, forms and all the assets of a BPM project. You can also create or clone existing projects from remote GIT repositories and group such repositories into different organizational units. Everything can be done from the jBPM authoring console (aka KIE Workbench), a unified UI built using the Uberfire framework & GWT.  
  
In this latest release, they have also added a new perspective to monitor the activity of the source GIT repositories and organizational units managed by the tooling (see screenshot below). The perspective itself it’s just a dashboard displaying several indicators about the commit activity. From the dashboard controls it is possible to:  

  * Show the overall activity on our repositories
  * Select a single organizational unit or repository
  * List the top contributors
  * Show only the activity for an specific time frame

  
In this [video](<https://www.youtube.com/watch?v=IX4XfggAR7s>) you can see the dashboard in action (do not forget to select HD).  

[![](/legacy/assets/images/2015/03/cdc22720ec18-contributors.png)](</assets/images/2015/03/85c4c7ebb8df-contributors.png>)  
---  
Contributors Perspective  
  
  
Organizational units can be managed from the menu  _Authoring >Administration>Organizational Units_. Every time an organizational unit is added or removed the dashboard is updated.  

[![](/legacy/assets/images/2015/03/6d7dc9ecc548-orgunits.png)](</assets/images/2015/03/cf6be706081f-orgunits.png>)  
---  
Administration – Organizational Units   
  
  
Likewise, from the  _Authoring >Administration>Repositories_ view we can create, clone or delete repositories. The dashboard will always feed from the list of repositories available.  

[![](/legacy/assets/images/2015/03/9c84b832c933-repos.png)](</assets/images/2015/03/4aeea90e8c73-repos.png>)  
---  
Administration – Repositories  
  
  
  
  
As shown, activity monitoring in jBPM can be applied to not only to the processes business domain but also to the authoring lifecycle in order the get a detailed view of the ongoing development activities.  
  
**How it’s made**  
  
  
The following diagram shows the overall design of the dashboard architecture. Components in grey are platform components, blue ones are specific to the contributors dashboard.  

[![](/legacy/assets/images/2015/03/a03b99c8762c-Contributors_2Bperspective_2Barchitecture.png)](</assets/images/2015/03/b79f8f3d40fc-Contributors_2Bperspective_2Barchitecture.png>)  
---  
Contributors dashboard architecture  
  
  
These are the steps the backend components take to build the contributors data set:  

  * The  _ContributorsManager_ asks the platform services for the set of available org. units & repos. 
  * Once it has such information, it builds a data set containing the commit activity.
  * The contributors dataset is registered into the Dashbuilder’s  _DataSetManager_.

All the steps above are executed on application start up time. Once running, the  _ContributorsManager_ also receives notifications form the platform services about any changes on the org. units & repositories registered, so that the contributors data set is synced up accordingly. 

  
  
From the UI perspective, the jBPM’s contributors dashboard is an example of hard-coded dashboard built using the Dashbuilder Displayer API which was introduced in [this](<http://dashbuilder.blogspot.com.es/2015/03/uf-dashbuilder-displayer-editor-api_3.html>) blog entry. The  _ContributorsDashboard_ component is just a GWT composite widget containing several  _Displayer_ instances feeding from the contributors data set.

(The source code of the contributors perspective can be found [here](<https://github.com/droolsjbpm/kie-wb-common/tree/master/kie-wb-common-screens/kie-wb-common-contributors>))  
  
This has been a good example of how to leverage the Dashbuilder technology to build activity monitoring dashboards. In the future, we plan for applying the technology in other areas within jBPM, like, for instance, an improved version of the jBPM process dashboard. We will keep you posted!