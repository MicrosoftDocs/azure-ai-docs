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

We're continually improving and enhancing Azure AI Translator and its features. This page details known issues related to Azure AI Translator capabilities and provides steps to resolve them. Before submitting a support request, review the following list to see if your problem is already being addressed and to find a solution.

## Active Known Issues

For more information regarding service-level outages, *see* the [Azure status page](https://azure.status.microsoft/en-us/status). To set up outage notifications and alerts, *see* the [Azure Service Health Portal](/service-health/service-health-portal-update).

### Text Translation

This table lists the current known issues and workarounds for the Text Translator feature:

| **Issue ID** | **Category / Feature Area** | **Title**  |**Description** | **Workaround** | **Issues publish date** |
| ---| --- | ---| --- | --- |
| 1004 | Model| Preserving context and pronouns| Some translation models don't handle pronouns well; especially third-person pronouns. This issue is due to an inherent problem with sentence-level training and inference where context isn't preserved. We're actively working to shift all our models to document-level training and inference to preserve the context. New models should significantly improve pronoun resolution and overall translation coherence. | Currently, there's no direct workaround. Users should manually review and adjust pronoun usage as needed.  | February 5, 2025|
| 1006 | Content     | Translating sentences with mixed language text | The Text Translation API doesn't support translating sentences that contain mixed language input. As a result, translations can be incorrect or incomplete when a single sentence includes multiple languages.  | Specify the intended source language, remove the mixed-language sentence, or split the text into single-language segments. | February 5, 2025|



### Document Translation

This table list the active known issues for the Document Translator feature. This table includes existing challenges and new items related to complex or mixed content inputs.

| **Issue ID** | **Category / Feature Area** | **Title**  | **Description**| **Workaround**| **Issues publish date** |
| --- | --- | --- | --- | --- | --- |
| 3001 | Formatting  | Formatting of mathematical expressions     | In some cases, translated documents don't fully retain the formatting of mathematical expressions. Superscript and subscript numbers can be reformatted incorrectly, leading to discrepancies between expected and actual output.   | Currently, there's no direct workaround. Users should manually adjust the formatting of mathematical expressions as needed.  | February 5, 2025|
| 3007 | Content     | Translating documents with mixed source languages  | In some cases, document translation doesn't translate source documents with multiple languages leading to incorrect or incomplete results. For example, a sentence contains more than one language.| To ensure that the desired language is translated to the target language, specify the intended source language. Alternatively, remove the mixed-language sentence, or split the text into segments containing only one language. | February 5, 2025|
| 3008 | File types  | Translating complex documents      | When translating documents with thousands of intricate pages—which comprise images, embedded text within images, and manually typed text—it's possible for the batch translation request to encounter failures during extraction, translation, and reassembly.      | Split the large document into smaller sections (for example, divide a 1000-page file into approximately 10 files of 100 pages each) and submit them individually for the best results.| February 5, 2025|
| 3009 | Formatting  | Translating documents containing borderless tables | Borderless tables aren't always be processed accurately during translation. Borderless tables present a unique formatting challenge, requiring additional processing to maintain translation accuracy without affecting overall performance. | Recreate documents using bordered tables instead of borderless ones to improve the translation output quality.| February 5, 2025|


## Recently closed known issues

Resolved known issues are organized in this section in descending order by fixed date. Fixed issues are retained for at least 60 days.

## Related content

* [Azure Service Health Portal](/service-health/service-health-portal-update).
* [Azure Status overview](/service-health/azure-status-overview)
* [What's new in Azure AI Translator?](../whats-new.md)