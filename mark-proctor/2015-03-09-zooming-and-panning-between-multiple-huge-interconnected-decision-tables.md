---
layout: post
title: "Zooming and Panning between Multiple Huge Interconnected Decision Tables"
date: 2015-03-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/03/zooming-and-panning-between-multiple-huge-interconnected-decision-tables.html
---

Michael has started the work on revamping our web based decision tables. We’ve been experimenting with HMTL5 canvas with great results, using the excellent [Lienzo](<https://github.com/ahome-it/lienzo-core>) tool. First we needed to ensure we could scale to really large decision tables, with thousands of rows. Secondly we wanted to be able to pan and zoom between related or interconnected decision tables. We’ll be working towards [Decision Model and Notation](<http://www.programering.com/a/MzN5QTNwATA.html>) support, that allows networked diagrams of Decision Tables.

You can watch the video here, don’t forget to select HD:  
<https://www.youtube.com/watch?v=WgZTdfLis0Q>

Notice in the video that while you can manually pan and zoom it also has links between tables. When you select the link it animates the pan and zoom to the linked location. 25s to 47s in is showing that we can have really large number of rows and keep excellent performance, while 55s is showing the pan speed with these large tables. Initially the example starts with 50% of cells populated, at 1m in we change that to 100% populated and demonstrate that we still have excellent performance.

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2015/03/79a63228cf45-nt44Fdu.png>)