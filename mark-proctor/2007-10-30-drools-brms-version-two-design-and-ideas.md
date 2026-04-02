---
layout: post
title: "Drools BRMS version two design and ideas"
date: 2007-10-30
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/10/drools-brms-version-two-design-and-ideas.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools BRMS version two design and ideas](<https://blog.kie.org/2007/10/drools-brms-version-two-design-and-ideas.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- October 30, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

Hi folks

After delivering 4.0.3 Michael and I had some conversations about adding more features and a complete re-design of the BRMS web interface. Basically we are looking at how to break things up into “perspectives” kind of like eclipse has (but simpler), just to make it easier to present the user with the information they need for their current work example:

  1. BA type users (no package configuration, follow templates, read only sometimes etc)
  2. Developers (configure stuff – eventually should only need eclipse so this doesn’t have to be too strong on the web side)
  3. Admins/operator types (migrate, security setup etc).

Nothing that complex, but we do need to have it scale up and down to these skill levels.

I think we can do something like merging the previous BRMS organization with the new tree feature. We do like the tree/explorer motif, fairly familiar to most people and easy to make it filterable based on both server side and user settings. Also, its more like ideas that the jboss web console is moving to.

The new package feature  
![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)![](https://fmeyer.org/brmsv2/brmsexplorer/BRMS2.png)

Categorization  
![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)![](https://fmeyer.org/brmsv2/brmsexplorer/BRMS1.png)

Administration  
![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)![](https://fmeyer.org/brmsv2/brmsexplorer/BRMS4.png)

Also with this refactory we will enable I18n internationalization then people can easily edit the bundle file/config to add they own language setting. Other key features like rule based authorization and custom queries are also some of the new features.

We are messing around with a few designs and also very receptive on ideas and feature requests you can find our task list on [Jira](<http://jira.jboss.org/jira/browse/JBRULES-684>) and suggest something, also you can ping the dev mailing list on [rules-dev@lists.jboss.org](<mailto:rules-dev@lists.jboss.org>)

The new BRMS design concept  
[![](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7)![](https://fmeyer.org/brmsv2/BRMSv2.png)](<http://fmeyer.org/brmsv2/BRMSv2.png>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F10%2Fdrools-brms-version-two-design-and-ideas.html&linkname=Drools%20BRMS%20version%20two%20design%20and%20ideas> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F10%2Fdrools-brms-version-two-design-and-ideas.html&linkname=Drools%20BRMS%20version%20two%20design%20and%20ideas> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F10%2Fdrools-brms-version-two-design-and-ideas.html&linkname=Drools%20BRMS%20version%20two%20design%20and%20ideas> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F10%2Fdrools-brms-version-two-design-and-ideas.html&linkname=Drools%20BRMS%20version%20two%20design%20and%20ideas> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F10%2Fdrools-brms-version-two-design-and-ideas.html&linkname=Drools%20BRMS%20version%20two%20design%20and%20ideas> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F10%2Fdrools-brms-version-two-design-and-ideas.html&linkname=Drools%20BRMS%20version%20two%20design%20and%20ideas> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F10%2Fdrools-brms-version-two-design-and-ideas.html&linkname=Drools%20BRMS%20version%20two%20design%20and%20ideas> "Email")