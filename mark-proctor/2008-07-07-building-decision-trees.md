---
layout: post
title: "Building Decision Trees"
date: 2008-07-07
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/07/building-decision-trees.html
---

The simplest approach is building a single decision tree from the data set. However, this approach is not very powerful when the classification problem gets harder.  

Bagging: Boostrap Aggregating

Given a set of N instances, each belonging to one of K classes here is the outline of the algorithm used to construct a decision tree forest:

For each decision tree

Draw a random sample of size N from the learning set with replacement (boostrapping)

Build the decision tree using the random sample

Output: The class labels with the maximum number of votes for each instance (a tree’s vote is its prediction for an instance)

Boosting: AdaBoost

Instead of drawing boostrap samples from the original data set boosting maintains weight for each instance. The higher the weight of the instance is, the more the instance influences the decision tree being trained. At each trial (each decision tree) the weights are adjusted in a way that the weight of the misclassified instances is increased. The final classifier aggregates the learned decision trees like the bagging but each decision tree’s vote is a function of its accuracy.

Classification Performance

I tried different data sets:

  * Poker Hand: 25010 instances with 10 attributes (5 literal and 5 integer = 5 Categorical and 5 Quantitative), Literal target attribute (10 possible values)
  * Triangle: 10000 instances with 3 attributes (3 double = 3 Quantitative) and a Boolean target function. The target function is to label the object if it is a valid triangle checking the length of 3 edges

(z < x + y) && (x < z + y) && (y < x + z)

So far bagging and boosting provide some interesting advantages from machine learning point of view. Let’s look at some classification results:

Using Single C4.5 decision tree

  * Poker hands: 10.96% classification error
  * Triangle: 19.23% classification

Bagging C4.5 Decision Trees

  * Poker hands: 8.9% classification error
  * Triangle: 19.19% classification

Boosting C4.5 Decision Trees

  * Poker hands: 0.0% classification error
  * Triangle: 8.61% classification

Boosting definetely improves the classification performance. But it is harder to say the same for bagging. Even if bagging improves the classification performance a little in the Poker hands example it does not make the same effect with the Triangle example. As we can see boosting the decision trees can produce perfect classification on the data set.