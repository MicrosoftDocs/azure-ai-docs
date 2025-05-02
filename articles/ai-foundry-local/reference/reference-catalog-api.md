
---
title: Catalog API Reference
titleSuffix: AI Foundry Local
description: Reference for Model Catalog V2 REST APIs.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: reference
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

# Catalog API Reference

This page documents the Model Catalog V2 REST APIs for discovering and retrieving model and publisher information. These APIs are used to interact with model catalogs such as Azure AI Model Catalog, but the URIs and paths are generic and can be adapted for any compatible provider.

## Base URI

```
https://<catalog provider URI>/<provider subpath>
```

Replace `<catalog provider URI>` and `<provider subpath>` with the appropriate values for your catalog provider.

---

## Supported APIs

- **Get Model Details**
- **Get Publisher Details**
- **List Publishers**
- **List Models**

---

## Authorization

All endpoints support:

- Anonymous access
- Azure Active Directory (AAD) token
- GitHub token

---

## Get Model Details

**GET** `/models/{modelName}/version/{version}`

**Example:**

```
GET https://<catalog provider URI>/<provider subpath>/models/{modelName}/version/{version}
```

**Sample cURL:**

```bash
curl -X GET --location "https://<catalog provider URI>/<provider subpath>/models/Phi-3-mini-128k-instruct/version/12"
```

---

## Get Publisher Details

**GET** `/publishers/{publisherName}`

**Example:**

```
GET https://<catalog provider URI>/<provider subpath>/publishers/{publisherName}
```

**Sample cURL:**

```bash
curl -X GET --location "https://<catalog provider URI>/<provider subpath>/publishers/contoso"
```

---

## List Publishers

**POST** `/publishers/list`

**Example:**

```
POST https://<catalog provider URI>/<provider subpath>/publishers/list
```

**Sample cURL:**

```bash
curl -X POST --location "https://<catalog provider URI>/<provider subpath>/publishers/list" \
  --header "Content-Type: application/json" \
  --data '{"continuationToken": ""}'
```

---

## List Models

**POST** `/models`

**Example:**

```
POST https://<catalog provider URI>/<provider subpath>/models
```

**Sample cURL:**

```bash
curl -X POST --location "https://<catalog provider URI>/<provider subpath>/models" \
  --header "Content-Type: application/json" \
  --data '{
    "filters": [
      {"field": "publisher", "operator": "eq", "values": ["AI21 Labs", "Mistral ai", "core42"]}
    ],
    "order": [
      {"field": "name", "direction": "asc"}
    ],
    "pageSize": 2
  }'
```

### Example Using Continuation Token

When listing models, you may receive a `continuationToken` in the response. Use this token in subsequent requests to fetch the next set of results.

```bash
curl -X POST --location "https://<catalog provider URI>/<provider subpath>/models" \
  --header "Content-Type: application/json" \
  --data '{
    "filters": [
      {"field": "publisher", "operator": "eq", "values": ["AI21 Labs", "Mistral ai", "core42"]}
    ],
    "order": [
      {"field": "name", "direction": "asc"}
    ],
    "pageSize": 2,
    "continuationToken": "your-token-here"
  }'
```

---

## Supported Filterable Fields

You can filter models using the following fields:

- `name`
- `version`
- `labels`
- `freePlayground`
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

You can order results by the following fields:

- `name`
- `version`
- `popularity`
- `createdTime`
- `displayName`
- `publisher`

---

For more information, refer to your catalog provider's API documentation.
