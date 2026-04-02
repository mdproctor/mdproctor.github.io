---
layout: post
title: "XPath and JBoss Rules integration with SXC"
date: 2007-04-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/04/xpath-and-jboss-rules-integration-with-sxc.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [XPath and JBoss Rules integration with SXC](<https://blog.kie.org/2007/04/xpath-and-jboss-rules-integration-with-sxc.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- April 1, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

SXC (Simple XML Compiler)  
SXC has just been released and is a must have for any SOA project – <http://sxc.codehaus.org/> – best of all it comes with JBoss Rules integration :) SXC is a pluggeable XML compiler that provides a high performance streaming XPath parser with JBoss Rules integration. It allows you to specify XPath querries in your rules, as the XML is parsed those rules are then applied, you do not need to write additional XPath statements else where.
[code]
    rule "AddresTest"  
    when  
        event : XPathEvent( expression == "/order/address[@country]" );  
    then  
        System.out.println("Success! - " + drools.getRule().getName());  
    end  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F04%2Fxpath-and-jboss-rules-integration-with-sxc.html&linkname=XPath%20and%20JBoss%20Rules%20integration%20with%20SXC> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F04%2Fxpath-and-jboss-rules-integration-with-sxc.html&linkname=XPath%20and%20JBoss%20Rules%20integration%20with%20SXC> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F04%2Fxpath-and-jboss-rules-integration-with-sxc.html&linkname=XPath%20and%20JBoss%20Rules%20integration%20with%20SXC> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F04%2Fxpath-and-jboss-rules-integration-with-sxc.html&linkname=XPath%20and%20JBoss%20Rules%20integration%20with%20SXC> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F04%2Fxpath-and-jboss-rules-integration-with-sxc.html&linkname=XPath%20and%20JBoss%20Rules%20integration%20with%20SXC> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F04%2Fxpath-and-jboss-rules-integration-with-sxc.html&linkname=XPath%20and%20JBoss%20Rules%20integration%20with%20SXC> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F04%2Fxpath-and-jboss-rules-integration-with-sxc.html&linkname=XPath%20and%20JBoss%20Rules%20integration%20with%20SXC> "Email")