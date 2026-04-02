---
layout: post
title: "Guvnor - Improved default value handling"
date: 2012-03-27
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/03/guvnor-improved-default-value-handling.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Guvnor – Improved default value handling](<https://blog.kie.org/2012/03/guvnor-improved-default-value-handling.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 27, 2012  
[Tools](<https://blog.kie.org/category/tools>) [Article](<https://blog.kie.org/content_type/article>)

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

[![](/legacy/assets/images/2012/03/6d871155f9b5-dtable-default-1.png)](<http://2.bp.blogspot.com/-ke1R1ch9bJA/T3IaFSHoIqI/AAAAAAAAAks/7WSfnusWC9Q/s1600/dtable-default-1.png>)  
  
Setting the default value of a cell with a Value List  
  
[![](/legacy/assets/images/2012/03/2c35fdad00e1-dtable-default-2.png)](<http://2.bp.blogspot.com/-ZG-7ds5-080/T3IZEzs6P6I/AAAAAAAAAkg/8GPWUbR2ZwU/s1600/dtable-default-2.png>)

What started as a quick enhancement before CR1 turned out to be more extensive than expected.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fguvnor-improved-default-value-handling.html&linkname=Guvnor%20%E2%80%93%20Improved%20default%20value%20handling> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fguvnor-improved-default-value-handling.html&linkname=Guvnor%20%E2%80%93%20Improved%20default%20value%20handling> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fguvnor-improved-default-value-handling.html&linkname=Guvnor%20%E2%80%93%20Improved%20default%20value%20handling> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fguvnor-improved-default-value-handling.html&linkname=Guvnor%20%E2%80%93%20Improved%20default%20value%20handling> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fguvnor-improved-default-value-handling.html&linkname=Guvnor%20%E2%80%93%20Improved%20default%20value%20handling> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fguvnor-improved-default-value-handling.html&linkname=Guvnor%20%E2%80%93%20Improved%20default%20value%20handling> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F03%2Fguvnor-improved-default-value-handling.html&linkname=Guvnor%20%E2%80%93%20Improved%20default%20value%20handling> "Email")
  *[]: 2010-05-25T16:11:00+02:00