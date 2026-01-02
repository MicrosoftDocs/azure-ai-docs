---
title: Provisioned throughput for Microsoft Foundry Models
description: Learn about provisioned throughput and Microsoft Foundry.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: article
ms.date: 11/03/2025
manager: nitinme
author: msakande #ChrisHMSFT
ms.author: mopeakande #chrhoder
ms.reviewer: shiyingfu
reviewer: swingfu
recommendations: false
#CustomerIntent As a developer, I want to understand provisioned throughput so I can deploy and manage AI models efficiently.
---

# What is provisioned throughput?

[!INCLUDE [version-banner](../../includes/version-banner.md)]

The Microsoft Foundry provisioned throughput offering is a model deployment type that lets you specify a fixed amount of throughput capacity for a deployment. Foundry allocates the corresponding model processing capacity at deployment time and keeps it available for the lifetime of the deployment.
<!-- Comment: Removed redundant Tip block and clarified the definition to be concrete and non-promotional per agent feedback. -->

You can use the provisioned throughput you requested across a portfolio of [models that are sold directly by Azure](../../../ai-foundry/concepts/foundry-models-overview.md#models-sold-directly-by-azure). These include Azure OpenAI models and other Foundry Models such as Azure DeepSeek, Azure Grok, and Azure Llama.

Provisioned throughput provides:
- **Model eligibility:** Access to supported flagship models that are enabled for provisioned deployments.
<!-- Comment: Replaced marketing phrasing with a concrete eligibility statement. -->
- **Quota-based flexibility:** The same PTU quota can be reassigned across deployments and supported models within the same region and deployment type.
<!-- Comment: Tightened “flexibility” into a specific quota behavior. -->
- **Reservation-based pricing:** PTU reservations apply discounted pricing to matching provisioned deployments and improve reservation utilization.
<!-- Comment: Converted discount language into a pricing mechanism description. -->
- **Deterministic performance limits:** Requests are accepted until deployment utilization reaches 100%, providing predictable maximum throughput and bounded latency for uniform workloads.
<!-- Comment: Replaced “predictable performance” with explicit acceptance and utilization behavior. -->
- **Pre-allocated capacity:** The configured throughput is reserved for the deployment whether or not requests are sent.
<!-- Comment: Clarified allocated capacity behavior. -->
- **Cost efficiency at scale:** High, steady request volumes can be more cost-effective than token-based consumption.
<!-- Comment: Rephrased cost savings as a conditional, workload-based statement. -->

> [!TIP]
> * You can take advantage of additional savings by purchasing [Microsoft Foundry Provisioned Throughput reservations](/azure/cost-management-billing/reservations/azure-openai#buy-a-microsoft-azure-openai-service-reservation).
> * Provisioned throughput is available as the following deployment types: [global provisioned](../../foundry-models/concepts/deployment-types.md#global-provisioned), [data zone provisioned](../../foundry-models/concepts/deployment-types.md#data-zone-provisioned), and [regional provisioned](../../foundry-models/concepts/deployment-types.md#regional-provisioned).

## When to use provisioned throughput

You should consider switching from standard deployments to provisioned throughput deployments when you have well-defined and predictable throughput and latency requirements. This typically occurs when an application is production-ready or already running in production and expected traffic patterns are understood. In these scenarios, provisioned throughput helps you size capacity in advance and avoid unexpected billing. Provisioned throughput deployments are also appropriate for applications with real-time or latency-sensitive requirements.

## Key concepts
The sections that follow describe key concepts that you should be aware of when using the provisioned throughput offering.

### Provisioned Throughput Units (PTU)

Provisioned throughput units (PTU) are generic units of model processing capacity that you use to size provisioned deployments. PTU determine the maximum throughput available to process prompts and generate completions. PTU are granted to a subscription as quota, are scoped to a specific region, and define the maximum PTU that can be assigned to deployments in that subscription and region.

#### Cost management under shared PTU reservation

You can use PTU reservations to manage costs across Foundry Models that support provisioned throughput. The number of PTU required to achieve a given throughput varies by model and workload characteristics. For details about PTU costs and latency characteristics, see [Understanding costs associated with PTU](../how-to/provisioned-throughput-onboarding.md).

Existing PTU reservations are automatically upgraded to support Foundry Models. For example, suppose you have an existing reservation for 500 PTU. You allocate 300 PTU to Azure OpenAI models and use PTU to deploy Azure DeepSeek, Azure Llama, or other supported Foundry Models.

- If you allocate the remaining 200 PTU to DeepSeek-R1, all 500 PTU receive the reservation discount.
- If you allocate 300 PTU to DeepSeek-R1, 200 PTU receive the reservation discount and the additional 100 PTU are billed at DeepSeek-R1's hourly rate.

To learn more about reducing costs with PTU reservations, see [Save costs with Microsoft Foundry Provisioned Throughput Reservations](/azure/cost-management-billing/reservations/azure-openai).

### Deployment types

When you create a provisioned deployment in Foundry, you select one of the following deployment types based on data processing requirements: Global Provisioned Throughput, Data Zone Provisioned Throughput, or Regional Provisioned Throughput.

When you create a provisioned deployment by using the CLI or API, set the `sku-name` to `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, or `ProvisionedManaged` to match the selected deployment type.

| **Deployment type** | **sku-name in CLI** |
|----------|----------|
| Global Provisioned Throughput | GlobalProvisionedManaged    |
| Data Zone Provisioned Throughput | DataZoneProvisionedManaged    |
| Regional Provisioned Throughput | ProvisionedManaged    |

To adapt the following Azure CLI example to a different deployment type, update the `sku-name` parameter to match the deployment type you want to deploy.

```azurecli
az cognitiveservices account deployment create \
--name <myResourceName> \
--resource-group  <myResourceGroupName> \
--deployment-name MyDeployment \
--model-name gpt-4o \
--model-version 2024-08-06  \
--model-format OpenAI \
--sku-capacity 15 \
--sku-name GlobalProvisionedManaged
```

### Capacity transparency

Models sold directly by Azure are subject to finite GPU capacity, and customer demand can exceed available capacity in a region. Although quota defines the maximum PTU you can deploy in a region, it doesn't guarantee that capacity is available at deployment time. In general:

- Quota limits the maximum PTU that can be deployed in a subscription and region but doesn't guarantee capacity.
- Capacity is allocated when a deployment is created and remains allocated while the deployment exists. If capacity isn't available, deployment creation fails.
- Real-time quota and capacity information helps you select an appropriate region.
- Scaling down or deleting a deployment releases capacity back to the region. Released capacity might not be available later.

#### Regional capacity guidance

To determine available capacity, use the capacity API or the Foundry deployment experience, which provides real-time capacity information.

In Foundry, the deployment experience evaluates the selected model, version, region, and PTU. If capacity isn't available, you're prompted to select an alternative region.

For more information, see the Foundry [Provisioned get started guide](../how-to/provisioned-get-started.md).

The [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list?view=rest-aiservices-accountmanagement-2024-04-01-preview&tabs=HTTP&preserve-view=true) lets you programmatically determine the maximum supported deployment size for a model by considering both quota and service capacity.

If no region can support the desired model, version, or PTU, try the following:
- Deploy with fewer PTU.
- Retry deployment later, as capacity availability changes over time.
- Verify that sufficient quota exists in all acceptable regions.

### How can I monitor capacity?

The [Provisioned-Managed Utilization V2 metric](../how-to/monitor-openai.md#azure-monitor-platform-metrics) in Azure Monitor measures deployment utilization in one-minute intervals. All provisioned deployment types aim to process accepted requests with consistent model processing times, although end-to-end latency depends on request characteristics.

### How utilization performance works

Provisioned deployments allocate a fixed amount of model processing capacity.

When capacity is exceeded, the API returns an HTTP 429 status code. This fast-fail response allows you to manage traffic by redirecting requests, using standard deployments, or implementing retry logic. The service continues to return 429 responses until utilization drops below 100%.

#### What should I do when I receive a 429 response?
A 429 response indicates that the deployment is fully utilized at that moment. The `retry-after-ms` and `retry-after` headers specify when the next request is likely to be accepted.

Common strategies include:
- Redirecting traffic to another deployment or model for lower latency.
- Implementing client-side retries for higher overall throughput per PTU.

#### How does the service decide when to send a 429?

Each request is evaluated based on prompt size, expected generation size, and model characteristics to estimate utilization. This differs from standard deployments, which use [custom rate limiting](../how-to/quota.md).

Provisioned deployments use a variation of the leaky bucket algorithm:

1. Each deployment has a fixed utilization limit based on PTU.
1. When a request arrives:
   - If utilization exceeds 100%, the service returns a 429 with `retry-after-ms`.
   - Otherwise, the service estimates utilization based on prompt tokens (minus cached tokens) and `max_tokens`.
1. After the request completes, utilization is corrected based on actual compute usage.
1. Utilization decreases continuously based on deployed PTU.

> [!NOTE]
> Calls are accepted until utilization reaches 100%. Short bursts above 100% might occur, but sustained traffic is capped at 100%.

:::image type="content" source="../media/provisioned/utilization.jpg" alt-text="Diagram showing how subsequent calls are added to the utilization." lightbox="../media/provisioned/utilization.jpg":::

#### How many concurrent calls can I have on my deployment?

Concurrency depends on request characteristics such as prompt size and `max_tokens`. Requests are accepted until utilization reaches 100%. To estimate concurrency, model your workload by using the [capacity calculator](https://ai.azure.com/resource/calculator).

## Provisioned throughput capability for models sold directly by Azure  

This section lists Foundry Models that support provisioned throughput. You can use PTU quota and reservations across the models shown.

Key considerations:
- Model versions aren't listed. Check supported versions in the Foundry portal.
- Regional availability varies by deployment type.
- New models typically support Global provisioned throughput first.
- PTU quota and reservations must match the region and deployment type.
- Spillover is optional. For more information, see [Manage traffic with spillover for provisioned deployments](../how-to/spillover-traffic-management.md).

| Model family       | Model name       | Global provisioned | Data zone provisioned | Regional provisioned | Spillover feature |
|--------------------|------------------|--------------------|-----------------------|----------------------|-------------------|
| **Azure OpenAI**   | Gpt 5            | ✅                 | ✅                     |                      | ✅                 |
|                    | Gpt 4.1          | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | Gpt 4.1 mini     | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | Gpt 4.1 nano     | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | Gpt 4o           | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | Gpt 4o mini      | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | Gpt 3.5 Turbo    | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | o1               | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | O3 mini          | ✅                 | ✅                     | ✅                   | ✅                 |
|                    | O4 mini          | ✅                 | ✅                     | ✅                   | ✅                 |
| **Azure DeepSeek** | DeepSeek-R1      | ✅                 |                       |                      |                   |
|                    | DeepSeek-V3-0324 | ✅                 |                       |                      |                   |
|                    | DeepSeek-R1-0528 | ✅                 |                       |                      |                   |

### Region availability for provisioned throughput capability

# [Global Provisioned Throughput](#tab/global-ptum)

#### Global provisioned throughput model availability

[!INCLUDE [Provisioned Managed Global](../includes/model-matrix/provisioned-global.md)]

# [Data Zone Provisioned Throughput](#tab/datazone-provisioned-managed)

#### Data zone provisioned throughput model availability

[!INCLUDE [Global data zone provisioned managed](../includes/model-matrix/datazone-provisioned-managed.md)]

# [Regional Provisioned Throughput](#tab/provisioned)

#### Regional provisioned throughput deployment model availability

[!INCLUDE [Provisioned](../includes/model-matrix/provisioned-models.md)]

---

> [!NOTE]
> The provisioned version of `gpt-4` **Version:** `turbo-2024-04-09` is currently limited to text only.

## Related content

- [Learn about the onboarding steps for provisioned deployments](../how-to/provisioned-throughput-onboarding.md)
- [Provisioned Throughput Units (PTU) getting started guide](../how-to//provisioned-get-started.md)