---
title: Azure AI Content Understanding analyzer configuration reference
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding analyzers, how to configure them, and the parameters you can set when creating custom analyzers.
author: PatrickFarley 
ms.author: paulhsu
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Analyzer configuration reference

> [!IMPORTANT]
>
> Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development. Features, approaches, and processes can change or have limited capabilities before general availability. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

## What is an analyzer?

An **analyzer** in Azure AI Content Understanding is a configurable processing unit that defines how your content should be analyzed and what information should be extracted. Think of an analyzer as a recipe that tells the service:
- What type of content to process (documents, images, audio, or video)
- What elements to extract (text, layout, tables, fields, transcripts)
- How to structure the output (markdown, JSON fields, segments)
- Which AI models to use for processing

Analyzers are the core building blocks of Content Understanding. They combine content extraction, AI-powered analysis, and structured data output into a single, reusable configuration. You can use prebuilt analyzers for common scenarios or create custom analyzers tailored to your specific needs.

### Analyzer types

Content Understanding provides several types of analyzers:

- **Base analyzers**: Foundational analyzers that provide core processing capabilities for each content type (`prebuilt-document`, `prebuilt-audio`, `prebuilt-video`, `prebuilt-image`). These are typically used as building blocks for custom analyzers.
- **RAG analyzers**: Optimized for retrieval-augmented generation scenarios, extracting content with semantic understanding for search and AI applications (`prebuilt-documentAnalyzer`, `prebuilt-videoAnalyzer`).
- **Vertical analyzers**: Preconfigured for specific document types and industries, like invoices, receipts, ID documents, and contracts (`prebuilt-invoice`, `prebuilt-receipt`, `prebuilt-idDocument`).
- **Custom analyzers**: Analyzers you create by extending base analyzers with custom field schemas and configurations to meet your specific requirements.

For a complete list of available prebuilt analyzers, see [Prebuilt analyzers](prebuilt-analyzers.md).

## Analyzer configuration structure

An analyzer configuration consists of two main parts:

1. **Overall configuration**: Top-level settings that define the analyzer's identity, behavior, and processing options
2. **Field configuration**: Schema definitions that specify what structured data to extract

### Overall configuration properties

#### Core identity properties

These properties uniquely identify and describe your analyzer:

##### `analyzerId`
- **Type:** string
- **Required:** Yes
- **Description:** Unique identifier for the analyzer. This is how you reference the analyzer in API calls.
- **Example:** `"prebuilt-invoice"`, `"my-custom-analyzer"`
- **Guidelines:**
  - Use descriptive names that indicate the analyzer's purpose
  - For custom analyzers, choose names that don't conflict with prebuilt analyzer IDs
  - Use lowercase with hyphens for consistency

##### `name`
- **Type:** string
- **Required:** No
- **Description:** Human-readable display name shown in user interfaces and documentation
- **Example:** `"Invoice document understanding"`, `"Custom receipt processor"`

##### `description`
- **Type:** string
- **Required:** Yes
- **Description:** Brief explanation of what the analyzer does and what content it processes
- **Example:** `"Analyzes invoice documents to extract line items, totals, vendor information, and payment terms"`
- **Guidelines:**
  - Be specific about what the analyzer extracts
  - Mention the content types it supports
  - Keep it concise but informative

##### `baseAnalyzerId`
- **Type:** string
- **Required:** No (required for custom analyzers)
- **Description:** References a parent analyzer from which this analyzer inherits configuration
- **Supported base analyzers:**
  - `"prebuilt-document"` - for document-based custom analyzers
  - `"prebuilt-audio"` - for audio-based custom analyzers
  - `"prebuilt-video"` - for video-based custom analyzers
  - `"prebuilt-image"` - for image-based custom analyzers
  - `"prebuilt-callCenter"` - for call center audio analysis
- **Example:** `"baseAnalyzerId": "prebuilt-document"`
- **Note:** When you specify a base analyzer, your custom analyzer inherits all default configurations and can override specific settings.

#### Model configuration

These properties control which AI models the analyzer uses for processing:

##### `supportedModels`
- **Type:** object
- **Required:** Yes
- **Description:** Lists the AI models available for use with this analyzer
- **Properties:**
  - `completion` - Array of completion model names (for text generation and field extraction)
  - `embedding` - Array of embedding model names (for semantic search and similarity)
- **Example:**
  ```json
  {
    "completion": ["gpt-4o", "gpt-4o-mini", "gpt-4.1"],
    "embedding": ["text-embedding-3-large", "text-embedding-3-small"]
  }
  ```

##### `models`
- **Type:** object
- **Required:** Yes
- **Description:** Specifies the default models to use when no model is explicitly requested in the API call
- **Properties:**
  - `completion` - Default completion model
  - `embedding` - Default embedding model
- **Example:**
  ```json
  {
    "completion": "gpt-4.1",
    "embedding": "text-embedding-3-large"
  }
  ```
- **Note:** Empty object `{}` means defaults are inherited from the base analyzer.

#### Processing configuration

The `config` object contains all processing options that control how content is analyzed. These options are divided into categories based on functionality:

##### General options

###### `returnDetails`
- **Type:** boolean
- **Default:** false (varies by analyzer)
- **Description:** Controls whether to include detailed information in the response (confidence scores, bounding boxes, text spans, metadata)
- **When to use:**
  - Set to `true` when debugging extraction issues
  - When you need location information for extracted data
  - When confidence scores are required for validation
  - For quality assurance and testing
- **Impact on response:** Significantly increases response size with additional metadata

###### `omitContent`
- **Type:** boolean
- **Default:** false
- **Description:** When `true`, excludes raw content (full text, OCR results, images) from the response, returning only structured field data
- **When to use:**
  - When you only need extracted field values
  - To reduce bandwidth and improve response time
  - When raw content is not needed for downstream processing
- **Supported by:** Document and video analyzers

##### Document content extraction options

###### `enableOcr`
- **Type:** boolean
- **Default:** true
- **Description:** Enables Optical Character Recognition to extract text from images and scanned documents
- **When to use:**
  - Enable for scanned documents, photos, and image-based PDFs
  - Disable for native digital PDFs to improve performance
- **Supported by:** Document and image analyzers

###### `enableLayout`
- **Type:** boolean
- **Default:** true
- **Description:** Extracts layout information including paragraphs, lines, words, reading order, and structural elements
- **When to use:**
  - Required for understanding document structure and hierarchy
  - Needed for accurate paragraph and section extraction
  - Disable if only raw text extraction is needed
- **Supported by:** Document-based analyzers

###### `enableFormula`
- **Type:** boolean
- **Default:** true
- **Description:** Detects and extracts mathematical formulas and equations in LaTeX format
- **When to use:**
  - Enable for scientific papers, research documents, technical documentation
  - Disable for general business documents to improve performance
- **Supported by:** Document-based analyzers

###### `enableBarcode`
- **Type:** boolean
- **Default:** true
- **Description:** Detects and extracts barcodes and QR codes, returning the decoded values
- **When to use:**
  - Enable for inventory documents, shipping labels, product documentation
  - Disable when barcodes are not present to improve performance
- **Supported by:** Document-based analyzers
- **Supported barcode types:** QR Code, PDF417, UPC-A, UPC-E, Code 39, Code 128, EAN-8, EAN-13, DataBar, Code 93, Codabar, ITF, Micro QR Code, Aztec, Data Matrix, MaxiCode

##### Table and chart options

###### `tableFormat`
- **Type:** string
- **Default:** `"html"`
- **Supported values:** `"html"`, `"markdown"`
- **Description:** Specifies the output format for extracted tables
- **When to use:**
  - Use `"html"` for web rendering or when complex table structures need preservation
  - Use `"markdown"` for simple tables in documentation or text-based processing
- **Supported by:** Document-based analyzers

###### `chartFormat`
- **Type:** string
- **Default:** `"chartjs"`
- **Supported values:** `"chartjs"`
- **Description:** Specifies the format for extracted chart and graph data (compatible with Chart.js library)
- **When to use:**
  - When extracting data from bar charts, line graphs, pie charts
  - Converting visual charts to structured data for re-rendering
- **Supported by:** Document-based analyzers

##### Figure and image analysis options

###### `enableFigureDescription`
- **Type:** boolean
- **Default:** false
- **Description:** Generates natural language text descriptions for figures, diagrams, images, and illustrations
- **When to use:**
  - For accessibility requirements (alt text generation)
  - Understanding diagrams and flowcharts
  - Extracting insights from infographics
- **Supported by:** Document-based analyzers

###### `enableFigureAnalysis`
- **Type:** boolean
- **Default:** false
- **Description:** Performs deeper analysis of figures including chart data extraction and diagram component identification
- **When to use:**
  - Extracting structured data from charts embedded in documents
  - Understanding complex diagrams
  - Detailed figure classification
- **Supported by:** Document-based analyzers

##### Annotation options

###### `enableAnnotations`
- **Type:** boolean
- **Default:** false
- **Description:** Extracts annotations, comments, highlights, and markup from documents (for example, PDF comments)
- **When to use:**
  - Processing reviewed documents
  - Extracting editor comments
  - Understanding document revisions
- **Supported by:** Document-based analyzers

###### `annotationFormat`
- **Type:** string
- **Default:** `"markdown"`
- **Supported values:** `"markdown"`
- **Description:** Specifies the format for returned annotations
- **Supported by:** Document-based analyzers

##### Segmentation options

###### `enableSegment`
- **Type:** boolean
- **Default:** false
- **Description:** Enables content segmentation, dividing content into logical units
- **Segmentation behavior by content type:**
  - **Documents:** Sections, chapters, or logical content blocks
  - **Videos:** Scenes or temporal segments
  - **Audio:** Speaker turns or topic segments
- **When to use:**
  - Processing long documents in manageable chunks
  - Analyzing video by scenes
  - Breaking down multi-topic conversations
- **Supported by:** Document, video, and audio analyzers

###### `segmentPerPage`
- **Type:** boolean
- **Default:** false
- **Description:** When segmentation is enabled, creates one segment per page (document analyzers only)
- **When to use:**
  - Page-by-page processing workflows
  - When each page should be treated as a separate unit
  - Parallel processing of individual pages
- **Supported by:** Document-based analyzers

##### Field extraction options

###### `estimateFieldSourceAndConfidence`
- **Type:** boolean
- **Default:** false (varies by analyzer)
- **Description:** Returns source location (page number, bounding box) and confidence score for each extracted field value
- **When to use:**
  - Validation and quality assurance workflows
  - Understanding extraction accuracy
  - Debugging extraction issues
  - Highlighting source text in user interfaces
- **Supported by:** Structured document analyzers (invoice, receipt, ID documents, tax forms)

##### Audio and video options

###### `locales`
- **Type:** array of strings
- **Default:** `[]` (empty array)
- **Description:** List of locale/language codes for language-specific processing (primarily for transcription)
- **Supported values:** BCP-47 language codes (for example, `["en-US", "es-ES", "fr-FR", "de-DE"]`)
- **When to use:**
  - Multi-language audio transcription
  - Specifying expected language for better accuracy
  - Processing content in specific regional variants
- **Supported by:** `prebuilt-audio`, `prebuilt-video`, `prebuilt-callCenter`

###### `disableFaceBlurring`
- **Type:** boolean
- **Default:** false
- **Description:** Controls whether faces in images and videos should be blurred for privacy protection
- **When to use:**
  - Privacy compliance (GDPR, CCPA) - keep as `false`
  - Set to `true` when face visibility is required for analysis
  - De-identification of individuals in shared content
- **Supported by:** `prebuilt-image`, `prebuilt-video`

##### Document classification options

###### `contentCategories`
- **Type:** object
- **Default:** Not set (only on multi-variant analyzers)
- **Description:** Defines sub-categories or document types for automatic classification and routing to specialized handlers
- **Structure:** Each category contains:
  - `description` - Detailed description of the document type
  - `analyzerId` - Specific analyzer to use for this category
- **When to use:**
  - Automatic document type detection
  - Routing to specialized extractors
  - Mixed document batch processing
  - Handling variant document formats
- **Example:**
  ```json
  {
    "contentCategories": {
      "receipt.generic": {
        "description": "Standard retail or restaurant receipts",
        "analyzerId": "prebuilt-receipt.generic"
      },
      "receipt.hotel": {
        "description": "Hotel folio or lodging receipt",
        "analyzerId": "prebuilt-receipt.hotel"
      },
      "other": {
        "description": "Documents not matching above categories",
        "analyzerId": "prebuilt-documentFields"
      }
    }
  }
  ```
- **Supported by:** Multi-variant analyzers like `prebuilt-receipt`, `prebuilt-idDocument`

## Field configuration

The `fieldSchema` property defines what structured data your analyzer extracts from content. It specifies the fields, their types, and how they should be extracted.

### Field schema structure

```json
{
  "fieldSchema": {
    "name": "InvoiceAnalysis",
    "fields": {
      "VendorName": {
        "type": "string",
        "description": "Name of the vendor or supplier",
        "method": "preset"
      },
      "InvoiceTotal": {
        "type": "number",
        "description": "Total amount due on the invoice",
        "method": "preset"
      },
      "LineItems": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "Description": { "type": "string" },
            "Quantity": { "type": "number" },
            "UnitPrice": { "type": "number" },
            "Amount": { "type": "number" }
          }
        },
        "description": "List of items on the invoice, typically in a table format",
        "method": "generative"
      }
    }
  }
}
```

### Field schema properties

#### `name`
- **Type:** string
- **Required:** Yes
- **Description:** Name of the schema, typically describing the content type or use case
- **Example:** `"InvoiceAnalysis"`, `"ReceiptExtraction"`, `"ContractFields"`

#### `fields`
- **Type:** object
- **Required:** Yes
- **Description:** Object defining each field to extract, with field names as keys
- **Note:** Empty object `{}` indicates no structured fields are extracted (for example, layout-only analyzers)

### Field definition properties

Each field in the `fields` object has the following properties:

#### `type`
- **Type:** string
- **Required:** Yes
- **Supported values:** `"string"`, `"number"`, `"boolean"`, `"date"`, `"object"`, `"array"`
- **Description:** Data type of the field value
- **Guidelines:**
  - Use `"string"` for text values (names, addresses, descriptions)
  - Use `"number"` for numeric values (amounts, quantities, IDs)
  - Use `"boolean"` for yes/no or true/false values
  - Use `"date"` for date and time values
  - Use `"object"` for nested structures
  - Use `"array"` for lists or repeated items

#### `description`
- **Type:** string
- **Required:** Yes
- **Description:** Clear explanation of what the field contains and where to find it
- **Guidelines:**
  - Be specific about what to extract
  - Include identifying characteristics (for example, "Located in the header section")
  - Provide examples when helpful (for example, "Format: MM/DD/YYYY")
  - Mention edge cases or variations

#### `method`
- **Type:** string
- **Required:** No
- **Supported values:** `"preset"`, `"generative"`
- **Description:** Extraction method to use for this field
- **Method types:**
  - `"preset"` - Uses predefined extraction patterns (faster, more consistent, best for standard fields)
  - `"generative"` - Uses AI models for flexible extraction (better for complex or variable fields)
- **Default:** `"generative"` if not specified

#### `items` (for array types)
- **Type:** object
- **Required:** Yes (when `type` is `"array"`)
- **Description:** Defines the structure of items in the array
- **Properties:**
  - `type` - Type of array items (`"string"`, `"number"`, `"object"`)
  - `properties` - For object items, defines the nested field structure

#### `properties` (for object types)
- **Type:** object
- **Required:** Yes (when `type` is `"object"`)
- **Description:** Defines the structure of nested fields within the object
- **Example:**
  ```json
  {
    "Address": {
      "type": "object",
      "properties": {
        "Street": { "type": "string" },
        "City": { "type": "string" },
        "State": { "type": "string" },
        "ZipCode": { "type": "string" }
      },
      "description": "Complete mailing address"
    }
  }
  ```

### Field extraction best practices

1. **Be specific in descriptions**: The more specific your field description, the better the extraction accuracy
2. **Use preset method for standard fields**: When extracting common fields (dates, totals, names), use preset method for faster processing
3. **Use generative method for complex fields**: For fields that vary in location or format, use generative method for flexibility
4. **Structure nested data appropriately**: Use objects and arrays to represent hierarchical data (for example, line items, addresses)
5. **Provide examples**: In field descriptions, include format examples to guide extraction
6. **Consider confidence scores**: Enable `estimateFieldSourceAndConfidence` when validation is critical
7. **Test iteratively**: Start with a few key fields and expand your schema based on results

## Complete analyzer example

Here's a comprehensive example of a custom invoice analyzer configuration:

```json
{
  "analyzerId": "my-custom-invoice-analyzer",
  "name": "Custom Invoice Analyzer",
  "description": "Extracts vendor information, line items, and totals from commercial invoices",
  "baseAnalyzerId": "prebuilt-document",
  "config": {
    "returnDetails": true,
    "enableOcr": true,
    "enableLayout": true,
    "enableFormula": false,
    "tableFormat": "html",
    "estimateFieldSourceAndConfidence": true,
    "omitContent": false
  },
  "fieldSchema": {
    "name": "InvoiceFields",
    "fields": {
      "VendorName": {
        "type": "string",
        "description": "Name of the vendor or supplier, typically found in the header section",
        "method": "preset"
      },
      "VendorAddress": {
        "type": "object",
        "properties": {
          "Street": { "type": "string" },
          "City": { "type": "string" },
          "State": { "type": "string" },
          "ZipCode": { "type": "string" }
        },
        "description": "Complete vendor mailing address"
      },
      "InvoiceNumber": {
        "type": "string",
        "description": "Unique invoice number, often labeled as 'Invoice #' or 'Invoice No.'",
        "method": "preset"
      },
      "InvoiceDate": {
        "type": "date",
        "description": "Date the invoice was issued, in format MM/DD/YYYY",
        "method": "preset"
      },
      "DueDate": {
        "type": "date",
        "description": "Payment due date",
        "method": "preset"
      },
      "LineItems": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "Description": {
              "type": "string",
              "description": "Item or service description"
            },
            "Quantity": {
              "type": "number",
              "description": "Quantity ordered"
            },
            "UnitPrice": {
              "type": "number",
              "description": "Price per unit"
            },
            "Amount": {
              "type": "number",
              "description": "Line total (Quantity × UnitPrice)"
            }
          }
        },
        "description": "List of items or services on the invoice, typically in a table format",
        "method": "generative"
      },
      "Subtotal": {
        "type": "number",
        "description": "Sum of all line items before tax",
        "method": "preset"
      },
      "Tax": {
        "type": "number",
        "description": "Tax amount",
        "method": "preset"
      },
      "Total": {
        "type": "number",
        "description": "Total amount due (Subtotal + Tax)",
        "method": "preset"
      },
      "PaymentTerms": {
        "type": "string",
        "description": "Payment terms and conditions (e.g., 'Net 30', 'Due upon receipt')",
        "method": "generative"
      }
    }
  },
  "supportedModels": {
    "completion": ["gpt-4o", "gpt-4o-mini", "gpt-4.1"],
    "embedding": ["text-embedding-3-large", "text-embedding-3-small"]
  },
  "models": {
    "completion": "gpt-4.1",
    "embedding": "text-embedding-3-large"
  }
}
```

## Using analyzers in API calls

Once you've created or selected an analyzer, you can use it to process content through the Content Understanding API.

### Basic API request

```http
POST https://{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-05-01-preview
Content-Type: application/json

{
  "url": "https://example.com/document.pdf"
}
```

### Overriding configuration at runtime

You can override specific configuration options when making API calls:

```http
POST https://{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-05-01-preview
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "config": {
    "returnDetails": true,
    "tableFormat": "markdown",
    "estimateFieldSourceAndConfidence": true
  }
}
```

### Using base64-encoded content

```http
POST https://{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-05-01-preview
Content-Type: application/json

{
  "base64Source": "{base64-encoded-content}"
}
```

## Configuration by content type

Different content types support different configuration options. Here's a quick reference:

### Document analyzers
**Base analyzer:** `prebuilt-document`

**Supported configuration options:**
- ✅ `returnDetails`
- ✅ `omitContent`
- ✅ `enableOcr`
- ✅ `enableLayout`
- ✅ `enableFormula`
- ✅ `enableBarcode`
- ✅ `tableFormat`
- ✅ `chartFormat`
- ✅ `enableFigureDescription`
- ✅ `enableFigureAnalysis`
- ✅ `enableAnnotations`
- ✅ `annotationFormat`
- ✅ `enableSegment`
- ✅ `segmentPerPage`
- ✅ `estimateFieldSourceAndConfidence` (structured analyzers)
- ✅ `contentCategories` (multi-variant analyzers)

### Audio analyzers
**Base analyzer:** `prebuilt-audio`

**Supported configuration options:**
- ✅ `returnDetails`
- ✅ `locales`

### Video analyzers
**Base analyzer:** `prebuilt-video`

**Supported configuration options:**
- ✅ `returnDetails`
- ✅ `omitContent`
- ✅ `locales`
- ✅ `enableSegment`
- ✅ `disableFaceBlurring`

### Image analyzers
**Base analyzer:** `prebuilt-image`

**Supported configuration options:**
- ✅ `returnDetails`
- ✅ `enableOcr`
- ✅ `disableFaceBlurring`

## Related content

* Learn about [prebuilt analyzers](prebuilt-analyzers.md) available in Content Understanding
* Explore [analyzer templates](analyzer-templates.md) to get started quickly
* Follow the [custom analyzer tutorial](../tutorial/create-custom-analyzer.md) to create your own
* Understand [best practices](best-practices.md) for optimal extraction results
* Review [document elements](../document/elements.md) and [video elements](../video/elements.md) for details on extracted content
* Get started with [Azure AI Foundry](../quickstart/use-ai-foundry.md) to create and test analyzers
