---
layout: post
title: "Fun UI Projects we need help with"
date: 2012-10-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/10/fun-ui-projects-we-need-help-with.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Fun UI Projects we need help with](<https://blog.kie.org/2012/10/fun-ui-projects-we-need-help-with.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- October 18, 2012  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

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

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F10%2Ffun-ui-projects-we-need-help-with.html&linkname=Fun%20UI%20Projects%20we%20need%20help%20with> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F10%2Ffun-ui-projects-we-need-help-with.html&linkname=Fun%20UI%20Projects%20we%20need%20help%20with> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F10%2Ffun-ui-projects-we-need-help-with.html&linkname=Fun%20UI%20Projects%20we%20need%20help%20with> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F10%2Ffun-ui-projects-we-need-help-with.html&linkname=Fun%20UI%20Projects%20we%20need%20help%20with> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F10%2Ffun-ui-projects-we-need-help-with.html&linkname=Fun%20UI%20Projects%20we%20need%20help%20with> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F10%2Ffun-ui-projects-we-need-help-with.html&linkname=Fun%20UI%20Projects%20we%20need%20help%20with> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F10%2Ffun-ui-projects-we-need-help-with.html&linkname=Fun%20UI%20Projects%20we%20need%20help%20with> "Email")
  *[]: 2010-05-25T16:11:00+02:00