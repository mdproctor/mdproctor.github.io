---
layout: post
title: "Calendar support with Drools"
date: 2009-12-09
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/12/calendar-support-with-drools.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Calendar support with Drools](<https://blog.kie.org/2009/12/calendar-support-with-drools.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- December 9, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Last week I blogged about ‘cron’ and ‘int’ (interval) based timer support:  
[“Cron and Interval based timers for rule firing and re-firing”](<http://blog.athico.com/2009/12/cron-and-interval-based-timers-for-rule.html>)

This week I’ve added Calendaring support. Calendaring allows you to provide a Set of Calendar implementations that specify allowed and disallowed time segments. With this you could create a “week day” Calendar which would specify Monday to Friday as the included time segments, leaving Saturday and Sunday as not included. I can then specify that Calendar in a rule. Monday to Friday if the rule activates it will fire, over the weekend if the rule activates it will ignored.

The Calendar api is modelled on [Quartz ](<http://www.quartz-scheduler.org/>):
[code]
    public interface Calendar {      
        boolean isTimeIncluded(long timestamp);   
    }
[/code]

Quartz provides several good Calendar implementations, so it makes sense to leverage those, for this we we provide an adapter helper method:
[code]
    Calendar QuartzHelper.quartzCalendarAdapter(org.quartz.Calendar quartzCal)
[/code]

Calendars are registered with the StatefulKnowledgeSession:
[code]
    ksession.getCalendars().set( "week day", weekDayCal );
[/code]

Which means they can now be used in rules. They can be used in conjunction with normal rules and rules including timers.
[code]
    rule "weekdays are high priority"  
       calendars "weekday"  
    when   
        Alarm()  
    then  
        send( "priority high - we have an alarm );  
    end   
      
    rule "weekend are low priority"  
       calendars "weekend"  
    when   
        Alarm()  
    then  
        send( "priority low - we have an alarm );  
    end
[/code]

Now I can already imagine some of you are thinking, well that’s kinda cool and it’s nice the semantics of Calendars and a Calendaring api supported out of the box. But I could achieve much the same thing by asserting Calendars as facts, placing the Calendar constraint as the last pattern and it’ll block activations that are not included in the required time. While this is true, it would not work with Timer based rules. As we can now do this:
[code]
    rule "weekdays are high priority"  
       calendars "weekday"  
       timer (int:0 1h)  
    when   
        Alarm()  
    then  
        send( "priority high - we have an alarm );  
    end   
      
    rule "weekend are low priority"  
       calendars "weekend"  
       timer (int:0 4h)  
    when   
        Alarm()  
    then  
        send( "priority low - we have an alarm );  
    end
[/code]

The above rules use an interval based timer, a cron timer is also supported. On weekdays while there is an alarm it will trigger the rule initially straight away (delay of 0) and then every hour. At the weekends it will trigger the rule every four hours. If we had inserted the Calendar as a fact, we’d have to find some additional way to re-trigger the evaluation. Calendars themselves do not have mutable state, instead it’s more like a function that tells you if the specified date is included or not. While this is not impossible to solve, it’s getting messy very quickly. You’ll need additional trigger facts, that will force Calendar evaluation at required points in time, that are managed by your own scheduler. This way it’s efficient (no network propagation), clear syntax and intent and works out of the box. I should add that it’ll work out of the box with our simulation api, thanks to our unified clock implementation.

So what we have now is conditional rule based timers and calendaring. The cool thing here is we can use this for Drools Flow, using it to start processes or trigger wait states. While process centric implementations do have timer and calendaring support, the conditional rule integration adds a whole new level of power to this.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcalendar-support-with-drools.html&linkname=Calendar%20support%20with%20Drools> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcalendar-support-with-drools.html&linkname=Calendar%20support%20with%20Drools> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcalendar-support-with-drools.html&linkname=Calendar%20support%20with%20Drools> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcalendar-support-with-drools.html&linkname=Calendar%20support%20with%20Drools> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcalendar-support-with-drools.html&linkname=Calendar%20support%20with%20Drools> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcalendar-support-with-drools.html&linkname=Calendar%20support%20with%20Drools> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F12%2Fcalendar-support-with-drools.html&linkname=Calendar%20support%20with%20Drools> "Email")