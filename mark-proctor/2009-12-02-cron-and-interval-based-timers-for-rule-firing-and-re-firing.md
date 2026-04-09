---
layout: post
title: "Cron and Interval based timers for rule firing and re-firing"
date: 2009-12-02
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/12/cron-and-interval-based-timers-for-rule-firing-and-re-firing.html
---

At ORF I did a presentation on ideas I’d like to do to improve our language. You can see that presentation here:  
[“Drools “Where do we go from here” – presented at ORF09″](<http://blog.athico.com/2009/10/drools-where-do-we-go-from-here-orf09.html>)

In this presentation I discussed the idea of [“cron”](<http://en.wikipedia.org/wiki/Cron>) based rules. Drools has supported the “duration” attribute for a long time now. When a rule is activated it does not fire straight away, instead it is scheduled to fire based on the given duration. If the rule is still true on or after that duration lapses it fires, otherwise if it becomes false before the duration lapses it is cancelled and unscheduled.

The problem here is the duration is a single value and the rule fires just once. This is useful, but somewhat limited. Instead wouldn’t it better if we could support various time based semantics for rule firing and re-firing (if the rule is still true).

While not exposed to the user I created pluggable Time semantics. This introduces the Timer interface:

```text
interface Timer {
    /**
     * Creates a Trigger for this Timer, based on the provided current timestamp.
     */
    Trigger createTrigger(long timestamp);
}
```

The Trigger interface already existed as part of our unified clock and scheduling framework in Drools. Trigger tells the scheduler the next date to trigger the current job on. If we have multiple Timer semantics, not just duration, each Timer must be responsible for providing it’s own Trigger to handle the execution of those semantics.

The ‘duration’ keyword has now been renamed to ‘timer’, although backwards compatability has been kept. We now support two different timers ‘cron’ and ‘interval’. The ‘timer’ keyword takes a colon delimited prefix, using ‘cron:’ and ‘int:’ respectively. If no protocol is given, it assumes ‘int’.

We use the standard cron syntax (thank you quartz), with added support for seconds. And interval has two parameters and obeys the JDK Timer semantics of delay and period. Where delay is the initial delay and period is the period of time between each iteration.

So now we can do the following which will send an SMS to a give mobile number every 0, 15, 30 and 45 minutes past each hour, while the alarm remains true:

```drl
rule "Send SMS every 15 minutes"
timer (cron:* 0/15 * * * ?)
when
$a : Alarm( on == true )
then
exitPoint[ "sms" ].insert( new Sms( $a.mobileNumber, "The alarm is still on" );
end
```