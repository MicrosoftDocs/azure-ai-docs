---
title: 'Tutorial: Index multimodal content using embedding and document extraction skill'
titleSuffix: Azure AI Search
description: Learn how to extract, index, and search both text and images from Azure Blob Storage for multimodal RAG scenarios using the Azure AI Search REST APIs.

manager: arjagann
author: mdonovan
ms.author: mdonovan
ms.service: azure-ai-search
ms.custom:
ms.topic: tutorial
ms.date: 05/01/2025

---

# Tutorial: Index multimodal content using embedding and document extraction skill

Azure AI Search can extract and index both text and images from PDF documents stored in Azure Blob Storage. This tutorial shows how to build a multimodal retrieval pipeline that supports Retrieval-Augmented Generation (RAG) by embedding both text and images into a unified semantic search index.

You’ll work with a 36-page PDF document that combines rich visual content—such as charts, infographics, and scanned pages—with traditional text. Using the [Document Extraction skill](cognitive-search-skill-document-extraction.md), you’ll extract both text and normalized images. Each modality is then embedded using the same [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md), which generates dense vector representations suitable for semantic and hybrid search scenarios.

You'll use:

+ The [Document Extraction skill](cognitive-search-skill-document-extraction.md) for extracting text and normalized images.

+ Vectorization using the [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md), which generates embeddings from both text and images. The same skill is used for both modalities, with text inputs processed into embeddings for semantic search, and images processed into vector representations using Azure AI Vision models.

+ A search index configured to store text and image embeddings and support vector-based similarity search.

This tutorial demonstrates a lower-cost approach for indexing multimodal content using Document Extraction skill and image captioning. It enables extraction and search over both text and images from documents in Azure Blob Storage. However, it does not include locational metadata for text, such as page numbers or bounding regions. 

For a more comprehensive solution that includes structured text layout and spatial metadata, see [Indexing blobs with text and images for multimodal RAG scenarios using image verbalization and document layout skill](https://aka.ms/azs-multimodal).

Note: setting `imageAction` to `generateNormalizedImages` as is required for this tutorial will incur an additional charge for image extraction according to [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/).

This tutorial shows you how to  index such data, using a REST client and the [Search REST APIs](/rest/api/searchservice/) to:

> [!div class="checklist"]
> + Set up sample data and configure an `azureblob` data source
> + Create an index with support for text and image embeddings
> + Define a skillset with extraction and embedding steps
> + Create and run an indexer to process and index content
> + Search the index you just created

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ [Azure Storage](/azure/storage/common/storage-account-create).

+ [Azure AI Search](search-what-is-azure-search.md). [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription.  
  > Your service must be on the Basic tier or higher—this tutorial is not supported on the Free tier. Additionally, ensure your service is deployed in a [supported region for AI Vision](/azure/ai-services/computer-vision/overview-image-analysis#region-availability)

+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

### Download files

Download the sample PDF below:

+ [sustainable-ai-pdf](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Accelerating-Sustainability-with-AI-2025.pdf)


### Upload sample data to Azure Storage

1. In Azure Storage, create a new container named **doc-extraction-multimodality-container**.

1. [Upload the sample data file](/azure/storage/blobs/storage-quickstart-blobs-portal).

1. Get a storage connection string so that you can formulate a connection in Azure AI Search.

   1. On the left, select **Access keys**.

   1. Copy the connection string for either key one or key two. The connection string is similar to the following example:

      ```http
      DefaultEndpointsProtocol=https;AccountName=<your account name>;AccountKey=<your account key>;EndpointSuffix=core.windows.net
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
   @cognitiveServicesUrlKey= PUT-YOUR-COGNITIVE-SERVICES-URL-KEY-HERE
   @modelVersion = PUT-YOUR-VECTORIZE-MODEL-VERSION-HERE
   @imageProjectionContainer=PUT-YOUR-IMAGE-PROJECTION-CONTAINER-HERE
   ```

1. Save the file using a `.rest` or `.http` file extension.

For help with the REST client, see [Quickstart: Keyword search using REST](search-get-started-rest.md).

## Create a data source

[Create Data Source (REST)](/rest/api/searchservice/data-sources/create) creates a data source connection that specifies what data to index.

```http
### Create a data source
POST {{baseUrl}}/datasources?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

  {
    "name": "doc-extraction-multimodal-embedding-ds",
    "description": null,
    "type": "azureblob",
    "subtype": null,
    "credentials": {
      "connectionString":  "{{storageConnection}}"
    },
    "container": {
      "name": "doc-extraction-multimodality-container",
      "query": null
    },
    "dataChangeDetectionPolicy": null,
    "dataDeletionDetectionPolicy": null,
    "encryptionKey": null,
    "identity": null
  }
```

Send the request. The response should look like:

```json
HTTP/1.1 201 Created
Transfer-Encoding: chunked
Content-Type: application/json; odata.metadata=minimal; odata.streaming=true; charset=utf-8
Location: https://<YOUR-SEARCH-SERVICE-NAME>.search.windows-int.net:443/datasources('doc-extraction-multimodal-embedding-ds')?api-version=2025-05-01-preview -Preview
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
  "description": "A test datasource",
  "type": "azureblob",
  "subtype": null,
  "indexerPermissionOptions": [],
  "credentials": {
    "connectionString": null
  },
  "container": {
    "name": "doc-extraction-multimodality-container",
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
                    "apiKey": "{{}}",
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

+ Text and image embeddings are stored in the `content_embedding` field and must be configured with appropriate dimensions (e.g., 1024) and a vector search profile.

+ `location_metadata` captures bounding polygon and page number metadata for each normalized image, enabling precise spatial search or UI overlays. Note that `location_metadata` only exists for images in this scenario. If you'd like to capture locational metadata for text as well, consider using [Document Layout skill](cognitive-search-skill-document-intelligence-layout.md). An in-depth tutorial is linked at the bottom of the page.

+ For more information on vector search, see [Vectors in Azure AI Search](vector-search-overview.md).

+ For more information on semantic ranking, see [Semantic ranking in Azure AI Search](semantic-search-overview.md)

## Create a skillset

[Create Skillset (REST)](/rest/api/searchservice/skillsets/create) creates a search index on your search service. An index specifies all the parameters and their attributes.

```http
### Create a skillset
POST {{baseUrl}}/skillsets?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

{
  "name": "doc-extraction-multimodal-embedding-skillset",
	"description": "A test skillset",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Util.DocumentExtractionSkill",
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
    "@odata.type": "#Microsoft.Azure.Search.AIServicesByKey",
    "subdomainUrl": "{{cognitiveServicesUrl}}",
    "key": "{{cognitiveServicesUrlKey}}"
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

+ The Azure AI Vision multimodal embeddings skill enables embedding of both textual and visual data using the same skill type, differentiated by input (text vs image). For more information, see [Azure AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md).

## Create and run an indexer

[Create Indexer](/rest/api/searchservice/indexers/create) creates an indexer on your search service. An indexer connects to the data source, loads data, runs a skillset, and indexes the enriched data.

```http
### Create and run an indexer
POST {{baseUrl}}/indexers?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}

{
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
POST {{baseUrl}}/indexes/doc-extraction-multimodal-embedding-index/docs/search?api-version=2025-05-01-preview   HTTP/1.1
  Content-Type: application/json
  api-key: {{apiKey}}
  
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
  "@odata.nextLink": "https://<YOUR-SEARCH-SERVICE-NAME>.search.windows.net/indexes/doc-extraction-multimodal-embedding-index/docs/search?api-version=2025-05-01-preview "
}
```
100 documents are returned in the response.

For filters, you can also use Logical operators (and, or, not) and comparison operators (eq, ne, gt, lt, ge, le). String comparisons are case-sensitive. For more information and examples, see [Examples of simple search queries](search-query-simple-examples.md).

> [!NOTE]
> The `$filter` parameter only works on fields that were marked filterable during index creation.

## Reset and rerun

Indexers can be reset to clear execution history, which allows a full rerun. The following POST requests are for reset, followed by rerun.

```http
### Reset the indexer
POST {{baseUrl}}/indexers/doc-extraction-multimodal-embedding-indexer/reset?api-version=2025-05-01-preview   HTTP/1.1
  api-key: {{apiKey}}
```

```http
### Run the indexer
POST {{baseUrl}}/indexers/doc-extraction-multimodal-embedding-indexer/run?api-version=2025-05-01-preview   HTTP/1.1
  api-key: {{apiKey}}
```

```http
### Check indexer status 
GET {{baseUrl}}/indexers/doc-extraction-multimodal-embedding-indexer/status?api-version=2025-05-01-preview   HTTP/1.1
  api-key: {{apiKey}}
```

## Clean up resources

When you're working in your own subscription, at the end of a project, it's a good idea to remove the resources that you no longer need. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can use the Azure portal to delete indexes, indexers, and data sources.

## Next steps

Now that you're familiar with a sample implementation of a multimodal indexing scenario, check out

> [!div class="nextstepaction"]
> [AI Vision multimodal embeddings skill](cognitive-search-skill-vision-vectorize.md)
> [Vectors in Azure AI Search](vector-search-overview.md)
> [Semantic ranking in Azure AI Search](semantic-search-overview.md)
> [Indexing blobs with text and images for multimodal RAG scenarios using image verbalization and document layout skill](https://aka.ms/azs-multimodal)