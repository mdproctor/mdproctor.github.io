---
layout: post
title: "Wumpus World Lives!!!"
date: 2012-02-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/02/wumpus-world-lives.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Wumpus World Lives!!!](<https://blog.kie.org/2012/02/wumpus-world-lives.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- February 7, 2012  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Wumpus world continues to improve and is now fully playable. The UI has a lot more polish now and nearly all of the code has been moved to DRL now, including the swing graphics rendering for the cave and the sensor panels. You’ll need to use master head to try it. Java is just used to build the kbase from the drl files and to create the swing panels, buttons and forms. WindowBuilder was used to graphical layout things.

The final thing I have to do is allow for client integration, so that people can write rules to automate the hero.

<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/init.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/commands.drl>  
[https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/collision.drl ](<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/collision.drl%20>)  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/score.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/view/ui.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/view/paintCave.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/view/paintSensor.drl>

Cave is hidden, playing the game purely with Sensors.

[![](/legacy/assets/images/2012/02/7e2e00387cac-wumpus1.png)](<http://2.bp.blogspot.com/-hgzThfa_sik/TzCS2dNOfgI/AAAAAAAAAqA/cfw6t3trQis/s1600/wumpus1.png>)

Cave is now shown, but unvisited rooms are greyed out.

[![](/legacy/assets/images/2012/02/124a73573e3e-wumpus3.png)](<http://1.bp.blogspot.com/-CHNlj_6AaPg/TzCS0ej9pGI/AAAAAAAAApo/JunZB503d2U/s1600/wumpus3.png>)

Cheating reveals all, I have shot the Wumpus Dead

[![](/legacy/assets/images/2012/02/147b62a99260-wumpus2.png)](<http://2.bp.blogspot.com/-ai80aKpHv3A/TzCS06FwQtI/AAAAAAAAAp4/TrHgcRlasw0/s1600/wumpus2.png>)

Window Builder with MigLayout was used to create the panels, buttons and forms

[![](/legacy/assets/images/2012/02/b96013a42ed9-wumpus_window_builder.png)](<http://4.bp.blogspot.com/-_lYJ5U6s5J8/TzCW-v19CUI/AAAAAAAAAqI/Goy1kWNNtI4/s1600/wumpus_window_builder.png>)

Here is the code to incrementally render the cave rooms:
[code]
    function void paintCaveCell(String image, Cell cell, GameView gv, GameUI gui) {  
         int rowIndent = 20;  
         int colIndent = 5;  
         int rowPad = cell.getRow() * gv.getCellPadding();  
         int colPad = cell.getCol() * gv.getCellPadding();  
         int y = (4 - cell.getRow()) * 50 - rowPad + rowIndent;  
         int x = cell.getCol() * 50 + colPad + colIndent;  
           
         Graphics caveG = gui.getCavePanel().getCaveG();  
         caveG.setColor( Color.WHITE ); // background  
         caveG.fillRect( x, y,  gv.getCellWidth(), gv.getCellHeight() );  
         caveG.drawImage( ImageIO.read( GameView.class.getResource( image ) ), x, y, gv.getCellHeight(), gv.getCellWidth(), gui.getCavePanel() );  
    }  
      
    rule "Init CaveDirty" when  
        not CaveDirty()  
    then  
        insert( new CaveDirty() );  
    end  
      
    rule "Create CompositeImage" when  
        $c : Cell()  
        not CompositeImageName( cell == $c )  
    then  
        CompositeImageName cin = new CompositeImageName($c, "", "", "", "");  
        insert( cin );  
    end    
      
    rule "Reset CompositeImage" when  
        $cin : CompositeImageName()  
        not Cell( row == $cin.cell.row, col == $cin.cell.col)  
    then  
        retract( $cin );  
    end      
      
    rule "Base Paint" when  
        $c : Cell()  
        $cin : CompositeImageName( cell == $c );  
    then  
    end      
      
    rule "Paint Gold" extends "Base Paint" when  
        Gold(row == $c.row, col == $c.col)    
    then  
       modify( $cin ) { gold = "gold" };  
    end  
      
    rule "Paint Empty Gold" extends "Base Paint" when  
        not Gold(row == $c.row, col == $c.col)    
    then  
       modify( $cin ) { gold = "" };  
    end  
      
    rule "Paint Pit" extends "Base Paint" when  
        Pit(row == $c.row, col == $c.col)    
    then  
       modify( $cin ) { pit = "pit" };  
    end  
      
    rule "Paint Empty Pit" extends "Base Paint" when  
        not Pit(row == $c.row, col == $c.col)    
    then  
       modify( $cin ) { pit = "" };  
    end  
      
    rule "Paint Wumpus Alive" extends "Base Paint" when  
        Wumpus(alive == true, row == $c.row, col == $c.col)    
    then  
       modify( $cin ) { wumpus = "wumpus_alive" };  
    end  
      
    rule "Paint Wumpus Dead" extends "Base Paint" when  
        Wumpus(alive == false, row == $c.row, col == $c.col)    
    then  
       modify( $cin ) { wumpus = "wumpus_dead" }  
    end  
      
    rule "Paint Empty Wumpus" extends "Base Paint" when  
        not Wumpus(row == $c.row, col == $c.col)    
    then  
       modify( $cin ) { wumpus = "" }  
    end  
      
      
    rule "Paint Hero Direction Up" extends "Base Paint" when   
        $h : Hero( direction == Direction.UP, row == $c.row, col == $c.col )  
    then  
         modify( $cin ) { hero = "hero_up" };  
    end      
      
    rule "Paint Hero Direction Down" extends "Base Paint"  when  
        $h : Hero( direction == Direction.DOWN, row == $c.row, col == $c.col  )  
    then  
        modify( $cin ) { hero = "hero_down" };  
    end     
      
    rule "Paint Hero Direction Left" extends "Base Paint"  when  
        $h : Hero( direction == Direction.LEFT, row == $c.row, col == $c.col  )  
    then  
        modify( $cin ) { hero = "hero_left" };  
    end      
      
    rule "Paint Hero Direction Right" extends "Base Paint" when  
        $h : Hero( direction == Direction.RIGHT, row == $c.row, col == $c.col  )  
    then  
        modify( $cin ) { hero = "hero_right" };  
    end   
      
    rule "Paint Empty Hero" extends "Base Paint" when  
        not Hero( row == $c.row, col == $c.col  )  
    then  
        modify( $cin ) { hero = "" };  
    end     
      
    rule "Paint Hidden Room" when   
        $gui : GameUI( cavePanel != null && cavePanel.caveG != null  )  
        $cd : CaveDirty() @watch(!*)  
        $gv : GameView(showAllCells == false)  
        $c : Cell(hidden == true)   
    then  
       paintCaveCell( "hidden_room.png", $c, $gv, $gui);  
       modify( $cd ) { dirty = true };  
    end  
      
      
    rule "Paint Empty Room" when   
       $gui : GameUI( cavePanel != null && cavePanel.caveG != null )  
        $cd : CaveDirty() @watch(!*)     
       ($gv : GameView(showAllCells == true) and $c : Cell() ) or  
       ($gv : GameView(showAllCells == false) and $c : Cell(hidden == false) )        
       CompositeImageName( cell == $c, pit == "", wumpus == "", gold == "", hero == "" ) @watch(*)  
    then  
       paintCaveCell( "empty_room.png", $c, $gv, $gui );  
       modify( $cd ) { dirty = true };  
    end   
      
    rule "Paint Non Empty Room" when  
       $gui : GameUI( cavePanel != null && cavePanel.caveG != null )  
       $cd : CaveDirty() @watch(!*)     
       ($gv : GameView(showAllCells == true) and $c : Cell() ) or  
       ($gv : GameView(showAllCells == false) and $c : Cell(hidden == false) )      
       $cin : CompositeImageName( cell == $c, ( !(hero != "" && pit != "")  &&  // don't draw a hero on the same square as a pit or an alive wumpus, as the game is over  
                                                !(hero != "" && wumpus == "wumpus_alive") &&   
                                                !(pit == "" && wumpus == "" && gold == "" && hero == "") ) ) @watch(*)  
    then  
        paintCaveCell( $cin.pit + $cin.wumpus + $cin.gold +  $cin.hero + ".png", $cin.cell, $gv, $gui );  
        modify( $cd ) { dirty = true };  
    end  
      
    rule "Redraw Cave" no-loop salience -500 when  
       $gui : GameUI()   
       $cd : CaveDirty( dirty == true )  
    then  
       $gui.updateCave();  
       modify( $cd ) { dirty = false };  
    end  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fwumpus-world-lives.html&linkname=Wumpus%20World%20Lives%21%21%21> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fwumpus-world-lives.html&linkname=Wumpus%20World%20Lives%21%21%21> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fwumpus-world-lives.html&linkname=Wumpus%20World%20Lives%21%21%21> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fwumpus-world-lives.html&linkname=Wumpus%20World%20Lives%21%21%21> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fwumpus-world-lives.html&linkname=Wumpus%20World%20Lives%21%21%21> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fwumpus-world-lives.html&linkname=Wumpus%20World%20Lives%21%21%21> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2012%2F02%2Fwumpus-world-lives.html&linkname=Wumpus%20World%20Lives%21%21%21> "Email")
  *[]: 2010-05-25T16:11:00+02:00