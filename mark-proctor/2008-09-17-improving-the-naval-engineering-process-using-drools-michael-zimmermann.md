---
layout: post
title: "Improving the Naval engineering process using Drools ( Michael Zimmermann )"
date: 2008-09-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/09/improving-the-naval-engineering-process-using-drools-michael-zimmermann.html
---

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