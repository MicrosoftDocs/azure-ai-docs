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
# This is the primary instructional guidance for GenAI prompt, Document Layout, Azure AI Vision.
---

# Tutorial: Extract, chunk, and embed multimodal content

In this tutorial, you'll build a multimodal indexer pipeline that performs these tasks:

> [!div class="checklist"]
>
> + Extract and and chunk text and images
> + Vectorize text and images for similarity search
> + Send cropped images to a knowledge store for retrieval by your app

This tutorial includes multiple skillsets for showing different ways to extract, chunk, and vectorize multimodal content.

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md), on the basic pricing tier or higher if you want to use the sample data. [Configure a managed identity](search-how-to-managed-identities.md) for role-based access to models and data. If you plan to use Azure AI Vision multimodal, make sure Azure AI Search is in [region that's supported by Azure AI Vision multimodal](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).

+ [Azure Storage](/azure/storage/common/storage-account-create), used for storing sample data and for creating a [knowledge store](knowledge-store-concept-intro.md).

+ [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) that provides Foundry models and APIs. If you're using Azure AI Vision multimodal, choose one of its [supported regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) for your Microsoft Foundry resource.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). If you haven't installed a suitable version of Python, follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter).

Multimodal indexing is implemented through skills that call AI models and APIs in an indexer pipeline. Model prerequisites vary depending on the [skills chosen for each task](#choose-skills-for-multimodal-indexing).

> [!TIP]
> To complete this tutorial on the free tier, use a smaller document with fewer images. This tutorial uses Foundry models only, but you can create custom skills to use other models. 

### Configure access

[!INCLUDE [resource authentication](includes/resource-authentication.md)]

### Get endpoint

[!INCLUDE [resource endpoint](includes/resource-endpoint.md)]

### Prepare data

Sample data is a 36-page PDF document that combines rich visual content, such as charts, infographics, and scanned pages, with original text. Azure Storage provides the sample data and hosts the [knowledge store](knowledge-store-concept-intro.md). A search service managed identity needs:

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

   + Document Extraction, Text Split skill
   + Document layout extracts

1. Choose a skill or skill combination that vectorizes content. Choices include

   + GenAI Prompt, Azure OpenAI Embedding
   + Azure AI Vision Multimodal

Most of these skills have a dependency on a [deployed model](/azure/ai-foundry/foundry-models/how-to/deploy-foundry-models) or a Microsoft Foundry resource. The following table identifies the models backing each skill, plus the resource and permissions that provide model access.

| Skill | Usage | Model | Resource | Permissions |
| -- | -- | -- | -- | -- |
| [Document Extraction skill](cognitive-search-skill-document-extraction.md), [Text Split skill](cognitive-search-skill-textsplit.md) | Extract and chunk based on fixed size. <br>Text extraction is free. <br>[Image extraction is billable](https://azure.microsoft.com/pricing/details/search/). | None (built-in) | Azure AI Search | See [Configure access](#configure-access) |
| [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) | Extract and chunk based on document layout. | [Document Intelligence 4.0](/azure/ai-services/document-intelligence/model-overview?view=doc-intel-4.0.0&preserve-view=true) | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services User |
| [Azure AI Vision skill](cognitive-search-skill-vision-vectorize.md) | Vectorize text and image content. | [Azure AI Vision multimodal 4.0](/azure/ai-services/computer-vision/concept-image-retrieval) | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services User |
| [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)  | Call an LLM to generate text descriptions of image content. | [GPT-5 or GPT-4](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure) | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services User |
| [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md) | Vectorize text and generated textual image descriptions. | [Text-embedding-3 or text-embedding-ada-002](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure#embeddings) | [Microsoft Foundry](/azure/ai-services/multi-service-resource?pivots=azportal) | Cognitive Services User |

Model usage is billable, except for text extraction and text splitting.

Model deployments can be in any region if the search service connects over the public endpoint or a private connection. However, two models are accessed over the internal network, which can introduce a regional dependency. 

+ [Azure AI Vision multimodal 4.0 region requirements](/azure/ai-services/computer-vision/overview-image-analysis#region-availability). Make sure Azure AI Search is deployed in a region that provides an Azure AI Vision multimodal 4.0 model.

+ [Document Intelligence 4.0 region requirements](cognitive-search-skill-document-intelligence-layout.md#supported-regions). Version 4.0 is in [every region supported by Microsoft Foundry Document Intelligence](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table). Azure AI Search doesn't need to be in this region if you use keyless billing.

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

The same Foundry resource can provide Azure AI Vision, Document Intelligence, a chat completion model, and a text embedding model. Just make sure the region provides the models you need. If a Foundry model region is at capacity, you might need a resource to deploy the necessary models.

## Set up a pipeline

An indexer pipeline consists of four components: data source, index, skillset, and indexer.
+ [Create a data source](#create-a-data-source)
+ [Create an index](#create-an-index)
+ [Create a skillset for extraction, chunking, and vectorization](#create-a-skillset-for-extraction-chunking-and-vectorization)
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

For `text-embedding-3-large` vectorizers:

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

For `text-embedding-3-large` vector field:

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

For `text-embedding-3-small` vectorizers:

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

For `text-embedding-3-small` vector field:

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

For `text-embedding-ada-002` vectorizers:

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

For `text-embedding-ada-002` vector field:

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

+ `content_embedding` is the only vector field and it stores vectors for both text and image content. It must be configured with appropriate dimensions, such as 1024, and a vector search profile.

+ `location_metadata` captures bounding polygon and page number metadata for each normalized image, enabling precise spatial search or UI overlays. `location_metadata` only exists for images in this scenario. If you'd like to capture locational metadata for text as well, consider using [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md).

### Create a skillset for extraction, chunking, and vectorization

[Create Skillset (REST)](/rest/api/searchservice/skillsets/create) creates a skillset on your search service. A skillset defines the operations that extract, chunk, and vectorize content prior to indexing.

There are four skillsets. Each one demonstrates an extraction and chunking strategy with a vectorization strategy. Besides differences in skillset composition, the`indexProjections` section differs for each combination. It corresponds to the outputs of each of the embedding skills.

Extraction and chunking skills:

+ [Document Extraction skill](cognitive-search-skill-document-extraction.md), [Text Split skill](cognitive-search-skill-textsplit.md)
+ [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) for both extraction and chunking

Vectorization skills:

+ [Azure AI Vision multimodal skill](cognitive-search-skill-vision-vectorize.md)
+ [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md), [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md) for textual descriptions of images and text embedding

### [**Document extraction & multimodal embedding**](#tab/doc-extraction-vision)

```rest
### Create a skillset
### Extraction/chunking: Document Extraction, Text Split
### Vectorization: Azure AI Vision multimodal (text and images)

POST {{searchUrl}}/skillsets?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

{
   "name":"demo-multimodal-skillset",
   "description":"A test skillset",
   "skills":[
      {
         "@odata.type":"#Microsoft.Skills.Util.DocumentExtractionSkill",
         "name":"document-extraction-skill",
         "description":"Document extraction skill to extract text and images from documents",
         "parsingMode":"default",
         "dataToExtract":"contentAndMetadata",
         "configuration":{
            "imageAction":"generateNormalizedImages",
            "normalizedImageMaxWidth":2000,
            "normalizedImageMaxHeight":2000
         },
         "context":"/document",
         "inputs":[
            {
               "name":"file_data",
               "source":"/document/file_data"
            }
         ],
         "outputs":[
            {
               "name":"content",
               "targetName":"extracted_content"
            },
            {
               "name":"normalized_images",
               "targetName":"normalized_images"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Text.SplitSkill",
         "name":"split-skill",
         "description":"Split skill to chunk documents",
         "context":"/document",
         "defaultLanguageCode":"en",
         "textSplitMode":"pages",
         "maximumPageLength":2000,
         "pageOverlapLength":200,
         "unit":"characters",
         "inputs":[
            {
               "name":"text",
               "source":"/document/extracted_content",
               "inputs":[
                  
               ]
            }
         ],
         "outputs":[
            {
               "name":"textItems",
               "targetName":"pages"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Vision.VectorizeSkill",
         "name":"text-embedding-skill",
         "description":"Vision Vectorization skill for text",
         "context":"/document/pages/*",
         "modelVersion":"{{azureAiVisionModelVersion}}",
         "inputs":[
            {
               "name":"text",
               "source":"/document/pages/*"
            }
         ],
         "outputs":[
            {
               "name":"vector",
               "targetName":"text_vector"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Vision.VectorizeSkill",
         "name":"image-embedding-skill",
         "description":"Vision Vectorization skill for images",
         "context":"/document/normalized_images/*",
         "modelVersion":"{{azureAiVisionModelVersion}}",
         "inputs":[
            {
               "name":"image",
               "source":"/document/normalized_images/*"
            }
         ],
         "outputs":[
            {
               "name":"vector",
               "targetName":"image_vector"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Util.ShaperSkill",
         "name":"shaper-skill",
         "description":"Shaper skill to reshape the data to fit the index schema",
         "context":"/document/normalized_images/*",
         "inputs":[
            {
               "name":"normalized_images",
               "source":"/document/normalized_images/*",
               "inputs":[
                  
               ]
            },
            {
               "name":"imagePath",
               "source":"='{{imageProjectionContainer}}/'+$(/document/normalized_images/*/imagePath)",
               "inputs":[
                  
               ]
            },
            {
               "name":"dataUri",
               "source":"='data:image/jpeg;base64,'+$(/document/normalized_images/*/data)",
               "inputs":[
                  
               ]
            },
            {
               "name":"location_metadata",
               "sourceContext":"/document/normalized_images/*",
               "inputs":[
                  {
                     "name":"page_number",
                     "source":"/document/normalized_images/*/pageNumber"
                  },
                  {
                     "name":"bounding_polygons",
                     "source":"/document/normalized_images/*/boundingPolygon"
                  }
               ]
            }
         ],
         "outputs":[
            {
               "name":"output",
               "targetName":"new_normalized_images"
            }
         ]
      }
   ],
   "cognitiveServices":{
      "@odata.type":"#Microsoft.Azure.Search.AIServicesByIdentity",
      "subdomainUrl":"{{foundryUrl}}",
      "identity":null
   },
   "indexProjections":{
      "selectors":[
         {
            "targetIndexName":"demo-multimodal-index",
            "parentKeyFieldName":"text_document_id",
            "sourceContext":"/document/pages/*",
            "mappings":[
               {
                  "name":"content_embedding",
                  "source":"/document/pages/*/text_vector"
               },
               {
                  "name":"content_text",
                  "source":"/document/pages/*"
               },
               {
                  "name":"document_title",
                  "source":"/document/document_title"
               }
            ]
         },
         {
            "targetIndexName":"demo-multimodal-index",
            "parentKeyFieldName":"image_document_id",
            "sourceContext":"/document/normalized_images/*",
            "mappings":[
               {
                  "name":"content_embedding",
                  "source":"/document/normalized_images/*/image_vector"
               },
               {
                  "name":"content_path",
                  "source":"/document/normalized_images/*/new_normalized_images/imagePath"
               },
               {
                  "name":"location_metadata",
                  "source":"/document/normalized_images/*/new_normalized_images/location_metadata"
               },
               {
                  "name":"document_title",
                  "source":"/document/document_title"
               }
            ]
         }
      ],
      "parameters":{
         "projectionMode":"skipIndexingParentDocuments"
      }
   },
   "knowledgeStore":{
      "storageConnectionString":"{{storageConnection}}",
      "identity":null,
      "projections":[
         {
            "files":[
               {
                  "storageContainer":"{{imageProjectionContainer}}",
                  "source":"/document/normalized_images/*"
               }
            ]
         }
      ]
   }
}
```

### [**Document extraction & text embedding**](#tab/doc-extraction-text)

```rest
### Create a skillset
### Extraction/chunking: Document Extraction, Text Split
### Vectorization: GenAI Prompt (image verbalization), Azure OpenAI (text embedding)

POST {{searchUrl}}/skillsets?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

{
   "name":"demo-multimodal-skillset",
   "description":"A test skillset",
   "skills":[
      {
         "@odata.type":"#Microsoft.Skills.Util.DocumentExtractionSkill",
         "name":"document-extraction-skill",
         "description":"Document extraction skill to extract text and images from documents",
         "parsingMode":"default",
         "dataToExtract":"contentAndMetadata",
         "configuration":{
            "imageAction":"generateNormalizedImages",
            "normalizedImageMaxWidth":2000,
            "normalizedImageMaxHeight":2000
         },
         "context":"/document",
         "inputs":[
            {
               "name":"file_data",
               "source":"/document/file_data"
            }
         ],
         "outputs":[
            {
               "name":"content",
               "targetName":"extracted_content"
            },
            {
               "name":"normalized_images",
               "targetName":"normalized_images"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Text.SplitSkill",
         "name":"split-skill",
         "description":"Split skill to chunk documents",
         "context":"/document",
         "defaultLanguageCode":"en",
         "textSplitMode":"pages",
         "maximumPageLength":2000,
         "pageOverlapLength":200,
         "unit":"characters",
         "inputs":[
            {
               "name":"text",
               "source":"/document/extracted_content",
               "inputs":[
                  
               ]
            }
         ],
         "outputs":[
            {
               "name":"textItems",
               "targetName":"pages"
            }
         ]
      },
      {
      "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "name": "#2",
      "context": "/document/pages/*",
      "resourceUri": "{{textEmbeddingModelUri}}",
      "apiKey": "{{textEmbeddingModelKey}}",
      "deploymentId":"{{textEmbeddingDeploymentId}}",
      "modelName":"{{textEmbeddingModelName}}",
      "dimensions": 3072,
      "inputs": [
        {
          "name": "text",
          "source": "/document/pages/*",
          "inputs": []
        }
      ],
      "outputs": [
        {
          "name": "embedding",
          "targetName": "text_vector"
        }
      ]
    },
  {
    "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
    "name": "genAI-prompt-skill",
    "description": "GenAI Prompt skill for image verbalization",
    "uri": "{{chatCompletionModelUri}}",
    "timeout": "PT1M",
    "apiKey": "{{chatCompletionModelKey}}",
    "context": "/document/normalized_images/*",
    "responseFormat": { "type": "text" },
    "inputs": [
        {
        "name": "systemMessage",
        "source": "='You are tasked with generating concise, accurate descriptions of images, figures, diagrams, or charts in documents. The goal is to capture the key information and meaning conveyed by the image without including extraneous details like style, colors, visual aesthetics, or size.\n\nInstructions:\nContent Focus: Describe the core content and relationships depicted in the image.\n\nFor diagrams, specify the main elements and how they are connected or interact.\nFor charts, highlight key data points, trends, comparisons, or conclusions.\nFor figures or technical illustrations, identify the components and their significance.\nClarity & Precision: Use concise language to ensure clarity and technical accuracy. Avoid subjective or interpretive statements.\n\nAvoid Visual Descriptors: Exclude details about:\n\nColors, shading, and visual styles.\nImage size, layout, or decorative elements.\nFonts, borders, and stylistic embellishments.\nContext: If relevant, relate the image to the broader content of the technical document or the topic it supports.\n\nExample Descriptions:\nDiagram: \"A flowchart showing the four stages of a machine learning pipeline: data collection, preprocessing, model training, and evaluation, with arrows indicating the sequential flow of tasks.\"\n\nChart: \"A bar chart comparing the performance of four algorithms on three datasets, showing that Algorithm A consistently outperforms the others on Dataset 1.\"\n\nFigure: \"A labeled diagram illustrating the components of a transformer model, including the encoder, decoder, self-attention mechanism, and feedforward layers.\"'"
        },
        {
        "name": "userMessage",
        "source": "='Please describe this image.'"
        },
        {
        "name": "image",
        "source": "/document/normalized_images/*/data"
        }
        ],
        "outputs": [
            {
            "name": "response",
            "targetName": "verbalizedImage"
            }
        ]
  },    
  {
      "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "name": "verbalized-image-embedding-skill",
      "description": "Embedding skill for verbalized images",
      "resourceUri": "{{textEmbeddingModelUri}}",
      "apiKey": "{{textEmbeddingModelKey}}",
      "deploymentId":"{{textEmbeddingDeploymentId}}",
      "modelName":"{{textEmbeddingModelName}}",
      "dimensions": 3072,
      "context": "/document/normalized_images/*",
      "inputs": [
         {
         "name": "text",
         "source": "/document/normalized_images/*/verbalizedImage",
         "inputs": []
         }
      ],
      "outputs": [
         {
         "name": "embedding",
         "targetName": "verbalizedImage_vector"
         }
      ]
},
    {
      "@odata.type": "#Microsoft.Skills.Util.ShaperSkill",
      "name": "shaper-skill",
      "description": "Shaper skill to reshape the data to fit the index schema",
      "context": "/document/normalized_images/*",
      "inputs": [
        {
          "name": "normalized_images",
          "source": "/document/normalized_images/*",
          "inputs": []
        },
        {
          "name": "imagePath",
          "source": "='{{imageProjectionContainer}}/'+$(/document/normalized_images/*/imagePath)",
          "inputs": []
        },
        {
          "name": "location_metadata",
          "sourceContext": "/document/normalized_images/*",
          "inputs": [
            {
              "name": "page_number",
              "source": "/document/normalized_images/*/pageNumber"
            },
            {
              "name": "bounding_polygons",
              "source": "/document/normalized_images/*/boundingPolygon"
            }              
          ]
        }        
      ],
      "outputs": [
        {
          "name": "output",
          "targetName": "new_normalized_images"
        }
      ]
   }
   ],
  "indexProjections": {
      "selectors": [
        {
          "targetIndexName": "demo-multimodal-index",
          "parentKeyFieldName": "text_document_id",
          "sourceContext": "/document/pages/*",
          "mappings": [              
            {
              "name": "content_embedding",
              "source": "/document/pages/*/text_vector"
            },
            {
              "name": "content_text",
              "source": "/document/pages/*"
            },             
            {
              "name": "document_title",
              "source": "/document/document_title"
            }      
          ]
        },
        {
          "targetIndexName": "demo-multimodal-index",
          "parentKeyFieldName": "image_document_id",
          "sourceContext": "/document/normalized_images/*",
          "mappings": [    
            {
            "name": "content_text",
            "source": "/document/normalized_images/*/verbalizedImage"
            },  
            {
            "name": "content_embedding",
            "source": "/document/normalized_images/*/verbalizedImage_vector"
            },                                           
            {
              "name": "content_path",
              "source": "/document/normalized_images/*/new_normalized_images/imagePath"
            },                    
            {
              "name": "document_title",
              "source": "/document/document_title"
            },
            {
              "name": "location_metadata",
              "source": "/document/normalized_images/*/new_normalized_images/location_metadata"
            }            
          ]
        }
      ],
      "parameters": {
        "projectionMode": "skipIndexingParentDocuments"
      }
  },
   "knowledgeStore":{
      "storageConnectionString":"{{storageConnection}}",
      "identity":null,
      "projections":[
         {
            "files":[
               {
                  "storageContainer":"{{imageProjectionContainer}}",
                  "source":"/document/normalized_images/*"
               }
            ]
         }
      ]
   }
}
```

### [**Document layout & multimodal embedding**](#tab/doc-layout-vision)

```rest
### Create a skillset
### Extraction/chunking: Document Intelligence Layout
### Vectorization: Azure AI Vision multimodal (text and images)

POST {{searchUrl}}/skillsets?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

{
   "name":"demo-multimodal-skillset",
   "description":"A test skillset",
   "skills":[
      {
         "@odata.type":"#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
         "name":"document-layout-skill",
         "description":"Document Intelligence skill for document cracking",
         "context":"/document",
         "outputMode":"oneToMany",
         "outputFormat":"text",
         "extractionOptions":[
            "images",
            "locationMetadata"
         ],
         "chunkingProperties":{
            "unit":"characters",
            "maximumLength":2000,
            "overlapLength":200
         },
         "inputs":[
            {
               "name":"file_data",
               "source":"/document/file_data"
            }
         ],
         "outputs":[
            {
               "name":"text_sections",
               "targetName":"text_sections"
            },
            {
               "name":"normalized_images",
               "targetName":"normalized_images"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Vision.VectorizeSkill",
         "name":"text-embedding-skill",
         "description":"Vision Vectorization skill for text",
         "context":"/document/pages/*",
         "modelVersion":"{{azureAiVisionModelVersion}}",
         "inputs":[
            {
               "name":"text",
               "source":"/document/pages/*"
            }
         ],
         "outputs":[
            {
               "name":"vector",
               "targetName":"text_vector"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Vision.VectorizeSkill",
         "name":"image-embedding-skill",
         "description":"Vision Vectorization skill for images",
         "context":"/document/normalized_images/*",
         "modelVersion":"{{azureAiVisionModelVersion}}",
         "inputs":[
            {
               "name":"image",
               "source":"/document/normalized_images/*"
            }
         ],
         "outputs":[
            {
               "name":"vector",
               "targetName":"image_vector"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Util.ShaperSkill",
         "name":"shaper-skill",
         "context":"/document/normalized_images/*",
         "inputs":[
            {
               "name":"normalized_images",
               "source":"/document/normalized_images/*",
               "inputs":[
                  
               ]
            },
            {
               "name":"imagePath",
               "source":"='my_container_name/'+$(/document/normalized_images/*/imagePath)",
               "inputs":[
                  
               ]
            }
         ],
         "outputs":[
            {
               "name":"output",
               "targetName":"new_normalized_images"
            }
         ]
      }
   ],
   "cognitiveServices":{
      "@odata.type":"#Microsoft.Azure.Search.AIServicesByIdentity",
      "subdomainUrl":"{{foundryUrl}}",
      "identity":null
   },
   "indexProjections":{
      "selectors":[
         {
            "targetIndexName":"demo-multimodal-index",
            "parentKeyFieldName":"text_document_id",
            "sourceContext":"/document/text_sections/*",
            "mappings":[
               {
                  "name":"content_embedding",
                  "source":"/document/text_sections/*/text_vector"
               },
               {
                  "name":"content_text",
                  "source":"/document/text_sections/*/content"
               },
               {
                  "name":"location_metadata",
                  "source":"/document/text_sections/*/locationMetadata"
               },
               {
                  "name":"document_title",
                  "source":"/document/document_title"
               }
            ]
         },
         {
            "targetIndexName":"demo-multimodal-index",
            "parentKeyFieldName":"image_document_id",
            "sourceContext":"/document/normalized_images/*",
            "mappings":[
               {
                  "name":"content_embedding",
                  "source":"/document/normalized_images/*/image_vector"
               },
               {
                  "name":"content_path",
                  "source":"/document/normalized_images/*/new_normalized_images/imagePath"
               },
               {
                  "name":"document_title",
                  "source":"/document/document_title"
               },
               {
                  "name":"location_metadata",
                  "source":"/document/normalized_images/*/locationMetadata"
               }
            ]
         }
      ],
      "parameters":{
         "projectionMode":"skipIndexingParentDocuments"
      }
   },
   "knowledgeStore":{
      "storageConnectionString":"{{storageConnection}}",
      "projections":[
         {
            "files":[
               {
                  "storageContainer":"{{imageProjectionContainer}}",
                  "source":"/document/normalized_images/*"
               }
            ]
         }
      ]
   }
}
```

### [**Document layout & text embedding**](#tab/doc-layout-text)

```rest
### Create a skillset
### Extraction/chunking: Document Extraction, Text Split
### Vectorization: GenAI Prompt (image verbalization), Azure OpenAI (text embedding)

POST {{searchUrl}}/skillsets?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

{
   "name":"demo-multimodal-skillset",
   "description":"A test skillset",
   "skills":[
      {
         "@odata.type":"#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
         "name":"document-cracking-skill",
         "description":"Document Layout skill for document cracking",
         "context":"/document",
         "outputMode":"oneToMany",
         "outputFormat":"text",
         "extractionOptions":[
            "images",
            "locationMetadata"
         ],
         "chunkingProperties":{
            "unit":"characters",
            "maximumLength":2000,
            "overlapLength":200
         },
         "inputs":[
            {
               "name":"file_data",
               "source":"/document/file_data"
            }
         ],
         "outputs":[
            {
               "name":"text_sections",
               "targetName":"text_sections"
            },
            {
               "name":"normalized_images",
               "targetName":"normalized_images"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
         "name":"text-embedding-skill",
         "description":"Embedding skill for text",
         "context":"/document/pages/*",
         "inputs":[
            {
               "name":"text",
               "source":"/document/pages/*"
            }
         ],
         "outputs":[
            {
               "name":"embedding",
               "targetName":"text_vector"
            }
         ],
         "resourceUri":"{{textEmbeddingModelUri}}",
         "deploymentId":"text-embedding-3-large",
         "apiKey":"{{textEmbeddingModelKey}}",
         "dimensions":3072,
         "modelName":"text-embedding-3-large"
      },
      {
         "@odata.type":"#Microsoft.Skills.Custom.ChatCompletionSkill",
         "name":"genAI-prompt-skill",
         "description":"GenAI Prompt skill for image verbalization",
         "uri":"{{chatCompletionModelUri}}",
         "timeout":"PT1M",
         "apiKey":"{{chatCompletionModelKey}}",
         "context":"/document/normalized_images/*",
         "inputs":[
            {
               "name":"systemMessage",
               "source":"='You are tasked with generating concise, accurate descriptions of images, figures, diagrams, or charts in documents. The goal is to capture the key information and meaning conveyed by the image without including extraneous details like style, colors, visual aesthetics, or size.\n\nInstructions:\nContent Focus: Describe the core content and relationships depicted in the image.\n\nFor diagrams, specify the main elements and how they are connected or interact.\nFor charts, highlight key data points, trends, comparisons, or conclusions.\nFor figures or technical illustrations, identify the components and their significance.\nClarity & Precision: Use concise language to ensure clarity and technical accuracy. Avoid subjective or interpretive statements.\n\nAvoid Visual Descriptors: Exclude details about:\n\nColors, shading, and visual styles.\nImage size, layout, or decorative elements.\nFonts, borders, and stylistic embellishments.\nContext: If relevant, relate the image to the broader content of the technical document or the topic it supports.\n\nExample Descriptions:\nDiagram: \"A flowchart showing the four stages of a machine learning pipeline: data collection, preprocessing, model training, and evaluation, with arrows indicating the sequential flow of tasks.\"\n\nChart: \"A bar chart comparing the performance of four algorithms on three datasets, showing that Algorithm A consistently outperforms the others on Dataset 1.\"\n\nFigure: \"A labeled diagram illustrating the components of a transformer model, including the encoder, decoder, self-attention mechanism, and feedforward layers.\"'"
            },
            {
               "name":"userMessage",
               "source":"='Please describe this image.'"
            },
            {
               "name":"image",
               "source":"/document/normalized_images/*/data"
            }
         ],
         "outputs":[
            {
               "name":"response",
               "targetName":"verbalizedImage"
            }
         ]
      },
      {
         "@odata.type":"#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
         "name":"verbalized-image-embedding-skill",
         "description":"Embedding skill for verbalized images",
         "context":"/document/normalized_images/*",
         "inputs":[
            {
               "name":"text",
               "source":"/document/normalized_images/*/verbalizedImage",
               "inputs":[
                  
               ]
            }
         ],
         "outputs":[
            {
               "name":"embedding",
               "targetName":"verbalizedImage_vector"
            }
         ],
         "resourceUri":"{{textEmbeddingModelUri}}",
         "deploymentId":"text-embedding-3-large",
         "apiKey":"{{textEmbeddingModelKey}}",
         "dimensions":3072,
         "modelName":"text-embedding-3-large"
      },
      {
         "@odata.type":"#Microsoft.Skills.Util.ShaperSkill",
         "name":"shaper-skill",
         "description":"Shaper skill to reshape the data to fit the index schema",
         "context":"/document/normalized_images/*",
         "inputs":[
            {
               "name":"normalized_images",
               "source":"/document/normalized_images/*",
               "inputs":[
                  
               ]
            },
            {
               "name":"imagePath",
               "source":"='{{imageProjectionContainer}}/'+$(/document/normalized_images/*/imagePath)",
               "inputs":[
                  
               ]
            },
            {
               "name":"location_metadata",
               "sourceContext":"/document/normalized_images/*",
               "inputs":[
                  {
                     "name":"page_number",
                     "source":"/document/normalized_images/*/pageNumber"
                  },
                  {
                     "name":"bounding_polygons",
                     "source":"/document/normalized_images/*/boundingPolygon"
                  }
               ]
            }
         ],
         "outputs":[
            {
               "name":"output",
               "targetName":"new_normalized_images"
            }
         ]
      }
   ],
   "indexProjections":{
      "selectors":[
         {
            "targetIndexName":"demo-multimodal-index",
            "parentKeyFieldName":"text_document_id",
            "sourceContext":"/document/text_sections/*",
            "mappings":[
               {
                  "name":"content_embedding",
                  "source":"/document/text_sections/*/text_vector"
               },
               {
                  "name":"content_text",
                  "source":"/document/text_sections/*/content"
               },
               {
                  "name":"location_metadata",
                  "source":"/document/text_sections/*/locationMetadata"
               },
               {
                  "name":"document_title",
                  "source":"/document/document_title"
               }
            ]
         },
         {
            "targetIndexName":"demo-multimodal-index",
            "parentKeyFieldName":"image_document_id",
            "sourceContext":"/document/normalized_images/*",
            "mappings":[
               {
                  "name":"content_text",
                  "source":"/document/normalized_images/*/verbalizedImage"
               },
               {
                  "name":"content_embedding",
                  "source":"/document/normalized_images/*/verbalizedImage_vector"
               },
               {
                  "name":"content_path",
                  "source":"/document/normalized_images/*/new_normalized_images/imagePath"
               },
               {
                  "name":"document_title",
                  "source":"/document/document_title"
               },
               {
                  "name":"location_metadata",
                  "source":"/document/normalized_images/*/locationMetadata"
               }
            ]
         }
      ],
      "parameters":{
         "projectionMode":"skipIndexingParentDocuments"
      }
   },
   "cognitiveServices":{
      "@odata.type":"#Microsoft.Azure.Search.AIServicesByIdentity",
      "subdomainUrl":"{{foundryUrl}}",
      "identity":null
   },
   "knowledgeStore":{
      "storageConnectionString":"{{storageConnection}}",
      "projections":[
         {
            "files":[
               {
                  "storageContainer":"{{imageProjectionContainer}}",
                  "source":"/document/normalized_images/*"
               }
            ]
         }
      ]
   }
}
```

---

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

The `content_embedding` field contains over a thousand dimensions. Use a `select` statement to exclude that field from the response by explicitly choosing all of the other fields.

```http
### Query the index
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
  
  {
    "search": "*",
    "select": "content_id, text_document_id, document_title, image_document_id, content_text, content_path, offset, location_metadata/page_number, location_metadata/bounding_polygons",
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

Use a filter to exclude all non-image content. The `$filter` parameter only works on fields that were marked filterable during index creation.

For filters, you can also use Logical operators (and, or, not) and comparison operators (eq, ne, gt, lt, ge, le). String comparisons are case-sensitive. For more information and examples, see [Examples of simple search queries](search-query-simple-examples.md).

```http
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
  
  {
    "search": "*",
    "select": "image_document_id, content_path",
    "count": true,
    "filter": "image_document_id ne null"
  }
```

Search documents containing image content don't have text content, so you can exclude text fields.

The `content_embedding` field contains 1-to-3 thousand dimensional embeddings for both page text and verbalized image descriptions. We exclude this field from the query.

The `content_path` field contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from PDFs when `imageAction` is set to `generateNormalizedImages`, and can be mapped from the enriched document from the source field `/document/normalized_images/*/imagePath`. 

### Query for content related to "energy"

Query for text or images with content related to energy, returning the content ID, parent document, and text (only populated for text chunks), and the content path where the image is saved in the knowledge store (only populated for images).

This query is full text search only, but you can [query the vector field](vector-search-how-to-query.md) for similarity search.

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
