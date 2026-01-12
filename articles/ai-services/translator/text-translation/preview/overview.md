---
title: Azure Translator in Foundry Tools 2025-10-01-preview reference
titleSuffix: Foundry Tools
description: Reference documentation for Azure Translator in Foundry Tools 2025-10-01-preview operations and capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.custom: references_regions
ms.date: 01/18/2026
ms.author: lajanuar
---

# Azure Translator in Foundry Tools 2025-10-01-preview

Azure Translator in Foundry Tools `2025-10-01-preview` is our latest cloud-based, multilingual, neural machine translation service. The Text translation API enables robust and scalable translation capabilities suitable for diverse applications.

Translator is an optimal solution for managing extensive multilingual content. It easily integrates with your applications and workflows through a single REST API call and supports multiple programming languages. Translator supports over 100 languages and dialects, making it ideal for businesses, developers, and organizations seeking to seamlessly integrate multilingual communication.


>[!IMPORTANT]
> * Azure Translator REST API `2025-10-01-preview` is new version of the Azure Translator REST API **with breaking changes**.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * It's essential to thoroughly test your code against the new release before migrating any production applications from Azure Translator v3.0.
> * Make sure to review your code and internal workflows for adherence to best practices and restrict your production code to versions that you fully test.
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).


## What's new for 2025-10-01-preview?

* **Revised request and response JSON format**. The REST API structure has been revised to add specific key names for both the request and response arrays. The request array now uses "inputs" as its key name, while the response array uses "value" as its key name. For more information, *see* [REST API guide (preview)](rest-api-guide.md#rest-api-code-sample-translate).

* **`LLM` choice**. By default, Azure Translator uses neural Machine Translation (NMT) technology. With the newest preview release, you now can optionally select either the standard NMT translation or Large Language Model (LLM) models—GPT-4o-mini or GPT-4o. You can choose a large language model for translation based on factors such as quality, cost, and other considerations. However, **using an LLM model requires you to have a Microsoft Foundry resource**. For more information, *see* [Configure Azure resources](../../how-to/create-translator-resource.md)

* **Adaptive custom translation**. You can provide up to five reference translations or translation memory datasets to enable an `LLM` model to perform few-shot translations in a similar style and tailored to your needs.

* **Tone variant translations**. Use generative AI LLMs translate text across multiple tonal categories—formal, informal, and neutral—ensuring precise contextual adaptation.

*  **Gender-specific language translations**. Apply generative AI LLMs for the linguistic transformation of text according to specified gender parameters—male, female, and neutral—to ensure targeted stylistic and semantic alignment.

## Language support

The languages supported for LLM and Adaptive custom translations are listed in the Translation section of our [Language support page](../../language-support.md#translation).

## Authentication

The `2025-10-01-preview` API supports both the resource API key and Microsoft Entra ID authentication. For your information, *see* [Authorization and authentication](../../text-translation/reference/authentication.md)

## NMT Base URLs

Requests to Translator are, in most cases, handled by the datacenter that's closest to where the request originated. If there's a datacenter failure when using the global endpoint, the request may be routed outside of the geography.

To force the request to be handled within a specific geography, use the desired geographical endpoint. All requests are processed among the datacenters within the geography.

✔️ Feature: **Translator Text** </br>


| NMT model service endpoint | Request processing data center |
|------------------|--------------------------|
|**Global (recommended):**</br>**`api.cognitive.microsofttranslator.com`**|Closest available data center.|
|**Americas:**</br>**`api-nam.cognitive.microsofttranslator.com`**|East US 2 &bull; West US 2|
|**Asia Pacific:**</br>**`api-apc.cognitive.microsofttranslator.com`**|Japan East &bull; Southeast Asia|
|**Europe (except Switzerland):**</br>**`api-eur.cognitive.microsofttranslator.com`**|France Central &bull; West Europe|
|**Switzerland:**</br> For more information, *see* [Switzerland service endpoints](#switzerland-service-endpoints).|Switzerland North &bull; Switzerland West|

#### Switzerland service endpoints

Customers with a resource located in Switzerland North or Switzerland West can ensure that their Text API requests are served within Switzerland. To ensure that requests are handled in Switzerland, create the Translator resource in the `Resource region` `Switzerland North` or `Switzerland West`, then use the resource's custom endpoint in your API requests.

### LLM processing

When you deploy a large language model (LLM), the configuration options you choose—global, data zone, or regional—directly impact and determine the specific location in which your data is processed. Therefore, your selections during setup play a significant role in defining the geographical boundaries for how and where the model processes your information.

#### Service limits

| Operation | Maximum Number of Array Elements | Maximum Size of Array Element | Generative AI LLM: Maximum Number of Array Elements | Generative AI LLM: Maximum Size of Array Element |
| --- | --- | --- | --- | --- |
| Translate | 1,000 | 50,000 | 50 | 5,000 |

The amount of computing resources you provide influences translation latency when you use generative AI large language models. By adjusting the capacity allocated during model deployment, you can affect latency.

#### Pricing

* By default, translations using general NMT (Neural Machine Translation) models are billed according to the number of characters in the source text. For more information, *see* [Azure Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator/).

* Translations using generative AI LLMs are charged according to the number of input and output tokens processed. For more information, *see* [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).


## Next steps

> [!div class="nextstepaction"]
> [View 2025-10-01-preview migration guide](../how-to/migrate-to-preview.md)



