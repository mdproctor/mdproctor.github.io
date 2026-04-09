---
layout: post
title: "Declarative Relational Programming"
date: 2007-06-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/declarative-relational-programming.html
---

This blog post is from a comment I made over at the InfoQ article [Debate: ODBMS sometimes a better alternative to O/R Mapping?](<http://www.infoq.com/news/2007/06/orm-obms-debate#view_7741>).

Object Oriented deep graph models, pojos specifically, cannot be easily reasoned over declaratively – which can create a reliance on imperative programming. With the work that W3C has done to standardise [Description Logic](<http://en.wikipedia.org/wiki/Description_logic>) with OWL-DL combined with declarative reasoning sytems like Drools (we’ll be adding Description Logic based modelling after 4.0) you have a much more powerful metaphor for application development (although probably not framework/subs system development) – also forget OWL Full, its an academic exercise, and RDF triples are unfortunate, but luckily can just be considered a transport mechanism. Declarative relational programming obviously has a much closer 1 to 1 mapping with the database itself.

<http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/drools-examples/src/main/rules/org/drools/examples/conway/conway.drl>

For a simple example look at the Conways Game of Life example we provide (will be updated to ruleflow soon, instead of agenda groups, which will make it more declarative). In this example we have a large NxN grid of Cell objects, the previous approach was for each Cell to have a HashSet of its surrounding Cells. The only way to calculate the number of surrounding Dead/Live cells was to imperatively iterate that HashSet for each Cell. This would create repeatedly redundant work, as we don’t know what has and what hasn’t change, we could track that, but again it’s more imperative code and tracking we have to do. The updated Conways example uses a relational approach, no nested objects,(Although no DL yet, that is post 4.0) instead we use a Neighbour class to bi-directionally relate each surrounding cell; this means we simply declare what we want it to do to track Dead/Live cells and the system, with its understanding of the relations and what has and what hasn’t changed, does the rest for us.

```drl
rule "Calculate Live"
    agenda-group "calculate"
    lock-on-active 
when
    theCell: Cell(cellState == CellState.LIVE)
    Neighbor(cell == theCell, $neighbor : neighbor) 
then
    $neighbor.setLiveNeighbors( $neighbor.getLiveNeighbors() + 1 );
    $neighbor.setPhase( Phase.EVALUATE ); 
    modify( $neighbor );
end

rule "Calculate Dead"
    agenda-group "calculate"
    lock-on-active 
when
    theCell: Cell(cellState == CellState.DEAD)
    Neighbor(cell == theCell, $neighbor : neighbor )
then
    $neighbor.setLiveNeighbors( $neighbor.getLiveNeighbors() – 1 );
    $neighbor.setPhase( Phase.EVALUATE );
    modify( $neighbor ); 
end
```

I also invite you to look at the “register neighbor” set of rules, so you can see how these Neighbour relations are setup declaratively, exploiting the cross products of the column and row fields in the Cell.

While this is just a simple example using propositional logic you can exploit these relations much further, especially when working with sets of data and first order logic using things like ‘collect’, ‘accumulate’ and ‘forall’. For more info see [What’s new in JBoss Rules 4.0](<http://wiki.jboss.org/wiki/attach?page=JBossRules%2Fwhats_new_in_jbossrules_4.0.pdf>) which is released mid next month.

Mark  
[http://markproctor.com](<http://markproctor.com/>)  
[http://markproctor.blogspot.com](<http://markproctor.blogspot.com/>)