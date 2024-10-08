---
title: Azure AI Studio model stages and retirement
titleSuffix: Azure AI Studio
description: Learn about the model stages and retirement in Azure AI Studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: concept-article
ms.date: 10/08/2024
ms.custom: ignite-2024
author: mopeakande
ms.author: msakande
ms.reviewer: mabables
reviewer: ManojBableshwar

---

# Azure AI Studio model stages and retirement

Models that are available in Azure AI Studio through the model catalog are continually refreshed with newer and more capable models. As part of this process, models can move through stages as we deprecate and retire older models. This document provides information about the models, their stages, and what the models stages mean for you as a customer.

Every models in the model catalog belongs to one of these stages:

- Preview
- General availability
- Legacy
- Deprecated
- Retired

## Preview 

New models are launched in preview stage if model weights, such as quantized or optimized weights, or APIs such as tool support will change in the future. This stage is optional, as new models can be launched in the general availability stage. For a model in the preview stage:

- The model page in the Studio includes a _Preview_ tag
- The model info API returns _Preview_

## General availability

General availability (GA) is the default model stage. A model can be launched in the GA stage without going through preview if there are no plans to upgrade its weights or APIs. Once the model is GA, no breaking changes, such as API changes or weight updates are allowed. However, container updates that address security or vulnerability issues are allowed, provided that they don't change model quality or outputs. The only way to improve this model is by providing a new model and deprecating the existing model. For a model in the GA stage:

- The model page in the Studio doesn't have a preview tag
- The model info API returns _GA_
 
## Legacy

A model in the legacy stage (or soft deprecation stage) is on the path for deprecation because a new is available that provides better quality, performance, or price. We encourage you to start trying the new model, but you can still create new deployments and fine-tuned versions of the legacy model.  For a model in the legacy stage:

- The model page in the Studio includes a _Legacy_ tag
- The model info API returns _Legacy_
- Documentation pages for the model and email notifications provide information about suggested new model to use, legacy date, planned deprecation date, and planned retirement date

## Deprecated

Once a model is deprecated, you can't create new deployments for the model, you can't submit finetuning jobs, and you can't deploy a finetuned version of the model. However, existing deployments and fine-tuned endpoints will continue to work until the model is retired. For a deprecated model:

- The model page in the Studio includes a _Deprecated_ tag
- The model info API returns _Deprecated_
- Documentation pages for the model and email notifications provide information about suggested new model to use, legacy date, deprecation date, and planned retirement date

## Retired

Once a model is retired, existing deployments — both the base model and inference — stop working. For a retired model:

- The model page in the Studio includes a _Retired_ tag
- The model info API returns no longer works
- Documentation pages for the model and email notifications provide information about suggested new model to use, legacy date, deprecation date, and retirement date


-----------------------------------


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
5.    We reserve the right to limit future customers using a particular region to balance service quality for existing customers.
6.    As always at Microsoft, security is of the utmost importance. If a model or model version is found to have compliance or security issues, we reserve the right to invoke the need to do emergency retirements. See the terms of service for more information.

### Special considerations for Azure Government clouds

1.    Global standard deployments won't be available in government clouds.
2.    Not all models or model versions available in commercial / public cloud will be available in government clouds.
3.    In the Azure Government clouds, we intend to support only one version of a given model at a time.
    1. For example only one version of `gpt-35-turbo 0125` and `gpt-4o (2024-05-13)`.
4.    There will however be a 30 day overlap between new model versions, where more than two will be available.
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
| `dall-e-2`| 2 | January 27, 2025 | `dalle-3` |
| `dall-e-3` | 3 | No earlier than April 30, 2025 | |
| `gpt-35-turbo` | 0301 | January 27, 2025<br><br> Deployments set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on November 13, 2024.   | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |


 **<sup>1</sup>** We will notify all customers with these preview deployments at least 30 days before the start of the upgrades. We will publish an upgrade schedule detailing the order of regions and model versions that we will follow during the upgrades, and link to that schedule from here.



## Default model versions

| Model | Current default version | New default version | Default upgrade date |
|---|---|---|---|
| `gpt-35-turbo` | 0301 | 0125 | Deployments of versions `0301`, `0613`, and `1106` set to [**Auto-update to default**](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#auto-update-to-default) will be automatically upgraded to version: `0125`, starting on November 13, 2024.|



## Deprecated models

These models were deprecated on July 6, 2023 and were retired on June 14, 2024. These models are no longer available for new deployments. Deployments created before July 6, 2023 remain available to customers until June 14, 2024. We recommend customers migrate their applications to deployments of replacement models before the June 14, 2024 retirement.

If you're an existing customer looking for information about these models, see [Legacy models](./legacy-models.md).

| Model | Deprecation date | Retirement date | Suggested replacement |
| --------- | --------------------- | ------------------- | -------------------- |
| ada | July 6, 2023 | June 14, 2024 | babbage-002 |
| babbage | July 6, 2023 | June 14, 2024 | babbage-002 |
| curie | July 6, 2023 | June 14, 2024 | davinci-002 |
| davinci | July 6, 2023 | June 14, 2024 | davinci-002 |



## Retirement and deprecation history

## September 12, 2024

* `gpt-35-turbo` (0301), (0613), (1106) and `gpt-35-turbo-16k` (0613) auto-update to default upgrade date updated to November 13, 2024.

## September 9, 2024

* `gpt-35-turbo` (0301) and (0613) retirement changed to January 27, 2025.
* `gpt-4` preview model upgrade date changed to starting no sooner than January 27, 2025.


