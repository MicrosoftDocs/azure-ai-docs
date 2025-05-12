---
title: Create an Azure AI services multi-service resource
titleSuffix: Azure AI services
description: Create and manage an Azure AI Services multi-services resource for Content Understanding operations
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.date: 05/19/2025
ms.custom: references_regions
ms.author: lajanuar
---

# Create an Azure AI Services multi-service resource

To use Content Understanding, you need an Azure AI Services resource. This multi-service resource enables access to multiple Azure AI services with a single set of credentials.

## Prerequisites

1. To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free subscription**](https://azure.microsoft.com/free/).

1. Once you have your Azure subscription, create an [**Azure AI services multi-services resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) in the Azure portal. The Azure AI services multi-service resource is listed under Azure AI services → Azure AI services in the portal:

    :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

    > [!IMPORTANT]
    > Azure provides more than one resource type named Azure AI services. Be sure to select the one that is listed under Azure AI services → Azure AI services with the logo as shown previously.

1. Select the **Create** button.

## Create a resource

To use the Azure AI Content Understanding service, you must create your Azure AI Service resource in a supported region. Content Understanding is available in the following regions:

| Region | Region Identifier |
| --- | --- |
| West US 2 | westus2 |
| Sweden Central | swedencentral |
| Australia East | australiaeast |

1. Complete the **Azure AI Services** fields with the following values:

    * **Subscription**. Select one of your available Azure subscriptions.
    * **Resource group**. The [Azure resource group](/azure/cloud-adoption-framework/govern/resource-consistency/resource-access-management#what-is-an-azure-resource-group) that contains your resource. You can create a new group or add it to an existing group.
    * **Name**. Enter a name for your resource. We recommend using a descriptive name, for example `ProjectNameAIServicesResource`.

1. Configure other settings for your resource as needed, read, and accept the conditions (as applicable), and then select **Review + create**.

1. Azure will run a quick validation check, after a few seconds you should see a green banner that says **Validation Passed**.

1. Once the validation banner appears, select the **Create** button from the bottom-left corner.

1. After you select create, you'll be redirected to a new page that says **Deployment in progress**. After a few seconds, you'll see a message that says, **Your deployment is complete**.
 

## Next steps: Try out Content Understanding

Now that you created your Azure AI Services multi-service resource, you're ready to try out the Content Understanding service.

* Try Content Understanding with no code in [Azure AI Foundry](https://ai.azure.com/explore/aiservices/vision/contentunderstanding).
* Ready to go straight to code? Follow the [REST API QuickStart](../quickstart/use-rest-api.md).
