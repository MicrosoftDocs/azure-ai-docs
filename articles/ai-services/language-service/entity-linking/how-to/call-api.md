---
title: How to call the entity linking API
titleSuffix: Foundry Tools
description: Learn how to identify and link entities found in text with the entity linking API.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-entity-linking
---
# How to use entity linking

> [!IMPORTANT]
> Entity Linking is retiring from Azure Language in Foundry Tools effective **September 1, 2028**. After this date, the Entity Linking feature is no longer supported.   During the support window, we recommend that users migrate existing workloads and direct all new projects to Language [**Named Entity Recognition**](../../named-entity-recognition/overview.md) or consider other alternative solutions.


The entity linking feature enables the detection and clarification of the specific identity of entities mentioned within text. For instance, it can determine whether the term "Mars" refers to the planet or to the Roman god of war. This capability helps eliminate ambiguity by associating each entity with the correct context. It returns the entities in the text with links to [Wikipedia](https://www.wikipedia.org/) as a knowledge base.


## Development options

[!INCLUDE [development-options](../includes/development-options.md)]

## Determine how to process the data (optional)

### Specify the entity linking model

By default, entity linking uses the latest available AI model on your text. You can also configure your API requests to use a specific [model version](../../concepts/model-lifecycle.md).

### Input languages

When you submit documents to for entity linking processing, you can specify which of [the supported languages](../language-support.md) they're written in. If you don't specify a language, entity linking defaults to English. Due to [multilingual and emoji support](../../concepts/multilingual-emoji-support.md), the response may contain text offsets. 

## Submitting data

Entity linking produces a higher-quality result when you give it smaller amounts of text to work on. This characteristic is opposite from some features, like key phrase extraction that performs better on larger blocks of text. To get the best results from both operations, consider restructuring the inputs accordingly.

To send an API request, you need a Language resource endpoint and API key.

> [!NOTE]
> You can find the key and endpoint for your Language resource on the Azure portal. They're located on the resource's **Key and endpoint** page, under **resource management**. 

Analysis is performed upon receipt of the request. Using entity linking synchronously is stateless. No data is stored in your account, and results are returned immediately in the response.

[!INCLUDE [asynchronous-result-availability](../../includes/async-result-availability.md)]

### Getting entity linking results  

You can stream the results to an application, or save the output to a file on the local system.

## Service and data limits

[!INCLUDE [service limits article](../../includes/service-limits-link.md)]

## See also

* [Entity linking overview](../overview.md)
