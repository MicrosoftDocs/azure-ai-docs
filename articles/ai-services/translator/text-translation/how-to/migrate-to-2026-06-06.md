---
title: Migrate from Azure Translator Text API v3 to Azure Translator Text API (2026-06-06).
titleSuffix: Microsoft Foundry
description: This article provides the steps to help you migrate from Azure Translator Text API v3 to Azure Translator Text API 2026-06-06.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: concept-article
ms.date: 04/21/2026
ms.author: lajanuar
---

# Migrate from Azure Translator Text API v3 to Azure Translator Text API (2026-06-06)

Azure Translator Text API **2026-06-06** (GA), available through Microsoft Foundry, is the latest cloud-based, multilingual neural machine translation service. This release reflects the continued evolution of Azure Translator, with a focus on modern usage patterns, improved customization, and more flexible translation workflows.

As Translator matures, Microsoft is standardizing best practices to help customers adopt newer capabilities while maintaining quality, reliability, and cost control.

>[!IMPORTANT]
>
> * Translator REST API `2026-06-06` is the **generally available (GA)** version and **introduces breaking changes**.
> * Thoroughly test your applications against this version before migrating any production workloads from Translator Text API v3.0.
> * Review your application code and internal workflows to ensure they follow current best practices, and restrict production usage to API versions you have fully validated.

## What's new in API version 2026-06-06

The latest version of Azure Translator introduces the following enhancements:

* **Large language model (LLM) selection**: Choose the translation model that best fits your requirements for quality, cost, and performance without the overhead of prompt engineering or manual quality evaluation.

* **Adaptive custom translation**: Support for adaptive custom translation enables you to refine output using datasets or reference pairs, improving accuracy, terminology consistency, and contextual relevance.

* **Expanded translation parameters**: Translation requests now support additional parameters such as text type, language codes, and controls for tone and gender, allowing for more nuanced and purpose-specific translations.

## Method changes

The following section compares available methods in Translator Text API `2026-06-06` with those in Translator Text API v3.0.

>[!WARNING]
>
> * API version `2025-10-01-preview` is deprecated 90 days after GA.
> * To migrate from `2025-10-01-preview` to GA, set `api-version=2026-06-06`.

### Required parameters

| API version: 2026-06-06 | API version: v3.0 |
| --- | --- |
| **api-version**<br>&bullet; Value must be **2026-06-06** | **api-version**<br>&bullet; Value must be **3.0** |
| **text**<br>&bullet; Specifies the source text to translate. | **text**<br>&bullet; Specifies the source text to translate. |
| **targets**<br>&bullet; An array that defines one or more translation targets. | &bullet; *The `targets` array isn't used in the v3.0 schema.* |
| **language**<br>&bullet; Target language code specified within the `targets` array.<br>&bullet; Values must be from the [supported languages](../../language-support.md). | **to**<br>&bullet; Specifies the target language for translation.<br>&bullet; Values must be from the [supported languages](../../language-support.md#translation). |

For details about supported **`targets` array** values, see [Translate text](../preview/translate-api.md).

## API compatibility

The following table summarizes method-level changes between Translator Text API v3.0 and API version 2026-06-06:

| Azure Translator v3.0 | Azure Translator 2026-06-06 |
| --- | --- |
| [Translate text](../reference/v3/translate.md) | [Translate text](../preview/translate-api.md) |
| [Transliterate](../reference/v3/transliterate.md) | [Transliterate](../preview/transliterate-api.md) |
| [Languages](../reference/v3/languages.md) | [Languages](../preview/get-languages.md) |
| [BreakSentence](../reference/v3/break-sentence.md) | No longer supported.<br>Use a sentence delimiter or an NLP library compatible with your programming language. |
| [Detect](../reference/v3/detect.md) | No longer supported.<br>Use the [Language detection API](../../../language-service/language-detection/how-to/call-api.md). |
| [Dictionary Lookup](../reference/v3/dictionary-lookup.md) | No longer supported. |
| [Dictionary Examples](../reference/v3/dictionary-examples.md) | No longer supported. |

## Next Steps

> [!div class="nextstepaction"]
> [View 2026-06-06 Translate method](../2026-06-06/translate-api.md)
