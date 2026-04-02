---
layout: post
title: "Why Java code is bad for rules and a declarative alternative"
date: 2006-07-10
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2006/07/why-java-code-is-bad-for-rules-and-a-declarative-alternative.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Why Java code is bad for rules and a declarative alternative](<https://blog.kie.org/2006/07/why-java-code-is-bad-for-rules-and-a-declarative-alternative.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- July 10, 2006  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

One of the selling features of Drools, and one of the reasons we are often chosen over competitors, has always been the ability to allow the use of Java code in specific parts of rules; expressions and consequences. This makes for a lower learning curve as Java developers can start writing consequences without additional training; whether its updating a value, sending messages or retrieving information from a database. This alignment with Java, or “Java like” languages, for Rule Engines is often touted by marketing as a reason to choose their systems over others. On the face of it this looks great and its something that management can relate to – less training, leveraging existing skill sets, where’s the down side?

The use of a Java language detracts from the real value of a Production Rule System like Drools. The moment you allow the use of Java code in a rule you encourage the use of imperative programming. Rule Engines offer a Turing complete system with a declarative language, if you read the Drools manual we spend some time explaining propositional and first order logic and how they can be used to describe any scenario in a declarative manner – this is an incredibly power approach to software development. In quick summary Java is imperative because you have describe how to do things, this can often take up many lines of code and means you have to read all those lines of code to understand what it is doing. As the code gets more complex the more lines of code you have to read, eventually to the point that the complexity becomes large enough to make the code difficult to understand and maintain; thus creating a dependency on the original author who becomes the only person able to efficiently maintain the code. Declarative programming allows you to express complex rules using keywords; each rule identifies a specific scenario and details the corresponding actions. Those actions should also be specified in a declarative manner, otherwise we reduce the value of investment that we made in defining and authoring the conditions of the rule. This is very much in spirit with the Business Rules Approach methodology. For those more interested in this methodology I recommend the following three books:  
Business Rules and Information Systems: Aligning IT with Business Goals  
Tony Morgan  
ISBN: 0201743914

Principles of the Business Rule Approach  
Ronald G. Ross  
ISBN: 0201788934

Business Rules Applied  
Von Halle  
ISBN: 0471412937

So the moment we start putting in complex nested if structures and loops into our consequence we increase the complexity of maintenance. Instead the consequence should focus on the calling of functions or object methods. Each function or method has a clear and documented role; it specifies the parameters it takes, the operations it makes on those parameters and what it returns – they also align themselves better to be represented with a simple domain specific language.

While Drools has no plans to drop its Java support and we soon hope to be adding back in Groovy and later Javascript – we also want to introduce a language that will support the declarative approach, rather than detract from it. This new language will then become the “default” standard that we push for rule authoring.

So what should such a language include?

  * full expression support

  * Auto-box and auto-unbox

  * Object method calls

  * Object field assignments

  * Object creation

  * simple declerative data structures

  * basic if/switch/loop support (to be used sparingly)

I’m still trying to decide if we need support for anonymous classes – there may be times when we need to specify callbacks or action listeners on objects. However this obviously adds a level of complexity that I wish to avoid inside of consequences and may well be something that should be farmed out to function or method. Control structures like if/switch/loop might also be made configurably “optional” and discouraged. The language should be able to work in both interpreted and compiled mode. Compiled mode allows for maximum speed execution and is ideal for small to medium systems – large systems in the thousands of rules will suffer permgen issues and it may be best to use interpreted mode.

I have done some searching but most languages are “complete” in that they are full blown languages for application development – we need something much smaller and simpler. This is more inline with what templating languages, like FreeMarker and Velocity, already have – but is not available as a stand alone language. I have recently discovered [“Simple Declarative Language”](<http://sdl.ikayzo.org/docs/display/SDL/Home%3Cbr%20/%3E>) which seems to go in the right direction; but has no support for function or method calls or expression evaluation – that I can see – however with the absence of anything else on the market it may be a good place to start in building our own solution.

[Post Comment](<https://beta.blogger.com/comment.g?blogID=5869426&postID=4815006043127514921>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F07%2Fwhy-java-code-is-bad-for-rules-and-a-declarative-alternative.html&linkname=Why%20Java%20code%20is%20bad%20for%20rules%20and%20a%20declarative%20alternative> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F07%2Fwhy-java-code-is-bad-for-rules-and-a-declarative-alternative.html&linkname=Why%20Java%20code%20is%20bad%20for%20rules%20and%20a%20declarative%20alternative> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F07%2Fwhy-java-code-is-bad-for-rules-and-a-declarative-alternative.html&linkname=Why%20Java%20code%20is%20bad%20for%20rules%20and%20a%20declarative%20alternative> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F07%2Fwhy-java-code-is-bad-for-rules-and-a-declarative-alternative.html&linkname=Why%20Java%20code%20is%20bad%20for%20rules%20and%20a%20declarative%20alternative> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F07%2Fwhy-java-code-is-bad-for-rules-and-a-declarative-alternative.html&linkname=Why%20Java%20code%20is%20bad%20for%20rules%20and%20a%20declarative%20alternative> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F07%2Fwhy-java-code-is-bad-for-rules-and-a-declarative-alternative.html&linkname=Why%20Java%20code%20is%20bad%20for%20rules%20and%20a%20declarative%20alternative> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2006%2F07%2Fwhy-java-code-is-bad-for-rules-and-a-declarative-alternative.html&linkname=Why%20Java%20code%20is%20bad%20for%20rules%20and%20a%20declarative%20alternative> "Email")