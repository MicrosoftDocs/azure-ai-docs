---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 01/21/2025
---

## Prerequisites
- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- Make sure you have the **Azure AI Developer** [RBAC role](../../../ai-foundry/concepts/rbac-azure-ai-foundry.md) assigned.

## Basic agent setup support

Before getting started, determine if you want to perform a basic agent setup or a standard agent setup. Azure AI Foundry only supports basic agent setup. 

**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources. A basic setup can be created using the Azure AI Foundry portal or an automated bicep template.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage. Standard setup can only be performed using an automated bicep template.

> [!IMPORTANT]
> The Azure AI Foundry portal only supports basic setup at this time. If you want to perform a standard agent setup, use the other tabs at the top of the article to learn about standard agent configuration.  

## Create a Foundry project in Azure AI Foundry portal

To create a new project, you need either the Owner or Contributor role on the resource group. If you're unable to create a project due to permissions, reach out to your administrator.

To create a project in Azure AI Foundry, follow these steps:

1. Go to Azure AI Foundry. If you are in a project, select Azure AI Foundry at the top left of the page to go to the Home page.

1. Select **+ New**.

1. Enter a name for the project. If you want to customize the default values, select **Advanced options**.    
<!-- 
 see the [Azure AI Foundry documentation](../../../ai-foundry/how-to/create-projects.md?tabs=ai-studio#customize-the-hub).
-->

    :::image type="content" source="../media/quickstart/create-project.png" alt-text="Screenshot of the project details page within the create project dialog." lightbox="../media/quickstart/create-project.png":::

1. Select **Create**.

## Deploy a model

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
1. Go to your project or [create a new project](../../../ai-foundry/how-to/create-projects.md) in Azure AI Foundry portal.
1. From your project overview, select **Agents**, located under **Build and customize**.

1. Select your Azure OpenAI resource.

    :::image type="content" source="../media/quickstart/agents-foundry.png" alt-text="A screenshot of the initial Agents screen." lightbox="../media/quickstart/agents-foundry.png"::: 
 
1. Select a [model](../concepts/model-region-support.md) deployment for the Agent to use. If you don't have one, a screen to deploy a new model will open. Otherwise you can select **Deploy a model**.

    :::image type="content" source="../media/quickstart/select-deploy-model.png" alt-text="A screenshot of the model selection screen." lightbox="../media/quickstart/select-deploy-model.png"::: 

    :::image type="content" source="../media/quickstart/model-list.png" alt-text="A screenshot of the available models." lightbox="../media/quickstart/model-list.png"::: 

## Use the agent playground

The **Agents playground** allows you to explore, prototype, and test agents without needing to run any code. From this page, you can quickly iterate and experiment with new ideas.

1. In the **Create and debug your agents** screen, select your agent, or create a new one with **New agent**. The **Setup** pane on the right is where you can change its parameters and tools. 

    You can optionally give your agent a name other than the one generated for it, and add instructions to help improve its performance. Give your agent clear directions on what to do and how to do it. Include specific tasks, their order, and any special instructions like tone or engagement style.

    :::image type="content" source="../media/quickstart/create-debug-agent.png" alt-text="A screenshot of the Agents create and debug screen." lightbox="../media/quickstart/create-debug-agent.png":::

    > [!TIP]
    > Your agent can access multiple tools such as [code interpreter](../how-to/tools/code-interpreter.md) that extend its capabilities, such as the ability to search the web with Bing, run code, and more. In the **Setup** pane, scroll down to **knowledge** and **action** and select **Add** to see the tools available for use. 
    > :::image type="content" source="../media/quickstart/portal-tools.png" alt-text="A screenshot of the Agents tool choices." lightbox="../media/quickstart/portal-tools.png":::

## See also

Check out the [models](../concepts/model-region-support.md) that you can use with Agents.
