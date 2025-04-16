---
title: Migrate to v4.0 - Azure AI Translator
titleSuffix: Azure AI services
description: This article provides the steps to help you migrate from v3 to Azure AI Translator v4.0 text translation.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: conceptual
ms.date: 04/15/2025
ms.author: lajanuar
---

# Azure AI Translator v4.0 migration

Azure AI Translator text translation 2025-05-01-preview (v4.0) is our latest cloud-based, multilingual neural machine translation service. As Azure AI Translator matures we are focused on learning the patterns and practices to best support and add value to our users.

There are many benefits to using the latest Azure AI Translator version:

*  **Backward compatibility**. Azure AI Translator 2025-05-01-preview (v4.0) is designed to seamlessly work with Azure AI Translator v3.0, requiring minimal updates for existing customers. 

 * **Large language model (LLM) choice**. You can choose a large language model based for translation based on quality, cost, and other factors, while avoiding costs associated with prompt engineering and quality evaluations.

* **Adaptive custom translation**. New features enable adaptive custom translations using datasets or reference pairs to ensure more accurate and contextually relevant translations.

* **Expanded translation parameters**. The API supports a range of parameters, including text type, language codes, and options for tone and gender, providing more nuanced translation outputs.

 
## Method changes

The following list outlines the v4.0 method that aligns with the v3.0 method.

### Query string

|v4.0 method|v3.0 method|
|---|---|
|&bullet; **`api-version`**<br>&bullet; *Required parameter*<br>&bullet; Version of the API requested by the client. Value must be **`2025-05-01-preview`** | &bullet; **`api-version`**<br>&bullet; *Required parameter*<br>&bullet; Version of the API requested by the client. Value must be **`3.0`**|
|*See [targets array](#targets-array)*|&bullet; **`to`**<br>&bullet; *Required parameter*<br>&bullet; Specifies the language of the output text. The target language must be one of the [supported languages](../../language-support.md#translation) included in the translation scope.|
|&bullet; **`text`**<br>&bullet; *Required parameter*<br>&bullet; **Specifies source text for translation**. | &bullet; **`text`**<br>&bullet; *Required parameter*<br>&bullet; **Specifies source text for translation**.|

### Targets array

|v4.0 method|v3.0 method|
|---|---|
|Translator v4.0 **`targets array`** contains user-specified values for the translated text|Translator v3.0 doesn't use the target array.|
|&bullet; **`language`**<br>|The language code for the translated (`target`) text. Values are [supported language](../../language-support.md) codes for the translation operation.|

For more information on **`targets array`** values, *see* [Translate v4.0 reference ](../reference/v4/translate-api.md)