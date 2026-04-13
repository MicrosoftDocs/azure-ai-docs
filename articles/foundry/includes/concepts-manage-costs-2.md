---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: aashishb
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Create budgets

**Prevent cost overruns with automated alerts.** [Create budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets) that track your spending limits and [set up alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending) to notify you when costs approach or exceed thresholds.

**Best practice:** Create budgets and alerts for Azure subscriptions and resource groups as part of an overall cost monitoring strategy.

Create budgets with filters for specific resources or services in Azure if you want more granularity in your monitoring. Filters help ensure that you don't accidentally create new resources that cost more money. For more about filter options when you create a budget, see [Group and filter options](/azure/cost-management-billing/costs/group-filter).

> [!IMPORTANT]
> While OpenAI has an option for hard limits that prevent you from going over your budget, Azure OpenAI doesn't currently provide this functionality. You can start automation from action groups as part of your budget notifications to take more advanced actions, but this functionality requires additional custom development.

## Export cost data

You can [export your cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data) to a storage account. Exporting data is helpful when you or others need to do additional data analysis for costs. For example, finance teams can analyze the data by using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended way to retrieve cost datasets.

## Other costs that might accrue

Enabling capabilities such as sending data to Azure Monitor Logs and alerting incur extra costs for those services. These costs are visible under those other services and at the subscription level, but aren't visible when scoped just to your Foundry resource.

### Using Azure Prepayment

You can pay for Models Sold Directly by Azure charges with your Azure Prepayment (previously called monetary commitment) credit. However, you can't use Azure Prepayment credit to pay for charges for other provider models because they're billed through Azure Marketplace.

For more information, see [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).
