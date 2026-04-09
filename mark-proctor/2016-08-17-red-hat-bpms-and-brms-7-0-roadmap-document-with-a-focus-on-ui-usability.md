---
layout: post
title: "Red Hat BPMS and BRMS 7.0 Roadmap Document - With a Focus on UI Usability"
date: 2016-08-17
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2016/08/red-hat-bpms-and-brms-7-0-roadmap-document-with-a-focus-on-ui-usability.html
---

BPMS and BRMS 6.x put in a lot of foundations, but the UI aspects fell short in a number of areas with regards to maturity and usability.

In the last 4 years Red Hat has made considerable investment into the BPMS and BRMS space. Our engineering numbers have tripled, and so have our QE numbers. We also now have a number of User Experience and Design (UXD0 people, to improve our UI designs and usability.

The result is we hope the 7x series will take our product to a whole new level, with a much stronger focus on maturity and usability, now with the talent and bandwidth to deliver.

We had an internal review where we had to demonstrate how we were going to go about delivering a kick ass product in 7.0. I thought I would share, in this blog, what we produced, which is a roadmap document with a focus on UI Usability. The live version can be found at google docs, [here](<https://docs.google.com/document/d/1sJo7Z-Vaa-JE6NJk7wiWvwXCpic_S8ZdJg9KeOpCyNw/edit#>) – feel free to leave comments.

Enjoy :)

Mark  
BPMS and BRMS Platform Architect.

```drl
Other Links:
Drools 7.0 Happenings  (Includes videos)
Page and Form Builder Improvements (Video blog)
Security Management (Detailed blog on 7.0 improvements)
User and Group Management (Default blog on 7.0 improvements)
——–
```

## About This Document

This document presents the 7.0 roadmap with an eye on usability, in terms of where, how and who for. It is an aggressive and optimistic plan for 7.0 and it is fully expected that some items or a percentage of some items will eventually be pushed to 7.1, to ensure we can deliver close to time. Longer term 7.1 and onward items are not discussed or presented in this document, although it does touch on some of the items which would be raised as a result of reading this document – such as the “What’s not being improved” (for 7.0) section.

Wider field feedback remains limited, with a scarcity of specifics. This creates challenges in undertaking a more evidence based approach to planning, which can stand up strongly to scrutiny on all sides. However, engineering and UXD have been working with the field, primarily through Jim Tyrrell and Justin Holmes over the last year on this topic and this document represents the culmination of many discussions over the last year. As such it represents a good heuristic, based on the information and resources available to us at the time.

## Understanding Feedback from the Field

Broadly speaking, we have two types of customers:

  1. Those who want developers to use our product, often times embedded in their apps
  2. Those who want a cross-functional team to use our product

Generally speaking, we do quite well with customer 1, but we have a huge challenge with customer 2. The market has set a pretty clear expectation, on features and quality for targeted audiences, with IBM ODM and Pega’s BPM/Case Management. Almost every customer type 2 either has a significant deployment of these two competitors in place, or the decision maker has done significant work with these products in the past. Moreover, customer 2 is interested in larger, department or organization wide deployments. Customer 1 is usually interested on project level deployments.

Customer 2 is primarily upset with our authoring experience, both in eclipse and in Business Central. It is uncommon that customer 1 or 2 is upset with missing features or functions from our runtime (especially now that 6.3 has been released with a solid execution server and management function), and when she is, our current process to resolve these gaps works well. Therefore, the field feedback in this document (and our current process) is focused on the authoring experience. This isn’t to say other elements of the product are perfect, but simply an acknowledgement that we have limited time and energy and that the authoring experience is the most important barrier to success with customer 2.

The key issues that we have authoring side are fundamental (customer stories available here at request – some are a bit off color). Generally, these issues fall into 3 areas which are further enumerated in “Product Analysis and Planned Changes.”

  1. Lack of support for a team centric workflow – Functional
     1. See Asset Manager (we need to add detail here)
  2. Knowledge Asset Editors
     1. See BPMN2 designer (functional / reliable), decision table editor (usable) and data modeller (usable), forms (usable)
  3. Navigation between functions and layout of those functions in the design perspective
     1. See Design (Authoring perspective)
     2. Deepak – (usable/reliable)
     3. Aimee – Functional

## Introduction – The Product Maturity Model and what is Usability

Version 6.x has done well getting BRMS and BPMS to where it is today, with a strong revenue stream. The product maturity model (see image below) is a useful tool for discussing product improvements. It demonstrates that we are low on the model and need to mature and move up if we are to continue to improve sales. Too many aspects of the system, within the UI, may be considered neither functional (F), nor reliable (R), nor usable (U). The purpose of this document is to articulate a plan to address these issues, and in particular highlight the type of users the tool is being designed for and what they’ll be doing with it. The goal for 7.0 is to get as close to the “chasm” described in the model, with an aim to go beyond it as 7.x matures.

[![](/legacy/assets/images/2016/08/ceba79654025-egKdlu4vEiRP0AqA0c0_D99bGvjhtFe25eg-8Sb6MzeulWcKR3PKioCezGl6yn-3RhFSbG4khT9Y-rsh)](</assets/images/2016/08/639a74449fbe-zF37TiwsTB01sN-ktuWAeG1qlDTAOf_hFVZo_aUhQSpQiEQlDVsT3eCy.jpg>)

[Product Maturity Model](<https://sarasoueidan.com/blog/lessons-from-seductive-interaction-design-book/>)

When discussing usability it’s very important we understand whether we are talking about lack of features (F), too many or too serious defects (R) or poor UI design (U).

Quite often people report an issue as usability simply because they want to go from A to D, but get stuck at B or C. Either because the functionality is not there to complete the task, or it’s too buggy and they cannot progress. So while good UI design is important, we must balance our efforts across F, R and U to become usable – a focus on UI design only will not help usability, if the underlying product is neither reliable or functional. Commonly this is called Human Centered Design. By leveraging this common vocabulary, we can foster a more effective and inclusive dialogue with the wider team. So going forward, we are asking our stakeholders to employ the usability model presented here, and in particular the Functional, Reliable, Usable and Convenient terms.

## High Level Goal

A minimal viable product for case management is the main goal for 7.0. Case management provides a well defined end-to-end use case for product management, engineering and UXD. This is more than just adding another feature. When a user creates an end-to-end case management solution they will need to use most aspects of our system. Case management also has a clear set of target audiences (personas) for design UI and case worker UI. This allows us to identify both where and how and who for our “fit and finish” efforts are spent to improve things. Ensuring a strong directed focus on what we do and making it easier to communicate this, with hopefully a more realistic understanding of expectations from others within the organisation.

## High Level Plan

When considering the plan as a whole, the initial target user for 7.0, or persona, for the design ui is that of a casual or low skilled developer, who typically favours tooled (low code) environments where possible. See Deepak in Persons:

  * [Persona Presentation](<https://docs.google.com/presentation/d/1PDpl5BQOE6IHR96mDS5UQRB7hg_vGBNYOw5FOywBZ4Q/edit#slide=id.p4>)
  * [Persona Detailed Spec](<https://docs.google.com/document/d/1ib0EgPdVw2ApYROVew1YZOqHikHJe6d1tTzu_MIkIPw/edit>)
  * [Persona Quick Cards](<https://drive.google.com/folderview?id=0B-E5iaTCY4kVcm0yWDFlUnpNUTA&usp=sharing>)

Where possible and it makes sense, designs will be optimized for the less technical, citizen developers, of Aimee and Cameron [Personas](<https://docs.google.com/document/d/1ib0EgPdVw2ApYROVew1YZOqHikHJe6d1tTzu_MIkIPw/edit>). With either optional advanced functionality for Deepak or common denominator designs suitable for all personas. While

Citizen developers are not the primary focus for 7.0, it will become increasingly important and should ideally be targeted for 7.1 onwards, so it’s important as much as practically possible is done for this direction n 7.0. See [“The advent of the citizen developer”.](<http://www.zdnet.com/article/the-advent-of-the-citizen-developer/>)

Throughout this work, where possible and time permitting, designs will be put in place, either as alternative persona support or common denominator persona support for the, 

7.0 will primarily be focusing on all the components and parts that a Business Central user will come into contact with, while building a case management solution. For each of those areas we will try to have a sustained effort, over a long period of time to ensure depth and maturity, with UXD fully involved.

The aim for case management, the targeted components it uses and the Deepak persona is to achieve an acceptable level for functional, reliable and usable. For 7.1 we hope to look more holistically across the system and cross the chasm to become convenient. To become convenient we will need a strong effort in looking at the end-to-end user interaction using the system and trying to streamline all the steps they go through and making it easier and faster for them to achieve the goals they set out to achieve.

Detailed plans [here](<https://docs.google.com/document/d/1-fd7waz9vyndhdTanJFdP7cafahse5UAQHkAtjryzXA/edit>)

## Product Changes Done (6.3)

  * The whole business central was updated to PatternFly for v6.3. (See screenshots at end).
  * Execution server UI has been fully redesign with UXD involvement and great field feedback. (See screenshots at end).
    * “I want to congratulate you on the great work on the new kie server management features and UI. It’s surprisingly intuitive and does just what it needs to do. Keep up the good work!” (Justin Holmes, Business Automation Practice Lead).
  * The process runtime views have been augmented with the redesigned and newly integrated DashBuilder. They look great and have already had good feedback. (See screenshots at end).

## Product Analysis and Planned Changes

The 7.0 development cycle only started early/mid May, we do not yet have UXD input (wireframes/css/html) for every area. This UXD input will take time and will be produced incrementally across the product, throughout the 7.0 life cycle. What we do have, and is included below, where those efforts will be.

  * Design (Authoring perspective)
    * Problem:
      * The authoring perspective is designed for power users, and fails to work for less technical personas.
      * The project configuration works just like normal editors, which is confusing.
      * The project explorer mixes switching org/repo/project and navigation, which crowds the area. It’s also repository oriented.
      * Versioning, branching are too hard and commits do not squash, creating long unreadable logs for every small save.
    * Solution:
      * See UXD wire diagrams for most of what is described here, although there is still more to do.
      * Create new views for navigating projects, that is content and information oriented and more suitable for the casual coder and moving towards citizen developer. Make things project oriented.
      * Centralise project settings, and improve their reliability and usability.
  * Support for Collaborative Team Based Workflow
    * Problem:
      * Most customers using Business Central want it to support a team, which generally reflects the Deepak, Aimee, Paula and Cameron from our personas.
      * We have no clear workflow for changes to be approved and promoted in the team.
        * The asset manager (versioning and branch management) needs an overhaul. It is extremely confusing to the point of not being functional even for technical users. The current feature does weird branching/merging with git in a single repo, so it’s too technical for Aimee but confusing for Deepak as it doesn’t follow conventions.
        * The screens are way too small to be usable and the actual workflow can be quite confusing
        * The feature hasn’t been QE’d
      * The single git repository model can make integrating Business Central into a CI/CD flow complicated. It’s doable now that we have git hooks, but it is far from convenient. Give our strength in the CI/CD space, this needs to get to convenient.
    * Solution
      * Underlying changes going on for the cloud work (every user gets their own fork) will put in place the backside which will make this easier to progress. Exactly how we will improve the UXD here, to hide and simplify GIT has to be investigated. We have a hiring slot open for someone to focus on this area.
      * Will move to a repository per user. This will support a pull request type workflow in the tool between users.
      * Repo per user will simplify CI/CD
      * To be clear 7.0 will work to improve around the scope of what we have in 6x now, as we have limited time left for 7.0 on this now. With the aim of being minimally viable for deepak. It’s not clear how easy we can make this for aimee too. Likewise wider collaborative workflow, really needs to be considered future work, to avoid expectation problems.
  * BPMN Designer
    * Problem
      * The BPMN designer is the most important area in the product and also the area that gets the most complaints. These complaints are primarily about reliability, Oryx was inherited from an old community project (for time to market) and came with too much technical debt. There are lots of small details, which can detract from the overall experience.
      * Oryx is not testable and regressions happen with almost every fix, making it very hard and costly to stabilise.
    * Solution
      * Work with the Lienzo (a modern canvas library) community to build a new visio like tool, that can support BPMN2, and provide a commercial quality experience.
      * Have a strong focus on enabling testability.
      * Real time drawing of shapes and lines during drag. Including real time alignment and distribution guidelines and snap.
      * Proper orthogonal lines, with multipoint support, and heuristics to provide minimal number of turns for each line.
      * Reduced and more attractive property panels (designed by UXD) for each of the node types, focusing on hiding technical details and (also) targeting less technical users.
      * Change palette from accordion to vertical bar with fly-outs. Support standard and compact palettes.
    * Eclipse
      * To unify authoring experience across web and Eclipse, we are investigating using web-based modelling components inside of Eclipse, without the need for business-central or any other server. However this is a research topic and we are unable to promise anything. We plan to investigate decision tables first, as they are simpler, as they require a single view (and also use lienzo), which may make 7.0. If that goes well, we will look into the designer – but this is not planned for 7.0.
      * Until we have a supported Lienzo based BPMN2 designer for eclipse, we will continue to support and maintain the existing eclipse plug in. The existing items, such as project wizards, will remain and have support.
  * Administration/Settings
    * Problem:
      * Administration and settings are spread out in different locations and are neither consistent nor intuitive. In some cases, such as imports, they have been buggy.
    * Solution:
      * Centralise administrations and settings and ensure they are consistent and intuitive.
      * Ensure all administration and settings are reliable.
      * Work with UXD on improving designs.
        * Designs TBD.
  * Case Management
    * This does not exist yet, but UXD are involved. They have produced visionary documents, which go beyond what we can implement now, and are working with us to produce more incremental and simpler steps that we can achieve for 7.0
  * Decision Tables
    * Problem
      * There are not a lot of complaints about decision tables, other than they could be more attractive. The main issue is they are not functional compared to our competitors.
    * Solution
      * Focus the two Drools UI developers solely on decision tables and moving towards Decision Model and Notation, an OMG standard for decision tables that compliments BPMN2.
    * Must support tabular chaining (part of DMN spec), design time verification and validation and excel import/export.
    * Work with UXD to improve the aesthetics.
  * Reporting (DashBuilder)
    * Problem
      * Dashbuilder is already a mature and well featured product, with few complaints. However it came from Polymita and uses a different technology stack, which produces a design miss match – as it’s not PatternFly. Nor can its charts be easily integrated into other pages, which is necessary for process views and case management.
    * Solution
      * An effort has been going on for some time to port Dashbuilder to the same technology as the rest of the platform and adopt Pattern Fly. The results for this can already be seen in the improved jBPM process views for 6.3 and we should have full migration for 7.0
  * Forms
    * Problem
      * This is an inherited Polymita item which was written in a different technology stack and it never integrated well nor is it PatternFly, creating an impedance mismatch.
      * It has some powerful parts to it, but it’s layout capabilities are too limited, where users are restricted to new items in rows only. There is no row spanning, or grid like views.
    * Solution
      * A new effort has been going on for some time now that ports the forms to the same technology stack as the rest of the platform and adopt PatternFly.
      * We are focusing around a bootstrap grid layout system, to ensure we have intuitive and powerful layout capabilities. We have invested in a dynamic-grid system for bootstrap grids, to avoid the issue of having to design your layout first, as it’s hard to change after.
    * Working with UXD to redesign each of the editors for the form components.
  * Data Modeller
    * Problem
      * There are less complaints on this item than others, probably due to it’s more simplistic nature. But UXD have a number requests, to try and improve the overall experience anyway.
    * Solution
      * Support simple business types, optionally and in addition to java types.
    * i.e. number, string, currency, but we won’t lose the ability to use the Java types when required.
    * Layout changes and CSS improvements
    * Longer term we need a visual ERD/UML style modeller, but that will not happen for 7.0
  * Data Services/Management
    * This does not exist yet, but is necessary for case management to work end-to-end. It entails the system allowing data sources to be used, tables to be viewed and their data to be edited. More importantly it allows design time data driven components for forms.

## What’s Not being improved for 7.0

  * 7.1 will need to have a stronger focus on trying to become more convenient and pleasurable. This will require stronger focus on streamlining how the user uses the tool as a whole, making it easier and faster for them to get things done. Wizards and task oriented flows will be essential here, and general improved interaction design.
  * General
    * Refactoring
  * BRMS
    * Guided Editor
    * Scenario/Simulation
      * We hope to pick this up for 7.1 in 2017.
    * DSLs
  * BPMS
    * Redesign of the navigation
    * Major redesign of process instance list or task list (though adding features to support case management)
      * More focus on building custom case applications that can be tailored specifically to what the customer needs
  * Product Installer
  * It is unclear if the product team will be improving the usability of the installer and patching.
  * Product Portal and Download
    * It is unclear if the product team will be improving how product and patches are found.

## Other Notable Roadmap Work

  * Drools
    * Drools is currently focusing on trying to enable multi-core scalability for CEP use cases and also high availability for CEP use cases. There is also ongoing longer term research into pojo-rules and a drl replacement (will most likely be a superset of java).
  * jBPM
    * Horizontal scaling for the cloud is the main focus for jBPM and represents a number of challenges for jBPM, related to how processes running on different services work with each other, as well as how signals and messages are routed and information collected and aggregated.
  * OptaPlanner
    * Horizontal scaling through Partitioned Search is the main focus for OptaPlanner.

## Organisational Changes Done and Ongoing

  * The group is now focusing engineers for longer periods of time to specific parts of the product. This will bring about depth and maturity to those areas the engineers work on.
    * 6.x focus was on rapid breadth expansion of features. This gave time to market, which allowed the revenue growth we have, but comes with the pains we have now. The shift to depth will help address this.
  * Migrating to PatternFly
    * Allows engineering and UXD to be more fully engaged. Ensures our product is consistent with all other Red Hat products. Allow Business Central to leverage ongoing research from the PatternFly team.
  * UXD team has increased from 1 person to 2.5. With one person dedicated to providing HTML and CSS to developers.
  * Usability testing of primary workflows and new features with participants representing target Personas for the given workflows/features.
  * The field has become and continues to become more engaged, via the [BPM and BRMS Community of Practice](<https://mojo.redhat.com/groups/brms-community-of-practice>) initiative, and in particular Justin Holmes and Jim Tyrell’s involvement.
    * They have attended multiple team meetings now, and provide constant feedback and guidance. This has been invaluable.
    * The field engages with UXD in a twice monthly meeting, which lead the effort in developing Personas. These design tools provide a structure to discussions about who our users are and what we need to build in order to make them happy. Today, these personas are all focused on the design/authoring experience, as this is currently the field’s biggest perceived gap in features and we want to focus our effort as much as possible.
    * Jim Tyrrell is proposing to lead a regular field UXD review, to review any changes going on in community, as they happen. This effort should be scheduled to be done every 3 weeks or so.
    * We also should think about bringing in System Integrator Consulting Partners to help with designing our offering.
    * Engineering releases of the product are being consumed by SA’s and Consultants in order to do exploratory testing before GA.
  * More continuous sustaining effort: organisational and planning changes to support a continuous effort on improving the quality of the platform across the board. Rather than continuous switching of developer’s focus or postponing bug fixing towards the end of the cycle, there should be a continuous effort to fix known issues (large and small) to improve the overall quality and experience. Currently set at 20% on average across the team (where some developers are much more focused on sustaining than others).
  * The documentation team have agreed to move to the same tooling (asciidoc) and content source (git repo) as engineering. This should make it easier for them to stay in sync and add value.
    * For 6.x and prior the documentation team had been silo’d before and using a completely different tool chain and document source. They were unable to effectively track community docs, meaning that products docs were lagging behind, as well as lacking content and often wrong. This means the product docs devalued the product, compared to community. We would typically hear field people say they wish they could just show community docs to customers, rather than product docs – this is a situation that cannot be allowed to continue.
  * A subcontractor has been hired to assist with user guide and getting started documentation in a tutorial format, as well as installation and setup – to improve the onboarding experience. This work is currently focused on 6x, but it will be updated to 7.0 towards the end of the project life cycle.
  * QE are now working far more closely with engineering, adding tests upstream into community, ensuring they run earlier and regressions found faster. We have also been working to embed the QE team within engineering, so that there is a greater communication and thus understanding and collaboration between engineering and QE (which did not happen on 6x or earlier).
  * We have greatly improved our PR process. With gatekeepers and an insistence that all code now, backend and frontend is reviewed for tests. 6x has no community provided UI tests, this is no longer the case for 7x.
  * We have also improved our CI/CD situation.

## 6.3 Improvement Images

### Execution Server

[![](/legacy/assets/images/2016/08/1855c227dc60-8qtS_SR82eI_sEq_VxBnroE5BIOYZL0X5ep74DkSvwzqk6_8viQLxnPXN9cVpET1tTI3nbvcgfiYfPrz)](</assets/images/2016/08/40143f2bdb7a-TwRXEffuh10nn84HnprmDDOvfqv_JASYGmp2h2xJ9m08fMN2zThvfDQB.png>)

### Data Modeller (Before and After)

[![](/legacy/assets/images/2016/08/c8f4f61efea4-F7JZ6iK02pkS2NLEZ7Cod031D84U0IColSW-f52KvFjPg7-EinTX1tO5ctu-BSt7PSe29stTajjcTXHm)](</assets/images/2016/08/1356f379f1ce-jhD-beiuvexNwflg-ibkbc_B8HjZarMATrZA-fR-_flw0r-CjvZDk-qr.png>)

[![](/legacy/assets/images/2016/08/a087444d3fbc-SNLl4WN7lC_MuiFOYYv1g8es1Dhp0Jix509CcpQOhDTdA7ycrclUFtDbgTwJYeOmdXsYccuRqtAdyfBJ)](</assets/images/2016/08/414367f66391-0MGuRVmYaZBVfA5KuDADcKupNzpMtCp9kzXO651D2wEHMTqzowCytKmC.png>)

### jBPM Runtime Views (Before and After)

[![](/legacy/assets/images/2016/08/b9535f7d3299-29vDZ399wka_KePqPoYgB6TGFOLeHzCX0aQomJbOlYIHeP00vZz3vqKyoKw8iIdR8yRAlbH963tCzR27)](</assets/images/2016/08/f5f427f855dd-cZTbqk_mNen1Ocd_YKbdY7u6rjdIzf-KIGS8Vhm_Hol4Gvrv8jdRZlPs.png>)

[![](/legacy/assets/images/2016/08/9258e0ed01ef-GsQo6lPNmdsE3TOB2rmqM4J64r2fx23OBVD0Rx4fC9dxkeh4P8bUuqF_gYtCPgKeFsDTgfXd6oFvvdBx)](</assets/images/2016/08/a257c7bc6729-AZhKrQEqi5eJAoNEM-103Ii-Hkvu3mx_kE8rVJGgPfle9FSydgWDg0jU.png>)