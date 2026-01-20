---
title: Build a robotic process automation (RPA) solution with Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Learn to build a robotic process automation solution with Content Understanding
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 10/19/2025
ms.service: azure-ai-content-understanding
ms.topic: tutorial
ms.custom:
  - ignite-2025
---

# Tutorial: Use Azure Content Understanding in Foundry Tools in a robotic process automation (RPA) solution

Robotic Process Automation (RPA) enables organizations to automate repetitive tasks by orchestrating workflows across systems. When combined with **Azure Content Understanding**, RPA can handle complex content ingestion scenarios across documents, images, audio, and video.

The **goal of any RPA solution is Straight Through Processing (STP)**—automating end-to-end workflows with minimal human intervention to **reduce costs and lower latency**. Achieving STP requires **confidence scores** and **grounding information** to ensure data accuracy and compliance. These capabilities allow systems to make decisions automatically while maintaining transparency and trust.

---

## What is RPA?
RPA automates **tedious and repetitive tasks** that typically require manual effort, such as data entry, document processing, and system integration

**Example:** Automating invoice processing—extracting fields from invoices, validating totals, and updating ERP (Enterprise Resource Planning) systems without manual intervention.

---

## Components of an RPA Solution
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
   - **Grounding information**—where the field was identified in the source (page number, bounding box, or text snippet/citiation). This is critical for auditability and human review.

4. **Post-Processing & Validation**  
   Apply business rules (for example, totals must match line items, dates must be valid).

5. **Human Review & Validation**  
   Trigger review when confidence scores fall below a threshold or rules fail.

6. **Other Steps**  
   - **Routing**: Direct documents to downstream analyzers or systems.
   - **Integration**: Push validated data into ERP, CRM, or other business systems.

---

## Architecture Flow
:::image type="content" source="../media/concepts/robotic-process-automation.png" alt-text="The workflow of a typical RPA process.":::

## Building your RPA solution with Content Understanding

Content Understanding offers flexibility to define your entire workflow within a single analyzer. You can configure document splitting, classification, field extraction, and validation steps in one call. This workflow can be structured as a single level or with multiple levels, depending on your automation requirements.

### Single level classification and extraction

An insurance claim is a good example of a single level classification where each claim packet can consist of a claim form and one or more estimates.

### Multi-level classification

Tax processing requires more complex classification, where you might start at the top level by classifying a document as a tax form or an expense record. The next level of classification will further classify the tax documents into the specific type to improve the accuracy of the classification.

### Define your analyzer

For this scenario, we're going to process a file containing an insurance claim, we expect to see four types of files.
* The claim form  - routed to the custom `claimForm` analyzer
* Estimates (could be for car repairs or property damage)  - route each estimate to the `prebuilt-invoice` analyzer
* Medical reports for any injuries - route to the custom `medicalReport` analyzer
* Police report  - Ignore


Since this scenario is document specific, start by deriving the analyzer from the `prebuilt-document` analyzer. 

``` REST

{
  "baseAnalyzerId": "prebuilt-document"
  // Use the base analyzer to invoke the document specific capabilities.

  "analyzerId": "insuranceClaim",
  //Specify the model the analyzer should use. This is one of the suported completion models and one of the supported embeddings model. The specific deployment used during analyze is set on the resource or provided in the analyze request.
  "models": {
      "completion": "gpt-4.1",
      "embedding": "text-embedding-ada-002"

    },
  "config": {
    // Enable splitting of the input into segments. Set this property to false if you only expect a single document within the input file. When specified and enableSegment=false, the whole content will be classified into one of the categories.
    "enableSegment": true,

    "contentCategories": {
      // Category name.
      "claimForm": {
        // Description to help with classification and splitting.
        "description": "The claim form for Zava Insurance",

        // Define the analyzer that any content classified as a calimForm should be routed to
        "analyzerId": "claimForm"
      },

      "estimate": {
        "description": "The body shop estimate or contractor estimate to fix the property damage.",
        "analyzerId": "prebuilt-invoice"
      },
      "medicalReport": {
        "description": "A doctors assessment or medical report related to injury suffered.",
        "analyzerId": "medicalReport"
      },
      "policeReport": {
        "description": "A police or law enforcement report detailing the events that lead to the loss."
        // Don't perform analysis for this category.
      }

    },

    // Omit original content object and only return content objects from additional analysis.
    "omitContent": true
  },

  //You can use fieldSchema here to define fields that are needed from the entire input content.

}

```
> [!NOTE]
> The `insuranceClaim` analyzer configuration demonstrates how you can route different document segments to either prebuilt or custom analyzers. In this example, the `claimForm` and `medicalReport` analyzers must be defined separately before use. You can reference analyzers by their `analyzerId` or define them inline using the `analyzer` property for more granular control. Additionally, you can choose to ignore specific document types (such as `policeReport` in this example) to optimize processing costs. This flexible approach allows you to tailor classification, segmentation, and extraction workflows to your business requirements.

### Post processing, validations, and normalization

Analyzers support post processing like extracting just the numeric portion or a product ID, normalizing a date to a specific format or validating that the line items add up to the sub total with simple instructions in the description for the fields.

### Confidence scores and grounding

Confidence and grounding (source) are set at the field level. For each field that requires confidence and grounding, set the `estimateSourceAndConfidence` property to true.

### Triggering human review based on confidence scores

After extracting fields and their associated confidence scores and grounding information, you can automate human review by setting a confidence threshold. Only fields with confidence scores below this threshold are flagged for manual validation. This approach ensures that only uncertain data is reviewed, improving data accuracy and completeness while maximizing straight through processing (STP).

This selective review process helps maintain high automation rates and ensures that only critical exceptions require manual intervention.

## Next steps

* [Build a RAG solution](build-rag-solution.md)

* [Try a multimodal content solution accelerator](https://github.com/microsoft/content-processing-solution-accelerator)

* [Learn more Content Understanding analyzers](../concepts/analyzer-templates.md)