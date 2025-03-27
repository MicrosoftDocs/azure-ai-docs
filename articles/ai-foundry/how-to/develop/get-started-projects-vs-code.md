---
title: Work with the Azure AI Foundry for Visual Studio Code extension
titleSuffix: Azure AI Foundry
description: Use this article to learn how to deploy Large Language Models and develop AI agents using Azure AI Foundry capabilities directly in VS Code.
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ms.topic: how-to
ms.date: 03/28/2025
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex
# customer intent: As an AI app developer, I want to learn how to use the Azure AI Foundry for Visual Studio Code extension so that I can deploy Large Language Models and develop AI agents using Azure AI Foundry capabilities directly in VS Code.
---

# Work with the Azure AI Foundry for Visual Studio Code extension (Preview)

[Azure AI Foundry](/azure/ai-foundry/what-is-ai-foundry) provides a unified platform for enterprise AI operations, model builders, and application development. This foundation combines production-grade infrastructure with friendly interfaces, ensuring organizations can build and operate AI applications with confidence.

With Azure AI Foundry, you can: 

- Deploy the latest language models from Microsoft, OpenAI, Meta, DeepSeek, and more using the robust model catalog 

- Test the deployed models in a model playground 

- Quickly get started with developing generative AI applications using a collection of Azure curated code templates 

- Configure and deploy agents with Azure AI Agent Service 

With the Azure AI Foundry for Visual Studio Code extension, you can accomplish much of this workflow directly from Visual Studio Code. It also comes with other features, such as code templates, playgrounds, and integration with other VS Code extensions and features. 

This article shoes you how to quickly get started using the features of the Azure AI Foundry for Visual Studio Code extension. 

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]


## Prerequisites

Before using the Azure AI Foundry for Visual Studio Code extension, you must:

- Download, install, and configure Visual Studio Code. More information: [Download Visual Studio Code](https://code.visualstudio.com/Download)

- [An existing Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects?tabs=ai-studio). The extension interacts with Azure AI Foundry at the project level.

- Your subscription needs to be below your [quota limit](../quota.md) to [deploy a new model in this quickstart](#deploy-a-model-from-the-model-catalog). Otherwise you already need to have a [deployed chat model](../deploy-models-openai.md).

## Installation

After you install Visual Studio Code, you need to install the Azure AI Foundry for Visual Studio Code extension.

To install the Azure AI Foundry for Visual Studio Code extension:

1. Open Visual Studio Code.

1. Select **Extensions** from the left pane.

1. Select the **Settings** icon from the top-right on the extensions pane.

1. Search for and select **Azure AI Foundry**.

1. Select **Install**.

1. Verify the extension is installed successfully from the status messages.

## Get started

Get started with the Azure AI Foundry extension by using the following steps. 

> [!NOTE]
> For a full list of features available in the extension, use the Command Palette. Select <kbd>F1</kbd> to open the command palette and search **Azure AI Foundry**. The following screenshot shows some of the actions for Azure AI Foundry.
>     :::image type="content" source="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png" alt-text="A screenshot of the Visual Studio Code command palette for Azure AI Foundry." lightbox="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png":::


### Sign-in to your resources

Sign-in to your Azure subscription to access your resources with the following steps:

1. Select the Azure Icon on the VS Code Navbar. 

1. Sign in by selecting the `Sign in to Azure...` item in the **Azure Resources** view.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/sign-in-to-azure-resources.png" alt-text="A screenshot of the Sign in to Azure option." lightbox="../../media/how-to/get-started-projects-vs-code/sign-in-to-azure-resources.png":::


1. Under the "Resources" section, select your Azure Subscription and Resource Group. 

1. Select **Azure AI Foundry** and open your project.

1. The **Agents** and **Models** sections are listed under your project. 


### Set the default Azure AI Foundry Project

 Set your default Azure AI Foundry Project with the following steps:

1. Open a new Visual Studio Code window.

1. Select <kbd>F1</kbd> to open the command palette.

1. Enter **Azure AI Foundry: Select Default Project** and press enter.

1. Select the Azure AI Foundry Project you want to use from the list of available projects and press enter.

Your selected project will now display **Default** after the project name.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/default-project.png" alt-text="A screenshot of the designated default project." lightbox="../../media/how-to/get-started-projects-vs-code/default-project.png"::: 


## Work with models

The Azure AI Foundry for Visual Studio Code extension enables you to create, interact with, and deploy Large Language Models from within Visual Studio Code.

### Explore all models with the model catalog

The [model catalog](/azure/ai-foundry/how-to/model-catalog-overview) in Azure AI Foundry portal is the hub to discover and use a wide range of models for building generative AI applications.

 Access the model catalog from the command palette to explore and deploy a curated selection of models available in Azure AI Foundry, right from inside VS Code.

1. Select <kbd>F1</kbd> to open the command palette.

1. Enter **Azure AI Foundry: Open Model Catalog** and press enter.

1. The **Model Catalog** page is displayed.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png" alt-text="Screenshot of the **Model Catalog** page in VS Code." lightbox="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png":::


1. Filter the **Model Catalog** by `Publisher` and/or `Task` using the dropdowns at the top-left of the page. 

1. Search for a specific model using the search bar at the top-center of the page.


#### Deploy a model from the model catalog

Deploy a selected model in the model catalog using the following steps:

1. Select the **Deploy in Azure** immediately following the selected model name. 

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deploy-from-model-catalog.png" alt-text="Screenshot of the highlighted Deploy in Azure link of the selected model." lightbox="../../media/how-to/get-started-projects-vs-code/deploy-from-model-catalog.png":::

1. In the top center, select the AI service to use in the **Choose an AI service** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-ai-service.png" alt-text="Screenshot of the Chosen AI service dropdown." lightbox="../../media/how-to/get-started-projects-vs-code/choose-ai-service.png":::

1. In the top center, select the model version to use in the **Choose model version** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-model-version.png" alt-text="Screenshot of the Choose model version dropdown." lightbox="../../media/how-to/get-started-projects-vs-code/select-model-version.png":::

1. In the top center, select the deployment type to use in the **Choose deployment type** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-deployment-type.png" alt-text="Screenshot of the Choose deployment type dropdown." lightbox="../../media/how-to/get-started-projects-vs-code/select-deployment-type.png":::

1. In the top center, enter the model deployment name to use in the **Enter deployment name** textbox and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/enter-deployment-name.png" alt-text="Screenshot of the Enter deployment name textbox." lightbox="../../media/how-to/get-started-projects-vs-code/enter-deployment-name.png":::

1. A confirmation dialog box appears. Select the **Deploy** button to deploy the model to your project.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deploy-model-popup.png" alt-text="Screenshot of the confirmation dialog box with the Deploy button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/deploy-model-popup.png":::

1. After a successful deployment, your model will be listed by deployment name with your other deployed models under the **Models** section in your project.  

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deployed-model.png" alt-text="Screenshot of the newly deployed model under the Models section." lightbox="../../media/how-to/get-started-projects-vs-code/deployed-model.png":::

### Deploy, view, and update models

#### Deploy a model

You can also deploy a model directly from your Azure AI Foundry project. 

1. In the Azure Resources Extension view, select the **plus** icon next to **Models** to start the deployment process.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-model-plus-expanded.png" alt-text="Screenshot of the plus sign next to models with the list of models expanded." lightbox="../../media/how-to/get-started-projects-vs-code/select-model-plus-expanded.png":::

    > [!TIP] 
    > You can also right-click on **Models** and select the **Deploy new AI model** option to start the deployment process. 

1. In the top center, select the AI service to use in the **Choose an AI service** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-ai-service.png" alt-text="Screenshot of the Choose AI service dropdown for model deployment." lightbox="../../media/how-to/get-started-projects-vs-code/choose-ai-service.png":::

1. In the top center, select the model to deploy in the **Choose a model to deploy** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-deployment-model.png" alt-text="Screenshot of the Choose a model to deploy dropdown." lightbox="../../media/how-to/get-started-projects-vs-code/select-deployment-model.png":::

1. In the top center, select the model version to use in the **Choose model version** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-model-version-2.png" alt-text="Screenshot of the Choose model version dropdown for model deployment." lightbox="../../media/how-to/get-started-projects-vs-code/select-model-version-2.png":::

1. In the top center, select the deployment type to use in the **Choose deployment type** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-deployment-type.png" alt-text="Screenshot of the Choose deployment type dropdown for model deployment." lightbox="../../media/how-to/get-started-projects-vs-code/select-deployment-type.png":::

1. In the top center, enter the model deployment name to use in the **Enter deployment name** textbox and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/enter-deployment-name-2.png" alt-text="Screenshot of the Enter deployment name textbox for model deployment." lightbox="../../media/how-to/get-started-projects-vs-code/enter-deployment-name-2.png":::

1. A confirmation dialog box appears. Select the **Deploy** button to deploy the model to your project.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deploy-model-popup-2.png" alt-text="Screenshot of the model deployment confirmation dialog box with the Deploy button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/deploy-model-popup-2.png":::

1. After a successful deployment, your model will be listed with your other deployed models under the **Models** section in your project.  

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deployed-model-2.png" alt-text="Screenshot of the deployed model under the Models section." lightbox="../../media/how-to/get-started-projects-vs-code/deployed-model-2.png":::

#### View deployed models

In the Azure Resources Extension view, select the **caret** icon in front of the **Models** 
section to view the list of deployed models.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-model-caret.png" alt-text="Screenshot of the highlighted caret icon next to the Models subsection." lightbox="../../media/how-to/get-started-projects-vs-code/select-model-caret.png":::

The expanded **Models** section displays the list of deployed models.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-model-caret-expanded.png" alt-text="Screenshot of the deployed models in the Models subsection." lightbox="../../media/how-to/get-started-projects-vs-code/select-model-caret-expanded.png":::

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

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/edit-model-card.png" alt-text="Screenshot of the model card for the selected model with the Edit button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/edit-model-card.png":::

Update the desired editable fields such as rate limit directly within VS Code.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/save-model-changes.png" alt-text="Screenshot of the model card with editable fields and the Save button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/save-model-changes.png":::

To save the changes, select the **Save** button on the top-right of the model card. 

### Explore the model sample code

Create a sample code file using the following steps.

1. Right-click on your deployed model and select the **Open code file** option. 

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/open-code-file.png" alt-text="Screenshot of the model context menu with the Open Code file option highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/open-code-file.png":::

1. In the top center, select your preferred SDK to use in the **Choose preferred SDK** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-preferred-sdk.png" alt-text="Screenshot of the Choose preferred SDK dropdown for model code file selection." lightbox="../../media/how-to/get-started-projects-vs-code/choose-preferred-sdk.png":::

1. In the top center, select your preferred language to use in the **Choose language** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-language.png" alt-text="Screenshot of the Choose language dropdown for model code file selection." lightbox="../../media/how-to/get-started-projects-vs-code/choose-language.png":::

1. In the top center, select your preferred authentication method to use in the **Choose authentication method** dropdown and press enter.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/choose-auth-method.png" alt-text="Screenshot of the Choose authentication method dropdown for model code file selection." lightbox="../../media/how-to/get-started-projects-vs-code/choose-auth-method.png":::

#### Sample code file

This Python sample code file that demonstrates a basic call to the chat completion API. The call is synchronous:

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/sample-code-file.png" alt-text="Screenshot of generated sample code file." lightbox="../../media/how-to/get-started-projects-vs-code/sample-code-file.png":::

### Interact with models using a model playground

Chat interactively with the model, change settings, and system instructions using the **Model Playground**.

Open the model playground using the following steps:

1. Right-click on your deployed model and select the **Open in playground** option. 

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/open-playground.png" alt-text="Screenshot of the model context menu with the Open in playground option highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/open-playground.png":::

1. The **Playground** page is displayed.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/display-playground.png" alt-text="Screenshot of the **Playground** page in VS Code." lightbox="../../media/how-to/get-started-projects-vs-code/display-playground.png":::

1. Type your prompt and see the outputs.

1. Additionally, you can use **View code** in the top-right corner to see details about how to access the model deployment programmatically.

1. Select the **History** link at the top-left of the playground to view the chat history. 


## Work with Azure AI Agent Service

After you deploy a model using the VS Code extension, AI Foundry, API, or SDK, you can work with [Azure AI Agent Service](/azure/ai-services/agents/overview). Agents are "smart" microservices that:

- Answer questions using their training data or search other sources with Retrieval Augmented Generation (RAG)
- Perform specific actions
- Automate complete workflows

Agents combine AI models with tools to access and interact with your data.

Azure AI Foundry developers can stay productive by developing, testing, and deploying agents in the familiar and powerful environment of VS Code.

###	Create and edit Azure AI Agents within the designer view

Follow these steps to create an Azure AI Agent:

1. First, finish the [Get Started](#get-started) section to sign in to your Azure resources and set your default project.
 
1. [Deploy a model](#deploy-a-model) to use with your agent.

1. Select your AI Foundry project in the Azure Resources sidebar. 

1. Under your project, find the **Agents** section.

1. Select the **+** (plus) icon next to the **Agents** subsection to create a new AI Agent.

 :::image type="content" source="../../media/how-to/get-started-projects-vs-code/select-agent-plus.png" alt-text="Screenshot of the plus sign next to the Agents subsection.":::

1. In the **Save As** dialog box, select a directory and enter a name for your new AI Agent .yaml file. 

1. Select the **Save Agent File** button to save your AI Agent file.

 :::image type="content" source="../../media/how-to/get-started-projects-vs-code/enter-agent-name.png" alt-text="Screenshot of the VS Code Save As dialog to save the agent yaml file." lightbox="../../media/how-to/get-started-projects-vs-code/enter-agent-name.png":::

### Interact with your agent in the designer

After you choose your save location, the Designer view will open to edit your AI Agent.

1. Perform the following tasks in the agent designer:

    1. Enter a name for your agent in the prompt.

    1. Enter your model deployment name. The deployment name you chose when you deployed an existing model.

    > [!TIP]
    > The model deployment name must be the exact name you chose for the model you deployed in your Azure AI Foundry project. In the following image, `gpt-4o-1` is the model deployment name you chose at deployment. `gpt-4o` is the model name. 
    >  :::image type="content" source="../../media/how-to/get-started-projects-vs-code/deployment-model-name.png" alt-text="Screenshot of the highlighted deployment model names, an arrow between them, and the model name highlighted in a different color." lightbox="../../media/how-to/get-started-projects-vs-code/deployment-model-name.png":::

    1. Configure the following fields. The **ID** is generated by the extension:
    
       - Add a description for your agent
       - Set system instructions 
       - Configure tools for agent use

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-designer.png" alt-text="Screenshot of the Agent designer that enables you to edit and interact with your AI Agent." lightbox="../../media/how-to/get-started-projects-vs-code/agent-designer.png":::
 
1. Select the **Save locally** button in the bottom-center of the **Agent Preferences** screen to store your agent configuration.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/save-agent-locally.png" alt-text="Screenshot of the Agent designer with the 'Save locally' button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/save-agent-locally.png":::

###	Show the Azure AI Agent YAML definition

Select the **Open Yaml File** on the top-right of the designer to open your AI Agent .yaml file. This file contains the details and setup information for your agent, similar to the following .yaml file example: 

```yml
version: 1.0.0
name: BingAgent
description: Description of the agent
metadata:
  author: Author Name
  tag: basic
id: ''
model:
  id: ''
  options:
    temperature: 1
    top_p: 1
instructions: Instructions for the agent
tools: []
```

### Add tools to the Azure AI Agent

Azure AI Agent Service has a set of tools that you can use to interact with your data sources, such as:
 - Grounding with Bing search
 - Azure AI Search 
 - Azure Functions 
 - File retrieval 
 - Code interpreter

#### Create the tool configuration file

The Agent Designer adds tools to an AI Agent via .yaml files. 

Create a tool configuration .yaml file using the following steps:

1. Perform any setup steps that might be required. See the article for the tool you’re interested in using. For example, [Grounding with Bing search](/azure/ai-services/agents/how-to/tools/bing-grounding?tabs=python&pivots=overview#setup).

1. Once you complete the setup, create a yaml code file that specifies the tool’s configuration. For example, this format for Grounding with Bing Search:

    ```yml
    type: bing_grounding
    name: bing_search
    configuration:
      tool_connections:
        - >-
          /subscriptions/<Azure Subscription ID>/resourceGroups/<Azure Resource Group name>/providers/Microsoft.MachineLearningServices/workspaces/<Azure AI Foundry Project name>/connections/<Bing connection name>
    ```
1. Replace the placeholders in the connection string under the `tool_connections` section with your information: 
    
    - Azure Subscription ID
    - Azure Resource Group name
    - Azure AI Foundry Project name
    - Bing connection name

1. Save the .yaml file.

#### Add the tool to the AI Agent

Add a tool to the AI Agent with the following steps:

1. Select the **+** (plus) icon next to the **TOOL** section in the designer.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-tool-plus.png" alt-text="Screenshot of the Agent designer TOOL section with the plus icon highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-tool-plus.png":::

1. In the file explorer that appears, select the .yaml tool file to use. Select the **Select a tool file** button to add the tool to the agent.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-select-tool-file.png" alt-text="Screenshot of the file explorer with the selected file and the 'Select a tool file' button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-select-tool-file.png":::

1. The tool is displayed in the **TOOL** section. 

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-added-tool.png" alt-text="Screenshot of the Agent designer TOOL section with the new tool highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-added-tool.png":::

1. Select the **Save locally** button in the bottom-center of the **Agent Preferences** screen to store your agent configuration. 

###	Deploy Azure AI Agents to the Azure AI Foundry Studio

Deploy your agent directly to Azure AI Foundry with the following steps:

1.  Select the **Deploy to Azure AI Foundry** button in the bottom-left of the designer.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deploy.png" alt-text="Screenshot of the Agent designer with the 'Deploy to Azure AI Foundry' button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deploy.png":::

1. In the VS Code navbar, refresh the **Azure Resources** view. The deployed agent is displayed under the **Agents** subsection.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-deployed.png" alt-text="Screenshot of the 'Azure Resources' view. The deployed agent is highlighted under the 'Agents' subsection." lightbox="../../media/how-to/get-started-projects-vs-code/agent-deployed.png":::

#### View the deployed AI Agent details

Selecting the deployed agent opens the **Agent Preferences** page in a view only mode.  

- Select the **Open Yaml File** to view the yaml definition of the agent. 

- Select the **Open Playground** button to open the **Agent Playground**.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png" alt-text="Screenshot of the Agent Preferences page with the 'Open Yaml File' and 'Open Playground' buttons highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/deployed-agent-view.png":::


### Interact with Agents using agents playground

Open the **Agents Playground** using the following steps:

1. Right-click on your deployed agent and select the **Open Playground** option This action starts a thread with your agent and let you send messages.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-open-playground.png" alt-text="Screenshot of the agent context menu with the 'Open Playground' option highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/agent-open-playground.png":::

1. The **Playground** page is displayed.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/agent-display-playground.png" alt-text="Screenshot of the **Agents Playground** page in VS Code." lightbox="../../media/how-to/get-started-projects-vs-code/agent-display-playground.png":::

1. Type your prompt and see the outputs. 

## Clean up resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your agents

Delete the deployed agent in the [online AI Foundry portal](https://ai.azure.com). Select **Agents** from the navigation menu on the left, select your agent, then select the **Delete** button.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/delete-agent.png" alt-text="Screenshot of the AI Foundry portal with 'Agents' from the navigation menu on the left and the **Delete** button highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/delete-agent.png":::

### Delete your models

1. In the VS Code navbar, refresh the **Azure Resources** view. Expand the **Models** subsection to display the list of deployed models.

1. Right-click on your deployed model to delete and select the **Delete** option.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/delete-model.png" alt-text="Screenshot of the model context menu with the 'Delete' option highlighted." lightbox="../../media/how-to/get-started-projects-vs-code/delete-model.png":::

### Delete your tools

Delete the connected tool with the following steps:

1. Open the Azure portal
1. Select the Azure Resource Group containing the tool.
1. Select the **Delete** button.  

##	Next steps

- Learn about the tools you can use with Azure AI Agents, such as [file search](/azure/ai-services/agents/how-to/tools/file-search?tabs=python&pivots=overview), or [code interpreter](/azure/ai-services/agents/how-to/tools/code-interpreter?tabs=python&pivots=overview).