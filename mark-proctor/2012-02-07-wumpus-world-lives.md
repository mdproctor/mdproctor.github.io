---
layout: post
title: "Wumpus World Lives!!!"
date: 2012-02-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/02/wumpus-world-lives.html
---

Wumpus world continues to improve and is now fully playable. The UI has a lot more polish now and nearly all of the code has been moved to DRL now, including the swing graphics rendering for the cave and the sensor panels. You’ll need to use master head to try it. Java is just used to build the kbase from the drl files and to create the swing panels, buttons and forms. WindowBuilder was used to graphical layout things.

The final thing I have to do is allow for client integration, so that people can write rules to automate the hero.

<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/init.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/commands.drl>  
[https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/collision.drl](<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/collision.drl%20>)   
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/score.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/view/ui.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/view/paintCave.drl>  
<https://github.com/droolsjbpm/drools/blob/master/drools-examples/src/main/resources/org/drools/examples/wumpus/view/paintSensor.drl>

Cave is hidden, playing the game purely with Sensors.

[![](/legacy/assets/images/2012/02/7e2e00387cac-wumpus1.png)](</assets/images/2012/02/809cf3423d13-wumpus1.png>)

Cave is now shown, but unvisited rooms are greyed out.

[![](/legacy/assets/images/2012/02/124a73573e3e-wumpus3.png)](</assets/images/2012/02/a7ccf05a90ab-wumpus3.png>)

Cheating reveals all, I have shot the Wumpus Dead

[![](/legacy/assets/images/2012/02/147b62a99260-wumpus2.png)](</assets/images/2012/02/e2a077c74226-wumpus2.png>)

Window Builder with MigLayout was used to create the panels, buttons and forms

[![](/legacy/assets/images/2012/02/b96013a42ed9-wumpus_window_builder.png)](</assets/images/2012/02/3981609bd194-wumpus_window_builder.png>)

Here is the code to incrementally render the cave rooms:

```drl
function void paintCaveCell(String image, Cell cell, GameView gv, GameUI gui) {     int rowIndent = 20;     int colIndent = 5;     int rowPad = cell.getRow() * gv.getCellPadding();     int colPad = cell.getCol() * gv.getCellPadding();     int y = (4 - cell.getRow()) * 50 - rowPad + rowIndent;     int x = cell.getCol() * 50 + colPad + colIndent;      Graphics caveG = gui.getCavePanel().getCaveG();     caveG.setColor( Color.WHITE ); // background     caveG.fillRect( x, y,  gv.getCellWidth(), gv.getCellHeight() );     caveG.drawImage( ImageIO.read( GameView.class.getResource( image ) ), x, y, gv.getCellHeight(), gv.getCellWidth(), gui.getCavePanel() );}
rule "Init CaveDirty"
when
not CaveDirty()
then
insert( new CaveDirty() );endrule "Create CompositeImage"
when
$c : Cell()    not CompositeImageName( cell == $c )
then
CompositeImageName cin = new CompositeImageName($c, "", "", "", "");    insert( cin );
end
rule "Reset CompositeImage"
when
$cin : CompositeImageName()    not Cell( row == $cin.cell.row, col == $cin.cell.col)
then
retract( $cin );
end
rule "Base Paint"
when
$c : Cell()    $cin : CompositeImageName( cell == $c );thenend
rule "Paint Gold" extends "Base Paint"
when
Gold(row == $c.row, col == $c.col)
then
modify( $cin ) { gold = "gold" };endrule "Paint Empty Gold" extends "Base Paint"
when
not Gold(row == $c.row, col == $c.col)
then
modify( $cin ) { gold = "" };endrule "Paint Pit" extends "Base Paint"
when
Pit(row == $c.row, col == $c.col)
then
modify( $cin ) { pit = "pit" };endrule "Paint Empty Pit" extends "Base Paint"
when
not Pit(row == $c.row, col == $c.col)
then
modify( $cin ) { pit = "" };endrule "Paint Wumpus Alive" extends "Base Paint"
when
Wumpus(alive == true, row == $c.row, col == $c.col)
then
modify( $cin ) { wumpus = "wumpus_alive" };endrule "Paint Wumpus Dead" extends "Base Paint"
when
Wumpus(alive == false, row == $c.row, col == $c.col)
then
modify( $cin ) { wumpus = "wumpus_dead" }endrule "Paint Empty Wumpus" extends "Base Paint"
when
not Wumpus(row == $c.row, col == $c.col)
then
modify( $cin ) { wumpus = "" }endrule "Paint Hero Direction Up" extends "Base Paint"
when
$h : Hero( direction == Direction.UP, row == $c.row, col == $c.col )
then
modify( $cin ) { hero = "hero_up" };
end
rule "Paint Hero Direction Down" extends "Base Paint"
when
$h : Hero( direction == Direction.DOWN, row == $c.row, col == $c.col  )
then
modify( $cin ) { hero = "hero_down" };
end
rule "Paint Hero Direction Left" extends "Base Paint"
when
$h : Hero( direction == Direction.LEFT, row == $c.row, col == $c.col  )
then
modify( $cin ) { hero = "hero_left" };
end
rule "Paint Hero Direction Right" extends "Base Paint"
when
$h : Hero( direction == Direction.RIGHT, row == $c.row, col == $c.col  )
then
modify( $cin ) { hero = "hero_right" };
end
rule "Paint Empty Hero" extends "Base Paint"
when
not Hero( row == $c.row, col == $c.col  )
then
modify( $cin ) { hero = "" };
end
rule "Paint Hidden Room"
when
$gui : GameUI( cavePanel != null && cavePanel.caveG != null  )    $cd : CaveDirty() @watch(!*)    $gv : GameView(showAllCells == false)    $c : Cell(hidden == true)
then
paintCaveCell( "hidden_room.png", $c, $gv, $gui);   modify( $cd ) { dirty = true };endrule "Paint Empty Room"
when
$gui : GameUI( cavePanel != null && cavePanel.caveG != null )    $cd : CaveDirty() @watch(!*)      ($gv : GameView(showAllCells == true) and $c : Cell() ) or   ($gv : GameView(showAllCells == false) and $c : Cell(hidden == false) )         CompositeImageName( cell == $c, pit == "", wumpus == "", gold == "", hero == "" ) @watch(*)
then
paintCaveCell( "empty_room.png", $c, $gv, $gui );   modify( $cd ) { dirty = true };
end
rule "Paint Non Empty Room"
when
$gui : GameUI( cavePanel != null && cavePanel.caveG != null )   $cd : CaveDirty() @watch(!*)      ($gv : GameView(showAllCells == true) and $c : Cell() ) or   ($gv : GameView(showAllCells == false) and $c : Cell(hidden == false) )       $cin : CompositeImageName( cell == $c, ( !(hero != "" && pit != "")  &&  // don't draw a hero on the same square as a pit or an alive wumpus, as the game is over                                            !(hero != "" && wumpus == "wumpus_alive") &&                                             !(pit == "" && wumpus == "" && gold == "" && hero == "") ) ) @watch(*)
then
paintCaveCell( $cin.pit + $cin.wumpus + $cin.gold +  $cin.hero + ".png", $cin.cell, $gv, $gui );    modify( $cd ) { dirty = true };endrule "Redraw Cave"
no-loop
salience -500
when
$gui : GameUI()    $cd : CaveDirty( dirty == true )
then
$gui.updateCave();   modify( $cd ) { dirty = false };
end
```