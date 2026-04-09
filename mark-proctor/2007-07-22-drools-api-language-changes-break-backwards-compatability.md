---
layout: post
title: "Drools api/language changes break backwards compatability"
date: 2007-07-22
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2007/07/drools-api-language-changes-break-backwards-compatability.html
---

I’ve had a few people mention their unhappiness with the lack of backwards compatible in 4.0 to 3.0.

Yes I do apologise about the changes, but I do feel that if we want to progress towards the best engine, it can’t be helped – I do offer to assist the community in developing backward compatible wrappers, or upgrade scripts, no one ever volunteers.

2.0 really had to be scrapped, it just wasn’t a real expert system language – a compatibility layer could have been written and we put up [details](<http://wiki.jboss.org/wiki/Wiki.jsp?page=Drools2Migration>) on how to get started on this, but no one was interested.

3.0 was a total rewrite for a “proper” expert system, but time constraints and limited understanding meant some compromises where made. With 4.0 we had the opportunity to get this all right and I now believe we have the best declarative rule language, bar none, a language that we can live with and extend for some time.

There are a number of changes that will cause 3.0 upgrade problems, I detailed these in email 3 times and also a [blog entry](<http://blog.athico.com/2007/06/api-and-language-changes.html>). We also do regular milestone releases, so people can see what we are doing, and document the backward comparability issues in the release notes. I only got one feedback saying “go for it”. Again I [blogged](<http://blog.athico.com/2007/06/drools-v3to4-update-tool-edson-tirelli.html>) and emailed about the start of an upgrade script, zero interest of volunteers from the community.

We want to make the best rule engine/language if we break something, it’s because something isn’t right; to live with that will be, longer term, strategically worse than breaking it now.

To give you an idea of this decision making consider in 3.0 we auto-boxed all primitives (as we couldn’t handle primitives directly) and didn’t auto-unbox – this was an ugly situation – so people had to handle all their own unboxing. Now in 4.0 we handle primitives directly, allowing people to write cleaner code; however all the manual unboxing they did will now be bust; which in many code bases is considerable.

So we have a choice we can keep a really ugly limitation of 3.0, or we can break it in 4.0 (hence the major number change) and get it right which results in much cleaner rules. For me the choice was clear, break 3.0. There is also the argument that all breakages should be “deprecated” and switches added to enable legacy execution – which is what some commercial firms do – this is an expensive undertaking and we simply don’t have the resources we are a small team and rely on community involvement. If we continue to build up layers of cruft for legacy support, we simply won’t be able to innovate at the pace we do. I prefer instead to create upgrade paths which is absolutely feasible, and zero impact on the main codebase; however as I mentioned previously people only want to complain about the changes, and not do anything to assist in making it work, which is a shame :(

When 4.0 final comes out and suddenly all these users that don’t read my blog, don’t read the mailing lists, don’t participate in the community try and upgrade and realises it breaks there systems they are going to give us stick for it; probably publicly in various forums. I hope those reading those forum postings can point them here and to the upgrade script we want to build and encourage them to help solve this.

We will work on those scripts, and they will get better over time, but if we want those fixed quickly we need your help.