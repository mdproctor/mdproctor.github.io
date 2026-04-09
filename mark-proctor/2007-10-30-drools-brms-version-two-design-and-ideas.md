---
layout: post
title: "Drools BRMS version two design and ideas"
date: 2007-10-30
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/10/drools-brms-version-two-design-and-ideas.html
---

Hi folks

After delivering 4.0.3 Michael and I had some conversations about adding more features and a complete re-design of the BRMS web interface. Basically we are looking at how to break things up into “perspectives” kind of like eclipse has (but simpler), just to make it easier to present the user with the information they need for their current work example:

  1. BA type users (no package configuration, follow templates, read only sometimes etc)
  2. Developers (configure stuff – eventually should only need eclipse so this doesn’t have to be too strong on the web side)
  3. Admins/operator types (migrate, security setup etc).

Nothing that complex, but we do need to have it scale up and down to these skill levels.

I think we can do something like merging the previous BRMS organization with the new tree feature. We do like the tree/explorer motif, fairly familiar to most people and easy to make it filterable based on both server side and user settings. Also, its more like ideas that the jboss web console is moving to.

The new package feature  

> **📷 Missing image** — _BRMS2_

Categorization  

> **📷 Missing image** — _BRMS1_

Administration  

> **📷 Missing image** — _BRMS4_

Also with this refactory we will enable I18n internationalization then people can easily edit the bundle file/config to add they own language setting. Other key features like rule based authorization and custom queries are also some of the new features.

The new BRMS design concept  

> **📷 Missing image** — _BRMSv2_