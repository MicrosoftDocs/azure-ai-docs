---
title: What is sentiment analysis and opinion mining in the Language service?
titleSuffix: Azure AI services
description: An overview of the sentiment analysis feature in Azure AI services, which helps you find out what people think of a topic by mining text for clues.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 02/17/2025
ms.author: lajanuar
ms.custom: language-service-sentiment-opinion-mining
---

# What is sentiment analysis and opinion mining?

Sentiment analysis and opinion mining are features offered by [the Language service](../overview.md), a collection of machine learning and AI algorithms in the cloud for developing intelligent applications that involve written language. These features help you find out what people think of your brand or topic by mining text for clues about positive or negative sentiment, and can associate them with specific aspects of the text. 

Both sentiment analysis and opinion mining work with various [written languages](./language-support.md).

## Sentiment analysis 

The sentiment analysis feature provides sentiment labels (such as "negative", "neutral" and "positive") based on the highest confidence score found by the service at a sentence and document-level. This feature also returns confidence scores between 0 and 1 for each document & sentences within it for positive, neutral, and negative sentiment. 

## Opinion mining

Opinion mining is a feature of sentiment analysis, also known as aspect-based sentiment analysis in Natural Language Processing (NLP). This feature provides more granular information about the opinions related to words (such as the attributes of products or services) in text.

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]

## Get started with sentiment analysis

[!INCLUDE [development options](./includes/development-options.md)]

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)] 

## Reference documentation

As you use sentiment analysis, see the following reference documentation and samples for the Language service:

|Development option / language  |Reference documentation |Samples  |
|---------|---------|---------|
|REST APIs (Authoring)   | [REST API documentation](https://aka.ms/ct-authoring-swagger)        |         |
|REST APIs (Runtime)    | [REST API documentation](https://aka.ms/ct-runtime-swagger)        |         |

--- 

## Responsible AI 

An AI system includes not only the technology, but also the people who use it, the people who are affected by it, and the environment in which it's deployed. Read the [transparency note for sentiment analysis](/azure/ai-foundry/responsible-ai/language-service/transparency-note-sentiment-analysis) to learn about responsible AI use and deployment in your systems. You can also see the following articles for more information:

## Next steps

* The quickstart articles with instructions on using the service for the first time.
    * [Use sentiment analysis and opinion mining](./quickstart.md)