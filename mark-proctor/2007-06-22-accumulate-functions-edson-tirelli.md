---
layout: post
title: "Accumulate Functions (Edson Tirelli)"
date: 2007-06-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/accumulate-functions-edson-tirelli.html
---

As we get closer to the release, everything is taking its final shape. This week was the time to get Accumulate CE ready for the release. For those who missed, Accumulate is a very powerful new Conditional Element for Drools 4.0, released next month. It allows you to operate on sets of data.

The general syntax for it is:

```drl
ResultPattern( fieldconstraint* )
from accumulate ( SourcePattern( fieldconstraint* )
                  init( code )
                  action( code )
                  reverse( code )
                  result( code ) )
```

Basically what accumulate does is execute the init code block, then “iterate” over the facts that match the SourcePattern executing the action code block for each of the facts and finally executing the result code block. The given result is matched against the ResultPattern and in case it evaluates to true, the condition matches. The reverse code block is optional and its function is to improve performance when retracting or modifying facts that had previously matched the SourcePattern.

Well, nothing better than a sample to get things more clear.

Rule: apply 10% discount to orders that include at least US$ 100,00 of toys.

```drl
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
```

As you can see in the example above, accumulate is really flexible and powerful. As each of the code blocks are either Java or MVEL code blocks, one can really do any kind of operation in there.

But then, someone can say: “Well, accumulate is pretty flexible and powerful, but I don’t want to keep writing code for common operations like the above”. So, that is something we were playing with during this week. We really want to provide you all the flexibility you need, but we also want to provide you with simplicity for the common cases. So, Accumulate Functions comes to the rescue.

You now have the possibility of using predefined functions to simplify accumulate usage for common cases. For instance, the rule above is using accumulate to perform a sum of values. The same rule can be written like that:

```drl
rule "Discount for orders that include US$100,00 of toys"
when
$o : Order()
$toysTotal : Number( doubleValue > 100 )
             from accumulate( OrderItem( order == $o, type == "toy", $value : value ),
                              sum( $value ) )
then
$o.setDiscountPercentage( 10 );
end
```

Much more simple now. What if you want a rule that tells you how much it would cost you a raise of X% for each department?

```drl
rule "Total raise"
when
$dpt : Department( $raise : raise )
$total : Number()
         from accumulate( Employee( dept == $dpt, $salary : salary ),
                            sum( $salary * $raise ) )
then
$dpt.setSalaryIncreaseValue( $total );
end
```

So, you can use any expression as a parameter to accumulate functions. We added most common used functions for use out of the box, like sum, average, count, min, max, etc.

But you say: “I liked the functions, but I have a custom function that I would like to provide to my users write rules with. Can I implement that function and provide to them, so that they don’t need to keep writing it themselves?”

Our answer is: “Of course!” ;)

We made Accumulate Functions pluggable and as simple as we could make them, so you can easily provide new functions for your users to use. For instance, pretend you have a very complex calculation that you need to do to get the cost of a given stock trade operation. Your users are writing rules to your specialist system to enable it to advise on which operations are more profitable, and so they have several rules that need to calculate such stock trade operation costs.  
To develop a new accumulate function, the only thing you need to do is create a java class that implements the [AccumulateFunction](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-core/src/main/java/org/drools/base/accumulators/AccumulateFunction.java?view=markup>) interface. The interface basically has a method that correspond to each of the Accumulate operations: init, action, reverse and result. [Here](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-core/src/main/java/org/drools/base/accumulators/AverageAccumulateFunction.java?view=markup>) you can see how easy it is to implement things like the [average function](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-core/src/main/java/org/drools/base/accumulators/AverageAccumulateFunction.java?view=markup>).

Finally, to wire your function into the system you can either call an [API (addAccumulateFunction())](<http://viewvc.jboss.org/cgi-bin/viewvc.cgi/labs/labs/jbossrules/trunk/drools-compiler/src/main/java/org/drools/compiler/PackageBuilderConfiguration.java?view=markup&sortdir=down>) or define a property. The property can be defined either in a configuration file or as a system property:

Example:

```
drools.accumulate.function.average = org.drools.base.accumulators.AverageAccumulateFunction
```

As simple as that.

Hope you all enjoy.

Happy Drooling!