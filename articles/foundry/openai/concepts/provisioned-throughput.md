---
title: "What is provisioned throughput for Foundry Models?"
description: "Learn how provisioned throughput gives you dedicated AI model capacity with predictable latency, how to size PTU deployments, and how quota, capacity, and billing work for provisioned throughput in Microsoft Foundry."
ai-usage: ai-assisted
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: concept-article
ms.date: 05/13/2026
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

Provisioned throughput is a model deployment type in Microsoft Foundry that allocates dedicated model processing capacity to your deployment. Unlike standard deployments—where inference capacity is shared across customers and throughput can vary with demand—a provisioned deployment holds a fixed amount of processing capacity exclusively for your use, whether or not requests are being made.

This article explains the core concepts behind provisioned throughput: what it is, when to use it, how capacity is measured and billed, and what to know about quota and capacity before you deploy.

## Deployment types compared

Standard deployments, priority processing, and provisioned throughput are three ways to deploy models in Microsoft Foundry. The right choice depends on your latency requirements, traffic patterns, and cost tolerance.

| Deployment type | Billing | Latency guarantee | Capacity | Best for |
|---|---|---|---|---|
| **Standard** | Pay per token | None | Shared pool | Development, testing, variable or unpredictable workloads |
| **Priority processing** | Pay per token (priority tier rate) | [Defined latency target per model](priority-processing.md) | Shared pool, priority queue | Bursty or business-hours traffic needing consistent low latency without a long-term commitment |
| **Provisioned** | Per [PTU](#provisioned-throughput-units) per hour | [Defined latency target per model](../how-to/provisioned-throughput-onboarding.md#throughput-and-deployment-parameter-values-by-model) | Dedicated once deployed; availability not guaranteed at deployment time | Sustained high-volume production workloads |

> [!NOTE]
> Priority processing is available on Global standard and Data Zone standard (US) deployments only, and uses the same quota as standard processing (see [Quota and capacity](#quota-and-capacity)). To learn about priority processing, see [Enable priority processing for Microsoft Foundry models](priority-processing.md).

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
- **Region-specific**: PTU quota is granted per subscription, per region, and per [deployment type](#deployment-types-that-support-provisioned-throughput). Quota in East US doesn't carry over to West Europe.
- **Throughput varies by model**: The tokens per minute (TPM) that a given number of PTUs delivers depends on the model. A heavier model requires more PTUs to serve the same TPM as a lighter one. For per-model PTU-to-TPM ratios, see [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md#how-much-throughput-per-ptu-you-get-for-each-model).
- **Minimum deployment sizes apply**: Each model has a minimum PTU count required to create a deployment. Minimums vary by model and are listed in [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md#how-much-throughput-per-ptu-you-get-for-each-model).

For details on PTU quota, capacity, and how to request more, see [Quota and capacity](#quota-and-capacity). Note that having PTU quota doesn't guarantee that capacity is available when you deploy—quota is a policy limit, not a capacity reservation.

## PTU sizing

Before creating a provisioned deployment, estimate how many PTUs your workload requires. PTU requirements depend on your expected requests per minute (RPM), prompt size, response size, and cache hit rate.

### Estimate PTU manually

Use your expected traffic and the per-model values from [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md#how-much-throughput-per-ptu-you-get-for-each-model) to estimate the PTUs your workload needs. The calculation converts your expected token volume into a single *converted input TPM* figure, then divides by the model's **Input TPM per PTU** value.

Before applying the formulas, note two key terms:

- The **output-to-input ratio** reflects how much more processing capacity an output token requires compared to an input token. For example, a ratio of 8 means one output token counts as 8 input tokens toward the model's TPM limit.
- The **cache rate** is the fraction of input tokens served from the prompt cache (0 if caching isn't used). Cached tokens are deducted 100% from the utilization calculation and don't consume PTU capacity.

**Formulas:**

- Input TPM = Peak RPM × prompt size (tokens)
- Output TPM = Peak RPM × response size (tokens)
- Converted input TPM = (input TPM × (1 − cache rate)) + (output-to-input ratio × output TPM)
- PTUs required = converted input TPM ÷ Input TPM per PTU

**Worked example:**

Suppose your application sends requests at a peak rate of 1,000 RPM with an average prompt size of 100 tokens and an average response size of 50 tokens, using the gpt-5.2 model. From the per-model table, gpt-5.2 has an Input TPM per PTU of 3,400 and an output-to-input ratio of 8.

- Input TPM = 1,000 × 100 = 100,000
- Output TPM = 1,000 × 50 = 50,000
- Converted input TPM = 100,000 + (8 × 50,000) = 500,000
- PTUs required = 500,000 ÷ 3,400 = 147.06 → **150 PTUs** (rounded up to the nearest 50 PTUs, matching the Regional Provisioned scale increment for gpt-5.2)

### Estimate PTU with the capacity calculator

Use the [capacity calculator](https://ai.azure.com/resource/calculator) in the Foundry portal to size specific workload shapes. Find the calculator under **Operate** > **Quota** > **Provisioned throughput unit**, then enter your workload parameters.

For full details on the formulas, per-model Input TPM per PTU values, output-to-input ratios, and the capacity calculator, see [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md#determine-ptu-requirements-for-a-workload).

## Deployment types that support provisioned throughput

Provisioned throughput is available as three deployment types. They all provide dedicated capacity and predictable latency once deployed. The difference is where your inference traffic is processed:

| Deployment type | `sku-name` in CLI | Data routing | Best for |
|---|---|---|---|
| **Global Provisioned** | `GlobalProvisionedManaged` | Routed across Azure regions globally | Highest availability; when routing region isn't constrained |
| **Data Zone Provisioned** | `DataZoneProvisionedManaged` | Stays within a geographic zone (US or EU) | Zone-level data residency with higher availability than regional |
| **Regional Provisioned** | `ProvisionedManaged` | Stays in the deployment's specific Azure region | Strict single-region data residency requirements |

> [!NOTE]
> New models sold directly by Azure are typically onboarded with the Global Provisioned type first. Data Zone Provisioned support follows. See [Supported models](#supported-models) for current availability by deployment type.

For a full comparison of all Foundry deployment types—including standard, batch, and provisioned—see [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md).

## Supported models

For the full list of models that support provisioned throughput—including which deployment types each model supports and regional availability—see [Region availability for Foundry Models sold directly by Azure](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=provisioned).

> [!NOTE]
> Check the Foundry portal for supported model versions when you configure a deployment. Regional provisioned availability varies by region.

> [!NOTE]
> The provisioned version of `gpt-4` **Version:** `turbo-2024-04-09` is currently limited to text only.

## Spillover

Spillover manages traffic fluctuations on provisioned deployments by automatically routing overflow requests to a corresponding standard deployment in the same Foundry resource. When a provisioned deployment is fully utilized and returns non-200 responses—such as a `429` when PTUs are exhausted—spillover redirects those requests to the standard deployment, helping reduce disruptions during traffic bursts.

All Azure OpenAI models that support provisioned throughput also support spillover. Models from other providers (Azure DeepSeek, Meta Llama) don't currently support spillover.

Spillover is optional and can be configured for all requests on a deployment or controlled on a per-request basis using the `x-ms-spillover-deployment` request header. Both the provisioned and standard deployments must reside in the same Foundry resource.

For configuration steps, see [Manage traffic with spillover for provisioned deployments](../how-to/spillover-traffic-management.md).

## Billing

Provisioned deployments support two billing modes: hourly billing for flexible, short-term usage, and Azure Reservations for sustained production workloads at a discounted rate.

### Hourly billing

All provisioned deployment types are billed at an hourly rate ($/PTU/hr) based on the number of PTUs deployed—not on tokens consumed. The meter starts when the deployment is created and stops when it's deleted. Hourly billing is practical for short-term scenarios like benchmarking a new model or temporarily scaling up for an event such as a hackathon.

> [!IMPORTANT]
> Don't plan to scale provisioned deployments up and down with traffic to stay on hourly billing. Capacity isn't always available when you need to scale back up, and continuous hourly billing at high utilization typically exceeds reservation pricing.

### Azure Reservations

Azure Reservations are a financial discount applied to the PTU billing meter (the hourly usage counter Azure charges against), not to individual deployments. In exchange for a 1-month or 1-year commitment, you receive a discounted effective $/PTU/hr rate. Reservations are purchased per deployment type (Global, Data Zone, or Regional) and can be scoped to cover one or more subscriptions or resource groups.

Reservations and deployments are loosely coupled—you create deployments and reservations independently.

> [!NOTE]
> Reservations don't guarantee capacity. Create deployments first to confirm that capacity is available, then purchase the reservation to lock in the discounted rate.

For complete guidance on sizing, purchasing, and managing reservations, see [Azure Reservations for provisioned throughput](../how-to/provisioned-throughput-onboarding.md#azure-reservations-for-provisioned-throughput).<!-- TODO: Update link to dedicated reservations article when published -->

## Quota and capacity

### What is PTU quota?

PTU quota is the maximum number of PTUs you can deploy per subscription, per region, and per deployment type. Quota is a policy limit enforced by Azure—it has no cost. Quota is scoped at the offering level (Global Provisioned, Data Zone Provisioned, and Regional Provisioned are separate quota pools) and at the region level. Quota in East US doesn't apply to West Europe.

A default amount of quota is assigned to eligible subscriptions in several regions.

### What is capacity?

Capacity is the actual GPU compute available to serve your deployment when you create it. Capacity is allocated at deployment time and held for the deployment's lifetime.

> [!IMPORTANT]
> Having PTU quota doesn't guarantee that capacity is available. If GPU capacity in the region is insufficient for the requested PTU count, the deployment fails. Always verify capacity availability before planning a deployment or purchasing a reservation.

Because GPU capacity is a finite, dynamically changing resource:

- **Capacity availability changes throughout the day** based on customer demand across all regions and models.
- **Deleting or scaling down a deployment releases its capacity** back to the region pool. There's no guarantee the same capacity is available if you re-create or scale the deployment up later.

### How to get quota

A default amount of global, data zone, and regional provisioned quota is assigned to eligible subscriptions in several regions. To request additional quota:

- Submit the [quota request form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu). You receive an email notification when the request is approved.
- In the Foundry portal, go to **Operate** > **Quota**, select the target subscription and region, then select **Request Quota** and complete the form.

### How to check available capacity

To check real-time capacity availability:

- Use the **Foundry portal deployment experience**, which surfaces capacity status inline when you configure a deployment and lists alternative regions with available capacity if your target region doesn't have enough.
- Use the [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list) to programmatically query the maximum deployable PTU count for a given model and region.

If your target region doesn't have available capacity:

- Try deploying with fewer PTUs.
- Try a different region where quota is available.
- Retry later—capacity availability changes dynamically throughout the day.

For step-by-step guidance on creating provisioned deployments and handling capacity constraints, see [Get started with provisioned deployments](../how-to/provisioned-get-started.md).

## How to see PTU costs

Use Azure Cost Management to track and analyze your PTU usage and reservation costs:

| What you want to do | Article |
|---|---|
| See what percentage of your reserved PTUs are actively in use across your deployments | [View Azure reservation utilization](/azure/cost-management-billing/reservations/reservation-utilization) |
| Review purchase history and any refund activity | [View Azure Reservation purchase and refund transactions](/azure/cost-management-billing/reservations/view-purchase-refunds) |
| Understand the amortized cost impact of your reservations for clearer per-deployment billing visibility | [View amortized benefit costs](/azure/cost-management-billing/reservations/view-amortized-costs) |
| Distribute reservation costs across teams or projects for internal cost attribution | [Charge back Azure Reservation costs](/azure/cost-management-billing/reservations/charge-back-usage) |
| Set up auto-renewal to prevent reservation expiry and maintain the discounted rate | [Automatically renew Azure reservations](/azure/cost-management-billing/reservations/reservation-renew) |

## Related content

- [Get started with provisioned deployments](../how-to/provisioned-get-started.md)
- [PTU costs and billing](../how-to/provisioned-throughput-onboarding.md)
- [Manage traffic with spillover for provisioned deployments](../how-to/spillover-traffic-management.md)
- [Enable priority processing for Microsoft Foundry models](priority-processing.md)
- [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md)
- [Save costs with Microsoft Foundry Provisioned Throughput reservations](/azure/cost-management-billing/reservations/azure-openai)
- [Foundry Models quotas and limits](../../foundry-models/quotas-limits.md)
- [Performance and latency](../how-to/latency.md)
- [Migrate from the Commitment purchase model](../../../foundry-classic/openai/concepts/provisioned-migration.md)
