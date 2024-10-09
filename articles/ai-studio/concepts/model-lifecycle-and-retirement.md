---
title: Azure AI Studio model lifecycle and retirement
titleSuffix: Azure AI Studio
description: Learn about the lifecycle stages and retirement for models in Azure AI Studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: concept-article
ms.date: 10/08/2024
ms.custom: ignite-2024
ms.author: mopeakande
author: msakande
ms.reviewer: mabables
reviewer: ManojBableshwar

---

# Azure AI Studio model lifecycle and retirement

Models that are available in Azure AI Studio through the model catalog are continually refreshed with newer and more capable models. As part of this process, models can move through stages as we deprecate and retire older models. This document provides information about the models, their stages, and what the models stages mean for you as a customer.

Every models in the model catalog belongs to one of these stages:

- Preview
- General availability
- Legacy
- Deprecated
- Retired

## Preview 

New models are launched in preview stage if model weights, such as quantized or optimized weights, or APIs such as tool support will change in the future. This stage is optional, as new models can be launched in the general availability stage. For a model in the preview stage:

- The model page in AI Studio includes a _Preview_ tag.
- The model info API returns _Preview_.

## General availability

General availability (GA) is the default model stage. A model can be launched in the GA stage without going through preview if there are no plans to upgrade its weights or APIs. Once the model is GA, no breaking changes, such as API changes or weight updates are allowed. However, container updates that address security or vulnerability issues are allowed, provided that they don't change model quality or outputs. The only way to improve this model is by providing a new model and deprecating the existing model. For a model in the GA stage:

- The model page in AI Studio doesn't have a preview tag.
- The model info API returns _GA_.
 
## Legacy

A model in the legacy stage (or soft deprecation stage) is on the path for deprecation because a new is available that provides better quality, performance, or price. We encourage you to start trying the new model, but you can still create new deployments and fine-tuned versions of the legacy model.  For a model in the legacy stage:

- The model page in AI Studio includes a _Legacy_ tag.
- The model info API returns _Legacy_.
- Documentation pages for the model and email notifications provide information about suggested new model to use, legacy date, planned deprecation date, and planned retirement date.

## Deprecated

Once a model is deprecated, you can't create new deployments for the model, you can't submit finetuning jobs, and you can't deploy a finetuned version of the model. However, existing deployments and fine-tuned endpoints will continue to work until the model is retired. For a deprecated model:

- The model page in AI Studio includes a _Deprecated_ tag.
- The model info API returns _Deprecated_.
- Documentation pages for the model and email notifications provide information about suggested new model to use, legacy date, deprecation date, and planned retirement date.

## Retired

Once a model is retired, existing deployments — both the base model and inference — stop working. For a retired model:

- The model page in AI Studio includes a _Retired_ tag.
- The model info API returns no longer works.
- Documentation pages for the model and email notifications provide information about suggested new model to use, legacy date, deprecation date, and retirement date.


-----------------------------------


## Notifications


## Model availability


### Considerations for the Azure public cloud


### Special considerations for Azure Government clouds


### Who is notified of upcoming retirements


## How to get ready for model retirements and version upgrades


## Current models

for a list of models that are currently available for use in Azure AI Studio, see [Model deployment: Managed compute and serverless API (pay-as-you-go)](../how-to/model-catalog-overview.md#model-deployment-managed-compute-and-serverless-api-pay-as-you-go).

| Model | Version | Retirement date | Suggested replacements |
| ---- | ---- | ---- | --- |
| `<model>`| 2 | January 27, 2025 | `<replacement>` |



## Default model versions



## Deprecated models



## Retirement and deprecation history




