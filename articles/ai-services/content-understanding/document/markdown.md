---
title: Content Understanding document modality supported markdown elements
titleSuffix: Azure AI services
description: Description of the supported Markdown elements returned as part of the Content Understanding Document response and how to use the response in your applications.
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: conceptual
ms.date: 05/19/2025
ms.author: paulhsu
 
---
 
# Document analysis: Markdown representation
 
Azure AI Content Understanding's document analysis capabilities help you transform unstructured document data into [GitHub Flavored Markdown](https://github.github.com/gfm), preserving the original content and layout for higher fidelity downstream applications and workflows.  This document describes how each content and layout element is represented in markdown.
 
## Words and selection marks
 
Recognized words and detected selection marks are represented in markdown as plain text.  Content may be escaped to avoid ambiguity with markdown formatting syntax.
 
## Barcodes
 
Barcodes are represented as markdown images with alt text and title: `![alt text](url "title")`.
 
| Content Type | Markdown Pattern | Example |
| --- | --- | --- |
| Barcode | `![{barcode.kind}]({barcode.path} "{barcode.value}")` | `![QRCode](barcodes/1.2 "https://www.microsoft.com")` |
 
## Formulas
 
Mathematical formulas are encoded using LaTeX in Markdown:
 
* Inline formulas are enclosed in single dollar signs (`$...$`) to maintain text flow.
* Display formulas use double dollar signs (`$$...$$`) for standalone display.
* Multi-line formulas are represented as consecutive display formulas without intervening empty lines, preserving mathematical relationships.
 
| Formula Kind | Markdown | Visualization |
| --- | --- | --- |
| Inline | `$\sqrt { -1 } $ is $i$` | $\sqrt { -1 } $ is $i$
| Display | `$$a^2 + b^2 = c^2$$` | $a^2 + b^2 = c^2$ |
| Multi-line | `$$( x + 2 ) ^ 2 = x ^ 2 + 4 x + 4$$`<br/>`$$= x ( x + 4 ) + 4$$` | $$( x + 2 ) ^ 2 = x ^ 2 + 4 x + 4$$ $$= x ( x + 4 ) + 4$$ |
 
## Images
 
Detected images, including figures and charts, are currently represented using HTML `<figure>` elements in markdown that wrap the detected text in the image.  Any caption is represented via an `<figcaption>` elements.  Any associated footnotes appear as text immediately after the figure.
 
``` md
<figure>
<figcaption>Figure 2: Example</figcaption>
 
Values
300
200
100
0
 
Jan Feb Mar Apr May Jun Months
 
</figure>
 
This is a footnote.
```
 
## Lines and paragraph
 
Paragraphs are represented in markdown as a block of text separate by blank lines.
When lines are available, each document line maps to a separate line in the markdown.
 
## Sections
 
Paragraphs with title or section heading role are converted into markdown headings.  Title, if any, is assigned heading level 1.  The heading level of all other sections are assigned to preserve the detected hierarchical structure.
 
## Tables
 
Tables are currently represented in markdown using HTML table markup (`<table>`, `<tr>`, `<th>`, `<td>`) to enable support for merged cells via `rowspan` and `colspan` attributes and rich headers via `<th>`.  Any caption is represented via an `<caption>` element.  Any associated footnotes appear as text immediately after the table.
 
:::row:::
:::column:::
 
``` md
<table>
<caption>Table 1. Example</caption>
<tr><th>Header A</th><th>Header B</th></tr>
<tr><td>Cell 1A</td><td>Cell 1B</td></tr>
<tr><td>Cell 2A</td><td>Cell 2B</td></tr>
</table>
This is a footnote.
```
 
:::column-end:::
:::column:::
   
<table>
<caption>Table 1. Example</caption>
<tr><th>Header A</th><th>Header B</th></tr>
<tr><td>Cell 1A</td><td>Cell 1B</td></tr>
<tr><td>Cell 2A</td><td>Cell 2B</td></tr>
</table>
This is a footnote.
       
:::column-end:::
:::row-end:::
 
## Page metadata
 
Markdown does not natively encode page metadata, such as page numbers, headers, footers, and breaks.
Since this information may be useful for downstream applications, we encode such metadata as HTML comments.
 
| Metadata | Markdown |
| --- | --- |
| Page number | `<!-- PageNumber="1" -->` |
| Page header | `<!-- PageHeader="Header" -->` |
| Page footer | `<!-- PageNumber="Footer" -->` |
| Page break | `<!-- PageBreak -->` |
 
## Conclusion
 
Content Understanding's Markdown elements provide a powerful way to represent the structure and content of analyzed documents. By understanding and properly utilizing these Markdown elements, you can enhance your document processing workflows and build more sophisticated content extraction applications.
 
## Next steps
 
* Try processing your document content using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
* Learn to analyze document content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code samples: [**visual document search**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
 
 
 