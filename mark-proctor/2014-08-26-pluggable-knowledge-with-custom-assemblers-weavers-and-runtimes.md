---
layout: post
title: "Pluggable Knowledge with Custom Assemblers, Weavers and Runtimes"
date: 2014-08-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/08/pluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Pluggable Knowledge with Custom Assemblers, Weavers and Runtimes](<https://blog.kie.org/2014/08/pluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- August 26, 2014  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

As part of the [Bayesian work](<http://blog.athico.com/2014/08/drools-bayesian-belief-network.html>) I’ve refactored much of Kie to have clean extension points. I wanted to make sure that all the working parts for a Bayesian system could be done, without adding any code to the existing core.

So now each knowledge type can have it’s own package, assembler, weaver and runtime. Knowledge is no longer added directly into KiePackage, but instead into an encapsulated knowledge package for that domain, and that is then added to KiePackage. The assembler stage is used when parsing and assembling the knowledge definitions. The weaving stage is when weaving those knowledge definitions into an existing KieBase. Finally the runtime encapsulates and provides the runtime for the knowledge.

drools-beliefs contains the Bayesian integration and a good starting point to see how this works:  
<https://github.com/droolsjbpm/drools/tree/beliefs/drools-beliefs/>

For this to work you and a META-INF/kie.conf file and it will be discovered and made available:  
<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/resources/META-INF/kie.conf>

The file uses the MVEL syntax and specifies one or more services:
[code]
    [
    'assemblers' : [ new org.drools.beliefs.bayes.assembler.BayesAssemblerService() ],
    'weavers' : [ new org.drools.beliefs.bayes.weaver.BayesWeaverService() ],
    'runtimes' : [ new org.drools.beliefs.bayes.runtime.BayesRuntimeService() ]
    ]
    
[/code]

Github links to the package and service implementations:  
[Bayes Package](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/assembler/BayesPackage.java>)  
[Assembler Service](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/assembler/BayesAssemblerService.java>)  
[Weaver Service](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/weaver/BayesWeaverService.java>)  
[Runtime Service](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/main/java/org/drools/beliefs/bayes/runtime/BayesRuntimeService.java>)

Here is a [quick unit test ](<https://github.com/droolsjbpm/drools/blob/beliefs/drools-beliefs/src/test/java/org/drools/beliefs/bayes/integration/BayesRuntimeTest.java>)showing things working end to end, notice how the runtime can be looked up and accessed. It’s using the old api in the test, but will work fine with the declarative kmodule.xml stuff too. The only bit that is still hard coded is the ResourceType.Bayes. As ResourceTypes is an enum. We will probably refactor that to be a standard Class instead, so that it’s not hard coded.

The code to lookup the runtime:
[code]
    StatefulKnowledgeSessionImpl ksession = (StatefulKnowledgeSessionImpl) kbase.newStatefulKnowledgeSession();
    BayesRuntime bayesRuntime = ksession.getKieRuntime(BayesRuntime.class);
    
[/code]

The unit test:
[code]
    KnowledgeBuilder kbuilder = new KnowledgeBuilderImpl();
    kbuilder.add( ResourceFactory.newClassPathResource("Garden.xmlbif", AssemblerTest.class), ResourceType.BAYES );
    KnowledgeBase kbase = getKnowledgeBase();
    kbase.addKnowledgePackages( kbuilder.getKnowledgePackages() );
    StatefulKnowledgeSessionImpl ksession = (StatefulKnowledgeSessionImpl) kbase.newStatefulKnowledgeSession();
    BayesRuntime bayesRuntime = ksession.getKieRuntime(BayesRuntime.class);
    BayesInstance instance = bayesRuntime.getInstance( Garden.class );
    assertNotNull(  instance );
    
[/code]

jBPM is already refactored out from core and compiler, although it uses it’s own interfaces for this. We plan to port the existing jBPM way to this and actually all the Drools stuff will eventually be done this way too. This will create a clean KIE core and compiler with rules, processes, bayes or any other user knowledge type are all added as plugins.

A community person is also already working on a new type declaration system, that will utilise these extensions. Here is an example of what this new type system will look like:  
<https://github.com/sotty/metaprocessor/blob/master/deklare/src/test/resources/test1.ktd>

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fpluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html&linkname=Pluggable%20Knowledge%20with%20Custom%20Assemblers%2C%20Weavers%20and%20Runtimes> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fpluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html&linkname=Pluggable%20Knowledge%20with%20Custom%20Assemblers%2C%20Weavers%20and%20Runtimes> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fpluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html&linkname=Pluggable%20Knowledge%20with%20Custom%20Assemblers%2C%20Weavers%20and%20Runtimes> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fpluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html&linkname=Pluggable%20Knowledge%20with%20Custom%20Assemblers%2C%20Weavers%20and%20Runtimes> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fpluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html&linkname=Pluggable%20Knowledge%20with%20Custom%20Assemblers%2C%20Weavers%20and%20Runtimes> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fpluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html&linkname=Pluggable%20Knowledge%20with%20Custom%20Assemblers%2C%20Weavers%20and%20Runtimes> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2014%2F08%2Fpluggable-knowledge-with-custom-assemblers-weavers-and-runtimes.html&linkname=Pluggable%20Knowledge%20with%20Custom%20Assemblers%2C%20Weavers%20and%20Runtimes> "Email")
  *[]: 2010-05-25T16:11:00+02:00