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

# Content Understanding classifier

You can use the Azure AI Content Understanding classifier to detect and identify documents that you process within your application. The Content Understanding classifier can perform classification of an input file as a whole. It can also identify multiple documents or multiple instances of a single document within an input file.

> [!IMPORTANT]
>
> The Azure AI Content Understanding classifier is available only in the `2025-05-01-preview` release. Public preview releases provide early access to features that are in active development. Features, approaches, and processes can change or have limited capabilities before general availability. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

## Business use cases

The classifier can process complex documents in various formats and templates:

* **Invoices**: Categorize invoices from multiple vendors to process each category with a different Content Understanding analyzer, if needed.
* **Tax documents**: Categorize multiple tax documents into different types of tax forms, such as 1040 and 1099.
* **Contracts**: Categorize long, unstructured contracts to streamline operations to understand different types of agreements and their specific legal implications.

## Content Understanding classifier capabilities

The Content Understanding classifier can analyze single or multifile documents to identify if an input file can be classified into a category as defined. The following scenarios are supported:

* A single file that contains one document type, such as a loan application form.
* A single file that contains multiple document types. An example is a loan application package that contains a loan application form, pay slip, and bank statement.
* A single file that contains multiple instances of the same document. An example is a collection of scanned invoices.
* By default, an `$OTHER` class is used for cases where none of the defined categories seems suitable.

### Use the Content Understanding classifier

A Content Understanding classifier doesn't require any training dataset. You can define up to 50 category names and descriptions and create a classifier. By default, the entire file is treated as a single content object, which means the file or object is associated to a single category.

When you have more than one document in a file, the classifier can identify the different document types that are contained within the input file with splitting capability. The classifier response contains the page ranges for each of the identified document types that are contained within a file. This response can include multiple instances of the same document type.

When you call the classifier, the `analyze` operation includes a `splitMode` property that gives you granular control over the splitting behavior. You can also specify the page numbers to analyze only certain pages of the input document:

* To treat the entire input file as a single document for classification, set `splitMode` to `none`. When you do so, the service returns one category for the entire input file.
* To classify each page of the input file, set `splitMode` to `perPage`. The service attempts to classify each page as an individual document.
* To identify the documents and associated page ranges, set `splitMode` to `auto`.

### Optional analysis

For a complete end-to-end flow, you can link classifier categories with existing analyzers. For each content object classified to categories with linked analyzers, the service automatically invokes analysis on the content object by using the corresponding analyzer.

For example, you can use this linking to create classifiers that identify and analyze only invoices from a PDF that contains multiple types of forms in a document. Set `analyzerId` to an existing analyzer to route and perform field extraction from the classified documents or pages.

## Classifier limits

For information on supported input document formats and classifier limits, see [Service quotas and limits](../service-limits.md#classifier).

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
