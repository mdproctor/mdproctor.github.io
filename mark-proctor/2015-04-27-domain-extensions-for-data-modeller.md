---
layout: post
title: "Domain Extensions for Data Modeller"
date: 2015-04-27
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/04/domain-extensions-for-data-modeller.html
---

Walter is working on adding domain extensions to the Data Modeller. This will allow different domains to augment the model – such as custom annotations for JPA or OptaPlanner. Each domain is pluggable via a “facet” extension system. Currently, as a temporary solution, each domain extension is added as an item in the toolbar, but this will change soon. In parallel to this Eder will be working on something similar to [Intellij’s Tool Windows](<https://www.jetbrains.com/idea/help/intellij-idea-tool-windows.html>) for side bars. Once that is ready those domain extensions plugged in as facets and exposed via this tool window capability. Here is a video showing JPA and it’s annotations being used with the Data Modeller.

[![YouTube video: dA54-HJcoSc](/legacy/assets/images/youtube/dA54-HJcoSc.jpg)  
▶ Watch on YouTube](<https://www.youtube.com/watch?v=dA54-HJcoSc>)

(Click to turn on 720p HD and full screen)