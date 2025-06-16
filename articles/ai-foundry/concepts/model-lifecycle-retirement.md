---
title: Deprecation for Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about the lifecycle stages, deprecation, and retirement for Azure AI Foundry Models.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 05/19/2025
ms.author: mopeakande
author: msakande
ms.reviewer: kritifaujdar
reviewer: fkriti

#Customer intent: As a data scientist, I want to learn about the lifecycle of models that are available in the model catalog.
---

# Model deprecation and retirement for Azure AI Foundry Models

Azure AI Foundry Models in the model catalog are continually refreshed with newer and more capable models. As part of this process, model providers might deprecate and retire their older models, and you might need to update your applications to use a newer model. This document communicates information about the model lifecycle and deprecation timelines and explains how you're informed of model lifecycle stages.


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

This stage is the default model stage. Models that don't include a lifecycle label next to their name are generally available and suitable for use in production environments. In this stage, model weights and APIs are fixed. However, model containers or runtimes with vulnerabilities might get patched, but patches don't affect model outputs.  
 
### Legacy

Models labeled _Legacy_ are intended for deprecation. You should plan to move to a different model, such as a new, improved model that might be available in the same model family. While a model is in the legacy stage, existing deployments of the model continue to work, and you can create new deployments of the model until the deprecation date.

### Deprecated

Models labeled _Deprecated_ are no longer available for new deployments. You can't create any new deployments for the model; however, existing deployments continue to work until the retirement date.

### Retired

Models labeled _Retired_ are no longer available for use. You can't create new deployments, and attempts to use existing deployments return `<return code>` errors.


## Notifications

- Models are labeled as _Legacy_ and remain in the legacy state for at least 30 days before being moved to the deprecated state. During this notification period, you can create new deployments as you prepare for deprecation and retirement.

- Models are labeled _Deprecated_ and remain in the deprecated state for at least 90 days before being moved to the retired state. During this notification period, you can migrate any existing deployments to newer or replacement models.

- For each subscription that has a model deployed as a standard deployment or deployed in Foundry Models, members of the _owner_, _contributor_, _reader_, _monitoring contributor_, and _monitoring reader_ roles receive a notification when a model deprecation is announced. The notification contains the dates when the model enters legacy, deprecated, and retired states. The notification might provide information about possible replacement model options, if applicable.

### More notification details for Azure OpenAI in Foundry Models

Additionally, for Azure OpenAI models, customers with active Azure OpenAI deployments receive notice for models with upcoming retirement as follows:

- At model launch, we programmatically designate a "not sooner than" retirement date (typically one year out).
- At least 60 days notice before model retirement for Generally Available (GA) models.
- At least 30 days notice before preview model version upgrades.  

Retirements are done on a rolling basis, region by region. Notifications are sent from an unmonitored mailbox, `azure-noreply@microsoft.com`.

## Model availability for Azure OpenAI  models

- At least one year of model availability for GA models after the release date of a model in at least one region worldwide.
- For global deployments, all future model versions starting with `gpt-4o` and `gpt-4 0409` will be available with their (`N`) next succeeding model (`N+1`) for comparison together. 
- Customers have 60 days to try out a new GA model in at least one global, or standard region, before any upgrades happen to a newer GA model.  

### Considerations for the Azure public cloud

Be aware of the following details for the Azure public cloud : 

- All model version combinations will **not** be available in all regions.
- Model version `N` and `N+1` might not always be available in the same region. 
- GA model version `N` might upgrade to a future model version `N+X` in some regions based on capacity limitations, and without the new model version `N+X` separately being available to test in the same region. The new model version will be available to test in other regions before any upgrades are scheduled.   
- Preview model versions and GA versions of the same model won't always be available to test together in the same region. There will be preview and GA versions available to test in different regions. 
- To balance service quality for existing customers, we reserve the right to limit future customers from using a particular region. 
- As always at Microsoft, security is of the utmost importance. If a model or model version is found to have compliance or security issues, we reserve the right to invoke the need to do emergency retirements. For more information, see the terms of service.

### Special considerations for Azure Government clouds

- Global standard deployments won't be available in government clouds.
- Not all models or model versions available in commercial/public cloud will be available in government clouds.
- In the Azure Government clouds, we intend to support only one version of a given model at a time.
  - For example, only one version of `gpt-35-turbo 0125` and `gpt-4o (2024-05-13)`.
- There will, however, be a 30-day overlap between new model versions, where more than two will be available.
  - For example, if `gpt-35-turbo 0125` or `gpt-4o (2024-05-13)` is updated to a future version, or
  - For model family changes beyond version updates, such as when moving from `gpt-4 1106-preview` to `gpt-4o (2024-05-13)`. 


## How to get ready for model retirements and version upgrades

To prepare for model retirements and version upgrades, we recommend that customers test their applications with the new models and versions and evaluate their behavior. We also recommend that customers update their applications to use the new models and versions before the retirement date.

For more information on the model evaluation process, see the [Getting started with model evaluation guide](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880).

For information on the model upgrade process, see [Model versions in Azure AI Foundry Models](../model-inference/concepts/model-versions.md) and [How to upgrade to a new model or version](../../ai-services/openai/concepts/model-versions.md).

For more information on how to manage model upgrades and migrations for provisioned deployments, see [Managing models on provisioned deployment types](../../ai-services/openai/how-to/working-with-models.md#managing-models-on-provisioned-deployment-types)

## Timelines for Azure OpenAI models

The following sections list the current, default, and deprecated Azure OpenAI models.

### Current Azure OpenAI models

> [!NOTE]
> Not all models go through a deprecation period before retirement. Some models/versions only have a retirement date.
>
> **Fine-tuned models** are subject to the same deprecation and retirement schedule as their equivalent base model.
>
> The specified dates are in UTC time.

These models are currently available for use in Azure OpenAI.

| Model                     | Version         | Retirement date                    | Replacement model                    |
| --------------------------|-----------------|------------------------------------|--------------------------------------|
| `computer-use-preview`    | 2025-03-11      | No earlier than June 11, 2025      |                                      |
| `dall-e-3`                | 3               | No earlier than June 30, 2025      |                                      |
| `gpt-35-turbo-16k`        | 0613            | April 30, 2025                    | `gpt-4.1-mini` version: `2025-04-14` |
| `gpt-35-turbo`            | 1106            | No earlier than July 16, 2025      | `gpt-4.1-mini` version: `2025-04-14` |
| `gpt-35-turbo`            | 0125            | No earlier than July 16, 2025      | `gpt-4.1-mini` version: `2025-04-14` |
| `gpt-4`<br>`gpt-4-32k`    | 0314            | June 6, 2025                       | `gpt-4o` version: `2024-11-20`       |
| `gpt-4`<br>`gpt-4-32k`    | 0613            | June 6, 2025                       | `gpt-4o` version: `2024-11-20`       |
| `gpt-4`                   | turbo-2024-04-09| No earlier than June 6, 2025       | `gpt-4o` version: `2024-11-20`       |
| `gpt-4`                   | 1106-preview    | May 1, 2025                        | `gpt-4o` version: `2024-11-20`       |
| `gpt-4`                   | 0125-preview    | May 1, 2025                        | `gpt-4o` version: `2024-11-20`        |
| `gpt-4`                   | vision-preview  | May 15, 2025                       | `gpt-4o` version: `2024-11-20`       |
| `gpt-4.5-preview`         | 2025-02-27      | No Auto-upgrades <br>July 14, 2025 | `gpt-4.1` version: `2025-04-14`      |
| `gpt-4.1`                 | 2025-04-14      | No earlier than April 11, 2026     |                                      |
| `gpt-4.1-mini`            | 2025-04-14      | No earlier than April 11, 2026     |                                      |
| `gpt-4.1-nano`            | 2025-04-14      | No earlier than April 11, 2026     |                                      |
| `gpt-4o`                  | 2024-05-13      | No earlier than June 30, 2025      | `gpt-4.1` version: `2025-04-14`      |
| `gpt-4o`                  | 2024-08-06      | No earlier than August 6, 2025     | `gpt-4.1` version: `2025-04-14`      |
| `gpt-4o`                  | 2024-11-20      | No earlier than March 1, 2026      | `gpt-4.1` version: `2025-04-14`      |
| `gpt-4o-mini`             | 2024-07-18      | No earlier than August 16, 2025    | `gpt-4.1-mini` version: `2025-04-14` |
| `gpt-3.5-turbo-instruct`  | 0914            | No earlier than May 31, 2025       |                                      |
| `gpt-image-1`             | 2025-04-15      | No earlier than August 01, 2025    |                                      |
| `o1-preview`              | 2024-09-12      | May 29, 2025                       | `o1`                                 |
| `o1`                      | 2024-12-17      | No earlier than December 17, 2025  |                                      |
| `o4-mini`                 | 2025-04-16      | No earlier than April 11, 2026     |                                      |
| `o3`                      | 2025-04-16      | No earlier than April 11, 2026     |                                      |
| `o3-mini`                 | 2025-01-31      | No earlier than February 1, 2026   |                                      |
| `text-embedding-ada-002`  | 2               | No earlier than April 30, 2026     | `text-embedding-3-small` or `text-embedding-3-large` |
| `text-embedding-ada-002`  | 1               | No earlier than April 30, 2026     | `text-embedding-3-small` or `text-embedding-3-large` |
| `text-embedding-3-small`  |                 | No earlier than April 30, 2026     |                                      |
| `text-embedding-3-large`  |                 | No earlier than April 30, 2026     |                                      |


We'll notify all customers with these preview deployments at least 30 days before the start of the upgrades. We'll publish an upgrade schedule detailing the order of regions and model versions that we'll follow during the upgrades, and link to that schedule from here.

> [!TIP]
> **Will a model upgrade happen if the new model version is not yet available in that region?**
>
> Yes, even in cases where the latest model version isn't yet available in a region, we will automatically upgrade deployments during the scheduled upgrade window. For more information, see [Azure OpenAI model versions](/azure/ai-services/openai/concepts/model-versions#will-a-model-upgrade-happen-if-the-new-model-version-is-not-yet-available-in-that-region).

> [!IMPORTANT]
> Vision enhancements preview features including Optical Character Recognition (OCR), object grounding, video prompts will be retired and no longer available once `gpt-4` Version: `vision-preview` is upgraded to `turbo-2024-04-09`. If you're currently relying on any of these preview features, this automatic model upgrade will be a breaking change.

### Default Azure OpenAI model versions

| Model | Current default version | New default version | Default upgrade date |
|---|---|---|---|
| `gpt-35-turbo` | 0301 | 0125 | Deployments of versions `0301`, `0613`, and `1106` set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on January 21, 2025.|
|  `gpt-4o` | 2024-08-06 | - | - |

### Deprecated Azure OpenAI models

These models are no longer available for new deployments.

If you're an existing customer looking for information about these models, see [Legacy models](../../ai-services/openai/concepts/legacy-models.md).

| Model | Deprecation date | Retirement date | Suggested replacement |
| --------- | --------------------- | ------------------- | -------------------- |
| `gpt-4o-realtime-preview` - 2024-10-01 | February 25, 2025 | March 26, 2025 | `gpt-4o-realtime-preview` (version 2024-12-17) or `gpt-4o-mini-realtime-preview` (version 2024-12-17) |
| `gpt-35-turbo` - 0301 | | February 13, 2025   | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |
| `gpt-35-turbo` - 0613 | | February 13, 2025 | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |
| babbage-002 | | January 27, 2025 |  |
| davinci-002 | | January 27, 2025 | |
| dall-e-2|  | January 27, 2025 | dalle-3 |
| ada | July 6, 2023 | June 14, 2024 |  |
| babbage | July 6, 2023 | June 14, 2024 |  |
| curie | July 6, 2023 | June 14, 2024 | |
| davinci | July 6, 2023 | June 14, 2024 |  |
| text-ada-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-babbage-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-curie-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-davinci-002 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-davinci-003 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| code-cushman-001 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| code-davinci-002 | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| text-similarity-ada-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-similarity-babbage-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-similarity-curie-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-similarity-davinci-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-ada-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-ada-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-babbage-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-babbage-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-curie-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-curie-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-davinci-doc-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| text-search-davinci-query-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-ada-code-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-ada-text-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-babbage-code-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| code-search-babbage-text-001 | July 6, 2023 | June 14, 2024 | text-embedding-3-small |


To track individual updates to this article for Azure OpenAI model retirements, refer to the [Git History](https://github.com/MicrosoftDocs/azure-ai-docs/commits/main/articles/ai-services/openai/concepts/model-retirements.md).


## Timelines for other Foundry Models

The following tables list the timelines for models that are on track for retirement. The specified dates are in UTC time.

#### AI21 Labs

| Model | Legacy date (UTC) | Deprecation date (UTC) | Retirement date (UTC) | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| Jamba Instruct | February 1, 2025 | February 1, 2025 | March 1, 2025 | [AI21-Jamba-1.5-Large](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Large/version/1/registry/azureml-ai21) <br> [AI21-Jamba-1.5-Mini](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Mini/version/1/registry/azureml-staging) |
| Jamba Instruct | February 1, 2025 | February 1, 2025 | March 1, 2025 | N/A |
| [AI21-Jamba-1.5-Large](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Large/version/1/registry/azureml-ai21) | May 1, 2025 | July 1, 2025 | August 1, 2025 | N/A |
| [AI21-Jamba-1.5-Mini](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Mini/version/1/registry/azureml-ai21) | May 1, 2025 | July 1, 2025 | August 1, 2025 | N/A |

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

- [Explore Azure AI Foundry Models](foundry-models-overview.md)
- [Data, privacy, and security for use of models through the model catalog in Azure AI Foundry portal](../how-to/concept-data-privacy.md)
