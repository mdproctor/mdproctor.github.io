---
layout: post
title: "API and Language changes"
date: 2007-06-12
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/api-and-language-changes.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [API and Language changes](<https://blog.kie.org/2007/06/api-and-language-changes.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 12, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’ve given notice several times on the mailing lists for these changes, so thought I would put the info up on the blog too, for maximum exposure. These changes are now under way.

assert will change to insert

  * Avoid the constant keyword collision with “assert”, most languages are seem to support this now
  * Will change in both the drl and working memory api

modify to become update

  * Instead of workingMemory.modify(FactHandle, Object) it will be workingMemory.update(FactHandle, Object), will change modify to update in drl.
  * This method is now only used for ShadowFact objects, it’s a method to let the engine know that an external object has been updated and to update it’s internal cache. and reprocess.
  * Avoid keyword collision in MVEL which has nice “modify” sugar now

insertObject (assertObject), retractObject and updateObject to beome insert, retract and update

  * The Object part seems superflous, might as well remove it, especially as we start to support None Object fact types
  * drl and working memory api will now use the same method names.

Added new WorkingMemory modifyRetract and modifyAssert methods

  * Allows for non shadow fact objects.
  * When not using shadow facts (although will ofcourse work with shadow facts) you cannot call ‘update’, or what use to be called ‘modify’, because we need to know the “old” value of fields so we can retract the from the workign memory. The only safe way is to first retract the object and then assert it. However with the existing api this adds extra work and results in new fact handle. modifyRetract and modifyAssert can now be used together to “simulate” a modify on a none shadow fact object in two parts. First call modifyRetract, then change your field values, then call modifyAssert.
  * AMVEL has sugar to do: modify ( person ) { age += 1, location = “london” }, what actually happens here is it first calls modifyRetract then applies the setters and then calles modifyAssert.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fapi-and-language-changes.html&linkname=API%20and%20Language%20changes> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fapi-and-language-changes.html&linkname=API%20and%20Language%20changes> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fapi-and-language-changes.html&linkname=API%20and%20Language%20changes> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fapi-and-language-changes.html&linkname=API%20and%20Language%20changes> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fapi-and-language-changes.html&linkname=API%20and%20Language%20changes> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fapi-and-language-changes.html&linkname=API%20and%20Language%20changes> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fapi-and-language-changes.html&linkname=API%20and%20Language%20changes> "Email")