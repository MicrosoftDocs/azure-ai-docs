---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 05/05/2025
---

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In this quickstart, you use [agentic retrieval](search-agentic-retrieval-concept.md) to create a conversational search experience powered by large language models (LLMs) and your proprietary data. Agentic retrieval breaks down complex user queries into subqueries, runs the subqueries in parallel, and extracts grounding data from documents indexed in Azure AI Search. The output is intended for integration with custom chat solutions.

Although you can provide your own data, this quickstart uses [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) from NASA's Earth at Night e-book. The documents provide detailed descriptions of the urban structures and lighting patterns of Phoenix, Arizona as observed from space.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource) in the [same region](#same-region-requirement) as your Azure AI Search service.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

### Same-region requirement

Agentic retrieval requires that Azure AI Search and Azure OpenAI be in the same region. To meet this requirement:

1. [Choose an Azure OpenAI region](/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#global-standard-model-availability) in which `gpt-4o-mini` and `text-embedding-3-large` are available. Agentic retrieval supports other chat and embedding models, but this quickstart assumes those previously mentioned.

1. Confirm that [Azure AI Search is available in the same region](search-region-support.md#azure-public-regions). The region must also support semantic ranker, which is essential to query execution during agentic retrieval.

1. Deploy both resources in the same region.

## Deploy models

To run agentic retrieval, you must deploy a supported chat model and a supported embedding model to your Azure OpenAI resource. This quickstart assumes `gpt-4o-mini` and `text-embedding-3-large`, respectively.

> [!IMPORTANT]
> Regardless of the chat model and embedding model that you use, make sure they meet the [same-region requirement](#same-region-requirement) for Azure AI Search and Azure OpenAI.

To deploy both Azure OpenAI models:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/).

1. On the home page, find the Azure OpenAI tile and select **Let's go**.

    :::image type="content" source="media/search-get-started-agentic-retrieval/azure-openai-lets-go-tile.png" alt-text="Screenshot of the Azure OpenAI tile in the Azure AI Foundry portal." border="true" lightbox="media/search-get-started-agentic-retrieval/azure-openai-lets-go-tile.png":::

   Your most recently used Azure OpenAI resource appears. If you have multiple Azure OpenAI resources, select **All resources** to switch between them.

1. From the left pane, select **Model catalog**.

1. Deploy `gpt-4o-mini` and `text-embedding-3-large` to your Azure OpenAI resource.

   > [!NOTE]
   > To simplify your code, don't use a custom deployment name for either model. This quickstart assumes the deployment and model names are the same.

<!--
### Supported models

Agentic retrieval supports the following Azure OpenAI models:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`

| Model type | Description | Supported models |
| -- | -- | -- |
| Chat model | XYZ | `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-nano`, and `gpt-4.1-mini` |
| Embedding model | XYZ | `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large` |
-->

## Configure access

Azure AI Search needs access to your Azure OpenAI models. For this task, you can use API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. [Enable role-based access](search-security-enable-roles.md) on your Azure AI Search service.

1. [Create a system-assigned managed identity](search-howto-managed-identities-data-sources.md#create-a-system-managed-identity) on your Azure AI Search service.

1. On your Azure AI Search service, [assign the following roles](search-security-rbac.md#how-to-assign-roles-in-the-azure-portal) to yourself.

    + **Owner/Contributor** or **Search Service Contributor**
    + **Search Index Data Contributor**
    + **Search Index Data Reader**

1. On your Azure OpenAI resource, assign **Cognitive Services User** to the managed identity of your search service.

## Get endpoints

In your code, you specify the following endpoints to establish connections with Azure AI Search and Azure OpenAI. These steps assume that you configured role-based access in the previous section.

To obtain your service endpoints:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. On your Azure AI Search service:

    1. From the left pane, select **Overview**.

    1. Copy the URL, which should be similar to `https://my-service.search.windows.net`.

1. On your Azure OpenAI resource:

    1. From the left pane, select **Resource Management** > **Keys and Endpoint**.

    1. Copy the URL, which should be similar to `https://my-resource.openai.azure.com`.

## Connect from your local system

You've configured role-based access to interact with Azure AI Search and Azure OpenAI. From the command line, use the Azure CLI to sign in to the same tenant and subscription for both services. For more information, see [Quickstart: Connect without keys](search-get-started-rbac.md).

To connect from your local system, run the following commands in sequence.

```Azure CLI
az account show

az account set --subscription <PUT YOUR SUBSCRIPTION ID HERE>
    
az login --tenant <PUT YOUR TENANT ID HERE>
```

## Load connections

<!--Add information.-->

1. In Visual Studio Code, create a `.ipynb` file.

1. Install the following Python packages.

    ```Python
    ! pip install azure-search-documents==11.6.0b11 --quiet
    ! pip install azure-identity --quiet
    ! pip install openai --quiet
    ! pip install aiohttp --quiet
    ! pip install ipykernel --quiet
    ! pip install requests --quiet
    ```

1. In another code cell, paste the following import statements and variables.

    ```Python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    import os

    answer_model = "gpt-4o"
    endpoint = "PUT YOUR SEARCH SERVICE ENDPOINT HERE"
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")
    index_name = "earth_at_night"
    azure_openai_endpoint = "PUT YOUR AZURE OPENAI ENDPOINT HERE"
    azure_openai_gpt_deployment = "gpt-4o-mini"
    azure_openai_gpt_model = "gpt-4o-mini"
    azure_openai_api_version = "2025-03-01-preview"
    azure_openai_embedding_deployment = "text-embedding-3-large"
    azure_openai_embedding_model = "text-embedding-3-large"
    agent_name = "earth-search-agent"
    api_version = "2025-05-01-Preview"
    ```

1. Replace `endpoint` and `azure_openai_endpoint` with the values you obtained in [Get endpoints](#get-endpoints).

---

## Create a search index

A search index provides grounding data for the chat model. <!--Add information.-->

```Python

```

---

## Upload documents to the index

```Python

```

## Create a search agent

```Python

```
