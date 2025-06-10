---
title: What is Azure Text translation?
titlesuffix: Azure AI services
description: Integrate the Text translation API into your applications, websites, tools, and other solutions for multi-language user experiences.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 06/19/2025
ms.author: lajanuar
---

# What is Azure Text translation?

 Azure Text translation is a cloud-based REST API feature of the Translator service that uses neural machine translation technology to enable quick and accurate source-to-target text translation in real time across all [supported languages](../language-support.md). In this overview, you learn how the Text translation REST APIs enable you to build intelligent solutions for your applications and workflows.

Text translation documentation contains the following article types:

* [**Quickstarts**](quickstart/rest-api.md). Getting-started instructions to guide you through making requests to the service.
* [**How-to guides**](../how-to/create-translator-resource.md). Instructions for accessing and using the service in more specific or customized ways.
* [**Reference articles**](reference/v3/reference.md). REST API documentation and programming language-based content.

## Text translation features

 Text translation supports the following methods:

* [**Languages**](reference/v3/languages.md). Returns a list of languages supported by **Translate**, **Transliterate**, and **Dictionary Lookup** operations. This request doesn't require authentication; just copy and paste the following GET request into your favorite REST API tool or browser:

    ```http
    https://api.cognitive.microsofttranslator.com/languages?api-version=3.0
    ```

* [**Translate**](reference/v3/translate.md#translate-to-multiple-languages). Renders single source-language text to multiple target-language texts with a single request.

* [**Transliterate**](reference/v3/transliterate.md). Converts characters or letters of a source language to the corresponding characters or letters of a target language.

* [**Detect**](reference/v3/detect.md). Returns the source code language code and a boolean variable denoting whether the detected language is supported for text translation and transliteration.

    > [!NOTE]
    > You can **Translate, Transliterate, and Detect** text with [a single REST API call](reference/v3/translate.md#translate-a-single-input-with-language-autodetection) .

* [**Dictionary lookup**](reference/v3/dictionary-lookup.md). Returns equivalent words for the source term in the target language.
* [**Dictionary example**](reference/v3/dictionary-examples.md) Returns grammatical structure and context examples for the source term and target term pair.

## Text translation deployment options

Add Text translation to your projects and applications using the following resources:

* Access the cloud-based Translator service via the [**REST API**](reference/rest-api-guide.md), available in Azure.

* Use the REST API [translate request](../containers/translator-container-supported-parameters.md) with the [**Text translation Docker container**](../containers/translator-how-to-install-container.md).

    > [!IMPORTANT]
    >
    > * To use the Translator container, you must complete and submit the [**Azure AI services application for Gated Services**](https://aka.ms/csgate-translator) online request form for approval for access to the container.
    >
    > * The [**Translator container image**](https://mcr.microsoft.com/product/azure-cognitive-services/translator/text-translation/about) supports limited features compared to cloud offerings.
    >

## Data residency

Text translation data residency depends on the Azure region where your Translator resource was created:

### Text translation data residency

✔️ Feature: **Translator Text** </br>

| Service endpoint | Request processing data center |
|------------------|--------------------------|
|**Global (recommended):**</br>**`api.cognitive.microsofttranslator.com`**|Closest available data center.|
|**Americas:**</br>**`api-nam.cognitive.microsofttranslator.com`**|East US 2 &bull; West US 2|
|**Asia Pacific:**</br>**`api-apc.cognitive.microsofttranslator.com`**|Japan East &bull; Southeast Asia|
|**Europe (except Switzerland):**</br>**`api-eur.cognitive.microsofttranslator.com`**|France Central &bull; West Europe|
|**Switzerland:**</br> For more information, *see* [Switzerland service endpoints](#switzerland-service-endpoints).|Switzerland North &bull; Switzerland West|

#### Switzerland service endpoints

Customers with a resource located in Switzerland North or Switzerland West can ensure that their Text API requests are served within Switzerland. To ensure that requests are handled in Switzerland, create the Translator resource in the `Resource region` `Switzerland North` or `Switzerland West`, then use the resource's custom endpoint in your API requests.

For example: If you create a Translator resource in Azure portal with `Resource region` as `Switzerland North` and your resource name is `my-swiss-n`, then your custom endpoint is `https&#8203;://my-swiss-n.cognitiveservices.azure.com`. And a sample request to translate is:

```curl
// Pass secret key and region using headers to a custom endpoint
curl -X POST "https://my-swiss-n.cognitiveservices.azure.com/translator/text/v3.0/translate?to=fr" \
-H "Ocp-Apim-Subscription-Key: xxx" \
-H "Ocp-Apim-Subscription-Region: switzerlandnorth" \
-H "Content-Type: application/json" \
-d "[{'Text':'Hello'}]" -v
```

Custom Translator isn't currently available in Switzerland.

## Get started with Text translation

Ready to begin?

* [**Create a Translator resource**](../how-to/create-translator-resource.md "Go to the Azure portal.") in the Azure portal.

* [**Get your access keys and API endpoint**](../how-to/create-translator-resource.md#authentication-keys-and-endpoint-url). An endpoint URL and read-only key are required for authentication.

* Explore our [**Quickstart**](quickstart/rest-api.md) "Learn to use Translator via REST and a preferred programming language.") and view use cases and code samples for the following programming languages: 
  * [**C#/.NET**](quickstart/rest-api.md?tabs=csharp)
  * [**Go**](quickstart/rest-api.md?tabs=go)
  * [**Java**](quickstart/rest-api.md?tabs=java)
  * [**JavaScript/Node.js**](quickstart/rest-api.md?tabs=nodejs)
  * [**Python**](quickstart/rest-api.md?tabs=python)

## Next steps

Dive deeper into the Text translation REST API:

> [!div class="nextstepaction"]
> [See the REST API reference](reference/v3/reference.md)
