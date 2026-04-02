---
layout: post
title: "Guvnor - Using jBPM Work Items in decision tables"
date: 2011-11-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/11/guvnor-using-jbpm-work-items-in-decision-tables.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Guvnor – Using jBPM Work Items in decision tables](<https://blog.kie.org/2011/11/guvnor-using-jbpm-work-items-in-decision-tables.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- November 6, 2011  
[Process](<https://blog.kie.org/category/process>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

Work is now complete for 5.4.0.beta1 to use jBPM Work Items in the guided decision table.

[![](/legacy/assets/images/2011/11/f34169330bbe-dtable.png)](<http://2.bp.blogspot.com/-q8S4k9EeVRE/Trb8VLy9x2I/AAAAAAAAAc4/AsgPZb_K_ls/s1600/dtable.png>)

New Actions have been added to perform the following:-

  * Call a Work Item. Parameters can be either literal values, or bound to a Fact or Fact Field.

  * Set the value of a field on an existing Fact to the value of a Work Item result.

  * Set the value of a field on a new Fact to the value of a Work Item result.

[![](/legacy/assets/images/2011/11/ae6ffdd9d138-actions.png)](<http://1.bp.blogspot.com/-24nsM6JlGuA/TrcBANon9aI/AAAAAAAAAdE/zQLjhw266SI/s1600/actions.png>)

Significantly, to maximize the usefulness of using Work Items in actions, is the ability to define bindings for Fact field values. This allows Facts’ fields to be passed to Work Items.

Bound fields can also be used in predicate and formula Condition definitions too; which opens a world of further possibility which up until now has been unavailable.

[![](/legacy/assets/images/2011/11/068c4a4ba99f-binding.png)](<http://1.bp.blogspot.com/-iBk91wKnHV0/TrcBI9WYE0I/AAAAAAAAAdQ/oCu_7nDYWOE/s1600/binding.png>)

Work Item definitions can either be defined as assets in Guvnor or included in a workitem-definitions.xml the format of which follows the normal jBPM Work Item definition.

A short video [here](<http://vimeo.com/31693827>) demonstrates using Work Items in a decision table and a short example of how the feature can be leveraged from a Java application.

Unrelated to Work Items, but a welcome addition, is the ability to define an action to retract Facts.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F11%2Fguvnor-using-jbpm-work-items-in-decision-tables.html&linkname=Guvnor%20%E2%80%93%20Using%20jBPM%20Work%20Items%20in%20decision%20tables> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F11%2Fguvnor-using-jbpm-work-items-in-decision-tables.html&linkname=Guvnor%20%E2%80%93%20Using%20jBPM%20Work%20Items%20in%20decision%20tables> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F11%2Fguvnor-using-jbpm-work-items-in-decision-tables.html&linkname=Guvnor%20%E2%80%93%20Using%20jBPM%20Work%20Items%20in%20decision%20tables> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F11%2Fguvnor-using-jbpm-work-items-in-decision-tables.html&linkname=Guvnor%20%E2%80%93%20Using%20jBPM%20Work%20Items%20in%20decision%20tables> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F11%2Fguvnor-using-jbpm-work-items-in-decision-tables.html&linkname=Guvnor%20%E2%80%93%20Using%20jBPM%20Work%20Items%20in%20decision%20tables> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F11%2Fguvnor-using-jbpm-work-items-in-decision-tables.html&linkname=Guvnor%20%E2%80%93%20Using%20jBPM%20Work%20Items%20in%20decision%20tables> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F11%2Fguvnor-using-jbpm-work-items-in-decision-tables.html&linkname=Guvnor%20%E2%80%93%20Using%20jBPM%20Work%20Items%20in%20decision%20tables> "Email")
  *[]: 2010-05-25T16:11:00+02:00