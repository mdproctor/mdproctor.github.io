---
layout: post
title: "W3C Rule Interchange Format for Production Rule Systems"
date: 2007-06-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/w3c-rule-interchange-format-for-production-rule-systems.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [W3C Rule Interchange Format for Production Rule Systems](<https://blog.kie.org/2007/06/w3c-rule-interchange-format-for-production-rule-systems.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 1, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’ve just had the pleasure of working with Ilog on a Production Rule (PR) dialect implementation for the [W3C’s Rule Interchange Format (RIF)](<http://www.w3.org/2005/rules/>). The goal of RIF is to create a universal rule interchange format specification for all reasoning systems, they have focused on building a [RIF Core](<http://www.w3.org/TR/rif-core/>) based on [Horn Rules](<http://www.w3.org/TR/rif-core/#Horn_Rules>), with dialect extensions for the different reasoning systems,

Ilog undertook the hard work of devising a simple proof of concept xml language and the marshaller to a pojo AST. The scope was kept very simple focusing on literal constraints and function calls.

A while back the [MISMO](<http://www.mismo.org/>) group contacted us and said they wanted to attempt a proof of concept (POC) for rule standardisation within the MISMO group, they provided some real world data for us to work against. We all agreed to developed a PR RIF dialect for JRules and JBoss Rules, with the idea of demoing these two systems working off the same rule documents and payloads in a web service environment. Click image to enlarge:  
[![](/legacy/assets/images/2007/06/1b6b7db0c3ef-mismo1.PNG)](<http://bp0.blogger.com/_Jrhwx8X9P7g/RmJGWj7W5FI/AAAAAAAAABs/DgDOAK-M4HQ/s1600-h/mismo1.PNG>)  
It was decided that the implementation would not extend the available elements at this stage, staying with 10 elements provided by [RIF Core](<http://www.w3.org/TR/rif-core/>), Click image to enlarge:  
[![](/legacy/assets/images/2007/06/cdafc7e8aeda-ConditionModel.png)](<http://bp3.blogger.com/_Jrhwx8X9P7g/RmI3rT7W5EI/AAAAAAAAABk/yhgzYe7bZPU/s1600-h/ConditionModel.png>)  
By staying with the RIF Core elements to represent a PR System you end up with a very generic and weak XML with no ability for semantic validation via a schema xsd. Let’s take a look at a very simple literal constraint, in DRL this would be:  
CreditScore(division == “division”)

In PR RIF it’s:  
<Equal>  
<Uniterm>  
<Const type=”xsd:QName”>aprif:xmlGetter</Const>  
<Const type=”xsd:QName”>ns0:CreditScore</Const>  
<Const>division</Const>  
<Var type=”ns0:CreditScore”>cs</Var>  
</Uniterm>  
<Const type=”xsd:string”>Wholesale</Const>  
</Equal>

The problem is that we have no idea what that Uniterm is, it’s role is contained within the element’s text “aprif:xmlGetter”. This means the entire XML block must be parsed and validated by PR RIF validator, instead of being able to leverage standard validation languages like Schema XSD. My preference is that we build richer higher level XML language, such as:  
<literal-constraint slot=”division” type=”xs:string”>Wholesale</literal-constraint>

This would facilitate as much XSD validation up front, the mapping to RIF core can be dictated in the spec and XSLT translators provided.

In this POC each constraint must be placed on a variable, this means all Patterns must be bound to a variable, which is obviously not needed in PR Systems – I hope that is something which is eventually resolved. The XML to show this concept is quite verbose, so I’ll show what this limitation would look like in DRL:  
CreditScore(division == “division”)  
Instead it must be:  
cs : CreditScore( cs.division == “division”)

Another area likely to be of contention is the ability to navigate nested structures, using a ‘from’ like conditional element. Personally I hope this is accepted, but I know it is not supported by PR Systems that only allow “value types” to be used as fields; i.e. strings, numbers, booleans etc. Disallowing nested structures would certainly be a step back for modern PR Systems.

Another concern was on the weakness of type, for instance we need to be able to differentiate between decimals and currency.

Those wanting to go deeper can checkout the project from subversion here:  
<http://anonsvn.labs.jboss.com/labs/jbossrules/contrib/apocrif/>

This is an eclipse project and consists of three projects:

  * apocrif
    * The core module and handles the RIF XML marshalling.
  * jbossrules
    * The JBoss Rules implementation, works out of the box with unit tests, all jars are provded in the lib directory, the wonders of working with an open source system :)
  * jrules
    * The source code is there but won’t work, or even compile, as it is missing the neccessary Ilog JRules dependencies.

In the jbossrules project there is a single test class, JBossRulesTest, that shows everything done to date, including a full integration test with the MISMO provided data:  
<http://anonsvn.labs.jboss.com/labs/jbossrules/contrib/apocrif/jbossrules/src/test/java/jbossrules/tests/JBossRulesTest.java>

I previously blogged on the technical aspects of this implementation, including payload marshalling and nested object navigation:  
[Working with JBoss Rules and Web Services](<http://markproctor.blogspot.com/2007/05/working-with-jboss-rules-and-web.html>)

For those without subversion clients I have zipped up the check and place here:  
<http://wiki.jboss.org/wiki/attach?page=JBossRules%2Fapocrif1.1.zip>

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fw3c-rule-interchange-format-for-production-rule-systems.html&linkname=W3C%20Rule%20Interchange%20Format%20for%20Production%20Rule%20Systems> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fw3c-rule-interchange-format-for-production-rule-systems.html&linkname=W3C%20Rule%20Interchange%20Format%20for%20Production%20Rule%20Systems> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fw3c-rule-interchange-format-for-production-rule-systems.html&linkname=W3C%20Rule%20Interchange%20Format%20for%20Production%20Rule%20Systems> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fw3c-rule-interchange-format-for-production-rule-systems.html&linkname=W3C%20Rule%20Interchange%20Format%20for%20Production%20Rule%20Systems> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fw3c-rule-interchange-format-for-production-rule-systems.html&linkname=W3C%20Rule%20Interchange%20Format%20for%20Production%20Rule%20Systems> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fw3c-rule-interchange-format-for-production-rule-systems.html&linkname=W3C%20Rule%20Interchange%20Format%20for%20Production%20Rule%20Systems> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fw3c-rule-interchange-format-for-production-rule-systems.html&linkname=W3C%20Rule%20Interchange%20Format%20for%20Production%20Rule%20Systems> "Email")