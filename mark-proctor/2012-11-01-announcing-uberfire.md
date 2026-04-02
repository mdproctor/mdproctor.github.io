---
layout: post
title: "Announcing UberFire"
date: 2012-11-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/11/announcing-uberfire.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Announcing UberFire](<https://blog.kie.org/2012/11/announcing-uberfire.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- November 1, 2012  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

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

2\. Rich Client App

**Screenshots**

Here are some screenshots of our Showcase demo application

1\. Login

[![](/legacy/assets/images/2012/11/b693e3a0d475-1-login.png)](<http://1.bp.blogspot.com/-NmJVtWS2WWM/UJKr1vOVTmI/AAAAAAAAApo/QlRmf_Jh9ys/s1600/1-login.png>)

2\. Home perspective with same panels including You Tube videos.

[![](/legacy/assets/images/2012/11/cfed27d82014-2-home.png)](<http://1.bp.blogspot.com/-mCilQnc9tMQ/UJKr8VAUA9I/AAAAAAAAApw/ir9ZeDkyuiQ/s1600/2-home.png>)

3\. Selecting a new perspective.

[![](/legacy/assets/images/2012/11/efb9bf6715cf-3-new_perspective.png)](<http://2.bp.blogspot.com/-3jbOw83eMTQ/UJKr9T6PfTI/AAAAAAAAAp4/W8ViF8IGCpU/s1600/3-new_perspective.png>)

4\. Dashboard composed by some panels, including mounted Google gadgets.

[![](/legacy/assets/images/2012/11/b4c556ee36f3-4-dashboard.png)](<http://4.bp.blogspot.com/-oExraaazNQU/UJKr-G7RyrI/AAAAAAAAAqA/3Ykyz0mONZ4/s1600/4-dashboard.png>)

5\. Notice the “File explorer” any GIT repo can be created or cloned, with seamless server side storage. Also notice the context sensitive toolbar and menu bar entries, because the “File Explorer” panel has focus.

[![](/legacy/assets/images/2012/11/0e1b9f0596fb-5-file_explorer.png)](<http://2.bp.blogspot.com/-Rj3kXAQ5dXY/UJKr_MPUIBI/AAAAAAAAAqI/EitF1gNamlg/s1600/5-file_explorer.png>)

6\. Markdown editor with live preview.

[![](/legacy/assets/images/2012/11/a25853f96bcb-6-mdeditor.png)](<http://1.bp.blogspot.com/-1KQLJV7QeJ8/UJKr_1wgquI/AAAAAAAAAqQ/X_xZsfAwQRw/s1600/6-mdeditor.png>)

7\. Panel drag and drop – The compass helps give visual indication for the drop zone. Panels can either be dropped onto the current panel, and added as a tab, or they can dragged to a new panel area, below it is added to the bottom.

[![](/legacy/assets/images/2012/11/b42f78866eb3-7-drag-n-drop.png)](<http://2.bp.blogspot.com/-v4p71nfVbcY/UJKsAzDwkxI/AAAAAAAAAqU/JCN3G4zmNvk/s1600/7-drag-n-drop.png>)

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

UberFire is also a great opportunity if you’re looking for make an Open Source contribution, as this is a very new project we have lot’s of things to do. Click [here](<http://github.com/droolsjbpm/uberfire/wiki/Contribute>) to get some ideas for contributions.****

**Getting started now**

With all that said, we invite you to visit our landing page at <http://droolsjbpm.github.com/uberfire>

Get the latest artifacts from [JBoss Nexus](<https://repository.jboss.org/nexus/index.html#nexus-search;gav~org.uberfire*~~~~>), or download our binary distribution direct from here.

Try it out and give us some feed-back on our [user list](<https://lists.jboss.org/mailman/listinfo/uberfire-users>).

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F11%2Fannouncing-uberfire.html&linkname=Announcing%20UberFire> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F11%2Fannouncing-uberfire.html&linkname=Announcing%20UberFire> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F11%2Fannouncing-uberfire.html&linkname=Announcing%20UberFire> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F11%2Fannouncing-uberfire.html&linkname=Announcing%20UberFire> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F11%2Fannouncing-uberfire.html&linkname=Announcing%20UberFire> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F11%2Fannouncing-uberfire.html&linkname=Announcing%20UberFire> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F11%2Fannouncing-uberfire.html&linkname=Announcing%20UberFire> "Email")
  *[]: 2010-05-25T16:11:00+02:00