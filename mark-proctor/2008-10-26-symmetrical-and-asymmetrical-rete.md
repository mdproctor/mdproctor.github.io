---
layout: post
title: "Symmetrical and Asymmetrical Rete"
date: 2008-10-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/10/symmetrical-and-asymmetrical-rete.html
---

In my endeavours to understand Clips I realised that it’s Rete implementation was different to the more classical approach, as used by Drools 4. I haven’t read anything in the past that attempted to give this difference a name, so I adopted the terminology of symmetrical Rete and asymmetrical Rete. It was really nice to see this decision validated by Gary Riley, the author of Clips, who used the terminology in his presentation on Rete enhancements in Clips at the [Rules Fest](<http://www.rulesfest.org/>) in Texas.

Here is a quick explanation of the difference, without getting into the details on merit, in Drools 4 we use the classical approach of the retract being the same work as assert, except on the assert data is added to the memory on retract data is removed. By this I mean that the fact propagates through the network, for each join node the constraints are evaluated to determine the joins, the join is made and the fact plus the new join fact are propagated, each propagation into a new join node is added to the join node’s memory. The retract is exactly the same, the constraints are re-evaluated to determine the previous joins so that the join and propagation can be remade, this time the facthandle and it’s joined data are removed from the join node memory. With the work done for the attract and assert being the same I dubbed this symmetrical Rete.

In Drools 5 we adopted the Clips algorithm. Here the assert uses a lot of linked reference so that the propagation creates a chain of tokens. The retract can now iterate this chain of references removing data from the node memories, the joins do not need to be recalculated to determine which facts we joined against, we already know this as we have the references. As the work done for the retract is now different to the assert I dubbed this assymetrical Rete.