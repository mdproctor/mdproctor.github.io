---
layout: post
title: "More Widgets for Guvnor (Anton Arhipov)"
date: 2008-08-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/08/more-widgets-for-guvnor-anton-arhipov.html
---

For properties and XML editors in Guvnor I’m trying to make use of GWT-Ext components. The widgets from this library look really nice. Also the API looks OK. For the properties widget, theres a PropertiesGridPanel available, which provides some nice features for editing the properties (see the screenshot below).

[![](/legacy/assets/images/2008/08/a225e5a8b453-gwtext_prop.png)](</assets/images/2008/08/8c4951e214f8-gwtext_prop.png>)

.. and a piece of code that assembles the panel:

```
PropertyGridPanel grid = new PropertyGridPanel();
    GridView view = new GridView();
    grid.setView(view);
    Map map = new HashMap();
    PropertyHolder[] props = getProps(); //RPC call here
    for (PropertyHolder holder : props.list) {
      map.put(holder.name,holder.value);
    }
    grid.setSource(map);
```

How does it know which editor should be attached to the value column? Simple the type is known at the compile time! One of the benefits of GWT is claimed to be its performance. It is fast, but this power comes at a price – you cannot leave the type undefined, i.e. you cannot use java.lang.Object for the type of your class members.

Consider the following class, which is intended for exchanging the information via RPC calls:

```java
public class PropertyHolder implements IsSerializable {
        public String name;
        public Object value; // coudn't use Object type here
    }
```

While trying to compile this code down to javaScript, we’ll get the following messages from the GWT’s compiler:

```
org.drools.guvnor.client.ruleeditor.PropertyHolder
     Analyzing the fields of type 'org.drools.guvnor.client.ruleeditor.PropertyHolder' that qualify for serialization
     public java.lang.Object value
     java.lang.Object
     [ERROR] In order to produce smaller client-side code, 'Object' is not allowed; consider using a more specific type
     [ERROR] Type 'org.drools.guvnor.client.ruleeditor.PropertyHolder' was not serializable and has no concrete serializable subtypes
```

So that’s it! I couldn’t think of any solution how to cheat the compiler and leave the value’s type undefined, so I have to use strings for now.