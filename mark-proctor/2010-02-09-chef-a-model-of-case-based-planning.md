---
layout: post
title: "CHEF: A Model of Case-based Planning"
date: 2010-02-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/02/chef-a-model-of-case-based-planning.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [CHEF: A Model of Case-based Planning](<https://blog.kie.org/2010/02/chef-a-model-of-case-based-planning.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 9, 2010  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

The original CHEF application for Case Based Reasoning (CBR) makes for an interesting read and is covered in the Expert Systems book (Peter Jackson) . I just found the original paper online, so I thought I’d share it. Maybe someone could start doing a CHEF implementation on top of Drools?  
<https://www.aaai.org/Papers/AAAI/1986/AAAI86-044.pdf>

“CHEF is a case-based planner that builds new plans out of its  
memory of old ones. CHEF’s domain is Szechwan cooking and its  
task is to build new recipes on the basis of a user’s requests. CHEF’s  
input is a set of goals for different tastes, textures, ingredients and  
types of dishes and its output is a single recipe that satisfies all of its  
goals. Its output is a single plan, in the form of a recipe, that satisfies  
all of the users goals.

Before searching for a plan to modify, CHEF examines the goals in  
its input and tries to anticipate any problems that might arise while  
planning for them. If a failure is predicted, CHEF adds a goal to avoid  
the failure to its list of goals to satisfy and this new goal is also used  
to search for a plan. Because plans are indexed in memory by the  
problems they avoid, this prediction can be used to find a plan that  
solves the predicted problem. Much of CHEF’s planning power lies  
in this ability to predict and thus avoid failures it has encountered  
before.”

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fchef-a-model-of-case-based-planning.html&linkname=CHEF%3A%20A%20Model%20of%20Case-based%20Planning> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fchef-a-model-of-case-based-planning.html&linkname=CHEF%3A%20A%20Model%20of%20Case-based%20Planning> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fchef-a-model-of-case-based-planning.html&linkname=CHEF%3A%20A%20Model%20of%20Case-based%20Planning> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fchef-a-model-of-case-based-planning.html&linkname=CHEF%3A%20A%20Model%20of%20Case-based%20Planning> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fchef-a-model-of-case-based-planning.html&linkname=CHEF%3A%20A%20Model%20of%20Case-based%20Planning> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fchef-a-model-of-case-based-planning.html&linkname=CHEF%3A%20A%20Model%20of%20Case-based%20Planning> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F02%2Fchef-a-model-of-case-based-planning.html&linkname=CHEF%3A%20A%20Model%20of%20Case-based%20Planning> "Email")