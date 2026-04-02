---
layout: post
title: "Drools Smooks Data Loader"
date: 2008-07-05
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/drools-smooks-data-loader.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Smooks Data Loader](<https://blog.kie.org/2008/07/drools-smooks-data-loader.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 5, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

[Smooks](<http://milyn.codehaus.org/>) is a powerful open source ETL tool, it can transform variety of data sources.

[![](/legacy/assets/images/2008/07/3cf4804093c7-smooks-usecase.gif)](<http://bp1.blogger.com/_Jrhwx8X9P7g/SG-CJKaIWCI/AAAAAAAAAKI/QyJd48fTupg/s1600-h/smooks-usecase.gif>)

Drools now supports an internal model, so ideally you want to be able to load different payloads, such as XML, into this model. I’ve just added support for this and it’ll be in M2 :)

Here is an example of the api loading an XML file into a drools session, the xml entries for OrderItem are mapped into the internal class and inserted into the given session. The matching rules simple do a print statement.
[code]
    declare OrderItem  
        productId : long  
        quantity : Integer  
        price : double  
    end  
      
    rule someRule  
    when  
        $i : OrderItem()  
    then  
        System.out.println( $i );   
    end
[/code]
[code]
    PackageBuilder pkgBuilder = new PackageBuilder();  
    pkgBuilder.addPackageFromDrl( new InputStreamReader( getClass().getResourceAsStream( "test.drl" )) );  
      
    RuleBase ruleBase = RuleBaseFactory.newRuleBase();  
    ruleBase.addPackage( pkgBuilder.getPackage() );  
      
    StatefulSession session = ruleBase.newStatefulSession();  
      
    // Instantiate Smooks with the config...  
    Smooks smooks = new Smooks( "smooks-config.xml" );  
      
    // set rood id  
    DroolsSmooksConfiguration conf = new DroolsSmooksConfiguration( "root" );  
    DroolsSmooks loader = new DroolsSmooks( session, smooks, conf );  
    loader.insertFilter( new StreamSource( new ByteArrayInputStream( readInputMessage() ) ) );  
      
    session.fireAllRules();
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-smooks-data-loader.html&linkname=Drools%20Smooks%20Data%20Loader> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-smooks-data-loader.html&linkname=Drools%20Smooks%20Data%20Loader> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-smooks-data-loader.html&linkname=Drools%20Smooks%20Data%20Loader> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-smooks-data-loader.html&linkname=Drools%20Smooks%20Data%20Loader> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-smooks-data-loader.html&linkname=Drools%20Smooks%20Data%20Loader> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-smooks-data-loader.html&linkname=Drools%20Smooks%20Data%20Loader> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F07%2Fdrools-smooks-data-loader.html&linkname=Drools%20Smooks%20Data%20Loader> "Email")