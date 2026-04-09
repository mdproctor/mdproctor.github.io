---
layout: post
title: "Rules-based Validation using Drools, JSR303 and Spring (Patrick van Kann)"
date: 2011-01-13
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2011/01/rules-based-validation-using-drools-jsr303-and-spring-patrick-van-kann.html
---

Original Article(Patrick van Kann)  
<http://nonrepeatable.blogspot.com/2010/11/rules-based-validation-using-drools.html>

## Rules-based Validation using Drools, JSR303 and Spring

Validation and business rules are closely linked. Indeed validation logic could be thought of as being part of the implicit business rules for an application.It seems natural that integrating a business rules solution with a validation technology might be a natural step. In this post, I explore the possibility of integrating JSR303 and Drools to provide business rule driven validation within a Spring application. [JSR303](<http://jcp.org/aboutJava/communityprocess/edr/jsr303/index.html>) is the standard Java method for data validation using annotations and [Drools](<http://jboss.org/drools/>) is a business rules engine that is a JBoss project and an implementation of [JSR94](<http://jcp.org/aboutJava/communityprocess/review/jsr094/>), the standard Java rule engine API.

## When to use (and when not to)

I don’t think that this is a natural choice for all data validation needs. For a start, if the validation in your application is simple, the standard JSR303 annotations mixed with a few custom annotations might be enough. Integrating Drools comes at a cost in terms of architectural complexity and additional dependencies for you application. And although Drools is highly performance-optimised, a set of business rules in Drools will probably be slower than a set of custom Java statements.

However, there are significant benefits to complex applications – particularly if you are using Drools already. In that case, the complexity and dependency arguments are not valid.

The big benefit is the ability to externalise the business rules from the application and enable them to be edited without redeploying the application.

## Drools overview

In a Drools application, business rules can be written in a powerful expression language called mvel (although XML can be used as well). In the [Drools Expert documentation](<http://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/trunk/target/docs/drools-expert/html_single/index.html#d0e251>), the following basic example is given.

```java
package com.company.license;

public class Applicant {

  private String name;

  private int age;

  private boolean valid;

  // getter and setter methods here

}
```

```drl
package com.company.license;
rule "Is of valid age"
when
$a : Applicant( age < 18 )
then
$a.setValid( false );
end
```

The rule consists of conditions (when) and consequences (then). In this rule, when the Applicant age property is less than 18, the valid property is set to false.

Often, business rules will need to access collaborators such as services or DAOs. These can be injected as “globals” in the rule definition. For example, the scenario above could be modified so that the applicant needs to be loaded from a DAO in order to check the age. The applicant identifier is a property in an ApplicationForm, submitted from a GUI or web application.We’ll also introduce a new class to hold the validation result, rather than setting the validity on the model object itself, which is somewhat artificial. This object could be returned to the presentation tier to tell the user what went wrong.Error object to hold validation result:

```java
package com.acme.app.validation;

import java.util.ArrayList;
import java.util.List;
import java.util.Collections;

public class Errors {

  private final List<Error> errors = Collections.synchronizedList(new ArrayList<Error>());

  public Collection<Error> getErrors() {
      return Collections.unmodifiableCollection(errors);
  }

  public void addError(Object target, String field, String message) {
      this.errors.add(new Error(target, field, message));
  }

  public boolean hasErrors() {
      if (this.errors.size() > 0) {
          return true;
      }
      return false;
  }
}

class Error {
  private final Object target;
  private final String field;
  private final String message;

  public Error(Object target, String field, String message) {
      super();
      this.target = target;
      this.field = field;
      this.message = message;
  }

  public Object getTarget() {
      return target;
  }

  public String getField() {
      return field;
  }

  public String getMessage() {
      return message;
  }
}
```

Modified Applicant (with identity)

```java
public class Applicant {

  private int id;

  private String name;

  private int age;

  private boolean valid;

  // getter and setter methods here

}
```

ApplicationForm from the GUI/web:

```java
public class ApplicationForm {

  private int applicantId;

  private Date date;

  // getter and setter methods here

}
```

Here is a slightly silly test DAO:

```java
public class ApplicantDaoImpl implements ApplicantDao {

  private final Map<Integer, Applicant> applicants = new HashMap<Integer, Applicant>();

  public ApplicantDaoImpl() {
      Applicant app1 = new Applicant(1, "Mr John Smith", 16);
      applicants.put(app1.getId(), app1);
      Applicant app2 = new Applicant(2, "Mr Joe Bloggs", 21);
      applicants.put(app2.getId(), app2);
  }

  @Override
  public Applicant findApplicant(Integer identifier) {
     return applicants.get(identifier);
  }

}
```

Finally, a rule with a global representing the ApplicantDao and using our new Errors object could look like:

```drl
package com.acme.app.rulesimport com.acme.app.form.ApplicationFormimport com.acme.app.model.Applicantimport com.acme.app.validation.Errorsimport com.acme.app.dao.ApplicantDaoglobal ApplicantDao applicantDaopackage com.acme.app.rulesimport com.acme.app.form.ApplicationFormimport com.acme.app.model.Applicantimport com.acme.app.validation.Errorsimport com.acme.app.dao.ApplicantDaoglobal ApplicantDao applicantDaorule "Check applicant age"
when
$a : ApplicationForm()       $errors : Errors()       $applicant:Applicant( age < 18 ) from applicantDao.findApplicant($a.getApplicantId())
then
$errors.addError( $a, "applicantId", "Applicant age < 18" );
end
```

In this version of the rule, the applicant is loaded from a DAO based on their identity. If the age of the applicant is less than 18, an error is inserted into the Errors object specifying the target object, field and message to return to the GUI. Obviously, this could be internationalized by putting a message code instead of the actual message.

That’s an extremely brief overview of rules. Next, I’ll quickly discuss the main API that Java programmers use when interacting with Drools. These will be used by the JSR303 validator when validating a bean using business rules.

At the most basic level, Drools stores business rules in a [KnowledgeBase](<http://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/trunk/target/javadocs/stable/drools-api/org/drools/KnowledgeBase.html>), from which can be created “sessions” which enable users to execute the rules based on facts, which are usually model objects inserted into the session.

There are two types of session: [StatefulKnowldegeSession](<http://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/trunk/target/javadocs/stable/drools-api/org/drools/runtime/StatefulKnowledgeSession.html>) and [StatelessKnowledgeSession](<http://hudson.jboss.org/hudson/job/drools/lastSuccessfulBuild/artifact/trunk/target/javadocs/stable/drools-api/org/drools/runtime/StatelessKnowledgeSession.html>). A StatelessKnowledgeSession is considered appropriate for use cases such as validation, because they are intended as a “one-shot” function call: pass in the facts, execute the rules, get a result. That’s therefore the interface I will use for the integration with a JSR303 validation.  
Here is a simple example of creating a StatelessKnowledgeSession and executing the rules based on a collection of facts, each of which is inserted in turn before the rules are fired.

```text
KnowledgeBuilder kbuilder = KnowledgeBuilderFactory.newKnowledgeBuilder();
kbuilder.add( ResourceFactory.newFileSystemResource( fileName ), ResourceType.DRL );
assertFalse( kbuilder.hasErrors() );   
if (kbuilder.hasErrors() ) {
   System.out.println( kbuilder.getErrors() );
}
KnowledgeBase kbase = KnowledgeBaseFactory.newKnowledgeBase();
kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );

StatelessKnowledgeSession ksession = kbase.newStatelessKnowledgeSession();
ksession.execute( collection );
```

## Spring integration

Conveniently, in Drools 5.1 some additional Spring integration was added that enables you to create KnowledgeBases and sessions declaratively in the application context, using a purpose-built namespace.

In this example, Spring is the “glue” bringing together the Drools and JSR303 parts. Here’s the configuration.

```xml
<?xml version="1.0" ?>
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:context="http://www.springframework.org/schema/context" xmlns:drools="http://drools.org/schema/drools-spring" xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd             http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd                         http://drools.org/schema/drools-spring http://anonsvn.jboss.org/repos/labs/labs/jbossrules/trunk/drools-container/drools-spring/src/main/resources/org/drools/container/spring/drools-spring-1.0.0.xsd">
  <drools:kbase id="kbase">
      
    <drools:resources>
          
      <drools:resource type="DRL" source="classpath:testSpring.drl"/>
        
    </drools:resources>
  </drools:kbase>
  <drools:ksession id="statelessKSession" type="stateless" name="statelessKSession" kbase="kbase"/>
</beans>
```

I’m keeping things very simple – there is a lot more that the namespace can do in terms of configuring knowledge bases, agents, sessions etc.

## JSR 303 Overview

JSR303 is a standard Java mechanism for validating JavaBeans using convenient annotations. Creating custom annotations is a matter of creating the annotation and an accompanying [ConstraintValidator](<http://jackson.codehaus.org/javadoc/bean-validation-api/1.0/javax/validation/ConstraintValidator.html>) implementation, which will be automatically used by the [Validator](<http://jackson.codehaus.org/javadoc/bean-validation-api/1.0/javax/validation/Validator.html>) when it encounters the annotation on a bean getting validated.

The annotation itself is simple.

```java
package com.acme.app.validation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import javax.validation.Constraint;
import javax.validation.Payload;

@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Constraint(validatedBy=BusinessRulesConstraintValidator.class)

public @interface BusinessRulesConstraint {
String message() default "Business rules validation failed.";
Class<?>[] groups() default {};
Class<? extends Payload>[] payload() default {};
}
```

The validator is also reasonably simple. A StatelessKnowledgeSession and a simple bean carrying a Map of the needed collaborators (to be set as globals) are injected into the constructor.  
When the isValid() method is called, an Errors object and the target of the validation are inserted into the session and the validation rules are fired. If the Errors object comes back with errors, validation has failed and a ConstraintViolation is built using the data in the Errors object.

```java
package com.acme.app.validation;

import java.util.Arrays;
import java.util.Map;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.drools.runtime.StatefulKnowledgeSession;
import org.drools.runtime.StatelessKnowledgeSession;
import org.springframework.beans.factory.annotation.Autowired;

/**
* Custom JSR303 {@link ConstraintValidator} that
* uses a Drools {@link StatelessKnowledgeSession} to
* implement rules-based validation of objects
* decorated with a @BusinessRulesConstraint annotation
*/
public class BusinessRulesConstraintValidator implements ConstraintValidator<BusinessRulesConstraint, Object> {

  private final Log logger = LogFactory.getLog(BusinessRulesConstraintValidator.class);

  private final StatelessKnowledgeSession session;

  @Autowired
  public BusinessRulesConstraintValidator(StatelessKnowledgeSession session, Collaborators collaborators) {
      this.session = session;
      if (collaborators != null) {
          Map<String, Object> map = collaborators.getCollaborators();
          for (String key : map.keySet()) {
              session.setGlobal(key, map.get(key));
          }
      }
  }

  @Override
  public void initialize(BusinessRulesConstraint constraint) {}

  @Override
  public boolean isValid(Object target, ConstraintValidatorContext context) {

      // Create Errors
      Errors errors = new Errors();

      try {

          // Fire rules
          session.execute(Arrays.asList(new Object[]{errors, target}));

          // Check for errors
          if (errors.hasErrors()) {
              // Build constraint violations
              context.disableDefaultConstraintViolation();
              for (Error error : errors.getErrors()) {
                  context.buildConstraintViolationWithTemplate(error.getMessage()).addNode(error.getField()).addConstraintViolation();
              }
              return false;
          }
      }
      catch (Exception e) {
          logger.error(e);
          return false;
      }

      return true;
  }

}
```

The Collaborators object is extremely simple:

```java
package com.acme.app.validation;

import java.util.Collections;
import java.util.Map;

public class Collaborators {

  private final Map collaborators;

  public Collaborators(Map collaborators) {
      super();
      this.collaborators = collaborators;
  }

  public Map getCollaborators() {
      return Collections.unmodifiableMap(collaborators);
  }
}
```

It’s simply a container holding a map into which collaborators such as DAO or Service facades could be injected using Spring.  
The full Spring configuration gluing the whole thing together is below:

```xml
<?xml version="1.0" ?>
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:context="http://www.springframework.org/schema/context" xmlns:drools="http://drools.org/schema/drools-spring" xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd             http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd                         http://drools.org/schema/drools-spring http://anonsvn.jboss.org/repos/labs/labs/jbossrules/trunk/drools-container/drools-spring/src/main/resources/org/drools/container/spring/drools-spring-1.0.0.xsd">
  <drools:kbase id="kbase">
      
    <drools:resources>
          
      <drools:resource type="DRL" source="classpath:testSpring.drl"/>
        
    </drools:resources>
  </drools:kbase>
  <drools:ksession id="statelessKSession" type="stateless" name="statelessKSession" kbase="kbase"/>
  <bean id="validator" class="org.springframework.validation.beanvalidation.LocalValidatorFactoryBean"/>
  <bean id="collaborators" class="com.acme.app.validation.Collaborators">
        
    <constructor-arg>
                
      <map>
                    
        <entry key="applicantDao" value-ref="applicantDao"/>
                
      </map>
          
    </constructor-arg>
      
  </bean>
  <bean id="applicantDao" class="com.acme.app.dao.impl.ApplicantDaoImpl"/>
</beans>
```

Using the validator is very simple. First, the ApplicantForm object needs to be decorated with the @BusinessRulesConstraint annotation at class level so that the JSR303 validator will be triggered to use the BusienssRulesConstraintValidator.

```java
package com.acme.app.form;

import java.util.Date;

import com.acme.app.validation.BusinessRulesConstraint;

@BusinessRulesConstraint
public class ApplicationForm {

private Integer applicantId;

private Date date;

// getters/setters
}
```

Then it is a matter of invoking the validator with a bean instance like this:

```java
package com.acme.app.validation.tests;

import java.util.Date;
import java.util.Set;

import javax.validation.ConstraintViolation;
import javax.validation.Validator;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import com.acme.app.form.ApplicationForm;

public class ValidationTestCase {

  private static ApplicationContext ctx;

  private static Validator validator;

  @BeforeClass
  public static void beforeClass() {

      // Create the Spring application context
      String[] paths = { "application-context.xml" };
      ctx = new ClassPathXmlApplicationContext(paths);

  }

  @Before
  public void before() {
      validator = (Validator)ctx.getBean("validator");
  }

  @Test
  public void testInvalidAge() {
      ApplicationForm applicationForm = new ApplicationForm(1, new Date());
      Set<ConstraintViolation<ApplicationForm>> violations = validator.validate(applicationForm);
      Assert.assertNotNull(violations);
      Assert.assertEquals(Integer.valueOf(2), Integer.valueOf(violations.size()));
  }

}
```

## Summary

This post shows you an approach for integrating JSR303 and Drools in a Spring application, something you might want to do if you were using these technologies already in your application and it was sufficiently complex to warrant it. The steps involved are:

  * Create your domain objects and decorate them withe @BusinessRulesConstraint where business rule validation is to be used.
  * Create the .drl file with your validation logic in it.
  * Configure Spring as above with a KnowledgeBase containing your drl file as a resource, a StatelessKnowledgeSession derived from that KnowledgeBase, your collaborators for the rules and the JSR303 validator.

That’s it!

## Postscript: Maven configuration

For Maven users, this should be useful in getting all the dependencies for this example to work.

```xml
<dependencies>

  <!-- Spring bits -->
  <dependency>

      <groupid>org.springframework</groupId>
      <artifactid>spring-core</artifactId>
      <version>${org.springframework.version}</version>
  </dependency>

  <dependency>
      <groupid>org.springframework</groupId>

      <artifactid>spring-context</artifactId>
      <version>${org.springframework.version}</version>
  </dependency>  

  <dependency>
      <groupid>org.springframework</groupId>
      <artifactid>spring-beans</artifactId>
      <version>${org.springframework.version}</version>

  </dependency> 

  <!-- Drools bits -->
  <dependency>
      <groupid>org.drools</groupId>
      <artifactid>drools-core</artifactId>
      <version>5.1.1</version>
  </dependency>

  <dependency>

      <groupid>org.drools</groupId>
      <artifactid>drools-spring</artifactId>
      <version>5.1.1</version>
  </dependency>

  <!-- JSR303 bits -->
  <dependency>
      <groupid>org.hibernate</groupId>

      <artifactid>hibernate-validator</artifactId>
      <version>4.1.0.Final</version>
  </dependency>

  <dependency>
      <groupid>org.slf4j</groupId>
      <artifactid>slf4j-api</artifactId>

      <version>1.5.6</version>
  </dependency>

  <!-- concrete Log4J Implementation for SLF4J API-->
  <dependency>
      <groupid>org.slf4j</groupId>
      <artifactid>slf4j-log4j12</artifactId>
      <version>1.5.6</version>

  </dependency>

</dependencies>
```