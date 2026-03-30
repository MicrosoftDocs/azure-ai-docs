---
title: "Plan and Manage Costs"
description: "Manage Microsoft Foundry costs by estimating expenses, monitoring usage, and setting up alerts for spending anomalies with Microsoft Cost Management."
#customer intent: As an IT admin or developer, I want to estimate and manage costs for Microsoft Foundry so that I can optimize my organization's budget and understand how billing works for different model types.
author: sdgilley
ms.author: sgilley
ms.reviewer: aashishb
ms.date: 03/23/2026
ms.topic: how-to
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
ms.service: azure-ai-foundry
---

# Plan and manage costs for Microsoft Foundry

[!INCLUDE [manage-costs 1](../includes/concepts-manage-costs-1.md)]

## Understand the billing model for Foundry Models

### Token-based pricing

Language and vision models process inputs by breaking them down into tokens. Text, image, and audio workloads can all use token-based metering. The billing unit and rate can vary by model, deployment type, and meter. Check the pricing page for the exact meter names and units for your deployment. For current rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/azure-openai/).

### Models sold directly by Azure

Models sold directly by Azure (including Azure OpenAI) are billed by Microsoft. In Cost Management, these charges typically appear as model-related meters associated with your deployed resources.

### Fine-tuned models

Azure OpenAI fine-tuned models are charged in three ways:

- **Training:** Charged per token or per hour, depending on the model.
- **Hosting:** Hourly cost per deployed model (applies even if the model is unused).
- **Inference:** Per 1,000 tokens (input and output) when the model is called.

Monitor hosted fine-tuned model costs closely to avoid unexpected charges. For current rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/azure-openai/).

> [!IMPORTANT]
> Fine-tuned deployments can incur hosting charges while deployed, even during low usage periods. Deployments inactive for more than 15 days might be automatically deleted. Remove or scale down deployments that you don't need, and verify current lifecycle behavior in the [fine-tuning documentation](../openai/how-to/fine-tuning.md) before relying on automatic cleanup behavior.

### HTTP Error response code and billing status

HTTP status codes alone don't determine whether usage is billed. Charges depend on whether billable processing occurred for the request and on the specific meter behavior.

Use Cost Management meter data and service metrics to reconcile billed usage, and treat your invoice and meter records as the source of truth.

## Monitor costs

Track your Foundry spending using cost analysis tools. You can view costs by day, month, or year, compare against budgets, and identify spending trends.

Access cost information from the [!INCLUDE [foundry-link](../includes/foundry-link.md)] portal or the [Azure portal](https://portal.azure.com/).
**Reference:** [Cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis)

> [!IMPORTANT]
> Your Foundry costs are only a subset of your overall application or solution costs. You need to monitor costs for all Azure resources used in your application or solution.

[!INCLUDE [manage-costs-permissions](../includes/concepts-manage-costs-permissions.md)]

## Monitor in Foundry portal

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Use the sections below to monitor costs.

> [!NOTE]
> Foundry portal labels and navigation can vary slightly by tenant and release wave. If you don't see an exact label in this article, use equivalent cost views in the same project scope.

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

**Reference:** [Agent concepts](../agents/concepts/development-lifecycle.md)

:::image type="content" source="media/manage-costs/agent-list.png" alt-text="Screenshot of the Agents tab showing a list of agents with columns for Name, Status, and Estimated costs. The Estimated costs column displays monthly values." lightbox="media/manage-costs/agent-list.png":::

To view detailed agent costs:

1. Select **Build** in the upper-right navigation.
1. Select **Agents** in the left pane.
1. Select an agent.
1. Select the **Monitor** tab.
1. Set the date range in the upper-right corner.
1. View token costs and usage metrics for the selected range.

**Reference:** [Monitor agent metrics](../observability/how-to/how-to-monitor-agents-dashboard.md)

:::image type="content" source="media/manage-costs/agent-build-cost.png" alt-text="Screenshot of the Build page showing the Models pane with a selected model highlighted." lightbox="media/manage-costs/agent-build-cost.png":::

### Model deployment costs

1. Select **Build** in the upper-right navigation.
1. Select **Models** in the left pane.
1. Select a model.
1. Select the **Monitor** tab.
1. Set the date range in the upper-right corner.
You see total cost and an estimated cost chart for the selected range.

**Reference:** [Monitor models](../foundry-models/how-to/monitor-models.md) 

:::image type="content" source="media/manage-costs/model-costs.png" alt-text="Screenshot of Azure portal showing the Monitor tab with total cost and estimated cost chart for a selected model and date range." lightbox="media/manage-costs/model-costs.png":::

When you select **View More Details** or **Azure Cost Management**, you're directed to the Azure portal's **Cost Management** section. Azure portal costs can show aggregated charges for the related account scope, not only individual models.

> [!NOTE]
> Token and request charts can temporarily differ from **Estimated cost** because of ingestion timing and aggregation differences. Use **Estimated cost** for near-real-time monitoring, and use Azure Cost Management and invoiced charges for financial reconciliation.

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

Models sold directly by Azure (including Azure OpenAI) are billed directly by Microsoft. When you inspect your bill, you typically see meters that account for model input and output usage.

:::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry resource is deployed, highlighting the meters for Azure OpenAI and Phi models. Cost is group by meter." lightbox="../foundry-models/media/manage-cost/cost-by-meter-1p.png":::

### Monitor costs by resource

You can get more detailed billing information by grouping costs by resource:

1. In **Cost Analysis**, select **View** > **Cost by resource**.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-resource.png" alt-text="Screenshot of how to see the cost by each resource in the resource group." lightbox="../foundry-models/media/manage-cost/cost-by-resource.png":::

1. Now you can see the resources generating each of the billing meters. To understand the breakdown of what makes up that cost, it can help to modify **Group by** to **Meter** and switching the chart type to **Line**.

1. Azure OpenAI models and Microsoft models are displayed as meters under each Foundry resource.

1. Some providers' models are displayed as meters under Global resources. The word *Global* **isn't** related to the SKU of the model deployment (for instance, *Global standard*). If you have multiple Foundry resources, your bill contains one entry **for each model for each Foundry resource**. The resource meters have the format *model-name-GUID* where the GUID is an identifier associated with a given Foundry resource. You notice billing meters accounting for inputs and outputs for each model you consumed.

   :::image type="content" source="../foundry-models/media/manage-cost/cost-by-resource-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by resource." lightbox="../foundry-models/media/manage-cost/cost-by-resource-saas.png":::

[!INCLUDE [manage-costs-scope](../includes/concepts-manage-costs-scope.md)]

[!INCLUDE [manage-costs 2](../includes/concepts-manage-costs-2.md)]

[!INCLUDE [manage-costs-troubleshoot](../includes/concepts-manage-costs-troubleshoot.md)]

## Related content

- [Microsoft Foundry pricing](https://azure.microsoft.com/pricing/details/microsoft-foundry/)
- [Foundry status dashboard](../foundry-status-dashboard-documentation.md)
- Learn [how to optimize your cloud investment with cost management](/azure/cost-management-billing/costs/cost-mgt-best-practices).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/understand/analyze-unexpected-charges).
- Take the [Cost Management](/training/paths/control-spending-manage-bills) guided learning course.
