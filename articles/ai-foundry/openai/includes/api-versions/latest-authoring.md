---
title: Azure OpenAI latest preview authoring API documentation
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Latest preview data plane authoring documentation generated from OpenAPI 3.0 spec
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 05/08/2025
---


## Batch - List

```HTTP
GET {endpoint}/openai/batches?api-version=2025-04-01-preview
```

Gets a list of all batches owned by the Azure OpenAI resource.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| after | query | No | string | Identifier for the last event from the previous pagination request. |
| limit | query | No | integer | Number of batches to retrieve. Defaults to 20. |
| $filter | query | No | string | The OData expression to describe the filtering conditions. |
| $orderby | query | No | string | The OData expression to describe the sorting order. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [BatchesList](#batcheslist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/batches?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "has_more": false,
    "data": [
      {
        "object": "batch",
        "id": "batch_72a2792ef7d24ba7b82c7fe4a37e379f",
        "endpoint": "/chat/completions",
        "errors": null,
        "input_file_id": "file-b4fa7277f3eb4722ac18b90f46102c3f",
        "completion_window": "24h",
        "status": "completed",
        "output_file_id": "file-f2ddaf43-b48b-46dd-b264-90da10c7a85b",
        "error_file_id": "file-c3b563b0-ebc7-47da-93e3-a2fa694aef0c",
        "created_at": 1646126127,
        "in_progress_at": 1646126130,
        "expires_at": 1646126170,
        "finalizing_at": 1646126134,
        "completed_at": 1646126136,
        "failed_at": null,
        "expired_at": null,
        "cancelling_at": null,
        "cancelled_at": null,
        "request_counts": {
          "total": 500,
          "completed": 400,
          "failed": 100
        },
        "first_id": "batch_abc123",
        "last_id": "batch_abc456",
        "metadata": {
          "batch_description": "Evaluation job"
        }
      }
    ],
    "object": "list"
  }
}
```

## Batch - Create

```HTTP
POST {endpoint}/openai/batches?api-version=2025-04-01-preview
```

Creates and executes a batch from an uploaded file of requests.

Response includes details of the enqueued job including job status.

The ID of the result file is added to the response once complete.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_window | string | The time frame within which the batch should be processed. | Yes |  |
| endpoint | string | The API endpoint used by the batch. | Yes |  |
| input_blob | string | The url of an Azure Storage blob to use as input for the batch. | No |  |
| input_file_id | string | The ID of the input file for the batch. | No |  |
| metadata | object | A set of key-value pairs that can be attached to the batch. This can be useful for storing additional information about the batch in a structured format. | No |  |
| output_expires_after | [FileExpiresAfter](#fileexpiresafter) | Defines an expiration for the file. | No |  |
| output_folder | [BatchOutputReference](#batchoutputreference) | The Azure Storage folder to store output. | No |  |

### Responses

**Status Code:** 201

**Description**: The batch has been successfully created. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Batch](#batch) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/batches?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 201

```json
{
  "headers": {
    "deployment-enqueued-tokens": 1000,
    "deployment-maximum-enqueued-tokens": 5000
  },
  "body": {
    "object": "batch",
    "id": "batch_72a2792ef7d24ba7b82c7fe4a37e379f",
    "endpoint": "/chat/completions",
    "errors": null,
    "input_file_id": "file-b4fa7277f3eb4722ac18b90f46102c3f",
    "completion_window": "24h",
    "status": "validating",
    "output_file_id": null,
    "error_file_id": null,
    "created_at": 1646126127,
    "in_progress_at": null,
    "expires_at": null,
    "finalizing_at": null,
    "completed_at": null,
    "failed_at": null,
    "expired_at": null,
    "cancelling_at": null,
    "cancelled_at": null,
    "request_counts": {
      "total": 0,
      "completed": 0,
      "failed": 0
    },
    "metadata": {
      "batch_description": "Evaluation job"
    }
  }
}
```

## Batch - Get

```HTTP
GET {endpoint}/openai/batches/{batch-id}?api-version=2025-04-01-preview
```

Gets details for a single batch specified by the given batch-id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| batch-id | path | Yes | string | The identifier of the batch. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Batch](#batch) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/batches/{batch-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "batch",
    "id": "batch_72a2792ef7d24ba7b82c7fe4a37e379f",
    "endpoint": "/chat/completions",
    "errors": null,
    "input_file_id": "file-b4fa7277f3eb4722ac18b90f46102c3f",
    "completion_window": "24h",
    "status": "completed",
    "output_file_id": "file-f2ddaf43-b48b-46dd-b264-90da10c7a85b",
    "error_file_id": "file-c3b563b0-ebc7-47da-93e3-a2fa694aef0c",
    "created_at": 1646126127,
    "in_progress_at": 1646126130,
    "expires_at": 1646126170,
    "finalizing_at": 1646126134,
    "completed_at": 1646126136,
    "failed_at": null,
    "expired_at": null,
    "cancelling_at": null,
    "cancelled_at": null,
    "request_counts": {
      "total": 500,
      "completed": 400,
      "failed": 100
    },
    "metadata": {
      "batch_description": "Evaluation job"
    }
  }
}
```

## Batch - Cancel

```HTTP
POST {endpoint}/openai/batches/{batch-id}/cancel?api-version=2025-04-01-preview
```

Cancels the processing of the batch specified by the given batch-id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| batch-id | path | Yes | string | The identifier of the batch. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The batch has been successfully canceled. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Batch](#batch) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/batches/{batch-id}/cancel?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "batch",
    "id": "batch_72a2792ef7d24ba7b82c7fe4a37e379f",
    "endpoint": "/chat/completions",
    "errors": null,
    "input_file_id": "file-b4fa7277f3eb4722ac18b90f46102c3f",
    "completion_window": "24h",
    "status": "cancelling",
    "output_file_id": null,
    "error_file_id": null,
    "created_at": 1646126127,
    "in_progress_at": 1646126130,
    "expires_at": 1646126170,
    "finalizing_at": null,
    "completed_at": null,
    "failed_at": null,
    "expired_at": null,
    "cancelling_at": 1646126138,
    "cancelled_at": null,
    "request_counts": {
      "total": 500,
      "completed": 100,
      "failed": 5
    },
    "metadata": {
      "batch_description": "Evaluation job"
    }
  }
}
```

## Stored completion - List

```HTTP
GET {endpoint}/openai/chat/completions?api-version=2025-04-01-preview
```

Gets list of stored completions.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| metadata | query | No | string | Filter by the (key, value) pair in stored completion. |
| model | query | No | string | Filter by model name. |
| after | query | No | string | Identifier for the last stored completion from the previous pagination request. |
| limit | query | No | integer | Number of stored completions to retrieve. Defaults to 20. |
| order | query | No | string | Order of the results by created time (ascending or descending). Default to desc. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [StoredCompletionList](#storedcompletionlist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/chat/completions?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "list",
    "data": [
      {
        "id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
        "model": "gpt-4o-mini-2024-07-18",
        "created": 1738193475,
        "request_id": "e539c139-a97d-4ee1-bde9-3be3d5c6edb5",
        "usage": {
          "total_tokens": 25,
          "completion_tokens": 7,
          "prompt_tokens": 18
        },
        "seed": 123,
        "top_p": 1,
        "temperature": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "system_fingerprint": "fp_f3927aa00d",
        "metadata": {
          "key_1": "val_1",
          "key_2": "val_2"
        },
        "choices": [
          {
            "index": 0,
            "message": {
              "content": "Hello, how are you?",
              "role": "assistant"
            },
            "finish_reason": "stop"
          }
        ]
      }
    ],
    "total": 1,
    "first_id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
    "last_id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
    "has_more": false
  }
}
```

## Stored completion - Get

```HTTP
GET {endpoint}/openai/chat/completions/{stored-completion-id}?api-version=2025-04-01-preview
```

Gets stored completion by the given stored completion id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| stored-completion-id | path | Yes | string | The identifier of the stored completion. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [StoredCompletionResponse](#storedcompletionresponse) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/chat/completions/{stored-completion-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "chat.completion",
    "id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
    "model": "gpt-4o-mini-2024-07-18",
    "created": 1738193475,
    "request_id": "e539c139-a97d-4ee1-bde9-3be3d5c6edb5",
    "usage": {
      "total_tokens": 25,
      "completion_tokens": 7,
      "prompt_tokens": 18
    },
    "seed": 123,
    "top_p": 1,
    "temperature": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "system_fingerprint": "fp_f3927aa00d",
    "metadata": {
      "key_1": "val_1",
      "key_2": "val_2"
    },
    "choices": [
      {
        "index": 0,
        "message": {
          "content": "Hello, how are you?",
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ]
  }
}
```

## Stored completion - Update

```HTTP
POST {endpoint}/openai/chat/completions/{stored-completion-id}?api-version=2025-04-01-preview
```

Update stored completion by the given stored completion id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| stored-completion-id | path | Yes | string | The identifier of the stored completion. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Arbitrary key-value pairs for additional information. | No |  |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [StoredCompletion](#storedcompletion) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/chat/completions/{stored-completion-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "chat.completion",
    "id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
    "model": "gpt-4o-mini-2024-07-18",
    "created": 1738193475,
    "request_id": "e539c139-a97d-4ee1-bde9-3be3d5c6edb5",
    "usage": {
      "total_tokens": 25,
      "completion_tokens": 7,
      "prompt_tokens": 18
    },
    "seed": 123,
    "top_p": 1,
    "temperature": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "system_fingerprint": "fp_f3927aa00d",
    "metadata": {
      "key_1": "val_1",
      "key_2": "val_2"
    },
    "choices": [
      {
        "index": 0,
        "message": {
          "content": "Hello, how are you?",
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ]
  }
}
```

## Stored completion - Delete

```HTTP
DELETE {endpoint}/openai/chat/completions/{stored-completion-id}?api-version=2025-04-01-preview
```

Delete stored completion by the given stored completion id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| stored-completion-id | path | Yes | string | The identifier of the stored completion. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The stored completion was successfully deleted. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [StoredCompletionDelete](#storedcompletiondelete) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
DELETE {endpoint}/openai/chat/completions/{stored-completion-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "chat.completion.deleted",
    "id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
    "deleted": true
  }
}
```

## Stored completion - Getmessages

```HTTP
GET {endpoint}/openai/chat/completions/{stored-completion-id}/messages?api-version=2025-04-01-preview
```

Gets stored completion messages by the given stored completion id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| stored-completion-id | path | Yes | string | The identifier of the stored completion. |
| after | query | No | string | Identifier for the last stored completion message from the previous pagination request. |
| limit | query | No | integer | Number of stored completions messages to retrieve. Defaults to 20. |
| order | query | No | string | Order of the results by message index (ascending or descending). Default to asc. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [StoredCompletionMessages](#storedcompletionmessages) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/chat/completions/{stored-completion-id}/messages?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "list",
    "data": [
      {
        "role": "user",
        "content": "Hello"
      }
    ],
    "total": 1,
    "first_id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
    "last_id": "chatcmpl-AvBCKqg2xqxVHCCEnUB4Bgj1Bjl7Y",
    "has_more": false
  }
}
```

## Evaluation - Get list

```HTTP
GET {endpoint}/openai/evals?api-version=2025-04-01-preview
```

List evaluations for a project.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| after | query | No | string | Identifier for the last eval from the previous pagination request. |
| limit | query | No | integer | Number of evals to retrieve. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for evals by timestamp. Use `asc` for ascending order or `desc` for descending order. |
| order_by | query | No | string<br>Possible values: `created_at`, `updated_at` | Evals can be ordered by creation time or last updated time. Use `created_at` for creation time or `updated_at` for last updated time. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: A list of evals 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalList](#evallist) | |

### Examples




```HTTP
GET {endpoint}/openai/evals?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "list",
    "data": [
      {
        "object": "eval",
        "id": "eval_6801694950848190b10968bb628b651d",
        "data_source_config": {
          "type": "custom",
          "schema": {
            "type": "object",
            "properties": {
              "item": {
                "type": "object",
                "properties": {
                  "question": {
                    "type": "string"
                  },
                  "A": {
                    "type": "string"
                  },
                  "B": {
                    "type": "string"
                  },
                  "C": {
                    "type": "string"
                  },
                  "D": {
                    "type": "string"
                  },
                  "answer": {
                    "type": "string"
                  }
                }
              }
            },
            "required": [
              "item"
            ]
          }
        },
        "testing_criteria": [
          {
            "name": "string check",
            "type": "string_check",
            "input": "{{sample.output_text}}",
            "reference": "{{item.answer}}",
            "operation": "eq"
          }
        ],
        "name": "Math Quiz",
        "created_at": 1744922953,
        "metadata": {}
      }
    ],
    "first_id": "eval_6801694950848190b10968bb628b651d",
    "last_id": "eval_6801694950848190b10968bb628b651d",
    "has_more": false
  }
}
```

## Evaluation - Create

```HTTP
POST {endpoint}/openai/evals?api-version=2025-04-01-preview
```

Create the structure of an evaluation that can be used to test a model's performance.
An evaluation is a set of testing criteria and a datasource. After creating an evaluation, you can run it on different models and model parameters. We support several types of graders and datasources. 

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 201

**Description**: OK 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Eval](#eval) | |

### Examples




```HTTP
POST {endpoint}/openai/evals?api-version=2025-04-01-preview

{
 "name": "Math Quiz",
 "data_source_config": {
  "type": "custom",
  "include_sample_schema": true,
  "item_schema": {
   "type": "object",
   "properties": {
    "question": {
     "type": "string"
    },
    "A": {
     "type": "string"
    },
    "B": {
     "type": "string"
    },
    "C": {
     "type": "string"
    },
    "D": {
     "type": "string"
    },
    "answer": {
     "type": "string"
    }
   }
  }
 },
 "testing_criteria": [
  {
   "type": "string_check",
   "reference": "{{item.answer}}",
   "input": "{{sample.output_text}}",
   "operation": "eq",
   "name": "string check"
  }
 ]
}

```

**Responses**:
Status Code: 201

```json
{
  "headers": {},
  "body": {
    "object": "eval",
    "id": "eval_6801694950848190b10968bb628b651d",
    "data_source_config": {
      "type": "custom",
      "schema": {
        "type": "object",
        "properties": {
          "item": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string"
              },
              "A": {
                "type": "string"
              },
              "B": {
                "type": "string"
              },
              "C": {
                "type": "string"
              },
              "D": {
                "type": "string"
              },
              "answer": {
                "type": "string"
              }
            }
          }
        },
        "required": [
          "item"
        ]
      }
    },
    "testing_criteria": [
      {
        "name": "string check",
        "type": "string_check",
        "input": "{{sample.output_text}}",
        "reference": "{{item.answer}}",
        "operation": "eq"
      }
    ],
    "name": "Math Quiz",
    "created_at": 1744922953,
    "metadata": {}
  }
}
```

## Evaluation - Delete

```HTTP
DELETE {endpoint}/openai/evals/{eval-id}?api-version=2025-04-01-preview
```

Delete an evaluation.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to delete. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Successfully deleted the evaluation. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Status Code:** 404

**Description**: Evaluation not found. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Error](#error) | |

### Examples




```HTTP
DELETE {endpoint}/openai/evals/{eval-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "eval.deleted",
    "deleted": true,
    "eval_id": "eval_6801694950848190b10968bb628b651d"
  }
}
```
Status Code: 404

```json
{
  "headers": {},
  "body": {
    "code": "notFound",
    "message": "Evaluation with ID eval_6801694950848190b10968bb628b651d not found."
  }
}
```

## Evaluation - Get

```HTTP
GET {endpoint}/openai/evals/{eval-id}?api-version=2025-04-01-preview
```

Get an evaluation by ID.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to retrieve. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The evaluation 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Eval](#eval) | |

### Examples




```HTTP
GET {endpoint}/openai/evals/{eval-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "eval",
    "id": "eval_6801694950848190b10968bb628b651d",
    "data_source_config": {
      "type": "custom",
      "schema": {
        "type": "object",
        "properties": {
          "item": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string"
              },
              "A": {
                "type": "string"
              },
              "B": {
                "type": "string"
              },
              "C": {
                "type": "string"
              },
              "D": {
                "type": "string"
              },
              "answer": {
                "type": "string"
              }
            }
          }
        },
        "required": [
          "item"
        ]
      }
    },
    "testing_criteria": [
      {
        "name": "string check",
        "type": "string_check",
        "input": "{{sample.output_text}}",
        "reference": "{{item.answer}}",
        "operation": "eq"
      }
    ],
    "name": "Math Quiz",
    "created_at": 1744922953,
    "metadata": {}
  }
}
```

## Evaluation - Update

```HTTP
POST {endpoint}/openai/evals/{eval-id}?api-version=2025-04-01-preview
```

Update certain properties of an evaluation.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to update. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The updated evaluation 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Eval](#eval) | |

### Examples




```HTTP
POST {endpoint}/openai/evals/{eval-id}?api-version=2025-04-01-preview

{
 "name": "Updated Math Quiz",
 "metadata": {
  "description": "Updated description"
 }
}

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "eval",
    "id": "eval_6801694950848190b10968bb628b651d",
    "data_source_config": {
      "type": "custom",
      "schema": {
        "type": "object",
        "properties": {
          "item": {
            "type": "object",
            "properties": {
              "question": {
                "type": "string"
              },
              "A": {
                "type": "string"
              },
              "B": {
                "type": "string"
              },
              "C": {
                "type": "string"
              },
              "D": {
                "type": "string"
              },
              "answer": {
                "type": "string"
              }
            }
          }
        },
        "required": [
          "item"
        ]
      }
    },
    "testing_criteria": [
      {
        "name": "string check",
        "type": "string_check",
        "input": "{{sample.output_text}}",
        "reference": "{{item.answer}}",
        "operation": "eq"
      }
    ],
    "name": "Updated Math Quiz",
    "created_at": 1744922953,
    "metadata": {
      "description": "Updated description"
    }
  }
}
```

## Evaluation - Getrunlist

```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs?api-version=2025-04-01-preview
```

Get a list of runs for an evaluation.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to retrieve runs for. |
| after | query | No | string | Identifier for the last run from the previous pagination request. |
| limit | query | No | integer | Number of runs to retrieve. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for runs by timestamp. Use `asc` for ascending order or `desc` for descending order. Defaults to `asc`. |
| status | query | No | string<br>Possible values: `queued`, `in_progress`, `completed`, `canceled`, `failed` | Filter runs by status. Use "queued", "in_progress", "failed", "completed", "canceled". |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: A list of runs for the evaluation 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRunList](#evalrunlist) | |

### Examples




```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "list",
    "data": [
      {
        "object": "eval.run",
        "id": "evalrun_68016a056f0481909b9774447bdd1aa3",
        "eval_id": "eval_6801694950848190b10968bb628b651d",
        "report_url": "https://ai.azure.com/resource/evaluation",
        "status": "queued",
        "model": "gpt-4o-mini",
        "name": "Math quiz",
        "created_at": 1744923141,
        "result_counts": {
          "total": 0,
          "errored": 0,
          "failed": 0,
          "passed": 0
        },
        "per_model_usage": null,
        "per_testing_criteria_results": null,
        "data_source": {
          "type": "completions",
          "source": {
            "type": "file_content",
            "content": [
              {
                "item": {
                  "question": "Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.",
                  "A": "0",
                  "B": "4",
                  "C": "2",
                  "D": "6",
                  "answer": "B"
                }
              },
              {
                "item": {
                  "question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.",
                  "A": "8",
                  "B": "2",
                  "C": "24",
                  "D": "120",
                  "answer": "C"
                }
              }
            ]
          },
          "input_messages": {
            "template": [
              {
                "type": "message",
                "role": "system",
                "content": {
                  "text": "Answer the question's with A, B, C, or D."
                }
              },
              {
                "type": "message",
                "role": "user",
                "content": {
                  "text": "Question: {{item.question}} A: {{item.A}} B: {{item.B}} C: {{item.C}} D: {{item.D}}."
                }
              }
            ]
          },
          "model": "gpt-4o-mini",
          "sampling_params": {
            "seed": 42,
            "temperature": 1,
            "top_p": 1
          }
        },
        "error": null,
        "metadata": {}
      }
    ],
    "first_id": "evalrun_68016a056f0481909b9774447bdd1aa3",
    "last_id": "evalrun_68016a056f0481909b9774447bdd1aa3",
    "has_more": false
  }
}
```

## Evaluation - Create run

```HTTP
POST {endpoint}/openai/evals/{eval-id}/runs?api-version=2025-04-01-preview
```

Create a new evaluation run. This is the endpoint that will kick off grading.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to create a run for. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 201

**Description**: Successfully created a run for the evaluation 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRun](#evalrun) | |

**Status Code:** 400

**Description**: Bad request (for example, missing eval object) 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Error](#error) | |

### Examples




```HTTP
POST {endpoint}/openai/evals/{eval-id}/runs?api-version=2025-04-01-preview

{
 "name": "Math quiz",
 "data_source": {
  "type": "completions",
  "source": {
   "type": "file_content",
   "content": [
    {
     "item": {
      "question": "Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.",
      "A": "0",
      "B": "4",
      "C": "2",
      "D": "6",
      "answer": "B"
     }
    },
    {
     "item": {
      "question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.",
      "A": "8",
      "B": "2",
      "C": "24",
      "D": "120",
      "answer": "C"
     }
    }
   ]
  },
  "input_messages": {
   "type": "template",
   "template": [
    {
     "type": "message",
     "role": "system",
     "content": {
      "text": "Answer the question's with A, B, C, or D."
     }
    },
    {
     "type": "message",
     "role": "user",
     "content": {
      "text": "Question: {{item.question}} A: {{item.A}} B: {{item.B}} C: {{item.C}} D: {{item.D}}."
     }
    }
   ]
  },
  "model": "gpt-4o-mini",
  "sampling_params": {
   "temperature": 1,
   "top_p": 1,
   "seed": 42
  }
 }
}

```

**Responses**:
Status Code: 201

```json
{
  "headers": {},
  "body": {
    "object": "eval.run",
    "id": "evalrun_68016a056f0481909b9774447bdd1aa3",
    "eval_id": "eval_6801694950848190b10968bb628b651d",
    "report_url": "https://ai.azure.com/resource/evaluation",
    "status": "queued",
    "model": "gpt-4o-mini",
    "name": "Math quiz",
    "created_at": 1744923141,
    "result_counts": {
      "total": 0,
      "errored": 0,
      "failed": 0,
      "passed": 0
    },
    "per_model_usage": null,
    "per_testing_criteria_results": null,
    "data_source": {
      "type": "completions",
      "source": {
        "type": "file_content",
        "content": [
          {
            "item": {
              "question": "Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.",
              "A": "0",
              "B": "4",
              "C": "2",
              "D": "6",
              "answer": "B"
            }
          },
          {
            "item": {
              "question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.",
              "A": "8",
              "B": "2",
              "C": "24",
              "D": "120",
              "answer": "C"
            }
          }
        ]
      },
      "input_messages": {
        "type": "template",
        "template": [
          {
            "type": "message",
            "role": "system",
            "content": {
              "text": "Answer the question's with A, B, C, or D."
            }
          },
          {
            "type": "message",
            "role": "user",
            "content": {
              "text": "Question: {{item.question}} A: {{item.A}} B: {{item.B}} C: {{item.C}} D: {{item.D}}."
            }
          }
        ]
      },
      "model": "gpt-4o-mini",
      "sampling_params": {
        "seed": 42,
        "temperature": 1,
        "top_p": 1
      }
    },
    "error": null,
    "metadata": {}
  }
}
```

## Evaluation - Delete run

```HTTP
DELETE {endpoint}/openai/evals/{eval-id}/runs/{run-id}?api-version=2025-04-01-preview
```

Delete an eval run.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to delete the run from. |
| run-id | path | Yes | string | The ID of the run to delete. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Successfully deleted the eval run 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Status Code:** 404

**Description**: Run not found 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Error](#error) | |

### Examples




```HTTP
DELETE {endpoint}/openai/evals/{eval-id}/runs/{run-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "eval.deleted",
    "deleted": true,
    "run_id": "evalrun_68016a056f0481909b9774447bdd1aa3"
  }
}
```
Status Code: 404

```json
{
  "headers": {},
  "body": {
    "code": "notFound",
    "message": "Evaluation Run with ID evalrun_68016a056f0481909b9774447bdd1aa3 not found."
  }
}
```

## Evaluation - Get run

```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs/{run-id}?api-version=2025-04-01-preview
```

Get an evaluation run by ID.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to retrieve runs for. |
| run-id | path | Yes | string | The ID of the run to retrieve. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The evaluation run 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRun](#evalrun) | |

### Examples




```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs/{run-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "eval.run",
    "id": "evalrun_68016a056f0481909b9774447bdd1aa3",
    "eval_id": "eval_6801694950848190b10968bb628b651d",
    "report_url": "https://ai.azure.com/resource/evaluation",
    "status": "queued",
    "model": "gpt-4o-mini",
    "name": "Math quiz",
    "created_at": 1744923141,
    "result_counts": {
      "total": 0,
      "errored": 0,
      "failed": 0,
      "passed": 0
    },
    "per_model_usage": null,
    "per_testing_criteria_results": null,
    "data_source": {
      "type": "completions",
      "source": {
        "type": "file_content",
        "content": [
          {
            "item": {
              "question": "Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.",
              "A": "0",
              "B": "4",
              "C": "2",
              "D": "6",
              "answer": "B"
            }
          },
          {
            "item": {
              "question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.",
              "A": "8",
              "B": "2",
              "C": "24",
              "D": "120",
              "answer": "C"
            }
          }
        ]
      },
      "input_messages": {
        "type": "template",
        "template": [
          {
            "type": "message",
            "role": "system",
            "content": {
              "text": "Answer the question's with A, B, C, or D."
            }
          },
          {
            "type": "message",
            "role": "user",
            "content": {
              "text": "Question: {{item.question}} A: {{item.A}} B: {{item.B}} C: {{item.C}} D: {{item.D}}."
            }
          }
        ]
      },
      "model": "gpt-4o-mini",
      "sampling_params": {
        "seed": 42,
        "temperature": 1,
        "top_p": 1
      }
    },
    "error": null,
    "metadata": {}
  }
}
```

## Evaluation - Cancel run

```HTTP
POST {endpoint}/openai/evals/{eval-id}/runs/{run-id}?api-version=2025-04-01-preview
```

Cancel an ongoing evaluation run.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation whose run you want to cancel. |
| run-id | path | Yes | string | The ID of the run to cancel. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The canceled eval run object 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRun](#evalrun) | |

### Examples




```HTTP
POST {endpoint}/openai/evals/{eval-id}/runs/{run-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "eval.run",
    "id": "evalrun_68016a056f0481909b9774447bdd1aa3",
    "eval_id": "eval_6801694950848190b10968bb628b651d",
    "report_url": "https://ai.azure.com/resource/evaluation",
    "status": "canceled",
    "model": "gpt-4o-mini",
    "name": "Math quiz",
    "created_at": 1744923141,
    "result_counts": {
      "total": 0,
      "errored": 0,
      "failed": 0,
      "passed": 0
    },
    "per_model_usage": null,
    "per_testing_criteria_results": null,
    "data_source": {
      "type": "completions",
      "source": {
        "type": "file_content",
        "content": [
          {
            "item": {
              "question": "Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.",
              "A": "0",
              "B": "4",
              "C": "2",
              "D": "6",
              "answer": "B"
            }
          },
          {
            "item": {
              "question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.",
              "A": "8",
              "B": "2",
              "C": "24",
              "D": "120",
              "answer": "C"
            }
          }
        ]
      },
      "input_messages": {
        "type": "template",
        "template": [
          {
            "type": "message",
            "role": "system",
            "content": {
              "text": "Answer the question's with A, B, C, or D."
            }
          },
          {
            "type": "message",
            "role": "user",
            "content": {
              "text": "Question: {{item.question}} A: {{item.A}} B: {{item.B}} C: {{item.C}} D: {{item.D}}."
            }
          }
        ]
      },
      "model": "gpt-4o-mini",
      "sampling_params": {
        "seed": 42,
        "temperature": 1,
        "top_p": 1
      }
    },
    "error": null,
    "metadata": {}
  }
}
```

## Evaluation - Getrunoutputitems

```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs/{run-id}/output_items?api-version=2025-04-01-preview
```

Get a list of output items for an evaluation run.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to retrieve runs for. |
| run-id | path | Yes | string | The ID of the run to retrieve output items for. |
| after | query | No | string | Identifier for the last output item from the previous pagination request. |
| limit | query | No | integer | Number of output items to retrieve. |
| status | query | No | string<br>Possible values: `fail`, `pass` | Filter output items by status. Use `failed` to filter by failed output items or `pass` to filter by passed output items. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for output items by timestamp. Use `asc` for ascending order or `desc` for descending order. Defaults to `asc`. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: A list of output items for the evaluation run 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRunOutputItemList](#evalrunoutputitemlist) | |

### Examples




```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs/{run-id}/output_items?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "list",
    "data": [
      {
        "object": "eval.run.output_item",
        "id": "outputitem_68017251ff3881908bf5096bf4cd91c6",
        "created_at": 1744925265,
        "run_id": "evalrun_68016a056f0481909b9774447bdd1aa3",
        "eval_id": "eval_6801694950848190b10968bb628b651d",
        "status": "fail",
        "datasource_item_id": 1,
        "datasource_item": {
          "question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.",
          "A": "8",
          "B": "2",
          "C": "24",
          "D": "120",
          "answer": "C"
        },
        "results": [
          {
            "name": "string check-63b1fffa-bee6-4c37-ae77-ed46e3dce2b7",
            "sample": null,
            "passed": false,
            "score": 0
          }
        ],
        "sample": {
          "input": [
            {
              "role": "system",
              "content": "Answer the question's with A, B, C, or D.",
              "function_call": null
            },
            {
              "role": "user",
              "content": "Question: Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5. A: 8 B: 2 C: 24 D: 120.",
              "function_call": null
            }
          ],
          "output": [
            {
              "role": "assistant",
              "content": "To find the index of the subgroup generated by the permutation \\( p = (1, 2, 5, 4)(2, 3) \\) in \\( S_5 \\), we first need to determine the order of \\( p \\).\n\n1. The cycle \\( (1, 2, 5, 4) \\) has length 4.\n2. The cycle \\( (2, 3) \\) has length 2.\n3. The least common multiple (LCM) of these lengths gives the order of the permutation \\( p \\).\n\nCalculating the LCM:\n\\[\n\\text{lcm}(4, 2) = 4\n\\]\nThus, the order of \\( p \\) is 4.\n\nNext, we find the size of the subgroup \\( \\langle p \\rangle \\):\n- The size of \\( \\langle p \\rangle \\) is equal to the order of \\( p \\), which is 4.\n\nNow, we know the size of \\( S_5 \\):\n\\[\n|S_5| = 5! = 120\n\\]\n\nFinally, to find the index of \\( \\langle p \\rangle \\) in \\( S_5 \\), we use the formula:\n\\[\n\\text{index} = \\frac{|S_5|}{|\\langle p \\rangle|} = \\frac{120}{4} = 30\n\\]\n\nHowever, the available answer choices do not include 30. There may be a mistake because the question expects an answer among A, B, C, and D.\n\nLet\u00e2\u20ac\u2122s assume we misunderstood \\( \\langle p \\rangle \\), and instead, we can deduce based solely on given answers looking for a relation to \\( S_5 \\) without delving into detailed subgroup tracks. \n\nSince \\( S_5 \\) has 30 different elements in a subgroup configuration, the closest answer physically relating as long as \\( p \\) covers two elements effectively would logically fit an answer of 120 / 60 which has no direct relationship.\n\nGiven the option choices and specific rank formulations as often made regarding elements in specific construct the subgroup at best reflects around a viable ratio of parts allowed through available indices. \n\nThus, after reasoning through which aligns most structurally geometrically yielding across all configurations possible integrated yet arrives leading \\( p \\) through neighborhood distributions leaving reflections outstanding:\n\n\n\nThe correct answer is:\n**C: 24**\n\nHowever per the discussion migrating \\( p \\) may leave various pathways leading ultimately toward that framing in modeling. Always a good suggestion confirming the elements group generating any possible in outputs rationales. ",
              "function_call": null
            }
          ],
          "finish_reason": "stop",
          "model": "gpt-4o-mini-2024-07-18",
          "usage": {
            "total_tokens": 627,
            "completion_tokens": 546,
            "prompt_tokens": 81,
            "cached_tokens": 0
          },
          "error": null,
          "temperature": 1,
          "top_p": 1,
          "seed": 42
        }
      },
      {
        "object": "eval.run.output_item",
        "id": "outputitem_6801724f54888190942ec66a197309dd",
        "created_at": 1744925263,
        "run_id": "evalrun_68016a056f0481909b9774447bdd1aa3",
        "eval_id": "eval_6801694950848190b10968bb628b651d",
        "status": "fail",
        "datasource_item_id": 0,
        "datasource_item": {
          "question": "Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.",
          "A": "0",
          "B": "4",
          "C": "2",
          "D": "6",
          "answer": "B"
        },
        "results": [
          {
            "name": "string check-63b1fffa-bee6-4c37-ae77-ed46e3dce2b7",
            "sample": null,
            "passed": false,
            "score": 0
          }
        ],
        "sample": {
          "input": [
            {
              "role": "system",
              "content": "Answer the question's with A, B, C, or D.",
              "function_call": null
            },
            {
              "role": "user",
              "content": "Question: Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q. A: 0 B: 4 C: 2 D: 6.",
              "function_call": null
            }
          ],
          "output": [
            {
              "role": "assistant",
              "content": "To find the degree of the field extension \\(\\mathbb{Q}(\\sqrt{2}, \\sqrt{3}, \\sqrt{18})\\) over \\(\\mathbb{Q}\\), we can simplify \\(\\sqrt{18}\\) since \\(\\sqrt{18} = \\sqrt{9 \\cdot 2} = 3\\sqrt{2}\\). \n\nThus, the field can be rewritten as \\(\\mathbb{Q}(\\sqrt{2}, \\sqrt{3})\\).\n\nNext, we calculate the degree of the extensions step by step:\n\n1. The extension \\(\\mathbb{Q}(\\sqrt{2})\\) over \\(\\mathbb{Q}\\) has degree 2, since \\(\\sqrt{2}\\) is not in \\(\\mathbb{Q}\\) and satisfies the polynomial \\(x^2 - 2\\).\n\n2. Next, we consider the extension \\(\\mathbb{Q}(\\sqrt{2}, \\sqrt{3})\\) over \\(\\mathbb{Q}(\\sqrt{2})\\). The element \\(\\sqrt{3}\\) is also not in \\(\\mathbb{Q}(\\sqrt{2})\\) and satisfies the polynomial \\(x^2 - 3\\), which is irreducible over \\(\\mathbb{Q}(\\sqrt{2})\\). Hence, the degree of the extension \\(\\mathbb{Q}(\\sqrt{2}, \\sqrt{3})\\) over \\(\\mathbb{Q}(\\sqrt{2})\\) is also 2.\n\nNow we can combine these degrees:\n\n\\[\n[\\mathbb{Q}(\\sqrt{2}, \\sqrt{3}) : \\mathbb{Q}] = [\\mathbb{Q}(\\sqrt{2}, \\sqrt{3}) : \\mathbb{Q}(\\sqrt{2})] \\times [\\mathbb{Q}(\\sqrt{2}) : \\mathbb{Q}] = 2 \\times 2 = 4.\n\\]\n\nThus, the degree of the field extension \\(\\mathbb{Q}(\\sqrt{2}, \\sqrt{3}, \\sqrt{18})\\) over \\(\\mathbb{Q}\\) is 4.\n\nTherefore, the answer is:\n\n**B: 4**.",
              "function_call": null
            }
          ],
          "finish_reason": "stop",
          "model": "gpt-4o-mini-2024-07-18",
          "usage": {
            "total_tokens": 556,
            "completion_tokens": 487,
            "prompt_tokens": 69,
            "cached_tokens": 0
          },
          "error": null,
          "temperature": 1,
          "top_p": 1,
          "seed": 42
        }
      }
    ],
    "first_id": "outputitem_68017251ff3881908bf5096bf4cd91c6",
    "last_id": "outputitem_6801724f54888190942ec66a197309dd",
    "has_more": false
  }
}
```

## Evaluation - Getrunoutputitem

```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs/{run-id}/output_items/{output-item-id}?api-version=2025-04-01-preview
```

Get an evaluation run output item by ID.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| eval-id | path | Yes | string | The ID of the evaluation to retrieve runs for. |
| run-id | path | Yes | string | The ID of the run to retrieve. |
| output-item-id | path | Yes | string | The ID of the output item to retrieve. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The evaluation run output item 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [EvalRunOutputItem](#evalrunoutputitem) | |

### Examples




```HTTP
GET {endpoint}/openai/evals/{eval-id}/runs/{run-id}/output_items/{output-item-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "eval.run.output_item",
    "id": "outputitem_68017251ff3881908bf5096bf4cd91c6",
    "created_at": 1744925265,
    "run_id": "evalrun_68016a056f0481909b9774447bdd1aa3",
    "eval_id": "eval_6801694950848190b10968bb628b651d",
    "status": "fail",
    "datasource_item_id": 1,
    "datasource_item": {
      "question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.",
      "A": "8",
      "B": "2",
      "C": "24",
      "D": "120",
      "answer": "C"
    },
    "results": [
      {
        "name": "string check-63b1fffa-bee6-4c37-ae77-ed46e3dce2b7",
        "sample": null,
        "passed": false,
        "score": 0
      }
    ],
    "sample": {
      "input": [
        {
          "role": "system",
          "content": "Answer the question's with A, B, C, or D."
        },
        {
          "role": "user",
          "content": "Question: Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5. A: 8 B: 2 C: 24 D: 120."
        }
      ],
      "output": [
        {
          "role": "assistant",
          "content": "To find the index of the subgroup generated by the permutation \\( p = (1, 2, 5, 4)(2, 3) \\) in \\( S_5 \\), we first need to determine the order of \\( p \\).\n\n1. The cycle \\( (1, 2, 5, 4) \\) has length 4.\n2. The cycle \\( (2, 3) \\) has length 2.\n3. The least common multiple (LCM) of these lengths gives the order of the permutation \\( p \\).\n\nCalculating the LCM:\n\\[\n\\text{lcm}(4, 2) = 4\n\\]\nThus, the order of \\( p \\) is 4.\n\nNext, we find the size of the subgroup \\( \\langle p \\rangle \\):\n- The size of \\( \\langle p \\rangle \\) is equal to the order of \\( p \\), which is 4.\n\nNow, we know the size of \\( S_5 \\):\n\\[\n|S_5| = 5! = 120\n\\]\n\nFinally, to find the index of \\( \\langle p \\rangle \\) in \\( S_5 \\), we use the formula:\n\\[\n\\text{index} = \\frac{|S_5|}{|\\langle p \\rangle|} = \\frac{120}{4} = 30\n\\]\n\nHowever, the available answer choices do not include 30. There may be a mistake because the question expects an answer among A, B, C, and D.\n\nLet\u00e2\u20ac\u2122s assume we misunderstood \\( \\langle p \\rangle \\), and instead, we can deduce based solely on given answers looking for a relation to \\( S_5 \\) without delving into detailed subgroup tracks. \n\nSince \\( S_5 \\) has 30 different elements in a subgroup configuration, the closest answer physically relating as long as \\( p \\) covers two elements effectively would logically fit an answer of 120 / 60 which has no direct relationship.\n\nGiven the option choices and specific rank formulations as often made regarding elements in specific construct the subgroup at best reflects around a viable ratio of parts allowed through available indices. \n\nThus, after reasoning through which aligns most structurally geometrically yielding across all configurations possible integrated yet arrives leading \\( p \\) through neighborhood distributions leaving reflections outstanding:\n\n\n\nThe correct answer is:\n**C: 24**\n\nHowever per the discussion migrating \\( p \\) may leave various pathways leading ultimately toward that framing in modeling. Always a good suggestion confirming the elements group generating any possible in outputs rationales. "
        }
      ],
      "finish_reason": "stop",
      "model": "gpt-4o-mini-2024-07-18",
      "usage": {
        "total_tokens": 627,
        "completion_tokens": 546,
        "prompt_tokens": 81,
        "cached_tokens": 0
      },
      "error": null,
      "temperature": 1,
      "top_p": 1,
      "seed": 42
    }
  }
}
```

## Files - List

```HTTP
GET {endpoint}/openai/files?api-version=2025-04-01-preview
```

Gets a list of all files owned by the Azure OpenAI resource.

These include user uploaded content like files with purpose "fine-tune" for training or validation of fine-tunes models as well as files that are generated by the service such as "fine-tune-results" which contains various metrics for the corresponding fine-tuning job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| purpose | query | No | string<br>Possible values: `fine-tune`, `fine-tune-results`, `assistants`, `assistants_output`, `batch`, `batch_output`, `evals`, `evals_output` | Only return files with the given purpose. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 10,000, and the default is 10,000. |
| `after` | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| order | query | No | string | Sort order by the created_at timestamp of the objects. `asc` for ascending order and `desc` for descending order. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FileList](#filelist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/files?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "data": [
      {
        "status": "processed",
        "bytes": 140,
        "purpose": "fine-tune",
        "filename": "puppy.jsonl",
        "id": "file-181a1cbdcdcf4677ada87f63a0928099",
        "created_at": 1646126127,
        "object": "file"
      },
      {
        "status": "processed",
        "bytes": 32423,
        "purpose": "fine-tune-results",
        "filename": "results.csv",
        "id": "file-181a1cbdcdcf4677ada87f63a0928099",
        "created_at": 1646126127,
        "object": "file"
      }
    ],
    "object": "list"
  }
}
```

## Files - Upload

```HTTP
POST {endpoint}/openai/files?api-version=2025-04-01-preview
```

Creates a new file entity by uploading data from a local machine. Uploaded files can, for example, be used for training or evaluating fine-tuned models.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: multipart/form-data

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| anchor | string | Defines the anchor relative to what time the absolute expiration should be generated from. | No |  |
| seconds | integer | Gets the relative expiration time in seconds.
Range: [1209600 - 2592000]. | No |  |
| file | string | Gets or sets the file to upload into Azure OpenAI. | Yes |  |
| purpose | string | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |

### Responses

**Status Code:** 201

**Description**: The file has been successfully created. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [File](#file) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/files?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 201

```json
{
  "headers": {
    "location": "https://aoairesource.openai.azure.com/openai/files/file-181a1cbdcdcf4677ada87f63a0928099"
  },
  "body": {
    "status": "pending",
    "purpose": "fine-tune",
    "filename": "puppy.jsonl",
    "id": "file-181a1cbdcdcf4677ada87f63a0928099",
    "created_at": 1646126127,
    "object": "file"
  }
}
```

## Files - Import

```HTTP
POST {endpoint}/openai/files/import?api-version=2025-04-01-preview
```

Creates a new file entity by importing data from a provided url. Uploaded files can, for example, be used for training or evaluating fine-tuned models.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_url | string | The url to download the document from (can be SAS url of a blob or any other external url accessible with a GET request). | Yes |  |
| expires_after | [FileExpiresAfter](#fileexpiresafter) | Defines an expiration for the file. | No |  |
| filename | string | The name of the [JSON Lines](https://jsonlines.readthedocs.io/en/latest/) file to be uploaded.
If the `purpose` is set to "fine-tune", each line is a JSON record with "prompt" and "completion" fields representing your training examples. | Yes |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |

### Responses

**Status Code:** 201

**Description**: The file has been successfully created. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [File](#file) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/files/import?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 201

```json
{
  "headers": {
    "location": "https://aoairesource.openai.azure.com/openai/files/file-181a1cbdcdcf4677ada87f63a0928099"
  },
  "body": {
    "status": "pending",
    "purpose": "fine-tune",
    "filename": "puppy.jsonl",
    "id": "file-181a1cbdcdcf4677ada87f63a0928099",
    "created_at": 1646126127,
    "object": "file"
  }
}
```

## Files - Get

```HTTP
GET {endpoint}/openai/files/{file-id}?api-version=2025-04-01-preview
```

Gets details for a single file specified by the given file-id including status, size, purpose, etc.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| file-id | path | Yes | string | The identifier of the file. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [File](#file) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/files/{file-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "status": "processed",
    "bytes": 140,
    "purpose": "fine-tune",
    "filename": "puppy.jsonl",
    "id": "file-181a1cbdcdcf4677ada87f63a0928099",
    "created_at": 1646126127,
    "object": "file"
  }
}
```

## Files - Delete

```HTTP
DELETE {endpoint}/openai/files/{file-id}?api-version=2025-04-01-preview
```

Deletes the file with the given file-id.

Deletion is also allowed if a file was used, e.g., as training file in a fine-tuning job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| file-id | path | Yes | string | The identifier of the file. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The file was successfully deleted. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FileDelete](#filedelete) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
DELETE {endpoint}/openai/files/{file-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "object": "file",
    "deleted": true,
    "id": "file-181a1cbdcdcf4677ada87f63a0928099"
  }
}
```

## Files - Get content

```HTTP
GET {endpoint}/openai/files/{file-id}/content?api-version=2025-04-01-preview
```

Gets the content of the file specified by the given file-id.

Files can be user uploaded content or generated by the service like result metrics of a fine-tuning job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| file-id | path | Yes | string | The identifier of the file. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/octet-stream | string | |
|application/json | string | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/octet-stream | [ErrorResponse](#errorresponse) | |
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/files/{file-id}/content?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": "raw file content"
}
```

## Fine-tuning - List

```HTTP
GET {endpoint}/openai/fine_tuning/jobs?api-version=2025-04-01-preview
```

Gets a list of all fine-tuning jobs owned by the Azure OpenAI resource.The details that are returned for each fine-tuning job contain besides its identifier the base model, training and validation files, hyper parameters, time stamps, status and events.

Events are created when the job status changes. For example, running or complete, and when results are uploaded.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| after | query | No | string | Identifier for the last event from the previous pagination request. |
| limit | query | No | integer | Number of events to retrieve. Defaults to 20. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJobList](#finetuningjoblist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/fine_tuning/jobs?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "has_more": false,
    "data": [
      {
        "hyperparameters": {
          "n_epochs": -1
        },
        "integrations": [
          {
            "type": "wandb",
            "wandb": {
              "project": "custom-wandb-project",
              "tags": [
                "project:tag",
                "lineage"
              ]
            }
          }
        ],
        "method": {
          "type": "supervised"
        },
        "status": "succeeded",
        "model": "curie",
        "fine_tuned_model": "curie.ft-72a2792ef7d24ba7b82c7fe4a37e379f",
        "training_file": "file-181a1cbdcdcf4677ada87f63a0928099",
        "result_files": [
          "file-181a1cbdcdcf4677ada87f63a0928099"
        ],
        "finished_at": 1646127311,
        "trained_tokens": 2342,
        "id": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
        "created_at": 1646126127,
        "object": "fine_tuning.job"
      }
    ],
    "object": "list"
  }
}
```

## Fine-tuning - Create

```HTTP
POST {endpoint}/openai/fine_tuning/jobs?api-version=2025-04-01-preview
```

Creates a job that fine-tunes a specified model from a given training file.

Response includes details of the enqueued job including job status and hyper parameters.

The name of the fine-tuned model is added to the response once complete.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [FineTuningHyperParameters](#finetuninghyperparameters) | The hyper parameter settings used in a fine tune job. | No |  |
| integrations | array | A list of configurations for integrations supporting the fine-tuning job. There are many integrations planned, so make sure to check and act on the integration type. | No |  |
| method | object | Method used for supervised fine-tuning | No |  |
| └─ type | [FineTuningMethodType](#finetuningmethodtype) |  | No |  |
| model | string | The identifier (model-id) of the base model used for this fine-tune. | Yes |  |
| seed | integer | The seed used for the fine-tuning job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be generated for you. | No |  |
| suffix | string | The suffix used to identify the fine-tuned model. The suffix can contain up to 40 characters (a-z, A-Z, 0-9,- and _) that will be added to your fine-tuned model name. | No |  |
| training_file | string | The file identity (file-id) that is used for training this fine tuned model. | Yes |  |
| validation_file | string | The file identity (file-id) that is used to evaluate the fine tuned model during training. | No |  |

### Responses

**Status Code:** 201

**Description**: The fine tune has been successfully created. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJob](#finetuningjob) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/fine_tuning/jobs?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 201

```json
{
  "headers": {
    "location": "https://aoairesource.openai.azure.com/openai/fine_tuning/jobs/ft-72a2792ef7d24ba7b82c7fe4a37e379f"
  },
  "body": {
    "hyperparameters": {
      "n_epochs": -1
    },
    "integrations": [
      {
        "type": "wandb",
        "wandb": {
          "project": "custom-wandb-project",
          "tags": [
            "project:tag",
            "lineage"
          ]
        }
      }
    ],
    "method": {
      "type": "supervised"
    },
    "status": "pending",
    "model": "curie",
    "training_file": "file-181a1cbdcdcf4677ada87f63a0928099",
    "id": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "fine_tuning.job"
  }
}
```

## Fine-tuning - Get

```HTTP
GET {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}?api-version=2025-04-01-preview
```

Gets details for a single fine-tuning job specified by the given fine-tune-id.

The details contain the base model, training and validation files, hyper parameters, time stamps, status and events.

Events are created when the job status changes, e.g. running or complete, and when results are uploaded.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| fine-tuning-job-id | path | Yes | string | The identifier of the fine-tuning job. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJob](#finetuningjob) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "hyperparameters": {
      "n_epochs": -1
    },
    "integrations": [
      {
        "type": "wandb",
        "wandb": {
          "project": "custom-wandb-project",
          "tags": [
            "project:tag",
            "lineage"
          ]
        }
      }
    ],
    "method": {
      "type": "supervised"
    },
    "status": "succeeded",
    "model": "curie",
    "fine_tuned_model": "curie.ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "training_file": "file-181a1cbdcdcf4677ada87f63a0928099",
    "result_files": [
      "file-181a1cbdcdcf4677ada87f63a0928099"
    ],
    "finished_at": 1646127311,
    "trained_tokens": 2342,
    "id": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "fine_tuning.job"
  }
}
```

## Fine-tuning - Delete

```HTTP
DELETE {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}?api-version=2025-04-01-preview
```

Deletes the fine-tuning job specified by the given fine-tune-id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| fine-tuning-job-id | path | Yes | string | The identifier of the fine-tuning job. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 204

**Description**: The fine tune was successfully deleted. 

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
DELETE {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 204

```json
{
  "headers": {}
}
```

## Fine-tuning - Cancel

```HTTP
POST {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/cancel?api-version=2025-04-01-preview
```

Cancels the processing of the fine-tuning job specified by the given fine-tune-id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| fine-tuning-job-id | path | Yes | string | The identifier of the fine-tuning job. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The fine tune has been successfully canceled 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJob](#finetuningjob) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/cancel?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "hyperparameters": {
      "n_epochs": -1
    },
    "integrations": [
      {
        "type": "wandb",
        "wandb": {
          "project": "custom-wandb-project",
          "tags": [
            "project:tag",
            "lineage"
          ]
        }
      }
    ],
    "method": {
      "type": "supervised"
    },
    "status": "cancelled",
    "model": "curie",
    "training_file": "file-181a1cbdcdcf4677ada87f63a0928099",
    "finished_at": 1646127311,
    "id": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "fine_tuning.job"
  }
}
```

## Fine-tuning - Get checkpoints

```HTTP
GET {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/checkpoints?api-version=2025-04-01-preview
```

Gets the checkpoints for the fine-tuning job specified by the given fine-tune-id.

Checkpoints are created at the end of successful epochs during training.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| fine-tuning-job-id | path | Yes | string | The identifier of the fine-tuning job. |
| after | query | No | string | Identifier for the last checkpoint ID from the previous pagination request. |
| limit | query | No | integer | Number of checkpoints to retrieve. Defaults to 10. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJobCheckpointList](#finetuningjobcheckpointlist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/checkpoints?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "has_more": false,
    "data": [
      {
        "id": "ftckpt_qtZ5Gyk4BLq1SfLFWp3RtO3P",
        "created_at": 1646126127,
        "fine_tuned_model_checkpoint": "gpt-35-turbo-0613.ft-72a2792ef7d24ba7b82c7fe4a37e379f:ckpt-step-10",
        "step_number": 10,
        "metrics": {
          "step": 10,
          "train_loss": 0.478,
          "train_mean_token_accuracy": 0.924,
          "valid_loss": 10.112,
          "valid_mean_token_accuracy": 0.145,
          "full_valid_loss": 0.567,
          "full_valid_mean_token_accuracy": 0.944
        },
        "fine_tuning_job_id": "ftjob-72a2792ef7d24ba7b82c7fe4a37e379f",
        "object": "fine_tuning.job.checkpoint"
      },
      {
        "id": "ftckpt_frtXDR2453C4FG67t03MLPs5",
        "created_at": 1646126137,
        "fine_tuned_model_checkpoint": "gpt-35-turbo-0613.ft-72a2792ef7d24ba7b82c7fe4a37e379f:ckpt-step-20",
        "step_number": 20,
        "metrics": {
          "step": 20,
          "train_loss": 0.355,
          "train_mean_token_accuracy": 0.947,
          "valid_loss": 11.32,
          "valid_mean_token_accuracy": 0.122,
          "full_valid_loss": 0.317,
          "full_valid_mean_token_accuracy": 0.955
        },
        "fine_tuning_job_id": "ftjob-72a2792ef7d24ba7b82c7fe4a37e379f",
        "object": "fine_tuning.job.checkpoint"
      },
      {
        "id": "ftckpt_agLk6Gio560ORp14gl123fgd",
        "created_at": 1646126147,
        "fine_tuned_model_checkpoint": "gpt-35-turbo-0613.ft-72a2792ef7d24ba7b82c7fe4a37e379f:ckpt-step-30",
        "step_number": 30,
        "metrics": {
          "step": 30,
          "train_loss": 0.155,
          "train_mean_token_accuracy": 0.975,
          "valid_loss": 9.31,
          "valid_mean_token_accuracy": 0.092,
          "full_valid_loss": 0.114,
          "full_valid_mean_token_accuracy": 0.963
        },
        "fine_tuning_job_id": "ftjob-72a2792ef7d24ba7b82c7fe4a37e379f",
        "object": "fine_tuning.job.checkpoint"
      }
    ],
    "object": "list"
  }
}
```

## Fine-tuning - Get events

```HTTP
GET {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/events?api-version=2025-04-01-preview
```

Gets the events for the fine-tuning job specified by the given fine-tune-id.

Events are created when the job status changes, e.g. running or complete, and when results are uploaded.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| fine-tuning-job-id | path | Yes | string | The identifier of the fine-tuning job. |
| after | query | No | string | Identifier for the last event from the previous pagination request. |
| limit | query | No | integer | Number of events to retrieve. Defaults to 20. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJobEventList](#finetuningjobeventlist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/events?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "has_more": false,
    "data": [
      {
        "id": "ftevent-363dcd7cb4c74539bc53293c1dceef05",
        "created_at": 1646126127,
        "level": "info",
        "message": "Job enqueued. Waiting for jobs ahead to complete.",
        "type": "message",
        "object": "fine_tuning.job.event"
      },
      {
        "id": "ftevent-8c2a44999790437cb3230e543fa2cf0f",
        "created_at": 1646126169,
        "level": "info",
        "message": "Job started.",
        "type": "message",
        "object": "fine_tuning.job.event"
      },
      {
        "id": "ftevent-2d47d651d2f3484c8187c88c00078147",
        "created_at": 1646126192,
        "level": "info",
        "message": "Job succeeded.",
        "type": "message",
        "object": "fine_tuning.job.event"
      }
    ],
    "object": "list"
  }
}
```

## Fine-tuning - Pause

```HTTP
POST {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/pause?api-version=2025-04-01-preview
```

Pausing the processing of the fine-tuning job specified by the given fine-tune-id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| fine-tuning-job-id | path | Yes | string | The identifier of the fine-tuning job. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The fine tune has been successfully paused. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJob](#finetuningjob) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/pause?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "hyperparameters": {
      "n_epochs": -1
    },
    "integrations": [
      {
        "type": "wandb",
        "wandb": {
          "project": "custom-wandb-project",
          "tags": [
            "project:tag",
            "lineage"
          ]
        }
      }
    ],
    "method": {
      "type": "supervised"
    },
    "status": "paused",
    "model": "curie",
    "training_file": "file-181a1cbdcdcf4677ada87f63a0928099",
    "finished_at": 1646127311,
    "id": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "fine_tuning.job"
  }
}
```

## Fine-tuning - Resume

```HTTP
POST {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/resume?api-version=2025-04-01-preview
```

Resumes the processing of the fine-tuning job specified by the given fine-tune-id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| fine-tuning-job-id | path | Yes | string | The identifier of the fine-tuning job. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The fine tune has been successfully resumed. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [FineTuningJob](#finetuningjob) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/fine_tuning/jobs/{fine-tuning-job-id}/resume?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "hyperparameters": {
      "n_epochs": -1
    },
    "integrations": [
      {
        "type": "wandb",
        "wandb": {
          "project": "custom-wandb-project",
          "tags": [
            "project:tag",
            "lineage"
          ]
        }
      }
    ],
    "method": {
      "type": "supervised"
    },
    "status": "resuming",
    "model": "curie",
    "training_file": "file-181a1cbdcdcf4677ada87f63a0928099",
    "finished_at": 1646127311,
    "id": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "fine_tuning.job"
  }
}
```

## Ingestion jobs - List

```HTTP
GET {endpoint}/openai/ingestion/jobs?api-version=2025-04-01-preview
```

Lists the ingestion jobs.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |
| mgmt-user-token | header | No | string | The token used to access the workspace (needed only for user compute jobs). |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [IngestionJobList](#ingestionjoblist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/ingestion/jobs?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "value": [
      {
        "jobId": "usercompute-ingestion-job",
        "kind": "UserCompute",
        "workspaceId": "/subscriptions/f375b912-331c-4fc5-8e9f-2d7205e3e036/resourceGroups/adrama-copilot-demo/providers/Microsoft.MachineLearningServices/workspaces/adrama-rag-dev"
      },
      {
        "jobId": "syscompute-ingestion-job",
        "kind": "SystemCompute"
      }
    ]
  }
}
```

## Ingestion jobs - Create

```HTTP
PUT {endpoint}/openai/ingestion/jobs/{job-id}?api-version=2025-04-01-preview
```

Creates an ingestion job with the specified job id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |
| job-id | path | Yes | string | The id of the job that will be created. |
| mgmt-user-token | header | No | string | The token used to access the workspace (needed only for user compute jobs). |
| aml-user-token | header | No | string | The token used to access the resources within the job in the workspace (needed only for user compute jobs). |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| jobId | string |  | No |  |
| kind | [IngestionJobType](#ingestionjobtype) | The job type. | Yes |  |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [IngestionJob](#ingestionjob) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
PUT {endpoint}/openai/ingestion/jobs/{job-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {
    "operation-location": "https://aoairesource.openai.azure.com/openai/ingestion/jobs/ingestion-job/runs/72a2792ef7d24ba7b82c7fe4a37e379f?api-version=2025-04-01-preview"
  },
  "body": {
    "kind": "SystemCompute",
    "jobId": "ingestion-job",
    "searchServiceConnection": {
      "kind": "EndpointWithManagedIdentity",
      "endpoint": "https://aykame-dev-search.search.windows.net"
    },
    "datasource": {
      "kind": "Storage",
      "connection": {
        "kind": "EndpointWithManagedIdentity",
        "endpoint": "https://mystorage.blob.core.windows.net/",
        "resourceId": "/subscriptions/1234567-abcd-1234-5678-1234abcd/resourceGroups/my-resource/providers/Microsoft.Storage/storageAccounts/mystorage"
      },
      "containerName": "container",
      "chunking": {
        "maxChunkSizeInTokens": 2048
      },
      "embeddings": [
        {
          "connection": {
            "kind": "RelativeConnection"
          },
          "deploymentName": "Ada"
        }
      ]
    },
    "dataRefreshIntervalInHours": 24,
    "completionAction": "keepAllAssets"
  }
}
```




```HTTP
PUT {endpoint}/openai/ingestion/jobs/{job-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {
    "operation-location": "https://aoairesource.openai.azure.com/openai/ingestion/jobs/ingestion-job/runs/72a2792ef7d24ba7b82c7fe4a37e379f?api-version=2025-04-01-preview"
  },
  "body": {
    "kind": "UserCompute",
    "jobId": "ingestion-job",
    "workspaceId": "/subscriptions/f375b912-331c-4fc5-8e9f-2d7205e3e036/resourceGroups/adrama-copilot-demo/providers/Microsoft.MachineLearningServices/workspaces/adrama-rag-dev",
    "compute": {
      "kind": "ServerlessCompute"
    },
    "target": {
      "kind": "AzureAISearch",
      "connectionId": "/subscriptions/f375b912-331c-4fc5-8e9f-2d7205e3e036/resourceGroups/adrama-copilot-demo/providers/Microsoft.MachineLearningServices/workspaces/adrama-rag-dev/connections/search-connection"
    },
    "datasource": {
      "kind": "Dataset",
      "datasetId": "azureml://locations/centraluseuap/workspaces/83317fe6-efa6-4e4a-b020-d0edd11ec382/data/PlainText/versions/1",
      "datasetType": "uri_folder"
    }
  }
}
```

## Ingestion jobs - Get

```HTTP
GET {endpoint}/openai/ingestion/jobs/{job-id}?api-version=2025-04-01-preview
```

Gets the details of the specified job id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |
| job-id | path | Yes | string | The id of the job. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [IngestionJob](#ingestionjob) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/ingestion/jobs/{job-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "kind": "UserCompute",
    "jobId": "ingestion-job",
    "workspaceId": "/subscriptions/f375b912-331c-4fc5-8e9f-2d7205e3e036/resourceGroups/adrama-copilot-demo/providers/Microsoft.MachineLearningServices/workspaces/adrama-rag-dev",
    "compute": {
      "kind": "ServerlessCompute"
    },
    "target": {
      "kind": "AzureAISearch",
      "connectionId": "/subscriptions/f375b912-331c-4fc5-8e9f-2d7205e3e036/resourceGroups/adrama-copilot-demo/providers/Microsoft.MachineLearningServices/workspaces/adrama-rag-dev/connections/search-connection"
    },
    "datasource": {
      "kind": "Dataset",
      "datasetId": "azureml://locations/centraluseuap/workspaces/83317fe6-efa6-4e4a-b020-d0edd11ec382/data/PlainText/versions/1",
      "datasetType": "uri_folder"
    }
  }
}
```

## Ingestionjobruns - List

```HTTP
GET {endpoint}/openai/ingestion/jobs/{job-id}/runs?api-version=2025-04-01-preview
```

Lists the runs of the specified job id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |
| job-id | path | Yes | string | The id of the job. |
| mgmt-user-token | header | No | string | The token used to access the workspace (needed only for user compute jobs). |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [IngestionJobRunList](#ingestionjobrunlist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/ingestion/jobs/{job-id}/runs?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "value": [
      {
        "jobId": "ingestion-job",
        "runId": "f375b912-331c-4fc5-8e9f-2d7205e3e036",
        "status": "succeeded"
      },
      {
        "jobId": "ingestion-job",
        "runId": "07f2d192-add7-4202-a2e3-858c2577f4fd",
        "status": "failed"
      },
      {
        "jobId": "ingestion-job",
        "runId": "5ef7a436-1147-4cbb-82e0-3d502bcc6a7b",
        "status": "running"
      }
    ]
  }
}
```

## Ingestionjobruns - Get

```HTTP
GET {endpoint}/openai/ingestion/jobs/{job-id}/runs/{run-id}?api-version=2025-04-01-preview
```

Gets the details of the specified run id as part of the specified job id.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |
| job-id | path | Yes | string | The id of the job. |
| run-id | path | Yes | string | The id of the run. |
| mgmt-user-token | header | No | string | The token used to access the workspace (needed only for user compute jobs). |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [IngestionJobRun](#ingestionjobrun) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/ingestion/jobs/{job-id}/runs/{run-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "jobId": "ingestion-job",
    "runId": "5ef7a436-1147-4cbb-82e0-3d502bcc6a7b",
    "status": "running",
    "progress": {
      "stageProgress": [
        {
          "name": "Preprocessing",
          "totalItems": 14,
          "processedItems": 0,
          "state": "notRunning"
        },
        {
          "name": "Indexing",
          "state": "notRunning"
        }
      ]
    }
  }
}
```

## Models - List

```HTTP
GET {endpoint}/openai/models?api-version=2025-04-01-preview
```

Gets a list of all models that are accessible by the Azure OpenAI resource.

These include base models as well as all successfully completed fine-tuned models owned by the Azure OpenAI resource.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ModelList](#modellist) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/models?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "data": [
      {
        "status": "succeeded",
        "capabilities": {
          "fine_tune": true,
          "inference": true,
          "completion": true,
          "chat_completion": false,
          "embeddings": false
        },
        "lifecycle_status": `generally-available`,
        "deprecation": {
          "fine_tune": 1677662127,
          "inference": 1709284527
        },
        "id": "curie",
        "created_at": 1646126127,
        "object": "model"
      },
      {
        "status": "succeeded",
        "model": "curie",
        "fine_tune": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
        "capabilities": {
          "fine_tune": false,
          "inference": true,
          "completion": true,
          "chat_completion": false,
          "embeddings": false
        },
        "lifecycle_status": `generally-available`,
        "deprecation": {
          "inference": 1709284527
        },
        "id": "curie.ft-72a2792ef7d24ba7b82c7fe4a37e379f",
        "created_at": 1646126127,
        "object": "model"
      }
    ],
    "object": "list"
  }
}
```

## Models - Get

```HTTP
GET {endpoint}/openai/models/{model-id}?api-version=2025-04-01-preview
```

Gets details for the model specified by the given modelId.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| model-id | path | Yes | string | The identifier of the model. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [Model](#model) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
GET {endpoint}/openai/models/{model-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "status": "succeeded",
    "capabilities": {
      "fine_tune": true,
      "inference": true,
      "completion": true,
      "chat_completion": false,
      "embeddings": false
    },
    "lifecycle_status": `generally-available`,
    "deprecation": {
      "fine_tune": 1677662127,
      "inference": 1709284527
    },
    "id": "curie",
    "created_at": 1646126127,
    "object": "model"
  }
}
```




```HTTP
GET {endpoint}/openai/models/{model-id}?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "status": "succeeded",
    "model": "curie",
    "fine_tune": "ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "capabilities": {
      "fine_tune": false,
      "inference": true,
      "completion": true,
      "chat_completion": false,
      "embeddings": false
    },
    "lifecycle_status": `generally-available`,
    "deprecation": {
      "inference": 1709284527
    },
    "id": "curie.ft-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "model"
  }
}
```

## Upload file - Start

```HTTP
POST {endpoint}/openai/uploads?api-version=2025-04-01-preview
```

An intermediate Upload object is created, allowing you to add Parts to it. Currently, an Upload size can be a maximum of 9 GB in total and will expire two hours after being created.

After the Upload is completed a File object will be generated, containing all the uploaded parts. This File object can then be used across our platform just like any other file.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer |  | Yes |  |
| filename | string |  | Yes |  |
| mime_type | string |  | Yes |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |
### Request Body

**Content-Type**: text/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer |  | Yes |  |
| filename | string |  | Yes |  |
| mime_type | string |  | Yes |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |
### Request Body

**Content-Type**: application/*+json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer |  | Yes |  |
| filename | string |  | Yes |  |
| mime_type | string |  | Yes |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |

### Responses

**Status Code:** 200

**Description**: The upload has been successfully created. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [UploadResource](#uploadresource) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/uploads?api-version=2025-04-01-preview

{
 "purpose": "fine-tune",
 "filename": "training_data_v21.jsonl",
 "bytes": 2097152,
 "mime_type": "application/json"
}

```

**Responses**:
Status Code: 200

```json
{
  "headers": {
    "location": "https://aoairesource.openai.azure.com/openai/uploads/runs/fine-tune-72a2792ef7d24ba7b82c7fe4a37e379f"
  },
  "body": {
    "bytes": 2097152,
    "filename": "training_data_v21.jsonl",
    "purpose": "fine-tune",
    "status": "pending",
    "expires_at": 1646133327,
    "file": {
      "status": "pending",
      "bytes": 140,
      "purpose": "fine-tune",
      "filename": "puppy.jsonl",
      "id": "file-181a1cbdcdcf4677ada87f63a0928099",
      "created_at": 1646126127,
      "object": "file"
    },
    "id": "fine-tune-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "upload"
  }
}
```

## Upload file - Cancel

```HTTP
POST {endpoint}/openai/uploads/{upload-id}/cancel?api-version=2025-04-01-preview
```

Cancels the Upload, and will lead to all uploaded parts to be deleted asynchronously.

No Parts may be added after an Upload is cancelled.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| upload-id | path | Yes | string | The identifier of the upload. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [UploadResource](#uploadresource) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/uploads/{upload-id}/cancel?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "bytes": 2097152,
    "filename": "training_data_v21.jsonl",
    "purpose": "fine-tune",
    "status": "cancelled",
    "expires_at": 1646133327,
    "file": {
      "status": "pending",
      "bytes": 140,
      "purpose": "fine-tune",
      "filename": "puppy.jsonl",
      "id": "file-181a1cbdcdcf4677ada87f63a0928099",
      "created_at": 1646126127,
      "object": "file"
    },
    "id": "fine-tune-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "upload"
  }
}
```

## Upload file - Complete

```HTTP
POST {endpoint}/openai/uploads/{upload-id}/complete?api-version=2025-04-01-preview
```

This completes the Upload, and the returned Upload object contains a nested File object that is ready for use across the platform.

You can define the order of the Parts by providing an ordered list of Part IDs.

The total number of bytes uploaded must match the size originally specified when creating the Upload object.

After this operation no additional Parts can be added once the Upload is completed.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| upload-id | path | Yes | string | The identifier of the upload. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| md5 | string |  | No |  |
| part_ids | array |  | Yes |  |
### Request Body

**Content-Type**: text/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| md5 | string |  | No |  |
| part_ids | array |  | Yes |  |
### Request Body

**Content-Type**: application/*+json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| md5 | string |  | No |  |
| part_ids | array |  | Yes |  |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [UploadResource](#uploadresource) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/uploads/{upload-id}/complete?api-version=2025-04-01-preview

{
 "part_ids": [
  "LnmictL3p0u4LH/ko343nw==",
  "LmmictL3p0u4LH/ko343nw=="
 ]
}

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "bytes": 2097152,
    "filename": "training_data_v21.jsonl",
    "purpose": "fine-tune",
    "status": "completed",
    "expires_at": 1646133327,
    "file": {
      "status": "processed",
      "bytes": 140,
      "purpose": "fine-tune",
      "filename": "puppy.jsonl",
      "id": "file-181a1cbdcdcf4677ada87f63a0928099",
      "created_at": 1646126127,
      "object": "file"
    },
    "id": "fine-tune-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "upload"
  }
}
```

## Upload file - Part

```HTTP
POST {endpoint}/openai/uploads/{upload-id}/parts?api-version=2025-04-01-preview
```

Adds a Part to an Upload object, where each Part represents a segment of the file you're uploading.

Each Part can be up to the standard size limit for file upload, based on the File Purpose. You can continue adding Parts until reaching the Upload size limit of 9 GB.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| upload-id | path | Yes | string | The identifier of the upload. |
| api-version | query | Yes | string | The requested API version. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: multipart/form-data

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string |  | Yes |  |

### Responses

**Status Code:** 200

**Description**: Success 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [UploadPartResource](#uploadpartresource) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [ErrorResponse](#errorresponse) | |

### Examples




```HTTP
POST {endpoint}/openai/uploads/{upload-id}/parts?api-version=2025-04-01-preview

```

**Responses**:
Status Code: 200

```json
{
  "headers": {},
  "body": {
    "upload_id": "fine-tune-72a2792ef7d24ba7b82c7fe4a37e379f",
    "azure_block_id": "LnmictL3p0u4LH/ko343nw==",
    "id": "uplprt-72a2792ef7d24ba7b82c7fe4a37e379f",
    "created_at": 1646126127,
    "object": "upload.part"
  }
}
```

## Components

### AzureAISearchIndex

Azure AI Search Index.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionId | string | The id of the connection pointing to the Azure AI Search Index. | No |  |
| kind | [TargetType](#targettype) | The target type. | Yes |  |

### BaseConnection

A connection to a resource.


### Discriminator for BaseConnection

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [ConnectionType](#connectiontype) | The connection type. | Yes |  |

### Batch

Defines the values of a batch.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cancelled_at | integer | A timestamp when this batch was cancelled (in unix epochs). | No |  |
| cancelling_at | integer | A timestamp when this batch started cancelling (in unix epochs). | No |  |
| completed_at | integer | A timestamp when this batch was completed (in unix epochs). | No |  |
| completion_window | string | The time frame within which the batch should be processed. | No |  |
| created_at | integer | A timestamp when this batch was created (in unix epochs). | No |  |
| endpoint | string | The API endpoint used by the batch. | No |  |
| error_blob | string | The blob url containing outputs of requests with errors. | No |  |
| error_file_id | string | The ID of the file containing outputs of requests with errors. | No |  |
| errors | [BatchErrors](#batcherrors) | For batches that have failed, this will contain more information on the cause of the failures. | No |  |
| expired_at | integer | A timestamp when this batch expired (in unix epochs). | No |  |
| expires_at | integer | A timestamp when this batch will expire (in unix epochs). | No |  |
| failed_at | integer | A timestamp when this batch failed (in unix epochs). | No |  |
| finalizing_at | integer | A timestamp when this batch started finalizing (in unix epochs). | No |  |
| id | string | The identity of this item. | Yes |  |
| in_progress_at | integer | A timestamp when this batch started progressing (in unix epochs). | No |  |
| input_blob | string | The blob url containing the input file for the batch. | No |  |
| input_file_id | string | The ID of the input file for the batch. | Yes |  |
| metadata | object | A set of key-value pairs that can be attached to the batch. This can be useful for storing additional information about the batch in a structured format. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| output_blob | string | The blob url containing outputs of successfully executed requests. | No |  |
| output_file_id | string | The ID of the file containing outputs of successfully executed requests. | No |  |
| request_counts | [BatchRequestCounts](#batchrequestcounts) | The request counts for different statuses within the batch. | No |  |
| status | [BatchStatus](#batchstatus) | The status of a batch. | No |  |

### BatchCreateRequest

Defines the request to create a batch.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_window | string | The time frame within which the batch should be processed. | Yes |  |
| endpoint | string | The API endpoint used by the batch. | Yes |  |
| input_blob | string | The url of an Azure Storage blob to use as input for the batch. | No |  |
| input_file_id | string | The ID of the input file for the batch. | No |  |
| metadata | object | A set of key-value pairs that can be attached to the batch. This can be useful for storing additional information about the batch in a structured format. | No |  |
| output_expires_after | [FileExpiresAfter](#fileexpiresafter) | Defines an expiration for the file. | No |  |
| output_folder | [BatchOutputReference](#batchoutputreference) | The Azure Storage folder to store output. | No |  |

### BatchErrorData

Error information for a failure in batch.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | An error code identifying the error type. | No |  |
| line | string | The line number of the input file where the error occurred, if applicable (can be null). | No |  |
| message | string | A human-readable message providing more details about the error. | No |  |
| param | string | The name of the parameter that caused the error, if applicable (can be null). | No |  |

### BatchErrors

For batches that have failed, this will contain more information on the cause of the failures.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | [BatchErrorData](#batcherrordata) | Error information for a failure in batch. | No |  |
| object | string | The type of the errors object. This is always 'list'. | No |  |

### BatchRequestCounts

The request counts for different statuses within the batch.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completed | integer | The number of requests in the batch that have been completed successfully. | No |  |
| failed | integer | The number of requests in the batch that have failed. | No |  |
| total | integer | The total number of requests in the batch. | No |  |

### BatchOutputReference

The Azure Storage folder to store output.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delimiter | string | Optional. The delimiter used in the folder path, by default /. | No |  |
| url | string | The url of the Azure Storage folder where the batch output would be saved. | No |  |

### BatchStatus

The status of a batch.

| Property | Value |
|----------|-------|
| **Description** | The status of a batch. |
| **Type** | string |
| **Values** | `validating`<br>`failed`<br>`in_progress`<br>`finalizing`<br>`completed`<br>`expired`<br>`cancelling`<br>`cancelled` |

### BatchesList

Represents a list of batches.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of items. | No |  |
| first_id | string | The id of the first batch in the list of batches returned. | No |  |
| has_more | boolean | A value indicating whether the list contains more elements than returned. | No |  |
| last_id | string | The id of the last batch in the list of batches returned. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |

### Capabilities

The capabilities of a base or fine tune model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chat_completion | boolean | A value indicating whether a model supports chat completion. | Yes |  |
| completion | boolean | A value indicating whether a model supports completion. | Yes |  |
| embeddings | boolean | A value indicating whether a model supports embeddings. | Yes |  |
| fine_tune | boolean | A value indicating whether a model can be used for fine tuning. | Yes |  |
| inference | boolean | A value indicating whether a model can be deployed. | Yes |  |

### Choice

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| finish_reason | string | The reason the model stopped generating tokens. | No |  |
| index | integer | The index of the choice in the list of choices. | No |  |
| logprobs | object | Log probability information for the choice. | No |  |
| message | [ChoiceMessage](#choicemessage) |  | No |  |

### ChoiceMessage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string | The contents of the message. | No |  |
| role | string | The role of the entity that is creating the message. | No |  |
| tool_calls | array | A list of the relevant tool calls. | No |  |

### ChunkingSettings

Chunking settings

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| maxChunkSizeInTokens | integer |  | No |  |

### CompletionAction

The completion action.

| Property | Value |
|----------|-------|
| **Description** | The completion action. |
| **Type** | string |
| **Values** | `cleanUpTempAssets`<br>`keepAllAssets` |

### ComputeType

The compute type.

| Property | Value |
|----------|-------|
| **Description** | The compute type. |
| **Type** | string |
| **Values** | `ServerlessCompute`<br>`CustomCompute` |

### ConnectionStringConnection

Connection string connection.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionString | string | Connection string | No |  |
| kind | [ConnectionType](#connectiontype) | The connection type. | Yes |  |

### ConnectionType

The connection type.

| Property | Value |
|----------|-------|
| **Description** | The connection type. |
| **Type** | string |
| **Values** | `EndpointWithKey`<br>`ConnectionString`<br>`EndpointWithManagedIdentity`<br>`WorkspaceConnection`<br>`RelativeConnection` |

### CosmosDBIndex

CosmosDB Index.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| collectionName | string | The name of the cosmos DB collection. | No |  |
| connectionId | string | The id of the connection pointing to the cosmos DB. | No |  |
| databaseName | string | The name of the cosmos DB database. | No |  |
| kind | [TargetType](#targettype) | The target type. | Yes |  |

### CrawlingSettings

Crawling settings

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| maxCrawlDepth | integer |  | No |  |
| maxCrawlTimeInMins | integer |  | No |  |
| maxDownloadTimeInMins | integer |  | No |  |
| maxFileSize | integer |  | No |  |
| maxFiles | integer |  | No |  |
| maxRedirects | integer |  | No |  |

### CreateEvalCompletionsRunDataSource

A CompletionsRunDataSource object describing a model sampling configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | object |  | No |  |
| └─ item_reference | string | A reference to a variable in the 'item' namespace, e.g., 'item.name'. | No |  |
| └─ template | array | A list of chat messages forming the prompt or context. May include variable references to the 'item' namespace, e.g., {{item.name}}. | No |  |
| └─ type | enum | The type of input messages. Either `template` or `item_reference`.<br>Possible values: `template`, `item_reference` | No |  |
| model | string | The name of the model to use for generating completions (e.g., 'o3-mini'). | No |  |
| sampling_params | object |  | No |  |
| └─ max_completion_tokens | integer | The maximum number of tokens in the generated output. | No |  |
| └─ seed | integer | A seed value to initialize the randomness, during sampling. | No | 42 |
| └─ temperature | number | A higher temperature increases randomness in the outputs. | No | 1 |
| └─ top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No | 1 |
| source | object |  | Yes |  |
| └─ type | enum | The type of source. Can be one of `EvalJsonlFileContentSource`, `EvalJsonlFileIdSource`, or `EvalStoredCompletionsSource`.<br>Possible values: `EvalJsonlFileContentSource`, `EvalJsonlFileIdSource`, `EvalStoredCompletionsSource` | No |  |
| type | enum | The type of run data source. Always `completions`.<br>Possible values: `completions` | Yes |  |

### CreateEvalCustomDataSourceConfig

A CustomDataSourceConfig object that defines the schema for the data source used for the evaluation runs. This schema is used to define the shape of the data that will be: - Used to define your testing criteria and - What data is required when creating a run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_sample_schema | boolean | Whether the eval should expect you to populate the sample namespace (ie, by generating responses off of your data source) | No | False |
| item_schema | object | The json schema for each row in the data source. | Yes |  |
| type | enum | The type of data source. Always `custom`.<br>Possible values: `custom` | Yes |  |

### CreateEvalItem

A chat message that makes up the prompt or context. May include variable references to the "item" namespace, ie {{item.name}}.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | ['string', '[InputTextContent](#inputtextcontent)', 'object'] | Text inputs to the model - can contain template strings. | Yes |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or `developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | No |  |

### CreateEvalJsonlRunDataSource

A JsonlRunDataSource object with that specifies a JSONL file that matches the eval

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| source | object |  | Yes |  |
| └─ content | array | The content of the jsonl file. | No |  |
| └─ id | string | The identifier of the file. | No |  |
| └─ type | enum | The type of jsonl source. Always `file_id`.<br>Possible values: `file_id` | No |  |
| type | enum | The type of data source. Always `jsonl`.<br>Possible values: `jsonl` | Yes |  |

### CreateEvalLabelModelGrader

A LabelModelGrader object which uses a model to assign labels to each item in the evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array | A list of chat messages forming the prompt or context. May include variable references to the "item" namespace, ie {{item.name}}. | Yes |  |
| labels | array | The labels to classify to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### CreateEvalLogsDataSourceConfig

A data source config which specifies the metadata property of your stored completions query. This is usually metadata like `usecase=chatbot` or `prompt-version=v2`, etc.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Metadata filters for the logs data source. | No |  |
| type | enum | The type of data source. Always `logs`.<br>Possible values: `logs` | Yes |  |

### CreateEvalRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source_config | object | A CustomDataSourceConfig object that defines the schema for the data source used for the evaluation runs. This schema is used to define the shape of the data that will be: - Used to define your testing criteria and - What data is required when creating a run | Yes |  |
| └─ include_sample_schema | boolean | Whether the eval should expect you to populate the sample namespace (ie, by generating responses off of your data source) | No | False |
| └─ item_schema | object | The json schema for each row in the data source. | No |  |
| └─ metadata | object | Metadata filters for the logs data source. | No |  |
| └─ type | enum | The type of data source. Always `logs`.<br>Possible values: `logs` | No |  |
| metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| name | string | The name of the evaluation. | No |  |
| testing_criteria | array | A list of graders for all eval runs in this group. | Yes |  |

### CreateEvalRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source | object | A JsonlRunDataSource object with that specifies a JSONL file that matches the eval | Yes |  |
| └─ input_messages | object |  | No |  |
|   └─ item_reference | string | A reference to a variable in the 'item' namespace, e.g., 'item.name'. | No |  |
|   └─ template | array | A list of chat messages forming the prompt or context. May include variable references to the 'item' namespace, e.g., {{item.name}}. | No |  |
|   └─ type | enum | The type of input messages. Either `template` or `item_reference`.<br>Possible values: `template`, `item_reference` | No |  |
| └─ model | string | The name of the model to use for generating completions (e.g., 'o3-mini'). | No |  |
| └─ sampling_params | object |  | No |  |
|   └─ max_completion_tokens | integer | The maximum number of tokens in the generated output. | No |  |
|   └─ seed | integer | A seed value to initialize the randomness, during sampling. | No | 42 |
|   └─ temperature | number | A higher temperature increases randomness in the outputs. | No | 1 |
|   └─ top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No | 1 |
| └─ source | object |  | No |  |
|   └─ type | enum | The type of source. Can be one of `EvalJsonlFileContentSource`, `EvalJsonlFileIdSource`, or `EvalStoredCompletionsSource`.<br>Possible values: `EvalJsonlFileContentSource`, `EvalJsonlFileIdSource`, `EvalStoredCompletionsSource` | No |  |
| └─ type | enum | The type of run data source. Always `completions`.<br>Possible values: `completions` | No |  |
| metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| name | string | The name of the run. | No |  |

### CreateEvalStoredCompletionsRunDataSource

A StoredCompletionsRunDataSource configuration describing a set of filters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | integer | An optional Unix timestamp to filter items created after this time. | No |  |
| created_before | integer | An optional Unix timestamp to filter items created before this time. | No |  |
| limit | integer | An optional maximum number of items to return. | No |  |
| metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| model | string | An optional model to filter by (e.g., 'gpt-4o'). | No |  |
| type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### CustomCompute

Custom compute.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| computeId | string | Id of the custom compute | No |  |
| kind | [ComputeType](#computetype) | The compute type. | Yes |  |

### DeploymentConnection

Relative deployment connection.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [ConnectionType](#connectiontype) | The connection type. | Yes |  |

### Deprecation

Defines the dates of deprecation for the different use cases of a model.

Usually base models support 1 year of fine tuning after creation. Inference is typically supported 2 years after creation of base or fine tuned models. The exact dates are specified in the properties.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| fine_tune | integer | The end date of fine tune support of this model. Will be `null` for fine tune models. | No |  |
| inference | integer | The end date of inference support of this model. | Yes |  |

### DpoHyperparamsRequest

Hyperparameters for DPO method of fine-tuning

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we've found that larger batch sizes tend to work better for larger datasets.The default value as well as the maximum value for this property are specific to a base model. | No |  |
| beta | number | DPO beta value. | No |  |
| l2_multiplier | number | L2 regularization multiplier | No |  |
| learning_rate_multiplier | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. | No |  |
| n_epochs | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |

### DpoMethod

Request for DPO method fine-tuning

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| `dpo` | [DpoMethodConfigRequest](#dpomethodconfigrequest) | Configuration for `dpo` fine-tuning method. Includes DPO specific hyperparameters | Yes |  |
| type | [FineTuningMethodType](#finetuningmethodtype) |  | Yes |  |

### DpoMethodConfigRequest

Configuration for `dpo` fine-tuning method. Includes DPO specific hyperparameters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [DpoHyperparamsRequest](#dpohyperparamsrequest) | Hyperparameters for DPO method of fine-tuning | No |  |

### DpoMethodRequest

Request for DPO method fine-tuning

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| `dpo` | [DpoMethodConfigRequest](#dpomethodconfigrequest) | Configuration for `dpo` fine-tuning method. Includes DPO specific hyperparameters | Yes |  |
| type | [FineTuningMethodType](#finetuningmethodtype) |  | Yes |  |

### EndpointKeyConnection

Endpoint key connection.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| endpoint | string | Endpoint | No |  |
| key | string | Key | No |  |
| kind | [ConnectionType](#connectiontype) | The connection type. | Yes |  |

### EndpointMIConnection

Endpoint Managed Identity connection.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| endpoint | string | Endpoint | No |  |
| kind | [ConnectionType](#connectiontype) | The connection type. | Yes |  |
| resourceId | string | Resource Id | No |  |

### Error

Error content as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | [ErrorCode](#errorcode) | Error codes as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses). | Yes |  |
| details | array | The error details if available. | No |  |
| `innererror` | [InnerError](#innererror) | Inner error as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses). | No |  |
| message | string | The message of this error. | Yes |  |
| target | string | The location where the error happened if available. | No |  |

### ErrorCode

Error codes as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses).

| Property | Value |
|----------|-------|
| **Description** | Error codes as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses). |
| **Type** | string |
| **Values** | `conflict`<br>`invalidPayload`<br>`forbidden`<br>`notFound`<br>`unexpectedEntityState`<br>`itemDoesAlreadyExist`<br>`serviceUnavailable`<br>`internalFailure`<br>`quotaExceeded`<br>`jsonlValidationFailed`<br>`fileImportFailed`<br>`tooManyRequests`<br>`unauthorized`<br>`contentFilter` |

### ErrorResponse

Error response as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [Error](#error) | Error content as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses). | Yes |  |

### Eval

An Eval object with a data source config and testing criteria.
An Eval represents a task to be done for your LLM integration.
Like:
 - Improve the quality of my chatbot
 - See how well my chatbot handles customer support
 - Check if o3-mini is better at my use case than gpt-4o


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the eval was created. | Yes |  |
| data_source_config | object | A CustomDataSourceConfig which specifies the schema of your `item` and optionally `sample` namespaces. The response schema defines the shape of the data that will be: - Used to define your testing criteria and - What data is required when creating a run | Yes |  |
| └─ metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| └─ schema | object | The json schema for the run data source items. Learn how to build JSON schemas [here](https://json-schema.org/). | No |  |
| └─ type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | No |  |
| id | string | Unique identifier for the evaluation. | Yes |  |
| metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | Yes |  |
| name | string | The name of the evaluation. | Yes |  |
| object | enum | The object type.<br>Possible values: `eval` | Yes |  |
| testing_criteria | array | A list of testing criteria. | Yes |  |

### EvalApiError

An object representing an error response from the Eval API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The error code. | Yes |  |
| message | string | The error message. | Yes |  |

### EvalCustomDataSourceConfig

A CustomDataSourceConfig which specifies the schema of your `item` and optionally `sample` namespaces. The response schema defines the shape of the data that will be: - Used to define your testing criteria and - What data is required when creating a run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| schema | object | The json schema for the run data source items. Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `custom`.<br>Possible values: `custom` | Yes |  |

### EvalFileRunDataSource

A FileRunDataSource configuration with a file id

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The identifier of the file. | Yes |  |
| type | enum | The type of data source. Always `file`.<br>Possible values: `file` | Yes |  |

### EvalItem

A message input to the model with a role indicating instruction following hierarchy. Instructions given with the `developer` or `system` role take precedence over instructions given with the `user` role. Messages with the `assistant` role are presumed to have been generated by the model in previous interactions.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | object | A text input to the model. | Yes |  |
| └─ text | string | The text output from the model. | No |  |
| └─ type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | No |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or `developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | No |  |

### EvalJsonlFileContentSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content of the jsonl file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_content`.<br>Possible values: `file_content` | Yes |  |

### EvalJsonlFileIdSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The identifier of the file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_id`.<br>Possible values: `file_id` | Yes |  |

### EvalLabelModelGrader

A LabelModelGrader object which uses a model to assign labels to each item in the evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array |  | Yes |  |
| labels | array | The labels to assign to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### EvalList

An object representing a list of evals.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | An array of eval objects. | Yes |  |
| first_id | string | The identifier of the first eval in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more evals available. | Yes |  |
| last_id | string | The identifier of the last eval in the data array. | Yes |  |
| object | enum | The type of this object. It's always set to "list".<br>Possible values: `list` | Yes |  |

### EvalRun

A schema representing an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the evaluation run was created. | Yes |  |
| data_source | object | A JsonlRunDataSource object with that specifies a JSONL file that matches the eval | Yes |  |
| └─ input_messages | object |  | No |  |
|   └─ item_reference | string | A reference to a variable in the 'item' namespace, e.g., 'item.name'. | No |  |
|   └─ template | array | A list of chat messages forming the prompt or context. May include variable references to the 'item' namespace, e.g., {{item.name}}. | No |  |
|   └─ type | enum | The type of input messages. Either `template` or `item_reference`.<br>Possible values: `template`, `item_reference` | No |  |
| └─ model | string | The name of the model to use for generating completions (e.g., 'o3-mini'). | No |  |
| └─ sampling_params | object |  | No |  |
|   └─ max_completion_tokens | integer | The maximum number of tokens in the generated output. | No |  |
|   └─ seed | integer | A seed value to initialize the randomness, during sampling. | No | 42 |
|   └─ temperature | number | A higher temperature increases randomness in the outputs. | No | 1 |
|   └─ top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No | 1 |
| └─ source | object |  | No |  |
|   └─ type | enum | The type of source. Can be one of `EvalJsonlFileContentSource`, `EvalJsonlFileIdSource`, or `EvalStoredCompletionsSource`.<br>Possible values: `EvalJsonlFileContentSource`, `EvalJsonlFileIdSource`, `EvalStoredCompletionsSource` | No |  |
| └─ type | enum | The type of run data source. Always `completions`.<br>Possible values: `completions` | No |  |
| error | [EvalApiError](#evalapierror) | An object representing an error response from the Eval API. | Yes |  |
| eval_id | string | The identifier of the associated evaluation. | Yes |  |
| id | string | Unique identifier for the evaluation run. | Yes |  |
| metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | Yes |  |
| model | string | The model that is evaluated, if applicable. | Yes |  |
| name | string | The name of the evaluation run. | Yes |  |
| object | enum | The type of the object. Always "eval.run".<br>Possible values: `eval.run` | Yes |  |
| per_model_usage | array | Usage statistics for each model during the evaluation run. | Yes |  |
| per_testing_criteria_results | array | Results per testing criteria applied during the evaluation run. | Yes |  |
| report_url | string | The URL to the rendered evaluation run report on the UI dashboard. | Yes |  |
| result_counts | object | Counters summarizing the outcomes of the evaluation run. | Yes |  |
| └─ errored | integer | Number of output items that resulted in an error. | No |  |
| └─ failed | integer | Number of output items that failed to pass the evaluation. | No |  |
| └─ passed | integer | Number of output items that passed the evaluation. | No |  |
| └─ total | integer | Total number of executed output items. | No |  |
| status | string | The status of the evaluation run. | Yes |  |

### EvalRunList

An object representing a list of runs for an evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | An array of eval run objects. | Yes |  |
| first_id | string | The identifier of the first eval run in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more evals available. | Yes |  |
| last_id | string | The identifier of the last eval run in the data array. | Yes |  |
| object | enum | The type of this object. It's always set to "list".<br>Possible values: `list` | Yes |  |

### EvalRunOutputItem

A schema representing an evaluation run output item.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the evaluation run was created. | Yes |  |
| datasource_item | object | Details of the input data source item. | Yes |  |
| datasource_item_id | integer | The identifier for the data source item. | Yes |  |
| eval_id | string | The identifier of the evaluation group. | Yes |  |
| id | string | Unique identifier for the evaluation run output item. | Yes |  |
| object | enum | The type of the object. Always "eval.run.output_item".<br>Possible values: `eval.run.output_item` | Yes |  |
| results | array | A list of results from the evaluation run. | Yes |  |
| run_id | string | The identifier of the evaluation run associated with this output item. | Yes |  |
| sample | object | A sample containing the input and output of the evaluation run. | Yes |  |
| └─ error | [EvalApiError](#evalapierror) | An object representing an error response from the Eval API. | No |  |
| └─ finish_reason | string | The reason why the sample generation was finished. | No |  |
| └─ input | array | An array of input messages. | No |  |
| └─ max_completion_tokens | integer | The maximum number of tokens allowed for completion. | No |  |
| └─ model | string | The model used for generating the sample. | No |  |
| └─ output | array | An array of output messages. | No |  |
| └─ seed | integer | The seed used for generating the sample. | No |  |
| └─ temperature | number | The sampling temperature used. | No |  |
| └─ top_p | number | The top_p value used for sampling. | No |  |
| └─ usage | object | Token usage details for the sample. | No |  |
|   └─ cached_tokens | integer | The number of tokens retrieved from cache. | No |  |
|   └─ completion_tokens | integer | The number of completion tokens generated. | No |  |
|   └─ prompt_tokens | integer | The number of prompt tokens used. | No |  |
|   └─ total_tokens | integer | The total number of tokens used. | No |  |
| status | string | The status of the evaluation run. | Yes |  |

### EvalRunOutputItemList

An object representing a list of output items for an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | An array of eval run output item objects. | Yes |  |
| first_id | string | The identifier of the first eval run output item in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more eval run output items available. | Yes |  |
| last_id | string | The identifier of the last eval run output item in the data array. | Yes |  |
| object | enum | The type of this object. It's always set to "list".<br>Possible values: `list` | Yes |  |

### EvalScoreModelGrader

A ScoreModelGrader object that uses a model to assign a score to the input.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array | The input text. This may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | No |  |
| range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params | object | The sampling parameters for the model. | No |  |
| type | enum | The object type, which is always `score_model`.<br>Possible values: `score_model` | Yes |  |

### EvalStoredCompletionsDataSourceConfig

A StoredCompletionsDataSourceConfig which specifies the metadata property of your stored completions query. This is usually metadata like `usecase=chatbot` or `prompt-version=v2`, etc. The schema returned by this data source config is used to defined what variables are available in your evals. `item` and `sample` are both defined when using this data source config. 

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| schema | object | The json schema for the run data source items. Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### EvalStoredCompletionsSource

A StoredCompletionsRunDataSource configuration describing a set of filters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | integer | An optional Unix timestamp to filter items created after this time. | No |  |
| created_before | integer | An optional Unix timestamp to filter items created before this time. | No |  |
| limit | integer | An optional maximum number of items to return. | No |  |
| metadata | [Metadata](#metadata) | Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters. | No |  |
| model | string | An optional model to filter by (e.g., 'gpt-4o'). | No |  |
| type | enum | The type of source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### EvalStringCheckGrader

A StringCheckGrader object that performs a string comparison between input and reference using a specified operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The input text. This may include template strings. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | Yes |  |
| reference | string | The reference text. This may include template strings. | Yes |  |
| type | enum | The object type, which is always `string_check`.<br>Possible values: `string_check` | Yes |  |

### EvalTextSimilarityGrader

A TextSimilarityGrader object which grades text based on similarity metrics.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
| input | string | The text being graded. | Yes |  |
| name | string | The name of the grader. | No |  |
| pass_threshold | number | A float score where a value greater than or equal indicates a passing grade. | Yes |  |
| reference | string | The text being graded against. | Yes |  |
| type | enum | The type of grader.<br>Possible values: `text_similarity` | Yes |  |

### EventType

Defines the severity of a content filter result.

| Property | Value |
|----------|-------|
| **Description** | Defines the severity of a content filter result. |
| **Type** | string |
| **Values** | `message`<br>`metrics` |

### File

A file is a document usable for training and validation. It can also be a service generated document with result details.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer | The size of this file when available (can be null). File sizes larger than 2^53-1 aren't supported to ensure compatibility with JavaScript integers. | No |  |
| created_at | integer | A timestamp when this job or item was created (in unix epochs). | No |  |
| expires_at | integer | A unix timestamp (the number of seconds that have elapsed since January 1, 1970) when the file is expired. | No |  |
| filename | string | The name of the file. | Yes |  |
| id | string | The identity of this item. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |
| status | [FileState](#filestate) | The state of a file. | No |  |
| status_details | string | The error message with details in case processing of this file failed. Deprecated. | No |  |

### FileCreate

Defines a document to import from an external content url to be usable with Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_url | string | The url to download the document from (can be SAS url of a blob or any other external url accessible with a GET request). | Yes |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |

### FileDelete

Defines the response for File Delete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | A value indicating whether gets if the file was deleted. | Yes |  |
| id | string | The file-id that was deleted. | Yes |  |
| object | string | If the file was deleted. | Yes |  |

### FileDetails

A file detail is a document used by batch service to fetch file blob details.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filename | string | The name of the file. | Yes |  |
| id | string | The identity of this item. | No |  |
| path | string | The  the relative path to the file within the container. | No |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |
| storage_account_uri | string | The storage account url of this file. | No |  |
| storage_container_name | string | The Storage Container Name of this file blob. | No |  |

### FileExpiresAfter

Defines an expiration for the file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| anchor | [FileExpiryAnchor](#fileexpiryanchor) | Defines the anchor relative to what time the absolute expiration should be generated from. | No |  |
| seconds | integer | The relative expiration time in seconds. Range: [1209600 - 2592000]. | No |  |

### FileExpiryAnchor

Defines the anchor relative to what time the absolute expiration should be generated from.

| Property | Value |
|----------|-------|
| **Description** | Defines the anchor relative to what time the absolute expiration should be generated from. |
| **Type** | string |
| **Values** | `created_at` |

### FileImport

Defines a document to import from an external content url to be usable with Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_url | string | The url to download the document from (can be SAS url of a blob or any other external url accessible with a GET request). | Yes |  |
| expires_after | [FileExpiresAfter](#fileexpiresafter) | Defines an expiration for the file. | No |  |
| filename | string | The name of the [JSON Lines](https://jsonlines.readthedocs.io/en/latest/) file to be uploaded. If the `purpose` is set to "fine-tune", each line is a JSON record with "prompt" and "completion" fields representing your training examples. | Yes |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |

### FileList

Represents a list of files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of items. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |

### FileState

The state of a file.

| Property | Value |
|----------|-------|
| **Description** | The state of a file. |
| **Type** | string |
| **Values** | `uploaded`<br>`pending`<br>`running`<br>`processed`<br>`error`<br>`deleting`<br>`deleted` |

### FineTuneMethod


### Discriminator for FineTuneMethod

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [FineTuningMethodType](#finetuningmethodtype) |  | Yes |  |

### FineTuneMethodRequest


### Discriminator for FineTuneMethodRequest

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [FineTuningMethodType](#finetuningmethodtype) |  | Yes |  |

### FineTuningHyperParameters

The hyper parameter settings used in a fine tune job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | integer | The batch size to use for training. The batch size is the number of training examples used to train a single forward and backward pass. In general, we've found that larger batch sizes tend to work better for larger datasets. The default value as well as the maximum value for this property are specific to a base model. | No |  |
| learning_rate_multiplier | number | The learning rate multiplier to use for training. The fine-tuning learning rate is the original learning rate used for pre-training multiplied by this value. Larger learning rates tend to perform better with larger batch sizes. We recommend experimenting with values in the range 0.02 to 0.2 to see what produces the best results. | No |  |
| n_epochs | integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |

### FineTuningJob

Defines the values of a fine tune job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | A timestamp when this job or item was created (in unix epochs). | No |  |
| error | [FineTuningJobError](#finetuningjoberror) | For fine-tuning jobs that have failed, this will contain more information on the cause of the failure. | No |  |
| estimated_finish | integer | The Unix timestamp (in seconds) for when the fine-tuning job is estimated to finish. The value will be null if the fine-tuning job isn't running. | No |  |
| fine_tuned_model | string | The identifier (model-id) of the resulting fine tuned model. This property is only populated for successfully completed fine-tuning runs. Use this identifier to create a deployment for inferencing. | No |  |
| finished_at | integer | A timestamp when this job or item has finished successfully (in unix epochs). | No |  |
| hyperparameters | [FineTuningHyperParameters](#finetuninghyperparameters) | The hyper parameter settings used in a fine tune job. | No |  |
| id | string | The identity of this item. | No |  |
| integrations | array | A list of configurations for integrations supporting the fine-tuning job. There are many integrations planned, so make sure to check and act on the integration type. | No |  |
| method | object | Method used for supervised fine-tuning | No |  |
| └─ type | [FineTuningMethodType](#finetuningmethodtype) |  | No |  |
| model | string | The identifier (model-id) of the base model used for the fine-tune. | Yes |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| organisation_id | string | The organization id of this fine tune job. Unused on Azure OpenAI; compatibility for OpenAI only. | No |  |
| result_files | array | The result file identities (file-id) containing training and evaluation metrics in csv format. The file is only available for successfully completed fine-tuning runs. | No |  |
| seed | integer | The seed used for the fine-tuning job. | No |  |
| status | [FineTuningState](#finetuningstate) | The state of a fine-tuning object or fine tuning job. | No |  |
| suffix | string | The suffix used to identify the fine-tuned model. The suffix can contain up to 40 characters (a-z, A-Z, 0-9,- and _) that will be added to your fine-tuned model name. | No |  |
| trained_tokens | integer | The total number of billable tokens processed by this fine tuning job. | No |  |
| training_file | string | The file which is used for training. | Yes |  |
| validation_file | string | The file which is used to evaluate the fine tuned model during training. | No |  |

### FineTuningJobCheckpoint

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the checkpoint was created. | Yes |  |
| fine_tuned_model_checkpoint | string | The name of the fine-tuned checkpoint model that is created. | Yes |  |
| fine_tuning_job_id | string | The name of the fine-tuning job that this checkpoint was created from. | Yes |  |
| id | string | The identity of this checkpoint. | No |  |
| metrics | object | The metrics at the step number during the fine-tuning job. | Yes |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| step_number | integer | The step number that the checkpoint was created at. | Yes |  |

### FineTuningJobCheckpointList

Represents a list of checkpoints.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of items. | No |  |
| has_more | boolean | A value indicating whether the list contains more elements than returned. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |

### FineTuningJobCreation

Defines the values of a fine tune job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [FineTuningHyperParameters](#finetuninghyperparameters) | The hyper parameter settings used in a fine tune job. | No |  |
| integrations | array | A list of configurations for integrations supporting the fine-tuning job. There are many integrations planned, so make sure to check and act on the integration type. | No |  |
| method | object | Method used for supervised fine-tuning | No |  |
| └─ type | [FineTuningMethodType](#finetuningmethodtype) |  | No |  |
| model | string | The identifier (model-id) of the base model used for this fine-tune. | Yes |  |
| seed | integer | The seed used for the fine-tuning job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases. If a seed isn't specified, one will be generated for you. | No |  |
| suffix | string | The suffix used to identify the fine-tuned model. The suffix can contain up to 40 characters (a-z, A-Z, 0-9,- and _) that will be added to your fine-tuned model name. | No |  |
| training_file | string | The file identity (file-id) that is used for training this fine tuned model. | Yes |  |
| validation_file | string | The file identity (file-id) that is used to evaluate the fine tuned model during training. | No |  |

### FineTuningJobError

For fine-tuning jobs that have failed, this will contain more information on the cause of the failure.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The machine-readable error code. | No |  |
| message | string | The human-readable error message. | No |  |
| param | string | The parameter that was invalid, usually training_file or validation_file. This field will be null if the failure was not parameter-specific. | No |  |

### FineTuningJobEvent

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | A timestamp when this event was created (in unix epochs). | Yes |  |
| data |  | Machine readable data of this event. | No |  |
| id | string | The identity of this event. | No |  |
| level | [LogLevel](#loglevel) | The verbosity level of an event. | Yes |  |
| message | string | The message describing the event. This can be a change of state, e.g., enqueued, started, failed or completed, or other events like uploaded results. | Yes |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| type | [EventType](#eventtype) | Defines the severity of a content filter result. | Yes |  |

### FineTuningJobEventList

Represents a list of events.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of items. | No |  |
| has_more | boolean | A value indicating whether the list contains more elements than returned. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |

### FineTuningJobList

Represents a list of fine tunes.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of items. | No |  |
| has_more | boolean | A value indicating whether the list contains more elements than returned. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |

### FineTuningMethodType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `dpo`<br>`supervised` |

### FineTuningState

The state of a fine-tuning object or fine tuning job.

| Property | Value |
|----------|-------|
| **Description** | The state of a fine-tuning object or fine tuning job. |
| **Type** | string |
| **Values** | `created`<br>`pending`<br>`running`<br>`pausing`<br>`paused`<br>`resuming`<br>`succeeded`<br>`cancelled`<br>`failed` |

### FunctionCallFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | The arguments that the model expects you to pass to the function. | No |  |
| name | string | The name of the function. | No |  |

### FunctionDefinition

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| name | string | The name of the function to be called. | No |  |
| parameters |  | The parameters the functions accepts, described as a JSON Schema object. | No |  |

### GenericEmbeddingSettings

Connection Embedding Settings

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connection | [BaseConnection](#baseconnection) | A connection to a resource. | No |  |
| deploymentName | string |  | No |  |
| modelName | string |  | No |  |

### IngestionError

The details of the ingestion error

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| innerErrors | array |  | No |  |
| message | string |  | No |  |

### IngestionJob

Represents the details of a job.


### Discriminator for IngestionJob

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| jobId | string |  | No |  |
| kind | [IngestionJobType](#ingestionjobtype) | The job type. | Yes |  |

### IngestionJobList

Represents a list of ingestion jobs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page. | No |  |
| value | array | The list of items. | No |  |

### IngestionJobProgress

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| stageProgress | array |  | Yes |  |

### IngestionJobRun

The details of a job run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [IngestionError](#ingestionerror) | The details of the ingestion error | No |  |
| jobId | string |  | No |  |
| progress | [IngestionJobProgress](#ingestionjobprogress) |  | No |  |
| runId | string |  | No |  |
| status | [OperationState](#operationstate) | The state of a job or item. | No |  |
| warnings | array |  | No |  |

### IngestionJobRunList

Represents a list of ingestion job runs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| nextLink | string | The link to the next page. | No |  |
| value | array | The list of items. | No |  |

### IngestionJobStageProgress

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string |  | No |  |
| processedItems | integer |  | No |  |
| state | [OperationState](#operationstate) | The state of a job or item. | No |  |
| subStageProgress | array |  | No |  |
| totalItems | integer |  | No |  |

### IngestionJobSystemCompute

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completionAction | [CompletionAction](#completionaction) | The completion action. | No |  |
| dataRefreshIntervalInHours | integer |  | No |  |
| datasource | [SystemComputeDatasource](#systemcomputedatasource) |  | No |  |
| jobId | string |  | No |  |
| kind | [IngestionJobType](#ingestionjobtype) | The job type. | Yes |  |
| searchServiceConnection | [BaseConnection](#baseconnection) | A connection to a resource. | No |  |

### IngestionJobType

The job type.

| Property | Value |
|----------|-------|
| **Description** | The job type. |
| **Type** | string |
| **Values** | `SystemCompute`<br>`UserCompute` |

### IngestionJobUserCompute

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| compute | [JobCompute](#jobcompute) | The compute settings of the job. | No |  |
| dataRefreshIntervalInHours | integer |  | No |  |
| datasource | [UserComputeDatasource](#usercomputedatasource) |  | No |  |
| jobId | string |  | No |  |
| kind | [IngestionJobType](#ingestionjobtype) | The job type. | Yes |  |
| target | [TargetIndex](#targetindex) | Information about the index to be created. | No |  |
| workspaceId | string |  | No |  |

### InnerError

Inner error as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | [InnerErrorCode](#innererrorcode) | Inner error codes as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses). | No |  |
| `innererror` | [InnerError](#innererror) | Inner error as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses). | No |  |

### InnerErrorCode

Inner error codes as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses).

| Property | Value |
|----------|-------|
| **Description** | Inner error codes as defined in the [Microsoft REST guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#7102-error-condition-responses). |
| **Type** | string |
| **Values** | `invalidPayload` |

### InputMessage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string | The contents of the message. | No |  |
| id | string | The identity of message. | No |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| role | string | The role of the entity that is creating the message. | No |  |

### InputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### IntegrationTypes

List of the fine-tuning integrations that are available.

| Property | Value |
|----------|-------|
| **Description** | List of the fine-tuning integrations that are available. |
| **Type** | string |
| **Values** | `wandb` |

### JobCompute

The compute settings of the job.


### Discriminator for JobCompute

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [ComputeType](#computetype) | The compute type. | Yes |  |

### LifeCycleStatus

The life cycle status of a model.

Note: A model can be promoted from `preview` to `generally-available`, but never from `generally-available` to `preview`.

| Property | Value |
|----------|-------|
| **Description** | The life cycle status of a model. Note: A model can be promoted from `preview` to `generally-available`, but never from `generally-available` to `preview`. |
| **Type** | string |
| **Values** | `preview`<br>`generally-available`<br>`deprecating`<br>`deprecated` |

### LogLevel

The verbosity level of an event.

| Property | Value |
|----------|-------|
| **Description** | The verbosity level of an event. |
| **Type** | string |
| **Values** | `info`<br>`warning`<br>`error` |

### Logprob

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logprob | number | The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely. | No |  |
| token | string | The token. | No |  |

### Metadata

Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard. Keys are strings with a maximum length of 64 characters. Values are strings with a maximum length of 512 characters.

No properties defined for this component.


### Model

A model is either a base model or the result of a successful fine tune job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| capabilities | [Capabilities](#capabilities) | The capabilities of a base or fine tune model. | Yes |  |
| created_at | integer | A timestamp when this job or item was created (in unix epochs). | No |  |
| deprecation | [Deprecation](#deprecation) | Defines the dates of deprecation for the different use cases of a model. Usually base models support 1 year of fine tuning after creation Inference is typically supported 2 years after creation of base or fine tuned models. The exact dates are specified in the properties. | Yes |  |
| fine_tune | string | The fine tune job identity (fine-tune-id) if this is a fine tune model; otherwise `null`. | No |  |
| id | string | The identity of this item. | No |  |
| lifecycle_status | [LifeCycleStatus](#lifecyclestatus) | The life cycle status of a model. Note: A model can be promoted from "preview" to `generally-available`, but never from `generally-available` to "preview". | Yes |  |
| model | string | The base model identity (model-id) if this is a fine tune model; otherwise `null`. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| status | [FineTuningState](#finetuningstate) | The state of a fine-tuning object or fine tuning job. | No |  |

### ModelList

Represents a list of models.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of items. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |

### OperationState

The state of a job or item.

| Property | Value |
|----------|-------|
| **Description** | The state of a job or item. |
| **Type** | string |
| **Values** | `notRunning`<br>`running`<br>`succeeded`<br>`failed` |

### Order

Defines the purpose of a file.

| Property | Value |
|----------|-------|
| **Description** | Defines the purpose of a file. |
| **Type** | string |
| **Values** | `desc`<br>`asc` |

### OrderByOrder

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `asc`<br>`desc` |

### PineconeIndex

Pinecone Index.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionId | string | The id of the connection pointing to the pinecone. | No |  |
| kind | [TargetType](#targettype) | The target type. | Yes |  |

### Purpose

The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file.

| Property | Value |
|----------|-------|
| **Description** | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. |
| **Type** | string |
| **Values** | `fine-tune`<br>`fine-tune-results`<br>`assistants`<br>`assistants_output`<br>`batch`<br>`batch_output`<br>`evals`<br>`evals_output` |

### ServerlessCompute

Serverless compute.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| instanceCount | integer | The count of instances to run the job on. | No |  |
| kind | [ComputeType](#computetype) | The compute type. | Yes |  |
| sku | string | SKU Level | No |  |

### StoredCompletion

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| choices | array | A list of chat completion choices. Can be more than one if `n` is greater than 1. | No |  |
| created | integer | The Unix timestamp (in seconds) of when the chat completion was created. | No |  |
| frequency_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. | No |  |
| id | string | The identity of stored completion. | No |  |
| input_user | string | The input user for this request. | No |  |
| metadata | object | Arbitrary key-value pairs for additional information. | No |  |
| model | string | ID of the model to use. | No |  |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. | No |  |
| request_id | string | A unique identifier for the OpenAI API request. Please include this request ID when contacting support. | No |  |
| seed | integer | If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result. Determinism isn't guaranteed, and you should refer to the
`system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| service_tier | string | Specifies the latency tier to use for processing the request. | No |  |
| system_fingerprint | string | This fingerprint represents the backend configuration that the model runs with. Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism. | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. | No |  |
| tool_choice | string | Controls which (if any) tool is called by the model. | No |  |
| tools | array | A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both. | No |  |
| usage | [Usage](#usage) |  | No |  |

### StoredCompletionDelete

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | A value indicating whether gets if the stored completion was deleted. | No |  |
| id | string | The stored completion id that was deleted. | No |  |
| object | string | If the stored completion was deleted. | Yes |  |

### StoredCompletionList

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of retrieved objects. | No |  |
| first_id | string | The first id in the retrieved `list` | No |  |
| has_more | boolean | The `has_more` property is used for pagination to indicate there are additional results. | No |  |
| last_id | string | The last id in the retrieved `list` | No |  |
| object | string | The object type, which is always `list` | No |  |
| total | integer | Total number of items. | No |  |

### StoredCompletionMessages

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of retrieved objects. | No |  |
| first_id | string | The first id in the retrieved `list` | No |  |
| has_more | boolean | The `has_more` property is used for pagination to indicate there are additional results. | No |  |
| last_id | string | The last id in the retrieved `list` | No |  |
| object | string | The object type, which is always `list` | No |  |
| total | integer | Total number of items. | No |  |

### StoredCompletionResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| choices | array | A list of chat completion choices. Can be more than one if `n` is greater than 1. | No |  |
| created | integer | The Unix timestamp (in seconds) of when the chat completion was created. | No |  |
| frequency_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. | No |  |
| id | string | The identity of stored completion. | No |  |
| input_user | string | The input user for this request. | No |  |
| metadata | object | Arbitrary key-value pairs for additional information. | No |  |
| model | string | ID of the model to use. | No |  |
| object | string | The type of this object. | No |  |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. | No |  |
| request_id | string | A unique identifier for the OpenAI API request. Please include this request ID when contacting support. | No |  |
| seed | integer | If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed`and parameters should return the same result. Determinism isn't guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| service_tier | string | Specifies the latency tier to use for processing the request. | No |  |
| system_fingerprint | string | This fingerprint represents the backend configuration that the model runs with. Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism. | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. | No |  |
| tool_choice | string | Controls which (if any) tool is called by the model. | No |  |
| tools | array | A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both. | No |  |
| usage | [Usage](#usage) |  | No |  |

### SupervisedMethod

Method used for supervised fine-tuning

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [FineTuningMethodType](#finetuningmethodtype) |  | Yes |  |

### SupervisedMethodRequest

Method used for supervised fine-tuning

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [FineTuningMethodType](#finetuningmethodtype) |  | Yes |  |

### SystemComputeDatasource


### Discriminator for SystemComputeDatasource

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [SystemComputeDatasourceType](#systemcomputedatasourcetype) | The datasource type. | Yes |  |

### SystemComputeDatasourceType

The datasource type.

| Property | Value |
|----------|-------|
| **Description** | The datasource type. |
| **Type** | string |
| **Values** | `Storage`<br>`Urls` |

### SystemComputeStorage

Storage account

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking | [ChunkingSettings](#chunkingsettings) | Chunking settings | No |  |
| connection | [BaseConnection](#baseconnection) | A connection to a resource. | No |  |
| containerName | string | container name | No |  |
| embeddings | array |  | No |  |
| kind | [SystemComputeDatasourceType](#systemcomputedatasourcetype) | The datasource type. | Yes |  |

### SystemComputeUrl

Urls

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking | [ChunkingSettings](#chunkingsettings) | Chunking settings | No |  |
| connection | [BaseConnection](#baseconnection) | A connection to a resource. | No |  |
| containerName | string | container name | No |  |
| crawling | [CrawlingSettings](#crawlingsettings) | Crawling settings | No |  |
| embeddings | array |  | No |  |
| kind | [SystemComputeDatasourceType](#systemcomputedatasourcetype) | The datasource type. | Yes |  |
| urls | array |  | No |  |

### TargetIndex

Information about the index to be created.


### Discriminator for TargetIndex

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [TargetType](#targettype) | The target type. | Yes |  |

### TargetType

The target type.

| Property | Value |
|----------|-------|
| **Description** | The target type. |
| **Type** | string |
| **Values** | `AzureAISearch`<br>`CosmosDB`<br>`Pinecone` |

### Tool

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [FunctionDefinition](#functiondefinition) |  | No |  |
| type | string | The type of tool call. This is always going to be `function` for this type of tool call. | No |  |

### ToolCall

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [FunctionCallFunction](#functioncallfunction) |  | No |  |
| id | string | The ID of the tool call. | No |  |
| type | string | The type of tool call the output is required for. For now, this is always `function`. | No |  |

### TypeDiscriminator

Defines the type of an object.

| Property | Value |
|----------|-------|
| **Description** | Defines the type of an object. |
| **Type** | string |
| **Values** | `list`<br>`fine_tuning.job`<br>`file`<br>`fine_tuning.job.event`<br>`fine_tuning.job.checkpoint`<br>`model`<br>`upload`<br>`upload.part`<br>`batch`<br>`wandb` |

### UpdateStoredCompletionRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Arbitrary key-value pairs for additional information. | No |  |

### UploadFileCompleteBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| md5 | string |  | No |  |
| part_ids | array |  | Yes |  |

### UploadFileStartBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer |  | Yes |  |
| filename | string |  | Yes |  |
| mime_type | string |  | Yes |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | Yes |  |

### UploadPartResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| azure_block_id | string |  | No |  |
| created_at | integer | A timestamp when this job or item was created (in unix epochs). | No |  |
| id | string | The identity of this item. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| upload_id | string |  | No |  |

### UploadResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer |  | No |  |
| created_at | integer | A timestamp when this job or item was created (in unix epochs). | No |  |
| expires_at | integer |  | No |  |
| file | [File](#file) | A file is a document usable for training and validation. It can also be a service generated document with result details. | No |  |
| filename | string |  | No |  |
| id | string | The identity of this item. | No |  |
| object | [TypeDiscriminator](#typediscriminator) | Defines the type of an object. | No |  |
| purpose | [Purpose](#purpose) | The intended purpose of the uploaded documents. Use "fine-tune" for fine-tuning. This allows us to validate the format of the uploaded file. | No |  |
| status | [UploadStatus](#uploadstatus) |  | No |  |

### UploadStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `pending`<br>`expired`<br>`completed`<br>`cancelled` |

### Usage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_tokens | integer | Number of tokens in the generated completion. | No |  |
| prompt_tokens | integer | Number of tokens in the prompt. | No |  |
| total_tokens | integer | Total number of tokens used in the request (prompt + completion). | No |  |

### UserComputeDataset

Storage account

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking | [ChunkingSettings](#chunkingsettings) | Chunking settings | No |  |
| datasetId | string |  | No |  |
| datasetType | string |  | No |  |
| embeddings | array |  | No |  |
| kind | [UserComputeDatasourceType](#usercomputedatasourcetype) | The datasource type. | Yes |  |

### UserComputeDatasource


### Discriminator for UserComputeDatasource

This component uses the property `kind` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| kind | [UserComputeDatasourceType](#usercomputedatasourcetype) | The datasource type. | Yes |  |

### UserComputeDatasourceType

The datasource type.

| Property | Value |
|----------|-------|
| **Description** | The datasource type. |
| **Type** | string |
| **Values** | `Dataset`<br>`Urls` |

### UserComputeUrl

Urls

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking | [ChunkingSettings](#chunkingsettings) | Chunking settings | No |  |
| crawling | [CrawlingSettings](#crawlingsettings) | Crawling settings | No |  |
| embeddings | array |  | No |  |
| kind | [UserComputeDatasourceType](#usercomputedatasourcetype) | The datasource type. | Yes |  |
| urls | array |  | No |  |

### WandBIntegrationRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| entity | string |  | No |  |
| name | string |  | No |  |
| project | string |  | Yes |  |
| tags | array |  | No |  |

### WandBIntegrationRequestWrapper

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [IntegrationTypes](#integrationtypes) | List of fine-tuning integrations that are available. | Yes |  |
| wandb | [WandBIntegrationRequest](#wandbintegrationrequest) |  | Yes |  |

### WorkspaceConnection

AML Workspace connection.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionId | string | ConnectionId | No |  |
| kind | [ConnectionType](#connectiontype) | The connection type. | Yes |  |

### WorkspaceConnectionEmbeddingSettings

Connection id to the embedding model

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connectionId | string |  | No |  |
| deploymentName | string |  | No |  |
| modelName | string |  | No |  |

