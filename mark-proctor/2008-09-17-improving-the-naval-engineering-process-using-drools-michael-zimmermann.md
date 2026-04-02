---
layout: post
title: "Improving the Naval engineering process using Drools ( Michael Zimmermann )"
date: 2008-09-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/09/improving-the-naval-engineering-process-using-drools-michael-zimmermann.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Improving the Naval engineering process using Drools ( Michael Zimmermann )](<https://blog.kie.org/2008/09/improving-the-naval-engineering-process-using-drools-michael-zimmermann.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 17, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Michael Zimmermann, from Rostock University, has emailed us an overview with findings for his Phd thesis on helping to improve the navel engineering process using Drools. The thesis title is “Knowledge based design patterns for detailed steel structural design”.

The Scope: Naval Engineering,

In naval engineering vessels consists of thousands of parts (read: way more than an aircraft has today). Focusing on the steel structure, most of these parts are 2-dimensional plates of a certain size, thickness, grade and contour. For most fields of applications detailed regulations  
from classification societies etc. exist.

Currently, the design of such objects is done using specialized CAD systems. Here the following issues are present in all cad systems and the design process today:

  * Design time is 6 – 18 months (and not 10 – 15 years as for an air plane)
  * This means concurrent design, i. e. different people are working on parts or features that are closely related (strength, fatigue, cost, functional aspects or just being in the same room) on different levels of granularity (changing the hull 6 weeks before building happens!).
  * No connection between design intent (specification on paper), design conditions (regulations, by the customer, results of calculations) and design solution chosen.

Result:

  * We just have the geometrical data, nothing more in the CAD-model
  * No automatic checks if a certain component is changed; no automatic tests if a chosen design solutions really satisfies the conditions at lowest cost today
  * Therefore, changes (which you can’t avoid) are cost intensive and error prone. Also, no one really knows why a certain solutions was chosen

Enter Logic & Drools

The objective of our research is to make the design process context aware. Example: If I design a “door” in a watertight “wall” the cad system should check whether the selected door is a watertight model.

So, using one of the most popular commercial cad systems for naval engineering the approach is to define the standards (currently paper-based) electronically using DROOLS. Also, context-information like watertight, stress level=x … is added to the model and reused in the design process. For standard design tasks (in a part of the field of detailed steel structural design) we use drools to completely automate the design process, i. e.

  * Find a design problem in the model
  * Select a suitable solution adhering to all known boundary conditions
  * Design the solution
  * And assign a assurance level for the solution (how good is it?)

Lessons Learnt from an Engineering POV

  1. Extracting the knowledge is hard
  2. Formulating it logically sound even harder (even official regulations are vague on a regular basis)
  3. Defining the context a solution is valid for is even more difficult.
  4. Current CAD systems in naval engineering are not really capable to store meta information and to interface with other applications.

Lessons Learnt from a Drools POV

  1. Drools is quite a nice system :-)
  2. With DSL even engineers can use it (once they are trained how to “Think Rules”. And that is next to impossible)
  3. What’s missing is some solution to easily define classes, class hierarchies and (!) instance data. We use OWL for now. eCore might be usable yet is terrible from a UI usability perspective
  4. Not drools is the problem but getting the data in and out!
     1. The Smooks binding could be a godsend for this
     2. Fact templates sound really promising if you think dynamically generated classes via web services…

What’s missing in Drools?

  * An OWL/RDF binding would be really great (we use OWL to define, edit, store our standards. But encountered the clash of open world logic (DL) and closed world logic (CS) more than once.) I know there is quite a large interest for such a solution in the Ontology user base.
  * Better support for constraint programming (what we do here and there) for simple primitive cases (read: selection processes) would help. Drools solver is overkill; drools rules can not handle this if you think optional constraints. The custom operator “== (open world style)” we talked about helps, though.

University of Rostock, [http://www.uni-rostock.de](<http://www.uni-rostock.de/>)  
Chair of Naval Architecture,[ http://www.schiffbauforschung.de](<http://www.schiffbauforschung.de/>)  
Contact: michael.zimmermann at uni-rostock.de

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F09%2Fimproving-the-naval-engineering-process-using-drools-michael-zimmermann.html&linkname=Improving%20the%20Naval%20engineering%20process%20using%20Drools%20%28%20Michael%20Zimmermann%20%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F09%2Fimproving-the-naval-engineering-process-using-drools-michael-zimmermann.html&linkname=Improving%20the%20Naval%20engineering%20process%20using%20Drools%20%28%20Michael%20Zimmermann%20%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F09%2Fimproving-the-naval-engineering-process-using-drools-michael-zimmermann.html&linkname=Improving%20the%20Naval%20engineering%20process%20using%20Drools%20%28%20Michael%20Zimmermann%20%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F09%2Fimproving-the-naval-engineering-process-using-drools-michael-zimmermann.html&linkname=Improving%20the%20Naval%20engineering%20process%20using%20Drools%20%28%20Michael%20Zimmermann%20%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F09%2Fimproving-the-naval-engineering-process-using-drools-michael-zimmermann.html&linkname=Improving%20the%20Naval%20engineering%20process%20using%20Drools%20%28%20Michael%20Zimmermann%20%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F09%2Fimproving-the-naval-engineering-process-using-drools-michael-zimmermann.html&linkname=Improving%20the%20Naval%20engineering%20process%20using%20Drools%20%28%20Michael%20Zimmermann%20%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F09%2Fimproving-the-naval-engineering-process-using-drools-michael-zimmermann.html&linkname=Improving%20the%20Naval%20engineering%20process%20using%20Drools%20%28%20Michael%20Zimmermann%20%29> "Email")