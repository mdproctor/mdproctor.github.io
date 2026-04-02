---
layout: post
title: "Two Part Drools and Guvnor Tutorial (Brian Du Preez)"
date: 2011-01-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/01/two-part-drools-and-guvnor-tutorial-brian-du-preez.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Two Part Drools and Guvnor Tutorial (Brian Du Preez)](<https://blog.kie.org/2011/01/two-part-drools-and-guvnor-tutorial-brian-du-preez.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- January 17, 2011  
[Rules](<https://blog.kie.org/category/rules>) [Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

[Part 1 (Brian Du Preez)](<http://www.briandupreez.net/2010/11/learning-to-drool-part-1.html>)  
[Part 2 (Brian Du Preez)](<http://www.briandupreez.net/2010/11/learning-to-drool-part-2.html>)

Part 1 (Excerpt – Brian Du Preez)  
This series of posts will be about me getting to grips with [JBoss Drools](<http://www.jboss.org/drools>). The reasoning behind it is: SAP bought out my company’s current rules engine and Drools is one alternative we will be looking into as soon as someone has the skills to get a proof of concept up.

Although there seems to be a fair amount of documentation, I always find it helps having walked through examples, which is what I am going to do here.Drools on first glance can be quite daunting, it is made up of :

[Drools Expert](<http://www.jboss.org/drools/drools-expert.html>) (rule engine)  
Being a developer this is where I will begin, the actual rules and implementation of them.

The other parts I’ll get to later are:  
[Drools Guvnor](<http://www.jboss.org/drools/drools-guvnor.html>) (BRMS/BPMS)  
[Drools Flow](<http://www.jboss.org/drools/drools-flow.html>) (process/workflow)  
[Drools Fusion](<http://www.jboss.org/drools/drools-fusion.html>) (event processing/temporal reasoning)  
[Drools Planner](<http://www.jboss.org/drools/drools-planner.html>) (automated planning)

So to begin.  
For part 1, I just want to get my feet wet, I download only the [Eclipse plugin and the binaries ](<http://www.jboss.org/drools/downloads.html>)  
…  
…

[![](/legacy/assets/images/2011/01/c3864bc5d6b4-Guided_20Rule_20Example.jpg)](<http://lh5.ggpht.com/_4oXSoLPl3uY/TNw6pKtEfkI/AAAAAAAAAN0/BljQDr8CphE/Guided%20Rule%20Example.jpg>)  
[![](/legacy/assets/images/2011/01/13e0c94c7141-Decision_20Table.jpg)](<http://lh6.ggpht.com/_4oXSoLPl3uY/TN_zttsAgjI/AAAAAAAAAOM/RwQpE5zz2SY/Decision%20Table.jpg>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Ftwo-part-drools-and-guvnor-tutorial-brian-du-preez.html&linkname=Two%20Part%20Drools%20and%20Guvnor%20Tutorial%20%28Brian%20Du%20Preez%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Ftwo-part-drools-and-guvnor-tutorial-brian-du-preez.html&linkname=Two%20Part%20Drools%20and%20Guvnor%20Tutorial%20%28Brian%20Du%20Preez%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Ftwo-part-drools-and-guvnor-tutorial-brian-du-preez.html&linkname=Two%20Part%20Drools%20and%20Guvnor%20Tutorial%20%28Brian%20Du%20Preez%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Ftwo-part-drools-and-guvnor-tutorial-brian-du-preez.html&linkname=Two%20Part%20Drools%20and%20Guvnor%20Tutorial%20%28Brian%20Du%20Preez%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Ftwo-part-drools-and-guvnor-tutorial-brian-du-preez.html&linkname=Two%20Part%20Drools%20and%20Guvnor%20Tutorial%20%28Brian%20Du%20Preez%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Ftwo-part-drools-and-guvnor-tutorial-brian-du-preez.html&linkname=Two%20Part%20Drools%20and%20Guvnor%20Tutorial%20%28Brian%20Du%20Preez%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2011%2F01%2Ftwo-part-drools-and-guvnor-tutorial-brian-du-preez.html&linkname=Two%20Part%20Drools%20and%20Guvnor%20Tutorial%20%28Brian%20Du%20Preez%29> "Email")
  *[]: 2010-05-25T16:11:00+02:00