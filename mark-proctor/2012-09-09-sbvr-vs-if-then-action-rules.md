---
layout: post
title: "SBVR vs If-Then-Action Rules"
date: 2012-09-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/09/sbvr-vs-if-then-action-rules.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [SBVR vs If-Then-Action Rules](<https://blog.kie.org/2012/09/sbvr-vs-if-then-action-rules.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 9, 2012  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I just found a nice interview with Ronald G. Ross about SBVR, that helps shed some light on how this works in relation to If-Then format’s.

**More on the If-Then Format for Expressing Business Rules**  
<http://www.brcommunity.com/b588.php>  
…snip…

 _Question: Do you have a rote way to translate an If-Then statement into declarative form?_  
_  
__RGR: You can’t translate If-Then-Action statements into declarative form because the business intent is missing. Translating If-Then-Fact back and forth from RuleSpeak, on the other hand, is trivial. We do that often. One client described it “embarrassingly easy.”_  
 _  
__Question: What would RuleSpeak do with the business rule, “If the news is bad, shoot the messenger.”?_  
_  
__RGR: As currently structured, that statement uses the If-Then-Action format. In declarative form it would read: The messenger of bad news must be shot. Or if you prefer the If-Then-Fact format then: If the news is bad, the messenger must be shot._  
_  
__By the way, the business rule in its present form is not practicable. For example, does the messenger need to be shot dead? And does the messenger actually need to be shot, or is just killing him sufficient?_  
_  
__Question: What would RuleSpeak do with the business rule, “If a rental car is returned more than one hour late, charge a late-return penalty.”?_  
_  
__RGR: That statement again uses the If-Then-Action format. In declarative form it would read: A late-return penalty must be charged for a car rental if the rental car is returned over one hour late. Or if you prefer the If-Then-Fact format then: If a rental car is returned over one hour late, a late-return penalty must be charged for the car rental._  
_  
__As soon as you let any actions creep into business rules, all bets are off on side effects. As the statements become more and more slanted toward programming, they become less and less comprehensible to business people and to most business analysts as well._  
…snip…

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fsbvr-vs-if-then-action-rules.html&linkname=SBVR%20vs%20If-Then-Action%20Rules> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fsbvr-vs-if-then-action-rules.html&linkname=SBVR%20vs%20If-Then-Action%20Rules> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fsbvr-vs-if-then-action-rules.html&linkname=SBVR%20vs%20If-Then-Action%20Rules> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fsbvr-vs-if-then-action-rules.html&linkname=SBVR%20vs%20If-Then-Action%20Rules> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fsbvr-vs-if-then-action-rules.html&linkname=SBVR%20vs%20If-Then-Action%20Rules> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fsbvr-vs-if-then-action-rules.html&linkname=SBVR%20vs%20If-Then-Action%20Rules> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fsbvr-vs-if-then-action-rules.html&linkname=SBVR%20vs%20If-Then-Action%20Rules> "Email")
  *[]: 2010-05-25T16:11:00+02:00