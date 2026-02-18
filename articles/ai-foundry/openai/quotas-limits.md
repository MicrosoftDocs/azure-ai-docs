---
title: Azure OpenAI in Microsoft Foundry Models Quotas and Limits
description: This article features detailed descriptions and best practices on the quotas and limits for Azure OpenAI.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 02/17/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: limits-and-quotas
ms.custom:
  - ignite-2023
  - references_regions
  - build-2025
monikerRange: 'foundry-classic || foundry'

---

# Azure OpenAI in Microsoft Foundry Models quotas and limits


This article contains a quick reference and a detailed description of the quotas and limits for Azure OpenAI.

## Scope of quota

Quotas and limits aren't enforced at the tenant level. Instead, the highest level of quota restrictions is scoped at the Azure subscription level.

## Regional quota allocation

Tokens per minute (TPM) and requests per minute (RPM) limits are defined *per region*, *per subscription*, and *per model or deployment type*.

For example, if the `gpt-4.1` Global Standard model is listed with a quota of *5 million TPM* and *5,000 RPM*, then *each region* where that [model or deployment type is available](../foundry-models/concepts/models-sold-directly-by-azure.md) has its own dedicated quota pool of that amount for *each* of your Azure subscriptions. Within a single Azure subscription, it's possible to use a larger quantity of total TPM and RPM quota for a given model and deployment type, as long as you have resources and model deployments spread across multiple regions.

## Quota tiers

To improve the Foundry Models and provide a frictionless experience, we're launching Foundry Quota Tiers. Foundry Quota Tiers allows model quota to increase as consumption grows, helping you grow without hitting rate limits while creating a fairer environment for all users. Seven new levels will be available starting today: Free Tier and Tier 1 through Tier 6. Your quota tier will be determined by both your usage and your Microsoft relationship such as Enterprise status. 

### What’s changing for me? 

Before Quota Tiers, Foundry offered Default and Enterprise quota levels. However, the quota gap between these two levels was too high and requesting more quota was a long process. With Quota Tiers, all Foundry users will be assigned a tier with a quota that’s either equal or higher than their previous quota allocation. If additional quota was granted through the quota increase process, that quota will be applicable and won't be lowered. As your consumption increases, Foundry will automatically grant you more quota by moving you to next tier. You can always ask for more quota using the quota form.  

### What are the tier change criteria? 

Foundry looks at your consumption trends over time. If there's an increase in your consumption and the current tier is preventing you from seamlessly using Foundry Models, it will automatically upgrade your tier to the next tier. Another factor is your relationship with Microsoft. For example, if you have Enterprise relationship (including MCA-E) you'll be assigned a higher tier regardless of your consumption. Finally, customers who qualify for auto-upgrades also have consistent payment history.  

### Can I opt out of auto upgrades? 

Yes, you can opt out of auto upgrades and you'll remain in your current tier regardless of changes in your consumption. We recognize that some of our customers use quota to manage their billing. This isn't the Azure best practice, however, we understand that if your system is configured that way we don’t want to break it. You can learn more about billing management and best practices here: [Cost Management](../concepts/manage-costs.md). 

To opt out, you can set the following flag to `NoAutoUpgrade`: 

```bash
curl -X PATCH \
  "https://management.azure.com/subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.CognitiveServices/quotaTiers/default?api-version=2025-10-01-preview" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "tierUpgradePolicy": "NoAutoUpgrade"
    }
  }'
```

> [!NOTE]
> The opt out feature is preview and may be subject to change/removal in the future.


### Can I request more quota?

Yes, using the [quota request form](https://aka.ms/oai/stuquotarequest) you can always request more quota. However, note that your request, if approved, will be rounded up to the next tier and your current tier will remain the same.


### Quota tier reference

# [Tier 6](#tab/tier6)

[!INCLUDE [Quota](./includes/quota-tier/tier-6.md)]

# [Tier 5](#tab/tier5)

[!INCLUDE [Quota](./includes/quota-tier/tier-5.md)]

# [Tier 4](#tab/tier4)

[!INCLUDE [Quota](./includes/quota-tier/tier-4.md)]

# [Tier 3](#tab/tier3)

[!INCLUDE [Quota](./includes/quota-tier/tier-3.md)]

# [Tier 2](#tab/tier2)

[!INCLUDE [Quota](./includes/quota-tier/tier-2.md)]

# [Tier 1](#tab/tier1)

[!INCLUDE [Quota](./includes/quota-tier/tier-1.md)]

# [Free](#tab/tierfree)

[!INCLUDE [Quota](./includes/quota-tier/free.md)]

---



## Quotas and limits reference

The following section provides you with a quick guide to the default quotas and limits that apply to Azure OpenAI:

| Limit name | Limit value |
|--|--|
| Azure OpenAI resources per region, per Azure subscription | 30. |
| Default DALL-E 2 quota limits | 2 concurrent requests. |
| Default DALL-E 3 quota limits| 6 requests per minute |
| Default GPT-image-1 quota limits | 9 requests per minute |
| Default GPT-image-1-mini quota limits | 12 requests per minute |
| Default GPT-image-1.5 quota limits | 9 requests per minute |
| Default Sora quota limits | 60 requests per minute. |
| Default Sora 2 quota limits | 2 job requests<sup>1</sup> per minute| 
| Default speech-to-text audio API quota limits | 3 requests per minute. |
| Maximum prompt tokens per request | Varies per model. For more information, see [Azure OpenAI models](../foundry-models/concepts/models-sold-directly-by-azure.md).|
| Maximum standard deployments per resource | 32. |
| Maximum fine-tuned model deployments | 10. |
| Total number of training jobs per resource | 100. |
| Maximum simultaneously running training jobs per resource | Standard and global training: 3; <br> Developer training: 5 |
| Maximum training jobs queued | 20. |
| Maximum files per resource (fine-tuning) | 100. |
| Total size of all files per resource (fine-tuning) | 1 GB. |
| Maximum training job time (job fails if exceeded) | 720 hours. |
| Maximum training job size `(tokens in training file) x (# of epochs)` | 2 billion. |
| Maximum size of all files per upload (Azure OpenAI on your data) | 16 MB. |
| Maximum number or inputs in array with `/embeddings` | 2,048. |
| Maximum number of `/chat/completions` messages | 2,048. |
| Maximum number of `/chat/completions` functions | 128. |
| Maximum number of `/chat completions` tools | 128. |
| Maximum number of provisioned throughput units per deployment | 100,000. |
| Maximum files per assistant or thread | 10,000 when using the API or the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).|
| Maximum file size for assistants and fine-tuning | 512 MB via the API<br/><br/>200 MB via the [Foundry portal](https://ai.azure.com/?cid=learnDocs). |
| Maximum file upload requests per resource | 30 requests per second. |
| Maximum size for all uploaded files for assistants |200 GB. |
| Assistants token limit | 2,000,000 token limit. |
| `GPT-4o` and `GPT-4.1` maximum images per request (number of images in the messages array or conversation history) | 50. |
| `GPT-4 vision-preview` and `GPT-4 turbo-2024-04-09` default maximum tokens | 16. <br><br> Increase the `max_tokens` parameter value to avoid truncated responses. `GPT-4o` maximum tokens defaults to 4,096. |
| Maximum number of custom headers in API requests<sup>2</sup> | 10. |
| Message character limit | 1,048,576. |
| Message size for audio files | 20 MB. |

<sup>1</sup> The Sora 2 RPM quota only counts video job requests. Other types of requests aren't rate-limited.

<sup>2</sup> Our current APIs allow up to 10 custom headers, which are passed through the pipeline and returned. Some customers now exceed this header count, which results in HTTP 431 errors. There's no solution for this error, other than to reduce header volume. In future API versions, we won't pass through custom headers. We recommend that customers don't depend on custom headers in future system architectures.


> [!NOTE]
> Quota limits are subject to change.

## model-router rate limits

| Model                              | Deployment Type  | Default RPM   | Default TPM   | Enterprise and MCA-E RPM    | Enterprise and MCA-E TPM     |
|:----------------------------------:|------------------|:-------------:|:-------------:|:---------------------------:|:----------------------------:|
| `model-router` <br> `(2025-11-18)` | DataZoneStandard | 150           | 150,000       | 300                         | 300,000                      |
| `model-router` <br> `(2025-11-18)` | GlobalStandard   | 250           | 250,000       | 400                         | 400,000                      |


[!INCLUDE [Quota](./includes/global-batch-limits.md)]

## gpt-oss

| Model          | Tokens per minute (TPM) | Requests per minute (RPM) |
|----------------|-------------------|---------------------------------|
| `gpt-oss-120b` | 5 M               | 5 K                             |


## Usage tiers

Global Standard deployments use the global infrastructure of Azure. They dynamically route customer traffic to the data center with the best availability for the customer's inference requests. Similarly, Data Zone Standard deployments allow you to use the global infrastructure of Azure to dynamically route traffic to the data center within the Microsoft-defined data zone with the best availability for each request. This practice enables more consistent latency for customers with low to medium levels of traffic. Customers with high sustained levels of usage might see greater variability in response latency.

Azure OpenAI usage tiers are designed to provide consistent performance for most customers with low to medium levels of traffic. Each usage tier defines the maximum throughput (tokens per minute) you can expect with predictable latency. When your usage stays within your assigned tier, latency remains stable and response times are consistent.

### What happens if you exceed your usage tier?

- If your request throughput exceeds your usage tier—especially during periods of high demand—your response latency may increase significantly.
- Latency can vary and, in some cases, may be more than two times higher than when operating within your usage tier.
- This variability is most noticeable for customers with high sustained usage or bursty traffic patterns.

### Recommended actions If you exceed your usage tier
If you encounter 429 errors or notice increased latency variability, here’s what you should do:

- Request a quota increase: visit the Azure portal to request a higher quota for your subscription.
- Consider upgrading to a premium offer (PTU): for latency-critical or high-volume workloads, upgrade to Provisioned Throughput Units (PTU). PTU provides dedicated resources, guaranteed capacity, and predictable latency—even at scale. This is the best choice for mission-critical applications that require consistent performance.
- Monitor your usage: regularly review your usage metrics in the Azure portal to ensure you're operating within your tier limits. Adjust your workload or deployment strategy as needed.

The usage limit determines the level of usage above which customers might see larger variability in response latency. A customer's usage is defined per model. It's the total number of tokens consumed across all deployments in all subscriptions in all regions for a given tenant.

> [!NOTE]
> Usage tiers apply only to Standard, Data Zone Standard, and Global Standard deployment types. Usage tiers don't apply to global batch and provisioned throughput deployments.

### Global Standard, Data Zone Standard, and Standard

|Model| Usage tiers per month |
|----|:----|
| `gpt-5` | 32 billion tokens |
| `gpt-5-mini` | 160 billion tokens |
| `gpt-5-nano` | 800 billion tokens |
| `gpt-5-chat` | 32 billion tokens |
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

### General best practices to remain within rate limits

To minimize issues related to rate limits, it's a good idea to use the following techniques:

- Implement retry logic in your application.
- Avoid sharp changes in the workload. Increase the workload gradually.
- Test different load increase patterns.
- Increase the quota assigned to your deployment. Move quota from another deployment, if necessary.

## Request quota increases

[!INCLUDE [quota-increase- request](includes/quota-increase-request.md)]

## Regional quota capacity limits

You can view quota availability by region for your subscription in the [Foundry portal](https://ai.azure.com/resource/quota).

To view quota capacity by region for a specific model or version, you can query the [capacity API](/rest/api/aiservices/accountmanagement/model-capacities/list) for your subscription. Provide a `subscriptionId`, `model_name`, and `model_version` and the API returns the available capacity for that model across all regions and deployment types for your subscription.

> [!NOTE]
> Currently, both the Foundry portal and the capacity API return quota/capacity information for models that are [retired](./concepts/model-retirements.md) and no longer available.

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
- Learn more about the [underlying models that power Azure OpenAI](../foundry-models/concepts/models-sold-directly-by-azure.md).