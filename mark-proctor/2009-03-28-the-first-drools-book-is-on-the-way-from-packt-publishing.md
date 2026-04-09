---
layout: post
title: "The first Drools book is on the way from Packt Publishing"
date: 2009-03-28
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/03/the-first-drools-book-is-on-the-way-from-packt-publishing.html
---

The first Drools book is on the way from Packt Publishing:  
JBoss Drools Business Rules  
<http://www.packtpub.com/jboss-drools-business-rules/book>

The author of the book is Paul Brown who many of you will know from the mailing list and his O’Reilly articles:  
[Using Drools in Your Enterprise Java Application](<http://www.onjava.com/pub/a/onjava/2005/08/24/drools.html>)  
[Give Your Business Logic a Framework with Drools](<http://www.onjava.com/pub/a/onjava/2005/08/03/drools.html>)

Here is copy/paste from the website for the chapter outlines:

What you will learn from this book

  * Understand the basics of business rules and JBoss rules with minimal effort
  * Install the required software easily and learn to use the Guvnor, which is a user-friendly web editor that’s also powerful enough to test our rules as we write them
  * Learn to write sophisticated rules and import the fact model into the Guvnor and then build a guided rule around it, which makes your web pages a lot clearer
  * Gain complete knowledge of what we can do with the Guvnor rule editor, and then use the JBoss IDE as an even more powerful way of writing rules, and automate processes for discounts, orders, sales, and more
  * Know the structure of the rule file through the example of a shipping schedule, which will help you with your own shipping schedule
  * Test your rules not only in the Guvnor, but also using FIT for rule testing against requirements documents; run unit tests using JUnit for error-free rules and interruption-free services
  * Specifically, non-developers can work with Excel spreadsheets as a fact model to develop business processes without learning any other new technology
  * Work with DSLs (Domain-Specific Languages) and rule flow to make writing rules easy; which makes staff training quicker and your working life easier
  * Deploy your business rules to the real world, which completes your project successfully, and combine this into a web project using the framework of your choice to provide better services
  * Benefit from concepts such as truth maintenance, conflict resolution, pattern matching rules agenda, and the Rete algorithm to provide advanced and faster business systems so that staff efficiency is maximized

Chapter 1, Drooling over JBoss Rules. This chapter gives you a good platform to understand business rules and JBoss rules. We look at the problems that you might have (and why you’re probably reading this book). We look at what business rule engines are, and how they evaluate business rules that appear very simple and how they become powerful when multiple rules are combined.

Chapter 2, Getting the software, deals with installation. This chapter explains setting up Java, setting up Business Rule Management System (BRMS)/Guvnor running on the JBoss App Server, setting up Eclipse, and installing the Drools Plug-in. It also details the installation of the Drools examples for this book and the Maven to build them.

Chapter 3, Meet the Guvnor, deals with writing our rules using the ‘Guvnor’. Guvnor is the user-friendly web editor that’s also powerful enough to test our rules as we write them. We take up an example to make things easier. Then we look at the various Guvnor screens, and see that it can not only write rules (using both guided and advanced editors), but that it can also organize rules and other assets in packages, and also allow us to test and deploy those packages. Finally, we write our very first business rule—the traditional ‘Hello World’ message announcing to everyone that we are now business rule authors.

Chapter 4, Guided Rules with the Guvnor. This chapter shows how to use the Guvnor rule editor to write some more sophisticated rules. It also shows how to get information in and out of our rules, and demonstrates how to create the fact model needed to do this. We import our new fact model into the Guvnor and then build a guided rule around it. Finally we test our rule as a way of making sure that it runs correctly.

Chapter 5, From Guvnor to JBoss IDE. This chapter pushes the boundries of what we can do with the Guvnor rule editor, and then brings in the JBoss IDE as an even more powerful way of writing rules. We start by using variables in our rules example. Then we discuss rule attributes (such as salience) to stop our rules from making changes that cause them to fi re again and again. After testing this successfully, we look at text-based rules, in both the Guvnor and the JBoss IDE, for running ‘Hello World’ in the new environment.

Chapter 6, More Rules in the jBoss IDE. This chapter looks again at the structure of a rule fi le. At the end of this chapter, we look at some more advanced rules that we can write and run in the IDE.

Chapter 7, Testing your Rules. This chapter explains how testing is not a standalone activity, but part of an ongoing cycle. In this chapter we see how to test our rules, not only in the Guvnor, but also using FIT for rule testing against requirements documents. This chapter also explains Unit Testing using JUnit.

Chapter 8, Data in Excel, Rules in Excel. This chapter explains how to use Excel Spreadsheets (cells and ranges) as our fact model to hold information, instead of the write-your-own-JavaBean approach we took earlier. Then we use Excel spreadsheets to hold Decision tables, to make repetitive rules easier to write.

Chapter 9, Domain-Specific Languages [DSL] and rule flow. This chapter aims to make our rules both easier to use, and more powerful. We start with DSLs—Domain-Specifi c Languages. This chapter follows on from the ‘easy to write rules’ theme from the previous chapter and also discusses both ruleflow and workflow. It would be great to draw a workfl ow diagram to see/control what (groups of) rules should fi re and when. Rule flow gives us this sort of control.

Chapter 10, Deploying rules in real life. This chapter shows you how to deploy your business rules into the real world. We look at the pieces that make up an entire web application, and where rules fit into it. We see the various options to deploy rules as part of our application, and the team involved in doing so. Once they are deployed, we look at the code that would load and run the rules—both home-grown and using the standard RuleAgent. Finally we see how to combine this into a web project using the framework of your choice.

Chapter 11, Peeking under the covers. This chapter looks at what happens under the cover by opening up the internals of the Drools rule engine to understand concepts such as truth maintenance, confl ict resolution, pattern matching, and the rules agenda. In this chapter, we explore the Rete algorithm and discuss why it makes rules run faster than most comparable business logic. Finally we see the working memory audit log and the rules debug capabilities of the Drools IDE.

Chapter 12, Other Drools features. This chapter deals with the other advanced Drools features that have not yet been covered. This includes Smooks to bulk load data, Complex Event Processing, and Drools solver to provide solutions where traditional techniques would take too long.

Approach This book takes a practical approach, with step-by-step instructions. It doesn't hesitate to talk about the technologies, but takes time to explain them (to an Excel power-user level). There is a good use of graphics and code where necessary. Who this book is written forIf you are a business analyst – somebody involved with enterprise IT but at a high level, understanding problems and planning solutions, rather than coding in-depth implementations – then this book is for you.  
  
If you are a business user who needs to write rules, or a technical person who needs to support rules, this book is for you.  
  
If you are looking for an introduction to rule engine technology, this book will satisfy your needs.  
  
If you are a business user and want to write rules using Guvnor/JBoss IDE, this book will be suitable for you.  
  
This book will also suit your need if you are a business user and want to understand what Drools can do and how it works, but would rather leave the implementation to a developer.