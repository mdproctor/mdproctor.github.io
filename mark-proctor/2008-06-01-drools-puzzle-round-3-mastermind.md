---
layout: post
title: "Drools Puzzle Round 3: Mastermind"
date: 2008-06-01
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/06/drools-puzzle-round-3-mastermind.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Puzzle Round 3: Mastermind](<https://blog.kie.org/2008/06/drools-puzzle-round-3-mastermind.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 1, 2008  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Important: [Participation Rules](<http://blog.athico.com/2007/08/drools-puzzles.html>). The rules are updated. Links to past puzzles and result reports can be found at the end of that entry.

Difficulty of this round: middle++

Submission deadline: August 16th, 2008 (since there hasn’t been any submission for this puzzle till August 16th, the deadline is now October 16th, 2008. The T-shirts as prizes will have the new Drools logo printed on them. Added on October 15th: there still isn’t any submission yet…is this puzzle really that difficult? The new deadline is now December 16th. )  
Submission email: **droolspuzzle@gmail.com**

This time we’d like to see implementation of the codebreaker for a variation of the classic game “[Mastermind](<http://en.wikipedia.org/wiki/Mastermind_%28board_game%29>)“.

Please refer to the [wikipedia Mastermind page](<http://www.blogger.com/Please%20refer%20to%20the%20wikipedia%20Mastermind%20page%20for%20the%20basic%20rules%20for>) for the game’s basic rules. Our variation employs 12 different colors and 8 code slots. The [CodeMaker.java](<http://www.ningning.org/droolspuzzles/mastermind/CodeMaker.java>) is provided [here](<http://www.ningning.org/droolspuzzles/mastermind/CodeMaker.java>). Participators must use this class as codemaker. The inline documentation of this class explains the judging rules in detail. The main method in the CodeMaker.java demonstrates how to call the code getter and how to use the answer judge.

Participators are required to write the codebreaker part of the mastermind application. Maximal trials is not specified in our codemaker, your should design a strategy which can minimize the number of trials.

Your test code should break 1000 different codes and output

  * the number of average trials for breaking a code,
  * the average time used for breaking a code

Something looks like this:  

[code]
    long totalTrials = 0;  
    long startTime = System.currentTimeMillis();  
      
    for (int i = 0; i  1000, i++){  
    CodeMaker maker = new CodeMaker();  
    CodePeg[] code = maker.getCode();  
      
    // call your code breaker routine here  
    //...  
    }  
    long endTime = System.currentTimeMillis();  
      
    System.out.println("Average trials per code-breaking: " + totalTrials/1000);  
    System.out.println("Average time per code-breaking: " + (endTime - startTime) / 1000 + " ms");  
    
[/code]

Your code should be reasonably packaged and documented. Please by all means document your strategy as comprehensible as necessary.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-puzzle-round-3-mastermind.html&linkname=Drools%20Puzzle%20Round%203%3A%20Mastermind> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-puzzle-round-3-mastermind.html&linkname=Drools%20Puzzle%20Round%203%3A%20Mastermind> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-puzzle-round-3-mastermind.html&linkname=Drools%20Puzzle%20Round%203%3A%20Mastermind> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-puzzle-round-3-mastermind.html&linkname=Drools%20Puzzle%20Round%203%3A%20Mastermind> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-puzzle-round-3-mastermind.html&linkname=Drools%20Puzzle%20Round%203%3A%20Mastermind> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-puzzle-round-3-mastermind.html&linkname=Drools%20Puzzle%20Round%203%3A%20Mastermind> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2008%2F06%2Fdrools-puzzle-round-3-mastermind.html&linkname=Drools%20Puzzle%20Round%203%3A%20Mastermind> "Email")