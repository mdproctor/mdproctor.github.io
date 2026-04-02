---
layout: post
title: "Declarative Relational Programming"
date: 2007-06-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/declarative-relational-programming.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Declarative Relational Programming](<https://blog.kie.org/2007/06/declarative-relational-programming.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 19, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

This blog post is from a comment I made over at the InfoQ article [Debate: ODBMS sometimes a better alternative to O/R Mapping?](<http://www.infoq.com/news/2007/06/orm-obms-debate#view_7741>).

Object Oriented deep graph models, pojos specifically, cannot be easily reasoned over declaratively – which can create a reliance on imperative programming. With the work that W3C has done to standardise [Description Logic](<http://en.wikipedia.org/wiki/Description_logic>) with OWL-DL combined with declarative reasoning sytems like Drools (we’ll be adding Description Logic based modelling after 4.0) you have a much more powerful metaphor for application development (although probably not framework/subs system development) – also forget OWL Full, its an academic exercise, and RDF triples are unfortunate, but luckily can just be considered a transport mechanism. Declarative relational programming obviously has a much closer 1 to 1 mapping with the database itself.

For a simple example look at the Conways Game of Life example we provide (will be updated to ruleflow soon, instead of agenda groups, which will make it more declarative). In this example we have a large NxN grid of Cell objects, the previous approach was for each Cell to have a HashSet of its surrounding Cells. The only way to calculate the number of surrounding Dead/Live cells was to imperatively iterate that HashSet for each Cell. This would create repeatedly redundant work, as we don’t know what has and what hasn’t change, we could track that, but again it’s more imperative code and tracking we have to do. The updated Conways example uses a relational approach, no nested objects,(Although no DL yet, that is post 4.0) instead we use a Neighbour class to bi-directionally relate each surrounding cell; this means we simply declare what we want it to do to track Dead/Live cells and the system, with its understanding of the relations and what has and what hasn’t changed, does the rest for us.  
<http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/drools-examples/src/main/rules/org/drools/examples/conway/conway.drl>  
rule “Calculate Live”  
agenda-group “calculate”  
lock-on-active   
when  
theCell: Cell(cellState == CellState.LIVE)  
Neighbor(cell == theCell, $neighbor : neighbor)   
then  
$neighbor.setLiveNeighbors( $neighbor.getLiveNeighbors() + 1 );  
$neighbor.setPhase( Phase.EVALUATE );   
modify( $neighbor );  
end

rule “Calculate Dead”  
agenda-group “calculate”  
lock-on-active   
when  
theCell: Cell(cellState == CellState.DEAD)  
Neighbor(cell == theCell, $neighbor : neighbor )  
then  
$neighbor.setLiveNeighbors( $neighbor.getLiveNeighbors() – 1 );  
$neighbor.setPhase( Phase.EVALUATE );  
modify( $neighbor );   
end

I also invite you to look at the “register neighbor” set of rules, so you can see how these Neighbour relations are setup declaratively, exploiting the cross products of the column and row fields in the Cell.

While this is just a simple example using propositional logic you can exploit these relations much further, especially when working with sets of data and first order logic using things like ‘collect’, ‘accumulate’ and ‘forall’. For more info see [What’s new in JBoss Rules 4.0](<http://wiki.jboss.org/wiki/attach?page=JBossRules%2Fwhats_new_in_jbossrules_4.0.pdf>) which is released mid next month.

Mark  
[http://markproctor.com](<http://markproctor.com/>)  
[http://markproctor.blogspot.com](<http://markproctor.blogspot.com/>)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fdeclarative-relational-programming.html&linkname=Declarative%20Relational%20Programming> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fdeclarative-relational-programming.html&linkname=Declarative%20Relational%20Programming> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fdeclarative-relational-programming.html&linkname=Declarative%20Relational%20Programming> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fdeclarative-relational-programming.html&linkname=Declarative%20Relational%20Programming> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fdeclarative-relational-programming.html&linkname=Declarative%20Relational%20Programming> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fdeclarative-relational-programming.html&linkname=Declarative%20Relational%20Programming> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fdeclarative-relational-programming.html&linkname=Declarative%20Relational%20Programming> "Email")