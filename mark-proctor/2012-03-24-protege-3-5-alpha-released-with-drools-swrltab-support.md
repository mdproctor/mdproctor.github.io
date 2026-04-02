---
layout: post
title: "Protege 3.5 Alpha released with Drools SWRLTab support"
date: 2012-03-24
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/03/protege-3-5-alpha-released-with-drools-swrltab-support.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Protege 3.5 Alpha released with Drools SWRLTab support](<https://blog.kie.org/2012/03/protege-3-5-alpha-released-with-drools-swrltab-support.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 24, 2012  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Thanks to[ Martin O’Connor, from Stanford,](<http://bmir.stanford.edu/people/view.php/martin_j_oconnor>) for implementing the Drools SWRLTab for Protege:   
[http://protegewiki.stanford.edu/wiki/Protege_3.5_Alpha_Release_Notes ](<http://protegewiki.stanford.edu/wiki/Protege_3.5_Alpha_Release_Notes%20>)  
—–

**We are pleased to announce Protege 3.5 alpha! The main focus of the 3.5 series is the SWRLTab’s support of the Drools rule engine, thus providing a completely free and open source solution for executing SWRL rules in Protege-OWL.**

Please contact us via one of the [Protege 3 mailing lists](<http://protege.stanford.edu/community/lists.html>) with questions, feedback, and bug reports.   
Download [Protege 3.5 alpha](<http://protege.stanford.edu/download/registered.html#p3.5>) from the main Protege website (new users, please [register first](<http://protege.stanford.edu/download/register.html>)).

##  Release Notes 

The contents of the release notes section describe changes relative to Protege 3.4.8.

###  Build 643 — March 23, 2012 

The [SWRLTab](<http://protege.cim3.net/cgi-bin/wiki.pl?SWRLTab>) now supports the [Drools](<http://www.jboss.org/drools>) rule engine.

A new tab called the [SWRLDroolsTab](<http://protege.cim3.net/cgi-bin/wiki.pl?SWRLDroolsTab>) provides a graphical interface for interacting with this implementation. The existing [SWRLJessTab](<http://protege.cim3.net/cgi-bin/wiki.pl?SWRLJessTab>) is still available. All existing [SWRL built-in libraries](<http://protege.cim3.net/cgi-bin/wiki.pl?SWRLTabBuiltInLibraries>) are supported in the Drools implementation.

Both the Drools and Jess implementations now use a pair of [OWL 2 RL](<http://www.w3.org/TR/owl2-profiles/#OWL_2_RL>)-based reasoners for performing inference ([read more](<http://protege.cim3.net/cgi-bin/wiki.pl?SWRLTabOWL2RL>)). These reasoners are also used by the [SQWRL](<http://protege.cim3.net/cgi-bin/wiki.pl?SQWRL>) query language.

The Java APIs provided by the SWRLTab have changed slightly so users of these APIs will need to update their code. Information on these changes can be found [here](<http://protege.cim3.net/cgi-bin/wiki.pl?SWRLTabAPIUpdating>). The process of building the SWRLTab and its associated rule engines has also changed. The new build process is outlined [here](<http://protege.cim3.net/cgi-bin/wiki.pl?SWRLTabBuilding>).

[![](/legacy/assets/images/2012/03/79b040a58d05-SWRLDroolsTab.png)](<http://protegewiki.stanford.edu/images/e/e1/SWRLDroolsTab.png>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fprotege-3-5-alpha-released-with-drools-swrltab-support.html&linkname=Protege%203.5%20Alpha%20released%20with%20Drools%20SWRLTab%20support> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fprotege-3-5-alpha-released-with-drools-swrltab-support.html&linkname=Protege%203.5%20Alpha%20released%20with%20Drools%20SWRLTab%20support> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fprotege-3-5-alpha-released-with-drools-swrltab-support.html&linkname=Protege%203.5%20Alpha%20released%20with%20Drools%20SWRLTab%20support> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fprotege-3-5-alpha-released-with-drools-swrltab-support.html&linkname=Protege%203.5%20Alpha%20released%20with%20Drools%20SWRLTab%20support> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fprotege-3-5-alpha-released-with-drools-swrltab-support.html&linkname=Protege%203.5%20Alpha%20released%20with%20Drools%20SWRLTab%20support> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fprotege-3-5-alpha-released-with-drools-swrltab-support.html&linkname=Protege%203.5%20Alpha%20released%20with%20Drools%20SWRLTab%20support> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fprotege-3-5-alpha-released-with-drools-swrltab-support.html&linkname=Protege%203.5%20Alpha%20released%20with%20Drools%20SWRLTab%20support> "Email")
  *[]: 2010-05-25T16:11:00+02:00