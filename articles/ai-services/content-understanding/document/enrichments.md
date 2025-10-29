---
title: "Document analysis with confidence, grounding, and in-context learning"
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding's value add-ons that improve model extraction quality and performance
author: PatrickFarley 
ms.author: admaheshwari
manager: nitinme
ms.date: 08/11/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---


# Improve document output quality with confidence, grounding, and in-context learning

Intelligent document processing, whether for unstructured documents like contracts and statements of work, or structured documents like invoices and insurance forms, is done for critical information for RAG, search, agentic workflows, and any downstream applications or automation. Extracting this data reliably, at scale, requires more capabilities than just text extraction. Intelligent document processing requires information like what was extracted, why it was extracted, and how reliably it was extracted.

Most enterprises face the following challenges when handling a variety of documents at scale:
- Need to **validate the sources** of extracted data for true reference. For example, if the model pulls out a payment term or contract clause, you must know exactly where in the document it came from.
- Need to **automate workflows**, but only when the extraction is meeting an accuracy threshold that is critical for the business application. You need to know how confident/accurate the model is in its predictions.
- Need a way to **correct the model without retraining  from scratch** (ideally by providing a few labeled examples) when it gets something wrong or encounters a new format.

To address these needs, Azure AI Content Understanding supports the following features for post-processing your extracted output.

| Feature | Purpose | Value |
|--------|---------|-------|
| **Grounding** | Provides references/citations for every extracted output to the original document content | Ensures traceability, compliance, and user trust |
| **Confidence scoring** | Quantifies the model’s certainty in each prediction through confidence scores. | Drives automation with quality controls |
| **In-context learning** | Teaches the model new patterns using examples and correcting the predicted outputs for incorrect values, improving overall accuracy and extraction quality. | Rapidly adapts to new formats or edge cases |

> [!NOTE]
> These features are only available for the extractive field type. (Method == Extract)

Learn more about these features below.

## Grounding: Trace every result to its source 

Grounding ensures that every extracted field, answer, or classification has a reference to its original location in the document. This includes source information: page number and spatial coordinates, and spans: offset and length details. 

### Why grounding matters

In enterprise workflows, accuracy is not enough; you also need traceability. When a model extracts a customer name or a termination clause, you must be able to validate where that information came from. Grounding is critical for:
- Maintaining clear traceability and localization of extracted data for any extracted output like clauses, financial numbers, tables, insurance ID, etc.
- Ensure transparency with internal compliance checks.
- Use efficient human-in-the-loop validation from the actual reference source.

### Example

You want to extract the *termination clause* from a contract. The model returns:

- **Extracted text**: "Either party may terminate this agreement with 60 days’ notice."
-	"spans":  [ <br>
              { <br>
                "offset": 343, <br>
                "length": 102 <br>
              } <br>
            ] <br>
- **Source**: <br>
	  Page: 3 <br>
	  Coordinates: ({x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4})

Span indicates the element's logical position using character offset and length, while source gives its visual position with page number and bounding box coordinates. 

With this grounding data, your legal team can verify the extraction by jumping directly to the source paragraph in the PDF. This eliminates guesswork and builds trust in the application output.


## Confidence scoring: Automate with control

Every extraction field type comes with a confidence score between 0 and 1, indicating how certain the model is about the result. This number gives you a tunable point to automate high-confidence results and flag lower-confidence outputs for human reviews.

### Why confidence score matters

Confidence score let you design intelligent workflows, such as:
- Auto-approving extractions when confidence is above a defined threshold to intelligently automate document processing tasks.
- Optimizing resource allocation by reducing operational costs and using human-in-the-loop review for critical aspects.
- Rejecting or flagging extractions below a certain threshold for manual intervention, enhancing decision-making accuracy.

### Example

You're processing scanned utility bills to extract billing address and amount due. For a document:

- **Billing address**: "1234 Market St., San Francisco, CA" → Confidence: 0.96
- **Amount due**: "$128.74" → Confidence: 0.52

In this case, your automation pipeline can post the billing address directly to your downstream application while routing the amount due to a human for verification. By using confidence scores, you reduce manual effort while maintaining accuracy.


## In-context learning: Teach the model by giving examples

If the context for all the fields is clearly provided in the testing document, a zero-shot document extraction call should be sufficient. In-context learning allows you to provide extra labeled examples in Foundry to guide the model’s behavior without the need for retraining or fine-tuning. The model uses these examples to adapt to new formats, naming conventions, or extraction rules by correcting itself.

To enhance the model quality: 
- For datasets with minimal template variations, you can add just a single labeled example. 
- For more complex variations, add a sample per templates to cover all the scenarios.


### Why in-context learning matters

To manage diverse layout changes across different versions, templates, languages, or regions, help the model learn by adding examples.

In-context learning helps: 
- Provide context for the model to understand the meaning of each field by examples and thus improve model accuracy.
- Rapidly onboard new templates without labeling data within a single analyzer.
- Add samples only when dealing with lower confidence scores or incomplete/partial extraction.

To add a label sample, go to a document extraction result page in the Azure AI Foundry portal and select the **Label data** tab. Upload a sample, and select the **Auto label** button. Auto label predicts all the fields out of the box.

:::image type="content" source="../media/document/in-context-learning.png" lightbox="../media/document/in-context-learning.png" alt-text="Screenshot of auto labeling an invoice sample.":::

Then you can edit the fields by selecting the correct values. Once you save it, it shows with the **corrected** tag for all the extracted fields that were corrected. 

:::image type="content" source="../media/document/label-corrected.png" lightbox="../media/document/label-corrected.png" alt-text="Screenshot of corrected labels.":::

> [!NOTE]
> Labeled samples can be added in the Azure AI Foundry portal. Once samples are added, you need to build the analyzer again so that samples can take effect. This will not improve any OCR corrections or generative fields output. (Method == `Generate` or `Classify`)

### Example

You start receiving invoices from a new vendor that uses the label "Invoice Total" instead of "Amount Due." The model keeps missing the correct value. Instead of retraining, you can add an example of the different invoice vendor.

The model will now refer to this pattern to correctly extract the value in future similar types of documents, even though it wasn’t part of the original training data.

## A complete workflow

For building an intelligent document automation pipeline, these capabilities help you reliably extract and scale the application. For example if you want to process procurement contracts, you extract:
- Vendor name
- Start and end dates
- Cancellation clause

To ensure quality and trust, which is critical for enterprise-scale document understanding:
- **Grounding** gives your team full traceability to every field.
- **Confidence scores** helps you automate, as human review is needed only when threshold is low.
- **In-context learning** lets your model adapt to new contract templates or handling edge cases using just a few labeled examples.



