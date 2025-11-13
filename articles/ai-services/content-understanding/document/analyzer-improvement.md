---
title: "Document analysis with confidence, grounding, and labeled samples"
titleSuffix: Azure AI services
description: Learn about Azure Content Understanding in Foundry Tools's value add-ons that improve model extraction quality and performance
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 08/11/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - ignite-2025
---


# Validate document analyzer quality with confidence, grounding, and improve with labeled samples

Processing unstructured documents like contracts and statements of work, or structured documents like invoices and insurance forms, is critical for accelerating business value in workflows (IDP), ingesting information for RAG and  agentic workflows. Extracting this data reliably, at scale, requires more capabilities than just text/content extraction. Intelligent document processing requires information like what was extracted, why it was extracted, did the extracted value align with the intent, and how reliably was it extracted.

Most enterprises face the following challenges when handling various documents at scale:
- Need to **automate workflows**, but only when the extraction meets an accuracy threshold that is required for the business application. You need to know how confident/accurate the analyzer is in its results.
- Need to **validate the sources** of extracted data for true reference. When seeing lower than expected confidence scores, validate the results quickly by reviewing the specific location in the document.
- Ideally, require ways to **improve the quality of the analyzer results** (by providing a few labeled examples) when it gets something wrong or encounters a new format with lower than expected confidence scores.

Azure Content Understanding in Foundry Tools provides critical features for post-processing your extracted output.

| Feature | Purpose | Value |
|--------|---------|-------|
| **Confidence scoring** | Quantifies the analyzer's certainty in each prediction through confidence scores. | Enables STP (Straight Through Processing) |
| **Grounding** | Provides references/citations for every extracted output to the original document content | Ensures traceability, compliance, and user trust |
| **Labeled samples** | Provides examples to the analyzer on new patterns using examples and correcting the predicted outputs for incorrect values, improving overall accuracy and extraction quality. | Rapidly adapts to new formats or edge cases |

> [!NOTE]
> These features are only available for the extractive field type. (Method == Extract)

Learn more about these features below.

## Confidence scoring: Automate with control

Every field type now can generate a confidence score between 0 and 1, indicating how certain the analyzer is about the result. This number gives you a tunable point to automate high-confidence results and flag lower-confidence outputs for human reviews. The confidence scores can be enabled for all fields on an analyzer or on specific fields using the ```estimateFieldSourceAndConfidence``` property. Learn more about [configuring confidence scores for analyzers](../concepts/analyzer-reference.md#estimatefieldsourceandconfidence).

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

## Grounding: Trace every result to its source 

Grounding ensures that every  field, answer, or classification has a reference to its original location in the document. This includes source information: page number and spatial coordinates, and spans: offset and length details. 

### Why grounding matters

In enterprise workflows, accuracy isn't enough; you also need traceability. When a model extracts a customer name or a termination clause, you must be able to validate where that information came from. Grounding is critical for:
- Maintaining clear traceability and localization of extracted data for any extracted output like clauses, financial numbers, tables, insurance ID, etc.
- Ensure transparency with internal compliance checks.
- Use efficient human-in-the-loop validation from the actual reference source. Navigate to the page, section, and content that provided the field value.

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


## Labeled samples (In-context learning): Improve with examples

If the context for all the fields is clearly provided in the testing document, a zero-shot document extraction call should be sufficient. Start with following the [best practices for schema definitions](../concepts/best-practices.md), if you are still seeing field values being extracted incorrectly or confidence scores below the threshold you want to straight through process, labeled samples or in-context learning can target analyzer improvements. The analyzer uses these examples  at analyze time to adapt to new formats, naming conventions, or extraction rules by correcting itself.

To enhance the model quality: 
- For datasets with minimal template variations, you can add just a single labeled example. 
- For more complex variations, where you see extraction quality issues, add a sample per templates to cover all the scenarios.


### Why labeled samples matter

To manage diverse layout changes across different versions, templates, languages, or regions, help the analyzer learn by adding examples.

In-context learning helps: 
- Provide context for the analyzer to recognize the different ways the field could be represented in input documents and thus improve model accuracy.
- Rapidly onboard new templates within a single analyzer.
- Add samples only when dealing with lower confidence scores or incomplete/partial extraction.

To add a label sample, go to a document extraction result page in the Azure AI Studio and select the **Label data** tab. Upload a sample, and select the **Auto label** button. Auto label, runs the existing analyzer to prepopulate the results that you can now update.

:::image type="content" source="../media/document/in-context-learning.png" lightbox="../media/document/in-context-learning.png" alt-text="Screenshot of auto labeling an invoice sample.":::

Then you can edit the fields by selecting the correct values. Once you save it, it shows with the **corrected** tag for all the extracted fields that were corrected. 

:::image type="content" source="../media/document/label-corrected.png" lightbox="../media/document/label-corrected.png" alt-text="Screenshot of corrected labels.":::

> [!NOTE]
> Labeled samples can be added in the Content Understanding Studio. Once samples are added, you need to build the analyzer again so that samples re available for the analyzer to use. 

### Limitations

Labeled samples don't correct any text recognition issues. For instance if the letter `l` is recognized as the digit `1`, labeling the value as the letter `l` will not improve the extraction quality. OCR errors aren't currently in scope for analyzer improvement with labeling.

### Example

You start receiving invoices from a new vendor that produces a lower than expected confidence scores on the amount due field or incorrectly extracts the total amount value for those specific invoices. You can now add an example of the invoice with the labeled values. This improves the quality of the extracted values for the variations labeled.

The analyzer will now generalize better on this pattern to correctly extract the value for similar templates of documents.

## A complete workflow

For building an intelligent document automation pipeline, these capabilities help you reliably extract and scale the application. For example if you want to process procurement contracts, you extract:
- Vendor name
- Start and end dates
- Cancellation clause

To ensure quality and trust, which is critical for enterprise-scale document understanding:
- **Grounding** gives your team full traceability to every field.
- **Confidence scores** helps you automate, as human review is needed only when threshold is low.
- **In-context learning** lets your model adapt to new contract templates or handling edge cases using just a few labeled examples.

## Next steps

* [Review analyzer best practices](../concepts/best-practices.md)
* [Build a custom analyzer in the Studio](../quickstart/content-understanding-studio.md)




