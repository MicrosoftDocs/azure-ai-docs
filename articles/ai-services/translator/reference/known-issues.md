---
title: Azure Translator in Foundry Tools known issues
titlesuffix: Foundry Tools
description: Known and common issues with Azure Translator in Foundry Tools.
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Azure Translator in Foundry Tools known issues

Azure Translator in Foundry Tools is updated regularly and we're continually improving and enhancing its features and capabilities. This page details known issues related to Azure Translator and provides steps to resolve them. Before submitting a support request, review the following list to see if your problem is already being addressed and to find a possible solution.

## Active known issues

* For more information regarding service-level outages, *see* the [Azure status page](https://azure.status.microsoft/en-us/status). 
* To set up outage notifications and alerts, *see* the [Azure Service Health Portal](/azure/service-health/service-health-portal-update).

### Text translation

This table lists the current known issues and workarounds for the `Text translation` feature:

| **Issue ID** | **Category / Feature Area** | **Title**  |**Description** | **Workaround** | **Issues publish date** |
| ---| --- | ---| --- | --- |
| `1006` | Content| Translating sentences with mixed language text | The Text translation API doesn't support translating sentences that contain mixed language input. As a result, translations can be incorrect or incomplete when a single sentence includes multiple languages.  | Specify the intended source language, remove the mixed-language sentence, or split the text into single-language segments. | February 5, 2025|
| `1004` | Model| Preserving context and pronouns| Some translation models don't handle pronouns well; especially third-person pronouns. This issue is due to an inherent problem with sentence-level training and inference where context isn't preserved. We're actively working to shift all our models to document-level training and inference to preserve the context.| Currently, there's no direct workaround. Users should manually review and adjust pronoun usage as needed.  | February 5, 2025|



### Document translation

This table lists the active known issues for the `Document translation` feature. This table includes existing challenges and new items related to complex or mixed content inputs.

| **Issue ID** | **Category / Feature Area** | **Title**  | **Description**| **Workaround**| **Issues publish date** |
| --- | --- | --- | --- | --- | --- |
|`3010`|Content|Translating documents containing visible watermarks or seals|Documents with visible watermarks or seals can significantly hinder the translation process, as the watermarks may overlap with the text, making it difficult for the models to accurately recognize and process the content. This issue can result in the document remaining untranslated or only partially translated.|For optimal translation results, use clean, watermark-free documents. Files without visible watermarks or seals translate accurately and as expected.|May 21, 2025|
| `3009` |Formatting | Translating documents containing borderless charts and tables|Complex tables and charts can present significant challenges during translation, especially when they're large and intricate. Charts and tables with mixed horizontal and vertical text, varying cell sizes, or grid structures that are borderless, are difficult to format accurately. These types of tables may require added processing to ensure precision without compromising overall performance. | To improve the quality of translation output, consider recreating documents using bordered tables and charts rather than borderless ones. |April 1, 2025  |
| `3008` | File types  | Translating complex documents | Translating documents with thousands of intricate pages can be challenging. These documents often include images, embedded text within images, and manually typed text. As a result, the batch translation request can encounter failures during the extraction, translation, and reassembly processes.| Split the large document into smaller sections (for example, divide a 1000-page file into approximately 10 files of 100 pages each) and submit them individually for the best results.| February 5, 2025|
| `3007` | Content| Translating documents with mixed source languages  | In some cases, document translation doesn't translate source documents with multiple languages leading to incorrect or incomplete results. For example, a sentence that contains more than one language.| To ensure that the desired language is translated to the target language, specify the intended source language. Alternatively, remove the mixed-language sentence, or split the text into segments containing only one language. | February 5, 2025|
| `3001` | Formatting  | Formatting of mathematical expressions| In some cases, translated documents don't fully retain the formatting of mathematical expressions. Superscript and subscript numbers can be reformatted incorrectly, leading to discrepancies between expected and actual output.   | Currently, there's no direct workaround. Users should manually adjust the formatting of mathematical expressions as needed.  | February 5, 2025|

## Related content

* [Azure Service Health Portal](/azure/service-health/service-health-portal-update)
* [Azure Status overview](/azure/service-health/azure-status-overview)
* [What's new in Azure Translator?](../whats-new.md)
