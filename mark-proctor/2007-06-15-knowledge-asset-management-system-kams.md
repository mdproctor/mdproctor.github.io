---
layout: post
title: "Knowledge Asset Management System (KAMS)"
date: 2007-06-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/knowledge-asset-management-system-kams.html
---

I just read this article over at infoq which is titled [“CentraSite: Registry/Repository and Free Community Edition”](<http://www.infoq.com/news/2007/06/sag-centrasite-31>). I’m glad that someone is getting this message out, it’s something I’ve been pushing internally for a while now; Enterprise Government is serious and important stuff and deserves more attention.

I want people to realise that rules, processes, policies, xstl transformations, routing configurations, hibernate mapping files etc are all important pieces of enterprise knowledge, for this reason I also prefer the term “asset” to “artefact” to signify that these artefacts are assets of value. I also believe the term “Registry/Repository” under sells the idea. You aren’t just creating a JNDI lookup type system for files, all stored assets are versioned along [dublin core](<http://dublincore.org/>) meta data and user defined classifications. These assets can be be further combined to create configurations of assets, also versioned. If we talk in terms of “rules” you create a package which is a configuration of one or more rules; a specific package configuration will use a specific version of a rule, just because a rule gets updated doesn’t mean I want that version of the package configuration to use the newer version of the rule; if I want that I have to create a new version of the package configuration. This provides an important level of auditing, it means applications using this system can be audited to let us know at any point in time what policies where being applied.

Our BRMS, which we are thinking of renaming to KAMS, is a step in this direction. At the core it’s just versionable, categorisable and configurable assets, of any type built ontop of [Jackrabbit JCR](<http://jackrabbit.apache.org/>) – which is a much stronger spec than [JXR](<http://java.sun.com/webservices/jaxr/index.jsp>) which [CentreSite](<http://www.softwareag.com/de/products/centrasite/default.asp>) is built on. This is in fact a seperate and self contained project, seperate from any rules or gui stuff. Ontop of this is the BRMS, which is built with GWT, currently much of this is hard coded for asset types – like rules, process etc. The plan is to eventually refactor this into a base system with extension points for different asset types.