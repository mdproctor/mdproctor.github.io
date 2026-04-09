---
layout: post
title: "Who do you know and how do you know them?"
date: 2009-03-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/03/who-do-you-know-and-how-do-you-know-them.html
---

No, this isn’t a police interrogation. This article is about facilitating the management of complex object model relationships within the context of a rules engine. Rule engines are fantastic at solving a vast array of business problems with the greatest of ease, however, with a caveat being that any object you want to reason over must be in working memory.

One of the problems I encountered when working with Drools was that the _developer_ was faced with the task of asserting objects into working memory. Coming from an [ArtEnterprise](<http://www.mindbox.com/Products/ARTEnterprise.aspx>) background this was a bit odd to me. ArtEnterprise is a [forward chaining](<http://en.wikipedia.org/wiki/Forward_chaining>) inference engine derived from ART(Automated Reasoning Tool)/CLIPS(C Language Integrated Production System). It is a powerful and feature rich expert system development language with a [Common Lisp](<http://en.wikipedia.org/wiki/Common_Lisp>) syntax.

In ArtEnterprise, there is no distinction between working memory and non-working memory; If you want to write rules to reason over some set of objects, you simply do it. In other words, you do not have to worry about an object being in memory or not. After some research, I soon learned that many Java based rules engines such as JESS and iLog also require you to actively assert the objects your rules will reason over. This is quite an onus to place on the developer, especially in the case of complex object models.

To say that the object model I was dealing with was complex, along with the business rules that were needed, is an understatement. The client, a large availability services company, was looking for an agile approach to dealing with ever changing business rules specific to individual clients. Without a solution to facilitate the assertion of objects, I would not be able to sell a rules based approach.

Enter the Java Persistence API (JPA). JPA is a persistence framework that allows developers to map Java domain objects to tables in a relational database. This object/relational mapping is expressed either directly in the domain object via Java Annotations, or in a separate XML file bundled with the application.

Fortunately for me, as it turned out, our project utilized the annotation based mappings. For example, our object model contains a Server object to represent, not surprisingly, a physical server . The following is a snippet of the class declaration

```java
@Entity
public class Server extends {
     @ManyToOne
     private Architecture architecture;

     @OneToMany
     private Set<OperatingSystem> operatingSystems;

     @OneToOne
     private Keyboard keyboard;
}
```

The @_Entity_ annotation on the _Server_ class declaration specifies that this class should be persisted. The @_ManyToOne_ annotation on the _architecture_ field means that many servers can have the same architecture. While the @_OneToMany_ annotation on the _operatingSystems_ field means that a server can have multiple operating systems. And finally, the @_OneToOne_ annotation on the _keyboard_ field means that a server can only have a single keyboard attached.

```
protected boolean isPersistentEntity(Class clazz) {
 return clazz.isAnnotationPresent(Entity.class) ||
        clazz.isAnnotationPresent(MappedSuperclass.class) ||
        clazz.isAnnotationPresent(Embeddable.class);
}
```

Associated collections and maps were handled similarly except there was an additional level of indirection to check the generic type the collection held.

```java
protected void handleCollectionField(Class clazz, Field field) {
     ParameterizedType parameterizedType = (ParameterizedType) field.getGenericType();
     Type types[] = parameterizedType.getActualTypeArguments();

     for (Type parameterType : types) {
         Class parameterClass = (Class) parameterType;

         if (isPersistenantEntity(parameterClass)) {
             ...
         }
     }
}
```

The final piece of the puzzle was to use this information along with [Velocity](<http://velocity.apache.org/>) to generate traversal rules. Velocity is a templating engine that can be used to generate code based on data and a template defined in Velocity Template Language (VTL). The engine takes a template and merges it with the data to produce some type of output. The data, in my case, are the class and field information. The template is of the rule that will be generated. The following is the template I defined for handling one-to-one and many-to-one associations:

```drl
#set( $ruleName = $className +  $fieldName + "FieldWalker")
rule '$ruleName'
agenda-group "$constants.TRAVERSAL_AGENDA_GROUP"
when
$className : $className ($fieldName: $fieldName != null)
then
insert($$fieldName);
end
```

Rules were generated for each association an object has. Please note that this generation is happening at build time, not runtime. For example, given the previous Server class declaration, the following rules would be generated:

```drl
rule 'ServerarchitectureFieldWalker'
agenda-group "Traversal"
when
$Server : Server($architecture : architecture != null)
then
insert($architecture);endrule 'ServerkeyboardFieldWalker'
agenda-group "Traversal"
when
$Server : Server($keyboard : keyboard != null)
then
insert($keyboard);
end
```

So what this means is that anytime a _Server_ object is asserted into memory, the _Architecture_ , _Keyboard_ , and any other associations the server has will automatically be asserted also. Since _Architecture_ and _Keyboard_ are also persistable, any associations _they_ have will also be asserted, and so on.

I also introduced the capability to mark either a Class or association as “non traversable”. For example, say that your _Server_ is within a _Rack_ , and the rack contains multiple servers. If we would not like the server’s rack to be asserted into memory we can markup the _rack_ field on the server with a @_DoNotTraverse_ annotation to to prevent this from happening.

```
@Entity
public class Server extends {
 @ManyToOne
 private Architecture architecture;

 ...

 @DoNotTraverse
 private Rack rack;
}
```

With these rules now in place, the developer is now freed from having to worry about whether they have all objects asserted into working memory or not. This allows them to focus on solving the “real” business problems.

* * *