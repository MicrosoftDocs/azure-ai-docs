---
title: What is sentiment analysis and opinion mining in Azure Language service?
titleSuffix: Foundry Tools
description: An overview of the sentiment analysis feature in Azure Language, which helps you find out what people think of a topic by mining text for clues.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-sentiment-opinion-mining
---
# What is sentiment analysis and opinion mining?

Sentiment analysis and opinion mining are features offered by [Azure Language](../overview.md), a collection of machine learning and AI algorithms in the cloud for developing intelligent applications that involve written language. These features help you discover what people think about your brand or topic by analyzing text for signs of positive or negative sentiment. They can also link these sentiments to specific aspects of the text.

Both sentiment analysis and opinion mining work with various [written languages](./language-support.md).

## Sentiment analysis

The sentiment analysis feature assigns sentiment labels, such as "negative," "neutral," and "positive." The service determines these labels using the highest confidence score. Sentiment is evaluated at both the sentence level and the document level. This feature also returns confidence scores between 0 and 1 for each document & sentences within it for positive, neutral, and negative sentiment.

## Opinion mining

Opinion mining is a feature of sentiment analysis, also known as aspect-based sentiment analysis in Natural Language Processing (NLP). This feature provides more granular information about the opinions related to words (such as the attributes of products or services) in text.

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]

## Get started with sentiment analysis

[!INCLUDE [development options](./includes/development-options.md)]

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)]

## Reference documentation

As you use sentiment analysis, see the following reference documentation and samples for Azure Language:

|Development option / language  |Reference documentation |Samples  |
|---------|---------|---------|
|REST APIs (Authoring)   | [REST API documentation](https://aka.ms/ct-authoring-swagger)        |         |
|REST APIs (Runtime)    | [REST API documentation](https://aka.ms/ct-runtime-swagger)        |         |

---

## Responsible AI

An AI system encompasses more than just the technology itself. An AI system includes the individuals who operate the system, the people who experience its effects, and the broader environment where the system functions all play a role. Read the [transparency note for sentiment analysis](/azure/ai-foundry/responsible-ai/language-service/transparency-note-sentiment-analysis) to learn about responsible AI use and deployment in your systems. 

## Next steps

Get started with our quickstart articles with instructions on using the service for the first time: [Use sentiment analysis and opinion mining](./quickstart.md)
