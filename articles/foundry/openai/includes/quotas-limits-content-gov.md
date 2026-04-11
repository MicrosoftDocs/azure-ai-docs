---
title: include file
description: include file
author: challenp
ms.author: challenp
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/03/2026
ms.custom: include, classic-and-new
---

This article contains a quick reference and a detailed description of the quotas and limits for Azure OpenAI in Azure Government.

## Scope of quota

Quotas and limits aren't enforced at the tenant level. Instead, the highest level of quota restrictions is scoped at the Azure subscription level.

## Regional quota allocation

Tokens per minute (TPM) and requests per minute (RPM) limits are defined *per region*, *per subscription*, and *per model or deployment type*.

For example, if the `gpt-4.1` DataZone Standard model is listed with a quota of *5 million TPM* and *5,000 RPM*, then *each region* where that [model or deployment type is available](../../foundry-models/concepts/models-sold-directly-by-azure-gov.md) has its own dedicated quota pool of that amount for *each* of your Azure subscriptions. Within a single Azure subscription, it's possible to use a larger quantity of total TPM and RPM quota for a given model and deployment type, as long as you have resources and model deployments spread across multiple regions.

### Quota tiers

In Azure Government, we don't support Quota Tiers or automatic adjustments to quota. Instead, we provide two levels including a Default level and an Enterprise level for customers with an Enterprise Agreement. 

### Can I request more quota?

Yes, using the [Azure Gov Quota Request Form](https://aka.ms/AOAIGovQuota) you can always request more quota. If the request is approved, the current tier will remain the same, but with more quota assigned.  

### Azure Government quota reference

# [DataZone Standard](#tab/default)

[!INCLUDE [Quota](quota-tier/gov-dzstd.md)]

# [Standard](#tab/standard)

[!INCLUDE [Quota](quota-tier/gov-std.md)]

### General best practices to remain within rate limits

To minimize issues related to rate limits, it's a good idea to use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

## Regional quota capacity limits

You can view quota availability by region for your subscription in the [Foundry portal](https://ai.azure.us/resource/quota).

To view quota capacity by region for a specific model or version, you can query the [capacity API](/rest/api/aiservices/accountmanagement/model-capacities/list) for your subscription. Provide a `subscriptionId`, `model_name`, and `model_version` and the API returns the available capacity for that model across all regions and deployment types for your subscription.

> [!NOTE]
> Currently, both the Foundry portal and the capacity API return quota/capacity information for models that are [retired](../concepts/model-retirements.md) and no longer available.

## Related content

- Explore how to [manage quota](../../../foundry-classic/openai/how-to/quota.md) for your Azure OpenAI deployments.
- Learn more about the [underlying models that power Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure-gov.md).
