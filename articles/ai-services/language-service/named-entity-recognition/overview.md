---
title: What is the Named Entity Recognition (NER) feature in Azure Language in Foundry Tools?
titleSuffix: Foundry Tools
description: An overview of the Named Entity Recognition feature in Azure Language, which helps you extract categories of entities in text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-ner
---
# What is Named Entity Recognition (NER) in Azure Language in Foundry Tools?

Named Entity Recognition (NER) is one of the features offered by [Azure Language in Foundry Tools](../overview.md), a collection of machine learning and AI algorithms in the cloud for developing intelligent applications that involve written language. The NER feature can identify and categorize entities in unstructured text. For example: people, places, organizations, and quantities. The prebuilt NER feature has a preset list of [recognized entities](concepts/named-entity-categories.md). The custom NER feature allows you to train the model to recognize specialized entities specific to your use case.

* [**Quickstarts**](quickstart.md) are getting-started instructions to guide you through making requests to the service.
* [**How-to guides**](how-to-call.md) contain instructions for using the service in more specific or customized ways.
* The [**conceptual articles**](concepts/named-entity-categories.md) provide in-depth explanations of the service's functionality and features.

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]

## Get started with named entity recognition

[!INCLUDE [development options](./includes/development-options.md)]

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)]

## Responsible AI

An AI system consists of more than just its core technology. It also includes the people who operate it, the people its use affects, and the broader deployment context.
All these interconnected elements shape the effectiveness and outcomes of AI. Read the [transparency note for NER](/azure/ai-foundry/responsible-ai/language-service/transparency-note-named-entity-recognition) to learn about responsible AI use and deployment in your systems. For more information, *see* the following articles:

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]

## Scenarios

* **Enhance search capabilities and search indexing**. Customers can build knowledge graphs based on entities detected in documents to enhance document search as tags.
* **Automate business processes** - Insurance claims, recognized entities like name and location can be highlighted to facilitate review. Support tickets can be automatically generated with customer name and company from an email.
* **In-depth customer analysis**. Determine the most popular information conveyed by customers in reviews, emails, and calls to determine relevant topics and trends over time.

## Next steps

There are two ways to get started using the Named Entity Recognition (NER) feature:
* [Microsoft Foundry](../../../ai-foundry/what-is-foundry.md) is a web-based platform that lets you use several Language features without needing to write code.
* The [quickstart article](quickstart.md) for instructions on making requests to the service using the REST API and client library SDK.
