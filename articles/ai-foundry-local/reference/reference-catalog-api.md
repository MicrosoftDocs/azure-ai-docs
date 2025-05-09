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

This document provides a detailed reference for the Model Catalog APIs. Catalog implementers can use this guide when creating their own catalog implementations.

## Base URI

```
https://<catalog provider URI>/<provider subpath>
```

Replace `<catalog provider URI>` and `<provider subpath>` with your specific catalog hosting information.

---

## Available APIs

- **Get Model Details** - Retrieve information about a specific model
- **Get Publisher Details** - Access publisher information
- **List Publishers** - View all available publishers
- **List Models** - Browse available models

---

## Authorization

All endpoints must support:

- Anonymous access (no authentication required)

---

## Get Model Details

Retrieves detailed information about a specific model version.

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

## Filterable Fields

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
