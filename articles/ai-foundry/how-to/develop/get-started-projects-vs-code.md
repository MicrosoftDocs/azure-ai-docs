---
title: Work with the Microsoft Foundry for Visual Studio Code extension
titleSuffix: Microsoft Foundry
description: Create projects, deploy models from the model catalog, and interact with model playgrounds using the Microsoft Foundry for Visual Studio Code extension.
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

# customer intent: As an AI app developer, I want to learn how to use the Microsoft Foundry for Visual Studio Code extension so that I can create projects and deploy models using Microsoft Foundry capabilities directly in VS Code.
---

# Work with the Microsoft Foundry for Visual Studio Code extension

In this article, learn how to install and use the [Microsoft Foundry](../../what-is-foundry.md) for Visual Studio Code extension. Create projects, deploy models from the Foundry model catalog, and interact with model playgrounds from within VS Code.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]


## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- [Visual Studio Code](https://code.visualstudio.com/Download) installed.
- Your subscription needs to be below your [quota limit](../quota.md) to [deploy a new model in this article](#deploy-a-model-from-the-model-catalog). If you already reached your quota limit, you need to have a [deployed chat model](../../foundry-models/how-to/deploy-foundry-models.md).
- Appropriate RBAC permissions to create and manage Foundry resources. For more information, see [Role-based access control for Foundry](../../concepts/rbac-foundry.md).

## Install the extension

To use Foundry capabilities in VS Code, install the Foundry for Visual Studio Code extension. Install from the Visual Studio Code Marketplace or directly from within VS Code.

### Install from the Visual Studio Code Marketplace

Use the marketplace to install the extension without opening VS Code first.

1. Open the [Foundry for Visual Studio Code extension page](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).
1. Select the **Install** button.
1. Follow the prompts to install the extension in Visual Studio Code.
1. After installation, open Visual Studio Code and verify the extension is installed successfully from the status messages.
1. The Foundry icon appears in the primary navigation bar on the left side of VS Code.

### Install from within Visual Studio Code

Alternatively, search for the extension directly from the VS Code extensions view.

1. Open VS Code.

1. Select **Extensions** from the left pane.

1. Select the **Settings** icon from the top-right on the extensions pane.

1. Search for and select **Foundry**.

1. Select **Install**.

1. After installation completes, a status message confirms the extension is installed. The Foundry icon appears in the left navigation bar.

## Connect to your Azure resources

After you install the extension, sign in to your Azure subscription and open a Foundry project to begin working with models, agents, and playgrounds.

> [!NOTE]
> For a full list of features available in the extension, use the Command Palette. Select <kbd>F1</kbd> to open the command palette and search **Foundry**. The following screenshot shows some of the available commands.
>     :::image type="content" source="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png" alt-text="Screenshot of the VS Code command palette showing available Foundry commands such as Open Model Catalog and Open Playground." lightbox="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png":::

### Sign in to your resources

Sign in to your Azure subscription so the extension can access your Foundry projects and deployed models.

1. Select the Azure icon on the VS Code navigation bar.

1. Select **Sign in to Azure...** in the **Azure Resources** view.

1. Under the **Resources** section, select your Azure subscription and resource group.

1. Select **Foundry** and right-click your project.

1. Select **Open in Foundry Extension**.

    Your Foundry project resources appear in the extension view, and the Foundry icon displays on the VS Code navigation bar.

### Navigate the extension interface

The Foundry extension organizes your workspace into three main sections.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/initial-view.png" alt-text="Screenshot of the Foundry extension interface showing the Resources, Tools, and Help and Feedback sections.":::

| Section | What it contains | When to use it |
| ------- | --------------- | -------------- |
| **Resources** | Deployed models, declarative agents, hosted agents, connections, and vector stores for your Foundry project. | View and manage your project resources. |
| **Tools** | Model Catalog, Model Playground, Agent Playgrounds (remote and local), Local Visualizer, and Deploy Hosted Agents. | Deploy new models, test prompts, and interact with agents. |
| **Help and Feedback** | Documentation, GitHub repository, Microsoft Privacy Statement, and community links. | Get help or provide feedback. |

> [!NOTE]
> To learn more about working with agents in the Foundry extension, see [Work with Agent Service in Visual Studio Code](./vs-code-agents.md).

## Create a project

Create a new Foundry project directly from the extension to organize your models and resources.

1. Select the **plus** icon next to **Resources** in the **Resources** section of the Foundry extension view.

    You can either create a new resource group or select an existing one.
1. To create a new resource group:
    1. Select **Create new resource group** and press Enter.

    1. Enter the Azure resource group name in the **Enter new resource group** textbox and press Enter.

    1. Select the location you want to use from the list of available locations and press Enter.

1. To use an existing resource group:
    - Select the resource group you want to use from the list of available resource groups and press Enter.

1. Enter the Foundry project name in the **Enter project name** textbox and press Enter.

After project deployment, a popup appears with the message **Project deployed successfully**.

To deploy a model to the newly created project, select the **Deploy a model** button in the popup. This action opens the **Model Catalog** page where you can select the desired model to [deploy](#deploy-a-model-from-the-model-catalog).

### Switch the default project

When you open a project in the Foundry extension, that project is set as your default project. To switch your default project:

1. Right-click on the Foundry project and select the **Switch Default Project in Azure Extension** option.

1. Select the Foundry project you want to use from the list of available projects and press Enter.

The selected project now displays **Default** after the project name.

> [!TIP]
> Right-click on your project name to access the project endpoint or the project API key.

## Work with models

The Foundry extension lets you discover, deploy, and interact with models from the [Foundry model catalog](../../concepts/foundry-models-overview.md) directly in VS Code.

### Browse the model catalog

The model catalog provides access to models from Microsoft, OpenAI, Meta, DeepSeek, and other providers. You can open the model catalog in several ways:

- Run the **Foundry: Open Model Catalog** command from the command palette.
- Select the **plus** icon next to **Models** in the **Resources** section of the Foundry extension view.
- Select the **Model Catalog** link in the **Tools** section of the Foundry extension view.

#### Open the model catalog from the command palette

Use the command palette to open the model catalog without navigating the extension view.

1. Select <kbd>F1</kbd> to open the command palette.

1. Enter **Foundry: Open Model Catalog** and press Enter.

1. The **Model Catalog** page opens.

    :::image type="content" source="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png" alt-text="Screenshot of the Model Catalog page in VS Code showing model cards with filters for publisher and model type." lightbox="../../media/how-to/get-started-projects-vs-code/display-model-catalog.png":::

1. Filter the **Model Catalog** by **Hosted by**, **Publisher**, **Feature**, or **Model type** using the dropdowns at the top of the page. Select the **Fine-Tuning Support** toggle to filter models that support fine-tuning.

1. Search for a specific model using the search bar at the top-center of the page.

#### Open the model catalog from the Resources section

In the Foundry extension view, select the **plus** icon next to **Models** to open the model catalog.

> [!TIP]
> You can also right-click on **Models** and select **Deploy new AI model** to go directly to the deployment flow.

#### Open the model catalog from the Tools section

In the **Tools** section of the Foundry extension view, double-click the **Model Catalog** link.

### Deploy a model from the model catalog

After you find a model in the catalog, deploy it to your Foundry project so you can use it in your applications.

1. Select the **Deploy** button next to the selected model name.

1. The **Model deployment** page opens.

1. Enter the model deployment name in the **Enter deployment name** textbox and press Enter.

1. Select the deployment type in the **Deployment type** dropdown.

1. Select the model version in the **Model version** dropdown.

1. (Optional) Adjust the tokens per minute using the **Tokens per minute** slider.

1. Select the **Deploy in Foundry** button in the bottom-left corner.

1. In the confirmation dialog, select **Deploy**.

1. After deployment completes, the model appears by deployment name under the **Models** section in your project.

### View and manage deployed models

Expand the **Models** section in the Foundry extension view to see all deployed models in your project.

#### View model card information

Select a deployed model to open a panel with the following details:

- **Deployment Info**: Name, provisioning state, deployment type, rate limit, version info, model name, and model version.
- **Endpoint info**: Target URI link, authentication type, and key.
- **Useful links**: Code sample repository and tutorial links for AI application development.

#### Update model deployment settings

To update deployment settings such as rate limits:

1. Select the **Edit** button on the top-right of the model card.
1. Update the editable fields.
1. Select the **Save** button to apply the changes.

### Generate sample code for a model

Generate a starter code file for your deployed model to accelerate application development.

1. Right-click on your deployed model and select **Open code file**.

1. Select your preferred SDK in the **Choose preferred SDK** dropdown.

1. Select your preferred language in the **Choose language** dropdown.

1. Select your preferred authentication method in the **Choose authentication method** dropdown.

1. A sample code file opens in a new tab in VS Code.

The following screenshot shows a generated Python sample that makes a synchronous call to the responses API:

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/sample-code-file.png" alt-text="Screenshot of a generated Python sample code file showing a synchronous responses API call in VS Code." lightbox="../../media/how-to/get-started-projects-vs-code/sample-code-file.png":::

### Interact with models in the playground

Use the model playground to chat interactively with your deployed model, adjust settings, and modify system instructions.

To open the playground, double-click the **Model Playground** link in the **Tools** section of the Foundry extension view. Alternatively, right-click on your deployed model and select **Open in playground**.

1. The **Playground** page opens.

1. Type your prompt and review the output.

1. Select **View code** in the top-right corner to see how to access the model deployment programmatically.

1. Select the **History** link at the top-left of the playground to view your chat history.

## Troubleshoot common issues

If you run into problems while using the Foundry extension, check the following common issues:

| Issue | Resolution |
| ----- | ---------- |
| Extension doesn't appear after installation | Restart VS Code and verify the extension is enabled in the **Extensions** view. |
| Sign-in fails or subscriptions don't load | Verify your Azure account has the correct permissions. Try signing out and signing in again from the **Azure Resources** view. |
| Model deployment fails with a quota error | Check your [subscription quota](../quota.md) and either request an increase or delete unused deployments. |

## Clean up resources

The Azure resources that you created in this article are billed to your Azure subscription. If you don't expect to need these resources in the future, delete them to avoid incurring more charges.

### Delete your models

1. In the VS Code navigation bar, refresh the Foundry extension. In the **Resources** section, expand the **Models** subsection.

1. Right-click the deployed model you want to remove and select **Delete**.

### Delete Azure resources

To delete the resource group and all resources within, it:

> [!WARNING]
> Deleting a resource group permanently removes all resources within it, including your Foundry project and any deployed models. This action can't be undone.

1. Open the [Azure portal](https://portal.azure.com).
1. Navigate to the resource group that contains your Foundry project.
1. Select **Delete resource group** and confirm the deletion.

## Next steps

- [Work with Agent Service in Visual Studio Code](./vs-code-agents.md)
- [Explore Foundry models](../../concepts/foundry-models-overview.md)
- [Deploy models with Foundry](../../foundry-models/how-to/deploy-foundry-models.md)
