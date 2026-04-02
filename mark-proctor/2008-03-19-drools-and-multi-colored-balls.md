---
layout: post
title: "Drools and Multi Colored Balls"
date: 2008-03-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/03/drools-and-multi-colored-balls.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools and Multi Colored Balls](<https://blog.kie.org/2008/03/drools-and-multi-colored-balls.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 19, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I thought I would share with our readers a thread from our priority support system. It’s an interesting thread as it covers some complex constraint problems in good detail, which I think most rules users might find interesting, and it also demonstrates the level of support we provide to our priority customers. This conversation is printed “as is” with only the user and customer names removed. Services have just asked me to mention that when you purchase JBoss Drools priority support subscriptions, you aren’t just getting high quality support as shown below, but also a legal commitment from us to respond with guaranteed response times (whose values depend on the type of agreement they purchased of course).

User  
I have a query to help me retrieve different combination of 5 balls out of 20 balls.

Here is my simple query,
[code]
    query "get balls set"  
    ball1 : Ball();  
    ball2 : Ball(this != ball1);  
    ball3 : Ball(this != ball1 && != ball2);  
    ball4 : Ball(this != ball1 && != ball2 && != ball3);  
    ball5 : Ball(this != ball1 && != ball2 && != ball3 && != ball4);  
    end  
    
[/code]

And now, I want to add one more rule to this query.  
The rule is, only 0-2 balls can be (color == ‘yellow’).

That means, after the rule was added, I may have a set of balls that having,  
no balls in yellow color; or  
1 ball in yellow color; or  
2 balls in yellow color.

So, how should I modify the query?

* * *

Edson   
In other words, balls 3, 4 and 5 must be different from yellow, right?

query “get balls set”  
ball1 : Ball();  
ball2 : Ball(this != ball1);  
ball3 : Ball(this != ball1 && != ball2, color != “yellow” );  
ball4 : Ball(this != ball1 && != ball2 && != ball3, color != “yellow” );  
ball5 : Ball(this != ball1 && != ball2 && != ball3 && != ball4, color != “yellow” );  
end

Does that help you?

* * *

User  
Yes, you are right. Thank you.  
What if I want to apply some rules on the ball set to ensure some mutually exclusion?

Say,  
1\. color == ‘red’ and color == ‘blue’ cannot be co-exists in the same ball set.  
2\. when having 2 size == ‘medium’, no ball with size == ‘big’ can be selected.

And I am going to have dozen of these mutually exclusion rules.

* * *

Edson  
Well, all constraints must be expressed in some way. Some are more complex than others, but the language is Turing complete and any constraint can be expressed.

So, for your first question, we can use a simple approach writing down the possible combinations and using a class to represent the mutually exclusive colors. You can obviously hard code the colors, but I’m just trying to show you different approaches to the problem:
[code]
    query "avoid mutually exclusive colors"  
    ball1 : Ball( $c1 : color );  
    ball2 : Ball(this not in ( ball1 ), $c2 : color );  
    ball3 : Ball(this not in ( ball1, ball2 ), $c3 : color  );  
    ball4 : Ball(this not in ( ball1, ball2, ball3 ), $c4 : color  );  
    ball5 : Ball(this not in ( ball1, ball2, ball3, ball4 ), $c5 : color );  
    not MutuallyExclusiveColors((color1==$c1 && color2 in ($c2,$c3,$c4,$c5))||  
                            (color1==$c2 && color2 in ($c1,$c3,$c4,$c5))||  
                            (color1==$c3 && color2 in ($c1,$c2,$c4,$c5))||  
                            (color1==$c4 && color2 in ($c1,$c2,$c3,$c5))||  
                            (color1==$c5 && color2 in ($c1,$c2,$c3,$c4)))  
    end
[/code]

Now, we can also use a simple trick to add some flexibility, and a whole new set of possibilities are open for us. Since we can create lists using the MVEL dialect, we can define a dummy function to help us.
[code]
    function java.util.List returnList( java.util.List list ) {  
    return list;  
    }
[/code]

So, we can express your original question with a rule like that:
[code]
    rule "Select maximum 2 yellow balls"  
    when  
    $b1 : Ball( )  
    $b2 : Ball( this not in ($b1) )  
    $b3 : Ball( this not in ($b1, $b2) )  
    $b4 : Ball( this not in ($b1, $b2, $b3) )  
    $b5 : Ball( this not in ($b1, $b2, $b3, $b4) )  
    Number( intValue <= 2 )    
     from accumulate( $b : Ball( color == "yellow" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),                    
                      count( $b ) )  
    then  
    System.out.println( "Balls: "+$b1+" "+$b2+" "+$b3+" "+$b4+" "+$b5 );  
    end
[/code]

The same way, we can express your red/blue constraint by writing something like:
[code]
    rule "red and blue can not co-exist"  
    when  
    $b1 : Ball( )  
    $b2 : Ball( this not in ($b1) )  
    $b3 : Ball( this not in ($b1, $b2) )  
    $b4 : Ball( this not in ($b1, $b2, $b3) )  
    $b5 : Ball( this not in ($b1, $b2, $b3, $b4) )  
    Number( $red : intValue )  
    from accumulate( $b : Ball( color == "red" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),  
                  count( $b ) )  
    Number( intValue == 0 || eval( $red == 0 ) )  
    from accumulate( $b : Ball( color == "blue" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),  
                  count( $b ) )  
    then  
    System.out.println( "Balls: "+$b1+" "+$b2+" "+$b3+" "+$b4+" "+$b5 );  
    end
[/code]

Your second constraint can be expressed as:
[code]
    rule "if there are 2 or more mediums, no big allowed"  
    when  
    $b1 : Ball( )  
    $b2 : Ball( this not in ($b1) )  
    $b3 : Ball( this not in ($b1, $b2) )  
    $b4 : Ball( this not in ($b1, $b2, $b3) )  
    $b5 : Ball( this not in ($b1, $b2, $b3, $b4) )  
    Number( $big : intValue )  
    from accumulate( $b : Ball( size == "big" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),  
                     count( $b ) )  
    Number( intValue < 2 || eval( $big == 0 ) )  
    from accumulate( $b : Ball( size == "medium" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),  
                     count( $b ) )  
    then  
    System.out.println( "Balls: "+$b1+" "+$b2+" "+$b3+" "+$b4+" "+$b5 );  
    end
[/code]

Now I would like to call your attention to the fact that such kind of rules have the potential for combinatory explosion and, as such, a great performance degradation.

What I mean is that if you have for instance 10 balls in the working memory and you want to select 5, you are effectivelly doing permutation without repetitions, whose total possible permutations are given by the formula:
[code]
    P(10, 5) = 10! / (10-5)! = 30240 possible results.
[/code]

If you add just one more ball to the working memory, you will get:
[code]
    P(11, 5) = 11! / (11-5)! = 55440 possible results.
[/code]

As you can see, it is an exponential growth. Just something to be aware of.

* * *

User  
OK, I digested your message now.  
It helps alot.

I am trying to merge all your 3 rules into a single query.  
Like this,
[code]
    Query "Merging all rules into single query"  
    $b1 : Ball( )  
    $b2 : Ball( this not in ($b1) )  
    $b3 : Ball( this not in ($b1, $b2) )  
    $b4 : Ball( this not in ($b1, $b2, $b3) )  
    $b5 : Ball( this not in ($b1, $b2, $b3, $b4) )  
    Number( intValue <= 2 )    
    from accumulate( $b : Ball( color == "yellow" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),                    
                     count( $b ) )  
    not ( Number( $red : intValue )  
          from accumulate( $b : Ball( color == "red" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),                          
                           count( $b ) )       
      &&     
      Number( intValue == 0 || eval( $red == 0 ) )          
          from accumulate( $b : Ball( color == "blue" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),                          
                           count( $b ) ) )  
    not ( Number( $big : intValue )          
          from accumulate( $b : Ball( size == "big" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),                          
                           count( $b ) )     
      &&     
      Number( intValue < 2 || eval( $big == 0 ) )  
           from accumulate( $b : Ball( size == "medium" ) from returnList( [$b1, $b2, $b3, $b4, $b5] ),  
                            count( $b ) )  
    
[/code]

Do you think I can merge these 3 rules like this?  
And after merging it, would it introduce any new performance issues?

* * *

Edson  
Technically speaking, you can merge them. The major impact is still the combinatorial explosion the first 5 patterns will cause, as detailed in my previous message, but of course, each additional pattern will make the query a bit heavier.

Also, it is not easy to read it, but if that is what you need, then I don’t think there is any other way.

Finally, with a small modification to your dummy function, you can avoid calling it every time to create the list over and over again.

The “from” CE will always iterate over the elements of the collection that is returned by the function call, so, instead of returning a collection of balls, change it to return a collection of collection of balls:
[code]
    function java.util.List returnWrappedList( java.util.List list ) {  
    return new ArrayList( list );  
    }
[/code]

Then you can write a pattern in your query like:
[code]
    $balls : List() from returnWrappedList( [$b1,$b2,$b3,$b4,$b5] )
[/code]

And then you can use $balls instead of recreating the list over and over again. Example:
[code]
    Number( intValue <= 2 )  
    from accumulate( $b : Ball( color == "yellow" ) from $balls,  
                     count( $b ) )  
      
    
[/code]

————————  
NB:  
With latest MVEL (1.2.24), we don’t need a dummy function anymore… we can simply use MVEL’s return statement:

from return( [$b1, $b2, $b3, $b4, $b5] )

Or if we need a wrapped list:

from return( [[ $b1, $b2, $b3, $b4, $b5 ]] )

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-and-multi-colored-balls.html&linkname=Drools%20and%20Multi%20Colored%20Balls> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-and-multi-colored-balls.html&linkname=Drools%20and%20Multi%20Colored%20Balls> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-and-multi-colored-balls.html&linkname=Drools%20and%20Multi%20Colored%20Balls> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-and-multi-colored-balls.html&linkname=Drools%20and%20Multi%20Colored%20Balls> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-and-multi-colored-balls.html&linkname=Drools%20and%20Multi%20Colored%20Balls> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-and-multi-colored-balls.html&linkname=Drools%20and%20Multi%20Colored%20Balls> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F03%2Fdrools-and-multi-colored-balls.html&linkname=Drools%20and%20Multi%20Colored%20Balls> "Email")