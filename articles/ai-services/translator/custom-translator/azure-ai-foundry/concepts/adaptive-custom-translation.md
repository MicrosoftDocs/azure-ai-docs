---
title: Foundry Tools adaptive custom translation
titleSuffix: Foundry Tools
description: Understand the parameters, headers, and body messages for the Azure AI adaptive custom translation API v1.0 preview to create and manage adaptive dataset indexes.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.author: lajanuar
ms.date: 11/18/2025
ms.topic: reference
---

# Foundry Tools adaptive custom translation (preview)

> [!IMPORTANT]
>
> * Azure Translator adaptive custom translation is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure Translator in Foundry Tools adaptive custom translation (adaptCT) is a translation enhancement feature, designed to adapt and optimize large language model (LLM) outputs—such as GPT-4o deployed in Microsoft Foundry—using a small set of reference sentence pairs.

AdaptCT lets you upload 5–10,000 pre‑aligned bilingual segment pairs (source+target). Each pair can contain up to 512 total characters (combined across both sides). The service builds a custom language‑pair dataset index in minutes, which you can then query with the [Azure Translator 2025-05-01-preview APIs](/azure/ai-services/translator/text-translation/preview/overview).
Unlike traditional custom models that require large training sets and separate deployment, AdaptCT uses few‑shot retrieval at inference time: it selects relevant sentence pairs from your dataset index on the fly to adapt and optimize the LLM’s output toward your domain terminology, context, and style. `Availability: Foundry.`

### Key differences
*    **Custom translator**: Fine-tunes a dedicated translation model using your dataset; model is trained and deployed within ~48 hours.
*    **Adaptive custom translation**: No fine-tuning or deployment required; updates by rebuilding the dataset index, ready within minutes. ​


> [!IMPORTANT]
> - The Adaptive custom translation API (v1.0 preview) enables adaptCT dataset indexes lifecycle management capabilities.
> - This API requires proper authentication and foundry project setup before use.
> - Make sure to test thoroughly before using in production environments.
> - Project and workspace are used interchangeably to mean a Foundry created project.

## Compare adaptive and custom translation

| Feature | Adaptive custom translation | Custom translator |
| --- | --- | --- |
| **System Creation** | Enables dynamic translation adaptation and optimization of an existing LLM model using a compact dataset index. The process is streamlined, as it doesn't require offline training or manual deployment steps. | Empowers the creation of a dedicated neural machine translation (NMT) model through comprehensive, end-to-end training. Deployment to production environments ensures that the model is tailored for operational use. |
| **Data Requirements** | Facilitates domain-specific translation improvements with a minimal dataset, such as five parallel, prealigned sentence pairs, or a small indexed sample. This approach efficiently grounds translation outputs. | Uses a large dataset, typically at least 10,000 parallel sentence pairs, to build a highly accurate NMT model. This extensive data supports robust supervised learning and high-fidelity translations. |
| **Speed** | Quickly incorporates and applies dataset updates within minutes, allowing for immediate adjustments in translation behavior and output. | Completes model training over a variable period—potentially up to 48 hours—depending on the dataset size and computational capacity. Updates require retraining and redeployment to reflect changes. |
| **Maintenance** | Simplifies operational management by focusing on dataset index updates and integrity checks, removing the need for ongoing model maintenance. | Supports sustained translation quality with periodic maintenance, including retraining and redeployment, to keep the model current and accurate. |
| **Use Case** | Best for rapidly evolving or low-volume content (for example, support tickets) where quick updates to terminology or phrasing are needed without retraining a model. | Ideal for high-volume, consistent translation of domain-specific content (for example, legal contracts) where strict terminology and style adherence are critical across all documents. |



## Base URL

Here's the base URL for all adaptive custom translation API requests:

```http
   https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/
```

## Authentication

Each request to an adaptCT API must include an authentication header. This header passes along a Foundry resource secret key and authentication token, which is used to validate your subscription for a service or group of services. 

* Authenticate with a [secret key](../../../text-translation/reference/authentication.md#secret-key).
* Authenticate with a [bearer token](../../../text-translation/reference/authentication.md#authenticating-with-an-access-token).


Form more information about Azure resources, *see* [Azure resources for Azure AI translation](../../../how-to/create-translator-resource.md)

### Required headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Ocp-Apim-Subscription-Key` | Your subscription key | **True** | Azure Translator subscription key |
| `Ocp-Apim-Subscription-Region` | Your resource region | **True** | Azure resource region (for example, "eastus2") |
| `Authorization` | `Bearer <your-token>` | **True** | OAuth Bearer token for enhanced authentication |

## How to create and use a dataset index
1. You must use a Foundry resource. To learn how to create and manage a Foundry resource see [Create your first Foundry resource](../../../how-to/create-translator-resource.md)
2. [Create Project](#create-project)
3. [Import Adaptive Documents (TMX/TSV)](#import-documents-tsv-tmx)
4. [Create Dataset Index](#create-dataset-index)
5. To translate with dataset index see [Use Text Translation API](/azure/ai-services/translator/text-translation/preview/overview)


## API operations

The Adaptive custom translation API is organized into three main operation categories ([project operations](#project-operations-1), [document operations](#document-operations-1), and [dataset index operations](#dataset-index-operations-1)):

### Project operations
* [Get All Projects](#get-all-projects)
* [Get Project](#get-project)
* [Create Project](#create-project)

### Document operations
* [Get Adaptive Documents](#get-documents)
* [Import Adaptive Documents (TMX/TSV)](#import-documents-tsv-tmx)
* [Get Import Job Status](#get-import-job-status)

### Dataset index operations
* [Create Dataset Index](#create-dataset-index)
* [Get Dataset Index](#get-dataset-index)
* [Get All Dataset Indexes](#get-all-dataset-indexes)
* [Delete Dataset Index](#delete-dataset-index)

## Project operations

### Get all projects

Retrieves all projects available to the authenticated user.

#### Request URL

```bash
   GET /workspaces/
```

#### Request example

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

### Get project

Retrieves details for a specific project.

#### Request URL

```bash
   GET /workspaces/<workspaceId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Unique identifier for the project |

#### Request example

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

### Create project

Creates a new project for organizing adaptCT translation dataset data and indexes.

#### Request URL

```bash
   POST /workspaces
```

#### Request headers

| Header | Value | Required |
|--------|-------|----------|
| `Content-Type` | `application/json` | **True** |
| `Ocp-Apim-Subscription-Key` | Your subscription key | **True** |
| `Ocp-Apim-Subscription-Region` | Your resource region | **True** |

#### Request body

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

#### Request example

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

## Document operations

### Get documents

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

#### Request headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |
| `Content-Type` | `multipart/form-data` | False |

#### Request example

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

### Import documents (TSV, TMX)

Imports adaptive documents in TSV and TMX format to a project.

#### Request URL

```bash
   POST /documents/import?workspaceId=<workspaceId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

#### Request headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |

#### Request body (multipart form data)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `DocumentDetails` | string | **True** | JSON string containing document metadata |
| `FILES` | file | **True** | TSV or TMX file to upload |

#### DocumentDetails JSON format

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

#### TMX request example

***English to supported target language, for example, French.***

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

### Get import job status

Retrieves the status of a document import job.

#### Request URL

```bash
   GET /documents/import/jobs/<jobId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jobId` | string | **True** | Import job identifier |

#### Request headers

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |

#### Request example

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

## Dataset index operations

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

#### Request headers

| Header | Value | Required |
|--------|-------|----------|
| `Content-Type` | `application/json` | **True** |

#### Request body

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
| `documentIds` | array | **True** | Array of document ID identifiers that include in dataset index. |
| `IndexName` | string | **True** | Name for the new dataset index |
| `SourceLanguage` | string | **True** | Source language code |
| `TargetLanguage` | string | **True** | Target language code |

#### Request example

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

### Get dataset index

Retrieves details for a specific dataset index.

#### Request URL

```bash
   GET /index/{indexId}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `indexId` | string | **True** | Index identifier |

#### Request example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

**Linux/macOS**
```bash
cucurl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

### Get all dataset indexes

Retrieves all dataset indexes in a project.

#### Request URL

```bash
   GET /index?workspaceId=<workspaceId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

#### Request example

**Windows**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

**Linux/macOS**
```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

### Delete dataset index

Deletes a specific dataset index.

#### Request URL

```bash
   DELETE /index/<indexId>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `indexId` | string | **True** | Dataset index identifier |

#### Request example

**Windows**
```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

**Linux/macOS**
```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

## Translate with dataset index

[Use Text Translation API](/azure/ai-services/translator/text-translation/preview/overview)

## Error responses

The API returns standard HTTP status codes. Common error responses:

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid parameters or request format |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Service error |

## Best practices

1. **Authentication**: Use Bearer tokens for document operations
1. **Error Handling**: Implement proper error handling and retry logic for API calls
1. **Project Organization**: Use descriptive names for projects and dataset indexes to maintain organization
1. **Document Management**: Ensure TSV and TMX files are properly formatted with well aligned source-target pairs

## Troubleshooting

1. **Authentication Errors**
   * Verify your Azure tokens are valid and not expired.
   * Check that all required environment variables are set.
   * Ensure your Azure services are properly configured.

1. **Index Creation Issues**
   * Verify documents are properly uploaded before creating indices.
   * Check that the Custom Translator API endpoint is accessible.
   * Ensure your subscription is active.



## Next steps

* [Learn about custom translator models](/azure/ai-services/translator/custom-translator/overview)
* [Learn about the text translation API](/azure/ai-services/translator/text-translation/preview/overview)
* [Explore Foundry for advanced AI capabilities](/azure/ai-foundry/)

