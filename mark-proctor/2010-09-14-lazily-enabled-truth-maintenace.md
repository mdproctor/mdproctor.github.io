---
layout: post
title: "Lazily Enabled Truth Maintenace"
date: 2010-09-14
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/09/lazily-enabled-truth-maintenace.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Lazily Enabled Truth Maintenace](<https://blog.kie.org/2010/09/lazily-enabled-truth-maintenace.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 14, 2010  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Three weeks ago I posted the project idea for [“Left and Right Unlinking”](<http://blog.athico.com/2010/08/left-and-right-unlinking-community.html>). So far there are no takers, so if you are interested let me know :)

In the meantime I tried to think of a simpler enhancement that we would like to see done.

At the moment Drools has a user setting “MaintainTMSOption” which can be true or false. It’s a small optimisation that when turned off avoids using the equality hashmap that is maintained for all inserted objects.

It would be a much better idea to remove this configuration setting, thus simplifying things for end users and have TMS lazily enabled on demand.

For each object type there is an “ObjectTypeConf” configuration object that is retrieved every time a working memory action, such as insert, is executed. The enabledTMS boolean should be moved there, so there is one per object type, by default it is false.

When a working memory action occurs, like insert, it retrieved the ObjectTypeConf and checks the maintainTms boolean there, instead of the current engine scoped configuration. When a logical insertion occurs and the ObjectTypeConf is retrieved if maintainTms is false it sets the value to true and then iterates the associated ObjectTypeNode memory lazily adding all the objects to the TMS equality map. From then on for that ObjectType all inserted objects are added to that equality map.

With this you now have the advantage of TMS being laziy enabled, so the minor hashmap operation is no longer used and likewise a small memory saving from not populating the map. There is a further advantage that this is now fine grained and when enabled only impacts for that specific object type.

A further enhancement could use a int counter, instead of a boolean. Each logical insertion for that object type increases the counter, each retraction decreases the counter; even if automatically retracted if the truth is broken for that logical assertion. When the counter reaches zero, TMS for that OTN can be disabled. We do not however remove the objects from the equality map, as this would cause “churn” if TMS is continuously enabled and disabled. Instead when TMS is disabled record the current fact counter id. Then if TMS is disabled on a retraction but there is a counter id, we can check that counter id to see if the fact is prior to TMS being disabled and thus would need to be retracted from the equality map.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F09%2Flazily-enabled-truth-maintenace.html&linkname=Lazily%20Enabled%20Truth%20Maintenace> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F09%2Flazily-enabled-truth-maintenace.html&linkname=Lazily%20Enabled%20Truth%20Maintenace> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F09%2Flazily-enabled-truth-maintenace.html&linkname=Lazily%20Enabled%20Truth%20Maintenace> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F09%2Flazily-enabled-truth-maintenace.html&linkname=Lazily%20Enabled%20Truth%20Maintenace> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F09%2Flazily-enabled-truth-maintenace.html&linkname=Lazily%20Enabled%20Truth%20Maintenace> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F09%2Flazily-enabled-truth-maintenace.html&linkname=Lazily%20Enabled%20Truth%20Maintenace> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F09%2Flazily-enabled-truth-maintenace.html&linkname=Lazily%20Enabled%20Truth%20Maintenace> "Email")
  *[]: 2010-05-25T16:11:00+02:00