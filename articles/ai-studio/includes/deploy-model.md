---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-studio
ms.topic: include
ms.date: 10/29/2024
ms.custom: include
---
1. Sign in to [Azure AI Studio](https://ai.azure.com).
1. Studio remembers where you were last, so what you do next depends on where you are:

    * If you are in a project, select **Model catalog** from the left navigation pane.
    * If you have projects but are not in one, select the project you wish to use, then select **Model catalog** from the left navigation pane. Or, you can select **Model catalog and benchmarks** at the bottom of the screen.
    * If you have never used Azure AI Studio before, select **Explore models**. 
  
        :::image type="content" source="../media/tutorials/chat/home-page.png" alt-text="Screenshot of the home page if you have never created a project." lightbox="../media/tutorials/chat/home-page.png":::

1. Select the model you want to deploy from the list of models. For example, select **gpt-4o-mini**.

    :::image type="content" source="../media/tutorials/chat/select-model.png" alt-text="Screenshot of the model selection page." lightbox="../media/tutorials/chat/select-model.png":::

1. On the model details page, select **Deploy**.

    :::image type="content" source="../media/tutorials/chat/deploy-model.png" alt-text="Screenshot of the model details page with a button to deploy the model." lightbox="../media/tutorials/chat/deploy-model.png":::

1. If you are already signed into a project, you won't see this step.  Your model is deployed to your existing project.  If you are not in a project, on the **Select or create a project** page: 
 
    * If you have a project you want to use, select it.
    * If you don't yet have a project:
        1. Select **Create a new project**.
        1. Provide a name for your project.
        1. Select **Create a project**.

1. Change the default name if you want, then select **Connect and deploy**.
1. Once the model is deployed, select **Open in playground** to test your model.