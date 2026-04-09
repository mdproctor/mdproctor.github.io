---
layout: post
title: "Zementis Drools Case Study"
date: 2008-02-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/02/zementis-drools-case-study.html
---

Here at Zementis we have developed a decision engine called ADAPA – Adaptive Decision and Predictive Analytics (http://zementis.com/products.htm) that offers at its core batch and real-time scoring of predictive models as well as fast execution of business rules. As you readers might have guessed, the rules engine is Drools. 

I will briefly sketch the core philosophy behind the our decision engine and then detail the successful implementation of Drools in ADAPA and how Drools has been an integral part of helping us gain a strong foothold in the analytics market.

The key idea behind our decision engine has always been to integrate two philosophies: Rules-based systems (explicit knowledge) and predictive models (implicit, data-driven algorithms). We believe that in order to have a complete, “intelligent” decision engine, it should not be limited to either rules or predictive models. Hence in ADAPA, rules and predictive models can be combined with great ease to create a complex decision model.

The resulting ADAPA decision engine has been used successfully to deliver intelligent systems to the financial industry. Typically, the financial industry relies heavily on rules-based systems for making decisions on credit applications. We, on the other hand, have implemented systems that not only use conventional business rules but also calculate a custom risk score as part of the decision process. The process in a nutshell: Upon matching of appropriate facts, a rule would fire which would in turn call the appropriate predictive model, and after the predictive model returns a risk score, that number would further be used in other rules to get the correct decision.

The key points about the Drools rule engine that we want to emphasize are:

  * Drools is extremely reliable: Over the past years, we have successfully used multiple versions of Drools for complex, mission-critical deployments.

  * Drools is scalable: The rules aspect of our system has supported several thousand rules and hundreds of users while delivering sub-second response times for AJAX-based user interfaces and web services.

  * Drools is fast: The great thing about Drools that the clients immediately noticed was the speed of execution. The Drools rule engine would return a decision on complex loan applications so fast that we had clients ask: “How can it be so fast?”

  * Usability: We authored all rules using the Excel based decision table approach. This approach worked better for our user base over writing drl files since it enabled, e.g., a mortgage lender to make changes to rules on a regular basis without needing dedicated IT staff. We would initially create all appropriate Excel files and then let them enter data to reflect their mortgage guidelines. Hence having the ability to generate rules through Excel, versus only being able to write ‘drl’ files gave us a strategic advantage in usability. 

Thank you Drools team!