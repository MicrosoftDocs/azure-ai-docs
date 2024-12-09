---
title: Azure OpenAI On Your Data Python & REST API reference
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI On Your Data Python & REST API.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 07/18/2024
author: aahill
ms.author: aahi
recommendations: false
ms.custom: devx-track-python
---

# Azure OpenAI On Your Data API Reference

This article provides reference documentation for Python and REST for the new Azure OpenAI On Your Data API. The latest API version is `2024-05-01-preview` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-05-01-preview).

> [!NOTE]
> Since API version `2024-02-15-preview` we introduced the following breaking changes comparing to earlier API versions:
> * The API path is changed from `/extensions/chat/completions` to `/chat/completions`.
> * The naming convention of property keys and enum values is changed from camel casing to snake casing. Example: `deploymentName` is changed to `deployment_name`.
> * The data source type `AzureCognitiveSearch` is changed to `azure_search`.
> * The citations and intent is moved from assistant message's context tool messages to assistant message's context root level with explicit [schema defined](#context).

```http
POST {endpoint}/openai/deployments/{deployment-id}/chat/completions?api-version={api-version}
```

**Supported versions**
* `2024-02-15-preview` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-02-15-preview/inference.json).
* `2024-02-01` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/stable/2024-02-01).
* `2024-05-01-preview` [Swagger spec](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-05-01-preview)

> [!NOTE]
> [Azure Machine learning indexes](./azure-machine-learning.md), [Pinecone](./pinecone.md), and [Elasticsearch](./elasticsearch.md) are supported as a preview.

## URI parameters

|Name               | In   | Type     | Required | Description                                                                           |
|---                |---   |---       |---       |---                                                                                    |
|```deployment-id```|path  |string    |True      |Specifies the chat completions model deployment name to use for this request.          |
|```endpoint```     |path  |string    |True      |Azure OpenAI endpoints. For example: `https://{YOUR_RESOURCE_NAME}.openai.azure.com`   |
|```api-version```  |query |string    |True      |The API version to use for this operation.                                             |

## Request body

The request body inherits the same schema of chat completions API request. This table shows the parameters unique for Azure OpenAI On Your Data.

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `data_sources` | [DataSource](#data-source)[] | True | The configuration entries for Azure OpenAI On Your Data. There must be exactly one element in the array. If `data_sources` is not provided, the service uses chat completions model directly, and does not use Azure OpenAI On Your Data. When you specify the `data_sources` parameter, you won't be able to to use the `logprobs` or `top_logprobs` parameters. |

## Response body

The response body inherits the same schema of chat completions API response. The [response chat message](#chat-message) has a `context` property, which is added for Azure OpenAI On Your Data.

## Chat message

The response assistant message schema inherits from the chat completions assistant [chat message](../reference.md#chatmessage), and is extended with the property `context`.

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `context` | [Context](#context) | False | Represents the incremental steps performed by the Azure OpenAI On Your Data while processing the request, including the retrieved documents. |

## Context
|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `citations` | [Citation](#citation)[] | False | The data source retrieval result, used to generate the assistant message in the response. Clients can render references from the citations. |
| `intent` | string | False | The detected intent from the chat history. Passing back the previous intent is no longer needed. Ignore this property. |
| `all_retrieved_documents` | [Retrieved documents](#retrieved-documents)[] | False | All the retrieved documents. |


## Citation

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `content` | string | True | The content of the citation.|
| `title` | string | False | The title of the citation.|
| `url` | string | False | The URL of the citation.|
| `filepath` | string | False | The file path of the citation.|
| `chunk_id` | string | False | The chunk ID of the citation.|

## Retrieved documents

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `search_queries` | string[] | True | The search queries used to retrieve the document. |
| `data_source_index` | integer | True | The index of the data source. |
| `original_search_score` | double | True | The original search score of the retrieved document. |
| `rerank_score` | double | False | The rerank score of the retrieved document. |
| `filter_reason` | string | False | Represents the rationale for filtering the document. If the document does not undergo filtering, this field will remain unset. Will be `score` if the document is filtered by original search score threshold defined by `strictness`. Will be `rerank` if the document is not filtered by original search score threshold, but is filtered by rerank score and `top_n_documents`. |

## Data source

This list shows the supported data sources.

* [Azure AI Search](./azure-search.md)
* [Azure Cosmos DB for MongoDB vCore](./cosmos-db.md)
* [Azure Machine Learning index (preview)](./azure-machine-learning.md)
* [Elasticsearch (preview)](./elasticsearch.md)
* [Pinecone (preview)](./pinecone.md)

## Examples

This example shows how to pass conversation history for better results.

Prerequisites:
* Configure the role assignments from Azure OpenAI system assigned managed identity to Azure search service. Required roles: `Search Index Data Reader`, `Search Service Contributor`.
* Configure the role assignments from the user to the Azure OpenAI resource. Required role: `Cognitive Services OpenAI User`.
* Install [Az CLI](/cli/azure/install-azure-cli), and run `az login`.
* Define the following environment variables: `AzureOpenAIEndpoint`, `ChatCompletionsDeploymentName`,`SearchEndpoint`, `SearchIndex`.
```bash
export AzureOpenAIEndpoint=https://example.openai.azure.com/
export ChatCompletionsDeploymentName=turbo
export SearchEndpoint=https://example.search.windows.net
export SearchIndex=example-index
```


# [Python 1.x](#tab/python)

Install the latest pip packages `openai`, `azure-identity`.

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = os.environ.get("AzureOpenAIEndpoint")
deployment = os.environ.get("ChatCompletionsDeploymentName")
search_endpoint = os.environ.get("SearchEndpoint")
search_index = os.environ.get("SearchIndex")

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)

completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "Who is DRI?",
        },
        {
            "role": "assistant",
            "content": "DRI stands for Directly Responsible Individual of a service. Which service are you asking about?"
        },
        {
            "role": "user",
            "content": "Opinion mining service"
        }
    ],
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_endpoint,
                    "index_name": search_index,
                    "authentication": {
                        "type": "system_assigned_managed_identity"
                    }
                }
            }
        ]
    }
)

print(completion.model_dump_json(indent=2))

# render the citations

content = completion.choices[0].message.content
context = completion.choices[0].message.context
for citation_index, citation in enumerate(context["citations"]):
    citation_reference = f"[doc{citation_index + 1}]"
    url = "https://example.com/?redirect=" + citation["url"] # replace with actual host and encode the URL
    filepath = citation["filepath"]
    title = citation["title"]
    snippet = citation["content"]
    chunk_id = citation["chunk_id"]
    replaced_html = f"<a href='{url}' title='{title}\n{snippet}''>(See from file {filepath}, Part {chunk_id})</a>"
    content = content.replace(citation_reference, replaced_html)
print(content)
```

# [REST](#tab/rest)

```bash
az rest --method POST \
 --uri $AzureOpenAIEndpoint/openai/deployments/$ChatCompletionsDeploymentName/chat/completions?api-version=2024-05-01-preview \
 --resource https://cognitiveservices.azure.com/ \
 --body \
'
{
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": "'$SearchEndpoint'",
                "index_name": "'$SearchIndex'",
                "authentication": {
                    "type": "system_assigned_managed_identity"
                }
            }
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "Who is DRI?"
        },
        {
            "role": "assistant",
            "content": "DRI stands for Directly Responsible Individual of a service. Which service are you asking about?"
        },
        {
            "role": "user",
            "content": "Opinion mining service"
        }
    ]
}
'
```

---
