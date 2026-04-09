---
layout: post
title: "Announcing UberFire"
date: 2012-11-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/11/announcing-uberfire.html
---

Today we’re pleased to announce the first public release of UberFire, a web based workbench framework inspired by Eclipse Rich Client Platform.

**What is it?**

UberFire is a new independent project developed and maintained by Drool & jBPM team. This is a very strategic project for us, once it’s the base technology for our next generation of web tooling.

One key aspect for UberFire is the compile time composition of plugins. Every plugin can be a maven module, when building a distribution, you simple add those maven modules as dependencies. Those plugins then become available a panels to be placed in perspective, via drag and drop, with docking.

The clean and powerful design was made possible by [GWT](<https://developers.google.com/web-toolkit/>), [Errai](<http://www.jboss.org/errai>) and [CDI](<http://docs.oracle.com/javaee/6/tutorial/doc/giwhl.html>).

In 0.1.0.Alpha1 version we have the following features:

**Workbench API**

  * Perspectives
  * Panels
  * Drag and Drop and Docking
  * Model-View-Presenter framework

**Core Widgets**

  * File Explorer
  * Text Editor
  * Markdown Preview & Live Editor

**Virtual File System API (back port of NIO2)**

  * File System default backend
  * GIT backend

**Security API/Framework**

  * Authentication
  * Authorization

Other important aspect of UberFire APIs is the fact that you can use them for client or server side development. Please remember this is our first alpha release, expect bugs, unfinished features and we’ll work on improving the look and feel over the coming months.

**Video**

1\. Quick tour

This embed could not be captured in the archive. Original source: unknown source

2\. Rich Client App

This embed could not be captured in the archive. Original source: unknown source

**Screenshots**

Here are some screenshots of our Showcase demo application

1\. Login

[![](/legacy/assets/images/2012/11/b693e3a0d475-1-login.png)](</assets/images/2012/11/88a412ce02d9-1-login.png>)

2\. Home perspective with same panels including You Tube videos.

[![](/legacy/assets/images/2012/11/cfed27d82014-2-home.png)](</assets/images/2012/11/625c92bb1c48-2-home.png>)

3\. Selecting a new perspective.

[![](/legacy/assets/images/2012/11/efb9bf6715cf-3-new_perspective.png)](</assets/images/2012/11/7686c6b65f7e-3-new_perspective.png>)

4\. Dashboard composed by some panels, including mounted Google gadgets.

[![](/legacy/assets/images/2012/11/b4c556ee36f3-4-dashboard.png)](</assets/images/2012/11/abb2ebd87a06-4-dashboard.png>)

5\. Notice the “File explorer” any GIT repo can be created or cloned, with seamless server side storage. Also notice the context sensitive toolbar and menu bar entries, because the “File Explorer” panel has focus.

[![](/legacy/assets/images/2012/11/0e1b9f0596fb-5-file_explorer.png)](</assets/images/2012/11/e65515066de1-5-file_explorer.png>)

6\. Markdown editor with live preview.

[![](/legacy/assets/images/2012/11/a25853f96bcb-6-mdeditor.png)](</assets/images/2012/11/050169991b3d-6-mdeditor.png>)

7\. Panel drag and drop – The compass helps give visual indication for the drop zone. Panels can either be dropped onto the current panel, and added as a tab, or they can dragged to a new panel area, below it is added to the bottom.

[![](/legacy/assets/images/2012/11/b42f78866eb3-7-drag-n-drop.png)](</assets/images/2012/11/6df4a891a7b6-7-drag-n-drop.png>)

**  
Important Note:** No effort has yet been spent on its Look & Feel.****

**What to expect in the next releases**

We already have other new features scheduled for next releases (some already under development, others still just a PoC):

  * Metadata engine (index/search)
  * Embeddable infrastructure
  * Panels exposed as IDE Plugins (Eclipse is the first target)

**Eating our own dog food**

There’s nothing like believing in your own ideas than using them for your own work. Drools Guvnor is currently being ported to the UberFire framework. Anybody can experience the extent of our work so far by downloading the latest SNAPSHOT.

Furthermore the jBPM Console is also being ported to UberFire.****

**Community Call**

UberFire is also a great opportunity if you’re looking for make an Open Source contribution, as this is a very new project we have lot’s of things to do. Click [here](<http://github.com/droolsjbpm/uberfire/wiki/Contribute>) to get some ideas for contributions.

**Getting started now**

With all that said, we invite you to visit our landing page at <http://droolsjbpm.github.com/uberfire>

Get the latest artifacts from [JBoss Nexus](<https://repository.jboss.org/nexus/index.html#nexus-search;gav~org.uberfire*~~~~>), or download our binary distribution direct from here.

Try it out and give us some feed-back on our [user list](<https://lists.jboss.org/mailman/listinfo/uberfire-users>).