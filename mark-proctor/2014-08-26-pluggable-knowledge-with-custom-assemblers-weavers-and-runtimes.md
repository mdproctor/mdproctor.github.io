---
layout: post
title: "Pluggable Knowledge with Custom Assemblers, Weavers and Runtimes"
date: 2014-08-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/08/pluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html
---

As part of the [Bayesian work](<http://blog.athico.com/2014/08/drools-bayesian-belief-network.html>) I’ve refactored much of Kie to have clean extension points. I wanted to make sure that all the working parts for a Bayesian system could be done, without adding any code to the existing core.

So now each knowledge type can have it’s own package, assembler, weaver and runtime. Knowledge is no longer added directly into KiePackage, but instead into an encapsulated knowledge package for that domain, and that is then added to KiePackage. The assembler stage is used when parsing and assembling the knowledge definitions. The weaving stage is when weaving those knowledge definitions into an existing KieBase. Finally the runtime encapsulates and provides the runtime for the knowledge.

drools-beliefs contains the Bayesian integration and a good starting point to see how this works:  
<https://github.com/droolsjbpm/drools/tree/beliefs/drools-beliefs/>

For this to work you and a META-INF/kie.conf file and it will be discovered and made available:  
<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/resources/META-INF/kie.conf>

The file uses the MVEL syntax and specifies one or more services:

```
[
'assemblers' : [ new org.drools.beliefs.bayes.assembler.BayesAssemblerService() ],
'weavers' : [ new org.drools.beliefs.bayes.weaver.BayesWeaverService() ],
'runtimes' : [ new org.drools.beliefs.bayes.runtime.BayesRuntimeService() ]
]
```

Github links to the package and service implementations:  
[Bayes Package](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/assembler/BayesPackage.java>)  
[Assembler Service](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/assembler/BayesAssemblerService.java>)  
[Weaver Service](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/weaver/BayesWeaverService.java>)  
[Runtime Service](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/runtime/BayesRuntimeService.java>)

Here is a [quick unit test](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/test/java/org/drools/beliefs/bayes/integration/BayesRuntimeTest.java>) showing things working end to end, notice how the runtime can be looked up and accessed. It’s using the old api in the test, but will work fine with the declarative kmodule.xml stuff too. The only bit that is still hard coded is the ResourceType.Bayes. As ResourceTypes is an enum. We will probably refactor that to be a standard Class instead, so that it’s not hard coded.

The code to lookup the runtime:

```
StatefulKnowledgeSessionImpl ksession = (StatefulKnowledgeSessionImpl) kbase.newStatefulKnowledgeSession();
BayesRuntime bayesRuntime = ksession.getKieRuntime(BayesRuntime.class);
```

The unit test:

```
KnowledgeBuilder kbuilder = new KnowledgeBuilderImpl();
kbuilder.add( ResourceFactory.newClassPathResource("Garden.xmlbif", AssemblerTest.class), ResourceType.BAYES );
KnowledgeBase kbase = getKnowledgeBase();
kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );
StatefulKnowledgeSessionImpl ksession = (StatefulKnowledgeSessionImpl) kbase.newStatefulKnowledgeSession();
BayesRuntime bayesRuntime = ksession.getKieRuntime(BayesRuntime.class);
BayesInstance instance = bayesRuntime.getInstance( Garden.class );
assertNotNull(  instance );
```

jBPM is already refactored out from core and compiler, although it uses it’s own interfaces for this. We plan to port the existing jBPM way to this and actually all the Drools stuff will eventually be done this way too. This will create a clean KIE core and compiler with rules, processes, bayes or any other user knowledge type are all added as plugins.

A community person is also already working on a new type declaration system, that will utilise these extensions. Here is an example of what this new type system will look like:  
<https://github.com/sotty/metaprocessor/blob/master/deklare/src/test/resources/test1.ktd>