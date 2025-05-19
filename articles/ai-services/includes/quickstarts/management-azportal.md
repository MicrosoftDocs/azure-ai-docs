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

## Create a new Azure AI Foundry resource

AI Foundry portal provides a way to create a new Azure resource with basic,  defaulted, settings. If your organization requires customized Azure configurations like alternative names, security controls or cost tags, you may have to use Azure portal or [template options](../../../ai-foundry/how-to/create-resource-template.md) to comply with your organization's Azure Policy compliance.

The Azure AI Foundry multi-service resource is listed under **AI Foundry** > **AI Foundry** in the portal. The API kind is **AIServices**. Look for the logo as shown here:

:::image type="content" source="../../media/ai-services-resource-portal.png" alt-text="Screenshot of the Azure AI Foundry resource in the Azure portal." lightbox="../../media/ai-services-resource-portal.png":::

> [!IMPORTANT]
> Azure provides more than one resource kinds named Azure AI services. Be sure to select the one that is listed under **AI Foundry** > **AI Foundry** with the logo as shown previously.

To create an AI Foundry resource follow these instructions:

> [!TIP]
> If you need to create an [!INCLUDE [fdp](../../../ai-foundry/includes/fdp-project-name.md)] or [!INCLUDE [hub](../../../ai-foundry/includes/hub-project-name.md)] resource, you can also use the [Azure Foundry portal](https://ai.azure.com) to create the resource. For more information, see the following articles:
>
> - [Create an Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry&pivots=fdp-project).
> - [Create an Azure AI hub based project](/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry&pivots=hub-project).

1. Select this link to create an **AI Foundry** resource: [https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices)

1. On the **Create** page, provide the following information:

    |Project details| Description   |
    |--|--|
    | **Subscription** | Select one of your available Azure subscriptions. |
    | **Resource group** | The Azure resource group that will contain your Azure AI Foundry resource. You can create a new group or add it to a preexisting group. |
    | **Region** | The location of your Azure AI service instance. Different locations may introduce latency, but have no impact on the runtime availability of your resource. |
    | **Name** | A descriptive name for your Azure AI Foundry resource. For example, *MyAIServicesResource*. |

1. Configure other settings for your resource as needed, read and accept the conditions (as applicable), and then select **Review + create**.

> [!TIP]
> If your subscription doesn't allow you to create an AI Foundry resource, you might need to enable the privilege of that [Azure resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) using the [Azure portal](/azure/azure-resource-manager/management/resource-providers-and-types#azure-portal), [PowerShell command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-powershell) or an [Azure CLI command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-cli). If you are not the subscription owner, ask someone with the role of *Owner* or *Admin* to complete the registration for you or ask for the **/register/action** privileges to be granted to your account.

## Clean up resources

If you want to clean up and remove an AI Foundry resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources contained in the group.

1. In the Azure portal, expand the menu on the left side to open the menu of services, and choose **Resource Groups** to display the list of your resource groups.
1. Locate the resource group containing the resource to be deleted.
1. If you want to delete the entire resource group, select the resource group name. On the next page, Select **Delete resource group**, and confirm.
1. If you want to delete only the Azure AI Foundry resource, select the resource group to see all the resources within it. On the next page, select the resource that you want to delete, select the ellipsis menu for that row, and select **Delete**.
