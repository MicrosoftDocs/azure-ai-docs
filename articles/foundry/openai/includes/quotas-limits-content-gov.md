---
title: include file
description: include file
author: challenp
ms.author: challenp
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/24/2026
ms.custom: include, classic-and-new
---

This article provides a quick reference and a detailed description of the quotas and limits for Azure OpenAI in Azure Government.

## Scope of quota

Azure Government doesn't enforce quotas and limits at the tenant level. Instead, it enforces the highest level of quota restrictions at the Azure subscription level.

## Regional quota allocation

Tokens per minute (TPM) and requests per minute (RPM) limits are defined *per region*, *per subscription*, and *per model or deployment type*.

For example, if the `gpt-4.1` DataZone Standard model has a quota of *5 million TPM* and *5,000 RPM*, then *each region* where that [model or deployment type is available](../../foundry-models/concepts/models-sold-directly-by-azure-gov.md) has its own dedicated quota pool of that amount for *each* of your Azure subscriptions. Within a single Azure subscription, you can use a larger quantity of total TPM and RPM quota for a given model and deployment type, as long as you spread resources and model deployments across multiple regions.

### Quota tiers

In Azure Government, the service doesn't support quota tiers or automatic adjustments to quota. Instead, it provides two levels: a default level and an enterprise level for customers with an Enterprise Agreement. 

### Can I request more quota?

Yes, use the [Azure Gov Quota Request Form](https://aka.ms/AOAIGovQuota) to request more quota. If the request is approved, the current tier stays the same, but you get more quota.  

### Azure Government quota reference

# [DataZone Standard](#tab/default)

[!INCLUDE [Quota](quota-tier/gov-dzstd.md)]

# [Standard](#tab/standard)

[!INCLUDE [Quota](quota-tier/gov-std.md)]

---

### General best practices to stay within rate limits

To minimize problems related to rate limits, use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

## Regional quota capacity limits

You can view quota availability by region for your subscription in the [Foundry portal](https://ai.azure.us/resource/quota).

To view quota capacity by region for a specific model or version, query the [capacity API](/rest/api/aiservices/accountmanagement/model-capacities/list) for your subscription. Provide a `subscriptionId`, `model_name`, and `model_version`. The API returns the available capacity for that model across all regions and deployment types for your subscription.

> [!NOTE]
> Currently, both the Foundry portal and the capacity API return quota and capacity information for models that are [retired](../concepts/model-retirements.md) and no longer available.

## Related content

- Explore how to [manage quota](../../../foundry-classic/openai/how-to/quota.md) for your Azure OpenAI deployments.
- Learn more about the [underlying models that power Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure-gov.md).
