---
title: Create a Microsoft Foundry resource
titleSuffix: Foundry Tools
description: Create and manage a Microsoft Foundry resource for Content Understanding operations
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - build-2025
---

# Create a Microsoft Foundry resource

To use Content Understanding, you need a Microsoft Foundry resource.

> [!IMPORTANT]
> The steps below explain how to create a resource for use with the [REST API](../quickstart/use-rest-api.md). To use Content Understanding in the Content Understanding Studio, see the [Content Understanding Studio quickstart](../quickstart/content-understanding-studio.md).


## Prerequisites

To get started, you need an active [**Azure account**](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). If you don't have one, you can [**create a free subscription**](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Create a resource

To use the Azure Content Understanding in Foundry Tools service, you must create an [**Microsoft Foundry resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal. Be sure to create your resource in a supported region. The Content Understanding features are available in supported regions listed here [Support Regions](../language-region-support.md#region-support).

1. Complete the **Foundry** resource fields with the following values:

    * **Subscription**. Select one of your available Azure subscriptions.
    * **Resource group**. The [Azure resource group](/azure/cloud-adoption-framework/govern/resource-consistency/resource-access-management#what-is-an-azure-resource-group) that contains your resource. You can create a new group or add it to an existing group.
    * **Name**. Enter a name for your resource. We recommend using a descriptive name, for example *YourNameAIFoundryResource*.

1. Configure other settings for your resource as needed, read, and accept the conditions (as applicable), and then select **Review + create**.

1. Azure will run a quick validation check, after a few seconds you should see a green banner that says **Validation Passed**.

1. Once the validation banner appears, select the **Create** button from the bottom-left corner.

1. After you select create, you'll be redirected to a new page that says **Deployment in progress**. After a few seconds, you'll see a message that says, **Your deployment is complete**.
 

## Try out Content Understanding

Now that you created your Microsoft Foundry resource, you're ready to try out the Content Understanding service.

* Ready to go straight to code? Follow the [REST API QuickStart](../quickstart/use-rest-api.md).
* Try Content Understanding with no code in [Content Understanding Studio](https://aka.ms/cu-studio).
