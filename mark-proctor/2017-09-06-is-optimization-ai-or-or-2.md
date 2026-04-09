---
layout: post
title: "Is Optimization AI or OR?"
date: 2017-09-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2017/09/is-optimization-ai-or-or-2.html
---

With the renewed interest in AI the same conversations are starting to come up again, about what is or isn’t AI. My recent discussion was on whether optimisation products, such as [OptaPlanner](<https://www.optaplanner.org/>), are considered AI as some considered it more Operations Research (OR). For some background, OptaPlanner started out as a [Tabu Solver](<https://en.wikipedia.org/wiki/Tabu_search>) implementation, but has since added other techniques like Simulated Annealing.

Although I’d like to add that no single technique **is** AI, they are all tools and techniques that are quite typically used together in a blended, hybrid or integrated AI solution. So it’s the right tool or tools for the job.

The answer is that Optimisation is both an AI and an OR problem. It is a technique used and researched by both groups, the two different disciplines tend to take different approaches to the problem, having differing use cases and have historically used different techniques, with a lot of cross pollination from both sides.

I’ll start with a consumer oriented answer to the question. StaffJoy has a nice blog article on the overlap of OR and AI, and I’ll quote from that below:  
<https://blog.staffjoy.com/how-operations-research-and-artificial-intelligence-overlap-b128a3efee2e>  
“Startups are using OR techniques in products like OnFleet, Instacart, and Lyft Line. However, when similar techniques are being exposed externally as services, they are often described as AI — e.g. x.ai, Atomwise, and Sentient. Very few companies describe algorithms that they sell as optimization (with the exception of SigOpt) because the end goal of customers is automating decisions. With StaffJoy, we have found that customers better understand our product when we describe it as an “artificial intelligence” tool rather than an “optimization” or “operations” tool. We think that this is because customers care more about what a product achieves, rather than the means it uses to achieve it.”

In short consumers do not see the difference between OR and AI, when applied to real world problems and it is commonly marketed as AI.

I’ll go a little more technical now, to further demonstrate it’s more than just marketing – as that side is only touched on in the above blog post.

While the two groups (OR and AI) may have once been distinct, it’s been well established that the OR and AI groups overlap in this space and have collaborated for years. Glover (1986) states them as “the recent remarriage of two disciplines that were once united, having issued from a common origin, but which became separated” – see final paper link at end.

A cursory google with terms “operations research” and “artificial intelligence” will more than prove this. Some techniques, like Linear Programming, are strongly on the OR side, others like Local Search (which OptaPlanner falls under) are shared. Optimisation, and local search (along with other techniques), is a core fundamental taught in every AI course without fail, and will be covered in every general AI book, used in schools – such as “AI: A Modern Approach”- see chapter 4, page 120  
<http://aima.cs.berkeley.edu/contents.html>

The book “Artificial Intelligence Methods and Applications” also makes it clear the two (OR and AI) are linked:  
“Local search, or local optimisation, is one of the primitive forms of continuous optimisation in a discrete problem space. It was one of the early techniques proposed during the mid sixties to cope with the overwhelming computational intractability of NP-hard combinatorial optimisation problems. Unlike continuous optimisation techniques, local search has often been used in AI research and has established a strong link between AI and the operational research area.”  
[https://books.google.co.uk/books?id=0a_j0R0qh1EC&pg=PA67&lpg=PA67&dq=%22local+search%22+operations+research+artificial+intelligence&source=bl&ots=h2jGquBm4d&sig=2V7CKRIs3ZL-NKzqL3Dnkx33_NI&hl=en&sa=X&redir_esc=y#v=onepage&q=%22local%20search%22%20operations%20research%20artificial%20intelligence&f=false](<https://books.google.co.uk/books?id=0a_j0R0qh1EC&pg=PA67&lpg=PA67&dq=%22local+search%22+operations+research+artificial+intelligence&source=bl&ots=h2jGquBm4d&sig=2V7CKRIs3ZL-NKzqL3Dnkx33_NI&hl=en&sa=X&redir_esc=y#v=onepage&q=%22local%20search%22%20operations%20research%20artificial%20intelligence&f=false>)

Lastly I’ll quote directly from the original Tabu Solver paper “These developments may be usefully viewed as a synthesis of the perspectives of operations research and artificial intelligence… … The foundation for this prediction derives, perhaps surprisingly, from the recent remarriage of two disciplines that were once united, having issued from a common origin, but which became separated and maintained only loose ties for several decades: operations research and artificial intelligence. This renewed reunion is highlighting limitations in the frameworks of each (as commonly applied, in contrast to advocated), and promises fertile elaborations to the strategies each has believed fruitful or approaching combinatorial complexity.” Glover (1986). Note the paper is from “The Center of Applied Artificial Intelligence”.  
<http://leeds-faculty.colorado.edu/glover/TS%20-%20Future%20Paths%20for%20Integer%20Programming.pdf>

So I hope that clears that up – AI is a very broad church :)