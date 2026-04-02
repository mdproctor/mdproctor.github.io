---
layout: post
title: "Dynamic Salience Expressions"
date: 2007-05-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/dynamic-salience-expressions.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Dynamic Salience Expressions](<https://blog.kie.org/2007/05/dynamic-salience-expressions.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 26, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

The other week in the mailing list someone was asking about whether it’s possible to have the salience’s value derived from the matched facts. Which got me thinking as I haven’t seen that in any other rule engines – I only know a few engines, so someone with more experience care to verify that?

Anyway a few weeks later and a bored friday night dynamic salience expressions are born :) The salience value can now be derived from an expression that has full access to the variables bindings, ofcourse integer values can still be specified. Before, during conflict resolution, the salience value was read directly from the rule on each comparison, now when the Activation is created the salience value is determined once and stored in the Activation for comparison during conflict resolution. So now you can write things like have rules with the highest priced items combined with the shoppers bonus rating fire first:
[code]
    rule "high value fires first"  
        salience (person.bonus * item.price)  
    when  
        person : Person()  
        item : Item()  
    then  
        ...  
    end
[/code]

MVEL is used for the salience expressions, as part of the pluggeable dialect system we have just built – I’ll blog on pluggeable dialects and parsers next week.

Update — Thanks to Johan Lindberg, who has pointed out that Clips and Jess allow the salience to be set via function calls in Jess/Clips.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fdynamic-salience-expressions.html&linkname=Dynamic%20Salience%20Expressions> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fdynamic-salience-expressions.html&linkname=Dynamic%20Salience%20Expressions> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fdynamic-salience-expressions.html&linkname=Dynamic%20Salience%20Expressions> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fdynamic-salience-expressions.html&linkname=Dynamic%20Salience%20Expressions> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fdynamic-salience-expressions.html&linkname=Dynamic%20Salience%20Expressions> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fdynamic-salience-expressions.html&linkname=Dynamic%20Salience%20Expressions> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fdynamic-salience-expressions.html&linkname=Dynamic%20Salience%20Expressions> "Email")