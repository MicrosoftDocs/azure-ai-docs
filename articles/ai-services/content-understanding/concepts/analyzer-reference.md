---
title: Azure Content Understanding in Foundry Tools - What is an analyzer? Configuration and reference
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools analyzers, how to configure them, and the parameters you can set when creating custom analyzers.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# What is a Content Understanding analyzer?

An **analyzer** in Azure Content Understanding in Foundry Tools is a configurable processing unit that defines how your content is analyzed and what information is extracted.

An analyzer defines:

- What type of content to process (documents, images, audio, or video)
- What elements to extract (text, layout, tables, fields, transcripts)
- How to structure the output (markdown, JSON fields, segments)
- Which AI models to use for processing

Analyzers are the core building blocks of Content Understanding. They combine content extraction, AI-powered analysis, and structured data output into a single, reusable configuration. You can use prebuilt analyzers for common scenarios or create custom analyzers tailored to your specific needs.

### Analyzer types

Content Understanding provides several types of analyzers:

- **Base analyzers**: Foundational analyzers that provide core processing capabilities for each content type (`prebuilt-document`, `prebuilt-audio`, `prebuilt-video`, `prebuilt-image`). Use these analyzers as building blocks for custom analyzers.
- **RAG analyzers**: Extract content with semantic understanding for search and AI applications. They're optimized for retrieval-augmented generation scenarios. Examples include `prebuilt-documentSearch` and `prebuilt-videoSearch`.
- **Domain-specific analyzers**: Preconfigured for specific document types and industries, like invoices, receipts, ID documents, and contracts. Examples include `prebuilt-invoice`, `prebuilt-receipt`, and `prebuilt-idDocument`.
- **Custom analyzers**: Analyzers you create by extending base analyzers with custom field schemas and configurations to meet your specific requirements.

For more information and a complete list of available domain-specific analyzers, see [Prebuilt analyzers](prebuilt-analyzers.md).

## Analyzer configuration structure

Define an analyzer configuration using a JSON object with several top-level properties. You can configure the following components:

* [Analyzer properties](#analyzer-properties) - Core identity and metadata
  * [analyzerId](#analyzerid) - Unique identifier
  * [name](#name) - Display name
  * [description](#description) - Purpose description
  * [baseAnalyzerId](#baseanalyzerid) - Parent analyzer reference
* [Model configuration](#model-configuration) - AI model settings
  * [models](#models) - Default models
* [Processing configuration](#processing-configuration) - Content processing options
  * [config](#config-object-properties) - Behavior settings
* [Field schema](#field-configuration) - Structured data extraction
  * [fieldSchema](#field-schema-structure) - Field definitions

Here's a condensed example that shows the overall structure of an analyzer configuration:

```json
{
  "analyzerId": "my-custom-invoice-analyzer",
  "description": "Extracts vendor information, line items, and totals from commercial invoices",
  "baseAnalyzerId": "prebuilt-document",
  "config": {
    "enableOcr": true
  },
  "fieldSchema": {
    "fields": {
      "vendorName": {
        "type": "string"
      }
    }
  },
  "models": {
    "completion": "gpt-4.1",
    "embedding": "text-embedding-3-large"
  }
}
```

## Analyzer properties

Use these properties to uniquely identify and describe your analyzer:

### `analyzerId`
- **Description:** Unique identifier for the analyzer. Use this identifier to reference the analyzer in API calls.
- **Example:** `"prebuilt-invoice"`, `"my-custom-analyzer"`
- **Guidelines:**
  - Use descriptive names that indicate the analyzer's purpose.
  - For custom analyzers, choose names that don't conflict with prebuilt analyzer names.
  - Use lowercase with hyphens for consistency.

### `name`
- **Description:** Human-readable display name shown in user interfaces and documentation.
- **Example:** `"Invoice document understanding"`, `"Custom receipt processor"`

### `description`
- **Description:** Brief explanation of what the analyzer does and what content it processes. The AI model uses this description as context during field extraction, so clear descriptions improve extraction accuracy.
- **Example:** `"Analyzes invoice documents to extract line items, totals, vendor information, and payment terms"`
- **Guidelines:**
  - Be specific about what the analyzer extracts.
  - Mention the content types it supports.
  - Keep it concise but informative.
  - Write clear descriptions as they guide the AI model's understanding.

### `baseAnalyzerId`
- **Description:** References a parent analyzer from which this analyzer inherits configuration.
- **Supported base analyzers:**
  - `"prebuilt-document"` - for document-based custom analyzers
  - `"prebuilt-audio"` - for audio-based custom analyzers
  - `"prebuilt-video"` - for video-based custom analyzers
  - `"prebuilt-image"` - for image-based custom analyzers
- **Example:** `"baseAnalyzerId": "prebuilt-document"`

> [!NOTE]
> When you specify a base analyzer, your custom analyzer inherits all default configurations and can override specific settings.

## Model configuration

### `models`
- **Description:** Specifies which Foundry model names to use when processing with this analyzer. These are the model names (not deployment names) that the service uses. They must match one of the `supportedModels` from the base analyzer. The full list of models supported by Content Understanding is listed at [supported models](../service-limits.md#supported-generative-models).
- **Properties:**
  - `completion` - Model name for completion tasks (field extraction, segmentation, figure analysis, for example)
  - `embedding` - Model name for embedding tasks (using a knowledge base)
- **Important:** These model names come from the Foundry catalog, not deployment names. At runtime, the service maps these model names to the actual model deployments you configure at the resource level.
- **Example:**
  ```json
  {
    "completion": "gpt-4o",
    "embedding": "text-embedding-3-large"
  }
  ```

See [Connect your Content Understanding resource with Foundry models](models-deployments.md) for more details on how to configure connected models.

## Processing configuration

The `config` object contains all processing options that control how content is analyzed. These options are divided into categories based on functionality:

### Config object properties

#### General options

##### `returnDetails`
- **Default:** false (varies by analyzer)
- **Description:** Controls whether to include detailed information in the response, such as confidence scores, bounding boxes, text spans, and metadata.
- **When to use:**
  - Set to `true` when debugging extraction problems.
  - When you need location information for extracted data.
  - When confidence scores are required for validation.
  - For quality assurance and testing.
- **Impact on response:** Significantly increases response size with more metadata.

#### Document content extraction options

##### `enableOcr`
- **Default:** true
- **Description:** Enables Optical Character Recognition to extract text from images and scanned documents.
- **When to use:**
  - Enable for scanned documents, photos, and image-based PDFs.
  - Disable for native digital PDFs to improve performance.
- **Supported by:** Document analyzers.

##### `enableLayout`
- **Default:** true
- **Description:** Extracts layout information including paragraphs, lines, words, reading order, and structural elements.
- **When to use:**
  - Required for understanding document structure and hierarchy.
  - Needed for accurate paragraph and section extraction.
  - Disable if only raw text extraction is needed.
- **Supported by:** Document-based analyzers.

##### `enableFormula`
- **Default:** true
- **Description:** Detects and extracts mathematical formulas and equations in LaTeX format.
- **When to use:**
  - Enable for scientific papers, research documents, technical documentation.
  - Disable for general business documents to improve performance.
- **Supported by:** Document-based analyzers.

##### `enableBarcode`
- **Default:** true
- **Description:** Detects and extracts barcodes and QR codes, returning the decoded values.
- **When to use:**
  - Enable for inventory documents, shipping labels, product documentation.
  - Disable when barcodes aren't present to improve performance.
- **Supported by:** Document-based analyzers.
- **Supported barcode types:** QR Code, PDF417, UPC-A, UPC-E, Code 39, Code 128, EAN-8, EAN-13, DataBar, Code 93, Codabar, ITF, Micro QR Code, Aztec, Data Matrix, MaxiCode.

#### Table and chart options

##### `tableFormat`
- **Default:** `"html"`
- **Supported values:** `"html"`, `"markdown"`
- **Description:** Specifies the output format for extracted tables.
- **When to use:**
  - Use `"html"` for web rendering or when complex table structures need preservation.
  - Use `"markdown"` for simple tables in documentation or text-based processing.
- **Supported by:** Document-based analyzers.

##### `chartFormat`
- **Default:** `"chartjs"`
- **Supported values:** `"chartjs"`
- **Description:** Specifies the format for extracted chart and graph data. Compatible with Chart.js library.
- **When to use:**
  - When extracting data from bar charts, line graphs, and pie charts.
  - When converting visual charts to structured data for re-rendering.
- **Supported by:** Document-based analyzers.

#### Figure and image analysis options

##### `enableFigureDescription`
- **Default:** false
- **Description:** Generates natural language text descriptions for figures, diagrams, images, and illustrations.
- **When to use:**
  - For accessibility requirements (alt text generation).
  - For understanding diagrams and flowcharts.
  - For extracting insights from infographics.
- **Supported by:** Document-based analyzers.

##### `enableFigureAnalysis`
- **Default:** false
- **Description:** Performs deeper analysis of figures including chart data extraction and diagram component identification.
- **When to use:**
  - For extracting structured data from charts embedded in documents.
  - For understanding complex diagrams.
  - For detailed figure classification.
- **Supported by:** Document-based analyzers.

#### Annotation options

##### `annotationFormat`
- **Default:** `"markdown"`
- **Supported values:** `"markdown"`
- **Description:** Specifies the format for returned annotations.
- **Supported by:** Document-based analyzers.

#### Field extraction options

##### `estimateFieldSourceAndConfidence`
- **Default:** false (varies by analyzer)
- **Description:** Returns source location (page number, bounding box) and confidence score for each extracted field value.
- **When to use:**
  - For validation and quality assurance workflows.
  - For understanding extraction accuracy.
  - For debugging extraction issues.
  - For highlighting source text in user interfaces.
- **Supported by:** Document analyzers (invoice, receipt, ID documents, tax forms)

#### Audio and video options

##### `locales`
- **Default:** `[]` (empty array)
- **Description:** List of locale and language codes for language-specific processing, primarily for transcription.
- **Supported values:** BCP-47 language codes (for example, `["en-US", "es-ES", "fr-FR", "de-DE"]`)
- **When to use:**
  - For multi-language audio transcription.
  - For specifying expected language for better accuracy.
  - For processing content in specific regional variants.
- **Supported by:** `prebuilt-audio`, `prebuilt-video`, `prebuilt-callCenter`

>[!NOTE] 
>For a complete list of supported languages and locales, see [Language and region support](../language-region-support.md).

##### `disableFaceBlurring`
- **Default:** false
- **Description:** Controls whether faces in images and videos are blurred for privacy protection.
- **When to use:**
  - Set to `true` when face visibility is required for analysis.
  - Set to `false` when de-identification of individuals in shared content is desired.
- **Supported by:** `prebuilt-image`, `prebuilt-video`

> [!IMPORTANT]
> The Face capabilities feature in Content Understanding is a Limited Access service and registration is required for access. Face grouping and identification feature in Content Understanding is limited based on eligibility and usage criteria. Face service is only available to Microsoft managed customers and partners. Use the [Face Recognition intake form](https://aka.ms/facerecognition) to apply for access. For more information, see the [Responsible AI investments and safeguards for facial recognition](../../cognitive-services-limited-access.md).

#### Classification options

##### `contentCategories`
- **Default:** Not set
- **Description:** Defines categories or content types for automatic classification and routing to specialized handlers. When used with `enableSegment set to false` is currently only supported for documents. It classifies the entire file. When used with `enableSegment=true`, the file is broken into chunks based on these categories, with each segment classified and optionally processed by a category-specific analyzer. Always selects a single option from the list of available categories. 
- **Structure:** Each category contains:
  - `description` - (Required) Detailed description of the category or document type. This description acts as a prompt that guides the AI model in determining segment boundaries and classification. Include distinguishing characteristics to help identify where one category ends and another begins.
  - `analyzerId` - (Optional) Reference to another analyzer to use for this category. The referenced analyzer is linked, not copied, ensuring consistent behavior. If omitted, only categorization is performed without more processing (split-only scenario).
- **Model usage:** The models specified in the parent analyzer's `models` property are used only for segmentation and classification. Each subanalyzer uses its own model configuration for extraction.
- **Behavior with `enableSegment`:**
  - **`enableSegment: true`:** Content is split into segments based on the category descriptions. Each segment is classified into one of the defined categories. Returns segment metadata in the original content object, plus more content objects for segments with `analyzerId` specified.
  - **`enableSegment: false`:** The entire content is classified as a whole into one category and routed accordingly. Useful for hierarchical classification without splitting.
- **Category matching:** If an "other" or "default" category isn't defined, content is forced to classify into one of the listed categories. Include an "other" category to handle unmatched content gracefully.
- **Supported by:** Document and video analyzers. For video, you can only define one contentCategory.

##### `enableSegment`
- **Default:** false
- **Description:** Enables content segmentation, breaking the file into chunks based on the categories specified in `contentCategories`. Each segment is then classified into one of the defined categories for selective processing.
- **Segmentation behavior:** The service divides content into logical units by analyzing the content against the category descriptions. Segment boundaries are determined using:
  - **Documents:** Category descriptions combined with content structure (pages, sections, formatting changes).
  - **Videos:** Category descriptions combined with visual cues (shot changes, scene transitions, temporal boundaries). Only one contentCategory is supported.
- **When to use:**
  - Processing mixed-content batches where different parts need different handling (for example, a PDF containing both invoices and receipts).
  - Splitting long documents into categorized chunks for selective analysis.
  - Analyzing videos by content type (for example, separate ads from main content).
- **Output structure:**
  - Returns a `segments` array in the content object containing metadata for each segment (ID, boundaries, category).
  - Each segment includes its classified category from `contentCategories`.
  - More content objects are returned for segments with category `analyzerId` specified.
- **Hierarchical segmentation:** If a category's analyzer also has `enableSegment: true`, segments can be recursively split, enabling multi-level content breakdown.
- **Performance impact:** Increases processing time for large files, especially with many segments.
- **Supported by:** Document and video analyzers.

##### `segmentPerPage`
- **Default:** false
- **Description:** When segmentation is enabled, force one segment per page instead of using logical content boundaries. Replaces the need for separate "perPage" split modes.
- **When to use:**
  - Page-by-page processing workflows.
  - Each page should be treated as an independent unit.
  - Parallel processing of individual pages.
  - Page-level field extraction in multi-page documents.
  - Mixed document batches where each page is a different document type.
- **Supported by:** Document-based analyzers.

##### `omitContent`
- **Default:** false
- **Description:** When `true`, excludes the original content object from the response. The response includes only structured field data or content objects from subanalyzers when using `contentCategories`.
- **When to use:**
  - When you only need extracted field values.
  - In composed analyzers with `contentCategories` to return only categorized results.
  - For hierarchical classification chains, return only leaf analyzer results.
- **Example - Selective analysis:**
  ```json
  {
    "config": {
      "enableSegment": true,
      "contentCategories": {
        "invoice": { "analyzerId": "prebuilt-invoice" },
        "other": { }  // Categorize but don't process
      },
      "omitContent": true  // Only return invoice analysis results
    }
  }
  ```
- **Supported by:** Document analyzers.

## Field configuration

The `fieldSchema` property defines what structured data your analyzer extracts from content. It specifies the fields, their types, and how they should be extracted.

### Design intent: Structured extraction

Field schemas transform unstructured content into structured, queryable data. The schema acts as both:
- A **contract** defining what data is extracted
- A **guide** for the AI model on what to look for and how to interpret it

### Field schema structure

```json
{
  "fieldSchema": {
    "name": "InvoiceAnalysis",
    "fields": {
      "VendorName": {
        "type": "string",
        "description": "Name of the vendor or supplier",
        "method": "extract"
      },
      "InvoiceTotal": {
        "type": "number",
        "description": "Total amount due on the invoice",
        "method": "extract"
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
- **Description:** Name of the schema, typically describing the content type or use case
- **Example:** `"InvoiceAnalysis"`, `"ReceiptExtraction"`, `"ContractFields"`

#### `fields`
- **Description:** Object defining each field to extract, with field names as keys. An empty object `{}` indicates no structured fields are extracted (for example, layout-only analyzers).
- **Hierarchical support:** Supports nested fields through `object` and `array` types for representing complex data structures
- **Best practice:** Avoid deep nesting (more than two or three levels) as it can reduce performance and extraction accuracy


### Field definition properties

Each field in the `fields` object has the following properties:

#### `type`
- **Supported values:** `"string"`, `"number"`, `"boolean"`, `"date"`, `"object"`, `"array"`
- **Description:** Data type of the field value. Choose the type that best matches your data semantics for optimal extraction.

#### `description`
- **Description:** Clear explanation of what the field contains and where to find it. The AI model processes this description as a mini-prompt to guide field extraction, so specificity and clarity directly improve extraction accuracy.

For information about writing effective field descriptions, see [Best practices for field extraction](best-practices.md).

#### `method`
- **Supported values:** `"generate"`, `"extract"`, `"classify"`
- **Description:** Extraction method to use for this field. When you don't specify a method, the system automatically determines the best method based on the field type and description.
- **Method types:**
  - `"generate"` - Values are generated freely based on the content by using AI models (best for complex or variable fields requiring interpretation)
  - `"extract"` - Values are extracted as they appear in the content (best for literal text extraction from specific locations). Extract requires `enableSourceGroundingAndConfidence` to be set to true for this field.
  - `"classify"` - Values are classified against a predefined set of categories (best when using `enum` with a fixed set of possible values)

##### `estimateSourceAndConfidence`
- **Default:** false
- **Description:** Returns source location (page number, bounding box) and confidence score for this field value. Must be true for fields with `method` = extract. This property overrides the analyzer level `estimateFieldSourceAndConfidence` property. 
- **When to use:**
  - For validation and quality assurance workflows.
  - For understanding extraction accuracy.
  - For debugging extraction issues.
  - For highlighting source text in user interfaces.
- **Supported by:** Document analyzers (invoice, receipt, ID documents, tax forms)

#### `items` (for array types)
- **Description:** Defines the structure of items in the array
- **Properties:**
  - `type` - Type of array items (`"string"`, `"number"`, `"object"`)
  - `properties` - For object items, defines the nested field structure

#### `properties` (for object types)
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

## Complete analyzer example

Here's a comprehensive example of a custom invoice analyzer configuration that demonstrates the key concepts discussed in this reference:

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
        "method": "extract"
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
        "method": "extract"
      },
      "InvoiceDate": {
        "type": "date",
        "description": "Date the invoice was issued, in format MM/DD/YYYY",
        "method": "extract"
      },
      "DueDate": {
        "type": "date",
        "description": "Payment due date",
        "method": "extract"
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
        "method": "extract"
      },
      "Tax": {
        "type": "number",
        "description": "Tax amount",
      },
      "Total": {
        "type": "number",
        "description": "Total amount due (Subtotal + Tax)",
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

## Creating a custom analyzer

To create a custom analyzer based on the configuration structure described in this document, use the Content Understanding REST API to submit your analyzer definition.

### API endpoint

Use the following curl command to create a custom analyzer by submitting your analyzer configuration from a JSON file:

```bash
curl -X PUT "https://{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2025-11-01-preview" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -d @analyzer-definition.json
```

Replace the following placeholders:
- `{endpoint}` - Your Content Understanding resource endpoint
- `{analyzerId}` - Unique identifier for your analyzer
- `{key}` - Your Content Understanding subscription key
- `analyzer-definition.json` - Path to your analyzer configuration file

### Request body

The analyzer configuration file should be a JSON object containing the properties described in this reference. For a complete example, see the [Create Custom Analyzer tutorial](..\tutorial\create-custom-analyzer.md).

### Response

The API returns a `201 Created` response with an `Operation-Location` header that you can use to track the status of the analyzer creation operation.

### Next steps

For a complete walkthrough with examples for different content types (documents, images, audio, video), see [Create a custom analyzer](../tutorial/create-custom-analyzer.md).

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
- ✅ `locales`
- ✅ `contentCategories`
- ✅ `enableSegment`
- ✅ `omitContent`
- ✅ `disableFaceBlurring`

### Image analyzers
**Base analyzer:** `prebuilt-image`

**Supported configuration options:**
- ✅ `returnDetails`
- ✅ `disableFaceBlurring`

## Related content

* Learn about [prebuilt analyzers](prebuilt-analyzers.md) available in Content Understanding.
* Explore [analyzer templates](analyzer-templates.md) to get started quickly.
* Create your own analyzer by following the [custom analyzer tutorial](../tutorial/create-custom-analyzer.md). 
* Understand [best practices](best-practices.md) for optimal extraction results.
* Review [document elements](../document/elements.md) and [video elements](../video/elements.md) for details on extracted content.
* Get started by creating and testing analyzers in [Foundry](../quickstart/use-ai-foundry.md).
