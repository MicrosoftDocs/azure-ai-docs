---
title: "What is provisioned throughput for Foundry Models?"
description: "Learn how provisioned throughput gives you dedicated AI model capacity with predictable latency, how PTUs and quota relate, and when to use it over standard deployments."
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 04/03/2026
ms.custom:
  - dev-focus, pilot-ai-workflow-jan-2026
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

In a standard deployment, your requests draw from a shared pool of model processing capacity. This model works well for exploratory or variable workloads. Under heavy demand, however, latency and throughput can vary, and you might encounter rate limits before your quota is exhausted.

A provisioned throughput deployment gives you:

- **Predictable latency**: Accepted requests are processed with a consistent per-call maximum latency, because no other customer's traffic competes for your capacity.
- **Dedicated capacity**: The allocated compute is held for your deployment and doesn't fluctuate with broader service demand.
- **No shared rate limits**: Your requests won't be throttled because of other customers' traffic spikes.
- **Cost efficiency at scale**: For sustained high-volume workloads, reserved capacity is typically more cost-effective than per-token billing.

The tradeoff is that you commit to a capacity level upfront—and you're billed for it hourly regardless of actual utilization.

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

**Provisioned throughput units (PTUs)** are the unit of measure for provisioned capacity. A PTU represents a fixed amount of model processing capacity—similar in concept to a vCPU for a virtual machine. When you create a provisioned deployment, you specify how many PTUs to allocate. Foundry reserves that amount of compute and holds it for your deployment.

Key characteristics of PTUs:

- **Model-independent**: The same PTU quota can be used to deploy any [supported model](#supported-models). You don't buy PTUs for a specific model.
- **Region-specific**: PTU quota is granted per subscription, per region. Quota in East US doesn't carry over to West Europe.
- **Throughput varies by model**: The tokens per minute (TPM) that a given number of PTUs delivers depends on the model. A heavier model requires more PTUs to serve the same TPM as a lighter one. For per-model PTU-to-TPM ratios, see [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md#how-much-throughput-per-ptu-you-get-for-each-model).

### PTU quota vs. capacity

Quota and capacity are related but distinct:

| Concept | What it means |
|---|---|
| **PTU quota** | The maximum number of PTUs you're allowed to deploy in a subscription and region. Quota is a policy limit enforced by Azure. |
| **Capacity** | The actual GPU compute available to serve your deployment when you create it. Capacity is allocated at deployment time and held for the deployment's lifetime. |

> [!IMPORTANT]
> Having PTU quota doesn't guarantee that capacity is available. If GPU capacity in the region is insufficient for the requested PTU count, the deployment fails. Always verify capacity availability before planning a deployment or purchasing a reservation.

To check real-time capacity availability:
- Use the **Foundry portal deployment experience**, which surfaces capacity status inline when you configure a deployment.
- Use the [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list?view=rest-aiservices-accountmanagement-2024-04-01-preview&tabs=HTTP) to programmatically query the maximum deployable PTU count for a given model and region, factoring in your current quota.

## Deployment types that support provisioned throughput

Provisioned throughput is available as three deployment types. They all provide the same predictable latency and dedicated capacity. The difference is where your inference traffic is processed:

| Deployment type | `sku-name` in CLI | Data routing | Best for |
|---|---|---|---|
| **Global Provisioned** | `GlobalProvisionedManaged` | Routed across Azure regions globally | Highest availability; when routing region isn't constrained |
| **Data Zone Provisioned** | `DataZoneProvisionedManaged` | Stays within a geographic zone (US or EU) | Zone-level data residency with higher availability than regional |
| **Regional Provisioned** | `ProvisionedManaged` | Stays in the deployment's specific Azure region | Strict single-region data residency requirements |

> [!NOTE]
> New models sold directly by Azure are typically onboarded with the Global Provisioned type first. Data Zone Provisioned and Regional Provisioned support follows. See [Supported models](#supported-models) for current availability by deployment type.

For a full comparison of all Foundry deployment types—including standard, batch, and provisioned—see [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md).

## Billing

### Hourly billing

Provisioned deployments are billed hourly at a rate of $/PTU/hr based on the number of PTUs deployed—not on tokens consumed. The meter runs from the moment the deployment exists.

- A 300 PTU deployment is charged: hourly rate × 300.
- A deployment that exists for 15 minutes during an hour is charged at 1/4 of the hourly rate.
- If you resize the deployment, billing adjusts to the new PTU count.

Hourly billing is practical for short-term scenarios like benchmarking a new model or temporarily scaling up for an event. For sustained production workloads, purchasing an Azure Reservation is significantly more cost-effective.

> [!IMPORTANT]
> Don't plan to scale provisioned deployments up and down with traffic to stay on hourly billing. Capacity isn't always available when you need to scale back up, and the cost of continuous hourly billing at high utilization typically exceeds reservation pricing.

### Azure Reservations

**Azure Reservations** are a term-discount mechanism applied to the PTU billing meter. In exchange for a 1-month or 1-year commitment, you receive a discounted effective $/PTU/hr rate. Reservations apply automatically—no per-deployment configuration is required.

Key facts:

- **Purchased per deployment type**: Global, Data Zone, and Regional reservations are separate purchases. A Global Provisioned reservation doesn't cover a Regional Provisioned deployment.
- **Flexibly scoped**: A reservation can cover a resource group, subscription, management group, or billing account. All matching deployments within the scope share the discount, up to the reservation's PTU quantity.
- **Model-independent**: The discount applies to any model deployed with PTUs under the matching reservation. You don't purchase a reservation for a specific model.
- **Excess is billed hourly**: If deployed PTUs in scope exceed the reservation quantity, the excess PTUs are charged at the standard hourly rate.
- **Reservations don't guarantee capacity**: Purchasing a reservation doesn't reserve GPU capacity. Create deployments first to confirm capacity, then purchase the reservation.

#### Shared reservation example

You have a 500 PTU Global Provisioned reservation in East US 2. Your deployments currently consume 300 PTUs for Azure OpenAI models. You add a DeepSeek-R1 deployment:

| Scenario | DeepSeek PTUs added | Covered by reservation | Hourly overage |
|---|---|---|---|
| Add 200 PTUs for DeepSeek-R1 | 200 | All 200 (200 PTUs remaining in reservation) | None — total = 500 PTU |
| Add 300 PTUs for DeepSeek-R1 | 300 | 200 (reservation exhausted at 500 total) | 100 PTUs billed hourly |

The discount is shared automatically across all models in scope. You don't reconfigure the reservation when you add a new model.

To purchase or manage reservations, visit the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations). For pricing, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

## Capacity and availability

Provisioned capacity is allocated at deployment time and held for the deployment's lifetime. Because GPU capacity is a finite, dynamically changing resource:

- **Capacity availability changes throughout the day** based on customer demand across all regions and models.
- **Deleting a deployment releases its capacity** back to the region pool. There's no guarantee that the same capacity is available if you re-create the deployment later.
- **Scaling down also releases capacity**. Re-scaling up later might fail if capacity has been claimed by other deployments.
- **Quota doesn't hold capacity**. A subscription can have PTU quota in a region with no available GPU capacity at a given moment.

If your target region doesn't have available capacity:
- Try deploying with fewer PTUs.
- Try a different region where your quota is also available.
- Retry later—capacity availability changes dynamically and more might become available.

## Utilization and HTTP 429 responses

Once a provisioned deployment is running, the service tracks utilization using a leaky bucket algorithm:

1. Each incoming request is evaluated for its expected compute cost, based on prompt token count, `max_tokens`, and model.
2. If current utilization is at 100%, the service returns **HTTP 429** immediately, with `retry-after-ms` and `retry-after` headers indicating how long to wait.
3. Utilization drains continuously at a rate proportional to deployed PTUs.
4. When a request finishes, the service corrects the utilization estimate using actual token counts.

Accepted requests always complete with predictable latency, because 429 responses are returned immediately rather than queuing traffic. A 429 from a provisioned deployment is a traffic-management signal—not an error indicating a service problem.

### How to handle HTTP 429 responses

- **Redirect to a standard deployment**: This produces the lowest additional latency, because the action is taken as soon as the 429 is received. The [spillover feature](../how-to/spillover-traffic-management.md) automates this pattern.
- **Retry using the wait time in the response header**: Use the value from `retry-after-ms` if you need the provisioned deployment and can tolerate added latency. The Azure OpenAI client libraries include built-in retry logic that respects `retry-after` by default.

## Supported models

The following models support provisioned throughput deployment types. PTU quota and reservations are shared across all supported models within the same region and deployment type.

| Model family | Model | Global provisioned | Data zone provisioned | Regional provisioned | Spillover |
|---|---|:---:|:---:|:---:|:---:|
| **Azure OpenAI** | gpt-5.2 | ✅ | | | ✅ |
| | gpt-5.1 | ✅ | ✅ | | ✅ |
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

For per-region capacity tables, see [Get started with provisioned deployments](../how-to/provisioned-get-started.md).

## Next steps and advanced topics

| What you want to do | Article | Type |
|---|---|---|
| Create a provisioned deployment, verify quota, handle 429s, run a benchmark | [Get started with provisioned deployments](../how-to/provisioned-get-started.md) | How-to |
| Understand hourly billing details, PTU-to-TPM ratios by model, PTU minimums, and reservation management | [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md) | How-to |
| Route overflow traffic to a standard deployment when a provisioned deployment is fully utilized | [Manage traffic with spillover](../how-to/spillover-traffic-management.md) | How-to |
| Optimize for latency, understand prompt size effects and call shape tradeoffs | [Performance and latency](../how-to/latency.md) | How-to |
| Migrate from the older Commitment purchase model | [Provisioned August update](../../../../foundry-classic/openai/concepts/provisioned-migration.md) | Concept |

## Related content

- [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md)
- [Save costs with Microsoft Foundry Provisioned Throughput reservations](/azure/cost-management-billing/reservations/azure-openai)
- [Foundry Models quotas and limits](../../foundry-models/quotas-limits.md)
