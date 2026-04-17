---
title: include file
description: include file
author: msakande
ms.author: mopeakande
ms.reviewer: rasavage
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/16/2026
ms.custom: include, classic-and-new
---

Microsoft Foundry continuously refreshes its model catalog with newer, more capable models. As part of this process, model providers might deprecate and retire their older models, and you might need to update your applications to use a newer model.

For full details on lifecycle stages (Preview, GA, Legacy, Deprecated, Retired), notification timelines, automatic upgrade behavior, and migration guidance, see [Model Lifecycle and Support Policy](../openai/concepts/model-retirements.md).

> [!IMPORTANT]
> In some cases, model providers might retire models on an accelerated schedule with shorter notice periods. Always check the specific dates in the [upcoming retirements](#upcoming-retirements-for-foundry-models) table for your model, as the actual timeline for a given model takes precedence over the general policy.

## Upcoming retirements for Foundry Models

The following tables list the timelines for models that are on track for retirement. The lifecycle stages go into effect at 00:00:00 UTC on the specified dates.

#### Cohere

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere/?cid=learnDocs) | January 14, 2026 | February 14, 2026 | May 14, 2026 | [Cohere-rerank-v4.0-pro](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-pro/version/1/registry/azureml-cohere/?cid=learnDocs), [Cohere-rerank-v4.0-fast](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-fast/version/2/registry/azureml-cohere/?cid=learnDocs) |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | February 12, 2026 | March 12, 2026 | May 12, 2026 | [Cohere-command-a](https://ai.azure.com/explore/models/Cohere-command-a/version/1/registry/azureml-cohere/?cid=learnDocs) |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | February 12, 2026 | March 12, 2026 | May 12, 2026 | [Cohere-command-a](https://ai.azure.com/explore/models/Cohere-command-a/version/1/registry/azureml-cohere/?cid=learnDocs) |

#### Deci AI

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [deci-decidiffusion-v1-0](https://ai.azure.com/explore/models/deci-decidiffusion-v1-0/version/7/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |

#### Meta

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | February 13, 2026 | March 13, 2026 | June 13, 2026 | N/A |
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/6/registry/azureml-meta/?cid=learnDocs) | February 13, 2026 | March 13, 2026 | June 13, 2026 | N/A |
| [Meta-Llama-3.1-8B](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B/version/1/registry/azureml-meta/?cid=learnDocs) | February 13, 2026 | March 13, 2026 | June 13, 2026 | N/A |
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | February 13, 2026 | March 13, 2026 | June 13, 2026 | [Llama-4-Maverick-17B-128E-Instruct-FP8](https://ai.azure.com/explore/models/Llama-4-Maverick-17B-128E-Instruct-FP8/version/1/registry/azureml-meta/?cid=learnDocs), [Llama-4-Scout-17B-16E-Instruct](https://ai.azure.com/explore/models/Llama-4-Scout-17B-16E-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) |
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | February 13, 2026 | March 13, 2026 | June 13, 2026 | [Llama-4-Maverick-17B-128E-Instruct-FP8](https://ai.azure.com/explore/models/Llama-4-Maverick-17B-128E-Instruct-FP8/version/1/registry/azureml-meta/?cid=learnDocs), [Llama-4-Scout-17B-16E-Instruct](https://ai.azure.com/explore/models/Llama-4-Scout-17B-16E-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) |

#### Microsoft

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [financial-reports-analysis](https://ai.azure.com/explore/models/financial-reports-analysis/version/2/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |
| [financial-reports-analysis-v2](https://ai.azure.com/explore/models/financial-reports-analysis-v2/version/1/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |
| [supply-chain-trade-regulations](https://ai.azure.com/explore/models/supply-chain-trade-regulations/version/3/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |
| [supply-chain-trade-regulations-v2](https://ai.azure.com/explore/models/supply-chain-trade-regulations-v2/version/1/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |

#### xAI

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [grok-4-fast-reasoning](https://ai.azure.com/explore/models/grok-4-fast-reasoning/version/1/registry/azureml-xai/?cid=learnDocs) | March 26, 2026 | April 1, 2026 | May 1, 2026 | [grok-4-1-fast-reasoning](https://ai.azure.com/explore/models/grok-4-1-fast-reasoning/version/1/registry/azureml-xai/?cid=learnDocs) |
| [grok-4-fast-non-reasoning](https://ai.azure.com/explore/models/grok-4-fast-non-reasoning/version/1/registry/azureml-xai/?cid=learnDocs) | March 26, 2026 | April 1, 2026 | May 1, 2026 | [grok-4-1-fast-non-reasoning](https://ai.azure.com/explore/models/grok-4-1-fast-non-reasoning/version/1/registry/azureml-xai/?cid=learnDocs) |
| [grok-3-mini](https://ai.azure.com/explore/models/grok-3-mini/version/1/registry/azureml-xai/?cid=learnDocs) | March 26, 2026 | April 1, 2026 | May 1, 2026 | [grok-4-1-fast-reasoning](https://ai.azure.com/explore/models/grok-4-1-fast-reasoning/version/1/registry/azureml-xai/?cid=learnDocs) |
| [grok-3](https://ai.azure.com/explore/models/grok-3/version/1/registry/azureml-xai/?cid=learnDocs) | March 26, 2026 | April 1, 2026 | May 1, 2026 | [grok-4](https://ai.azure.com/explore/models/grok-4/version/1/registry/azureml-xai/?cid=learnDocs) |

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
| MAI-DS-R1 | February 27, 2026 | Any DeepSeek model available in the Model catalog |
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

#### Moonshot AI

| Model | Retirement date | Suggested replacement model |
|-------|-----------------------|-----------------------------|
| Kimi-k2-thinking | March 29, 2026 | [Kimi-k2.5](https://ai.azure.com/explore/models/Kimi-k2.5/version/1/registry/azureml-moonshotai/?cid=learnDocs) |

## Migrate to a replacement model

When a model you use enters the legacy or deprecated stage, follow these steps to migrate:

1. **Identify the replacement.** Check the **Suggested replacement model** column in the [upcoming retirements](#upcoming-retirements-for-foundry-models) or [retired models](#retired-foundry-models) tables.
1. **Test the replacement.** Deploy the suggested replacement model and validate that it meets your application requirements, including output quality, latency, and cost.
1. **Update your deployments.** Create a new deployment with the replacement model and update your application code to point to the new deployment name.
1. **Delete the old deployment.** After you confirm the replacement works correctly, delete the deprecated model deployment to avoid unexpected `404` errors after retirement.

> [!TIP]
> Start migration as soon as a model enters the _Legacy_ stage. This gives you the maximum time to test and transition before the model is deprecated and new deployments are blocked.

## Related content

- [Azure OpenAI in Foundry Models model deprecations and retirements](../openai/concepts/model-retirements.md)
- [Data, privacy, and security for use of models through the model catalog in Foundry portal](../../foundry-classic/how-to/concept-data-privacy.md)
- [Set up Service Health alerts](/azure/service-health/alerts-activity-log-service-notifications-portal)
