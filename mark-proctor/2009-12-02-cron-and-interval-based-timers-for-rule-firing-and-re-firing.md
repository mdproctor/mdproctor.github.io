---
layout: post
title: "Cron and Interval based timers for rule firing and re-firing"
date: 2009-12-02
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/12/cron-and-interval-based-timers-for-rule-firing-and-re-firing.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Cron and Interval based timers for rule firing and re-firing](<https://blog.kie.org/2009/12/cron-and-interval-based-timers-for-rule-firing-and-re-firing.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- December 2, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

At ORF I did a presentation on ideas I’d like to do to improve our language. You can see that presentation here:  
[“Drools “Where do we go from here” – presented at ORF09″](<http://blog.athico.com/2009/10/drools-where-do-we-go-from-here-orf09.html>)

In this presentation I discussed the idea of [“cron”](<http://en.wikipedia.org/wiki/Cron>) based rules. Drools has supported the “duration” attribute for a long time now. When a rule is activated it does not fire straight away, instead it is scheduled to fire based on the given duration. If the rule is still true on or after that duration lapses it fires, otherwise if it becomes false before the duration lapses it is cancelled and unscheduled.

The problem here is the duration is a single value and the rule fires just once. This is useful, but somewhat limited. Instead wouldn’t it better if we could support various time based semantics for rule firing and re-firing (if the rule is still true).

While not exposed to the user I created pluggable Time semantics. This introduces the Timer interface:
[code]
    interface Timer {  
        /**  
         * Creates a Trigger for this Timer, based on the provided current timestamp.  
         */  
        Trigger createTrigger(long timestamp);  
    }
[/code]

The Trigger interface already existed as part of our unified clock and scheduling framework in Drools. Trigger tells the scheduler the next date to trigger the current job on. If we have multiple Timer semantics, not just duration, each Timer must be responsible for providing it’s own Trigger to handle the execution of those semantics.

The ‘duration’ keyword has now been renamed to ‘timer’, although backwards compatability has been kept. We now support two different timers ‘cron’ and ‘interval’. The ‘timer’ keyword takes a colon delimited prefix, using ‘cron:’ and ‘int:’ respectively. If no protocol is given, it assumes ‘int’.

We use the standard cron syntax (thank you quartz), with added support for seconds. And interval has two parameters and obeys the JDK Timer semantics of delay and period. Where delay is the initial delay and period is the period of time between each iteration.

So now we can do the following which will send an SMS to a give mobile number every 0, 15, 30 and 45 minutes past each hour, while the alarm remains true:
[code]
    rule "Send SMS every 15 minutes"  
        timer (cron:* 0/15 * * * ?)  
    when  
        $a : Alarm( on == true )  
    then  
        exitPoint[ "sms" ].insert( new Sms( $a.mobileNumber, "The alarm is still on" );  
    end
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcron-and-interval-based-timers-for-rule-firing-and-re-firing.html&linkname=Cron%20and%20Interval%20based%20timers%20for%20rule%20firing%20and%20re-firing> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcron-and-interval-based-timers-for-rule-firing-and-re-firing.html&linkname=Cron%20and%20Interval%20based%20timers%20for%20rule%20firing%20and%20re-firing> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcron-and-interval-based-timers-for-rule-firing-and-re-firing.html&linkname=Cron%20and%20Interval%20based%20timers%20for%20rule%20firing%20and%20re-firing> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcron-and-interval-based-timers-for-rule-firing-and-re-firing.html&linkname=Cron%20and%20Interval%20based%20timers%20for%20rule%20firing%20and%20re-firing> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcron-and-interval-based-timers-for-rule-firing-and-re-firing.html&linkname=Cron%20and%20Interval%20based%20timers%20for%20rule%20firing%20and%20re-firing> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcron-and-interval-based-timers-for-rule-firing-and-re-firing.html&linkname=Cron%20and%20Interval%20based%20timers%20for%20rule%20firing%20and%20re-firing> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcron-and-interval-based-timers-for-rule-firing-and-re-firing.html&linkname=Cron%20and%20Interval%20based%20timers%20for%20rule%20firing%20and%20re-firing> "Email")