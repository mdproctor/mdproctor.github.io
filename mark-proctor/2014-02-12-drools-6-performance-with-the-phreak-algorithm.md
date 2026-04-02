---
layout: post
title: "Drools 6 Performance with the PHREAK Algorithm"
date: 2014-02-12
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/02/drools-6-performance-with-the-phreak-algorithm.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools 6 Performance with the PHREAK Algorithm](<https://blog.kie.org/2014/02/drools-6-performance-with-the-phreak-algorithm.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 12, 2014  
[Optimization](<https://blog.kie.org/category/optimization>) [Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Drools 6 introduces a new lazy matching algorithm. The details of that algorithm have been covered in two previous blogs:  
[R.I.P. RETE time to get PHREAKY](<http://blog.athico.com/2013/11/rip-rete-time-to-get-phreaky.html>)  
[PHREAK Stack Based Evaluations and Backward Chaining](<http://blog.athico.com/2014/01/drools-phreak-stack-based-evaluations.html>)

The first article discussed performance and why the batch and lazy aspects of the algorithm, make it hard to compare.  
_“ One final point on performance. One single rule in general will not evaluate any faster with PHREAK than it does with RETE. For a given rule and same data set, which using a root context object to enable and disable matching, both attempt the same amount of matches and produce the same number of rule instances, and take roughly the same time. Except for the use case with subnetworks and accumulates._  
_  
PHREAK can however be considered more forgiving that RETE for poorly written rule bases and with a more graceful degradation of performance as the number of rules and complexity increases.  
  
RETE will also churn away producing partial machines for rules that do not have data in all the joins; where as PHREAK will avoid this.  
  
So it’s not that PHREAK is faster than RETE, it just won’t slow down as much as your system grows :)”_

 _  
_

_  
_

More recently the OptaPlanner team started benchmarking the same set of rules between ReteOO and Phreak:

[Which rule engine algorithm is faster: ReteOO or Phreak? ](<http://blog.athico.com/2014/01/which-rule-engine-algorithm-is-faster.html>)

They found that that three tests were 20% faster, and one test 4% slower. A user left a comment, for that article, relating at 17% performance difference.

[![](/legacy/assets/images/2014/02/a956b76894b7-phreakperf.png)](<http://4.bp.blogspot.com/-d_RrDnl-TUY/UvvLYGJjTJI/AAAAAAAABE4/-dHGBJSluj8/s1600/phreakperf.png>)

The OptaPlanner team have invested time into making sure the way they write the rules do not hit any Rete walls. They have removed many of the issues, such as multiple accumulates in a single rule.

One user was interested in what happens if you implement rules in a way known to cause problems with ReteOO, would it handle it more gracefully. They created 4 rules, each with two accumulates. The DRL file can be found [here](<https://github.com/winklerm/phreak-examples/blob/master/src/main/resources/org/kie/examples/phreak/laziness/laziness.drl>), and a copy of one of the rules is shown below:
[code]
    rule gold_account
    when
      account: Account()
      Number(this >= 50000) from accumulate(t: Transaction(source == account); sum(t.amount))
      Number(this >= 50000) from accumulate(t: Transaction(target == account); sum(t.amount))
    then
      //System.out.println("Gold account: " + account);
    end
    
[/code]

The results were promising, a 400% (5x) performance gain for Phreak :) This is mostly enabled by the way that Phreak evaluates rules in batches, avoiding a lot of wasted work. It certainly shows we’ve achieved one of the aims quoted from the earlier paragraph:  
_“PHREAK can however be considered more forgiving that RETE for poorly written rule bases and with a more graceful degradation of performance as the number of rules and complexity increases.”_

If you want to try this for yourself, you can checkout the project here:  
<https://github.com/winklerm/phreak-examples>

The algorithm so far has been designed for correctness, especially with regards to thread safety and future multi-core exploitation. So this is just the start, we still have plenty more optimisations and improvements to do.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F02%2Fdrools-6-performance-with-the-phreak-algorithm.html&linkname=Drools%206%20Performance%20with%20the%20PHREAK%20Algorithm> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F02%2Fdrools-6-performance-with-the-phreak-algorithm.html&linkname=Drools%206%20Performance%20with%20the%20PHREAK%20Algorithm> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F02%2Fdrools-6-performance-with-the-phreak-algorithm.html&linkname=Drools%206%20Performance%20with%20the%20PHREAK%20Algorithm> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F02%2Fdrools-6-performance-with-the-phreak-algorithm.html&linkname=Drools%206%20Performance%20with%20the%20PHREAK%20Algorithm> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F02%2Fdrools-6-performance-with-the-phreak-algorithm.html&linkname=Drools%206%20Performance%20with%20the%20PHREAK%20Algorithm> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F02%2Fdrools-6-performance-with-the-phreak-algorithm.html&linkname=Drools%206%20Performance%20with%20the%20PHREAK%20Algorithm> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F02%2Fdrools-6-performance-with-the-phreak-algorithm.html&linkname=Drools%206%20Performance%20with%20the%20PHREAK%20Algorithm> "Email")
  *[]: 2010-05-25T16:11:00+02:00