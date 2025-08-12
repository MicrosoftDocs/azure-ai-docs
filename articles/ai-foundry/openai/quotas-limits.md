---
title: Azure OpenAI in Azure AI Foundry Models Quotas and Limits
description: This article features detailed descriptions and best practices on the quotas and limits for Azure OpenAI.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 08/07/2025
ms.service: azure-ai-openai
ms.topic: conceptual
ms.custom:
  - ignite-2023
  - references_regions
  - build-2025
---

# Azure OpenAI in Azure AI Foundry Models quotas and limits

This article contains a quick reference and a detailed description of the quotas and limits for Azure OpenAI.

## Scope of quota

Quotas and limits aren't enforced at the tenant level. Instead, the highest level of quota restrictions is scoped at the Azure subscription level.

## Regional quota allocation

Tokens per minute (TPM) and requests per minute (RPM) limits are defined *per region*, *per subscription*, and *per model or deployment type*.

For example, if the `gpt-4.1` Global Standard model is listed with a quota of *5 million TPM* and *5,000 RPM*, then *each region* where that [model or deployment type is available](./concepts/models.md) has its own dedicated quota pool of that amount for *each* of your Azure subscriptions. Within a single Azure subscription, it's possible to use a larger quantity of total TPM and RPM quota for a given model and deployment type, as long as you have resources and model deployments spread across multiple regions.

## Quotas and limits reference

The following section provides you with a quick guide to the default quotas and limits that apply to Azure OpenAI:

| Limit name | Limit value |
|--|--|
| Azure OpenAI resources per region, per Azure subscription | 30. |
| Default DALL-E 2 quota limits | 2 concurrent requests. |
| Default DALL-E 3 quota limits| 2 capacity units (6 requests per minute).|
| Default GPT-image-1 quota limits | 2 capacity units (6 requests per minute). |
| Default Sora quota limits | 60 requests per minute. |
| Default speech-to-text audio API quota limits | 3 requests per minute. |
| Maximum prompt tokens per request | Varies per model. For more information, see [Azure OpenAI models](./concepts/models.md).|
| Maximum standard deployments per resource | 32. |
| Maximum fine-tuned model deployments | 5. |
| Total number of training jobs per resource | 100. |
| Maximum simultaneously running training jobs per resource | 1. |
| Maximum training jobs queued | 20. |
| Maximum files per resource (fine-tuning) | 50. |
| Total size of all files per resource (fine-tuning) | 1 GB. |
| Maximum training job time (job fails if exceeded) | 720 hours. |
| Maximum training job size `(tokens in training file) x (# of epochs)` | 2 billion. |
| Maximum size of all files per upload (Azure OpenAI on your data) | 16 MB. |
| Maximum number or inputs in array with `/embeddings` | 2,048. |
| Maximum number of `/chat/completions` messages | 2,048. |
| Maximum number of `/chat/completions` functions | 128. |
| Maximum number of `/chat completions` tools | 128. |
| Maximum number of provisioned throughput units per deployment | 100,000. |
| Maximum files per assistant or thread | 10,000 when using the API or the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).|
| Maximum file size for assistants and fine-tuning | 512 MB<br/><br/>200 MB via the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs). |
| Maximum file upload requests per resource | 30 requests per second. |
| Maximum size for all uploaded files for assistants |200 GB. |
| Assistants token limit | 2,000,000 token limit. |
| `GPT-4o` and `GPT-4.1` maximum images per request (number of images in the messages array or conversation history) | 50. |
| `GPT-4` `vision-preview` and `GPT-4` `turbo-2024-04-09` default maximum tokens | 16. <br><br> Increase the `max_tokens` parameter value to avoid truncated responses. `GPT-4o` maximum tokens defaults to 4,096. |
| Maximum number of custom headers in API requests<sup>1</sup> | 10. |
| Message character limit | 1,048,576. |
| Message size for audio files | 20 MB. |

<sup>1</sup> Our current APIs allow up to 10 custom headers, which are passed through the pipeline and returned. Some customers now exceed this header count, which results in HTTP 431 errors. There's no solution for this error, other than to reduce header volume. In future API versions, we won't pass through custom headers. We recommend that customers don't depend on custom headers in future system architectures.

> [!NOTE]
> Quota limits are subject to change.

## GPT-5 Series

| Model       | Global Default<br>Tokens per minute (TPM)  | Global Enterprise and MCA-E <br>Tokens per minute (TPM)  | Data Zone Default <br>Tokens per minute (TPM)  | Data Zone Enterprise and MCA-E <br>Tokens per minute (TPM) |
|-------------|----------------|-------------------|-------------------|----------------------|
| gpt-5       | 1 M             | 10 M               | 300 K              | 3 M                   |
| gpt-5-mini  | 1 M             | 10 M               | 300 K              | 3 M                   |
| gpt-5-nano  | 5 M             | 150 M              | 2 M                | 50 M                  |
| gpt-5-chat  | 1 M             | 5 M                | N/A              |    N/A                  |


[!INCLUDE [Quota](./includes/global-batch-limits.md)]

## gpt-oss

| Model          | Tokens per minute (TPM) | Requests per minute (RPM) |
|----------------|-------------------|---------------------------------|
| `gpt-oss-120b` | 5 M               | 5 K                             |

## GPT-4 rate limits

### GPT-4.5 preview Global Standard

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
| `gpt-4.5` | Enterprise and MCA-E | 200K | 200 |
| `gpt-4.5` | Default | 150K | 150 |

### GPT-4.1 series Global Standard

| Model|Tier| Quota limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `gpt-4.1` (2025-04-14) | Enterprise and MCA-E | 5M | 5K |
| `gpt-4.1` (2025-04-14) | Default | 1M | 1K |
| `gpt-4.1-nano` (2025-04-14) | Enterprise and MCA-E | 150M | 150K |
| `gpt-4.1-nano` (2025-04-14) | Default | 5M | 5K |
| `gpt-4.1-mini` (2025-04-14) | Enterprise and MCA-E | 150M | 150K |
| `gpt-4.1-mini` (2025-04-14) | Default | 5M | 5K |

### GPT-4.1 series Data Zone Standard

| Model|Tier| Quota limit in tokens per minute (TPM) | Requests per minute |
|---|---|:---:|:---:|
| `gpt-4.1` (2025-04-14) | Enterprise and MCA-E | 2M | 2K |
| `gpt-4.1` (2025-04-14) | Default | 300K | 300 |
| `gpt-4.1-nano` (2025-04-14) | Enterprise and MCA-E | 50M | 50K |
| `gpt-4.1-nano` (2025-04-14) | Default | 2M | 2K |
| `gpt-4.1-mini` (2025-04-14) | Enterprise and MCA-E | 50M | 50K |
| `gpt-4.1-mini` (2025-04-14) | Default | 2M | 2K |

### GPT-4 Turbo

`gpt-4` (`turbo-2024-04-09`) has rate limit tiers with higher limits for certain customer types.

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4` (turbo-2024-04-09) | Enterprise and MCA-E | 2M | 12K |
|`gpt-4` (turbo-2024-04-09) | Default | 450K | 2.7K |

## model-router rate limits

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
| `model-router` (2025-05-19) | Enterprise and MCA-E | 10M | 10K |
| `model-router` (2025-05-19) | Default         | 1M | 1K |

## computer-use-preview Global Standard rate limits

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
| `computer-use-preview`| Enterprise and MCA-E | 30M | 300K |
| `computer-use-preview`| Default         | 450K | 4.5K |

## o-series rate limits

> [!IMPORTANT]
> The ratio of requests per minute to tokens per minute for quota can vary by model. When you deploy a model programmatically or [request a quota increase](https://aka.ms/oai/stuquotarequest), you don't have granular control over tokens per minute and requests per minute as independent values. Quota is allocated in terms of units of capacity, which have corresponding amounts of requests per minute and tokens per minute.
>
> | Model                  | Capacity   | Requests per minute (RPM)  | Tokens per minute (TPM) |
> |------------------------|:----------:|:--------------------------:|:-----------------------:|
> | Older chat models | 1 unit     | 6 RPM                      | 1,000 TPM               |
> | `o1` and `o1-preview`   | 1 unit     | 1 RPM                      | 6,000 TPM               |
> | `o3`                 | 1 unit     | 1 RPM                      | 1,000 TPM               |
> | `o4-mini`            | 1 unit     | 1 RPM                      | 1,000 TPM               |
> | `o3-mini`           | 1 unit     | 1 RPM                      | 10,000 TPM              |
> | `o1-mini`           | 1 unit     | 1 RPM                      | 10,000 TPM              |
> | `o3-pro`            | 1 unit     | 1 RPM                      | 10,000 TPM              |
>
> This concept is important for programmatic model deployment, because changes in the RPM to TPM ratio can result in accidental misallocation of quota.

### o-series Global Standard

| Model              |Tier                    | Quota limit in tokens per minute | Requests per minute |
|--------------------|------------------------|:--------------------------------------:|:---:  |
| `codex-mini`       | Enterprise and MCA-E   | 10M                                   | 10K  |
| `o3-pro`           | Enterprise and MCA-E   | 16M                                   | 1.6K |
| `o4-mini`          | Enterprise and MCA-E   | 10M                                   | 10K  |
| `o3`               | Enterprise and MCA-E   | 10M                                   | 10K  |
| `o3-mini`          | Enterprise and MCA-E   | 50M                                   | 5K   |
| `o1` and `o1-preview`| Enterprise and MCA-E   | 30M                                   | 5K   |
| `o1-mini`          | Enterprise and MCA-E   | 50M                                   | 5K   |
| `codex-mini`       | Default                | 1M                                    | 1K   |
| `o3-pro`           | Default                | 1.6M                                  | 160   |
| `o4-mini`          | Default                | 1M                                    | 1K   |
| `o3`               | Default                | 1M                                    | 1K   |
| `o3-mini`          | Default                | 5M                                    | 500   |
| `o1` and `o1-preview`| Default                | 3M                                    | 500   |
| `o1-mini`          | Default                | 5M                                    | 500   |

### o-series Data Zone Standard

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
| `o3-mini` | Enterprise and MCA-E | 20M | 2K  |
| `o3-mini` | Default | 2M | 200 |
| `o1` | Enterprise and MCA-E | 6M | 1K |
| `o1` | Default | 600K | 100 |

### o1-preview and o1-mini Standard

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
| `o1-preview` | Enterprise and MCA-E | 600K | 100 |
| `o1-mini`| Enterprise and MCA-E |  1M | 100 |
| `o1-preview` | Default | 300K | 50 |
| `o1-mini`| Default | 500K | 50 |

## gpt-4o rate limits

`gpt-4o` and `gpt-4o-mini` have rate limit tiers with higher limits for certain customer types.

### gpt-4o Global Standard

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o`|Enterprise and MCA-E | 30M | 180K |
|`gpt-4o-mini` | Enterprise and MCA-E | 50M | 300K |
|`gpt-4o` |Default | 450K | 2.7K |
|`gpt-4o-mini` | Default | 2M | 12K  |

### gpt-4o Data Zone Standard

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o`|Enterprise and MCA-E | 10M | 60K |
|`gpt-4o-mini` | Enterprise and MCA-E | 20M | 120K |
|`gpt-4o` |Default | 300K | 1.8K |
|`gpt-4o-mini` | Default | 1M | 6K  |

### gpt-4o Standard

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o`|Enterprise and MCA-E | 1M | 6K |
|`gpt-4o-mini` | Enterprise and MCA-E | 2M | 12K |
|`gpt-4o`|Default | 150K | 900 |
|`gpt-4o-mini` | Default | 450K | 2.7K |

### gpt-4o audio

The rate limits for each `gpt-4o` audio model deployment are 100,000 tokens per minute and 1,000 requests per minute. During the preview, [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and APIs might inaccurately show different rate limits. Even if you try to set a different rate limit, the actual rate limit is 100,000 tokens per minute and 1,000 requests per minute.

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
|`gpt-4o-audio-preview` | Default | 450K | 1K |
|`gpt-4o-realtime-preview` | Default | 800K | 1K |
|`gpt-4o-mini-audio-preview` | Default | 2M | 1K |
|`gpt-4o-mini-realtime-preview` | Default | 800K | 1K |

## GPT-image-1 rate limits

### GPT0-image-1 Global Standard

| Model|Tier| Quota limit in tokens per minute | Requests per minute |
|---|---|:---:|:---:|
|`gpt-image-1`|Enterprise and MCA-E | N/A | 20 |
|`gpt-image-1` |Default | N/A | 6 |

## Usage tiers

Global Standard deployments use the global infrastructure of Azure. They dynamically route customer traffic to the data center with the best availability for the customer's inference requests. Similarly, Data Zone Standard deployments allow you to use the global infrastructure of Azure to dynamically route traffic to the data center within the Microsoft-defined data zone with the best availability for each request. This practice enables more consistent latency for customers with low to medium levels of traffic. Customers with high sustained levels of usage might see greater variability in response latency.

The usage limit determines the level of usage above which customers might see larger variability in response latency. A customer's usage is defined per model. It's the total number of tokens consumed across all deployments in all subscriptions in all regions for a given tenant.

> [!NOTE]
> Usage tiers apply only to Standard, Data Zone Standard, and Global Standard deployment types. Usage tiers don't apply to global batch and provisioned throughput deployments.

### Global Standard, Data Zone Standard, and Standard

|Model| Usage tiers per month |
|----|:----|
| `gpt-4` + `gpt-4-32k`  (all versions) | 6 billion tokens |
| `gpt-4o` | 12 billion tokens |
| `gpt-4o-mini` | 85 billion tokens |
| `o3-mini`  | 50 billion tokens |
| `o1` | 4 billion tokens |
| `o4-mini` | 50 billion tokens |
| `o3` | 5 billion tokens |
| `gpt-4.1` | 30 billion tokens |
| `gpt-4.1-mini` | 150 billion tokens |
| `gpt-4.1-nano` | 550 billion tokens |

## Other offer types

If your Azure subscription is linked to certain [offer types](https://azure.microsoft.com/support/legal/offer-details/), your maximum quota values are lower than the values indicated in the previous tables.

|Tier| Quota limit in tokens per minute |
|---|:---|
|`Azure for Students` | 1K (all models) <br>Exception o-series, GPT-4.1, and GPT 4.5 Preview: 0|
| `MSDN` | GPT-4o-mini: 200K <br> GPT 3.5 Turbo Series: 200K <br> GPT-4 series: 50K <br>computer-use-preview: 8K <br> gpt-4o-realtime-preview: 1K <br> o-series: 0 <br> GPT 4.5 Preview: 0 <br> GPT-4.1: 50K <br> GPT-4.1-nano: 200K  |
|`Standard` | GPT-4o-mini: 200K <br> GPT 3.5 Turbo Series: 200K <br> GPT-4 series: 50K <br>computer-use-preview: 30K <br> o-series: 0 <br> GPT 4.5 Preview: 0  <br> GPT-4.1: 50K <br> GPT-4.1-nano: 200K  |
| `Azure_MS-AZR-0111P`  <br> `Azure_MS-AZR-0035P` <br> `Azure_MS-AZR-0025P` <br> `Azure_MS-AZR-0052P` <br>| GPT-4o-mini: 200K <br> GPT 3.5 Turbo Series: 200K <br> GPT-4 series: 50K |
| `CSP Integration Sandbox` <sup>*</sup> | All models: 0 |
| `Lightweight trial`<br>`Free trials`<br>`Azure Pass`  | All models: 0 |

<sup>*</sup>This limit applies to only a small number of legacy CSP sandbox subscriptions. Use the following query to determine what `quotaId` value is associated with your subscription.

To determine the offer type associated with your subscription, you can check your `quotaId` value. If your `quotaId` value isn't listed in this table, your subscription qualifies for the default quota.

# [REST](#tab/REST)

See the [API reference](/rest/api/subscription/subscriptions/get).

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

## Output

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
| Enterprise and MCA-E | `EnterpriseAgreement_2014-09-01` |
| Pay-as-you-go | `PayAsYouGo_2014-09-01`|
| MSDN | `MSDN_2014-09-01` |
| CSP Integration Sandbox | `CSPDEVTEST_2018-05-01` |
| Azure for Students | `AzureForStudents_2018-01-01` |
| Free trial    | `FreeTrial_2014-09-01` |
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

## Request quota increases

Quota increase requests can be submitted via the [quota increase request form](https://aka.ms/oai/stuquotarequest). Due to high demand, quota increase requests are accepted and filled in the order they're received. Priority is given to customers who generate traffic that consumes the existing quota allocation. Your request might be denied if this condition isn't met.

You can [submit a service request](../../ai-services/cognitive-services-support-options.md?context=/azure/ai-foundry/openai/context/context) for other rate limits.

## Regional quota capacity limits

You can view quota availability by region for your subscription in the [Azure AI Foundry portal](https://ai.azure.com/resource/quota).

To view quota capacity by region for a specific model or version, you can query the [capacity API](/rest/api/aiservices/accountmanagement/model-capacities/list) for your subscription. Provide a `subscriptionId`, `model_name`, and `model_version` and the API returns the available capacity for that model across all regions and deployment types for your subscription.

> [!NOTE]
> Currently, both the Azure AI Foundry portal and the capacity API return quota/capacity information for models that are [retired](./concepts/model-retirements.md) and no longer available.

See the [API reference](/rest/api/aiservices/accountmanagement/model-capacities/list).

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

## Related content

- Explore how to [manage quota](./how-to/quota.md) for your Azure OpenAI deployments.
- Learn more about the [underlying models that power Azure OpenAI](./concepts/models.md).
