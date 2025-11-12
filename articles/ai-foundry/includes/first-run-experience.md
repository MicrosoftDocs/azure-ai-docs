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

## Create resources


::: moniker range="foundry-classic"
[!INCLUDE [first-run-experience-classic](first-run-experience-classic.md)]
::: moniker-end

::: moniker range="foundry"
You'll start in Microsoft Foundry portal to create a project and deploy a model. This quickstart uses the **gpt-4-1-mini** model, but you can use any supported model from several providers. 

1. [!INCLUDE [version-sign-in](version-sign-in.md)]
1. Projects help organize your work. The project you're working on appears in the upper-left corner. 
1. To create a new project, select the project name, then  **Create new project**.
1. Give your project a name and select **Create project**.
1. Now deploy a model into the project:
    1. Select **Discover** in the upper-right navigation.
    1. Select **Models**.
    1. Search for the **gpt-4.1-mini** model.
    1. Select **Deploy** > **Quick deploy** to add it to your project.

Foundry Models allows customers to consume the most powerful models from flagship model providers using a single endpoint and credentials. This means that you can switch between models and consume them from your application without changing a single line of code.

You're now ready to move on to interacting with your model and creating an agent.

::: moniker-end
