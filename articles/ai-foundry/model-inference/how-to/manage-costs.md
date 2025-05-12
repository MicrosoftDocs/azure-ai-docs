---
title: Plan to manage costs for Azure AI Foundry Models in Azure AI Foundry Service
description: Learn how to plan for and manage costs for Azure AI Foundry Models in Azure AI Foundry Service by using cost analysis in the Azure portal.
author: santiagxf
ms.author: fasantia 
ms.custom: subject-cost-optimization
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
---


# Plan to manage costs for Azure AI Foundry Models in Azure AI Foundry Service

This article describes how you can view, plan for, and manage costs for Foundry Models in Azure AI Foundry Service.

Although this article is about planning for and managing costs for Foundry Models in Azure AI Foundry Service, you're billed for all Azure services and resources used in your Azure subscription.

## Prerequisites

* Cost analysis in Cost Management supports most Azure account types, but not all of them. To view the full list of supported account types, see [Understand Cost Management data](/azure/cost-management-billing/costs/understand-cost-mgt-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn). 
* To view cost data, you need at least read access for an Azure account. For information about assigning access to cost management data, see [Assign access to data](/azure/cost-management/assign-access-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).


## Understand Foundry Models billing model

Language models understand and process inputs by breaking them down into tokens. For reference, each token is roughly four characters for typical English text. Models that can process images or audio break down them into tokens too for billing purposes. The number of tokens per image or audio content depends on the model and the resolution of the input.

Costs per token vary depending on which model series you choose but in all cases models deployed in Azure AI Services are charged per 1,000 tokens. Token costs are for both input and output. For example, suppose you have a 1,000 token JavaScript code sample that you ask a model to convert to Python. You would be charged approximately 1,000 tokens for the initial input request sent, and 1,000 more tokens for the output that is received in response for a total of 2,000 tokens.

### Cost breakdown

To understand the breakdown of what makes up the cost, it can be helpful to use **Cost Analysis** tool in Azure portal. Follow these steps to understand the cost of inference:

1. Go to [Azure AI Foundry Portal](https://ai.azure.com).

2. In the upper right corner of the screen, select on the name of your Azure AI Services resource, or if you're working on an AI project, on the name of the project.

3. Select the name of the project. Azure portal opens in a new window.

    :::image type="content" source="../media/manage-cost/view-azure-portal-resource-group.png" alt-text="Screenshot of how to access the resource group details page in Azure portal from Azure AI Foundry portal." lightbox="../media/manage-cost/view-azure-portal-resource-group.png":::

4. Under **Cost Management** select **Cost analysis**

5. By default, cost analysis is scoped to the selected resource group.

    > [!IMPORTANT]
    > It's important to scope *Cost Analysis* to the resource group where the Azure AI Services resource is deployed. Cost meters associated with some provider model providers, like Mistral AI or Cohere, are displayed under the resource group instead of the Azure AI Services resource.

6. Modify **Group by** to **Meter**. You can now see that for this particular resource group, the source of the costs comes from different models series.  

    :::image type="content" source="../media/manage-cost/cost-by-meter.png" alt-text="Screenshot of how to see the cost by each meter in the resource group." lightbox="../media/manage-cost/cost-by-meter.png":::

The following sections explain the entries in details.

### Azure OpenAI and Microsoft models

Azure OpenAI models and models offered as first-party consumption services from Microsoft (including DeepSeek family and Phi family of models) are charged directly and they show up as billing meters under each Azure AI services resource. This billing happens directly through Microsoft. When you inspect your bill, you notice billing meters accounting for inputs and outputs for each consumed model.

:::image type="content" source="../media/manage-cost/cost-by-meter-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for Azure OpenAI and Microsoft's models. Cost is group by meter." lightbox="../media/manage-cost/cost-by-meter-1p.png":::

### Provider models

Models provided by another provider, like Mistral AI, Cohere, Meta AI, or AI21 Labs, are billed using Azure Marketplace. As opposite to Microsoft billing meters, those entries are associated with the resource group where your Azure AI services is deployed instead of to the Azure AI Services resource itself. Given model providers charge you directly, you see entries under the category **Marketplace** and **Service Name** *SaaS* accounting for inputs and outputs for each consumed model.

:::image type="content" source="../media/manage-cost/cost-by-meter-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by meter." lightbox="../media/manage-cost/cost-by-meter-saas.png":::

> [!IMPORTANT]
> This distinction between Azure OpenAI, Microsoft-offered models, and provider models only affects how the model is made available to you and how you are charged. In all cases, models are hosted within Azure cloud and there is no interaction with external services or providers.

### Using Azure Prepayment

You can pay for Azure OpenAI and Microsoft's models charges with your Azure Prepayment credit. However, you can't use Azure Prepayment credit to pay for charges for other provider models given they're billed through Azure Marketplace.

### HTTP Error response code and billing status

If the service performs processing, you're charged even if the status code isn't successful (not 200).
For example, a 400 error due to a content filter or input limit, or a 408 error due to a time-out.

If the service doesn't perform processing, you aren't charged. For example, a 401 error due to authentication or a 429 error due to exceeding the Rate Limit.

## Monitor costs

Azure resource usage unit costs vary by time intervals, such as seconds, minutes, hours, and days, or by unit usage, such as bytes and megabytes. As soon as Azure AI services use starts, costs can be incurred and you can see the costs in the [cost analysis](/azure/cost-management/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

You can get more detailed billing information by using **Cost Analysis**:

To understand the breakdown of what makes up that cost, it can be helpful to use **Cost Analysis** tool in Azure portal.

1. Go to [Azure AI Foundry Portal](https://ai.azure.com).

2. In the upper right corner of the screen, select on the name of your Azure AI Services resource, or if you're working on an AI project, on the name of the project.

3. Select the name of the project. Azure portal opens in a new window.

4. Under **Cost Management** select **Cost analysis**

5. By default, cost analysis is scoped to the resource group you have selected.

6. Since we're seeing the cost of all the resource group, it's useful to see the cost by resource. In that case, select **View** > **Cost by resource**.

    :::image type="content" source="../media/manage-cost/cost-by-resource.png" alt-text="Screenshot of how to see the cost by each resource in the resource group." lightbox="../media/manage-cost/cost-by-resource.png":::

7. Now you can see the resources generating each of the billing meters.

8. Azure OpenAI models and Microsoft models, as explained before, are displayed as meters under each Azure AI services resource:

    :::image type="content" source="../media/manage-cost/cost-by-resource-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for Azure OpenAI and Microsoft's models. Cost is group by resource." lightbox="../media/manage-cost/cost-by-resource-1p.png":::

9. Some providers' models are displayed as meters under Global resources. Notice that the word *Global* **isn't** related to the SKU of the model deployment (for instance, *Global standard*). If you have multiple Azure AI services resources, your bill contains one entry **for each model for each Azure AI services resource**. The resource meters have the format *[model-name]-[GUID]* where *[GUID]* is an identifier unique an associated with a given Azure AI Services resource. You notice billing meters accounting for inputs and outputs for each model you have consumed.

    :::image type="content" source="../media/manage-cost/cost-by-resource-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Azure AI Services resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by resource." lightbox="../media/manage-cost/cost-by-resource-saas.png":::

It's important to understand scope when you evaluate costs associated with Azure AI Services. If your resources are part of the same resource group, you can scope Cost Analysis at that level to understand the effect on costs. If your resources are spread across multiple resource groups, you can scope to the subscription level.

## Create budgets

You can create [budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to manage costs and create [alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that notify stakeholders of spending anomalies and overspending risks. Alerts are based on spending compared to budget and cost thresholds. You create budgets and alerts for Azure subscriptions and resource groups. They're useful as part of an overall cost monitoring strategy.

You can create budgets with filters for specific resources or services in Azure if you want more granularity present in your monitoring. Filters help ensure that you don't accidentally create new resources that cost you more money. For more information about the filter options available when you create a budget, see [Group and filter options](/azure/cost-management-billing/costs/group-filter?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).


## Export cost data

You can also [export your cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to a storage account, which is helpful when you need others to do extra data analysis for costs. For example, a finance team can analyze the data using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. We recommend exporting cost data as the way to retrieve cost datasets.

## Other costs

Enabling capabilities such as sending data to Azure Monitor Logs and alerting incurs extra costs for those services. These costs are visible under those other services and at the subscription level, but aren't visible when scoped just to your Azure AI services resource.

## Next steps

- Learn [how to optimize your cloud investment with cost management](/azure/cost-management-billing/costs/cost-mgt-best-practices?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/understand/analyze-unexpected-charges?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Take the [Cost Management](/training/paths/control-spending-manage-bills?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) guided learning course.
