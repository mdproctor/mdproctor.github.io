---
layout: post
title: "Symmetrical and Asymmetrical Rete"
date: 2008-10-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/10/symmetrical-and-asymmetrical-rete.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Symmetrical and Asymmetrical Rete](<https://blog.kie.org/2008/10/symmetrical-and-asymmetrical-rete.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- October 26, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

In my endeavours to understand Clips I realised that it’s Rete implementation was different to the more classical approach, as used by Drools 4. I haven’t read anything in the past that attempted to give this difference a name, so I adopted the terminology of symmetrical Rete and asymmetrical Rete. It was really nice to see this decision validated by Gary Riley, the author of Clips, who used the terminology in his presentation on Rete enhancements in Clips at the [Rules Fest](<http://www.rulesfest.org/>) in Texas.

Here is a quick explanation of the difference, without getting into the details on merit, in Drools 4 we use the classical approach of the retract being the same work as assert, except on the assert data is added to the memory on retract data is removed. By this I mean that the fact propagates through the network, for each join node the constraints are evaluated to determine the joins, the join is made and the fact plus the new join fact are propagated, each propagation into a new join node is added to the join node’s memory. The retract is exactly the same, the constraints are re-evaluated to determine the previous joins so that the join and propagation can be remade, this time the facthandle and it’s joined data are removed from the join node memory. With the work done for the attract and assert being the same I dubbed this symmetrical Rete.

In Drools 5 we adopted the Clips algorithm. Here the assert uses a lot of linked reference so that the propagation creates a chain of tokens. The retract can now iterate this chain of references removing data from the node memories, the joins do not need to be recalculated to determine which facts we joined against, we already know this as we have the references. As the work done for the retract is now different to the assert I dubbed this assymetrical Rete.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Fsymmetrical-and-asymmetrical-rete.html&linkname=Symmetrical%20and%20Asymmetrical%20Rete> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Fsymmetrical-and-asymmetrical-rete.html&linkname=Symmetrical%20and%20Asymmetrical%20Rete> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Fsymmetrical-and-asymmetrical-rete.html&linkname=Symmetrical%20and%20Asymmetrical%20Rete> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Fsymmetrical-and-asymmetrical-rete.html&linkname=Symmetrical%20and%20Asymmetrical%20Rete> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Fsymmetrical-and-asymmetrical-rete.html&linkname=Symmetrical%20and%20Asymmetrical%20Rete> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Fsymmetrical-and-asymmetrical-rete.html&linkname=Symmetrical%20and%20Asymmetrical%20Rete> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F10%2Fsymmetrical-and-asymmetrical-rete.html&linkname=Symmetrical%20and%20Asymmetrical%20Rete> "Email")