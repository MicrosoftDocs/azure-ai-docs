---
title: "What is provisioned throughput for Foundry Models?"
description: "Learn how provisioned throughput gives you dedicated AI model capacity with predictable latency, how PTUs and quota relate, and when to use provisioned throughput over standard deployments."
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 04/06/2026
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
manager: nitinme
author: msakande
ms.author: mopeakande
ms.reviewer: seramasu
reviewer: rsethur
recommendations: false
#CustomerIntent: As a developer familiar with Foundry deployments, I want to understand provisioned throughput so that I can decide whether to use it and correctly plan PTU quota, reservations, and capacity for my workload.
---

# What is provisioned throughput for Foundry Models?

Provisioned throughput is a model deployment type in Microsoft Foundry that reserves dedicated model processing capacity for your application. Unlike standard deployments—where inference capacity is shared across customers and throughput can vary with demand—a provisioned deployment allocates a fixed amount of processing capacity to your deployment and holds it ready whether or not requests are being made.

This article explains the core concepts behind provisioned throughput: what it is, when to use it, how capacity is measured and billed, and what to know about availability before you deploy.

## How provisioned throughput differs from standard deployments

In a standard deployment, your requests draw from a shared pool of model processing capacity. Standard deployment works well for exploratory or variable workloads. Under heavy demand, however, latency and throughput can vary, and you might encounter rate limits before your quota is exhausted.

A provisioned throughput deployment gives you:

- **Predictable latency**: Accepted requests are processed with a consistent per-call maximum latency, because no other customer's traffic competes for your capacity.
- **Dedicated capacity**: The allocated compute is held for your deployment and doesn't fluctuate with broader service demand.
- **No shared rate limits**: Your requests won't be throttled because of other customers' traffic spikes.
- **Cost efficiency at scale**: For sustained high-volume workloads, reserved capacity is typically more cost-effective than per-token billing.

With provisioned throughput, you commit to a capacity level upfront—and you're billed for it hourly, regardless of actual utilization.

## When to use provisioned throughput

Provisioned throughput is the right choice when your application has:

- **Predictable traffic patterns**: You have a reasonable estimate of requests per minute and token volumes.
- **Latency-sensitive requirements**: Your users or downstream systems need consistent, low-latency responses.
- **Production-scale volume**: High throughput use cases where per-token billing becomes expensive.
- **Real-time or interactive scenarios**: Chat applications, copilots, or agents where variable response times degrade user experience.

Standard deployments remain the better fit for development, testing, low-volume usage, or highly variable traffic that makes it difficult to size a deployment in advance.

> [!NOTE]
> In function calling and agent use cases, token usage can be variable. Understand your expected tokens per minute (TPM) usage in detail before migrating workloads to provisioned throughput.

## Provisioned throughput units

**Provisioned throughput units (PTUs)** are the unit of measure for provisioned capacity. A PTU represents a fixed amount of model processing capacity. When you create a provisioned deployment, you specify how many PTUs to allocate. Foundry reserves that amount of compute and holds it for your deployment.

Key characteristics of PTUs:

- **Model-independent**: The same PTU quota can be used to deploy any [supported model](#supported-models). You don't buy PTUs for a specific model.
- **Region-specific**: PTU quota is granted per subscription, per region. Quota in East US doesn't carry over to West Europe.
- **Throughput varies by model**: The tokens per minute (TPM) that a given number of PTUs delivers depends on the model. A heavier model requires more PTUs to serve the same TPM as a lighter one. For per-model PTU-to-TPM ratios, see [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md#how-much-throughput-per-ptu-you-get-for-each-model).
- **Minimum deployment sizes apply**: Each model has a minimum PTU count required to create a deployment. Minimums vary by model and are listed in [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md#how-much-throughput-per-ptu-you-get-for-each-model).

### PTU quota vs. capacity

Quota and capacity are related but distinct:

| Concept | What it means |
|---|---|
| **PTU quota** | The maximum number of PTUs you're allowed to deploy in a subscription and region. Quota is a policy limit enforced by Azure. To request quota, submit the [quota request form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu). |
| **Capacity** | The actual GPU compute available to serve your deployment when you create it. Capacity is allocated at deployment time and held for the deployment's lifetime. |

PTU quota isn't provisioned automatically. To request PTU quota for your subscription and region, see [Obtain PTU quota](../how-to/provisioned-throughput-onboarding.md#obtain-ptu-quota).

> [!IMPORTANT]
> Having PTU quota doesn't guarantee that capacity is available. If GPU capacity in the region is insufficient for the requested PTU count, the deployment fails. Always verify capacity availability before planning a deployment or purchasing a reservation.

To check real-time capacity availability:
- Use the **Foundry portal deployment experience**, which surfaces capacity status inline when you configure a deployment.
- Use the [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list) to programmatically query the maximum deployable PTU count for a given model and region. The API factors in your current quota and service capacity in the region.

For guidance on finding available capacity and handling situations where capacity isn't available, see [Capacity and availability](#capacity-and-availability).

## Deployment types that support provisioned throughput

Provisioned throughput is available as three deployment types. They all provide the same predictable latency and dedicated capacity. The difference is where your inference traffic is processed:

| Deployment type | `sku-name` in CLI | Data routing | Best for |
|---|---|---|---|
| **Global Provisioned** | `GlobalProvisionedManaged` | Routed across Azure regions globally | Highest availability; when routing region isn't constrained |
| **Data Zone Provisioned** | `DataZoneProvisionedManaged` | Stays within a geographic zone (US or EU) | Zone-level data residency with higher availability than regional |
| **Regional Provisioned** | `ProvisionedManaged` | Stays in the deployment's specific Azure region | Strict single-region data residency requirements |

> [!NOTE]
> New models sold directly by Azure are typically onboarded with the Global Provisioned type first. Data Zone Provisioned support follows. See [Supported models](#supported-models) for current availability by deployment type.

For a full comparison of all Foundry deployment types—including standard, batch, and provisioned—see [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md).

## Supported models

The following models support provisioned throughput deployment types. PTU quota and reservations are shared across all supported models within the same region and deployment type. The **Spillover** column indicates whether the model supports the [spillover feature](../how-to/spillover-traffic-management.md), which automatically redirects overflow requests from a fully utilized provisioned deployment to a standard deployment.

| Model family | Model | Global provisioned | Data zone provisioned | Regional provisioned | Spillover |
|---|---|:---:|:---:|:---:|:---:|
| **Azure OpenAI** | gpt-5.4 | ✅ |✅ |✅ | ✅ |
| | gpt-5.3-codex | ✅ | | | ✅ |
| | gpt-5.2 | ✅ |✅ |✅ | ✅ |
| | gpt-5.2-codex | ✅ | | | ✅ |
| | gpt-5.1 | ✅ | ✅ |✅ | ✅ |
| | gpt-5.1-codex | ✅ | ✅ | | ✅ |
| | gpt-5 | ✅ | ✅ | ✅ | ✅ |
| | gpt-5-mini | ✅ | ✅ | ✅ | ✅ |
| | gpt-4.1 | ✅ | ✅ | ✅ | ✅ |
| | gpt-4.1-mini | ✅ | ✅ | ✅ | ✅ |
| | gpt-4.1-nano | ✅ | ✅ | ✅ | ✅ |
| | gpt-4o | ✅ | ✅ | ✅ | ✅ |
| | gpt-4o-mini | ✅ | ✅ | ✅ | ✅ |
| | gpt-3.5-turbo | ✅ | ✅ | ✅ | ✅ |
| | o1 | ✅ | ✅ | ✅ | ✅ |
| | o3 | ✅ | ✅ | ✅ | ✅ |
| | o3-mini | ✅ | ✅ | ✅ | ✅ |
| | o4-mini | ✅ | ✅ | ✅ | ✅ |
| **Azure DeepSeek** | DeepSeek-R1 | ✅ | | | |
| | DeepSeek-V3-0324 | ✅ | | | |
| | DeepSeek-R1-0528 | ✅ | | | |
| **Meta Llama** | Llama-3.3-70B-Instruct | ✅ | | | |

> [!NOTE]
> The model version isn't listed in this table. Check supported versions for each model in the Foundry portal when you configure a deployment. Regional provisioned availability varies by region.

### Region availability for provisioned throughput capability

Region availability for provisioned throughput is listed in the following tables.

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


## Billing

Provisioned deployments support two billing modes: hourly billing for flexible, short-term usage, and Azure Reservations for sustained production workloads at a discounted rate.

### Hourly billing

All provisioned deployment types are billed at an hourly rate ($/PTU/hr) based on the number of PTUs deployed—not on tokens consumed. The meter starts when the deployment is created and stops when it's deleted. Hourly billing is practical for short-term scenarios like benchmarking a new model or temporarily scaling up for an event such as a hackathon.

> [!IMPORTANT]
> Don't plan to scale provisioned deployments up and down with traffic to stay on hourly billing. Capacity isn't always available when you need to scale back up, and continuous hourly billing at high utilization typically exceeds reservation pricing.

### Azure Reservations

Azure Reservations are a financial discount applied to the PTU billing meter, not to individual deployments. In exchange for a 1-month or 1-year commitment, you receive a discounted effective $/PTU/hr rate. Reservations are purchased per deployment type (Global, Data Zone, or Regional) and can be scoped to cover one or more subscriptions or resource groups.

Reservations and deployments are loosely coupled—you create or delete deployments and reservations independently.

> [!NOTE]
> Reservations don't guarantee capacity. Create deployments first to confirm that capacity is available, then purchase the reservation to lock in the discounted rate.

For complete guidance—including how to size and purchase a reservation, how billing matches deployments to reservations, and how to monitor utilization—see [Azure Reservations for provisioned throughput](../how-to/provisioned-throughput-onboarding.md#azure-reservations-for-provisioned-throughput).

## Capacity and availability

Provisioned capacity is allocated at deployment time. If service capacity isn't available, the deployment fails. Once capacity is allocated, it's held for the deployment's lifetime.
Because GPU capacity is a finite, dynamically changing resource:

- **Capacity availability changes throughout the day** based on customer demand across all regions and models.
- **Deleting a deployment or scaling it down releases its capacity** back to the region pool. There's no guarantee that the same capacity is available if you re-create the deployment or scale it up later, as capacity might have been claimed by other deployments.
- **Quota doesn't guarantee capacity**. A subscription can have PTU quota in a region with no available GPU capacity at a given moment.

If your target region doesn't have available capacity:
- Try deploying with fewer PTUs.
- Try a different region where quota is also available. The [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list) and Foundry experience consider quota availability in returning alternative regions for creating a deployment.
- Retry later—capacity availability changes dynamically and more might become available.


## Utilization and HTTP 429 responses

Once a provisioned deployment is running, the service tracks utilization using a leaky bucket algorithm:

1. The service estimates each incoming request's expected compute cost — the incremental utilization change needed to serve it — by combining the prompt token count, less any cached tokens, and the specified `max_tokens` parameter. A customer can receive up to a 100% discount on prompt tokens depending on cached token volume. If `max_tokens` isn't specified, the service estimates a value. This estimation can lead to lower concurrency than expected when actual generated tokens are fewer than assumed. For highest concurrency, set `max_tokens` as close as possible to the true generation size.
1. If current utilization is at 100%, the service returns **HTTP 429** immediately, with the `retry-after-ms` and `retry-after` headers indicating how long to wait.
1. Utilization drains continuously at a rate proportional to deployed PTUs. A deployment with more PTUs drains utilization faster, which means it recovers capacity more quickly between requests and can sustain a higher overall request rate.
1. When a request finishes, the service corrects the utilization estimate using actual token counts. If the actual cost is greater than the estimate, the difference is added to the deployment's utilization. If the actual cost is less than the estimate, the difference is subtracted.

Accepted requests always complete with predictable latency, because 429 responses are returned immediately rather than queuing traffic. A 429 from a provisioned deployment is a traffic-management signal—not an error indicating a service problem.

> [!NOTE]
> Calls are accepted until utilization reaches 100%. Bursts just over 100% might be permitted in short periods, but over time, your traffic is capped at 100% utilization.

:::image type="content" source="../media/provisioned/utilization.jpg" alt-text="Diagram of the leaky bucket algorithm for provisioned throughput utilization showing how incoming requests add to utilization while capacity drains based on deployed PTU count." lightbox="../media/provisioned/utilization.jpg":::

### How to handle HTTP 429 responses

In all provisioned deployment types, when capacity is exceeded, the API returns a HTTP 429 status code. The HTTP 429 response isn't an error, but instead it's part of the design for telling users that a given PTU deployment is fully utilized at a point in time. The service continues to return the HTTP 429 status code until the utilization drops below 100%. By providing a fast-fail response, you have control over how to handle these situations in a way that best fits your application requirements.

Here are some strategies for handling the HTTP 429 response:

- **Redirect to a standard deployment or another model**: This option produces the lowest additional latency, because the action can be taken as soon as you receive the 429 signal. The [spillover feature](../how-to/spillover-traffic-management.md) automates the process of redirecting the request from your provisioned deployment to your standard deployment for processing.
- **Retry using the wait time in the response header**: The `retry-after-ms` and `retry-after` headers in the response tell you the time to wait before the next call will be accepted. If you need the provisioned deployment and can tolerate added latency, implement client-side retry logic. The Foundry client libraries include built-in capabilities for handling retries.

### Concurrent call limits

The number of concurrent calls you can achieve on a deployment depends on each call's shape (prompt size, `max_tokens` parameter, and similar factors). The service continues to accept calls until the utilization reaches 100%. To determine the approximate number of concurrent calls, you can model out the maximum requests per minute for a particular call shape in the [capacity calculator](https://ai.azure.com/resource/calculator). If the system generates less than the number of output tokens set for the `max_tokens` parameter, then the provisioned deployment will accept more requests.


## Advanced topics

| What you want to do | Article | Type |
|---|---|---|
| Create a provisioned deployment, verify quota, handle 429s, run a benchmark | [Get started with provisioned deployments](../how-to/provisioned-get-started.md) | How-to |
| Understand hourly billing details, PTU-to-TPM ratios by model, PTU minimums, and reservation management | [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md) | How-to |
| Route overflow traffic to a standard deployment when a provisioned deployment is fully utilized | [Manage traffic with spillover](../how-to/spillover-traffic-management.md) | How-to |
| Optimize for latency, understand prompt size effects and call shape tradeoffs | [Performance and latency](../how-to/latency.md) | How-to |
| Migrate from the older Commitment purchase model | [Provisioned August update](../../../foundry-classic/openai/concepts/provisioned-migration.md) | Concept |

## Related content

- [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md)
- [Save costs with Microsoft Foundry Provisioned Throughput reservations](/azure/cost-management-billing/reservations/azure-openai)
- [Foundry Models quotas and limits](../../foundry-models/quotas-limits.md)
