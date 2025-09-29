---
title: Plan to manage costs for Azure AI Foundry Models
description: Learn how to plan for and manage costs for Azure AI Foundry Models by using cost analysis in the Azure portal.
author: msakande   
ms.author: mopeakande
ms.custom: subject-cost-optimization
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 09/29/2025
ms.reviewer: aashishb
reviewer: aashishb
---

# Plan to manage costs for Azure AI Foundry Models

This article describes how you can view, plan for, and manage costs for Azure AI Foundry Models, including Azure OpenAI in Foundry Models. First, use the Azure pricing calculator to help plan for Azure AI Foundry costs before you add any resources. Later, as you deploy Azure resources, review the estimated costs. After you start using Azure resources, use cost management features to set budgets and monitor costs.

You can also review forecasted costs and identify spending trends to identify areas where you might want to act. Costs for Foundry Models are only a portion of the monthly costs in your Azure bill. Although this article is about planning for and managing costs for Azure AI Foundry Models, you're billed for all Azure services and resources used in your Azure subscription, including the third-party services.


## Prerequisites

* Cost analysis in Cost Management supports most Azure account types, but not all of them. To view the full list of supported account types, see [Understand Cost Management data](/azure/cost-management-billing/costs/understand-cost-mgt-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn). 
* To view cost data, you need at least read access for an Azure account. For information about assigning access to cost management data, see [Assign access to data](/azure/cost-management/assign-access-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

## Estimate costs before using Foundry Models

To learn how to use the Azure pricing calculator to estimate the costs of using Foundry Models, see [Estimate costs before using Azure AI services](../../how-to/costs-plan-manage.md#estimate-costs-before-using-azure-ai-services).

## Understand Foundry Models billing model

Language models understand and process inputs by breaking them down into tokens. For reference, each token is roughly four characters for typical English text. Models that can process images or audio break them down into tokens too for billing purposes. The number of tokens per image or audio content depends on the model and the resolution of the input.

Costs per token vary depending on which model series you choose but in all cases models deployed in Azure AI Foundry are charged per 1,000 tokens. For example, Azure OpenAI chat completions model inference is [charged per 1,000 tokens with different rates](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) depending on the model and [deployment type](../concepts/deployment-types.md). For most models, pricing is now listed in terms of 1 million tokens.

Token costs are for both input and output. For example, suppose you have a 1,000 token JavaScript code sample that you ask a model to convert to Python. You pay for approximately 1,000 tokens for the initial input request sent, and 1,000 more tokens for the output that is received in response for a total of 2,000 tokens.

In practice, for this type of completion call, the token input/output isn't perfectly 1:1. A conversion from one programming language to another could result in a longer or shorter output depending on many factors. One such factor is the value assigned to the `max_tokens` parameter.


### Cost breakdown

To understand the breakdown of the cost, use the **Cost Analysis** tool in Azure portal. Follow these steps to understand the cost of inference:

1. Go to [Azure AI Foundry Portal](https://ai.azure.com/?cid=learnDocs).

1. In the upper right corner of the screen, select the name of your Azure AI Foundry resource (formerly known as Azure AI Services), or if you're working on an AI project, select the name of the project.

1. Select the name of the project. Azure portal opens in a new window.

    :::image type="content" source="../media/manage-cost/view-azure-portal-resource-group.png" alt-text="Screenshot of how to access the resource group details page in Azure portal from Azure AI Foundry portal." lightbox="../media/manage-cost/view-azure-portal-resource-group.png":::

1. Under **Cost Management**, select **Cost analysis**.

1. By default, cost analysis is scoped to the selected resource group.

    > [!IMPORTANT]
    > Scope *Cost Analysis* to the resource group where you deployed the Azure AI Foundry resource. The cost meters associated with [Models from Partners and Community](#models-from-partners-and-community) display under the resource group instead of the Azure AI Foundry resource.

1. Modify **Group by** to **Meter**. You can now see that for this particular resource group, the source of the costs comes from different model series.  

    :::image type="content" source="../media/manage-cost/cost-by-meter.png" alt-text="Screenshot of how to see the cost by each meter in the resource group." lightbox="../media/manage-cost/cost-by-meter.png":::

The following sections explain the entries in detail.

### Models sold directly by Azure 

[Models sold directly by Azure](../concepts/models.md#models-sold-directly-by-azure) (including Azure OpenAI) are charged directly. They appear as billing meters under each Azure AI Foundry resource (formerly known Azure AI Services). Microsoft handles this billing directly. When you inspect your bill, you see billing meters that account for inputs and outputs for each consumed model.

:::image type="content" source="../media/manage-cost/cost-by-meter-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Foundry resource is deployed, highlighting the meters for Azure OpenAI and Phi models. Cost is group by meter." lightbox="../media/manage-cost/cost-by-meter-1p.png":::

### Models from partners and community

Models provided by third-party providers, like Cohere, are billed using Azure Marketplace. As opposite to Microsoft billing meters, those entries are associated with the resource group where your Azure AI Foundry (formerly known as Azure AI Services) is deployed instead of to the Azure AI Foundry resource itself. Given model providers charge you directly, you see entries under the category **Marketplace** and **Service Name** *SaaS* accounting for inputs and outputs for each consumed model.

:::image type="content" source="../media/manage-cost/cost-by-meter-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Foundry resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by meter." lightbox="../media/manage-cost/cost-by-meter-saas.png":::

> [!IMPORTANT]
> This distinction between [Models Sold Directly by Azure ](../concepts/models.md#models-sold-directly-by-azure) (including Azure OpenAI) and [Models from Partners and Community](../concepts/models.md#models-from-partners-and-community) only affects how the model is made available to you and how you are charged. In all cases, models are hosted within Azure cloud and there's no interaction with external services or providers.


### Fine-tuned models

Azure OpenAI fine-tuning models are charged based on the [number of tokens in your training file](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/pricing-update-token-based-billing-for-fine-tuning-training-%F0%9F%8E%89/4164465). For the latest prices, see the [official pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

Once your fine-tuned model is deployed, you're also charged based on:

- Hosting hours
- Inference per 1,000 tokens (broken down by input usage and output usage)

The hosting hours cost is important to be aware of since after a fine-tuned model is deployed, it continues to incur an hourly cost regardless of whether you're actively using it. Monitor deployed fine-tuned model costs closely.

> [!IMPORTANT]
> After you deploy a customized model, if at any time the deployment remains inactive for greater than fifteen (15) days,
> the deployment is deleted. The deployment of a customized model is _inactive_ if the model was deployed more than fifteen (15) days ago
> and no completions or chat completions calls were made to it during a continuous 15-day period.
>
> The deletion of an inactive deployment doesn't delete or affect the underlying customized model,
> and the customized model can be redeployed at any time.
>
> Each customized (fine-tuned) model that's deployed incurs an hourly hosting cost regardless of whether completions
> or chat completions calls are being made to the model. .

### Other costs that might accrue with Foundry Models

Enabling capabilities such as sending data to Azure Monitor Logs and alerting incurs extra costs for those services. These costs are visible under those other services and at the subscription level.


### Using Azure Prepayment

You can pay for Models Sold Directly by Azure charges with your Azure Prepayment credit. However, you can't use Azure Prepayment credit to pay for charges for other provider models given they're billed through Azure Marketplace.

### HTTP Error response code and billing status

If the service performs processing, you're charged even if the status code isn't successful (not 200).
For example, a 400 error due to a content filter or input limit, or a 408 error due to a time-out.

If the service doesn't perform processing, you aren't charged. For example, a 401 error due to authentication or a 429 error due to exceeding the Rate Limit.

## Monitor costs

Azure resource usage unit costs vary by time intervals, such as seconds, minutes, hours, and days, or by unit usage, such as bytes and megabytes. As soon as Azure AI services use starts, costs can be incurred and you can see the costs in the [cost analysis](/azure/cost-management/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

You can get more detailed billing information by using **Cost Analysis**:

To understand the breakdown of what makes up that cost, it can be helpful to use **Cost Analysis** tool in Azure portal.

1. Go to [Azure AI Foundry Portal](https://ai.azure.com/?cid=learnDocs).

1. In the upper right corner of the screen, select on the name of your Azure AI Services resource, or if you're working on an AI project, on the name of the project.

1. Select the name of the project. Azure portal opens in a new window.

1. Under **Cost Management**, select **Cost analysis**.

1. By default, cost analysis is scoped to the resource group you selected.

1. Since you're seeing the cost of all the resource group, it's useful to see the cost by resource. In that case, select **View** > **Cost by resource**.

    :::image type="content" source="../media/manage-cost/cost-by-resource.png" alt-text="Screenshot of how to see the cost by each resource in the resource group." lightbox="../media/manage-cost/cost-by-resource.png":::

1. Now you can see the resources generating each of the billing meters. To understand the breakdown of what makes up that cost, it can help to modify **Group by** to **Meter** and switching the chart type to **Line**.

1. Azure OpenAI models and Microsoft models, as explained earlier, are displayed as meters under each Azure AI services resource:

    :::image type="content" source="../media/manage-cost/cost-by-resource-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for Azure OpenAI and Microsoft's models. Cost is group by resource." lightbox="../media/manage-cost/cost-by-resource-1p.png":::

1. Some providers' models are displayed as meters under Global resources. The word *Global* **isn't** related to the SKU of the model deployment (for instance, *Global standard*). If you have multiple Azure AI services resources, your bill contains one entry **for each model for each Azure AI services resource**. The resource meters have the format *[model-name]-[GUID]* where *[GUID]* is an identifier unique an associated with a given Azure AI Services resource. You notice billing meters accounting for inputs and outputs for each model you consumed.

    :::image type="content" source="../media/manage-cost/cost-by-resource-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by resource." lightbox="../media/manage-cost/cost-by-resource-saas.png":::

It's important to understand scope when you evaluate costs associated with Azure AI Services. If your resources are part of the same resource group, you can scope Cost Analysis at that level to understand the effect on costs. If your resources are spread across multiple resource groups, you can scope to the subscription level.

When scoped at a higher level, you often need to add more filters to focus on Azure OpenAI usage. When scoped at the subscription level, you see many other resources that you might not care about in the context of Azure OpenAI cost management. When you scope at the subscription level, navigate to the full **Cost analysis tool** under the **Cost Management** service.

Here's an example of how to use the **Cost analysis tool** to see your accumulated costs for a subscription or resource group:

1. Search for *Cost Management* in the top Azure search bar to navigate to the full service experience, which includes more options such as creating budgets.
1. If necessary, select **change** if the **Scope:** isn't pointing to the resource group or subscription you want to analyze.
1. On the left, select **Reporting + analytics** > **Cost analysis**.
1. On the **All views** tab, select **Accumulated costs**.

:::image type="content" source="../../openai/media/manage-costs/cost-analyzer.png" alt-text="Screenshot of cost analysis dashboard showing how to access accumulated costs." lightbox="../../openai/media/manage-costs/cost-analyzer.png":::

The cost analysis dashboard shows the accumulated costs that are analyzed depending on what you specified for **Scope**.

:::image type="content" source="../../openai/media/manage-costs/subscription.png" alt-text="Screenshot of cost analysis dashboard with scope set to subscription." lightbox="../../openai/media/manage-costs/subscription.png":::

If you try to add a filter by service, you can't find Azure OpenAI in the list. This situation occurs because Azure OpenAI has commonality with a subset of Azure AI services where the service level filter is **Cognitive Services**. If you want to see all Azure OpenAI resources across a subscription without any other type of Azure AI services resources, instead scope to **Service tier: Azure OpenAI**:

:::image type="content" source="../../openai/media/manage-costs/service-tier.png" alt-text="Screenshot of cost analysis dashboard with service tier highlighted." lightbox="../../openai/media/manage-costs/service-tier.png":::

## Create budgets

Create [budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to manage costs and create [alerts](/azure/cost-management-billing/csots/cost-mgt-alerts-monitor-usage-spending?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that notify stakeholders of spending anomalies and overspending risks. Alerts are based on spending compared to budget and cost thresholds. You create budgets and alerts for Azure subscriptions and resource groups. They're useful as part of an overall cost monitoring strategy.

Create budgets with filters for specific resources or services in Azure if you want more granularity in your monitoring. Filters help ensure that you don't accidentally create new resources that cost you more money. For more information about the filter options available when you create a budget, see [Group and filter options](/azure/cost-management-billing/costs/group-filter?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

> [!IMPORTANT]
> While OpenAI has an option for hard limits that prevent you from going over your budget, Azure OpenAI doesn't currently provide this functionality. You can kick off automation from action groups as part of your budget notifications to take more advanced actions, but this functionality requires additional custom development on your part.  

## Export cost data

You can also [export your cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to a storage account, which is helpful when you need others to do extra data analysis for costs. For example, a finance team can analyze the data using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended way to retrieve cost datasets.

## Other costs

Enabling capabilities such as sending data to Azure Monitor Logs and alerting incurs extra costs for those services. These costs are visible under those other services and at the subscription level, but aren't visible when scoped just to your Azure AI services resource.

## Related content

- Learn [how to optimize your cloud investment with cost management](/azure/cost-management-billing/costs/cost-mgt-best-practices?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/understand/analyze-unexpected-charges?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Take the [Cost Management](/training/paths/control-spending-manage-bills?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) guided learning course.
