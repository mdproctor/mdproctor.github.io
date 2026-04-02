---
layout: post
title: "Guvnor's Asset Viewer"
date: 2011-07-25
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/07/guvnors-asset-viewer.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Guvnor’s Asset Viewer](<https://blog.kie.org/2011/07/guvnors-asset-viewer.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 25, 2011  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

New for 5.3.0.Beta1 we have changed where asset groups are shown.

Those familiar with Guvnor 5.2.0 (and prior) will know asset groups have previously been listed within the Explorer tree-view underneath the package name. Starting from 5.3.0.Beta1 we have moved asset groups to a new screen, shown as a tab in the main view.

[![](/legacy/assets/images/2011/07/237687802aa5-Screenshot.png)](<http://1.bp.blogspot.com/-r43QaVPxLlU/Ti1HMdpwtZI/AAAAAAAAAa0/j-Tkq8bVsik/s1600/Screenshot.png>)

The format of the new screen is being trialled for 5.3.0.Beta1. There has been some discussion whether a single table containing all assets would be better – with collapsible rows to group different types of asset.

The immediate problem with this approach is however that finding different asset types on a “paged table” becomes more cumbersome for the user; as they’d have to sort by type and page through.

We therefore ask for community feedback.

The asset groups are configurable within a compile-time preferences file; src/main/resources/drools-asseteditors.xml. This file is used at GWT compile time to wire-up asset types with their respective editor, group and group icon.

An example extract from the foregoing file looks like this:-

<asseteditor>  
<class>org.drools.guvnor.client.modeldriven.ui.RuleModeller</class>  
<format>brl</format>  
<icon>images.ruleAsset()</icon> <title>constants.BusinessRuleAssets()</title>  
</asseteditor>

We have also made a few changes to the Knowledge Bases tree view:-

  * Hierarchical view, as has been the default up to 5.2.0.Final.

  * “Flat” view with no nesting

  * The tree’s nodes can be fully expanded or collapsed.

[![](/legacy/assets/images/2011/07/f505deecae1f-improved-knowledgebases-view1.png)](<http://1.bp.blogspot.com/-RSrlfHBtz6s/Ti6LXRSvtxI/AAAAAAAAAbM/lpeWjk1T3T0/s1600/improved-knowledgebases-view1.png>)

As always you can watch a video demonstrating these features [here](<http://www.youtube.com/watch?v=jdT4fHgc3Qw>) or [here](<http://vimeo.com/26863955>).

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Fguvnors-asset-viewer.html&linkname=Guvnor%E2%80%99s%20Asset%20Viewer> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Fguvnors-asset-viewer.html&linkname=Guvnor%E2%80%99s%20Asset%20Viewer> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Fguvnors-asset-viewer.html&linkname=Guvnor%E2%80%99s%20Asset%20Viewer> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Fguvnors-asset-viewer.html&linkname=Guvnor%E2%80%99s%20Asset%20Viewer> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Fguvnors-asset-viewer.html&linkname=Guvnor%E2%80%99s%20Asset%20Viewer> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Fguvnors-asset-viewer.html&linkname=Guvnor%E2%80%99s%20Asset%20Viewer> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F07%2Fguvnors-asset-viewer.html&linkname=Guvnor%E2%80%99s%20Asset%20Viewer> "Email")
  *[]: 2010-05-25T16:11:00+02:00