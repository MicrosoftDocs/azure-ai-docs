---
title: "Tutorial: Deploy an enterprise chat web app in the Azure AI Foundry portal playground"
titleSuffix: Azure AI Foundry
description: Use this article to deploy an enterprise chat web app in the Azure AI Foundry portal playground.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: tutorial
ms.date: 12/27/2024
ms.reviewer: tgokal
ms.author: sgilley
author: sdgilley
# customer intent: As a developer, I want to deploy an enterprise chat web app in the Azure AI Foundry portal playground so that I can use my own data with a large language model.
---

# Tutorial: Deploy an enterprise chat web app

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you deploy an enterprise chat web app that uses your own data with a large language model in Azure AI Foundry portal.

Your data source is used to help ground the model with specific data. Grounding means that the model uses your data to help it understand the context of your question. You're not changing the deployed model itself. Your data is stored separately and securely in your original data source

The steps in this tutorial are:

1. Deploy and test a chat model without your data.
1. Add your data.
1. Test the model with your data.
1. Deploy your web app.

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- A [deployed Azure OpenAI](../how-to/deploy-models-openai.md) chat model. Complete the [Azure AI Foundry playground quickstart](../quickstarts/get-started-playground.md) to create this resource if you haven't already.

- An Azure AI Search service connection to index the sample product data.  If you don't have one, follow the steps to [create](copilot-sdk-create-resources.md#create-search) and [connect](copilot-sdk-create-resources.md#connect-search) a search service.

- A local copy of product data. The [Azure-Samples/rag-data-openai-python-promptflow repository on GitHub](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/) contains sample retail product information that's relevant for this tutorial scenario. Specifically, the `product_info_11.md` file contains product information about the TrailWalker hiking shoes that's relevant for this tutorial example. [Download the example Contoso Trek retail product data in a ZIP file](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/raw/refs/heads/main/tutorial/data/product-info.zip) to your local machine.

- A **Microsoft.Web** resource provider registered in the selected subscription, to be able to deploy to a web app. For more information on registering a resource provide, see [Register resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1).

- Necessary permissions to add role assignments in your Azure subscription. 

## Configure resources

> [!IMPORTANT]
> You must have the necessary permissions to add role assignments in your Azure subscription. Granting permissions by role assignment is only allowed by the Owner of the specific Azure resources. You might need to ask your Azure subscription owner (who might be your IT admin) to complete this section for you.

In order for the resources you're about to deploy to work correctly, you need to configure them with the correct permissions. This work is done in the Azure portal.  

To start, find the resources you need to configure in the Azure AI Foundry portal.

1. Open the [Azure AI Foundry portal](https://ai.azure.com) and select the project where you deployed the Azure OpenAI model.
1. Select **Management center** from the left pane.
1. Select **Connected resources** under your project.
1. Identify the three resources you need to configure: the **Azure AI Search service**, the **Azure OpenAI service**, and the **Azure Blob storage** for your workspaceblobstore.

    :::image type="content" source="../media/tutorials/deploy-chat-web-app/resources.png" alt-text="Screenshot shows the connected resources that need to be configured.":::

1. For each resource, select the link to open the resource details.  From the details page, select the resource name to open the resource in the Azure portal.  (For the workspaceblobstore, select **View in Azure Portal**). 
1. After the tab opens, go back to the Azure AI Foundry portal and repeat the process for the next resource. 
1. Keep all three new tabs open as you'll go back and forth between them to configure the resources.

### Enable managed identity

Both the **Azure AI Search service** and the **Azure OpenAI service** need managed identity enabled.  For each of these two resources, follow these steps in their respective Azure portal pages:

1. From the left pane, under **Settings**, select **Identity**.
1. Switch **Status** to **On**.
1. Select **Save**.

### Set access control for search

On the tab for the **Azure AI Search service** resource in the Azure portal, set the API Access policy:

1. From the left pane, under **Settings**, select **Keys**.
1. Under **API Access control**, select **Both**.
1. When prompted, select **Yes** to confirm the change.

### Assign roles

You'll repeat this pattern multiple times in the bulleted items below.

[!INCLUDE [Assign RBAC](../includes/assign-rbac.md)]

Use these steps to assign roles for the resources you're configuring in this tutorial:

* Assign the following roles on the tab for **Azure AI Search service** in the Azure portal:
    * **Search Index Data Reader** to the **Azure OpenAI service** managed identity
    * **Search Service Contributor** to the **Azure OpenAI service** managed identity
    * **Contributor** to yourself (to find **Contributor**, switch to the **Privileged administrator roles** tab at the top.  All other roles are in the **Job function roles** tab.)

* Assign the following roles on the tab for **Azure OpenAI service** in the Azure portal:

    * **Cognitive Services OpenAI Contributor** to the **Azure AI Search service** managed identity
    * **Contributor** to yourself.

* Assign the following roles on the tab for **Azure Blob storage** in the Azure portal:

    * **Storage Blob Data Contributor** to the **Azure OpenAI service** managed identity
    * **Storage Blob Data Reader** to the **Azure AI Search service** managed identity
    * **Contributor** to yourself

## Add your data and try the chat model again

In the [Azure AI Foundry playground quickstart](../quickstarts/get-started-playground.md) (that's a prerequisite for this tutorial), observe how your model responds without your data. Now add your data to the model to help it answer questions about your products.

[!INCLUDE [Chat with your data](../includes/chat-with-data.md)] 

## Deploy your web app

Once you're satisfied with the experience in Azure AI Foundry portal, you can deploy the model as a standalone web application. 

### Find your resource group in the Azure portal

In this tutorial, your web app is deployed to the same resource group as your [Azure AI Foundry hub](../how-to/create-secure-ai-hub.md). Later you configure authentication for the web app in the Azure portal.

Follow these steps to navigate from Azure AI Foundry to your resource group in the Azure portal:

1. Go to your project in [Azure AI Foundry](https://ai.azure.com). Then select **Management center** from the left pane.
1. Under the **Project** heading, select **Overview**.
1. Select the resource group name to open the resource group in the Azure portal. In this example, the resource group is named `rg-contoso`.

    :::image type="content" source="../media/tutorials/chat/resource-group-manage-page.png" alt-text="Screenshot of the resource group in the Azure AI Foundry portal." lightbox="../media/tutorials/chat/resource-group-manage-page.png":::

1. You should now be in the Azure portal, viewing the contents of the resource group where you deployed the hub. Keep this page open in a browser tab. You return to it later.

### Deploy the web app

Publishing creates an Azure App Service in your subscription. It might incur costs depending on the [pricing plan](https://azure.microsoft.com/pricing/details/app-service/windows/) you select. When you're done with your app, you can delete it from the Azure portal.

To deploy the web app:

> [!NOTE]
> You need to have **Microsoft.Web** resource provider registered in the selected subscription, to be able to deploy to a web app.

1. Complete the steps in the previous section to [add your data](#add-your-data-and-try-the-chat-model-again) to the playground. 

    > [!NOTE]
    > You can deploy a web app with or without your own data, but at least you need a deployed model as described in the [Azure AI Foundry playground quickstart](../quickstarts/get-started-playground.md).

1. Select **Deploy > ...as a web app**.

    :::image type="content" source="../media/tutorials/chat/deploy-web-app.png" alt-text="Screenshot of the deploy new web app button." lightbox="../media/tutorials/chat/deploy-web-app.png":::

1. On the **Deploy to a web app** page, enter the following details:
    - **Name**: A unique name for your web app.
    - **Subscription**: Your Azure subscription.
    - **Resource group**: Select a resource group in which to deploy the web app. You can use the same resource group as the hub.
    - **Location**: Select a location in which to deploy the web app. You can use the same location as the hub.
    - **Pricing plan**: Choose a pricing plan for the web app.
    - **Enable chat history in the web app**: For the tutorial, the chat history box isn't selected. If you enable the feature, your users have access to their individual previous queries and responses. For more information, see [chat history remarks](#understand-chat-history).

1. Select **Deploy**.

1. Wait for the app to be deployed, which might take a few minutes. 

1. When it's ready, the **Launch** button is enabled on the toolbar. But don't launch the app yet and don't close the chat playground page - you return to it later.

### Configure web app authentication

By default, the web app is only accessible to you. In this tutorial, you add authentication to restrict access to the app to members of your Azure tenant. Users are asked to sign in with their Microsoft Entra account to be able to access your app. You can follow a similar process to add another identity provider if you prefer. The app doesn't use the user's sign in information in any other way other than verifying they're a member of your tenant.

1. Return to the browser tab containing the Azure portal (or reopen the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the hub and web app (you might need to refresh the view the see the web app).

1. Select the **App Service** resource from the list of resources in the resource group.

1. From the collapsible left menu under **Settings**, select **Authentication**. 

    :::image type="content" source="../media/tutorials/chat/azure-portal-app-service.png" alt-text="Screenshot of web app authentication menu item under settings in the Azure portal." lightbox="../media/tutorials/chat/azure-portal-app-service.png":::

1. If you see **Microsoft** listed an Identity provider on this page, you can skip the next step.
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

1. Wait 10 minutes or so for the authentication settings to take effect.
1. Return to the browser tab containing the chat playground page in Azure AI Foundry portal.
1. Select **Launch** to launch the deployed web app. If prompted, accept the permissions request.

    *If the authentication settings haven't yet taken effect, close the browser tab for your web app and return to the chat playground in Azure AI Foundry portal. Then wait a little longer and try again.*

1. In your web app, you can ask the same question as before ("How much are the TrailWalker hiking shoes"), and this time it uses information from your data to construct the response. You can expand the **reference** button to see the data that was used.

   :::image type="content" source="../media/tutorials/chat/chat-with-data-web-app.png" alt-text="Screenshot of the chat experience via the deployed web app." lightbox="../media/tutorials/chat/chat-with-data-web-app.png":::

## Understand chat history

With the chat history feature, your users have access to their individual previous queries and responses.

You can enable chat history when you [deploy the web app](#deploy-the-web-app). Select the **Enable chat history in the web app** checkbox.

:::image type="content" source="../media/tutorials/chat/deploy-web-app-chat-history.png" alt-text="Screenshot of the option to enable chat history when deploying a web app." lightbox="../media/tutorials/chat/deploy-web-app-chat-history.png":::

> [!IMPORTANT]
> Enabling chat history will create a [Cosmos DB instance](/azure/cosmos-db/introduction) in your resource group, and incur [additional charges](https://azure.microsoft.com/pricing/details/cosmos-db/autoscale-provisioned/) for the storage used.
> Deleting your web app does not delete your Cosmos DB instance automatically. To delete your Cosmos DB instance, along with all stored chats, you need to navigate to the associated resource in the Azure portal and delete it.

Once you enable chat history, your users are able to show and hide it in the top right corner of the app. When the history is shown, they can rename, or delete conversations. As they're logged into the app, conversations are automatically ordered from newest to oldest, and named based on the first query in the conversation.

If you delete the Cosmos DB resource but keep the chat history option enabled on the studio, your users are notified of a connection error, but can continue to use the web app without access to the chat history.

## Update the web app

Use the playground to add more data or test the model with different scenarios. When you're ready to update the web app with the new model, select **Deploy > ...as a web app** again. Select **updat an existing web app** and choose the existing web app from the list. The new model deploys to the existing web app.

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this quickstart if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

## Related content

- [Get started building a chat app using the prompt flow SDK](../quickstarts/get-started-code.md)
- [Build a custom chat app with the Azure AI SDK.](./copilot-sdk-create-resources.md).
