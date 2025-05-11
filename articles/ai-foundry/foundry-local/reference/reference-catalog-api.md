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

This document provides a detailed reference for catalog implementers can use this guide when creating their own catalog implementations to be integrated with Foundry Local.

## Catalog Host

### URI format

The catalog host URI is the base URL for your catalog API. It should be in the following format:

```
https://<catalog provider URI>/<provider subpath>
```

### Authorization

All endpoints must support:

- Anonymous access (no authentication required)


## JSON response format

Your endpoint must return a JSON response. The response schema is as follows:

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
