---
title: Azure OpenAI on your Mongo DB Atlas data Python & REST API reference
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI on your Mongo DB Atlas data with Python & REST API.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: reference
ms.date: 02/06/2026
author: aahill
ms.author: aahi
recommendations: false
ms.custom: devx-track-python, ignite-2024
---

# Data source - Mongo DB Atlas

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [on-your-data-deprecation](../includes/on-your-data-deprecation.md)]

The configurable options of Mongo DB Atlas when using Azure OpenAI On Your Data. This data source is supported starting in API version `2024-08-01`.


|Name | Type | Required | Description |
|--- | --- | --- | --- |
|`parameters`| [Parameters](#parameters)| True| The parameters to use when configuring Mongo DB Atlas.|
| `type`| string| True | Must be `mongo_db`. |

## Parameters

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `authentication` | object | True | The [authentication options](#authentication) for Azure OpenAI On Your Data when using a username and a password. |
| `app_name` | string | True | The name of the Mongo DB Atlas Application. |
| `collection_name` | string | True | The name of the Mongo DB Atlas Collection. |
| `database_name` | string | True | The name of the Mongo DB Atlas database. |
| `endpoint` | string | True | The name of the Mongo DB Atlas cluster endpoint. |
| `embedding_dependency` | One of [DeploymentNameVectorizationSource](#deployment-name-vectorization-source), [EndpointVectorizationSource](#endpoint-vectorization-source) | True | The embedding dependency for vector search.|
| `fields_mapping` | object | True | [Settings](#field-mapping-options) to control how fields are processed when using a configured Mongo DB Atlas resource. |
| `index_name` | string | True | The name of the Mongo DB Atlas index.|
| `top_n_documents` | integer | False | The configured top number of documents to feature for the configured query.|
| `max_search_queries` | integer | False | The max number of rewritten queries should be sent to search provider for one user message. If not specified, the system will decide the number of queries to send.|
| `allow_partial_result` | boolean | False | If specified as true, the system will allow partial search results to be used and the request fails if all the queries fail. If not specified, or specified as false, the request will fail if any search query fails.|
| `in_scope` | boolean | False | Whether queries should be restricted to use indexed data. |
| `strictness` | integer | False | The configured strictness of the search relevance filtering, from 1 to 5. The higher the  strictness, the higher precision but lower recall of the answer. |
| `include_contexts` | array | False | The included properties of the output context. If not specified, the default value is `citations` and `intent`. Valid properties are `all_retrieved_documents`, `citations` and `intent`. |

## Authentication

The authentication options for Azure OpenAI On Your Data when using a username and a password.

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `type` | string | True | Must be `username_and_password`. |
| `username` | string | True | The username to use for authentication. |
| `password` | string | True | The password to use for authentication. |

## Deployment name vectorization source

The details of the vectorization source, used by Azure OpenAI On Your Data when applying vector search. This vectorization source is based on an internal embeddings model deployment name in the same Azure OpenAI resource. This vectorization source enables you to use vector search without Azure OpenAI api-key and without Azure OpenAI public network access.

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `deployment_name`|string|True|The embedding model deployment name within the same Azure OpenAI resource. |
| `type`|string|True| Must be `deployment_name`.|

## Endpoint vectorization source

The details of the vectorization source, used by Azure OpenAI On Your Data when applying vector search. This vectorization source is based on the Azure OpenAI embedding API endpoint.

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `endpoint`|string|True|Specifies the resource endpoint URL from which embeddings should be retrieved. It should be in the format of `https://{YOUR_RESOURCE_NAME}.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/embeddings`. The api-version query parameter isn't allowed.|
| `authentication`| [ApiKeyAuthenticationOptions](#authentication)|True | Specifies the authentication options to use when retrieving embeddings from the specified endpoint.|
| `type`|string|True| Must be `endpoint`.|

## Field mapping options

Optional settings to control how fields are processed when using a configured Mongo DB Atlas resource.

|Name | Type | Required | Description |
|--- | --- | --- | --- |
| `content_fields`|string[] |True| The names of index fields that should be treated as content. |
| `vector_fields`|string[] |True| The names of fields that represent vector data. |
| `title_field`|string |False | The name of the index field to use as a title. |
| `url_field`|string |False | The name of the index field to use as a URL. |
| `filepath_field`|string |False | The name of the index field to use as a filepath. |
| `content_fields_separator` | string | False | The separator pattern that content fields should use.|

## Examples


# [Python 1.x](#tab/python)

Install the latest pip packages `openai`, `azure-identity`.

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = os.environ.get("AzureOpenAIEndpoint")
deployment = os.environ.get("ChatCompletionsDeploymentName")
index_name = os.environ.get("IndexName")
key = os.environ.get("Key")
embedding_name = os.environ.get("EmbeddingName")
embedding_type = os.environ.get("EmbeddingType")

# Additional variables for Mongo DB Atlas
mongo_db_username = os.environ.get("MongoDBUsername")
mongo_db_password = os.environ.get("MongoDBPassword")
mongo_db_endpoint = os.environ.get("MongoDBEndpoint")
mongo_db_app_name = os.environ.get("MongoDBAppName")
mongo_db_database_name = os.environ.get("MongoDBName")
mongo_db_collection = os.environ.get("MongoDBCollection")
mongo_db_index = os.environ.get("MongoDBIndex")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

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
    ],
    extra_body={
        "data_sources": [
            {
                "type": "mongo_db",
                "parameters": {
                "authentication": {
                    "type": "username_and_password",
                    "username": mongo_db_username,
                    "password": mongo_db_password
                },
                "endpoint": mongo_db_endpoint,
                "app_name": mongo_db_app_name,
                "database_name": mongo_db_database_name,
                "collection_name": mongo_db_collection,
                "index_name": mongo_db_index,
                "embedding_dependency": {
                    "type": embedding_type,
                    "deployment_name": embedding_name
                },
                "fields_mapping": {
                    "content_fields": [
                    "content"
                    ],
                    "vector_fields": [
                    "contentvector"
                    ]
                }
                }
            }
        ]
    }
)

print(completion.model_dump_json(indent=2))

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
        "type": "mongo_db",
        "parameters": {
        "authentication": {
            "type": "username_and_password",
            "username": "<username>",
            "password": "<password>"
        },
        "endpoint": "<endpoint_name>",
        "app_name": "<application name>",
        "database_name": "sampledb",
        "collection_name": "samplecollection",
        "index_name": "sampleindex",
        "embedding_dependency": {
            "type": "deployment_name",
            "deployment_name": "{embedding deployment name}"
        },
        "fields_mapping": {
            "content_fields": [
            "content"
            ],
            "vector_fields": [
            "contentvector"
            ]
        }
        }
    }
    ]
}
'
```

---
