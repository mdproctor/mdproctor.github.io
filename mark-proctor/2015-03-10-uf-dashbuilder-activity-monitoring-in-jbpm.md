---
layout: post
title: "UF Dashbuilder - Activity monitoring in jBPM"
date: 2015-03-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/03/uf-dashbuilder-activity-monitoring-in-jbpm.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [UF Dashbuilder – Activity monitoring in jBPM](<https://blog.kie.org/2015/03/uf-dashbuilder-activity-monitoring-in-jbpm.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 10, 2015  
[Process](<https://blog.kie.org/category/process>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

syndicated from <http://dashbuilder.blogspot.com.es/2015/03/uf-dashbuilder-in-jbpm-for-activity.html>

Last week, the jBPM team announced the 6.2.0.Final release (announcement [here](<http://blog.athico.com/2015/03/jbpm-620final-released.html>)). In this release (like in previous ones) you can author processes, rules, data models, forms and all the assets of a BPM project. You can also create or clone existing projects from remote GIT repositories and group such repositories into different organizational units. Everything can be done from the jBPM authoring console (aka KIE Workbench), a unified UI built using the Uberfire framework & GWT.  
  
In this latest release, they have also added a new perspective to monitor the activity of the source GIT repositories and organizational units managed by the tooling (see screenshot below). The perspective itself it’s just a dashboard displaying several indicators about the commit activity. From the dashboard controls it is possible to:  

  * Show the overall activity on our repositories
  * Select a single organizational unit or repository
  * List the top contributors
  * Show only the activity for an specific time frame

  
In this [video](<https://www.youtube.com/watch?v=IX4XfggAR7s>) you can see the dashboard in action (do not forget to select HD).  

[![](/legacy/assets/images/2015/03/cdc22720ec18-contributors.png)](<http://4.bp.blogspot.com/-VeilZWpTQbA/VP7GSVvZpuI/AAAAAAAAAP8/piPsY5mtwcs/s1600/contributors.png>)  
---  
Contributors Perspective  
  
  
Organizational units can be managed from the menu  _Authoring >Administration>Organizational Units_. Every time an organizational unit is added or removed the dashboard is updated.  

[![](/legacy/assets/images/2015/03/6d7dc9ecc548-orgunits.png)](<http://3.bp.blogspot.com/-eMPIPV6MNkI/VP7GSWAHKrI/AAAAAAAAAQA/Kd7W8Q0oTks/s1600/orgunits.png>)  
---  
Administration – Organizational Units   
  
  
Likewise, from the  _Authoring >Administration>Repositories _view we can create, clone or delete repositories. The dashboard will always feed from the list of repositories available.  

[![](/legacy/assets/images/2015/03/9c84b832c933-repos.png)](<http://4.bp.blogspot.com/-BL1n6pQlKWo/VP7GScHTHeI/AAAAAAAAAP4/mRZXbqn7HTc/s1600/repos.png>)  
---  
Administration – Repositories  
  
  
  
  
As shown, activity monitoring in jBPM can be applied to not only to the processes business domain but also to the authoring lifecycle in order the get a detailed view of the ongoing development activities.  
  
**How it’s made**  
  
  
The following diagram shows the overall design of the dashboard architecture. Components in grey are platform components, blue ones are specific to the contributors dashboard.  

[![](/legacy/assets/images/2015/03/a03b99c8762c-Contributors_2Bperspective_2Barchitecture.png)](<http://4.bp.blogspot.com/-WYq5xJJGdvI/VP7W-3I0w2I/AAAAAAAAAQQ/944mkWmp7Q0/s1600/Contributors%2Bperspective%2Barchitecture.png>)  
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

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Fuf-dashbuilder-activity-monitoring-in-jbpm.html&linkname=UF%20Dashbuilder%20%E2%80%93%20Activity%20monitoring%20in%20jBPM> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Fuf-dashbuilder-activity-monitoring-in-jbpm.html&linkname=UF%20Dashbuilder%20%E2%80%93%20Activity%20monitoring%20in%20jBPM> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Fuf-dashbuilder-activity-monitoring-in-jbpm.html&linkname=UF%20Dashbuilder%20%E2%80%93%20Activity%20monitoring%20in%20jBPM> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Fuf-dashbuilder-activity-monitoring-in-jbpm.html&linkname=UF%20Dashbuilder%20%E2%80%93%20Activity%20monitoring%20in%20jBPM> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Fuf-dashbuilder-activity-monitoring-in-jbpm.html&linkname=UF%20Dashbuilder%20%E2%80%93%20Activity%20monitoring%20in%20jBPM> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Fuf-dashbuilder-activity-monitoring-in-jbpm.html&linkname=UF%20Dashbuilder%20%E2%80%93%20Activity%20monitoring%20in%20jBPM> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F03%2Fuf-dashbuilder-activity-monitoring-in-jbpm.html&linkname=UF%20Dashbuilder%20%E2%80%93%20Activity%20monitoring%20in%20jBPM> "Email")
  *[]: 2010-05-25T16:11:00+02:00