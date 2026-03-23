---
title: "Plan and Manage Costs (classic)"
description: "Manage Microsoft Foundry costs by estimating expenses, monitoring usage, and setting up alerts for spending anomalies with Microsoft Cost Management. (classic)"
#customer intent: As an IT admin or developer, I want to estimate and manage costs for Microsoft Foundry so that I can optimize my organization's budget and understand how billing works for different model types.
author: sdgilley
ms.author: sgilley
ms.reviewer: aashishb
ms.date: 03/23/2026
ms.topic: how-to
ms.custom:
  - dev-focus
  - classic-and-new
ai-usage: ai-assisted
ms.service: azure-ai-foundry
ROBOTS: NOINDEX, NOFOLLOW
---

# Plan and manage costs for Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/manage-costs.md)

[!INCLUDE [manage-costs 1](../../foundry/includes/concepts-manage-costs-1.md)]

## Understand the billing model for Foundry Models

### Token-based pricing

Language and vision models process inputs by breaking them down into tokens. Text, image, and audio workloads can all use token-based metering. The billing unit and rate can vary by model, deployment type, and meter. Check the pricing page for the exact meter names and units for your deployment. For current rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

### Models sold directly by Azure

Models sold directly by Azure (including Azure OpenAI) are billed by Microsoft. In Cost Management, these charges typically appear as model-related meters associated with your deployed resources.

### Models from partners and community

Third-party provider models (such as Cohere) are billed via Azure Marketplace. These entries appear at the resource group level (not the Foundry resource level) under **Marketplace** > **Service Name** *SaaS*, with separate meters for inputs and outputs.

> [!IMPORTANT]
> Billing scope and meter placement differ between Microsoft-sold models and partner/community offers. Validate the exact meter names and charge location in your subscription before you finalize budgets.

### Fine-tuned models

Azure OpenAI fine-tuned models are charged in three ways:

- **Training:** Charged per token in your training file.
- **Hosting:** Hourly cost per deployed model (applies even if the model is unused).
- **Inference:** Per 1,000 tokens (input and output) when the model is called.

Monitor hosted fine-tuned model costs closely to avoid unexpected charges. For current rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

> [!IMPORTANT]
> Fine-tuned deployments can incur hosting charges while deployed, even during low usage periods. Remove or scale down deployments that you don't need, and verify current lifecycle behavior in the Azure OpenAI documentation before relying on automatic cleanup behavior.

### HTTP Error response code and billing status

HTTP status codes alone don't determine whether usage is billed. Charges depend on whether billable processing occurred for the request and on the specific meter behavior.

Use Cost Management meter data and service metrics to reconcile billed usage, and treat your invoice and meter records as the source of truth.

## Monitor costs

Track your Foundry spending using cost analysis tools. You can view costs by day, month, or year, compare against budgets, and identify spending trends.

Access cost information from the [!INCLUDE [classic-link](../../foundry/includes/classic-link.md)] portal or the [Azure portal](https://portal.azure.com/).
**Reference:** [Cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis)

> [!IMPORTANT]
> Your Foundry costs are only a subset of your overall application or solution costs. You need to monitor costs for all Azure resources used in your application or solution.

### Configure permissions to view costs

To view Foundry costs, assign roles based on the task and scope. For cost reporting, assign the [Cost Management Reader role](/azure/role-based-access-control/built-in-roles/management-and-governance#cost-management-reader) at the required scope. Assign the [AI User role](rbac-foundry.md#built-in-roles) when users also need to inspect Foundry resources and usage context.

If built-in roles don't meet your needs, you can create a custom role with least-privilege permissions. Validate role actions in your environment because available actions can evolve over time.

Example read permissions:

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

To create a custom role, construct a role definition JSON file that specifies permissions and scope for the role. The following example is an illustrative starting point for a custom Foundry Cost Reader role:

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

> [!NOTE]
> Validate custom role definitions in a nonproduction environment before broad rollout, and verify each action against your tenant's supported resource provider operations.

> [!NOTE]
> This custom role example doesn't grant access to Foundry resources by itself. Assign an additional role such as [AI User](rbac-foundry.md#built-in-roles) if users also need Foundry resource visibility.

## Monitor in Azure portal

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. View costs for your resource group or individual Foundry resource.

    [!INCLUDE [find-region](../includes/find-region.md)]

1. In the Azure portal, select **Cost analysis** under **Cost Management** (for your resource group or Foundry resource).

1. View the cost overview. Optionally, add filters (deployment tags, user-defined tags) to segment costs by model deployment:

   :::image type="content" source="../../foundry/media/manage-costs/cost-overview-deployment-tags.png" alt-text="Screenshot of cost overview showing deployment-level tags filter." lightbox="../../foundry/media/manage-costs/cost-overview-deployment-tags.png":::

1. Select **Costs by resource** > **Resources** to see your Foundry resource cost split across model deployments:

   :::image type="content" source="../../foundry/media/manage-costs/azure-foundry-cost-split.png" alt-text="Screenshot of split of Foundry resource cost across model deployments." lightbox="../../foundry/media/manage-costs/azure-foundry-cost-split.png":::

### Understand cost breakdown by meter

Use the **Cost Analysis** tool to view costs grouped by billing meter:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your resource group.
1. Select **Cost analysis** under **Cost Management**.

1. By default, cost analysis is scoped to the selected resource group.

   > [!IMPORTANT]
   > Scope *Cost Analysis* to the resource group where you deployed the Foundry resource. The cost meters associated with Models from Partners and Community display under the resource group instead of the Foundry resource.

1. Modify **Group by** to **Meter**. You can now see that for this particular resource group, the source of the costs comes from different model series.

## Troubleshoot common cost analysis issues

- **Costs don't match your estimate:** Confirm that all dependent resources (for example, storage, networking, and Marketplace resources) are included in your Cost Management scope.
- **Can't see cost data:** Confirm you have both cost visibility permissions and Foundry access permissions at the correct scope.
- **Unexpected meter charges:** Group by **Meter** and **Resource** to identify which service generated the charge, then compare with deployment and traffic patterns.
- **Region rollout cost variance:** Validate region/model availability before deployment and recheck assumptions if you deploy in different regions.
- **Tag filters return incomplete results:** Verify required tags are applied to all participating resources and inherited consistently from your deployment process.
- **Budget alerts are noisy or delayed:** Recalibrate alert thresholds after observing normal usage for a full trend window, then separate warning and critical thresholds.
- **Policy or scope drift changes cost visibility:** Confirm your selected scope and policy assignments still include all resources used by the workload.
- **Data appears delayed after test runs:** Wait for ingestion latency, then recheck the same time window before concluding there is a billing discrepancy.

   :::image type="content" source="../../foundry/foundry-models/media/manage-cost/cost-by-meter.png" alt-text="Screenshot of how to see the cost by each meter in the resource group." lightbox="../../foundry/foundry-models/media/manage-cost/cost-by-meter.png":::

#### Models sold directly by Azure

Models sold directly by Azure (including Azure OpenAI) are billed directly by Microsoft. When you inspect your bill, you typically see meters that account for model input and output usage.

:::image type="content" source="../../foundry/foundry-models/media/manage-cost/cost-by-meter-1p.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry resource is deployed, highlighting the meters for Azure OpenAI and Phi models. Cost is group by meter." lightbox="../../foundry/foundry-models/media/manage-cost/cost-by-meter-1p.png":::

#### Models from partners and community

Models provided by third-party providers, like Cohere, are billed using Azure Marketplace. As opposite to Microsoft billing meters, those entries are associated with the resource group where your Foundry is deployed instead of to the Foundry resource itself. Given model providers charge you directly, you see entries under the category **Marketplace** and **Service Name** *SaaS* accounting for inputs and outputs for each consumed model.

:::image type="content" source="../foundry-models/media/manage-cost/cost-by-meter-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by meter." lightbox="../foundry-models/media/manage-cost/cost-by-meter-saas.png":::

> [!IMPORTANT]
> This distinction affects how offers are represented and billed in Cost Management. Verify offer details, compliance requirements, and billing meters for each model provider in your environment.
### Monitor costs by resource

You can get more detailed billing information by grouping costs by resource:

1. In **Cost Analysis**, select **View** > **Cost by resource**.

   :::image type="content" source="../../foundry/foundry-models/media/manage-cost/cost-by-resource.png" alt-text="Screenshot of how to see the cost by each resource in the resource group." lightbox="../../foundry/foundry-models/media/manage-cost/cost-by-resource.png":::

1. Now you can see the resources generating each of the billing meters. To understand the breakdown of what makes up that cost, it can help to modify **Group by** to **Meter** and switching the chart type to **Line**.

1. Azure OpenAI models and Microsoft models are displayed as meters under each Foundry resource.

1. Some providers' models are displayed as meters under Global resources. The word *Global* **isn't** related to the SKU of the model deployment (for instance, *Global standard*). If you have multiple Foundry resources, your bill contains one entry **for each model for each Foundry resource**. The resource meters have the format *model-name-GUID* where the GUID is an identifier associated with a given Foundry resource. You notice billing meters accounting for inputs and outputs for each model you consumed.

   :::image type="content" source="../../foundry/foundry-models/media/manage-cost/cost-by-resource-saas.png" alt-text="Screenshot of cost analysis dashboard scoped to the resource group where the Foundry Tools resource is deployed, highlighting the meters for models billed throughout Azure Marketplace. Cost is group by resource." lightbox="../../foundry/foundry-models/media/manage-cost/cost-by-resource-saas.png":::

It's important to understand scope when you evaluate costs associated with Foundry resources. If your resources are part of the same resource group, you can scope Cost Analysis at that level to understand the effect on costs. If your resources are spread across multiple resource groups, you can scope to the subscription level.

When scoped at a higher level, you often need to add more filters to focus on Azure OpenAI usage. When scoped at the subscription level, you see many other resources that you might not care about in the context of Azure OpenAI cost management. When you scope at the subscription level, navigate to the full **Cost analysis tool** under the **Cost Management** service.

Here's an example of how to use the **Cost analysis tool** to see your accumulated costs for a subscription or resource group:

1. Search for *Cost Management* in the top Azure search bar to navigate to the full service experience, which includes more options such as creating budgets.
1. If necessary, select **change** if the **Scope:** isn't pointing to the resource group or subscription you want to analyze.
1. On the left, select **Reporting + analytics** > **Cost analysis**.
1. On the **All views** tab, select **Accumulated costs**.

:::image type="content" source="../../foundry/openai/media/manage-costs/cost-analyzer.png" alt-text="Screenshot of cost analysis dashboard showing how to access accumulated costs." lightbox="../../foundry/openai/media/manage-costs/cost-analyzer.png":::

The cost analysis dashboard shows the accumulated costs that are analyzed depending on what you specified for **Scope**.

:::image type="content" source="../../foundry/openai/media/manage-costs/subscription.png" alt-text="Screenshot of cost analysis dashboard with scope set to subscription." lightbox="../../foundry/openai/media/manage-costs/subscription.png":::

If you try to add a filter by service, you can't find Azure OpenAI in the list. This situation occurs because Azure OpenAI usage appears under the broader **Cognitive Services** service classification in Cost Management. If you want to focus on Azure OpenAI usage across a subscription, use **Service tier: Azure OpenAI**:

:::image type="content" source="../../foundry/openai/media/manage-costs/service-tier.png" alt-text="Screenshot of cost analysis dashboard with service tier highlighted." lightbox="../../foundry/openai/media/manage-costs/service-tier.png":::

### Monitor costs for models in Azure Marketplace

Azure Marketplace offers serverless API deployments. Model publishers might apply different costs depending on the offering. Costs are tied to the subscription and resources where the offer is deployed. Use [Microsoft Cost Management](https://azure.microsoft.com/products/cost-management) to monitor these charges:

1. Sign in to the [Azure portal](https://portal.azure.com/)

1. On the left pane, select **Cost Management + Billing** and then select **Cost Management**.

1. On the left pane, under the section for **Reporting + analytics**, select **Cost Analysis**.

1. Select a view such as **Resources**. The cost associated with each resource is displayed.

   :::image type="content" source="../media/manage-costs/cost-analysis-resource-filter.png" alt-text="Screenshot of the Cost Analysis tool displaying how to show cost per resource." lightbox="../media/manage-costs/cost-analysis-resource-filter.png":::

1. On the **Type** column, select the filter icon to filter all the resources of type **microsoft.saas/resources**. This type corresponds to resources created from offers available in Azure Marketplace. For convenience, you can filter by resource types containing the string **SaaS**.

   :::image type="content" source="../media/manage-costs/filter-resource-type-saas.png" alt-text="Screenshot of how to filter by resource type containing the string SaaS." lightbox="../media/manage-costs/filter-resource-type-saas.png":::

1. One resource is displayed for each model offer per project. Naming of those resources is *model-offer-name-GUID*.

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

[!INCLUDE [manage-costs 2](../../foundry/includes/concepts-manage-costs-2.md)]

## Related content

- [Foundry management center](management-center.md)- [Foundry status dashboard](../foundry-status-dashboard-documentation.md)
- Learn [how to optimize your cloud investment with cost management](/azure/cost-management-billing/costs/cost-mgt-best-practices).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/understand/analyze-unexpected-charges).
- Take the [Cost Management](/training/paths/control-spending-manage-bills) guided learning course.
