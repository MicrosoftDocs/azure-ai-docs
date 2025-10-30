---
title: Use Azure AI Foundry with Azure AI Search skills
titleSuffix: Azure AI services
description: Learn how to create a multi-service resource to use Azure AI Search skills with an Azure AI Foundry resource.
author: jonburchel
ms.author: jburchel
ms.date: 10/20/2025
ms.service: azure-ai-services
ms.topic: quickstart
---

# Use Azure AI Foundry with Azure AI Search skills

In this Quickstart, you learn how to create a classic Azure AI services multi-service account that supports [skillset processing](/azure/search/cognitive-search-concept-intro) in Azure AI Search. 

[Azure AI Search skills](../search/tutorial-skillset.md) don't natively support the AI Foundry resource. You need to create a classic _multi-service_ resource, instead, to use Azure AI Search skills with Azure AI Foundry and any other workflow that includes built-in skills.

## Create a multi-service resource

The multi-service resource that you can use with Azure AI Search skills is listed under **AI Foundry** > **Classic AI services** > **Azure AI services multi-service account (classic)** in the portal. Look for the logo as shown here:

:::image type="content" source="./media/cognitive-services-resource-portal.png" alt-text="Screenshot of the Azure AI services multi-service account in the Azure portal." lightbox="./media/cognitive-services-resource-portal.png":::

To create a multi-service resource for Azure AI Search skills follow these instructions:

1. Select this link to create an **Azure AI services multi-service account (classic)** resource: [https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne)

1. On the **Create** page, provide the following information:

    |Project details| Description   |
    |--|--|
    | **Subscription** | Select one of your available Azure subscriptions. |
    | **Resource group** | The Azure resource group that contains your Azure AI services multi-service account resource. You can create a new group or add it to a preexisting group. |
    | **Region** | The location of your Azure AI services multi-service account instance. Different locations might introduce latency, but have no impact on the runtime availability of your resource. Check the [Azure AI Search region](/azure/search/search-region-support) support column for *AI Enrichment*.|
    | **Name** | A descriptive name for your Azure AI services multi-service account resource. For example, *MyCognitiveServicesResource*. |
    | **Pricing tier** | The cost of your Azure AI services multi-service account depends on the options you choose and your usage. For more information, see the API [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/). |

1. Configure other settings for your resource as needed, read, and accept the conditions (as applicable), and then select **Review + create**.

> [!TIP]
> If your subscription doesn't allow you to create an AI Foundry resource, you might need to enable the privilege of that [Azure resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) using the [Azure portal](/azure/azure-resource-manager/management/resource-providers-and-types#azure-portal), [PowerShell command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-powershell), or an [Azure CLI command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-cli). If you aren't the subscription owner, ask someone with the role of *Owner* or *Admin* to complete the registration for you or ask for the **/register/action** privileges to be granted to your account.

## Related content

[Create an AI Foundry resource](multi-service-resource.md).
