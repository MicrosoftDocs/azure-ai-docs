---
title: Migrate from Translator v3 to the latest Azure Translator in Foundry Tools text translation version.
titleSuffix: Foundry Tools
description: This article provides the steps to help you migrate from Azure Translator v3 to 2025-05-01-preview text translation API.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
---

# Text translation 2025-10-01-preview migration

Azure Translator in Foundry Tools text translation 2025-10-01-preview is our latest cloud-based, multilingual neural machine translation service. As Translator matures, we're focused on patterns and practices to best support and add value to our users.

>[!IMPORTANT]
> * Translator REST API `2025-10-01-preview` is new version of the Translator REST API **with breaking changes**.
> * It's essential to thoroughly test your code against the new release before migrating any production applications from Translator v3.0.
> * Make sure to review your code and internal workflows for adherence to best practices and restrict your production code to versions that you fully test.


The latest version of Azure Translator includes the following enhancements and capabilities:

 * **Large language model (LLM) choice**. You can choose a large language model based for translation based on quality, cost, and other factors, while avoiding costs associated with prompt engineering and quality evaluations.

* **Adaptive custom translation**. New features enable adaptive custom translations using datasets or reference pairs to ensure more accurate and contextually relevant translations.

* **Expanded parameters for translation requests**. The API supports a range of parameters, including text type, language codes, and options for tone and gender, providing more nuanced translation outputs.

## Method changes

The following list compares available Translator `2025-10-01-preview` methods with available v3.0 method.

### Required parameters

|API version: 2025-10-01-preview|API version: v3|
|:---|---|
|**api-version**<br>&bullet; Value must be **2025-10-01-preview** |**api-version**<br>&bullet; Value must be **3.0**|
|**text**<br>&bullet; Specifies source text for translation. | **text**<br>&bullet; Specifies source text for translation|
|**targets**<br>&bullet; Array containing user-specified values for the translated text|&bullet; *The targets array isn't included with the Translator v3.0 schema.*|
|**language**<br>&bullet; The language code for the translated (target) text *specified in the targets array*. <br> &bullet; Values are [supported language](../../language-support.md) codes for the translation operation.|**to**<br>&bullet; Specifies the language of the output text.<br>&bullet; The target language must be one of the [supported languages](../../language-support.md#translation) included in the translation scope.|

For more information on **targets array** values, *see* [Translate text](../preview/translate-api.md).

## API compatibility

The following table provides a detailed comparison of the updates introduced in API version 2025-10-01-preview.

|API version: v3|API version: 2025-10-01-preview|
|---|---|
|[Translate text](../reference/v3/translate.md)|[Translate text](../preview/translate-api.md)|
|[Transliterate](../reference/v3/transliterate.md)|[Transliterate](../preview/transliterate-api.md)|
|[Languages](../reference/v3/languages.md)|[Languages](../preview/get-languages.md)|
|[BreakSentence](../reference/v3/break-sentence.md)|Feature no longer supported.<br>Use a sentence delimiter function or a Natural Language Processing (NLP) library that's compatible with your programming language.|
|[Detect](../reference/v3/detect.md)|Feature no longer supported.<br>Use the [Azure Language in Foundry Tools detection API](../../../language-service/language-detection/how-to/call-api.md).|
|[Dictionary Lookup](../reference/v3/dictionary-lookup.md)|Feature no longer supported.|
|[Dictionary Examples](../reference/v3/dictionary-examples.md)|Feature no longer supported.|


## Next Steps

> [!div class="nextstepaction"]
> [View 2025-10-01-preview Translate method](../preview/translate-api.md)
