---
title: Migrate to v4.0 - Azure AI Translator
titleSuffix: Azure AI services
description: This article provides the steps to help you migrate from Azure AI Translator v3 to  2025-05-01-preview Text translation API.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: conceptual
ms.date: 04/18/2025
ms.author: lajanuar
---

# Azure AI Translator 2025-05-01-preview migration

Azure AI Translator text translation 2025-05-01-preview (v4.0) is our latest cloud-based, multilingual neural machine translation service. As Azure AI Translator matures, we're focused on patterns and practices to best support and add value to our users.

>[!IMPORTANT]
> * Azure AI Translator REST API `2025-05-01-preview` is new version of the Azure AI Translator REST API **with breaking changes**.
> * It's essential to thoroughly test your code against the new release before migrating any production applications from Azure AI Translator v3.0.
> * Make sure to review your code and internal workflows for adherence to best practices and restrict your production code to versions that you fully test.


The latest version of Azure AI Translator includes the following enhancements and capabilities:

 * **Large language model (LLM) choice**. You can choose a large language model based for translation based on quality, cost, and other factors, while avoiding costs associated with prompt engineering and quality evaluations.

* **Adaptive custom translation**. New features enable adaptive custom translations using datasets or reference pairs to ensure more accurate and contextually relevant translations.

* **Expanded translation parameters**. The API supports a range of parameters, including text type, language codes, and options for tone and gender, providing more nuanced translation outputs.

## Method changes

The following list compares available Azure AI Translator `2025-05-01-preview` methods with available v3.0 method.

### Required parameters

|2025-05-01 method|v3 method|
|:---|---|
|**`api-version`**<br>&bullet; Value must be **`2025-05-01-preview`** |**`api-version`**<br>&bullet; Value must be **`3.0`**|
|**`text`**<br>&bullet; Specifies source text for translation. | **`text`**<br>&bullet; Specifies source text for translation|
|**`targets`**<br>&bullet; Array containing user-specified values for the translated text|&bullet; *The targets array isn't included with the Translator v3.0 schema.*|
|**`language`**<br>&bullet; The language code for the translated (target) text *specified in the `targets` array*. <br> &bullet; Values are [supported language](../../language-support.md) codes for the translation operation.|**`to`**<br>&bullet; Specifies the language of the output text.<br>&bullet; The target language must be one of the [supported languages](../../language-support.md#translation) included in the translation scope.|

For more information on **`targets array`** values, *see* [Translate text](../reference/v4/translate-api.md).

## API compatibility

The following table compares Translator `2025-05-01-preview` and Translator v3 API methods.

|Translator 2025-05-01-preview method|Translator v3 compatibility|
|---|---|
|[Translate text](../reference/v4/translate-api.md)|[Translate text](../reference/v3/translate.md)|
|[Transliterate](../reference/v4/transliterate-api.md)|[Transliterate](../reference/v3/transliterate.md)|
|[Languages](../reference/v4/get-languages.md)|[Languages](../reference/v3/languages.md)|
|Feature no longer supported|[Detect language](../reference/v3/detect.md)|
|Feature no longer supported|[BreakSentence](../reference/v3/break-sentence.md)|
|Feature no longer supported|[Dictionary Lookup](../reference/v3/dictionary-lookup.md)|
|Feature no longer supported|[Dictionary Examples](../reference/v3/dictionary-examples.md)|

## Next Steps

> [!div class="nextstepaction"]
> [View 2025-05-01-preview Translate method](../reference/v4/translate-api.md)
