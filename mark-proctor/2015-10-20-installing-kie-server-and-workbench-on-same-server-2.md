---
layout: post
title: "Installing KIE Server and Workbench on same server"
date: 2015-10-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2015/10/installing-kie-server-and-workbench-on-same-server-2.html
---

syndicated from <http://mswiderski.blogspot.co.uk/2015/10/installing-kie-server-and-workbench-on.html>  
—-  
A common requirement for installation on development machine is to run both KIE Workbench and KIE Server on same server to simplify execution environment and avoid any port offset configuration.  
  
This article will explain all installation steps needed to make this happen on two most frequently used containers:  

  * Wildfly 8.2.0.Final
  * Apache Tomcat 8

#### Download binaries

So let’s get our hands dirty and play around with some installation steps. First make sure you download correct versions of workbench and KIE Server for the container you target.

Wildfly

[kie-wb-distribution-wars-6.3.0.Final-wildfly8.war](<http://repo1.maven.org/maven2/org/kie/kie-wb-distribution-wars/6.3.0.Final/kie-wb-distribution-wars-6.3.0.Final-wildfly8.war>)

[kie-server-6.3.0.Final-ee7.war](<http://repo1.maven.org/maven2/org/kie/server/kie-server/6.3.0.Final/kie-server-6.3.0.Final-ee7.war>)

Tomcat

[kie-wb-distribution-wars-6.3.0.Final-tomcat7.war](<http://repo1.maven.org/maven2/org/kie/kie-wb-distribution-wars/6.3.0.Final/kie-wb-distribution-wars-6.3.0.Final-tomcat7.war>)

[kie-server-6.3.0.Final-webc.war](<http://repo1.maven.org/maven2/org/kie/server/kie-server/6.3.0.Final/kie-server-6.3.0.Final-webc.war>)

### Wildfly

#### Deploy applications

Copy downloaded files into WILDFLY_HOME/standalone/deployments, while copying rename them to simplify the context paths that will be used on application server:

  * rename **kie-wb-distribution-wars-6.3.0.Final-wildfly8.war** to **kie-wb.war**
  * rename **kie-server-6.3.0.Final-ee7.war** to **kie-server.war**

#### 

#### Configure your server

With Wildfly there is not much to setup as both transaction manager and persistence (including data source) is already preconfigured.

#### 

#### Configure users

  * create user in application realm 
    * name: kieserver 
    * password: kieserver1!
    * roles: kie-server
  * create user in application realm to logon to workbench
    * name: workbench 
    * password: workbench!
    * roles: admin, kie-server

#### Configure system properties

Following list of properties needs to be given to work smoothly for both workbench and KIE Server:

  * -Dorg.kie.server.id=wildfly-kieserver 
  * -Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server 
  * -Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller

#### Launching the server

best way is to add system properties into startup command when launching Wildfly server. Go to WILDFLY_HOME/bin and issue following command:

./standalone.sh –server-config=standalone-full.xml -Dorg.kie.server.id=wildfly-kieserver -Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server -Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller

### Tomcat

#### Deploy applications

Copy downloaded files into TOMCAT_HOME/webapps, while copying rename them to simplify the context paths that will be used on application server:

  * rename **kie-wb-distribution-wars-6.3.0.Final-tomcat7.war** to **kie-wb.war**
  * rename **kie-server-6.3.0.Final-webc.war** to **kie-server.war**

#### Configure your server

  1. Copy following libraries into TOMCAT_HOME/lib
     1. btm-2.1.4
     2. btm-tomcat55-lifecycle-2.1.4
     3. h2-1.3.161
     4. jacc-1.0
     5. jta-1.1
     6. kie-tomcat-integration-6.3.0.Final
     7. slf4j-api-1.7.2
     8. slf4j-api-1.7.2
  2. Create Bitronix configuration files to enable JTA transaction manager

  * Create file ‘btm-config.properties’ under TOMCAT_HOME/conf with following content

bitronix.tm.serverId=tomcat-btm-node0

bitronix.tm.journal.disk.logPart1Filename=${btm.root}/work/btm1.tlog

bitronix.tm.journal.disk.logPart2Filename=${btm.root}/work/btm2.tlog

bitronix.tm.resource.configuration=${btm.root}/conf/resources.properties

  * Create file ‘resources.properties’ under TOMCAT_HOME/conf with following content

resource.ds1.className=bitronix.tm.resource.jdbc.lrc.LrcXADataSource

resource.ds1.uniqueName=jdbc/jbpm

resource.ds1.minPoolSize=10

resource.ds1.maxPoolSize=20

resource.ds1.driverProperties.driverClassName=org.h2.Driver

resource.ds1.driverProperties.url=jdbc:h2:mem:jbpm

resource.ds1.driverProperties.user=sa

resource.ds1.driverProperties.password=

resource.ds1.allowLocalTransactions=true

#### Configure users

Create following users in tomcat-users.xml under TOMCAT_HOME/conf

  * create user
    * name: kieserver 
    * password: kieserver1!
    * roles: kie-server
  * create user to logon to workbench
    * name: workbench 
    * password: workbench!
    * roles: admin, kid-server

[?](<http://mswiderski.blogspot.co.uk/2015/10/installing-kie-server-and-workbench-on.html#>)

```
"admin"/>  "analyst"/>   "user"/>  "kie-server"/>  "workbench" password="workbench1!" roles="admin,kie-server"/>  "kieserver" password="kieserver1!" roles="kie-server"/>
```

#### Configure system properties

Configure following system properties in file setenv.sh under TOMCAT_HOME/bin

-Dbtm.root=$CATALINA_HOME 

-Dorg.jbpm.cdi.bm=java:comp/env/BeanManager 

-Dbitronix.tm.configuration=$CATALINA_HOME/conf/btm-config.properties 

-Djbpm.tsr.jndi.lookup=java:comp/env/TransactionSynchronizationRegistry 

-Djava.security.auth.login.config=$CATALINA_HOME/webapps/kie-wb/WEB-INF/classes/login.config 

-Dorg.kie.server.persistence.ds=java:comp/env/jdbc/jbpm 

-Dorg.kie.server.persistence.tm=org.hibernate.service.jta.platform.internal.BitronixJtaPlatform 

-Dorg.kie.server.id=tomcat-kieserver 

-Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server 

-Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller

NOTE: Simple copy this into setenv.sh files to properly setup KIE Server and Workbench on Tomcat:

CATALINA_OPTS=”-Xmx512M -XX:MaxPermSize=512m -Dbtm.root=$CATALINA_HOME -Dorg.jbpm.cdi.bm=java:comp/env/BeanManager -Dbitronix.tm.configuration=$CATALINA_HOME/conf/btm-config.properties -Djbpm.tsr.jndi.lookup=java:comp/env/TransactionSynchronizationRegistry -Djava.security.auth.login.config=$CATALINA_HOME/webapps/kie-wb/WEB-INF/classes/login.config -Dorg.kie.server.persistence.ds=java:comp/env/jdbc/jbpm -Dorg.kie.server.persistence.tm=org.hibernate.service.jta.platform.internal.BitronixJtaPlatform -Dorg.kie.server.id=tomcat-kieserver -Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server -Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller“

#### Launching the server

Go to TOMCAT_HOME/bin and issue following command:

./startup.sh

### Going beyond default setup

#### Disabling KIE Server extensions

And that’s all to do to setup both KIE Server and Workbench on single server instance (either Wildfly or Tomcat). This article focused on fully featured KIE server installation meaning both BRM (rules) and BPM (processes, tasks) capabilities. Although KIE Server can be configured to serve only subset of the capabilities – e.g. only BRM or only BPM.

To do so one can configure KIE Server with system properties to disable extensions (BRM or BPM)

**Wildfly:**

add following system property to startup command:

  * disable BRM: -Dorg.drools.server.ext.disabled=true
  * disable BPM: -Dorg.jbpm.server.ext.disabled=true

So the startup command would look like this:

./standalone.sh –server-config=standalone-full.xml -Dorg.kie.server.id=wildfly-kieserver -Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server -Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller -Dorg.jbpm.server.ext.disabled=true

**Tomcat**

add following system property to setenv.sh script (must be still part of CATALINA_OPTS configuration):

  * disable BRM: -Dorg.drools.server.ext.disabled=true
  * disable BPM: -Dorg.jbpm.server.ext.disabled=true

Complete content of setenv.sh is as follows:

CATALINA_OPTS=”-Xmx512M -XX:MaxPermSize=512m -Dbtm.root=$CATALINA_HOME -Dorg.jbpm.cdi.bm=java:comp/env/BeanManager -Dbitronix.tm.configuration=$CATALINA_HOME/conf/btm-config.properties -Djbpm.tsr.jndi.lookup=java:comp/env/TransactionSynchronizationRegistry -Djava.security.auth.login.config=$CATALINA_HOME/webapps/kie-wb/WEB-INF/classes/login.config -Dorg.kie.server.persistence.ds=java:comp/env/jdbc/jbpm -Dorg.kie.server.persistence.tm=org.hibernate.service.jta.platform.internal.BitronixJtaPlatform -Dorg.kie.server.id=tomcat-kieserver -Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server -Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller -Dorg.jbpm.server.ext.disabled=true“

#### Changing data base and persistence settings

Since by default persistence uses just in memory data base (H2) it is good enough for first tryouts or demos but not for real usage. So to be able to change persistence settings following needs to be done:

**KIE Workbench on Wildfly**

Modify data source configuration in Wildfly – either via manual editing of standalone-full.xml file or using tools such as Wildfly CLI. See [Wildfly documentation](<https://docs.jboss.org/author/display/WFLY8/DataSource+configuration>) on how to define data sources.

  * Next modify persistence.xml that resides inside workbench war file. Extract the kie-wb.war file into directory with same name and in same location (WILDFLY_HOME/standalone/deployments). 
  * Then navigate to kie-wb.war/WEB-INF/classes/META-INF
  * Edit persistence.xml file and change following elements
    * jta-data-source to point to the newly created data source (JNDI name) for your data base
    * hibernate.dialect to hibernate supported dialect name for you data base

**KIE Server on Wildfly**

there is no need to do any changes to the application (the war file) as the persistence can be reconfigured via system properties. Set following system properties at the end of server startup command

  * -Dorg.kie.server.persistence.ds=java:jboss/datasources/jbpmDS
  * -Dorg.kie.server.persistence.dialect=org.hibernate.dialect.MySQL5Dialect

Full command to start server will be:

./standalone.sh –server-config=standalone-full.xml -Dorg.kie.server.id=wildfly-kieserver -Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server -Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller –Dorg.kie.server.persistence.ds=java:jboss/datasources/jbpmDS 

-Dorg.kie.server.persistence.dialect=org.hibernate.dialect.MySQL5Dialect

**KIE Workbench on Tomcat**

To modify data source configuration in Tomcat you need to alter resources.properties (inside TOMCAT_HOME/conf) file that defines data base connection. For MySQL it could look like this:

resource.ds1.className=com.mysql.jdbc.jdbc2.optional.MysqlXADataSource

resource.ds1.uniqueName=jdbc/jbpmDS

resource.ds1.minPoolSize=0

resource.ds1.maxPoolSize=10

resource.ds1.driverProperties.user=guest

resource.ds1.driverProperties.password=guest

resource.ds1.driverProperties.URL=jdbc:mysql://localhost:3306/jbpm

resource.ds1.allowLocalTransactions=true

 _**Make sure you’re copy mysql JDBC driver into TOMCAT_HOME/lib otherwise it won’t provide proper connection handling.**_

  * Next modify persistence.xml that resides inside workbench war file. Extract the kie-wb.war file into directory with same name and in same location (TOMCAT_HOME/webapps). 
  * Then navigate to kie-wb.war/WEB-INF/classes/META-INF
  * Edit persistence.xml file and change following elements
    * jta-data-source to point to the newly created data source (JNDI name) for your data base
    * hibernate.dialect to hibernate supported dialect name for you data base

**KIE Server on Tomcat**

there is no need to do any changes to the application (the war file) as the persistence can be reconfigured via system properties. Set or modify (as data source is already defined there) following system properties in setenv.sh script inside TOMCAT_HOME/bin

  * -Dorg.kie.server.persistence.ds=java:comp/env/jdbc//jbpmDS
  * -Dorg.kie.server.persistence.dialect=org.hibernate.dialect.MySQL5Dialect

Complete content of the setenv.sh script is as follows:

CATALINA_OPTS=”-Xmx512M -XX:MaxPermSize=512m -Dbtm.root=$CATALINA_HOME -Dorg.jbpm.cdi.bm=java:comp/env/BeanManager -Dbitronix.tm.configuration=$CATALINA_HOME/conf/btm-config.properties -Djbpm.tsr.jndi.lookup=java:comp/env/TransactionSynchronizationRegistry -Djava.security.auth.login.config=$CATALINA_HOME/webapps/kie-wb/WEB-INF/classes/login.config -Dorg.kie.server.persistence.ds=java:comp/env/jdbc/jbpmDS -Dorg.kie.server.persistence.tm=org.hibernate.service.jta.platform.internal.BitronixJtaPlatform 

-Dorg.kie.server.persistence.dialect=org.hibernate.dialect.MySQL5Dialect

-Dorg.kie.server.id=tomcat-kieserver -Dorg.kie.server.location=http://localhost:8080/kie-server/services/rest/server -Dorg.kie.server.controller=http://localhost:8080/kie-wb/rest/controller”

** _Note that KIE Server persistence is required only for BPM capability so if you disable it you can skip any KIE server related persistence changes._**

And that would be it. Hopefully this article will help with installation of KIE Workbench and Server on single application server. 

Have fun and comments more than welcome.