---
title: What are common issues with Azure AI Translator?
titlesuffix: Azure AI services
description: Known issues with Azure AI Translator.
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 02/20/2025
ms.author: lajanuar
---

# Azure AI Translator Known Issues

This page lists known issues for Azure AI Translator features. We're continually improving the Microsoft Azure AI Translator, but if you are experiencing an issue, before submitting a support request, review the following list to see if the issue you're experiencing is being addressed and try one of the workaround steps to get unblocked.

For notifications regarding service-level outages or degradations, check the [Azure Service Health Portal - Azure Service Health | Microsoft Learn](/azure/service-health/service-health-portal-update).

## Active Known Issues

### Text Translation

This table lists the current known issues and workarounds for the Text Translator feature:

| **Issue ID**            | **Category / Feature Area** | **Title**                                      | **Description**                                                                                                                                                                                                                                                                                                                                                                                               | **Workaround**                                                                                                             | **Issues publish date** |
| ----------------------- | --------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| 1004                    | Model                       | Preserving context and pronouns                | Some translation models do not handle pronouns well; especially third-person pronouns. This is an inherent problem with sentence-level training and inference where context is not preserved. We are actively working to shift all our models to document-level training and inference to preserve the context. New models should significantly improve pronoun resolution and overall translation coherence. | Currently, there is no direct workaround. Users should manually review and adjust pronoun usage as needed.                 | February 5, 2025        |
| 1006                    | Content                     | Translating sentences with mixed language text | The Text Translation API does not support translating sentences that contain mixed language input. As a result, translations may be incorrect or incomplete when a single sentence includes multiple languages.                                                                                                                                                                                               | Specify the intended source language, remove the mixed-language sentence, or split the text into single-language segments. | February 5, 2025        |

### Document Translation

This table list the active known issues for the Document Translator feature. This table includes existing challenges as well as new items related to complex or mixed content inputs.

| **Issue ID** | **Category / Feature Area** | **Title**                                          | **Description**                                                                                                                                                                                                                               | **Workaround**                                                                                                                                                                                                                                        | **Issues publish date** |
| ------------ | --------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| 3001         | Formatting                  | Formatting of mathematical expressions             | In some cases, translated documents may not fully retain the formatting of mathematical expressions. Superscript and subscript numbers can be reformatted incorrectly, leading to discrepancies between expected and actual output.           | Currently, there is no direct workaround. Users should manually adjust the formatting of mathematical expressions as needed.                                                                                                                          | February 5, 2025        |
| 3007         | Content                     | Translating documents with mixed source languages  | Document translation may not translate source documents with multiple languages in some cases. This may lead to incorrect or incomplete results when, for example, a sentence contains more than one language.                                | To work around this and ensure that the desired language is translated to the target language, specify the intended source language. Alternatively, remove the mixed-language sentence, or split the text into segments containing only one language. | February 5, 2025        |
| 3008         | File types                  | Translating complex documents                      | When translating documents with thousands of complex pages—including images, embedded text within images, and manually typed text—the batch translation request may fail during extraction, translation, and reassembly.                      | Split the large document into smaller sections (for example, divide a 1000-page file into approximately 10 files of 100 pages each) and submit them individually for the best results.                                                                | February 5, 2025        |
| 3009         | Formatting                  | Translating documents containing borderless tables | Borderless tables may not always be processed accurately during translation. Borderless tables present a unique formatting challenge, requiring additional processing to maintain translation accuracy without affecting overall performance. | Recreate documents using bordered tables instead of borderless ones to improve the translation output quality.                                                                                                                                        | February 5, 2025        |


## Recently closed known issues

Resolved known issues will be organized in this section in descending order by fixed date. Fixed issues are retained for at least 60 days.

## Related content

* [Azure Service Health Portal - Azure Service Health | Microsoft Learn](/azure/service-health/service-health-portal-update).
* [What's new in Azure AI Translator? - Azure AI services | Microsoft Learn](/azure/ai-services/translator/whats-new?tabs=csharp)