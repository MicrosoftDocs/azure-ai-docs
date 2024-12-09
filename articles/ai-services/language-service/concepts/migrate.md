---
title: "Migrate to Azure AI Language from: LUIS, QnA Maker, and Text Analytics"
titleSuffix: Azure AI services
description: Use this article to learn if you need to migrate your applications from LUIS, QnA Maker, and Text Analytics.
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 11/21/2024
ms.author: jboback
---

# Migrating to Azure AI Language

On November 2nd 2021, Azure AI Language was released into public preview. This language service unifies the Text Analytics, QnA Maker, and LUIS service offerings, and provides several new features as well. 

## Do I need to migrate to the language service if I am using Text Analytics?

Text Analytics has been incorporated into the language service, and its features are still available. If you were using Text Analytics features, your applications should continue to work without breaking changes. If you are using Text Analytics API (v2.x or v3), see the [Text Analytics migration guide](migrate-language-service-latest.md) to migrate your applications to the unified Language endpoint and the latest client library. 

Consider using one of the available quickstart articles to see the latest information on service endpoints, and API calls. 

## How do I migrate to the language service if I am using LUIS?

If you're using Language Understanding (LUIS), you can [import your LUIS JSON file](../conversational-language-understanding/how-to/migrate-from-luis.md) to the new Conversational language understanding feature. 

## How do I migrate to the language service if I am using QnA Maker?

If you're using QnA Maker, see the [migration guide](../question-answering/how-to/migrate-qnamaker.md) for information on migrating knowledge bases from QnA Maker to question answering.

## See also

* [Azure AI Language overview](../overview.md)
* [Conversational language understanding overview](../conversational-language-understanding/overview.md)
* [Question answering overview](../question-answering/overview.md)
