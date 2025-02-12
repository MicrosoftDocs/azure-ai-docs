# Best Practices for Content Understanding

## Overview
This document provides guidance on how to effectively use Content Understanding for processing and analyzing various kinds of data.

---

## Use Field Descriptions to Guide Output
When defining a schema, it is essential to provide detailed field descriptions and examples. Clear descriptions and relevant examples guide the model to focus on the correct information, improving the accuracy of the output.

### Example 1:
If you want to extract the date from an invoice, in addition to naming the field `"Date"`, provide a description such as:
> **"The date when the invoice was issued, typically found at the top right corner of the document."**

### Example 2:
Suppose you want to extract the `"Customer Name"` from an invoice. Your description might read:
> **"It should be the name of the business or person, but not the entire mailing address. The name of the customer or client to whom this invoice is addressed, usually located near the billing address."**

---

## Fix Mistakes by Editing Field Descriptions
If the system’s output isn’t meeting expectations, the first thing to try is refining and updating the field descriptions. By clarifying the context and being more explicit about what you need, you reduce ambiguity and improve accuracy.

### Example:
If the `"Shipping date"` field generated inconsistent or incorrect extraction, often after a "Dispatch Date" label, update it to something more precise like:
> **"The date when the products were shipped, typically found below the item list. It may also be labeled something similar like Delivery Date or Dispatch Date. Dates should typically have a format like 1/23/2024 or 01-04-2025."**

This extra context guides the model to the right location in the document.

---

## Use Classification Fields for Specific Outputs
When you need the system to choose from a set of predefined options (e.g., document type, product category, or status), use classification fields. When there's ambiguity with the options, provide clear descriptions for each option, enabling the model to categorize the data accurately.

### Example 1:
If you need to classify documents as either `"Invoice"`, `"Claim"`, or `"Report"`, create a classification field with these words as class names.

### Example 2:
When processing product images, you might need to assign them to categories like `"Alcoholic Drinks"`, `"Soft Drinks"`, `"Snacks"`, and `"Dairy Products"`. Since some items may appear similar, providing precise definitions for close-call cases can help. For example:

- **`"Alcoholic Drinks"`**: Beverages containing alcohol, such as beer, wine, and spirits. This excludes soft drinks or non-alcoholic beverages.
- **`"Soft Drinks"`**: Carbonated non-alcoholic beverages, such as soda and sparkling water. This does not include juices or alcoholic drinks.

By clearly defining each category, you ensure that the system correctly classifies products while minimizing misclassification.

---

## Use Confidence Scores to Determine When Human Review is Needed
Confidence scores help you decide when to involve human reviewers. Customers can interpret confidence scores using thresholds to decide which results need more review, minimizing the risk of errors.

### Example:
For an Invoice review use case, if a key extracted field like `"Total Invoice Amount"` has a confidence score under **80%**, the system routes that document for manual review. This ensures that critical fields like invoice totals or legal statements are verified by a human when necessary.

You might set different confidence thresholds based on the type of field. For instance, a lower threshold for a `"comments"` field that’s less critical and a higher one for `"contract termination date"` to ensure no mistakes.

---

## Reduce Errors by Narrowing Language Selection for Audio and Video
When working with audio and video content, selecting a narrow set of languages for transcription significantly reduces errors. The more languages you include, the more the system has to guess which language is being spoken, which can lead to increased misclassifications.

### Example 1:
If your content is only in English and Spanish, configure your transcription to those two languages only. Avoid adding options like French or Arabic unless you truly need them.

### Example 2:
If you have conference calls that occasionally include Portuguese speakers, add Portuguese only for those meetings. For all other calls, stick to English if that’s what you expect 90% of the time.

---

## Transcript, OCR Text, and Speaker Data Don’t Require Fields
By default, Content Extraction information such as transcripts, OCR results, and video key frames can be accessed directly for immediate review or custom processing. Fields can be used when advanced transformations are needed (e.g., summarizing transcripts, identifying entities, or extracting specific items from OCR). Each field can instruct the system to extract or generate the content you need.

---

## Connect Analyzer to an Existing Content Understanding Project via REST API
To connect an analyzer created through the REST API to an existing Content Understanding project, add the following `tags` to the analyzer JSON:

```json
"projectId": "<add your project's ID here! You can find the projectId on the Azure Portal in the Overview of the project resource or by reading any analyzer you created via the project in AI Foundry through the REST API>",
"templateId": "postCallAnalytics-2024-12-01"
```

### Example:
```json
"tags": {"projectId": "1232abcdef1234","templateId": "postCallAnalytics-2024-12-01"}
```

### Available Template IDs:
| Modality  | Template IDs |
|-----------|-------------|
| **Audio** | postCallAnalytics-2024-12-01, conversationAnalysis-2024-12-01 |
| **Text**  | text-2024-12-01 |
| **Image** | image-2024-12-01 |
| **Document** | - |
| **Video** | - |

---
