---
title: "Text translation REST API reference guide"
titleSuffix: Foundry Tools
description: View a list of with links to the Text translation REST APIs.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Text translation REST API

Text translation is a cloud-based feature of the Azure Translator and is part of the Foundry Tool family of REST APIs. The Text translation API translates text between language pairs across all [supported languages and dialects](../../language-support.md). The available methods are listed in the following table:

| Request| Method| Description|
|---------|--------------|---------|
| [**languages**](../reference/v3/languages.md) | **GET** | Returns the set of languages currently supported by the **translation**, **transliteration**, and **dictionary** methods. This request doesn't require authentication headers and you don't need a Translator resource to view the supported language set.|
|[**translate**](../reference/v3/translate.md) | **POST**| Translate specified source language text into the target language text.|
|[**transliterate**](../reference/v3/transliterate.md) |  **POST** | Map source language script or alphabet to a target language script or alphabet.
|[**detect**](../reference/v3/detect.md) | **POST** | Identify the source language. |
|[**breakSentence**](../reference/v3/break-sentence.md) | **POST** | Returns an array of integers representing the length of sentences in a source text. |
| [**dictionary/lookup**](../reference/v3/dictionary-lookup.md) | **POST** | Returns alternatives for single word translations. |
| [**dictionary/examples**](../reference/v3/dictionary-examples.md) | **POST** | Returns how a term is used in context. |

> [!div class="nextstepaction"]
> [Create a Translator resource in the Azure portal.](../../create-translator-resource.md)

> [!div class="nextstepaction"]
> [Quickstart: REST API and your programming language](../quickstart/rest-api.md)
