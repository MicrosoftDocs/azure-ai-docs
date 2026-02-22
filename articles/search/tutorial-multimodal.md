---
title: 'Tutorial: Multimodal Chunking and Embedding'
titleSuffix: Azure AI Search
description: Learn how to extract, chunk, index, and search multimodal content using an indexer and skills.
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
ms.topic: tutorial
ms.date: 02/20/2026
---

# Tutorial: Extract, chunk, and embed multimodal content

In this tutorial, you'll build a multimodal indexer pipeline that performs these tasks:

> [!div class="checklist"]
>
> + Extract and and chunk text and images
> + Vectorize text and images for similarity search
> + Send cropped images to a knowledge store for retrieval by your app

The tutorial shows multiple skillsets, illustrating different combinations of Document Extraction and Text Split, or Document Layout for extraction and chunking. Vectorization is demonstrating using either Azure AI Vision multimodal embedding, or GenAI Prompt for image verbalization paired with Azure OpenAI embedding for text vectorization.

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md), on the basic pricing tier or higher if you want to use the sample data. To complete this tutorial on the free tier, use a smaller document with fewer images. We recommend [configuring a managed identity](search-how-to-managed-identities.md) for role-based access to models and data. If you plan to use Azure AI Vision multimodal, make sure Azure AI Search is in [region that's supported by Azure AI Vision multimodal](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).

+ [Azure Storage](/azure/storage/common/storage-account-create), used for storing sample data and for creating a [knowledge store](knowledge-store-concept-intro.md).

+ [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) that provides Foundry models and APIs. If you're using Azure AI Vision multimodal, choose one of its [supported regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) for your Microsoft Foundry resource.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). If you haven't installed a suitable version of Python, follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter).

Multimodal indexing is implemented through skills that call AI models and APIs in an indexer pipeline. This tutorial uses Foundry models only, but you can create custom skills to use other models. Model prerequisites vary depending on the [skill choice for each task](#choose-skills-for-multimodal-indexing).

### Configure access

[!INCLUDE [resource authentication](includes/resource-authentication.md)]

### Get endpoint

[!INCLUDE [resource endpoint](includes/resource-endpoint.md)]

### Prepare data

The sample data is a 36-page PDF document that combines rich visual content, such as charts, infographics, and scanned pages, with original text.

Azure Storage provides the sample data and hosts the knowledge store. A search service managed identity needs:

+ Read access to Azure Storage to retrieve the sample data.

+ Write access to create the knowledge store. The search service creates the container for cropped images during skillset processing, using the name you provide in an environment variable.

Follow these steps to set up the sample data.

1. Download the following sample PDF: [sustainable-ai-pdf](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Accelerating-Sustainability-with-AI-2025.pdf)

1. Sign in to the [Azure portal](https://portal.azure.com).

1. In Azure Storage, create a new container named **sustainable-ai-pdf**.

1. [Upload the sample data file](/azure/storage/blobs/storage-quickstart-blobs-portal).

1. [Assign roles to the search service managed identity](search-howto-managed-identities-storage.md):

   + **Storage Blob Data Reader** for data retrieval
  
   + **Storage Blob Data Contributor** and **Storage Table Data Contributor** for creating the knowledge store.

While you have the Azure Storage pages open in the Azure portal, get a connection string for the environment variable.

1. Under **Settings** > **Endpoints**, select the endpoint for Resource ID. It should look similar to the following example: `/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/rg-mydemo/providers/Microsoft.Storage/storageAccounts/mydemostorage/blobServices/default`.

1. Prefix `ResourceId=` to this connection string. Use this version for your environment variable.

   `ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/rg-mydemo/providers/Microsoft.Storage/storageAccounts/mydemostorage/blobServices/default`

1. If your environment variables are in a JSON configuration file, the connection string for a system-assigned managed identity connection has the following syntax.

      ```json
      "credentials" : { 
          "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
      }
      ```

1. For connections made using a user-assigned managed identity, use the same connection string but also provide an `identity` set to a predefined user-assigned managed identity. 

      ```json
      "credentials" : { 
          "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
      },
      "identity" : { 
          "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
          "userAssignedIdentity" : "/subscriptions/00000000-0000-0000-0000-00000000/resourcegroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/MY-DEMO-USER-MANAGED-IDENTITY" 
      }
      ```

## Choose skills for multimodal indexing

The index, data source, and indexer definitions are the same for all scenarios, but the skillset can include a different skill combination depending on how you want to extract, chunk, and vectorize text and images.

1. Choose a skill or skill combination that extracts and chunks content. Choices include:

   + Document Extraction plus Text Split skill
   + Document layout

1. Choose a skill or skill combination that vectorizes content. Choices include

   + GenAI Prompt to generate text descriptions of images plus Azure OpenAI Embedding to vectorize the raw and generated text
   + Azure AI Vision multimodal for text and image vectorization

Most of these skills have a dependency on a [deployed model](/azure/ai-foundry/foundry-models/how-to/deploy-foundry-models) or a Microsoft Foundry resource. The following table identifies the models backing each skill, plus the resource and permissions that provide model access.

| Model | Skill | Usage | Resource | Permissions |
| -- | -- | -- | -- | -- |
| None (built-in) | [Document Extraction skill](cognitive-search-skill-document-extraction.md), [Text Split skill](cognitive-search-skill-textsplit.md) | Extract and chunk based on fixed size. <br>Text extraction is free. <br>[Image extraction is billable](https://azure.microsoft.com/pricing/details/search/). | Azure AI Search | See [Configure access](#configure-access) |
| [Document Intelligence 4.0](/azure/ai-services/document-intelligence/model-overview?view=doc-intel-4.0.0&preserve-view=true) | [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) | Extract and chunk based on document layout. | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services User |
| [Azure AI Vision multimodal 4.0](/azure/ai-services/computer-vision/concept-image-retrieval) | [Azure AI Vision skill](cognitive-search-skill-vision-vectorize.md) | Vectorize text and image content. | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services User |
| [GPT-5 or GPT-4](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure) | [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)  | Generate text descriptions of image content. | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services OpenAI User |
| [Text-embedding-3 or text-embedding-ada-002](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure#embeddings) | [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md) | Vectorize text and generated image descriptions. | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services User |

Model usage is billable, except for text extraction and text splitting.

Model deployments can be in any region if the search service connects over the public endpoint or a private connection. However, two models are accessed over the internal network, which can introduce a regional dependency. 

+ [Azure AI Vision multimodal 4.0 region requirements](/azure/ai-services/computer-vision/overview-image-analysis#region-availability). Make sure Azure AI Search is deployed in a region that provides an Azure AI Vision multimodal 4.0 model.

+ [Document Intelligence 4.0 region requirements](cognitive-search-skill-document-intelligence-layout.md#supported-regions).

*Billing for model usage is a separate connection*. If you use [key-based access to a Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md), your model must be in the same region as Azure AI Search. To relax regional dependencies for billing, [set up a keyless connection](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) and use roles for the connection.

## Set up your environment

For this tutorial, your local REST client connection to Azure AI Search requires an endpoint and an API key. You can get these values from the Azure portal. For alternative connection methods, see [Connect to a search service](search-get-started-rbac.md).

For authenticated connections that occur during indexer and skillset processing, the search service uses the role assignments you previously defined.

1. Start Visual Studio Code and create a new file.

1. Provide values for variables used in the request:

   ```http
    @searchUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
    @searchApiKey = PUT-YOUR-ADMIN-API-KEY-HERE
    @storageConnection = PUT-YOUR-STORAGE-CONNECTION-STRING-HERE
    @imageProjectionContainer=sustainable-ai-pdf-images
   ```

   For `@storageConnection`, make sure your connection string doesn't have a trailing semicolon or quotation marks. See [Prepare your data](#prepare-data) for connection string syntax.

   For `@imageProjectionContainer`, provide a container name that's unique in blob storage. Azure AI Search creates this container during skills processing.

1. Add this variable if you're using the Document Layout skill or the Azure AI Vision skill (uses model version 2023-04-15):

   ```http
   @foundryUrl = PUT-YOUR-MULTISERVICE-AZURE-AI-FOUNDRY-ENDPOINT-HERE
   @azureAiVisionModelVersion = 2023-04-15
   ```

1. Add these variables if you're using the GenAI Prompt skill and Azure OpenAI Embedding skill:

   ```http
    @chatCompletionModelUri = PUT-YOUR-DEPLOYED-MODEL-URI-HERE
    @chatCompletionModelKey = PUT-YOUR-MODEL-KEY-HERE
    @textEmbeddingModelUri = PUT-YOUR-DEPLOYED-MODEL-URI-HERE
    @textEmbeddingModelKey = PUT-YOUR-MODEL-KEY-HERE
   ```

1. Save the file using a `.rest` or `.http` file extension. For help with the REST client, see [Quickstart: Full-text search using REST](search-get-started-text.md).

## Set up a pipeline

An indexer pipeline consists of four components: data source, index, skillset, and indexer.
+ [Create a data source](#create-a-data-source)
+ [Create an index](#create-an-index)
+ [Create a skillset for extraction, chunking, and vectorization](#stub-out-a-skillset-definition)
+ [Create (and run) an indexer](#run-the-indexer)

### Create a data source

[Create Data Source (REST)](/rest/api/searchservice/data-sources/create) creates a data source connection that specifies what data to index.

```http
POST {{searchUrl}}/datasources?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

{
   "name":"demo-multimodal-ds",
   "description":null,
   "type":"azureblob",
   "subtype":null,
   "credentials":{
      "connectionString":"{{storageConnection}}"
   },
   "container":{
      "name":"sustainable-ai-pdf",
      "query":null
   },
   "dataChangeDetectionPolicy":null,
   "dataDeletionDetectionPolicy":null,
   "encryptionKey":null,
   "identity":null
}
```

Send the request. The response should look like:

```json
HTTP/1.1 201 Created
Transfer-Encoding: chunked
Content-Type: application/json; odata.metadata=minimal; odata.streaming=true; charset=utf-8
Location: https://<YOUR-SEARCH-SERVICE-NAME>.search.windows-int.net:443/datasources('demo-multimodal-ds')?api-version=2025-11-01-preview -Preview
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=2592000, max-age=15724800; includeSubDomains
Preference-Applied: odata.include-annotations="*"
OData-Version: 4.0
request-id: 4eb8bcc3-27b5-44af-834e-295ed078e8ed
elapsed-time: 346
Date: Sat, 26 Apr 2025 21:25:24 GMT
Connection: close

{
  "name": "demo-multimodal-ds",
  "description": null,
  "type": "azureblob",
  "subtype": null,
  "indexerPermissionOptions": [],
  "credentials": {
    "connectionString": null
  },
  "container": {
    "name": "sustainable-ai-pdf",
    "query": null
  },
  "dataChangeDetectionPolicy": null,
  "dataDeletionDetectionPolicy": null,
  "encryptionKey": null,
  "identity": null
}
```

### Create an index

[Create Index (REST)](/rest/api/searchservice/indexes/create) creates a search index on your search service. The index is identical for all skillsets, with the following exceptions:

+ The `vectorizers` section should match the embedding model used in the skillset. Embedding is either Azure AI Vision or Azure OpenAI text embedding.

+ The `content_embedding` field has a `dimensions` property for the number of dimensions in a vector field. The value corresponds to the number of dimensions created by the embedding model.

#### [**Azure AI Vision multimodal**](#tab/index-vision-embedding)

Vectorizer definition:

```json
"vectorizers": [
    {
        "name": "demo-vectorizer",
        "kind": "aiServicesVision",
        "aiServicesVisionParameters": {
            "resourceUri": "{{foundryUrl}}",
            "authIdentity": null,
            "modelVersion": "{{azureAiVisionModelVersion}}"
        }
    }
]  
```

Vector field definition:

```json
{
    "name": "content_embedding",
    "type": "Collection(Edm.Single)",
    "dimensions": 1024,
    "searchable": true,
    "retrievable": true,
    "vectorSearchProfile": "hnsw"
}
```

#### [**Azure OpenAI embedding (text)**](#tab/index-text-embedding)

For text-embedding-3-large vectorizers:

```json
"vectorizers":[
    {
      "name":"demo-vectorizer",
      "kind":"azureOpenAI",
      "azureOpenAIParameters":{
          "resourceUri": "{{textEmbeddingModelUri}}",
          "apiKey": "{{textEmbeddingModelKey}}",
          "deploymentId":"text-embedding-3-large",
          "modelName":"text-embedding-3-large"
      }
    }
]
```

For text-embedding-3-large vector field:

```json
{
    "name":"content_embedding",
    "type":"Collection(Edm.Single)",
    "dimensions":3072,
    "searchable":true,
    "retrievable":true,
    "vectorSearchProfile":"hnsw"
}
```

For text-embedding-3-small vectorizers:

```json
"vectorizers":[
    {
      "name":"demo-vectorizer",
      "kind":"azureOpenAI",
      "azureOpenAIParameters":{
          "resourceUri": "{{textEmbeddingModelUri}}",
          "apiKey": "{{textEmbeddingModelKey}}",
          "deploymentId":"text-embedding-3-small",
          "modelName":"text-embedding-3-small"
      }
    }
]
```

For text-embedding-3-small vector field:

```json
{
    "name":"content_embedding",
    "type":"Collection(Edm.Single)",
    "dimensions":1056,
    "searchable":true,
    "retrievable":true,
    "vectorSearchProfile":"hnsw"
}
```

For text-embedding-ada-002 vectorizers:

```json
"vectorizers":[
    {
      "name":"demo-vectorizer",
      "kind":"azureOpenAI",
      "azureOpenAIParameters":{
          "resourceUri": "{{textEmbeddingModelUri}}",
          "apiKey": "{{textEmbeddingModelKey}}",
          "deploymentId":"text-embedding-ada-002",
          "modelName":"text-embedding-ada-002"
      }
    }
]
```

For text-embedding-ada-002 vector field:

```json
{
    "name":"content_embedding",
    "type":"Collection(Edm.Single)",
    "dimensions":1536,
    "searchable":true,
    "retrievable":true,
    "vectorSearchProfile":"hnsw"
}
```

---

For nested JSON like the `locations_metadata` field, the index fields must be identical to the source fields. Currently, Azure AI Search doesn't support field mappings to nested JSON, so field names and data types must match completely. The following index aligns to the JSON elements in the raw content.

```http
### Create an index
POST {{searchUrl}}/indexes?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

{
    "name": "demo-multimodal-index",
    "fields": [
        {
            "name": "content_id",
            "type": "Edm.String",
            "retrievable": true,
            "key": true,
            "analyzer": "keyword"
        },
        {
            "name": "text_document_id",
            "type": "Edm.String",
            "searchable": false,
            "filterable": true,
            "retrievable": true,
            "stored": true,
            "sortable": false,
            "facetable": false
        },          
        {
            "name": "document_title",
            "type": "Edm.String",
            "searchable": true
        },
        {
            "name": "image_document_id",
            "type": "Edm.String",
            "filterable": true,
            "retrievable": true
        },
        {
            "name": "content_text",
            "type": "Edm.String",
            "searchable": true,
            "retrievable": true
        },
        {
            "name": "content_embedding",
            "type": "Collection(Edm.Single)",
            "dimensions": 1024,
            "searchable": true,
            "retrievable": true,
            "vectorSearchProfile": "hnsw"
        },
        {
            "name": "content_path",
            "type": "Edm.String",
            "searchable": false,
            "retrievable": true
        },
        {
            "name": "offset",
            "type": "Edm.String",
            "searchable": false,
            "retrievable": true
        },
        {
            "name": "location_metadata",
            "type": "Edm.ComplexType",
            "fields": [
                {
                "name": "page_number",
                "type": "Edm.Int32",
                "searchable": false,
                "retrievable": true
                },
                {
                "name": "bounding_polygons",
                "type": "Edm.String",
                "searchable": false,
                "retrievable": true,
                "filterable": false,
                "sortable": false,
                "facetable": false
                }
            ]
        }         
    ],
    "vectorSearch": {
        "profiles": [
            {
                "name": "hnsw",
                "algorithm": "defaulthnsw",
                "vectorizer": "demo-vectorizer"
            }
        ],
        "algorithms": [
            {
                "name": "defaulthnsw",
                "kind": "hnsw",
                "hnswParameters": {
                    "m": 4,
                    "efConstruction": 400,
                    "metric": "cosine"
                }
            }
        ],
        "vectorizers": [
            {
                "name": "demo-vectorizer",
                "kind": "aiServicesVision",
                "aiServicesVisionParameters": {
                    "resourceUri": "{{foundryUrl}}",
                    "authIdentity": null,
                    "modelVersion": "{{azureAiVisionModelVersion}}"
                }
            }
        ]     
    },
    "semantic": {
        "defaultConfiguration": "semanticconfig",
        "configurations": [
            {
                "name": "semanticconfig",
                "prioritizedFields": {
                    "titleField": {
                        "fieldName": "document_title"
                    },
                    "prioritizedContentFields": [
                    ],
                    "prioritizedKeywordsFields": []
                }
            }
        ]
    }
}
```

Key points:

+ Text and image embeddings are stored in the `content_embedding` field and must be configured with appropriate dimensions, such as 1024, and a vector search profile.

+ `location_metadata` captures bounding polygon and page number metadata for each normalized image, enabling precise spatial search or UI overlays. `location_metadata` only exists for images in this scenario. If you'd like to capture locational metadata for text as well, consider using [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md). An in-depth tutorial is linked at the bottom of the page.

+ For more information on vector search, see [Vectors in Azure AI Search](vector-search-overview.md).

+ For more information on semantic ranking, see [Semantic ranking in Azure AI Search](semantic-search-overview.md)

### Create skillsets for extraction, chunking, and vectorization

[Create Skillset (REST)](/rest/api/searchservice/skillsets/create) creates a skillset on your search service. A skillset defines the operations that extract, chunk, and vectorize content prior to indexing.

There are four skillsets. Each one demonstrates an extraction and chunking strategy with a vectorization strategy. Besides differences in skillset composition, the`indexProjections` section differs for each combination. It corresponds to the outputs of each of the embedding skills.

Extraction and chunking strategies include:

| Skill | Usage | 
| -- | -- | 
| [Document Extraction skill](cognitive-search-skill-document-extraction.md), [Text Split skill](cognitive-search-skill-textsplit.md) | Extract and chunk based on fixed size. <br>Text extraction is free. <br>[Image extraction is billable](https://azure.microsoft.com/pricing/details/search/). |
| [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) | Extract and chunk based on document layout. |

Vectorization strategies include:

| Skill | Usage |
| -- | -- |
| [Azure AI Vision multimodal skill](cognitive-search-skill-vision-vectorize.md) | Vectorize text and image content. |
| [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)  | Generate text descriptions of image content. |
| [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md) | Vectorize text and generated text of image descriptions. | 

### [**Document extraction & multimodal embedding**](#tab/doc-extraction-vision)

TBD 

### [**Document extraction & text embedding**](#tab/doc-extraction-vision)

TBD 

### [**Document layout & multimodal embedding**](#tab/doc-extraction-vision)

TBD 

### [**Document layout & text embedding**](#tab/doc-extraction-vision)

TBD 

---



<!-- This skillset extracts text and images, verbalizes images, vectorizes text, and shapes the image metadata for projection into the index.

Key points:

The content_text field is populated in two ways:

From document text extracted using the Document Extraction skill and chunked using the Text Split skill

From image content using the GenAI Prompt skill, which generates descriptive captions for each normalized image

The content_embedding field contains 3072-dimensional embeddings for both page text and verbalized image descriptions. These are generated using the text-embedding-3-large model from Azure OpenAI.

content_path contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from PDFs when imageAction is set to generateNormalizedImages, and can be mapped from the enriched document from the source field /document/normalized_images/*/imagePath. -->

<!-- Key points:

+ The `content_text` field is populated with text extracted using the Document Extraction Skill and chunked using the Split Skill

+ Within `indexProjections`, the `content_path` contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from PDFs when `imageAction` is set to `generateNormalizedImages`, and can be mapped from the enriched document from the source field `/document/normalized_images/*/imagePath`.

+ The Azure AI Vision multimodal embeddings skill enables embedding of both textual and visual data using the same skill type, differentiated by input (text vs image). For more information, see [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md). -->

## Run the indexer

[Create Indexer](/rest/api/searchservice/indexers/create) creates an indexer on your search service. An indexer connects to the data source, loads data, runs a skillset, and indexes the enriched data.

```http
### Create and run an indexer
POST {{searchUrl}}/indexers?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

{
  "name": "demo-multimodal-indexer",
  "dataSourceName": "demo-multimodal-ds",
  "targetIndexName": "demo-multimodal-index",
  "skillsetName": "demo-multimodal-skillset",
  "parameters": {
    "maxFailedItems": -1,
    "maxFailedItemsPerBatch": 0,
    "batchSize": 1,
    "configuration": {
      "allowSkillsetToReadFileData": true
    }
  },
  "fieldMappings": [
    {
      "sourceFieldName": "metadata_storage_name",
      "targetFieldName": "document_title"
    }
  ],
  "outputFieldMappings": []
}
```

## Run queries

You can start searching as soon as the first document is loaded. This is an unspecified full-text search query that returns all of the fields marked as retrievable in the index, along with a document count. 

```http
### Query the index
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
  
  {
    "search": "*",
    "count": true
  }
```

Send the request. The response should look like:

```json
HTTP/1.1 200 OK
Transfer-Encoding: chunked
Content-Type: application/json; odata.metadata=minimal; odata.streaming=true; charset=utf-8
Content-Encoding: gzip
Vary: Accept-Encoding
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=2592000, max-age=15724800; includeSubDomains
Preference-Applied: odata.include-annotations="*"
OData-Version: 4.0
request-id: 712ca003-9493-40f8-a15e-cf719734a805
elapsed-time: 198
Date: Wed, 30 Apr 2025 23:20:53 GMT
Connection: close

{
  "@odata.count": 100,
  "@search.nextPageParameters": {
    "search": "*",
    "count": true,
    "skip": 50
  },
  "value": [
  ],
  "@odata.nextLink": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview "
}
```
100 documents are returned in the response.

### Query for image-only content

Use a filter to exclude all non-image content.

For filters, you can also use Logical operators (and, or, not) and comparison operators (eq, ne, gt, lt, ge, le). String comparisons are case-sensitive. For more information and examples, see [Examples of simple search queries](search-query-simple-examples.md).

The `$filter` parameter only works on fields that were marked filterable during index creation.

```http
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
  
  {
    "search": "*",
    "count": true,
    "filter": "image_document_id ne null"
  }
```

### Query for content related to "energy"

Query for text or images with content related to energy, returning the content ID, parent document, and text (only populated for text chunks), and the content path where the image is saved in the knowledge store (only populated for images).

```http
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
  

  {
    "search": "energy",
    "count": true,
    "select": "content_id, document_title, content_text, content_path"
  }
```

### Reset and rerun

Indexers can be reset to clear the high-water mark, which allows a full rerun. The following POST requests are for reset, followed by rerun.

```http
### Reset the indexer
POST {{searchUrl}}/indexers/demo-multimodal-indexer/reset?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
```

```http
### Run the indexer
POST {{searchUrl}}/indexers/demo-multimodal-indexer/run?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
```

```http
### Check indexer status 
GET {{searchUrl}}/indexers/demo-multimodal-indexer/status?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
```

### View images in the knowledge store

Recall that the skillset in this tutorial creates a [knowledge store](knowledge-store-concept-intro.md) for image content extracted from the PDF. After the indexer runs, the **sustainable-ai-pdf-images** container should have approximately 23 images. 

You can't return these images in a search query. However, you can write application code that calls the Azure Storage APIs to retrieve the images if you need them for the user experience.

To view the images in the Storage Browser:

1. Sign in to the Azure portal and navigate to your Storage account.

1. In Storage Browser, expand the sustainable-ai-pdf-images container.

1. Select an image.

1. In the far right menu (...), select **View/Edit**.

:::image type="content" source="media/tutorial-multimodal/normalized-image-in-storage.png" alt-text="Screenshot of an image extracted from the PDF document." lightbox="media/tutorial-multimodal/normalized-image-in-storage.png" :::

## Clean up resources

[!INCLUDE [clean up resources (paid)](includes/resource-cleanup-paid.md)]
