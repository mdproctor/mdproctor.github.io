---
layout: post
title: "Guvnor - Recent improvements"
date: 2012-03-15
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2012/03/guvnor-recent-improvements.html
---

### Guvnor – Recent improvements

Other than a sighting at the London BRMS 2012 event last week it would appear I have been somewhat quiet in recent weeks. This, it can be argued, is a good thing ;)

However I’ve just finished a couple of improvements to Guvnor for CR1 I thought it worth telling you about:-

Improved numeric data-type handling  
  
To be honest, numerical data-types in Guvnor have not been supported that well in the past. The best you’d get, to edit such values, was a text box that had very limited restriction on what could be entered. This was largely because the heart of Guvnor used to drive most of the editors was only aware of a generic “numerical” type.

With a little bit of blood, sweat and tears this has now been improved to differentiate between all of Java’s primitive numerical types (byte, short, integer, long, double and float) together with BigDecimal and BigInteger. When adding a numerical field to a rule you now get an editor relevant for the type with more strict validation.

[![](/legacy/assets/images/2012/03/a7029a8d8088-guvnor-numeric-value-editors.png)](</assets/images/2012/03/af62f1410ee6-guvnor-numeric-value-editors.png>)

DRL generation has subsequently been improved to ensure the distinction between numerical sub-types is rendered correctly (most notably the treatment of BigDecimal and BigInteger in the right-hand-side of a rule for Java or MVEL dialects).

**MVEL DRL example**

```drl
rule “brl”
dialect “mvel”
when
  $c : Container( )
then
  $c.setBi( 35352324242424242424I );
  $c.setBd( 4343.3434344343B );
  update( $c );
end
```

**Java DRL example**

```drl
rule “brl”
dialect “java”
when
  $c : Container( )
then
  $c.setBi( new java.math.BigInteger(“35352324242424242424”) );
  $c.setBd( new java.math.BigDecimal(“4343.3434344343”) );
  update( $c );
end
```

  
Dependent enumerations  
  
Dependent enumerations are now available to the Web Guided Decision Table editor in Guvnor. A dependent enumeration is one whose values depend upon the value of another (parent) enumeration. Examples include ContinentCountryRegion, ManufacturerProduct etc.

Dependent enumerations are available to both Extended Entry and Limited Entry tables; together with appropriate expansion when generating an expanded form table.

[![](/legacy/assets/images/2012/03/837ec9d020e6-dtable-dependent-enums.png)](</assets/images/2012/03/3a576447bbc4-dtable-dependent-enums.png>)

Dependent enumerations also function in the BRL Rule Editor and Rule Templates.

For those wanting to see dependent enumerations in action and can’t wait for CR1 here’s a quick video demonstrating them: The dependent enumerations are shown first, then a new expanded form decision table is generated before being edited.

[![vimeo embed](/legacy/assets/images/2012/03/4a0e70c4f03e-265611834-b32236200fa043204913016dc7161ead20cb8a877e95e0d0ea4473d1ac14ac45-d_640)  
Watch on Vimeo](<https://vimeo.com/38576157>)

A couple of regressions were noticed by a vigilant community user (thanks Nicolas Héron) and have been subsequently fixed. The changes for both enhancements have been extensive hence I would urge you to download and try CR1, when it becomes available, so anything else untoward can be squashed before 5.4.0.Final.

Enjoy.