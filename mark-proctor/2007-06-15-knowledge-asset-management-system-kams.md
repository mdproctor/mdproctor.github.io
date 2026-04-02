---
layout: post
title: "Knowledge Asset Management System (KAMS)"
date: 2007-06-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/knowledge-asset-management-system-kams.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Knowledge Asset Management System (KAMS)](<https://blog.kie.org/2007/06/knowledge-asset-management-system-kams.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 15, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I just read this article over at infoq which is titled [“CentraSite: Registry/Repository and Free Community Edition”](<http://www.infoq.com/news/2007/06/sag-centrasite-31>). I’m glad that someone is getting this message out, it’s something I’ve been pushing internally for a while now; Enterprise Government is serious and important stuff and deserves more attention.

I want people to realise that rules, processes, policies, xstl transformations, routing configurations, hibernate mapping files etc are all important pieces of enterprise knowledge, for this reason I also prefer the term “asset” to “artefact” to signify that these artefacts are assets of value. I also believe the term “Registry/Repository” under sells the idea. You aren’t just creating a JNDI lookup type system for files, all stored assets are versioned along [dublin core](<http://dublincore.org/>) meta data and user defined classifications. These assets can be be further combined to create configurations of assets, also versioned. If we talk in terms of “rules” you create a package which is a configuration of one or more rules; a specific package configuration will use a specific version of a rule, just because a rule gets updated doesn’t mean I want that version of the package configuration to use the newer version of the rule; if I want that I have to create a new version of the package configuration. This provides an important level of auditing, it means applications using this system can be audited to let us know at any point in time what policies where being applied.

Our BRMS, which we are thinking of renaming to KAMS, is a step in this direction. At the core it’s just versionable, categorisable and configurable assets, of any type built ontop of [Jackrabbit JCR](<http://jackrabbit.apache.org/>) – which is a much stronger spec than [JXR](<http://java.sun.com/webservices/jaxr/index.jsp>) which [CentreSite](<http://www.softwareag.com/de/products/centrasite/default.asp>) is built on. This is in fact a seperate and self contained project, seperate from any rules or gui stuff. Ontop of this is the BRMS, which is built with GWT, currently much of this is hard coded for asset types – like rules, process etc. The plan is to eventually refactor this into a base system with extension points for different asset types.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fknowledge-asset-management-system-kams.html&linkname=Knowledge%20Asset%20Management%20System%20%28KAMS%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fknowledge-asset-management-system-kams.html&linkname=Knowledge%20Asset%20Management%20System%20%28KAMS%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fknowledge-asset-management-system-kams.html&linkname=Knowledge%20Asset%20Management%20System%20%28KAMS%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fknowledge-asset-management-system-kams.html&linkname=Knowledge%20Asset%20Management%20System%20%28KAMS%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fknowledge-asset-management-system-kams.html&linkname=Knowledge%20Asset%20Management%20System%20%28KAMS%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fknowledge-asset-management-system-kams.html&linkname=Knowledge%20Asset%20Management%20System%20%28KAMS%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fknowledge-asset-management-system-kams.html&linkname=Knowledge%20Asset%20Management%20System%20%28KAMS%29> "Email")