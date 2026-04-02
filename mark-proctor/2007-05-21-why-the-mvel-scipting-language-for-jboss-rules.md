---
layout: post
title: "Why the MVEL scipting language for JBoss Rules"
date: 2007-05-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/why-the-mvel-scipting-language-for-jboss-rules.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Why the MVEL scipting language for JBoss Rules](<https://blog.kie.org/2007/05/why-the-mvel-scipting-language-for-jboss-rules.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 21, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’m currently working hard to finish off the pluggeable dialect system, this is similar to the semantic modules we had in Drools 2.0. With this people will be able to write drl dialect implementatinos for any language they like and then users can use that language to author their predicates, return values, evals and consequences. We will be supporting two dialect implementations one for Java and another for [MVEL, http://mvel.codehaus.org/](<http://mvel.codehaus.org/>). So of couse the first thing people ask is why MVEL, why not Groovy, Jython etc, so I put the following together:

  * Reflection/bytecode(JIT) compilation and execution modes.
    * For huge systems we need to be able to avoid excessive bytecode generation, but still have the option for bytecode JIT for performance sensitive areas.
  * Fast reflection mode.
    * We originally started with our own language [JFDI](<http://markproctor.blogspot.com/2006/11/jfdi-new-business-action-scripting.html>), which was designed to be a simple and fast reflection based language, the idea is all work is done at compile time so runtime is just a series of reflection invokers. This design has been carried through to MVEL, so that it has good enough reflection performance. Where as other languages have to drop reflection mode and use bytecode to get any reasonable level of performance.
  * Pluggeable resolvers.
    * Dictionary population is too slow, MVEL can resolve it’s variable direct from the provided resolvers, which we make array based for performance.
  * Size.
    * MVEL is currently < 350K
  * Custom language extensions.
    * MVEL is extending the language to support rule friendly constructs, in particular block setters. So I can do “modify (person) ( age += 1, location = “london” )” with the ability to treat that as a transaction block so I can run before and after interceptors on the entire block. This is made easier through the use of macros, so we can define our own keywords and have them expanded into mvel code.
  * Static/Inferred typed or dynamic modes.
    * Variables can be untyped and totally dynamic.
    * Variables can be statically typed or type can be inferred, casting is supported.
    * Optional verifier for “typed mode”, disallows dynamic variables and ensures all types and method calls are correct. Which helps with.
      * Authoring time validation.
      * Code completion.
      * Refactoring.
  * Configurable language feature support.
    * Language features can be turned off.
    * We don’t want imperative flow structures in the “then” part, no ‘if’ ‘switch’ etc. Rules should be declarative, “when this do that” not “when this maybe do that”.

MVEL is BSF compliant and will soon support EL too. MVEL is already a superset of EL, but it doesn’t yet support some of the esoteric features like having different ways to express equality.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fwhy-the-mvel-scipting-language-for-jboss-rules.html&linkname=Why%20the%20MVEL%20scipting%20language%20for%20JBoss%20Rules> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fwhy-the-mvel-scipting-language-for-jboss-rules.html&linkname=Why%20the%20MVEL%20scipting%20language%20for%20JBoss%20Rules> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fwhy-the-mvel-scipting-language-for-jboss-rules.html&linkname=Why%20the%20MVEL%20scipting%20language%20for%20JBoss%20Rules> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fwhy-the-mvel-scipting-language-for-jboss-rules.html&linkname=Why%20the%20MVEL%20scipting%20language%20for%20JBoss%20Rules> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fwhy-the-mvel-scipting-language-for-jboss-rules.html&linkname=Why%20the%20MVEL%20scipting%20language%20for%20JBoss%20Rules> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fwhy-the-mvel-scipting-language-for-jboss-rules.html&linkname=Why%20the%20MVEL%20scipting%20language%20for%20JBoss%20Rules> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fwhy-the-mvel-scipting-language-for-jboss-rules.html&linkname=Why%20the%20MVEL%20scipting%20language%20for%20JBoss%20Rules> "Email")