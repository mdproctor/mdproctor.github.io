---
layout: post
title: "Red Hat JBoss BRMS and BPMS Rich Client Framework demonstrating Polyglot Integration with GWT/Errai/UberFire and AngularJS"
date: 2014-11-21
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2014/11/red-hat-jboss-brms-and-bpms-rich-client-framework-demonstrating-polyglot-integration-with-gwt-errai-uberfire-and-angularjs.html
---

Last week I published a blog highlighting a presentation I gave showing our rich client platform that has resulted from the work we have done within the BRMS and BPMS platforms, the productised versions of the Drools and jBPM projects. The presentation is all screenshots and videos, you can find the blog and the link to the slideshare here:  
[“Red Hat JBoss BRMS and BPMS Workbench and Rich Client Technology”](<http://blog.athico.com/2014/11/red-hat-jboss-brms-and-bpms-workbench.html>)

The presentation highlighted the wider scope of our UI efforts; demonstrating what we’ve done within the BRMS and BPMS platform and the flexibility and adaptability provided by our UI technology. It provides a great testimony for the power of [GWT](<http://www.gwtproject.org/>), [Errai](<http://erraiframework.org/>) and [UberFire](<http://www.uberfireframework.org/>), the three technologies driving all of this. We can’t wait for the [GWT 2.7 upgrade](<https://vaadin.com/blog/-/blogs/what-s-new-in-gwt-2-7>) :)

As mentioned in the last blog the UberFire website is just a placeholder and there is no release yet. The plan is first to publish our 0.5 release, but that is more for our BRMS and BPMS platforms. We will then move it to GWT 2.7 and work towards a UF 1.0, which will be suitable for wider consumption.  With 1.0 we will add examples and documentation and work on making things more easily understood and consumable for end users. Of course there is nothing to stop the adventurous trying 0.5, the code is robust and already productized within BRMS and BPMS – we are always on irc to help, Freenode #uberfire.

That presentation itself built on the early video’s showing our new Apps framework:  
[The Drools and jBPM KIE Apps Framework](<http://blog.athico.com/2014/10/the-drools-and-jbpm-kie-apps-platform.html>)

The above video already demonstrates our polyglot capabilities, building AngularJS components and using them within the UF environments. It also shows of our spiffy new [JSFiddle](<http://jsfiddle.net/>) inspired RAD environment.

I’d now like to share with you the work we’ve done on the other side of polyglot development – this time using GWT and UF from within AngularJS. It was important we allow for an AngularJS first approach, that worked with the tool chain that AngularJS people are familiar with. By AngularJS first, I mean that AngularJS is the outer most container. Where as in the above video UF is already running and is the outer container in which individual AngularJS components can be used.

Before I detail the work we’ve done it’s first best to cover the concepts of Screens and Perspectives, our two main components that provide our polyglot interoprability – there are others, but this is enough to understand the videos and examples that come next. A Screen is our simplest component, it is a DIV plus optional life cycle callbacks. A Perspective is also a DIV, but it contains a composition of 1..n Screen with different possible layout managers and persistence of the layout.

**Screen**

  * [CDI](<http://www.cdi-spec.org/>) discovery, or programmatically registered.
  * DIV on a page.
  * Life cycle callbacks.
    * OnStart, OnClose, OnFocus, OnLostFocus, OnMayClose, OnReveal.
  * Decoupling via Errai Bus.
    * Components do not invoke each other, all communication handled by a bus.
  * Editors extend screens, are associated with resource types and provide the additional life cycles
    * onSave, isDirty.

**Perspective**

  * [CDI](<http://www.cdi-spec.org/>) discovery, or programmatically registered.
  * Composition of 1..n Screens, but is itself a DIV.
  * Supports pluggable window management of Screens.
    * North, East, South West (NESW).
      * Drag and Drop docking capabilities.
    * Bootstrap Grid Views.
      * Separate design time and runtime.
    * Templates (ErraiUI or AngularJS).
      * Absolute control of Perspective content and layout.
  * Supports persistence of Perspective layout, should the user re-design it.
    * Only applicable to NESW and Bootstrap Grid views.

A picture is worth a thousands words, so here is a screenshot of the Perspective Builder in action. Here it uses the Bootstrap Grid View layout manager. Within each grid cell is a Screen. The Perspective is saved and then available from within the application. If the NESW layout manager was used there is no separate design time, and all dragging is done in-place and persistence happens in the background after each change. Although it’s not shown in the screenshot below we also support both list (drop list) and tab stacks for Screens.

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/076a4c472a0f-iberMAO.png>)

Now back to what an AngularJS first approach means. 6 different points were identified as necessary to demonstrate that this is possible.

  1. UF Screens and Perspectives should be available seamlessly as AngularJS Directives.
  2. [Bower](<http://bower.io/>) packaging for a pre-compiled UFJS. UFJS is the pre-compile client only version of UF.
  3. UFJS can work standalone, file:// for example. UFJS can optionally work with an UF war backend, allowing persistence of perspectives and other optional places that UFJS might need to save state as well as access to our full range of provided services, like identity management.
  4. Support live refresh during development.
  5. Nested Controllers.
  6. Persistence and routing.
  7. Work with tools such as [Yeoman](<http://yeoman.io/>), [Grunt](<http://gruntjs.com/>) and [Karma](<http://karma-runner.github.io/0.12/index.html>).

Eder has produced a number of examples, that you can run yourself. These demonstrate all of the points have been solved. You can find the code [here](<https://github.com/ederign/uf-js>), along with the README to get you started. We did not provide video’s for point 7, as I believe the video’s for points 1 to 6 show that this would not be a problem.

Eder has also created several short videos running the examples, for each of the use cases, and put them into a YouTube playlist. He has added text and callouts to make it clear what’s going on:  
[AngularJS + UF PlayList](<http://youtu.be/jDpmMeFO_q8?list=PLOwIXYCm38DklIzT8E7qKmW1kNQA4N7vN>)

  1. Overview explaining what each video demonstrates (33s).
  2. AngularJS App + UFJS, client only, distribution using Bower. (2m30s).

  * Install and play with UFJS through Bower
  * Create a Native AngularJS App
  * Integrate this app with UFJS
    * Show UF Screen Directives
    * Show UF Perspective Directives

* AngularJS App + UFJS client and UF Server.

  * 1 of 2 (3m58s).
    * Download UF War
    * Install and run on EAP
    * Download and run our Angular demo on Apache
    * Show AngularJS Routes + UF Integration
  * 2 of 2 (4m06s).
    * Use UF to create Dynamic Screens and Perspectives
    * Encapsulate an AngularJS template in a UF Screen
    * Show an AngularJS App (inside a UF screen) nested in a parent controller.
      * Demonstrated multiple levels of controller nesting.

* KIE UF Workbench RAD environment with AngularJS component.
* Uberfire Editor working seamlessly as an Eclipse editor.

For completeness the original video’s showing the JSFiddle inspired RAD environment, which demonstrates an UF first polyglot environment, have been added to the playlist. See point 4. above

Finally just to show of, and because we can, we added a bonus video demonstrating a UF editor component running seamlessly in Eclipse. This demonstrates the power of our component model – which has been designed to allow our components to work standalone in any environment. We use Errai to intercept all the RPC calls and bridge them to Eclipse. Because the virtual file system our editors use, like other services, is decoupled and abstracted we can adapt it to the Eclipse File io. For the end user the result is a seamless editor, that appears native. This allows the development of components that can work on the web and in Eclipse, or even IntelliJ. We’ll work on making this example public at a later date.

Here are some screenshots taken from the video’s

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/034dbbb3a864-OQh5eY6.png>)

(click image to enlarge)

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/c8ae63b65d35-Y7NRIw0.png>)

(click image to enlarge)

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/27ea6491e94f-krbL27k.png>)

(click image to enlarge)

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/ea27315e01e9-E75wwoq.png>)

(click image to enlarge)

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/2b3e38fd9251-NU1uGlk.png>)

(click image to enlarge)

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/264133310d2c-Hv2pmAh.png>)

(click image to enlarge)

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/ba3b497f3867-Q0CP5cu.png>)

(click image to enlarge)

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/14dd58ed8fb5-W9r05En.png>)

(click image to enlarge)

Finally to all those that said it couldn’t be done!!!!

[![](/legacy/assets/images/2018/02/faa24ec881e6-x9UoSTS.png)](</assets/images/2014/11/5cf3df5b0795-w8YXP7O.png>)