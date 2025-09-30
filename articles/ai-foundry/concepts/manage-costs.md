---
title: Plan and manage Costs
description: Manage Azure AI Foundry costs by estimating expenses, monitoring usage, and setting up alerts for spending anomalies with Microsoft Cost Management.
#customer intent: As an IT admin, I want to estimate and manage costs for Azure AI Foundry so that I can optimize my organization's budget.
author: jonburchel
ms.author: jburchel
ms.reviewer: aashishb
ms.date: 09/26/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
---

# Plan and manage costs for Azure AI Foundry

This article describes how to plan for and manage costs for [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). First, use the Azure pricing calculator to help plan for Azure AI Foundry costs before you add any resources. Next, as you add Azure resources, review the estimated costs.

> [!TIP]
> Azure AI Foundry doesn't have a specific page in the Azure pricing calculator. Azure AI Foundry is composed of several other Azure services, some of which are optional. This article provides information on using the pricing calculator to estimate costs for these services.

You use Azure AI services in Azure AI Foundry portal. Costs for Azure AI services are only a portion of the monthly costs in your Azure bill. You're billed for all Azure services and resources used in your Azure subscription, including third-party services.

## Prerequisites

Cost analysis in Microsoft Cost Management supports most Azure account types, but not all of them. To view the full list of supported account types, see [Understand Cost Management data](/azure/cost-management-billing/costs/understand-cost-mgt-data). To view cost data, at a minimum, you need read access for an Azure account. For information about assigning access to Microsoft Cost Management data, see [Assign access to data](/azure/cost-management-billing/costs/assign-access-acm-data).

## Estimate costs before using Azure AI services

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs before you add Azure AI services.

1.  Select a product such as Azure OpenAI in the Azure pricing calculator.

:::image type="content" source="../media/manage-costs/azure-openai-pricing-calculator.png" alt-text="Screenshot of selecting Azure OpenAI in the Azure pricing calculator.":::

1.  Enter the number of units you plan to use. For example, enter the number of input tokens.

:::image type="content" source="../media/manage-costs/azure-openai-cost-estimate.png" alt-text="Screenshot of Azure OpenAI cost estimate in the Azure pricing calculator." lightbox="../media/manage-costs/azure-openai-cost-estimate.png":::

1.  Select more than one product to estimate costs for multiple products. For example, search for and select Azure AI Search to add potential costs.

:::image type="content" source="../media/manage-costs/azure-ai-foundry-cost-calculator.png" alt-text="Screenshot showing the cost calculator in Azure." lightbox="../media/manage-costs/azure-ai-foundry-cost-calculator.png":::

As you add new resources to your project, return to this calculator and add the same resource here to update your cost estimates.

## Costs associated with Azure AI Foundry

When you create an Azure AI Foundry resource, you pay to use services such as Azure OpenAI, Speech, Content Safety, Vision, Document Intelligence, and Language. Costs vary for each service and for some features within each service. You can find more details on the [Azure AI services](https://azure.microsoft.com/pricing/details/cognitive-services/) pricing page.

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

To manage costs, create [budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets) and set up [alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending) that automatically notify stakeholders of spending anomalies and overspending risks. Alerts are based on spending compared to budget and cost thresholds. Create budgets and alerts for Azure subscriptions and resource groups, so they're useful as part of an overall cost monitoring strategy.

Create budgets with filters for specific resources or services in Azure if you want more granularity in your monitoring. Filters help ensure that you don't accidentally create new resources that cost you more money. For more about the filter options when you create a budget, see [Group and filter options](/azure/cost-management-billing/costs/group-filter).

## Export cost data

You can also [export your cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data) to a storage account. Exporting data is helpful when you or others need to do more data analysis for costs. For example, finance teams can analyze the data using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended way to retrieve cost datasets.

## Understand the full billing model for Azure AI services

Azure AI services run on Azure infrastructure that accrues costs along
with Azure AI when you deploy the new resource. It's important to
understand that extra infrastructure might accrue cost. You need to
manage that cost when you make changes to deployed resources.

When you create or use Azure AI services resources, you might get charged based on the services that you use. Two billing models are available for Azure AI services:

 - Serverless API: With serverless API pricing, you're billed according to the Azure AI services offering that you use, based on its billing information.

 - Commitment tiers: With commitment tier pricing, you commit to using several service features for a fixed fee, enabling you to have a predictable total cost based on the needs of your workload. You're billed according to the plan you choose. For information on available services, how to sign up, and considerations when purchasing a plan, see [Quickstart: purchase commitment tier pricing](/azure/ai-services/commitment-tier).

> [!NOTE]
> If you use the resource above the quota provided by the commitment plan, you pay for the extra usage as described in the overage amount in the Azure portal when you purchase a commitment plan.

You can pay for Azure AI services charges with your Azure Prepayment (previously called monetary commitment) credit. However, you can't use Azure Prepayment credit to pay for charges for third-party products and services, including ones from Azure Marketplace.

For more information, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

## Related content

- [Azure AI Foundry management center](management-center.md)
- [Azure AI Foundry status dashboard](../azure-ai-foundry-status-dashboard-documentation.md)
