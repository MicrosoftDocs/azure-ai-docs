---
title: Manage and increase quotas for resources
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to manage and increase quotas for resources with Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 02/19/2025
ms.reviewer: siarora
ms.author: larryfr
author: Blackmist
zone_pivot_groups: project-type
# Customer intent: As an Azure AI Foundry user, I want to know how to manage and increase quotas for resources with Azure AI Foundry.
---

# Manage and increase quotas for resources with Azure AI Foundry

::: zone pivot="hub-project"

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing quota for your Azure AI Foundry virtual machines and Azure OpenAI in Foundry models.

Azure uses limits and quotas to prevent budget overruns due to fraud, and to honor Azure capacity constraints. It's also a good way to control costs for admins. Consider these limits as you scale for production workloads. 

In this article, you learn about: 

- Default limits on Azure resources  
- Creating Azure AI Foundry hub-level quotas. 
- Viewing your quotas and limits 
- Requesting quota and limit increases 

::: zone-end

::: zone pivot="fdp-project"

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing quota for your Azure OpenAI in Foundry models.

Azure uses limits and quotas to prevent budget overruns due to fraud, and to honor Azure capacity constraints. It's also a good way to control costs for admins. Consider these limits as you scale for production workloads. 

In this article, you learn about: 

- Viewing your quotas and limits 
- Requesting quota and limit increases 

::: zone-end

::: zone pivot="hub-project"

## Special considerations 

Quotas are applied to each subscription in your account. If you have multiple subscriptions, you must request a quota increase for each subscription. 

A quota is a credit limit on Azure resources, not a capacity guarantee. If you have large-scale capacity needs, contact Azure support to increase your quota. 

> [!NOTE]
> Azure AI Foundry compute has a separate quota from the core compute quota. 

Default limits vary by offer category type, such as free trial, pay-as-you-go, and virtual machine (VM) series (such as Dv2, F, and G). 

## Azure AI Foundry quota 

The following actions in [Azure AI Foundry portal](https://ai.azure.com) consume quota: 

- Creating a compute instance.
- Building a vector index.
- Deploying open models from model catalog.

## Azure AI Foundry compute 

[Azure AI Foundry compute](./create-manage-compute.md) has a default quota limit on both the number of cores and the number of unique compute resources that are allowed per region in a subscription. 

- The quota on the number of cores is split by each VM Family and cumulative total cores.
- The quota on the number of unique compute resources per region is separate from the VM core quota, as it applies only to the managed compute resources  

To raise the limits for compute, you can [request a quota increase](#view-and-request-quotas-in-azure-ai-foundry-portal) in the [Azure AI Foundry](https://ai.azure.com).

Available resources include:
- Dedicated cores per region have a default limit of 24 to 300, depending on your subscription offer type. You can increase the number of dedicated cores per subscription for each VM family. Specialized VM families like NCv2, NCv3, or ND series start with a default of zero cores. GPUs also default to zero cores. 
- Total compute limit per region has a default limit of 500 per region within a given subscription and can be increased up to a maximum value of 2500 per region. This limit is shared between compute instances, and managed online endpoint deployments. A compute instance is considered a single-node cluster for quota purposes. In order to increase the total compute limit, [open an online customer support request](https://portal.azure.com/#view/Microsoft_Azure_Support/NewSupportRequestV3Blade/callerWorkflowId/5088c408-f627-4398-9aa3-c41cdd93a6eb/callerName/Microsoft_Azure_Support%2FHelpAndSupportOverview.ReactView). 

When opening the support request to increase the total compute limit, provide the following information:
1. Select **Technical** for the issue type. 
1. Select the subscription that you want to increase the quota for. 
1. Select **Machine Learning** as the service type. 
1. Select the resource that you want to increase the quota for.
1. In the **Summary** field, enter "Increase total compute limits" 
1. Select **Compute instance** the problem type and **Quota** as the problem subtype.

    :::image type="content" source="../media/cost-management/quota-azure-portal-support.png" alt-text="Screenshot of the page to submit compute quota requests in Azure portal." lightbox="../media/cost-management/quota-azure-portal-support.png":::

1. Select **Next**.
1. On the **Additional details** page, provide the subscription ID, region, new limit (between 500 and 2500), and business justification to increase the total compute limits for the region. 
1. Select **Create** to submit the support request ticket. 

::: zone-end

## Azure AI Foundry shared quota 

Azure AI Foundry provides a pool of shared quota that is available for different users across various regions to use concurrently. Depending upon availability, users can temporarily access quota from the shared pool, and use the quota to perform testing for a limited amount of time. The specific time duration depends on the use case. By temporarily using quota from the quota pool, you no longer need to file a support ticket for a short-term quota increase or wait for your quota request to be approved before you can proceed with your workload. 

Use of the shared quota pool is available for testing inferencing for Llama-2, Phi, Nemotron, Mistral, Dolly, and Deci-DeciLM models from the Model Catalog. You should use the shared quota only for creating temporary test endpoints, not production endpoints. For endpoints in production, you should [request dedicated quota](#view-and-request-quotas-in-azure-ai-foundry-portal). Billing for shared quota is usage-based. 

::: zone pivot="hub-project"

## Container Instances 

For more information, see [Container Instances limits](/azure/azure-resource-manager/management/azure-subscription-service-limits#container-instances-limits). 

## Storage

Azure Storage has a limit of 250 storage accounts per region, per subscription. This limit includes both Standard and Premium storage accounts.  

::: zone-end

## View and request quotas in Azure AI Foundry portal

::: zone pivot="hub-project"

Use quotas to manage compute target allocation and model quota between multiple [!INCLUDE [hub](../includes/hub-project-name.md)]s in the same subscription. 

By default, all hubs share the same quota as the subscription-level quota for VM families. However, you can set a maximum quota for individual VM families for more granular cost control and governance on hubs in a subscription. Quotas for individual VM families let you share capacity and avoid resource contention issues.

::: zone-end
::: zone pivot="fdp-project"

Use quotas to manage model quota allocation between multiple [!INCLUDE [fdp](../includes/fdp-project-name.md)]s in the same subscription

::: zone-end

::: zone pivot="hub-project"

1. In Azure AI Foundry portal, select **Management center** from the bottom of the left menu.

    :::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the management center link.":::

1. Select **Quota** from the left menu.

    :::image type="content" source="../media/cost-management/quotas.png" alt-text="Screenshot of the Model and VM quota entries in the management section." lightbox="../media/cost-management/quotas.png":::

1. From the quota view, you can see the quota for the models in the selected Azure region. To request more quota, select the model and then select **Request quota**. 

    - Use the **Show all quota** toggle to display all quota or only the currently allocated quota.
    - Use the **Group by** dropdown to group the list by **Quota type, Region & Model**, **Quota type, Model & Region**, or **None**. The **None** grouping displays a list of model deployments.
    - Expand the groupings to view information on specific model deployments. While viewing a model deployment, select the **pencil icon** in the **Quota allocation** column to edit the quota allocation for the model deployment.
    - Use the **charts** along the side of the page to view more details about quota usage. The charts are interactive; hovering over a section of the chart displays more information, and selecting the chart filters the list of models. Selecting the chart legend filters the data displayed in the chart.
    - Use the **Azure OpenAI Provisioned** link to view information about provisioned models, including a **Capacity calculator**.
  
    :::image type="content" source="../media/cost-management/model-quota.png" alt-text="Screenshot of the Model quota page in Azure AI Foundry portal." lightbox="../media/cost-management/model-quota.png":::

1. When you select the **VM quota** link, you can view the quota and usage for the virtual machine families in the selected Azure region. To request more quota, select the VM family and then select **Request quota**.

    > [!TIP]
    > If you don't see the **VM quota** link, you were viewing a [!INCLUDE [fdp](../includes/fdp-project-name.md)] project when you selected **Management center**. Use the **All resources** link and then select a project where the **Type** contains **Parent resource : name (Hub)**, and then select **Quota** from the left menu.

    :::image type="content" source="../media/cost-management/vm-quota.png" alt-text="Screenshot of the VM quota page in Azure AI Foundry portal." lightbox="../media/cost-management/vm-quota.png":::

::: zone-end

::: zone pivot="fdp-project"

1. In Azure AI Foundry portal, select **Management center** from the bottom of the left menu.

    :::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the management center link.":::

1. Select **Quota** from the left menu.

    :::image type="content" source="../media/cost-management/quotas.png" alt-text="Screenshot of the Model and VM quota entries in the management section." lightbox="../media/cost-management/quotas.png":::

1. From the quota view, you can see the quota for the models in the selected Azure region. To request more quota, select the model and then select **Request quota**.

    :::image type="content" source="../media/cost-management/project-model-quota.png" alt-text="Screenshot of the Model quota page for a Foundry project in Azure AI Foundry portal." lightbox="../media/cost-management/project-model-quota.png":::

    - Use the **Show all quota** toggle to display all quota or only the currently allocated quota.
    - Use the **Group by** dropdown to group the list by **Quota type, Region & Model**, **Quota type, Model & Region**, or **None**. The **None** grouping displays a list of model deployments.
    - Expand the groupings to view information on specific model deployments. While viewing a model deployment, select the **pencil icon** in the **Quota allocation** column to edit the quota allocation for the model deployment.
    - Use the **charts** along the side of the page to view more details about quota usage. The charts are interactive; hovering over a section of the chart displays more information, and selecting the chart filters the list of models. Selecting the chart legend filters the data displayed in the chart.
    - Use the **Azure OpenAI Provisioned** link to view information about provisioned models, including a **Capacity calculator**.

::: zone-end

## Next steps 

- [Plan to manage costs](./costs-plan-manage.md)
- [How to create compute](./create-manage-compute.md)
