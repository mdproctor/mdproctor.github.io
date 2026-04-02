---
layout: post
title: "XMLUnit for xml assertions"
date: 2009-03-20
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/03/xmlunit-for-xml-assertions.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [XMLUnit for xml assertions](<https://blog.kie.org/2009/03/xmlunit-for-xml-assertions.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 20, 2009  
[General](<https://blog.kie.org/category/general>) [Article](<https://blog.kie.org/content_type/article>)

Thought i’d blog this little snippet. Was struggling with xml comparisons for unit testing, I initially tried [XMLUnit](<http://xmlunit.sourceforge.net/>) but found that it was too sensitive. After a bit of digging in the docs, I found how to configure it to be much more forgiving on element ordering, whitespace etc. Here is what I did, hopefully others will find this useful:
[code]
      
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
    
[/code]

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fxmlunit-for-xml-assertions.html&linkname=XMLUnit%20for%20xml%20assertions> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fxmlunit-for-xml-assertions.html&linkname=XMLUnit%20for%20xml%20assertions> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fxmlunit-for-xml-assertions.html&linkname=XMLUnit%20for%20xml%20assertions> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fxmlunit-for-xml-assertions.html&linkname=XMLUnit%20for%20xml%20assertions> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fxmlunit-for-xml-assertions.html&linkname=XMLUnit%20for%20xml%20assertions> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fxmlunit-for-xml-assertions.html&linkname=XMLUnit%20for%20xml%20assertions> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fxmlunit-for-xml-assertions.html&linkname=XMLUnit%20for%20xml%20assertions> "Email")