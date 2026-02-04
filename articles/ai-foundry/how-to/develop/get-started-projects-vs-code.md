---
title: Work with the Microsoft Foundry for Visual Studio Code extension
titleSuffix: Microsoft Foundry
description: Use this article to learn how to create projects and deploy Large Language Models using Microsoft Foundry capabilities directly in VS Code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 01/28/2026
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
monikerRange: foundry-classic || foundry

# customer intent: As an AI app developer, I want to learn how to use the Microsoft Foundry for Visual Studio Code extension so that I can create projects and deploy Large Language Models using Microsoft Foundry capabilities directly in VS Code.
---

# Work with the Microsoft Foundry for Visual Studio Code extension (Preview)

[Microsoft Foundry](/azure/ai-foundry/what-is-foundry) provides a unified platform for enterprise AI operations, model builders, and application development. This foundation combines production-grade infrastructure with friendly interfaces, ensuring organizations can build and operate AI applications with confidence.

With Foundry, you can: 

- Deploy the latest language models from Microsoft, OpenAI, Meta, DeepSeek, and more using the robust model catalog 

- Test the deployed models in a model playground 

- Quickly get started with developing generative AI applications using a collection of Azure curated code templates 

- Configure and deploy agents with Foundry Agent Service 

With the Foundry for Visual Studio Code extension, you can accomplish much of this workflow directly from Visual Studio Code. It also comes with other features, such as code templates, playgrounds, and integration with other VS Code extensions and features. 

This article shows you how to quickly get started using the features of the Foundry for Visual Studio Code extension. 

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]


## Prerequisites

Before using the Foundry for Visual Studio Code extension, you must:

- Download, install, and configure Visual Studio Code. More information: [Download Visual Studio Code](https://code.visualstudio.com/Download)

- Your subscription needs to be below your [quota limit](../quota.md) to [deploy a new model in this quickstart](#deploy-a-model-from-the-model-catalog). Otherwise you already need to have a [deployed chat model](../../foundry-models/how-to/deploy-foundry-models.md).

- Set the appropriate RBAC permissions to create and manage Foundry resources with the Visual Studio Code extension. For more information, see [Role-based access control for Foundry](/azure/ai-foundry/concepts/rbac-foundry).

## Installation

After you install Visual Studio Code, you need to install the Foundry for Visual Studio Code extension.

To install the Foundry for Visual Studio Code extension, either use the Visual Studio Code Marketplace or install it directly from within Visual Studio Code.

### Install from the Visual Studio Code Marketplace
To install the Foundry for Visual Studio Code extension from the Visual Studio Code Marketplace, follow these steps:

1. Open the [Foundry for Visual Studio Code extension page](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).
1. Select the **Install** button.
1. Follow the prompts to install the extension in Visual Studio Code.
1. After installation, open Visual Studio Code and verify the extension is installed successfully from the status messages.
1. The extension should now be visible in the primary navigation bar on the left side of Visual Studio Code.

### Install from within Visual Studio Code

To install the Foundry for Visual Studio Code extension in Visual Studio Code, follow these steps:

1. Open Visual Studio Code.

1. Select **Extensions** from the left pane.

1. Select the **Settings** icon from the top-right on the extensions pane.

1. Search for and select **Foundry**.

1. Select **Install**.

1. Verify the extension is installed successfully from the status messages.

## Get started

Get started with the Foundry extension by using the following steps. 

> [!NOTE]
> For a full list of features available in the extension, use the Command Palette. Select <kbd>F1</kbd> to open the command palette and search **Foundry**. The following screenshot shows some of the actions for Foundry.
>     :::image type="content" source="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png" alt-text="A screenshot of the Visual Studio Code command palette for Foundry." lightbox="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png":::

### Sign in to your resources

Sign in to your Azure subscription to access your resources with the following steps:

1. Select the Azure Icon on the VS Code Navbar. 

1. Sign in by selecting the `Sign in to Azure...` item in the **Azure Resources** view.

1. Under the "Resources" section, select your Azure Subscription and Resource Group. 

1. Select **Foundry** and right-click your project.

1. Select **Open in Foundry Extension**.

### Explore the Foundry Extension

The Foundry Extension opens in its own view, with the Foundry Icon now displayed on the VS Code Navbar. The extension has three main sections: **Resources**, **Tools**, and **Help and Feedback**.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/initial-view.png" alt-text="A screenshot of the Foundry Extension with highlighted sections.":::

- **Resources**: This section contains the resources you have access to in your Foundry project. The **Resources** section is the main view for interacting with your Foundry Services. It contains the following subsections:
  - **Models**: This section contains the models you can use to build and deploy your AI applications. The **Models** view is where you can find your deployed models in your Foundry project.  
  - **Declarative Agents**: This section contains your deployed declarative agents in your Foundry project.
  - **Hosted Agents (Preview)**: This section contains your deployed hosted agents in your Foundry project.
  - **Assets**: This section contains the assets you have in your Foundry project.
      - Connections: This subsection contains the connections you have in your Foundry project. for example, Bing Grounding connections.
      - Vector Stores: This subsection contains the vector stores you have in your Foundry project.
  - **Classic**: This section contains the agents built in your classic Foundry projects.

- **Tools**: This section contains the tools you can use to build and deploy your AI applications. The **Tools** view is where you can find the tools available to deploy and then work with your deployed models and agents. It contains the following subsections:
    - **Model Catalog**: The link to the model catalog you can use to discover and deploy models. 
    - **Model Playground**: The link to the model playground for interacting with your deployed models in your Foundry project.
    - **Remote Agent Playground**: The link to the agent playground for interacting with your deployed remote agents in your Foundry project.
    - **Local Agent Playground**: The link to the agent playground for interacting with your deployed local agents in your Foundry project.
    - **Local Visualizer**: The link to the local visualizer to visualize the interactions between agents and how they collaborate in your Foundry project.
    - **Deploy Hosted Agents**: The link to deploy a new hosted agent using a dockerfile in your Foundry project.
- **Help and Feedback**: This section contains links to the Foundry documentation, feedback, support, and the Microsoft Privacy Statement. It contains the following subsections:
    - **Documentation**: The link to the Foundry Extension documentation.
    - **GitHub**: The link to the Foundry extension GitHub repository.
    - **Microsoft Privacy Statement**: The link to the Microsoft Privacy Statement.
    - **Join the Foundry Community: Discord + Forum**: The link to the Foundry community Discord server.

>[!NOTE]
> To learn more about working with Agents in the Foundry Extension, see the [Work with Agent Service in Visual Studio Code](./vs-code-agents.md) article. 

## Create a project

You can create a new Foundry project from the Foundry Extension view with the following steps:

1. Select the **plus** icon next to **Resources** in the **Resources** section of the Foundry Extension view.

    You can either create a new resource group or select an existing one.
1. To create a new resource group:
    1. In the top center, select **Create new resource group** and press Enter.

    1. In the top center, enter the Azure Resource Group name to use in the **Enter new resource group** textbox and press Enter.

    1. In the top center, select the location you want to use from the list of available locations and press Enter.

1. To use an existing resource group:
    - In the top center, select the resource group you want to use from the list of available resource groups and press Enter.

1. In the top center, enter the Foundry Project name to use in the **Enter project name** textbox and press Enter.

After project deployment, a popup appears with the message **Project deployed successfully**.

To deploy a model to the newly created project, select the **Deploy a model** button in the popup.
This action opens the **Model Catalog** page in the Foundry Extension view to select the desired model to [deploy.](#deploy-a-model-from-the-model-catalog) 

### The default Foundry Project

When you open a project in the Foundry Extension, that project is set as your default project. 

Switch your default project by following these steps:

1. Right-click on the Foundry Project and select the **Switch Default Project in Azure Extension** option. 

1. In the top center, select the Foundry Project you want to use from the list of available projects and press Enter.

Your selected project will now display **Default** after the project name.

> [!TIP]
> Right-click on your project name to access the project endpoint and/or the project API key.

## Work with models

The Foundry for Visual Studio Code extension enables you to create, interact with, and deploy Large Language Models from within Visual Studio Code.

### Explore all models with the model catalog

The [model catalog](/azure/ai-foundry/how-to/model-catalog-overview) in Foundry portal is the hub to discover and use a wide range of models for building generative AI applications.

 Access the model catalog from several different ways:
- The **Foundry: Open Model Catalog** command palette command.
- Select the **plus** icon next to **Models** in the **Resources** section of the Foundry Extension view.
- Select the **Model Catalog** link in the **Tools** section of the Foundry Extension view.

#### Open the model catalog from the command palette

Access the model catalog from the command palette to explore and deploy a curated selection of models available in Foundry, right from inside VS Code.

1. Select <kbd>F1</kbd> to open the command palette.

1. Enter **Foundry: Open Model Catalog** and press Enter.

1. The **Model Catalog** page is displayed.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png" alt-text="Screenshot of the **Model Catalog** page in VS Code." lightbox="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png":::


1. Filter the **Model Catalog** by `Hosted by`,`Publisher`, `Feature` and/or `Model type` using the dropdowns at the top-left of the page. Select `Fine-Tuning Support` using the toggle button to filter models that support fine-tuning.

1. Search for a specific model using the search bar at the top-center of the page.

#### Open the model catalog from the Resources section

The **Model Catalog** is also available in the **Resources** section of the Foundry Extension view. 

In the Foundry Extension view, select the **plus** icon next to **Models** to open the Model Catalog.

> [!TIP] 
> You can also right-click on **Models** and select the **Deploy new AI model** option to open the Model Catalog to start the deployment process. 

#### Open the model catalog from the Tools section

The **Model Catalog** is also available in the **Tools** section of the Foundry Extension view. Double-click on the **Model Catalog** link to open the Model Catalog.

### Deploy a model from the model catalog

Deploy a selected model in the model catalog using the following steps:

1. Select the **Deploy** button immediately following the selected model name. 

1. The **Model deployment** page is displayed.

1. Enter the model deployment name to use in the **Enter deployment name** textbox and press Enter.

1. Select the deployment type to use in the **Deployment type** dropdown and press Enter.

1. Select the model version to use in the **Model version** dropdown and press Enter.

1. (Optional) Select the tokens per minute to use in the **Tokens per minute** slider and press Enter.

1. In the bottom-left corner, select the **Deploy in Foundry** button to deploy the model.

1. A confirmation dialog box appears. Select the **Deploy** button to deploy the model to your project.

1. After a successful deployment, your model will be listed by deployment name with your other deployed models under the **Models** section in your project.  

### View deployed models

In the Azure Resources Extension view, select the **caret** icon in front of the **Models** section to view the list of deployed models.

The expanded **Models** section displays the list of deployed models.

#### View model card information

Selecting a deployed model opens up a panel that provides some basic information:

- Deployment Info: This section contains the information about the model:
    - Name
    - Provisioning state
    - Deployment type
    - Rate limit information
    - Version info
    - Model name
    - Model version
- Endpoint info: This section contains the Target URI link, authentication type, and key.
- Useful links: This section contains the code sample repository and tutorial links to get started with AI application development.

#### Update a model

To update the model card information, select the **Edit** button on the top-right of the model card. 

Update the desired editable fields such as rate limit directly within VS Code.

To save the changes, select the **Save** button on the top-right of the model card. 

### Explore the model sample code

Create a sample code file using the following steps.

1. Right-click on your deployed model and select the **Open code file** option. 

1. In the top center, select your preferred SDK to use in the **Choose preferred SDK** dropdown and press Enter.

1. In the top center, select your preferred language to use in the **Choose language** dropdown and press Enter.

1. In the top center, select your preferred authentication method to use in the **Choose authentication method** dropdown and press Enter.

1. A sample code file is generated and opened in a new tab in VS Code.

#### Sample code file

This Python sample code file demonstrates a basic call to the responses API. The call is synchronous:

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/sample-code-file.png" alt-text="Screenshot of generated sample code file." lightbox="../../media/how-to/get-started-projects-vs-code/sample-code-file.png":::

### Interact with models using a model playground

Chat interactively with the model, change settings, and system instructions using the **Model Playground**.

The **Model Playground** is available in the **Tools** section of the Foundry Extension view. Double-click on the **Model Playground** link to open the Model Playground.

You can also open the model playground using the following steps:

1. Right-click on your deployed model and select the **Open in playground** option. 

1. The **Playground** page is displayed.

1. Type your prompt and see the outputs.

1. Additionally, you can use **View code** in the top-right corner to see details about how to access the model deployment programmatically.

1. Select the **History** link at the top-left of the playground to view the chat history. 

## Cleanup resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your models

1. In the VS Code navbar, refresh the **Foundry Extension**. In the **Resources** section, expand the **Models** subsection to display the list of deployed models.

1. Right-click on your deployed model to delete and select the **Delete** option.

### Delete your tools

Delete the connected tool with the following steps:

1. Open the Azure portal
1. Select the Azure Resource Group containing the tool.
1. Select the **Delete** button.  

##    Next steps

- Learn about [working with the Agent Service](./vs-code-agents.md) using this Visual Studio Code extension.
