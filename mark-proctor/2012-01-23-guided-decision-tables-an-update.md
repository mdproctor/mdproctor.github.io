---
layout: post
title: "Guided Decision Tables - An update"
date: 2012-01-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/01/guided-decision-tables-an-update.html
---

The guided decision table editor in Guvnor has come a long way since it was first added to Guvnor in 2008 so I thought it worth while consolidating the efforts we’ve made into a short summary so those unfamiliar with recent developments can re-consider what a powerful tool Guvnor now posses.

The editor in 2008   
[![](/legacy/assets/images/2012/01/9c530e19deb2-WebDT.png)](</assets/images/2012/01/144851c3f7bf-WebDT.png>)  
Complete re-write

When Guvnor moved from GWT-EXT to vanilla GWT we took the opportunity to re-write the entire editor. GWT’s table widgets did not offer the flexibility we wanted to provide users in their authoring environment: We wanted users to be able to quickly and easily build tables enabling them to concentrate on their rules rather than data-entry. Thus the new editor was born offering keyboard or mouse navigation, in-cell editing together with merging and grouping of cells.

The editor as it is today   
[![](/legacy/assets/images/2012/01/a17c2dd5a980-dtable-extended-entry.png)](</assets/images/2012/01/39b79442f823-dtable-extended-entry.png>)

Guided construction

To make the initial definition process as pain-free as possible we added a Wizard to walk users through creation. The Wizard also offers users the ability to generate an expanded form table.

The wizard   
[![](/legacy/assets/images/2012/01/5734b9b931a4-dtable-wizard-defining.png)](</assets/images/2012/01/c03693173062-dtable-wizard-defining.png>)

  
Merging

Merging of cells combines cells with identical values into one; thus providing a quick way to change the value of multiple cells in a single operation (of course, you could equally select multiple-cells with either a mouse-drag operation or keyboard but we felt merging minimized the process). Merging was also the precursor to grouping of cells, a powerful facility to collapse sections of the table whilst authoring.

Merged cells   
[![](/legacy/assets/images/2012/01/e831058906fe-dtable-merged.png)](</assets/images/2012/01/ba7ca03f86eb-dtable-merged.png>)

Grouping

Merged cells can be collapsed into one. All editing operations continue to work as normal: copying-pasting rows and editing cell values etc. The only difference being that you can effectively hide sections of the table. Copying and pasting a grouped row also offers a convenient way to duplicate sections of the table (before editing as appropriate).

Grouped cells   
[![](/legacy/assets/images/2012/01/a3b102eab0c7-dtable-grouped.png)](</assets/images/2012/01/2e11953fb761-dtable-grouped.png>)

Extended and Limited Entry

What type of decision table editor would we have without offering both Extended Entry and Limited Entry? Extended entry allows constraint and action values to be defined in the table body; whereas Limited entry moves the entire definition to the column itself with the body simply allowing the user to define which constraints and/or actions apply.

Limited Entry   
[![](/legacy/assets/images/2012/01/a81100777762-dtable-limited-entry.png)](</assets/images/2012/01/63951b2a2527-dtable-limited-entry.png>)  

Analysis

Support has been added to detect mistakes in your decision table. Currently we detect 2 types of problem and want to add many more.

  * Impossible matches
  * Conflict detection

Conflict detection  
[![](/legacy/assets/images/2012/01/a69ff5313bc8-conflictingMatch2.png)](</assets/images/2012/01/95e0698f4094-conflictingMatch2.png>)

Integration of jBPM work items

Rules are frequently used from within jBPM to drive dynamic processes. What better then than providing a means for jBPM Work Items to be used in your rules’ consequences? Work Item input parameters can be bound to Facts or their properties and likewise output parameters used to populate Facts.

Use of BRL fragments

Column definitions have historically only been able to offer a thin veil of abstraction. With the introduction of BRL fragments, columns can be defined using the full range of Guvnor’s guided rule authoring capabilities (including DSL) which, coupled with Limited Entry, allows a higher level of abstraction to be realized.

A BRL fragment column   
[![](/legacy/assets/images/2012/01/0de4816c23e1-dtable-brl-condition.png)](</assets/images/2012/01/9650b75a2a0f-dtable-brl-condition.png>)  

Roadmap

Whilst, you might agree, significant progress has been made made there is still a long way to go. There still is a tremendous amount of work we want to complete before feeling our decision table offering is as complete as we’d like.

  * Round-trip between Excel and Guvnor
  * Improved integration of V&V to provide visual feedback
  * Further V&V to check conflict, completeness, ambiguity, subsumption etc
  * Expansion and contraction
  * Enforcement of multi-hit and single-hit variants
  * Typed input of default values and lists of permitted values for Conditions
  * Pluggable editors for domain types
  * Column and row drag and drop
  * Horizontal decision table
  * Integration of WorkingSets