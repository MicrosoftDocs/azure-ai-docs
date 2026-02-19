---
title: Configure Vectorizer
titleSuffix: Azure AI Search
description: Configure a vectorizer in your Azure AI Search index to convert text to vectors at query time using Azure OpenAI or custom embedding models.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - build-2024
ms.topic: how-to
ms.date: 02/19/2026
---

# Configure a vectorizer in a search index

In Azure AI Search, a *vectorizer* converts text or images into vectors during query execution. Instead of passing a precomputed vector with each query, the search service handles the embedding call for you.

A vectorizer is defined in a search index and assigned to vector fields through a vector profile. At query time, the vectorizer calls an embedding model to generate a vector from your query input. You must use the same embedding model for both indexing and queries.

To add a vectorizer, use the index designer in Azure portal, [Indexes - Create Or Update](/rest/api/searchservice/indexes/create-or-update) (REST API), or an Azure SDK package that supports this capability. A vectorizer is generally available as long as you use a generally available skill–vectorizer pair.

> [!TIP]
> A vectorizer handles query-time vectorization. To also vectorize content during indexing, set up an indexer and skillset with an embedding skill. For more information, see [Using integrated vectorization during indexing](vector-search-integrated-vectorization.md#using-integrated-vectorization-during-indexing).

## Prerequisites

+ An [index with searchable vector fields](vector-search-how-to-create-index.md) on your Azure AI Search service.

+ (Optional) [Diagnostic logging enabled](search-monitor-enable-logging.md) on your search service to confirm vector query execution.

+ A [supported embedding model](#choose-an-embedding-model).

+ Permissions to update the search index. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ Permissions to use the embedding model. For example, with Azure OpenAI, the caller must have [**Cognitive Services OpenAI User**](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles) permissions. You can also use an API key.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) to follow the programmatic examples in this article.

## Choose an embedding model

Azure AI Search offers several types of vectorizers. You must use the [same embedding model for indexing and queries](vector-search-integrated-vectorization.md#using-integrated-vectorization-in-queries), so each vectorizer has a corresponding skill. The skill generates embeddings during indexing, while the vectorizer uses the same model to generate embeddings at query time.

The following table lists the vectorizers and their supported models, model providers, and associated skills.

| Vectorizer | Model names | Model provider | Associated skill |
|-----------------|------------|----------------|------------------|
| [Azure OpenAI](vector-search-vectorizer-azure-open-ai.md) | text-embedding-ada-002<br>text-embedding-3-large<br>text-embedding-3-small | Azure OpenAI in Foundry Models | [Azure OpenAI Embedding](cognitive-search-skill-azure-openai-embedding.md) |
| [Microsoft Foundry model catalog](vector-search-vectorizer-azure-machine-learning-ai-studio-catalog.md) | Cohere-embed-v3-english<br>Cohere-embed-v3-multilingual<br>Cohere-embed-v4 <sup>1</sup> | Microsoft Foundry model catalog | [AML](cognitive-search-aml-skill.md) |
| [Azure Vision](vector-search-vectorizer-ai-services-vision.md) | [Multimodal embeddings 4.0 API](/azure/ai-services/computer-vision/concept-image-retrieval) | Azure Vision in Foundry Tools (via Microsoft Foundry resource) | [Azure Vision multimodal embeddings](cognitive-search-skill-vision-vectorize.md) |
| [Custom Web API](vector-search-vectorizer-custom-web-api.md) | Any embedding model | Hosted externally | [Custom Web API](cognitive-search-custom-skill-web-api.md) |

<sup>1</sup> You can only specify `embed-v-4-0` programmatically through the [AML skill](cognitive-search-aml-skill.md) or [Microsoft Foundry model catalog vectorizer](vector-search-vectorizer-azure-machine-learning-ai-studio-catalog.md), not through the Azure portal. However, you can use the portal to manage the skillset or vectorizer afterward.

## Define a vectorizer using a wizard

The **Import data (new)** wizard in the Azure portal can read files from Azure Blob Storage, create an index with chunked and vectorized fields, and add a vectorizer. By design, the wizard-generated vectorizer is set to the same embedding model used to index the blob content.

To create a sample index with a vectorizer using the wizard:

1. [Upload files](/azure/storage/blobs/storage-quickstart-blobs-portal) to a container in Azure Storage. We used [small text files from NASA's Earth at Night e-book](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-txt-10) to test these instructions on a free search service.

1. Run the [**Import data (new)** wizard](search-get-started-portal-import-vectors.md). Choose the blob container for the data source.

   :::image type="content" source="media/vector-search-how-to-configure-vectorizer/connect-to-data.png" lightbox="media/vector-search-how-to-configure-vectorizer/connect-to-data.png" alt-text="Screenshot of the connect to your data page.":::

1. Choose a vectorizer kind and, if applicable, a model deployment. This example uses Azure OpenAI and a **text-embedding-ada-002** deployment.

   :::image type="content" source="media/vector-search-how-to-configure-vectorizer/vectorize-enrich-data.png" lightbox="media/vector-search-how-to-configure-vectorizer/vectorize-enrich-data.png" alt-text="Screenshot of the vectorize and enrich data page for configuring a vectorizer embedding model.":::

1. After the wizard finishes and all indexer processing is complete, you should have an index with a searchable vector field. The field's JSON definition looks like this:

   ```json
    {
        "name": "vector",
        "type": "Collection(Edm.Single)",
        "searchable": true,
        "retrievable": true,
        "dimensions": 1536,
        "vectorSearchProfile": "vector-nasa-ebook-text-profile"
    }
   ```

    You should also have a vector profile and vectorizer. Their JSON definitions look like this:

   ```json
   "profiles": [
      {
        "name": "vector-nasa-ebook-text-profile",
        "algorithm": "vector-nasa-ebook-text-algorithm",
        "vectorizer": "vector-nasa-ebook-text-vectorizer"
      }
    ],
    "vectorizers": [
      {
        "name": "vector-nasa-ebook-text-vectorizer",
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "https://my-fake-azure-openai-resource.openai.azure.com",
          "deploymentId": "text-embedding-ada-002",
          "modelName": "text-embedding-ada-002",
          "apiKey": "0000000000000000000000000000000000000",
          "authIdentity": null
        },
        "customWebApiParameters": null
      }
    ]
    ```

1. Skip ahead to [test your vectorizer](#test-a-vectorizer) for text-to-vector conversion during query execution.

## Define a vectorizer and vector profile manually

If you didn't use the wizard or want to add a vectorizer to an existing index, you can define a vectorizer and vector profile manually. A vector profile links a vectorizer to one or more vector fields and specifies the vector search algorithm used for navigation structures.

To define a vectorizer and vector profile in an existing index:

1. Open a `.rest` or `.http` file in Visual Studio Code.

1. Provide the index definition using [Indexes - Create Or Update](/rest/api/searchservice/indexes/create-or-update) (REST API). Replace the service name, index name, and [admin API key](search-security-api-keys.md#find-existing-keys) with your own values.

   ```http
   PUT https://my-search-service.search.windows.net/indexes/my-index?api-version=2025-09-01 HTTP/1.1
   Content-Type: application/json
   api-key: <your-admin-api-key>
   ```

1. Add a `vectorizers` section to the index definition. This section specifies connection information to a deployed embedding model. The following example includes both Azure OpenAI and Custom Web API for comparison.

    ```json
      "vectorizers": [
        {
          "name": "my_azure_open_ai_vectorizer",
          "kind": "azureOpenAI",
          "azureOpenAIParameters": {
            "resourceUri": "https://url.openai.azure.com",
            "deploymentId": "text-embedding-ada-002",
            "modelName": "text-embedding-ada-002",
            "apiKey": "mytopsecretkey"
          }
        },
        {
          "name": "my_custom_vectorizer",
          "kind": "customWebApi",
          "customVectorizerParameters": {
            "uri": "https://my-endpoint",
            "authResourceId": null,
            "authIdentity": null
          }
        }
      ]
    ```

1. Add a `profiles` section that references the vectorizer and a [vector search algorithm](vector-search-ranking.md), which is used to create navigation structures.

    ```json
    "profiles": [ 
        { 
            "name": "my_vector_profile", 
            "algorithm": "my_hnsw_algorithm", 
            "vectorizer":"my_azure_open_ai_vectorizer" 
        }
    ]
    ```

1. Assign a vector profile to one or more vector fields by specifying the `vectorSearchProfile` property.

    ```json
    "fields": [ 
            ... // Trimmed for brevity
            { 
                "name": "vector", 
                "type": "Collection(Edm.Single)", 
                "dimensions": 1536, 
                "vectorSearchProfile": "my_vector_profile", 
                "searchable": true, 
                "retrievable": true
            }, 
            { 
                "name": "my-second-vector", 
                "type": "Collection(Edm.Single)", 
                "dimensions": 1024, 
                "vectorSearchProfile": "my_vector_profile", 
                "searchable": true, 
                "retrievable": true
            }
    ]
    ```

1. To verify the vectorizer and vector profile, send a GET request for the index definition. Confirm the `vectorizers` and `profiles` sections contain the definitions you added.

    ```http
    GET https://my-search-service.search.windows.net/indexes/my-index?api-version=2025-09-01 HTTP/1.1
    api-key: <your-admin-api-key>
    ```

## Test a vectorizer

This example assumes the sample index from [Define a vectorizer using a wizard](#define-a-vectorizer-using-a-wizard), but you can test any vectorizer by adjusting the field names and query parameters.

To test a vectorizer:

1. Open a `.rest` or `.http` file in Visual Studio Code.

1. Send a [vector query](vector-search-how-to-query.md) using [Documents - Search Post](/rest/api/searchservice/documents/search-post) (REST API). Replace the service name, index name, and [query API key](search-security-api-keys.md#find-existing-keys) with your own values.

   ```http
   POST https://my-search-service.search.windows.net/indexes/vector-nasa-ebook-txt/docs/search?api-version=2025-09-01 HTTP/1.1
   Content-Type: application/json
   api-key: <your-query-api-key>

   {
       "count": true,
       "select": "title,chunk",
       "vectorQueries": [
           {
               "kind": "text",
               "text": "what cloud formations exist in the troposphere",
               "fields": "vector",
               "k": 3,
               "exhaustive": true
           }
       ]
   }
   ```

   Key points about the query:

   + `"kind": "text"` tells the search engine that the input is a text string and that it should use the vectorizer associated with the search field.

   + `"text": "what cloud formations exist in the troposphere"` is the text string to vectorize.

   + `"fields": "vector"` is the name of the field to query over. If you use the sample index produced by the wizard, the generated vector field is named `vector`.

   + Notice that the query doesn't set any vectorizer properties. The search engine reads them automatically from the vector profile assigned to the field.

1. Send the request. You should get three `k` results, the first of which is the most relevant.

   ```json
   {
       "@odata.count": 3,
       "value": [
           {
               "@search.score": 0.8399121,
               "title": "earth_at_night_508 702702702 702 702702 702.txt",
               "chunk": "Tropospheric cloud formations are influenced by..."
           },
           ... // Trimmed for brevity
       ]
   }
   ```

## Check logs

If you enabled diagnostic logging for your search service, run a Kusto query to confirm query execution on your vector field:

```kusto
OperationEvent
| where TIMESTAMP > ago(30m)
| where Name == "Query.Search" and AdditionalInfo["QueryMetadata"]["Vectors"] has "TextLength"
```

## Troubleshooting

The following table lists common vectorizer errors and how to resolve them.

| Error | Cause | Resolution |
|-------|-------|------------|
| **Authentication failure** (401/403) | Invalid API key or missing RBAC role assignment for the embedding model. | Verify your API key or confirm that the search service identity has the `Cognitive Services OpenAI User` role on the Azure OpenAI resource. |
| **Dimension mismatch** | The vectorizer model produces embeddings with a different dimension count than the vector field expects. | Ensure the `dimensions` property on the vector field matches the output dimensions of the embedding model (for example, 1536 for `text-embedding-ada-002`). |
| **Rate limiting** (429) | The embedding model provider is throttling requests. | Review [Azure OpenAI quota limits](/azure/ai-services/openai/quotas-limits) and consider increasing your tokens-per-minute (TPM) allocation or reducing batch size. |
| **Vectorizer not found** | The vector profile references a vectorizer name that doesn't exist in the index. | Confirm that the `vectorizer` property in the vector profile matches the `name` of a vectorizer in the `vectorizers` array. |
| **Empty results** | Text-to-vector conversion succeeded but the query returns no matches. | Verify the `fields` parameter in the vector query matches the name of a searchable vector field. Increase `k` to return more results. |

## Best practices

Keep these recommendations in mind when setting up and operating a vectorizer:

+ **Use managed identity instead of API keys in production.** Managed identities are more secure and avoid key rotation overhead. For more information, see [Configure a search service to connect using a managed identity](search-security-managed-identity.md).

+ **Deploy the embedding model in the same region as your search service.** Colocation reduces latency and improves the speed of data transfer between services.

+ **Use a separate embedding model deployment for indexing and queries.** This approach lets you tailor each deployment for its workload and makes it easier to identify traffic sources.

+ **Monitor your Azure OpenAI TPM quota.** If you're hitting your tokens-per-minute (TPM) limit, review the [quota limits](/azure/ai-services/openai/quotas-limits) and consider requesting a higher limit through a [support case](/azure/azure-portal/supportability/how-to-create-azure-support-request).

For more best practices specific to the Azure OpenAI embedding skill, see [Azure OpenAI Embedding skill best practices](cognitive-search-skill-azure-openai-embedding.md#best-practices).

## Related content

+ [Vector search in Azure AI Search](vector-search-overview.md)
+ [Integrated vector embedding](vector-search-integrated-vectorization.md)
+ [Create a vector query](vector-search-how-to-query.md)