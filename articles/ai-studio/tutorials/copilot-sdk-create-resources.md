---
title: "Part 1: Create resources to build a custom chat application with the prompt flow SDK"
titleSuffix: Azure AI Studio
description:  Learn how to build a RAG-based chat app using the prompt flow SDK. This tutorial is part 1 of a 3-part tutorial series, and shows how to create the resources you'll need for parts 2 and 3.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: tutorial
ms.date: 08/29/2024
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can build a RAG-based chat app.
---

# Tutorial:  Part 1 - Create resources for building a custom chat application with the prompt flow SDK

In this [Azure AI Studio](https://ai.azure.com) tutorial, you use the prompt flow SDK (and other libraries) to build, configure, evaluate, and deploy a chat app for your retail company called Contoso Trek. Your retail company specializes in outdoor camping gear and clothing. The chat app should answer questions about your products and services. For example, the chat app can answer questions such as "which tent is the most waterproof?" or "what is the best sleeping bag for cold weather?".

This tutorial is part one of a three-part tutorial.  This part one shows you how to create and configure the resources you'll need for parts two and three of the tutorials.

In this part one, you learn how to:

> [!div class="checklist"]
> - Create an Azure AI Studio hub
> - Create a project
> - Create an Azure AI Search index
> - Configure access for the Azure AI Studio and Azure AI Search resources

## Prerequisites

* A valid Azure subscription - [Create one for free](https://azure.microsoft.com/free)

> [!IMPORTANT]
> You must have the necessary permissions to add role assignments in your Azure subscription. Granting permissions by role assignment is only allowed by the **Owner** of the specific Azure resources. You might need to ask your Azure subscription owner (who might be your IT admin) to complete this tutorial for you.  

## Azure AI Studio and Azure portal

In this tutorial, you perform some tasks in Azure AI Studio and some tasks in the Azure portal.  

Azure AI Studio is a web-based environment for building, training, and deploying AI models. It's where the developer will build and deploy the chat application.  

The Azure portal allows an administrator to manage and monitor Azure resources.  As an administrator, you'll use the portal to configure settings for various Azure services that the developer will use in parts two and three of this tutorial series.  

## Create an Azure AI Studio hub

[!INCLUDE [Create Azure AI Studio hub](../includes/create-hub.md)]

## Create a project

To create a project in [Azure AI Studio](https://ai.azure.com), follow these steps:

1. Go to the **Home** page of [Azure AI Studio](https://ai.azure.com). 
1. Select **+ New project**.
1. Enter a name for the project.
1. Select the hub you created in the previous step.
1. Select an existing Azure AI services resource (including Azure OpenAI) from the dropdown or create a new one. 

    :::image type="content" source="../media/how-to/projects/projects-create-resource.png" alt-text="Screenshot of the create resource page within the create project dialog." lightbox="../media/how-to/projects/projects-create-resource.png":::

1. On the **Review and finish** page, you see the Azure AI services resource name and other settings to review.

    :::image type="content" source="../media/how-to/projects/projects-create-review-finish.png" alt-text="Screenshot of the review and finish page within the create project dialog." lightbox="../media/how-to/projects/projects-create-review-finish.png":::

1. Review the project details and then select **Create a project**. You see progress of resource creation and the project is created when the process is complete.

    :::image type="content" source="../media/how-to/projects/projects-create-review-finish-progress.png" alt-text="Screenshot of the resource creation progress within the create project dialog." lightbox="../media/how-to/projects/projects-create-review-finish-progress.png":::

Once a project is created, you can access the playground, tools, and other assets in the left navigation panel.

## Create an Azure AI Search index

The goal with this application is to ground the model responses in your custom data. You use an Azure AI Search index that stores vectorized data from the embeddings model. The search index is used to retrieve relevant documents based on the user's question.

You need an Azure AI Search service and connection in order to create a search index.

> [!NOTE]
> Creating an [Azure AI Search service](/azure/search/) and subsequent search indexes has associated costs. You can see details about pricing and pricing tiers for the Azure AI Search service on the creation page, to confirm cost before creating the resource.

### Create an Azure AI Search service

If you already have an Azure AI Search service in the same location as your project, you can skip to the [next section](#create-an-azure-ai-search-connection).

Otherwise, you can create an Azure AI Search service using the [Azure portal](https://portal.azure.com).

> [!IMPORTANT]
> Use the same location as your project for the Azure AI Search service. Find your project's location in the top-right project picker of the Azure AI Studio in the project view.

1. Go to the [Azure portal](https://portal.azure.com).
1. [Create an Azure AI Search service](https://portal.azure.com/#create/Microsoft.Search) in the Azure portal.
1. Select your resource group and instance details. You can see details about pricing and pricing tiers on this page.
1. Continue through the wizard and select **Review + assign** to create the resource.
1. Confirm the details of your Azure AI Search service, including estimated cost.
1. Select **Create** to create the Azure AI Search service.

### Create an Azure AI Search connection

If you already have an Azure AI Search connection in your project, you can skip to [configure access for the Azure AI Search service](#configure). Only use an existing connection if it's in the same location as your project.

In the Azure AI Studio, check for an Azure AI Search connected resource.

1. In [AI Studio](https://ai.azure.com), go to your project and select **Settings** from the left pane.
1. In the **Connected resources** section, look to see if you have a connection of type Azure AI Search.
1. If you have an Azure AI Search connection, verify that it is in the same location as your project. If so, you can skip ahead to [configure access for the Azure AI Search service](#configure).
1. Otherwise, select **New connection** and then **Azure AI Search**.
1. Find your Azure AI Search service in the options and select **Add connection**.
1. Continue through the wizard to create the connection. For more information about adding connections, see [this how-to guide](../how-to/connections-add.md#create-a-new-connection).

## <a name="configure"></a> Configure access

This section shows how to configure the various access controls needed for the resources you created in the previous sections.

We recommend using [Microsoft Entra ID](/entra/fundamentals/whatis) instead of using API keys. In order to use this authentication, you need to set the right access controls and assign the right roles for your services. 

Start in the project to find the AI Services resource:

1. In [AI Studio](https://ai.azure.com), go to your project and select **Settings** from the left pane.
1. Select **Connected resources**.
1. For each resource, select the **AI Services** or **Azure OpenAI** in the connected resources list to open the resource details page.  Then select the Resource name again in the **Connection Details** page, which opens the resource in the Azure portal.

Specify the access control in the Azure portal:

1. From the left page in the Azure portal, select **Access control (IAM)** > **+ Add** > **Add role assignment**.
1. Search for the role **Cognitive Services OpenAI User** and then select it. Then select **Next**.
1. Select **User, group, or service principal**. Then select **Select members**.
1. In the **Select members** pane that opens, search for the name of the user that you want to add the role assignment for. Select the user and then select **Select**.
1. Continue through the wizard and select **Review + assign** to add the role assignment.

Now go back to [AI Studio](https://ai.azure.com) **Settings** > **Connected Resources**.  This time select **Azure AI Search** in the connected resources list to open the resource details page.  Then select the Resource name again in the **Connection Details** page, which opens the resource in the Azure portal.

You'll do two settings in the portal for the Azure AI Search service:

To enable role-based access control for your Azure AI Search service, follow these steps:

1. On your Azure AI Search service in the [Azure portal](https://portal.azure.com), select **Settings > Keys** from the left pane.
1. Select **Both** to ensure that API keys and role-based access control are both enabled for your Azure AI Search service. 

    :::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/search-access-control.png" alt-text="Screenshot shows API Access control setting.":::

> [!WARNING]
> You can use role-based access control locally because you run `az login` later in this tutorial. But when you deploy your app in [part 2 of the tutorial](./copilot-sdk-evaluate-deploy.md), the deployment is authenticated using API keys from your Azure AI Search service. Support for Microsoft Entra ID authentication of the deployment is coming soon.

Next you grant your user identity (or the identity of the developer who will complete parts two and three) the **Search Index Data Contributor** and **Search Service Contributor** roles on the Azure AI Search service. These roles enable you to call the Azure AI Search service the associated user identity.

In the Azure portal, assign the **Search Index Data Contributor** role to your Azure AI Search service, (using the same steps you did previously for the Azure OpenAI service):

1. From the left page in the Azure portal, select **Access control (IAM)** > **+ Add** > **Add role assignment**.
1. Search for the **Search Index Data Contributor** role and then select it. Then select **Next**.
1. Select **User, group, or service principal**. Then select **Select members**.
1. In the **Select members** pane that opens, search for the name of the user that you want to add the role assignment for. Select the user and then select **Select**.
1. Continue through the wizard and select **Review + assign** to add the role assignment. 

Repeat the previous steps to also add the **Search Service Contributor** role to the Azure AI Search service.

You're now ready to hand off the project to a developer to build the chat application.  The developer will use the prompt flow SDK to build, configure, evaluate, and deploy the chat app for your retail company called Contoso Trek.

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

But don't delete them yet, if you want to build a chat app in [the next part of this tutorial series](copilot-sdk-build-rag.md).

## Next step

> [!div class="nextstepaction"]
> [Part 2: Build a custom chat app with the prompt flow SDK](copilot-sdk-build-rag.md)
