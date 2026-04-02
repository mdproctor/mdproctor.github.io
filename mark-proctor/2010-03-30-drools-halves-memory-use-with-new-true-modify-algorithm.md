---
layout: post
title: "Drools halves memory use with new \"True Modify\" algorithm"
date: 2010-03-30
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2010/03/drools-halves-memory-use-with-new-true-modify-algorithm.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools halves memory use with new “True Modify” algorithm](<https://blog.kie.org/2010/03/drools-halves-memory-use-with-new-true-modify-algorithm.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 30, 2010  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Edson and I finally merged in our latest Rete algorithm improvements and fixed the last bugs; with a herculean effort by Edson to isolate the memory leak issue highlighted to us by Geoffrey De Smet using his Planner example. The initial results show the work was definitely worth while.

The original motivation for this change was from our high end users running large and intensive stateful engines. They found Drools, while favourable compared to our competition, in these large environments was still using large amount of memory and having garbage collection issues; where the GC could not keep up with the rate of allocation and usage and exhibiting very high peaks and troughs.

The latest change introduces something we dubbed “true modify”, although we need a better technical name for it, maybe “tree preserving updates”, so that it matches the previous Drools 5.0.x algorithm change “tree based removal” for retractions. I previously explained “true modify” in more detail [here](<http://blog.athico.com/2010/01/rete-and-true-modify.html>). The gist of it is that previously an update in the Rete algorithm would pass through the network twice with a retract and then an assert. This meant the network of partial matches that form the Rete tree would be blown away and rebuilt. In cases where only a small amount of the tree genuinely changed it was quite a waste, because it recreated what already existed. True modify performs a single pass through the network and attempts to preserve and re-use partial matches where they where true before and continue to be true now.

Less intensive applications won’t see much difference, for instance Manners and Waltz are unchanged, but applications with a large number of objects with repeated modifications should benefit. Using the Drools Planner example as our initial test case for the new algorithm changes we found a 35% speed gain, but more importantly we managed a 50% peak memory reduction with a resulting much smoother curve. We recorded the 5.0.x and trunk graphs and you can see the results for yourself below. I’m hoping our users running truly large, close to 8GB, systems might even receive greater gains; I’ll post any results fed back to us.

[![](/legacy/assets/images/2010/03/59223bc39c27-telemetry_2.png)](<http://2.bp.blogspot.com/_Jrhwx8X9P7g/S7FbC107QBI/AAAAAAAAAZs/kHst_pwFHaM/s1600/telemetry_2.png>)  
[5.0.x (click to enlarge))](<http://2.bp.blogspot.com/_Jrhwx8X9P7g/S7FbC107QBI/AAAAAAAAAZs/kHst_pwFHaM/s1600/telemetry_2.png>)

[![](/legacy/assets/images/2010/03/ea31da89f696-telemetry.png)](<http://2.bp.blogspot.com/_Jrhwx8X9P7g/S7FbDM1WA3I/AAAAAAAAAZ0/qKxu40ooSS8/s1600/telemetry.png>)  
[trunk (click to enlarge)](<http://2.bp.blogspot.com/_Jrhwx8X9P7g/S7FbDM1WA3I/AAAAAAAAAZ0/qKxu40ooSS8/s1600/telemetry.png>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F03%2Fdrools-halves-memory-use-with-new-true-modify-algorithm.html&linkname=Drools%20halves%20memory%20use%20with%20new%20%E2%80%9CTrue%20Modify%E2%80%9D%20algorithm> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F03%2Fdrools-halves-memory-use-with-new-true-modify-algorithm.html&linkname=Drools%20halves%20memory%20use%20with%20new%20%E2%80%9CTrue%20Modify%E2%80%9D%20algorithm> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F03%2Fdrools-halves-memory-use-with-new-true-modify-algorithm.html&linkname=Drools%20halves%20memory%20use%20with%20new%20%E2%80%9CTrue%20Modify%E2%80%9D%20algorithm> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F03%2Fdrools-halves-memory-use-with-new-true-modify-algorithm.html&linkname=Drools%20halves%20memory%20use%20with%20new%20%E2%80%9CTrue%20Modify%E2%80%9D%20algorithm> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F03%2Fdrools-halves-memory-use-with-new-true-modify-algorithm.html&linkname=Drools%20halves%20memory%20use%20with%20new%20%E2%80%9CTrue%20Modify%E2%80%9D%20algorithm> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F03%2Fdrools-halves-memory-use-with-new-true-modify-algorithm.html&linkname=Drools%20halves%20memory%20use%20with%20new%20%E2%80%9CTrue%20Modify%E2%80%9D%20algorithm> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2010%2F03%2Fdrools-halves-memory-use-with-new-true-modify-algorithm.html&linkname=Drools%20halves%20memory%20use%20with%20new%20%E2%80%9CTrue%20Modify%E2%80%9D%20algorithm> "Email")