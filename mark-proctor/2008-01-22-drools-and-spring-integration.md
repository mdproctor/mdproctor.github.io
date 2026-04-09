---
layout: post
title: "Drools and Spring Integration"
date: 2008-01-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/01/drools-and-spring-integration.html
---

I’ve posted a donated drools-spring module to the dev mailing list for feedback on Drools integration with Spring. I’ve had no feedback yet, so I thought I’d open it up to a wider audience. I’m also hoping this work can be replicated into a drools-guice module, so we can start to have out of the box integration for the various containers out there, all working in a similar manner, possibly with standardised annotations.

You can also read about the JBoss MicroContainer integration work for Drools here:  
[http://www.jboss.org/index.html?module=bb&op=viewtopic&t=117607](<http://www.jboss.org/index.html?module=bb&op=viewtopic&t=117607>)

```drl
Here is a copy of the message sent to the dev mailing list:
You can declare the transaction beans as follows:
<bean id=”droolsTransactionManager”
class=”org.drools.spring.core.DroolsTransactionManager”>
 <property name=”workingMemory” ref=”workingMemory”/>
</bean>
```

<bean id=”txProxyTemplate” abstract=”true”  
class=”org.springframework.transaction.interceptor.TransactionProxyFactoryBean”>  
<property name=”proxyTargetClass”>  
<value>true</value>  
</property>  
<property name=”transactionManager” ref=”droolsTransactionManager”/>  
<property name=”transactionAttributes”>  
<props>  
<prop key=”newStatefullSession*”>PROPAGATION_REQUIRED</prop>  
</props>  
</property>  
</bean>

The last one is only a proxy for the transaction, to declare the pointcuts.  
I think the classes for aspects in Ales implementation can be  
implemented this way for spring, if not it will be needed to look at :  
<http://static.springframework.org/spring/docs/2.5.x/reference/aop.html>  
but I need time for that.

The DroolsTransactionManager is for standalone use.

It was added rule base configuration support for the bean factory of  
Geoffrey as well to set the type.

Here are information about getting Resources like URL, input stream, file…  
<http://static.springframework.org/spring/docs/2.5.x/reference/resources.html>

attachment [http://cache.gmane.org//gmane/comp/java/drools/devel/2388-001.bin](<>)

original post:  
<http://article.gmane.org/gmane.comp.java.drools.devel/2388>