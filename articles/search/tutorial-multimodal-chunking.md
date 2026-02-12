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
ms.date: 02/14/2026
---

# Tutorial: Extract, chunk, and embed multimodal content

In this tutorial, you will build a multimodal indexing pipeline that:

> [!div class="checklist"]
>
> + Extracts and and chunks text and and image content
> + Vectorizes text and image content for similarity search
> + Stores reshaped and cropped images in a knowledge store for retrieval by your app

Source data is a 36-page PDF document that combines rich visual content, such as charts, infographics, and scanned pages, with original text.

Multimodal indexing is implemented through a combination of skills that bring Foundry models and APIs into an indexer pipeline.

<!-- + An indexer and skillset to create an indexing pipeline that includes AI enrichment through skills.

+ The [Document Extraction skill](cognitive-search-skill-document-extraction.md) for extracting normalized images and text. The [Text Split skill](cognitive-search-skill-textsplit.md) chunks the data.

+ The [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) to vectorize text and images.

+ A search index configured to store extracted text and image content. Some content is vectorized for vector-based similarity search.

This tutorial demonstrates a lower-cost approach for indexing multimodal content using the Document Extraction skill. It enables extraction and search over both text and images from documents pulled from Azure Blob Storage. However, it doesn't include locational metadata for text, such as page numbers or bounding regions. For a more comprehensive solution that includes structured text layout and spatial metadata, see [Tutorial: Vectorize from a structured document layout](tutorial-document-layout-multimodal-embeddings.md).

> [!NOTE]
> Image extraction by the Document Extraction skill isn't free. Setting `imageAction` to `generateNormalizedImages` in the skillset triggers image extraction, which is an extra charge. For billing information, see [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/). -->

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md), any region, on the basic pricing tier or higher if you want to use the sample data. To complete this tutorial on the free tier, use a smaller a document with fewer images.

+ [Azure Storage](/azure/storage/common/storage-account-create), used for storing sample data and for creating a [knowledge store](knowledge-store-concept-intro.md).

+ [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) that provides Foundry models and APIs.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). If you haven't installed a suitable version of Python, follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter).

The [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) has limited regional availability. When you create a Foundry resource, [choose a region](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) that provides the multimodal embeddings 4.0 API.

## Configure access

[!INCLUDE [resource authentication](/includes/resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](/includes/resource-endpoint.md)]

## Prepare data

Azure Storage provides the sample data and hosts the knowledge store. A search service managed identity needs:

+ Read access to Azure Storage to retrieve the sample data.

+ Write access to create the knowledge store. The search service creates the container for cropped images during skillset processing, using the name you provide in an environment variable.

1. Download the following sample PDF: [sustainable-ai-pdf](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Accelerating-Sustainability-with-AI-2025.pdf)

1. In Azure Storage, create a new container named **sustainable-ai-pdf**.

1. [Upload the sample data file](/azure/storage/blobs/storage-quickstart-blobs-portal).

1. [Create role assignments and specify a managed identity in a connection string](search-howto-managed-identities-storage.md):

   1. Assign **Storage Blob Data Reader** for data retrieval by the indexer.
  
   1. Assign **Storage Blob Data Contributor** and **Storage Table Data Contributor** to create and load the knowledge store. 

   1. For connections made using a system-assigned managed identity, get a connection string that contains a ResourceId, with no account key or password. The connection string is similar to the following example:

    ```json
    "credentials" : { 
        "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
    }
    ```

   1. For connections made using a user-assigned managed identity, get the same connection string but also provide an `identity` set to a predefined user-assigned managed identity. The connection string is similar to the following example:

    ```json
    "credentials" : { 
        "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
    },
    "identity" : { 
        "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
        "userAssignedIdentity" : "/subscriptions/00000000-0000-0000-0000-00000000/resourcegroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/MY-DEMO-USER-MANAGED-IDENTITY" 
    }
    ```

## Choose an approach

The index, data source, and indexer definitions are the same for all scenarios, but you can pick different skills depending on the task.

#### Extract and chunk content

| Skills | Explanation |
|--|--|
| Document Extraction and Text Split | Uses built-in skills to extract text and images, and chunk text based on fixed size. Usage is free of charge. |
| Document Layout | Calls Content Understanding APIs to extract text and images, and chunk text based on document structure. Usage is based on pay-as-you-go pricing. |

### Describe images

| Skills | Explanation |
|--|--|
| None | Image descriptions are optional. If you don't generate a description, you can vectorize images using Azure AI Vision and run vector queries for matches on vector content. |
| GenAI Prompt (chat completion) | Calls a supported chat completion model in Microsoft Foundry to generate a text description for each extracted image. Generated text, rather then an image, is vectorized and used for content retrieval. Usage is based on pay-as-you-go pricing. |

#### Vectorize content

| Skills | Explanation |
|--|--|
| Azure OpenAI Embedding skill | Uses a supported embedding model to vectorize text, either raw text or generated text for image descriptions. Usage is based on pay-as-you-go pricing. |
| Azure AI Vision skill | Calls the Azure AI Vision multimodal 4.0 API to vectorize both text and images extracted from the source document. If you want image vectors, you must use this skill. Usage is based on pay-as-you-go pricing. |

<!-- ## Deploy models

Model requirements vary based on how you extract and describe images, and chunk content.

| Task | Skill | Dependency|
|-|-|
| Extract and chunk | [Document Extraction skill](cognitive-search-skill-document-extraction.md) for extracting normalized images and text. [Text Split skill](cognitive-search-skill-textsplit.md) chunks the data. | Foundry resource used for billing. No model requirement. |
| Extract and chunk | [Document Layout skill (Content Understanding)](cognitive-search-skill-document-intelligence-layout.md#supported-regions) | Foundry resource in a [supported region](cognitive-search-skill-document-intelligence-layout.md#supported-regions). |
| Describe images | [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) | Foundry resource in a [supported region](/azure/ai-services/computer-vision/overview-image-analysis#region-availability). |
| Describe images | [GenAI Prompt skill (preview)](cognitive-search-skill-genai-prompt.md) that calls a chat completion model to create descriptions of visual content.| Foundry resource in a [supported region](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?view=foundry-classic&tabs=global-standard-aoai%2Cglobal-standard&pivots=azure-openai&preserve-view=true). |

The search service connects to the model during skillset processing using its managed identity. This section gives you guidance and links for assigning roles for authorized access.

1. Sign in to the Azure portal (not the Foundry portal) and find the Foundry resource. Make sure it's in a region that provides the [multimodal 4.0 API](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).

1. Select **Access control (IAM)**.

1. Select **Add** and then **Add role assignment**.

1. Search for **Cognitive Services User** and then select it.

1. Choose **Managed identity** and then assign your [search service managed identity](search-how-to-managed-identities.md).
 -->

## Set up your environment

### [REST API](#tab/rest-api)

For this tutorial, your local REST client connection to Azure AI Search requires an endpoint and an API key. You can get these values from the Azure portal. For alternative connection methods, see [Connect to a search service](search-get-started-rbac.md).

For authenticated connections that occur during indexer and skillset processing, the search service uses the role assignments you previously defined.

1. Start Visual Studio Code and create a new file.

1. Provide values for variables used in the request. For `@storageConnection`, make sure your connection string doesn't have a trailing semicolon or quotation marks. For `@imageProjectionContainer`, provide a container name that's unique in blob storage. Azure AI Search creates this container for you during skills processing.

   ```http
    @searchUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
    @searchApiKey = PUT-YOUR-ADMIN-API-KEY-HERE
    @storageConnection = PUT-YOUR-STORAGE-CONNECTION-STRING-HERE
    @cognitiveServicesUrl = PUT-YOUR-AZURE-AI-FOUNDRY-ENDPOINT-HERE
    @modelVersion = 2023-04-15
    @imageProjectionContainer=sustainable-ai-pdf-images
   ```

1. Save the file using a `.rest` or `.http` file extension. For help with the REST client, see [Quickstart: Full-text search using REST](search-get-started-text.md).

To get the Azure AI Search endpoint and API key:

1. Sign in to the [Azure portal](https://portal.azure.com), navigate to the search service **Overview** page, and copy the URL. An example endpoint might look like `https://mydemo.search.windows.net`.

1. Under **Settings** > **Keys**, copy an admin key. Admin keys are used to add, modify, and delete objects. There are two interchangeable admin keys. Copy either one.

   :::image type="content" source="media/search-get-started-rest/get-url-key.png" alt-text="Screenshot of the URL and API keys in the Azure portal.":::

## Create an indexer pipeline

TBD

### Create a data source

[Create Data Source (REST)](/rest/api/searchservice/data-sources/create) creates a data source connection that specifies what data to index.

```http
POST {{searchUrl}}/datasources?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

{
   "name":"doc-extraction-multimodal-embedding-ds",
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
Location: https://<YOUR-SEARCH-SERVICE-NAME>.search.windows-int.net:443/datasources('doc-extraction-multimodal-embedding-ds')?api-version=2025-11-01-preview -Preview
Server: Microsoft-IIS/10.0
Strict-Transport-Security: max-age=2592000, max-age=15724800; includeSubDomains
Preference-Applied: odata.include-annotations="*"
OData-Version: 4.0
request-id: 4eb8bcc3-27b5-44af-834e-295ed078e8ed
elapsed-time: 346
Date: Sat, 26 Apr 2025 21:25:24 GMT
Connection: close

{
  "name": "doc-extraction-multimodal-embedding-ds",
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

[Create Index (REST)](/rest/api/searchservice/indexes/create) creates a search index on your search service. An index specifies all the parameters and their attributes.

For nested JSON, the index fields must be identical to the source fields. Currently, Azure AI Search doesn't support field mappings to nested JSON, so field names and data types must match completely. The following index aligns to the JSON elements in the raw content.

```http
### Create an index
POST {{searchUrl}}/indexes?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

{
    "name": "doc-extraction-multimodal-embedding-index",
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
                    "resourceUri": "{{cognitiveServicesUrl}}",
                    "authIdentity": null,
                    "modelVersion": "{{modelVersion}}"
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

### Stub out a skillset definition

[Create Skillset (REST)](/rest/api/searchservice/skillsets/create) creates a skillset on your search service. A skillset defines the operations that chunk and embed content prior to indexing. This skillset uses the built-in Document Extraction skill to extract text and images. It uses Text Split skill to chunk large text. It uses Azure Vision multimodal embeddings skill to vectorize image and text content.


## Extract and chunk text

```http
### Create a skillset
POST {{searchUrl}}/skillsets?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

{
  "name": "doc-extraction-multimodal-embedding-skillset",
	"description": "A test skillset",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Util.DocumentExtractionSkill",
      "name": "document-extraction-skill",
      "description": "Document extraction skill to extract text and images from documents",
      "parsingMode": "default",
      "dataToExtract": "contentAndMetadata",
      "configuration": {
          "imageAction": "generateNormalizedImages",
          "normalizedImageMaxWidth": 2000,
          "normalizedImageMaxHeight": 2000
      },
      "context": "/document",
      "inputs": [
        {
          "name": "file_data",
          "source": "/document/file_data"
        }
      ],
      "outputs": [
        {
          "name": "content",
          "targetName": "extracted_content"
        },
        {
          "name": "normalized_images",
          "targetName": "normalized_images"
        }
      ]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
      "name": "split-skill",
      "description": "Split skill to chunk documents",
      "context": "/document",
      "defaultLanguageCode": "en",
      "textSplitMode": "pages",
      "maximumPageLength": 2000,
      "pageOverlapLength": 200,
      "unit": "characters",
      "inputs": [
        {
          "name": "text",
          "source": "/document/extracted_content",
          "inputs": []
        }
      ],
      "outputs": [
        {
          "name": "textItems",
          "targetName": "pages"
        }
      ]
    },  
  { 
    "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill", 
    "name": "text-embedding-skill",
    "description": "Vision Vectorization skill for text",
    "context": "/document/pages/*", 
    "modelVersion": "{{modelVersion}}", 
    "inputs": [ 
      { 
        "name": "text", 
        "source": "/document/pages/*" 
      } 
    ], 
    "outputs": [ 
      { 
        "name": "vector",
        "targetName": "text_vector"
      } 
    ] 
  },
  { 
    "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill", 
    "name": "image-embedding-skill",
    "description": "Vision Vectorization skill for images",
    "context": "/document/normalized_images/*", 
    "modelVersion": "{{modelVersion}}", 
    "inputs": [ 
      { 
        "name": "image", 
        "source": "/document/normalized_images/*" 
      } 
    ], 
    "outputs": [ 
      { 
        "name": "vector",
  "targetName": "image_vector"
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
          "name": "dataUri",
          "source": "='data:image/jpeg;base64,'+$(/document/normalized_images/*/data)",
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
  "cognitiveServices": {
    "@odata.type": "#Microsoft.Azure.Search.AIServicesByIdentity",
    "subdomainUrl": "{{cognitiveServicesUrl}}",
    "identity": null
  },
  "indexProjections": {
      "selectors": [
        {
          "targetIndexName": "doc-extraction-multimodal-embedding-index",
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
          "targetIndexName": "doc-extraction-multimodal-embedding-index",
          "parentKeyFieldName": "image_document_id",
          "sourceContext": "/document/normalized_images/*",
          "mappings": [                                   
            {
              "name": "content_embedding",
              "source": "/document/normalized_images/*/image_vector"
            },
            {
              "name": "content_path",
              "source": "/document/normalized_images/*/new_normalized_images/imagePath"
            },
            {
              "name": "location_metadata",
              "source": "/document/normalized_images/*/new_normalized_images/location_metadata"
            },                      
            {
              "name": "document_title",
              "source": "/document/document_title"
            }                
          ]
        }
      ],
      "parameters": {
        "projectionMode": "skipIndexingParentDocuments"
      }
  },
  "knowledgeStore": {
    "storageConnectionString": "{{storageConnection}}",
    "identity": null,
    "projections": [
      {
        "files": [
          {
            "storageContainer": "{{imageProjectionContainer}}",
            "source": "/document/normalized_images/*"
          }
        ]
      }
    ]
  }
}
```

This skillset extracts text and images, vectorizes both, and shapes the image metadata for projection into the index.

Key points:

+ The `content_text` field is populated with text extracted using the Document Extraction Skill and chunked using the Split Skill

+ `content_path` contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from PDFs when `imageAction` is set to `generateNormalizedImages`, and can be mapped from the enriched document from the source field `/document/normalized_images/*/imagePath`.

+ The Azure Vision multimodal embeddings skill enables embedding of both textual and visual data using the same skill type, differentiated by input (text vs image). For more information, see [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md).

## Vectorize multimodal content

```http
### Create a skillset
POST {{searchUrl}}/skillsets?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

{
  "name": "doc-extraction-multimodal-embedding-skillset",
	"description": "A test skillset",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Util.DocumentExtractionSkill",
      "name": "document-extraction-skill",
      "description": "Document extraction skill to extract text and images from documents",
      "parsingMode": "default",
      "dataToExtract": "contentAndMetadata",
      "configuration": {
          "imageAction": "generateNormalizedImages",
          "normalizedImageMaxWidth": 2000,
          "normalizedImageMaxHeight": 2000
      },
      "context": "/document",
      "inputs": [
        {
          "name": "file_data",
          "source": "/document/file_data"
        }
      ],
      "outputs": [
        {
          "name": "content",
          "targetName": "extracted_content"
        },
        {
          "name": "normalized_images",
          "targetName": "normalized_images"
        }
      ]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
      "name": "split-skill",
      "description": "Split skill to chunk documents",
      "context": "/document",
      "defaultLanguageCode": "en",
      "textSplitMode": "pages",
      "maximumPageLength": 2000,
      "pageOverlapLength": 200,
      "unit": "characters",
      "inputs": [
        {
          "name": "text",
          "source": "/document/extracted_content",
          "inputs": []
        }
      ],
      "outputs": [
        {
          "name": "textItems",
          "targetName": "pages"
        }
      ]
    },  
  { 
    "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill", 
    "name": "text-embedding-skill",
    "description": "Vision Vectorization skill for text",
    "context": "/document/pages/*", 
    "modelVersion": "{{modelVersion}}", 
    "inputs": [ 
      { 
        "name": "text", 
        "source": "/document/pages/*" 
      } 
    ], 
    "outputs": [ 
      { 
        "name": "vector",
        "targetName": "text_vector"
      } 
    ] 
  },
  { 
    "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill", 
    "name": "image-embedding-skill",
    "description": "Vision Vectorization skill for images",
    "context": "/document/normalized_images/*", 
    "modelVersion": "{{modelVersion}}", 
    "inputs": [ 
      { 
        "name": "image", 
        "source": "/document/normalized_images/*" 
      } 
    ], 
    "outputs": [ 
      { 
        "name": "vector",
  "targetName": "image_vector"
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
          "name": "dataUri",
          "source": "='data:image/jpeg;base64,'+$(/document/normalized_images/*/data)",
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
  "cognitiveServices": {
    "@odata.type": "#Microsoft.Azure.Search.AIServicesByIdentity",
    "subdomainUrl": "{{cognitiveServicesUrl}}",
    "identity": null
  },
  "indexProjections": {
      "selectors": [
        {
          "targetIndexName": "doc-extraction-multimodal-embedding-index",
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
          "targetIndexName": "doc-extraction-multimodal-embedding-index",
          "parentKeyFieldName": "image_document_id",
          "sourceContext": "/document/normalized_images/*",
          "mappings": [                                   
            {
              "name": "content_embedding",
              "source": "/document/normalized_images/*/image_vector"
            },
            {
              "name": "content_path",
              "source": "/document/normalized_images/*/new_normalized_images/imagePath"
            },
            {
              "name": "location_metadata",
              "source": "/document/normalized_images/*/new_normalized_images/location_metadata"
            },                      
            {
              "name": "document_title",
              "source": "/document/document_title"
            }                
          ]
        }
      ],
      "parameters": {
        "projectionMode": "skipIndexingParentDocuments"
      }
  },
  "knowledgeStore": {
    "storageConnectionString": "{{storageConnection}}",
    "identity": null,
    "projections": [
      {
        "files": [
          {
            "storageContainer": "{{imageProjectionContainer}}",
            "source": "/document/normalized_images/*"
          }
        ]
      }
    ]
  }
}
```

This skillset extracts text and images, vectorizes both, and shapes the image metadata for projection into the index.

Key points:

+ The `content_text` field is populated with text extracted using the Document Extraction Skill and chunked using the Split Skill

+ `content_path` contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from PDFs when `imageAction` is set to `generateNormalizedImages`, and can be mapped from the enriched document from the source field `/document/normalized_images/*/imagePath`.

+ The Azure Vision multimodal embeddings skill enables embedding of both textual and visual data using the same skill type, differentiated by input (text vs image). For more information, see [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md).

## Create and run an indexer

[Create Indexer](/rest/api/searchservice/indexers/create) creates an indexer on your search service. An indexer connects to the data source, loads data, runs a skillset, and indexes the enriched data.

```http
### Create and run an indexer
POST {{searchUrl}}/indexers?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

{
  "name": "doc-extraction-multimodal-embedding-indexer",
  "dataSourceName": "doc-extraction-multimodal-embedding-ds",
  "targetIndexName": "doc-extraction-multimodal-embedding-index",
  "skillsetName": "doc-extraction-multimodal-embedding-skillset",
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

You can start searching as soon as the first document is loaded.

```http
### Query the index
POST {{searchUrl}}/indexes/doc-extraction-multimodal-embedding-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}
  
  {
    "search": "*",
    "count": true
  }
```

Send the request. This is an unspecified full-text search query that returns all of the fields marked as retrievable in the index, along with a document count. The response should look like:

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
  "@odata.nextLink": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes/doc-extraction-multimodal-embedding-index/docs/search?api-version=2025-11-01-preview "
}
```
100 documents are returned in the response.

For filters, you can also use Logical operators (and, or, not) and comparison operators (eq, ne, gt, lt, ge, le). String comparisons are case-sensitive. For more information and examples, see [Examples of simple search queries](search-query-simple-examples.md).

> [!NOTE]
> The `$filter` parameter only works on fields that were marked filterable during index creation.

```http
### Query for only images
POST {{searchUrl}}/indexes/doc-extraction-multimodal-embedding-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}
  
  {
    "search": "*",
    "count": true,
    "filter": "image_document_id ne null"
  }
```

```http
### Query for text or images with content related to energy, returning the id, parent document, and text (only populated for text chunks), and the content path where the image is saved in the knowledge store (only populated for images)
POST {{searchUrl}}/indexes/doc-extraction-multimodal-embedding-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}
  

  {
    "search": "energy",
    "count": true,
    "select": "content_id, document_title, content_text, content_path"
  }
```

## Reset and rerun

Indexers can be reset to clear the high-water mark, which allows a full rerun. The following POST requests are for reset, followed by rerun.

```http
### Reset the indexer
POST {{searchUrl}}/indexers/doc-extraction-multimodal-embedding-indexer/reset?api-version=2025-11-01-preview   HTTP/1.1
  api-key: {{searchApiKey}}
```

```http
### Run the indexer
POST {{searchUrl}}/indexers/doc-extraction-multimodal-embedding-indexer/run?api-version=2025-11-01-preview   HTTP/1.1
  api-key: {{searchApiKey}}
```

```http
### Check indexer status 
GET {{searchUrl}}/indexers/doc-extraction-multimodal-embedding-indexer/status?api-version=2025-11-01-preview   HTTP/1.1
  api-key: {{searchApiKey}}
```

## Clean up resources

[!INCLUDE [clean up resources (paid)](/includes/resource-cleanup-paid.md)]

## See also

Now that you're familiar with a sample implementation of a multimodal indexing scenario, check out:

* [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md)
* [Vectors in Azure AI Search](vector-search-overview.md)
* [Semantic ranking in Azure AI Search](semantic-search-overview.md)
* [Tutorial: Verbalize images from a structured document layout](tutorial-document-layout-image-verbalization.md)
