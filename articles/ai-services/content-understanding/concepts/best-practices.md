---
title: Best practices for using Content Understanding
titleSuffix: Azure AI services
description: Learn how to best use Azure AI Content Understanding for document, image, video, and audio file content and field extractions.
author: laujan
ms.author: jfilcik
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/19/2025
---

# Best practices for Azure AI Content Understanding

Azure AI Content Understanding is an innovative Generative AI service designed to facilitate the precise and accurate analysis of extensive data sets. The service processes various content modalities, including documents, images, videos, and audio, transforming them into user-specified output formats.

This document provides guidance and best practices to effectively utilize Content Understanding for your data processing and analysis requirements.

## Use field descriptions to guide output

When defining a schema, it's essential to provide detailed field descriptions. Clear and concise descriptions guide the model to focus on the correct information, improving the accuracy of the output.

##### &emsp; ***Example 1***

  * If you want to extract the date from an invoice, in addition to naming the field `Date`, provide a description such as:


    > `The date when the invoice was issued, typically found at the top right corner of the document.`


##### &emsp; ***Example 2***

   * Suppose you want to extract the `Customer Name` from an invoice. Your description might read:

     > `The name of the customer or client to whom this invoice is addressed, usually located near the billing address. It should be the name of the business or person, but not the entire mailing address.`

## Correct mistakes by editing field descriptions

If the system's output isn't meeting expectations, the first step is to try refining and updating the field descriptions. Clarifying the context and being more explicit about what you need, reduces ambiguity and improves accuracy.

##### &emsp; ***Example 3***

   * If the `Shipping date` field generated inconsistent or incorrect extraction, often after a `Dispatch Date` label, update it to something more precise like:

     > `The date when the products were shipped, typically found below the item list. It may also be labeled something similar like Delivery Date or Dispatch Date. Dates should typically have a format like 1/23/2024 or 01-04-2025.`

   * This extra context guides the model to the right location in the document.


## Use classification fields for specific outputs

When you need the system to choose from a set of predefined options, for example, document type, product category, or status, use classification fields. Where there's ambiguity with the options, provide clear descriptions for each option, enabling the model to categorize the data accurately.

##### &emsp; ***Example 4***

   * If you need to classify documents as either `Invoice`, `Claim`, or `Report`, create a classification field with these words as category names.

##### &emsp; ***Example 5***

   * When processing product images, you might need to assign them to categories like `AlcoholicDrinks`, `SoftDrinks`, `Snacks`, and `DairyProducts`. Since some items can appear similar, providing precise definitions for close-call cases can help. For example:

     * **`Alcoholic Drinks`**: Beverages containing alcohol, such as beer, wine, and spirits. This category excludes soft drinks or other nonalcoholic beverages.

     * **`Soft Drinks`**: Carbonated nonalcoholic beverages, such as soda and sparkling water. This category doesn't include juices or alcoholic drinks.

   * By clearly defining each category, you ensure that the system correctly classifies products while minimizing misclassification.

## Use confidence scores to determine when human review is needed

Confidence scores help you decide when to involve human reviewers. Customers can interpret confidence scores using thresholds to decide which results need more reviews, minimizing the risk of errors.

   ##### &emsp; ***Example 6***

   * For an invoice review use case, if a key extracted field like `TotalInvoiceAmount` has a confidence score under **0.80**, route that document to manual review. This helps ensure that a human verifies critical fields like invoice totals or legal statements when necessary.

   * You might set different confidence thresholds based on the type of field. For instance, a lower threshold for a `Comments` field that's less critical and a higher one for `ContractTerminationDate` to ensure no mistakes.

## Reduce errors by narrowing language selection for audio and video

When you're working with audio and video content, selecting a narrow set of languages for transcription can potentially reduce errors. The more languages you include, the more the system has to guess which language is being spoken, which can increase misrecognition.

##### &emsp; ***Example 7***

   * If you're certain that the content only contains English and Spanish, configuring your transcription to only these two languages can improve quality. But if the content accidentally includes other languages, such configuration can actually degrade overall quality.

## Transcript, document text, and speaker data: fields not required

By default, Content Extraction information such as speech transcripts, document text extracted by `OCR`, and video key frames can be accessed directly from the analyzer output for immediate review or custom processing. There's no need to define a field in the schema for these items. Fields can be used when more processing is needed, for example, summarizing transcripts, identifying entities, or extracting specific items from `OCR`. Each field can instruct the system to extract or generate the content you need.

## Classifier category names and descriptions

To improve the classifier and splitting accuracy, it's important to give a good category name and description with context. For example:

* Common titles for category names (ex. Annual Financial Report, SEC Form 10-K)
* Semantic definition of the category for descriptions (ex. receipts for expense reporting)
* Common layout of the initial page in the description (two-column form)
* Key content that uniquely identifies a category as a description ("2025" on the upper right)

