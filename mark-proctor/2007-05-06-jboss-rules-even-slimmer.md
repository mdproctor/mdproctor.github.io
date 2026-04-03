---
layout: post
title: "JBoss Rules even slimmer"
date: 2007-05-06
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/05/jboss-rules-even-slimmer.html
---

So the diet has gone well for JBoss Rules which is now even slimmer. If you remember from a previous blog we already removed a lot of dependencies by inlining JCI and removing the uneeded code and the dependencies they needed, you can read about that [here](<http://markproctor.blogspot.com/2007/02/jboss-rules-dependencies-slim-down.html>).

This time we have removed the need for Antlr 2.77 and StringTemplate 3.0; we already use antlr 3.0 for our parser so it was a little annoying that our choice of template systems required another antlr jar adding to the dependency bloat. As it happens [MVEL](<http://mvel.codehaus.org/>), the new scripting language we are adopting, has its own templating system, so we can use that and drop two further dependencies – eventually we’ll inline MVEL itself as its only 300kb, removing another dependency.

Initially MVEL wasn’t quite as powerful as we needed but a day or two of hacking on MVEL brought it up to scratch so that we could migrate. The main missing features, which are important for code generations are multiple list iteration with seperators and nested templates.

Using multiple list iterations, with seperators, you can do following:

```
myMethod(@foreach{types, identifiers as type, identifier}type, identifier@end{","})
```

This allows you to have two lists or arrays where one contains the list of types and the other the list of identifiers and you need to iterate over these together in sequence. Further to that it will add in the seperator string, specified inside the @end marker, after the first value and before the last. This is something that StringTemplate already had but I don’t believe that Velocity or Freemarker have this powerful feature.

We also added nested templates, although this is something all the other templating systems, when calling a template you must pass down the needed variables. Templates can be nested by using the @includeByRef marker:

```
@includeByRef{myTemplate(var1 = "string1", var2 = someOtherVar)}
```

The [README](<http://anonsvn.labs.jboss.com/labs/jbossrules/trunk/README_DEPENDENCIES.txt>) has been updated to detail the current needed dependencies for the project. Part of the document, for core and compiler, has been reproduced below:

CORE RUNTIME  
Runtime assumes that you are “compiling” rules using drools-compiler.

  * drools-core – the rule engine itself.
  * mvel14-1.2beta16
  * optional packages:
    * xpp3-1.1.3.4.O, xstream-1.1.3 – if you are using the file based audit feature

Note you can use the drools-core stand-alone if you are compiling “outside” your runtime application, and deploying serialized Package or RuleBase? objects.

COMPILER – rule assembly time  
Rule compiler takes rules in some textual format and prepares binary Packages of rules for deployment. This depends on the CORE RUNTIME.

  * drools-core
  * drools-compiler – the rule compiler itself.
  * antlr3-3.0b7
  * xerces-2.4.0, xml-apis-1.0.b2 – only if you are using XML rules, if DRL only, can skip this.
  * eclipse-jdt-core-3.2.1.v_677_R32x – only if you want to compile with eclipse
  * janino-2.5.6 – only if you want to compile with janino