---
title: Azure Content Understanding in Foundry Tools Classifier Overview
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools classifier solutions.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 03/23/2026
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
  - dev-focus
ai-usage: ai-assisted
---

# Content Understanding classification/segmentation

Content Understanding lets you implement classification and splitting as part of the analyzer operation request. You can perform content classification and content extraction as part of a single API call. 

The global concept of `analyzer` now includes the concept of `contentCategories` and `enableSegment` to classify and split the input data you process within your application. This analyzer feature can perform classification of an input file as a whole. It can also identify multiple documents or multiple instances of a single document within an input file. 

Starting with the GA version, document classification and video segmentation design are unified, allowing for a coherent approach to process input data regardless of its modality. In the documentation, "Content Understanding classification" refers to the analyze operations required for classifying and splitting input data (`contentCategories` and `enableSegment`).

## Business use cases

Content Understanding classification lets you process complex documents and videos in various formats and templates:

* **Invoices**: Categorize invoices from multiple vendors to process each category with a different Content Understanding analyzer, if needed.
* **Tax documents**: Categorize multiple tax documents into different types of tax forms, such as 1040 and 1099.
* **Contracts**: Categorize long, unstructured contracts to streamline operations to understand different types of agreements and their specific legal implications.
* **Sports video**: Automatically segment the scenes to break the video into logical chunks such as ads and the actual sports content.

## Classification/segmentation capabilities

Content Understanding can analyze single or multi-file documents to identify whether an input file can be classified into a defined category. The following scenarios are supported:

**Document scenarios:**
* **Classify only**: Classifies the input file as a whole. For example, a single file that contains one document type, such as a loan application form.
* **Classify and analyze**: Classifies and analyzes the input file by routing the input to the desired extraction analyzer.
* **Classify and segment**: Classifies and segments a single input file that might have multiple types or instances of documents concatenated. For example, a loan application package that contains a loan application form, pay slip, and bank statement. Another example is a collection of scanned invoices in a single file.
* **Classify, segment, and analyze**: Once the segments are classified, route each segment to the desired extraction analyzer for further field extraction.
* **[Hierarchical classifier](#hierarchical-classifier)**: Optional additional analysis depending on the category can also be a classifier analyzer.

**Video scenarios:**
* **Segment only**: Split video into segments based on content characteristics defined in the `description` field of `contentCategories`. For example, splitting a sports broadcast into game play, commercials, and commentary segments.
* **Segment and analyze**: Split video into segments and route each segment to an analyzer for field extraction.

> [!NOTE]
> The minimum unit for classification of documents is a single page. Intra-page classification isn't supported.

### Create classification categories

Content Understanding classification doesn't require a training dataset. You can define up to 200 category names and descriptions within the analyze operation. By default, the entire file is treated as a single content object, which means the file is associated with a single category.

Starting with the GA version, you need to include the `other` category within the `contentCategories` to ensure that content can remain unmatched to any of your defined categories. If the `other` category isn't included, all files are classified into one of your defined categories. Each of the category names you define within `contentCategories` can also include a `description` to give further information about the category you're defining.


### Input file splitting

When you have more than one document in a file, the classifier can identify the different document types that are contained within the input file with splitting capability. The classifier response contains the page ranges for each of the identified document types that are contained within a file. This response can include multiple instances of the same document type.

When you run the `analyze` operation, it includes an `enableSegment` property that gives you granular control over the splitting behavior. You can also specify the page numbers to analyze only certain pages of the input document:

* To treat the entire input file as multiple documents combined together for classification, set `enableSegment` to `true`. When you do so, the service returns categories for the segments within the input file automatically.
* To treat the entire input file as a single document, set `enableSegment` to `false`.

> [!NOTE]
> For videos, only segmentation is supported. You must define a single `contentCategories` with `enableSegment` set to `true`. Use the `description` field to specify criteria for splitting the video into segments.


### Optional analysis

For a complete end-to-end flow, you can link classifier categories with existing custom analyzers and prebuilt analyzers. For each content object classified to categories with linked analyzers, the service automatically invokes analysis on the content object by using the corresponding analyzer.

For example, you can use this linking to create classifiers that identify and analyze only invoices from a PDF that contains multiple types of forms. Set `analyzerId` to a prebuilt analyzer or custom analyzer to route and perform field extraction from the classified documents or pages.

You can also omit setting any `analyzerId` to categorize, but not perform any content analysis on the categorized file or segment.

At the top layer, you can also set `omitContent` to `true` to omit the original content object and return only content objects from analysis performed on the classified segments or files.

#### Hierarchical classifier

The analyzer operation supports hierarchical splitting and classification. For example, within the base analyzer operation, you can set the `analyzerID` for content categories to a custom analyzer that performs additional classification or splitting. Hierarchical analyzers support scenarios such as categorizing document types like invoices, contracts, and receipts, where the `analyzerID` for each category can itself be an analyze operation with additional classification enabled for different document subtypes.

Document inputs support five levels of nesting, and video inputs support two.

## Classifier limits

For information on supported input document formats and classifier limits, see [Service quotas and limits](../service-limits.md#basic-limits).

## Best practices

To improve classification and splitting quality, use a good category name and description so that the model can understand the categories with some context. For more information on category names and descriptions, see [Best practices](../concepts/best-practices.md#optimize-classification-and-categorization).

### Key benefits

* **Accuracy and reliability**: Ensure precise document classification to reduce errors and boost efficiency.
* **Scalability**: Scale out document processing to meet business demands.
* **Customizable**: Adapt the document classifier to fit specific workflows.

## Supported languages and regions

For a list of supported languages and regions, see [Language and region support](../language-region-support.md).

## Data privacy and security

If you use Content Understanding, review Microsoft policies on customer data. For more information, see [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy).

## Related content

* Try processing your document content in [Content Understanding Studio](../quickstart/content-understanding-studio.md)
* Learn about how to process document content using [analyzer templates](../concepts/analyzer-templates.md).
