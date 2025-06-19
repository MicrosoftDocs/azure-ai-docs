---
title: 'Tutorial: Use Multimodal Embeddings and Document Layout Skill for Multimodal Indexing'
titleSuffix: Azure AI Search
description: Learn how to extract, index, and search multimodal content using the Document Layout skill for chunking and Azure AI Vision for embeddings.

manager: arjagann
author: rawan
ms.author: rawan
ms.service: azure-ai-search
ms.custom:
ms.topic: tutorial
ms.date: 06/11/2025

---

# Tutorial: Index mixed content using multimodal embeddings and the Document Layout skill

<!-- Multimodal plays an essential role in generative AI apps and the user experience as it enables the extraction of information not only from text but also from complex images embedded within documents.  -->
In this Azure AI Search tutorial, learn how to build a multimodal indexing pipeline that chunks data based on document structure, and uses a multimodal embedding model to vectorize text and images in a searchable index.

In this tutorial, you use:

+ A 36-page PDF document that combines rich visual content, such as charts, infographics, and scanned pages, with traditional text.

+ The [Document Layout skill (preview)](cognitive-search-skill-document-intelligence-layout.md) for extracting text and normalized images with its locationMetadata from various documents, such as page numbers or bounding regions.

  The [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md) has limited regional availability, is bound to Azure AI services, and requires a [billable resource](cognitive-search-attach-cognitive-services.md) for transactions that exceed 20 documents per indexer per day. For a lower-cost solution to indexing multimodal content, see [Index multimodal content using image verbalization and Document Extraction skill](tutorial-document-extraction-image-verbalization.md).

+ Vectorization using the [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md), which generates embeddings for both text and images.

+ A search index configured to store text and image embeddings and support for vector-based similarity search.

Using a REST client and the [Search REST APIs](/rest/api/searchservice/), you will:

> [!div class="checklist"]
> + Set up sample data and configure an `azureblob` data source
> + Create an index with support for text and image embeddings
> + Define a skillset with extraction, embedding and knowleage store file projection steps
> + Create and run an indexer to process and index content
> + Search the index you just created

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ [Azure Storage](/azure/storage/common/storage-account-create).

+ An [Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills) for image vectorization. Image vectorization requires Azure AI Vision multimodal embeddings. For an updated list of regions, see the [Azure AI Vision documentation](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).

+ [Azure AI Search](search-what-is-azure-search.md), with a managed identity. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. Your service must be on the Basic tier or higher—this tutorial isn't supported on the Free tier. It must also be in the same region as your multi-service account.

+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

### Download files

Download the following sample PDF:

+ [sustainable-ai-pdf](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Accelerating-Sustainability-with-AI-2025.pdf)


### Upload sample data to Azure Storage

1. In Azure Storage, create a new container named **doc-intelligence-multimodality-container**.

1. [Upload the sample data file](/azure/storage/blobs/storage-quickstart-blobs-portal).

1. [Create a role assignment in Azure Storage and specify a managed identity in a connection string](search-howto-managed-identities-storage.md)

   1. For connections made using a system-assigned managed identity, provide a connection string that contains a ResourceId, with no account key or password. The ResourceId must include the subscription ID of the storage account, the resource group of the storage account, and the storage account name. The connection string is similar to the following example:

        ```json
        "credentials" : { 
            "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
        }
        ```
   1. For connections made using a user-assigned managed identity. Provide a connection string that contains a ResourceId, with no account key or password. The ResourceId must include the subscription ID of the storage account, the resource group of the storage account, and the storage account name. Provide an identity using the syntax shown in the following example. Set userAssignedIdentity to the user-assigned managed identity The connection string is similar to the following example:

        ```json
        "credentials" : { 
            "connectionString" : "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;" 
        },
        "identity" : { 
            "@odata.type": "#Microsoft.Azure.Search.DataUserAssignedIdentity",
            "userAssignedIdentity" : "/subscriptions/00000000-0000-0000-0000-00000000/resourcegroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.ManagedIdentity/userAssignedIdentities/MY-DEMO-USER-MANAGED-IDENTITY" 
        }
    ```

### Copy a search service URL and API key

For this tutorial, connections to Azure AI Search require an endpoint and an API key. You can get these values from the Azure portal. For alternative connection methods, see [Managed identities](search-howto-managed-identities-data-sources.md).

1. Sign in to the [Azure portal](https://portal.azure.com), navigate to the search service **Overview** page, and copy the URL. An example endpoint might look like `https://mydemo.search.windows.net`.

1. Under **Settings** > **Keys**, copy an admin key. Admin keys are used to add, modify, and delete objects. There are two interchangeable admin keys. Copy either one.

   :::image type="content" source="media/search-get-started-rest/get-url-key.png" alt-text="Screenshot of the URL and API keys in the Azure portal.":::

## Set up your REST file

1. Start Visual Studio Code and create a new file.

1. Provide values for variables used in the request.

   ```http
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
   @apiKey = PUT-YOUR-ADMIN-API-KEY-HERE
   @storageConnection = PUT-YOUR-STORAGE-CONNECTION-STRING-HERE
   @cognitiveServicesUrl = PUT-YOUR-COGNITIVE-SERVICES-URL-HERE
   @cognitiveServicesKey= PUT-YOUR-COGNITIVE-SERVICES-URL-KEY-HERE
   @modelVersion = PUT-YOUR-VECTORIZE-MODEL-VERSION-HERE
   @imageProjectionContainer=PUT-YOUR-IMAGE-PROJECTION-CONTAINER-HERE
   ```

1. Save the file using a `.rest` or `.http` file extension.

For help with the REST client, see [Quickstart: Keyword search using REST](search-get-started-rest.md).

## Create a data source

[Create Data Source (REST)](/rest/api/searchservice/data-sources/create) creates a data source connection that specifies what data to index.

```http
### Create a data source using system-assigned managed identities
POST {{baseUrl}}/datasources?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

  {
    "name": "doc-intelligence-multimodal-embedding-ds",
    "description": "A data source to store multimodal documents",
    "type": "azureblob",
    "subtype": null,
    "credentials": {
      "connectionString":  "ResourceId=/subscriptions/00000000-0000-0000-0000-00000000/resourceGroups/MY-DEMO-RESOURCE-GROUP/providers/Microsoft.Storage/storageAccounts/MY-DEMO-STORAGE-ACCOUNT/;"
    },
    "container": {
      "name": "doc-intelligence-multimodality-container",
      "query": null
    },
    "dataChangeDetectionPolicy": null,
    "dataDeletionDetectionPolicy": null,
    "encryptionKey": null,
    "identity": null
  }

```

## Create an index

[Create Index (REST)](/rest/api/searchservice/indexes/create) creates a search index on your search service. An index specifies all the parameters and their attributes.

For nested JSON, the index fields must be identical to the source fields. Currently, Azure AI Search doesn't support field mappings to nested JSON, so field names and data types must match completely. The following index aligns to the JSON elements in the raw content.

```http
### Create an index
POST {{baseUrl}}/indexes?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

{
    "name": "doc-intelligence-multimodal-embedding-index",
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
                "vectorizer": "{{vectorizer}}"
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
                "name": "{{ vectorizer }}",
                "kind": "aiServicesVision",
                "aiServicesVisionParameters": {
                    "resourceUri": "{{cognitiveServicesUrl}}",
                    "apiKey": "{{cognitiveServicesKey}}",
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

+ `location_metadata` captures bounding polygon and page number metadata for each text chunk and normalized image, enabling precise spatial search or UI overlays.

+ For more information on vector search, see [Vectors in Azure AI Search](vector-search-overview.md).

+ For more information on semantic ranking, see [Semantic ranking in Azure AI Search](semantic-search-overview.md).

## Create a skillset

[Create Skillset (REST)](/rest/api/searchservice/skillsets/create) creates a search index on your search service. An index specifies all the parameters and their attributes.

```http
### Create a skillset
POST {{baseUrl}}/skillsets?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

{
  "name": "doc-intelligence-multimodal-embedding-skillset",
  "description": "A sample skillset for multimodal using multimodal embedding",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
      "name": "document-layout-skill",
      "description": "Document Intelligence skill for document cracking",
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
    { 
      "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill", 
      "name": "text-embedding-skill",
      "description": "Vision Vectorization skill for text",
      "context": "/document/text_sections/*", 
      "modelVersion": "2023-04-15", 
      "inputs": [ 
        { 
          "name": "text", 
          "source": "/document/text_sections/*/content" 
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
      "modelVersion": "2023-04-15", 
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
      "context": "/document/normalized_images/*",
      "inputs": [
        {
          "name": "normalized_images",
          "source": "/document/normalized_images/*",
          "inputs": []
        },
        {
          "name": "imagePath",
          "source": "='my_container_name/'+$(/document/normalized_images/*/imagePath)",
          "inputs": []
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
          "targetIndexName": "{{index}}",
          "parentKeyFieldName": "text_document_id",
          "sourceContext": "/document/text_sections/*",
          "mappings": [    
            {
            "name": "content_embedding",
            "source": "/document/text_sections/*/text_vector"
            },                      
            {
              "name": "content_text",
              "source": "/document/text_sections/*/content"
            },
            {
              "name": "location_metadata",
              "source": "/document/text_sections/*/locationMetadata"
            },                
            {
              "name": "document_title",
              "source": "/document/document_title"
            }   
          ]
        },        
        {
          "targetIndexName": "{{index}}",
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
              "name": "document_title",
              "source": "/document/document_title"
            },
            {
              "name": "location_metadata",
              "source": "/document/normalized_images/*/locationMetadata"
            }             
          ]
        }
      ],
      "parameters": {
        "projectionMode": "skipIndexingParentDocuments"
      }
  },  
  "knowledgeStore": {
    "storageConnectionString": "",
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

+ The `content_text` field is populated with text extracted and chunked using the Document Layout Skill

+ `content_path` contains the relative path to the image file within the designated image projection container. This field is generated only for images extracted from documents when `extractOption` is set to `["images", "locationMetadata"]` or `["images"]`, and can be mapped from the enriched document from the source field `/document/normalized_images/*/imagePath`.

+ The Azure AI Vision multimodal embeddings skill enables embedding of both textual and visual data using the same skill type, differentiated by input (text vs image). For more information, see [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md).

## Create and run an indexer

[Create Indexer](/rest/api/searchservice/indexers/create) creates an indexer on your search service. An indexer connects to the data source, loads data, runs a skillset, and indexes the enriched data.

```http
### Create and run an indexer
POST {{baseUrl}}/indexers?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

{
  "dataSourceName": "doc-intelligence-multimodal-embedding-ds",
  "targetIndexName": "doc-intelligence-multimodal-embedding-index",
  "skillsetName": "doc-intelligence-multimodal-embedding-skillset",
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
POST {{baseUrl}}/indexes/doc-intelligence-multimodal-embedding-index/docs/search?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}
  
  {
    "search": "*",
    "count": true
  }
```

Send the request. This is an unspecified full-text search query that returns all of the fields marked as retrievable in the index, along with a document count. The response should look like:

```json
{
  "@odata.count": 100,
  "@search.nextPageParameters": {
    "search": "*",
    "count": true,
    "skip": 50
  },
  "value": [
  ],
  "@odata.nextLink": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes/doc-intelligence-multimodal-embedding-index/docs/search?api-version=2025-05-01-preview "
}
```
100 documents are returned in the response.

For filters, you can also use Logical operators (and, or, not) and comparison operators (eq, ne, gt, lt, ge, le). String comparisons are case-sensitive. For more information and examples, see [Examples of simple search queries](search-query-simple-examples.md).

> [!NOTE]
> The `$filter` parameter only works on fields that were marked filterable during index creation.

```http
### Query for only images
POST {{baseUrl}}/indexes/doc-intelligence-multimodal-embedding-index/docs/search?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}
  
  {
    "search": "*",
    "count": true,
    "filter": "image_document_id ne null"
  }
```

```http
### Query for text or images with content related to energy, returning the id, parent document, and text (only populated for text chunks), and the content path where the image is saved in the knowledge store (only populated for images)
POST {{baseUrl}}/indexes/doc-intelligence-multimodal-embedding-index/docs/search?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}
  
  {
    "search": "energy",
    "count": true,
    "select": "content_id, document_title, content_text, content_path"
  }
```

## Reset and rerun

Indexers can be reset to clear execution history, which allows a full rerun. The following POST requests are for reset, followed by rerun.

```http
### Reset the indexer
POST {{baseUrl}}/indexers/doc-intelligence-multimodal-embedding-indexer/reset?api-version=2025-05-01-preview   HTTP/1.1
  api-key: {{apiKey}}
```

```http
### Run the indexer
POST {{baseUrl}}/indexers/doc-intelligence-multimodal-embedding-indexer/run?api-version=2025-05-01-preview   HTTP/1.1
  api-key: {{apiKey}}
```

```http
### Check indexer status 
GET {{baseUrl}}/indexers/doc-intelligence-multimodal-embedding-indexer/status?api-version=2025-05-01-preview   HTTP/1.1
  api-key: {{apiKey}}
```

## Clean up resources

When you're working in your own subscription, at the end of a project, it's a good idea to remove the resources that you no longer need. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can use the Azure portal to delete indexes, indexers, and data sources.

## See also

Now that you're familiar with a sample implementation of a multimodal indexing scenario, check out:

+ [AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md)
+ [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md)
+ [Vectors in Azure AI Search](vector-search-overview.md)
+ [Semantic ranking in Azure AI Search](semantic-search-overview.md)
+ [Index multimodal content using embeddings and Document Extraction skill](tutorial-document-extraction-multimodal-embeddings.md)
