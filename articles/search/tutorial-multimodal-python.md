---
title: 'Tutorial: Multimodal Chunking and Embedding (Python)'
titleSuffix: Azure AI Search
description: Learn how to extract, chunk, index, and search multimodal content using Python and Azure AI Search.
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - devx-track-python
ms.topic: tutorial
ms.date: 02/22/2026
---

# Tutorial: Extract, chunk, and embed multimodal content using Python

In this tutorial, you build a multimodal indexer pipeline using Python and the Azure SDK for Python.

> [!div class="checklist"]
>
> + Extract and chunk text and images
> + Vectorize text and images for similarity search
> + Send cropped images to a knowledge store for retrieval by your app

This tutorial includes multiple skillsets for showing different ways to extract, chunk, and vectorize multimodal content.

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md), Basic tier or higher for the sample data. To use Azure AI Vision multimodal, deploy Azure AI Search in a [supported region](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).

+ [Azure Storage](/azure/storage/common/storage-account-create), used for sample data and a [knowledge store](knowledge-store-concept-intro.md).

+ [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) for model access.

+ Python 3.9+ and either Visual Studio Code or a notebook environment.

### Configure access

[!INCLUDE [resource authentication](includes/resource-authentication.md)]

### Get endpoint

[!INCLUDE [resource endpoint](includes/resource-endpoint.md)]

## Prepare data

Use the same sample document and storage setup from the REST tutorial:

+ Download [sustainable-ai-pdf](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Accelerating-Sustainability-with-AI-2025.pdf).
+ Upload it to a blob container named **sustainable-ai-pdf**.
+ Assign **Storage Blob Data Reader**, **Storage Blob Contributor**, and **Storage Table Contributor** to the search service managed identity.

For full setup steps, see [Prepare data](tutorial-multimodal.md#prepare-data).

## Set up your environment

This tutorial uses the latest preview features in Azure AI Search. Install the latest preview package for Python:

```bash
pip install --pre --upgrade azure-search-documents azure-identity python-dotenv
```

Create a `.env` file:

```text
AZURE_SEARCH_ENDPOINT=https://<your-service>.search.windows.net
AZURE_SEARCH_ADMIN_KEY=<admin-key>
AZURE_SEARCH_API_VERSION=2025-11-01-preview

STORAGE_CONNECTION=ResourceId=/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>/blobServices/default
IMAGE_PROJECTION_CONTAINER=sustainable-ai-pdf-images

FOUNDRY_URL=https://<your-foundry>.cognitiveservices.azure.com/
AZURE_AI_VISION_MODEL_VERSION=2023-04-15

CHAT_COMPLETION_MODEL_URI=https://<your-openai-resource>.openai.azure.com/
CHAT_COMPLETION_MODEL_KEY=<model-key>
TEXT_EMBEDDING_MODEL_URI=https://<your-openai-resource>.openai.azure.com/
TEXT_EMBEDDING_MODEL_KEY=<model-key>
```

## Initialize clients

```python
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.core.rest import HttpRequest
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexerClient

load_dotenv()

search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
search_admin_key = os.environ["AZURE_SEARCH_ADMIN_KEY"]
api_version = os.getenv("AZURE_SEARCH_API_VERSION", "2025-11-01-preview")

credential = AzureKeyCredential(search_admin_key)
indexer_client = SearchIndexerClient(endpoint=search_endpoint, credential=credential, api_version=api_version)

index_name = "demo-multimodal-index"
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=credential)


def send_preview_request(method: str, path: str, payload: dict | None = None):
    request = HttpRequest(
        method=method,
        url=f"{search_endpoint}{path}?api-version={api_version}",
        headers={"Content-Type": "application/json"},
        json=payload,
    )
    response = indexer_client.send_request(request)
    if response.status_code >= 400:
        raise RuntimeError(f"{response.status_code}: {response.text()}")
    return response.json() if response.content else None
```

## Choose skills for multimodal indexing

Use the same skill combinations and model guidance as the REST tutorial:

+ [Choose skills for multimodal indexing](tutorial-multimodal.md#choose-skills-for-multimodal-indexing)

The Python workflow in this tutorial uses the same JSON payloads, submitted through SDK clients.

## Set up a pipeline

An indexer pipeline has four components:

+ Data source
+ Index
+ Skillset
+ Indexer

### Create a data source

```python
data_source_payload = {
    "name": "demo-multimodal-ds",
    "type": "azureblob",
    "credentials": {
        "connectionString": os.environ["STORAGE_CONNECTION"]
    },
    "container": {
        "name": "sustainable-ai-pdf"
    }
}

send_preview_request("POST", "/datasources", data_source_payload)
```

### Create an index

The index schema is the same as the REST version. For Azure AI Vision multimodal, keep `dimensions` at `1024` and use `aiServicesVision` vectorizer. For text embeddings, use the dimensions that match your model.

```python
index_payload = {
    "name": "demo-multimodal-index",
    "fields": [
        {"name": "content_id", "type": "Edm.String", "key": True, "retrievable": True, "analyzer": "keyword"},
        {"name": "text_document_id", "type": "Edm.String", "filterable": True, "retrievable": True, "stored": True},
        {"name": "document_title", "type": "Edm.String", "searchable": True},
        {"name": "image_document_id", "type": "Edm.String", "filterable": True, "retrievable": True},
        {"name": "content_text", "type": "Edm.String", "searchable": True, "retrievable": True},
        {"name": "content_embedding", "type": "Collection(Edm.Single)", "dimensions": 1024, "searchable": True, "retrievable": True, "vectorSearchProfile": "hnsw"},
        {"name": "content_path", "type": "Edm.String", "retrievable": True},
        {"name": "offset", "type": "Edm.String", "retrievable": True},
        {
            "name": "location_metadata",
            "type": "Edm.ComplexType",
            "fields": [
                {"name": "page_number", "type": "Edm.Int32", "retrievable": True},
                {"name": "bounding_polygons", "type": "Edm.String", "retrievable": True}
            ]
        }
    ],
    "vectorSearch": {
        "profiles": [
            {"name": "hnsw", "algorithm": "defaulthnsw", "vectorizer": "demo-vectorizer"}
        ],
        "algorithms": [
            {
                "name": "defaulthnsw",
                "kind": "hnsw",
                "hnswParameters": {"m": 4, "efConstruction": 400, "metric": "cosine"}
            }
        ],
        "vectorizers": [
            {
                "name": "demo-vectorizer",
                "kind": "aiServicesVision",
                "aiServicesVisionParameters": {
                    "resourceUri": os.environ["FOUNDRY_URL"],
                    "authIdentity": None,
                    "modelVersion": os.environ.get("AZURE_AI_VISION_MODEL_VERSION", "2023-04-15")
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
                    "titleField": {"fieldName": "document_title"},
                    "prioritizedContentFields": [],
                    "prioritizedKeywordsFields": []
                }
            }
        ]
    }
}

send_preview_request("POST", "/indexes", index_payload)
```

### Create a skillset for extraction, chunking, and vectorization

Use one of the four skillset combinations from the REST tutorial, and submit it through Python:

+ Document extraction + multimodal embedding
+ Document extraction + text embedding
+ Document layout + multimodal embedding
+ Document layout + text embedding

```python
# Build one of the skillset payloads from tutorial-multimodal.md
skillset_payload = {
    "name": "demo-multimodal-skillset",
    "description": "Multimodal extraction, chunking, and embedding",
    "skills": [
        # Paste one of the skillset combinations here.
    ],
    "indexProjections": {
        # Paste matching index projection mappings here.
    }
}

send_preview_request("POST", "/skillsets", skillset_payload)
```

### Create and run an indexer

```python
indexer_payload = {
    "name": "demo-multimodal-indexer",
    "dataSourceName": "demo-multimodal-ds",
    "targetIndexName": "demo-multimodal-index",
    "skillsetName": "demo-multimodal-skillset",
    "parameters": {
        "maxFailedItems": -1,
        "maxFailedItemsPerBatch": 0,
        "batchSize": 1,
        "configuration": {
            "allowSkillsetToReadFileData": True
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

send_preview_request("POST", "/indexers", indexer_payload)
```

## Run queries

### Query all content

```python
results = search_client.search(search_text="*", include_total_count=True)
print(f"Document count: {results.get_count()}")
for doc in results:
    print(doc.get("content_id"), doc.get("document_title"))
```

### Query image-only content

```python
results = search_client.search(
    search_text="*",
    filter="image_document_id ne null",
    include_total_count=True,
)

for doc in results:
    print(doc.get("content_id"), doc.get("content_path"))
```

### Query for content related to energy

```python
results = search_client.search(
    search_text="energy",
    include_total_count=True,
    select=["content_id", "document_title", "content_text", "content_path"],
)

for doc in results:
    print(doc)
```

## Reset and rerun the indexer

```python
send_preview_request("POST", "/indexers/demo-multimodal-indexer/reset")
send_preview_request("POST", "/indexers/demo-multimodal-indexer/run")
status = send_preview_request("GET", "/indexers/demo-multimodal-indexer/status")
print(status)
```

## View images in the knowledge store

After indexing runs, the `sustainable-ai-pdf-images` container should contain extracted image files.

For portal steps, see [View images in the knowledge store](tutorial-multimodal.md#view-images-in-the-knowledge-store).

## Clean up resources

[!INCLUDE [clean up resources (paid)](includes/resource-cleanup-paid.md)]
