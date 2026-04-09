---
layout: post
title: "Drools Rule Templates"
date: 2008-08-26
author: Mark Proctor
categories: []
tags: []
original_url: https://blog.kie.org/2008/08/drools-rule-templates.html
---

Drools 5 sees the addition of a new feature – rule templates. Rule templates allow you to set up templates (!) that may then be merged with data. You can think of them as similar to decision tables but far more powerful. With Rule Templates the data is separated from the rule and there are no restrictions on which part of the rule is data-driven. So whilst you can do everything you could do in decision tables you can also do the following:

  * store your data in a database (or any other format)
  * conditionally generate rules based on the values in the data
  * use data for any part of your rules (e.g. condition operator, class name, property name)
  * run different templates over the same data

I find the best way to explain things is via example so over a few posts I will take you through three of the examples in the drools-examples project. The first shows how to achieve exactly the same functionality as a decision table using a rule template. The second example extends the first to include array fields and optional fields. The third gives an example of using a rule template with a different datasource – in this case Plain Old Java Objects (POJOs), and conditional templates.

The first example is SimpleRuleTemplateExample. We start with two files – the data and the template. In this case the data is the spreadsheet from an example you may be familiar with.

ExampleCheese.xls

> **📷 Missing image** — _cheese.PNG_

  
If this was a regular decision table there would be hidden rows before row 1 and between rows 1 and 2 containing rule metadata. With rule templates the data is completely separate from the rules. This has two handy consequences – you can apply multiple rule templates to the same data and your data is not tied to your rules at all. So what does the template look like?

Cheese.drt

```drl
1  template header2  age3  type4  log56
package org.drools.examples.templates;78
global java.util.List list;910 template "cheesefans"1112
rule "Cheese fans_@{row.rowNumber}"13 when14    Person(age == @{age})15    Cheese(type == "@{type}")16 then17    list.add("@{log}");18 end1920
end
template
```

Line 1: all rule templates start with “template header”  
Lines 2-4: following the header is the list of columns in the order they appear in the data. In this case we are calling the first column “age”, the second “type” and the third “log”.  
Lines 5: empty line signifying the end of the column definitions  
Lines 6-9: standard rule header text. This is standard rule DRL and will appear at the top of the generated DRL. Put the package statement and any imports and global definitions  
Line 10: The “template” keyword signals the start of a rule template. There can be more than one template in a template file. The template should have a unique name.  
Lines 11-18: The rule template – see below  
Line 20: “end template” signifies the end of the template.

The rule templates rely on MVEL to do substitution using the syntax @{token_name}. There is currently one built-in expression, @{row.rowNumber} which gives a unique number for each row of data and enables you to generate unique rule names. For each row of data a rule will be generated with the values in the data substituted for the tokens in the template. With the example data above the following rule file would be generated.

```drl
package org.drools.examples.templates;
global java.util.List list;
rule "Cheese fans_1"
when
Person(age == 42)  Cheese(type == "stilton")
then
list.add("Old man stilton");endrule "Cheese fans_2"
when
Person(age == 21)  Cheese(type == "cheddar")
then
list.add("Young man cheddar");
end
```

The code to run this is simple

```
//first we compile the spreadsheet with the template
//to create a whole lot of rules.
final ExternalSpreadsheetCompiler converter = new ExternalSpreadsheetCompiler();
//the data we are interested in starts at row 2, column 2 (e.g. B2)
final String drl = converter.compile(getSpreadsheetStream(), getRulesStream(), 2, 2);
```

We create an ExternalSpreadsheetCompiler object and use it to merge the spreadsheet with the rules. The two integer parameters indicate the column and row where the data actually starts – in our case column 2, row 2 (i.e. B2)