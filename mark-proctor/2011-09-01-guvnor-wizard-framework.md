---
layout: post
title: "Guvnor Wizard Framework"
date: 2011-09-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/09/guvnor-wizard-framework.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Guvnor Wizard Framework](<https://blog.kie.org/2011/09/guvnor-wizard-framework.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 1, 2011  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

I was asked by Mark Proctor to add a Wizard to Guvnor facilitating the creation of a guided Decision Table (i.e. the web-based one!) by Business Users. As a pre-cursor to the specific Wizard in question I needed a generic Wizard framework…

I wrote a framework in Guvnor that others can hopefully use to write their own Wizards. Other developers can write their own Wizards by implementing only the following requirements:-  

  * Extend AbstractWizard. AbstractWizard is the base-class for the whole Wizard.

  * Write a series of Wizard pages implementing WizardPage. WizardPage is an interface for a single page of the whole Wizard.

  * Write a Wizard context implementing WizardContext. WizardContext is used in conjunction with WizardPlace by MVP to launch the correct Wizard.  

  * AmendWizardFactoryImpl to return an instance of your Wizard depending upon the WizardContext. WizardFactoryImpl is used to create an instance of the correct Wizard based upon the WizardContext. The framework is not meant for run-time extension and hence reflection has not been used.

Here’s a screenshot of a Wizard:-

[![](/legacy/assets/images/2011/09/79a15f4a266e-Screenshot-1.png)](<http://4.bp.blogspot.com/-Tp7YDPNnY_4/Tl-hGiUIP9I/AAAAAAAAAb4/mgqqyixjk0A/s1600/Screenshot-1.png>)

As always, a video of operation, is available [here](<http://vimeo.com/28473009>).

Now I have this in place I can carry on writing the required Wizard :)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F09%2Fguvnor-wizard-framework.html&linkname=Guvnor%20Wizard%20Framework> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F09%2Fguvnor-wizard-framework.html&linkname=Guvnor%20Wizard%20Framework> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F09%2Fguvnor-wizard-framework.html&linkname=Guvnor%20Wizard%20Framework> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F09%2Fguvnor-wizard-framework.html&linkname=Guvnor%20Wizard%20Framework> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F09%2Fguvnor-wizard-framework.html&linkname=Guvnor%20Wizard%20Framework> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F09%2Fguvnor-wizard-framework.html&linkname=Guvnor%20Wizard%20Framework> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F09%2Fguvnor-wizard-framework.html&linkname=Guvnor%20Wizard%20Framework> "Email")
  *[]: 2010-05-25T16:11:00+02:00