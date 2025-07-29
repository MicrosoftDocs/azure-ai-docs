---
title: 'Document Analysis: Extract Structured Content with Azure AI Content Understanding'
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding document layout analysis and data extraction capabilities.
author: PatrickFarley 
ms.author: paulhsu
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Document analysis: Extract structured content

> [!IMPORTANT]
>
Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development. Features, approaches, and processes can change or have limited capabilities before general availability. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

## Overview

The document analysis capabilities in Azure AI Content Understanding help you transform unstructured document data into structured, machine-readable information. You can precisely identify and extract document elements while you preserve their structural relationships. Then you can build powerful document processing workflows for a wide range of applications.

This article explains the document analysis features that you can use to extract meaningful content from your documents, preserve document structures, and unlock the full potential of your document data.

## Document elements

You can extract the following document elements through content extraction:

* [Markdown](#markdown-content-elements)
* Content elements
  * [Words](#words)
  * [Selection marks](#selection-marks)
  * [Barcodes](#barcodes)
  * [Formulas](#formulas)
  * [Images](#images)
* Layout elements
  * [Pages](#pages)
  * [Paragraphs](#paragraphs)
  * [Lines](#lines)
  * [Tables](#tables)
  * [Sections](#sections)

Not all content and layout elements are applicable or currently supported by all document file types.

### Markdown content elements

Content Understanding generates richly formatted Markdown that preserves the original document's structure. For this reason, large language models can better comprehend document context and hierarchical relationships for AI-powered analysis and generation tasks. In addition to words, selection marks, barcodes, formulas, and images as content, the Markdown also includes sections, tables, and page metadata for both visual rendering and machine processing. Learn more about how Content Understanding represents [content and layout elements in Markdown](markdown.md).

#### Words

A *word* is a content element composed of a sequence of characters. [Unicode Standard Annex #29](https://www.unicode.org/reports/tr29/#Word_Boundaries) defines the word boundaries. For Latin languages, words might be split from punctuation even without intervening spaces. In some languages, such as Chinese, supplemental word dictionaries are used to enable word breaking at semantic boundaries. For more information, see [Boundary analysis](https://unicode-org.github.io/icu/userguide/boundaryanalysis/).

:::image type="content" source="../media/document/word-boundaries.png" alt-text="Screenshot that shows detected words.":::

#### Selection marks

A *selection mark* is a content element that represents a visual glyph that indicates the state of a selection. Selection marks might appear in the document as checkboxes, check marks, or buttons. You can select or clear a selection mark, with different visual representation to indicate the state. Selection marks are encoded as words in the document analysis result by using the Unicode characters `☒` (selected) and `☐` (cleared).

Content Understanding detects check marks inside a table cell as selection marks in the selected state. It doesn't detect empty table cells as selection marks in the cleared state.

:::image type="content" source="../media/document/selection-marks.png" alt-text="Screenshot that shows detected selection marks.":::

#### Barcodes

A *barcode* is a content element that describes both linear (for example, UPC or EAN) and two-dimensional (for example, QR or MaxiCode) barcodes. Content Understanding represents barcodes by using their detected types and extracted values. The following barcode formats are currently accepted:

* QR Code
* Code 39
* Code 93
* Code 128
* UPC (UPC-A & UPC-E)
* PDF417
* EAN-8
* EAN-13
* Codabar
* Databar
* Databar (expanded)
* ITF
* Data Matrix

#### Formulas

A *formula* is a content element that represents mathematical expressions in the document. It might be an inline formula embedded with other text or a display formula that takes up an entire line. Multiline formulas are represented as multiple display formula elements grouped into paragraphs to preserve mathematical relationships.

#### Images

An *image* is a content element that represents an embedded image, figure, or chart in the document. Content Understanding extracts any embedded text from the images and any associated captions and footnotes.

### Layout elements

Document *layout elements* are visual and structural components, such as pages, tables, paragraphs, lines, tables, sections, and overall structure, that help to interpret content. Extracting these elements enables tools to analyze documents efficiently for tasks like information retrieval, semantic understanding, and data structuring.

#### Pages

A *page* is a grouping of content that typically corresponds to one side of a sheet of paper. A rendered page is characterized via width and height in the specified unit. In general, images use pixels while PDFs use inches. The `angle` property describes the overall text angle in degrees for pages that might be rotated.

For spreadsheets like Excel, each sheet is mapped to a page. For presentations, like PowerPoint, each slide is mapped to a page. For file formats like HTML or Word documents, which lack a native page concept without rendering, the entire main content is treated as a single page.

#### Paragraphs

A *paragraph* is an ordered sequence of lines that form a logical unit. Typically, the lines share common alignment and spacing between lines. Paragraphs are often delimited via indentation, added spacing, or bullets/numbering. Some paragraphs have special functional roles in the document. Currently supported roles include page header, page footer, page number, title, section heading, footnote, and formula block.

#### Lines

A *line* is an ordered sequence of consecutive content elements, which are often separated by visual spaces. Content elements in the same horizontal plane (row) but that are separated by more than a single visual space are most often split into multiple lines. This feature sometimes splits semantically contiguous content into separate lines. It also enables the representation of textual content split into multiple columns or cells. Lines in vertical writing are detected in the vertical direction.

#### Tables

A *table* organizes content into a group of cells in a grid layout. The rows and columns might be visually separated by grid lines, color banding, or greater spacing. The position of a table cell is specified via its row and column indices. A cell can span across multiple rows and columns.

Based on its position and styling, a cell is classified as general content, row header, column header, stub head, or description:

* A row header cell is typically the first cell in a row that describes the other cells in the row.
* A column header cell is typically the first cell in a column that describes the other cells in a column.
* A row or column can contain multiple header cells to describe hierarchical content.
* A stub head cell is typically the cell in the first row and first column position. The cell is either empty or describes the values in the header cells in the same row/column.
* A description cell generally appears at the uppermost or lowermost area of a table and describes the overall table content. It can sometimes appear in the middle of a table to break the table into sections. Typically, description cells span across multiple cells in a single row.

A table caption specifies content that explains the table. A table can also have a set of footnotes. Unlike a description cell, a caption typically lies outside the grid layout. Table footnotes annotate content inside the table and are often marked with footnote symbols. They're often found underneath the table grid.

A table might span across consecutive pages of a document. In this situation, table continuations in subsequent pages generally maintain the same column count, width, and styling. They often repeat the column headers. Typically, no intervening content comes between the initial table and its continuations except for page headers, footers, and page numbers.

The span for tables covers only the core content and excludes associated captions and footnotes.

:::image type="content" source="../media/document/table.png" alt-text="Screenshot that shows a table by using the layout feature.":::

#### Sections

A *section* is a logical grouping of related content elements that form a hierarchical structure within the document. It often starts with a section heading as the first paragraph. A section might contain subsections to create a nested document structure that preserves semantic relationships.

### Element properties

Documents consist of various components that are categorized into structural, textual, and form-related elements. These elements define the organization and presentation of the document. You can systematically identify and extract the elements for further analysis or application.

#### Spans

The `span` property specifies the logical position of the element in the document via the character offset and length into the top-level `markdown` string property. By default, character offsets and lengths are returned in Unicode code points, which are used by Python 3. To accommodate different development environments that use different character units, you can specify the `stringEncoding` query parameter to return span offsets and lengths in UTF16 code units (Java, JavaScript, or .NET) or UTF8 bytes (Go, Rust, Ruby, or PHP).

#### Source

The `source` property describes the visual position of the element in the file by using an encoded string. For documents, the source string is in one of the following formats:

* **Bounding polygon**: `D({pageNumber},{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4})`
* **Axis-aligned bounding box**: `D({pageNumber},{left},{top},{width},{height})`

Page numbers are 1-indexed. The bounding polygon describes a sequence of points that are clockwise from the left relative to the natural orientation of the element. For quadrilaterals, the points represent the upper-left, upper-right, lower-right, and lower-left corners. Each point represents the *x*, *y* coordinate in the length unit specified by the `unit` property. In general, the unit of measure for images is pixels. PDFs use inches.

:::image type="content" source="../media/document/bounding-regions.png" alt-text="Screenshot that shows detected bounding regions.":::

> [!NOTE]
> Currently, Content Understanding returns only four-point quadrilaterals as bounding polygons. Future versions might return a different number of points to describe more complex shapes, such as curved lines or nonrectangular images. Currently, source is returned only for elements from rendered files (.pdf/image).

## Related content

* Try processing your document content by using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
* Learn to analyze document content [analyzer templates](../quickstart/use-ai-foundry.md).
* Review code samples with [visual document search](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb).
* Review the code sample [analyzer templates](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
