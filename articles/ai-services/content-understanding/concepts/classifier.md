---
title: Azure AI Content Understanding Classifier Overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding classifier solutions.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 09/16/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Content Understanding classification/segmentation

Azure AI Content Understanding doesn't have an explicit classifier API. Classifier is now part of the analyzer operation request that you would send in for any analysis, eliminating the need to call two separate APIs to perform content classification and content extraction at once. The global concept of `analyzer` now includes the concept of `contentCategories` and `enableSegment` to classify and split the input data that you process within your application. This feature within the analyzer can perform classification of an input file as a whole. It can also identify multiple documents or multiple instances of a single document within an input file. Starting with the GA version, document classification and video segmentation design is now unified, allowing for a coherent approach to classify input data regardless of its modality. In this documentation, Content Understanding classification refers to analyze operations needed (`contentCategories` and `enableSegment`) for classifying and splitting input data.

## Business use cases

Content Understanding classification can allow for processing complex documents and videos in various formats and templates:

* **Invoices**: Categorize invoices from multiple vendors to process each category with a different Content Understanding analyzer, if needed.
* **Tax documents**: Categorize multiple tax documents into different types of tax forms, such as 1040 and 1099.
* **Contracts**: Categorize long, unstructured contracts to streamline operations to understand different types of agreements and their specific legal implications.
* **Sports video**: Automatically segment the scenes to break the video into logical chunks such as ads and the actual sports content.

## Content Understanding classification/segmentation capabilities

Content Understanding classification can analyze single or multifile documents to identify if an input file can be classified into a category as defined. The following scenarios are supported:

* A single file that contains one document type, such as a loan application form.
* A single file that contains multiple document types. An example is a loan application package that contains a loan application form, pay slip, and bank statement.
* A single file that contains multiple instances of the same document. An example is a collection of scanned invoices.
* Starting with GA version,`$OTHER` class isn't included as default. To filter out the data, add the `$OTHER` class explicitly.

### Use Content Understanding classification/segmentation

Content Understanding classification doesn't require any training dataset. You can define up to 200 category names and descriptions within the analyze operation. By default, the entire file is treated as a single content object, which means the file will be associated to a single category.

Starting with the GA version, you need to include the `other` within the `contentCategories` to ensure that the content can't be matched to any of your defined categories. If the `other` category is unincluded, all of the files is forced to be classified  into one of the categories you have set in the `contentCategories`. Each of the category names you define within `contentCategories` can also include `description` to give further information about the category you're defining.

When you have more than one document in a file, the classifier can identify the different document types that are contained within the input file with splitting capability. The classifier response contains the page ranges for each of the identified document types that are contained within a file. This response can include multiple instances of the same document type.

When you run the `analyze` operation, it now includes a `enableSegment` property that gives you granular control over the splitting behavior. You can also specify the page numbers to analyze only certain pages of the input document:

* To treat the entire input file as multiple documents combined together for classification, set `enableSegment` to `true`. When you do so, the service returns categories for the segments within the input file automatically. Likewise for any videos, it categorizes each segment with respect to its included classified category.
* To treat the entire input file as a single document or a video, set `enableSegment` to `false`.


### Optional analysis

For a complete end-to-end flow, you can link classifier categories with existing custom analyzers and prebuilt analyzers. For each content object classified to categories with linked analyzers, the service automatically invokes analysis on the content object by using the corresponding analyzer.

For example, you can use this linking to create classifiers that identify and analyze only invoices from a PDF that contains multiple types of forms in a document. Set `analyzerId` to one of our prebuilt analyzers or custom analyzers to route and perform field extraction from the classified documents or pages.

You can also omit setting any `analyzerId` to categorize, but not perform any content analysis on the categorized file or segment.

On the top layer, you can also specify `omitContent` as true to ensure that original content object is omitted and only return content objects from additional analysis performed on the classified segment or files.

#### Hierarchical classifier

The newly designed analyzer operation allows for hierarchical splitting and classification. For example, within the base analyzer operation, you can set the `analyzerID` for the content categories you defined with your custom analyzer that performs additional classification or splitting, depending on the need. Defining herarchical analyzers allow for scenarios such as categorizing different types of documents like invoices, contracts, and receipts, with the analyzerID for each of these categories can also be an analyze operation with additional classification enabled for different types of files within invoices, contracts, and receipts. 

## Classifier limits

For information on supported input document formats and classifier limits, see [Service quotas and limits](../service-limits.md#segmentationclassification).

## Best practices

To improve classification and splitting quality, use a good category name and description so that the model can understand the categories with some context. For more information on category names and descriptions, see [Best practices](../concepts/best-practices.md#classifier-category-names-and-descriptions).

## Key benefits

* **Accuracy and reliability**: Ensure precise document classification to reduce errors and boost efficiency.
* **Scalability**: Scale out document processing to meet business demands.
* **Customizable**: Adapt the document classifier to fit specific workflows.

## Supported languages and regions

For a list of supported languages and regions, see [Language and region support](../language-region-support.md).

## Data privacy and security

Developers who use Content Understanding should review Microsoft policies on customer data. For more information, see [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy).

## Related content

* Try processing your document content by using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
* Learn to analyze document content [analyzer templates](../quickstart/use-ai-foundry.md).
