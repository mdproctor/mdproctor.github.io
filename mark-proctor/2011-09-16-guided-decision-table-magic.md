---
layout: post
title: "Guided Decision Table magic"
date: 2011-09-16
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/09/guided-decision-table-magic.html
---

Following from my previous [blog](<http://blog.athico.com/2011/09/guvnor-wizard-framework.html>) about the Wizard Framework added to Guvnor I have now had time to complete a Wizard to aid with the creation of new decision tables in Guvnor. This will be available in Drools 5.3, 5.3.CR1 is out end of this week.

[![](/legacy/assets/images/2011/09/98a300b4b9d9-wizard3.png)](</assets/images/2011/09/ee17d0d97cb6-wizard3.png>)

The Wizard takes the user through both the condition definition and action definition process, with full immediate visual validation and feedback of errors in the definition that need correcting before the table can be generated:-

  * Adding Facts
  * Adding constraints to these Facts
  * Setting fields on bound Facts
  * Inserting new Facts

What’s also exciting is the ability to now generate an expanded form decision table; where rows are created for every combination of discrete condition combinations. An explanation of expanded form can be found [here](<http://www.slideshare.net/manstis/buenos-aires-decision-table-presentation>).

[![](/legacy/assets/images/2011/09/e32c74ab45ab-wizard6b.png)](</assets/images/2011/09/fd498da4705b-wizard6b.png>)

It is the first step we are making towards providing expansion and contraction of decision tables in Guvnor.

You can watch a video [here](<http://vimeo.com/29157326>).