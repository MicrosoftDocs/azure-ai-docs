---
title: Best practices for using Content Understanding
titleSuffix: Foundry Tools
description: Learn how to best use Azure Content Understanding in Foundry Tools for document, image, video, and audio file content and field extractions.
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

# Best practices for Azure Content Understanding in Foundry Tools

Azure Content Understanding in Foundry Tools uses generative AI to process documents, images, videos, and audio, transforming them into structured output formats. This article provides best practices to maximize accuracy and efficiency.

## Define effective field schemas

Clear and detailed field definitions are critical to accurate extraction. Follow these principles:

### Write detailed descriptions

Provide clear, specific descriptions that guide the model to the correct information. Include location hints, format expectations, and alternative labels.

**Example - Invoice date field:**
```text
The date when the invoice was issued, typically found at the top right corner. May be labeled as 'Invoice Date', 'Billing Date', or 'Issue Date'. Format is usually MM/DD/YYYY or DD-MM-YYYY.
```

### Include all aliases

List all possible names for each field, when possible, especially when working with diverse file templates. This diversity helps the model recognize the field regardless of labeling variations.

**Example - Investment distributions:**
```text
Equal to the 'Distributions' column. Also disclosed as 'Realizations' or 'Realized Proceeds'.
```

### Use affirmative language

Describe what the field is rather than what it isn't. Positive descriptions are clearer and more effective.

**Instead of:** "This field isn't the invoice date and isn't the due date."  
**Use:** "The date when goods or services were delivered, found in the delivery information section."

### Match language to content

Define field names and descriptions in the same language as your file. Language mismatches can significantly reduce accuracy.

**Example:** For Italian invoices, use `Fornitore` with Italian descriptions instead of `Vendor` with English descriptions.

### Use structured types for repeated data

Define repeated items, like line items or entries, as arrays of objects rather than string fields requesting JSON output.

**Example - Invoice line items:**
```json
"lineItems": {
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "description": { "type": "string" },
      "quantity": { "type": "number" },
      "unitPrice": { "type": "number" },
      "total": { "type": "number" }
    }
  }
}
```

### Specify generation methods

Explicitly set the method (`extract`, `generate`, or `classify`) for each field based on its purpose:
- **Generate**: Values requiring inference or summarization, such as risk level or summary.  
- **Classify**: Selection from predefined options, like document type or category.
- **Extract**: Values appearing directly in the content, such as invoice number or date.

> [!NOTE]
> `extract` is only supported for document analyzers.

## Optimize classification and categorization

Content Understanding automatically handles visual template variations within semantic categories. Follow these guidelines:

### Use semantic categories, not visual templates, for document classification

Don't create separate categories for documents or files with the same semantic type but different visual layouts. For example, use one `Invoice` category for all invoice variations rather than `Invoice_Template_A` and `Invoice_Template_B`.

### Write effective category definitions

* **Use common titles**: "Annual Financial Report", "SEC Form 10-K"
* **Use only ASCII characters** in category names
* **Provide distinguishing context**: Semantic meaning, key content markers, or distinctive layouts
* **Define an "Other" category** if you need to identify outliers
* **Avoid checkbox-only differences**: Don't create separate categories that differ only in checkbox values

**Example - Tax form categories:**
```
"2024_Form_1040": "US Individual Income Tax Return for tax year 2024. Contains '2024' prominently at the top."
"2025_Form_1040": "US Individual Income Tax Return for tax year 2025. Contains '2025' prominently at the top."
```

## Use confidence scores effectively

Confidence scores help determine when human review is needed. Set different thresholds based on field criticality:

* **Critical fields** (TotalAmount, ContractTerminationDate): Use higher thresholds (≥0.90)
* **Important fields** (VendorName, InvoiceNumber): Use medium thresholds (≥0.80)  
* **Non-critical fields** (Comments, Notes): Use lower thresholds (≥0.70)

Currently, only document analyzers support confidence scores.

> [!NOTE]
> These thresholds are included as an illustration. Determine thresholds experimentally for each use case.

## Improve accuracy over time

### Start with descriptions, then add examples

Prioritize refining field descriptions before adding labeled training examples. Clear descriptions often resolve issues without requiring more data.

### Add training examples for low confidence

If accuracy or confidence scores are lower than expected with zero-shot extraction, add similar documents to the knowledge base as training examples to improve accuracy.

## Optimize audio and video processing

All the best practices described earlier for defining field schemas apply to audio and video processing as well. The following are additional tips specific to audio and video content:

### Narrow language selection

Specify only the languages you expect in the content. Including too many languages increases transcription errors as the system must guess which language is being spoken.

**Example:** For content containing only English and Spanish, configure only those two languages rather than using autodetect from all available languages.

### Avoid extracting content as fields unnecessarily    

Speech transcripts, optical character recognition (OCR) text, and video key frames are automatically available in analyzer output. Don't define fields for this content unless you need extra processing, such as summarization or entity extraction.

## Related content

* [Create a custom analyzer](../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](prebuilt-analyzers.md)
* [Service quotas and limits](../service-limits.md)


