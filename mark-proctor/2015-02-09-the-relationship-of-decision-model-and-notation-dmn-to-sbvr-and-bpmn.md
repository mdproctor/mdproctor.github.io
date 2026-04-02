---
layout: post
title: "The Relationship of Decision Model and Notation (DMN) to SBVR and BPMN"
date: 2015-02-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/02/the-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [The Relationship of Decision Model and Notation (DMN) to SBVR and BPMN](<https://blog.kie.org/2015/02/the-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 9, 2015  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

<http://www.brcommunity.com/b597.php> (Full Article)

**Overview**  
“Publications by James Taylor and Neil Raden[[2]](<http://www.brcommunity.com/b597.php#fn2>), Barbara von Halle and Larry Goldberg[[1]](<http://www.brcommunity.com/b597.php#fn1>), Ron Ross[[7]](<http://www.brcommunity.com/b597.php#fn7>), and others have popularized “Decision Modeling.” The very short summary is that this is about modeling business decision logic for and by business users.

[](<http://blog.athico.com/>)[](<http://blog.athico.com/>)A recent  _Decision Modeling Information Day_ conducted by the Object Management Group (OMG)[[4]](<http://www.brcommunity.com/b597.php#fn4>) showed considerable interest among customers, consultants, and software vendors. The OMG followed up by releasing a Request for Proposals (RFP) for a Decision Model and Notation (DMN) specification.[[5]](<http://www.brcommunity.com/b597.php#fn5>) According to the RFP,

> “Decision Models are developed to define how businesses make decisions, usually as a part of a business process model (covered by the OMG BPMN standard in Business Process Management Solutions). Such models are both business (for example, using business vocabularies per OMG SBVR) and IT (for example, mapping to rule engines per OMG PRR in Business Rule Management Systems).”

[](<http://blog.athico.com/>)[](<http://blog.athico.com/>)This quote says a little about how DMN may relate to SBVR[[6]](<http://www.brcommunity.com/b597.php#fn6>) and BPMN[[3]](<http://www.brcommunity.com/b597.php#fn3>), but there are many more open questions than answers. How do SBVR rules relate to decisions? Is there just one or are there multiple decisions per SBVR rule? Is there more to say about how SBVR and DMN relate to BPMN?

This article attempts to “position” DMN against the SBVR and BPMN specifications. Of course, DMN doesn’t exist yet so the concepts presented here are more the authors’ ideas about how these three specifications ** _should_** relate to each other, than reality. We present these ideas in the hope that they will positively influence the discussions that lead up to the DMN specification.”

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F02%2Fthe-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html&linkname=The%20Relationship%20of%20Decision%20Model%20and%20Notation%20%28DMN%29%20to%20SBVR%20and%20BPMN> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F02%2Fthe-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html&linkname=The%20Relationship%20of%20Decision%20Model%20and%20Notation%20%28DMN%29%20to%20SBVR%20and%20BPMN> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F02%2Fthe-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html&linkname=The%20Relationship%20of%20Decision%20Model%20and%20Notation%20%28DMN%29%20to%20SBVR%20and%20BPMN> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F02%2Fthe-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html&linkname=The%20Relationship%20of%20Decision%20Model%20and%20Notation%20%28DMN%29%20to%20SBVR%20and%20BPMN> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F02%2Fthe-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html&linkname=The%20Relationship%20of%20Decision%20Model%20and%20Notation%20%28DMN%29%20to%20SBVR%20and%20BPMN> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F02%2Fthe-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html&linkname=The%20Relationship%20of%20Decision%20Model%20and%20Notation%20%28DMN%29%20to%20SBVR%20and%20BPMN> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2015%2F02%2Fthe-relationship-of-decision-model-and-notation-dmn-to-sbvr-and-bpmn.html&linkname=The%20Relationship%20of%20Decision%20Model%20and%20Notation%20%28DMN%29%20to%20SBVR%20and%20BPMN> "Email")
  *[]: 2010-05-25T16:11:00+02:00