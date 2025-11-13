---
title: Choose the best Document Intelligence model for your applications and workflows.
titleSuffix: Foundry Tools
description: Choose the best Document Intelligence model for your applications and workflows.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
---


# Which model should I choose?

Azure Document Intelligence in Foundry Tools supports a wide variety of models that enable you to add intelligent document processing to your applications and optimize your workflows. Selecting the right model is essential to ensure the success of your enterprise. In this article, we explore the available Document Intelligence models and provide guidance for how to choose the best solution for your projects.

> [!VIDEO 364078d4-14bc-4b16-995a-526db31ea1ee]

The following decision charts highlight the features of each supported model to help you choose the model that best meets the needs and requirements of your application.

> [!IMPORTANT]
> Be sure to check the [**language support**](../language-support/prebuilt.md) page for supported language text and field extraction  by feature.

## Pretrained document-analysis models

| Document type | Example| Data to extract | Your best solution |
| -----------------|-----------|--------|-------------------|
|**A generic document**. | A contract or letter. |You want to primarily extract written or printed text lines, words, locations, and detected languages.|[**Read OCR model**](../prebuilt/read.md)|
|**A document that includes structural information**. |A report or study.| In addition to written or printed text, you need to extract structural information like tables, selection marks, paragraphs, titles, headings, and subheadings.| [**Layout analysis model**](../prebuilt/layout.md)|
|**A structured or semi-structured document that includes content formatted as fields (keys) and values**.|A form or document that is a standardized format commonly used in your business or industry like a credit application or survey. | You want to extract fields and values including ones not covered by the scenario-specific prebuilt models **without having to train a custom model**.| [**Layout analysis model with the optional query string parameter `features=keyValuePairs` enabled **](../prebuilt/layout.md)|

## Pretrained scenario-specific models

| Document type | Data to extract | Your best solution |
| -----------------|--------------|-------------------|
|**US Unified Tax**|You want to extract key information across all tax forms of W2, 1040, 1090, 1098 from a single file without running any custom classification of your own.|[**US Unified tax model**](../prebuilt/tax-document.md)|
|**US Tax W-2 tax**|You want to extract key information such as salary, wages, and taxes withheld.|[**US tax W-2 model**](../prebuilt/tax-document.md)|
|**US Tax W-4 tax**|You want to extract key information such as claim adjustments, personal information.|[**US tax W-4 model**](../prebuilt/tax-document.md)|
|**US Tax 1095(A,C)**|You want to extract premium tax credit, advance credit payment details.|[**US tax 1095 model**](../prebuilt/tax-document.md)|
|**US Tax 1098**|You want to extract mortgage interest details such as principal, points, and tax.|[**US tax 1098 model**](../prebuilt/tax-document.md)|
|**US Tax 1098-E**|You want to extract student loan interest details such as lender and interest amount.|[**US tax 1098-E model**](../prebuilt/tax-document.md)|
|**US Tax 1098T**|You want to extract qualified tuition details such as scholarship adjustments, student status, and lender information.|[**US tax 1098-T model**](../prebuilt/tax-document.md)|
|**US Tax 1099(Variations)**|You want to extract information from `1099` forms and its variations (A, B, C, CAP, DIV, G, H, INT, K, LS, LTC, MISC, NEC, OID, PATR, Q, QA, R, S, SA, SB).|[**US tax 1099 model**](../prebuilt/tax-document.md)|
|**US Tax 1040(Variations)**|You want to extract information from `1040` forms and its variations (Schedule 1, Schedule 2, Schedule 3, Schedule 8812, Schedule A, Schedule B, Schedule C, Schedule D, Schedule E, Schedule `EIC`, Schedule F, Schedule H, Schedule J, Schedule R, Schedule `SE`, Schedule Senior).|[**US tax 1040 model**](../prebuilt/tax-document.md)|
|**Bank Statement**  |You want to extract key information from US bank statement | [**\Bank Statement**](../concept-bank-statement.md)|
|**Bank check** |You want to extract key information from check document. | [**Bank Check**](../concept-bank-check.md)|
|**Contract** (legal agreement between parties).|You want to extract contract agreement details such as parties, dates, and intervals.|[**Contract model**](../prebuilt/contract.md)|
|**Health insurance card** or health insurance ID.| You want to extract key information such as insurer, member ID, prescription coverage, and group number.|[**Health insurance card model**](../prebuilt/health-insurance-card.md)|
|**Credit/Debit card** |You want to extract key information bank cards such as card number and bank name. | [**Credit/Debit card model**](../concept-credit-card.md)|
|**Marriage Certificate** |You want to extract key information from marriage certificates. | [**Marriage certificate model**](../concept-marriage-certificate.md)|
|**Invoice** or billing statement|You want to extract key information such as customer name, billing address, and amount due.|[**Invoice model**](../prebuilt/invoice.md)|
|**Receipt**, voucher, or single-page hotel receipt. |You want to extract key information such as merchant name, transaction date, and transaction total.|[**Receipt model**](../prebuilt/receipt.md)|
|**Identity document (ID)** like a U.S. driver's license or international passport |You want to extract key information such as first name, surname, date of birth, address, and signature. | [**Identity document (ID) model**](../prebuilt/id-document.md)|
|**Pay stub** |You want to extract key information from the pay stub document. | [**Pay stub Model**](../concept-pay-stub.md)|
|**US Mortgage 1003** |You want to extract key information from the Uniform Residential loan application. | [**1003 form model**](../concept-mortgage-documents.md)|
|**US Mortgage 1004** |You want to extract key information from the Uniform Residential Appraisal Report (URAR). | [**1004 form model**](../concept-mortgage-documents.md)|
|**US Mortgage 1005** |You want to extract key information from the Verification of employment form | [**1005 form model**](../concept-mortgage-documents.md)|
|**US Mortgage 1008**  |You want to extract key information from the Uniform Underwriting and Transmittal summary. | [**1008 form model**](../concept-mortgage-documents.md)|
|**US Mortgage Closing Disclosure** |You want to extract key information from a mortgage closing disclosure form. | [**Mortgage closing disclosure form model**](../concept-mortgage-documents.md)|
|**Mixed-type document(s)** with structured, semi-structured, and/or unstructured elements | You want to extract key-value pairs, selection marks, tables, signature fields, and selected regions not extracted by prebuilt or general document models.| [**Custom model**](../train/custom-model.md)|

>[!Tip]
>
> * If you're still unsure which pretrained model to use, try the **layout model** with the optional query string parameter **`features=keyValuePairs`** enabled.
> * The layout model is powered by the Read OCR engine to detect pages, tables, styles, text, lines, words, locations, and languages.

## Custom extraction models

| Training set | Example documents | Your best solution |
| -----------------|--------------|-------------------|
|**Structured, consistent, documents with a static layout**. |Structured forms such as questionnaires or applications. | [**Custom template model**](./../train/custom-template.md)|
|**Structured and semi-structured**.|&#9679; Structured &rightarrow; surveys</br>&#9679; Semi-structured &rightarrow; invoices | [**Custom neural model**](../train/custom-neural.md)|
|**A collection of several models each trained on similar-type documents.** |&#9679; Supply purchase orders</br>&#9679; Equipment purchase orders</br>&#9679; Furniture purchase orders</br> **All composed into a single model**.| [**Composed custom model**](../train/composed-models.md)|

## Custom classification model

| Training set | Example documents | Your best solution |
| -----------------|--------------|-------------------|
|**At least two different types of documents**. |Forms, letters, or documents | [**Custom classification model**](./../train/custom-classifier.md)|

## Next steps

* [Learn how to process your own forms and documents](../studio-overview.md) with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio)
