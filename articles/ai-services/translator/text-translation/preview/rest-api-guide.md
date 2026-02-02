---
title: "Text translation REST API preview reference guide"
titleSuffix: Azure AI services
description: View a list of text translation preview REST APIs.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/19/2025
ms.author: lajanuar
---

# Text translation REST API (preview)

Text translation is a cloud-based feature of the Azure AI Translator service and is part of the Azure AI service family of REST APIs. The Text translation API translates text between language pairs across all [supported languages and dialects](../../../language-support.md). If you already have an Azure AI Translator or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Translator resources within the Azure AI Foundry portal for NMT deployment. 

By default, Azure AI Translator utilizes neural Machine Translation (NMT) technology. With the newest preview release, you now can optionally select either the standard NMT translation or one of two Large Language Model (LLM) deployment types: GPT-4o-mini or GPT-4o. However, using an LLM model requires you to have an Azure AI Foundry resource. For more information, *see*, [Configure Azure AI resources](../../how-to/create-translator-resource.md).

The available preview methods are listed in the following table:

| Request| Method| Description|
|---------|--------------|---------|
| [**languages**](get-languages.md) | **GET** | Returns the set of languages currently supported by the **translation**, and **transliteration** methods. This request doesn't require authentication headers and you don't need a Translator resource to view the supported language set.|
|[**translate**](translate-api.md) | **POST**| Translate specified source language text into the target language text.|
|[**transliterate**](transliterate-api.md) |  **POST** | Map source language script or alphabet to a target language script or alphabet.

## Next steps

> [!div class="nextstepaction"]
> [View 2025-05-01-preview migration guide](../how-to/migrate-to-preview.md)
