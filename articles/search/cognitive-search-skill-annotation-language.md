---
title: Skill context and input annotation reference language
titleSuffix: Azure AI Search
description: Annotation syntax reference for annotation in the context, inputs, and outputs of a skillset in an AI enrichment pipeline in Azure AI Search.

author: BertrandLeRoy
ms.author: beleroy
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: reference
ms.date: 08/20/2024
---
# Skill context and input annotation language

This article is the reference documentation for skill context and input syntax. It's a full description of the expression language used to construct paths to nodes in an enriched document.

Azure AI Search skills can use and [enrich the data coming from the data source and from the output of other skills](cognitive-search-defining-skillset.md).
The data working set that represents the current state of the indexer work for the current document starts from the raw data coming from the data source and is
progressively enriched with each skill iteration's output data.
That data is internally organized in a tree-like structure that can be queried to be used as skill inputs or to be added to the index.
The nodes in the tree can be simple values such as strings and numbers, arrays, or complex objects and even binary files.
Even simple values can be enriched with additional structured information.
For example, a string can be annotated with additional information that is stored beneath it in the enrichment tree.
The expressions used to query that internal structure use a rich syntax that is detailed in this article.
The enriched data structure can be [inspected from debug sessions](cognitive-search-debug-session.md).
Expressions querying the structure can also be tested from debug sessions.

Throughout the article, we'll use the following enriched data as an example.
This data is typical of the kind of structure you would get when enriching a document using a skillset with [OCR](cognitive-search-skill-ocr.md), [key phrase extraction](cognitive-search-skill-keyphrases.md), [text translation](cognitive-search-skill-text-translation.md), [language detection](cognitive-search-skill-language-detection.md), and [entity recognition](cognitive-search-skill-entity-recognition-v3.md) skills, as well as a custom tokenizer skill.

|Path|Value|
|---|---|
|`document`||
|&emsp;`merged_content`|"Study of BMN 110 in Pediatric Patients"...|
|&emsp;&emsp;`keyphrases`||
|&emsp;&emsp;&emsp;`[0]`|"Study of BMN"|
|&emsp;&emsp;&emsp;`[1]`|"Syndrome"|
|&emsp;&emsp;&emsp;`[2]`|"Pediatric Patients"|
|&emsp;&emsp;&emsp;...||
|&emsp;&emsp;`locations`||
|&emsp;&emsp;&emsp;`[0]`|"IVA"|
|&emsp;&emsp;`translated_text`|"Étude de BMN 110 chez les patients pédiatriques"...|
|&emsp;&emsp;`entities`||
|&emsp;&emsp;&emsp;`[0]`||
|&emsp;&emsp;&emsp;&emsp;`category`|"Organization"|
|&emsp;&emsp;&emsp;&emsp;`subcategory`|`null`|
|&emsp;&emsp;&emsp;&emsp;`confidenceScore`|0.72|
|&emsp;&emsp;&emsp;&emsp;`length`|3|
|&emsp;&emsp;&emsp;&emsp;`offset`|9|
|&emsp;&emsp;&emsp;&emsp;`text`|"BMN"|
|&emsp;&emsp;&emsp;...||
|&emsp;&emsp;`organizations`||
|&emsp;&emsp;&emsp;`[0]`|"BMN"|
|&emsp;&emsp;`language`|"en"|
|&emsp;`normalized_images`||
|&emsp;&emsp;`[0]`||
|&emsp;&emsp;&emsp;`layoutText`|...|
|&emsp;&emsp;&emsp;`text`||
|&emsp;&emsp;&emsp;&emsp;`words`||
|&emsp;&emsp;&emsp;&emsp;&emsp;`[0]`|"Study"|
|&emsp;&emsp;&emsp;&emsp;&emsp;`[1]`|"of"|
|&emsp;&emsp;&emsp;&emsp;&emsp;`[2]`|"BMN"|
|&emsp;&emsp;&emsp;&emsp;&emsp;`[3]`|"110"|
|&emsp;&emsp;&emsp;&emsp;&emsp;...||
|&emsp;&emsp;`[1]`||
|&emsp;&emsp;&emsp;`layoutText`|...|
|&emsp;&emsp;&emsp;`text`||
|&emsp;&emsp;&emsp;&emsp;`words`||
|&emsp;&emsp;&emsp;&emsp;&emsp;`[0]`|"it"|
|&emsp;&emsp;&emsp;&emsp;&emsp;`[1]`|"is"|
|&emsp;&emsp;&emsp;&emsp;&emsp;`[2]`|"certainly"|
|&emsp;&emsp;&emsp;&emsp;&emsp;...||
|&emsp;&emsp;&emsp;&emsp;...
|&emsp;&emsp;...||

## Document root

All the data is under one root element, for which the path is `"/document"`. The root element is the default context for skills.

## Simple paths

Simple paths through the internal enriched document can be expressed with simple tokens separated by slashes.
This syntax is similar to [the JSON Pointer specification](https://datatracker.ietf.org/doc/html/rfc6901.html).

### Object properties

The properties of nodes that represent objects add their values to the tree under the property's name.
Those values can be obtained by appending the property name as a token separated by a slash:

|Expression|Value|
|---|---|
|`/document/merged_content/language`|`"en"`|

Property name tokens are case-sensitive.

### Array item index

Specific elements of an array can be referenced by using their numeric index like a property name:

|Expression|Value|
|---|---|
|`/document/merged_content/keyphrases/1`|`"Syndrome"`|
|`/document/merged_content/entities/0/text`|`"BMN"`|

### Escape sequences

There are two characters that have special meaning and need to be escaped if they appear in an expression and must be interpreted as is instead of as their special meaning: `'/'` and `'~'`.
Those characters must be escaped respectively as `'~0'` and `'~1'`. 

## Array enumeration

An array of values can be obtained using the `'*'` token:

|Expression|Value|
|---|---|
|`/document/normalized_images/0/text/words/*`|`["Study", "of", "BMN", "110" ...]`|

The `'*'` token doesn't have to be at the end of the path. It's possible to enumerate all nodes matching a path with a star in the middle or with multiple stars:

|Expression|Value|
|---|---|
|`/document/normalized_images/*/text/words/*`|`["Study", "of", "BMN", "110" ... "it", "is", "certainly" ...]`|

This example returns a flat list of all matching nodes.

It's possible to maintain more structure and get a separate array for the words of each page by using a `'#'` token instead of the second `'*'` token:

|Expression|Value|
|---|---|
|`/document/normalized_images/*/text/words/#`|`[["Study", "of", "BMN", "110" ...], ["it", "is", "certainly" ...] ...]`|

The `'#'` token expresses that the array should be treated as a single value instead of being enumerated.

### Enumerating arrays in context

It's often useful to process each element of an array in isolation and have a different set of skill inputs and outputs for each.
This can be done by setting the context of the skill to an enumeration instead of the default `"/document"`.

In the following example, we use one of the input expressions we used before, but with a different context that changes the resulting value.

|Context|Expression|Values|
|---|---|---|
|`/document/normalized_images/*`|`/document/normalized_images/*/text/words/*`|`["Study", "of", "BMN", "110" ...]`<br/>`["it", "is", "certainly" ...]`<br>...|

For this combination of context and input, the skill gets executed once for each normalized image: once for `"/document/normalized_images/0"` and once for `"/document/normalized_images/1"`. The two input values corresponding to each skill execution are detailed in the values column.

When enumerating an array in context, any outputs the skill produces will also be added to the document as enrichments of the context.
In the above example, an output named `"out"` has its values for each execution added to the document respectively under `"/document/normalized_images/0/out"` and `"/document/normalized_images/1/out"`.

## Literal values

Skill inputs can take literal values as their inputs instead of dynamic values queried from the existing document. This can be achieved by prefixing the value with an equal sign. Values can be numbers, strings or Boolean.
String values can be enclosed in single `'` or double `"` quotes.

|Expression|Value|
|---|---|
|`=42`|`42`|
|`=2.45E-4`|`0.000245`|
|`="some string"`|`"some string"`|
|`='some other string'`|`"some other string"`|
|`="unicod\u0065"`|`"unicode"`|
|`=false`|`false`|

### In line arrays

If a certain skill input requires an array of data, but the data is represented as a single value currently or you need to combine multiple different single values into an array field, then you can create an array value inline as part of a skill input expression by wrapping a comma separated list of expressions in brackets (`[` and `]`). The array value can be a combination of expression paths or literal values as needed. You can also create nested arrays within arrays this way.

|Expression|Value|
|---|---|
|`=['item']`|["item"]|
|`=[$(/document/merged_content/entities/0/text), 'item']`|["BMN", "item"]|
|`=[1, 3, 5]`|[1, 3, 5]|
|`=[true, true, false]`|[true, true,  false]|
|`=[[$(/document/merged_content/entities/0/text), 'item'],['item2', $(/document/merged_content/keyphrases/1)]]`|[["BMN", "item"], ["item2", "Syndrome"]]|

If the skill has a context that explains to run the skill per an array input (that is, how `"context": "/document/pages/*"` means the skill runs once per "page" in `pages`) then passing that value as the expression as input to an in line array uses one of those values at a time. 

For an example with our sample enriched data, if your skill's `context` is `/document/merged_content/keyphrases/*` and then you create an inline array of the following `=['key phrase', $(/document/merged_content/keyphrases/*)]` on an input of that skill, then the skill is executed three times, once with a value of ["key phrase", "Study of BMN"], another with a value of ["key phrase", "Syndrome"], and finally with a value of ["key phrase", "Pediatric Patients"]. The literal "key phrase" value stays the same each time, but the value of the expression path changes with each skill execution.

## Composite expressions

It's possible to combine values together using unary, binary, and ternary operators.
Operators can combine literal values and values resulting from path evaluation.
When used inside an expression, paths should be enclosed between `"$("` and `")"`.

### Boolean not `'!'`

|Expression|Value|
|---|---|
|`=!false`|`true`|

### Negative `'-'`

|Expression|Value|
|---|---|
|`=-42`|`-42`|
|`=-$(/document/merged_content/entities/0/offset)`|`-9`|

### Addition `'+'`

|Expression|Value|
|---|---|
|`=2+2`|`4`|
|`=2+$(/document/merged_content/entities/0/offset)`|`11`|

### Subtraction `'-'`

|Expression|Value|
|---|---|
|`=2-1`|`1`|
|`=$(/document/merged_content/entities/0/offset)-2`|`7`|

### Multiplication `'*'`

|Expression|Value|
|---|---|
|`=2*3`|`6`|
|`=$(/document/merged_content/entities/0/offset)*2`|`18`|

### Division `'/'`

|Expression|Value|
|---|---|
|`=3/2`|`1.5`|
|`=$(/document/merged_content/entities/0/offset)/3`|`3`|

### Modulo `'%'`

|Expression|Value|
|---|---|
|`=15%4`|`3`|
|`=$(/document/merged_content/entities/0/offset)%2`|`1`|

### Less than, less than or equal, greater than and greater than or equal `'<'` `'<='` `'>'` `'>='`

|Expression|Value|
|---|---|
|`=15<4`|`false`|
|`=4<=4`|`true`|
|`=15>4`|`true`|
|`=1>=2`|`false`|

### Equality and nonequality `'=='` `'!='`

|Expression|Value|
|---|---|
|`=15==4`|`false`|
|`=4==4`|`true`|
|`=15!=4`|`true`|
|`=1!=1`|`false`|

### Logical operations and, or and exclusive or `'&&'` `'||'` `'^'`

|Expression|Value|
|---|---|
|`=true&&true`|`true`|
|`=true&&false`|`false`|
|`=true||true`|`true`|
|`=true||false`|`true`|
|`=false||false`|`false`|
|`=true^false`|`true`|
|`=true^true`|`false`|

### Ternary operator `'?:'`

It's possible to give an input different values based on the evaluation of a Boolean expression using the ternary operator.

|Expression|Value|
|---|---|
|`=true?"true":"false"`|`"true"`|
|`=$(/document/merged_content/entities/0/offset)==9?"nine":"not nine"`|`"nine"`|

### Parentheses and operator priority

Operators are evaluated with priorities that match usual conventions: unary operators, then multiplication, division and modulo, then addition and subtraction, then comparison, then equality, and then logical operators.
Usual associativity rules also apply.

Parentheses can be used to change or disambiguate evaluation order.

|Expression|Value|
|---|---|
|`=3*2+5`|`11`|
|`=3*(2+5)`|`21`|

## See also
+ [Create a skillset in Azure AI Search](cognitive-search-defining-skillset.md)
+ [Reference enrichments in an Azure AI Search skillset](cognitive-search-concept-annotations-syntax.md)
