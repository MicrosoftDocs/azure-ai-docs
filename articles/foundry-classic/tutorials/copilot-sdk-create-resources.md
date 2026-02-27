---
title: "Part 1: Set up project and development environment to build a custom knowledge retrieval (RAG) app"
titleSuffix: Microsoft Foundry
description:  Build a custom chat app using the Microsoft Foundry SDK. Part 1 of a 3-part tutorial series, which shows how to create the resources you need for parts 2 and 3.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
  - update-code
  - hub-only
  - dev-focus
ms.topic: tutorial
ai-usage: ai-assisted
ms.date: 12/16/2025
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley

#customer intent: As a developer, I want to create a project and set up my development environment to build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK.
---

# Tutorial:  Part 1 - Set up project and development environment to build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In this tutorial, you set up the resources needed to build a custom knowledge retrieval (RAG) chat app with the Microsoft Foundry SDK. This is part one of a three-part tutorial series. You create the resources here, build the app in part two, and evaluate it in part three. In this part, you:

> [!div class="checklist"]
> - Create a project
> - Create an Azure AI Search index
> - Install the Azure CLI and sign in
> - Install Python and packages
> - Deploy models into your project
> - Configure your environment variables

If you completed other tutorials or quickstarts, you might have already created some of the resources needed for this tutorial. If you did, feel free to skip those steps.

## Prerequisites

[!INCLUDE [uses-hub-only](../includes/uses-hub-only.md)]

* An Azure account with an active subscription and **Owner** or **Contributor** role assigned. If you don't have one, [create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Microsoft Foundry**: Owner or Contributor role to create a project.


## Create a hub-based project

[!INCLUDE [create-hub-project-simple](../includes/create-hub-project-simple.md)]

## Deploy models

You need two models to build a RAG-based chat app: an Azure OpenAI chat model (`gpt-4o-mini`) and an Azure OpenAI embedding model (`text-embedding-ada-002`). Deploy these models in your Foundry project by using this set of steps for each model.

These steps deploy a model to a real-time endpoint from the Foundry portal [model catalog](../concepts/foundry-models-overview.md):

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. On the left pane, select **Model catalog**.
1. Select the **gpt-4o-mini** model from the list of models. You can use the search bar to find it. 

    :::image type="content" source="../media/tutorials/chat/select-model.png" alt-text="Screenshot of the model selection page." lightbox="../media/tutorials/chat/select-model.png":::

1. On the model details page, select **Use this model**.

1. Leave the default **Deployment name** and select **Deploy**. Or, if the model isn't available in your region, a different region is selected for you and connected to your project. In this case, select **Connect and deploy**.

After you deploy the **gpt-4o-mini**, repeat the steps to deploy the **text-embedding-ada-002** model.

## Create an Azure AI Search service

The goal of this application is to ground the model responses in your custom data. The search index retrieves relevant documents based on the user's question.

You need an Azure AI Search service and connection to create a search index.

> [!NOTE]
> Creating an [Azure AI Search service](/azure/search/) and subsequent search indexes incurs costs. To confirm the cost before creating the resource, check the pricing and pricing tiers for the Azure AI Search service on the creation page. For this tutorial, use a pricing tier of **Basic** or higher.

If you already have an Azure AI Search service, go to the [next section](#connect-the-azure-ai-search-to-your-project).

Otherwise, create an Azure AI Search service by using the Azure portal. 

> [!TIP]
> This step is the only time you use the Azure portal in this tutorial series.  You do the rest of your work in the Foundry portal or in your local development environment.

1. [Create an Azure AI Search service](https://portal.azure.com/#create/Microsoft.Search) in the Azure portal.
1. Select your resource group and instance details. Check the pricing and pricing tiers on this page. For this tutorial, use a pricing tier of **Basic** or higher.
1. Continue through the wizard and select **Review + assign** to create the resource.
1. Confirm the details of your Azure AI Search service, including the estimated cost.
1. Select **Create** to create the Azure AI Search service.

### Connect the Azure AI Search to your project

If your project already has an Azure AI Search connection, go to [Install the Azure CLI and sign in](#install-the-azure-cli-and-sign-in).

In the Foundry portal, check for an Azure AI Search connected resource.

1. In [Foundry](https://ai.azure.com/?cid=learnDocs), go to your project and select **Management center** from the left pane.
1. In the **Connected resources** section, look to see if you have a connection of type **Azure AI Search**.
1. If you have an Azure AI Search connection, you can skip the next steps.
1. Otherwise, select **New connection** and then **Azure AI Search**.
1. Find your Azure AI Search service in the options and select **Add connection**.
1. Use **API key** for **Authentication**.

    > [!IMPORTANT]
    > The **API key** option isn't recommended for production. The recommended approach is **Microsoft Entra ID** authentication, which requires the *Search Index Data Contributor* and *Search Service Contributor* roles (configured in Prerequisites). For more information, see [Connect to Azure AI Search using roles](../../search/search-security-rbac.md).
    > For this tutorial, **API key** is acceptable if you want to proceed quickly. Switch to Entra ID before deploying to production.

1. Select **Add connection**.  


## Create a new Python environment

In the IDE of your choice, create a new folder for your project.  Open a terminal window in that folder.

[!INCLUDE [Install Python](../includes/install-python.md)]

## Install packages

Install the required packages.

1. Create a file named **requirements.txt** in your project folder. Add the following packages to the file:

    :::code language="txt" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/requirements.txt":::

    References: [Azure AI Projects client library](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects), [azure-ai-inference](https://pypi.org/project/azure-ai-inference/), [python-dotenv](https://pypi.org/project/python-dotenv/).

1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configure environment variables

[!INCLUDE [create-env-file](../includes/create-env-file-tutorial.md)]

## Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../includes/install-cli.md)]

Keep this terminal window open to run your python scripts from here as well, now that you signed in.

## Verify your setup

Verify that your environment is set up correctly by running a quick test:

```python
import os
from azure.identity import DefaultAzureCredential
import azure.ai.projects

# Check the SDK version
print(f"Azure AI Projects SDK version: {azure.ai.projects.__version__}")

# Test that you can connect to your project
project = AIProjectClient.from_connection_string(
    conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
)
print("✓ Setup verified! Ready to build your RAG app.")
```

If you see `"Setup successful!"`, your Azure credentials and SDK are configured correctly. 

> [!TIP]
> This tutorial requires Azure AI Projects SDK version `1.0.0b10`. The SDK version displayed above helps you verify compatibility. If you have a different version, the `from_connection_string()` method may not be available. To install the required version, run `pip install azure-ai-projects==1.0.0b10`. 

References: [Azure AI Projects client library](/python/api/azure-ai-projects/azure.ai.projects), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.DefaultAzureCredential).

## Create helper script

Create a folder for your work. Create a file named **config.py** in this folder. You'll use this helper script in the next two parts of the tutorial series. The script loads your environment variables and initializes the Azure AI Projects client. Add the following code:

:::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/config.py":::

References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.DefaultAzureCredential), [load_dotenv](https://pypi.org/project/python-dotenv/).

> [!NOTE]
> This script also uses a package you haven't installed yet, `azure.monitor.opentelemetry`.  You'll install this package in the next part of the tutorial series.


## Clean up resources

To avoid incurring unnecessary Azure costs, delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

But don't delete them yet if you want to build a chat app in [the next part of this tutorial series](copilot-sdk-build-rag.md).

## Next step

In this tutorial, you set up everything you need to build a custom chat app with the Azure AI SDK. In the next part of this tutorial series, you build the custom app.

> [!div class="nextstepaction"]
> [Part 2: Build a custom chat app with the Azure AI SDK](copilot-sdk-build-rag.md)
