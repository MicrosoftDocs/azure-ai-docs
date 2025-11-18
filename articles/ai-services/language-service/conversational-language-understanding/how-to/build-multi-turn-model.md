---
title: Build multi-turn conversational language understanding (CLU) models with entity slot filling
titleSuffix: Foundry Tools
description: This article shows you how to create a CLU model for multi-turn interactions using slot-filling
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/05/2025
ms.author: lajanuar
ms.custom: language-service-clu
---

# Build multi-turn CLU models with entity slot filling

In this article, learn how to build a CLU model that implements entity slot filling to facilitate multi-turn conversations. With this approach, your model can incrementally collect the required information across multiple conversation turns. Users don't need to provide all the details in a single interaction. As a result, you can complete tasks more naturally and efficiently.

## Prerequisites

* **Azure subscription** - If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* **Required permissions** - Ensure that the person establishing the account and project has the Azure AI Account Owner role at the subscription level. Alternatively, the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, see [Role based access control (RBAC)](/azure/ai-foundry/openai/how-to/role-based-access-control#cognitive-services-contributor).

* **Azure Language in Foundry Tools resource** - Create a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics) in the Azure portal.

     > [!NOTE]
     > You need the **owner** role assigned on the **resource group** to create a Language resource.

* **Microsoft Foundry project** - Create a project in Foundry. For more information, see [Create a Foundry project](/azure/ai-foundry/how-to/create-projects).

* **Deployed OpenAI model** - Deploy an OpenAI model in Foundry as described in the [Deploy an OpenAI model](#deploy-an-openai-model-in-foundry) section.

## Configure required roles, permissions, and settings

Begin by configuring your Azure resources with the appropriate roles and permissions.

### Add required roles for your Language resource

1. Navigate to your Language resource page in the [Azure portal](https://portal.azure.com/) and select **Access Control (IAM)** from the left navigation pane.

1. Select **Add** > **Add Role Assignments**, and assign either the **Cognitive Services Language Owner** or **Cognitive Services Contributor** role for your Language resource.

1. Under **Assign access to**, select **User, group, or service principal**.

1. Select **Select members**.

1. Choose your user name from the list. You can search for user names in the **Select** field. Repeat this step for all required roles.

1. Repeat these steps for all user accounts that require access to this resource.

## Connect your Azure Language resource to Foundry

To enable secure access, create a connection between your Language resource and Foundry. This connection provides secure identity management, authentication, and controlled access to your data.

  > [!NOTE]
  > The multi-turn capability is currently only available in the Foundry (classic) portal.

1. Navigate to [Foundry (classic)](https://ai.azure.com/).

1. Access your existing Foundry project for this tutorial.

1. Select **Management center** from the left navigation menu.

1. Select **Connected resources** from the **Hub** section of the **Management center** menu.

1. In the main window, select **+ New connection**.

1. Select **Language** from the **Add a connection to external assets** window.

1. Select **Add connection**, then select **Close**.

    :::image type="content" source="../media/add-connection.png" alt-text="Screenshot of the connection window in Foundry.":::

## Deploy an OpenAI model in Foundry

Deploy an OpenAI model to provide the foundational intelligence and advanced reasoning capabilities for your CLU model.

1. Select **Models + endpoints** from the **My assets** section of the navigation menu.

   :::image type="content" source="../media/models-endpoints.png" alt-text="Screenshot of the deploy model button menu in Foundry.":::

1. From the main window, select **+ Deploy model**.

1. Select **Deploy base model** from the dropdown menu.

   :::image type="content" source="../media/deploy-model-button.png" alt-text="Screenshot of the connected resources menu selection in Foundry.":::

1. In the **Select a model** window, choose a model. The **gpt-4** base model is recommended for this project.

   :::image type="content" source="../media/gpt-4-selection.png" alt-text="Screenshot of the select a model selection in Foundry.":::

1. Select **Confirm**.

1. In the **Deploy gpt-4** window, retain the default values and select **Deploy**.

   :::image type="content" source="../media/deploy-gpt-4.png" alt-text="Screenshot of the gpt-4 deployment window in Foundry.":::

1. The model deployment is now complete.

## Build your multi-turn model

Now that your Language resource, Foundry project, and OpenAI deployment are configured, you're ready to build your CLU model.

### Create a CLU project

In this section, you create a travel agent model and deploy it using Quick Deploy.

1. Navigate to [Foundry (classic)](https://ai.azure.com).

1. If you aren't already signed in, the portal prompts you to authenticate with your Azure credentials.

1. Once signed in, create or access your existing projects within Foundry.

1. If you're not already in your project for this task, select it.

1. In the left navigation pane **Overview** section, select **Fine-tuning**.

1. From the main window, select the **AI Service fine-tuning** tab, then select **+ Fine-tune**.

1. In the **Create service fine-tuning** window, choose the **Conversational language understanding** tab, then select **Next**.

1. In the **Create CLU fine-tuning task** window, complete the following fields:

   * **Connected service** - The name of your language service resource should appear by default. If not, select it from the dropdown menu.
   * **Name** - Provide a name for your fine-tuning task project.
   * **Language** - English is set as the default and should already appear in the field.
   * **Description** - Optionally provide a description or leave this field empty.

1. Select **Create**. The creation operation may take a few minutes to complete.

### Add intents

1. From the **Getting Started** menu, select **Define schema**.

1. In the main window, select **Add Intent**.

1. The **Add Intent** window contains two required fields:
   * Intent name(Pascal case)
   * Intent description (required for Quick Deploy)

1. After completing these fields, select **+ Add** to create your intents.

1. After defining all intents, select **Add Intent**.

### Add entities

1. Select the **Entities** tab, then select **Add entity**.

1. The **Add an entity** window contains two required fields:
   * Entity name (Pascal case)|
   * Entity description
1. After completing the entity fields, select **Add an entity**.

### Associate intents with entities

1. Select the **Associations** tab.

1. Select each intent and link it to the required entities from the **Available entities** section. This step ensures the model knows which slots to fill for each intent.

1. All entities must have an association with at least one intent. After configuring the associations, select **Update associations**.

Once all entities have associations, you can proceed with Quick Deploy using a large language model (LLM).

### Quick deploy with LLM

1. From the **Getting Started** menu, select **Train model**.

1. In the **Train your model** section, select **Quick deploy with LLM**.

1. Complete the **Quick deploy with LLM** window fields:

   * **Deployment name** - Provide a name for the deployment.
   * **Select Azure OpenAI Model Deployment** - Choose the Azure OpenAI model deployment you created for this project.
   * **Deployment regions** - Select the region associated with your Azure Language resource.

1. Select **Create**. Foundry manages the configuration and deployment processes through backend operations.

### Test in playground

1. From the **Getting Started** menu, select **Deploy your model**.

1. In the main window, select your model.

1. Select **Try in playground**.

1. In the playground, select the **Conversational language understanding** tile.

1. Under the **Configuration** menu on the left, verify that the following fields are completed correctly:
   * **Project name** - Ensure this matches the project you created for this CLU fine-tuning task.
   * **Deployment name** - Verify this matches the name you assigned to your OpenAI model.

1. Select the **Multi-turn** understanding checkbox.

1. Simulate a multi-turn dialog by entering a conversation.

1. Select **Run**.

1. The model returns a response in both **Text** and **JSON** formats.


1. In the **Details** panel on the right, review the **Top Intent** and detected **Entities**.

    :::image type="content" source="../media/multi-turn/details.png" alt-text="Screenshot of the Details response window.":::

That's it! You successfully created a multi-turn CLU model with entity slot filling capabilities to collect required information across multiple dialog turns.

## Clean up resources

To clean up and remove an Azure AI resource, delete either the individual resource or the entire resource group. Deleting the resource group removes all contained resources.

## Related content

[Learn how CLU handles entity slot-filling across multi-turn conversations](../concepts/multi-turn-conversations.md)
