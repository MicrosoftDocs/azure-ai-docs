---
title: Azure OpenAI in Azure AI Foundry Models model retirements
titleSuffix: Azure OpenAI
description: Learn about the model deprecations and retirements in Azure OpenAI.
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 06/11/2025
ms.custom: 
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin 
recommendations: false
---

# Azure OpenAI in Azure AI Foundry Models model deprecations and retirements

## Overview

Azure OpenAI models are continually refreshed with newer and more capable models. As part of this process, we deprecate and retire older models. This document provides information about the models that are currently available, deprecated, and retired.

### Terminology

* Deprecation
	* When a model is deprecated, it's no longer available for new customers. It continues to be available for use by customers with existing deployments until the model is retired.
* Retirement
	* When a model is retired, it's no longer available for use. Azure OpenAI deployments of a retired model always return error responses.

## Notifications

Azure OpenAI notifies customers of active Azure OpenAI deployments for models with upcoming retirements. We notify customers of upcoming retirements as follows for each deployment:

1. At model launch, we programmatically designate a "not sooner than" retirement date (for preview models this is between 90-120 days from launch, for generally available (GA) models this is 365 days from launch).
2. At least 60 days notice before model retirement for Generally Available (GA) models.
3. At least 30 days notice before preview model version upgrades.

Retirements are done on a rolling basis, region by region. There is no schedule for when a specific region, or SKU will be upgraded.

### Who is notified of upcoming retirements

Azure OpenAI notifies customers via two methods:
- **Azure Resource Health** - Anyone with reader permissions or above can see Azure health alerts, as well as configure personalized alerts via email, SMS, etc. See [Create Service Health Alerts](/azure/service-health/alerts-activity-log-service-notifications-portal)
- **Email** - email notifications are automatically sent to subscription owners. Any individual with reader permissions may however configure their own alerts by following the guidance above.

**Azure Service Health filter configuration**:

**Services** = `azure OpenAI service` (Casing reflects current UX experience)
**Event types**
    - `Health advisories = Upgrade, Deprecation, & Retirement Notifications`
    - `Service issue = Outages` (Recommended only if you wish to be notified of outages)

If you wish to receive SMS text-based alerts rather than just e-mails, you will need to select **Create action group** and under **Notification type**, select **Email/SMS message/Push/Voice** and then configure your phone number.

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

## How to get ready for model retirements and version upgrades

To prepare for model retirements and version upgrades, we recommend that customers test their applications with the new models and versions and evaluate their behavior. We also recommend that customers update their applications to use the new models and versions before the retirement date.

For more information on the model evaluation process, see the [Getting started with model evaluation guide](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880).

For information on the model upgrade process, see [How to upgrade to a new model or version](./model-versions.md).

For more information on how to manage model upgrades and migrations for provisioned deployments, see [Managing models on provisioned deployment types](../how-to/working-with-models.md#managing-models-on-provisioned-deployment-types)

## Current models

> [!NOTE]
> Not all models go through a deprecation period prior to retirement. Some models/versions only have a retirement date.
>
> **Fine-tuned models** are subject to a [different](#fine-tuned-models) deprecation and retirement schedule from their equivalent base model.

These models are currently available for use in Azure OpenAI.

[!INCLUDE [Model retirement table](../includes/retirement/models.md)]

## Retirement and deprecation history

To track individual updates to this article refer to the [Git History](https://github.com/MicrosoftDocs/azure-ai-docs/commits/main/articles/ai-services/openai/includes/retirement/models.md)
