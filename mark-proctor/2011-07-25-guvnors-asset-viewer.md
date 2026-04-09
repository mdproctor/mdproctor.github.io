---
layout: post
title: "Guvnor's Asset Viewer"
date: 2011-07-25
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/07/guvnors-asset-viewer.html
---

### Guvnor’s Asset Viewer

New for 5.3.0.Beta1 we have changed where asset groups are shown.

Those familiar with Guvnor 5.2.0 (and prior) will know asset groups have previously been listed within the Explorer tree-view underneath the package name. Starting from 5.3.0.Beta1 we have moved asset groups to a new screen, shown as a tab in the main view.

[![](/legacy/assets/images/2011/07/237687802aa5-Screenshot.png)](</assets/images/2011/07/3f8c28f0310c-Screenshot.png>)

The format of the new screen is being trialled for 5.3.0.Beta1. There has been some discussion whether a single table containing all assets would be better – with collapsible rows to group different types of asset.

The immediate problem with this approach is however that finding different asset types on a “paged table” becomes more cumbersome for the user; as they’d have to sort by type and page through.

We therefore ask for community feedback.

The asset groups are configurable within a compile-time preferences file; src/main/resources/drools-asseteditors.xml. This file is used at GWT compile time to wire-up asset types with their respective editor, group and group icon.

An example extract from the foregoing file looks like this:-

```xml
<asseteditor>
  <class>org.drools.guvnor.client.modeldriven.ui.RuleModeller</class>
  <format>brl</format>
  <icon>images.ruleAsset()</icon>
  <title>constants.BusinessRuleAssets()</title>
</asseteditor>
```

We have also made a few changes to the Knowledge Bases tree view:-

  * Hierarchical view, as has been the default up to 5.2.0.Final.

  * “Flat” view with no nesting

  * The tree’s nodes can be fully expanded or collapsed.

[![](/legacy/assets/images/2011/07/f505deecae1f-improved-knowledgebases-view1.png)](</assets/images/2011/07/5174779aa7f3-improved-knowledgebases-view1.png>)

As always you can watch a video demonstrating these features [here](<http://www.youtube.com/watch?v=jdT4fHgc3Qw>) or [here](<http://vimeo.com/26863955>).