---
title: Azure AI Content Understanding classifier overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding classifier solutions.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Content Understanding classifier

> [!IMPORTANT]
>
> * The classifier API is only available for documents with the `2025-05-01-preview` release.
> * Azure AI Content Understanding classifier is available in `2025-05-01-preview` release. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding classifier enables you to detect and identify documents you process within your application. Content Understanding classifier can perform classification of an input file as a whole, or identify multiple documents or multiple instances of a single document within an input file.

## Business use cases

Classifier can process complex documents in various formats and templates:

* **Invoices**: Categorize invoices from multiple vendors to process each category with a different Content Understanding analyzer if needed.
* **Tax documents**: Categorize multiple tax documents into different types of tax forms such as 1040, 1099, etc.
* **Contracts**: Long, unstructured contracts can now be categorized to streamline operations to understand different types of agreements and their specific legal implications.


## Content Understanding classifier capabilities

Content Understanding classifier can analyze a single- or multi-file documents to identify if an input file can be classified into a category as defined. Here are the currently supported scenarios:

* A single file containing one document type, such as a loan application form.
* A single file containing multiple document types. For instance, a loan application package that contains a loan application form, payslip, and bank statement.
* A single file containing multiple instances of the same document. For instance, a collection of scanned invoices.
* By default, there's an `$OTHER` class as well, which we utilize for cases where any of the defined categories doesn't seem suitable.


### How to use Content Understanding classifier

Content Understanding classifier doesn't require any training dataset. Define up to 50 category name and description and create a classifier. By default, the entire file is treated as a single content object, meaning the file/object is associated to a single category.

However, when you have more than one document in a file, the classifier can identify the different document types contained within the input file with splitting capability. The classifier response contains the page ranges for each of the identified document types contained within a file. This response can include multiple instances of the same document type.

When you call the classifier, the `analyze` operation includes a `splitMode` property that gives you granular control over the splitting behavior. You can also specify the page numbers to analyze only certain pages of the input document.

* To treat the entire input file as a single document for classification set the `splitMode` to `none`. When you do so, the service returns just one category for the entire input file.
* To classify each page of the input file, set the `splitMode` to `perPage`. The service attempts to classify each page as an individual document.
* Set the `splitMode` to `auto` and the service identifies the documents and associated page ranges.

### Optional analysis

For a complete end to end flow, you may link classifier categories with existing analyzers. For each content object classified to categories with linked analyzers, the service automatically invokes analysis on the content object using the corresponding analyzer. As an example, this linking can be used to create classifiers that identify and analyze only invoices from a PDF that may contain multiple types of forms in a document.

* Set the `analyzerId` to an existing analyzer to route and perform field extraction from the classified documents or pages.

### Classifier limits

For information on supported input document formats and classifier limits, refer to our [Service quotas and limits](../service-limits.md#classifier) page.


### Best practices

To improve classification and splitting quality, it's important to give a good category name and description so the model can understand the categories with some context. For more information on category names and descriptions, *see* [Best practices](../concepts/best-practices.md#classifier-category-names-and-descriptions).

## Key benefits

* **Accuracy and reliability:** Ensure precise document classification, reducing errors and boosting efficiency.
* **Scalability:** Seamlessly scale out document processing to meet business demands.
* **Customizable:** Adapt document classifier to fit specific workflows.

## Supported languages and regions
For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page.

## Data privacy and security
Developers using Content Understanding should review Microsoft's policies on customer data. For more information, visit our [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) page.

## Next step
* Try processing your document content using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
* Learn to analyze document content [**analyzer templates**](../quickstart/use-ai-foundry.md).
