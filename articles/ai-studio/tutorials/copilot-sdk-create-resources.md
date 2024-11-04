---
title: "Part 1: Create resources to build a custom chat app"
titleSuffix: Azure AI Studio
description:  Build a custom chat app using the prompt flow SDK. Part 1 of a 3-part tutorial series, which shows how to create the resources you'll need for parts 2 and 3.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: tutorial
ms.date: 11/03/2024
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can build a RAG-based chat app.
---

# Tutorial:  Part 1 - Create resources for building a custom chat application with the prompt flow SDK

In this tutorial, you use the prompt flow SDK (and other libraries) to build, configure, evaluate, and deploy a chat app for your retail company called Contoso Trek. Your retail company specializes in outdoor camping gear and clothing. The chat app should answer questions about your products and services. For example, the chat app can answer questions such as "which tent is the most waterproof?" or "what is the best sleeping bag for cold weather?".

This tutorial is part one of a three-part tutorial.  This part one shows how an administrator of an Azure subscription creates and configures the resources needed for parts two and three of the tutorial series. Parts two and three show how a developer uses the resources. In many organizations, the same person might take on both of these roles. In this part one, you learn how to:

> [!div class="checklist"]
> - Create a project
> - Create an Azure AI Search index
> - Install the Azure CLI and sign in
> - Install Python and packages
> - Configure your environment variables

If you've completed other tutorials or quickstarts, you might have already created some of the resources needed for this tutorial. If you have, feel free to skip those steps here.

This tutorial is part one of a three-part tutorial.

## Prerequisites

* An Azure account with an active subscription. If you don't have one, [create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

## Create a project

To create a project in [Azure AI Studio](https://ai.azure.com), follow these steps:

1. Go to the **Home** page of [Azure AI Studio](https://ai.azure.com). 
1. Select **+ New project**.
1. Enter a name for the project.  Keep all the other settings as default.
1. Select **Create project**.

## Create an Azure AI Search service

The goal with this application is to ground the model responses in your custom data. The search index is used to retrieve relevant documents based on the user's question.

You need an Azure AI Search service and connection in order to create a search index.

> [!NOTE]
> Creating an [Azure AI Search service](/azure/search/) and subsequent search indexes has associated costs. You can see details about pricing and pricing tiers for the Azure AI Search service on the creation page, to confirm cost before creating the resource.

If you already have an Azure AI Search service, you can skip to the [next section](#connect).

Otherwise, you can create an Azure AI Search service using the Azure portal.

1. [Create an Azure AI Search service](https://portal.azure.com/#create/Microsoft.Search) in the Azure portal.
1. Select your resource group and instance details. You can see details about pricing and pricing tiers on this page.
1. Continue through the wizard and select **Review + assign** to create the resource.
1. Confirm the details of your Azure AI Search service, including estimated cost.
1. Select **Create** to create the Azure AI Search service.

### <a name="connect"></a>Connect the Azure AI Search to your project

If you already have an Azure AI Search connection in your project, you can skip to [configure access for the Azure AI Search service](#configure).

In the Azure AI Studio, check for an Azure AI Search connected resource.

1. In [AI Studio](https://ai.azure.com), go to your project and select **Management center** from the left pane.
1. In the **Connected resources** section, look to see if you have a connection of type **Azure AI Search**.
1. If you have an Azure AI Search connection, you can skip ahead to the next section.
1. Otherwise, select **New connection** and then **Azure AI Search**.
1. Find your Azure AI Search service in the options and select **Add connection**.
1. Use **API key** for **Authentication**.
1. Select **Add connection**.  

> [!NOTE]
> You can instead use **Microsoft Entra ID** for **Authentication**. If you do this, you must also configure access control for the Azure AI Search service. Assign yourself the **Cognitive Services OpenAI User** role.

## Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../includes/install-cli.md)]

## Create a new Python environment

[!INCLUDE [Install Python](../includes/install-python.md)]

## Install packages

* Install the Azure AI SDK packages you need.

    ```bash
    pip install azure_ai_projects azure_ai_inference azure-identity --force-reinstall
    ```

* Install additional packages needed to run the sample app

    ```python
    pip install azure-search-documents pandas
    ```

* Install packages needed to run evaluation

    ```python
    pip install azure-ai-evaluation[remote]
    ```

* Install packages needed for logging traces to AI Studio projects:

    ```python
    pip install azure-monitor-opentelemetry
    ```

## Deploy models

You need two models to build a RAG-based chat app: an Azure OpenAI chat model (`gpt-40-mini`) and an Azure OpenAI embedding model (`text-embedding-ada-002`). Deploy these models in your Azure AI Studio project, using this set of steps for each model.

These steps deploy a model to a real-time endpoint from the AI Studio [model catalog](../how-to/model-catalog-overview.md):

1. Sign in to [Azure AI Studio](https://ai.azure.com).
1. Studio remembers where you were last, so if you just completed the [Part 1 tutorial](copilot-sdk-create-resources.md), you're already in a project. If you're not in a project, select the project you created in Part 1.
1. 
1. Select the **gpt-4o-mini** model from the list of models. You can use the search bar to find it. 

    :::image type="content" source="../media/tutorials/chat/select-model.png" alt-text="Screenshot of the model selection page." lightbox="../media/tutorials/chat/select-model.png":::

1. On the model details page, select **Deploy**.

    :::image type="content" source="../media/tutorials/chat/deploy-model.png" alt-text="Screenshot of the model details page with a button to deploy the model." lightbox="../media/tutorials/chat/deploy-model.png":::

1. Leave the default **Deployment name**. Select **Connect and deploy**.

After you deploy the **gpt-40-mini**, repeat the steps to deploy the **text-embedding-ada-002** model.

## Configure environment variables

[!INCLUDE [create-env-file](../includes/create-env-file-tutorial.md)]

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

But don't delete them yet, if you want to build a chat app in [the next part of this tutorial series](copilot-sdk-build-rag.md).

## Next step

In this tutorial, you set up everything you need to build a custom chat app with the Azure AI SDK. In the next part of this tutorial series, you build the custom app.

> [!div class="nextstepaction"]
> [Part 2: Build a custom chat app with the Azure AI SDK](copilot-sdk-build-rag.md)
