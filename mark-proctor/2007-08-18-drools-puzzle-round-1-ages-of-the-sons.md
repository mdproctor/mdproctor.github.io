---
layout: post
title: "Drools Puzzle Round 1: Ages of the Sons"
date: 2007-08-18
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/08/drools-puzzle-round-1-ages-of-the-sons.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Drools Puzzle Round 1: Ages of the Sons](<https://blog.kie.org/2007/08/drools-puzzle-round-1-ages-of-the-sons.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- August 18, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

**Start date** : August 1st, 2008. **Submission deadline** : August 15th, 2008.

Please post your solution to: **droolspuzzle@gmail.com  
**

[Participation Rules](<http://blog.athico.com/2007/08/drools-puzzles.html>)

** _Ages of the Sons_**

**Difficulty level** : settler

An old man asked a mathematician to guess the ages of his three sons.

Old man said: “The product of their ages is 36.”  
Mathematician said: “I need more information.”

Old man said:”Over there you can see a building. The sum of their ages  
equals the number of the windows in that building.”  
After a short while the mathematician said: “I need more information.”

Old man said: “The oldest son has blue eyes.”  
Mathematician said: “I got it.”

What are the ages of the three sons of the old man?

Result Report

The rule in the first sentence of the old man is obvious. The mathematician cannot decide the solution after he was told the second condition. This indicates that there are more than one triple of numbers whose products are 36 and sums are the same. The third condition tells that the greatest number in the triple has only one occurrence. So there is nothing really fancy in the rule definition files.

The solution space of this puzzle is so tiny that the brute force search is good enough. Indeed, all participators implemented brute force search for this puzzle. Very interestingly there are three slightly different variants of this brute force search in the submissions.

This time we got totally five solutions from 4 participators. The [first correct solution](<http://www.ningning.org/droolspuzzles/ChrisBarham/SonsAgesPuzzle.jar>) was from Chris Barham. Chris showed very good discipline on software engineering in his submission. The program files are well packaged and the readme file is concise and clear. I strongly suggest every participator in the future take a look at this solution from Chris and package her programs similarly. His readme file is a perfect example, future participators can use it as a template. The ThreeSons.java in his solution is in fact a solution object. This class adds more structure to the algorithm. This class can be generalized to a “Solution” object and be used in any back tracking solvers. It is a little bit closer to the [“Taseree”](<http://blog.athico.com/search/label/search%20space>) approach.
[code]
    1  
    2  
    3  
    4  
    5  
    6  
    7  
    8  
    
[/code]

| 
[code]
    private static void assertAllFacts(WorkingMemory workingMemory) {  
          for (int i = 1; i 3; i++) {  
              for (int j = 1; j 36; j++) {  
                  Son son = new Son((char)(i + 64), j);  
                  workingMemory.insert(son);  
              }  
          }  
      }
[/code]  
  
---|---  
  
This is plain brute force without any pre-filtering in the main class.

We received the [second correct solution](<http://www.ningning.org/droolspuzzles/ElmoNazareno/AgesOfSons/>) from Elmo Nazareno. His [rules definition](<http://www.ningning.org/droolspuzzles/ElmoNazareno/AgesOfSons/finage.drl>) is the most concise and clear one among the all submissions. This rules definition file is an excellent example of concise, clear and correct rules. In addition, there is some smart pre-filering prior to the working memory insertion in his Main.java:
[code]
    1  
    2  
    3  
    4  
    
[/code]

| 
[code]
    for (int i = 1; i 36; i++) {  
          // this is just to limit the number of assertions  
          if ((36 % i) == 0) workingMemory.insert(new Son(i));  
        }
[/code]  
  
---|---  
  
This pre-filtering is without loss of correctness.

The [third and fourth solution](<http://www.ningning.org/droolspuzzles/GernotStarke/AgesOfSons/>) were from Dr. Gernot Starke. Gernot’s code has excellent inline documentation. This is a good example how readable code should look like. He also did a pre-filtering prior to the working memory insertion:
[code]
    1  
    2  
    3  
    
[/code]

| 
[code]
    int i;  
      for (i = 0; i 19; i++)  
        session.insert(new Son(i));
[/code]  
  
---|---  
  
However there is a correctness problem with this filtering rule. The solution candidate “36, 1, 1″ is missing in the search space. Although the program finally gives out the right answer to this puzzle: 9 years old, 2 years old, 2 years old, the logic in the main class is not really correct. And so is the prolog solution since the prolog program also does not search up to 36 years old ;-).

So far, Chris’ solution has the best packaging the readme, and most sophisticated structure of the algorithm, Elmo’s solution has the best pre-filtering rule, Gernot’s solution has the best documentation and most efficient testing code in the main class (not counting the problematic pre-filtering logic). Elmo’s and Gernot’s rules definition files are essentially the same.

Now the performance.

**Testing environment:**

  * Hardware: AMD Athlon 64 bit Dual Core 4200+; 2GB memory.
  * Software: Debian Lenny for AMD 64 bit multi core. Java 1.6.0 b105 Sun HotSpot VM. Drools 4.0.0 snapshot from CVS 2007-08-03. Eclipse core_3.3.0.v_771 for rules compilation.

All the valid solutions are edited slightly for testing purpose. Please pay attention to the main classes. Participators in the future should write performance measurement code following this template (based on Gernot’s solution):
[code]
    1  
    2  
    3  
    4  
    5  
    6  
    7  
    8  
    9  
    10  
    11  
    12  
    13  
    14  
    15  
    16  
    17  
    18  
    19  
    20  
    21  
    22  
    23  
    24  
    25  
    26  
    27  
    28  
    29  
    30  
    31  
    
[/code]

| 
[code]
    ...  
      // timer  
      final long setupBegin = System.currentTimeMillis();  
      
      final PackageBuilder builder = new PackageBuilder();  
      builder.addPackageFromDrl(new InputStreamReader(  
          AgeOfTheSonsRiddle.class  
              .getResourceAsStream("/your-rules-definition.drl")));  
      
      final RuleBase ruleBase = RuleBaseFactory.newRuleBase();  
      ruleBase.addPackage(builder.getPackage());  
      
      final StatefulSession session = ruleBase.newStatefulSession();  
      
      final long insertionBegin = System.currentTimeMillis();  
      
      // int i;  
      //for (i = 0; i   
      //  session.insert(new Son(i));  
      
      session.fireAllRules();    
      final long end = System.currentTimeMillis();  
      session.dispose();  
      
      long setupTime = insertionBegin - setupBegin;  
      long problemSolvingTime = end - insertionBegin;  
      long totalTime = end - setupBegin;  
      
      System.out.print("Setting up the rule base took: " + setupTime + " ms");  
      System.out.println("Finding the solution took " + problemSolvingTime + " ms");  
      System.out.println("Total run time: " + totalTime + " ms");
[/code]  
  
---|---  
  
Elmo wanted to use Janino compiler in his code but I edited his main class slightly to make the evaluation fair for all participators. Participators in the future please do not specify the compiler for your rules. All solutions will use the same rule compiler in evaluator’s machine.

I gave each submission 5 runs and took the best result of the five. So here is the best run-time result of three participators (setup time, problem-solving time):

  * Chris Barham: 2330 ms, 195 ms
  * Elmo Nazareno: 2345 ms, 215 ms
  * Gernot Starke: 2367ms, 134 ms

This time I ingored the RuleBase setup and initialization time, only took problem-solving time into account. It’s clear who’s the performance winner. ![:-\)](/legacy/assets/images/2007/08/5f5239a67e6b-icon_smile.gif)

Now comes the final scoring. Each submission is scored with respect to correctness, performance, testability, code quality, documentation quality (be it inline or separated), packaging quality and user interface quality. Each aspect (except performance) has possible scores from 1 to 5. 5 means excellent, 4 means good, 3 means so so, 2 means questionable, 1 means problematic. The performance score is calculated with this rule: The best one gets 10 points. Let’s call the time used Tb. Formula for calculating other people’s performance scores:

PerformanceScore_i = 10 / (Ti / Tb), with Ti meaning a time used of a submission.

Final scores:

Participator| Correctness| Performance| Testability| Code Q.| Docu. Q.| Packaging Q.| UI Q.| Total  
---|---|---|---|---|---|---|---|---  
Chris Barham| 5| 6.87| 5| 5| 5| 5| 4| 35.87  
Elmo Nazareno| 5| 6.23| 5| 5| 4| 3| 4| 32.23  
Gernot Starke| 4| 10| 5| 5| 5| 3| 4| 36.0  
  
Both Elmo and Gernot pasted their code in the email body that’s why each of them got 2 points away from the packaging quality. ![;\)](/legacy/assets/images/2007/08/1fb1f5499594-icon_wink.gif)

Congratulations to Dr. Starke and let’s wait for the puzzle from him for next round. ![;-\)](/legacy/assets/images/2007/08/1fb1f5499594-icon_wink.gif) Since he himself cannot compete in the next round, he will get the average score of next round to make things fair.

Happy Drooling!

PS: Dr. Dirk Farin also submitted [a solution](<http://ningning.org/droolspuzzles/DirkFarin/AgesOfSons/>) but was not eligible to official evaluation since his code is in C++. The unfortunate fact to all Droolers is, Dirk’s C++ program, which also used plain brute force without any pre-optimization, took only less than 3 ms from initialization to finish.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F08%2Fdrools-puzzle-round-1-ages-of-the-sons.html&linkname=Drools%20Puzzle%20Round%201%3A%20Ages%20of%20the%20Sons> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F08%2Fdrools-puzzle-round-1-ages-of-the-sons.html&linkname=Drools%20Puzzle%20Round%201%3A%20Ages%20of%20the%20Sons> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F08%2Fdrools-puzzle-round-1-ages-of-the-sons.html&linkname=Drools%20Puzzle%20Round%201%3A%20Ages%20of%20the%20Sons> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F08%2Fdrools-puzzle-round-1-ages-of-the-sons.html&linkname=Drools%20Puzzle%20Round%201%3A%20Ages%20of%20the%20Sons> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F08%2Fdrools-puzzle-round-1-ages-of-the-sons.html&linkname=Drools%20Puzzle%20Round%201%3A%20Ages%20of%20the%20Sons> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F08%2Fdrools-puzzle-round-1-ages-of-the-sons.html&linkname=Drools%20Puzzle%20Round%201%3A%20Ages%20of%20the%20Sons> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F08%2Fdrools-puzzle-round-1-ages-of-the-sons.html&linkname=Drools%20Puzzle%20Round%201%3A%20Ages%20of%20the%20Sons> "Email")