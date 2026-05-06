---
title: "Manage Azure OpenAI in Microsoft Foundry Models quota (classic)"
description: "Learn how to use Azure OpenAI to control your deployments rate limits. (classic)"
author: alvinashcraft
ms.reviewer: shiyingfu
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 05/04/2026
ms.author: aashcraft
ms.custom: classic-and-new
#CustomerIntent: As a developer or AI practitioner, I want to understand how to manage Azure OpenAI deployment quotas in Microsoft Foundry so that I can control rate limits for my models.
ROBOTS: NOINDEX, NOFOLLOW
---

# Manage Azure OpenAI in Microsoft Foundry Models quota (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/quota.md)

[!INCLUDE [classic-links](../../includes/classic-links.md)]

[!INCLUDE [quota 1](../../../foundry/openai/includes/quota-1.md)]

## Assign quota

When you create a model deployment, you have the option to assign Tokens-Per-Minute (TPM) to that deployment. TPM can be modified in increments of 1,000, and will map to the TPM and RPM rate limits enforced on your deployment, as discussed above.

To create a new deployment from within the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) select **Deployments** > **Deploy model** > **Deploy base model** > **Select Model** > **Confirm**.

Post deployment you can adjust your TPM allocation by selecting and editing your model from the **Deployments** page in [Foundry portal](https://ai.azure.com/?cid=learnDocs). You can also modify this setting from the **Management** > **Model quota** page.

> [!IMPORTANT]
> Quotas and limits are subject to change, for the most up-date-information consult our [quotas and limits article](../quotas-limits.md).

## View and request quota

For an all up view of your quota allocations across deployments in a given region, select **Management** > **Quota** in [Foundry portal](https://ai.azure.com/?cid=learnDocs):

- **Deployment**: Model deployments divided by model class.
- **Quota type**: There's one quota value per region for each model type. The quota covers all versions of that model.  
- **Quota allocation**: For the quota name, this shows how much quota is used by deployments and the total quota approved for this subscription and region. This amount of quota used is also represented in the bar graph.
- **Request Quota**: The icon navigates to [this form](https://aka.ms/oai/stuquotarequest) where requests to increase quota can be submitted.

[!INCLUDE [quota 2](../../../foundry/openai/includes/quota-2.md)]
