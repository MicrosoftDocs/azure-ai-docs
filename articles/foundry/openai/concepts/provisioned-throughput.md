---
title: "Provisioned throughput for Foundry Models"
description: "Provisioned throughput in Microsoft Foundry gives you dedicated AI model capacity with predictable latency. Learn how to size PTU deployments, manage quota, and optimize billing."
ai-usage: ai-assisted
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.topic: concept-article
ms.date: 05/20/2026
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

Provisioned throughput is a deployment type in Microsoft Foundry that provides dedicated model processing throughput for your deployment. Unlike standard deployments, where inference capacity is shared across customers and throughput can vary with demand, a provisioned deployment holds a fixed amount of processing capacity exclusively for your deployment's use, whether or not requests are being made.

This article introduces the core concepts behind provisioned throughput: what it is, when to use it, how capacity is measured and billed, and what to know about quota and capacity before you deploy.

## Deployment categories compared

Standard deployments, batch deployments, priority processing, and provisioned throughput are ways to deploy models in Microsoft Foundry. The right choice depends on your latency requirements, traffic patterns, and cost tolerance.

| Deployment type | Billing | Latency Service Level Agreement (SLA) | Workload type and needs |
|---|---|---|---|
| **Standard** | Pay per token | None | Balanced workloads: development, testing, and production with variable or unpredictable traffic |
| **Priority processing** | Pay per token (priority tier rate) | [Defined latency target per model](priority-processing.md#latency-target) | Latency-sensitive production workloads needing consistent low latency without a long-term commitment |
| **Batch** | Pay per token (discounted batch rate) | None | Bulk processing workloads without latency requirements. Results are returned asynchronously. |
| **Provisioned** | Per [PTU](#provisioned-throughput-units) per hour (or using [Azure reservations](#azure-reservations)) | [Defined latency target per model](../how-to/determine-ptu-requirements.md#deployment-parameters-and-throughput-values-by-model) | Mission-critical, high-scale production workloads requiring guaranteed throughput and consistent latency |

## When to use provisioned throughput

Provisioned throughput is the right choice when your application has:

- **Predictable traffic patterns**: You have a reasonable estimate of requests per minute and token volumes.
- **Latency-sensitive requirements**: Your users or downstream systems need consistent, low-latency responses.
- **Production-scale volume**: High throughput use cases where per-token billing becomes expensive.
- **Real-time or interactive scenarios**: Chat applications, copilots, or agents where variable response times degrade user experience.

Standard deployments remain the better fit for development, testing, low-volume usage, or highly variable traffic that makes it difficult to size a deployment in advance.

## Provisioned throughput units

**Provisioned throughput units (PTUs)** are the unit of measure for provisioned throughput. A PTU represents a fixed amount of model processing capacity. When you create a provisioned deployment, you specify how many PTUs to allocate. Foundry reserves that amount of compute and holds it for your deployment.

Key characteristics of PTUs:

- **Model-independent**: The same PTU quota can be used to deploy any [supported model](#supported-models). You don't buy PTUs for a specific model.
- **Region-specific**: PTU quota is granted per subscription, per region, and per [deployment type](#provisioned-throughput-deployment-types). Quota in East US doesn't carry over to West Europe.
- **Throughput varies by model**: The tokens per minute (TPM) that a given number of PTUs delivers depends on the model. A heavier model requires more PTUs to serve the same TPM as a lighter one. For per-model PTU-to-TPM ratios, see [Per-model throughput parameters](../how-to/determine-ptu-requirements.md#deployment-parameters-and-throughput-values-by-model).
- **Minimum deployment sizes apply**: Each model has a minimum PTU count required to create a deployment. Minimums vary by model and are listed in [Deployment parameters and throughput values by model](../how-to/determine-ptu-requirements.md#deployment-parameters-and-throughput-values-by-model).

## Quota and capacity

PTU quota and capacity are related but distinct concepts that both affect whether you can create a deployment. This section explains what each is, how to request additional quota, and how to check whether capacity is available in your region.

### What is PTU quota?

PTU quota is the maximum number of PTUs you can deploy per subscription, per region, and per deployment type. Quota is a policy limit enforced by Azure, and it has no associated cost. Quota is scoped at the offering level (Global Provisioned, Data Zone Provisioned, and Regional Provisioned are separate quota pools) and at the region level (for example, quota in East US doesn't apply to West Europe).

A default amount of quota is assigned to eligible subscriptions in several regions.

### What is capacity?

Capacity is the actual GPU compute available to serve your deployment when you create it. Capacity is allocated at deployment time and held for the deployment's lifetime.

> [!IMPORTANT]
> Having PTU quota doesn't guarantee that capacity is available. If GPU capacity in the region is insufficient for the requested PTU count, the deployment fails. Always [verify capacity availability](#how-to-check-available-capacity) before planning a deployment or purchasing a reservation.

Because GPU capacity is a finite, dynamically changing resource:

- **Capacity availability changes throughout the day** based on customer demand across all regions and models.
- **Deleting or scaling down a deployment releases its capacity** back to the region pool. There's no guarantee the same capacity is available if you re-create or scale the deployment up later.

### How to get quota

A default amount of global, data zone, and regional provisioned quota is assigned to eligible subscriptions in several regions. There are two ways to request additional quota:

- Submit the [quota request form](https://aka.ms/oai/stuquotarequest) to request quota or capacity.

- In the Foundry portal, go to **Operate** > **Quota**, select the target subscription and region, then select **Request Quota** and complete the form.

Approval might take several days based on quota availability, and you receive an email notification when the request is approved.

### How to check available capacity

To check real-time capacity availability:

- Use the **Foundry portal deployment experience**, which tells you if capacity is available when you try to create a deployment and lists alternative regions with available capacity if your target region doesn't have enough.
- Use the [model capacities API](/rest/api/aiservices/accountmanagement/model-capacities/list) to programmatically query the maximum deployable PTU count for a given model and region.

If your target region doesn't have available capacity:

- Try deploying with fewer PTUs.
- Try a different region where quota is available.
- Retry later, as capacity availability changes dynamically throughout the day.
- Submit the [quota request form](https://aka.ms/oai/stuquotarequest) to request more quota or capacity.

For step-by-step guidance on creating provisioned deployments and handling capacity constraints, see [Get started with provisioned deployments](../how-to/provisioned-get-started.md).

## PTU sizing

Before creating a provisioned deployment, estimate how many PTUs your workload requires. Three factors drive the calculation:

- **Request shape**: Your expected requests per minute (RPM), average prompt size (input tokens), and average response size (output tokens).
- **Output-to-input ratio**: Output tokens require more processing capacity than input tokens. Each model has a ratio that expresses how many input tokens one output token is equivalent to for capacity purposes. For GPT-4.1 and later Azure OpenAI models, this ratio matches the model's global standard pricing ratio between output and input tokens. A model that costs more per output token has a higher ratio. Some models use a [ratio that differs from their pricing ratio](../how-to/determine-ptu-requirements.md#models-with-a-non-standard-output-to-input-ratio).
- **Cache rate**: The fraction of input tokens served from the prompt cache. Cached tokens don't consume PTU capacity, so a higher cache rate reduces the PTUs required.

The sizing calculation uses these factors to convert your expected token volumes into a single **normalized TPM** figure, then divides by the model's **Input TPM per PTU** value to arrive at the required PTU count.

You can size manually, using the formulas and per-model values, or use the [capacity calculator](https://ai.azure.com/resource/calculator) in the Foundry portal (navigate to **Operate** > **Quota** > **Provisioned throughput unit**) for a guided estimate.

For the complete sizing methodology that includes formulas, worked examples with cache variation, and the full capacity calculator reference, see [Determine PTU requirements for a workload](../how-to/determine-ptu-requirements.md).

## Provisioned throughput deployment types

Provisioned throughput is available as three deployment types. They all provide dedicated capacity and predictable latency once deployed. The difference is where your inference traffic is processed:

| Deployment type | `sku-name` in CLI | Data routing | Best for |
|---|---|---|---|
| **Global Provisioned** | `GlobalProvisionedManaged` | Routed across Azure regions globally | Highest availability; when routing region isn't constrained |
| **Data Zone Provisioned** | `DataZoneProvisionedManaged` | Stays within a geographic zone (US or EU) | Zone-level data residency with higher availability than regional |
| **Regional Provisioned** | `ProvisionedManaged` | Stays in the deployment's specific Azure region | Strict single-region data residency requirements |

For a full comparison of all Foundry deployment types, including standard, batch, and provisioned, see [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md).

## Supported models

For a full list of Foundry Models that support provisioned throughput, including which deployment types each model supports and regional availability, see [Region availability for Foundry Models sold directly by Azure](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=provisioned).

## Spillover

Spillover is an optional configuration for managing traffic fluctuations on provisioned deployments by automatically routing overflow requests to a corresponding standard deployment in the same Foundry resource. When a provisioned deployment is fully utilized and returns non-200 responses (such as a `429` when PTUs are exhausted), spillover redirects those requests to the standard deployment, helping reduce disruptions during traffic bursts.

All Azure OpenAI in Foundry Models that support provisioned throughput also support spillover. Foundry Models from other providers (Azure DeepSeek, Meta Llama) don't currently support spillover.

Spillover can be configured for all requests on a deployment or controlled on a per-request basis using the `x-ms-spillover-deployment` request header. For configuration steps, see [Manage traffic with spillover for provisioned deployments](../how-to/spillover-traffic-management.md).

## Hourly billing and Azure reservations

Provisioned deployments support two billing modes: *hourly billing* for flexible, short-term usage, and *Azure Reservations* for sustained production workloads at a discounted rate.

### Hourly billing

All provisioned deployment types are billed at an hourly rate ($/PTU/hr) based on the number of PTUs deployed, regardless of the number of tokens consumed. The meter starts when the deployment is created and stops when it's deleted.

Hourly billing is practical for short-term scenarios like benchmarking a new model or temporarily scaling up for an event such as a hackathon. However, don't plan to scale provisioned deployments up and down with traffic to stay on hourly billing for these reasons:

- Capacity might not be available when you need to scale back up.

- Continuous hourly billing at high utilization typically exceeds reservation pricing.

For complete guidance on hourly billing and scaling provisioned deployments, see [Hourly billing](./provisioned-throughput-billing.md#hourly-billing).

### Azure reservations

Azure Reservations are a financial discount applied to the PTU billing meter (the hourly usage counter Azure charges against), not to individual deployments. In exchange for a 1-month or 1-year commitment, you receive a discounted effective $/PTU/hr rate. Some key things to note about reservations include:

- Reservations are purchased per deployment type (Global, Data Zone, or Regional) and can be scoped to cover one or more subscriptions or resource groups.

- Reservations and deployments are loosely coupled, meaning that you create deployments and reservations independently.

- Reservations don't guarantee capacity. First create deployments to confirm that capacity is available, then purchase the reservation to lock in the discounted rate.

For complete guidance on sizing, purchasing, and managing reservations, see [Azure Reservations for provisioned throughput](./provisioned-throughput-billing.md#azure-reservations-for-provisioned-throughput).

## How to track PTU costs and billing

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
- [PTU costs and billing](./provisioned-throughput-billing.md)
- [Manage traffic with spillover for provisioned deployments](../how-to/spillover-traffic-management.md)
- [Enable priority processing for Microsoft Foundry models](priority-processing.md)
- [Save costs with Microsoft Foundry Provisioned Throughput reservations](/azure/cost-management-billing/reservations/azure-openai)
- [Foundry Models quotas and limits](../../foundry-models/quotas-limits.md)