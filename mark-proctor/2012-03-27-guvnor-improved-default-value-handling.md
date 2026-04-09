---
layout: post
title: "Guvnor - Improved default value handling"
date: 2012-03-27
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/03/guvnor-improved-default-value-handling.html
---

### Guvnor – Improved default value handling

Some things start simple.

Take the “Default Value Editor” for example. This simple editor provides the means to define a default value for columns’ cell values for the Guided Decision Table editor. When a new row is inserted the cell assumes it’s default value. Simple.

The Default Value Editor has always been a TextBox and it was time it was improved to be consistent with the new improved “typed” [editors](<http://blog.athico.com/2012/03/guvnor-recent-improvements.html>) used through-out Guvnor (with CR1 looming more extensive enhancements take a back seat).

The requirement was simple: make the editor suitable for the data-type of the column.

After the first day of re-factoring it became apparent things were not going to be quite as simple as I’d hoped. Things needing consideration:-

  * If a “Value List” is provided, the default value needs to be one of the values in the list
  * If the column represents a field with an enumeration the default value must be one of the enumeration’s members
  * If the column uses an operator that does not need a value (e.g. “is null”) a default value cannot be provided
  * If the column field is a “dependent enumeration” the default value must be one of the permitted values based upon parent enumeration default values, if any.
  * Default values are not required for Limited Entry tables.
  * Default values always remain optional.
  * Default values can be defined in either the Guided Decision Table editor or the Guided Decision Table Wizard.

The changes are now complete and committed to [github](<https://github.com/droolsjbpm/guvnor>) in time for the CR1 branch. If you use decision tables, if you use default values be sure to check it out before Final.

Setting the default value of a Date column

[![](/legacy/assets/images/2012/03/6d871155f9b5-dtable-default-1.png)](</assets/images/2012/03/f803105d7ac6-dtable-default-1.png>)  
  
Setting the default value of a cell with a Value List  
  
[![](/legacy/assets/images/2012/03/2c35fdad00e1-dtable-default-2.png)](</assets/images/2012/03/7855d1e346ff-dtable-default-2.png>)

What started as a quick enhancement before CR1 turned out to be more extensive than expected.