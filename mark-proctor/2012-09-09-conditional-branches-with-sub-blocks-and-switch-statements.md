---
layout: post
title: "Conditional Branches with sub blocks and 'switch' statements"
date: 2012-09-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/09/conditional-branches-with-sub-blocks-and-switch-statements.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Conditional Branches with sub blocks and ‘switch’ statements](<https://blog.kie.org/2012/09/conditional-branches-with-sub-blocks-and-switch-statements.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 9, 2012  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Last week Mario introduced the new left hand side conditional element [‘if/else if/else’](<http://blog.athico.com/2012/09/conditional-named-consequences-in.html>). The next plans for this is to allow nested blocks in each conditional branch and to then to provide a ‘switch’ statement for sugar. You can see more examples of both, plus their logical rule equivalents here, <https://community.jboss.org/wiki/BranchCEs>

Some time ago I started to write a pacman example, it’s still unfinished, but I can share with you how these new constructs will improve maintainability with reduced rules. The original drl can be found here:  
<https://raw.github.com/droolsjbpm/drools/master/drools-examples/src/main/resources/org/drools/examples/pacman/pacman.drl>

The pacman.drl has the following three rules:
[code]
    /**  
     * By increasing the tick we slow down the time to the next move.  
     * I use the CE 'or' here rathre than an infix "in" to maximise node sharing  
     * with both the EatFood and EatPowerPill rules.  
     */  
    rule SlowWhenEating dialect "mvel" no-loop salience 10when  
        $char : Character( name == "Pacman" )  
        $l : Location( character == $char )  
        $target : Cell( row == $l.row, col == $l.col)  
        (or $contents : CellContents( cell == $target, cellType == CellType.FOOD )  
            $contents : CellContents( cell == $target, cellType == CellType.POWER_PILL ) )      
        $update : ScheduledLocationUpdate( character == $char )  
    then    
        modify ( $update ) { tock += 2 };  
    end  
      
      
    /**  
     * When we move onto a FOOD cell, increase the score by 1  
     */  
    rule EatFood dialect "mvel" when  
        $char : Character( name == "Pacman" )  
        $l : Location( character == $char )  
        $target : Cell( row == $l.row, col == $l.col)  
        $contents : CellContents( cell == $target, cellType == CellType.FOOD )  
        $s : Score()     
    then  
        modify( $contents ) { cellType = CellType.EMPTY };  
        modify( $s ) { score += 1 };      
    end  
      
    /**  
     * When we move onto a POWER_PILL cell, increase the score by 5  
     */  
    rule EatPowerPill dialect "mvel" when  
        $char : Character( name == "Pacman" )  
        $l : Location( character == $char )  
        $target : Cell( row == $l.row, col == $l.col)  
        $contents : CellContents( cell == $target, cellType == CellType.POWER_PILL )  
        $s : Score()     
    then  
        modify( $contents ) { cellType = CellType.EMPTY };  
        modify( $s ) { score += 5 };      
    end  
    
[/code]

Once we support ‘switch’ with nested blocks we should be able to do the following. Note I also removed the ‘no-loop’, as it’s no longer needed with property reactive.
[code]
    rule eatFoodOrPill when  
        $s : Score()    
        $char : Character( name == "Pacman" )  
        $l : Location( character == $char )  
        $target : Cell( row == $l.row, col == $l.col)  
        $contents : CellContents( cell == $target )  
        switch( cellType ) {  
            case CellType.FOOD : {    
                do[scorePlus1]        
                $update : ScheduledLocationUpdate( character == $char )  
                do[slowWhenEating]  
            }  
            case CellType.POWER_PILL  : {  
                do[scorePlus5]          
                $update : ScheduledLocationUpdate( character == $char )  
                do[slowWhenEating]              
            }          
        }  
    then[slowWhenEating]    
        modify ( $update ) { tock += 2 };  
    then[scorePlus1]  
        modify( $contents ) { cellType = CellType.EMPTY };  
        modify( $s ) { score += 5 };      
    then[scorePlus5]  
        modify( $contents ) { cellType = CellType.EMPTY };  
        modify( $s ) { score += 5 };       
    end  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fconditional-branches-with-sub-blocks-and-switch-statements.html&linkname=Conditional%20Branches%20with%20sub%20blocks%20and%20%E2%80%98switch%E2%80%99%20statements> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fconditional-branches-with-sub-blocks-and-switch-statements.html&linkname=Conditional%20Branches%20with%20sub%20blocks%20and%20%E2%80%98switch%E2%80%99%20statements> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fconditional-branches-with-sub-blocks-and-switch-statements.html&linkname=Conditional%20Branches%20with%20sub%20blocks%20and%20%E2%80%98switch%E2%80%99%20statements> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fconditional-branches-with-sub-blocks-and-switch-statements.html&linkname=Conditional%20Branches%20with%20sub%20blocks%20and%20%E2%80%98switch%E2%80%99%20statements> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fconditional-branches-with-sub-blocks-and-switch-statements.html&linkname=Conditional%20Branches%20with%20sub%20blocks%20and%20%E2%80%98switch%E2%80%99%20statements> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fconditional-branches-with-sub-blocks-and-switch-statements.html&linkname=Conditional%20Branches%20with%20sub%20blocks%20and%20%E2%80%98switch%E2%80%99%20statements> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F09%2Fconditional-branches-with-sub-blocks-and-switch-statements.html&linkname=Conditional%20Branches%20with%20sub%20blocks%20and%20%E2%80%98switch%E2%80%99%20statements> "Email")
  *[]: 2010-05-25T16:11:00+02:00