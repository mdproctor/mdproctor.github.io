---
layout: post
title: "Production Rules implementation for the Rule Interchange Format and The Mortgage Industry Standards Maintenance Organization"
date: 2007-06-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/06/production-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Production Rules implementation for the Rule Interchange Format and The Mortgage Industry Standards Maintenance Organization](<https://blog.kie.org/2007/06/production-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- June 20, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

(Guest Writer : Tracy Bost from valocity.com)

The [Mortgage Industry Standards Maintenance Organization (MISMO)](<http://mismo.org/>) is a subsidiary of the Mortgage Banker’s Association and acts as the mortgage industry’s standards body for electronic standards. Its stated mission is “to develop, promote, and maintain voluntary electronic commerce standards for the mortgage industry”. In June of 2006, MISMO created the Business Rules Exchange Workgroup (BREW) to help organize a standard in the industry for exchanging “business rules” from one trading partner to another. The participants are volunteers from various organizations within the industry. Over the course of a few months, several participants presented use cases that were felt relevant to the workgroup and its mission.

To demonstrate to the industry the possibility of exchanging business rules was in the realm of today’s technical capabilities, and it could help meet real business needs, the group decided to perform a proof-concept (POC).

In order for the POC to be meaningful, the group decided it should be performed using an existing documented use case. Additionally, it was desired the POC should consist of at least two different vendors and platforms to add to the credibility (a reality) of the task.

Of the several use cases discussed, the “pricing rules” use case seemed to be the one most often mentioned since inception of the work group. For that reason, the group agreed to use pricing rules as it first proof-of concept.

Because the group wanted to focus on a simple subset of production rules that contained easy vocabulary references to the MISMO AUS 2.4 version. With this in mind, a subset of 17 pricing rules using a simple look up table were chosen as the actual rules to be exchanged and executed against.  
[![](/legacy/assets/images/2007/06/1b6b7db0c3ef-mismo1.PNG)](<http://bp0.blogger.com/_Jrhwx8X9P7g/RmJGWj7W5FI/AAAAAAAAABs/DgDOAK-M4HQ/s1600-h/mismo1.PNG>)  
Because some of the participates in the MISMO BREW workgroup were active with the W3C Rules Interchange Format (RIF) working group as well, and RIF releasing its first core draft recently, RIF was chosen as the standard language to use for the POC.

Fortunately, after approaching JBoss Rules and ILOG concerning this POC, both agreed to this challenge. Mark covers the actual implementation of it in a previous a blog entry “[W3C Rule Interchange Format for Production Rule Systems](<http://markproctor.blogspot.com/2007/06/w3c-rule-interchange-format-for.html>)”.

## Background on Pricing Rules

Simply put, pricing is the interest rate a borrower will pay on the mortgage loan. Due to the complexity of a mortgage loan, several factors could affect ‘pricing”. Some of these could be the borrower’s FICO score, the type of loan, loan to value percent (LTV), whether the borrower has full stated documents(proof of income) or non-stated.

A lender or broker will typically obtain these pricing rules from a PDF downloaded from the various lenders’ web site or through email. Once the PDF file is retrieved, one can than enter the pricing rules into a business rules management system. It is easy to see this can be a time consuming and error prone process.

Having a standardized way to exchange these rules potentially save the industry millions of dollars in efficiency and effectiveness. Just as important, the customer (borrower) will be able to have a more accurate picture of what the “pricing” for a loan will be in his/her unique circumstance in more real time.

## The Client Tool

My task in this POC was to build a client user interface tool that could act as a “controller” and query a rule producer (or publisher) for its rules, send a ruleset to a consumer, and send XML data to each rule engine’s web service to be executed. ILog would be the producer or publisher or the RIF ruleset, while JBoss Rules would act as the consumer. Using a MISMO compliant data payload of borrower information, the controller was to send the XML data to each ILog and JBoss rule engines for execution and get a returned modified “RequestedInterestRate” value in back, which would in essence, be the borrower’s “pricing”.

ILog came up with “apocrif” for the project name. Therefore, I decided to name my tool “APOCRIF-UI”. Since the core(written by ILog) was in Java, and JBoss Rules is a Java implementation; it only made sense the tool would be written in Java as well. Initially, I had planned on creating a web-based JSP application for this task, but it was quickly discovered a lot of testing would need to be done using the “localhost” or some other server within the tester’s private network. Asking anyone who wanted to use the tool to download and install a web application on their local machine to run it, seems to have defeat the purpose of developing a web application.

Additionally, the tool needed to provide much visual aid to the audience since BREW was planning on demonstrating this to a large crowd geared more to the business aspects of the mortgage industry, than the technicalities of rules and rule languages. A canvas with a drag-n-drop functionality seemed like a good choice for that task as well. It seemed a more traditional desktop or Rich Internet Client would fit the requirements better than a traditional web application.

After a little research, it seemed using the Standard Widget Toolkit (SWT) and deploying it as a Java Web Start application would be a good fit for our scenario. I had used the Kettle Extract, Transform, & Load (ETL) tool in the past and liked very much how the developers architected this program. With Kettle being licensed under the LGPL, I decided to us it as my model for this project.

To help save time for users of the tool, I created a pre-cooked “rules interchange job” (RIJ) and loaded into the working canvas. The RIJ is simply an XML based file containing the vendor connections, and components that are part of the project.

The RIJ had two vendor connections set up, one for the ILOG web service, and another for the JBoss Rules web service.

A component is what I gave the name to the various actions or tasks that could be dragged and dropped on the job canvas (RIJ Designer).

The components loaded onto RIJ Designer were:

  1. Three XML Payloads. These are MISMO compliant (AUS version 2.4 schema) data payloads with sample borrower information. Each file resided on my hard drive and each had different information for three fictitious borrowers.
  2. Four Agent Components. Two components for the ILOG connection (One enabled as a publisher of rules, and the other enabled as an “execution” of rules), and two for the JBoss Rules Connection. (One enabled as a consumer of rules and the other enabled as an execution engine for rules).
  3. The controller. This component (APOCRIF Controller) is what sent requests to the publisher asking for the RIF ruleset, sent the retrieved ruleset to the publisher, and sent various payloads to both rules engines for execution.

Here is a screenshot of the pre-cooked Rules Interchange Job loaded onto the RIJ Designer

[![](/legacy/assets/images/2007/06/d6ed6bb9af6f-mismo1.PNG)](<http://bp3.blogger.com/_Jrhwx8X9P7g/RnlP_iSCx_I/AAAAAAAAACM/MeTRLf5n1uk/s1600-h/mismo1.PNG>)  
To retrieve the ruleset from the ILOG Web service, I right clicked on the controller component, and selected Get? Ruleset. A dialog box appeared. I then provided my own name for the ruleset as “Pricing Rules”. Next I selected from an enabled “publisher” within the job which was the ILog Publisher component. Once it was selected, the client tool understood the vendor ILog‘s web service name “DecisionService”, and the method to retrieve a ruleset as “exportAsRIF”.

This is a screenshot of retrieving a RIF ruleset from the ILog Publisher

[![](/legacy/assets/images/2007/06/800606dffa90-mismo2.PNG)](<http://bp0.blogger.com/_Jrhwx8X9P7g/RnlP_ySCyAI/AAAAAAAAACU/0IidCO3X4lo/s1600-h/mismo2.PNG>)  
Once the ruleset was successfully retrieved, it created a RIF component named “Pricing Rules” on the canvas as part of the job. By clicking on the Transaction History tab, I was able to get a browser view of the returned ruleset and information on the transaction.

This is a screenshot of the transaction history tab view after the RIF ruleset was retrieved from ILog

[![](/legacy/assets/images/2007/06/1a871a2cd12f-mismo3.PNG)](<http://bp0.blogger.com/_Jrhwx8X9P7g/RnlP_ySCyBI/AAAAAAAAACc/CaftPcOLUuQ/s1600-h/mismo3.PNG>)  
Next, I right clicked the controller icon and selected “Send”->Ruleset. A dialog box appeared, and I selected the newly retrieved ruleset on the RIJ Designer. Then from the drop down list of consumers, I selected the JBoss Consumer component. As in the ILog connection, the tool understood what it needed to do in order to interface with the appropriate web service for the JBoss Rules vendor connection. Hence, it automatically provided the “PricingRuleService” as the web service and “updatePricingRules” method.  
  

This is a screenshot of the Pricing Rules ruleset that was sent to the JBoss Consumer

[![](/legacy/assets/images/2007/06/797c412b7a1f-mismo4.PNG)](<http://bp1.blogger.com/_Jrhwx8X9P7g/RnlQACSCyCI/AAAAAAAAACk/y9NcX-w8Ux8/s1600-h/mismo4.PNG>)  
Now that both rules engines had the same set of RIF rules, the fun began. I selected each payload on the job and first sent to ILOG Execution, and then to JBoss Execution and compared the results.  
  

This is a screenshot of the controller preparing to send a XML payload to the JBoss Execution component

[![](/legacy/assets/images/2007/06/83082afc99cb-mismo5.PNG)](<http://bp1.blogger.com/_Jrhwx8X9P7g/RnlQACSCyDI/AAAAAAAAACs/pRJdFvR0RBs/s1600-h/mismo5.PNG>)Both engines returned the same value for the modified element “RequestedInterestRate” For example, the AUSMXARM.xml payload caused each engine to return a value of 15.6% for this value.

This is a screenshot after that particular payload was sent to JBoss Rules.

[![](/legacy/assets/images/2007/06/f35e17d5afe4-mismo6.PNG)](<http://bp0.blogger.com/_Jrhwx8X9P7g/RnlQTySCyEI/AAAAAAAAAC0/jDZ7vlCJQkM/s1600-h/mismo6.PNG>)  
Future demonstrations could include JBoss Rules modifying the ruleset and returning back to ILog for consumption, or round tripping. It is also my understanding JBoss Rules & ILog are in discussions of using a more up to data extension of the RIF core for the next demonstration. Additionally, the upcoming MISMO version 3.0 should allow for a more consistent organization of the vocabulary. This should allow more dynamic references to the data elements within the ruleset.

Nonetheless, I believe this to be the tip of the iceberg of the possibilities that could exist once business rules can be successfully communicated and shared among distributed systems.

Again, thanks to JBoss Rules & ILog for taking an innovative role in this exciting new area of sharing and exchanging business rules.

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fproduction-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html&linkname=Production%20Rules%20implementation%20for%20the%20Rule%20Interchange%20Format%20and%20The%20Mortgage%20Industry%20Standards%20Maintenance%20Organization> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fproduction-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html&linkname=Production%20Rules%20implementation%20for%20the%20Rule%20Interchange%20Format%20and%20The%20Mortgage%20Industry%20Standards%20Maintenance%20Organization> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fproduction-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html&linkname=Production%20Rules%20implementation%20for%20the%20Rule%20Interchange%20Format%20and%20The%20Mortgage%20Industry%20Standards%20Maintenance%20Organization> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fproduction-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html&linkname=Production%20Rules%20implementation%20for%20the%20Rule%20Interchange%20Format%20and%20The%20Mortgage%20Industry%20Standards%20Maintenance%20Organization> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fproduction-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html&linkname=Production%20Rules%20implementation%20for%20the%20Rule%20Interchange%20Format%20and%20The%20Mortgage%20Industry%20Standards%20Maintenance%20Organization> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fproduction-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html&linkname=Production%20Rules%20implementation%20for%20the%20Rule%20Interchange%20Format%20and%20The%20Mortgage%20Industry%20Standards%20Maintenance%20Organization> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F06%2Fproduction-rules-implementation-for-the-rule-interchange-format-and-the-mortgage-industry-standards-maintenance-organization.html&linkname=Production%20Rules%20implementation%20for%20the%20Rule%20Interchange%20Format%20and%20The%20Mortgage%20Industry%20Standards%20Maintenance%20Organization> "Email")