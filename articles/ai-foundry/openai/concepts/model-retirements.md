---
title: Azure OpenAI in Microsoft Foundry Model Retirements
titleSuffix: Azure OpenAI
description: Learn about model deprecations and retirements in Azure OpenAI.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 01/30/2026
ms.custom: 
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin 
recommendations: false
---

# Azure OpenAI in Microsoft Foundry model deprecations and retirements

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI models are continually refreshed with newer and more capable models. As part of this process, we deprecate and retire older models. This article provides information about models that are currently available, deprecated, and retired.

## Model availability

For the availability of models, see the following information:

- Generally Available (GA) model versions will be available for a minimum of 12 months.
- After 12 months, existing customers may continue to use older model versions for an additional six months.
- New customers who have never deployed the older model version will no longer have access after 12 months.
- For global deployments, all future model versions starting with `gpt-4o` and `gpt-4 0409` will be available with their (`N`) next succeeding model (`N+1`) for comparison together.
- Customers have 60 days to try out a new GA model in at least one global or standard region before any upgrades happen to a newer GA model.

### Terminology

- **Deprecation**: When a model is deprecated, it's no longer available for new customers. It continues to be available for use by customers who have existing deployments until the model is retired.
- **Retirement**: When a model is retired, it's no longer available for use. Azure OpenAI deployments of a retired model always return error responses.

## Notifications

Azure OpenAI notifies customers of active Azure OpenAI deployments for models with upcoming retirements. We notify customers of upcoming retirements for each deployment in the following ways:

- We notify customers at model launch by programmatically designating a *not sooner than* retirement date. For preview models, it's 90-120 days from launch. For generally available (GA) models, it's 365 days from launch.
- We provide customers with at least 60 days' notice before model retirement for GA models.
- We provide customers with least 30 days' notice before preview model version upgrades.

Retirements are done on a rolling basis, region by region. There's no schedule for when a specific region or SKU is upgraded.

### Notifications of upcoming retirements

Azure OpenAI notifies customers via two methods:

- **Azure Resource Health**: Anyone with **reader** permissions or higher can see Azure health alerts and configure personalized alerts via email and SMS. See [Create Service Health alerts](/azure/service-health/alerts-activity-log-service-notifications-portal).
- **Email**: Email notifications are automatically sent to subscription owners. However, any individual with **reader** permissions can configure their own alerts by following the previous guidance.

#### Azure Service Health filter configuration

The service is `azure OpenAI service`. (The casing reflects the current UX experience.)

Event types include:

- `Health advisories = Upgrade, Deprecation, & Retirement Notifications`.
- `Service issue = Outages`. (We recommend this event type only if you want to be notified of outages.)

If you want to receive SMS text-based alerts versus just emails, select **Create action group**. Then, under **Notification type**, select **Email/SMS message/Push/Voice** and configure your phone number.

### Considerations for Azure public cloud

Be aware of the following information:

- Not all model version combinations will be available in all regions.
- Model version `N` and `N+1` might not always be available in the same region.
- A GA model version `N` might upgrade to a future model version `N+X` in some regions based on capacity limitations, and without the new model version `N+X` separately being available to test in the same region. The new model version will be available to test in other regions before any upgrades are scheduled.
- Preview model versions and GA versions of the same model won't always be available to test together in the same region. There will be preview and GA versions available to test in different regions.
- We reserve the right to limit future customers' use of a particular region to balance service quality for existing customers.
- As always at Microsoft, security is of the utmost importance. If a model or model version is found to have compliance or security issues, we reserve the right to invoke the need to do emergency retirements. Refer to the terms of service for more information.

### Special considerations for Azure Government clouds

- Global standard deployments aren't available in government clouds.
- Not all models or model versions available in commercial and public clouds will be available in government clouds.
- In Azure Government clouds, we intend to support only one version of a given model at a time. For example, only one version of `gpt-35-turbo 0125` and `gpt-4o (2024-05-13)`.
- However, there's a 30-day overlap between new model versions, when more than two will be available. For example, if `gpt-35-turbo 0125` or `gpt-4o (2024-05-13)` is updated to a future version. Another example is model family changes beyond version updates, like when moving from `gpt-4 1106-preview` to `gpt-4o (2024-05-13)`.

## Preparation for model retirements and version upgrades

To prepare for model retirements and version upgrades, we recommend that customers test their applications with the new models and versions and evaluate their behavior. We also recommend that customers update their applications to use the new models and versions before the retirement date.

For more information on the model evaluation process, see the [Getting started with model evaluation](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880) blog post.

For information on the model upgrade process, see [How to upgrade to a new model or version](./model-versions.md).

For more information on how to manage model upgrades and migrations for provisioned deployments, see [Managing models on provisioned deployment types](../how-to/working-with-models.md#managing-models-on-provisioned-deployment-types).

## Current models

> [!NOTE]
> Not all models go through a deprecation period before retirement. Some models or versions only have a retirement date.
>
> Fine-tuned models are subject to a [different](#fine-tuned-models) deprecation and retirement schedule from their equivalent base model.

These models are currently available for use in Azure OpenAI.

[!INCLUDE [Model retirement table](../includes/retirement/models.md)]

## Retirement and deprecation history

To track individual updates to this article, refer to the [Git history](https://github.com/MicrosoftDocs/azure-ai-docs/commits/main/articles/ai-foundry/openai/includes/retirement/models.md).

For a list of retired models, refer to the [retired models page](./legacy-models.md).
