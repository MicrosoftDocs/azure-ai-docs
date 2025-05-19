---
title: Azure AI Foundry Models quotas and limits
titleSuffix: Azure AI Foundry
description: Quick reference, detailed description, and best practices on the quotas and limits for the Azure AI Foundry service.
author: santiagxf
manager: nitinme
ms.service: azure-ai-model-inference
ms.custom: ignite-2024, github-universe-2024
ms.topic: conceptual
ms.date: 1/21/2025
ms.author: fasantia
---

# Azure AI Foundry Models quotas and limits

This article contains a quick reference and a detailed description of the quotas and limits for Azure AI Foundry Models. For quotas and limits specific to the Azure OpenAI in Foundry Models, see [Quota and limits in Azure OpenAI](../../ai-services/openai/quotas-limits.md).

## Quotas and limits reference

Azure uses quotas and limits to prevent budget overruns due to fraud, and to honor Azure capacity constraints. Consider these limits as you scale for production workloads. The following sections provide you with a quick guide to the default quotas and limits that apply to Azure AI model's inference service in Azure AI services:

### Resource limits

| Limit name | Limit value |
|--|--|
| Azure AI services resources per region per Azure subscription | 30 |
| Max deployments per resource | 32 | 

### Rate limits

| Limit name           | Applies to          | Limit value |
| -------------------- | ------------------- | ----------- |
| Tokens per minute    | Azure OpenAI models | Varies per model and SKU. See [limits for Azure OpenAI](../../ai-services/openai/quotas-limits.md). |
| Requests per minute  | Azure OpenAI models | Varies per model and SKU. See [limits for Azure OpenAI](../../ai-services/openai/quotas-limits.md). |
| Tokens per minute    | DeepSeek-R1<br />DeepSeek-V3-0324         | 5,000,000 |
| Requests per minute  | DeepSeek-R1<br />DeepSeek-V3-0324         | 5,000     |
| Concurrent requests  | DeepSeek-R1<br />DeepSeek-V3-0324         | 300       |
| Tokens per minute    | Rest of models      | 400,000   |
| Requests per minute  | Rest of models      | 1,000     |
| Concurrent requests  | Rest of models      | 300       |

You can [request increases to the default limits](#request-increases-to-the-default-limits). Due to high demand, limit increase requests can be submitted and evaluated per request.

### Other limits

| Limit name | Limit value |
|--|--|
| Max number of custom headers in API requests<sup>1</sup> | 10 |

<sup>1</sup> Our current APIs allow up to 10 custom headers, which are passed through the pipeline, and returned. We have noticed some customers now exceed this header count resulting in HTTP 431 errors. There is no solution for this error, other than to reduce header volume. **In future API versions we will no longer pass through custom headers**. We recommend customers not depend on custom headers in future system architectures.

## Usage tiers

Global Standard deployments use Azure's global infrastructure, dynamically routing customer traffic to the data center with best availability for the customer's inference requests. This enables more consistent latency for customers with low to medium levels of traffic. Customers with high sustained levels of usage might see more variabilities in response latency.

The Usage Limit determines the level of usage above which customers might see larger variability in response latency. A customer's usage is defined per model and is the total tokens consumed across all deployments in all subscriptions in all regions for a given tenant.

## Request increases to the default limits

Limit increase requests can be submitted and evaluated per request. [Open an online customer support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest/). When requesting for endpoint limit increase, provide the following information:

1. When opening the support request, select **Service and subscription limits (quotas)** as the **Issue type**.

1. Select the subscription of your choice.

1. Select **Cognitive Services** as **Quota type**.

1. Select **Next**.

1. On the **Additional details** tab, you need to provide detailed reasons for the limit increase in order for your request to be processed. Be sure to add the following information into the reason for limit increase:

   * Model name, model version (if applicable), and deployment type (SKU).
   * Description of your scenario and workload.
   * Rationale for the requested increase.
   * Provide the target throughput: Tokens per minute, requests per minute, etc.
   * Provide planned time plan (by when you need increased limits).

1. Finally, select **Save and continue** to continue.

## General best practices to remain within rate limits

To minimize issues related to rate limits, it's a good idea to use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

## Next steps

* Learn more about the [models available in Azure AI Foundry Models](./concepts/models.md)
