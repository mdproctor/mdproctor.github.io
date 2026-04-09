---
layout: post
title: "Fun UI Projects we need help with"
date: 2012-10-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/10/fun-ui-projects-we-need-help-with.html
---

We are now very close to an alpha release of our UberFire workbench. Uberfire is an Eclipse like workbench, built with of GWT, Errai and CDI. UF provides a clean and simple extension model for custom panels as plugins. I previously mentioned it in this list post, [found here](<http://drools.46999.n3.nabble.com/rules-users-UderFire-tt4019929.html#a4019938>), which has some screenshots and towards the end a link to an older video.

UberFire will form the foundations for all our web based tooling in the 6.0 series. However it’s a separate standalone project, useful to others, Drools&jBPM will provide all functionality through plugins.

So if you were looking for a fun project, to get involved with some cool tech. It doesn’t get much better than this :) So here are some projects we could do with some help with.

  * Errai JSON Tree Editor
    * “data driven” by the provided domain class model. Domain model drives “suggestion” lists for allowed keys and values, as well as client side validation. Additional annotations might be needed to further constrain the authoring view – i.e. choice, sequence, max/min occurs.
    * Here is a simple JSon tree view that works well. Port this idea to pure GWT as a UF component. Make it easier to add/remove entries and provide type safe entries for keys and values, based on the provided domain model. <http://braincast.nl/samples/jsoneditor/>
    * Errai JSon provides seamless client and server side marshalling of json strings, back into pojo models. <http://docs.jboss.org/errai/2.0.0.Final/errai/reference/html/sid-5931328.html>
  * Audit Viewer
    * Migrate to support ErraiJSon, instead of our XStream dump, for seamless client and server marshalling. This way the client view can load and display any data file, without needing a server component. Bonus points if you can update this to support some sort of “streaming” continuous update of data.
  * Rete Viewer
    * The ReteViewer should be ported to svg/gwt, again using ErraiJSon to provide the tree format.
  * Grid/Tile layout manager for panels.
    * This would be a UF workbench part, which displays the attached panels in a grid/tile layout, allowing vertical/horizontal merging, so one area can be larger than another, and also support DnD. This is instead of current default, where attached panels are displayed in a tab format, where only one tab is visible at a time.

Until we push out the alpha release, you are best placed to contact us via IRC, where we’ll talk you through code, and get you started. Just make sure to use our nicks when asking Qs, so we get notified – ask for porcelli, manstis, salaboy or conan on the #droolsdev channel.  
<http://www.jboss.org/drools/irc>