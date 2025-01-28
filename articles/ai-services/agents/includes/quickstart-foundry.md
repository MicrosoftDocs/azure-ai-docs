---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: include
ms.date: 01/21/2025
---

## Prerequisites
- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
<!--
- An [Azure AI hub resource](../../../ai-studio/how-to/create-azure-ai-resource.md) with a model deployed. For more information about model deployment, see the [resource deployment guide](../../../ai-studio/how-to/create-azure-ai-resource.md).
- An [Azure AI project](../../../ai-studio/how-to/create-projects.md) in Azure AI Foundry portal.
-->
- Make sure you have the **Azure AI Developer** [RBAC role](../../../ai-studio/concepts/rbac-ai-studio.md) assigned.

## Choose basic or standard agent setup

Before getting started, determine if you want to perform a basic agent setup or a standard agent setup. 

**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources. A basic setup can be created using the Azure AI Foundry portal or an automated bicep template.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage. Standard setup can only be performed using an automated bicep template.

## [Basic setup (AI Foundry)](#tab/basic-foundry)

## Create a hub in Azure AI Foundry portal

To create a new hub, you need either the Owner or Contributor role on the resource group or on an existing hub. If you're unable to create a hub due to permissions, reach out to your administrator.

[!INCLUDE [Create Azure AI Foundry hub](../../../ai-studio/includes/create-hub.md)] 

## Use the Azure AI Foundry portal

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
1. Go to your project or [create a new project](../../../ai-studio//how-to/create-projects.md) in Azure AI Foundry portal.
1. From your project overview, select **Agents**, located under **playgrounds**. The Agents playground allows you to explore, prototype, and test AI Agents without needing to run any code. From this page, you can quickly iterate and experiment with new ideas.

1. Select your Azure OpenAI resource.

    :::image type="content" source="../media/quickstart/agents-foundry.png" alt-text="A screenshot of the initial Agents screen." lightbox="../media/quickstart/agents-foundry.png"::: 
 
1. Select a [model](../concepts/model-region-support.md) deployment for the Agent to use. If you don't have one, a screen to deploy a new model will open. Otherwise you can select **Deploy a model**.

    :::image type="content" source="../media/quickstart/select-deploy-model.png" alt-text="A screenshot of the model selection screen." lightbox="../media/quickstart/select-deploy-model.png"::: 

    :::image type="content" source="../media/quickstart/model-list.png" alt-text="A screenshot of the available models." lightbox="../media/quickstart/model-list.png"::: 

## [Basic setup (Bicep template)](#tab/basic-template)

### Use a bicep template

If you want to set up your hub, project, and deploy a model in an automated way, you can use the following bicep template.

| Description and Autodeploy  |  Diagram (click to zoom in) |
| -----------------------------------------------| -----------------------|
| Deploy a basic agent setup that uses Managed Identity for authentication. Resources for the AI hub, AI project, storage account, and AI Services are created for you. <br><br> The AI Services account is connected to your project and hub, and a gpt-4o-mini model is deployed in the eastus region. A Microsoft-managed key vault is used by default. <br><br> [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fbasic-agent-identity%2Fazuredeploy.json) |  :::image type="content" source="../media/quickstart/basic-agent-setup-resources.png" alt-text="An architecture diagram for basic agent setup." lightbox="../media/quickstart/basic-agent-setup-resources.png"::: |

## [Standard setup (Bicep template)](#tab/standard-template)

### Bicep deployment

If you want to set up your hub, project, and deploy a model in an automated way, you can use the following bicep template.

| Description and Autodeploy  |  Diagram (click to zoom in) |
| -----------------------------------------------| -----------------------|
| Deploy a standard agent setup that uses Managed Identity for authentication. <br><br> Resources for the AI hub, AI project, key vault, storage account, AI Services, and AI Search are created for you. <br><br>The AI Services, AI Search, key vault, and storage account are connected to your project and hub. A gpt-4o-mini model is deployed in eastus region. <br><br> [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json) | :::image type="content" source="../media/quickstart/standard-agent-setup-resources.png" alt-text="An architecture diagram for standard agent setup." lightbox="../media/quickstart/standard-agent-setup-resources.png"::: |

---

## Go to the Azure AI Foundry portal (Preview)


1. In the **Create and debug your agents** screen that appears, select **New agent**. This will create a new agent, and open a **Setup** pane where you can change its parameters and tools. 

    You can optionally give your agent a name other than the one generated for it, and add instructions to help improve its performance. Give your agent clear directions on what to do and how to do it. Include specific tasks, their order, and any special instructions like tone or engagement style.

    :::image type="content" source="../media/quickstart/create-debug-agent.png" alt-text="A screenshot of the Agents create and debug screen." lightbox="../media/quickstart/create-debug-agent.png":::

    > [!TIP]
    > Your agent can access multiple [**tools**](../how-to/tools/overview.md) that extend its capabilities, such as the ability to search the web with Bing, run code, and more. In the **Setup** pane, scroll down to **knowledge** and **action** and select **Add** to see the tools available for use. 
    > :::image type="content" source="../media/quickstart/portal-tools.png" alt-text="A screenshot of the Agents tool choices." lightbox="../media/quickstart/portal-tools.png":::

    

1. At the top of the **Setup** pane, select **Try in playground** to start using your agent.

## Use your agent

The **Agents playground** allows you to explore, prototype, and test agents without needing to run any code. From this page, you can quickly iterate and experiment with new ideas. When you interact with an agent, it:

1. Creates a thread object, which contains the context for a conversation, including individual messages sent between the agent and a user.

1. Appends a message object to the thread. A new message will be added to the thread for each turn of a conversation between an agent and a user. 

1. Creates a run object on the thread to generate a response by calling the model and any tools you've added.     

To interact with your agent:

1. Optionally change the **agent name** if you want, and add **instructions**. Instructions guide the personality of the agent and define its goals. Instructions are similar to [system messages](../../openai/concepts/advanced-prompt-engineering.md). 

1. In the chat area of the playground, enter a message and wait for the agent to respond. 
    
:::image type="content" source="../media/quickstart/agents-playground.png" alt-text="A screenshot of the Agents playground." lightbox="../media/quickstart/agents-playground.png":::

## See also

* See the [tools overview](../how-to/tools/overview.md) to learn about the tools you can allow your agent to use to extend its capabilities.