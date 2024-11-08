---
title: "How to: Azure AI Content Understanding Azure AI Foundry"
titleSuffix: Azure AI services
description: Learn about to create a Content Understanding Project in Azure AI Foundry
author: laujan
manager: nitinme
ms.service: azure
ms.topic: quickstart
ms.date: 11/7/2024
---

# Create a Content Understanding Project in Azure AI Foundry


## Prerequisites

To use Content Understanding, you need an Azure AI Services resource. This resource provides access to multiple Azure AI services with a single set of credentials.

1. Get an Azure account:
   - If you don't have an Azure account, you can [create a free subscription](https://azure.microsoft.com/free/).
2. Create an Azure AI Services resource:
   - Once you have an Azure subscription, create an [Azure AI Services resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) in the Azure portal. 
   - This resource is listed under Azure AI services → Azure AI services in the portal.

    :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

    > [!IMPORTANT]
    > Azure provides more than one resource type named Azure AI services. Ensure you select the one listed under Azure AI services → Azure AI services with the logo shown above.

   For more information, see [Create an Azure AI Services resource](../how-to/create-multi-service-resource.md).

3. Go to the [Azure AI Foundry home page](https://ai.azure.com/) and log in with your Azure account.

4. Once logged in, follow the steps below to create an AI hub and Content Understanding project.

   ![Image of the home page]()

## Create an AI Studio hub
You deploy and manage your Azure AI Studio projects in hubs. Follow these steps to create a new hub:

1. From the [Azure AI Foundry home page](https://ai.azure.com/), select **All hubs** from the left pane and then select **➕New hub**.


    :::image type="content" source="../media/ai-studio/hub/create-new.png" alt-text="Screenshot of the Create a new hub button." lightbox="../media/ai-studio/hub/create-new.png":::

1. In the **Create a new hub** dialog window, enter a name for your hub, and select **Next**. Leave the default **Connect Azure AI Services** option selected. A new Azure AI services connection is created for the hub.


    :::image type="content" source="../media/ai-studio/hub/create-new-connection.png" alt-text="Screenshot of the Create a new hub dialog window." lightbox="../media/ai-studio/hub/create-new-connection.png":::

1. Review your entries then select **Create**.

    :::image type="content" source="../media/ai-studio/hub/create-new-review.png" alt-text="Screenshot of the review and finish dialog window." lightbox="../media/ai-studio/hub/create-new-review.png":::

## Create a Content Understanding project

1. Navigate to the Home page and select the Content Understanding landing page, you can learn more about the key benefits of MMI, some of the many supported scenarios, and you can begin creating your first MMI project.
1. The first step of your project creation will allow you to create an AI Hub, if you don’t have one already.