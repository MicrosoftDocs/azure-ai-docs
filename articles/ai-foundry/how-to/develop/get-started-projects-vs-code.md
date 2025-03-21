---
title: Get started with the Azure AI Foundry for Visual Studio Code extension
titleSuffix: Azure AI Foundry
description: Use this article to learn how to deploy Large Language Models and develop AI agents using Azure AI Foundry capabilities directly in VS Code.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: quickstart
ms.date: 03/22/2025
ms.reviewer: 
ms.author: sgilley
author: sdgilley
# customer intent: As an AI app developer, I want to learn how to use the Azure AI Foundry for Visual Studio Code extension so that I can deploy Large Language Models and develop AI agents using Azure AI Foundry capabilities directly in VS Code.
---

# Get started with the Azure AI Foundry for Visual Studio Code extension

With the Azure AI Foundry for Visual Studio Code extension, deploy Large Language Models, build AI apps, work with Agents, and more from the Visual Studio Code interface.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]


## Prerequisites

Before using the Azure AI Foundry for Visual Studio Code extension, you must:

- Download, install, and configure Visual Studio Code. More information: [Download Visual Studio Code](https://code.visualstudio.com/Download)

- You need permissions to create an Azure AI Foundry hub or have one created for you.
    - If your role is **Contributor** or **Owner**, you can follow the steps in this tutorial.
    - If your role is **Azure AI Developer**, the hub must already be created before you can complete this tutorial. Your user role must be **Azure AI Developer**, **Contributor**, or **Owner** on the hub. For more information, see [hubs](../../concepts/ai-resources.md) and [Azure AI roles](../../concepts/rbac-ai-foundry.md).

- Your subscription needs to be below your [quota limit](../quota.md) to [deploy a new model in this tutorial](#deploy-a-chat-model). Otherwise you already need to have a [deployed chat model](../deploy-models-openai.md).

- Install [Azure Resources for Visual Studio Code (Preview) Extension](): View and manage Azure resources directly from VS Code.

- Install the [AI Toolkit for Visual Studio Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio): A VS Code extension that enables you to download, test, fine-tune, and deploy AI models with your apps or in the cloud. For more information, see the AI Toolkit overview.

## Installation

After you install Visual Studio Code, you need to install the Azure AI Foundry for Visual Studio Code extension.

To install the Azure AI Foundry for Visual Studio Code extension:

1. Open Visual Studio Code.

1. Select **Extensions** from the left pane.

1. Select the **Settings** icon from the top-right on the extensions pane.

1. Search for and select **Azure AI Foundry**.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/vs-code-extension.png" alt-text="Select Azure AI Foundry Visual Studio Code extension.":::

1. Select **Install**.

1. Verify the extension is installed successfully from the status messages.

## Getting started

Get started with the Azure AI Foundry extension by using the following steps. 

> [!NOTE]
> For a full list of features available in the extension, use the Command Palette and search **AI Foundry**. The following screenshot shows some of the actions for AI Foundry.
>     :::image type="content" source="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png" alt-text="A screenshot of the Visual Studio Code command palette for AI Foundry." lightbox="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png":::


### Sign-in to your resources

The following steps help you get started with the Azure AI Foundry extension: 

1. Select the Azure Icon on the VS Code Navbar. 

1. Sign in by selecting the `Sign in to Azure...` item in the **Azure Resources** view.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/sign-in-to-azure-resources.png" alt-text="A screenshot of the Visual Studio Code command palette for AI Foundry." lightbox="../../media/how-to/get-started-projects-vs-code/sign-in-to-azure-resources.png":::


1. Under the "Resources" section, select your Azure Subscription and Resource Group. 

1. Select "AI Foundry" and open your project.

1. The **Agents** and **Models** sections are listed under your project. 


### Set the default project

 Set your default AI Project with the following steps:

1. Open a new Visual Studio Code window.

1. Select <kbd>F1</kbd> to open the command palette.

1. Enter **AI Foundry: Select Default Project** and press enter.

1. Select the AI Foundry Project you want to use from the list of available projects and press enter.

Your selected project will now display **Default** after the project name.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/default-project.png" alt-text="A screenshot of the designated default project." lightbox="../../media/how-to/get-started-projects-vs-code/default-project.png"::: 


## Working with models

The Azure AI Foundry for Visual Studio Code extension enables you to create, interact with, and deploy Large Language Models from within Visual Studio Code.

### Explore all models with the model catalog

Use the model catalog to explore and deploy a curated selection of models available in Azure AI Foundry.

1. Select <kbd>F1</kbd> to open the command palette.

1. Enter **AI Foundry: Model Catalog** and press enter.

1. The **Model Catalog** page is displayed.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png" alt-text="Screenshot of the **Model Catalog** page in VS Code." lightbox="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png":::


1. Filter the **Model Catalog** by `Publisher` and/or `Task` using the dropdowns at the top-left of the page. 

1. Search for a specific model using the search bar at the top-center of the page.


#### Deploy a model from the model catalog

Deploy a selected model in the model catalog using the following steps:

1. Select the **Deploy in Azure** immediately following the selected model name. 

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deploy-from-model-catalog.png" alt-text="Screenshot of the highlighted Deploy in Azure link of the selected model." lightbox="../../media/how-to/get-started-projects-vs-code/deploy-from-model-catalog.png":::

1. In the top center, select the AI service to use in the **Choose an AI service** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-ai-service.png" alt-text="Screenshot of the Choose AI service dropdown." lightbox="../../media/how-to/get-started-projects-vs-code/choose-ai-service.png":::

1. In the top center, select the model version to use in the **Choose model version** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-model-version.png" alt-text="Screenshot of the Choose model version dropdown." lightbox="../../media/how-to/get-started-projects-vs-code/select-model-version.png":::

1. In the top center, select the deployment type to use in the **Choose deployment type** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-deployment-type.png" alt-text="Screenshot of the Choose deployment type dropdown." lightbox="../../media/how-to/get-started-projects-vs-code/select-deployment-type.png":::

1. In the top center, enter the model deployment name to use in the **Enter deployment name** textbox and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/enter-deployment-name.png" alt-text="Screenshot of the Choose deployment type dropdown." lightbox="./../media/how-to/get-started-projects-vs-code/enter-deployment-name.png":::

1. A confirmation dialog box will appear. Select the **Deploy** button to deploy the model to your project.


After a successful deployment, your model will be listed with your other deployed models under the **Models** section in your project.  

### Deploy, view, and update models

#### View deployed models

In the Azure Resources Extension view, select the **plus** icon next to **Models** to show the list of models deployed to your Azure AI Foundry project.

#### View model card information

Selecting the new model opens up a panel that provides some basic information

#### Update a model

I can make changes such as rate limit directly within VS Code.


### Explore the model sample code

Create sample code by right-clicking on your deployed model and selecting the **Open code file** option. 

By selecting your preferred SDK, coding language and authentication method, a code file will open, allowing you to jump straight into code.

### Interact with models using a model playground

If you need to do some testing before diving into code, the Playground is the right place for you.

We have integrated with the AI Toolkit extension to bring you a robust playground experience where you can chat interactively with the model and change settings and system instructions.

## Working with Azure AI Agent Service

###	Create and edit Azure AI Agents within the designer view

###	Show the Azure AI Agent YAML definition

###	Deploy Azure AI Agents to the AI Foundry Studio

### Add tools to the Azure AI Agent

### Interact with Agents using agents playground

## Clean up resources

##	Next step

