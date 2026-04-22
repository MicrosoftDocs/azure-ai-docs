---
title: Adaptive custom translation
titleSuffix: Microsoft Foundry
description: Understand the parameters, headers, and body messages for the Azure AI adaptive custom translation API v1.0 preview to create and manage adaptive dataset indexes.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.author: lajanuar
ms.date: 04/21/2026
ms.topic: reference
---
<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD036 -->

# Azure Translation adaptive custom translation (GA)

Azure Translator adaptive custom translation (**AdaptCT**) is a runtime translation adaptation capability available in Microsoft Foundry. It improves large language model (LLM) outputs, such as GPT-5.1, using a compact set of reference sentence pairs.

With **AdaptCT**, you upload 5-10,000 prealigned bilingual segment pairs (source and target). Each source segment can contain up to 250 characters, and each target segment can contain up to 250 characters. The service builds a language-pair dataset index in minutes, which you can apply through the [Azure Translator 2026-06-06 APIs](../../../text-translation/2026-06-06/translate-api.md).

Unlike traditional custom translation workflows that require large training corpora and separate model deployment, **AdaptCT** uses few-shot retrieval at inference time. For each request, the system retrieves relevant segment pairs from your dataset index and uses them to steer output toward domain-specific terminology, context, and style.

## Compare adaptive and custom translation

The following comparison highlights when to choose adaptive custom translation versus a fully trained Custom Translator model.

| Feature | Adaptive custom translation | Custom translator |
| --- | --- | --- |
| **System Creation** | Enables dynamic translation adaptation and optimization of an existing LLM model using a compact dataset index. The process is streamlined, as it doesn't require offline training or manual deployment steps. | Empowers the creation of a dedicated neural machine translation (NMT) model through comprehensive, end-to-end training. Deployment to production environments ensures that the model is tailored for operational use. |
| **Data Requirements** | Facilitates domain-specific translation improvements with a minimal dataset, such as five parallel, prealigned sentence pairs, or a small indexed sample. This approach efficiently grounds translation outputs. | Uses a large dataset, typically at least 10,000 parallel sentence pairs, to build a highly accurate NMT model. This extensive data supports robust supervised learning and high-fidelity translations. |
| **Speed** | Quickly incorporates and applies dataset updates within minutes, allowing for immediate adjustments in translation behavior and output. | Completes model training over a variable period—potentially up to 48 hours—depending on the dataset size and computational capacity. Updates require retraining and redeployment to reflect changes. |
| **Maintenance** | Simplifies operational management by focusing on dataset index updates and integrity checks, removing the need for ongoing model maintenance. | Supports sustained translation quality with periodic maintenance, including retraining and redeployment, to keep the model current and accurate. |
| **Use Case** | Best for rapidly evolving or low-volume content (for example, support tickets) where quick updates to terminology or phrasing are needed without retraining a model. | Ideal for high-volume, consistent translation of domain-specific content (for example, legal contracts) where strict terminology and style adherence are critical across all documents. |

### Key differences

Use these key points as a quick decision guide before you invest in data preparation, training, or deployment.

* **Custom translator**: Fine-tunes a dedicated translation model using your dataset; model is trained and deployed within ~48 hours.
* **Adaptive custom translation**: No fine-tuning or deployment required; updates by rebuilding the dataset index, ready within minutes. ​

> [!IMPORTANT]
>
> * The Adaptive custom translation playground (GA in Foundry NextGen) enables no-code adaptCT dataset indexes lifecycle management capabilities.
> * The Adaptive custom translation API (v1.0 preview) enables adaptCT dataset indexes lifecycle management capabilities.
> * This API requires proper authentication and foundry resource setup before use.
> * Make sure to test thoroughly before using in production environments.
> * Project and workspace are used interchangeably to mean a Foundry auto-created project.

## Adaptive Custom Translation base URL

Here's the base URL for all adaptive custom translation API requests:

```http
   https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/
```

## Authentication

Each request to an adaptCT API must include an authentication header. This header passes along a Foundry resource secret key and authentication token, which is used to validate your subscription for a service or group of services.

* Authenticate with a [secret key](../../../text-translation/reference/authentication.md#secret-key).
* Authenticate with a [bearer token](../../../text-translation/reference/authentication.md#authenticating-with-an-access-token).

For more information about Azure resources, *see* [Azure resources for Azure AI translation](../../../how-to/create-translator-resource.md)

### Required headers

Include the following headers in every request to ensure the service can authenticate and route your call correctly.

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Ocp-Apim-Subscription-Key` | Your subscription key | **True** | Azure Translator subscription key |
| `Ocp-Apim-Subscription-Region` | Your resource region | **True** | Azure resource region (for example, "eastus2") |

## How to create and use a dataset index

Complete the following workflow to provision your workspace, import bilingual data, create a dataset index, and apply it during translation.

1. You must use a Foundry resource. To learn how to create and manage a Foundry resource see [Create your first Foundry resource](../../../how-to/create-translator-resource.md)
1. [Create workspace](#create-workspace)
1. [Import Adaptive Documents (TMX/TSV)](#import-documents-tsv-tmx)
1. [Create Dataset Index](#create-dataset-index)
1. To translate with dataset index see [Use Text Translation API](/azure/ai-services/translator/text-translation/preview/overview)

## API operations

The Adaptive custom translation API is organized into three main operation categories.

### Workspace operation index

Use these endpoints to discover and retrieve workspaces.

* [Get all workspaces](#get-all-workspaces)
* [Get workspace](#get-workspace)
* [Create workspace](#create-workspace)

### Document operation index

Use these endpoints to list documents, import TMX or TSV files, and track import jobs.

* [Get documents](#get-documents)
* [Import documents (TSV, TMX)](#import-documents-tsv-tmx)
* [Get import job status](#get-import-job-status)

### Dataset index operation index

Use these endpoints to create, read, list, and delete dataset indexes.

* [Create dataset index](#create-dataset-index)
* [Get dataset index](#get-dataset-index)
* [Get all dataset indexes](#get-all-dataset-indexes)
* [Delete dataset index](#delete-dataset-index)

### Workspace operation reference

#### Get all workspaces

Retrieves all workspaces available to the authenticated user.

**Request URL**

```bash
GET /workspaces/
```

**Request example**

Windows:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/" ^
 -H "Ocp-Apim-Subscription-Key: <your-key>" ^
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

Linux/macOS:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/" \
 -H "Ocp-Apim-Subscription-Key: <your-key>" \
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

#### Get workspace

Retrieves details for a specific workspace.

**Request URL**

```bash
GET /workspaces/<workspaceId>
```

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Unique identifier for the project |

**Request example**

Windows:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/<workspaceId>" ^
 -H "Ocp-Apim-Subscription-Key: <your-key>" ^
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

Linux/macOS:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/workspaces/<workspaceId>" \
 -H "Ocp-Apim-Subscription-Key: <your-key>" \
 -H "Ocp-Apim-Subscription-Region: <your-region>"
```

#### Create workspace

Create a workspace in Microsoft Foundry after creating your Foundry resource and project.

1. Select a project.
1. Select Build > Models > AI Services > Azure Translator - Text Translation > Adaptive LLM. The workspace is created automatically.
1. Retrieve the workspace ID by creating your first adaptive dataset index in the playground using the Adaptive LLM tab, or by calling [Get all workspaces](#get-all-workspaces).

### Document operation reference

#### Get documents

Retrieves a paginated list of documents in a project.

**Request URL**

```bash
GET /documents?workspaceId=<workspaceId>&pageIndex={pageIndex}
```

**Parameters**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `workspaceId` | string | **True** | Project identifier |
| `pageIndex` | integer | False | Page index for pagination (default: 0) |

**Request headers**

| Header | Value | Required |
| -- | -- | -- |
| `Authorization` | `Bearer <token>` | **True** |
| `Content-Type` | `multipart/form-data` | False |

**Request example**

Windows:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents?workspaceId=<workspaceId>&pageIndex=0" ^
 -H "Authorization: Bearer <token>"
```

Linux/macOS:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents?workspaceId=<workspaceId>&pageIndex=0" \
 -H "Authorization: Bearer <token>"
```

#### Import documents (TSV, TMX)

Imports adaptive documents in TSV and TMX format to a project.

**Request URL**

```bash
POST /documents/import?workspaceId=<workspaceId>
```

**Parameters**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `workspaceId` | string | **True** | Project identifier |

**Request headers**

| Header | Value | Required |
| -------- | ----- | -------- |
| `Authorization` | `Bearer <token>` | **True** |

**Request body (multipart form data)**

| Field | Type | Required | Description |
| ------- | ------ | ---------- | ------------- |
| `DocumentDetails` | string | **True** | JSON string containing document metadata |
| `FILES` | file | **True** | TSV or TMX file to upload |

**DocumentDetails JSON format**

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

**TMX request example**

English to a supported target language, for example, French.

Windows:

```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import?workspaceId=<workspaceId>" ^
 -H "Authorization: Bearer <token>" ^
 -F "DocumentDetails=[{\"DocumentName\": \"my-document\",\"DocumentType\": \"Adaptive\",\"FileDetails\": [{\"Name\": \"data.tmx\",\"LanguageCode\": \"en\",\"OverwriteIfExists\": true}]}]" ^
 -F "FILES=@path/to/data.tmx"
```

Linux/macOS:

```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import?workspaceId=<workspaceId>" \
 -H "Authorization: Bearer <token>" \
 -F "DocumentDetails=[{\"DocumentName\": \"my-document\",\"DocumentType\": \"Adaptive\",\"FileDetails\": [{\"Name\": \"data.tmx\",\"LanguageCode\": \"en\",\"OverwriteIfExists\": true}]}]" \
 -F "FILES=@path/to/data.tmx"
```

#### Get import job status

Retrieves the status of a document import job.

**Request URL**

```bash
GET /documents/import/jobs/<jobId>
```

**Parameters**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `jobId` | string | **True** | Import job identifier |

**Request headers**

| Header | Value | Required |
| -------- | ----- | -------- |
| `Authorization` | `Bearer <token>` | **True** |

**Request example**

Windows:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import/jobs/<jobId>" ^
 -H "Authorization: Bearer <token>"
```

Linux/macOS:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/documents/import/jobs/<jobId>" \
 -H "Authorization: Bearer <token>"
```

### Dataset index operation reference

#### Create dataset index

Creates a new dataset index for adaptive translation using specified documents.

**Request URL**

```bash
POST /index?workspaceId=<workspaceId>
```

**Parameters**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `workspaceId` | string | **True** | Project identifier |

**Request headers**

| Header | Value | Required |
| -------- | ----- | -------- |
| `Content-Type` | `application/json` | **True** |

**Request body**

```json
{
  "documentIds": ["string"],
  "IndexName": "string",
  "SourceLanguage": "string",
  "TargetLanguage": "string"
}
```

**Request body fields**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `documentIds` | array | **True** | Array of document IDs to include in the dataset index |
| `IndexName` | string | **True** | Name for the new dataset index |
| `SourceLanguage` | string | **True** | Source language code |
| `TargetLanguage` | string | **True** | Target language code |

**Request example**

Windows:

```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>" ^
 -H "Content-Type: application/json" ^
 -d "{\"documentIds\": [\"1457362\"],\"IndexName\": \"my-index\",\"SourceLanguage\": \"en\",\"TargetLanguage\": \"de\"}"
```

Linux/macOS:

```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>" \
 -H "Content-Type: application/json" \
 -d "{\"documentIds\": [\"1457362\"],\"IndexName\": \"my-index\",\"SourceLanguage\": \"en\",\"TargetLanguage\": \"de\"}"
```

#### Get dataset index

Retrieves details for a specific dataset index.

**Request URL**

```bash
GET /index/{indexId}
```

**Parameters**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `indexId` | string | **True** | Index identifier |

**Request example**

Windows:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

Linux/macOS:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

#### Get all dataset indexes

Retrieves all dataset indexes in a project.

**Request URL**

```bash
GET /index?workspaceId=<workspaceId>
```

**Parameters**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `workspaceId` | string | **True** | Project identifier |

**Request example**

Windows:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

Linux/macOS:

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

#### Delete dataset index

Deletes a specific dataset index.

**Request URL**

```bash
DELETE /index/<indexId>
```

**Parameters**

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `indexId` | string | **True** | Dataset index identifier |

**Request example**

Windows:

```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

Linux/macOS:

```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

## Translate with dataset index

[Use Text Translation API with AdaptiveDatasetId](../../../text-translation/2026-06-06/translate-api.md#text-translation-request-applying-adaptive-custom-translation-with-dataset)

## Error responses

The API returns standard HTTP status codes. Common error responses:

| Status Code | Description |
| ------------- | ------------- |
| 400 | Bad Request - Invalid parameters or request format |
| 401 | Unauthorized - Missing or invalid authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Service error |

## Best practices

Apply these practices to improve reliability, maintainability, and translation quality in production workloads.

1. **Authentication**: Use Bearer tokens for document operations
1. **Error Handling**: Implement proper error handling and retry logic for API calls
1. **Project Organization**: Use descriptive names for projects and dataset indexes to maintain organization
1. **Document Management**: Ensure TSV and TMX files are properly formatted with well aligned source-target pairs

## Troubleshooting

If requests fail, use the following checks to isolate authentication, ingestion, and indexing issues.

1. **Authentication Errors**
   * Verify your Azure tokens are valid and not expired.
   * Check that all required environment variables are set.
   * Ensure your Azure services are properly configured.

1. **Index Creation Issues**
   * Verify documents are properly uploaded before creating indices.
   * Check that the Custom Translator API endpoint is accessible.
   * Ensure your subscription is active.

## Next steps

Use these resources to deepen implementation knowledge and connect AdaptCT with broader Azure AI translation capabilities.

* [Learn about custom translator models](../../../custom-translator/azure-ai-foundry/overview.md)
* [Learn about the text translation API](../../../text-translation/2026-06-06/overview.md)
* [Explore Foundry for advanced AI capabilities](../../../overview.md)
