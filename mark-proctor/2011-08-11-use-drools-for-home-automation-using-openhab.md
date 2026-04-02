---
layout: post
title: "Use Drools for Home Automation using OpenHAB"
date: 2011-08-11
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/08/use-drools-for-home-automation-using-openhab.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Use Drools for Home Automation using OpenHAB](<https://blog.kie.org/2011/08/use-drools-for-home-automation-using-openhab.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- August 11, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

<http://code.google.com/p/openhab/wiki/Drools>  

## “Introduction

The open Home Automation Bus (openHAB) project aims at providing a universal integration platform for all things around home automation.

It is designed to be absolutely vendor-neutral as well as hardware/protocol-agnostic. openHAB brings together different bus systems, hardware devices and interface protocols by dedicated bindings. These bindings send and receive commands and status updates on the openHAB event bus. This concept allows designing user interfaces with a unique look&feel, but with the possibility to operate devices based on a big number of different technologies. Besides the user interfaces, it also brings the power of automation logics across different system boundaries.”

…

## “Defining the When clause (LHS)

The when clause (LHS) of a rule should contain conditions based on the objects in the working memory, i.e. items and events.

Here is an example of a when clause: 
[code]
            $event : StateEvent(itemName=="Rain", changed==true)
      
            $window  : Item(name=="Window", state==OpenClosedType.OPEN)
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fuse-drools-for-home-automation-using-openhab.html&linkname=Use%20Drools%20for%20Home%20Automation%20using%20OpenHAB> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fuse-drools-for-home-automation-using-openhab.html&linkname=Use%20Drools%20for%20Home%20Automation%20using%20OpenHAB> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fuse-drools-for-home-automation-using-openhab.html&linkname=Use%20Drools%20for%20Home%20Automation%20using%20OpenHAB> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fuse-drools-for-home-automation-using-openhab.html&linkname=Use%20Drools%20for%20Home%20Automation%20using%20OpenHAB> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fuse-drools-for-home-automation-using-openhab.html&linkname=Use%20Drools%20for%20Home%20Automation%20using%20OpenHAB> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fuse-drools-for-home-automation-using-openhab.html&linkname=Use%20Drools%20for%20Home%20Automation%20using%20OpenHAB> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F08%2Fuse-drools-for-home-automation-using-openhab.html&linkname=Use%20Drools%20for%20Home%20Automation%20using%20OpenHAB> "Email")
  *[]: 2010-05-25T16:11:00+02:00