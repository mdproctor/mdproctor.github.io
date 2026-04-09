---
layout: post
title: "Rolodex Panel Assembly for Guvnor (Anton Arhipov)"
date: 2008-07-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/rolodex-panel-assembly-for-guvnor-anton-arhipov.html
---

In my previous post about [integrating rolodex into Guvnor](<http://blog.athico.com/2008/07/integrating-rolodex-to-guvnor-for-image.html>) I tried to create the example just with a set of pre-compiled images which are then assembled into drools-guvnor.war. But the real goal is actually to display the pictures stored in Jackrabbit repository for Guvnor.  
Now, after some experiments with rolodex and Guvnor, I have a widget where one may upload a picture and display it.

[![](/legacy/assets/images/2008/07/092895f2eb83-rolodex-working-widget-single-image.png)](</assets/images/2008/07/392f49afedf2-rolodex-working-widget-single-image.png>)Currently it can accept only one picture per RuleAsset class instance. Therefore the content handler for this asset should be extended to support multiple images per RuleAsset.

```
RolodexCardBundle images = getImagesFromAsset();
RolodexCard[] rolodexCards = images.getRolodexCards();
if (rolodexCards.length > 0) {
   final RolodexPanel rolodex =
   new RolodexPanel(images, 3, rolodexCards[0], true);
   layout.addRow(rolodex);
}
```

I have set the hight of the panel manually as the picture was cropped otherwise in the widget. (Don’t know the reason yet). getImagesFromAsset() is used for converting the asset’s content to the RolodexCard:

```
public RolodexCardBundle getImagesFromAsset() {
   return new RolodexCardBundle() {
      ClippedImagePrototype clip = new ClippedImagePrototype(
         GWT.getModuleBaseURL() + "asset?" + HTMLFileManagerFields.FORM_FIELD_UUID 
                                +  "=" + asset.uuid, 0, 0, 300, 200 );

      RolodexCard card = new RolodexCard(clip, clip, clip, 300, 100, 10);

      public int getMaxHeight() {
        return 200;
      }

      public RolodexCard[] getRolodexCards() {
        return new RolodexCard[]{card};
     }
  };
}
```

I’ve cheated with the code that composes the RolodexCard, as ClippedImagePrototype’s javadoc says:

This class is used internally by the image bundle generator and is not intended for general use. It is subject to change without warning.

But the implementation of ClippedImagePrototype is actually what I need. Probably, if it is really the subject to change at any time, I would rather cope’n’paste this class into Guvnor code base.

TODO:  
A heavy part of the work will have to be carried out by the content handler. The content handler will have to support the multiple images per asset and also perform some graphics routines in order to replace the pre-compilation phase implemented in rolodex to adjust images.