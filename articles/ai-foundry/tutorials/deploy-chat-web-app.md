---
title: "Tutorial: Deploy an enterprise chat web app in the Microsoft Foundry portal playground"
titleSuffix: Microsoft Foundry
description: Use this article to deploy an enterprise chat web app in the Microsoft Foundry portal playground.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ms.topic: tutorial
ms.date: 08/25/2025
ms.reviewer: tgokal
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
# customer intent: As a developer, I want to deploy an enterprise chat web app in the Microsoft Foundry portal playground so that I can use my own data with a large language model.
---

# Tutorial: Deploy an enterprise chat web app

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In this article, you deploy an enterprise chat web app that uses your data with a large language model in Microsoft Foundry portal.

Your data source grounds the model with specific data. Grounding means the model uses your data to understand the context of your question. You don't change the deployed model itself. Your data stays separate and secure in your original data source.

The steps in this tutorial are:

> [!div class="checklist"]
> * Configure resources.
> * Add your data.
> * Test the model with your data.
> * Deploy your web app.

## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

- A [deployed Azure OpenAI](../foundry-models/how-to/deploy-foundry-models.md) chat model. Finish the [Foundry playground quickstart](../quickstarts/get-started-playground.md) to create this resource if you don't have one.

- A Search service connection to index the sample product data. If you don't have one, follow the steps to [create](copilot-sdk-create-resources.md#create-an-azure-ai-search-service) and [connect](copilot-sdk-create-resources.md#connect-the-azure-ai-search-to-your-project) a search service.

- A local copy of product data. The [Azure-Samples/rag-data-openai-python-promptflow repository on GitHub](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/) has sample retail product information for this tutorial scenario. The `product_info_11.md` file has product information about the TrailWalker hiking shoes for this tutorial example. [Download the example Contoso Trek retail product data in a ZIP file](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/raw/refs/heads/main/tutorial/data/product-info.zip) to your local machine.

- A **Microsoft.Web** resource provider registered in the selected subscription so you can deploy to a web app. For more information on registering a resource provider, see [Register resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1).

- Necessary permissions to add role assignments in your Azure subscription. Only the Owner of the specific Azure resources can grant permissions by role assignment.

## Foundry portal and Azure portal 

In this tutorial, you perform some tasks in the Foundry portal and some tasks in the Azure portal.

The Foundry portal is a web-based environment for building, training, and deploying AI models. As a developer, it's where you build and deploy your chat web application.

The Azure portal lets an admin manage and monitor Azure resources. As an admin, you use the portal to set up settings for different Azure services required for access from the web app.

## Configure resources

> [!IMPORTANT]
> You must have the necessary permissions to add role assignments in your Azure subscription. Granting permissions by role assignment is only allowed by the Owner of the specific Azure resources. You might need to ask your Azure subscription owner (who might be your IT admin) to complete this section for you.

To make the resources work correctly in a web app, set up the correct permissions in the Azure portal.

First, identify the resources you need to set up in the Foundry portal.

1. Open the [Foundry portal](https://ai.azure.com/?cid=learnDocs), then select the hub-based project you used to deploy the Azure OpenAI chat model.
1. Select **Management center** from the left pane.
1. Select **Connected resources** under your project.
1. Identify the three resources you need to configure:  the **Azure OpenAI**, the **Azure AI Search**, and the **Azure Blob storage** that corresponds to your **workspaceblobstore**.

    :::image type="content" source="../media/tutorials/deploy-chat-web-app/resources.png" alt-text="Screenshot shows the connected resources that need to be configured.":::

    > [!TIP]
    > If you don't see **Type** in the table, select **Columns** in the upper right corner and add to or reorder the **Selected columns**.
    > If you have multiple **Azure OpenAI** resources, use the one that contains your deployed chat model.



1. Search for each of these names in the [Azure portal](https://portal.azure.com). Open each one in a new browser tab so that you can switch between them.
1. When you're done, you have three new browser tabs open: **Search service**, **Foundry**, and **blobstore Container**. Keep all three tabs open because you switch between them to set up the resources.

### Enable managed identity

In the browser tab for the **Search service** resource in the Azure portal, enable managed identity:

1. In the left pane, under **Settings**, select **Identity**.
1. Switch **Status** to **On**.
1. Select **Save**.

In the browser tab for the **Foundry** resource in the Azure portal, enable managed identity:

1. In the left pane, under **Resource Management**, select **Identity**.
1. Switch **Status** to **On**.
1. Select **Save**.

### Set access control for search

In the browser tab for the **Search service** resource in the Azure portal, set the API access policy:

1. In the left pane, under **Settings**, select **Keys**.
1. Under **API Access control**, select **Both**.
1. When prompted, select **Yes** to confirm.

### Assign roles

Repeat this pattern for each resource in the steps below.

[!INCLUDE [Assign RBAC](../includes/assign-rbac.md)]

Use these steps to assign roles for the resources you set up in this tutorial:

* Assign these roles in the browser tab for **Search service** in the Azure portal:
    * **Search Index Data Reader** to the **Foundry** managed identity
    * **Search Service Contributor** to the **Foundry** managed identity
    * **Contributor** to yourself (to find **Contributor**, switch to the **Privileged administrator roles** tab at the top. All other roles are in the **Job function roles** tab.)

* Assign these roles in the browser tab for **Foundry** in the Azure portal:

    * **Cognitive Services OpenAI Contributor** to the **Search service** managed identity
    * **Contributor** to yourself.

* Assign these roles in the browser tab for **Azure Blob storage** in the Azure portal:

    * **Storage Blob Data Contributor** to the **Foundry** managed identity
    * **Storage Blob Data Reader** to the **Search service** managed identity
    * **Contributor** to yourself

You're done setting up resources. You can close the Azure portal browser tabs now if you want.

## Add your data and try the chat model again

In the [Foundry playground quickstart](../quickstarts/get-started-playground.md) (that's a prerequisite for this tutorial), you see how your model responds without your data. Add your data to the model so it can answer questions about your products.

[!INCLUDE [Chat with your data](../includes/chat-with-data.md)]

## Deploy your web app

When you're satisfied with the experience in the Foundry portal, deploy the model as a standalone web application.

### Find your resource group in the Azure portal

In this tutorial, deploy your web app to the same resource group as your [Foundry hub](../how-to/create-secure-ai-hub.md). You'll set up authentication for the web app in the Azure portal.

Follow these steps to go to your resource group in the Azure portal:

1. Go to your project in [Foundry](https://ai.azure.com/?cid=learnDocs). Select **Management center** from the left pane.
1. Under the **Project** heading, select **Overview**.
1. Select the resource group name to open the resource group in the Azure portal. In this example, the resource group is named `rg-sdg-ai`.

    :::image type="content" source="../media/tutorials/chat/resource-group-manage-page.png" alt-text="Screenshot of the resource group in the Foundry portal." lightbox="../media/tutorials/chat/resource-group-manage-page.png":::

1. You're now in the Azure portal, viewing the contents of the resource group where you deployed the hub. Note the resource group name and location. You'll use this information in the next section.
1. Keep this page open in a browser tab. You'll return to it later.

### Deploy the web app

Publishing creates an Azure App Service in your subscription. You might incur costs depending on the [pricing plan](https://azure.microsoft.com/pricing/details/app-service/windows/) you select. When you're done with your app, delete it from the Azure portal.

To deploy the web app:

> [!IMPORTANT]
> Register [**Microsoft.Web** as a resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1) before you deploy to a web app. 

1. Complete the steps in the previous section to [add your data](#add-your-data-and-try-the-chat-model-again) to the playground. You can deploy a web app with or without your own data, but you need a deployed model as described in the [Foundry playground quickstart](../quickstarts/get-started-playground.md).

1. Select **Deploy > ...as a web app**.

    :::image type="content" source="../media/tutorials/chat/deploy-web-app.png" alt-text="Screenshot of the deploy new web app button." lightbox="../media/tutorials/chat/deploy-web-app.png":::

1. On the **Deploy to a web app** page, enter the following details:
    - **Name**: A unique name for your web app.
    - **Subscription**: Your Azure subscription. If you don't see any available subscriptions, first [register **Microsoft.Web** as a resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1).
    - **Resource group**: Select a resource group in which to deploy the web app. Use the same resource group as the hub.
    - **Location**: Select a location in which to deploy the web app. Use the same location as the hub.
    - **Pricing plan**: Choose a pricing plan for the web app.
    - **Enable chat history in the web app**: For the tutorial, the chat history box isn't selected. If you enable the feature, your users have access to their individual previous queries and responses. For more information, see [chat history remarks](#understand-chat-history).

1. Select **Deploy**.

1. Wait for the app to deploy. This process might take a few minutes.

1. When it's ready, the **Launch** button is enabled on the toolbar. Don't launch the app yet, and don't close the chat playground page—you'll return to it later.

### Configure web app authentication

By default, only you can access the web app. In this tutorial, add authentication to restrict access to members of your Azure tenant. Users sign in with their Microsoft Entra account to access your app. You can follow a similar process to add another identity provider if you prefer. The app only uses the user's sign-in information to verify they're a member of your tenant.

1. Return to the browser tab with the Azure portal, or open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab. View the contents of the resource group where you deployed the web app. You might need to refresh the view to see the web app.

1. Select the **App Service** resource from the list of resources in the resource group.

1. From the collapsible left menu under **Settings**, select **Authentication**. 

    :::image type="content" source="../media/tutorials/chat/azure-portal-app-service.png" alt-text="Screenshot of web app authentication menu item under settings in the Azure portal." lightbox="../media/tutorials/chat/azure-portal-app-service.png":::

1. If you see **Microsoft** listed an Identity provider on this page, nothing further is needed.  You can skip the next step.
1. Add an identity provider with the following settings:
    - **Identity provider**: Select Microsoft as the identity provider. The default settings on this page restrict the app to your tenant only, so you don't need to change anything else here.
    - **Tenant type**: Workforce
    - **App registration**: Create a new app registration
    - **Name**: *The name of your web app service*
    - **Supported account types**: Current tenant - Single tenant
    - **Restrict access**: Requires authentication
    - **Unauthenticated requests**: HTTP 302 Found redirect - recommended for websites

### Use the web app

You're almost there. Now you can test the web app.

1. If you changed settings, wait about 10 minutes for the authentication settings to take effect.
1. Return to the browser tab with the chat playground page in the Foundry portal.
1. Select **Launch** to open the deployed web app. If prompted, accept the permissions request.
1. If you don't see **Launch** in the playground, select **Web apps** from the left pane, then select your app from the list to open it.

    *If the authentication settings aren't active yet, close the browser tab for your web app and return to the chat playground in the Foundry portal. Wait a little longer, then try again.*

1. In your web app, ask the same question as before ("How much are the TrailWalker hiking shoes"). This time, the app uses information from your data to construct the response. Expand the **reference** button to see the data used.

   :::image type="content" source="../media/tutorials/chat/chat-with-data-web-app.png" alt-text="Screenshot of the chat experience via the deployed web app." lightbox="../media/tutorials/chat/chat-with-data-web-app.png":::

## Understand chat history

With the chat history feature, your users can see their previous queries and responses.

Enable chat history when you [deploy the web app](#deploy-the-web-app). Select the **Enable chat history in the web app** checkbox.

:::image type="content" source="../media/tutorials/chat/deploy-web-app-chat-history.png" alt-text="Screenshot of the option to enable chat history when deploying a web app." lightbox="../media/tutorials/chat/deploy-web-app-chat-history.png":::

> [!IMPORTANT]
> Enabling chat history creates a [Cosmos DB instance](/azure/cosmos-db/introduction) in your resource group, and incurs [additional charges](https://azure.microsoft.com/pricing/details/cosmos-db/autoscale-provisioned/) for the storage used.
> Deleting your web app doesn't delete your Cosmos DB instance automatically. To delete your Cosmos DB instance and all stored chats, go to the associated resource in the Azure portal and delete it.

After you enable chat history, your users can show or hide it in the top right corner of the app. When the history is shown, they can rename or delete conversations. As they're signed in to the app, conversations are ordered from newest to oldest and named based on the first query in the conversation.

If you delete the Cosmos DB resource but keep the chat history option enabled in the studio, your users see a connection error but can keep using the web app without chat history.

## Update the web app

Use the playground to add more data or test the model with different scenarios. When you're ready to update the web app with the new model, select **Deploy > ...as a web app** again. Select **Update an existing web app**, and choose the existing web app from the list. The new model deploys to the existing web app.

## Clean up resources

To avoid unnecessary Azure costs, delete the resources you created in this quickstart if you don't need them. Manage resources in the [Azure portal](https://portal.azure.com?azure-portal=true).

## Related content

- [Get started building a chat app](../quickstarts/get-started-code.md)
- [Build a custom chat app with the Azure AI SDK](./copilot-sdk-create-resources.md)
