---
title: Azure OpenAI Service model retirements
titleSuffix: Azure OpenAI
description: Learn about the model deprecations and retirements in Azure OpenAI.
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 12/02/2024
ms.custom: 
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin 
recommendations: false
---

# Azure OpenAI Service model deprecations and retirements

## Overview

Azure OpenAI Service models are continually refreshed with newer and more capable models. As part of this process, we deprecate and retire older models. This document provides information about the models that are currently available, deprecated, and retired.

### Terminology

* Retirement
	* When a model is retired, it's no longer available for use. Azure OpenAI Service deployments of a retired model always return error responses.
* Deprecation
	* When a model is deprecated, it's no longer available for new customers. It continues to be available for use by customers with existing deployments until the model is retired.

## Notifications

Azure OpenAI notifies customers of active Azure OpenAI Service deployments for models with upcoming retirements. We notify customers of upcoming retirements as follows for each deployment:

1. At model launch, we programmatically designate a "not sooner than" retirement date (typically one year out).
2. At least 60 days notice before model retirement for Generally Available (GA) models.
3. At least 30 days notice before preview model version upgrades.  

Retirements are done on a rolling basis, region by region.

## Model availability

1. At least one year of model availability for GA models after the release date of a model in at least one region worldwide
2. For global deployments, all future model versions starting with `gpt-4o` and `gpt-4 0409` will be available with their (`N`) next succeeding model (`N+1`) for comparison together. 
1. Customers have 60 days to try out a new GA model in at least one global, or standard region, before any upgrades happen to a newer GA model.  

### Considerations for the Azure public cloud

Be aware of the following: 

1. All model version combinations will **not** be available in all regions.
2. Model version `N` and `N+1` might not always be available in the same region. 
3. GA model version `N` might upgrade to a future model version `N+X` in some regions based on capacity limitations, and without the new model version `N+X` separately being available to test in the same region. The new model version will be available to test in other regions before any upgrades are scheduled.   
4. Preview model versions and GA versions of the same model won't always be available to test together in the same region. There will be preview and GA versions available to test in different regions. 
5.	We reserve the right to limit future customers using a particular region to balance service quality for existing customers.
6.	As always at Microsoft, security is of the utmost importance. If a model or model version is found to have compliance or security issues, we reserve the right to invoke the need to do emergency retirements. See the terms of service for more information.

### Special considerations for Azure Government clouds

1.	Global standard deployments won't be available in government clouds.
2.	Not all models or model versions available in commercial / public cloud will be available in government clouds.
3.	In the Azure Government clouds, we intend to support only one version of a given model at a time.
    1. For example only one version of `gpt-35-turbo 0125` and `gpt-4o (2024-05-13)`.
4.	There will however be a 30 day overlap between new model versions, where more than two will be available.
    1. For example if `gpt-35-turbo 0125` or `gpt-4o (2024-05-13)` is updated to a future version, or
    2. for model family changes beyond version updates, such as when moving from `gpt-4 1106-preview` to `gpt-4o (2024-05-13)`. 

### Who is notified of upcoming retirements

Azure OpenAI notifies those who are members of the following roles for each subscription with a deployment of a model with an upcoming retirement.

* Owner
* Contributor
* Reader
* Monitoring contributor
* Monitoring reader

## How to get ready for model retirements and version upgrades

To prepare for model retirements and version upgrades, we recommend that customers test their applications with the new models and versions and evaluate their behavior. We also recommend that customers update their applications to use the new models and versions before the retirement date.

For more information on the model evaluation process, see the [Getting started with model evaluation guide](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880).

For information on the model upgrade process, see [How to upgrade to a new model or version](./model-versions.md).

## Current models

> [!NOTE]
> Not all models go through a deprecation period prior to retirement. Some models/versions only have a retirement date.
>
> **Fine-tuned models** are subject to the same deprecation and retirement schedule as their equivalent base model.

These models are currently available for use in Azure OpenAI Service.

| Model | Version | Retirement date | Suggested replacements |
| ---- | ---- | ---- | --- |
| `babbage-002` | 1 | Retirement Date: January 27, 2025 | |
| `davinci-002` | 1 | Retirement Date: January 27, 2025 | |
| `dall-e-2`| 2 | January 27, 2025 | `dalle-3` |
| `dall-e-3` | 3 | No earlier than April 30, 2025 | |
| `gpt-35-turbo` | 0301 | February 13, 2025<br><br> Deployments set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on January 13, 2025.   | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |
| `gpt-35-turbo`<br>`gpt-35-turbo-16k` | 0613 | February 13, 2025 <br><br> Deployments set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on January 13, 2025.  | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`|
| `gpt-35-turbo` | 1106 | No earlier than March 31, 2025 <br><br> Deployments set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on January 13, 2025. | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini` |
| `gpt-35-turbo` | 0125 | No earlier than March 31, 2025 | `gpt-4o-mini` |
| `gpt-4`<br>`gpt-4-32k` | 0314 | June 6, 2025 | `gpt-4o` |
| `gpt-4`<br>`gpt-4-32k` | 0613 | June 6, 2025 | `gpt-4o` |
| `gpt-4` | 1106-preview | To be upgraded to `gpt-4` version: `turbo-2024-04-09`, starting no sooner than January 27, 2025 **<sup>1</sup>** | `gpt-4o`|
| `gpt-4` | 0125-preview |To be upgraded to `gpt-4` version: `turbo-2024-04-09`, starting no sooner than January 27, 2025 **<sup>1</sup>**  | `gpt-4o` |
| `gpt-4` | vision-preview | To be upgraded to `gpt-4` version: `turbo-2024-04-09`, starting no sooner than January 27, 2025  **<sup>1</sup>** | `gpt-4o`|
| `gpt-4o` | 2024-05-13 | No earlier than May 20, 2025 <br><br>Deployments set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `2024-08-06`, starting on February 13, 2025. | |
| `gpt-4o-mini` | 2024-07-18 | No earlier than July 18, 2025  | |
| `gpt-3.5-turbo-instruct` | 0914 | No earlier than February 1, 2025 |  |
| `text-embedding-ada-002` | 2 | No earlier than April 3, 2025 | `text-embedding-3-small` or `text-embedding-3-large` |
| `text-embedding-ada-002` | 1 | No earlier than April 3, 2025 | `text-embedding-3-small` or `text-embedding-3-large` |
| `text-embedding-3-small` | | No earlier than April 3, 2025 | |
| `text-embedding-3-large` | | No earlier than April 3, 2025 | |

 **<sup>1</sup>** We will notify all customers with these preview deployments at least 30 days before the start of the upgrades. We will publish an upgrade schedule detailing the order of regions and model versions that we will follow during the upgrades, and link to that schedule from here.

> [!IMPORTANT]
> Vision enhancements preview features including Optical Character Recognition (OCR), object grounding, video prompts will be retired and no longer available once `gpt-4` Version: `vision-preview` is upgraded to `turbo-2024-04-09`. If you are currently relying on any of these preview features, this automatic model upgrade will be a breaking change.

## Default model versions

| Model | Current default version | New default version | Default upgrade date |
|---|---|---|---|
| `gpt-35-turbo` | 0301 | 0125 | Deployments of versions `0301`, `0613`, and `1106` set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on January 13, 2025.|
|  `gpt-4o` | 2024-05-13 | 2024-08-06 | Deployments set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `2024-08-06`, starting on February 13, 2025. |

## Deprecated models

These models were deprecated on July 6, 2023 and were retired on June 14, 2024. These models are no longer available for new deployments. Deployments created before July 6, 2023 remain available to customers until June 14, 2024. We recommend customers migrate their applications to deployments of replacement models before the June 14, 2024 retirement.

If you're an existing customer looking for information about these models, see [Legacy models](./legacy-models.md).

| Model | Deprecation date | Retirement date | Suggested replacement |
| --------- | --------------------- | ------------------- | -------------------- |
| ada | July 6, 2023 | June 14, 2024 | babbage-002 |
| babbage | July 6, 2023 | June 14, 2024 | babbage-002 |
| curie | July 6, 2023 | June 14, 2024 | davinci-002 |
| davinci | July 6, 2023 | June 14, 2024 | davinci-002 |
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

## Retirement and deprecation history

## December 2, 2024

`gpt-3.5-turbo-instruct` updated to no earlier than February 1, 2025.

## November 22, 2024

`gpt-35-turbo` 1106 retirement date updated to no earlier than March 31, 2025.

## November 11, 2024

Updates to:

- `babbage-002`, `davinci-002`.
- `gpt-35-turbo` DEFAULT model version update date.
- `gpt-35-turbo` 0301, 0613 retirement date.
- `gpt-35-turbo` 0125 retirement date.
- `gpt-4o` DEFAULT model update date.
- `text-embeddings-3-small` & `text-embedding-3-large` retirement date.

## October 25, 2024

* `babbage-002` & `davinci-002` deprecation date: November 15, 2024  and retirement date: January 27, 2025.

## September 12, 2024

* `gpt-35-turbo` (0301), (0613), (1106) and `gpt-35-turbo-16k` (0613) auto-update to default upgrade date updated to November 13, 2024.

## September 9, 2024

* `gpt-35-turbo` (0301) and (0613) retirement changed to January 27, 2025.
* `gpt-4` preview model upgrade date changed to starting no sooner than January 27, 2025.

## September 3, 2024

* Updated tables to include information on `gpt-35-turbo` default version upgrades. Deployments of versions `0301`, `0613`, and `1106` set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on November 15, 2024.|

### August 22, 2024

* Updated `gpt-35-turbo` (0301) retirement date to no earlier than November 1, 2024.
* Updated `gpt4` and `gpt-4-32k` (0314 and 0613) deprecation date to November 1, 2024.

### August 8, 2024

* Updated `gpt-35-turbo` & `gpt-35-turbo-16k` (0613) model's retirement date to November 1, 2024.

### July 30, 2024

* Updated `gpt-4` preview model upgrade date to November 15, 2024 or later for the following versions:
  * 1106-preview
  * 0125-preview
  * vision-preview (Vision enhancements feature will no longer be supported once this model is retired/upgraded.)

### July 18, 2024

* Updated `gpt-4` 0613  deprecation date to October 1, 2024 and the retirement date to June 6, 2025.

### June 19, 2024

* Updated `gpt-35-turbo` 0301 retirement date to no earlier than October 1, 2024.
* Updated `gpt-35-turbo` & `gpt-35-turbo-16k`0613 retirement date to October 1, 2024.
* Updated `gpt-4` & `gpt-4-32k` 0314 deprecation date to October 1, 2024, and retirement date to June 6, 2025.  

### June 4, 2024

Retirement date for legacy models updated by one month.

### April 24, 2024

Earliest retirement date for `gpt-35-turbo` 0301 and 0613 has been updated to August 1, 2024.

### March 13, 2024

We published this document to provide information about the current models, deprecated models, and upcoming retirements.

### February 23, 2024

We announced the upcoming in-place upgrade of `gpt-4` version `1106-preview` to `0125-preview` to start no earlier than March 8, 2024.

### November 30, 2023

The default version of `gpt-4` and `gpt-3-32k` was updated from `0314` to `0613` starting on November 30, 2023. The upgrade of `0314` deployments set for autoupgrade to `0613` was completed on December 3, 2023.

### July 6, 2023

We announced the deprecation of models with upcoming retirement on July 5, 2024.
