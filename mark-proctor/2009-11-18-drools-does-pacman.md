---
layout: post
title: "Drools does Pacman"
date: 2009-11-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/11/drools-does-pacman.html
---

In the interests of finding a fun and more complex problem with multiple things happening, I decided to start writting a Pacman implementation. The basics are now in place, in that I can load a grid and guide a Pacman around it with a Monster (Ghost) tracking it.

[![](/legacy/assets/images/2009/11/80f1918da9d3-Pac-man.png)](</assets/images/2009/11/6fbe5035ea86-Pac-man.png>)  
The grid is loaded from a text file that uses symbols to map the layout, currently I use a very simple layout that looks like this:

```text
* * * * * * * * * * *
* # . . . _ . . . # *
* . * * * * * * * . *
* . * * * * * * * . *
* . . . . # . . . . *
* . * * * * * * * . *
* . * * * * * * * . *
* . . . . # . . . . *
* . * * * * * * * . *
* . * * * * * * * . *
* # . . . _ . . . # *
* * * * * * * * * * *
```

* Wall  
. Food  
# Power Pill  
_ Empty

When the game starts off Pacman is in the lower empty cell and the Monster in the top empty cell. The arrow keys move Pacman around and the Monster tracks the Pacman. The rules are split into four drl files; base, key-handlers, Pacman and Monster.

A KeyListener implementation is hooked up to a WorkingMemory EntryPoint and feeds in key presses. From the KeyEvent it creates a derived (not in WorkingMemory) possible Direction and validates that Direction. If the new Direction is valid the old Direction is retracted and the new one inserted. The exitpoint is used to send print information to a channel, which is appended to the GUI.

```drl
rule KeyListenerRule
dialect "mvel"
when
$keyEvent : KeyEvent() from entry-point "KeyListener"   $char     : Character( name == "Pacman" )   $l        : Location( character == $char )   $newD     : Direction() from createDirection( $l.character, $keyEvent )   $target   : Cell( row == ($l.row + $newD.vertical), col == ($l.col + $newD.horizontal) )               CellContents( cell == $target, cellType != CellType.WALL )      $oldD     : Direction( character == $l.character )
then
exitPoints["ConsoleExitPoint" ].insert( "insert " + $newD + "n" );   retract( $keyEvent );   retract( $oldD );   insert( $newD );
end
```

As the Tick, simulated time, increases we attempt to change a Character’s Location based on the given Direction. The rule makes sure the new Location is valid, and if so schedules the move to the new Location, in time with the Tick.

```drl
rule validDirection
dialect "mvel"
when
$l : Location( )  $d : Direction( character == $l.character )  $target : Cell( row == ($l.row + $d.vertical), col == ($l.col +$d.horizontal) )  CellContents( cell == $target, cellType != CellType.WALL )  not ScheduledLocationUpdate( location == $l )  $t : Tick()
then
insert( new ScheduledLocationUpdate($l, $l.row += $d.vertical,$l.col += $d.horizontal, $t.tock + 1) );endrule setNewDirection
dialect "mvel"
when
$s : ScheduledLocationUpdate()  $l : Location( this == $s.location )  Tick( tock == $s.tock )
then
exitPoints["ConsoleExitPoint"].insert( "set new Location " + $l + "n"  ); modify( $l ) { row = $s.row, col = $s.col }; retract( $s );
end
```

As the pacman moves around it detects the CellContents, if it’s Food it’ll increase the score by 1.

```drl
rule EatFood
dialect "mvel"
no-loop
when
$char : Character( name == "Pacman" )   $l : Location( character == $char )   $target : Cell( row == $l.row, col == $l.col)   $contents : CellContents( cell == $target, cellType == CellType.FOOD )   $s : Score()
then
modify( $contents ) { cellType = CellType.EMPTY };   modify( $s ) { score += 1 };
end
```

Among other things it’s also looking out for Monster collisions.

```drl
rule MonsterCollision
dialect "mvel"
no-loop
when
$pac    : Character( name == "Pacman" )   $pacLoc : Location( character == $pac )   $mon    : Character( name == "Monster" )   $monLoc : Location( character == $mon, col == $pacLoc.col, row == $pacLoc.row )   $t : Tick()
then
retract( $t );endrule FinishedKilled
dialect "mvel"
when
$pac    : Character( name == "Pacman" )   $pacLoc : Location( character == $pac )   $mon    : Character( name == "Monster" )   $monLoc : Location( character == $mon, col == $pacLoc.col, row == $pacLoc.row )   not Tick()      $s : Score()
then
exitPoints["ConsoleExitPoint"].insert( "Killed!!!! score = " + $s.score + " n" );   kcontext.knowledgeRuntime.halt();
end
```

The implementation currently uses a simple distance diff from the Monster to the Pacman to determine the Monster direction. The direction must be valid and if both a horizontal and a vertical direction is valid it uses dynamic salience to pick the one with the highest difference. This is a simplistic approach, just to get the ball rolling, ideally we would implement the logic as in the original arcade game.

```drl
rule GoRight
dialect "mvel"
salience (Math.abs( $df.colDiff ))
when
$df   : DirectionDiff(colDiff > 0 )   $target : Cell(  row == $df.row, col == ($df.col + 1) )   CellContents( cell == $target, cellType != CellType.WALL )      $d : Direction( character == $df.fromChar, horizontal != Direction.RIGHT)
then
retract( $d );   retract( $df );   insert( new Direction($df.fromChar, Direction.RIGHT, 0 ) );      endrule GoDown
dialect "mvel"
salience (Math.abs( $df.rowDiff ))
when
$df   : DirectionDiff(rowDiff < 0 )    $target : Cell(  col == $df.col, row == ($df.row - 1))    CellContents( cell == $target, cellType != CellType.WALL )        $d : Direction( character == $df.fromChar, vertical != Direction.DOWN)
then
retract( $d );    retract( $df );     insert( new Direction($df.fromChar, 0,  Direction.DOWN ) );
end
```

Running the game and pressing the left arrow gives the following output. Notice Pacman moves to the left and stops when he reaches the wall, the Monster tracks him to the left and then comes down for the kill.

```text
insert Direction Pacman speed = 5 LEFT
set new Location Location Monster speed = 3 10:4
set new Location Location Pacman speed = 5 1:4
set new Location Location Monster speed = 3 10:3
set new Location Location Pacman speed = 5 1:3
set new Location Location Monster speed = 3 10:4
set new Location Location Monster speed = 3 10:3
set new Location Location Pacman speed = 5 1:2
set new Location Location Monster speed = 3 10:2
retract Direction Monster speed = 3 LEFT
set new Location Location Monster speed = 3 10:1
set new Location Location Pacman speed = 5 1:1
retract Direction Pacman speed = 5 LEFT
set new Location Location Monster speed = 3 9:1
set new Location Location Monster speed = 3 8:1
set new Location Location Monster speed = 3 7:1
set new Location Location Monster speed = 3 6:1
set new Location Location Monster speed = 3 5:1
set new Location Location Monster speed = 3 4:1
set new Location Location Monster speed = 3 3:1
set new Location Location Monster speed = 3 2:1
set new Location Location Monster speed = 3 1:1
Killed!!!! score = 8
```

I’ve committed everything to drools-examples, you’ll need drools trunk, as there are a few fixes necessary for this to work:  
[trunk/drools-examples/drools-examples-drl/src/main/java/org/drools/examples/pacman/](<http://anonsvn.jboss.org/repos/labs/labs/jbossrules/trunk/drools-examples/drools-examples-drl/src/main/java/org/drools/examples/pacman/>)  
[trunk/drools-examples/drools-examples-drl/src/main/resources/org/drools/examples/pacman/](<http://anonsvn.jboss.org/repos/labs/labs/jbossrules/trunk/drools-examples/drools-examples-drl/src/main/resources/org/drools/examples/pacman/>)  
[trunk/drools-examples/drools-examples-drl/src/main/rules/org/drools/examples/pacman/](<http://anonsvn.jboss.org/repos/labs/labs/jbossrules/trunk/drools-examples/drools-examples-drl/src/main/rules/org/drools/examples/pacman/>)

It’s still very basic. Next it needs to be hooked up to a GUI, such as SwtPacman, the source code of which is provided here on a wiki page where you can also add notes:  
<http://www.jboss.org/community/docs/DOC-14378>

Then it should be updated to real Pacman grid layouts and all the monsters added, each with it’s own custom logic. There is also additional logic like Ghosts slowing down when they turn corners and Pacman slowing down when he eats food. You can find out all the details at Wikipedia, [here](<http://en.wikipedia.org/wiki/Pac-Man>).

Ghost Color| Original _Pac Man_[[13]](<http://en.wikipedia.org/wiki/Pac-Man#cite_note-12>)| American _Pac-Man_  
---|---|---  
Character (Personality)| Translation| Nickname| Translation| Alternate  
character| Alternate  
nickname| Character (Personality)| Nickname  
Red| Oikake (????)| chaser| Akabei (???)| red guy| Urchin| Macky| Shadow| Blinky  
Pink| Machibuse (????)| ambusher| Pinky (????)| pink guy| Romp| Micky| Speedy| Pinky  
Cyan| Kimagure (????)| fickle| Aosuke (??)| blue guy| Stylist| Mucky| Bashful| Inky  
Orange| Otoboke (???)| stupid| Guzuta (???)| slow guy| Crybaby| Mocky| Pokey| Clyde  
  
I hope everyone finds this useful, and if anyone wants to help me finish this please dive straight in :)