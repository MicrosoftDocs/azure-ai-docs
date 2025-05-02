---
title: Create an Azure AI Foundry resource
titleSuffix: Azure AI services
description: Create and manage an Azure AI Foundry resource for Content Understanding operations
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.date: 5/19/2025
ms.custom: ignite-2024-understanding-release, references_regions
ms.author: lajanuar
---

# Create an Azure AI Foundry resource

To use Content Understanding, you need an Azure AI Foundry resource. This multi-service resource enables access to multiple Azure AI services with a single set of credentials.

## Prerequisites

1. To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free subscription**](https://azure.microsoft.com/free/).

1. Once you have your Azure subscription, create an [**Azure AI Foundry resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) in the Azure portal. The Azure AI Foundry resource is listed under **AI Foundry** > **AI Foundry** in the portal. The API kind is **AIServices**. 

    :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the AI Foundry resource page in the Azure portal.":::

    > [!IMPORTANT]
    > Azure provides more than one resource type for Azure AI services. Be sure to select the one that is listed under **AI Foundry** > **AI Foundry** with the logo as shown previously.

1. Select the **Create** button.

## Create a resource

To use the Azure AI Content Understanding service, you must create your Azure AI Foundry resource in a supported region. The Content Understanding features are available in the following regions:

| Geography | Region | Region Identifier |
| --- | --- | --- |
| US | West US | westus |
| Europe | Sweden Central | swedencentral |
| Australia | Australia East | australiaeast |

1. Complete the **AI Foundry** resource fields with the following values:

    * **Subscription**. Select one of your available Azure subscriptions.
    * **Resource group**. The [Azure resource group](/azure/cloud-adoption-framework/govern/resource-consistency/resource-access-management#what-is-an-azure-resource-group) that contains your resource. You can create a new group or add it to an existing group.
    * **Name**. Enter a name for your resource. We recommend using a descriptive name, for example *YourNameAIFoundryResource*.

1. Configure other settings for your resource as needed, read, and accept the conditions (as applicable), and then select **Review + create**.

1. Azure will run a quick validation check, after a few seconds you should see a green banner that says **Validation Passed**.

1. Once the validation banner appears, select the **Create** button from the bottom-left corner.

1. After you select create, you'll be redirected to a new page that says **Deployment in progress**. After a few seconds, you'll see a message that says, **Your deployment is complete**.
 

## Next steps: Try out Content Understanding

Now that you created your Azure AI Foundry resource, you're ready to try out the Content Understanding service.

* Check out this Quickstart to [try Content Understanding in the AI Foundry](../quickstart/use-ai-foundry.md).
* Ready to go straight to code? [Try the Content Understanding REST API](../quickstart/use-rest-api.md).
