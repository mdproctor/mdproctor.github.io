---
layout: post
title: "Accumulate Functions (Edson Tirelli)"
date: 2007-06-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/accumulate-functions-edson-tirelli.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Accumulate Functions (Edson Tirelli)](<https://blog.kie.org/2007/06/accumulate-functions-edson-tirelli.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 22, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

As we get closer to the release, everything is taking its final shape. This week was the time to get Accumulate CE ready for the release. For those who missed, Accumulate is a very powerful new Conditional Element for Drools 4.0, released next month. It allows you to operate on sets of data.

The general syntax for it is:
[code]
      
    ResultPattern( fieldconstraint* )  
    from accumulate ( SourcePattern( fieldconstraint* )  
                      init( code )  
                      action( code )  
                      reverse( code )  
                      result( code ) )  
    
[/code]

Basically what accumulate does is execute the init code block, then “iterate” over the facts that match the SourcePattern executing the action code block for each of the facts and finally executing the result code block. The given result is matched against the ResultPattern and in case it evaluates to true, the condition matches. The reverse code block is optional and its function is to improve performance when retracting or modifying facts that had previously matched the SourcePattern.

Well, nothing better than a sample to get things more clear.

Rule: apply 10% discount to orders that include at least US$ 100,00 of toys.
[code]
      
    rule "Discount for orders that include US$100,00 of toys"  
    when  
    $o : Order()  
    $toysTotal : Number( doubleValue > 100 )  
      from accumulate( OrderItem( order == $o, type == "toy", $value : value ),  
                         init( double total = 0; ),  
                       action( total += $value; ),  
                       reverse( total -= $value; ),  
                       result( new Double( total ) ) )  
    then  
     $o.setDiscountPercentage( 10 );  
    end  
    
[/code]

As you can see in the example above, accumulate is really flexible and powerful. As each of the code blocks are either Java or MVEL code blocks, one can really do any kind of operation in there.

But then, someone can say: “Well, accumulate is pretty flexible and powerful, but I don’t want to keep writing code for common operations like the above”. So, that is something we were playing with during this week. We really want to provide you all the flexibility you need, but we also want to provide you with simplicity for the common cases. So, Accumulate Functions comes to the rescue.

You now have the possibility of using predefined functions to simplify accumulate usage for common cases. For instance, the rule above is using accumulate to perform a sum of values. The same rule can be written like that:
[code]
    rule "Discount for orders that include US$100,00 of toys"  
    when  
    $o : Order()  
    $toysTotal : Number( doubleValue > 100 )  
                 from accumulate( OrderItem( order == $o, type == "toy", $value : value ),  
                                  sum( $value ) )  
    then  
    $o.setDiscountPercentage( 10 );  
    end  
    
[/code]

Much more simple now. What if you want a rule that tells you how much it would cost you a raise of X% for each department?
[code]
      
    rule "Total raise"  
    when  
    $dpt : Department( $raise : raise )  
    $total : Number()  
             from accumulate( Employee( dept == $dpt, $salary : salary ),  
                                sum( $salary * $raise ) )  
    then  
    $dpt.setSalaryIncreaseValue( $total );  
    end  
    
[/code]

So, you can use any expression as a parameter to accumulate functions. We added most common used functions for use out of the box, like sum, average, count, min, max, etc.

But you say: “I liked the functions, but I have a custom function that I would like to provide to my users write rules with. Can I implement that function and provide to them, so that they don’t need to keep writing it themselves?”

Our answer is: “Of course!” ;)

We made Accumulate Functions pluggable and as simple as we could make them, so you can easily provide new functions for your users to use. For instance, pretend you have a very complex calculation that you need to do to get the cost of a given stock trade operation. Your users are writing rules to your specialist system to enable it to advise on which operations are more profitable, and so they have several rules that need to calculate such stock trade operation costs.  
To develop a new accumulate function, the only thing you need to do is create a java class that implements the [AccumulateFunction](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-core/src/main/java/org/drools/base/accumulators/AccumulateFunction.java?view=markup>) interface. The interface basically has a method that correspond to each of the Accumulate operations: init, action, reverse and result. [Here](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-core/src/main/java/org/drools/base/accumulators/AverageAccumulateFunction.java?view=markup>) you can see how easy it is to implement things like the [average function](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-core/src/main/java/org/drools/base/accumulators/AverageAccumulateFunction.java?view=markup>).

Finally, to wire your function into the system you can either call an [API (addAccumulateFunction())](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-compiler/src/main/java/org/drools/compiler/PackageBuilderConfiguration.java?view=markup&sortdir=down>) or define a property. The property can be defined either in a configuration file or as a system property:

Example:
[code]
      
    drools.accumulate.function.average = org.drools.base.accumulators.AverageAccumulateFunction  
    
[/code]

As simple as that.

Hope you all enjoy.

Happy Drooling!

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Faccumulate-functions-edson-tirelli.html&linkname=Accumulate%20Functions%20%28Edson%20Tirelli%29> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Faccumulate-functions-edson-tirelli.html&linkname=Accumulate%20Functions%20%28Edson%20Tirelli%29> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Faccumulate-functions-edson-tirelli.html&linkname=Accumulate%20Functions%20%28Edson%20Tirelli%29> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Faccumulate-functions-edson-tirelli.html&linkname=Accumulate%20Functions%20%28Edson%20Tirelli%29> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Faccumulate-functions-edson-tirelli.html&linkname=Accumulate%20Functions%20%28Edson%20Tirelli%29> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Faccumulate-functions-edson-tirelli.html&linkname=Accumulate%20Functions%20%28Edson%20Tirelli%29> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Faccumulate-functions-edson-tirelli.html&linkname=Accumulate%20Functions%20%28Edson%20Tirelli%29> "Email")