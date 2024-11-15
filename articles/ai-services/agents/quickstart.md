---
title: Quickstart - Create a new Azure Agent Runtime project.
titleSuffix: Azure AI services
description: Use this guide to start using Azure Agent Runtime.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: quickstart
ms.date: 11/13/2024
zone_pivot_groups: programming-languages-agents
recommendations: false
---

# Quickstart: Create a new agent

Azure Agent Runtime allows you to create AI agents tailored to your needs through custom instructions and augmented by advanced tools like code interpreter, and custom functions.

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).

## Create an Azure AI Foundry hub, agent project 

Before you can create an agent, you need an Azure AI Foundry hub and project to connect the various required Azure resources. In this section you will:

* Create an Azure AI Hub to set up your app environment and Azure resources.

* Create an Azure AI project under your Hub creates an endpoint for your app to call, and sets up app services to access to resources in your tenant. Your project is used to organize your work and save state.

* Connect an Azure OpenAI resource or an Azure AI resource. 

To create a project in Azure AI Foundry, follow these steps:

1. Go to the Home page of [Azure AI Foundry](https://ai.azure.com/).

1. Select **+ New project**.

1. Enter a name for the project.

1. Select a hub from the dropdown to host your project. For information about the relationship between hubs and projects, see the hubs and projects overview documentation. If you don't yet have a hub, select **Create a new hub**.

    :::image type="content" source="../../ai-studio/media/how-to/projects/projects-create-details.png" alt-text="a screenshot showing project and hub creation." lightbox="../../ai-studio/media/how-to/projects/projects-create-details.png":::

1. In the left navigation menu, select **Agents**. Make sure your resource is selected, then click **Let's go**.

    :::image type="content" source="media/quickstart/agents-studio.png" alt-text="A screenshot of the Agents main page." lightbox="media/quickstart/agents-studio.png":::

1.  Choose your model, then select next.

    :::image type="content" source="media/quickstart/choose-model.png" alt-text="A screenshot of the model selection screen." lightbox="media/quickstart/choose-model.png":::

1. In the **Create and debug your agents** screen, you can select the agent that was created. Later when you interact with the agent you'll be able to see your threads, which are conversation sessions between an agent and a user. 


    You can also change various parameters for the agent, and tools that it can access. For now, select **Try in playground**.

    :::image type="content" source="media/quickstart/create-debug-agent.png" alt-text="A screenshot of the Agents create and debug screen." lightbox="media/quickstart/create-debug-agent.png":::

## Use your agent

The **Agents playground** allows you to explore, prototype, and test agents without needing to run any code. From this page, you can quickly iterate and experiment with new ideas. When you interact with an agent, it:

1. Creates a thread object, which contains the context for a conversation, including individual messages sent between the agent and a user.

1. Appends a message object to the thread. A new message will be added to the thread for each turn of a conversation between an agent and a user. 

1. Creates a run object on the thread to generate a response by calling the model and any tools you've added.     

To interact with your agent:

1. Optionally change the **agent name** if you want, and add **instructions**. Instructions guide the personality of the agent and define its goals. Instructions are similar to [system messages](../openai/concepts/advanced-prompt-engineering.md). 

1. In the chat area of the playground, enter a message and wait for the agent to respond. 
    
:::image type="content" source="media/quickstart/agents-playground.png" alt-text="A screenshot of the Agents playground." lightbox="media/quickstart/agents-playground.png":::


<!--
# [Standard setup](#tab/standard-setup)

# [Basic setup](#tab/basic-setup)


---
-->

