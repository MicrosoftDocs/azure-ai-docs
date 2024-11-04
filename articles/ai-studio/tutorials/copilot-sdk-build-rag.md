---
title: "Part 1: Build a custom chat app with the Azure AI SDK"
titleSuffix: Azure AI Studio
description:  Learn how to build a RAG-based chat app using the Azure AI SDK. This tutorial is part 2 of a 3-part tutorial series.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: tutorial
ms.date: 11/03/2024
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
ms.custom: [copilot-learning-hub]
#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can build a RAG-based chat app.
---

# Tutorial:  Part 2 - Build a custom chat application with the Azure AI SDK

In this tutorial, you use the Azure AI SDK (and other libraries) to build, configure, evaluate, and deploy a chat app for your retail company called Contoso Trek. Your retail company specializes in outdoor camping gear and clothing. The chat app should answer questions about your products and services. For example, the chat app can answer questions such as "which tent is the most waterproof?" or "what is the best sleeping bag for cold weather?".

This part two shows you how to enhance a basic chat application by adding [retrieval augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) to ground the responses in your custom data. Retrieval Augmented Generation (RAG) is a pattern that uses your data with a large language model (LLM) to generate answers specific to your data. In this part two, you learn how to:

> [!div class="checklist"]
> - Deploy AI models in Azure AI Studio to use in your app
> - Develop custom RAG code
> - Use prompt flow to test your chat app

This tutorial is part two of a three-part tutorial.

## Prerequisites

* Complete [Tutorial:  Part 1 - Create resources for building a custom chat application with the Azure AI SDK](copilot-sdk-create-resources.md) to:

    * Create a project with a connected Azure AI Search index
    * Install the Azure CLI, Python, and required packages
    * Configure your environment variables

* You need a local copy of product data. The [Azure-Samples/rag-data-openai-python-promptflow repository on GitHub](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/) contains sample retail product information that's relevant for this tutorial scenario. [Download the example Contoso Trek retail product data in a ZIP file](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/tutorial/data/product-info.zip) to your local machine.


## Deploy models

You need two models to build a RAG-based chat app: an Azure OpenAI chat model (`gpt-40-mini`) and an Azure OpenAI embedding model (`text-embedding-ada-002`). Deploy these models in your Azure AI Studio project, using this set of steps for each model.

These steps deploy a model to a real-time endpoint from the AI Studio [model catalog](../how-to/model-catalog-overview.md):

[!INCLUDE [Deploy a model](../includes/deploy-model.md)]

After you deploy the **gpt-40-mini**, repeat the steps to deploy the **text-embedding-ada-002** model. The second time, you'll already be in a project, so you can skip the project selection step.

## Create an Azure AI Search index

The goal with this RAG-based application is to ground the model responses in your custom data. You use an Azure AI Search index that stores vectorized data from the embeddings model. The search index is used to retrieve relevant documents based on the user's question.

If you don't have an Azure AI Search index already created, we walk through how to create one. If you already have an index to use, you can skip to the [next](#develop-code) section. 

1. Use your own data or [download the example Contoso Trek retail product data in a ZIP file](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/tutorial/data/product-info.zip) to your local machine. Unzip the file into your **rag-tutorial/data** folder. This data is a collection of markdown files that represent product information. The data is structured in a way that is easy to ingest into a search index. You build a search index from this data.

1. Create the **create_search_index.py** file. 
1. Copy and paste the following code into your **create_search_index.py** file.

    ```python
    code here
    ```

1. From your console, run the code to build your index locally and register it to the cloud project:

    ```bash
    python create_search_index.py
    ```

1. Once the script is run, you can view your newly created index in the **Data + indexes** page of your Azure AI Studio project. For more information, see [How to build and consume vector indexes in Azure AI Studio](../how-to/index-add.md).

1. If you run the script again with the same index name, it creates a new version of the same index.


## Get product documents

You can test out what documents the search index returns from a query. This script uses the Azure AI SDK to query the search index for documents that match a user's question.
1. Create the **get_product_documents.py** file.
1. Copy and paste the following code into your **get_product_documents.py** file.

    ```python
    code here
    ```
1. From your console, run the code to test out what documents the search index returns from a query:

    ```bash
    python get_product_documents.py --query "I need a new tent for 4 people, what would you recommend?"
    ```

## <a href="develop-code"></a> Develop custom RAG code

Next you create custom code to add retrieval augmented generation (RAG) capabilities to a basic chat application.

1. Create a file named **chat_with_products.py**.
1. Copy and paste the following code into your **chat_with_products.py** file.

    ```python
    code here
    ```

1. Run the code to test your chat app with RAG capabilities:

    ```bash
    python chat_with_products.py --query "I need a new tent for 4 people, what would you recommend?"
    ```

1. To enable logging of telemetry to your project, add the `--enable-telemetry` flag:

    ```bash
    python chat_with_products.py --query "I need a new tent for 4 people, what would you recommend?" --enable-telemetry
    ```

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

But don't delete them yet, if you want to deploy your chat app to Azure in [the next part of this tutorial series](copilot-sdk-evaluate-deploy.md).

## Next step

> [!div class="nextstepaction"]
> [Part 2: Evaluate and deploy your chat app to Azure](copilot-sdk-evaluate-deploy.md)
