---
title: How to deploy Cohere Rerank models as serverless APIs
titleSuffix: Azure AI Foundry
description: Learn to deploy and use Cohere Rerank models with Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 02/18/2025
ms.reviewer: shubhiraj
ms.author: mopeakande
author: msakande
ms.custom: references_regions, build-2024, ignite-2024
---

# How to deploy Cohere Rerank models with Azure AI Foundry

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn about the Cohere Rerank models, how to use Azure AI Foundry to deploy them as serverless APIs with pay-as-you-go token-based billing, and how to work with the deployed models.

[!INCLUDE [models-preview](../includes/models-preview.md)]

## Cohere Rerank models

Cohere offers rerank models in [Azure AI Foundry](https://ai.azure.com). These models are available in the model catalog for deployment as serverless APIs:

- Cohere Rerank v3.5
- Cohere Rerank v3 - English
- Cohere Rerank v3 - Multilingual

You can browse the Cohere family of models in the [Model Catalog](model-catalog.md) by filtering on the Cohere collection.

# [Cohere Rerank v3.5](#tab/cohere-rerank-3-5)

Cohere Rerank 3.5 provides a significant boost to the relevancy of search results. This AI model, also known as a cross-encoder, precisely sorts lists of documents according to their semantic similarity to a provided query. This action allows information retrieval systems to go beyond keyword search, and also outperform traditional embedding models, surfacing the most contextually relevant data within end-user applications.  

Businesses use Cohere Rerank 3.5 to improve their enterprise search and retrieval-augmented generation (RAG) applications across more than 100 languages. With just a few lines of code, you can add the model to existing systems to boost the accuracy of search results. The model is also uniquely performant at searching across complex enterprise data such as JSON, code, and tables. Further, the model is capable of reasoning through hard questions which other search systems fail to understand.

- Context window of the model is 4,096 tokens
- Max query length is 4,096 tokens

#### Pricing for Cohere Rerank v3.5

*Queries*, not to be confused with a user's query, is a pricing meter that refers to the cost associated with the tokens used as input for inference of a Cohere Rerank model. Cohere counts a single search unit as a query with up to 100 documents to be ranked. Documents longer than 500 tokens when including the length of the search query are split up into multiple chunks, where each chunk counts as a single document.

# [Cohere Rerank v3 - English](#tab/cohere-rerank-3-en)

Cohere Rerank English is a reranking model used for semantic search and retrieval-augmented generation (RAG). Rerank enables you to significantly improve search quality by augmenting traditional keyword-based search systems with a semantic-based reranking system that can contextualize the meaning of a user's query beyond keyword relevance. Cohere's Rerank delivers higher quality results than embedding-based search, lexical search, and even hybrid search, and it requires only adding a single line of code into your application.

Use Rerank as a ranker after initial retrieval. In other words, after an initial search system finds the top 100 most relevant documents for a larger corpus of documents.

Rerank supports JSON objects as documents where users can specify, at query time, the fields (keys) to use for semantic search. Some other attributes of Rerank include:

- Context window of the model is 4,096 tokens
- The max query length is 2,048 tokens

Rerank English works well for code retrieval, semi-structured data retrieval, and long context.

#### Pricing for Cohere Rerank v3 English

*Queries*, not to be confused with a user's query, is a pricing meter that refers to the cost associated with the tokens used as input for inference of a Cohere Rerank model. Cohere counts a single search unit as a query with up to 100 documents to be ranked. Documents longer than 4096 tokens when including the length of the search query are split up into multiple chunks, where each chunk counts as a single document.

# [Cohere Rerank v3 - Multilingual](#tab/cohere-rerank-3-multi)

Cohere Rerank Multilingual is a reranking model used for semantic search and retrieval-augmented generation (RAG). Rerank Multilingual supports more than 100 languages and can be used to search within a language (for example, to search with a French query on French documents) and across languages (for example, to search with an English query on Chinese documents). Rerank enables you to significantly improve search quality by augmenting traditional keyword-based search systems with a semantic-based reranking system that can contextualize the meaning of a user's query beyond keyword relevance. Cohere's Rerank delivers higher quality results than embedding-based search, lexical search, and even hybrid search, and it requires only adding a single line of code into your application.

Use Rerank as a ranker after initial retrieval. In other words, after an initial search system finds the top 100 most relevant documents for a larger corpus of documents.

Rerank supports JSON objects as documents where users can specify, at query time, the fields (keys) to use for semantic search. Some other attributes of Rerank Multilingual include:

- Context window of the model is 4,096 tokens
- The max query length is 2,048 tokens

Rerank multilingual performs well on multilingual benchmarks such as Miracl.

#### Pricing for Cohere Rerank v3 Multilingual

*Queries*, not to be confused with a user's query, is a pricing meter that refers to the cost associated with the tokens used as input for inference of a Cohere Rerank model. Cohere counts a single search unit as a query with up to 100 documents to be ranked. Documents longer than 4096 tokens when including the length of the search query are split up into multiple chunks, where each chunk counts as a single document.

---

## Deploy Cohere Rerank models as serverless APIs

Certain models in the model catalog can be deployed as a serverless API with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. This deployment option doesn't require quota from your subscription.

You can deploy the previously mentioned Cohere models as a service with pay-as-you-go billing. Cohere offers these models through Microsoft Azure Marketplace and can change or update the terms of use and pricing of these models.

### Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry hub](../how-to/create-azure-ai-resource.md). The serverless API model deployment offering for Cohere Rerank is only available with hubs created in specific regions. For a list of regions that are available for each of the Cohere models that support serverless API endpoint deployments, see [Region availability for models in serverless API endpoints](deploy-models-serverless-availability.md#cohere-models).

- An [Azure AI Foundry project](../how-to/create-projects.md).

- Azure role-based access controls are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-studio.md).

### Create a new deployment 
The following steps demonstrate the deployment of Cohere Rerank v3.5, but you can use the same steps to deploy the other Cohere rerank models by replacing the model name.

To create a deployment:

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. Select the model card of the model you want to deploy. In this article, you select **Cohere-rerank-v3-5** to open the Model Details page.
1. Select **Deploy** to open a serverless API deployment window for the model.
1. Alternatively, you can initiate a deployment from your project in the Azure AI Foundry portal as follows:
    1. From the left sidebar of your project, select **Models + Endpoints**.
    1. Select **+ Deploy model** > **Deploy base model**.
    1. Search for and select **Cohere-rerank-v3-5** to open the Model Details page.
    1. Select **Confirm** to open a serverless API deployment window for the model.
1. In the deployment wizard, select the link to **Azure Marketplace Terms** to learn more about the terms of use.
1. Select the **Pricing and terms** tab to learn about pricing for the selected model.
1. Select the **Subscribe and Deploy** button. If it's your first time deploying the model in the project, you have to subscribe your project for the particular offering.

    > [!NOTE]
    > This step requires that your account has the **Azure AI Developer role** permissions on the resource group, as listed in the prerequisites. Models that are offered by non-Microsoft providers (for example, Cohere models) are billed through Azure Marketplace. For such models, you're required to subscribe your project to the particular model offering. Each project has its own subscription to the particular Azure Marketplace offering of the model, which allows you to control and monitor spending. Currently, you can have only one deployment for each model within a project.

1. Once you subscribe the project for the particular Azure Marketplace offering, subsequent deployments of the _same_ offering in the _same_ project don't require subscribing again. If this scenario applies to you, there's a **Continue to deploy** option to select.

1. Give the deployment a name. This name becomes part of the deployment API URL. This URL must be unique in each Azure region.

1. Select **Deploy**. Wait until the deployment is ready and you're redirected to the **Model deployments** page.
1. On the Deployments page, select the deployment, and note the endpoint's **Target** URL and the Secret **Key**. For more information on using the APIs, see the [reference](#rerank-api-reference-for-cohere-rerank-models-deployed-as-a-service) section.
1. [!INCLUDE [Find your deployment details](../includes/find-deployments.md)]

To learn about billing for the Cohere models deployed as a serverless API with pay-as-you-go token-based billing, see [Cost and quota considerations for Cohere models deployed as a service](#cost-and-quota-considerations-for-models-deployed-as-a-service).

### Consume the Cohere Rerank model as a service

Cohere Rerank models deployed as serverless APIs can be consumed using the Rerank API.

1. From the left sidebar of your project, select **Models + Endpoints**.

1. Find and select the deployment you created.

1. Copy the **Target** URL and the **Key** value.

Cohere currently exposes v2/rerank for inference with Rerank v3.5, Rerank v3 - English, and Rerank v3 - Multilingual models schema. For more information on using the APIs, see the [reference](#rerank-api-reference-for-cohere-rerank-models-deployed-as-a-service) section.

## Rerank API reference for Cohere Rerank models deployed as a service

The native **Cohere Rerank API v2** endpoint on `https://api.cohere.com/v2/rerank` supports inference with Cohere Rerank v3.5, Cohere Rerank v3 - English, and Cohere Rerank v3 - Multilingual.

The native **Cohere Rerank API v1** endpoint on `https://api.cohere.com/v1/rerank` supports inference with Cohere Rerank v3 - English and Cohere Rerank v3 - Multilingual.


### v2/rerank request schema

| Property | Type | Default | Description |
| ------------ | -------- | ----------- | ------------- |
| `query` | string | Required | The search query. |
| `documents` | List of strings | Required | A list of texts that will be compared to the query. For optimal performance we recommend against sending more than 1,000 documents in a single request.<br><br>Note: long documents will automatically be truncated to the value of **max_tokens_per_doc**.<br><br>Note: structured data should be formatted as YAML strings for best performance. |
| top_n | integer | Optional | Limits the number of returned rerank results to the specified value. If not passed, all the rerank results will be returned. |
| `return_documents` | boolean | `FALSE` | If FALSE, returns results without the doc text - the API returns a list of {index, relevance_score} where index is inferred from the list passed into the request.<br><br>If TRUE, returns results with the doc text passed in - the API returns an ordered list of {index, text, relevance_score} where index + text refers to the list passed into the request. |
| `max_chunks_per_doc` | integer | Optional | Defaults to 4096. Long documents will be automatically truncated to the specified number of tokens. |
| `Model` | string | Required | The identifier of the model to use, for example, rerank-v3.5. |


### v2/rerank response schema

Response fields are fully documented on [Cohere's Rerank API reference](https://docs.cohere.com/reference/rerank). The response payload is a dictionary with the following fields:

| Key | Type | Description |
| ------------ | -------- | ----------- |
| `id`  | string | Optional |
| `results` | List of objects | An ordered list of ranked documents |
| `meta` | object | document is described by an object that includes api_version and version and, optionally, is_deprecated and is_experimental. |
| `Billed units` | object | Described by an object that are all optionally images, input_tokens, output_tokens, search_units, and classifications |
| `tokens` | object | Described optionally as input_tokens which are the number of tokens used as input to the model and output_tokens which are the number of tokens produced by the model. |
| `warnings` | List of strings | Optional |

The `results` object is a dictionary with the following fields:

| Key | Type | Description |
| ------------ | -------- | ----------- |
| `index` | integer | Corresponds to the index in the original list of documents to which the ranked document belongs. (i.e. if the first value in the results object has an index value of 3, it means in the list of documents passed in, the document at index=3 had the highest relevance) |
| `relevance_score` | double | Relevance scores are normalized to be in the range \[0, 1\]. Scores close to 1 indicate a high relevance to the query, and scores closer to 0 indicate low relevance. It isn't accurate to assume a score of 0.9 means the document is 2x more relevant than a document with a score of 0.45 |
| `document` | object | If return_documents is set as false this returns none, if true it returns the documents passed in |

### Examples using Cohere Rerank API v2

#### Request example

```python

import cohere

co = cohere.ClientV2()

docs = [
"Carson City is the capital city of the American state of Nevada.",
"The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean. Its capital is Saipan.",
"Capitalization or capitalisation in English grammar is the use of a capital letter at the start of a word. English usage varies from capitalization in other languages.",
"Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district.",
"Capital punishment has existed in the United States since beforethe United States was a country. As of 2017, capital punishment is legal in 30 of the 50 states.",
]

response = co.rerank(
    model = "rerank-v3.5",
    query = "What is the capital of the United States?",
    documents = docs,
    top_n = 3,
)

print(response)
```

#### Response example

```json
    {
        "results": [
            {
                "index": 3,
                "relevance_score": 0.999071
            },
            {
                "index": 4,
                "relevance_score": 0.7867867
            },
            {
                "index": 0,
                "relevance_score": 0.32713068
            }
        ],
        "id": "00001111-aaaa-2222-bbbb-3333cccc4444",
        "meta": {
            "api_version": {
            "version": "2",
            "is_experimental": false
            },
        "billed_units": {
            "search_units": 1
            }
        }
    }

```


### v1/rerank request

```json

    POST /v1/rerank HTTP/1.1
    Host: <DEPLOYMENT_URI>
    Authorization: Bearer <TOKEN>
    Content-type: application/json
```

### v1/rerank request schema

Cohere Rerank v3 - English and Rerank v3 - Multilingual accept the following parameters for a v1/rerank API call:

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `query` | string | Required | The search query. |
| `documents` | array | None | A list of document objects or strings to rerank. |
| `top_n` | integer | Length of documents | The number of most relevant documents or indices to return. |
| `return_documents` | boolean | `FALSE` | If FALSE, returns results without the doc text - the API returns a list of {index, relevance_score} where index is inferred from the list passed into the request.<br><br>If TRUE, returns results with the doc text passed in - the API returns an ordered list of {index, text, relevance_score} where index + text refers to the list passed into the request. |
| `max_chunks_per_doc` | integer | None | The maximum number of chunks to produce internally from a document. |
| `rank_fields` | array of strings | None | If a JSON object is provided, you can specify which keys you would like to consider for reranking. The model reranks based on the order of the fields passed in (for example, rank_fields=\['title','author','text'\] reranks, using the values in title, author, and text in that sequence. If the length of title, author, and text exceeds the context length of the model, the chunking won't reconsider earlier fields).<br><br>If not provided, the model uses the default text field for ranking. |

### v1/rerank response schema

Response fields are fully documented on [Cohere's Rerank API reference](https://docs.cohere.com/reference/rerank). The response payload is a dictionary with the following fields:

| Key | Type | Description |
| --- | --- | --- |
| `id`  | string | An identifier for the response. |
| `results` | array of objects | An ordered list of ranked documents, where each document is described by an object that includes index and relevance_score and, optionally, text. |
| `meta` | array of objects | An optional meta object containing a list of warning strings. |

The `results` object is a dictionary with the following fields:

| Key | Type | Description |
| --- | --- | --- |
| `document` | object | The document objects or strings that were reranked. |
| `index` | integer | The index in the original list of documents to which the ranked document belongs. For example, if the first value in the results object has an index value of 3, it means in the list of documents passed in, the document at index=3 had the highest relevance. |
| `relevance_score` | float | Relevance scores are normalized to be in the range \[0, 1\]. Scores close to one indicate a high relevance to the query, and scores close to zero indicate low relevance. A score of 0.9 _doesn't_ necessarily mean that a document is twice as relevant as another with a score of 0.45. |

### Examples using Cohere Rerank API v1


#### Request example

```json
    {
        "query": "What is the capital of the United States?",
        "rank_fields": ["Title", "Content"],
        "documents": [
            {"Title": "Facts about Carson City", "Content": "Carson City is the capital city of the American state of Nevada. "}, 
            {"Title": "North Dakota", "Content" : "North Dakota is a state in the United States. 672,591 people lived in North Dakota in the year 2010. The capital and seat of government is Bismarck."}, 
            {"Title": "Micronesia", "Content" : "Micronesia, officially the Federated States of Micronesia, is an island nation in the Pacific Ocean, northeast of Papua New Guinea. The country is a sovereign state in free association with the United States. The capital city of Federated States of Micronesia is Palikir."}
        ],
        "top_n": 3
    }
```

#### Response example

```json
    {
        "id": "571e6744-3074-457f-8935-08646a3352fb",
        "results": [
            {
                "document": {
                    "Content": "Washington, D.C. (also known as simply Washington or D.C., and officially as the District of Columbia) is the capital of the United States. It is a federal district. The President of the USA and many major national government offices are in the territory. This makes it the political center of the United States of America.",
                    "Title": "Details about Washington D.C"
                },
                "index": 0,
                "relevance_score": 0.98347044
            },
            {
                "document": {
                    "Content": "Carson City is the capital city of the American state of Nevada. ",
                    "Title": "Facts about Carson City"
                },
                "index": 1,
                "relevance_score": 0.07172112
            },
            {
                "document": {
                    "Content": "Micronesia, officially the Federated States of Micronesia, is an island nation in the Pacific Ocean, northeast of Papua New Guinea. The country is a sovereign state in free association with the United States. The capital city of Federated States of Micronesia is Palikir.",
                    "Title": "Micronesia"
                },
                "index": 3,
                "relevance_score": 0.05281402
            },
            {
                "document": {
                    "Content": "North Dakota is a state in the United States. 672,591 people lived in North Dakota in the year 2010. The capital and seat of government is Bismarck.",
                    "Title": "North Dakota"
                },
                "index": 2,
                "relevance_score": 0.03138043
            }
        ]
    }
```

#### More inference examples

| Package | Sample Notebook |
| --- | --- |
| CLI using CURL and Python web requests | [cohere-rerank.ipynb](https://aka.ms/samples/cohere-rerank/webrequests) |
| LangChain | [langchain.ipynb](https://aka.ms/samples/cohere-rerank/langchain) |
| Cohere SDK | [cohere-sdk.ipynb](https://aka.ms/samples/cohere-rerank/cohere-python-sdk) |

## Cost and quota considerations for models deployed as a service

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

Cohere models deployed as serverless APIs with pay-as-you-go billing are offered by Cohere through Azure Marketplace and integrated with Azure AI Foundry for use. You can find Azure Marketplace pricing when deploying the model.

Each time a project subscribes to a given offer from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [monitor costs for models offered throughout Azure Marketplace](./costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

## Related content

- [What is Azure AI Foundry?](../what-is-ai-studio.md)
- [Azure AI FAQ article](../faq.yml)
- [Region availability for models in serverless API endpoints](deploy-models-serverless-availability.md)
