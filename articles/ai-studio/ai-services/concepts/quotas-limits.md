---
title: Azure AI model inference quotas and limits
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices on the quotas and limits for the Azure AI models service in Azure AI services.
ms.service: azure-ai-studio
ms.custom: ignite-2024, github-universe-2024
ms.topic: conceptual
ms.date: 10/21/2024
author: sdgilley
manager: scottpolly
ms.date: 10/24/2024
ms.author: sgilley
ms.reviewer: fasantia
---

# Azure AI model inference quotas and limits

This article contains a quick reference and a detailed description of the quotas and limits for Azure AI model's inference in Azure AI services. For quotas and limits specific to the Azure OpenAI Service, see [Quota and limits in the Azure OpenAI service](../../../ai-services/openai/quotas-limits.md).

## Quotas and limits reference

The following sections provide you with a quick guide to the default quotas and limits that apply to Azure AI model's inference service in Azure AI services:

### Resource limits

| Limit name | Limit value |
|--|--|
| Azure AI Services resources per region per Azure subscription | 30 |
| Max model deployments per resource | 32 | 

### Rate limits

| Limit name | Limit value |
| ---------- | ----------- |
| Tokens per minute (Azure OpenAI models)   | Varies per model and SKU. See [limits for Azure OpenAI](../../../ai-services/openai/quotas-limits.md). |
| Tokens per minute (rest of models)        | 200.000 |
| Requests per minute (Azure OpenAI models) | Varies per model and SKU. See [limits for Azure OpenAI](../../../ai-services/openai/quotas-limits.md). |
| Requests per minute (rest of models)      | 1.000   |

### Other limits

| Limit name | Limit value |
|--|--|
| Max number of custom headers in API requests<sup>1</sup> | 10 |

<sup>1</sup> Our current APIs allow up to 10 custom headers, which are passed through the pipeline, and returned. We have noticed some customers now exceed this header count resulting in HTTP 431 errors. There is no solution for this error, other than to reduce header volume. **In future API versions we will no longer pass through custom headers**. We recommend customers not depend on custom headers in future system architectures.

## Usage tiers

Global Standard deployments use Azure's global infrastructure, dynamically routing customer traffic to the data center with best availability for the customer’s inference requests. This enables more consistent latency for customers with low to medium levels of traffic. Customers with high sustained levels of usage might see more variability in response latency.

The Usage Limit determines the level of usage above which customers might see larger variability in response latency. A customer’s usage is defined per model and is the total tokens consumed across all deployments in all subscriptions in all regions for a given tenant.

## General best practices to remain within rate limits

To minimize issues related to rate limits, it's a good idea to use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

### Request increases to the default quotas and limits

Quota increase requests can be submitted and evaluated per request. [Submit a service request](../../../ai-services/cognitive-services-support-options.md?context=/azure/ai-studio/context/context).

## Next steps

* Learn more about the [Azure AI model inference service](../model-inference.md)