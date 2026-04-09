---
layout: post
title: "Protege 3.5 Alpha released with Drools SWRLTab support"
date: 2012-03-24
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/03/protege-3-5-alpha-released-with-drools-swrltab-support.html
---

Thanks to[ Martin O’Connor, from Stanford,](<http://bmir.stanford.edu/people/view.php/martin_j_oconnor>) for implementing the Drools SWRLTab for Protege:   
[http://protegewiki.stanford.edu/wiki/Protege_3.5_Alpha_Release_Notes](<http://protegewiki.stanford.edu/wiki/Protege_3.5_Alpha_Release_Notes%20>)   
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

[![](/legacy/assets/images/2012/03/79b040a58d05-SWRLDroolsTab.png)](</assets/images/2012/03/69f28a0eb247-SWRLDroolsTab.png>)