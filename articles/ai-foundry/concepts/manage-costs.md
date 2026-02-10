---
title: Plan and Manage Costs
titleSuffix: Microsoft Foundry
description: Manage Microsoft Foundry costs by estimating expenses, monitoring usage, and setting up alerts for spending anomalies with Microsoft Cost Management.
#customer intent: As an IT admin or developer, I want to estimate and manage costs for Microsoft Foundry so that I can optimize my organization's budget and understand how billing works for different model types.
author: sdgilley
ms.author: sgilley
ms.reviewer: aashishb
ms.date: 01/13/2026
ms.topic: how-to
ms.custom: dev-focus
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
---

# Plan and manage costs for Microsoft Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article shows you how to estimate expenses before deployment, track spending in real time, and set up alerts to avoid budget surprises.

## Prerequisites

Before you begin, ensure you have:

- **Azure subscription:** An active Azure subscription with the resources you want to monitor.
- **Role-based access control (RBAC):** One or both of the following roles at the subscription or resource group scope:
  - [**Cost Management Reader**](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) – View costs and usage data.
  - [**AI User**](rbac-foundry.md#built-in-roles) – View Foundry resource data and costs.
- **Supported Azure account type:** One of the [supported account types for Cost Management](/azure/cost-management-billing/costs/understand-cost-mgt-data).

If you need to grant these roles to team members, see [Assign access to Cost Management data](/azure/cost-management-billing/costs/assign-access-acm-data) and [Foundry RBAC roles](rbac-foundry.md).

> [!NOTE]
> Foundry doesn't have a dedicated page in the Azure pricing calculator because Foundry is composed of several optional Azure services. This article shows how to use the calculator to estimate costs for these services.

## Estimate costs before using Foundry

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs before you add Foundry resources.

1. Go to the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).
1. Search for and select a product, such as Azure Speech in Foundry or Azure Language in Foundry.
1. Select additional products to estimate costs for multiple services. For example, add Azure AI Search to include potential search costs.
1. As you add resources to your project, return to the calculator and update estimates.

**Reference:** [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/)

## Costs associated with Foundry

When you create a Foundry resource, you pay for the Azure services you use, such as Azure OpenAI, Azure Speech in Foundry, Content Safety, Azure Vision in Foundry, Azure Document Intelligence, and Azure Language in Foundry. Costs vary by service and feature. For details, see the [Foundry Tools pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/).

## Understand billing models for Foundry

Foundry resources run on Azure infrastructure and accrue costs when deployed. When you create or use Foundry resources, you're charged based on the services you use.

Two billing models are available:

- **Pay-as-you-go (Serverless API):** You're billed according to your usage of each Azure service.
- **Commitment tiers:** You commit to using service features for a fixed fee, providing predictable costs. For details, see [Commitment tier pricing](/azure/ai-services/commitment-tier).

> [!NOTE]
> If you use the resource above the quota provided by the commitment plan, you pay for the extra usage as described in the overage amount in the Azure portal when you buy a commitment plan.

## Understand the billing model for Foundry Models

### Token-based pricing

Language and vision models process inputs by breaking them down into tokens. Each token is roughly four characters of text; image and audio content are also converted to tokens for billing. You're charged per 1,000 tokens (input and output combined). Token pricing varies by model series and deployment type. For the latest rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

### Models sold directly by Azure

Models sold directly by Azure (including Azure OpenAI) appear as billing meters under each Foundry resource. Microsoft handles billing directly; you see separate meters for each model's input and output usage.

::: moniker range="foundry-classic"

### Models from partners and community

Third-party provider models (such as Cohere) are billed via Azure Marketplace. These entries appear at the resource group level (not the Foundry resource level) under **Marketplace** > **Service Name** *SaaS*, with separate meters for inputs and outputs.

> [!IMPORTANT]
> All models, whether Microsoft-sold or third-party, are hosted in Azure cloud with no external service interaction. Billing location differences affect cost analysis but not actual charges.

::: moniker-end

### Fine-tuned models

Azure OpenAI fine-tuned models are charged in three ways:

- **Training:** Charged per token in your training file.
- **Hosting:** Hourly cost per deployed model (applies even if the model is unused).
- **Inference:** Per 1,000 tokens (input and output) when the model is called.

Monitor hosted fine-tuned model costs closely to avoid unexpected charges. For current rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

> [!IMPORTANT]
> Inactive deployments (unused for 15 consecutive days) are deleted automatically. This deletion doesn't affect the underlying model; you can redeploy it at any time. However, deployed fine-tuned models incur hourly hosting costs even if inactive, so remove unused deployments promptly to control costs.

### HTTP Error response code and billing status

If the service performs processing, you're charged even if the status code isn't successful (not 200). For example, a 400 error due to a content filter or input limit, or a 408 error due to a timeout.

If the service doesn't perform processing, you aren't charged. For example, a 401 error due to authentication or a 429 error due to exceeding the rate limit.

## Monitor costs

Track your Foundry spending using cost analysis tools. You can view costs by day, month, or year, compare against budgets, and identify spending trends.

:::moniker range="foundry-classic"
Access cost information from the [!INCLUDE [classic-link](../includes/classic-link.md)] portal or the [Azure portal](https://portal.azure.com/).
:::moniker-end
:::moniker range="foundry"
Access cost information from the [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] portal or the [Azure portal](https://portal.azure.com/).
:::moniker-end

**Reference:** [Cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis)

> [!IMPORTANT]
> Your Foundry costs are only a subset of your overall application or solution costs. You need to monitor costs for all Azure resources used in your application or solution.

### Configure permissions to view costs

To view Foundry costs, ensure you have the [AI User role](rbac-foundry.md#built-in-roles) and [Cost Management Reader role](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) at the resource group or subscription level.

Or you can create the following custom rules:

* `Microsoft.Consumption/*/read`
* `Microsoft.CostManagement/*/read`
* `Microsoft.Resources/subscriptions/read`
* `Microsoft.CognitiveServices/accounts/AIServices/usage/read`

> [!NOTE]
> You need the **Owner** role at the subscription or resource group scope to create custom roles in that scope.
> 

To create a custom role, use one of the following articles:

* [Azure portal](/azure/role-based-access-control/custom-roles-portal)
* [Azure CLI](/azure/role-based-access-control/custom-roles-cli)
* [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)

For more information about custom roles, see [Azure custom roles](/azure/role-based-access-control/custom-roles).

To create a custom role, construct a role definition JSON file that specifies the permission and scope for the role. The following example defines a custom Foundry Cost Reader role scoped at a specific resource level:

```json
{
    "Name": "Foundry Cost Reader",
    "IsCustom": true,
    "Description": "Can see cost metrics in Foundry",
    "Actions": [
        "Microsoft.Consumption/*/read",
        "Microsoft.CostManagement/*/read",
        "Microsoft.Resources/subscriptions/read",
        "Microsoft.CognitiveServices/accounts/AIServices/usage/read"
    ],
    "NotActions": [],
    "DataActions": [],
    "NotDataActions": [],
    "AssignableScopes": [
        "/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.CognitiveServices/accounts/<foundryResourceName>"
    ]
}
```

Replace `<subscriptionId>`, `<resourceGroupName>`, and `<foundryResourceName>` with your actual values.

:::moniker range="foundry"

## Monitor in Foundry portal

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Use the sections below to monitor costs.

> [!NOTE]
> Estimates do not reflect discounts or contracted pricing that may appear on your final bill. Estimates cover standard deployment costs only, not [provisioned throughput](../openai/concepts/provisioned-throughput.md).

### Agent costs

1. Select **Operate** in the upper-right navigation.
1. Select **Overview** in the left pane.
1. At the top of the page, select the subscription, one or more projects, and a date range. 
1. The **Estimated cost** tile shows estimates of all the agents for the selected project(s) for the selected dates.  These estimates do not currently include prompt agent and non-Foundry agent costs.

:::image type="content" source="media/manage-costs/agent-costs.png" alt-text="Screenshot of the Agents tab under Assets, showing the Estimated costs column with monthly cost estimates for each agent based on configuration and usage." lightbox="media/manage-costs/agent-costs.png":::

For individual agent estimates:

1. Select **Assets** in the left pane.
1. Select the **Agents** tab.
1. The **Estimated costs** column shows monthly estimates based on agent configuration and usage patterns.

**Reference:** [Agent concepts](../default/agents/concepts/development-lifecycle.md)

:::image type="content" source="../default/media/manage-costs/agent-list.png" alt-text="Screenshot of the Agents tab showing a list of agents with columns for Name, Status, and Estimated costs. The Estimated costs column displays monthly values." lightbox="../default/media/manage-costs/agent-list.png":::

To view detailed agent costs:

1. Select **Build** in the upper-right navigation.
1. Select **Agents** in the left pane.
1. Select an agent.
1. Select the **Monitor** tab.
1. Set the date range in the upper-right corner.
1. View token costs and usage metrics for the selected range.

**Reference:** [Monitor agent metrics](../agents/how-to/metrics.md)

:::image type="content" source="../default/media/manage-costs/agent-build-cost.png" alt-text="Screenshot of the Build page showing the Models pane with a selected model highlighted." lightbox="../default/media/manage-costs/agent-build-cost.png":::

### Model deployment costs

1. Select **Build** in the upper-right navigation.
1. Select **Models** in the left pane.
1. Select a model.
1. Select the **Monitor** tab.
1. Set the date range in the upper-right corner.
You see total cost and an estimated cost chart for the selected range.

**Reference:** [Monitor models](../foundry-models/how-to/monitor-models.md) 

:::image type="content" source="../default/media/manage-costs/model-costs.png" alt-text="Screenshot of Azure portal showing the Monitor tab with total cost and estimated cost chart for a selected model and date range." lightbox="../default/media/manage-costs/model-costs.png":::

When you select **View More Details** or **Azure Cost Management**, you're directed to the Azure portal's **Cost Management** section. Note: Azure portal costs show aggregated charges for the entire Cognitive Services account, not individual models. Costs display in USD only.

> [!NOTE]
> Token and request charts can sometimes show lower values than the **Estimated cost** view because late‑arrival usage events may not be included in those charts. If there’s a mismatch, rely on **Estimated cost** as the most accurate view, and note that your **Azure Cost Management invoice** remains the final source of truth.

:::moniker-end

## Monitor in Azure portal

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. View costs for your resource group or individual Foundry resource.

    [!INCLUDE [find-region](../includes/find-region.md)]

1. In the Azure portal, select **Cost analysis** under **Cost Management** (for your resource group or Foundry resource).

1. View the cost overview. Optionally, add filters (deployment tags, user-defined tags) to segment costs by model deployment:

   :::image type="content" source="../media/manage-costs/cost-overview-deployment-tags.png" alt-text="Screenshot of cost overview showing deployment-level tags filter." lightbox="../media/manage-costs/cost-overview-deployment-tags.png":::

1. Select **Costs by resource** > **Resources** to see your Foundry resource cost split across model deployments:

   :::image type="content" source="../media/manage-costs/azure-foundry-cost-split.png" alt-text="Screenshot of split of Foundry resource cost across model deployments." lightbox="../media/manage-costs/azure-foundry-cost-split.png":::

### Understand cost breakdown by meter

Use the **Cost Analysis** tool to view costs grouped by billing meter:


1. Sign in to the [Azure portal](https://portal.azure.com/) and select your resource group.
1. Select **Cost analysis** under **Cost Management**.

1. By default, cost analysis is scoped to the selected resource group.

   > [!IMPORTANT]
   > Scope *Cost Analysis* to the resource group where you deployed the Foundry resource. The cost meters associated with Models from Partners and Community display under the resource group instead of the Foundry resource.

1. Modify **Group by** to **Meter**. You can now see that for this particular resource group, the source of the costs comes from different model series.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter.png" alt-text="Screenshot of how to see the cost by each meter in the resource group." lightbox="../foundry-models/media/manage-cost/cost-by-meter.png":::

#### Models sold directly by Azure

Models sold directly by Azure (including Azure OpenAI) are charged directly. They appear as billing meters under each Foundry resource. Microsoft handles this billing directly. When you inspect your bill, you see billing meters that account for inputs and outputs for each consumed model.

:::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry resource is deployed, highlighting the meters for Azure OpenAI and Phi models. Cost is group by meter." lightbox="../foundry-models/media/manage-cost/cost-by-meter-1p.png":::

::: moniker range="foundry-classic"
#### Models from partners and community

Models provided by third-party providers, like Cohere, are billed using Azure Marketplace. As opposite to Microsoft billing meters, those entries are associated with the resource group where your Foundry is deployed instead of to the Foundry resource itself. Given model providers charge you directly, you see entries under the category **Marketplace** and **Service Name** *SaaS* accounting for inputs and outputs for each consumed model.

:::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by meter." lightbox="../foundry-models/media/manage-cost/cost-by-meter-saas.png":::

> [!IMPORTANT]
> This distinction between Models Sold Directly by Azure (including Azure OpenAI) and Models from Partners and Community only affects how the model is made available to you and how you are charged. In all cases, models are hosted within Azure cloud and there's no interaction with external services or providers.
::: moniker-end

### Monitor costs by resource

You can get more detailed billing information by grouping costs by resource:

1. In **Cost Analysis**, select **View** > **Cost by resource**.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-resource.png" alt-text="Screenshot of how to see the cost by each resource in the resource group." lightbox="../foundry-models/media/manage-cost/cost-by-resource.png":::

1. Now you can see the resources generating each of the billing meters. To understand the breakdown of what makes up that cost, it can help to modify **Group by** to **Meter** and switching the chart type to **Line**.

1. Azure OpenAI models and Microsoft models are displayed as meters under each Foundry Tool resource.

1. Some providers' models are displayed as meters under Global resources. The word *Global* **isn't** related to the SKU of the model deployment (for instance, *Global standard*). If you have multiple Foundry Tool resources, your bill contains one entry **for each model for each Foundry Tool resource**. The resource meters have the format *[model-name]-[GUID]* where *[GUID]* is an identifier unique an associated with a given Foundry Tools resource. You notice billing meters accounting for inputs and outputs for each model you consumed.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-resource-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry Tools resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by resource." lightbox="../foundry-models/media/manage-cost/cost-by-resource-saas.png":::

It's important to understand scope when you evaluate costs associated with Foundry Tools. If your resources are part of the same resource group, you can scope Cost Analysis at that level to understand the effect on costs. If your resources are spread across multiple resource groups, you can scope to the subscription level.

When scoped at a higher level, you often need to add more filters to focus on Azure OpenAI usage. When scoped at the subscription level, you see many other resources that you might not care about in the context of Azure OpenAI cost management. When you scope at the subscription level, navigate to the full **Cost analysis tool** under the **Cost Management** service.

Here's an example of how to use the **Cost analysis tool** to see your accumulated costs for a subscription or resource group:

1. Search for *Cost Management* in the top Azure search bar to navigate to the full service experience, which includes more options such as creating budgets.
1. If necessary, select **change** if the **Scope:** isn't pointing to the resource group or subscription you want to analyze.
1. On the left, select **Reporting + analytics** > **Cost analysis**.
1. On the **All views** tab, select **Accumulated costs**.

:::image type="content" source="../openai/media/manage-costs/cost-analyzer.png" alt-text="Screenshot of cost analysis dashboard showing how to access accumulated costs." lightbox="../openai/media/manage-costs/cost-analyzer.png":::

The cost analysis dashboard shows the accumulated costs that are analyzed depending on what you specified for **Scope**.

:::image type="content" source="../openai/media/manage-costs/subscription.png" alt-text="Screenshot of cost analysis dashboard with scope set to subscription." lightbox="../openai/media/manage-costs/subscription.png":::

If you try to add a filter by service, you can't find Azure OpenAI in the list. This situation occurs because Azure OpenAI has commonality with a subset of Foundry Tools where the service level filter is **Cognitive Services**. If you want to see all Azure OpenAI resources across a subscription without any other type of Foundry Tool resources, instead scope to **Service tier: Azure OpenAI**:

:::image type="content" source="../openai/media/manage-costs/service-tier.png" alt-text="Screenshot of cost analysis dashboard with service tier highlighted." lightbox="../openai/media/manage-costs/service-tier.png":::

::: moniker range="foundry-classic"
### Monitor costs for models in Azure Marketplace

Azure Marketplace offers serverless API deployments. Model publishers might apply different costs depending on the offering. Each project in the Foundry portal has its own subscription with the offering, which you can use to monitor the costs and consumption happening on that project. Use [Microsoft Cost Management](https://azure.microsoft.com/products/cost-management) to monitor the costs:

1. Sign in to the [Azure portal](https://portal.azure.com/)

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


::: moniker-end

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

## Related content

:::moniker range="foundry-classic"
- [Foundry management center](management-center.md)
:::moniker-end
- [Foundry status dashboard](../foundry-status-dashboard-documentation.md)
- Learn [how to optimize your cloud investment with cost management](/azure/cost-management-billing/costs/cost-mgt-best-practices).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/understand/analyze-unexpected-charges).
- Take the [Cost Management](/training/paths/control-spending-manage-bills) guided learning course.