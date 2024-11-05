---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-studio
ms.topic: include
ms.date: 5/21/2024
ms.custom: include, build-2024
---

> [!NOTE]
> A hub in Azure AI Studio is a one-stop shop where you manage everything your AI project needs, like security and resources, so you can develop and test faster. To learn more about how hubs can help you, see the [Hubs and projects overview](/azure/ai-studio/concepts/ai-resources) article.

To create a hub in [Azure AI Studio](https://ai.azure.com), follow these steps:

1. Go to the **Home** page in [Azure AI Studio](https://ai.azure.com) and sign in with your Azure account.
1. Select **All resources** on the left pane. If you cannot see this option, in the top bar select **All resources & projects**. Then select **+ New hub**.

    :::image type="content" source="../media/how-to/hubs/hub-new.png" alt-text="Screenshot of the button to create a new hub." lightbox="../media/how-to/hubs/hub-new.png":::

1. In the **Create a new hub** dialog, enter a name for your hub (such as *contoso-hub*). If you don't have a resource group, a new **Resource group** will be created linked to the **Subscription** provided. Leave the default **Connect Azure AI Services** option selected. 
1. Select **Next**. If you didn't reuse an existing resource group, a new resource group (*rg-contoso*) is created.  Also an Azure AI service (*ai-contoso-hub*) is created for the hub.

    :::image type="content" source="../media/how-to/hubs/hub-new-connect-services.png" alt-text="Screenshot of the dialog to connect services while creating a new hub." lightbox="../media/how-to/hubs/hub-new-connect-services.png":::

    > [!NOTE]
    > If you don't see (new) before the **Resource group** and **Connect Azure AI Services** entries then an existing resource is being used. For the purposes of this tutorial, create a seperate entity via **Create new resource group** and **Create new AI Services**. This will allow you to prevent any unexpected charges by deleting the entities after the tutorial.

1. Review the information and select **Create**.

    :::image type="content" source="../media/how-to/hubs/hub-new-review-create.png" alt-text="Screenshot of the dialog to review the settings for the new hub." lightbox="../media/how-to/hubs/hub-new-review-create.png":::

1. You can view the progress of the hub creation in the wizard. 

    :::image type="content" source="../media/how-to/hubs/hub-new-creating-resources.png" alt-text="Screenshot of the dialog to review the progress of hub resources creation." lightbox="../media/how-to/hubs/hub-new-creating-resources.png":::
