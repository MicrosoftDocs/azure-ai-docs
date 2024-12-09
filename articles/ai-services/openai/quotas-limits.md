---
title: Azure OpenAI Service quotas and limits
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices on the quotas and limits for the OpenAI service in Azure AI services.
#services: cognitive-services
author: mrbullwinkle
manager: nitinme
ms.service: azure-ai-openai
ms.custom:
  - ignite-2023
  - references_regions
ms.topic: conceptual
ms.date: 11/11/2024
ms.author: mbullwin
---

# Azure OpenAI Service quotas and limits

This article contains a quick reference and a detailed description of the quotas and limits for Azure OpenAI in Azure AI services.

## Quotas and limits reference

The following sections provide you with a quick guide to the default quotas and limits that apply to Azure OpenAI:

| Limit Name | Limit Value |
|--|--|
| Azure OpenAI resources per region per Azure subscription | 30 |
| Default DALL-E 2 quota limits | 2 concurrent requests |
| Default DALL-E 3 quota limits| 2 capacity units (6 requests per minute)|
| Default Whisper quota limits | 3 requests per minute |
| Maximum prompt tokens per request | Varies per model. For more information, see [Azure OpenAI Service models](./concepts/models.md)|
| Max Standard deployments per resource | 32 |
| Max fine-tuned model deployments | 5 |
| Total number of training jobs per resource | 100 |
| Max simultaneous running training jobs per resource | 1 |
| Max training jobs queued | 20 |
| Max Files per resource (fine-tuning) | 50 |
| Total size of all files per resource (fine-tuning) | 1 GB |
| Max training job time (job will fail if exceeded) | 720 hours |
| Max training job size (tokens in training file) x (# of epochs) | 2 Billion |
| Max size of all files per upload (Azure OpenAI on your data) | 16 MB |
| Max number or inputs in array with `/embeddings` | 2048 |
| Max number of `/chat/completions` messages | 2048 |
| Max number of `/chat/completions` functions | 128 |
| Max number of `/chat completions` tools | 128 |
| Maximum number of Provisioned throughput units per deployment | 100,000 |
| Max files per Assistant/thread | 10,000 when using the API or Azure AI Foundry portal. In Azure OpenAI Studio the limit was 20.|
| Max file size for Assistants & fine-tuning | 512 MB<br/><br/>200 MB via Azure AI Foundry portal |
| Max size for all uploaded files for Assistants |100 GB |
| Assistants token limit | 2,000,000 token limit |
| GPT-4o max images per request (# of images in the messages array/conversation history) | 50 |
| GPT-4 `vision-preview` & GPT-4 `turbo-2024-04-09` default max tokens | 16 <br><br> Increase the `max_tokens` parameter value to avoid truncated responses. GPT-4o max tokens defaults to 4096. |
| Max number of custom headers in API requests<sup>1</sup> | 10 |
| Max number requests per minute<br/><br/>Current rate limits for real time audio (`gpt-4o-realtime-preview`) are defined as the number of new websocket connections per minute. For example, 100 requests per minute (RPM) means 100 new connections per minute. | 100 new connections per minute |

<sup>1</sup> Our current APIs allow up to 10 custom headers, which are passed through the pipeline, and returned. Some customers now exceed this header count resulting in HTTP 431 errors. There's no solution for this error, other than to reduce header volume. **In future API versions we will no longer pass through custom headers**. We recommend customers not depend on custom headers in future system architectures.

## Regional quota limits

[!INCLUDE [Quota](./includes/model-matrix/quota.md)]

[!INCLUDE [Quota](./includes/global-batch-limits.md)]

## o1-preview & o1-mini rate limits

> [!IMPORTANT]
> The ratio of RPM/TPM for quota with o1-series models works differently than older chat completions models:
>
> - **Older chat models:** 1 unit of capacity = 6 RPM and 1,000 TPM.
> - **o1-preview:** 1 unit of capacity = 1 RPM and 6,000 TPM.
> - **o1-mini:** 1 unit of capacity = 1 RPM per 10,000 TPM.
>
> This is particularly important for programmatic model deployment as this change in RPM/TPM ratio can result in accidental under allocation of quota if one is still assuming the 1:1000 ratio followed by older chat completion models.
>
> There is a known issue with the [quota/usages API](/rest/api/aiservices/accountmanagement/usages/list?view=rest-aiservices-accountmanagement-2024-06-01-preview&tabs=HTTP&preserve-view=true) where it assumes the old ratio applies to the new o1-series models. The API returns the correct base capacity number, but does not apply the correct ratio for the accurate calculation of TPM.

### o1-preview & o1-mini global standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `o1-preview` | Enterprise agreement | 30 M | 5 K |
| `o1-mini`| Enterprise agreement | 50 M | 5 K |
| `o1-preview` | Default | 3 M | 500 |
| `o1-mini`| Default | 5 M | 500 |

### o1-preview & o1-mini standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `o1-preview` | Enterprise agreement | 600 K | 100 |
| `o1-mini`| Enterprise agreement |  1 M | 100 |
| `o1-preview` | Default | 300 K | 50 |
| `o1-mini`| Default | 500 K | 50 |

## gpt-4o & GPT-4 Turbo rate limits

`gpt-4o` and `gpt-4o-mini`, and `gpt-4` (`turbo-2024-04-09`) have rate limit tiers with higher limits for certain customer types.

### gpt-4o & GPT-4 Turbo global standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o`|Enterprise agreement | 30 M | 180 K |
|`gpt-4o-mini` | Enterprise agreement | 50 M | 300 K |
|`gpt-4` (turbo-2024-04-09) | Enterprise agreement | 2 M | 12 K |
|`gpt-4o` |Default | 450 K | 2.7 K |
|`gpt-4o-mini` | Default | 2 M | 12 K  |
|`gpt-4` (turbo-2024-04-09) | Default | 450 K | 2.7 K |

M = million | K = thousand

### gpt-4o data zone standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o`|Enterprise agreement | 10 M | 60 K |
|`gpt-4o-mini` | Enterprise agreement | 20 M | 120 K |
|`gpt-4o` |Default | 300 K | 1.8 K |
|`gpt-4o-mini` | Default | 1 M | 6 K  |

M = million | K = thousand


### gpt-4o standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o`|Enterprise agreement | 1 M | 6 K |
|`gpt-4o-mini` | Enterprise agreement | 2 M | 12 K |
|`gpt-4o`|Default | 150 K | 900 |
|`gpt-4o-mini` | Default | 450 K | 2.7 K |

M = million | K = thousand

#### Usage tiers

Global standard deployments use Azure's global infrastructure, dynamically routing customer traffic to the data center with best availability for the customer’s inference requests. Similarly, Data zone standard deployments allow you to leverage Azure global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. This enables more consistent latency for customers with low to medium levels of traffic. Customers with high sustained levels of usage might see more variability in response latency.

The Usage Limit determines the level of usage above which customers might see larger variability in response latency. A customer’s usage is defined per model and is the total tokens consumed across all deployments in all subscriptions in all regions for a given tenant.

> [!NOTE]
> Usage tiers only apply to standard, data zone standard, and global standard deployment types. Usage tiers do not apply to global batch and provisioned throughput deployments.

#### GPT-4o global standard, data zone standard, & standard

|Model| Usage Tiers per month |
|----|----|
|`gpt-4o` | 12 Billion tokens |
|`gpt-4o-mini` | 85 Billion tokens |

#### GPT-4 standard

|Model| Usage Tiers per month|
|---|---|
| `gpt-4` + `gpt-4-32k`  (all versions) | 6 Billion |


## Other offer types

If your Azure subscription is linked to certain [offer types](https://azure.microsoft.com/support/legal/offer-details/) your max quota values are lower than the values indicated in the above tables.


|Tier| Quota Limit in tokens per minute (TPM) |
|---|:---|
|Azure for Students, Free Trials | 1 K (all models)|
| MSDN subscriptions | GPT 3.5 Turbo Series: 30 K <br> GPT-4 series: 8 K   |
| Monthly credit card based subscriptions <sup>1</sup> | GPT 3.5 Turbo Series: 30 K <br> GPT-4 series: 8 K  |

<sup>1</sup> This currently applies to [offer type 0003P](https://azure.microsoft.com/support/legal/offer-details/)

In the Azure portal you can view what offer type is associated with your subscription by navigating to your subscription and checking the subscriptions overview pane. Offer type corresponds to the plan field in the subscription overview.

### General best practices to remain within rate limits

To minimize issues related to rate limits, it's a good idea to use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

### How to request increases to the default quotas and limits

Quota increase requests can be submitted from the [Quotas](./how-to/quota.md) page in the Azure AI Foundry portal. Due to high demand, quota increase requests are being accepted and will be filled in the order they're received. Priority is given to customers who generate traffic that consumes the existing quota allocation, and your request might be denied if this condition isn't met.

For other rate limits, [submit a service request](../cognitive-services-support-options.md?context=/azure/ai-services/openai/context/context).

## Next steps

Explore how to [manage quota](./how-to/quota.md) for your Azure OpenAI deployments.
Learn more about the [underlying models that power Azure OpenAI](./concepts/models.md).
