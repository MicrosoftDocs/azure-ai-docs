---
title: Adaptive custom translation
titleSuffix: Azure AI services
description: Understand the parameters, headers, and body messages for the Azure AI adaptive custom translation API v1.0 preview to create and manage adaptive dataset indexes.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.author: lajanuar
ms.date: 09/30/2025
ms.topic: reference
---

# Adaptive custom translation (adaptCT) API v1.0 (preview)

> [!IMPORTANT]
>
> * Azure adaptive custom translation is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Adaptive custom translation in Azure is a capability of the Translator Text API designed for dynamic, real-time personalization of neural machine translation (NMT). Unlike traditional custom models—which require substantial training data and a separate deployment process—this feature enables the system to adjust to your preferred terminology and writing style using only a handful of examples. This adaptive technology, also known as few-shot learning, is accessible via Azure AI Foundry.

Key Differences
*    **Custom translator**: You provide your data to build a new, tailored translation model, which is then deployed for use.
*    **Adaptive custom translation**: Instead of constructing a new model, it uses an existing base model and incrementally improves it in real time by learning from user corrections and added data. This approach eliminates the need to rebuild models from scratch and supports continuous refinement.


> [!IMPORTANT]
> - The Adaptive custom translation API (v1.0 preview) enables adaptCT dataset indexes lifecycle management capabilities.
> - This API requires proper authentication and foundry project setup before use.
> - Make sure to test thoroughly before using in production environments.
> - Project and workspace are used interchangeably to mean a Foundry created project.

## Comparing adaptive and custom translation

| Feature | Adaptive custom translation | Custom translator |
| --- | --- | --- |
| **Model Creation** | Enables dynamic adaptation of an existing Neural Machine Translation (NMT) model using a compact dataset. The process is streamlined, as it doesn't require offline training or manual deployment steps. | Empowers the creation of a dedicated NMT model through comprehensive, end-to-end training. Deployment to production environments ensures that the model is tailored for operational use. |
| **Data Requirements** | Facilitates domain-specific translation improvements with a minimal dataset, such as five parallel, prealigned sentence pairs, or a small indexed sample. This approach efficiently grounds translation outputs. | Uses a large dataset, typically at least 10,000 parallel sentence pairs, to build a highly accurate NMT model. This extensive data supports robust supervised learning and high-fidelity translations. |
| **Speed** | Quickly incorporates and applies dataset updates within minutes, allowing for immediate adjustments in translation behavior and output. | Completes model training over a variable period—potentially up to 48 hours—depending on the dataset size and computational capacity. Updates require retraining and redeployment to reflect changes. |
| **Maintenance** | Simplifies operational management by focusing on dataset index updates and integrity checks, removing the need for ongoing model maintenance. | Supports sustained translation quality with periodic maintenance, including retraining and redeployment, to keep the model current and accurate. |

* Choose the standard Azure AI custom translator to create a custom neural machine translation model trained on your domain-specific documents. This option is ideal when you require specialized terminology, unique styles, and a fully tailored, high-quality solution.

* Choose Azure adaptive custom translation when you need continuous learning and real-time adaptation. It's best for workflows with user interactions and corrections, such as chatbots or help desks, where feedback improves translation quality dynamically.


## Base URL

The base URL for all adaptive custom translation API endpoints is:

```http
   https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/
```

## Authentication

All API requests require authentication using one or more of the following methods:

### Required Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Ocp-Apim-Subscription-Key` | Your subscription key | **True** | Azure AI Translator subscription key |
| `Ocp-Apim-Subscription-Region` | Your resource region | **True** | Azure resource region (for example, "eastus2") |
| `Authorization` | `Bearer <your-token>` | **True** | OAuth Bearer token for enhanced authentication |

## API Operations

The Adaptive custom translation API is organized into three main operation categories:

### 1. Project Operations
- [Get All Projects](#get-all-workspaces)
- [Get Project](#get-workspace)
- [Create Project](#create-workspace)

### 2. Document Operations
- [Get Adaptive Documents](#get-documents)
- [Import Adaptive Documents (TMX/TSV)](#import-documents-tmx)
- [Get Import Job Status](#get-import-job-status)
- [Delete Documents](#import-documents)

### 3. Dataset Index Operations
- [Create Dataset Index](#create-index)
- [Get Dataset Index](#get-index)
- [Get All Dataset Indexes](#get-all-indexes)
- [Delete Dataset Index](#delete-index)

## Project Operations

### Get All Projects

Retrieves all projects available to the authenticated user.

#### Request URL

```bash
   GET /workspaces/
```

#### Request Example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/" ^
 -H "Ocp-Apim-Subscription-Key: <your-key>" ^
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

**Linux/macOS**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/" \
 -H "Ocp-Apim-Subscription-Key: <your-key>" \
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

### Get Project

Retrieves details for a specific project.

#### Request URL

```bash
   GET /workspaces/<workspaceId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Unique identifier for the project |

#### Request Example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/<workspaceId>" ^
 -H "Ocp-Apim-Subscription-Key: <your-key>" ^
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

**Linux/macOS**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/<workspaceId>" \
 -H "Ocp-Apim-Subscription-Key: <your-key>" \
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

### Create Project

Creates a new project for organizing adaptCT translation dataset data and indexes.

#### Request URL

```bash
   POST /workspaces
```

#### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Content-Type` | `application/json` | **True** |
| `Ocp-Apim-Subscription-Key` | Your subscription key | **True** |
| `Ocp-Apim-Subscription-Region` | Your resource region | **True** |

#### Request Body

```json
{
    "name": "string",
    "subscription": {
        "billingRegionCode": "string",
        "subscriptionKey": "string"
    }
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | **True** | Name for the new workspace |
| `subscription.billingRegionCode` | string | **True** | Billing region code (for example, "USE2") |
| `subscription.subscriptionKey` | string | **True** | Subscription key for billing |

#### Request Example

**Windows**
```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces" ^
 -H "Ocp-Apim-Subscription-Key: <your-key>" ^
 -H "Ocp-Apim-Subscription-Region: <your-region>" ^
 -H "Content-Type: application/json" ^
 -d "{\"name\": \"my-workspace\", \"subscription\": {\"billingRegionCode\": \"USE2\", \"subscriptionKey\": \"<your-key>\"}}"
```

**Linux/macOS**
```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces" \
 -H "Ocp-Apim-Subscription-Key: <your-key>" \
 -H "Ocp-Apim-Subscription-Region: <your-region>" \
 -H "Content-Type: application/json" \
 -d "{\"name\": \"my-workspace\", \"subscription\": {\"billingRegionCode\": \"USE2\", \"subscriptionKey\": \"<your-key>\"}}"
```

## Document Operations

### Get Documents

Retrieves a paginated list of documents in a project.

#### Request URL

```bash
  GET /documents?workspaceId=<workspaceId>&pageIndex={pageIndex}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |
| `pageIndex` | integer | False | Page index for pagination (default: 0) |

#### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |
| `Content-Type` | `multipart/form-data` | False |

#### Request Example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents?workspaceId=<workspaceId>&pageIndex=0" ^
 -H "Authorization: Bearer <token>"
```

**Linux/macOS**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents?workspaceId=<workspaceId>&pageIndex=0" \
 -H "Authorization: Bearer <token>"
```

### Import Documents (TSV, TMX)

Imports adaptive documents in TSV and TMX format to a project.

#### Request URL

```bash
   POST /documents/import?workspaceId=<workspaceId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

#### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |

#### Request Body (Multipart Form Data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `DocumentDetails` | string | **True** | JSON string containing document metadata |
| `FILES` | file | **True** | TSV or TMX file to upload |

#### DocumentDetails JSON Format

```json
[{
  "DocumentName": "string",
  "DocumentType": "Adaptive",
  "FileDetails": [{
    "Name": "string",
    "LanguageCode": "string",
    "OverwriteIfExists": boolean
  }]
}]
```

#### TMX Request Example (English to supported target language, for example, French)

**Windows**
```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import?workspaceId=<workspaceId>" ^
 -H "Authorization: Bearer <token>" ^
 -F "DocumentDetails=[{\"DocumentName\": \"my-document\",\"DocumentType\": \"Adaptive\",\"FileDetails\": [{\"Name\": \"data.tmx\",\"LanguageCode\": \"en\",\"OverwriteIfExists\": true}]}]" ^
 -F "FILES=@path/to/data.tmx"
```

**Linux/macOS**
```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import?workspaceId=<workspaceId>" \
 -H "Authorization: Bearer <token>" \
 -F "DocumentDetails=[{\"DocumentName\": \"my-document\",\"DocumentType\": \"Adaptive\",\"FileDetails\": [{\"Name\": \"data.tmx\",\"LanguageCode\": \"en\",\"OverwriteIfExists\": true}]}]" \
 -F "FILES=@path/to/data.tmx"

```

### Get Import Job Status

Retrieves the status of a document import job.

#### Request URL

```bash
   GET /documents/import/jobs/<jobId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jobId` | string | **True** | Import job identifier |

#### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |

#### Request Example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import/jobs/<jobId>" ^
 -H "Authorization: Bearer <token>"
```

**Linux/macOS**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import/jobs/<jobId>" \
 -H "Authorization: Bearer <token>"
```

## Dataset Index Operations

### Create Dataset Index

Creates a new dataset index for adaptive translation using specified documents.

#### Request URL

```bash
   POST /index?workspaceId=<workspaceId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

#### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `Content-Type` | `application/json` | **True** |

#### Request Body

```json
{
  "documentIds": ["string"],
  "IndexName": "string",
  "SourceLanguage": "string",
  "TargetLanguage": "string"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `documentIds` | array | **True** | Array of document IDs to include in dataset index |
| `IndexName` | string | **True** | Name for the new dataset index |
| `SourceLanguage` | string | **True** | Source language code |
| `TargetLanguage` | string | **True** | Target language code |

#### Request Example

**Windows**
```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>" ^
 -H "Content-Type: application/json" ^
 -d "{\"documentIds\": [\"1457362\"],\"IndexName\": \"my-index\",\"SourceLanguage\": \"en\",\"TargetLanguage\": \"de\"}"
```

**Linux/macOS**
```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>" \
 -H "Content-Type: application/json" \
 -d "{\"documentIds\": [\"1457362\"],\"IndexName\": \"my-index\",\"SourceLanguage\": \"en\",\"TargetLanguage\": \"de\"}"
```

### Get Dataset Index

Retrieves details for a specific dataset index.

#### Request URL

```bash
   GET /index/{indexId}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `indexId` | string | **True** | Index identifier |

#### Request Example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

**Linux/macOS**
```bash
cucurl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

### Get All Dataset Indexes

Retrieves all dataset indexes in a project.

#### Request URL

```bash
   GET /index?workspaceId=<workspaceId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

#### Request Example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

**Linux/macOS**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

### Delete Dataset Index

Deletes a specific dataset index.

#### Request URL

```bash
   DELETE /index/<indexId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `indexId` | string | **True** | Dataset index identifier |

#### Request Example

**Windows**
```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

**Linux/macOS**
```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

## Translate With Dataset Index

[Use Text Translation API](https://learn.microsoft.com/azure/ai-services/translator/text-translation/preview/overview)

## Error Responses

The API returns standard HTTP status codes. Common error responses:

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid parameters or request format |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Service error |

## Best Practices

1. **Authentication**: Use Bearer tokens for document operations 
2. **Error Handling**: Implement proper error handling and retry logic for API calls
3. **Project Organization**: Use descriptive names for projects and dataset indexes to maintain organization
4. **Document Management**: Ensure TSV and TMX files are properly formatted with well aligned source-target pairs

## Next Steps

- [Learn about custom translator models](https://learn.microsoft.com/azure/ai-services/translator/custom-translator/overview)
- [Learn about the text translation API](https://learn.microsoft.com/azure/ai-services/translator/text-translation/preview/overview)
- [Explore Azure AI Foundry for advanced AI capabilities](https://learn.microsoft.com/azure/ai-foundry/)

