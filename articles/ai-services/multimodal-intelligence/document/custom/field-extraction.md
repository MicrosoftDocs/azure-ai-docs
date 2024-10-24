---
title: Azure AI Multimodal Intelligence custom document field extraction (preview)
titleSuffix: Azure AI services
description: Learn about Azure AI Multimodal Intelligence document solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 10/24/2024
---


# Azure AI Multimodal Intelligence custom document field extraction (preview)

> [!IMPORTANT]
>
> * Azure AI Multimodal Intelligence is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Multimodal Intelligence custom document field extraction uses generative AI to extract user-specified fields from documents across a wide variety of visual templates. The capability combines the power of document understanding with Large Language Models (`LLM`s) with the rigor and schema of custom extraction capabilities to create models with high accuracy in minutes.

With this new model type, you can start with a single document and go through the schema addition and model creation process with minimal labeling. Additionally, you can use [Azure AI studio](https://ai.azure.com/) for an interactive experience to train and test your custom model. Custom Document Field Extraction allows you to easily automate your data extraction workflows for any type of document, with greater accuracy and speed. The Multimodal Intelligence document capabilities enable access to the following benefits:

* **Automatic labeling**. Utilizing the generative AI document model, rather than manual annotation, saves time and effort. You can create models faster by using `LLM`s to extract data from various document types.

* **Improved Generalization**. Extract data with high accuracy across documents with unstructured data and varying document templates.

* **Grounded results**. Localize the data extracted from documents. Custom generative models ground the results where applicable, ensuring that the response is generated from the content and enabling human review workflows.

* **Confidence scores**. Use confidence scores for each extracted field to filter high quality extracted data, maximize straight-through processing, and minimize human review costs.

## Features and capabilities

Custom document field extraction currently supports the following fields:

|Form fields|Selection marks|Tabular fields|Signature|Region labeling|Overlapping fields|
|-----------|---------------|--------------|---------|---------------|------------------|
|Supported|Supported|Supported|Unsupported|Unsupported|Supported|

## Common use cassette

Custom Document Field Extraction can process complex documents with various formats, templates, and unstructured data:

* **Contract Lifecycle Management**. Contracts are complex documents with various formats, clauses, and types. With custom generative AI you can build a model to extract fields, clauses, and obligations from any type of contract.

* **Loan and Mortgage Applications**. Automation of loan and mortgage application processing enables banks, lenders, and government agencies to quickly process loan and mortgage application.

* **Financial Services**. Build models to accurately analyze complex documents like financial reports, asset management reports and more.

* **Expense management**. Receipts and invoices from various retailers and businesses need to be parsed to validate expenses. Custom generative AI can extract expenses across different formats and documents with varying templates.

## Supported languages

| Language  Locale code | Default |
|:----------------------|:---------|
| English (United States) `en-US`| English (United States) `en-US`|

## Supported regions

During the public preview, custom document field extraction model capabilities are only available in the following Azure regions:

* North Central US

* East US

## Input requirements

* For best results, provide one clear photo or high-quality scan per document.

* Supported file formats: `PDF`, `TIFF`.

* The file size for analyzing documents is 500 MB for paid (S0) tier and `4` MB for free (F0) tier.

* Image dimensions must be between 50 pixels x 50 pixels and 10,000 pixels x 10,000 pixels.

* If your PDFs are password-locked, you must remove the lock before submission.

* The minimum height of the text to be extracted is 12 pixels for a 1024 x 768 pixel image. This dimension corresponds to about `8` point text at 150 dots per inch (DPI).

* For custom model training, the maximum number of pages for training data is 1 GB.

## Best Practices

Generative AI models perform well extracting simple fields from documents with no labeled samples. Providing a few labeled samples improves the extraction accuracy for complex fields and user defined fields like tables.

* **Representative data**. Use representative documents that target actual data distribution. For example, if the target document tabular fields are  partially completed, add training documents with partially completed tables. Or if field is named date, values for this field should be a date as random strings can affect model performance.

* **Field naming**. Choose a precise field name that represents the field values. For example, for a field value containing the Transaction Date, consider naming the field TransactionDate instead of Date1.

* **Field Description**. Provide more contextual information in description to help clarify the field that needs to be extracted. Examples include location in the document, potential field labels it may be associated with, ways to differentiate with other terms that could be ambiguous.

* **Dealing with variation**. Custom generative models can generalize across different document templates of the same document type. As a best practice, create a single model for all variations of a document type. Ideally, include a visual template for each type.

## Preview limitations

* Custom document field extraction doesn't support fixed table and signature extraction.

* Inference on the same document could yield slightly different results across calls. This limitation is one that is known for current `GPT` models.

* Confidence scores for each field may vary. We recommend testing with your representative data to establish confidence thresholds for your scenario.

* Grounding, especially for tabular fields, is challenging and may not align in some cases.

* Latency for large documents is high.

* Composed models aren't supported in preview.


