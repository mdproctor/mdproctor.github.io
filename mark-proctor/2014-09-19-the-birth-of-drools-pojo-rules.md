---
layout: post
title: "The Birth of Drools Pojo Rules"
date: 2014-09-19
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/09/the-birth-of-drools-pojo-rules.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [The Birth of Drools Pojo Rules](<https://blog.kie.org/2014/09/the-birth-of-drools-pojo-rules.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- September 19, 2014  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

A few weeks back I blogged about our plans for a clean low level executable mode, you can read about that [here](<http://blog.athico.com/2014/07/drools-executable-model.html>).

We now have our first rules working, and you can find the project with unit tests [here](<https://github.com/mariofusco/drools-pojorule>). None of this requires drools-compiler any more, and allows people to write DSLs without ever going through DRL and heavy compilation stages.

It’s far off our eventually plans for the executable model, but it’s a good start that fits our existing problem domain. Here is a code snippet from the example in the project above, it uses the classic Fire Alarm example from the documentation.

We plan to build Scala and Clojure DSLs in the near future too, using the same technique as below.
[code]
    public static class WhenThereIsAFireTurnOnTheSprinkler {
        Variable<Fire> fire = any(Fire.class);
        Variable<Sprinkler> sprinkler = any(Sprinkler.class);
        Object when = when(
                input(fire),
                input(sprinkler),
                expr(sprinkler, s -> !s.isOn()),
                expr(sprinkler, fire, (s, f) -> s.getRoom().equals(f.getRoom()))
        );
        public void then(Drools drools, Sprinkler sprinkler) {
            System.out.println("Turn on the sprinkler for room " + sprinkler.getRoom().getName());
            sprinkler.setOn(true);
            drools.update(sprinkler);
        }
    }
    public static class WhenTheFireIsGoneTurnOffTheSprinkler {
        Variable<Fire> fire = any(Fire.class);
        Variable<Sprinkler> sprinkler = any(Sprinkler.class);
        Object when = when(
                input(sprinkler),
                expr(sprinkler, Sprinkler::isOn),
                input(fire),
                not(fire, sprinkler, (f, s) -> f.getRoom().equals(s.getRoom()))
        );
        public void then(Drools drools, Sprinkler sprinkler) {
            System.out.println("Turn off the sprinkler for room " + sprinkler.getRoom().getName());
            sprinkler.setOn(false);
            drools.update(sprinkler);
        }
    }
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F09%2Fthe-birth-of-drools-pojo-rules.html&linkname=The%20Birth%20of%20Drools%20Pojo%20Rules> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F09%2Fthe-birth-of-drools-pojo-rules.html&linkname=The%20Birth%20of%20Drools%20Pojo%20Rules> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F09%2Fthe-birth-of-drools-pojo-rules.html&linkname=The%20Birth%20of%20Drools%20Pojo%20Rules> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F09%2Fthe-birth-of-drools-pojo-rules.html&linkname=The%20Birth%20of%20Drools%20Pojo%20Rules> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F09%2Fthe-birth-of-drools-pojo-rules.html&linkname=The%20Birth%20of%20Drools%20Pojo%20Rules> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F09%2Fthe-birth-of-drools-pojo-rules.html&linkname=The%20Birth%20of%20Drools%20Pojo%20Rules> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F09%2Fthe-birth-of-drools-pojo-rules.html&linkname=The%20Birth%20of%20Drools%20Pojo%20Rules> "Email")
  *[]: 2010-05-25T16:11:00+02:00