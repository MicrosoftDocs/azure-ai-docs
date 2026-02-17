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

In this tutorial, you will build a multimodal indexer pipeline that performs these tasks:

> [!div class="checklist"]
>
> + Extract and and chunk text and images
> + Vectorize text and images for similarity search
> + Send cropped images to a knowledge store for retrieval by your app

Multimodal sample data is a 36-page PDF document that combines rich visual content, such as charts, infographics, and scanned pages, with original text.

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md), any region, on the basic pricing tier or higher if you want to use the sample data. To complete this tutorial on the free tier, use a smaller a document with fewer images. We recommend [configuring a managed identity](search-how-to-managed-identities.md) for role-based access to models and data.

+ [Azure Storage](/azure/storage/common/storage-account-create), used for storing sample data and for creating a [knowledge store](knowledge-store-concept-intro.md).

+ [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) that provides Foundry models and APIs.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). If you haven't installed a suitable version of Python, follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter).

> [!NOTE]
>  Multimodal indexing is implemented through skills that call Foundry models and APIs in an indexer pipeline. This tutorial uses Foundry models only, but the skills themselves support other models. Model prerequisites vary depending on the [skill choice for each task](#choose-skills-for-multimodal-indexing).

### Configure access

[!INCLUDE [resource authentication](includes/resource-authentication.md)]

### Get endpoint

[!INCLUDE [resource endpoint](includes/resource-endpoint.md)]

### Prepare data

Azure Storage provides the sample data and hosts the knowledge store. A search service managed identity needs:

+ Read access to Azure Storage to retrieve the sample data.

+ Write access to create the knowledge store. The search service creates the container for cropped images during skillset processing, using the name you provide in an environment variable.

Follow these steps to set up the sample data.

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

## Choose skills for multimodal indexing

The index, data source, and indexer definitions are the same for all scenarios, but the skillset can include a different skill combination depending on how you want to extract, chunk, and vectorize text and images.

1. Choose a skill or skill combination that extracts and chunks content.

1. Choose a skill or skill combination that vectorizes content:

   + Choose Azure AI Vision for text and image vectorization.

   + Choose GenAI Prompt to generate text descriptions of images, and Azure OpenAI embedding to vectorize raw and generated text.

Most skills depend on access to [deployed model](/azure/ai-foundry/foundry-models/how-to/deploy-foundry-models). Here's a list of the models backing the skills used in this tutorial:

| Model | Skill | Usage | Permissions |
| -- | -- | -- | -- |
| None (built-in) | [Document Extraction skill](cognitive-search-skill-document-extraction.md), [Text Split skill](cognitive-search-skill-textsplit.md) | Extract and chunk based on fixed size. <br>Text extraction is free. <br>[Image extraction is billable](https://azure.microsoft.com/pricing/details/search/). | See [Configure access](#configure-access) |
| Document Intelligence 4.0 | [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) | Extract and chunk based on document layout. | Cognitive Services User |
| Azure AI Vision multimodal 4.0 | [Azure AI Vision skill](cognitive-search-skill-vision-vectorize.md) | Vectorize text and image content. | Cognitive Services User |
| GPT-5 or GPT-4 | [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)  | Generate text descriptions of image content. | Cognitive Services OpenAI User |
| Text-embedding-3 (large or small) or text-embedding-ada-002 | [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md) | Vectorize text and generated image descriptions. | Cognitive Services User |

Model usage is billable, except for text extraction using a built-in model and text splitting.

Model deployments can be in any region if the search service connects over the public endpoint or a private connection. However, two models are accessed over the internal network, which can introduce a regional dependency. 

If you use a key-based connection, [attach a Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md) and ensure your model meets the same-region requirements for Azure AI Search:

+ [Azure AI Vision multimodal 4.0 regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability)

+ [Document Layout 4.0 regions](cognitive-search-skill-document-intelligence-layout.md#supported-regions)

To relax regional dependencies, [set up a keyless connection](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) to your Foundry resource.

## Set up your environment

<!-- variables vary for each model, split into core and model-specific variables, use a step to add variables for each model type -->
For this tutorial, your local REST client connection to Azure AI Search requires an endpoint and an API key. You can get these values from the Azure portal. For alternative connection methods, see [Connect to a search service](search-get-started-rbac.md).

For authenticated connections that occur during indexer and skillset processing, the search service uses the role assignments you previously defined.

1. Start Visual Studio Code and create a new file.

1. Provide values for variables used in the request:

   ```http
    @searchUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
    @searchApiKey = PUT-YOUR-ADMIN-API-KEY-HERE
    @storageConnection = PUT-YOUR-STORAGE-CONNECTION-STRING-HERE
    @cognitiveServicesUrl = PUT-YOUR-AZURE-AI-FOUNDRY-ENDPOINT-HERE
    @modelVersion = 2023-04-15
    @imageProjectionContainer=sustainable-ai-pdf-images
   ```

   For `@storageConnection`, make sure your connection string doesn't have a trailing semicolon or quotation marks. 

   For `@imageProjectionContainer`, provide a container name that's unique in blob storage. Azure AI Search creates this container during skills processing.

1. Save the file using a `.rest` or `.http` file extension. For help with the REST client, see [Quickstart: Full-text search using REST](search-get-started-text.md).

## Set up a pipeline

There are four components of an indexer pipeline: data source, index, skillset, and indexer. You create all four objects in this section, except that skill definitions are covered in separate sections related to chunking and vectorization. We approach skills this way to bring more focus on the behaviors that you want to effect.

+ [Create a data source](#create-a-data-source)
+ [Create an index](#create-an-index)
+ [Create a basic skillset definition](#stub-out-a-skillset-definition)
+ [Add skills for extraction and chunking](#extract-and-chunk-text)
+ [Add skills for vectorization](#vectorize-multimodal-content)
+ [Create (and run) an indexer](#run-the-indexer)

### Create a data source

[Create Data Source (REST)](/rest/api/searchservice/data-sources/create) creates a data source connection that specifies what data to index.

```http
POST {{searchUrl}}/datasources?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

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

[Create Index (REST)](/rest/api/searchservice/indexes/create) creates a search index on your search service. 

For nested JSON, the index fields must be identical to the source fields. Currently, Azure AI Search doesn't support field mappings to nested JSON, so field names and data types must match completely. The following index aligns to the JSON elements in the raw content.

<!-- Dimensions and vectorizer params vary by skill.
Image verbalization tutorials: 3072 (text-embedding-3-large)
Multimodal embeddings tutorials: 1024 (Azure AI Vision multimodal 4.0)
Vectorizer type:

Image verbalization: azureOpenAI vectorizer
Multimodal embeddings: aiServicesVision vectorizer -->

```http
### Create an index
POST {{searchUrl}}/indexes?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

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

[Create Skillset (REST)](/rest/api/searchservice/skillsets/create) creates a skillset on your search service. A skillset defines the operations that extract, chunk, and vectorize content prior to indexing.

Here's the basic definition. In the sections that follow, you'll add skills based on the behaviors you want for content extraction, chunking, and vectorization.

```http
### Create a skillset
POST {{searchUrl}}/skillsets?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

{
  "name": "demo-multimodal-skillset",
  "description": "A test skillset",
  "skills": [ SKILLS ADDED IN NEXT SECTIONS ],
  "cognitiveServices": {
    "@odata.type": "#Microsoft.Azure.Search.AIServicesByIdentity",
    "subdomainUrl": "{{cognitiveServicesUrl}}",
    "identity": null
  },
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

## Extract and chunk text

Recall that your skill choices for extraction and chunking include:

| Model | Skill | Usage | Permissions |
| -- | -- | -- | -- |
| None (built-in) | [Document Extraction skill](cognitive-search-skill-document-extraction.md), [Text Split skill](cognitive-search-skill-textsplit.md) | Extract and chunk based on fixed size. Text extraction is free. [Image extraction is billable](https://azure.microsoft.com/pricing/details/search/). | See [Configure access](#configure-access) |
| Document Intelligence 4.0 | [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) | Extract and chunk based on document layout. | Cognitive Services User |

Choose either approach for the skills array of your skillset.

### [**Document Extraction and Text Split**](#tab/doc-extraction)

```json
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
```

### [**Document Layout**](#tab/doc-layout)

```json
    {
      "@odata.type": "#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
      "name": "document-cracking-skill",
      "description": "Document Layout skill for document cracking",
      "context": "/document",
      "outputMode": "oneToMany",
      "outputFormat": "text",
      "extractionOptions": ["images", "locationMetadata"],
      "chunkingProperties": {     
          "unit": "characters",
          "maximumLength": 2000, 
          "overlapLength": 200
      },
      "inputs": [
        {
          "name": "file_data",
          "source": "/document/file_data"
        }
      ],
      "outputs": [
        { 
          "name": "text_sections", 
          "targetName": "text_sections" 
        }, 
        { 
          "name": "normalized_images", 
          "targetName": "normalized_images" 
        } 
      ]
    },
```

---

Key points:

+ The `content_text` field is populated with text extracted using the Document Extraction Skill and chunked using the Split Skill

+ `content_path` contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from PDFs when `imageAction` is set to `generateNormalizedImages`, and can be mapped from the enriched document from the source field `/document/normalized_images/*/imagePath`.

+ The Azure Vision multimodal embeddings skill enables embedding of both textual and visual data using the same skill type, differentiated by input (text vs image). For more information, see [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md).

## Vectorize multimodal content

Recall that your skill choices for vectorization include:

| Model | Skill | Usage | Permissions |
| -- | -- | -- | -- |
| Azure AI Vision multimodal 4.0 | [Azure AI Vision skill](cognitive-search-skill-vision-vectorize.md) | Vectorize text and image content. | Cognitive Services User |
| GPT-5 or GPT-4 | [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)  | Generate text descriptions of image content. | Cognitive Services OpenAI User |
| Text-embedding-3 (large or small) or text-embedding-ada-002 | [Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md) | Vectorize text and generated image descriptions. | Cognitive Services User |

Choose either approach for the skills array of your skillset.

### [**Azure AI Vision**](#tab/vision)

The [Azure Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md) vectorizes textual and visual data using the same skill type, differentiated by input (text vs image).

This skillset extracts text and images, vectorizes both, and shapes the image metadata for projection into the index.

```json
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
    },
```

### [**Image Verbalization and Text Embedding**](#tab/gpt-text-embedding)

This skillset vectorizes text, verbalizes images as text, and then vectorizes the text descriptions. It also shapes the image metadata for projection into the index.

```json
  {
    "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
    "name": "text-embedding-skill",
    "description": "Embedding skill for text",
    "context": "/document/pages/*",
    "inputs": [
        {
        "name": "text",
        "source": "/document/pages/*"
        }
    ],
    "outputs": [
        {
        "name": "embedding",
        "targetName": "text_vector"
        }
    ],
    "resourceUri": "{{openAIResourceUri}}",
    "deploymentId": "text-embedding-3-large",
    "searchApiKey": "{{openAIKey}}",
    "dimensions": 3072,
    "modelName": "text-embedding-3-large"
    },
    {
    "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
    "name": "genAI-prompt-skill",
    "description": "GenAI Prompt skill for image verbalization",
    "uri": "{{chatCompletionResourceUri}}",
    "timeout": "PT1M",
    "searchApiKey": "{{chatCompletionKey}}",
    "context": "/document/normalized_images/*",
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
    ],
    "resourceUri": "{{openAIResourceUri}}",
    "deploymentId": "text-embedding-3-large",
    "searchApiKey": "{{openAIKey}}",
    "dimensions": 3072,
    "modelName": "text-embedding-3-large"
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
    },
```
---

Key points:

+ The `content_text` field is populated with text extracted using the Document Extraction Skill and chunked using the Split Skill

+ `content_path` contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from PDFs when `imageAction` is set to `generateNormalizedImages`, and can be mapped from the enriched document from the source field `/document/normalized_images/*/imagePath`.

## Run the indexer

[Create Indexer](/rest/api/searchservice/indexers/create) creates an indexer on your search service. An indexer connects to the data source, loads data, runs a skillset, and indexes the enriched data.

```http
### Create and run an indexer
POST {{searchUrl}}/indexers?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}

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

You can start searching as soon as the first document is loaded.

```http
### Query the index
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
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
  "@odata.nextLink": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview "
}
```
100 documents are returned in the response.

For filters, you can also use Logical operators (and, or, not) and comparison operators (eq, ne, gt, lt, ge, le). String comparisons are case-sensitive. For more information and examples, see [Examples of simple search queries](search-query-simple-examples.md).

The `$filter` parameter only works on fields that were marked filterable during index creation.

```http
### Query for only images
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
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
POST {{searchUrl}}/indexes/demo-multimodal-index/docs/search?api-version=2025-11-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{searchApiKey}}
  

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
  api-key: {{searchApiKey}}
```

```http
### Run the indexer
POST {{searchUrl}}/indexers/demo-multimodal-indexer/run?api-version=2025-11-01-preview   HTTP/1.1
  api-key: {{searchApiKey}}
```

```http
### Check indexer status 
GET {{searchUrl}}/indexers/demo-multimodal-indexer/status?api-version=2025-11-01-preview   HTTP/1.1
  api-key: {{searchApiKey}}
```

## Clean up resources

[!INCLUDE [clean up resources (paid)](includes/resource-cleanup-paid.md)]
