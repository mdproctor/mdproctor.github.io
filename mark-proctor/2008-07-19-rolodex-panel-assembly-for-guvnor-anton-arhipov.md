---
layout: post
title: "Rolodex Panel Assembly for Guvnor (Anton Arhipov)"
date: 2008-07-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/rolodex-panel-assembly-for-guvnor-anton-arhipov.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Rolodex Panel Assembly for Guvnor (Anton Arhipov)](<https://blog.kie.org/2008/07/rolodex-panel-assembly-for-guvnor-anton-arhipov.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 19, 2008  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

In my previous post about [integrating rolodex into Guvnor](<http://blog.athico.com/2008/07/integrating-rolodex-to-guvnor-for-image.html>) I tried to create the example just with a set of pre-compiled images which are then assembled into drools-guvnor.war. But the real goal is actually to display the pictures stored in Jackrabbit repository for Guvnor.  
Now, after some experiments with rolodex and Guvnor, I have a widget where one may upload a picture and display it.

[![](/legacy/assets/images/2008/07/092895f2eb83-rolodex-working-widget-single-image.png)](<http://bp0.blogger.com/_Jrhwx8X9P7g/SIE08ALl5FI/AAAAAAAAALA/8nc0Hfn7dyY/s1600-h/rolodex-working-widget-single-image.png>)Currently it can accept only one picture per RuleAsset class instance. Therefore the content handler for this asset should be extended to support multiple images per RuleAsset.
[code]
    RolodexCardBundle images = getImagesFromAsset();  
    RolodexCard[] rolodexCards = images.getRolodexCards();  
    if (rolodexCards.length > 0) {  
       final RolodexPanel rolodex =  
       new RolodexPanel(images, 3, rolodexCards[0], true);  
       layout.addRow(rolodex);  
    }
[/code]

I have set the hight of the panel manually as the picture was cropped otherwise in the widget. (Don’t know the reason yet). getImagesFromAsset() is used for converting the asset’s content to the RolodexCard:
[code]
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
[/code]

I’ve cheated with the code that composes the RolodexCard, as ClippedImagePrototype’s javadoc says:

> This class is used internally by the image bundle generator and is not intended for general use. It is subject to change without warning.

But the implementation of ClippedImagePrototype is actually what I need. Probably, if it is really the subject to change at any time, I would rather cope’n’paste this class into Guvnor code base.

TODO:  
A heavy part of the work will have to be carried out by the content handler. The content handler will have to support the multiple images per asset and also perform some graphics routines in order to replace the pre-compilation phase implemented in rolodex to adjust images.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Frolodex-panel-assembly-for-guvnor-anton-arhipov.html&linkname=Rolodex%20Panel%20Assembly%20for%20Guvnor%20%28Anton%20Arhipov%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Frolodex-panel-assembly-for-guvnor-anton-arhipov.html&linkname=Rolodex%20Panel%20Assembly%20for%20Guvnor%20%28Anton%20Arhipov%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Frolodex-panel-assembly-for-guvnor-anton-arhipov.html&linkname=Rolodex%20Panel%20Assembly%20for%20Guvnor%20%28Anton%20Arhipov%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Frolodex-panel-assembly-for-guvnor-anton-arhipov.html&linkname=Rolodex%20Panel%20Assembly%20for%20Guvnor%20%28Anton%20Arhipov%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Frolodex-panel-assembly-for-guvnor-anton-arhipov.html&linkname=Rolodex%20Panel%20Assembly%20for%20Guvnor%20%28Anton%20Arhipov%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Frolodex-panel-assembly-for-guvnor-anton-arhipov.html&linkname=Rolodex%20Panel%20Assembly%20for%20Guvnor%20%28Anton%20Arhipov%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Frolodex-panel-assembly-for-guvnor-anton-arhipov.html&linkname=Rolodex%20Panel%20Assembly%20for%20Guvnor%20%28Anton%20Arhipov%29> "Email")