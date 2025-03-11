---
title: "Part 2: Build a custom knowledge retrieval (RAG) app with the Azure AI Foundry SDK"
titleSuffix: Azure AI Foundry
description:  Learn how to build a RAG-based chat app using the Azure AI Foundry SDK. This tutorial is part 2 of a 3-part tutorial series.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 02/12/2025
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
ms.custom: copilot-learning-hub, ignite-2024
#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can build a RAG-based chat app.
---

# Tutorial:  Part 2 - Build a custom knowledge retrieval (RAG) app with the Azure AI Foundry SDK

In this tutorial, you use the [Azure AI Foundry](https://ai.azure.com) SDK (and other libraries) to build, configure, and evaluate a chat app for your retail company called Contoso Trek. Your retail company specializes in outdoor camping gear and clothing. The chat app should answer questions about your products and services. For example, the chat app can answer questions such as "which tent is the most waterproof?" or "what is the best sleeping bag for cold weather?".

This part two shows you how to enhance a basic chat application by adding [retrieval augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) to ground the responses in your custom data. Retrieval Augmented Generation (RAG) is a pattern that uses your data with a large language model (LLM) to generate answers specific to your data. In this part two, you learn how to:

> [!div class="checklist"]
> - Get example data
> - Create a search index of the data for the chat app to use
> - Develop custom RAG code

This tutorial is part two of a three-part tutorial.

## Prerequisites

* Complete [Tutorial:  Part 1 - Create resources for building a custom chat application with the Azure AI SDK](copilot-sdk-create-resources.md) to:

    * Create a project with a connected Azure AI Search index
    * Install the Azure CLI, Python, and required packages
    * Configure your environment variables

## Create example data for your chat app

The goal with this RAG-based application is to ground the model responses in your custom data. You use an Azure AI Search index that stores vectorized data from the embeddings model. The search index is used to retrieve relevant documents based on the user's question.

If you already have a search index with data, you can skip to [Get product documents](#get-documents). Otherwise, you can create a simple example data set to use in your chat app.  

Create an **assets** directory and add this example data to a **products.csv** file:

:::code language="csv" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/products.csv":::

## Create a search index

The search index is used to store vectorized data from the embeddings model. The search index is used to retrieve relevant documents based on the user's question. 

1. Create the file **create_search_index.py** in your main folder (that is, the same directory where you placed your **assets** folder, not inside the **assets** folder).  
1. Copy and paste the following code into your **create_search_index.py** file.
1. Add the code to import the required libraries, create a project client, and configure some settings: 

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="imports_and_config":::

1. Now add the function to define a search index:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="create_search_index":::

1. Create the function to add a csv file to the index:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="add_csv_to_index":::

1. Finally, run the functions to build the index and register it to the cloud project:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="test_create_index":::

1. From your console, log in to your Azure account and follow instructions for authenticating your account:

    ```bash
    az login
    ```

1. Run the code to build your index locally and register it to the cloud project:

    ```bash
    python create_search_index.py
    ```

## <a name="get-documents"></a> Get product documents

Next, you create a script to get product documents from the search index. The script queries the search index for documents that match a user's question.

### Create script to get product documents

When the chat gets a request, it searches through your data to find relevant information.  This script uses the Azure AI SDK to query the search index for documents that match a user's question.  It then returns the documents to the chat app.

1. Create the **get_product_documents.py** file in your main directory. Copy and paste the following code into the file.

1. Start with code to import the required libraries, create a project client, and configure settings: 

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/get_product_documents.py" id="imports_and_config":::

1. Add the function to get product documents:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/get_product_documents.py" id="get_product_documents":::

1. Finally, add code to test the function when you run the script directly:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/get_product_documents.py" id="test_get_documents":::

### Create prompt template for intent mapping

The **get_product_documents.py** script uses a prompt template to convert the conversation to a search query. The template instructs how to extract the user's intent from the conversation.  

Before you run the script, create the prompt template. Add the file **intent_mapping.prompty** to your **assets** folder:

:::code language="prompty" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/intent_mapping.prompty":::

### Test the product document retrieval script

Now that you have both the script and template, run the script to test out what documents the search index returns from a query.  In a terminal window run:

```bash
python get_product_documents.py --query "I need a new tent for 4 people, what would you recommend?"
```

## <a name="develop-code"></a> Develop custom knowledge retrieval (RAG) code

Next you create custom code to add retrieval augmented generation (RAG) capabilities to a basic chat application.

### Create a chat script with RAG capabilities

1. In your main folder, create a new file called **chat_with_products.py**. This script retrieves product documents and generates a response to a user's question.
1. Add the code to import the required libraries, create a project client, and configure settings: 

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/chat_with_products.py" id="imports_and_config":::

1. Create the chat function that uses the RAG capabilities:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/chat_with_products.py" id="chat_function":::

1. Finally, add the code to run the chat function:
    
    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/chat_with_products.py" id="test_function":::

### Create a grounded chat prompt template

The **chat_with_products.py** script calls a prompt template to generate a response to the user's question. The template instructs how to generate a response based on the user's question and the retrieved documents.  Create this template now.

In your **assets** folder, add the file **grounded_chat.prompty**:

:::code language="prompty" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/grounded_chat.prompty":::

### Run the chat script with RAG capabilities

Now that you have both the script and the template, run the script to test your chat app with RAG capabilities:

```bash
python chat_with_products.py --query "I need a new tent for 4 people, what would you recommend?"
```

### <a name="logging"></a> Add telemetry logging

To enable logging of telemetry to your project:

1. Add an Application Insights resource to your project.  Navigate to the **Tracing** tab in the [Azure AI Foundry portal](https://ai.azure.com/), and create a new resource if you don't already have one.

    :::image type="content" source="../../ai-services/agents/media/ai-foundry-tracing.png" alt-text="A screenshot of the tracing screen in the Azure AI Foundry portal." lightbox="../../ai-services/agents/media/ai-foundry-tracing.png":::

1. Install `azure-monitor-opentelemetry`:

   ```bash
   pip install azure-monitor-opentelemetry
   ```
   
1. Add the `--enable-telemetry` flag when you use the `chat_with_products.py` script:

   ```bash
   python chat_with_products.py --query "I need a new tent for 4 people, what would you recommend?" --enable-telemetry 
   ```

Follow the link in the console output to see the telemetry data in your Application Insights resource. If it doesn't appear right away, wait a few minutes and select **Refresh** in the toolbar.

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

But don't delete them yet, if you want to deploy your chat app to Azure in [the next part of this tutorial series](copilot-sdk-evaluate.md).

## Next step

> [!div class="nextstepaction"]
> [Part 3: Evaluate your chat app to Azure](copilot-sdk-evaluate.md)
