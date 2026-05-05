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
<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD036 -->

# Azure Translator adaptive custom translation

> [!IMPORTANT]
>
> * Adaptive custom translation playground (GA in Foundry NextGen) enables no-code dataset lifecycle management.
> * Adaptive custom translation API (v1.0 preview) enables developers to manage the adaptive dataset lifecycles.
> * Segments with >250 characters (source or target) are rejected. If all segments are invalid, the document upload fails.
> * This API requires proper authentication and foundry resource setup before use.
> * Project and workspace both refer to a Foundry project.
> * General category is added to allow a language pair (e.g., English–French, French-English) to be created once in both directions. Future categories (e.g., finance, legal, healthcare) will enable coexistence—multiple datasets for the same language pair across categories.

Azure Translator adaptive custom translation (**AdaptCT**) is a runtime translation adaptation capability available in Microsoft Foundry. It improves large language model (LLM) outputs, such as GPT-5.1, using a compact set of reference sentence pairs.

With **AdaptCT**, upload 5–10,000 prealigned source–target segment pairs (≤250 characters each). The service creates the adaptive dataset in minutes, which you can apply through the [Azure Translator 2026-06-06 APIs](/azure/ai-services/translator/text-translation/2026-06-06/translate-api).

**AdaptCT** uses few-shot retrieval at inference—no large training or separate deployment. It retrieves similar segments per request from the adaptive dataset to guide terminology, context, and style.

## Compare adaptive and custom translation

The following comparison highlights when to choose adaptive custom translation versus a fully trained Custom Translator model.

| Feature | Adaptive custom translation | Custom translator |
| --- | --- | --- |
| **System Creation** | Enables dynamic translation adaptation and optimization of an existing LLM model using a compact dataset index. The process is streamlined, as it doesn't require offline training or manual deployment steps. | Empowers the creation of a dedicated neural machine translation (NMT) model through comprehensive, end-to-end training. Deployment to production environments ensures that the model is tailored for operational use. |
| **Data Requirements** | Facilitates domain-specific translation improvements with a minimal dataset, such as five parallel, prealigned sentence pairs, or a small table compacted sample. This approach efficiently grounds translation outputs. | Uses a large training data, typically at least 10,000 parallel sentence pairs, to build a highly accurate NMT model. This extensive data supports robust supervised learning and high-fidelity translations. |
| **Speed** | Quickly incorporates and applies dataset updates within minutes, allowing for immediate adjustments in translation behavior and output. | Completes model training over a variable period—potentially up to 48 hours—depending on the dataset size and computational capacity. Updates require retraining and redeployment to reflect changes. |
| **Maintenance** | Simplifies operational management by focusing on dataset updates and integrity checks, removing the need for ongoing model maintenance. | Supports sustained translation quality with periodic maintenance, including retraining and redeployment, to keep the model current and accurate. |
| **Use Case** | Best for rapidly evolving or low-volume content (for example, support tickets) where quick updates to terminology or phrasing are needed without retraining a model. | Ideal for high-volume, consistent translation of domain-specific content (for example, legal contracts) where strict terminology and style adherence are critical across all documents. |

## Key differences

Use the following decision guide to evaluate implementation effort, update speed, and operational impact before you commit to data preparation, training, and deployment workflows.

* **Custom translator**: Best when you need a dedicated, production-deployed neural translation model trained on a large parallel corpus. This path involves full model training and deployment, and updates typically follow a retrain-and-redeploy cycle that can take up to ~48 hours depending on dataset size and service capacity.

* **Adaptive custom translation**: Best when you need rapid, iterative control of terminology, phrasing, or style without creating a new model artifact. Instead of fine-tuning, the service builds a dataset from aligned sentence pairs in minutes and applies retrieval at inference time to select similar segments per request to guide terminology, context, and style.

## Adaptive custom translation base URL

Here's the base URL for all adaptive custom translation API requests:

```http
   https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/
```

## Authentication

Each request to an adaptCT API must include an authentication header. This header passes along a Foundry resource secret key and authentication token, which is used to validate your subscription for a service or group of services.

* Authenticate with a [secret key](../text-translation/reference/authentication.md#secret-key).
* Authenticate with an [access token](../text-translation/reference/authentication.md#authenticating-with-an-access-token).
* Authenticate with [Microsoft Entra ID](../text-translation/reference/authentication.md#authentication-with-microsoft-entra-id).

For more information about Azure resources, *see* [Azure resources for Azure AI translation](../how-to/create-translator-resource.md)

### Required headers

Include the following headers in every request to ensure the service can authenticate and route your call correctly.

| Header | Value | Required | Description |
| --- | --- | --- | --- |
| `Ocp-Apim-Subscription-Key` | Your subscription key | **True** | Azure Translator subscription key |
| `Ocp-Apim-Subscription-Region` | Your resource region | **True** | Azure resource region (for example, "eastus2") |

## How to create and use an adaptive dataset

1. You must use a Foundry resource. To learn how to create and manage a Foundry resource see [Create your first Foundry resource](../how-to/create-translator-resource.md)
2. [Create workspace](#create-workspace)
3. [Import adaptive documents (TMX/TSV)](#import-documents-tsv-tmx)
4. [Create adaptive dataset](#create-adaptive-dataset)
5. To translate with adaptive dataset see [Use Text Translation API](/azure/ai-services/translator/text-translation/preview/overview)

## API operations

The Adaptive custom translation API is organized into three main operation categories.

### Workspace adaptive dataset operations

* [Get All workspaces](#get-all-workspaces)
* [Get workspace](#get-workspace)
* [Create workspace](#create-workspace)

### Document operations

* [Get Adaptive Documents](#get-documents)
* [Import Adaptive Documents (TMX/TSV)](#import-documents-tsv-tmx)
* [Get Import Job Status](#get-import-job-status)

### Adaptive dataset operations

* [Create adaptive dataset](#create-adaptive-dataset)
* [Get adaptive dataset](#get-adaptive-dataset)
* [Get all adaptive datasets](#get-all-adaptive-datasets)
* [Delete adaptive dataset](#delete-adaptive-dataset)

## Workspace operation reference

### Get all workspaces

Retrieves all workspaces available to the authenticated user.

***Request URL***

```bash
   GET /workspaces/
```

***Request example***

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

### Get workspace

Retrieves details for a specific workspace.

***Request URL***

```bash
   GET /workspaces/<workspaceId>
```

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Unique identifier for the project |

***Request example***

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

### Create workspace

Create a workspace in Microsoft Foundry after creating your Foundry resource and project.

> 1. Select a project.
> 2. Select Build > Models > AI Services > Azure Translator - Text Translation > Adaptive LLM. The workspace is created automatically.
> 3. Retrieve the workspace ID by creating your first adaptive dataset in the playground using the Adaptive LLM tab (the GUID in <GUID>-adaptive-general), or by calling [Get all workspaces](#get-all-workspaces).

## Document operations

### Get documents

Retrieves a paginated list of documents in a project.

***Request URL***

```bash
  GET /documents?workspaceId=<workspaceId>&pageIndex={pageIndex}
```

**Parameters**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `workspaceId` | string | **True** | Project identifier |
| `pageIndex` | integer | False | Page index for pagination (default: 0) |

***Request headers***

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |
| `Content-Type` | `multipart/form-data` | False |

***Request example***

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

***Request URL***

```bash
   POST /documents/import?workspaceId=<workspaceId>
```

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

***Request headers***

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

***Request URL***

```bash
   GET /documents/import/jobs/<jobId>
```

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jobId` | string | **True** | Import job identifier |

***Request headers***

| Header | Value | Required |
|--------|-------|----------|
| `Authorization` | `Bearer <token>` | **True** |

***Request example***

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

## Adaptive dataset operations reference

### Create adaptive dataset

Creates a new dataset for adaptive translation using specified documents.

***Request URL***

```bash
   POST /index?workspaceId=<workspaceId>
```

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

***Request headers***

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

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `documentIds` | array | **True** | Array of document ID identifiers that include in dataset index. |
| `IndexName` | string | **True** | Name for the new dataset index |
| `SourceLanguage` | string | **True** | Source language code |
| `TargetLanguage` | string | **True** | Target language code |

***Request example***

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

### Get adaptive dataset

Retrieves details for a specific dataset.

***Request URL***

```bash
   GET /index/{indexId}
```

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `indexId` | string | **True** | Index identifier |

***Request example***

**Windows**

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

**Linux/macOS**

```bash
cucurl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

### Get all adaptive datasets

Retrieves all datasets in a project.

***Request URL***

```bash
   GET /index?workspaceId=<workspaceId>
```

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspaceId` | string | **True** | Project identifier |

***Request example***

**Windows**

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

**Linux/macOS**

```bash
curl -X GET "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index?workspaceId=<workspaceId>"
```

### Delete adaptive dataset

Deletes a specific language pair dataset.

***Request URL***

```bash
   DELETE /index/<indexId>
```

***Parameters***

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `indexId` | string | **True** | Dataset index identifier |

***Request example***

**Windows**

```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

**Linux/macOS**

```bash
curl -X DELETE "https://<your-resource-name>.cognitiveservices.azure.com/translator/customtranslator/api/texttranslator/v1.0/index/<indexId>"
```

## Translate with adaptive dataset ID

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

1. **Authentication**: Use MI or access token
1. **Error Handling**: Implement proper error handling and retry logic for API calls
1. **Project Organization**: Use descriptive names for projects and adaptive datasets to  organize related adaptive documents and datasets
1. **Document Management**: Ensure TSV and TMX files are properly formatted with well aligned source-target pairs. Examples are available, in foundry: select Build > Models > AI Services > Azure Translator - Text Translation > Adaptive LLM > Documents.

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

* [Learn about custom translator models](../custom-translator/overview)
* [Learn about the text translation API](../text-translation/preview/overview)
* [Explore Foundry for advanced AI capabilities](/azure/ai-foundry/)
