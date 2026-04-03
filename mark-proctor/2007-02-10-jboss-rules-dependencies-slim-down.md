---
layout: post
title: "JBoss Rules dependencies slim down"
date: 2007-02-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/02/jboss-rules-dependencies-slim-down.html
---

As useful as jakarta commons is, it does have a tendency to bloat your classpath, even if just one method is needed from a jar. JBoss Rules uses commons JCI to allow compiler abstraction, which allows us to easily move between the Janino and the Eclipse Java Compiler. JCI relies on commons-logging, commons-lang, commons-collection and commons-io; further to this JCI is split into 3 modules jci-core, jci-janino and jci-eclipse. We have receive a number of complaints on this matter, so I experimented with inlining JCI and ripping out any commons code. The result is we have now reduced our dependency list by 7 additional jars and slimmed the eclipse IDE release down to 7.3MB.

Later I will also move templates from StringTemplate to MVEL, our template use is minimal so we don’t really care what we use. MVEL is a needed dependency and already provides templates, so we might as well use that. The added bonus is that StringTemplate still relies on antlr-2.7.7, so I’ll be able to remove 2 more dependencies.

As part of this work I have also updated to the latest versions of the Eclipse and Janino compilers, which provide static imports even while targetting jdk1.4 src, we will soon update the function implementation to use static imports, which will make them more robust.