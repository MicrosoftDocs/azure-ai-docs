---
title: Azure Content Understanding in Foundry Tools Classifier Overview
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools classifier solutions.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Content Understanding classification/segmentation

Content Understanding allows customers to implement classification and splitting as part of the analyzer operation request. You can perform content classification and content extraction as part of a single API call. 

The global concept of `analyzer` now includes the concept of `contentCategories` and `enableSegment` to classify and split the input data you process within your application. This analyzer feature can perform classification of an input file as a whole. It can also identify multiple documents or multiple instances of a single document within an input file. 

Starting with the GA version, document classification and video segmentation design are unified, allowing for a coherent approach to process input data regardless of its modality. In the documentation, "Content Understanding classification" refers to the analyze operations required for classifying and splitting input data (`contentCategories` and `enableSegment`).

## Business use cases

Content Understanding classification allows for processing complex documents and videos in various formats and templates:

* **Invoices**: Categorize invoices from multiple vendors to process each category with a different Content Understanding analyzer, if needed.
* **Tax documents**: Categorize multiple tax documents into different types of tax forms, such as 1040 and 1099.
* **Contracts**: Categorize long, unstructured contracts to streamline operations to understand different types of agreements and their specific legal implications.
* **Sports video**: Automatically segment the scenes to break the video into logical chunks such as ads and the actual sports content.

## Classification/segmentation capabilities

Content Understanding can analyze single or multi-file documents to identify if an input file can be classified into a category as defined. The following scenarios are supported:

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
> The minimum unit for classification of documents is a single page. Intra-page classification is not supported.

### Create classification categories

Content Understanding classification doesn't require a training dataset. You can define up to 200 category names and descriptions within the analyze operation. By default, the entire file is treated as a single content object, which means the file will be associated to a single category.

Starting with the GA version, you need to include the `other` category within the `contentCategories` to ensure that content can remain unmatched to any of your defined categories. If the `other` category is not included, all the files are forced to be classified into one of your defined categories. Each of the category names you define within `contentCategories` can also include a `description` to give further information about the category you're defining.


### Input file splitting

When you have more than one document in a file, the classifier can identify the different document types that are contained within the input file with splitting capability. The classifier response contains the page ranges for each of the identified document types that are contained within a file. This response can include multiple instances of the same document type.

When you run the `analyze` operation, it now includes a `enableSegment` property that gives you granular control over the splitting behavior. You can also specify the page numbers to analyze only certain pages of the input document:

* To treat the entire input file as multiple documents combined together for classification, set `enableSegment` to `true`. When you do so, the service returns categories for the segments within the input file automatically.
* To treat the entire input file as a single document, set `enableSegment` to `false`.

> [!NOTE]
> For videos, only segmentation is supported. You must define a single `contentCategories` with `enableSegment` set to `true`. Use the `description` field to specify criteria for splitting the video into segments.


### Optional analysis

For a complete end-to-end flow, you can link classifier categories with existing custom analyzers and prebuilt analyzers. For each content object classified to categories with linked analyzers, the service automatically invokes analysis on the content object by using the corresponding analyzer.

For example, you can use this linking to create classifiers that identify and analyze only invoices from a PDF that contains multiple types of forms in a document. Set `analyzerId` to one of our prebuilt analyzers or custom analyzers to route and perform field extraction from the classified documents or pages.

You can also omit setting any `analyzerId` to categorize, but not perform any content analysis on the categorized file or segment.

On the top layer, you can also specify `omitContent` as true to ensure that original content object is omitted and only return content objects from other analysis performed on the classified segment or files.

#### Hierarchical classifier

The newly designed analyzer operation allows for hierarchical splitting and classification. For example, within the base analyzer operation, you can set the `analyzerID` for the content categories you defined with your custom analyzer that performs additional classification or splitting, depending on the need. Defining hierarchical analyzers allow for scenarios such as categorizing different types of documents like invoices, contracts, and receipts, with the analyzerID for each of these categories can also be an analyze operation with additional classification enabled for different types of files within invoices, contracts, and receipts. 

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

Developers who use Content Understanding should review Microsoft policies on customer data. For more information, see [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy).

## Related content

* Try processing your document content in [Content Understanding Studio](../quickstart/content-understanding-studio.md)
* Learn about how to process document content using [analyzer templates](../concepts/analyzer-templates.md).
