---
title: "How to generate text responses with Microsoft Foundry Models (classic)"
description: "Learn how to generate text responses from Foundry Models, such as Microsoft AI and DeepSeek models, by using the Responses API. (classic)"
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/24/2026
ms.author: mopeakande
author: msakande
ms.reviewer: achand
reviewer: achandmsft
ms.custom:
  - generated, pilot-ai-workflow-jan-2026
  - classic-and-new
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# How to generate text responses with Microsoft Foundry Models (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

This article explains how to generate text responses for Foundry Models, such as Microsoft AI, DeepSeek, and Grok models, by using the Responses API. For a full list of the Foundry Models that support use of the Responses API, see [Supported Foundry Models](#supported-foundry-models). 

## Prerequisites

To use the Responses API with deployed models in your application, you need:

- An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Microsoft Foundry Models](../how-to/quickstart-github-models.md) if that's your case.

- A Foundry project. This kind of project is managed under a Foundry resource. If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../how-to/create-projects.md).

- Your Foundry project's endpoint URL, which is of the form `https://YOUR-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR_PROJECT_NAME`.

- A deployment of a Foundry Model, such as the `DeepSeek-R1-0528` model used in this article. If you don't have a deployment already, see [Add and configure Foundry Models](create-model-deployments.md) to a model deployment to your resource.

### Use the AI model starter kit

The code snippets in this article are from the [AI model starter kit](https://aka.ms/ai-model-start). Use this starter kit as a quick way to get started with complete cloud infrastructure and code needed to call Foundry Models, using a stable OpenAI library with the Responses API.

## Use the Responses API to generate text

Use the code in this section to make Responses API calls for Foundry Models. In the code samples, you create the client to consume the model and then send it a basic request. 

[!INCLUDE [generate-responses-non-azure-openai](../../../foundry/includes/generate-responses-non-azure-openai.md)]


## Supported Foundry Models

A selection of Foundry Models are supported for use with the Responses API.

### View supported models in the Foundry portal

[!INCLUDE [agent-service-view-models-in-portal](../../agents/includes/agent-service-view-models-in-portal.md)]

### List of supported models

This section lists some of the Foundry Models that are supported for use with the Responses API. For the Azure OpenAI models that are supported, see [Available Azure OpenAI models](../../agents/concepts/model-region-support.md#available-models).
[!INCLUDE [agent-service-models-support-list](../../../foundry/agents/includes/agent-service-models-support-list.md)]

## Troubleshoot common errors

| Error | Cause | Resolution |
| --- | --- | --- |
| 401 Unauthorized | Invalid or expired credential | Verify your `DefaultAzureCredential` has the **Cognitive Services OpenAI User** role assigned on the resource. |
| 404 Not Found | Wrong endpoint or deployment name | Confirm your endpoint URL includes `/api/projects/YOUR_PROJECT_NAME` and the deployment name matches your Foundry portal. |
| 400 Model not supported | Model doesn't support Responses API | Check the [supported models list](#supported-foundry-models) and verify your deployment uses a compatible model. |

## Related content

- [Migrate from Azure AI Inference SDK to OpenAI SDK](../../how-to/model-inference-to-openai-migration.md)
- [Azure OpenAI supported programming languages](../../openai/supported-languages.md)
- [Switch between OpenAI and Azure OpenAI endpoints](/azure/developer/ai/how-to/switching-endpoints)
- [Model support for v1 Azure OpenAI API](../../openai/api-version-lifecycle.md#model-support)

