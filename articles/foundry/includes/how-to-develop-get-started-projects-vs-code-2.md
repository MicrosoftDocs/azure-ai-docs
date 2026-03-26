---
title: Include file
description: Include file
author: bobtabor-msft
ms.reviewer: erichen
ms.author: rotabor
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

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

The Foundry extension lets you discover, deploy, and interact with models from the [Foundry model catalog](../../foundry-classic/concepts/foundry-models-overview.md) directly in VS Code.

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

    :::image type="content" source="../media/how-to/get-started-projects-vs-code/display-model-catalog.png" alt-text="Screenshot of the Model Catalog page in VS Code showing model cards with filters for publisher and model type." lightbox="../media/how-to/get-started-projects-vs-code/display-model-catalog.png":::

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

:::image type="content" source="../media/how-to/get-started-projects-vs-code/sample-code-file.png" alt-text="Screenshot of a generated Python sample code file showing a synchronous responses API call in VS Code." lightbox="../media/how-to/get-started-projects-vs-code/sample-code-file.png":::

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
| Model deployment fails with a quota error | Check your [subscription quota](../how-to/quota.md) and either request an increase or delete unused deployments. |

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
