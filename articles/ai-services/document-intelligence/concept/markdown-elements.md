---
title: Document Intelligence supported Markdown elements
titleSuffix: Foundry Tools
description: Description of the supported Markdown elements returned as part of the Layout API response and how to use the response in your applications.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar

---

# Understanding Document Intelligence Layout API Markdown Output Format

Azure Document Intelligence in Foundry Tools Layout API can transform your documents into rich Markdown, preserving their original structure and formatting. Just specify `outputContentFormat=markdown` in your request to receive semantically structured content that maintains paragraphs, headings, tables, and other document elements in their proper hierarchy.

This Markdown output elegantly captures the document's original organization while providing standardized, easily consumable content for downstream applications. The preserved semantic structure enables more sophisticated document processing workflows without losing the context and relationships between document elements.


## Markdown elements supported in Layout Analysis

The following Markdown elements are included in Layout API responses:

* Paragraph
* Heading
* Table
* Figure
* Selection Mark
* Formula
* Barcode
* PageNumber/PageHeader/PageFooter
* PageBreak
* KeyValuePairs/Language/Style
* Spans and Content

### Paragraph

Paragraphs represent cohesive blocks of text that belong together semantically. The Layout API maintains paragraph integrity by:

* Preserving paragraph boundaries with empty lines between separate paragraphs
* Using line breaks within paragraphs to maintain the visual structure of the original document
* Maintaining proper text flow that respects the original document's reading order

Here's an example:

``` md
This is paragraph 1.
This is still paragraph 1, even if in another Markdown line.

This is paragraph 2. There is a blank line between paragraph 1 and paragraph 2.
```
---

### Heading

Headings organize document content into a hierarchical structure to make navigation and understanding easier. The Layout API has the following capabilities:

* Uses standard Markdown heading syntax with 1-6 hash symbols (#) corresponding to heading levels.
* Maintains proper spacing with two blank lines before each heading for improved readability.

Here's an example:

``` md
# This is a title

## This is heading 1

### This is heading 2

#### This is heading 3
```

---

### Table

Tables preserve complex structured data in a visually organized format. The Layout API uses HTML table syntax for maximum fidelity and compatibility:

* Implements full HTML table markup (`<table>`, `<tr>`, `<th>`, `<td>`) rather than standard Markdown tables
* Preserves merged cell with HTML rowspan and colspan attributes.
* Preserves table captions with the `<caption>` tag to maintain document context
* Handles complex table structures including headers, cells, and footers
* Maintains proper spacing with two blank lines before each table for improved readability
* Preserves table footnotes as separate paragraph following the table

Here's an example:

``` md
<table>
<caption>Table 1. This is a demo table</caption>
<tr><th>Header</th><th>Header</th></tr>
<tr><td>Cell</td><td>Cell</td></tr>
<tr><td>Cell</td><td>Cell</td></tr>
<tr><td>Cell</td><td>Cell</td></tr>
<tr><td>Footer</td><td>Footer</td></tr>
</table>
This is the footnote of the table.
```

---

### Figure

The Layout API preserves figure elements:

* Encapsulates figure content in `<figure>` tags to maintain semantic distinction from surrounding text
* Preserves figure captions with the `<figcaption>` tag to provide important context
* Preserves figure footnotes as separate paragraphs following the figure container

> [!IMPORTANT]
> In cases where we detect certain document components like section heading as part of the figures, markdown output will not present figures in the output and use the information for document structure analysis. For these cases, enumerate the figures field in JSON to retrieve all the figures.

Here's an example:

``` md 
<figure>
<figcaption>Figure 2 This is a figure</figcaption>

Values
300
200
100
0

Jan Feb Mar Apr May Jun Months

</figure>

This is footnote if the figure have.
```
---

### Selection Mark

Selection marks represent checkbox-like elements in forms and documents. The Layout API:

* Uses Unicode characters for visual clarity: ☒ (checked) and ☐ (unchecked)
* Filters out low-confidence checkbox detections (below 0.1 confidence) to improve reliability
* Maintains the semantic relationship between selection marks and their associated text


### Formula

Mathematical formulas are preserved with LaTeX-compatible syntax that allows for rendering of complex mathematical expressions:

* Inline formulas are enclosed in single dollar signs (`$...$`) to maintain text flow
* Block formulas use double dollar signs (`$$...$$`) for standalone display
* Multi-line formulas are represented as consecutive block formulas, preserving mathematical relationships
* Original spacing and formatting are maintained to ensure accurate representation

Here's an example of inline formula, single-line formula block and multiple-lines formula block:

``` md
The mass-energy equivalence formula $E = m c ^ { 2 }$ is an example of an inline formula

$$\frac { n ! } { k ! \left( n - k \right) ! } = \binom { n } { k }$$

$$\frac { p _ { j } } { p _ { 1 } } = \prod _ { k = 1 } ^ { j - 1 } e ^ { - \beta _ { k , k + 1 } \Delta E _ { k , k + 1 } }$$
$$= \exp \left[ - \sum _ { k = 1 } ^ { j - 1 } \beta _ { k , k + 1 } \Delta E _ { k , k + 1 } \right] .$$
```
---

### Barcode

Barcodes and QR codes are represented using Markdown image syntax with added semantic information:

* Uses standard image Markdown syntax with descriptive attributes
* Captures both the barcode type (QR code, barcode, etc.) and its encoded value
* Preserves the semantic relationship between barcodes and surrounding content

Here's an example:

```
![QRCode](barcodes/1.1 "https://www.microsoft.com")

![UPCA](barcodes/1.2 "012345678905")
 
![barcode type](barcodes/pagenumber.barcodenumber "barcode value/content")
```
---

### PageNumber/PageHeader/PageFooter

Page metadata elements provide context about document pagination but aren't meant to be displayed inline with the main content:

* Enclosed in HTML comments to preserve the information while keeping it hidden from standard Markdown rendering
* Maintains original page structure information that might be valuable for document reconstruction
* Enables applications to understand document pagination without disrupting the content flow

Here's an example:

``` md
<!-- PageHeader="This is page header" -->

<!-- PageFooter="This is page footer" -->
<!-- PageNumber="1" -->

```
---

### PageBreak

To easily figure out which parts belong to which page base on the pure Markdown content, we introduced PageBreak as the delimiter of the pages

Here's an example:
``` md
<!-- PageBreak -->
```
---

### KeyValuePairs/Language/Style

For KeyValuePairs/Language/Style, we map them to  Analytics JSON body and not in the Markdown content.


> [!NOTE]
> For more information on Markdown that is currently supported for user content on GitHub.com, *see* [GitHub Flavored Markdown Spec](https://github.github.com/gfm).

## Conclusion

Document Intelligence's Markdown elements provide a powerful way to represent the structure and content of analyzed documents. By understanding and properly utilizing these Markdown elements, you can enhance your document processing workflows and build more sophisticated content extraction applications.

## Next steps

* Try processing your documents with [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.
