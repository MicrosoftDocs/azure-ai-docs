---
title: Deprecation for Foundry Models
titleSuffix: Microsoft Foundry
description: Learn about the lifecycle stages, deprecation, and retirement for Microsoft Foundry Models.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.date: 02/03/2026
ms.author: mopeakande
manager: nitinme
author: msakande
ms.reviewer: rasavage
reviewer: rsavage2

#Customer intent: As a data scientist, I want to learn about the lifecycle of models that are available in the model catalog.
---

# Model deprecation and retirement for Microsoft Foundry Models

[!INCLUDE [version-banner](../includes/version-banner.md)]

Microsoft Foundry Models are continually refreshed with newer and more capable models. As part of this process, model providers might deprecate and retire their older models, and you might need to update your applications to use a newer model. This document communicates information about the model lifecycle and deprecation timelines and explains how you're informed of model lifecycle stages.

This article covers general deprecation and retirement information for Foundry Models. For details specific to Azure OpenAI in Foundry Models, see [Azure OpenAI in Foundry Models model deprecations and retirements](../openai/concepts/model-retirements.md). 


## Model lifecycle stages

Models in the model catalog belong to one of these stages:

- Preview
- Generally available
- Legacy
- Deprecated
- Retired

### Preview

Models labeled _Preview_ are experimental in nature. A model's weights, runtime, and API schema can change while the model is in preview. Models in preview aren't guaranteed to become generally available. Models in preview have a _Preview_ label next to their name in the model catalog.  

### Generally available (GA)

This stage is the default model stage. Models that don't include a lifecycle label next to their name are GA and suitable for use in production environments. In this stage, model weights and APIs are fixed. However, model containers or runtimes with vulnerabilities might get patched, but patches don't affect model outputs.  
 
### Legacy

Models labeled _Legacy_ are intended for deprecation. You should plan to move to a different model, such as a new, improved model that might be available in the same model family. While a model is in the legacy stage, existing deployments of the model continue to work, and you can create new deployments of the model until the deprecation date.

### Deprecated

Models labeled _Deprecated_ are no longer available for new deployments. You can't create any new deployments for the model; however, existing deployments continue to work until the retirement date.

### Retired

Models labeled _Retired_ are no longer available for use. You can't create new deployments, and attempts to use existing deployments return `404` errors.


## Notifications for Foundry Models

Customers that have Foundry Model deployments receive notifications for upcoming model retirements according to the following schedule:

- Models are labeled as _Legacy_ and remain in the legacy state for at least 30 days before being moved to the deprecated state. During this notification period, you can create new deployments as you prepare for deprecation and retirement.

- Models are labeled _Deprecated_ and remain in the deprecated state for at least 90 days before being moved to the retired state. During this notification period, you can migrate any existing deployments to newer or replacement models.

For each subscription that has a model deployed as a serverless API deployment or deployed to a Foundry resource, members of the _owner_, _contributor_, _reader_, _monitoring contributor_, and _monitoring reader_ roles receive a notification when a model deprecation is announced. The notification contains the dates when the model enters legacy, deprecated, and retired states. The notification might provide information about possible replacement model options, if applicable.

## Notifications for Azure OpenAI in Foundry Models

For Azure OpenAI models, customers with active Azure OpenAI deployments receive notice for models with upcoming retirement as follows:

- At model launch, we programmatically designate a "not sooner than" retirement date (typically one year out).
- At least 60 days notice before model retirement for Generally Available (GA) models.
- At least 30 days notice before preview model version upgrades.  

Members of the _owner_, _contributor_, _reader_, _monitoring contributor_, and _monitoring reader_ roles receive notification for each subscription with a deployment of a model that has an upcoming retirement.

Retirements are done on a rolling basis, region by region. Notifications are sent from an unmonitored mailbox, `azure-noreply@microsoft.com`.

To learn more about the Azure OpenAI models lifecycle, including information for current, deprecated, and retired models, see [Azure OpenAI in Foundry Models model deprecations and retirements](../openai/concepts/model-retirements.md). 

## Upcoming retirements for Foundry Models

The following tables list the timelines for models that are on track for retirement. The lifecycle stages go into effect at 00:00:00 UTC on the specified dates.

#### Cohere

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere/?cid=learnDocs) | January 14, 2026 | February 14, 2026 | May 14, 2026 | [Cohere-rerank-v4.0-pro](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-pro/version/1/registry/azureml-cohere/?cid=learnDocs), [Cohere-rerank-v4.0-fast](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-fast/version/2/registry/azureml-cohere/?cid=learnDocs) |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | February 12, 2026 | March 12, 2026 | May 12, 2026 | [Cohere-command-a](https://ai.azure.com/explore/models/Cohere-command-a/version/1/registry/azureml-cohere/?cid=learnDocs) |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | February 12, 2026 | March 12, 2026 | May 12, 2026 | [Cohere-command-a](https://ai.azure.com/explore/models/Cohere-command-a/version/1/registry/azureml-cohere/?cid=learnDocs) |

#### Microsoft

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml/?cid=learnDocs) | January 16, 2026 | January 27, 2026 | February 27, 2026 | Any DeepSeek model available in the Model catalog |

## Retired Foundry Models

The following models were retired at 00:00:00 UTC on the specified dates and aren't available for new deployments or inference.

#### AI21 Labs

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Jamba Instruct | March 1, 2025 | N/A |
| AI21-Jamba-1.5-Large | August 1, 2025 | N/A |
| AI21-Jamba-1.5-Mini | August 1, 2025 | N/A |

#### Bria

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Bria-2.3-Fast | October 31, 2025 | N/A |

#### Cohere

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Command R | June 30, 2025 | [Cohere Command R 08-2024](https://aka.ms/azureai/landing/Cohere-command-r-08-2024?cid=learnDocs) |
| Command R+ | June 30, 2025 | [Cohere Command R+ 08-2024](https://aka.ms/azureai/landing/Cohere-command-r-plus-08-2024?cid=learnDocs) |
| Cohere-rerank-v3-english | June 30, 2025 | [Cohere-rerank-v4.0-pro](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-pro/version/1/registry/azureml-cohere/?cid=learnDocs), [Cohere-rerank-v4.0-fast](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-fast/version/2/registry/azureml-cohere/?cid=learnDocs) |
| Cohere-rerank-v3-multilingual | June 30, 2025 | [Cohere-rerank-v4.0-pro](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-pro/version/1/registry/azureml-cohere/?cid=learnDocs), [Cohere-rerank-v4.0-fast](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-fast/version/2/registry/azureml-cohere/?cid=learnDocs) |

#### Core42

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| jais-30b-chat | January 30, 2026 | N/A |

#### DeepSeek

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| DeepSeek-V3 | August 31, 2025 | [DeepSeek-V3-0324](https://aka.ms/azureai/landing/DeepSeek-V3-0324?cid=learnDocs) |

#### Gretel

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Gretel-Navigator-Tabular | September 16, 2025 | N/A |

#### Meta

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Llama-2-13b | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Llama-2-13b-chat | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Llama-2-70b | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Llama-2-70b-chat | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Llama-2-7b | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Llama-2-7b-chat | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Meta-Llama-3-70B-Instruct | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Meta-Llama-3-8B-Instruct | June 30, 2025 | [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |
| Meta-Llama-3.1-70B-Instruct | June 30, 2025 | [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) |

#### Microsoft

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Phi-3-medium-4k-instruct | August 30, 2025 | [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/8/registry/azureml/?cid=learnDocs) |
| Phi-3-medium-128k-instruct | August 30, 2025 | [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/8/registry/azureml/?cid=learnDocs) |
| Phi-3-mini-4k-instruct | August 30, 2025 | [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) |
| Phi-3-mini-128k-instruct | August 30, 2025 | [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) |
| Phi-3-small-8k-instruct | August 30, 2025 | [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) |
| Phi-3-small-128k-instruct | August 30, 2025 | [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) |
| Phi-3.5-mini-instruct | August 30, 2025 | [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) |
| Phi-3.5-MoE-instruct | August 30, 2025 | [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) |
| Phi-3.5-vision-instruct | August 30, 2025 | [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) |

#### Mistral AI

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Mistral-Nemo | January 30, 2026 | [Mistral-small-2503](https://aka.ms/aistudio/landing/mistral-small-2503) |
| Mistral-large-2411 | January 30, 2026 | [Mistral-medium-2505](https://ai.azure.com/explore/models/mistral-medium-2505/version/1/registry/azureml-mistral/?cid=learnDocs) |
| Mistral-ocr-2503 | January 30, 2026 | [Mistral-document-ai-2505](https://ai.azure.com/explore/models/mistral-document-ai-2505/version/1/registry/azureml-mistral/?cid=learnDocs) |
| Mistral-small | July 31, 2025 | [Mistral-small-2503](https://aka.ms/aistudio/landing/mistral-small-2503) |
| Mistral-large-2407 | May 13, 2025 | [Mistral-medium-2505](https://ai.azure.com/explore/models/mistral-medium-2505/version/1/registry/azureml-mistral/?cid=learnDocs) |
| Mistral-large | April 15, 2025 | [Mistral-medium-2505](https://ai.azure.com/explore/models/mistral-medium-2505/version/1/registry/azureml-mistral/?cid=learnDocs) |

## Related content

- [Azure OpenAI in Foundry Models model deprecations and retirements](../openai/concepts/model-retirements.md)
- [Data, privacy, and security for use of models through the model catalog in Foundry portal](../how-to/concept-data-privacy.md)
