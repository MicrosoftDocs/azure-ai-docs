---
title: Deprecation for Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about the lifecycle stages, deprecation, and retirement for Azure AI Foundry Models.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 05/05/2025
ms.author: mopeakande
author: msakande
ms.reviewer: kritifaujdar
reviewer: fkriti

#Customer intent: As a data scientist, I want to learn about the lifecycle of models that are available in the model catalog.
---

# Model deprecation and retirement for Azure AI Foundry Models

Azure AI Foundry Models in the model catalog are continually refreshed with newer and more capable models. As part of this process, model providers might deprecate and retire their older models, and you might need to update your applications to use a newer model. This document communicates information about the model lifecycle and deprecation timelines and explains how you're informed of model lifecycle stages.

> [!IMPORTANT]
> This article describes deprecation and retirement only for models that can be deployed to [standard deployment](../how-to/model-catalog-overview.md#model-deployment-managed-compute-and-serverless-apis) or the [Azure AI model Inference](../../ai-foundry/model-inference/overview.md). This article doesn't cover deprecation information for models that can be deployed only to [managed computes](../how-to/model-catalog-overview.md#managed-compute). 

> [!NOTE]
> For information about deprecation and retirement for Azure OpenAI in Foundry Models, see the [Azure OpenAI models lifecycle documentation](/azure/ai-services/openai/concepts/model-retirements.md?context=/azure/ai-foundry/context/context).

## Model lifecycle stages

Models in the model catalog belong to one of these stages:

- Preview
- Generally available
- Legacy
- Deprecated
- Retired

### Preview

Models labeled _Preview_ are experimental in nature. A model's weights, runtime, and API schema can change while the model is in preview. Models in preview aren't guaranteed to become generally available. Models in preview have a _Preview_ label next to their name in the model catalog.  

### Generally available

This stage is the default model stage. Models that don't include a lifecycle label next to their name are generally available and suitable for use in production environments. In this stage, model weights and APIs are fixed. However, model containers or runtimes with vulnerabilities might get patched, but patches won't affect model outputs.  
 
### Legacy

Models labeled _Legacy_ are intended for deprecation. You should plan to move to a different model, such as a new, improved model that might be available in the same model family. While a model is in the legacy stage, existing deployments of the model continue to work, and you can create new deployments of the model until the deprecation date.

### Deprecated

Models labeled _Deprecated_ are no longer available for new deployments. You can't create any new deployments for the model; however, existing deployments continue to work until the retirement date.

### Retired

Models labeled _Retired_ are no longer available for use. You can't create new deployments, and attempts to use existing deployments return `<return code>` errors.


## Notifications

- Models are labeled as _Legacy_ and remain in the legacy state for at least 30 days before being moved to the deprecated state. During this notification period, you may create new deployments as you prepare for deprecation and retirement.

- Models are labeled _Deprecated_ and remain in the deprecated state for at least 90 days before being moved to the retired state. During this notification period, you can migrate any existing deployments to newer or replacement models.

- For each subscription that has a model deployed as a severless API or deployed to the Azure AI model inference, members of the _owner_, _contributor_, _reader_, monitoring contributor_, and _monitoring reader_ roles receive a notification when a model deprecation is announced. The notification contains the dates when the model enters legacy, deprecated, and retired states. The notification might provide information about possible replacement model options, if applicable.

The following tables list the timelines for models that are on track for retirement. The specified dates are in UTC time.

#### AI21 Labs

| Model | Legacy date (UTC) | Deprecation date (UTC) | Retirement date (UTC) | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| Jamba Instruct | February 1, 2025 | February 1, 2025 | March 1, 2025 | [AI21-Jamba-1.5-Large](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Large/version/1/registry/azureml-ai21) <br> [AI21-Jamba-1.5-Mini](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Mini/version/1/registry/azureml-staging) |

#### Cohere

| Model | Legacy date (UTC) | Deprecation date (UTC) | Retirement date (UTC) | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [Command R](https://aka.ms/azureai/landing/Cohere-command-r) | February 24, 2025 | March 25, 2025 | June 30, 2025 | [Cohere Command R 08-2024](https://aka.ms/azureai/landing/Cohere-command-r-08-2024) |
| [Command R+](https://aka.ms/azureai/landing/Cohere-command-r-plus) | February 24, 2025 | March 25, 2025 | June 30, 2025 | [Cohere Command R+ 08-2024](https://aka.ms/azureai/landing/Cohere-command-r-plus-08-2024) |
| [Cohere-rerank-v3-english](https://ai.azure.com/explore/models/Cohere-rerank-v3-english/version/1/registry/azureml-cohere) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Cohere-rerank-v3.5-english](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere) |
| [Cohere-rerank-v3-multilingual](https://ai.azure.com/explore/models/Cohere-rerank-v3-multilingual/version/1/registry/azureml-cohere) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Cohere-rerank-v3.5-multilingual](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere) |

#### DeepSeek

| Model | Legacy date (UTC) | Deprecation date (UTC) | Retirement date (UTC) | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [DeepSeek-V3](https://aka.ms/azureai/landing/DeepSeek-V3) | April 10, 2025 | May 31, 2025 | August 31, 2025 | [DeepSeek-V3-0324](https://aka.ms/azureai/landing/DeepSeek-V3-0324) |

#### Meta

| Model | Legacy date (UTC) | Deprecation date (UTC) | Retirement date (UTC) | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [Llama-2-13b](https://ai.azure.com/explore/models/Llama-2-13b/version/24/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) |
| [Llama-2-13b-chat](https://ai.azure.com/explore/models/Llama-2-13b-chat/version/22/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) |
| [Llama-2-70b](https://ai.azure.com/explore/models/Llama-2-70b/version/25/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) |
| [Llama-2-70b-chat](https://ai.azure.com/explore/models/Llama-2-70b-chat/version/22/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) |
| [Llama-2-7b](https://ai.azure.com/explore/models/Llama-2-7b/version/23/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) |
| [Llama-2-7b-chat](https://ai.azure.com/explore/models/Llama-2-7b-chat/version/27/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) |
| [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/9/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) |
| [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/9/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) |
| [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/4/registry/azureml-meta) | February 28, 2025 | March 31, 2025 | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) |

#### Mistral AI

| Model | Legacy date (UTC) | Deprecation date (UTC) | Retirement date (UTC) | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [Mistral-small](https://ai.azure.com/explore/models/Mistral-small/version/1/registry/azureml-mistral) | March 31, 2025 | April 30, 2025 | July 31, 2025 | [Mistral-small-2503](https://aka.ms/aistudio/landing/mistral-small-2503) |
| [Mistral-large-2407](https://aka.ms/azureai/landing/Mistral-Large-2407) | January 13, 2025 | February 13, 2025 | May 13, 2025 | [Mistral-large-2411](https://aka.ms/aistudio/landing/Mistral-Large-2411) |
| [Mistral-large](https://aka.ms/azureai/landing/Mistral-Large) | December 15, 2024 | January 15, 2025 | April 15, 2025 | [Mistral-large-2411](https://aka.ms/aistudio/landing/Mistral-Large-2411) |

## Related content

- [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md)
- [Data, privacy, and security for use of models through the model catalog in Azure AI Foundry portal](../how-to/concept-data-privacy.md)
