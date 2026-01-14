---
title: How to build an orchestration project schema
description: Learn how to define intents for your orchestration workflow project.
titleSuffix: Foundry Tools
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-orchestration
---
# How to build your project schema for orchestration workflow
 
In orchestration workflow projects, the *schema* is defined as the combination of intents within your project. Schema design is a crucial part of your project's success. When creating a schema, you should think about the intents to include in your project.

## Guidelines and recommendations

Consider the following guidelines and recommendations for your project:

*    Build orchestration projects when you need to manage the NLU for a multi-faceted virtual assistant or chatbot.
*    Orchestrate between different domains. A domain is a collection of intents and entities that serve the same purpose, such as Email commands vs. Restaurant commands.
*    If there's an overlap of similar intents between domains, create the common intents in a separate domain and removing them from the others for the best accuracy.
*    For intents that are general across domains, such as `Greeting`, `Confirm`, or `Reject`, you can either add them in a separate domain or as direct intents in the Orchestration project. 
*    Orchestrate to Custom question answering knowledge base when a domain has FAQ type questions with static answers. Ensure that the vocabulary and language used to ask questions is distinctive from the one used in the other Conversational Language Understanding projects and LUIS applications.
*    If an utterance is being misclassified and routed to an incorrect intent, then add similar utterances to the intent to influence its results. If the intent is connected to a project, then add utterances to the connected project itself. After you retrain your orchestration project, the new utterances in the connected project will influence predictions.
*    Add test data to your orchestration projects to validate there isn't confusion between linked projects and other intents.

## Next steps

* [Add utterances](tag-utterances.md)

