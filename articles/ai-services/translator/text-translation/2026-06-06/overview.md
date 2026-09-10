---
title: Azure Translator in Foundry Tools latest GA release reference
titleSuffix: Foundry Tools
description: Reference documentation for Azure Translator in Foundry Tools latest GA release operations and capabilities.
author: laujan
manager: mcleans
ms.service: azure-translator-foundry-tools
ms.topic: reference
ms.custom: references_regions
ms.date: 06/02/2026
ms.author: lajanuar
ai-usage: ai-assisted
---

# What is Azure Translator text translation?

Azure Translator in Foundry Tools `2026-06-06` is our latest cloud-based, multilingual, neural machine translation service. The Text translation API enables robust and scalable translation capabilities suitable for diverse applications.

Translator is an optimal solution for managing extensive multilingual content. It easily integrates with your applications and workflows through a single REST API call and supports multiple programming languages. Translator supports over 100 languages and dialects, making it ideal for businesses, developers, and organizations seeking to seamlessly integrate multilingual communication.

>[!IMPORTANT]
>
> * Azure Translator REST API `2026-06-06` is the latest version of the Azure Translator REST API **with breaking changes**.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * It's essential to thoroughly test your code against the new release before migrating any production applications from Azure Translator v3.0.
> * Make sure to review your code and internal workflows for adherence to best practices and restrict your production code to versions that you fully test.
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

## What's new for `2026-06-06` (GA) release?

* **Revised request and response JSON format**. The REST API structure is revised to add specific key names for both the request and response arrays. The request array now uses "inputs" as its key name, while the response array uses "value" as its key name. For more information, *see* [REST API guide](rest-api-guide.md#rest-api-code-sample-translate).

* **`LLM` choice**. By default, Azure Translator uses neural Machine Translation (NMT) technology. With the newest release, you now can optionally select either the standard NMT translation or Large Language Model (LLM), for example, GPT-5.1. You can choose a large language model for translation based on factors such as quality, cost, and other considerations. However, **using an LLM model requires you to have a Microsoft Foundry resource**. For more information, *see* [Configure Azure resources](../../how-to/create-translator-resource.md).

* **Adaptive custom translation**. You can provide up to five reference translations or adaptive dataset index ID to enable an `LLM` model to perform few-shot translations in a similar style and tailored to your needs. For more information, *see* [Adaptive custom translation](../../custom-translator/azure-ai-foundry/concepts/adaptive-custom-translation.md).

* **Tone variant translations**. Use generative AI LLMs translate text across multiple tonal categories—formal, informal, and neutral—ensuring precise contextual adaptation.

* **Gender-specific language translations**. Apply generative AI LLMs for the linguistic transformation of text according to specified gender parameters—male, female, and neutral—to ensure targeted stylistic and semantic alignment.

## Language support

The languages supported for LLM and Adaptive custom translations are listed in the Translation section of our [Language support page](../../language-support.md#translation).

## Authentication

The `2026-06-06` API supports both the resource API key and Microsoft Entra ID authentication. For your information, *see* [Authorization and authentication](../../text-translation/reference/authentication.md).

## Region support

NMT endpoint selection and Foundry LLM deployment types use different processing boundaries. For endpoint URLs, processing locations, and deployment differences, see [Region support for Azure Translator](../../region-support.md).

## Service limits

| Operation | Maximum Number of Array Elements | Maximum Size of Array Element | Generative AI LLM: Maximum Number of Array Elements | Generative AI LLM: Maximum Size of Array Element |
| --- | --- | --- | --- | --- |
| Translate | 1,000 | 50,000 | 50 | 5,000 |

The amount of computing resources you provide influences translation latency when you use generative AI large language models. By adjusting the capacity allocated during model deployment, you can affect latency.

#### Pricing

* By default, translations using general NMT (Neural Machine Translation) models are billed according to the number of characters in the source text. For more information, *see* [Azure Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator/).

* Translations using generative AI LLMs are charged according to the number of input and output tokens processed. For more information, *see* [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).


## Next steps

> [!div class="nextstepaction"]
> [View 2026-06-06 migration guide](../how-to/migrate-to-2026-06-06.md)



