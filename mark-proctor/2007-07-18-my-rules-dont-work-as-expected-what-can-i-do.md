---
layout: post
title: "My rules don't work as expected. What can I do?"
date: 2007-07-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/my-rules-dont-work-as-expected-what-can-i-do.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [My rules don’t work as expected. What can I do?](<https://blog.kie.org/2007/07/my-rules-dont-work-as-expected-what-can-i-do.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 18, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

A good blog [entry ](<http://rbs.gernotstarke.de/faq/faq/faq-devel.html>)from Dr. Gernot Starke, I love the opening paragraph, which can’t be said enough :)  
“Welcome to real life. Don’t ever believe that rules can and will be written by business-people only.”

Another useful titbit is to use an Agenda Filter with a Stateless Session. You use the AgendaFilter to isolate the rule(s) you wish to test. The Agenda Filter can be setup just once on the session and then collections of data can be executed against the session. You can then change the Agenda Filter when you wish to test a different rule.
[code]
      
    StatelessSession session = ruleBase.newStatelessSesssion();  
      
    session.setAgendaFilter( new RuleNameMatches("<regexp to your rule name here>") );  
      
    List data = new ArrayList();  
    ... // create your test data here (probably built from some external file)  
      
    StatelessSessionResult result == session.executeWithResults( data );  
      
    // check your results here.  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fmy-rules-dont-work-as-expected-what-can-i-do.html&linkname=My%20rules%20don%E2%80%99t%20work%20as%20expected.%20What%20can%20I%20do%3F> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fmy-rules-dont-work-as-expected-what-can-i-do.html&linkname=My%20rules%20don%E2%80%99t%20work%20as%20expected.%20What%20can%20I%20do%3F> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fmy-rules-dont-work-as-expected-what-can-i-do.html&linkname=My%20rules%20don%E2%80%99t%20work%20as%20expected.%20What%20can%20I%20do%3F> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fmy-rules-dont-work-as-expected-what-can-i-do.html&linkname=My%20rules%20don%E2%80%99t%20work%20as%20expected.%20What%20can%20I%20do%3F> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fmy-rules-dont-work-as-expected-what-can-i-do.html&linkname=My%20rules%20don%E2%80%99t%20work%20as%20expected.%20What%20can%20I%20do%3F> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fmy-rules-dont-work-as-expected-what-can-i-do.html&linkname=My%20rules%20don%E2%80%99t%20work%20as%20expected.%20What%20can%20I%20do%3F> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F07%2Fmy-rules-dont-work-as-expected-what-can-i-do.html&linkname=My%20rules%20don%E2%80%99t%20work%20as%20expected.%20What%20can%20I%20do%3F> "Email")