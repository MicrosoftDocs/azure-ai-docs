---
title: "Text translation REST API preview reference guide"
titleSuffix: Foundry Tools
description: View a list of text translation preview REST APIs.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Text translation REST API (preview)

> [!IMPORTANT]
>
> * Azure AI text translation is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Text translation is a cloud-based feature of the Azure Translator in Foundry Tools service and is part of the Foundry Tool family of REST APIs. The Text translation API translates text between language pairs across all [supported languages and dialects](../../../language-support.md). If you already have a Translator or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Translator resources within the Microsoft Foundry portal for NMT deployment. 

By default, Azure Translator utilizes neural Machine Translation (NMT) technology. With the newest preview release, you now can optionally select either the standard NMT translation or one of two Large Language Model (LLM) deployment types: GPT-4o-mini or GPT-4o. However, using an LLM model requires you to have a Foundry Tools resource. For more information, *see*, [Configure Azure resources](../../how-to/create-translator-resource.md).

The available preview methods are listed in the following table:

| Request| Method| Description|
|---------|--------------|---------|
| [**languages**](get-languages.md) | **GET** | Returns the set of languages currently supported by the **translation**, and **transliteration** methods. This request doesn't require authentication headers and you don't need a Translator resource to view the supported language set.|
|[**translate**](translate-api.md) | **POST**| Translate specified source language text into the target language text.|
|[**transliterate**](transliterate-api.md) |  **POST** | Map source language script or alphabet to a target language script or alphabet.

## REST API code sample: translate

***Request***
```json
{
  "inputs": [
    {
      "text": "Ciao",
      "language": "it",
      "targets": [
        {
          "language": "en"
        }
      ]
    }
  ]
}

```

***Response***
```json
{
  "value": [
    {
      "translations": [
        {
          "language": "en",
          "sourceCharacters": 4,
          "text": "Hello"
        }
      ]
    }
  ]
}
```




## Next steps

> [!div class="nextstepaction"]
> [View 2025-10-01-preview migration guide](../how-to/migrate-to-preview.md)
