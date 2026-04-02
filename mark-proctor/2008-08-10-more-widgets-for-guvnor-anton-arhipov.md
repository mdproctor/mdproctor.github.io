---
layout: post
title: "More Widgets for Guvnor (Anton Arhipov)"
date: 2008-08-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/08/more-widgets-for-guvnor-anton-arhipov.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [More Widgets for Guvnor (Anton Arhipov)](<https://blog.kie.org/2008/08/more-widgets-for-guvnor-anton-arhipov.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- August 10, 2008  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

For properties and XML editors in Guvnor I’m trying to make use of GWT-Ext components. The widgets from this library look really nice. Also the API looks OK. For the properties widget, theres a PropertiesGridPanel available, which provides some nice features for editing the properties (see the screenshot below).

[![](/legacy/assets/images/2008/08/a225e5a8b453-gwtext_prop.png)](<http://3.bp.blogspot.com/_Jrhwx8X9P7g/SJ7s1resy9I/AAAAAAAAALY/ApliEon6NDc/s1600-h/gwtext_prop.png>)

.. and a piece of code that assembles the panel:
[code]
        PropertyGridPanel grid = new PropertyGridPanel();  
        GridView view = new GridView();  
        grid.setView(view);  
        Map map = new HashMap();  
        PropertyHolder[] props = getProps(); //RPC call here  
        for (PropertyHolder holder : props.list) {  
          map.put(holder.name,holder.value);  
        }  
        grid.setSource(map);
[/code]

How does it know which editor should be attached to the value column? Simple the type is known at the compile time! One of the benefits of GWT is claimed to be its performance. It is fast, but this power comes at a price – you cannot leave the type undefined, i.e. you cannot use java.lang.Object for the type of your class members.

Consider the following class, which is intended for exchanging the information via RPC calls:
[code]
        public class PropertyHolder implements IsSerializable {  
            public String name;  
            public Object value; // coudn't use Object type here  
        }
[/code]

While trying to compile this code down to javaScript, we’ll get the following messages from the GWT’s compiler:
[code]
        org.drools.guvnor.client.ruleeditor.PropertyHolder  
         Analyzing the fields of type 'org.drools.guvnor.client.ruleeditor.PropertyHolder' that qualify for serialization  
         public java.lang.Object value  
         java.lang.Object  
         [ERROR] In order to produce smaller client-side code, 'Object' is not allowed; consider using a more specific type  
         [ERROR] Type 'org.drools.guvnor.client.ruleeditor.PropertyHolder' was not serializable and has no concrete serializable subtypes
[/code]

So that’s it! I couldn’t think of any solution how to cheat the compiler and leave the value’s type undefined, so I have to use strings for now.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F08%2Fmore-widgets-for-guvnor-anton-arhipov.html&linkname=More%20Widgets%20for%20Guvnor%20%28Anton%20Arhipov%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F08%2Fmore-widgets-for-guvnor-anton-arhipov.html&linkname=More%20Widgets%20for%20Guvnor%20%28Anton%20Arhipov%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F08%2Fmore-widgets-for-guvnor-anton-arhipov.html&linkname=More%20Widgets%20for%20Guvnor%20%28Anton%20Arhipov%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F08%2Fmore-widgets-for-guvnor-anton-arhipov.html&linkname=More%20Widgets%20for%20Guvnor%20%28Anton%20Arhipov%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F08%2Fmore-widgets-for-guvnor-anton-arhipov.html&linkname=More%20Widgets%20for%20Guvnor%20%28Anton%20Arhipov%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F08%2Fmore-widgets-for-guvnor-anton-arhipov.html&linkname=More%20Widgets%20for%20Guvnor%20%28Anton%20Arhipov%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F08%2Fmore-widgets-for-guvnor-anton-arhipov.html&linkname=More%20Widgets%20for%20Guvnor%20%28Anton%20Arhipov%29> "Email")