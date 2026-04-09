---
layout: post
title: "Drools & jBPM Community versus Product"
date: 2011-04-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/04/drools-jbpm-community-versus-product.html
---

A question that comes up often is what is the difference between community and product versions – or .org vs .com for short. What is the difference between Drools and BRMS.

As there is no product for jBPM5 yet, I’ll focus on Drools and BRMS – but the arguments are the same.

Branding  
First let me explain the brandings and what relates to what and is made up of what. JBoss BRMS is the branded product offering from Red Hat; for which you can buy support subscriptions and professional services, such as training and on-site consultancy. JBoss itself is a Red Hat brand for it’s Java middleware.

JBoss BRMS is made up from a number of community projects – Drools Expert, Fusion and Flow and Guvnor. Flow is already deprecated and has been incorporated into jBPM5; Drools will work with jBPM5 going forward.

Multi-Year support  
Red Hat commits to supporting a product release over a large number of years, the length varies from product to product. Cumulative patch releases ensure you get select bug fixes and mature features that have been more extensively tested, without the risk of new bleeding edge features. And the assurance that we will be there for the long term. .org does not do maintenance releases it’s a continuously forward moving R&D project, living on the [bleeding edge](<http://en.wikipedia.org/wiki/Bleeding_edge_technology>). If you want the fixes you are going to get all the new features too, and the risks that come with them. Getting community support for previous .org releases can be hard and introduces elements of risk – Red Hat engineers will not burden themselves answering or helping on .org legacy releases, leaving you to the mercy of a volunteer based community. This is important to ensure that research continues at a fast pace – see Unburdening R&D.

Red Hat provides additional detailed notes on this, see:  
[JBoss Enterprise Middleware product update and support policy](<https://access.redhat.com/support/policy/updates/jboss_notes/>)

Sanity through Sanitization  
A common fear with OSS is due to the transparency people get to the ongoing R&D. From casual inspection this can seem quite hairy as end users are exposed to all the unstable, unfinished and experimental works. This leaves a lot of uncertainty and fear in using OSS in a production environment.

Closed source companies get to do all their R&D behind closed doors, and end users are only exposed and aware of the highly polished marketing.

.com addresses this issue by removing or demarcating experimental or unstable features. To ensure there is a level of sanity and trust in what you are using. The product is typically 3 to 6 months behind in features, but offers strong levels of stability as a result. .com ensures you never have the dreaded “skip x.0 releases, wait for the x.1” which .org releases come with.

Cross platform and version compatibility  
Released products are tested across the range of JBoss and Red Hat products and also multiple versions. So if you are using JBoss BRMS you’ll know it’ll work on the range of AS services, or the JBoss SOA stack.

We also check compatibility across other platforms such as Websphere and even IBM z/OS.

.org community releases do not go through this compatibility matrix level of testing. If our unit tests pass on on hudson, we are release it.

Direct impact on Roadmap  
By being a .com customer you have a direct line to influence the roadmap and urgent bugs. Resources are prioritized for customers versus community jira’s or mailing lists posts. It is also the only way to get Red Hat engineering resources for help on legacy releases, they will ignore .org legacy issues in the community.

Community Independence  
By separating .org from .com it ensures that R&D can be bottom up user and community driven. This ensures a healthy eco system for ideas and innovation and collaboration – compared to a top down marketing driven model. The life cycle of .com and .org feeding into each other ensures the best of both worlds and help’s maintain an important but delicate balance of innovation versus sanity and stability.

I should add that .org is still relevant and important for .com customers as it provides an open environment for them to get involved and upstream their work, which may eventually end up in the product.

Unburden R&D  
Everything that goes into ensuring a great product for the enterprise version entails a lot of work. You need a lot of resources that have meticulous attention to detail. Their priorities will be different to the R&D developers priorities. Stability and maintenance are the enemy of innovation. To ensure we have continued innovation at a project level it’s important that we isolate R&D from these pressures. So everything about the product process is about freeing up the .org R&D developers so they can focus on ideas and innovations.

If you have any further questions on JBoss BRMS product, then please contact sales@jboss.org  
![](/legacy/assets/images/2011/04/c299d0c256bf-comparo_table.png)