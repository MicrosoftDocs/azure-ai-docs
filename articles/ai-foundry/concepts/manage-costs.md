---
title: Plan and Manage Costs
description: Manage Azure AI Foundry costs by estimating expenses, monitoring usage, and setting up alerts for spending anomalies with Microsoft Cost Management.
#customer intent: As an IT admin or developer, I want to estimate and manage costs for Azure AI Foundry so that I can optimize my organization's budget and understand how billing works for different model types.
author: sdgilley
ms.author: sgilley
ms.reviewer: aashishb
ms.date: 10/15/2025
ms.topic: how-to
ai-usage: ai-assisted
ms.service: azure-ai-foundry
---

# Plan and manage costs for Azure AI Foundry

**Managing Azure AI Foundry costs effectively starts with planning.** This article shows you how to estimate expenses before deployment, track spending in real-time, and set up alerts to avoid budget surprises.

**What you'll learn:**
- Estimate costs using the Azure pricing calculator
- Monitor actual spending across different model types
- Create budgets and alerts to control expenses
- Understand billing differences between Azure-hosted and partner models

This article describes how to plan for and manage costs for [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). First, use the Azure pricing calculator to help plan for Azure AI Foundry costs before you add resources. Next, as you add Azure resources, review the estimated costs. After you start using Azure resources, use cost management features to set budgets and monitor costs.

> [!TIP]
> Azure AI Foundry doesn't have a specific page in the Azure pricing calculator. Azure AI Foundry is composed of several other Azure services, some of which are optional. This article shows how to use the pricing calculator to estimate costs for these services.

You use Azure AI services in Azure AI Foundry portal. Costs for Azure AI services are only a portion of the monthly costs in your Azure bill. You're billed for all Azure services and resources used in your Azure subscription, including third-party services. You can also review forecasted costs and identify spending trends to find areas where you might want to act.

## Prerequisites

**To view and analyze costs, you need:**
- An Azure account with read access to Cost Management data
- One of the [supported Azure account types](/azure/cost-management-billing/costs/understand-cost-mgt-data)

**Need to grant access?** See [how to assign access to Cost Management data](/azure/cost-management-billing/costs/assign-access-acm-data).

## Estimate costs before using Azure AI services

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs before you add Azure AI services.

1. Select a product, such as Azure OpenAI, in the Azure pricing calculator.

    :::image type="content" source="../media/manage-costs/azure-openai-pricing-calculator.png" alt-text="Screenshot of selecting Azure OpenAI in the Azure pricing calculator.":::

1. Enter the number of units you plan to use. For example, enter the number of input tokens.

    :::image type="content" source="../media/manage-costs/azure-openai-cost-estimate.png" alt-text="Screenshot of Azure OpenAI cost estimate in the Azure pricing calculator." lightbox="../media/manage-costs/azure-openai-cost-estimate.png":::

1. Select more than one product to estimate costs for multiple products. For example, search for and select Azure AI Search to add potential costs.

    :::image type="content" source="../media/manage-costs/azure-ai-foundry-cost-calculator.png" alt-text="Screenshot showing the cost calculator in Azure." lightbox="../media/manage-costs/azure-ai-foundry-cost-calculator.png":::

As you add new resources to your project, return to this calculator and add the same resource here to update your cost estimates.

## Costs associated with Azure AI Foundry

When you create an Azure AI Foundry resource, you pay to use services like Azure OpenAI, Speech, Content Safety, Vision, Document Intelligence, and Language. Costs vary for each service and for some features within each service. Find more details on the [Azure AI services](https://azure.microsoft.com/pricing/details/cognitive-services/) pricing page.

## Understand the billing model for Azure AI services

Azure AI services run on Azure infrastructure that accrues costs when you deploy the new resource. It's important to understand that extra infrastructure can accrue cost. You need to manage that cost when you make changes to deployed resources.

When you create or use Azure AI services resources, you're charged based on the services that you use. Two billing models are available for Azure AI services:

 - **Serverless API**: With serverless API pricing, you're billed according to the Azure AI services offering you use, based on its billing information.

 - **Commitment tiers**: With commitment tier pricing, you commit to using several service features for a fixed fee, so you have a predictable total cost based on the needs of your workload. You're billed based on the plan you choose. For information on available services, how to sign up, and considerations when buying a plan, see [Quickstart: Purchase commitment tier pricing](/azure/ai-services/commitment-tier).

> [!NOTE]
> If you use the resource above the quota provided by the commitment plan, you pay for the extra usage as described in the overage amount in the Azure portal when you buy a commitment plan.

## Understand the billing model for Foundry Models

### Token-based pricing

Language models understand and process inputs by breaking them down into tokens. For reference, each token is roughly four characters for typical English text. Models that can process images or audio break them down into tokens too for billing purposes. The number of tokens per image or audio content depends on the model and the resolution of the input.

Costs per token vary depending on which model series you choose, but in all cases, models deployed in Azure AI Foundry are charged per 1,000 tokens. For example, Azure OpenAI chat completions model inference is [charged per 1,000 tokens with different rates](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) depending on the model and deployment type. For most models, pricing is now listed in terms of 1 million tokens.

Token costs are for both input and output. For example, suppose you have a 1,000-token JavaScript code sample that you ask a model to convert to Python. You pay for approximately 1,000 tokens for the initial input request sent, and 1,000 more tokens for the output that is received in response for a total of 2,000 tokens.

In practice, for this type of completion call, the token input/output isn't perfectly 1:1. A conversion from one programming language to another can result in a longer or shorter output depending on many factors. One such factor is the value assigned to the `max_tokens` parameter.

### Models sold directly by Azure

Models sold directly by Azure (including Azure OpenAI) are charged directly. They appear as billing meters under each Azure AI Foundry resource. Microsoft handles this billing directly. When you inspect your bill, you see billing meters that account for inputs and outputs for each consumed model.

### Models from partners and community

Models provided by third-party providers, such as Cohere, are billed using Azure Marketplace. Unlike Microsoft billing meters, those entries are associated with the resource group where your Azure AI Foundry resource is deployed instead of to the Azure AI Foundry resource itself. Given model providers charge you directly, you see entries under the category **Marketplace** and **Service Name** *SaaS* accounting for inputs and outputs for each consumed model.

> [!IMPORTANT]
> This distinction between Models Sold Directly by Azure (including Azure OpenAI) and Models from Partners and Community only affects how the model is made available to you and how you are charged. In all cases, models are hosted within Azure cloud, and there's no interaction with external services or providers.

### Fine-tuned models

Azure OpenAI fine-tuning models are charged based on the [number of tokens in your training file](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/pricing-update-token-based-billing-for-fine-tuning-training-%F0%9F%8E%89/4164465). For the latest prices, see the [official pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

Once your fine-tuned model is deployed, you're also charged based on:

- Hosting hours.
- Inference per 1,000 tokens (broken down by input usage and output usage).

The hosting hours cost is important to be aware of because after a fine-tuned model is deployed, it continues to incur an hourly cost regardless of whether you're actively using it. Monitor deployed fine-tuned model costs closely.

> [!IMPORTANT]
> After you deploy a customized model, if at any time the deployment remains inactive for more than 15 days, the deployment is deleted. The deployment of a customized model is *inactive* if the model was deployed more than 15 days ago and no completions or chat completions calls were made to it during a continuous 15-day period.
>
> The deletion of an inactive deployment doesn't delete or affect the underlying customized model, and the customized model can be redeployed at any time.
>
> Each customized (fine-tuned) model that's deployed incurs an hourly hosting cost regardless of whether completions or chat completions calls are being made to the model.

### HTTP Error response code and billing status

If the service performs processing, you're charged even if the status code isn't successful (not 200). For example, a 400 error due to a content filter or input limit, or a 408 error due to a timeout.

If the service doesn't perform processing, you aren't charged. For example, a 401 error due to authentication or a 429 error due to exceeding the rate limit.

## Monitor costs

As you use Azure AI Foundry, you incur costs. Azure resource usage unit costs vary by time intervals (seconds, minutes, hours, and days) or by unit usage (bytes, megabytes, and so on). You can see the incurred costs in [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis).

When you use cost analysis, you view costs in graphs and tables for different time intervals. Some examples are by day, current and prior month, and year. You also view costs against budgets and forecasted costs. Switching to longer views over time can help you identify spending trends so you can see where overspending might occur. If you create budgets, you can also easily see where they're exceeded.

### Monitor Azure AI Foundry costs

You can access cost analysis from the [Azure portal](https://portal.azure.com/).

> [!IMPORTANT]
> Your Azure AI Foundry costs are only a subset of your overall application or solution costs. You need to monitor costs for all Azure resources used in your application or solution.

Here's an example of how to monitor costs for a project. The costs are used as an example only. Your costs vary depending on the services that you use and the amount of usage.

1. Sign in to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).
1. Select your project, then select **Management center** from the left menu.
1. Under the **Resource** heading, select **Overview**.
1. Under the **Resource properties**, select on the resource group link. The [Azure portal](https://portal.azure.com/) opens to the resource group for your Foundry resource.

   :::image type="content" source="../media/manage-costs/azure-cost-analysis-overview.png" alt-text="Screenshot showing the AI Foundry portal with the resource Overview section and resource group highlighted." lightbox="../media/manage-costs/azure-cost-analysis-overview.png":::

1. Select **Cost analysis**.

   :::image type="content" source="../media/manage-costs/azure-cost-overview-filters.png" alt-text="Screenshot of the Azure portal showing the Cost Analysis section under Cost Management.":::

1. You see the cost overview. You can also add filters like the deployment level tags to see the costs based on model deployment, as shown in the following screenshot.

   :::image type="content" source="../media/manage-costs/cost-overview-deployment-tags.png" alt-text="Screenshot of cost overview with deployment level tags." lightbox="../media/manage-costs/cost-overview-deployment-tags.png":::

1. Select **Costs by resource** > **Resources** to open the Cost analysis page.

   :::image type="content" source="../media/manage-costs/azure-cost-analysis-resources.png" alt-text="Screenshot of the Azure portal cost analysis with the button to select costs by resources.":::

1. You can see cost of your Foundry resource and the split of that cost across multiple model deployments under that resource,

   :::image type="content" source="../media/manage-costs/azure-foundry-cost-split.png" alt-text="Screenshot of split of Foundry resource cost across model deployments." lightbox="../media/manage-costs/azure-foundry-cost-split.png":::

### Understand cost breakdown by meter

To understand the breakdown of the cost, use the **Cost Analysis** tool in Azure portal. Follow these steps to understand the cost of inference:

1. Go to [Azure AI Foundry Portal](https://ai.azure.com/?cid=learnDocs).

1. In the upper right corner of the screen, select the name of your Azure AI Foundry resource, or if you're working on an AI project, select the name of the project.

1. Select the name of the project. Azure portal opens in a new window.

1. Under **Cost Management**, select **Cost analysis**.

1. By default, cost analysis is scoped to the selected resource group.

   > [!IMPORTANT]
   > Scope *Cost Analysis* to the resource group where you deployed the Azure AI Foundry resource. The cost meters associated with Models from Partners and Community display under the resource group instead of the Azure AI Foundry resource.

1. Modify **Group by** to **Meter**. You can now see that for this particular resource group, the source of the costs comes from different model series.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter.png" alt-text="Screenshot of how to see the cost by each meter in the resource group." lightbox="../foundry-models/media/manage-cost/cost-by-meter.png":::

#### Models sold directly by Azure

Models sold directly by Azure (including Azure OpenAI) are charged directly. They appear as billing meters under each Azure AI Foundry resource. Microsoft handles this billing directly. When you inspect your bill, you see billing meters that account for inputs and outputs for each consumed model.

:::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Foundry resource is deployed, highlighting the meters for Azure OpenAI and Phi models. Cost is group by meter." lightbox="../foundry-models/media/manage-cost/cost-by-meter-1p.png":::

#### Models from partners and community

Models provided by third-party providers, like Cohere, are billed using Azure Marketplace. As opposite to Microsoft billing meters, those entries are associated with the resource group where your Azure AI Foundry is deployed instead of to the Azure AI Foundry resource itself. Given model providers charge you directly, you see entries under the category **Marketplace** and **Service Name** *SaaS* accounting for inputs and outputs for each consumed model.

:::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Foundry resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by meter." lightbox="../foundry-models/media/manage-cost/cost-by-meter-saas.png":::

> [!IMPORTANT]
> This distinction between Models Sold Directly by Azure (including Azure OpenAI) and Models from Partners and Community only affects how the model is made available to you and how you are charged. In all cases, models are hosted within Azure cloud and there's no interaction with external services or providers.

### Monitor costs by resource

You can get more detailed billing information by grouping costs by resource:

1. In **Cost Analysis**, select **View** > **Cost by resource**.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-resource.png" alt-text="Screenshot of how to see the cost by each resource in the resource group." lightbox="../foundry-models/media/manage-cost/cost-by-resource.png":::

1. Now you can see the resources generating each of the billing meters. To understand the breakdown of what makes up that cost, it can help to modify **Group by** to **Meter** and switching the chart type to **Line**.

1. Azure OpenAI models and Microsoft models are displayed as meters under each Azure AI services resource:

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-resource-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for Azure OpenAI and Microsoft's models. Cost is group by resource." lightbox="../foundry-models/media/manage-cost/cost-by-resource-1p.png":::

1. Some providers' models are displayed as meters under Global resources. The word *Global* **isn't** related to the SKU of the model deployment (for instance, *Global standard*). If you have multiple Azure AI services resources, your bill contains one entry **for each model for each Azure AI services resource**. The resource meters have the format *[model-name]-[GUID]* where *[GUID]* is an identifier unique an associated with a given Azure AI Services resource. You notice billing meters accounting for inputs and outputs for each model you consumed.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-resource-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by resource." lightbox="../foundry-models/media/manage-cost/cost-by-resource-saas.png":::

It's important to understand scope when you evaluate costs associated with Azure AI Services. If your resources are part of the same resource group, you can scope Cost Analysis at that level to understand the effect on costs. If your resources are spread across multiple resource groups, you can scope to the subscription level.

When scoped at a higher level, you often need to add more filters to focus on Azure OpenAI usage. When scoped at the subscription level, you see many other resources that you might not care about in the context of Azure OpenAI cost management. When you scope at the subscription level, navigate to the full **Cost analysis tool** under the **Cost Management** service.

Here's an example of how to use the **Cost analysis tool** to see your accumulated costs for a subscription or resource group:

1. Search for *Cost Management* in the top Azure search bar to navigate to the full service experience, which includes more options such as creating budgets.
1. If necessary, select **change** if the **Scope:** isn't pointing to the resource group or subscription you want to analyze.
1. On the left, select **Reporting + analytics** > **Cost analysis**.
1. On the **All views** tab, select **Accumulated costs**.

:::image type="content" source="../openai/media/manage-costs/cost-analyzer.png" alt-text="Screenshot of cost analysis dashboard showing how to access accumulated costs." lightbox="../openai/media/manage-costs/cost-analyzer.png":::

The cost analysis dashboard shows the accumulated costs that are analyzed depending on what you specified for **Scope**.

:::image type="content" source="../openai/media/manage-costs/subscription.png" alt-text="Screenshot of cost analysis dashboard with scope set to subscription." lightbox="../openai/media/manage-costs/subscription.png":::

If you try to add a filter by service, you can't find Azure OpenAI in the list. This situation occurs because Azure OpenAI has commonality with a subset of Azure AI services where the service level filter is **Cognitive Services**. If you want to see all Azure OpenAI resources across a subscription without any other type of Azure AI services resources, instead scope to **Service tier: Azure OpenAI**:

:::image type="content" source="../openai/media/manage-costs/service-tier.png" alt-text="Screenshot of cost analysis dashboard with service tier highlighted." lightbox="../openai/media/manage-costs/service-tier.png":::

### Monitor costs for models in Azure Marketplace

Azure Marketplace offers serverless API deployments. Model publishers might apply different costs depending on the offering. Each project in the Azure AI Foundry portal has its own subscription with the offering, which you can use to monitor the costs and consumption happening on that project. Use [Microsoft Cost Management](https://azure.microsoft.com/products/cost-management) to monitor the costs:

1. Sign in to [Azure portal](https://portal.azure.com/).

1. Select the portal menu icon to open the left pane.

   :::image type="content" source="../media/manage-costs/azure-portal-menu-icon.png" alt-text="Screenshot of the portal menu icon.":::

1. On the left pane, select **Cost Management + Billing** and then select **Cost Management**.

1. On the left pane, under the section for **Reporting + analytics**, select **Cost Analysis**.

1. Select a view such as **Resources**. The cost associated with each resource is displayed.

   :::image type="content" source="../media/manage-costs/cost-analysis-resource-filter.png" alt-text="Screenshot of the Cost Analysis tool displaying how to show cost per resource." lightbox="../media/manage-costs/cost-analysis-resource-filter.png":::

1. On the **Type** column, select the filter icon to filter all the resources of type **microsoft.saas/resources**. This type corresponds to resources created from offers available in Azure Marketplace. For convenience, you can filter by resource types containing the string **SaaS**.

   :::image type="content" source="../media/manage-costs/filter-resource-type-saas.png" alt-text="Screenshot of how to filter by resource type containing the string SaaS." lightbox="../media/manage-costs/filter-resource-type-saas.png":::

1. One resource is displayed for each model offer per project. Naming of those resources is [Model offer name]-[GUID].

1. Select to expand the resource details to get access to each of the costs meters associated with the resource.

   - **Tier** represents the offering.
   - **Product** is the specific product inside the offering.

   Some model providers might use the same name for both.

   :::image type="content" source="../media/manage-costs/resource-details-cost-meters.png" alt-text="A screenshot showing different resources corresponding to different model offers and their associated meters." lightbox="../media/manage-costs/resource-details-cost-meters.png":::

   > [!TIP]
   > Remember that one resource is created per project, for each plan that your project subscribes to.

1. When you expand the details, costs are reported per each of the meters associated with the offering. Each meter might track different sources of costs like inferencing, or fine tuning. The following meters are displayed (when some cost is associated with them):

   | **Meter** | **Group** | **Description** |
   | ---- | ---- | ---- |
   | paygo-inference-input-tokens | Base model | Costs associated with the tokens used as input for inference of a base model. |
   | paygo-inference-output-tokens | Base model | Costs associated with the tokens generated as output for the inference of base model. |
   | paygo-finetuned-model-inference-hosting | Fine-tuned model | Costs associated with the hosting of an inference endpoint for a fine-tuned model. This value isn't the cost of hosting the model, but the cost of having an endpoint serving it. |
   | paygo-finetuned-model-inference-input-tokens | Fine-tuned model | Costs associated with the tokens used as input for inference of a fine tuned model. |
   | paygo-finetuned-model-inference-output-tokens | Fine-tuned model | Costs associated with the tokens generated as output for the inference of a fine tuned model. |

## Create budgets

**Prevent cost overruns with automated alerts.** [Create budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets) that track your spending limits and [set up alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending) to notify you when costs approach or exceed thresholds.

**Best practice:** Create budgets and alerts for Azure subscriptions and resource groups as part of an overall cost monitoring strategy.

Create budgets with filters for specific resources or services in Azure if you want more granularity in your monitoring. Filters help ensure that you don't accidentally create new resources that cost more money. For more about filter options when you create a budget, see [Group and filter options](/azure/cost-management-billing/costs/group-filter).

> [!IMPORTANT]
> While OpenAI has an option for hard limits that prevent you from going over your budget, Azure OpenAI doesn't currently provide this functionality. You can start automation from action groups as part of your budget notifications to take more advanced actions, but this functionality requires additional custom development.

## Export cost data

You can [export your cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data) to a storage account. Exporting data is helpful when you or others need to do additional data analysis for costs. For example, finance teams can analyze the data by using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended way to retrieve cost datasets.

## Other costs that might accrue

Enabling capabilities such as sending data to Azure Monitor Logs and alerting incur extra costs for those services. These costs are visible under those other services and at the subscription level, but aren't visible when scoped just to your Azure AI services resource.

### Using Azure Prepayment

You can pay for Models Sold Directly by Azure charges with your Azure Prepayment (previously called monetary commitment) credit. However, you can't use Azure Prepayment credit to pay for charges for other provider models because they're billed through Azure Marketplace.

For more information, see [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

## Related content

- [Azure AI Foundry management center](management-center.md)
- [Azure AI Foundry status dashboard](../azure-ai-foundry-status-dashboard-documentation.md)
- Learn [how to optimize your cloud investment with cost management](/azure/cost-management-billing/costs/cost-mgt-best-practices).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/understand/analyze-unexpected-charges).
- Take the [Cost Management](/training/paths/control-spending-manage-bills) guided learning course.
