---
title: What is Azure Text translation in Foundry Tools?
titleSuffix: Foundry Tools
description: Integrate the Azure Translator in Foundry Tools Text translation API into your applications, websites, tools, and other solutions for multi-language user experiences.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 02/06/2026
ms.author: lajanuar
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# What is Azure Text translation in Foundry Tools?

Azure Translator in [Foundry Tools](../../what-are-ai-services.md) is a cloud-based REST API feature of the Translator service. It uses neural machine translation technology to enable quick and accurate source-to-target text translation in real time across all [supported languages](../language-support.md). In this overview, you learn how the Text translation REST APIs enable you to build intelligent solutions for your applications and workflows.

Text translation documentation contains the following article types:

* [**Quickstarts**](quickstart/rest-api.md). Getting-started instructions to guide you through making requests to the service.
* [**How-to guides**](../how-to/create-translator-resource.md). Instructions for accessing and using the service in more specific or customized ways.
* [**Reference articles**](reference/v3/reference.md). REST API documentation and programming language-based content.

## Text translation features

Use the following tabs to compare the latest preview version and the latest GA version.

### [Latest preview version](#tab/preview)

The latest preview release (`2025-10-01-preview`) lets you optionally select either the standard neural machine translation (NMT) or a Large Language Model (LLM) deployment (GPT-4o-mini or GPT-4o). However, using an LLM model requires a Microsoft Foundry resource. For more information, see [configure Azure resources](../how-to/create-translator-resource.md).

For a quick overview of Microsoft Foundry, see [What is Microsoft Foundry?](../../../ai-foundry/what-is-foundry.md)

* [**Languages**](preview/get-languages.md). Returns a list of languages supported by the [**Translate**](preview/translate-api.md) and [**Transliterate**](preview/transliterate-api.md) APIs. This request doesn't require authentication. Copy and paste the following `GET` request into your preferred REST API tool or browser:

    ```bash
        https://api.cognitive.microsofttranslator.com/languages?api-version=2025-10-01-preview
    ```

* [**Translate**](preview/translate-api.md). Renders single source-language text to multiple target-language texts with a single `POST` request.

    For an end-to-end request example, see [REST API guide (preview)](preview/rest-api-guide.md).


* [**Transliterate**](preview/transliterate-api.md). Converts characters or letters of a source language to the corresponding characters or letters of a target language with a single `POST` request.

### [Latest GA version](#tab/ga)

The latest GA release uses API version `3.0`.

* [**Languages**](reference/v3/languages.md). Returns a list of languages supported by **Translate**, **Transliterate**, and **Dictionary Lookup** operations. This request doesn't require authentication. Copy and paste the following `GET` request into your preferred REST API tool or browser:

    ```bash
    https://api.cognitive.microsofttranslator.com/languages?api-version=3.0
    ```

* [**Translate**](reference/v3/translate.md#translate-to-multiple-languages). Renders single source-language text to multiple target-language texts with a single request.

* [**Transliterate**](reference/v3/transliterate.md). Converts characters or letters of a source language to the corresponding characters or letters of a target language.

* [**Detect**](reference/v3/detect.md). Returns the source code language code and a boolean variable denoting whether the detected language is supported for text translation and transliteration.

    > [!NOTE]
    > You can **Translate, Transliterate, and Detect** text with [a single REST API call](reference/v3/translate.md#translate-a-single-input-with-language-autodetection).

* [**Dictionary lookup**](reference/v3/dictionary-lookup.md). Returns equivalent words for the source term in the target language.
* [**Dictionary example**](reference/v3/dictionary-examples.md). Returns grammatical structure and context examples for the source term and target term pair.

---

## Text translation development options

Add Text translation to your projects and applications using the following resources:

|Development option|Description|
|---|---|
|**Foundry portal**|&bull; [**Foundry (classic) portal**](https://ai.azure.com/) is a cloud-based AI platform that supports **hub-based** projects and other resource types.<br><br>&bull; [**Foundry (new) portal**](https://ai.azure.com/) is a cloud-based AI platform that provides streamlined access to Foundry models, agents, and tools through **Foundry projects**.|
|**REST API**|Integrate translation into your applications by using the [REST API (GA) version](reference/rest-api-guide.md) or [REST API (preview) version](preview/rest-api-guide.md).|
|**Client libraries (SDKs)**|Integrate translation capabilities into your applications by using the available [client libraries (SDKs)](quickstart/client-library-sdk.md) in various programming languages.|
|**Docker container**|&bull; To use the Translator container, complete and submit the [**Gated Services application**](https://aka.ms/csgate-translator) online request form for approval to access the container.<br>&bull; The [**Translator container image**](https://mcr.microsoft.com/product/azure-cognitive-services/translator/text-translation/about) supports limited features compared to cloud offerings.<br>For more information, see [Container: Translate Text](../containers/translate-text-parameters.md).|

## Authentication

Every text translation request requires authentication headers. The following methods are supported:

| Method | Description |
|---|---|
| **Resource key** | Pass the `Ocp-Apim-Subscription-Key` header with the key from your Translator resource. |
| **Bearer token** | Exchange your resource key for a time-limited token from the token service and pass it in the `Authorization` header. |
| **Microsoft Entra ID** | Use a managed identity or service principal to obtain an access token without managing keys. |

For details and examples, including required headers for global, regional, and custom endpoints, see [Authentication and authorization](reference/authentication.md).

## Service limits and pricing

Text translation enforces service limits and quotas, such as per-request character limits.

* For request limits and quotas, see [Service limits - Translator](../service-limits.md#text-translation).
* For pricing, see [Azure Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator-text-api/).

## Troubleshooting

If requests fail, start with the HTTP status code and the service-specific error code.

| Symptom | Likely cause | Resolution |
|---|---|---|
| `401 Unauthorized` | Invalid or missing subscription key. | Verify the `Ocp-Apim-Subscription-Key` value matches your Translator resource key. |
| `403 Forbidden` | Key valid but the resource doesn't have access to the requested operation. | Confirm the pricing tier supports the feature and that the resource region matches the endpoint. |
| `429 Too Many Requests` | Request rate or character quota exceeded. | Reduce request frequency or review the quotas in [Service limits - Translator](../service-limits.md#text-translation). |
| `400 Bad Request` | Malformed request body or unsupported language code. | Validate the JSON payload and check [supported languages](../language-support.md). |

* For the full list of status codes and error messages, see [Response codes and messages](reference/status-response-codes.md).

## Data residency

Text translation data residency depends on the Azure region where you create your Translator resource:

### Text translation data residency

✔️ Feature: **Translator Text** </br>

|Service endpoint|Request processing data center|
|------------------|--------------------------|
|**Global (recommended):**</br>**`api.cognitive.microsofttranslator.com`**|Closest available data center.|
|**Americas:**</br>**`api-nam.cognitive.microsofttranslator.com`**|East US 2 &bull; West US 2|
|**Asia Pacific:**</br>**`api-apc.cognitive.microsofttranslator.com`**|Japan East &bull; Southeast Asia|
|**Europe (except Switzerland):**</br>**`api-eur.cognitive.microsofttranslator.com`**|France Central &bull; West Europe|
|**Switzerland:**</br> For more information, see [Switzerland service endpoints](#switzerland-service-endpoints).|Switzerland North &bull; Switzerland West|

#### Switzerland service endpoints

Customers with a resource located in Switzerland North or Switzerland West can ensure that their Text API requests are served within Switzerland. To ensure that requests are handled in Switzerland, create the Translator resource in the `Resource region` `Switzerland North` or `Switzerland West`, then use the resource's custom endpoint in your API requests.

For example, if you create a Translator resource in the Azure portal with `Resource region` as `Switzerland North` and your resource name is `my-swiss-n`, then your custom endpoint is `https://my-swiss-n.cognitiveservices.azure.com`. A sample request to translate is:

```curl
# Pass secret key and region using headers to a custom endpoint
curl -X POST "https://my-swiss-n.cognitiveservices.azure.com/translator/text/v3.0/translate?to=fr" \
-H "Ocp-Apim-Subscription-Key: ${TRANSLATOR_KEY}" \
-H "Ocp-Apim-Subscription-Region: switzerlandnorth" \
-H "Content-Type: application/json" \
-d "[{\"Text\":\"Hello\"}]" -v
```

Custom Translator isn't currently available in Switzerland.

## Get started with Text translation

Follow these steps to start using Text translation:

1. [**Create a Translator resource**](../how-to/create-translator-resource.md) in the Azure portal.

1. [**Get your access keys and API endpoint**](../how-to/create-translator-resource.md#authentication-keys-and-endpoint-url). You need an endpoint URL and a read-only key for authentication.

1. Explore the [**Text translation quickstart**](quickstart/rest-api.md) for use cases and code samples in the following programming languages:
   * [**C#/.NET**](quickstart/rest-api.md?tabs=csharp)
   * [**Go**](quickstart/rest-api.md?tabs=go)
   * [**Java**](quickstart/rest-api.md?tabs=java)
   * [**JavaScript/Node.js**](quickstart/rest-api.md?tabs=nodejs)
   * [**Python**](quickstart/rest-api.md?tabs=python)

## Related content

* [Text translation REST API reference](reference/v3/reference.md)
* [Text translation quickstart](quickstart/rest-api.md)