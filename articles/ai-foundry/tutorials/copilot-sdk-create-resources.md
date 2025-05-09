---
title: "Part 1: Set up project and development environment to build a custom knowledge retrieval (RAG) app"
titleSuffix: Azure AI Foundry
description:  Build a custom chat app using the Azure AI Foundry SDK. Part 1 of a 3-part tutorial series, which shows how to create the resources you need for parts 2 and 3.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: tutorial
ms.date: 02/12/2025
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
#customer intent: As a developer, I want to create a project and set up my development environment to build a custom knowledge retrieval (RAG) app with the Azure AI Foundry SDK.
---

# Tutorial:  Part 1 - Set up project and development environment to build a custom knowledge retrieval (RAG) app with the Azure AI Foundry SDK

In this tutorial, you use the [Azure AI Foundry](https://ai.azure.com) SDK (and other libraries) to build, configure, and evaluate a chat app for your retail company called Contoso Trek. Your retail company specializes in outdoor camping gear and clothing. The chat app should answer questions about your products and services. For example, the chat app can answer questions such as "which tent is the most waterproof?" or "what is the best sleeping bag for cold weather?".

This tutorial is part one of a three-part tutorial.  This part one gets you ready to write code in part two and evaluate your chat app in part three. In this part, you:

> [!div class="checklist"]
> - Create a project
> - Create an Azure AI Search index
> - Install the Azure CLI and sign in
> - Install Python and packages
> - Deploy models into your project
> - Configure your environment variables

If you've completed other tutorials or quickstarts, you might have already created some of the resources needed for this tutorial. If you have, feel free to skip those steps here.

This tutorial is part one of a three-part tutorial.

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

## Prerequisites

* An Azure account with an active subscription. If you don't have one, [create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

## Create a project

To create a project in [Azure AI Foundry](https://ai.azure.com), follow these steps:

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com).
1. Select **+ Create project**.
1. Enter a name for the project.  Keep all the other settings as default.
1. Projects are created in hubs.  If you see **Create a new hub** select it and specify a name.  Then select **Next**. (If you don't see **Create new hub**, don't worry; it's because a new one is being created for you.) 
1. Select **Customize** to specify properties of the hub.
1. Use any values you want, except for **Region**.  We recommend you use either **East US2** or **Sweden Central** for the region for this tutorial series.
1. Select **Next**.
1. Select **Create project**.

## Deploy models

You need two models to build a RAG-based chat app: an Azure OpenAI chat model (`gpt-4o-mini`) and an Azure OpenAI embedding model (`text-embedding-ada-002`). Deploy these models in your Azure AI Foundry project, using this set of steps for each model.

These steps deploy a model to a real-time endpoint from the Azure AI Foundry portal [model catalog](../how-to/model-catalog-overview.md):

1. On the left pane, select **Model catalog**.
1. Select the **gpt-4o-mini** model from the list of models. You can use the search bar to find it. 

    :::image type="content" source="../media/tutorials/chat/select-model.png" alt-text="Screenshot of the model selection page." lightbox="../media/tutorials/chat/select-model.png":::

1. On the model details page, select **Deploy**.

    :::image type="content" source="../media/tutorials/chat/deploy-model.png" alt-text="Screenshot of the model details page with a button to deploy the model." lightbox="../media/tutorials/chat/deploy-model.png":::

1. Leave the default **Deployment name**. select **Deploy**.  Or, if the model isn't available in your region, a different region is selected for you and connected to your project.  In this case, select **Connect and deploy**.

After you deploy the **gpt-4o-mini**, repeat the steps to deploy the **text-embedding-ada-002** model.

## <a name="create-search"></a> Create an Azure AI Search service

The goal with this application is to ground the model responses in your custom data. The search index is used to retrieve relevant documents based on the user's question.

You need an Azure AI Search service and connection in order to create a search index.

> [!NOTE]
> Creating an [Azure AI Search service](/azure/search/) and subsequent search indexes has associated costs. You can see details about pricing and pricing tiers for the Azure AI Search service on the creation page, to confirm cost before creating the resource. For this tutorial, we recommend using a pricing tier of **Basic** or above.

If you already have an Azure AI Search service, you can skip to the [next section](#connect).

Otherwise, you can create an Azure AI Search service using the Azure portal. 

> [!TIP]
> This step is the only time you use the Azure portal in this tutorial series.  The rest of your work is done in Azure AI Foundry portal or in your local development environment.

1. [Create an Azure AI Search service](https://portal.azure.com/#create/Microsoft.Search) in the Azure portal.
1. Select your resource group and instance details. You can see details about pricing and pricing tiers on this page.
1. Continue through the wizard and select **Review + assign** to create the resource.
1. Confirm the details of your Azure AI Search service, including estimated cost.
1. Select **Create** to create the Azure AI Search service.

### <a name="connect"></a>Connect the Azure AI Search to your project

If you already have an Azure AI Search connection in your project, you can skip to [Install the Azure CLI and sign in](#installs).

In the Azure AI Foundry portal, check for an Azure AI Search connected resource.

1. In [Azure AI Foundry](https://ai.azure.com), go to your project and select **Management center** from the left pane.
1. In the **Connected resources** section, look to see if you have a connection of type **Azure AI Search**.
1. If you have an Azure AI Search connection, you can skip ahead to the next section.
1. Otherwise, select **New connection** and then **Azure AI Search**.
1. Find your Azure AI Search service in the options and select **Add connection**.
1. Use **API key** for **Authentication**.

    > [!IMPORTANT]
    > The **API key** option isn't recommended for production. To select and use the recommended **Microsoft Entra ID** authentication option, you must also configure access control for the Azure AI Search service. Assign the *Search Index Data Contributor* and *Search Service Contributor* roles to your user account. For more information, see [Connect to Azure AI Search using roles](../../search/search-security-rbac.md) and [Role-based access control in Azure AI Foundry portal](../concepts/rbac-azure-ai-foundry.md).

1. Select **Add connection**.  


## Create a new Python environment

In the IDE of your choice, create a new folder for your project.  Open a terminal window in that folder.

[!INCLUDE [Install Python](../includes/install-python.md)]

## Install packages

Install `azure-ai-projects`(preview) and `azure-ai-inference` (preview), along with other required packages.

1. First, create a file named **requirements.txt** in your project folder. Add the following packages to the file:

    :::code language="txt" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/requirements.txt":::

1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Create helper script

Create a folder for your work. Create a file called **config.py** in this folder. This helper script is used in the next two parts of the tutorial series. Add the following code:

:::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/config.py":::

> [!NOTE]
> This script also uses a package you haven't installed yet, `azure.monitor.opentelemetry`.  You'll install this package in the next part of the tutorial series.

## Configure environment variables

[!INCLUDE [create-env-file](../includes/create-env-file-tutorial.md)]

## <a name="installs"></a> Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../includes/install-cli.md)]

Keep this terminal window open to run your python scripts from here as well, now that you've signed in.

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

But don't delete them yet, if you want to build a chat app in [the next part of this tutorial series](copilot-sdk-build-rag.md).

## Next step

In this tutorial, you set up everything you need to build a custom chat app with the Azure AI SDK. In the next part of this tutorial series, you build the custom app.

> [!div class="nextstepaction"]
> [Part 2: Build a custom chat app with the Azure AI SDK](copilot-sdk-build-rag.md)
