---
title: Plan and manage costs for Microsoft Foundry hubs
titleSuffix: Microsoft Foundry
description: Learn how to plan for and manage costs for Microsoft Foundry hubs by using cost analysis in the Azure portal.
ms.author: mopeakande
manager: nitinme
author: msakande 
ms.reviewer: aashishb
reviewer: aashishb
ms.date: 09/26/2025
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - build-aifnd
  - build-2025
---

# Plan and manage costs for Microsoft Foundry hubs

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

This article describes how to plan for and manage costs for [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) hubs by using cost analysis in the Azure portal. First, use the Azure pricing calculator to help plan for Foundry costs before you add any resources. Next, as you add Azure resources, review the estimated costs. 

Foundry hub projects don't have a specific page in the Azure pricing calculator. Foundry hubs are composed of several other Azure services, some of which are optional. This article provides information on using the pricing calculator to estimate costs for these services. You use Foundry Tools in Foundry portal. Costs for Foundry Tools are only a portion of the monthly costs in your Azure bill. You're billed for all Azure services and resources used in your Azure subscription, including third-party services.

> [!NOTE]
> This article is specific to Foundry hub projects. For other costs associated with Foundry, refer to [Foundry cost management](../concepts/manage-costs.md).

## Prerequisites

Cost analysis in Microsoft Cost Management supports most Azure account types, but not all of them. To view the full list of supported account types, see [Understand Cost Management data](/azure/cost-management-billing/costs/understand-cost-mgt-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn). To view cost data, at a minimum, you need read access for an Azure account. For information about assigning access to Microsoft Cost Management data, see [Assign access to data](/azure/cost-management-billing/costs/assign-access-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

## Estimate costs before using Foundry Tools

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs before you add Foundry Tools.

1. Select a product such as Azure OpenAI in the Azure pricing calculator.

    :::image type="content" source="../media/cost-management/pricing-calculator-select-product.png" alt-text="Screenshot of selecting Azure OpenAI in the Azure pricing calculator." lightbox="../media/cost-management/pricing-calculator-select-product.png":::

1. Enter the number of units you plan to use. For example, enter the number of input tokens.

    :::image type="content" source="../media/cost-management/pricing-calculator-estimate-openai.png" alt-text="Screenshot of Azure OpenAI cost estimate in the Azure pricing calculator." lightbox="../media/cost-management/pricing-calculator-estimate-openai.png":::

1. Select more than one product to estimate costs for multiple products. For example, search for and select Virtual Machines to add potential costs for compute resources.

    :::image type="content" source="../media/cost-management/pricing-calculator-estimate.png" alt-text="Screenshot of total estimate in the Azure pricing calculator." lightbox="../media/cost-management/pricing-calculator-estimate.png":::

As you add new resources to your project, return to this calculator and add the same resource here to update your cost estimates.


### Costs that typically accrue with Foundry hubs

When you create resources for a hub, resources for other Azure services are also created. They are:

| Service pricing page | Description with example use cases | 
| --- | --- | 
| [Foundry Tools](https://azure.microsoft.com/pricing/details/cognitive-services/) | You pay to use services such as Azure OpenAI, Speech, Content Safety, Vision, Document Intelligence, and Language. Costs vary for each service and for some features within each service. For more information about provisioning of Foundry Tools, see [Foundry hubs](../concepts/ai-resources.md).| 
| [Azure AI Search](https://azure.microsoft.com/pricing/details/search/) | An example use case is to store data in a [vector search index](./index-add.md). |
| [Azure Machine Learning](https://azure.microsoft.com/pricing/details/machine-learning/) | You need compute instances to run [prompt flow](../concepts/prompt-flow.md) via Foundry.<br/><br/>When you create a compute instance, the virtual machine (VM) stays on so it's available for your work.<br/><br/>Enable idle shutdown to save on cost when the VM is idle for a specified time period.<br/><br/>Alternatively, set up a schedule to automatically start and stop the compute instance to save cost when you aren't planning to use it. | 
| [Azure Virtual Machine](https://azure.microsoft.com/pricing/details/virtual-machines/) | Azure Virtual Machines gives you the flexibility of virtualization for a wide range of computing solutions. It supports Linux, Windows Server, SQL Server, Oracle, IBM, SAP, and more. |
| [Azure Container Registry Basic account](https://azure.microsoft.com/pricing/details/container-registry) | Provides storage of private Docker container images, enabling fast, scalable retrieval, and network-close deployment of container workloads on Azure. |
| [Azure Blob Storage](https://azure.microsoft.com/pricing/details/storage/blobs/) | Can be used to store Foundry project files. |
| [Key Vault](https://azure.microsoft.com/pricing/details/key-vault/) | A key vault for storing secrets. |
| [Azure Private Link](https://azure.microsoft.com/pricing/details/private-link/) | Azure Private Link enables you to access Azure PaaS Services (for example, Azure Storage and SQL Database) over a private endpoint in your virtual network. |

### Costs might accrue before deleting a Foundry hub

Before you delete a hub in the Azure portal or with Azure CLI, the following sub resources are common costs that accumulate even when you aren't actively working in the workspace. If you plan to return to your hub at a later time, these resources might continue to accrue costs: 
- Azure AI Search (for the data)
- Virtual machines
- Load Balancer
- Azure Virtual Network
- Bandwidth

Each VM is billed per hour it's running. Cost depends on VM specifications. VMs that are running but not actively working on a dataset are still charged via the load balancer. For each compute instance, one load balancer is billed per day. Every 50 nodes of a compute cluster have one standard load balancer billed. To avoid load balancer costs on stopped compute instances and compute clusters, delete the compute resource.

Compute instances also incur P10 disk costs even in stopped state. This cost is because any user content saved to disk is persisted across the stopped state similar to Azure VMs. For Azure Virtual Networks, one virtual network is billed per subscription and per region. Virtual networks can't span regions or subscriptions. Setting up private endpoints in virtual network setups might also incur charges. If your virtual network uses an Azure Firewall, the firewall might also incur charges. Bandwidth usage is charged; the more data is transferred, the more you're charged. 

For more information, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

> [!TIP]
> Using a managed virtual network is free. However some features of the managed network rely on Azure Private Link (for private endpoints) and Azure Firewall (for fully qualified domain name (FQDN) rules) and incur charges. For more information, see [Managed virtual network isolation](configure-managed-network.md#pricing).

### Costs might accrue after deleting a Foundry hub

After you delete a hub in the Azure portal or with Azure CLI, the following resources continue to exist. They continue to accrue costs until you delete them.

- Azure Container Registry
- Azure Blob Storage
- Key Vault
- Application Insights (if you enabled it for your hub)

## Monitor costs

As you use Foundry, you incur costs. Azure resource usage unit costs vary by time intervals (seconds, minutes, hours, and days) or by unit usage (bytes, megabytes, and so on). You can see the incurred costs in [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

When you use cost analysis, you view costs in graphs and tables for different time intervals. Some examples are by day, current and prior month, and year. You also view costs against budgets and forecasted costs. Switching to longer views over time can help you identify spending trends so you can see where overspending might occur. If you create budgets, you can also easily see where they're exceeded.

### Monitor Foundry costs

You can access cost analysis from the [Azure portal](https://portal.azure.com).

> [!IMPORTANT]
> Your Foundry costs are only a subset of your overall application or solution costs. You need to monitor costs for all Azure resources used in your application or solution.

For the examples in this section, assume that all Foundry Services are in the same resource group. However, you can have resources in different resource groups. For example, your Azure AI Search resource might be in a different resource group than your project.

Here's an example of how to monitor costs for a project. The costs are used as an example only. Your costs vary depending on the services that you use and the amount of usage.

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

1. [!INCLUDE [classic-sign-in](../includes/classic-sign-in.md)]
1. Select your project, then select **Management center** from the left menu. 
1. Under the **Project** heading, select **Overview**. 
1. Select **View cost for resources** from the **Total cost** section. The [Azure portal](https://portal.azure.com) opens to the resource group for your project.

    :::image type="content" source="../media/cost-management/project-costs/project-settings-go-view-costs.png" alt-text="Screenshot of the Foundry portal showing how to see project settings." lightbox="../media/cost-management/project-costs/project-settings-go-view-costs.png":::

1. Expand the **Resource** column to see the costs for each service that's underlying your [project](../concepts/ai-resources.md). But this view doesn't include costs for all resources that you use in a project.

    :::image type="content" source="../media/cost-management/project-costs/costs-per-project-resource.png" alt-text="Screenshot of the Azure portal cost analysis with the project and associated resources." lightbox="../media/cost-management/project-costs/costs-per-project-resource.png":::

1. Select **Costs by resource** > **Resources** to open the Cost analysis page.

    :::image type="content" source="../media/cost-management/project-costs/select-costs-per-resource.png" alt-text="Screenshot of the Azure portal cost analysis with the button to select costs by resources." lightbox="../media/cost-management/project-costs/select-costs-per-resource.png":::

1. On the **Cost analysis** page, make sure the scope is set to your resource group. 

    :::image type="content" source="../media/cost-management/project-costs/costs-per-resource-group-details.png" alt-text="Screenshot of the Azure portal cost analysis for a resource group." lightbox="../media/cost-management/project-costs/costs-per-resource-group-details.png":::

    In this example:
    - The resource group name is **rg-contoso-ai**.
    - The total cost for all resources and services in the example resource group is **$174.71**. In this example, $174.71 is the total cost for your application or solution that you're building with Foundry. Again, this example assumes that all Foundry Services are in the same resource group. But you can have resources in different resource groups.
    - The project name is **contoso-proj**.
    - The costs that are limited to resources and services in the example [project](../concepts/ai-resources.md) total **$8.40**. 
    
1. Expand any of the resources listed to see the costs for their underlying services. You can also apply a filter to focus on other costs in your particular resource group. 

You can also view resource group costs directly from the Azure portal. To do so:
1. Sign in to [Azure portal](https://portal.azure.com).
1. Select **Resource groups**. 
1. Find and select the resource group that contains your Foundry Services.
1. From the left pane, select **Cost Management** > **Cost analysis**.

    :::image type="content" source="../media/cost-management/project-costs/costs-per-resource-group.png" alt-text="Screenshot of the Azure portal cost analysis at the resource group level." lightbox="../media/cost-management/project-costs/costs-per-resource-group.png":::

For more information, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

### Monitor costs for models offered through the Azure Marketplace

Azure Marketplace offers serverless API deployments. Model publishers might apply different costs depending on the offering. Each project in the Foundry portal has its own subscription with the offering, which you can use to monitor the costs and consumption happening on that project. Use [Microsoft Cost Management](https://azure.microsoft.com/products/cost-management) to monitor the costs:

1. Sign in to [Azure portal](https://portal.azure.com).

1. On the left pane, select **Cost Management + Billing** and then select **Cost Management**.

1. On the left pane, under the section for **Reporting + analytics**, select **Cost Analysis**.

1. Select a view such as **Resources**. The cost associated with each resource is displayed.

    :::image type="content" source="../media/cost-management/marketplace/costs-model-as-service-cost-analysis.png" alt-text="A screenshot of the Cost Analysis tool displaying how to show cost per resource." lightbox="../media/cost-management/marketplace/costs-model-as-service-cost-analysis.png":::

1. On the **Type** column, select the filter icon to filter all the resources of type **microsoft.saas/resources**. This type corresponds to resources created from offers available in Azure Marketplace. For convenience, you can filter by resource types containing the string **SaaS**. 

    :::image type="content" source="../media/cost-management/marketplace/costs-model-as-service-cost-filter.png" alt-text="A screenshot of how to filter by resource type containing the string 'SaaS'." lightbox="../media/cost-management/marketplace/costs-model-as-service-cost-filter.png":::

1. One resource is displayed for each model offer per project. Naming of those resources is `[Model offer name]-[GUID]`.

1. Select to expand the resource details to get access to each of the costs meters associated with the resource. 

    - **Tier** represents the offering.
    - **Product** is the specific product inside the offering. 
    
    Some model providers might use the same name for both.

    :::image type="content" source="../media/cost-management/marketplace/costs-model-as-service-cost-details.png" alt-text="A screenshot showing different resources corresponding to different model offers and their associated meters." lightbox="../media/cost-management/marketplace/costs-model-as-service-cost-details.png":::

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


## Understand the full billing model for Foundry Tools

Foundry Tools run on Azure infrastructure that accrues costs along with Azure AI when you deploy the new resource. It's important to understand that extra infrastructure might accrue cost. You need to manage that cost when you make changes to deployed resources.

When you create or use Foundry Tools resources, you might get charged based on the services that you use. Two billing models are available for Foundry Tools: 

- Serverless API: With serverless API pricing, you're billed according to the Foundry Tools offering that you use, based on its billing information.
- Commitment tiers: With commitment tier pricing, you commit to using several service features for a fixed fee, enabling you to have a predictable total cost based on the needs of your workload. You're billed according to the plan you choose. For information on available services, how to sign up, and considerations when purchasing a plan, see [Quickstart: purchase commitment tier pricing](../../ai-services/commitment-tier.md).

> [!NOTE]
> If you use the resource above the quota provided by the commitment plan, you pay for the extra usage as described in the overage amount in the Azure portal when you purchase a commitment plan. 

You can pay for Foundry Tools charges with your Azure Prepayment (previously called monetary commitment) credit. However, you can't use Azure Prepayment credit to pay for charges for third-party products and services, including ones from Azure Marketplace.

For more information, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

## Next steps

- Learn [how to optimize your cloud investment with Microsoft Cost Management](/azure/cost-management-billing/costs/cost-mgt-best-practices?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Learn about how to [prevent unexpected costs](/azure/cost-management-billing/cost-management-billing-overview?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
- Take the [Cost Management](/training/paths/control-spending-manage-bills?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) guided learning course.
