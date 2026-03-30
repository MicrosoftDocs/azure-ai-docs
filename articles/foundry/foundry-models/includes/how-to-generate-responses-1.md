---
title: Include file
description: Include file
author: msakande
ms.reviewer: achand
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

This article explains how to generate text responses for Foundry Models, such as Microsoft AI, DeepSeek, and Grok models, by using the Responses API. For a full list of the Foundry Models that support use of the Responses API, see [Supported Foundry Models](#supported-foundry-models).

## Prerequisites

To use the Responses API with deployed models in your application, you need:

- An Azure subscription. If you're using GitHub Models, you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) if that's your case.

- A Foundry project. This kind of project is managed under a Foundry resource. If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../how-to/create-projects.md).

- Your Foundry project's endpoint URL, which is of the form `https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME`.

- A deployment of a Foundry Model, such as the `DeepSeek-R1-0528` model used in this article. If you don't have a deployment already, see [Add and configure Foundry Models](../how-to/create-model-deployments.md) to a model deployment to your resource.

### Use the AI model starter kit

The code snippets in this article are from the [AI model starter kit](https://aka.ms/ai-model-start). Use this starter kit as a quick way to get started with complete cloud infrastructure and code needed to call Foundry Models, using a stable OpenAI library with the Responses API.

## Use the Responses API to generate text

Use the code in this section to make Responses API calls for Foundry Models. In the code samples, you create the client to consume the model and then send it a basic request. 

[!INCLUDE [generate-responses-non-azure-openai](../../includes/generate-responses-non-azure-openai.md)]
