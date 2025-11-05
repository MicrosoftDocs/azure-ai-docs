---
title: Include file
description: Include file
author: jonburchel
ms.reviewer: jburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 08/27/2025
ms.custom: include
---

## Create an agent 


::: moniker range="foundry-classic"

In the portal, you can explore a rich catalog of cutting-edge models from many different providers. For this tutorial, search and then select the **gpt-4o** model.

1. [!INCLUDE [version-sign-in](version-sign-in.md)]
1. If you're in a project, select **Azure AI Foundry** in the upper-left breadcrumb to leave the project. You'll create a new one in a moment.
1. From the landing page or **[Model catalog](https://ai.azure.com/explore/models)**, select **gpt-4o** (or **gpt-4o-mini**).

    :::image type="content" source="../media/quickstarts/start-building.png" alt-text="Screenshot shows how to start with a model in Azure AI Foundry portal.":::

1. Select **Use this model**. When prompted, enter a new project name and select **Create**.
1. Review the deployment name and select **Create**.
1. Then select **Connect and deploy** after selecting a deployment type.
1. Select **Open in playground** from the deployment page after it's deployed.
1. You land in the Chat playground with the model pre-deployed and ready to use.

If you're building an agent, you can instead start with **Create an agent**. The steps are similar, but in a different order.  Once the project is created, you arrive at the Agent playground instead of the Chat playground.

Now that you have an agent, you can interact with it either in code or in the portal.
::: moniker-end

::: moniker range="foundry"
You'll start in Azure AI Foundry portal to create a project and deploy a model.

1. [!INCLUDE [version-sign-in](version-sign-in.md)]
1. Projects help organize your work. The project you'e working on appears in the upper-left corner. 
1. To create a new project, select the project name, then  **Create new project**.
1. Give your project a name and select **Create project**.
1. Now deploy a model into the project:
    1. Select **Discover** in the upper-right navigation.
    1. Select **Models**.
    1. Search for the **gpt-4.1-mini** model.
    1. Select **Deploy** > **Quick deploy** to add it to your project.

You're now ready to move on to interacting with your model and creating an agent.

::: moniker-end
