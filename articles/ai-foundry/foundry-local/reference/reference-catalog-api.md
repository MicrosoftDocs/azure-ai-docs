---
title: Catalog API Reference
titleSuffix: Foundry Local
description: Complete reference guide for the Foundry Local Model Catalog API.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: reference
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

# Catalog API Reference

Foundry Local allows you to develop and integrate your own catalog service. This document provides guidance on:

- The model format required for the catalog API.
- The model storage requirements.
- The request and response format required for your catalog API to integrate with Foundry Local.

## Model format

The model files hosted in your model catalog are required to be in the [Open Neural Network Exchange (ONNX)](https://onnx.ai/) format to work with Foundry Local. For more information on how to compile Hugging Face and PyTorch models to ONNX, see the [Compile Hugging Face models to run on Foundry Local](../how-to/how-to-compile-hugging-face-models.md) article.

## Model Storage

The model files should be stored on [Azure Blob Storage](https://learn.microsoft.com/azure/storage/blobs/storage-blobs-introduction). The model catalog service should be able to access the model files stored in Azure Blob Storage.

## API format

### Request

Your catalog service needs to support a POST endpoint that accepts a JSON request body. The request format for the catalog API is as follows:

- **Method**: `POST`
- **Content-Type**: `application/json`

The request body *must* be a JSON object that *accepts* the following fields:

- `resourceIds`: An array of resource IDs that specify the resources to be queried.
    - `resourceId`: The ID of the resource.
    - `entityContainerType`: The type of entity container (for example, `Registry`, `Workspace`, etc.).
- `indexEntitiesRequest`: An object that contains the search parameters.
  - `filters`: An array of filter objects that specify the criteria for filtering the search results.
      - `field`: The field to filter on (for example, `type`, `kind`, etc.).
      - `operator`: The operator to use for the filter. For example, `eq` (equals), `ne` (not equals), `gt` (greater than), `lt` (less than), etc.
      - `values`: An array of values to match against the field.
  - `orderBy`: An array of fields to order the results by.
  - `searchText`: A string to search for in the results.
  - `pageSize`: The maximum number of results to return (for pagination).
  - `skip`: The number of results to skip (for pagination).
  - `continuationToken`: A token for pagination to continue from a previous request.

#### Filterable Fields (optional)

You *must* implement your catalog API that *accepts* the [Request](#request) format, but it's *optional* as to whether you implement server-side filtering in your catalog service. Not implementing server-side filtering is a fast way to implement your catalog service, but it might not be efficient way to search for models.

If you choose to implement server-side filtering, you can use the following fields to filter the results:

- `type`: The type of the model (for example, `models`, `datasets`, etc.).
- `kind`: The kind of the model (for example, `Versioned`, `Unversioned`, etc.).
- `properties/variantInfo/variantMetadata/device`: The device type (for example, `cpu`, `gpu`, etc.).
- `properties/variantInfo/variantMetadata/executionProvider`: The execution provider (for example, `cpuexecutionprovider`, `webgpuexecutionprovider`, etc.).


#### Example request

```bash
curl POST <your-catalog-api-endpoint> \
-H "Content-Type: application/json" \
-d '{
  "resourceIds": [
    {
      "resourceId": "azureml",
      "entityContainerType": "Registry"
    }
  ],
  "indexEntitiesRequest": {
    "filters": [
      {
        "field": "type",
        "operator": "eq",
        "values": [
          "models"
        ]
      },
      {
        "field": "kind",
        "operator": "eq",
        "values": [
          "Versioned"
        ]
      },
      {
        "field": "properties/variantInfo/variantMetadata/device",
        "operator": "eq",
        "values": [
          "cpu",
          "gpu"
        ]
      },
      {
        "field": "properties/variantInfo/variantMetadata/executionProvider",
        "operator": "eq",
        "values": [
          "cpuexecutionprovider",
          "webgpuexecutionprovider"
        ]
      }
    ],
    "pageSize": 10,
    "skip": null,
    "continuationToken": null
  }
}'
```

### Response

The response from the catalog API is a JSON object that contains the search results. The response schema is as follows:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "indexEntitiesResponse": {
      "type": "object",
      "properties": {
        "totalCount": {
          "type": "integer",
          "description": "The total count of entities."
        },
        "value": {
          "type": "array",
          "description": "An array of LocalModel objects.",
          "items": {
            "$ref": "#/definitions/LocalModel"
          }
        },
        "nextSkip": {
          "type": "integer",
          "description": "The number of items to skip for the next request."
        },
        "continuationToken": {
          "type": "string",
          "description": "A token to continue fetching results."
        },
      }
    }
  },
  "definitions": {
    "LocalModel": {
      "type": "object",
      "properties": {
        "annotations": {
          "type": "object",
          "description": "Annotations associated with the model.",
          "properties": {
            "tags": {
              "type": "object",
              "description": "Tags associated with the annotation.",
              "properties": {
                "author": { "type": "string" },
                "alias": { "type": "string" },
                "directoryPath": { "type": "string" },
                "license": { "type": "string" },
                "licenseDescription": { "type": "string" },
                "promptTemplate": { "type": "string" },
                "task": { "type": "string" }
              }
            },
            "systemCatalogData": {
              "type": "object",
              "properties": {
                "publisher": { "type": "string" },
                "displayName": { "type": "string" },
              }
            },
            "name": { "type": "string" }
          }
        },
        "properties": {
          "type": "object",
          "description": "Properties of the model.",
          "properties": {
            "name": { "type": "string" },
            "version": { "type": "integer" },
            "alphanumericVersion": { "type": "string" },
            "variantInfo": {
              "type": "object",
              "properties": {
                "parents": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "assetId": { "type": "string" }
                    }
                  }
                },
                "variantMetadata": {
                  "type": "object",
                  "properties": {
                    "modelType": { "type": "string" },
                    "device": { "type": "string" },
                    "executionProvider": { "type": "string" },
                    "fileSizeBytes": { "type": "integer" }
                  }
                }
              }
            }
          }
        },
        "version": {
          "type": "string",
          "description": "The version of the model."
        },
        "assetId": {
          "type": "string",
          "description": "The asset ID of the model."
        }
      }
    }
  }
}
```

> [!NOTE]
> The `assetID` should be the Azure Blob storage URL of the folder containing the model. For example, `https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{MODEL_PATH}`.

