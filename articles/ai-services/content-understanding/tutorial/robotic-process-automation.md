---
title: Build a robotic process automation (RPA) solution with Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Learn to build a robotic process automation solution with Content Understanding
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: tutorial
ms.custom:
  - ignite-2025
---

# Tutorial: Use Azure Content Understanding in Foundry Tools in a robotic process automation (RPA) solution

Robotic process automation (RPA) enables organizations to automate repetitive tasks by orchestrating workflows across systems. When combined with Azure Content Understanding, RPA can handle complex content ingestion scenarios across documents, images, audio, and video.

Many RPA solutions aim for straight-through processing (STP): automate end-to-end workflows with minimal human intervention. Confidence scores and grounding information help support STP by improving decision quality and auditability.

## What is RPA?

RPA automates repetitive tasks that typically require manual effort, such as data entry, document processing, and system integration.

**Example:** Automating invoice processing—extracting fields from invoices, validating totals, and updating ERP (Enterprise Resource Planning) systems without manual intervention.

## Components of an RPA solution
An effective RPA pipeline for content processing typically includes:

1. **Splitting**  
   Break large files (for example, PDFs with multiple invoices) into individual documents.

2. **Classification**  
   Identify document types (invoice, contract, receipt) for routing to appropriate analyzers.

3. **Field Extraction with Confidence & Grounding**  
   Extract structured data such as invoice number, date, and total amount.  
   **Key outputs include:**  
   - **Extracted fields** (for example, `InvoiceNumber`, `Date`, `TotalAmount`)  
   - **Confidence scores** for each field, enabling automated decision-making  
  - **Grounding information**—where the field was identified in the source (page number, bounding box, or text snippet/citation). This is critical for auditability and human review.

4. **Post-Processing & Validation**  
   Apply business rules (for example, totals must match line items, dates must be valid).

5. **Human Review & Validation**  
   Trigger review when confidence scores fall below a threshold or rules fail.

6. **Other Steps**  
   - **Routing**: Direct documents to downstream analyzers or systems.
   - **Integration**: Push validated data into ERP, CRM, or other business systems.

## Architecture flow
:::image type="content" source="../media/concepts/robotic-process-automation.png" alt-text="The workflow of a typical RPA process.":::

## Building your RPA solution with Content Understanding

Content Understanding offers flexibility to define your entire workflow within a single analyzer. You can configure document splitting, classification, field extraction, and validation steps in one call. This workflow can be structured as a single level or with multiple levels, depending on your automation requirements.

### Single level classification and extraction

An insurance claim is a good example of a single level classification where each claim packet can consist of a claim form and one or more estimates.

### Multi-level classification

Tax processing requires more complex classification, where you might start at the top level by classifying a document as a tax form or an expense record. The next level of classification will further classify the tax documents into the specific type to improve the accuracy of the classification.

### Define your analyzer

For this scenario, you're going to process a file that contains an insurance claim. You expect four content types:

* Claim form: Route to the custom `claimForm` analyzer.
* Estimates (car repairs or property damage): Route each estimate to the `prebuilt-invoice` analyzer.
* Medical reports: Route to the custom `medicalReport` analyzer.
* Police report: Ignore.


Because this scenario is document-specific, start by deriving the analyzer from the `prebuilt-document` analyzer.

```jsonc
{
  "analyzerId": "insuranceClaim",
  "baseAnalyzerId": "prebuilt-document",
  "models": {
    "completion": "gpt-4.1",
    "embedding": "text-embedding-ada-002"
  },
  "config": {
    "enableSegment": true,
    "contentCategories": {
      "claimForm": {
        "description": "The claim form for Zava Insurance.",
        "analyzerId": "claimForm"
      },
      "estimate": {
        "description": "The body shop estimate or contractor estimate to fix the property damage.",
        "analyzerId": "prebuilt-invoice"
      },
      "medicalReport": {
        "description": "A doctor's assessment or medical report related to injury suffered.",
        "analyzerId": "medicalReport"
      },
      "policeReport": {
        "description": "A police or law enforcement report detailing the events that led to the loss."
        /* Don't perform analysis for this category. */
      }
    },
    "omitContent": true
  }
}
```
> [!NOTE]
> The `insuranceClaim` analyzer configuration demonstrates how you can route different document segments to either prebuilt or custom analyzers. In this example, the `claimForm` and `medicalReport` analyzers must be defined separately before use. You can reference analyzers by their `analyzerId` or define them inline using the `analyzer` property for more granular control. Additionally, you can choose to ignore specific document types (such as `policeReport` in this example) to optimize processing costs. This flexible approach allows you to tailor classification, segmentation, and extraction workflows to your business requirements.

### Post-processing, validation, and normalization

Analyzers support post-processing, such as extracting only the numeric portion of a value, normalizing a date to a specific format, or validating that line items add up to the subtotal. You can specify these behaviors with simple instructions in field descriptions.

### Confidence scores and grounding

Confidence and grounding (source) are set at the field level. For each field that requires confidence and grounding, set `estimateSourceAndConfidence` to `true`.

### Triggering human review based on confidence scores

After extracting fields and their associated confidence scores and grounding information, you can automate human review by setting a confidence threshold. Only fields with confidence scores below this threshold are flagged for manual validation. This approach ensures that only uncertain data is reviewed, improving data accuracy and completeness while maximizing straight through processing (STP).

This selective review process helps maintain high automation rates and ensures that only critical exceptions require manual intervention.

## Next steps

* [Build a RAG solution](build-rag-solution.md)
* [Try a multimodal content solution accelerator](https://github.com/microsoft/content-processing-solution-accelerator)
* [Learn more about Content Understanding analyzers](../concepts/prebuilt-analyzers.md)