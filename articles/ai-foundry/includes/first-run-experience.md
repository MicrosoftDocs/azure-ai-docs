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

## First run experience


::: moniker range="foundry-classic"
Use this fast path when you don't have any projects yet.

In the portal, you can explore a rich catalog of cutting-edge models from many different providers. For this tutorial, search and then select the **gpt-4o** model.

1.  [!INCLUDE [version-sign-in](version-sign-in.md)]
1.  From the overview page or **[Model catalog](https://ai.azure.com/explore/models)**, select **gpt-4o** (or **gpt-4o-mini**).

    :::image type="content" source="../media/quickstarts/start-building.png" alt-text="Screenshot shows how to start with a model in Azure AI Foundry portal.":::

1. Select **Use this model**. When prompted, enter a project name and select **Create**.
1. Review the deployment name and select **Create**.
1. Then select **Connect and deploy** after selecting a deployment type.
1. Select **Open in playground** from the deployment page after it's deployed.
1. You land in the Chat playground with the model pre-deployed and ready to use.

If you're building an agent, you can instead start with **Create an agent**. The steps are similar, but in a different order.  Once the project is created, you arrive at the Agent playground instead of the Chat playground.

Now that you have an agent, you can interact with it either in code or in the portal.
::: moniker-end

::: moniker range="foundry"
Create an agent in the Azure AI Foundry portal.  Once you create the agent, you can interact with it either in code or in the portal.

1. [!INCLUDE [version-sign-in](version-sign-in.md)]
1. The project you are working on appears in the upper-left corner.  
1. To create a new project, select the project name, then **All resources**, then **Create project**.
1. Select  **Build** in the middle of the page, then **New agent**.
1. Give your agent a name or keep the default name.
1. Select **Create**.
1. A model is deployed into your project. You can now interact with your agent.


::: moniker-end
