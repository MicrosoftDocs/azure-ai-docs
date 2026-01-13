---
title: "Part 2: Build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK"
titleSuffix: Microsoft Foundry
description:  Learn how to build a RAG-based chat app using the Microsoft Foundry SDK. This tutorial is part 2 of a 3-part tutorial series.
ms.service: azure-ai-foundry
ms.topic: tutorial
ms.date: 12/16/2025
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
ms.custom: 
  - copilot-learning-hub
  - ignite-2024
  - hub-only
  - dev-focus
ai-usage: ai-assisted
#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can build a RAG-based chat app.
---

# Tutorial:  Part 2 - Build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In this tutorial, you use the [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) SDK and other libraries to build, configure, and evaluate a chat app for your retail company called Contoso Trek. Your retail company specializes in outdoor camping gear and clothing. The chat app answers questions about your products and services. For example, the chat app can answer questions such as "which tent is the most waterproof?" or "what is the best sleeping bag for cold weather?".

This part two shows you how to enhance a basic chat application by adding [retrieval augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) to ground the responses in your custom data. Retrieval Augmented Generation (RAG) is a pattern that uses your data with a large language model (LLM) to generate answers specific to your data. In this part two, you learn how to:

> [!div class="checklist"]
> - Get example data
> - Create a search index of the data for the chat app to use
> - Develop custom RAG code

This tutorial builds on [Tutorial: Part 1 - Create resources for building a custom chat application with the Microsoft Foundry SDK](copilot-sdk-create-resources.md).

> [!IMPORTANT]
> This example uses Azure AI Inference beta SDK.  We recommend that you transition to the generally available [OpenAI/v1 API](https://aka.ms/openai/v1), which uses an OpenAI stable SDK.
>
> For more information on how to migrate to the OpenAI/v1 API by using an SDK in your programming language of choice, see [Migrate from Azure AI Inference SDK to OpenAI SDK](../how-to/model-inference-to-openai-migration.md).

## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

* Complete [Tutorial: Part 1 - Create resources for building a custom chat application with the Microsoft Foundry SDK](copilot-sdk-create-resources.md) to:
    * Create a project with a connected Azure AI Search index.
    * Install the Azure CLI, Python, and required packages.
    * Configure your environment variables.
* Use the same **hub-based** project you created in Part 1.
* **Azure AI permissions**: Owner or Contributor role to create search indexes and deploy models; Cognitive Services Contributor or higher for AI Services resources. 

## Verify your setup

Before building the RAG app, confirm that your environment is properly configured by running a quick connection test:

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

If you see the success message, your Azure credentials and SDK are configured correctly. If you encounter authentication errors, verify your `FOUNDRY_*` environment variables are set correctly (see Part 1 prerequisites).

> [!TIP]
> This tutorial requires Azure AI Projects SDK version `1.0.0b10`. The SDK version displayed above helps you verify compatibility. If you have a different version, the `from_connection_string()` method may not be available. To install the required version, run `pip install azure-ai-projects==1.0.0b10`. 

References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.DefaultAzureCredential).

## Create example data for your chat app

The goal with this RAG-based application is to ground the model responses in your custom data. You use an Azure AI Search index that stores vectorized data from the embeddings model. The search index is used to retrieve relevant documents based on the user's question.

If you already have a search index with data, you can skip to [Get product documents](#get-product-documents). Otherwise, you can create a simple example data set to use in your chat app.  

Create an **assets** directory and add this example data to a **products.csv** file:

:::code language="csv" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/products.csv":::

This CSV file contains product information that the search index stores and retrieves to ground the chat responses.

## Create a search index

You use the search index to store vectorized data from the embeddings model. The search index retrieves relevant documents based on the user's question. 

1. Create the file **create_search_index.py** in your main folder (that is, the same directory where you placed your **assets** folder, not inside the **assets** folder).  
1. Copy and paste the following code into your **create_search_index.py** file.
1. Add the code to import the required libraries, create a project client, and configure some settings: 

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="imports_and_config":::

    The imports include `AIProjectClient` to connect to your project, `SearchClient` to manage the search index, and `EmbeddingsModel` to vectorize documents.

    References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [SearchClient](/python/api/azure-search-documents/azure.search.documents.SearchClient), [azure-ai-projects](https://pypi.org/project/azure-ai-projects/).

1. Now add the function to define a search index:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="create_search_index":::

    References: [SearchIndex](/python/api/azure-search-documents/azure.search.documents.indexes.models.SearchIndex), [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.SearchIndexClient).

1. Create the function to add a CSV file to the index:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="add_csv_to_index":::

    References: [azure-ai-projects](https://pypi.org/project/azure-ai-projects/), [SearchClient.upload_documents](/python/api/azure-search-documents/azure.search.documents.SearchClient).

1. Finally, run the functions to build the index and register it to the cloud project:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/create_search_index.py" id="test_create_index":::

    References: [AIProjectClient.agents](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [SearchIndexClient.create_or_update_index](/python/api/azure-search-documents/azure.search.documents.indexes.SearchIndexClient).

1. From your console, sign in to your Azure account and follow instructions for authenticating your account:

    ```bash
    az login
    ```

1. Run the code to build your index locally and register it to the cloud project:

    ```bash
    python create_search_index.py
    ```

    Successful completion displays: `➕ Uploaded 20 documents to 'example-index' index`.

## Get product documents

Next, create a script to query the search index and retrieve product documents that match user questions. When the chat app receives a query, it searches for relevant documents to ground the response in your data.

### Create script to get product documents

1. Create the **get_product_documents.py** file in your main directory. Copy and paste the following code into the file.

1. Start with code to import the required libraries, create a project client, and configure settings: 

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/get_product_documents.py" id="imports_and_config":::

    Key imports: `SearchClient` (to query the search index) and `PromptTemplate` (to construct search queries from user intent).

    References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [SearchClient](/python/api/azure-search-documents/azure.search.documents.SearchClient), [promptflow](https://pypi.org/project/promptflow/).

1. Add the function to get product documents:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/get_product_documents.py" id="get_product_documents":::

    References: [SearchClient.search](/python/api/azure-search-documents/azure.search.documents.SearchClient), [AIProjectClient.inference](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient).

1. Finally, add code to test the function when you run the script directly:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/get_product_documents.py" id="test_get_documents":::

    References: [AIProjectClient.from_config](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [argparse](https://docs.python.org/3/library/argparse.html).

### Create prompt template for intent mapping

The **get_product_documents.py** script uses a prompt template named **intent_mapping.prompty** to transform the user's question into an optimized search query. This transformation helps the search index find the most relevant product documents.

Before running the script, create the prompt template. Add the file **intent_mapping.prompty** to your **assets** folder:

:::code language="prompty" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/intent_mapping.prompty":::

This template instructs the model to extract the user's intent and convert it into a concise search query.

### Test the product document retrieval script

Now that you have both the script and template, run the script to test what documents the search index returns from a query. In a terminal window, run:

```bash
python get_product_documents.py --query "I need a new tent for 4 people, what would you recommend?"
```

The script returns a list of product documents from your search index that match the query. You should see JSON output showing product names, descriptions, and prices relevant to a 4-person tent.

## Develop custom knowledge retrieval (RAG) code

Next, you create custom code to add retrieval augmented generation (RAG) capabilities to a basic chat application.

### Create a chat script with RAG capabilities

1. In your main folder, create a new file named **chat_with_products.py**. This script retrieves product documents and generates a response to a user's question.
1. Add the code to import the required libraries, create a project client, and configure settings: 

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/chat_with_products.py" id="imports_and_config":::

    Key imports: `AIProjectClient` (connects to your project), `chat` function (from prompt flow), and `get_product_documents` (your retrieval function).

    References: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient), [promptflow](https://pypi.org/project/promptflow/).

1. Create the chat function that uses the RAG capabilities:

    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/chat_with_products.py" id="chat_function":::

    References: [azure-ai-projects](https://pypi.org/project/azure-ai-projects/), [AIProjectClient.inference](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient).

1. Finally, add the code to run the chat function:
    
    :::code language="python" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/chat_with_products.py" id="test_function":::

    References: [argparse](https://docs.python.org/3/library/argparse.html), [AIProjectClient.from_config](/python/api/azure-ai-projects/azure.ai.projects.AIProjectClient).

### Create a grounded chat prompt template

The **chat_with_products.py** script calls a prompt template named **grounded_chat.prompty** to generate responses. This template instructs the model to use the retrieved product documents to ground answers and stay on-topic for your retail business.

In your **assets** folder, add the file **grounded_chat.prompty**:

:::code language="prompty" source="~/azureai-samples-main/scenarios/rag/custom-rag-app/assets/grounded_chat.prompty":::

This template ensures responses are based on your product data rather than general knowledge.

### Run the chat script with RAG capabilities

Now that you have both the script and the template, run the script to test your chat app with RAG capabilities:

```bash
python chat_with_products.py --query "I need a new tent for 4 people, what would you recommend?"
```

The script returns a conversational response grounded in your product data. The response references specific products from your search index rather than generic advice.

### Add telemetry logging

To enable logging of telemetry to your project so you can track and monitor chat interactions:

1. Register the **Microsoft.OperationalInsights** and **microsoft.insights** resource providers in your subscription. For more information, see [Register resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider-1).

1. Add an Application Insights resource to your project. Navigate to the **Tracing** tab in the [Foundry portal](https://ai.azure.com/?cid=learnDocs), and create a new resource if you don't already have one.

    :::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/add-app-insights.png" alt-text="A screenshot of the tracing screen in the Foundry portal." lightbox="../media/tutorials/develop-rag-copilot-sdk/add-app-insights.png":::

1. Install the telemetry SDK:

   ```bash
   pip install azure-monitor-opentelemetry
   ```

   References: [azure-monitor-opentelemetry](https://pypi.org/project/azure-monitor-opentelemetry/), [OpenTelemetry](/python/api/azure-monitor-opentelemetry).
   
1. Add the `--enable-telemetry` flag when you use the `chat_with_products.py` script:

   ```bash
   python chat_with_products.py --query "I need a new tent for 4 people, what would you recommend?" --enable-telemetry 
   ```

Follow the link in the console output to see the telemetry data in your Application Insights resource. If it doesn't appear right away, wait a few minutes and select **Refresh** in the toolbar.

## Clean up resources

To avoid incurring unnecessary Azure costs, delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

Don't delete the resources if you want to deploy your chat app to Azure in [the next part of this tutorial series](copilot-sdk-evaluate.md).

## Next step

> [!div class="nextstepaction"]
> [Part 3: Evaluate your chat app to Azure](copilot-sdk-evaluate.md)
