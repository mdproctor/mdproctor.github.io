---
layout: post
title: "Marshalling with MVEL"
date: 2009-03-14
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2009/03/marshalling-with-mvel.html
---

[![](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)](<https://blog.kie.org/category/all?search_authors=3>)

### [Marshalling with MVEL](<https://blog.kie.org/2009/03/marshalling-with-mvel.html>)

by [Mark Proctor](<https://blog.kie.org/category/all?search_authors=3> "Posts by Mark Proctor") \- March 14, 2009  
[Rules](<https://blog.kie.org/category/rules>) [Article](<https://blog.kie.org/content_type/article>)

Till now MVEL was only able to read in MVEL data structures, not marshall them out to a string, stopping MVEL from being used as a marshalling format. I needed something different to do for a day so I wrote a quick MVEL marshaller, that takes a pojo structure and writes it out as an MVEL statement. It’s only a small bit of code and while spiking it I’ve left it in the main test class, so you can see everything currently here in [MarshallingTest.](<http://fisheye.codehaus.org/browse/mvel/trunk/src/test/java/org/mvel2/marshalling/MarshallingTest.java?r=2344>) testMVEL shows it working, there is a testXStream so you can compare it, there is a counter so you can do perf comparisons. We could probably speed it up some more if we use code generation instead of reflection.

This shows the code that generates the original pojo structure:
[code]
    Pet pet = new Pet();  
    pet.setName( "rover" );  
    pet.setAge( 7 );  
    List list = new ArrayList();  
    list.add( "a" );  
    list.add( 12 );  
    list.add( new SomeNumers( 10.02f, 22.02, 5, 100l, new BigDecimal( 23.0234d, MathContext.DECIMAL128 ), new BigInteger( "1001" ) ) );  
    list.add( new Date() );  
    list.add( new Cheese( "cheddar", 6 ) );  
      
    pet.setList( list );  
    pet.setArray( new int[]{1, 2, 3} );  
      
    Map map = new HashMap();  
    map.put( "key1", 13 );  
    map.put( "key3", "value3" );  
    map.put( "key2", 15 );  
    map.put( "key4", new Cheese( "stilton", 11 ) );  
      
    Person person = new Person();  
    person.setName( "mark" );  
    person.setAge( 33 );  
    person.setPet( pet );  
    person.setSomeDate( new Date() );  
    person.setMap( map );  
    Calendar cal = Calendar.getInstance();  
    cal.setTime( new Date() );  
    person.setCal( cal );
[/code]

Which generates the following MVEL statement:
[code]
    new org.mvel2.marshalling.MarshallingTest$Person().{ age = 33, cal =   
    with ( java.util.Calendar.getInstance() ) { time = new   
    java.util.Date(1237047853121)} , map = [ 'key1':13, 'key3':'value3',   
    'key2':15, 'key4':new org.mvel2.marshalling.MarshallingTest$Cheese().{   
    age = 11, edible = false, type = 'stilton' } ] , name = 'mark', nullTest   
    = null, pet = new org.mvel2.marshalling.MarshallingTest$Pet().{ age = 7,   
    array = { 1, 2, 3 } , list = [ 'a', 12, new   
    org.mvel2.marshalling.MarshallingTest$SomeNumers().{ ABigDecimal =   
    23.02339999999999875512912694830447, ABigInteger = 1001, ADouble =   
    22.02, AFloat = 10.02, AInt = 5, ALong = 100 }, new   
    java.util.Date(1237047853046), new   
    org.mvel2.marshalling.MarshallingTest$Cheese().{ age = 6, edible =   
    false, type = 'cheddar' } ] , name = 'rover' }, someDate = new   
    java.util.Date(1237047853121) }
[/code]

Which is a lot nicer than XML or JSON, we can improve this further if we add imports to avoid fully qualifying every Class and add a nice pretty printer :)

## Author

  * ![Mark Proctor](/legacy/assets/images/2016/04/61679b3b11ac-AOh14GgyKgCXknk1MzNYO1vGnqPuxeuitj4L4ipj61r3lA_s96-c)

[Mark Proctor](<https://blog.kie.org/author/mdproctor> "Mark Proctor")

[ View all posts ](<https://blog.kie.org/author/mdproctor> "View all posts") [ ](<mailto:mdproctor@gmail.com>)

[](<https://www.addtoany.com/add_to/copy_link?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fmarshalling-with-mvel.html&linkname=Marshalling%20with%20MVEL> "Copy Link")[](<https://www.addtoany.com/add_to/linkedin?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fmarshalling-with-mvel.html&linkname=Marshalling%20with%20MVEL> "LinkedIn")[](<https://www.addtoany.com/add_to/twitter?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fmarshalling-with-mvel.html&linkname=Marshalling%20with%20MVEL> "Twitter")[](<https://www.addtoany.com/add_to/facebook?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fmarshalling-with-mvel.html&linkname=Marshalling%20with%20MVEL> "Facebook")[](<https://www.addtoany.com/add_to/reddit?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fmarshalling-with-mvel.html&linkname=Marshalling%20with%20MVEL> "Reddit")[](<https://www.addtoany.com/add_to/tumblr?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fmarshalling-with-mvel.html&linkname=Marshalling%20with%20MVEL> "Tumblr")[](<https://www.addtoany.com/add_to/email?linkurl=https%3A%2F%2Fblog.kie.org%2F2009%2F03%2Fmarshalling-with-mvel.html&linkname=Marshalling%20with%20MVEL> "Email")