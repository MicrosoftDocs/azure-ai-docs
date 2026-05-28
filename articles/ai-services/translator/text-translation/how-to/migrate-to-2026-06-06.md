---
title: Migrate to Translator Text API 2026-06-06
titleSuffix: Microsoft Foundry
description: Learn how to migrate your applications from Translator Text API v3.0 to the latest generally available release, API version 2026-06-06.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: concept-article
ms.date: 04/21/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# Migrate to Translator Text API 2026-06-06

Azure Translator Text API **2026-06-06** is the latest generally available (GA) release, available through Microsoft Foundry. If you're currently using Translator Text API v3.0, this guide walks you through what changed and how to update your integration.

The new version introduces expanded model options, new translation controls, and a revised request and response schema. It is **not backward compatible** with v3.0—you need to update your API version, payload structure, and any code that depends on v3.0-specific methods.

>[!IMPORTANT]
>
> * API version `2026-06-06` **is not a drop-in replacement** for v3.0. Changes to request structure, response schema, and supported methods are required.
> * Test your application thoroughly in a nonproduction environment before migrating any production workloads.
> * Validate your code and internal workflows, and restrict production deployments to API versions you fully test.

## What's new in API version 2026-06-06

There are key capabilities added in the `2026-06-06` API. Review each one to understand whether it applies to your integration and whether it requires code changes or opens up new scenarios for your application.

* **Large language model (LLM) selection**. You can now choose between standard Neural Machine Translation (NMT) and a supported Large Language Model (LLM), such as GPT-5.1, for each translation request. This allowance lets you balance quality, cost, and performance without managing prompt engineering or manual quality pipelines. LLM-based translation requires a Microsoft Foundry resource.

* **Adaptive custom translation**. You can supply up to five reference translation pairs or an adaptive dataset index ID to guide LLM output toward your preferred style and terminology. This allowance is useful for domain-specific content or applications with established glossaries.

* **Tone and gender controls**. Translation requests now accept tone (formal, informal, neutral) and gender (male, female, neutral) parameters when using LLM-based translation. These parameters are optional but allow you to produce more targeted output for audience-specific scenarios.

## Method changes

The `2026-06-06` API changes several required parameters and removes methods that v3.0 supported. Review the following tables to identify what you need to update in your code.

>[!WARNING]
>
> * API version `2025-10-01-preview` is deprecated 90 days after GA.
> * To migrate from `2025-10-01-preview` to GA, set `api-version=2026-06-06`.

### Required parameters

The most important structural change is the replacement of the v3.0 `to` parameter with a `targets` array. Update all translation requests to use the new schema.

| API version: 2026-06-06 | API version: v3.0 |
| --- | --- |
| **api-version**<br>&bullet; Value must be **2026-06-06** | **api-version**<br>&bullet; Value must be **3.0** |
| **text**<br>&bullet; Specifies the source text to translate. | **text**<br>&bullet; Specifies the source text to translate. |
| **targets**<br>&bullet; An array that defines one or more translation targets. | &bullet; *The `targets` array isn't used in the v3.0 schema.* |
| **language**<br>&bullet; Target language code specified within the `targets` array.<br>&bullet; Values must be from the [supported languages](../../language-support.md). | **to**<br>&bullet; Specifies the target language for translation.<br>&bullet; Values must be from the [supported languages](../../language-support.md#translation). |

For details about supported **`targets` array** values, see [Translate text](../2026-06-06/translate-api.md).

## API compatibility

Several v3.0 methods are no longer available in `2026-06-06`. If your application uses any of the removed methods, plan a replacement before migrating.

| Azure Translator v3.0 | Azure Translator 2026-06-06 |
| --- | --- |
| [Translate text](../reference/v3/translate.md) | [Translate text](../2026-06-06/translate-api.md) |
| [Transliterate](../reference/v3/transliterate.md) | [Transliterate](../2026-06-06/transliterate-api.md) |
| [Languages](../reference/v3/languages.md) | [Languages](../2026-06-06/get-languages.md) |
| [BreakSentence](../reference/v3/break-sentence.md) | No longer supported. Replace with a sentence delimiter function or a natural language processing (NLP) library compatible with your programming language. |
| [Detect](../reference/v3/detect.md) | No longer supported. Replace with the [Azure AI Language detection API](../../../language-service/language-detection/how-to/call-api.md). |
| [Dictionary Lookup](../reference/v3/dictionary-lookup.md) | No longer supported. Consider using [adaptive custom translation](../../custom-translator/azure-ai-foundry/concepts/adaptive-custom-translation.md) for domain-specific term handling. |
| [Dictionary Examples](../reference/v3/dictionary-examples.md) | No longer supported. |

## Next steps

> [!div class="nextstepaction"]
> [Translate text (2026-06-06)](../2026-06-06/translate-api.md)

* [Text translation overview](../overview.md)
* [REST API guide (2026-06-06)](../2026-06-06/rest-api-guide.md)
* [Adaptive custom translation](../../custom-translator/azure-ai-foundry/concepts/adaptive-custom-translation.md)
* [Supported languages](../../language-support.md)
