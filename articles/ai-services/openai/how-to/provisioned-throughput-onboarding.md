---
title: Azure OpenAI Service Provisioned Throughput Units (PTU) onboarding
description: Learn about provisioned throughput units onboarding and Azure OpenAI. 
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 10/18/2024
manager: nitinme
author: mrbullwinkle 
ms.author: mbullwin 
recommendations: false
---

# Provisioned throughput units onboarding

This article walks you through the process of onboarding to [Provisioned Throughput Units (PTU)](../concepts/provisioned-throughput.md). Once you complete the initial onboarding, we recommend referring to the PTU [getting started guide](./provisioned-get-started.md).

## When to use provisioned throughput units (PTU)

You should consider switching from standard deployments to provisioned deployments when you have well-defined, predictable throughput and latency requirements. Typically, this occurs when the application is ready for production or has already been deployed in production and there's an understanding of the expected traffic. This allows users to accurately forecast the required capacity and avoid unexpected billing. 

### Typical PTU scenarios

- An application that is ready for production or in production. 
- An application that has predictable capacity/usage expectations. 
- An application has real-time/latency sensitive requirements. 

> [!NOTE]
> In function calling and agent use cases, token usage can be variable. You should understand your expected Tokens Per Minute (TPM) usage in detail prior to migrating workloads to PTU.

## Sizing and estimation: provisioned deployments

Determining the right amount of provisioned throughput, or PTUs, you require for your workload is an essential step to optimizing performance and cost. If you aren't familiar with the different approaches available to estimate system level throughput, review the system level throughput estimation recommendations in our [performance and latency documentation](./latency.md). This section describes how to use Azure OpenAI capacity calculators to estimate the number of PTUs required to support a given workload.

### Estimate provisioned throughput units and cost

To get a quick estimate for your workload using input and output TPM, leverage the built-in capacity planner in the deployment details section of the deployment dialogue screen. The built-in capacity planner is part of the deployment workflow to help streamline the sizing and allocation of quota to a PTU deployment for a given workload. For more information on how to identify and estimate TPM data, review the recommendations in our [performance and latency documentation](./latency.md). 

After filling out the input and output TPM data in the built-in capacity calculator, select the **Calculate** button to view your PTU allocation recommendation. 

![Screenshot of deployment workflow PTU capacity calculator.](media/provisioned-throughput-onboarding/deployment-ptu-capacity-calculator.png)




To estimate provisioned capacity using request level data, open the capacity planner in the [Azure AI Foundry](https://ai.azure.com). The capacity calculator is under **Shared resources** > **Model Quota** > **Azure OpenAI Provisioned**.

The **Provisioned** option and the capacity planner are only available in certain regions within the Quota pane, if you don't see this option setting the quota region to *Sweden Central* will make this option available. Enter the following parameters based on your workload.

| Input | Description |
|---|---|
|Model | OpenAI model you plan to use. For example: GPT-4 |
| Version | Version of the model you plan to use, for example 0614 |
| Peak calls per min | The number of calls per minute that are expected to be sent to the model |
| Tokens in prompt call | The number of tokens in the prompt for each call to the model. Calls with larger prompts utilize more of the PTU deployment. Currently this calculator assumes a single prompt value so for workloads with wide variance. We recommend benchmarking your deployment on your traffic to determine the most accurate estimate of PTU needed for your deployment. |
| Tokens in model response | The number of tokens generated from each call to the model. Calls with larger generation sizes utilize more of the PTU deployment. Currently this calculator assumes a single prompt value so for workloads with wide variance. We recommend benchmarking your deployment on your traffic to determine the most accurate estimate of PTU needed for your deployment. |

After you fill in the required details, select **Calculate** button in the output column.

The values in the output column are the estimated value of PTU units required for the provided workload inputs. The first output value represents the estimated PTU units required for the workload, rounded to the nearest PTU scale increment. The second output value represents the raw estimated PTU units required for the workload. The token totals are calculated using the following equation: `Total = Peak calls per minute * (Tokens in prompt call + Tokens in model response)`.

:::image type="content" source="../media/how-to/provisioned-onboarding/capacity-calculator.png" alt-text="Screenshot of the capacity calculator" lightbox="../media/how-to/provisioned-onboarding/capacity-calculator.png":::

> [!NOTE]
> The capacity calculators provide an estimate based on simple input criteria. The most accurate way to determine your capacity is to benchmark a deployment with a representational workload for your use case.

## Understanding the provisioned throughput purchase model

Azure OpenAI Provisioned, Data Zone Provisioned, and Global Provisioned are purchased on-demand at an hourly basis based on the number of deployed PTUs, with substantial term discount available via the purchase of Azure Reservations.   

The hourly model is useful for short-term deployment needs, such as validating new models or acquiring capacity for a hackathon.  However, the discounts provided by the Azure Reservation for Azure OpenAI Provisioned, Data Zone Provisioned, and Global Provisioned are considerable and most customers with consistent long-term usage will find a reserved model to be a better value proposition. 

> [!NOTE]
> Azure OpenAI Provisioned customers onboarded prior to the August self-service update use a purchase model called the Commitment model.  These customers can continue to use this older purchase model alongside the Hourly/reservation purchase model.  The Commitment model is not available for new customers or new models introduced after August 2024.  For details on the Commitment purchase model and options for coexistence and migration, please see the [Azure OpenAI Provisioned August Update](../concepts/provisioned-migration.md).
## Hourly usage

Provisioned, Data Zone Provisioned, and Global Provisioned deployments are charged an hourly rate ($/PTU/hr) on the number of PTUs that have been deployed.  For example, a 300 PTU deployment will be charged the hourly rate times 300.  All Azure OpenAI pricing is available in the Azure Pricing Calculator. 

If a deployment exists for a partial hour, it will receive a prorated charge based on the number of minutes it was deployed during the hour.  For example, a deployment that exists for 15 minutes during an hour will receive 1/4th the hourly charge.  

If the deployment size is changed, the costs of the deployment will adjust to match the new number of PTUs.   

:::image type="content" source="../media/provisioned/hourly-billing.png" alt-text="A diagram showing hourly billing." lightbox="../media/provisioned/hourly-billing.png":::

Paying for provisioned, data zoned provisioned, and global provisioned deployments on an hourly basis is ideal for short-term deployment scenarios.  For example: Quality and performance benchmarking of new models, or temporarily increasing PTU capacity to cover an event such as a hackathon.  

Customers that require long-term usage of provisioned, data zoned provisioned, and global provisioned deployments, however, might pay significantly less per month by purchasing a term discount via Azure Reservations as discussed in the next section. 

> [!NOTE]
> It is not recommended to scale production deployments according to incoming traffic and pay for them purely on an hourly basis. There are two reasons for this:
> * The cost savings achieved by purchasing Azure Reservations for Azure OpenAI Provisioned, Data Zone Provisioned, and Global Provisioned are significant, and it will be less expensive in many cases to maintain a deployment sized for full production volume paid for via a reservation than it would be to scale the deployment with incoming traffic.
> * Having unused provisioned quota (PTUs) does not guarantee that capacity will be available to support an increase in the size of the deployment when required. Quota limits the maximum number of PTUs that can be deployed, but it is not a capacity guarantee. Provisioned capacity for each region and model dynamically changes throughout the day and might not be available when required. As a result, it is recommended to maintain a permanent deployment to cover your traffic needs (paid for via a reservation).
> * Charges for deployments on a deleted resource will continue until the resource is purged.  To prevent this, delete a resource’s deployment before deleting the resource.  For more information, see [Recover or purge deleted Azure AI services resources](../../recover-purge-resources.md). 

## Azure Reservations for Azure OpenAI provisioned deployments

Discounts on top of the hourly usage price can be obtained by purchasing an Azure Reservation for Azure OpenAI Provisioned, Data Zone Provisioned, and Global Provisioned. An Azure Reservation is a term-discounting mechanism shared by many Azure products. For example, Compute and Cosmos DB. For Azure OpenAI Provisioned, Data Zone Provisioned, and Global Provisioned, the reservation provides a discount in exchange for committing to payment for fixed number of PTUs for a one-month or one-year period.  

* Azure Reservations are purchased via the Azure portal, not the Azure AI Foundry portal Link to Azure reservation portal.

* Reservations are purchased regionally and can be flexibly scoped to cover usage from a group of deployments. Reservation scopes include: 

    * Individual resource groups or subscriptions 

    * A group of subscriptions in a Management Group 

    * All subscriptions in a billing account 

* New reservations can be purchased to cover the same scope as existing reservations, to allow for discounting of new provisioned deployments.  The scope of existing reservations can also be updated at any time without penalty, for example to cover a new subscription. 

* Reservations for Global, Data Zone, and Regional deployments aren't interchangeable. You need to purchase a separate reservation for each deployment type. 

* Reservations can be canceled after purchase, but credits are limited.   

* If the size of provisioned deployments within the scope of a reservation exceeds the amount of the reservation, the excess is charged at the hourly rate. For example, if deployments amounting to 250 PTUs exist within the scope of a 200 PTU reservation, 50 PTUs will be charged on an hourly basis until the deployment sizes are reduced to 200 PTUs, or a new reservation is created to cover the remaining 50. 

* Reservations guarantee a discounted price for the selected term.  They don't reserve capacity on the service or guarantee that it will be available when a deployment is created. It's highly recommended that customers create deployments prior to purchasing a reservation to prevent from over-purchasing a reservation. 

> [!IMPORTANT] 
> * Capacity availability for model deployments is dynamic and changes frequently across regions and models.  To prevent you from purchasing a reservation for more PTUs than you can use, create deployments first, and then purchase the Azure Reservation to cover the PTUs you have deployed.  This best practice will ensure that you can take full advantage of the reservation discount and prevent you from purchasing a term commitment that you cannot use. 
>
> * The Azure role and tenant policy requirements to purchase a reservation are different than those required to create a deployment or Azure OpenAI resource.  Verify authorization to purchase reservations in advance of needing to do so. See Azure OpenAI [Provisioned reservation documentation](https://aka.ms/oai/docs/ptum-reservations) for more details.

## Important: sizing Azure OpenAI provisioned reservations

The PTU amounts in reservation purchases are independent of PTUs allocated in quota or used in deployments. It's possible to purchase a reservation for more PTUs than you have in quota, or can deploy for the desired region, model, or version.   Credits for over-purchasing a reservation are limited, and customers must take steps to ensure they maintain their reservation sizes in line with their deployed PTUs.  
 
The best practice is to always purchase a reservation after deployments have been created.  This prevents purchasing a reservation and then finding out that the required capacity isn't available for the desired region or model. 
 

Reservations for Global, Data Zone, and Regional deployments aren't interchangeable. You need to purchase a separate reservation for each deployment type.

To assist customers with purchasing the correct reservation amounts. The total number of PTUs in a subscription and region that can be covered by a reservation are listed on the Quotas page of Azure AI Foundry. See the message "PTUs Available for reservation." 

:::image type="content" source="../media/provisioned/available-quota.png" alt-text="A screenshot showing available PTU quota." lightbox="../media/provisioned/available-quota.png":::

Managing Azure Reservations 

After a reservation is created, it is a best practice monitor it to ensure it is receiving the usage you're expecting.  This can be done via the Azure Reservation Portal or Azure Monitor.  Details on these articles and others can be found here: 

* [View Azure reservation utilization](/azure/cost-management-billing/reservations/reservation-utilization) 
* [View Azure Reservation purchase and refund transactions](/azure/cost-management-billing/reservations/view-purchase-refunds) 
* [View amortized benefit costs](/azure/cost-management-billing/reservations/view-amortized-costs) 
* [Charge back Azure Reservation costs](/azure/cost-management-billing/reservations/charge-back-usage)
* [Automatically renew Azure reservations](/azure/cost-management-billing/reservations/reservation-renew)

## Next steps

- [Provisioned Throughput Units (PTU) getting started guide](./provisioned-get-started.md)
- [Provisioned Throughput Units (PTU) concepts](../concepts/provisioned-throughput.md)
- [Provisioned Throughput reservation documentation](https://aka.ms/oai/docs/ptum-reservations) 