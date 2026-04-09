---
layout: post
title: "API and Language changes"
date: 2007-06-12
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/api-and-language-changes.html
---

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