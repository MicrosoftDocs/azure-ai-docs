---
title: "Quickstart: Create an AI Foundry resource in the Azure portal"
titleSuffix: Azure AI services
description: Get started with Azure AI services by creating an AI Foundry resource in the Azure portal.
manager: nitinme
keywords: Azure AI services, cognitive intelligence, cognitive solutions, ai services
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
ms.topic: quickstart
ms.date: 8/1/2024
ms.author: eur
author: eric-urban
---

## Prerequisites

* A valid Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/).

## Create a first resource

AI Foundry portal provides a way to create a new Azure resource with basic,  defaulted, settings. If your organization requires customized Azure configurations like alternative names, security controls or cost tags, you may have to use Azure Portal or [template options](../../ai-foundry/how-to/create-resource-template.md) to comply with your organization's Azure Policy compliance.

# [Azure AI Foundry portal](#tab/ai-foundry)

* Access [AI Foundry Portal](https://ai.azure.com) to get started and sign in using your organization account.

  Do you see existing projects or Foundry resources listed? Then, you may not have to create a new resource. You may pick an existing project, or create a new project under an existing resource your IT admin may have pre-configured.

* If you are sure you want to create a new resource, there are multiple entry points to create new resources:
  
  1. Home page
  1. All resources 
  1. Management center -> All resources

  Click 'create new' or 'create project' to get started. If this is the first project you create, we automatically create a parent Azure resource for you.

# [Azure Portal](#tab/azure-portal)

* In Azure Portal or Azure marketplace, search for 'AI Foundry'.

  The Azure AI Foundry resource is listed under **AI Foundry** > **AI Foundry** in the portal. The API kind is **AIServices**. Look for the logo as shown here:

   :::image type="content" source="../../media/ai-services-resource-portal.png" alt-text="Screenshot of the Azure AI Foundry resource in the Azure portal." lightbox="../../media/ai-services-resource-portal.png":::

   > [!IMPORTANT]
   > Azure provides more than one resource kinds named Azure AI services. Be sure to select the one that is listed under **AI Foundry** > **AI Foundry** with the logo as shown previously.

* Click `create new` or follow this link to create an **AI Foundry** resource: [https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices)

1. On the **Create** page, provide the following information:

    |Project details| Description   |
    |--|--|
    | **Subscription** | Select one of your available Azure subscriptions. |
    | **Resource group** | The Azure resource group that will contain your Azure AI Foundry resource. You can create a new group or add it to a pre-existing group. |
    | **Region** | The location of your Azure AI service instance. Different locations may introduce latency, but have no impact on the runtime availability of your resource. |
    | **Name** | A descriptive name for your Azure AI Foundry resource. For example, *MyAIServicesResource*. |
    | **First project name** | The name for your first 'default' project. Projects are folders to organize your work. The default project has backwards compatibility with developer APIs that previously lived on a resource level for selected AI Services. |

1. Configure other settings for your resource as needed, read and accept the conditions (as applicable), and then select **Review + create**.

---

## Common issues

* If your subscription doesn't allow you to create an AI Foundry resource, you might need to enable the privilege of that [Azure resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) using the [Azure portal](/azure/azure-resource-manager/management/resource-providers-and-types#azure-portal), [PowerShell command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-powershell) or an [Azure CLI command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-cli). If you are not the subscription owner, ask someone with the role of *Owner* or *Admin* to complete the registration for you or ask for the **/register/action** privileges to be granted to your account.

* If you are unable to create resources due to Azure RBAC permissions, you may need to ask someone with the *Owner*, *Contributor* or *Azure AI Administrator* role to create it for you. Alternative, use an existing resource your admin may have pre-configured for you to create a new project. Creating projects requires less Azure permissions.

* Quota limit exceeded. See [resource limits](../../../ai-foundry/model-inference/quotas-limits.md) for possible causes including the maximum number of instances per subscription and region. 

## Clean up resources

If you want to clean up and remove an AI Foundry resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources contained in the group.

1. In the Azure portal, expand the menu on the left side to open the menu of services, and choose **Resource Groups** to display the list of your resource groups.
1. Locate the resource group containing the resource to be deleted.
1. If you want to delete the entire resource group, select the resource group name. On the next page, Select **Delete resource group**, and confirm.
1. If you want to delete only the Azure AI Foundry resource, select the resource group to see all the resources within it. On the next page, select the resource that you want to delete, select the ellipsis menu for that row, and select **Delete**.
