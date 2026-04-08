---
title: "Provisioned throughput unit (PTU) costs and billing"
description: "Learn how PTU billing works, choose between hourly billing and Azure Reservations, size your reservation, and monitor usage to control costs for provisioned throughput deployments in Microsoft Foundry."
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 04/07/2026
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
#customerIntent: As a developer deploying provisioned throughput in Microsoft Foundry, I want to understand PTU billing, choose the right billing mode, size and manage reservations, and monitor usage so I can control costs and avoid unexpected charges.
---

# Provisioned throughput unit (PTU) costs and billing

Provisioned throughput deployments in Microsoft Foundry support hourly billing for flexible, short-term usage, and Azure Reservations for sustained production workloads at a discounted rate. This article explains how Provisioned Throughput Units (PTU) billing works, helps you choose between hourly billing and Azure Reservations, and covers how to size and monitor reservations to keep costs predictable.

If you're new to provisioned throughput, start with [What is provisioned throughput?](../concepts/provisioned-throughput.md). When you're ready to create your first deployment, see [Get started with provisioned deployments](./provisioned-get-started.md).

> [!NOTE]
> In function calling and agent scenarios, token usage can be variable. Understand your expected tokens per minute (TPM) usage in detail before migrating those workloads to PTU.

## How PTU billing works

**Provisioned throughput units (PTUs)** are generic units of model processing capacity. When you create a provisioned deployment, you specify how many PTUs to allocate. Foundry reserves and holds that PTU capacity for the deployment, and you're charged for it hourly whether or not the deployment is handling requests. In other words, you're billed hourly based on the number of Provisioned Throughput Units (PTUs) you deploy—not on tokens consumed.

PTU billing has two important characteristics:

- **Model-independent**: Your [PTU quota](../concepts/provisioned-throughput.md#ptu-quota-vs-capacity) is shared across all supported models in a region and deployment type. The same PTU pool can be used to deploy any supported model. You don't buy PTUs for a specific model.
- **Billed on deployed capacity, not token consumption**: Unlike pay-per-token billing, you pay for reserved capacity. Requests that complete successfully consume that capacity, but you're billed for the full deployed PTU count regardless of actual utilization. 

:::image type="content" source="../media/provisioned/model-independent-quota.png" alt-text="Diagram of model independent quota with one pool of PTUs available to multiple Azure OpenAI models." lightbox="../media/provisioned/model-independent-quota.png":::

PTU quota for each provisioned deployment type appears in the Foundry portal's **Operate** section > **Quota** pane, and maps to these quota names:

| Deployment type | Quota name |
|---|---|
| [Regional Provisioned](../../foundry-models/concepts/deployment-types.md#regional-provisioned) | Regional Provisioned Throughput Unit |
| [Global Provisioned](../../foundry-models/concepts/deployment-types.md#global-provisioned) | Global Provisioned Throughput Unit |
| [Data Zone Provisioned](../../foundry-models/concepts/deployment-types.md#data-zone-provisioned) | Data Zone Provisioned Throughput Unit |

<!-- > [!NOTE]
> Quota doesn't guarantee capacity. Deploy your model in Foundry before purchasing a matching reservation in the Azure portal. -->

Provisioned deployments support two billing modes: hourly billing for flexible, short-term usage, and Azure Reservations for sustained production workloads at a discounted rate.

> [!NOTE]
> Foundry provisioned customers onboarded before the August 2024 self-service update use a purchase model called the Commitment model. These customers can continue to use the Commitment model alongside hourly/reservation billing. The Commitment model isn't available for new customers or [certain models introduced after August 2024](../../../foundry-classic/openai/concepts/provisioned-migration.md#supported-models-on-commitment-payment-model). For details on the Commitment purchase model and options for coexistence and migration, see [Foundry Provisioned August Update](../../../foundry-classic/openai/concepts/provisioned-migration.md).

## Hourly billing

Provisioned deployments (Regional, Data Zone, and Global) are charged at an hourly rate ($/PTU/hr) based on the number of PTUs deployed. For example, a 300 PTU deployment is charged at: hourly rate × 300.

If a deployment exists for only part of an hour, it receives a prorated charge:

- A deployment that exists for 15 minutes is charged at 1/4 of the hourly rate.
- If you resize the deployment, billing adjusts to the new PTU count immediately.

:::image type="content" source="../media/provisioned/hourly-billing.png" alt-text="A diagram showing hourly billing for provisioned deployments, where cost is determined by PTU count and hours deployed." lightbox="../media/provisioned/hourly-billing.png":::

### When to use hourly billing

Hourly billing is appropriate for short-term scenarios such as:

- Benchmarking model quality or performance before committing to a reservation.
- Temporarily scaling PTU capacity for an event such as a hackathon.

<!-- For all Azure pricing, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/). -->

Hourly billing isn't recommended for deployments in production—use reservations instead. Reasons why you shouldn't plan to use hourly billing with scaling production deployments up and down as traffic changes include:

- **Cost**: Azure Reservations provide significant discounts. Maintaining a deployment sized for full production volume under a reservation is typically less expensive than continuous hourly billing with the deployment scaled up or down for incoming traffic.
- **Capacity risk**: Unused quota doesn't guarantee that capacity is available when you want to scale back up your PTU deployment. Provisioned capacity is a finite, dynamically changing resource. A scale-down/scale-up strategy can leave you without capacity when you need it most.

## Azure Reservations for provisioned throughput

An Azure Reservation is a term-discounting mechanism shared by many Azure products. For example, Compute and Cosmos DB. Azure Reservations for provisioned throughput (Regional, Data Zone, and Global) are a financial discount applied to PTU billing meters—not to service interactions like deployment creation. In exchange for committing to payment for a fixed number of PTUs over a one-month or one-year term, you receive a discounted effective $/PTU/hr rate. The discount makes reservations significantly more cost-effective than long-term hourly billing for sustained workloads.

Reservations and deployments are loosely coupled: you create or delete deployments and reservations independently. This flexibility lets you change resources, subscriptions, or deployments without changing your billing construct.

> [!IMPORTANT]
> Capacity availability for model deployments is dynamic and changes frequently across regions and models. Always create deployments first, then purchase the Azure Reservation to cover the PTUs you've deployed. This approach ensures you receive the full reservation discount and protects you from committing to a reservation for PTUs you can't deploy.

Key reservation facts:

- **Purchased in the Azure portal**: Azure Reservations are purchased via the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations).
- **Purchased per deployment type**: Global Provisioned, Data Zone Provisioned, and Regional Provisioned reservations are separate purchases. A Global Provisioned reservation doesn't cover a Regional Provisioned deployment.
- **Flexibly scoped**: A reservation can cover an individual resource group or subscription, a group of subscriptions in a management group, or all subscriptions in a billing account. All matching deployments within the covered scope share the discount, up to the reservation's PTU quantity. See [How reservation matching works](#how-reservation-matching-works).
- **Overlapping and updatable**: New reservations can be purchased to cover the same scope as existing reservations, allowing you to discount new provisioned deployments. The scope of existing reservations can be updated at any time without penalty—for example, to cover a new subscription.
- **Model-independent**: The reservation discount applies to any supported model deployed within the matching scope. You don't purchase a reservation for a specific model. When you add a new model to your deployment portfolio, the existing reservation covers it automatically if it falls within scope.
- **Excess is billed hourly**: If deployed PTUs in scope exceed the reservation quantity, the excess PTUs are charged at the standard hourly rate. See [Reservation overage example](#reservation-overage-example).
- **Reservations don't guarantee capacity**: Purchasing a reservation doesn't reserve capacity on the service. Create deployments first to confirm that capacity is available, then purchase the reservation.
- **Cancelable, with limits**: Reservations can be canceled or exchanged after purchase, but those actions might incur fees.

### How reservation matching works

The discount applies automatically when all three conditions match between a running deployment and a reservation:

| Condition | What must match |
|---|---|
| Deployment type | Global, Data Zone, or Regional—must match exactly |
| Region | The Azure region of the deployment |
| Scope | The reservation scope must include the deployment's subscription or resource group |

Matching isn't by model or deployment ID. Multiple deployments that satisfy all three conditions share the same reservation up to its PTU quantity.

### Reservation overage example

You have a 500 PTU Global Provisioned reservation in East US 2. Your existing deployments consume 300 PTUs across Azure OpenAI models. You add a DeepSeek-R1 deployment:

| DeepSeek PTUs added | Covered by reservation | Hourly overage |
|---|---|---|
| 200 PTUs | All 200 (200 PTUs remaining in reservation) | None—total = 500 PTUs |
| 300 PTUs | 200 (reservation exhausted at 500 total) | 100 PTUs billed hourly until deployment sizes are reduced to 500 PTUs, or a new reservation is created to cover the remaining 100. |

The discount is shared automatically across all models in scope. You don't reconfigure the reservation when you add a new model.

> [!IMPORTANT]
> The Azure role and tenant policy requirements to purchase a reservation differ from those needed to create a Foundry deployment or resource. Verify authorization to purchase reservations before you need to do so. See [Foundry Provisioned Throughput reservations](https://aka.ms/oai/docs/ptum-reservations) for role requirements and purchase steps.

To purchase or manage reservations, go to the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations).

## Avoid unwanted charges

Billing begins the moment a provisioned deployment is created and stops when it's deleted. Follow these practices to avoid unexpected costs.

### Delete deployments before deleting resources

> [!IMPORTANT]
> Charges for deployments on a deleted resource continue until the resource is purged. Always delete all deployments from a resource before you delete the resource itself.
>
> If you already deleted the resource without removing its deployments first, you can recover or purge the resource to stop billing. See [Recover or purge deleted Azure AI resources](../../../ai-services/recover-purge-resources.md) for instructions.

To delete a provisioned deployment cleanly:

1. In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), navigate to the resource and delete the deployment.
1. If you're removing the Azure resource too, delete all its deployments first, then delete the resource.
1. Purge the resource to ensure billing stops. See [Recover or purge deleted Azure AI resources](../../../ai-services/recover-purge-resources.md) for instructions.
1. Go to the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations) to review your existing reservations. Deleting a deployment doesn't cancel or change any PTU reservation. You can cancel or exchange reservations in the Azure portal, but those actions might incur fees.

### Follow the recommended order of operations for reservations

To avoid purchasing a reservation for capacity that doesn't exist or that doesn't match your deployed PTUs:

1. Use Foundry to deploy your model in a region with available quota. This step confirms capacity is available—quota doesn't equal capacity.
1. After deployment, share deployment details—deployment type (Global Provisioned, Data Zone Provisioned, or Regional Provisioned), region, and subscription—with your Azure reservation admin.
1. The admin purchases a new reservation that matches the deployment details, or verifies that an existing reservation already covers the deployment.

## How much throughput per PTU you get for each model

The throughput (measured as tokens per minute, or TPM) that a deployment gets per PTU depends on both the model and the mix of input and output tokens in a minute. Generating output tokens requires more processing capacity than consuming input tokens.

Starting with GPT-4.1 models, the system matches the global standard pricing ratio between input and output tokens, [with exceptions for some models](#exceptions-to-input-and-output-throughput-ratio):

- For gpt-5, one output token counts as eight input tokens toward your utilization limit, matching the model's [pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) ratio.
- For gpt-4.1, one output token counts as four input tokens.
- Older models use different ratios.

For all deployments, cached tokens are deducted 100% from the utilization calculation, meaning repeated prompt tokens don't consume PTU capacity.

### Exceptions to input and output throughput ratio

Some models use a ratio that differs from their global standard price ratio. For example, with Llama-3.3-70B-Instruct, one output token counts as four input tokens toward your utilization limit, which differs from that model's standard price ratio. See [pricing for Llama models](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/) for the full input and output pricing breakdown.

### Latest Azure OpenAI models

> [!NOTE]
> gpt-5.4, gpt-4.1, gpt-4.1-mini, and gpt-4.1-nano don't support long context (requests estimated at larger than 128k prompt tokens).

| Topic | **gpt-5.4** | **gpt-5.3-codex** | **gpt-5.2** | **gpt-5.2-codex** | **gpt-5.1** | **gpt-5.1-codex** | **gpt-5** | **gpt-5-mini** | **gpt-4.1** | **gpt-4.1-mini** | **gpt-4.1-nano** | **o3** | **o4-mini** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Global & data zone provisioned minimum deployment | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 |
| Global & data zone provisioned scale increment | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Regional provisioned minimum deployment | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Regional provisioned scale increment | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Input TPM per PTU | 2,400 | 3,400 | 3,400 | 3,400 | 4,750 | 4,750 | 4,750 | 23,750 | 3,000 | 14,900 | 59,400 | 3,000 | 5,400 |
| Global standard output-to-input price ratio<sup>1</sup> | 6 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 4 | 4 | 4 | 4 | 4 |
| Latency target value<sup>2</sup> | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 80 TPS | 99% > 80 TPS | 99% > 90 TPS | 99% > 100 TPS | 99% > 80 TPS | 99% > 90 TPS |

<sup>1</sup> Calculated as the ratio of the output token price to the input token price for global standard deployment. For example, a ratio of 4 means one output token costs four times as much as one input token. See [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current pricing.

<sup>2</sup> Calculated as p50 request latency on a per 5-minute basis. TPS = tokens per second.

### Previous Azure OpenAI models

| Topic | **gpt-4o** | **gpt-4o-mini** | **o3-mini** | **o1** |
|---|---|---|---|---|
| Global & data zone provisioned minimum deployment | 15 | 15 | 15 | 15 |
| Global & data zone provisioned scale increment | 5 | 5 | 5 | 5 |
| Regional provisioned minimum deployment | 50 | 25 | 25 | 25 |
| Regional provisioned scale increment | 50 | 25 | 25 | 50 |
| Input TPM per PTU | 2,500 | 37,000 | 2,500 | 230 |
| Global standard output-to-input price ratio<sup>1</sup> | 4 | 4 | 4 | 4 |
| Latency target value<sup>2</sup> | 99% > 25 TPS | 99% > 33 TPS | 99% > 66 TPS | 99% > 25 TPS |


<sup>1</sup> Calculated as the ratio of the output token price to the input token price for global standard deployment. For example, a ratio of 4 means one output token costs four times as much as one input token. See [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for current pricing.

<sup>2</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

### Direct from Azure models

| Topic | **Llama-3.3-70B-Instruct** | **DeepSeek-R1** | **DeepSeek-V3-0324** | **DeepSeek-R1-0528** |
|---|---|---|---|---|
| Global & data zone provisioned minimum deployment | 100 | 100 | 100 | 100 |
| Global & data zone provisioned scale increment | 100 | 100 | 100 | 100 |
| Regional provisioned minimum deployment | NA | NA | NA | NA |
| Regional provisioned scale increment | NA | NA | NA | NA |
| Input TPM per PTU | 8,450<sup>1</sup> | 4,000 | 4,000 | 4,000 |
| Global standard output-to-input price ratio<sup>2</sup> | 1 | 4 | 4 | N/A |
| Latency target value<sup>3</sup> | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS | 99% > 50 TPS |

<sup>1</sup> For Llama-3.3-70B-Instruct, one output token counts as four input tokens toward your utilization limit. This ratio differs from the global standard price ratio between input and output tokens. See [Exceptions to input and output throughput ratio](#exceptions-to-input-and-output-throughput-ratio) and [Llama model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/).

<sup>2</sup> Calculated as the ratio of the output token price to the input token price for global standard deployment. For example, a ratio of 4 means one output token costs four times as much as one input token. See [Llama model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/) and [DeepSeek model pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/deepseek/) for current pricing.

<sup>3</sup> Calculated as the average request latency on a per-minute basis across the month. TPS = tokens per second.

## Determine PTU requirements for a workload

PTUs represent an amount of model processing capacity. Before creating a provisioned deployment, estimate how many PTUs your workload needs. The correct count depends on several factors:

- **Request shape**: Input tokens, output tokens, and requests per minute (RPM). Generating output tokens requires more processing than consuming input tokens.
- **Traffic patterns**: Highly variable traffic or bursts of large requests affect PTU consumption differently than steady traffic with consistent call shapes.
- **Model selected**: Each model delivers a different number of TPM per PTU. A heavier model requires more PTUs to serve the same TPM as a lighter model. See [How much throughput per PTU you get for each model](#how-much-throughput-per-ptu-you-get-for-each-model) for per-model data.

Additional sizing considerations:

- For GPT-4o and later models, input and output TPM per PTU are specified separately. For older models, the distribution of call shapes matters: a small number of large calls can consume significantly more capacity than many small calls with the same average token count.
- Use the [capacity calculator](https://ai.azure.com/resource/calculator) in the Foundry portal to estimate maximum requests per minute for a specific call shape and model.
- If the system generates fewer output tokens than the value specified in the `max_tokens` parameter, the deployment can accept more requests. For highest concurrency, set `max_tokens` as close as possible to the true expected generation size.

### Obtain PTU quota

New subscriptions receive a default amount of global, data zone, and regional provisioned quota in select regions. To request additional quota:

1. In the Foundry portal, go to the **Operate** section > **Quota** pane and select the subscription and target region.
1. Select **Request Quota** and complete the form.

You receive an email notification when the request is approved. You can also submit the [quota request form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu) directly.

## Size your Foundry provisioned throughput reservation

The PTU quantity in a reservation purchase is independent of your quota allocation and of the PTUs used in your current deployments. You can purchase a reservation for more or fewer PTUs than you've deployed, but only deployed PTUs that fall within the reservation scope receive the discount. To protect against over-purchasing:

- **Create deployments before purchasing a reservation**: This confirms that capacity is available for the desired region and model. Purchasing a reservation before deploying risks committing to PTUs you can't use.
- **Match reservation quantity to deployed PTUs**: Align the reservation size to the PTUs currently deployed within the reservation's scope. Any PTUs in scope beyond the reservation quantity are charged at the hourly rate.
- **Purchase separate reservations per deployment type**: Reservations for Global, Data Zone, and Regional deployments aren't interchangeable.
- **Use scoping to cover multiple deployments**: New reservations can be purchased to cover additional deployments within the same scope. You can also update the scope of an existing reservation at any time without penalty.

> [!IMPORTANT]
> Capacity availability for model deployments is dynamic and changes frequently across regions and models. Always create deployments first, then purchase the Azure Reservation to cover the PTUs you have deployed. This approach ensures you receive the full reservation discount and protects you from committing to a reservation for PTUs you can't deploy.

## Monitor your reservation and PTU usage

Monitoring reservation utilization helps you identify over-provisioning, catch unexpected billing, and plan for future capacity needs.

### Track reservation utilization and costs

Use these Azure Cost Management resources to track and analyze your reservation usage:

- [View Azure reservation utilization](/azure/cost-management-billing/reservations/reservation-utilization): See what percentage of your reserved PTUs are actively in use across your deployments.
- [View Azure Reservation purchase and refund transactions](/azure/cost-management-billing/reservations/view-purchase-refunds): Review purchase history and any refund activity.
- [View amortized benefit costs](/azure/cost-management-billing/reservations/view-amortized-costs): Understand the amortized cost impact of your reservations for clearer per-deployment billing visibility.
- [Charge back Azure Reservation costs](/azure/cost-management-billing/reservations/charge-back-usage): Distribute reservation costs across teams or projects for internal cost attribution.
- [Automatically renew Azure reservations](/azure/cost-management-billing/reservations/reservation-renew): Set up auto-renewal to prevent reservation expiry and maintain the discounted rate.

### Adjust reservations as your workload changes

As your provisioned deployment footprint grows or shrinks, adjust your reservations to match:

- **Add coverage**: Purchase an additional reservation for the same scope to cover new deployments.
- **Remove coverage**: Cancel or exchange a reservation in the Azure portal. Cancellations might be subject to fee limits. Exchanges reset the reservation term.
- **Update scope**: Change the scope of an existing reservation at any time without penalty, for example to extend coverage to a new subscription.

Manage all reservations from the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations).

## Related content

- [What is provisioned throughput?](../concepts/provisioned-throughput.md)
- [Get started with provisioned deployments](./provisioned-get-started.md)
- [Foundry Provisioned Throughput reservation documentation](https://aka.ms/oai/docs/ptum-reservations)
- [Performance and latency](./latency.md)
- [Deployment types for Microsoft Foundry Models](../../foundry-models/concepts/deployment-types.md)
- [Foundry Provisioned August Update](../../../foundry-classic/openai/concepts/provisioned-migration.md)
