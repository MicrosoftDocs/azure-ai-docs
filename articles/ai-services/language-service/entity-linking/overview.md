---
title: What is entity linking in Azure Language in Foundry Tools?
titleSuffix: Foundry Tools
description: An overview of entity linking in Foundry Tools, which helps you extract entities from text, and provides links to an online knowledge base.
author: laujan
manager: mcleans
ms.service: azure-ai-language
ms.topic: overview
ms.date: 06/30/2026
ms.author: lajanuar
ms.custom: language-service-entity-linking
---
<!-- markdownlint-disable MD025 -->

# What is entity linking in Azure Language in Foundry Tools?

> [!IMPORTANT]
> Entity Linking retires from Azure Language on **September 1, 2028**. To avoid production disruption, migrate existing workloads and create all new projects in Azure Language [**Named Entity Recognition**](../named-entity-recognition/overview.md) or [Microsoft Foundry](../../../foundry/concepts/foundry-models-overview.md), which provide enhanced natural language understanding capabilities and integrate directly into your applications. For more information, see [**Transitioning from Azure Language features to Foundry models**](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/transitioning-from-azure-language-features-to-foundry-models/4524092).

Entity linking is one of the features offered by [Language](../overview.md), a collection of machine learning and AI algorithms in the cloud for developing intelligent applications that involve written language. Entity linking identifies and disambiguates the identity of entities found in text. For example, in the sentence "*We went to Seattle last week.*", the word "*Seattle*" would be identified, with a link to more information on Wikipedia.

This documentation contains the following types of articles:

* [**Quickstarts**](quickstart.md) are getting-started instructions to guide you through making requests to the service.
* [**How-to guides**](how-to/call-api.md) contain instructions for using the service in more specific ways.

## Get started with entity linking

[!INCLUDE [development-options](includes/development-options.md)]

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)]

## Responsible AI

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Read the [transparency note for entity linking](/azure/ai-foundry/responsible-ai/language-service/transparency-note) to learn about responsible AI use and deployment in your systems.

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]

## Next steps

There are two ways to get started using the entity linking feature:

* [Microsoft Foundry](https://ai.azure.com/), which is a web-based platform that enables you to try several Language features without needing to write code.
* The [quickstart article](quickstart.md) for instructions on making requests to the service using the REST API and client library SDK.
