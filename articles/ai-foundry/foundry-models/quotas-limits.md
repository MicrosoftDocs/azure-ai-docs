---
title: Microsoft Foundry Models quotas and limits
titleSuffix: Microsoft Foundry
description: Quick reference, detailed description, and best practices on the quotas and limits for the Microsoft Foundry service.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: msakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom: ignite-2024, github-universe-2024
ms.topic: concept-article
ms.date: 12/04/2025
ms.author: mopeakande
ms.reviewer: haakar
reviewer: haakar
---

# Microsoft Foundry Models quotas and limits

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article provides a quick reference and detailed description of the quotas and limits for [Foundry Models sold directly by Azure](concepts/models-sold-directly-by-azure.md). For quotas and limits specific to the Azure OpenAI in Foundry Models, see [Quotas and limits in Azure OpenAI](../openai/quotas-limits.md).

## Quotas and limits reference

Azure uses quotas and limits to prevent budget overruns due to fraud and to honor Azure capacity constraints. Consider these limits as you scale for production workloads. The following sections provide a quick guide to the default quotas and limits that apply to Azure AI model inference service in Foundry:

### Resource limits (per Azure subscription, per region)

| Limit name | Limit value |
|--|--|
| Foundry resources per region per Azure subscription | 100 |
| Max projects per resource | 250 |
| Max deployments per resource (model deployments within a Foundry resource) | 32 | 

### Rate limits

The following table lists limits for Foundry Models for the following rates:

- Tokens per minute
- Requests per minute
- Concurrent request

| Models                                                                 | Tokens per minute                                   | Requests per minute                                   | Concurrent requests   |
| ---------------------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------- | -------------------- |
| Azure OpenAI models                                                    | Varies per model and SKU. See [limits for Azure OpenAI](../openai/quotas-limits.md). | Varies per model and SKU. See [limits for Azure OpenAI](../openai/quotas-limits.md). | not applicable       |
| - DeepSeek-R1<br />- DeepSeek-V3-0324                                      | 5,000,000                                           | 5,000                                                 | 300                  |
| - Llama 3.3 70B Instruct<br />- Llama-4-Maverick-17B-128E-Instruct-FP8<br />- Grok 3<br />- Grok 3 mini | 400,000                                             | 1,000                                                 | 300                  |
| - Flux.2-Pro                                  | not applicable                                      | - Low (Default): 15 <br> - Medium: 30 <br> - High (Enterprise): 100              | not applicable       |
|- Flux-Pro 1.1 <br />- Flux.1-Kontext Pro                                  | not applicable                                      | 2 capacity units (6 requests per minute)              | not applicable       |
| Rest of models                                                         | 400,000                                             | 1,000                                                 | 300                  |

To increase your quota:

- For Azure OpenAI, use [Foundry Service: Request for Quota Increase](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu) to submit your request. 
- For other models, see [request increases to the default limits](#request-increases-to-the-default-limits). 
 
Due to high demand, we evaluate limit increase requests per request.

### Other limits

| Limit name | Limit value |
|--|--|
| Max number of custom headers in API requests<sup>1</sup> | 10 |

<sup>1</sup> Our current APIs allow up to 10 custom headers, which the pipeline passes through and returns. If you exceed this header count, your request results in an HTTP 431 error. To resolve this error, reduce the header volume. **Future API versions won't pass through custom headers**. We recommend that you don't depend on custom headers in future system architectures.

## Usage tiers

Global Standard deployments use Azure's global infrastructure to dynamically route customer traffic to the data center with best availability for the customer's inference requests. This infrastructure enables more consistent latency for customers with low to medium levels of traffic. Customers with high sustained levels of usage might see more variabilities in response latency.

The Usage Limit determines the level of usage above which customers might see larger variability in response latency. A customer's usage is defined per model and is the total tokens consumed across all deployments in all subscriptions in all regions for a given tenant.

## Request increases to the default limits

[!INCLUDE [quota-increase-request](../openai/includes/quota-increase-request.md)]

## General best practices to stay within rate limits

To minimize issues related to rate limits, use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

## Setting client side timeout

We recommend explicitly setting the client side timeout as follows.

> [!NOTE]
> If not explicitly set, the client side timeout exists as per the library used, and may not be the same limits as above.

- Reasoning models (models that generate intermediate reasoning tokens before producing a summarized response): up to 29 minutes. 
- Non-reasoning models: 
    - For streaming, up to 60 seconds.
    - For non-streaming requests, up to 29 minutes.
    
29 minutes here does not mean all requests will take 29 minutes but rather depending on context tokens, generated tokens, and cache hit rates, requests can take up to 29 minutes.

You will need to set a timeout less than the above tuned to your traffic patterns.

For reasoning models including streaming requests, all the reasoning tokens are first generated and then summarized before sending the first response token back to the user.

You can modify the [reasoning effort](../openai/how-to/reasoning.md) parameter to control the number of reasoning tokens generated in the process.

## Next steps

* Learn more about the [models available in Foundry Models](./concepts/models-sold-directly-by-azure.md)
