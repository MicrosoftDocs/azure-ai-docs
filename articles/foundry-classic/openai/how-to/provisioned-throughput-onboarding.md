---
title: "Provisioned throughput unit (PTU) costs and billing (classic)"
description: "Learn about provisioned throughput unit (PTU) costs, hourly billing, Azure reservations, and capacity planning in Microsoft Foundry. (classic)"
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 03/16/2026
manager: nitinme
author: msakande 
ms.author: mopeakande 
ms.reviewer: seramasu
reviewer: rsethur
ms.custom:
  - pilot-ai-workflow-jan-2026
  - classic-and-new
recommendations: false
#customerIntent: As a developer, I want to understand PTU costs and billing so I can plan and manage my Microsoft Foundry provisioned throughput deployments efficiently.
ROBOTS: NOINDEX, NOFOLLOW
---

# Provisioned throughput unit (PTU) costs and billing (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/provisioned-throughput-onboarding.md)

[!INCLUDE [provisioned-throughput-onboarding 1](../../../foundry/openai/includes/how-to-provisioned-throughput-onboarding-1.md)]

## Model independent quota

Unlike the Tokens Per Minute (TPM) quota used by other Foundry offerings, PTUs are model-independent. The PTUs might be used to deploy any supported models hosted and sold directly by Microsoft in the region.

:::image type="content" source="../../../foundry/openai/media/provisioned/model-independent-quota.png" alt-text="Diagram of model independent quota with one pool of PTUs available to multiple Azure OpenAI models." lightbox="../../../foundry/openai/media/provisioned/model-independent-quota.png":::

Quota for provisioned deployments shows up in Foundry as the following deployment types: [global provisioned](../../foundry-models/concepts/deployment-types.md#global-provisioned), [data zone provisioned](../../foundry-models/concepts/deployment-types.md#data-zone-provisioned) and [regional provisioned](../../foundry-models/concepts/deployment-types.md#regional-provisioned).

> [!NOTE]
> Quota doesn't guarantee capacity. Deploy your model in Foundry before purchasing a matching reservation in the Azure portal.

|deployment type  |Quota name  |
|---------|---------|
|[Regional Provisioned](../../foundry-models/concepts/deployment-types.md#regional-provisioned)     |  Regional Provisioned Throughput Unit       |
|[Global Provisioned](../../foundry-models/concepts/deployment-types.md#global-provisioned)     | Global Provisioned Throughput Unit        |
|[Data zone Provisioned](../../foundry-models/concepts/deployment-types.md#data-zone-provisioned)    | Data Zone Provisioned Throughput Unit        |

You can find details about quota for provisioned deployments in the [Foundry portal](https://ai.azure.com/?cid=learnDocs) **Management center** > **Quota** page.

:::image type="content" source="../media/provisioned/ptu-quota-page.png" alt-text="Screenshot of quota UI for Foundry provisioned." lightbox="../media/provisioned/ptu-quota-page.png":::

[!INCLUDE [provisioned-throughput-onboarding 2](../../../foundry/openai/includes/how-to-provisioned-throughput-onboarding-2.md)]

## Delete PTU deployments

> [!IMPORTANT]
> Charges for deployments on a deleted resource will continue until the resource is purged. To prevent unwanted charges, delete a resource's deployment before deleting the resource. However, if you already deleted the resource first, you can recover or purge it. For more information, see [recover or purge deleted Azure OpenAI resources](../../../ai-services/recover-purge-resources.md). 

Deleting a deployment does not cancel or change any PTU reservation. Reservations don't support deletion. You can use the Azure portal to cancel or exchange reservations manually, and these options might incur extra fees.

Use these steps to delete a provisioned deployment to avoid unwanted charges.

1. Delete the deployment in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. If you plan to remove the Azure AI resource, delete deployments first, then delete the resource. Purge the resource to stop charges.
1. Go to the [Reservations page in the Azure portal](https://portal.azure.com/#view/Microsoft_Azure_Reservations/ReservationsBrowseBlade/productType/Reservations) to manage reservations. In the Azure portal, you can purchase, cancel, or exchange reservations to align with current deployments.

## How much throughput per PTU you get for each model

The amount of throughput (measured in tokens per minute or TPM) a deployment gets per PTU is a function of the input and output tokens in a given minute. Generating output tokens requires more processing than input tokens. Starting with GPT 4.1 models and later, the system generally matches the global standard price ratio between input and output tokens, with [exceptions for some models](#exceptions-to-input-and-output-throughput-ratio). For all deployments, cached tokens are deducted 100% from the utilization.

For example, for gpt-5, one output token counts as eight input tokens towards your utilization limit, which matches the [pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). For other models, such as gpt-4.1, one output token counts as four input tokens. Older models use a different ratio.

For a deeper understanding on how different ratios of input and output tokens impact the throughput your workload needs, see the [Foundry PTU quota calculator](https://ai.azure.com/resource/calculator).

### Exceptions to input and output throughput ratio

The system allows exceptions to the standard input-to-output token ratio for certain models. For example, with Llama-3.3-70B-Instruct, one output token counts as four input tokens toward your utilization limit. This ratio differs from the global standard price ratio between input and output tokens. To see the input and output pricing for the model, see [pricing for Llama models](https://azure.microsoft.com/pricing/details/ai-foundry-models/llama/).

[!INCLUDE [provisioned-throughput-onboarding 3](../../../foundry/openai/includes/how-to-provisioned-throughput-onboarding-3.md)]

## Direct from Azure models

|Topic| **Llama-3.3-70B-Instruct** | **DeepSeek-R1** | **DeepSeek-V3-0324** | **DeepSeek-R1-0528** |
|---|---|---|---|---|
|Global & data zone provisioned minimum deployment|100|100|100|100|
|Global & data zone provisioned scale increment|100|100|100|100|
|Regional provisioned minimum deployment|NA|NA|NA|NA|
|Regional provisioned scale increment|NA|NA|NA|NA|
|Input TPM per PTU|8,450<sup>1</sup>|4,000|4,000|4,000|
|Latency Target Value|99% > 50 Tokens Per Second\*|99% > 50 Tokens Per Second\*|99% > 50 Tokens Per Second\*|99% > 50 Tokens Per Second\*|

\* Calculated as the average request latency on a per-minute basis across the month.

<sup>1</sup> For Llama-3.3-70B-Instruct, one output token counts as four input tokens towards your utilization limit. This ratio differs from the global standard price ratio between input and output tokens. For more details, see [Exceptions to input and output throughput ratio](#exceptions-to-input-and-output-throughput-ratio).
 
For a full list, see the [Foundry calculator](https://ai.azure.com/resource/calculator).

## Determine PTU requirements for a workload

Determining the right number of provisioned throughput units (PTUs) for your workload is an essential step in optimizing performance and cost. 

PTUs represent an amount of model processing capacity. Similar to your computer or databases, different workloads or requests to the model will consume different amounts of underlying processing capacity. The conversion from throughput needs to PTUs can be approximated using historical token usage data or call shape estimations (input tokens, output tokens, and requests per minute) as outlined in the [performance and latency](./latency.md) documentation. 

To simplify this process, you can use the [Foundry calculator](https://ai.azure.com/resource/calculator) to size specific workload shapes.

A few high-level considerations:
- Generations require more capacity than prompts
- For GPT-4o and later models, the TPM per PTU is set for input and output tokens separately. For older models, larger calls are progressively more expensive to compute. For example, 100 calls of with a 1000 token prompt size requires less capacity than one call with 100,000 tokens in the prompt. This tiering means that the distribution of these call shapes is important in overall throughput. Traffic patterns with a wide distribution that includes some large calls might experience lower throughput per PTU than a narrower distribution with the same average prompt & completion token sizes.

### Obtain PTU quota

Customers need to request quota via the [Request Quota Link](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu).

If more quotas are required, you also need to request quota via the link in the quota hub in the management center of Foundry. The form allows the customer to request an increase in the specified PTU quota for a given region. The customer receives an email at the included address once the request is approved, typically within two business days.

### Per-Model PTU minimums

The minimum PTU deployment, increments, and processing capacity associated with each unit varies by model type & version. See the above [table](#how-much-throughput-per-ptu-you-get-for-each-model) for more information.

## Estimate provisioned throughput units and cost

To get a quick estimate for your workload using input and output TPM, leverage the built-in capacity planner in the deployment details section of the deployment dialogue screen. The built-in capacity planner is part of the deployment workflow to help streamline the sizing and allocation of quota to a PTU deployment for a given workload. For more information on how to identify and estimate TPM data, review the recommendations in our [performance and latency documentation](./latency.md). 

To use the capacity planner, go to the Foundry portal and select the **Deployments** button. Then select **Deploy model**.

:::image type="content" source="../media/provisioned/deploy-model-button.png" alt-text="A screenshot of the model deployment screen." lightbox="../media/provisioned/deploy-model-button.png":::

Choose a model, and click **Confirm**. Select a provision throughput deployment type. After filling out the input and output TPM data in the built-in capacity calculator, select the **Calculate** button to view your PTU allocation recommendation. 

:::image type="content" source="../media/provisioned/deployment-ptu-capacity-calculator.png" alt-text="A screenshot of deployment workflow PTU capacity calculator." lightbox="../media/provisioned/deployment-ptu-capacity-calculator.png":::

To estimate provisioned capacity using request level data, open the capacity planner in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). The capacity calculator is under **Management Center** > **Quota** > **Provisioned Throughput**.

The **Provisioned Throughput** option and the calculator are only available in certain regions within the Quota pane, if you don't see this option setting the quota region to *Sweden Central* will make this option available. Enter the following parameters based on your workload.

| Input | Description |
|---|---|
|Model | model you plan to use. For example: GPT-4 |
| Version | Version of the model you plan to use, for example 0614 |
| Peak calls per min | The number of calls per minute that are expected to be sent to the model |
| Tokens in prompt call | The number of tokens in the prompt for each call to the model. Calls with larger prompts utilize more of the PTU deployment. Currently this calculator assumes a single prompt value so for workloads with wide variance. We recommend benchmarking your deployment on your traffic to determine the most accurate estimate of PTU needed for your deployment. |
| Tokens in model response | The number of tokens generated from each call to the model. Calls with larger generation sizes utilize more of the PTU deployment. Currently this calculator assumes a single prompt value so for workloads with wide variance. We recommend benchmarking your deployment on your traffic to determine the most accurate estimate of PTU needed for your deployment. |

After you fill in the required details, select **Calculate** button in the output column.

The values in the output column are the estimated value of PTU units required for the provided workload inputs. The first output value represents the estimated PTU units required for the workload, rounded to the nearest PTU scale increment. The second output value represents the raw estimated PTU units required for the workload. The token totals are calculated using the following equation: `Total = Peak calls per minute * (Tokens in prompt call + Tokens in model response)`.

:::image type="content" source="../media/how-to/provisioned-onboarding/capacity-calculator.png" alt-text="Screenshot of the capacity calculator" lightbox="../media/how-to/provisioned-onboarding/capacity-calculator.png":::

> [!NOTE]
> The capacity calculators provide an estimate based on simple input criteria. The most accurate way to determine your capacity is to benchmark a deployment with a representational workload for your use case.

[!INCLUDE [provisioned-throughput-onboarding 4](../../../foundry/openai/includes/how-to-provisioned-throughput-onboarding-4.md)]

## Size your Foundry provisioned throughput reservation

The PTU amounts in reservation purchases are independent of PTUs allocated in quota or used in deployments. It's possible to purchase a reservation for more PTUs than you have in quota, or can deploy for the desired region, model, or version. Credits for over-purchasing a reservation are limited, and customers must take steps to ensure they maintain their reservation sizes in line with their deployed PTUs. 
 
The best practice is to always purchase a reservation after deployments have been created. This protects against purchasing a reservation and then finding out that the required capacity isn't available for the desired region or model. 
 
Reservations for Global, Data Zone, and Regional deployments aren't interchangeable. You need to purchase a separate reservation for each deployment type.

To assist customers with purchasing the correct reservation amounts. The total number of PTUs in a subscription and region that can be covered by a reservation are listed on the Quotas page of the Foundry portal. See the message "PTUs Available for reservation." 

:::image type="content" source="../media/provisioned/ptu-quota-page.png" alt-text="A screenshot showing available PTU quota." lightbox="../media/provisioned/ptu-quota-page.png":::

### Manage Azure reservations

After a reservation is created, monitor it via the Azure Reservation portal or Azure Monitor to ensure that the reservation is receiving the usage you expect. To learn more about managing and monitoring Azure reservations, see these articles:

* [View Azure reservation utilization](/azure/cost-management-billing/reservations/reservation-utilization) 
* [View Azure Reservation purchase and refund transactions](/azure/cost-management-billing/reservations/view-purchase-refunds) 
* [View amortized benefit costs](/azure/cost-management-billing/reservations/view-amortized-costs) 
* [Charge back Azure Reservation costs](/azure/cost-management-billing/reservations/charge-back-usage)
* [Automatically renew Azure reservations](/azure/cost-management-billing/reservations/reservation-renew)

[!INCLUDE [provisioned-throughput-onboarding 5](../../../foundry/openai/includes/how-to-provisioned-throughput-onboarding-5.md)]
