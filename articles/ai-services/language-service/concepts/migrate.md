---
title: "Migrate to Azure Language in Foundry Tools from: Language Understanding (LUIS), QnA Maker, and Text Analytics"
titleSuffix: Foundry Tools
description: Use this article to learn if you need to migrate your applications from Language Understanding (LUIS), QnA Maker, and Text Analytics.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
---
# Migrating to Azure Language in Foundry Tools

On November 2, 2021, Azure Language in Foundry Tools was released into public preview. Azure Language unifies the Text Analytics, QnA Maker, and Language Understanding (LUIS) service offerings, and provides several new features as well.

## Do I need to migrate to Azure Language if I'm using Text Analytics?

Text Analytics is incorporated into Azure Language, and its features are still available. If you're using Text Analytics features, your applications should continue to work without breaking changes. If you're using Text Analytics API (v2.x or v3), see the [Text Analytics migration guide](migrate-language-service-latest.md) to migrate your applications to the unified Language endpoint and the latest client library.

Consider using one of the available quickstart articles to see the latest information on service endpoints, and API calls.

## How do I migrate to Azure Language if I'm using Language Understanding (LUIS)?

If you're using Language Understanding (Language Understanding (LUIS)), you can [import your Language Understanding (LUIS) JSON file](../conversational-language-understanding/how-to/migrate-from-Language Understanding (LUIS).md) to the new Conversational language understanding feature.

## How do I migrate to Azure Language if I'm using QnA Maker?

If you're using QnA Maker, see the [migration guide](/previous-versions/azure/ai-services/qnamaker/overview/overview) for information on migrating knowledge bases from QnA Maker to question answering.

## See also

* [Azure Language in Foundry Tools overview](../overview.md)
* [Conversational language understanding overview](../conversational-language-understanding/overview.md)
* [Question answering overview](../question-answering/overview.md)
