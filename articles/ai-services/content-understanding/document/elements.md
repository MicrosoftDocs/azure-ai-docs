---
title: "Document analysis: extracting structured content with Azure AI Content Understanding"
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding's document layout analysis and data extraction capabilities
author: laujan
ms.author: paulhsu
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/19/2025
---

# Document analysis: extracting structured content

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

## Overview

Azure AI Content Understanding's document analysis capabilities help you transform unstructured document data into structured, machine-readable information. By precisely identifying and extracting document elements while preserving their structural relationships, you can build powerful document processing workflows for a wide range of applications.

This article explains the document analysis features that enable you to extract meaningful content from your documents, preserve document structures, and unlock the full potential of your document data.

## Document elements

The following document elements can be extracted through content extraction:

* [**Markdown**](#markdown-content-elements)
* Content elements
  * [**Words**](#words)
  * [**Selection marks**](#selection-marks)
  * [**Barcodes**](#barcodes)
  * [**Formulas**](#formulas)
  * [**Images**](#images)
* Layout elements
  * [**Pages**](#pages)
  * [**Paragraphs**](#paragraphs)
  * [**Lines**](#lines)
  * [**Tables**](#tables)
  * [**Sections**](#sections)

> [!NOTE]
> Not all content and layout elements are applicable or currently supported by all document file types.

### Markdown content elements

Content Understanding generates richly formatted markdown that preserves the original document's structure, enabling large language models to better comprehend document context and hierarchical relationships for AI-powered analysis and generation tasks. In addition to words, selection marks, barcodes, formulas, and images as content, the markdown also includes sections, tables, and page metadata for both visual rendering and machine processing. Learn more about how Content Understanding represents [content and layout element in markdown](markdown.md).

#### Words

A `word` is a content element composed of a sequence of characters. Content Understanding uses word boundaries defined by [Unicode Standard Annex #29](https://www.unicode.org/reports/tr29/#Word_Boundaries). For Latin languages, words may be split from punctuation even without intervening spaces. In some language, such as Chinese, supplemental word dictionaries are used to enable word breaking at semantic boundaries. For more information, *see* [Boundary Analysis](https://unicode-org.github.io/icu/userguide/boundaryanalysis/).


:::image type="content" source="../media/document/word-boundaries.png" alt-text="Screenshot of detected words.":::

#### Selection marks

A `selection mark` is a content element that represents a visual glyph indicating the state of a selection. They may be represented as check boxes, check marks, radio buttons, etc. The state of a selection mark can be selected or unselected, with different visual representation to indicate the state. They're encoded as words in the document analysis result using `☒` (selected) and `☐` (unselected).

Content Understanding detects check marks inside table cell as selection marks in the selected state. However, it doesn't detect empty table cells as selection marks in the unselected state.

:::image type="content" source="../media/document/selection-marks.png" alt-text="Screenshot of detected selection marks.":::

#### Barcodes

A `barcode` is a content element that describes both linear (ex. UPC, EAN) and 2D (ex. QR, MaxiCode) barcodes. Content Understanding represents barcodes using its detected type and extracted value. The following barcode formats are currently accepted:


* `QR Code`
* `Code 39`
* `Code 93`
* `Code 128`
* `UPC (UPC-A & UPC-E)`
* `PDF417`
* `EAN-8`
* `EAN-13`
* `Codabar`
* `Databar`
* `Databar (expanded)`
* `ITF`
* `Data Matrix`

#### Formulas

A `formula` is a content element representing mathematical expressions in the document. It may be an `inline` formula embedded with other text, or an `display` formula that takes up an entire line. Multiline formulas are represented as multiple `display` formula elements grouped into `paragraphs` to preserve mathematical relationships.

#### Images

An `image` is a content element that represents an embedded image, figure, or chart in the document. Content Understanding extracts any embedded text from the images, and any associated captions and footnotes.

### Layout elements

Document layout elements are visual and structural components, such as pages, tables, paragraphs, lines, tables, sections, and overall structure, that help interpret content. Extracting these elements enables tools to analyze documents efficiently for tasks like information retrieval, semantic understanding, and data structuring.

#### Pages

A `page` is a grouping of content that typically corresponds to one side of a sheet of paper. A rendered page is characterized via `width` and `height` in the specified `unit`. In general, images use pixel while PDFs use inch. The `angle` property describes the overall text angle in degrees for pages that may be rotated.

> [!NOTE]
> For spreadsheets like Excel, each sheet is mapped to a page. For presentations, like PowerPoint, each slide is mapped to a page. For file formats like HTML or Word documents, which lack a native page concept without rendering, the entire main content is treated as a single page.

#### Paragraphs

A `paragraph` is an ordered sequence of lines that form a logical unit. Typically, the lines share common alignment and spacing between lines. Paragraphs are often delimited via indentation, added spacing, or bullets/numbering. Some paragraphs may have special functional `role` in the document. Currently supported roles include page header, page footer, page number, title, section heading, footnote, and formula block.

#### Lines

A `line` is an ordered sequence of consecutive content elements, often separated by visual spaces. Content elements in the same horizontal plane (row) but separated by more than a single visual space are most often split into multiple lines. While this feature sometimes splits semantically contiguous content into separate lines, it enables the representation of textual content split into multiple columns or cells. Lines in vertical writing are detected in the vertical direction.

#### Tables

A `table` organizes content into a group of cells in a grid layout. The rows and columns may be visually separated by grid lines, color banding, or greater spacing. The position of a table cell is specified via its row and column indices. A cell can span across multiple rows and columns.

Based on its position and styling, a cell can be classified as general content, row header, column header, stub head, or description:

* A row header cell is typically the first cell in a row that describes the other cells in the row.

* A column header cell is typically the first cell in a column that describes the other cells in a column.

* A row or column can contain multiple header cells to describe hierarchical content.

* A stub head cell is typically the cell in the first row and first column position. It can be empty or describe the values in the header cells in the same row/column.

* A description cell generally appears at the top or bottom most area of a table, describing the overall table content. However, it can sometimes appear in the middle of a table to break the table into sections. Typically, description cells span across multiple cells in a single row.

A table caption specifies content that explains the table. A table can further have a set of footnotes. Unlike a description cell, a caption typically lies outside the grid layout. Table footnotes annotate content inside the table, often marked with footnote symbols. They're often found below the table grid.

A table may span across consecutive pages of a document. In this situation, table continuations in subsequent pages generally maintain the same column count, width, and styling. They often repeat the column headers. Other than page headers, footers, and page numbers, there's generally no intervening content between the initial table and its continuations.

> [!NOTE]
> The span for tables covers only the core content and exclude associated caption and footnotes.

:::image type="content" source="../media/document/table.png" alt-text="Illustration of table using the layout feature.":::

#### Sections

A `section` is a logical grouping of related content elements that form a hierarchical structure within the document. It often starts with a section heading as the first paragraph. A section may contain subsections, creating a nested document structure that preserves semantic relationships.

### Element properties

Documents consist of various components that can be categorized into structural, textual, and form-related elements. These elements not only define the organization and presentation of the document but can also be systematically identified and extracted for further analysis or application.

#### Spans

The `span` property specifies the logical position of the element in the document via the character offset and length into the top-level `markdown` string property. By default, character offsets and lengths are returned in Unicode code points, used by Python 3. To accommodate different development environments that use different character units, user can specify the `stringEncoding` query parameter to return span offsets and lengths in UTF16 code units (Java, JavaScript, .NET) or UTF8 bytes (Go, Rust, Ruby, PHP).

#### Source

The `source` property describes the visual position of the element in the file using an encoded string. For documents, the source string may be in one of the following formats:
* Bounding polygon: `D({pageNumber},{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4})`
* Axis-aligned bounding box: `D({pageNumber},{left},{top},{width},{height})`

Page numbers are `1-indexed`. The bounding polygon describes a sequence of points, clockwise from the left relative to the natural orientation of the element. For quadrilaterals, the points represent the top-left, top-right, bottom-right, and bottom-left corners. Each point represents the **x**, **y** coordinate in the length unit specified by the `unit` property. In general, the unit of measure for images is pixels while PDFs use inches.

:::image type="content" source="../media/document/bounding-regions.png" alt-text="Screenshot of detected bounding regions.":::

> [!NOTE]
> Currently, Content Understanding only returns `4-point` quadrilaterals as bounding polygons. Future versions may return different number of points to describe more complex shapes, such as curved lines or nonrectangular images. Currently, source is only returned for elements from rendered files (pdf/image).

## Supported content and layout elements

Different file formats support different subsets of content and layout elements. The following table lists the currently supported elements for each file type.

|Document type|Supported format|
|-----|-----|
|**Portable Document Format**|`.pdf`|
|**Image**|`.jpeg/.jpg`, `.png`, `.bmp`, `.tiff`, `.heif`|
|**Microsoft Office**|`.docx`, `.pptx`, `.xls`|

## Next steps

* Try processing your document content using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
* Learn to analyze document content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code samples: [**visual document search**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).