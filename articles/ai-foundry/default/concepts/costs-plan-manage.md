---
title: Manage Costs for Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn to plan, analyze, and monitor expenses for AI services in Azure. Create budgets and export cost data for better control.
ms.author: mopeakande
manager: nitinme
author: msakande 
ms.reviewer: aashishb
reviewer: aashishb
ms.date: 08/26/2025
ms.service: azure-ai-foundry
ms.topic: concept-article
# see also: ai-foundry/how-to/costs-plan-manage.md
---

# Manage Costs for Azure AI Foundry

This article describes how to plan for and manage costs for [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). First, use the Azure pricing calculator to help plan for Azure AI Foundry costs before you add any resources. Next, as you add Azure resources, review the estimated costs.

> [!TIP]
> Azure AI Foundry doesn't have a specific page in the Azure pricing calculator. Azure AI Foundry is composed of several other Azure services, some of which are optional. This article provides information on using the pricing calculator to estimate costs for these services.

You use Azure AI services in Azure AI Foundry portal. Costs for Azure AI services are only a portion of the monthly costs in your Azure bill. You're billed for all Azure services and resources used in your Azure subscription, including third-party services.

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

## Prerequisites

Cost analysis in Microsoft Cost Management supports most Azure account types, but not all of them. To view the full list of supported account types, see [Understand Cost Management data](/azure/cost-management-billing/costs/understand-cost-mgt-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn). To view cost data, at a minimum, you need read access for an Azure account. For information about assigning access to Microsoft Cost Management data, see [Assign access to data](/azure/cost-management-billing/costs/assign-access-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

## Estimate costs before using Azure AI services

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs before you add Azure AI services.

1. Select a product such as Azure OpenAI in the Azure pricing calculator.

    :::image type="content" source="../../media/cost-management/pricing-calculator-select-product.png" alt-text="Screenshot of selecting Azure OpenAI in the Azure pricing calculator." lightbox="../../media/cost-management/pricing-calculator-select-product.png":::

1. Enter the number of units you plan to use. For example, enter the number of input tokens.

    :::image type="content" source="../../media/cost-management/pricing-calculator-estimate-openai.png" alt-text="Screenshot of Azure OpenAI cost estimate in the Azure pricing calculator." lightbox="../../media/cost-management/pricing-calculator-estimate-openai.png":::

1. Select more than one product to estimate costs for multiple products. For example, search for and select Virtual Machines to add potential costs for compute resources.

    :::image type="content" source="../../media/cost-management/pricing-calculator-estimate.png" alt-text="Screenshot of total estimate in the Azure pricing calculator." lightbox="../../media/cost-management/pricing-calculator-estimate.png":::

As you add new resources to your project, return to this calculator and add the same resource here to update your cost estimates.

## Monitor costs

As you use Azure AI Foundry, you incur costs. Azure resource usage unit costs vary by time intervals (seconds, minutes, hours, and days) or by unit usage (bytes, megabytes, and so on). You can see the incurred costs in [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

When you use cost analysis, you view costs in graphs and tables for different time intervals. Some examples are by day, current and prior month, and year. You also view costs against budgets and forecasted costs. Switching to longer views over time can help you identify spending trends so you can see where overspending might occur. If you create budgets, you can also easily see where they're exceeded.

### Monitor Azure AI Foundry costs

You can access cost analysis from the [Azure portal](https://portal.azure.com).

> [!IMPORTANT]
> Your Azure AI Foundry costs are only a subset of your overall application or solution costs. You need to monitor costs for all Azure resources used in your application or solution.

For more information, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

### Monitor costs for models offered through the Azure Marketplace

Azure Marketplace offers serverless API deployments. Model publishers might apply different costs depending on the offering. Each project in the Azure AI Foundry portal has its own subscription with the offering, which you can use to monitor the costs and consumption happening on that project. Use [Microsoft Cost Management](https://azure.microsoft.com/products/cost-management) to monitor the costs:

1. Sign in to [Azure portal](https://portal.azure.com).

1. Select the portal menu icon to open the left pane.

    :::image type="content" source="../../media/cost-management/project-costs/portal-menu-icon.png" alt-text="Screenshot of the portal menu icon." lightbox="../../media/cost-management/project-costs/portal-menu-icon.png":::

1. On the left pane, select **Cost Management + Billing** and then select **Cost Management**.

1. On the left pane, under the section for **Reporting + analytics**, select **Cost Analysis**.

1. Select a view such as **Resources**. The cost associated with each resource is displayed.

    :::image type="content" source="../../media/cost-management/marketplace/costs-model-as-service-cost-analysis.png" alt-text="A screenshot of the Cost Analysis tool displaying how to show cost per resource." lightbox="../../media/cost-management/marketplace/costs-model-as-service-cost-analysis.png":::

1. On the **Type** column, select the filter icon to filter all the resources of type **microsoft.saas/resources**. This type corresponds to resources created from offers available in Azure Marketplace. For convenience, you can filter by resource types containing the string **SaaS**. 

    :::image type="content" source="../../media/cost-management/marketplace/costs-model-as-service-cost-filter.png" alt-text="A screenshot of how to filter by resource type containing the string 'SaaS'." lightbox="../../media/cost-management/marketplace/costs-model-as-service-cost-filter.png":::

1. One resource is displayed for each model offer per project. Naming of those resources is `[Model offer name]-[GUID]`.

1. Select to expand the resource details to get access to each of the costs meters associated with the resource. 

    - **Tier** represents the offering.
    - **Product** is the specific product inside the offering. 
    
    Some model providers might use the same name for both.

    :::image type="content" source="../../media/cost-management/marketplace/costs-model-as-service-cost-details.png" alt-text="A screenshot showing different resources corresponding to different model offers and their associated meters." lightbox="../../media/cost-management/marketplace/costs-model-as-service-cost-details.png":::

    > [!TIP]
    > Remember that one resource is created per project, for each plan that your project subscribes to.

1. When you expand the details, costs are reported per each of the meters associated with the offering. Each meter might track different sources of costs like inferencing, or fine tuning. The following meters are displayed (when some cost is associated with them):

    | Meter | Group | Description |
    |-----|-----|-----|
    | `paygo-inference-input-tokens` | Base model | Costs associated with the tokens used as input for inference of a base model. |
    | `paygo-inference-output-tokens` | Base model | Costs associated with the tokens generated as output for the inference of base model.|
    | `paygo-finetuned-model-inference-hosting` | Fine-tuned model | Costs associated with the hosting of an inference endpoint for a fine-tuned model. This value isn't the cost of hosting the model, but the cost of having an endpoint serving it. |
    | `paygo-finetuned-model-inference-input-tokens`  | Fine-tuned model | Costs associated with the tokens used as input for inference of a fine tuned model. |
    | `paygo-finetuned-model-inference-output-tokens` | Fine-tuned model | Costs associated with the tokens generated as output for the inference of a fine tuned model. |


## Create budgets

To manage costs, create [budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) and set up [alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that automatically notify stakeholders of spending anomalies and overspending risks. Alerts are based on spending compared to budget and cost thresholds. Create budgets and alerts for Azure subscriptions and resource groups, so they're useful as part of an overall cost monitoring strategy. 

Create budgets with filters for specific resources or services in Azure if you want more granularity in your monitoring. Filters help ensure that you don't accidentally create new resources that cost you more money. For more about the filter options when you create a budget, see [Group and filter options](/azure/cost-management-billing/costs/group-filter?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

## Export cost data

You can also [export your cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to a storage account. Exporting data is helpful when you or others need to do more data analysis for costs. For example, finance teams can analyze the data using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended way to retrieve cost datasets.


## Understand the full billing model for Azure AI services

Azure AI services run on Azure infrastructure that accrues costs along with Azure AI when you deploy the new resource. It's important to understand that extra infrastructure might accrue cost. You need to manage that cost when you make changes to deployed resources.

When you create or use Azure AI services resources, you might get charged based on the services that you use. Two billing models are available for Azure AI services: 

- Serverless API: With serverless API pricing, you're billed according to the Azure AI services offering that you use, based on its billing information.
- Commitment tiers: With commitment tier pricing, you commit to using several service features for a fixed fee, enabling you to have a predictable total cost based on the needs of your workload. You're billed according to the plan you choose. For information on available services, how to sign up, and considerations when purchasing a plan, see [Quickstart: purchase commitment tier pricing](../../../ai-services/commitment-tier.md).

> [!NOTE]
> If you use the resource above the quota provided by the commitment plan, you pay for the extra usage as described in the overage amount in the Azure portal when you purchase a commitment plan. 

You can pay for Azure AI services charges with your Azure Prepayment (previously called monetary commitment) credit. However, you can't use Azure Prepayment credit to pay for charges for third-party products and services, including ones from Azure Marketplace.

For more information, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

## Next steps

- Learn [how to optimize your cloud investment with Microsoft Cost Management](/azure/cost-management-billing/costs/cost-mgt-best-practices?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/cost-management-billing-overview?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Take the [Cost Management](/training/paths/control-spending-manage-bills?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) guided learning course.
