---
layout: post
title: "XMLUnit for xml assertions"
date: 2009-03-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/03/xmlunit-for-xml-assertions.html
---

Thought i’d blog this little snippet. Was struggling with xml comparisons for unit testing, I initially tried [XMLUnit](<http://xmlunit.sourceforge.net/>) but found that it was too sensitive. After a bit of digging in the docs, I found how to configure it to be much more forgiving on element ordering, whitespace etc. Here is what I did, hopefully others will find this useful:

```java
protected void setUp() throws Exception {
        XMLUnit.setIgnoreComments( true );
        XMLUnit.setIgnoreWhitespace( true );
        XMLUnit.setIgnoreAttributeOrder( true );
        XMLUnit.setNormalizeWhitespace( true );
        XMLUnit.setNormalize( true );
    }

    private void assertXMLEqual(String expectedXml,
                                String resultXml) {
        try {
            Diff diff = new Diff( expectedXml,
                                  resultXml );
            diff.overrideElementQualifier( new RecursiveElementNameAndTextQualifier() );
            XMLAssert.assertXMLEqual( diff,
                                      true );
        } catch ( Exception e ) {
            throw new RuntimeException( "XML Assertion failure",
                                        e );
        }
    }
```