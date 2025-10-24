# Prebuilt Analyzer Configuration Reference

This document provides comprehensive documentation for all configuration options and properties available in the prebuilt analyzer definitions (API version 2025-11-01).

## Table of Contents

- [Top-Level Properties](#top-level-properties)
- [Public Configuration Options](#public-configuration-options)
- [Configuration by Content Type](#configuration-by-content-type)
- [Examples](#examples)

---

## Top-Level Properties

Each prebuilt analyzer JSON definition contains the following top-level properties:

### `analyzerId`
- **Type:** `string`
- **Required:** Yes
- **Description:** Unique identifier for the analyzer (e.g., `"prebuilt-video"`, `"prebuilt-invoice"`, `"prebuilt-document"`). This is the primary identifier used to reference the analyzer in API calls.
- **Example:** `"prebuilt-invoice"`

### `name`
- **Type:** `string`
- **Required:** No
- **Description:** Human-readable display name for the analyzer. Used in UI and documentation to provide a friendly name.
- **Example:** `"Invoice document understanding"`, `"Post call analytics"`

### `description`
- **Type:** `string`
- **Required:** Yes
- **Description:** Brief description of what the analyzer does and what it extracts from documents or media files.
- **Example:** `"Analyze videos to extract transcript and description for each segment."`

### `baseAnalyzerId`
- **Type:** `string`
- **Required:** No
- **Description:** References a parent analyzer from which this analyzer inherits configuration. When specified, the analyzer inherits default configurations from its base analyzer and can override specific settings.
- **Common base analyzers:**
  - `"prebuilt-document"` - for document-based analyzers
  - `"prebuilt-audio"` - for audio-based analyzers
  - `"prebuilt-image"` - for image-based analyzers
- **Example:** `"baseAnalyzerId": "prebuilt-document"`

### `config`
- **Type:** `object`
- **Required:** Yes
- **Description:** Contains all configuration options for the analyzer, including both public (user-editable) and private (internal) settings. See [Public Configuration Options](#public-configuration-options) for details.

### `fieldSchema`
- **Type:** `object`
- **Required:** Yes
- **Description:** Defines the structured schema of fields that the analyzer extracts from content.
- **Properties:**
  - `name` - Schema name (e.g., `"InvoiceAnalysis"`)
  - `fields` - Object defining each extractable field with its type, description, and extraction method
- **Note:** Empty object (`{}`) indicates no structured fields are extracted (e.g., for layout-only analyzers).

### `supportedModels`
- **Type:** `object`
- **Required:** Yes
- **Description:** Lists the AI models that can be used with this analyzer.
- **Properties:**
  - `completion` - Array of completion model names (e.g., `["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"]`)
  - `embedding` - Array of embedding model names (e.g., `["text-embedding-3-large", "text-embedding-3-small"]`)

### `models`
- **Type:** `object`
- **Required:** Yes
- **Description:** Specifies the default models to use when no model is explicitly requested.
- **Properties:**
  - `completion` - Default completion model (e.g., `"gpt-4.1"`)
  - `embedding` - Default embedding model (e.g., `"text-embedding-3-large"`)
- **Note:** Empty object (`{}`) means defaults are inherited from base analyzer or determined at runtime.

### `warnings`
- **Type:** `array`
- **Required:** No
- **Description:** Array of warning messages or validation issues. Rarely populated in base analyzer definitions.

---

## Public Configuration Options

These are user-facing configuration options (under the `config` property) that can be modified when invoking an analyzer. Private options prefixed with underscore (`_`) are excluded from this documentation as they are for internal use only.

### General Options

#### `returnDetails`
- **Type:** `boolean`
- **Default:** `false` (varies by analyzer)
- **Description:** Controls whether to return detailed information in the response, including confidence scores, bounding boxes, text spans, and other metadata. When `false`, returns only the extracted values.
- **Use cases:**
  - Set to `true` for debugging
  - When you need location information for extracted data
  - When confidence scores are required for validation
  - For understanding extraction quality
- **Supported by:** All analyzers

#### `omitContent`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** When `true`, omits the raw content (e.g., full text, OCR results, images) from the response, returning only extracted structured data. This significantly reduces response size.
- **Use cases:**
  - When you only need structured field extractions
  - To reduce bandwidth and response time
  - When raw content is not needed for downstream processing
- **Supported by:** Document and video analyzers

---

### Document Content Extraction Options

#### `enableOcr`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Enables Optical Character Recognition (OCR) to extract text from images and scanned documents. When disabled, only embedded text (e.g., from native PDFs) is extracted.
- **Use cases:**
  - Disable for native digital documents to improve performance
  - Enable for scanned documents, images, or photos
- **Supported by:** Document and image analyzers

#### `enableLayout`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Extracts layout information including paragraphs, lines, words, reading order, selection marks, and structural elements like headers and footers.
- **Use cases:**
  - Required for understanding document structure
  - Needed for accurate paragraph and section extraction
  - Disable if only raw text is needed
- **Supported by:** Document-based analyzers

#### `enableFormula`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Detects and extracts mathematical formulas and equations, returning them in LaTeX format.
- **Use cases:**
  - Enable for scientific papers, research documents
  - Technical documentation with equations
  - Disable for general business documents to improve performance
- **Supported by:** Document-based analyzers

#### `enableBarcode`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Detects and extracts barcodes and QR codes from documents, returning the decoded values.
- **Note:** Hidden from preview.2 API but used internally for service branching.
- **Use cases:**
  - Inventory documents
  - Shipping labels
  - Product documentation
- **Supported by:** Document-based analyzers

---

### Table and Chart Options

#### `tableFormat`
- **Type:** `string`
- **Default:** `"html"`
- **Supported values:** `"html"`, `"markdown"`
- **Description:** Specifies the output format for extracted tables.
  - `"html"` - Returns tables with HTML markup including `<table>`, `<tr>`, `<td>` tags, preserving structure and cell merging
  - `"markdown"` - Returns tables in markdown format using pipes (`|`) and hyphens (`-`)
- **Use cases:**
  - Use `"html"` for rendering in web applications or when complex table structures need to be preserved
  - Use `"markdown"` for simple tables in documentation or text-based processing
- **Supported by:** Document-based analyzers

#### `chartFormat`
- **Type:** `string`
- **Default:** `"chartjs"`
- **Supported values:** `"chartjs"`
- **Description:** Specifies the format for extracted chart and graph data. Returns data structures compatible with Chart.js library for easy rendering.
- **Use cases:**
  - Extracting data from bar charts, line graphs, pie charts
  - Converting visual charts to structured data
  - Re-rendering charts in applications
- **Supported by:** Document-based analyzers

---

### Figure and Image Analysis Options

#### `enableFigureDescription`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Generates natural language text descriptions for figures, diagrams, images, and illustrations found in documents. Provides accessibility and understanding of visual content.
- **Use cases:**
  - Accessibility requirements (alt text generation)
  - Understanding diagrams and flowcharts
  - Extracting insights from infographics
- **Supported by:** Document-based analyzers

#### `enableFigureAnalysis`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Performs deeper analysis of figures including chart data extraction, diagram component identification, and visual element understanding.
- **Use cases:**
  - Extracting structured data from charts embedded in documents
  - Understanding complex diagrams
  - Detailed figure classification
- **Supported by:** Document-based analyzers

---

### Annotation Options

#### `enableAnnotations`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Extracts annotations, comments, highlights, and markup from documents (e.g., PDF comments, sticky notes).
- **Use cases:**
  - Processing reviewed documents
  - Extracting editor comments
  - Understanding document revisions
- **Supported by:** Document-based analyzers

#### `annotationFormat`
- **Type:** `string`
- **Default:** `"markdown"`
- **Supported values:** `"markdown"`
- **Description:** Specifies the format for returned annotations.
- **Supported by:** Document-based analyzers

---

### Segmentation Options

#### `enableSegment`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables segmentation of the content. When `true`, divides the document or media into logical segments:
  - **Documents:** Sections, chapters, or logical content blocks
  - **Videos:** Scenes or temporal segments
  - **Audio:** Speaker turns or topic segments
- **Use cases:**
  - Processing long documents in chunks
  - Analyzing video by scenes
  - Breaking down multi-topic conversations
- **Supported by:** Document, video, and audio analyzers

#### `segmentPerPage`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** When segmentation is enabled, this creates one segment per page. Only applies to document analyzers.
- **Use cases:**
  - Page-by-page processing
  - When each page should be treated as a separate unit
  - Parallel processing of pages
- **Supported by:** Document-based analyzers

---

### Field Extraction Options

#### `estimateFieldSourceAndConfidence`
- **Type:** `boolean`
- **Default:** `false` (varies by analyzer)
- **Description:** When enabled, returns the source location (e.g., page number, bounding box, line range) and confidence score for each extracted field value.
- **Use cases:**
  - Validation and quality assurance
  - Understanding extraction accuracy
  - Debugging extraction issues
  - Highlighting source text in UI
- **Supported by:** Most structured document analyzers (invoice, receipt, ID documents, tax forms, etc.)

---

### Audio and Video Options

#### `locales`
- **Type:** `array` of strings
- **Default:** `[]` (empty array)
- **Description:** List of locale/language codes for language-specific processing. Used primarily for transcription and speech recognition.
- **Supported values:** BCP-47 language codes (e.g., `["en-US", "es-ES", "fr-FR", "de-DE"]`)
- **Use cases:**
  - Multi-language audio transcription
  - Specifying expected language for better accuracy
  - Processing content in specific regional variants
- **Supported by:** `prebuilt-audio`, `prebuilt-video`, `prebuilt-callCenter`

#### `disableFaceBlurring`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Controls whether faces in images and videos should be blurred for privacy protection. When `false` (default), faces are automatically detected and blurred.
- **Use cases:**
  - Privacy compliance (GDPR, CCPA)
  - Set to `true` when face visibility is required
  - De-identification of individuals
- **Supported by:** `prebuilt-image`, `prebuilt-video`

#### `disableContentFiltering`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Controls content moderation and filtering. 
- **Note:** Hidden from GA (general availability) and used internally for service configuration.

---

### Document Classification Options

#### `contentCategories`
- **Type:** `object`
- **Default:** Not set by default (only on multi-variant analyzers)
- **Description:** Defines sub-categories or document types that the analyzer can classify and route to specialized handlers. This enables intelligent document classification before extraction.
- **Structure:** Each category contains:
  - `description` - Detailed description of the document type with identifying characteristics
  - `analyzerId` - The specific analyzer to use for this category
  - `_analyzerStorageObject` - Internal reference to the analyzer definition

**Example from `prebuilt-receipt`:**
```json
"contentCategories": {
  "receipt.generic": {
    "description": "Proof of payment for retail/restaurant or general POS transactions...",
    "analyzerId": "prebuilt-receipt.generic"
  },
  "receipt.hotel": {
    "description": "Hotel folio or lodging receipt acknowledging payment for a stay...",
    "analyzerId": "prebuilt-receipt.hotel"
  },
  "other": {
    "description": "Any document not matching the category above...",
    "analyzerId": "prebuilt-documentFields"
  }
}
```

**Example from `prebuilt-idDocument`:**
```json
"contentCategories": {
  "idDocument.generic": {
    "description": "Government-issued identity cards or permits other than passports...",
    "analyzerId": "prebuilt-idDocument.generic"
  },
  "idDocument.passport": {
    "description": "National passports (booklets) and passport cards...",
    "analyzerId": "prebuilt-idDocument.passport"
  },
  "other": {
    "description": "Any document not matching the category above...",
    "analyzerId": "prebuilt-documentFields"
  }
}
```

- **Use cases:**
  - Automatic document type detection
  - Routing to specialized extractors
  - Mixed document batch processing
  - Handling variant document formats
- **Supported by:** Multi-variant analyzers like `prebuilt-receipt`, `prebuilt-idDocument`

---

## Configuration by Content Type

### Document Analyzers
**Base Analyzer:** `prebuilt-document`

**Supported Options:**
- ✅ `returnDetails`
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
- ✅ `omitContent`
- ✅ `estimateFieldSourceAndConfidence` (structured analyzers)
- ✅ `contentCategories` (multi-variant analyzers)

**Examples:** `prebuilt-document`, `prebuilt-layout`, `prebuilt-read`, `prebuilt-invoice`, `prebuilt-receipt`, `prebuilt-contract`, `prebuilt-idDocument`

---

### Audio Analyzers
**Base Analyzer:** `prebuilt-audio`

**Supported Options:**
- ✅ `returnDetails`
- ✅ `locales`
- ✅ `disableContentFiltering`

**Examples:** `prebuilt-audio`, `prebuilt-callCenter`, `prebuilt-audioAnalyzer`

---

### Video Analyzers
**Base Analyzer:** `prebuilt-video` (or inherits from `prebuilt-audio`)

**Supported Options:**
- ✅ `returnDetails`
- ✅ `locales`
- ✅ `enableSegment`
- ✅ `omitContent`
- ✅ `disableFaceBlurring`
- ✅ `disableContentFiltering`
- ✅ `contentCategories`

**Examples:** `prebuilt-video`

---

### Image Analyzers
**Base Analyzer:** `prebuilt-image`

**Supported Options:**
- ✅ `returnDetails`
- ✅ `enableOcr`
- ✅ `disableFaceBlurring`
- ✅ `disableContentFiltering`

**Examples:** `prebuilt-image`, `prebuilt-imageAnalyzer`

---

## Examples

### Example 1: Extracting Invoice with Full Details

```json
{
  "analyzerId": "prebuilt-invoice",
  "config": {
    "returnDetails": true,
    "estimateFieldSourceAndConfidence": true,
    "enableFormula": false,
    "tableFormat": "html"
  }
}
```

**Result:** Extracts invoice fields with confidence scores, source locations, and tables in HTML format.

---

### Example 2: Layout Extraction with Figures

```json
{
  "analyzerId": "prebuilt-layoutWithFigures",
  "config": {
    "returnDetails": true,
    "enableAnnotations": true,
    "tableFormat": "markdown",
    "enableFigureDescription": true,
    "enableFigureAnalysis": true
  }
}
```

**Result:** Extracts layout, tables (in markdown), and generates descriptions for all figures.

---

### Example 3: Video Analysis with Segmentation

```json
{
  "analyzerId": "prebuilt-video",
  "config": {
    "returnDetails": false,
    "locales": ["en-US"],
    "enableSegment": true,
    "omitContent": false,
    "disableFaceBlurring": false
  }
}
```

**Result:** Transcribes video in English, segments by scene, includes full content, and blurs faces.

---

### Example 4: Receipt Processing with Classification

```json
{
  "analyzerId": "prebuilt-receipt",
  "config": {
    "enableSegment": true,
    "omitContent": true,
    "returnDetails": true,
    "estimateFieldSourceAndConfidence": true
  }
}
```

**Result:** Automatically classifies receipt type (generic vs. hotel), extracts fields with confidence, omits raw content.

---

### Example 5: Simple Document Reading

```json
{
  "analyzerId": "prebuilt-read",
  "config": {
    "returnDetails": true,
    "enableLayout": false
  }
}
```

**Result:** Extracts text, formulas, and barcodes without detailed layout information.

---

### Example 6: Call Center Analytics

```json
{
  "analyzerId": "prebuilt-callCenter",
  "config": {
    "returnDetails": false,
    "locales": ["en-US", "es-ES"]
  }
}
```

**Result:** Transcribes call in English and Spanish, extracts summary, sentiment, topics, and role-specific insights.

---

## Summary

This reference covers all public configuration options available in the 2025-11-01 prebuilt analyzer definitions. Key takeaways:

- **Document analyzers** offer the most comprehensive options for content extraction, layout analysis, and figure processing
- **Audio/video analyzers** focus on transcription, segmentation, and privacy controls
- **Structured document analyzers** (invoices, receipts, IDs) support field extraction with confidence scores
- **Multi-variant analyzers** use `contentCategories` for automatic classification and specialized extraction
- All analyzers support `returnDetails` for debugging and quality assurance
- Use `omitContent` to reduce response size when only structured data is needed

For specific field schemas and extraction capabilities, refer to the individual analyzer JSON definitions.
