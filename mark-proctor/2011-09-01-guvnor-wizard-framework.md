---
layout: post
title: "Guvnor Wizard Framework"
date: 2011-09-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/09/guvnor-wizard-framework.html
---

I was asked by Mark Proctor to add a Wizard to Guvnor facilitating the creation of a guided Decision Table (i.e. the web-based one!) by Business Users. As a pre-cursor to the specific Wizard in question I needed a generic Wizard framework…

I wrote a framework in Guvnor that others can hopefully use to write their own Wizards. Other developers can write their own Wizards by implementing only the following requirements:-  

  * Extend AbstractWizard. AbstractWizard is the base-class for the whole Wizard.

  * Write a series of Wizard pages implementing WizardPage. WizardPage is an interface for a single page of the whole Wizard.

  * Write a Wizard context implementing WizardContext. WizardContext is used in conjunction with WizardPlace by MVP to launch the correct Wizard.  

  * AmendWizardFactoryImpl to return an instance of your Wizard depending upon the WizardContext. WizardFactoryImpl is used to create an instance of the correct Wizard based upon the WizardContext. The framework is not meant for run-time extension and hence reflection has not been used.

Here’s a screenshot of a Wizard:-

[![](/legacy/assets/images/2011/09/79a15f4a266e-Screenshot-1.png)](</assets/images/2011/09/d520157c4ff6-Screenshot-1.png>)

As always, a video of operation, is available [here](<http://vimeo.com/28473009>).

Now I have this in place I can carry on writing the required Wizard :)