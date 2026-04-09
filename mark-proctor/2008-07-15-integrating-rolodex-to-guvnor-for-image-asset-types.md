---
layout: post
title: "Integrating Rolodex to Guvnor for Image Asset Types"
date: 2008-07-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/integrating-rolodex-to-guvnor-for-image-asset-types.html
---

In [Guvnor](<http://blog.athico.com/2008/04/brms-for-drools-5.html>), there are many different widgets that are used to display or edit different assets. One interesting widget is about to be added – a widget that could accept images and display them. For this purpose, [rolodex](<http://code.google.com/p/gwt-rolodex/>), a widget that can display a stack of images, can be used. Rolodex uses deferred binding for the image generation and animation. Let’s see how can we quickly add a new widget displaying some predefined images.

First, create a class, implementing RolodexCardBundle interface (from the rolodex library) and declare a few methods that will return the images (just like ImageBundle described in [the book](<http://arhipov.blogspot.com/2008/06/studying-google-web-toolkit.html>)):

```
public abstract class Images implements RolodexCardBundle {

   /**
    * @gwt.resource img_3861.jpg
    */
   public abstract RolodexCard imgA();

   /**
    * @gwt.resource img_3863.jpg
    */
   public abstract RolodexCard imgB();

   /**
    * @gwt.resource img_3865.jpg
    */
   public abstract RolodexCard imgC();

   ...

   private final RolodexCard[] cards = new RolodexCard[]{ imgA(), imgB(), imgC() };

   public RolodexCard[] getRolodexCards() {
      return cards;
   }
}
```

Next, to display those images, create ImageSetWidget (or you-name-it) class extending DirtyableComposite:

```java
public class ImageSetEditor extends DirtyableComposite {
 // asset and viewer are not used now...
 public ImageSetEditor(RuleAsset asset, RuleViewer viewer) {
   final Images images = (Images) GWT.create(Images.class);
   final RolodexPanel rolodex
        = new RolodexPanel(images, 3, images.imgA(), true);
   initWidget(rolodex);
 }
}
```

For Guvnor to be able to launch the editor, we have to modify EditorLauncher class:

```
...
else if (asset.metaData.format.equals(AssetFormats.IMAGE_SET)) {
 return new ImageSetEditor(asset, viewer);
...
```

AssetFormats should be supplied with the new constant for this new type, of course.

To allow user to create such widgets in UI, a new menu item needs to be added.

[![](/legacy/assets/images/2008/07/1568e4324531-menu-imageset.png)](</assets/images/2008/07/0f43dada7a80-menu-imageset.png>)  
This means, ExplorerLayoutManger#rulesNewMenu() should be modified

```java
m.addItem(new Item("New ImageSet",
 new BaseItemListenerAdapter() {
   public void onClick(BaseItem item, EventObject e) {
     launchWizard(AssetFormats.IMAGE_SET, "New ImageSet", true);
   }
}, "images/rule_asset.gif"));
```

And last, but not least we need to include the following line in Guvnor.gwt.xml

```
<inherits name='com.yesmail.gwt.rolodex.Rolodex'/>
```

Now, after the project has been rebuilt and redeployed we get the following widget on the screen:

[![](/legacy/assets/images/2008/07/23184d46e9c2-rolodex-in-guvnor.png)](</assets/images/2008/07/640123f0172f-rolodex-in-guvnor.png>)  
Currenly, the widget is displaying a predefined set of images and animates them as we roll the mouse over. So we have now a rolodex-powered widget inside Guvnor. Sounds cool! :)

Now, there are a lot of TODOs to make use of this new cool widget.

  * Menus should be pluggable. So far I knew that the only class that we should generate in order to support adding new rule editor widgets. Without doubt, a user needs a button to create the widget in his workspace, and therefor we should inject the new menu item. I suppose we can generate this part also. Therefore we need to extract the ExplorerLayoutManger#rulesNewMenu() method into a separate class.  
Currently I have an ant task ready to generate a new EditorLauncher class source to plug a new asset type editor. But perhaps, if we have more of these classes to be generated, I’d better add a new ruby script to do this job.
  * Upload of new images. There’s no use of this widget if it can redisplay only the predefined set of images.

[![](/legacy/assets/images/2008/07/40eb69230da5-extended-rolodex-widget-in-guvnor.png)](</assets/images/2008/07/3f081eba2156-extended-rolodex-widget-in-guvnor.png>)

  * RuleAsset support for images.The images should be supplied via the RuleAsset, i.e. the content should be a class that could represent a set of images.
  * A content handler is required as well.