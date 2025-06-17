---
title: Azure OpenAI in Azure AI Foundry Models quotas and limits
description: Quick reference, detailed description, and best practices on the quotas and limits for the OpenAI service in Azure AI services.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 05/29/2025
ms.service: azure-ai-openai
ms.topic: conceptual
ms.custom:
  - ignite-2023
  - references_regions
  - build-2025
---

# Azure OpenAI in Azure AI Foundry Models quotas and limits

This article contains a quick reference and a detailed description of the quotas and limits for Azure OpenAI.

## Quotas and limits reference

The following sections provide you with a quick guide to the default quotas and limits that apply to Azure OpenAI:

| Limit Name | Limit Value |
|--|--|
| Azure OpenAI resources per region per Azure subscription | 30 |
| Default DALL-E 2 quota limits | 2 concurrent requests |
| Default DALL-E 3 quota limits| 2 capacity units (6 requests per minute)|
| Default GPT-image-1 quota limits | 2 capacity units (6 requests per minute) |
| Default Sora quota limits | 60 requests per minute |
| Default speech to text audio API quota limits | 3 requests per minute |
| Maximum prompt tokens per request | Varies per model. For more information, see [Azure OpenAI models](./concepts/models.md)|
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
| Max files per Assistant/thread | 10,000 when using the API or [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).|
| Max file size for Assistants & fine-tuning | 512 MB<br/><br/>200 MB via [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) |
| Max size for all uploaded files for Assistants |200 GB |
| Assistants token limit | 2,000,000 token limit |
| GPT-4o and GPT-4.1 max images per request (# of images in the messages array/conversation history) | 50 |
| GPT-4 `vision-preview` & GPT-4 `turbo-2024-04-09` default max tokens | 16 <br><br> Increase the `max_tokens` parameter value to avoid truncated responses. GPT-4o max tokens defaults to 4096. |
| Max number of custom headers in API requests<sup>1</sup> | 10 |
| Message character limit | 1048576 |
| Message size for audio files | 20 MB |

<sup>1</sup> Our current APIs allow up to 10 custom headers, which are passed through the pipeline, and returned. Some customers now exceed this header count resulting in HTTP 431 errors. There's no solution for this error, other than to reduce header volume. **In future API versions we will no longer pass through custom headers**. We recommend customers not depend on custom headers in future system architectures.

> [!NOTE]
> Quota limits are subject to change. 

[!INCLUDE [Quota](./includes/global-batch-limits.md)]


## GPT-4 rate limits

### GPT-4.5 preview global standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `gpt-4.5` | Enterprise Tier | 200 K | 200 |
| `gpt-4.5` | Default | 150 K | 150 |

### GPT-4.1 series

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `gpt-4.1` (2025-04-14) | Enterprise Tier | 5 M | 5 K |
| `gpt-4.1` (2025-04-14) | Default | 1 M | 1 K |
| `gpt-4.1-nano` (2025-04-14) | Enterprise Tier | 5 M | 5 K |
| `gpt-4.1-nano` (2025-04-14) | Default | 1 M | 1 K |
| `gpt-4.1-mini` (2025-04-14) | Enterprise Tier | 5 M | 5 K |
| `gpt-4.1-mini` (2025-04-14) | Default | 1 M | 1 K |

### GPT-4 Turbo

`gpt-4` (`turbo-2024-04-09`) has rate limit tiers with higher limits for certain customer types.

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4` (turbo-2024-04-09) | Enterprise agreement | 2 M | 12 K |
|`gpt-4` (turbo-2024-04-09) | Default | 450 K | 2.7 K |

## model-router rate limits

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `model-router` (2025-05-19) | Enterprise Tier | 10 M | 10 K |
| `model-router` (2025-05-19) | Default         | 1 M | 1 K |


## computer-use-preview global standard rate limits

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `computer-use-preview`| Enterprise Tier | 30 M | 300 K |
| `computer-use-preview`| Default         | 450 K | 4.5 K |


## o-series rate limits

> [!IMPORTANT]
> The ratio of RPM/TPM for quota with o1-series models works differently than older chat completions models:
>
> - **Older chat models:** 1 unit of capacity = 6 RPM and 1,000 TPM.
> - **o1 & o1-preview:** 1 unit of capacity = 1 RPM and 6,000 TPM.
> - **o3** 1 unit of capacity = 1 RPM per 1,000 TPM
> - **o4-mini** 1 unit of capacity = 1 RPM per 1,000 TPM
> - **o3-mini:** 1 unit of capacity = 1 RPM per 10,000 TPM.
> - **o1-mini:** 1 unit of capacity = 1 RPM per 10,000 TPM.
>
> This is particularly important for programmatic model deployment as this change in RPM/TPM ratio can result in accidental under allocation of quota if one is still assuming the 1:1000 ratio followed by older chat completion models.
>
> There's a known issue with the [quota/usages API](/rest/api/aiservices/accountmanagement/usages/list?view=rest-aiservices-accountmanagement-2024-06-01-preview&tabs=HTTP&preserve-view=true) where it assumes the old ratio applies to the new o1-series models. The API returns the correct base capacity number, but doesn't apply the correct ratio for the accurate calculation of TPM.

### o-series global standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `o4-mini` | Enterprise agreement | 10 M | 10 K |
| `o3` | Enterprise agreement | 10 M | 10 K |
| `o3-mini` | Enterprise agreement | 50 M | 5 K |
| `o1` & `o1-preview` | Enterprise agreement | 30 M | 5 K |
| `o1-mini`| Enterprise agreement | 50 M | 5 K |
| `o4-mini` | Default | 1 M | 1 K  |
| `o3` | Default | 1 M | 1 K |
| `o3-mini` | Default | 5 M | 500 |
| `o1` & `o1-preview` | Default | 3 M | 500 |
| `o1-mini`| Default | 5 M | 500 |

### o-series data zone standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `o3-mini` | Enterprise agreement | 20 M | 2 K  |
| `o3-mini` | Default | 2 M | 200 |
| `o1` | Enterprise agreement | 6 M | 1 K |
| `o1` | Default | 600 K | 100 |

### o1-preview & o1-mini standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `o1-preview` | Enterprise agreement | 600 K | 100 |
| `o1-mini`| Enterprise agreement |  1 M | 100 |
| `o1-preview` | Default | 300 K | 50 |
| `o1-mini`| Default | 500 K | 50 |

## gpt-4o rate limits

`gpt-4o` and `gpt-4o-mini` have rate limit tiers with higher limits for certain customer types.

### gpt-4o global standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o`|Enterprise agreement | 30 M | 180 K |
|`gpt-4o-mini` | Enterprise agreement | 50 M | 300 K |
|`gpt-4o` |Default | 450 K | 2.7 K |
|`gpt-4o-mini` | Default | 2 M | 12 K  |

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

### gpt-4o audio

The rate limits for each `gpt-4o` audio model deployment are 100 K TPM and 1 K RPM. During the preview, [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and APIs might inaccurately show different rate limits. Even if you try to set a different rate limit, the actual rate limit is 100 K TPM and 1 K RPM.

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o-audio-preview` | Default | 450 K | 1 K |
|`gpt-4o-realtime-preview` | Default | 800 K | 1 K |
|`gpt-4o-mini-audio-preview` | Default | 2 M | 1 K |
|`gpt-4o-mini-realtime-preview` | Default | 800 K | 1 K |

M = million | K = thousand

## GPT-image-1 rate limits 

### GPT0-image-1 global standard

| Model|Tier| Quota Limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
|`gpt-image-1`|Enterprise agreement | N/A | 20 |
|`gpt-image-1` |Default | N/A | 6 |


## Usage tiers

Global standard deployments use Azure's global infrastructure, dynamically routing customer traffic to the data center with best availability for the customer’s inference requests. Similarly, Data zone standard deployments allow you to use Azure global infrastructure to dynamically route traffic to the data center within the Microsoft defined data zone with the best availability for each request. This enables more consistent latency for customers with low to medium levels of traffic. Customers with high sustained levels of usage might see greater variability in response latency.

The Usage Limit determines the level of usage above which customers might see larger variability in response latency. A customer’s usage is defined per model and is the total tokens consumed across all deployments in all subscriptions in all regions for a given tenant.

> [!NOTE]
> Usage tiers only apply to standard, data zone standard, and global standard deployment types. Usage tiers don't apply to global batch and provisioned throughput deployments.

### GPT-4o global standard, data zone standard, & standard

|Model| Usage Tiers per month |
|----|----|
|`gpt-4o` | 12 Billion tokens |
|`gpt-4o-mini` | 85 Billion tokens |

### GPT-4 standard

|Model| Usage Tiers per month|
|---|---|
| `gpt-4` + `gpt-4-32k`  (all versions) | 6 Billion |


## Other offer types

If your Azure subscription is linked to certain [offer types](https://azure.microsoft.com/support/legal/offer-details/), your max quota values are lower than the values indicated in the above tables.

|Tier| Quota Limit in tokens per minute (TPM) |
|---|:---|
|`Azure for Students` | 1 K (all models) <br>Exception o-series & GPT-4.1 & GPT 4.5 Preview: 0|
| `MSDN` | GPT-4o-mini: 200 K <br> GPT 3.5 Turbo Series: 200 K <br> GPT-4 series: 50 K <br>computer-use-preview: 8 K <br> gpt-4o-realtime-preview: 1 K <br> o-series: 0 <br> GPT 4.5 Preview: 0 <br> GPT-4.1: 50 K <br> GPT-4.1-nano: 200 K  |
|`Standard` | GPT-4o-mini: 200 K <br> GPT 3.5 Turbo Series: 200 K <br> GPT-4 series: 50 K <br>computer-use-preview: 30 K <br> o-series: 0 <br> GPT 4.5 Preview: 0  <br> GPT-4.1: 50 K <br> GPT-4.1-nano: 200 K  |
| `Azure_MS-AZR-0111P`  <br> `Azure_MS-AZR-0035P` <br> `Azure_MS-AZR-0025P` <br> `Azure_MS-AZR-0052P` <br>| GPT-4o-mini: 200 K <br> GPT 3.5 Turbo Series: 200 K <br> GPT-4 series: 50 K |
| `CSP Integration Sandbox` <sup>*</sup> | All models: 0 |
| `Lightweight trial`<br>`Free Trials`<br>`Azure Pass`  | All models: 0 |



<sup>*</sup>This only applies to a small number of legacy CSP sandbox subscriptions. Use the query below to determine what `quotaId` is associated with your subscription.

To determine the offer type that is associated with your subscription, you can check your `quotaId`. If your `quotaId` isn't listed in this table, your subscription qualifies for default quota.

# [REST](#tab/REST)

[API reference](/rest/api/subscription/subscriptions/get)

```bash
az login
access_token=$(az account get-access-token --query accessToken -o tsv)
```

```bash
curl -X GET "https://management.azure.com/subscriptions/{subscriptionId}?api-version=2020-01-01" \
  -H "Authorization: Bearer $access_token" \
  -H "Content-Type: application/json"
```

# [CLI](#tab/CLI)

```azurecli
az rest --method GET --uri "https://management.azure.com/subscriptions/{sub-id}?api-version=2020-01-01"
```
---

### Output

```json
{
  "authorizationSource": "Legacy",
  "displayName": "Pay-As-You-Go",
  "id": "/subscriptions/aaaaaa-bbbbb-cccc-ddddd-eeeeee",
  "state": "Enabled",
  "subscriptionId": "aaaaaa-bbbbb-cccc-ddddd-eeeeee",
  "subscriptionPolicies": {
    "locationPlacementId": "Public_2014-09-01",
    "quotaId": "PayAsYouGo_2014-09-01",
    "spendingLimit": "Off"
  }
}
```

| Quota allocation/Offer type | Subscription quota ID |
|:---|:----|
| Enterprise | `EnterpriseAgreement_2014-09-01` |
| Pay-as-you-go | `PayAsYouGo_2014-09-01`|
| MSDN | `MSDN_2014-09-01` |
| CSP Integration Sandbox | `CSPDEVTEST_2018-05-01` |
| Azure for Students | `AzureForStudents_2018-01-01` |
| Free Trial    | `FreeTrial_2014-09-01` |
| Azure Pass             | `AzurePass_2014-09-01` |
| Azure_MS-AZR-0111P            | `AzureInOpen_2014-09-01` |
| Azure_MS-AZR-0150P  | `LightweightTrial_2016-09-01` |
| Azure_MS-AZR-0035P <br> Azure_MS-AZR-0025P <br> Azure_MS-AZR-0052P <br>| `MPN_2014-09-01` |
| Azure_MS-AZR-0023P <br> Azure_MS-AZR-0060P <br> Azure_MS-AZR-0148P <br> Azure_MS-AZR-0148G | `MSDNDevTest_2014-09-01`|
| Default | Any quota ID not listed in this table  |

### General best practices to remain within rate limits

To minimize issues related to rate limits, it's a good idea to use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

## How to request quota increases

Quota increase requests can be submitted via the [quota increase request form](https://aka.ms/oai/stuquotarequest). Due to high demand, quota increase requests are being accepted and are filled in the order they're received. Priority is given to customers who generate traffic that consumes the existing quota allocation, and your request might be denied if this condition isn't met.

For other rate limits, [submit a service request](../cognitive-services-support-options.md?context=/azure/ai-services/openai/context/context).

## Regional quota capacity limits

You can view quota availability by region for your subscription in the [Azure AI Foundry portal](https://ai.azure.com/resource/quota).

Alternatively to view quota capacity by region for a specific model/version you can query the [capacity API](/rest/api/aiservices/accountmanagement/model-capacities/list) for your subscription. Provide a `subscriptionId`, `model_name`, and `model_version` and the API returns the available capacity for that model across all regions, and deployment types for your subscription.

> [!NOTE]
> Currently both the Azure AI Foundry portal and the capacity API return quota/capacity information for models that are [retired](./concepts/model-retirements.md) and no longer available.

[API Reference](/rest/api/aiservices/accountmanagement/model-capacities/list)

```python
import requests
import json
from azure.identity import DefaultAzureCredential

subscriptionId = "Replace with your subscription ID" #replace with your subscription ID
model_name = "gpt-4o"     # Example value, replace with model name
model_version = "2024-08-06"   # Example value, replace with model version

token_credential = DefaultAzureCredential()
token = token_credential.get_token('https://management.azure.com/.default')
headers = {'Authorization': 'Bearer ' + token.token}

url = f"https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/modelCapacities"
params = {
    "api-version": "2024-06-01-preview",
    "modelFormat": "OpenAI",
    "modelName": model_name,
    "modelVersion": model_version
}

response = requests.get(url, params=params, headers=headers)
model_capacity = response.json()

print(json.dumps(model_capacity, indent=2))

```

## Next steps

Explore how to [manage quota](./how-to/quota.md) for your Azure OpenAI deployments.
Learn more about the [underlying models that power Azure OpenAI](./concepts/models.md).
