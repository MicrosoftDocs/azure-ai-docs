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

This document provides a detailed reference for catalog implementers that want to create their own catalog implementations to be integrated with Foundry Local.

The catalog API is a RESTful API that allows you to query and manage your model catalog. The API supports the following operations:

- **Search**: Search for models in the catalog based on various criteria.
- **List**: List all models in the catalog.

## Request

THe catalog API is a POST endpoint that accepts a JSON request body. The request must be anonymous and does not require authentication.

The request format for the catalog API is as follows:

- **Method**: `POST`
- **Content-Type**: `application/json`
- **User-Agent**: `AzureAiStudio`

The request body must be a JSON object that contains the following fields:

- `resourceIds`: An array of resource IDs that specify the resources to be queried.
- `indexEntitiesRequest`: An object that contains the search parameters.
  - `filters`: An array of filter objects that specify the criteria for filtering the search results.
  - `pageSize`: The maximum number of results to return (for pagination).
  - `skip`: The number of results to skip (for pagination).
  - `continuationToken`: A token for pagination to continue from a previous request.

### Example request

```bash
curl POST <your-catalog-api-endpoint> \
-H "Content-Type: application/json" \
-H "User-Agent: AzureAiStudio" \
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
        "field": "labels",
        "operator": "eq",
        "values": [
          "latest"
        ]
      },
      {
        "field": "annotations/tags/foundryLocal",
        "operator": "eq",
        "values": [
          ""
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

## Reponse

The response from the catalog API is a JSON object that contains the search results. The response schema is as follows:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AzureFoundryResponse",
  "type": "object",
  "properties": {
    "indexEntitiesResponse": {
      "$ref": "#/definitions/IndexEntitiesResponse"
    },
    "regionalErrors": {
      "type": ["object", "null"]
    },
    "resourceSkipReasons": {
      "type": ["object", "null"]
    },
    "shardErrors": {
      "type": ["object", "null"]
    },
    "numberOfResourcesNotIncludedInSearch": {
      "type": ["integer", "null"]
    }
  },
  "definitions": {
    "IndexEntitiesResponse": {
      "type": "object",
      "properties": {
        "totalCount": {
          "type": ["integer", "null"]
        },
        "value": {
          "type": ["array", "null"],
          "items": {
            "$ref": "#/definitions/LocalModel"
          }
        },
        "nextSkip": {
          "type": ["integer", "null"]
        },
        "continuationToken": {
          "type": ["string", "null"]
        },
        "entityContainerIdsToEntityContainerMetadata": {
          "type": ["object", "null"],
          "additionalProperties": {
            "$ref": "#/definitions/EntityContainerMetadata"
          }
        },
        "resourcesNotQueriedReasons": {
          "type": ["object", "null"]
        },
        "numberOfEntityContainersNotQueried": {
          "type": ["integer", "null"]
        },
        "fanoutData": {
          "type": ["object", "null"]
        },
        "regionalFanoutState": {
          "type": ["object", "null"]
        },
        "shardErrors": {
          "type": ["object", "null"]
        },
        "canSupportSkip": {
          "type": ["boolean", "null"]
        },
        "facets": {
          "type": ["object", "null"]
        }
      }
    },
    "EntityContainerMetadata": {
      "type": "object",
      "properties": {
        "resourceId": {
          "type": ["string", "null"]
        },
        "subscriptionId": {
          "type": ["string", "null"]
        },
        "resourceGroup": {
          "type": ["string", "null"]
        },
        "resourceName": {
          "type": ["string", "null"]
        },
        "entityContainerType": {
          "type": ["string", "null"]
        },
        "regions": {
          "type": ["array", "null"],
          "items": {
            "$ref": "#/definitions/Region"
          }
        },
        "tenantId": {
          "type": ["string", "null"]
        },
        "immutableResourceId": {
          "type": ["string", "null"]
        },
        "isPublicResource": {
          "type": ["boolean", "null"]
        },
        "isTradeRestrictedResource": {
          "type": ["boolean", "null"]
        }
      }
    },
    "Region": {
      "type": "object",
      "properties": {
        "regionName": {
          "type": ["string", "null"]
        },
        "isPrimaryRegion": {
          "type": ["boolean", "null"]
        }
      }
    },
    "LocalModel": {
      "type": "object",
      "properties": {
        "relevancyScore": {
          "type": ["number", "null"]
        },
        "entityResourceName": {
          "type": ["string", "null"]
        },
        "highlights": {
          "type": ["object", "null"]
        },
        "schemaId": {
          "type": ["string", "null"],
          "format": "uuid"
        },
        "entityId": {
          "type": ["string", "null"]
        },
        "kind": {
          "type": ["string", "null"]
        },
        "annotations": {
          "type": ["object", "null"]
        },
        "properties": {
          "type": ["object", "null"]
        },
        "internal": {
          "type": ["object", "null"]
        },
        "updateSequence": {
          "type": ["integer", "null"]
        },
        "type": {
          "type": ["string", "null"]
        },
        "version": {
          "type": ["string", "null"]
        },
        "entityContainerId": {
          "type": ["string", "null"],
          "format": "uuid"
        },
        "entityObjectId": {
          "type": ["string", "null"]
        },
        "resourceType": {
          "type": ["string", "null"]
        },
        "relationships": {
          "type": ["array", "null"],
          "items": {
            "type": "object"
          }
        },
        "assetId": {
          "type": ["string", "null"]
        },
        "usage": {
          "type": ["object", "null"]
        },
        "isAFragment": {
          "type": ["boolean", "null"]
        },
        "fragmentId": {
          "type": ["object", "null"]
        }
      }
    }
  }
}

```

## Filterable Fields

The following fields should be filterable in your catalog API:

- `name`
- `version`
- `labels`
- `type`
- `kind`
- `properties/variantInfo/variantMetadata/device`
- `properties/variantInfo/variantMetadata/executionProvider`
- `properties/variantInfo/variantMetadata/modelType`
- `popularity`
- `createdTime`
- `displayName`
- `summary`
- `license`
- `publisher`
- `inferenceTasks`
- `finetuningTasks`
- `modelLimits/textLimits/maxOutputTokens`
- `modelLimits/textLimits/inputContextWindow`
- `modelLimits/supportedInputModalities`
- `modelLimits/supportedOutputModalities`
- `modelLimits/supportedLanguages`
- `playgroundLimits/rateLimitTier`
- `modelCapabilities`
- `AzureOffers`

## Supported Orderable Fields

The following fields should be orderable in your catalog API:

- `name`
- `version`
- `popularity`
- `createdTime`
- `displayName`
- `publisher`
