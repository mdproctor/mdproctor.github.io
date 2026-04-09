---
layout: post
title: "A Comparative Study of Correlation Engines for Security Event Management"
date: 2015-05-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/05/a-comparative-study-of-correlation-engines-for-security-event-management.html
---

This just paper came up on my google alerts, you can download the full text from [ResearchGate](<http://www.researchgate.net/publication/275654821_A_Comparative_Study_of_Correlation_Engines_for_Security_Event_Management>).   
[“A Comparative Study of Correlation Engines for Security Event Management”](<http://www.researchgate.net/publication/275654821_A_Comparative_Study_of_Correlation_Engines_for_Security_Event_Management>)

It’s an academic paper, published in the peer reviewed journal.   
[“10th International Conference on Cyber Warfare and Security (ICCWS-2015)”](<http://academic-conferences.org/iccws/iccws2015/iccws15-home.htm>)

Th paper is evaluating the correlation performance for large rule sets and large data sets in different open source engines. I was very pleased to see how well Drools scaled at the top end. I’ll quote this from the conclusion and copy the results charts.   
_“As for the comparison study, it must be said that if the sole criteria was raw performance Drools would be considered the best correlation engine, for several reasons: its consistent behaviour and superior performance in the most demanding test cases.”_   
  
In Table 2 (first image) we scale form 200 rules to 500 rules, with 1mil events with almost no speed loss – 67s vs 70s. 

In Table 1 (second image) our throughput increases as the event sets become much larger. 

I suspect the reason why our performance is less for for the lower rule and event set numbers, is due to the engine initialisation time for all the functionality we provide and for all the indexing we do. As the matching time becomes large enough, due to larger rule and data sets, this startup time becomes much less significant on the over all figure. 

[![](/legacy/assets/images/2015/05/d9e06756b729-NR54Isi.png)](</assets/images/2015/05/17b2df0bb1ba-NR54Isi.png>)

[![](/legacy/assets/images/2015/05/df97d0dc2ab3-8f6SE8S.png)](</assets/images/2015/05/3c8f07198ae3-8f6SE8S.png>)