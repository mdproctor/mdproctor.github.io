---
layout: post
title: "Conditional Branches with sub blocks and 'switch' statements"
date: 2012-09-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/09/conditional-branches-with-sub-blocks-and-switch-statements.html
---

Last week Mario introduced the new left hand side conditional element [‘if/else if/else’](<http://blog.athico.com/2012/09/conditional-named-consequences-in.html>). The next plans for this is to allow nested blocks in each conditional branch and to then to provide a ‘switch’ statement for sugar. You can see more examples of both, plus their logical rule equivalents here, <https://community.jboss.org/wiki/BranchCEs>

Some time ago I started to write a pacman example, it’s still unfinished, but I can share with you how these new constructs will improve maintainability with reduced rules. The original drl can be found here:  
<https://raw.github.com/droolsjbpm/drools/master/drools-examples/src/main/resources/org/drools/examples/pacman/pacman.drl>

The pacman.drl has the following three rules:

```drl
/** * By increasing the tick we slow down the time to the next move. * I use the CE 'or' here rathre than an infix "in" to maximise node sharing * with both the EatFood and EatPowerPill rules. */
rule SlowWhenEating
dialect "mvel"
no-loop
salience 10when    $char : Character( name == "Pacman" )    $l : Location( character == $char )    $target : Cell( row == $l.row, col == $l.col)    (or $contents : CellContents( cell == $target, cellType == CellType.FOOD )        $contents : CellContents( cell == $target, cellType == CellType.POWER_PILL ) )        $update : ScheduledLocationUpdate( character == $char )
then
modify ( $update ) { tock += 2 };
end
/** * When we move onto a FOOD cell, increase the score by 1 */
rule EatFood
dialect "mvel"
when
$char : Character( name == "Pacman" )    $l : Location( character == $char )    $target : Cell( row == $l.row, col == $l.col)    $contents : CellContents( cell == $target, cellType == CellType.FOOD )    $s : Score()
then
modify( $contents ) { cellType = CellType.EMPTY };    modify( $s ) { score += 1 };
end
/** * When we move onto a POWER_PILL cell, increase the score by 5 */
rule EatPowerPill
dialect "mvel"
when
$char : Character( name == "Pacman" )    $l : Location( character == $char )    $target : Cell( row == $l.row, col == $l.col)    $contents : CellContents( cell == $target, cellType == CellType.POWER_PILL )    $s : Score()
then
modify( $contents ) { cellType = CellType.EMPTY };    modify( $s ) { score += 5 };
end
```

Once we support ‘switch’ with nested blocks we should be able to do the following. Note I also removed the ‘no-loop’, as it’s no longer needed with property reactive.

```drl
rule eatFoodOrPill
when
$s : Score()      $char : Character( name == "Pacman" )    $l : Location( character == $char )    $target : Cell( row == $l.row, col == $l.col)    $contents : CellContents( cell == $target )    switch( cellType ) {        case CellType.FOOD : {              do[scorePlus1]                  $update : ScheduledLocationUpdate( character == $char )            do[slowWhenEating]        }        case CellType.POWER_PILL  : {            do[scorePlus5]                    $update : ScheduledLocationUpdate( character == $char )            do[slowWhenEating]                    }            }
then
[slowWhenEating]      modify ( $update ) { tock += 2 };
then
[scorePlus1]    modify( $contents ) { cellType = CellType.EMPTY };    modify( $s ) { score += 5 };
then
[scorePlus5]    modify( $contents ) { cellType = CellType.EMPTY };    modify( $s ) { score += 5 };
end
```