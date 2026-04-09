---
layout: post
title: "Drools Smooks Data Loader"
date: 2008-07-05
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/drools-smooks-data-loader.html
---

[Smooks](<http://milyn.codehaus.org/>) is a powerful open source ETL tool, it can transform variety of data sources.

[![](/legacy/assets/images/2008/07/3cf4804093c7-smooks-usecase.gif)](</assets/images/2008/07/4bdb71160730-smooks-usecase.gif>)

Drools now supports an internal model, so ideally you want to be able to load different payloads, such as XML, into this model. I’ve just added support for this and it’ll be in M2 :)

Here is an example of the api loading an XML file into a drools session, the xml entries for OrderItem are mapped into the internal class and inserted into the given session. The matching rules simple do a print statement.

```drl
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
```

```
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
```