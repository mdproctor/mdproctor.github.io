---
layout: post
title: "Working with JBoss Rules and Web Services"
date: 2007-05-23
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/working-with-jboss-rules-and-web-services.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Working with JBoss Rules and Web Services](<https://blog.kie.org/2007/05/working-with-jboss-rules-and-web-services.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- May 23, 2007  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

I’ve recently just done a project where JBoss Rules was used via web services. So thought I’d detail parts of what I did.

With this particular project only the root object from the payload was asserted, the payload was not split into smaller relational objects and asserted, which is generally considered best practice; however we do show you here how to effectively work with nested XML payloads using ‘from’.

The steps I undertook can roughly be defined as:

  1. Create an XSD for your model.
  2. Generate the classes using JAXB’s XJC, command line seems to have less issues.
  3. Unmarshal in your XML payload and assert the root object.
  4. Use from in your rules for model navitation.
  5. Retrieve the modified model and marshal.

Create an XSD for your model  
First you need an XSD that describes your mode, this will look something like this:
[code]
    <?xml version="1.0" encoding="UTF-8"?>  
     <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns="creditscore" targetNamespace="creditscore">  
       <xs:complexType name="root">  
         <xs:sequence>  
           <xs:element name="division" type="xs:string"/>  
           <xs:element name="occupancy" type="xs:string"/>  
           <xs:element name="occupancyAdjustment" type="xs:double"/>  
           <xs:element name="creditScore" type="CreditScore" minOccurs="0"/>         
         </xs:sequence>  
       </xs:complexType>  
      
     <xs:complexType name="CreditScore">  
       <xs:sequence>  
         <xs:element name="programGroup" type="xs:string"/>  
         <xs:element name="lienType" type="xs:string"/>  
         <xs:element name="division" type="xs:string"/>  
         <xs:element name="score" type="xs:double"/>  
       </xs:sequence>  
     </xs:complexType>  
      
     <xs:element name="Root" type="root"/>  
    </xs:schema>
[/code]

Generate the classes using JAXB’s XJC  
The pojo model can now be created using JAXB’s XJC. Get the latest JAXB reference implementation from sun, https://jaxb.dev.java.net/, I used jaxb 2.1.3. And execute the following from the command line:
[code]
    jaxb-ri-20070413binxjc -p org.domain -d c:folder MyModel.xsd
[/code]

This creates three objects, the ObjectFactory plus the two classes that represent Root and CreditScore, which look like this:
[code]
    @XmlAccessorType(XmlAccessType.FIELD)  
    @XmlType(name = "root", propOrder = {"division", "occupancy", "occupancyAdjustment", "creditScore1", "creditScore2"})  
    public class Root {  
    @XmlElement(required = true)  
    protected String            division;  
    @XmlElement(required = true)  
    protected String            occupancy;  
    protected double            occupancyAdjustment;  
    protected CreditScore       creditScore1;  
    protected List creditScore2;  
      
    public String getDivision() {  
       return division;  
    }  
      
    public void setDivision(String value) {  
       this.division = value;  
    }  
      
    public String getOccupancy() {  
       return occupancy;  
    }  
      
    public void setOccupancy(String value) {  
       this.occupancy = value;  
    }  
      
    public double getOccupancyAdjustment() {  
       return occupancyAdjustment;  
    }  
      
    public void setOccupancyAdjustment(double value) {  
       this.occupancyAdjustment = value;  
    }  
      
    public CreditScore getCreditScore1() {  
       return creditScore1;  
    }  
      
    public void setCreditScore1(CreditScore value) {  
       this.creditScore1 = value;  
    }  
      
    public List getCreditScore2() {  
       if ( creditScore2 == null ) {  
           creditScore2 = new ArrayList();  
       }  
       return this.creditScore2;  
    }  
    }
[/code]
[code]
    @XmlAccessorType(XmlAccessType.FIELD)  
    @XmlType(name = "CreditScore", propOrder = {"programGroup", "lienType", "division", "score"})  
    public class CreditScore {  
      
    @XmlElement(required = true)  
    protected String programGroup;  
    @XmlElement(required = true)  
    protected String lienType;  
    @XmlElement(required = true)  
    protected String division;  
    protected double score;  
      
    public String getProgramGroup() {  
       return programGroup;  
    }  
      
    public void setProgramGroup(String value) {  
       this.programGroup = value;  
    }  
      
    public String getLienType() {  
       return lienType;  
    }  
      
    public void setLienType(String value) {  
       this.lienType = value;  
    }  
      
    public String getDivision() {  
       return division;  
    }  
      
    public void setDivision(String value) {  
       this.division = value;  
    }  
      
    public double getScore() {  
       return score;  
    }  
      
    public void setScore(double value) {  
       this.score = value;  
    }  
    }
[/code]

Unmarshal in your XML payload and assert the root object  
You can now use JAXB to unmarshal your XML payloads, this example just takes the payload from disk:
[code]
    JAXBContextImpl jc = (JAXBContextImpl) JAXBContext.newInstance( "org.domain" );  
    Unmarshaller unmarshaller = jc.createUnmarshaller();  
    JAXBElement element = ( JAXBElement ) unmarshaller.unmarshal( new File( XML_FILE ) );  
    Root root = ( Root ) element.getValue();
[/code]

Use from in your rules for model navitation  
‘from’ is a new element in JBoss Rules 4.0 that allows a rule to localy reason over data not asserted into the working memory. We can use ‘from’ to navigate to sub objects in the model.
[code]
    package creditscore  
      
    import creditscore.CreditScore  
      
    rule "Credit_Score_Adjustments_0"  
       dialect "mvel"  
       no-loop true  
    when  
       r : Root( division=="wholesale",  
                 occupancy=="Investors" )  
       cs : CreditScore( programGroup=="ACMEPowerBuyerGroup",  
                        lienType=="FIRST_TD; SECOND_TD",  
                        division=="Wholesale",  
                        score >= 500,  
                        score then  
       cs.score = cs.score + 1;  
       modify(cs);  
    end
[/code]

Retrieve the modified model and marshal
[code]
     RuleBase ruleBase = RuleBaseFactory.newRuleBase();  
     ruleBase.addPackage( pkg );        
      
     StatelessSession session = ruleBase.newStatelessSession();  
          
     StatelessSessionResult results = session.executeWithResults( new Object[] { root }  );        
      
     Root returnedRoot = ( Root ) results.iterateObjects().next();  
     Marshaller marshaller = jc.createMarshaller();          
     marshaller.marshal( new JAXBElement( new QName("org.domain", "Root"), returnedRoot.getClass(), returnedRoot ), System.out );  
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fworking-with-jboss-rules-and-web-services.html&linkname=Working%20with%20JBoss%20Rules%20and%20Web%20Services> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fworking-with-jboss-rules-and-web-services.html&linkname=Working%20with%20JBoss%20Rules%20and%20Web%20Services> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fworking-with-jboss-rules-and-web-services.html&linkname=Working%20with%20JBoss%20Rules%20and%20Web%20Services> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fworking-with-jboss-rules-and-web-services.html&linkname=Working%20with%20JBoss%20Rules%20and%20Web%20Services> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fworking-with-jboss-rules-and-web-services.html&linkname=Working%20with%20JBoss%20Rules%20and%20Web%20Services> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fworking-with-jboss-rules-and-web-services.html&linkname=Working%20with%20JBoss%20Rules%20and%20Web%20Services> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2007%2F05%2Fworking-with-jboss-rules-and-web-services.html&linkname=Working%20with%20JBoss%20Rules%20and%20Web%20Services> "Email")