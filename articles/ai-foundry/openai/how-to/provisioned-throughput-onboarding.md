---
title:  Understanding costs associated with provisioned throughput units (PTU)
description: Learn about provisioned throughput costs and billing in Azure AI Foundry. 
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 06/25/2025
manager: nitinme
author: aahill 
ms.author: aahi 
recommendations: false
---

# Understanding costs associated with provisioned throughput units (PTU)

Use this article to learn about calculating and understanding costs associated with PTU. For an overview of the provisioned throughput offering, see [What is provisioned throughput?](../concepts/provisioned-throughput.md). When you're ready to sign up for the provisioned throughput offering, see the [getting started guide](./provisioned-get-started.md).

> [!NOTE]
> In function calling and agent use cases, token usage can be variable. You should understand your expected Tokens Per Minute (TPM) usage in detail before migrating workloads to PTU.

## Provisioned throughput units

Provisioned throughput units (PTUs) are generic units of model processing capacity that you can use to size provisioned deployments to achieve the required throughput for processing prompts and generating completions.  Provisioned throughput units are granted to a subscription as quota. Each quota is specific to a region and defines  the maximum number of PTUs that can be assigned to deployments in that subscription and region.

## Understanding provisioned throughput billing

Azure AI Foundry [Regional Provisioned Throughput](../how-to/deployment-types.md#regional-provisioned), [Data Zone Provisioned Throughput](../how-to/deployment-types.md#data-zone-provisioned), and [Global Provisioned Throughput](../how-to/deployment-types.md#global-provisioned) are purchased on-demand at an hourly basis based on the number of deployed PTUs, with substantial term discount available via the purchase of [Azure Reservations](#azure-reservations-for-azure-ai-foundry-provisioned-throughput).  

The hourly model is useful for short-term deployment needs, such as validating new models or acquiring capacity for a hackathon.  However, the discounts provided by the Azure Reservation for Azure AI Foundry Regional Provisioned, Data Zone Provisioned, and Global Provisioned are considerable and most customers with consistent long-term usage will find a reserved model to be a better value proposition. 

> [!NOTE]
> Azure AI Foundry Provisioned customers onboarded prior to the August self-service update use a purchase model called the Commitment model. These customers can continue to use this older purchase model alongside the Hourly/reservation purchase model. The Commitment model is not available for new customers or [certain new models](../concepts/provisioned-migration.md#supported-models-on-commitment-payment-model) introduced after August 2024. For details on the Commitment purchase model and options for coexistence and migration, see the [Azure AI Foundry Provisioned August Update](../concepts/provisioned-migration.md).


## Model independent quota

Unlike the Tokens Per Minute (TPM) quota used by other Azure AI Foundry offerings, PTUs are model-independent. The PTUs might be used to deploy any supported models hosted and sold directly by Microsoft in the region.

:::image type="content" source="../media/provisioned/model-independent-quota.png" alt-text="Diagram of model independent quota with one pool of PTUs available to multiple Azure OpenAI models." lightbox="../media/provisioned/model-independent-quota.png":::

Quota for provisioned deployments shows up in Azure AI Foundry as the following deployment types: [global provisioned](../how-to/deployment-types.md#global-provisioned), [data zone provisioned](../how-to/deployment-types.md#data-zone-provisioned) and [regional provisioned](../how-to/deployment-types.md#regional-provisioned).

|deployment type  |Quota name  |
|---------|---------|
|[Regional Provisioned](../how-to/deployment-types.md#regional-provisioned)     |  Regional Provisioned Throughput Unit       |
|[Global Provisioned](../how-to/deployment-types.md#global-provisioned)     | Global Provisioned Throughput Unit        |
|[Data zone Provisioned](../how-to/deployment-types.md#data-zone-provisioned)    | Data Zone Provisioned Throughput Unit        |

:::image type="content" source="../media/provisioned/ptu-quota-page.png" alt-text="Screenshot of quota UI for Azure AI Foundry provisioned." lightbox="../media/provisioned/ptu-quota-page.png":::

## Hourly usage

Regional Provisioned, Data Zone Provisioned, and Global Provisioned deployments are charged an hourly rate ($/PTU/hr) on the number of PTUs that have been deployed.  For example, a 300 PTU deployment will be charged the hourly rate times 300.  All Azure AI Foundry model pricing is available in the Azure Pricing Calculator. 

If a deployment exists for a partial hour, it will receive a prorated charge based on the number of minutes it was deployed during the hour.  For example, a deployment that exists for 15 minutes during an hour will receive 1/4th the hourly charge.  

If the deployment size is changed, the costs of the deployment will adjust to match the new number of PTUs.  

:::image type="content" source="../media/provisioned/hourly-billing.png" alt-text="A diagram showing hourly billing." lightbox="../media/provisioned/hourly-billing.png":::

Paying for regional provisioned, data zone provisioned, and global provisioned deployments on an hourly basis is ideal for short-term deployment scenarios.  For example: Quality and performance benchmarking of new models, or temporarily increasing PTU capacity to cover an event such as a hackathon.  

Customers that require long-term usage of regional provisioned, data zone provisioned, and global provisioned deployments, however, might pay significantly less per month by purchasing a term discount via [Azure Reservations](#azure-reservations-for-azure-ai-foundry-provisioned-throughput) as discussed later in the article. 

> [!IMPORTANT]
> It's not recommended to scale production deployments according to incoming traffic and pay for them purely on an hourly basis. There are two reasons for this:
> * The cost savings achieved by purchasing Azure Reservations for Azure AI Foundry Provisioned Throughput, Data Zone Provisioned, and Global Provisioned are significant, and it will be less expensive in many cases to maintain a deployment sized for full production volume paid for via a reservation than it would be to scale the deployment with incoming traffic.
> * Having unused provisioned quota (PTUs) doesn't guarantee that capacity will be available to support an increase in the size of the deployment when required. Quota limits the maximum number of PTUs that can be deployed, but it isn't a capacity guarantee. Provisioned capacity for each region and model dynamically changes throughout the day and might not be available when required. As a result, it's recommended to maintain a permanent deployment to cover your traffic needs (paid for via a reservation).
> Charges for deployments on a deleted resource will continue until the resource is purged. To prevent this, delete a resource's deployment before deleting the resource. For more information, see [Recover or purge deleted Azure OpenAI resources](../../../ai-services/recover-purge-resources.md). 

## How much throughput per PTU you get for each model





The amount of throughput (measured in tokens per minute or TPM) a deployment gets per PTU is a function of the input and output tokens in a given minute. Generating output tokens requires more processing than input tokens.  Starting with GPT 4.1 models and later, the system matches the global standard price ratio between input and output tokens. Cached tokens are deducted 100% from the utilization.

For example, for `gpt-4.1:2025-04-14`, 1 output token counts as 4 input tokens towards your utilization limit which matches the [pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). Older models use a different ratio and for a deeper understanding on how different ratios of input and output tokens impact the throughput your workload needs, see the [Azure AI Foundry PTU quota calculator](https://ai.azure.com/resource/calculator).

|Topic| **o4-mini** | **gpt-4.1** | **gpt-4.1-mini** | **gpt-4.1-nano** | **o3** | **o3-mini** | **o1** | **gpt-4o** | **gpt-4o-mini** |  **DeepSeek-R1** | **DeepSeek-V3-0324** | **DeepSeek-R1-0528** |
| --- |  --- | --- |  --- |  --- | --- | --- | --- | --- | --- | --- | --- | --- |
|Global & data zone provisioned minimum deployment| 15 | 15|15| 15 | 15 |15|15|15|15| 100|100|100|
|Global & data zone provisioned scale increment| 5 | 5|5| 5 | 5 |5|5|5|5|  100|100|100|
|Regional provisioned minimum deployment|25| 50|25| 25 |50 | 25|25|50|25| NA|NA|NA|
|Regional provisioned scale increment|25| 50|25| 25 | 50 | 25|50|50|25|NA|NA|NA|
|Input TPM per PTU|5,400 | 3,000|14,900| 59,400 | 3,000 | 2,500|230|2,500|37,000|4,000|4,000|4,000|
|Latency Target Value| 99% > 66 Tokens Per Second\* | 99% > 40 Tokens Per Second\* | 99% > 50 Tokens Per Second\*| 99% > 60 Tokens Per Second\* | 99% > 40 Tokens Per Second\* | 99% > 66 Tokens Per Second\* | 99% > 25 Tokens Per Second\* | 99% > 25 Tokens Per Second\* | 99% > 33 Tokens Per Second\* | 99% > 50 Tokens Per Second\*| 99% > 50 Tokens Per Second\*| 99% > 50 Tokens Per Second\*|

\* Calculated as the average request latency on a per-minute basis across the month.

For a full list, see the [Azure AI Foundry calculator](https://ai.azure.com/resource/calculator).

## Determining the number of PTUs needed for a workload

Determining the right amount of provisioned throughput, or PTUs, you require for your workload is an essential step to optimizing performance and cost. 

PTUs represent an amount of model processing capacity. Similar to your computer or databases, different workloads or requests to the model will consume different amounts of underlying processing capacity. The conversion from throughput needs to PTUs can be approximated using historical token usage data or call shape estimations (input tokens, output tokens, and requests per minute) as outlined in our [performance and latency](../how-to/latency.md) documentation. To simplify this process, you can use the [Azure AI Foundry PTU quota calculator](https://ai.azure.com/resource/calculator) to size specific workload shapes.

A few high-level considerations:
- Generations require more capacity than prompts
- For GPT-4o and later models, the TPM per PTU is set for input and output tokens separately. For older models, larger calls are progressively more expensive to compute. For example, 100 calls of with a 1000 token prompt size requires less capacity than one call with 100,000 tokens in the prompt. This tiering means that the distribution of these call shapes is important in overall throughput. Traffic patterns with a wide distribution that includes some large calls might experience lower throughput per PTU than a narrower distribution with the same average prompt & completion token sizes.

### Obtaining PTU quota

Customers need to request quota via the [Request Quota Link](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu). If more quotas are required, you also need to request quota via this link. This link can be found in the quota hub in management center of Azure AI Foundry. The form allows the customer to request an increase in the specified PTU quota for a given region. The customer receives an email at the included address once the request is approved, typically within two business days. 

### Per-Model PTU minimums

The minimum PTU deployment, increments, and processing capacity associated with each unit varies by model type & version. See the above [table](#how-much-throughput-per-ptu-you-get-for-each-model) for more information.

## Estimate provisioned throughput units and cost

To get a quick estimate for your workload using input and output TPM, leverage the built-in capacity planner in the deployment details section of the deployment dialogue screen. The built-in capacity planner is part of the deployment workflow to help streamline the sizing and allocation of quota to a PTU deployment for a given workload. For more information on how to identify and estimate TPM data, review the recommendations in our [performance and latency documentation](./latency.md). 

To use the capacity planner, go to the Azure AI Foundry Portal and select the **Deployments** button. Then select **Deploy model**.

:::image type="content" source="../media/provisioned/deploy-model-button.png" alt-text="A screenshot of the model deployment screen." lightbox="../media/provisioned/deploy-model-button.png":::

Choose a model, and click **Confirm**. Select a provision throughput deployment type. After filling out the input and output TPM data in the built-in capacity calculator, select the **Calculate** button to view your PTU allocation recommendation. 

:::image type="content" source="../media/provisioned/deployment-ptu-capacity-calculator.png" alt-text="A screenshot of deployment workflow PTU capacity calculator." lightbox="../media/provisioned/deployment-ptu-capacity-calculator.png":::

To estimate provisioned capacity using request level data, open the capacity planner in the [Azure AI Foundry](https://ai.azure.com?cid=learnDocs). The capacity calculator is under **Management Center** > **Quota** > **Provisioned Throughput**.

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

## Azure Reservations for Azure AI Foundry Provisioned Throughput

Discounts on top of the hourly usage price can be obtained by purchasing an Azure Reservation for Azure AI Foundry Regional Provisioned, Data Zone Provisioned, and Global Provisioned. An Azure Reservation is a term-discounting mechanism shared by many Azure products. For example, Compute and Cosmos DB. For Azure AI Foundry Regional Provisioned, Data Zone Provisioned, and Global Provisioned, the reservation provides a discount in exchange for committing to payment for fixed number of PTUs for a one-month or one-year period.  

* Azure Reservations are purchased via the Azure portal, not the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) Link to Azure reservation portal.

* Reservations are purchased regionally and can be flexibly scoped to cover usage from a group of deployments. Reservation scopes include: 

    * Individual resource groups or subscriptions 

    * A group of subscriptions in a Management Group 

    * All subscriptions in a billing account 

* New reservations can be purchased to cover the same scope as existing reservations, to allow for discounting of new provisioned deployments. The scope of existing reservations can also be updated at any time without penalty, for example to cover a new subscription. 

* Reservations for Global, Data Zone, and Regional deployments aren't interchangeable. You need to purchase a separate reservation for each deployment type. 

* Reservations can be canceled after purchase, but credits are limited.  

* If the size of provisioned deployments within the scope of a reservation exceeds the amount of the reservation, the excess is charged at the hourly rate. For example, if deployments amounting to 250 PTUs exist within the scope of a 200 PTU reservation, 50 PTUs will be charged on an hourly basis until the deployment sizes are reduced to 200 PTUs, or a new reservation is created to cover the remaining 50. 

* Reservations guarantee a discounted price for the selected term.  They don't reserve capacity on the service or guarantee that it will be available when a deployment is created. It's highly recommended that customers create deployments prior to purchasing a reservation to prevent from over-purchasing a reservation. 

> [!IMPORTANT] 
> * Capacity availability for model deployments is dynamic and changes frequently across regions and models. To prevent you from purchasing a reservation for more PTUs than you can use, create deployments first, and then purchase the Azure Reservation to cover the PTUs you have deployed. This best practice will ensure that you can take full advantage of the reservation discount and prevent you from purchasing a term commitment that you cannot use. 
>
> * The Azure role and tenant policy requirements to purchase a reservation are different than those required to create a deployment or Azure AI Foundry resource. Verify authorization to purchase reservations in advance of needing to do so. See [Azure AI Foundry Provisioned Throughput Reservation](https://aka.ms/oai/docs/ptum-reservations) for more details.

## Important: sizing Azure AI Foundry Provisioned Throughput Reservation

The PTU amounts in reservation purchases are independent of PTUs allocated in quota or used in deployments. It's possible to purchase a reservation for more PTUs than you have in quota, or can deploy for the desired region, model, or version. Credits for over-purchasing a reservation are limited, and customers must take steps to ensure they maintain their reservation sizes in line with their deployed PTUs. 
 
The best practice is to always purchase a reservation after deployments have been created. This prevents purchasing a reservation and then finding out that the required capacity isn't available for the desired region or model. 
 

Reservations for Global, Data Zone, and Regional deployments aren't interchangeable. You need to purchase a separate reservation for each deployment type.

To assist customers with purchasing the correct reservation amounts. The total number of PTUs in a subscription and region that can be covered by a reservation are listed on the Quotas page of Azure AI Foundry. See the message "PTUs Available for reservation." 

:::image type="content" source="../media/provisioned/ptu-quota-page.png" alt-text="A screenshot showing available PTU quota." lightbox="../media/provisioned/available-quota.png":::

Managing Azure Reservations 

After a reservation is created, it is a best practice monitor it to ensure it is receiving the usage you're expecting. This can be done via the Azure Reservation Portal or Azure Monitor. Details on these articles and others can be found here: 

* [View Azure reservation utilization](/azure/cost-management-billing/reservations/reservation-utilization) 
* [View Azure Reservation purchase and refund transactions](/azure/cost-management-billing/reservations/view-purchase-refunds) 
* [View amortized benefit costs](/azure/cost-management-billing/reservations/view-amortized-costs) 
* [Charge back Azure Reservation costs](/azure/cost-management-billing/reservations/charge-back-usage)
* [Automatically renew Azure reservations](/azure/cost-management-billing/reservations/reservation-renew)

## Next steps

- [Provisioned Throughput Units (PTU) getting started guide](./provisioned-get-started.md)
- [Provisioned Throughput Units (PTU) concepts](../concepts/provisioned-throughput.md)
- [Provisioned Throughput reservation documentation](https://aka.ms/oai/docs/ptum-reservations) 
