---
layout: post
title: "Lienzo for new jBPM Designer and Drools Decision Tables"
date: 2015-09-30
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/09/lienzo-for-new-jbpm-designer-and-drools-decision-tables.html
---

Michael Anstis and myself have been working on the [Lienzo](<http://www.lienzo-core.com/lienzo-ks/>) tool, a GWT based HTML Canvas library for Scene Graphs.

Michael has been working on lienzo-grid, as the basis for our next generation decision tables – so it can support multiple interconnected tables on a page.  
<http://blog.athico.com/2015/04/cell-merging-collapsing-and-sorting.html>  
<http://blog.athico.com/2015/03/zooming-and-panning-between-multiple.html>  
<https://www.youtube.com/channel/UCRjyzfzlWSPafTe4TDb5I4Q>

I’m working with Lienzo so that it can form the basis of our next generation designer. I wanted to make sure that we had a high quality core, in how users interact with shapes and connectors. I’ve just done a small demo, to show progress.

  1. Real time alignment and distribution of shapes
  2. Orthogonal line support with heuristics for minimising joins, and real time drawing. With easy add/remove of points, as well as avoiding ugly layouts:
     1. Corners should be nicely rounded, default canvas joins is not enough.
     2. Lines should not go back on themselves.
     3. When connected lines should go away from the shape.
     4. Corner connections can be in one of two directions, select the one that gives the least corners.
  3. Magnets should be auto determined by analysing the path, currently supports any SVG path of lines and arcs. So things like lightning bolts, or human outline shapes can be used.

Here is a link to my latest video, The lightning bold is added at 1m35s.

<http://www.screencast.com/users/MarkPr/folders/Jing/media/e50d689e-4a8a-4584-9a24-9a339350b87f>

All of the generic work is making it’s way back into Lienzo and we hope this will evolved to be a part of community soon. Hopefully early versions before end of this year, in community.

A big thanks to Dean Jones (Lienzo lead) for all his support and help.

This mean we can have the same canvas library for both decision tables and designers. Keeping our loading sizes smaller and reducing the number of libraries my teams have to support and maintain. Dean is also working on charts, so we can hopefully unify that too.

Mark