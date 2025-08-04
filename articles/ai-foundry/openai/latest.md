---
title: Azure OpenAI in Azure AI Foundry Models v1 REST API reference
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's v1 REST API. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 08/04/2025
author: mrbullwinkle 
ms.author: mbullwin
recommendations: false
ms.custom:
  - ignite-2023
---

# Azure OpenAI in Azure AI Foundry Models v1 REST API reference

Only a subset of dataplane authoring features are currently supported with the v1 API. A subset of dataplane inference and dataplane authoring features are supported with the [v1 preview API](./reference-preview-latest.md).

## List evals

```HTTP
GET {endpoint}/openai/v1/evals?api-version=v1
```

List evaluations for a project.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| after | query | No | string | Identifier for the last eval from the previous pagination request. |
| limit | query | No | integer | A limit on the number of evals to be returned in a single pagination response. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for evals by timestamp. Use `asc` for ascending order or<br>`desc` for descending order. |
| order_by | query | No | string<br>Possible values: `created_at`, `updated_at` | Evals can be ordered by creation time or last updated time. Use<br>`created_at` for creation time or `updated_at` for last updated<br>time. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalList](#openaievallist) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Create eval

```HTTP
POST {endpoint}/openai/v1/evals?api-version=v1
```

Create the structure of an evaluation that can be used to test a model's performance.

An evaluation is a set of testing criteria and a datasource. After creating an evaluation, you can run it on different models and model parameters. We support several types of graders and datasources.

NOTE: This Azure OpenAI API is in preview and subject to change.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |

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
| data_source_config | object |  | Yes |  |
| └─ type | [OpenAI.EvalDataSourceConfigType](#openaievaldatasourceconfigtype) |  | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the evaluation. | No |  |
| statusCode | enum | <br>Possible values: `201` | Yes |  |
| testing_criteria | array | A list of graders for all eval runs in this group. Graders can reference variables in the data source using double curly braces notation, like `{{item.variable_name}}`. To reference the model's output, use the `sample` namespace (ie, `{{sample.output_text}}`). | Yes |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Eval](#openaieval) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Get eval

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}?api-version=v1
```

Retrieve an evaluation by its ID.
Retrieves an evaluation by its ID.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Eval](#openaieval) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Update eval

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}?api-version=v1
```


Update select, mutable properties of a specified evaluation.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |

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
| metadata | [OpenAI.MetadataPropertyForRequest](#openaimetadatapropertyforrequest) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string |  | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Eval](#openaieval) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Delete eval

```HTTP
DELETE {endpoint}/openai/v1/evals/{eval_id}?api-version=v1
```


Delete a specified evaluation.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Get eval runs

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs?api-version=v1
```


Retrieve a list of runs for a specified evaluation.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |
| after | query | No | string |  |
| limit | query | No | integer |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |
| status | query | No | string<br>Possible values: `queued`, `in_progress`, `completed`, `canceled`, `failed` |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRunList](#openaievalrunlist) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Create eval run

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}/runs?api-version=v1
```


Create a new evaluation run, beginning the grading process.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |

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
| data_source | object |  | Yes |  |
| └─ type | [OpenAI.EvalRunDataSourceType](#openaievalrundatasourcetype) |  | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the run. | No |  |

### Responses

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRun](#openaievalrun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Get eval run

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}?api-version=v1
```


Retrieve a specific evaluation run by its ID.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRun](#openaievalrun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Cancel eval run

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}?api-version=v1
```


Cancel a specific evaluation run by its ID.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRun](#openaievalrun) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Delete eval run

```HTTP
DELETE {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}?api-version=v1
```


Delete a specific evaluation run by its ID.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Get eval run output items

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items?api-version=v1
```


Get a list of output items for a specified evaluation run.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |
| after | query | No | string |  |
| limit | query | No | integer |  |
| status | query | No | string<br>Possible values: `fail`, `pass` |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRunOutputItemList](#openaievalrunoutputitemlist) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Get eval run output item

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items/{output_item_id}?api-version=v1
```


Retrieve a specific output item from an evaluation run by its ID.

NOTE: This Azure OpenAI API is in preview and subject to change.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| aoai-evals | header | Yes | string<br>Possible values: `preview` | Enables access to AOAI Evals, a preview feature.<br>This feature requires the 'aoai-evals' header to be set to 'preview'. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |
| output_item_id | path | Yes | string |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRunOutputItem](#openaievalrunoutputitem) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Create file

```HTTP
POST {endpoint}/openai/v1/files?api-version=v1
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

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
| expires_after | object |  | Yes |  |
| └─ anchor | [AzureFileExpiryAnchor](#azurefileexpiryanchor) |  | No |  |
| └─ seconds | integer |  | No |  |
| file | string |  | Yes |  |
| purpose | enum | The intended purpose of the uploaded file. One of: - `assistants`: Used in the Assistants API - `batch`: Used in the Batch API - `fine-tune`: Used for fine-tuning - `evals`: Used for eval data sets<br>Possible values: `assistants`, `batch`, `fine-tune`, `evals` | Yes |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIFile](#azureopenaifile) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example



```HTTP
POST {endpoint}/openai/v1/files?api-version=v1

```

## List files

```HTTP
GET {endpoint}/openai/v1/files?api-version=v1
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| purpose | query | No | string |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureListFilesResponse](#azurelistfilesresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Retrieve file

```HTTP
GET {endpoint}/openai/v1/files/{file_id}?api-version=v1
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| file_id | path | Yes | string | The ID of the file to use for this request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIFile](#azureopenaifile) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Delete file

```HTTP
DELETE {endpoint}/openai/v1/files/{file_id}?api-version=v1
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| file_id | path | Yes | string | The ID of the file to use for this request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteFileResponse](#openaideletefileresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Download file

```HTTP
GET {endpoint}/openai/v1/files/{file_id}/content?api-version=v1
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| file_id | path | Yes | string | The ID of the file to use for this request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/octet-stream | string | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Run grader

```HTTP
POST {endpoint}/openai/v1/fine_tuning/alpha/graders/run?api-version=v1
```

Run a grader.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

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
| grader | object | A StringCheckGrader object that performs a string comparison between input and reference using a specified operation. | Yes |  |
| └─ calculate_output | string | A formula to calculate the output based on grader results. | No |  |
| └─ evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | No |  |
| └─ graders | object |  | No |  |
| └─ image_tag | string | The image tag to use for the python script. | No |  |
| └─ input | array | The input text. This may include template strings. | No |  |
| └─ model | string | The model to use for the evaluation. | No |  |
| └─ name | string | The name of the grader. | No |  |
| └─ operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | No |  |
| └─ range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| └─ reference | string | The text being graded against. | No |  |
| └─ sampling_params |  | The sampling parameters for the model. | No |  |
| └─ source | string | The source code of the python script. | No |  |
| └─ type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | No |  |
| item |  | The dataset item provided to the grader. This will be used to populate<br>the `item` namespace.  | No |  |
| model_sample | string | The model sample to be evaluated. This value will be used to populate<br>the `sample` namespace. <br>The `output_json` variable will be populated if the model sample is a<br>valid JSON string. | Yes |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunGraderResponse](#openairungraderresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Validate grader

```HTTP
POST {endpoint}/openai/v1/fine_tuning/alpha/graders/validate?api-version=v1
```

Validate a grader.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

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
| grader | object | A StringCheckGrader object that performs a string comparison between input and reference using a specified operation. | Yes |  |
| └─ calculate_output | string | A formula to calculate the output based on grader results. | No |  |
| └─ evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | No |  |
| └─ graders | object |  | No |  |
| └─ image_tag | string | The image tag to use for the python script. | No |  |
| └─ input | array | The input text. This may include template strings. | No |  |
| └─ model | string | The model to use for the evaluation. | No |  |
| └─ name | string | The name of the grader. | No |  |
| └─ operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | No |  |
| └─ range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| └─ reference | string | The text being graded against. | No |  |
| └─ sampling_params |  | The sampling parameters for the model. | No |  |
| └─ source | string | The source code of the python script. | No |  |
| └─ type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ValidateGraderResponse](#openaivalidategraderresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Create fine-tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs?api-version=v1
```

Creates a fine-tuning job which begins the process of creating a new model from a given dataset.

Response includes details of the enqueued job including job status and the name of the fine-tuned models once complete.



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

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
| hyperparameters | object | The hyperparameters used for the fine-tuning job.<br>This value is now deprecated in favor of `method`, and should be passed in under the `method` parameter. | No |  |
| └─ batch_size | enum | <br>Possible values: `auto` | No |  |
| └─ learning_rate_multiplier | enum | <br>Possible values: `auto` | No |  |
| └─ n_epochs | enum | <br>Possible values: `auto` | No |  |
| integrations | array | A list of integrations to enable for your fine-tuning job. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string (see valid models below) | The name of the model to fine-tune.  | Yes |  |
| seed | integer | The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases.<br>If a seed is not specified, one will be generated for you. | No |  |
| suffix | string | A string of up to 64 characters that will be added to your fine-tuned model name.<br><br>For example, a `suffix` of "custom-model-name" would produce a model name like `ft:gpt-4o-mini:openai:custom-model-name:7p4lURel`. | No | None |
| training_file | string | The ID of an uploaded file that contains training data. Additionally, you must upload your file with the purpose `fine-tune`.<br><br>The contents of the file should differ depending on if the model uses the chat, completions format, or if the fine-tuning method uses the preference format.| Yes |  |
| validation_file | string | The ID of an uploaded file that contains validation data.<br><br>If you provide this file, the data is used to generate validation<br>metrics periodically during fine-tuning. These metrics can be viewed in<br>the fine-tuning results file.<br>The same data should not be present in both train and validation files.<br><br>Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`.| No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## List paginated fine-tuning jobs

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs?api-version=v1
```

List your organization's fine-tuning jobs

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| after | query | No | string | Identifier for the last job from the previous pagination request. |
| limit | query | No | integer | Number of fine-tuning jobs to retrieve. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListPaginatedFineTuningJobsResponse](#openailistpaginatedfinetuningjobsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Retrieve fine-tuning job

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}?api-version=v1
```

Get info about a fine-tuning job.



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Cancel fine-tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel?api-version=v1
```

Immediately cancel a fine-tune job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to cancel. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## List fine-tuning job checkpoints

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints?api-version=v1
```

List the checkpoints for a fine-tuning job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to get checkpoints for. |
| after | query | No | string | Identifier for the last checkpoint ID from the previous pagination request. |
| limit | query | No | integer | Number of checkpoints to retrieve. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningJobCheckpointsResponse](#openailistfinetuningjobcheckpointsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## List fine-tuning events

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/events?api-version=v1
```

Get status updates for a fine-tuning job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to get events for. |
| after | query | No | string | Identifier for the last event from the previous pagination request. |
| limit | query | No | integer | Number of events to retrieve. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningJobEventsResponse](#openailistfinetuningjobeventsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Pause fine-tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/pause?api-version=v1
```

Pause a fine-tune job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to pause. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Resume fine-tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/resume?api-version=v1
```

Resume a paused fine-tune job.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to resume. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## List models

```HTTP
GET {endpoint}/openai/v1/models?api-version=v1
```

Lists the currently available models, and provides basic information about each one such as the
owner and availability.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListModelsResponse](#openailistmodelsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Retrieve model

```HTTP
GET {endpoint}/openai/v1/models/{model}?api-version=v1
```

Retrieves a model instance, providing basic information about the model such as the owner and
permissioning.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| model | path | Yes | string | The ID of the model to use for this request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Model](#openaimodel) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Components

### AzureAIFoundryModelsApiVersion

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `v1`<br>`preview` |

### AzureCreateFileRequestMultiPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | object |  | Yes |  |
| └─ anchor | [AzureFileExpiryAnchor](#azurefileexpiryanchor) |  | No |  |
| └─ seconds | integer |  | No |  |
| file | string |  | Yes |  |
| purpose | enum | The intended purpose of the uploaded file. One of: - `assistants`: Used in the Assistants API - `batch`: Used in the Batch API - `fine-tune`: Used for fine-tuning - `evals`: Used for eval data sets<br>Possible values: `assistants`, `batch`, `fine-tune`, `evals` | Yes |  |

### AzureErrorResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | object | The error details. | No |  |
| └─ code | string | The distinct, machine-generated identifier for the error. | No |  |
| └─ inner_error |  |  | No |  |
| └─ message | string | A human-readable message associated with the error. | No |  |
| └─ param | string | If applicable, the request input parameter associated with the error | No |  |
| └─ type | enum | The object type, always 'error.'<br>Possible values: `error` | No |  |

### AzureEvalAPICompletionsSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| parallel_tool_calls | boolean |  | No |  |
| response_format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tools | array |  | No |  |

### AzureEvalAPIModelSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_tokens | integer | The maximum number of tokens in the generated output. | No |  |
| reasoning_effort | enum | Controls the level of reasoning effort applied during generation.<br>Possible values: `low`, `medium`, `high` | No |  |
| seed | integer | A seed value to initialize the randomness during sampling. | No |  |
| temperature | number | A higher temperature increases randomness in the outputs. | No |  |
| top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No |  |

### AzureEvalAPIResponseSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| parallel_tool_calls | boolean |  | No |  |
| response_format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tools | array |  | No |  |

### AzureFileExpiryAnchor

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `created_at` |

### AzureFineTuneReinforcementMethod

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | object | A StringCheckGrader object that performs a string comparison between input and reference using a specified operation. | Yes |  |
| └─ calculate_output | string | A formula to calculate the output based on grader results. | No |  |
| └─ evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | No |  |
| └─ graders | object |  | No |  |
| └─ input | array | The input text. This may include template strings. | No |  |
| └─ model | string | The model to use for the evaluation. | No |  |
| └─ name | string | The name of the grader. | No |  |
| └─ operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | No |  |
| └─ range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| └─ reference | string | The text being graded against. | No |  |
| └─ sampling_params |  | The sampling parameters for the model. | No |  |
| └─ type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | No |  |
| hyperparameters | [OpenAI.FineTuneReinforcementHyperparameters](#openaifinetunereinforcementhyperparameters) | The hyperparameters used for the reinforcement fine-tuning job. | No |  |
| response_format | object |  | No |  |
| └─ json_schema | object | JSON Schema for the response format | No |  |
| └─ type | enum | Type of response format<br>Possible values: `json_schema` | No |  |

### AzureListFilesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### AzureOpenAIFile

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer | The size of the file, in bytes. | Yes |  |
| created_at | integer | The Unix timestamp (in seconds) for when the file was created. | Yes |  |
| expires_at | integer | The Unix timestamp (in seconds) for when the file will expire. | No |  |
| filename | string | The name of the file. | Yes |  |
| id | string | The file identifier, which can be referenced in the API endpoints. | Yes |  |
| object | enum | The object type, which is always `file`.<br>Possible values: `file` | Yes |  |
| purpose | enum | The intended purpose of the file. Supported values are `assistants`, `assistants_output`, `batch`, `batch_output`, `fine-tune` and `fine-tune-results`.<br>Possible values: `assistants`, `assistants_output`, `batch`, `batch_output`, `fine-tune`, `fine-tune-results`, `evals` | Yes |  |
| status | enum | <br>Possible values: `uploaded`, `pending`, `running`, `processed`, `error`, `deleting`, `deleted` | Yes |  |
| status_details | string | Deprecated. For details on why a fine-tuning training file failed validation, see the `error` field on `fine_tuning.job`. | No |  |

### OpenAI.ApproximateLocation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| city | string |  | No |  |
| country | string |  | No |  |
| region | string |  | No |  |
| timezone | string |  | No |  |
| type | enum | <br>Possible values: `approximate` | Yes |  |

### OpenAI.ChatCompletionTool

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.FunctionObject](#openaifunctionobject) |  | Yes |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | Yes |  |

### OpenAI.CodeInterpreterTool

A tool that runs Python code to help generate a response to a prompt.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container | object | Configuration for a code interpreter container. Optionally specify the IDs<br>of the files to run the code on. | Yes |  |
| └─ file_ids | array | An optional list of uploaded files to make available to your code. | No |  |
| └─ type | enum | Always `auto`.<br>Possible values: `auto` | No |  |
| type | enum | The type of the code interpreter tool. Always `code_interpreter`.<br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.CodeInterpreterToolAuto

Configuration for a code interpreter container. Optionally specify the IDs
of the files to run the code on.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_ids | array | An optional list of uploaded files to make available to your code. | No |  |
| type | enum | Always `auto`.<br>Possible values: `auto` | Yes |  |

### OpenAI.ComparisonFilter

A filter used to compare a specified attribute key to a given value using a defined comparison operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| key | string | The key to compare against the value. | Yes |  |
| type | enum | Specifies the comparison operator: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`.<br>- `eq`: equals<br>- `ne`: not equal<br>- `gt`: greater than<br>- `gte`: greater than or equal<br>- `lt`: less than<br>- `lte`: less than or equal<br>Possible values: `eq`, `ne`, `gt`, `gte`, `lt`, `lte` | Yes |  |
| value | string or number or boolean |  | Yes |  |

### OpenAI.CompoundFilter

Combine multiple filters using `and` or `or`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | array | Array of filters to combine. Items can be `ComparisonFilter` or `CompoundFilter`. | Yes |  |
| type | enum | Type of operation: `and` or `or`.<br>Possible values: `and`, `or` | Yes |  |

### OpenAI.ComputerUsePreviewTool

A tool that controls a virtual computer. 

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| display_height | integer | The height of the computer display. | Yes |  |
| display_width | integer | The width of the computer display. | Yes |  |
| environment | enum | The type of computer environment to control.<br>Possible values: `windows`, `mac`, `linux`, `ubuntu`, `browser` | Yes |  |
| type | enum | The type of the computer use tool. Always `computer_use_preview`.<br>Possible values: `computer_use_preview` | Yes |  |

### OpenAI.CreateEvalItem

A chat message that makes up the prompt or context. May include variable references to the `item` namespace, ie {{item.name}}.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or [OpenAI.EvalItemContent](#openaievalitemcontent) | Text inputs to the model - can contain template strings. | Yes |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or<br>`developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | No |  |

### OpenAI.CreateEvalRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source | object |  | Yes |  |
| └─ type | [OpenAI.EvalRunDataSourceType](#openaievalrundatasourcetype) |  | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the run. | No |  |

### OpenAI.CreateFineTuningJobRequest


**Valid models:**

```
babbage-002
davinci-002
gpt-3.5-turbo
gpt-4o-mini
```

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | object | The hyperparameters used for the fine-tuning job.<br>This value is now deprecated in favor of `method`, and should be passed in under the `method` parameter. | No |  |
| └─ batch_size | enum | <br>Possible values: `auto` | No |  |
| └─ learning_rate_multiplier | enum | <br>Possible values: `auto` | No |  |
| └─ n_epochs | enum | <br>Possible values: `auto` | No |  |
| integrations | array | A list of integrations to enable for your fine-tuning job. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string (see valid models below) | The name of the model to fine-tune.  | Yes |  |
| seed | integer | The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases.<br>If a seed is not specified, one will be generated for you. | No |  |
| suffix | string | A string of up to 64 characters that will be added to your fine-tuned model name.<br><br>For example, a `suffix` of "custom-model-name" would produce a model name like `ft:gpt-4o-mini:openai:custom-model-name:7p4lURel`. | No | None |
| training_file | string | The ID of an uploaded file that contains training data. Additionally, you must upload your file with the purpose `fine-tune`.<br><br>The contents of the file should differ depending on if the model uses the chat, completions format, or if the fine-tuning method uses the preference format.| Yes |  |
| validation_file | string | The ID of an uploaded file that contains validation data.<br><br>If you provide this file, the data is used to generate validation<br>metrics periodically during fine-tuning. These metrics can be viewed in<br>the fine-tuning results file.<br>The same data should not be present in both train and validation files.<br><br>Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`.| No |  |

### OpenAI.CreateFineTuningJobRequestIntegration


### Discriminator for OpenAI.CreateFineTuningJobRequestIntegration

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `wandb` | [OpenAI.CreateFineTuningJobRequestWandbIntegration](#openaicreatefinetuningjobrequestwandbintegration) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | string (see valid models below) |  | Yes |  |

### OpenAI.CreateFineTuningJobRequestWandbIntegration

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `wandb` | Yes |  |
| wandb | object |  | Yes |  |
| └─ entity | string |  | No |  |
| └─ name | string |  | No |  |
| └─ project | string |  | No |  |
| └─ tags | array |  | No |  |

### OpenAI.DeleteFileResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `file` | Yes |  |

### OpenAI.Eval

An Eval object with a data source config and testing criteria.
An Eval represents a task to be done for your LLM integration.
Like:
- Improve the quality of my chatbot
- See how well my chatbot handles customer support
- Check if o4-mini is better at my usecase than gpt-4o

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the eval was created. | Yes |  |
| data_source_config | object |  | Yes |  |
| └─ type | [OpenAI.EvalDataSourceConfigType](#openaievaldatasourceconfigtype) |  | No |  |
| id | string | Unique identifier for the evaluation. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| name | string | The name of the evaluation. | Yes |  |
| object | enum | The object type.<br>Possible values: `eval` | Yes |  |
| testing_criteria | array | A list of testing criteria. | Yes | None |

### OpenAI.EvalApiError

An object representing an error response from the Eval API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The error code. | Yes |  |
| message | string | The error message. | Yes |  |

### OpenAI.EvalCompletionsRunDataSourceParams

A CompletionsRunDataSource object describing a model sampling configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | object |  | No |  |
| └─ item_reference | string | A reference to a variable in the `item` namespace. Ie, "item.input_trajectory" | No |  |
| └─ template | array | A list of chat messages forming the prompt or context. May include variable references to the `item` namespace, ie {{item.name}}. | No |  |
| └─ type | enum | The type of input messages. Always `item_reference`.<br>Possible values: `item_reference` | No |  |
| model | string | The name of the model to use for generating completions (e.g. "o3-mini"). | No |  |
| sampling_params | [AzureEvalAPICompletionsSamplingParams](#azureevalapicompletionssamplingparams) |  | No |  |
| source | object |  | Yes |  |
| └─ content | array | The content of the jsonl file. | No |  |
| └─ created_after | integer | An optional Unix timestamp to filter items created after this time. | No |  |
| └─ created_before | integer | An optional Unix timestamp to filter items created before this time. | No |  |
| └─ id | string | The identifier of the file. | No |  |
| └─ limit | integer | An optional maximum number of items to return. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | An optional model to filter by (e.g., 'gpt-4o'). | No |  |
| └─ type | enum | The type of source. Always `stored_completions`.<br>Possible values: `stored_completions` | No |  |
| type | enum | The type of run data source. Always `completions`.<br>Possible values: `completions` | Yes |  |

### OpenAI.EvalCustomDataSourceConfigParams

A CustomDataSourceConfig object that defines the schema for the data source used for the evaluation runs.
This schema is used to define the shape of the data that will be:
- Used to define your testing criteria and
- What data is required when creating a run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_sample_schema | boolean | Whether the eval should expect you to populate the sample namespace (ie, by generating responses off of your data source) | No | False |
| item_schema | object | The json schema for each row in the data source. | Yes |  |
| type | enum | The type of data source. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.EvalCustomDataSourceConfigResource

A CustomDataSourceConfig which specifies the schema of your `item` and optionally `sample` namespaces.
The response schema defines the shape of the data that will be:
- Used to define your testing criteria and
- What data is required when creating a run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| schema | object | The json schema for the run data source items.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.EvalDataSourceConfigParams


### Discriminator for OpenAI.EvalDataSourceConfigParams

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `custom` | [OpenAI.EvalCustomDataSourceConfigParams](#openaievalcustomdatasourceconfigparams) |
| `logs` | [OpenAI.EvalLogsDataSourceConfigParams](#openaievallogsdatasourceconfigparams) |
| `stored_completions` | [OpenAI.EvalStoredCompletionsDataSourceConfigParams](#openaievalstoredcompletionsdatasourceconfigparams) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalDataSourceConfigType](#openaievaldatasourceconfigtype) |  | Yes |  |

### OpenAI.EvalDataSourceConfigResource


### Discriminator for OpenAI.EvalDataSourceConfigResource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `custom` | [OpenAI.EvalCustomDataSourceConfigResource](#openaievalcustomdatasourceconfigresource) |
| `stored_completions` | [OpenAI.EvalStoredCompletionsDataSourceConfigResource](#openaievalstoredcompletionsdatasourceconfigresource) |
| `logs` | [OpenAI.EvalLogsDataSourceConfigResource](#openaievallogsdatasourceconfigresource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalDataSourceConfigType](#openaievaldatasourceconfigtype) |  | Yes |  |

### OpenAI.EvalDataSourceConfigType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `custom`<br>`logs`<br>`stored_completions` |

### OpenAI.EvalGraderLabelModelParams

A LabelModelGrader object which uses a model to assign labels to each item
in the evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array | A list of chat messages forming the prompt or context. May include variable references to the `item` namespace, ie {{item.name}}. | Yes |  |
| labels | array | The labels to classify to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### OpenAI.EvalGraderLabelModelResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array |  | Yes |  |
| labels | array | The labels to assign to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### OpenAI.EvalGraderParams


### Discriminator for OpenAI.EvalGraderParams

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `label_model` | [OpenAI.EvalGraderLabelModelParams](#openaievalgraderlabelmodelparams) |
| `string_check` | [OpenAI.EvalGraderStringCheckParams](#openaievalgraderstringcheckparams) |
| `text_similarity` | [OpenAI.EvalGraderTextSimilarityParams](#openaievalgradertextsimilarityparams) |
| `python` | [OpenAI.EvalGraderPythonParams](#openaievalgraderpythonparams) |
| `score_model` | [OpenAI.EvalGraderScoreModelParams](#openaievalgraderscoremodelparams) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.GraderType](#openaigradertype) |  | Yes |  |

### OpenAI.EvalGraderPythonParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_tag | string | The image tag to use for the python script. | No |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | No |  |
| source | string | The source code of the python script. | Yes |  |
| type | enum | The object type, which is always `python`.<br>Possible values: `python` | Yes |  |

### OpenAI.EvalGraderPythonResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_tag | string | The image tag to use for the python script. | No |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | No |  |
| source | string | The source code of the python script. | Yes |  |
| type | enum | The object type, which is always `python`.<br>Possible values: `python` | Yes |  |

### OpenAI.EvalGraderResource


### Discriminator for OpenAI.EvalGraderResource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `label_model` | [OpenAI.EvalGraderLabelModelResource](#openaievalgraderlabelmodelresource) |
| `text_similarity` | [OpenAI.EvalGraderTextSimilarityResource](#openaievalgradertextsimilarityresource) |
| `python` | [OpenAI.EvalGraderPythonResource](#openaievalgraderpythonresource) |
| `score_model` | [OpenAI.EvalGraderScoreModelResource](#openaievalgraderscoremodelresource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.GraderType](#openaigradertype) |  | Yes |  |

### OpenAI.EvalGraderScoreModelParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array | The input text. This may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | No |  |
| range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params |  | The sampling parameters for the model. | No |  |
| type | enum | The object type, which is always `score_model`.<br>Possible values: `score_model` | Yes |  |

### OpenAI.EvalGraderScoreModelResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array | The input text. This may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | No |  |
| range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params |  | The sampling parameters for the model. | No |  |
| type | enum | The object type, which is always `score_model`.<br>Possible values: `score_model` | Yes |  |

### OpenAI.EvalGraderStringCheckParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The input text. This may include template strings. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | Yes |  |
| reference | string | The reference text. This may include template strings. | Yes |  |
| type | enum | The object type, which is always `string_check`.<br>Possible values: `string_check` | Yes |  |

### OpenAI.EvalGraderTextSimilarityParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
| input | string | The text being graded. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | Yes |  |
| reference | string | The text being graded against. | Yes |  |
| type | enum | The type of grader.<br>Possible values: `text_similarity` | Yes |  |

### OpenAI.EvalGraderTextSimilarityResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
| input | string | The text being graded. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | Yes |  |
| reference | string | The text being graded against. | Yes |  |
| type | enum | The type of grader.<br>Possible values: `text_similarity` | Yes |  |

### OpenAI.EvalItem

A message input to the model with a role indicating instruction following
hierarchy. Instructions given with the `developer` or `system` role take
precedence over instructions given with the `user` role. Messages with the
`assistant` role are presumed to have been generated by the model in previous
interactions.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | object |  | Yes |  |
| └─ type | [OpenAI.EvalItemContentType](#openaievalitemcontenttype) |  | No |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or<br>`developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | No |  |

### OpenAI.EvalItemContent


### Discriminator for OpenAI.EvalItemContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `input_text` | [OpenAI.EvalItemContentInputText](#openaievalitemcontentinputtext) |
| `output_text` | [OpenAI.EvalItemContentOutputText](#openaievalitemcontentoutputtext) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalItemContentType](#openaievalitemcontenttype) |  | Yes |  |

### OpenAI.EvalItemContentInputText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `input_text` | Yes |  |

### OpenAI.EvalItemContentOutputText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `output_text` | Yes |  |

### OpenAI.EvalItemContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`output_text` |

### OpenAI.EvalJsonlRunDataSourceParams

A JsonlRunDataSource object with that specifies a JSONL file that matches the eval

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| source | object |  | Yes |  |
| └─ content | array | The content of the jsonl file. | No |  |
| └─ id | string | The identifier of the file. | No |  |
| └─ type | enum | The type of jsonl source. Always `file_id`.<br>Possible values: `file_id` | No |  |
| type | enum | The type of data source. Always `jsonl`.<br>Possible values: `jsonl` | Yes |  |

### OpenAI.EvalList

An object representing a list of evals.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | An array of eval objects. | Yes |  |
| first_id | string | The identifier of the first eval in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more evals available. | Yes |  |
| last_id | string | The identifier of the last eval in the data array. | Yes |  |
| object | enum | The type of this object. It is always set to "list".<br>Possible values: `list` | Yes |  |

### OpenAI.EvalLogsDataSourceConfigParams

A data source config which specifies the metadata property of your logs query.
This is usually metadata like `usecase=chatbot` or `prompt-version=v2`, etc.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| type | enum | The type of data source. Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.EvalLogsDataSourceConfigResource

A LogsDataSourceConfig which specifies the metadata property of your logs query.
This is usually metadata like `usecase=chatbot` or `prompt-version=v2`, etc.
The schema returned by this data source config is used to defined what variables are available in your evals.
`item` and `sample` are both defined when using this data source config.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| schema | object | The json schema for the run data source items.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.EvalResponsesRunDataSourceParams

A ResponsesRunDataSource object describing a model sampling configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | object |  | No |  |
| └─ item_reference | string | A reference to a variable in the `item` namespace. Ie, "item.name" | No |  |
| └─ template | array | A list of chat messages forming the prompt or context. May include variable references to the `item` namespace, ie {{item.name}}. | No |  |
| └─ type | enum | The type of input messages. Always `item_reference`.<br>Possible values: `item_reference` | No |  |
| model | string | The name of the model to use for generating completions (e.g. "o3-mini"). | No |  |
| sampling_params | [AzureEvalAPIResponseSamplingParams](#azureevalapiresponsesamplingparams) |  | No |  |
| source | object |  | Yes |  |
| └─ content | array | The content of the jsonl file. | No |  |
| └─ created_after | integer | Only include items created after this timestamp (inclusive). This is a query parameter used to select responses. | No |  |
| └─ created_before | integer | Only include items created before this timestamp (inclusive). This is a query parameter used to select responses. | No |  |
| └─ id | string | The identifier of the file. | No |  |
| └─ instructions_search | string | Optional string to search the 'instructions' field. This is a query parameter used to select responses. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ model | string | The name of the model to find responses for. This is a query parameter used to select responses. | No |  |
| └─ reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Optional reasoning effort parameter. This is a query parameter used to select responses. | No |  |
| └─ temperature | number | Sampling temperature. This is a query parameter used to select responses. | No |  |
| └─ tools | array | List of tool names. This is a query parameter used to select responses. | No |  |
| └─ top_p | number | Nucleus sampling parameter. This is a query parameter used to select responses. | No |  |
| └─ type | enum | The type of run data source. Always `responses`.<br>Possible values: `responses` | No |  |
| └─ users | array | List of user identifiers. This is a query parameter used to select responses. | No |  |
| type | enum | The type of run data source. Always `responses`.<br>Possible values: `responses` | Yes |  |

### OpenAI.EvalRun

A schema representing an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the evaluation run was created. | Yes |  |
| data_source | object |  | Yes |  |
| └─ type | [OpenAI.EvalRunDataSourceType](#openaievalrundatasourcetype) |  | No |  |
| error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | Yes |  |
| eval_id | string | The identifier of the associated evaluation. | Yes |  |
| id | string | Unique identifier for the evaluation run. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
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

### OpenAI.EvalRunDataContentSource


### Discriminator for OpenAI.EvalRunDataContentSource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `file_id` | [OpenAI.EvalRunFileIdDataContentSource](#openaievalrunfileiddatacontentsource) |
| `stored_completions` | [OpenAI.EvalRunStoredCompletionsDataContentSource](#openaievalrunstoredcompletionsdatacontentsource) |
| `responses` | [OpenAI.EvalRunResponsesDataContentSource](#openaievalrunresponsesdatacontentsource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalRunDataContentSourceType](#openaievalrundatacontentsourcetype) |  | Yes |  |

### OpenAI.EvalRunDataContentSourceType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `file_id`<br>`file_content`<br>`stored_completions`<br>`responses` |

### OpenAI.EvalRunDataSourceCompletionsResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `completions` | Yes |  |

### OpenAI.EvalRunDataSourceJsonlResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `jsonl` | Yes |  |

### OpenAI.EvalRunDataSourceParams


### Discriminator for OpenAI.EvalRunDataSourceParams

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `jsonl` | [OpenAI.EvalJsonlRunDataSourceParams](#openaievaljsonlrundatasourceparams) |
| `completions` | [OpenAI.EvalCompletionsRunDataSourceParams](#openaievalcompletionsrundatasourceparams) |
| `responses` | [OpenAI.EvalResponsesRunDataSourceParams](#openaievalresponsesrundatasourceparams) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalRunDataSourceType](#openaievalrundatasourcetype) |  | Yes |  |

### OpenAI.EvalRunDataSourceResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalRunDataSourceType](#openaievalrundatasourcetype) |  | Yes |  |

### OpenAI.EvalRunDataSourceResponsesResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `responses` | Yes |  |

### OpenAI.EvalRunDataSourceType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `jsonl`<br>`completions`<br>`responses` |

### OpenAI.EvalRunFileContentDataContentSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content of the jsonl file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_content`.<br>Possible values: `file_content` | Yes |  |

### OpenAI.EvalRunFileIdDataContentSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The identifier of the file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_id`.<br>Possible values: `file_id` | Yes |  |

### OpenAI.EvalRunList

An object representing a list of runs for an evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | An array of eval run objects. | Yes |  |
| first_id | string | The identifier of the first eval run in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more evals available. | Yes |  |
| last_id | string | The identifier of the last eval run in the data array. | Yes |  |
| object | enum | The type of this object. It is always set to "list".<br>Possible values: `list` | Yes |  |

### OpenAI.EvalRunOutputItem

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
| └─ error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | No |  |
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

### OpenAI.EvalRunOutputItemList

An object representing a list of output items for an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | An array of eval run output item objects. | Yes |  |
| first_id | string | The identifier of the first eval run output item in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more eval run output items available. | Yes |  |
| last_id | string | The identifier of the last eval run output item in the data array. | Yes |  |
| object | enum | The type of this object. It is always set to "list".<br>Possible values: `list` | Yes |  |

### OpenAI.EvalRunResponsesDataContentSource

A EvalResponsesSource object describing a run data source configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | integer | Only include items created after this timestamp (inclusive). This is a query parameter used to select responses. | No |  |
| created_before | integer | Only include items created before this timestamp (inclusive). This is a query parameter used to select responses. | No |  |
| instructions_search | string | Optional string to search the 'instructions' field. This is a query parameter used to select responses. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string | The name of the model to find responses for. This is a query parameter used to select responses. | No |  |
| reasoning_effort | object | **o-series models only**<br><br>Constrains effort on reasoning forreasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| temperature | number | Sampling temperature. This is a query parameter used to select responses. | No |  |
| tools | array | List of tool names. This is a query parameter used to select responses. | No |  |
| top_p | number | Nucleus sampling parameter. This is a query parameter used to select responses. | No |  |
| type | enum | The type of run data source. Always `responses`.<br>Possible values: `responses` | Yes |  |
| users | array | List of user identifiers. This is a query parameter used to select responses. | No |  |

### OpenAI.EvalRunStoredCompletionsDataContentSource

A StoredCompletionsRunDataSource configuration describing a set of filters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | integer | An optional Unix timestamp to filter items created after this time. | No |  |
| created_before | integer | An optional Unix timestamp to filter items created before this time. | No |  |
| limit | integer | An optional maximum number of items to return. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| model | string | An optional model to filter by (e.g., 'gpt-4o'). | No |  |
| type | enum | The type of source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.EvalStoredCompletionsDataSourceConfigParams

Deprecated in favor of LogsDataSourceConfig.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Metadata filters for the stored completions data source. | No |  |
| type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.EvalStoredCompletionsDataSourceConfigResource

Deprecated in favor of LogsDataSourceConfig.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| schema | object | The json schema for the run data source items.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.FileSearchTool

A tool that searches for relevant content from uploaded files. 

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | object |  | No |  |
| max_num_results | integer | The maximum number of results to return. This number should be between 1 and 50 inclusive. | No |  |
| ranking_options | object |  | No |  |
| └─ ranker | enum | The ranker to use for the file search.<br>Possible values: `auto`, `default-2024-11-15` | No |  |
| └─ score_threshold | number | The score threshold for the file search, a number between 0 and 1. Numbers closer to 1 will attempt to return only the most relevant results, but may return fewer results. | No |  |
| type | enum | The type of the file search tool. Always `file_search`.<br>Possible values: `file_search` | Yes |  |
| vector_store_ids | array | The IDs of the vector stores to search. | Yes |  |

### OpenAI.Filters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | array | Array of filters to combine. Items can be `ComparisonFilter` or `CompoundFilter`. | Yes |  |
| key | string | The key to compare against the value. | Yes |  |
| type | enum | Type of operation: `and` or `or`.<br>Possible values: `and`, `or` | Yes |  |
| value | string or number or boolean | The value to compare against the attribute key; supports string, number, or boolean types. | Yes |  |

### OpenAI.FineTuneDPOHyperparameters

The hyperparameters used for the DPO fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | enum | <br>Possible values: `auto` | No |  |
| beta | enum | <br>Possible values: `auto` | No |  |
| learning_rate_multiplier | enum | <br>Possible values: `auto` | No |  |
| n_epochs | enum | <br>Possible values: `auto` | No |  |

### OpenAI.FineTuneDPOMethod

Configuration for the DPO fine-tuning method.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.FineTuneDPOHyperparameters](#openaifinetunedpohyperparameters) | The hyperparameters used for the DPO fine-tuning job. | No |  |

### OpenAI.FineTuneMethod

The method used for fine-tuning.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| dpo | [OpenAI.FineTuneDPOMethod](#openaifinetunedpomethod) | Configuration for the DPO fine-tuning method. | No |  |
| reinforcement | [AzureFineTuneReinforcementMethod](#azurefinetunereinforcementmethod) |  | No |  |
| supervised | [OpenAI.FineTuneSupervisedMethod](#openaifinetunesupervisedmethod) | Configuration for the supervised fine-tuning method. | No |  |
| type | enum | The type of method. Is either `supervised`, `dpo`, or `reinforcement`.<br>Possible values: `supervised`, `dpo`, `reinforcement` | Yes |  |

### OpenAI.FineTuneReinforcementHyperparameters

The hyperparameters used for the reinforcement fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | enum | <br>Possible values: `auto` | No |  |
| compute_multiplier | enum | <br>Possible values: `auto` | No |  |
| eval_interval | enum | <br>Possible values: `auto` | No |  |
| eval_samples | enum | <br>Possible values: `auto` | No |  |
| learning_rate_multiplier | enum | <br>Possible values: `auto` | No |  |
| n_epochs | enum | <br>Possible values: `auto` | No |  |
| reasoning_effort | enum | Level of reasoning effort.<br>Possible values: `default`, `low`, `medium`, `high` | No |  |

### OpenAI.FineTuneSupervisedHyperparameters

The hyperparameters used for the fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | enum | <br>Possible values: `auto` | No |  |
| learning_rate_multiplier | enum | <br>Possible values: `auto` | No |  |
| n_epochs | enum | <br>Possible values: `auto` | No |  |

### OpenAI.FineTuneSupervisedMethod

Configuration for the supervised fine-tuning method.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.FineTuneSupervisedHyperparameters](#openaifinetunesupervisedhyperparameters) | The hyperparameters used for the fine-tuning job. | No |  |

### OpenAI.FineTuningIntegration


### Discriminator for OpenAI.FineTuningIntegration

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `wandb` | [OpenAI.FineTuningIntegrationWandb](#openaifinetuningintegrationwandb) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | string (see valid models below) |  | Yes |  |

### OpenAI.FineTuningIntegrationWandb

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the integration being enabled for the fine-tuning job<br>Possible values: `wandb` | Yes |  |
| wandb | object | The settings for your integration with Weights and Biases. This payload specifies the project that<br>metrics will be sent to. Optionally, you can set an explicit display name for your run, add tags<br>to your run, and set a default entity (team, username, etc) to be associated with your run. | Yes |  |
| └─ entity | string | The entity to use for the run. This allows you to set the team or username of the WandB user that you would<br>like associated with the run. If not set, the default entity for the registered WandB API key is used. | No |  |
| └─ name | string | A display name to set for the run. If not set, we will use the Job ID as the name. | No |  |
| └─ project | string | The name of the project that the new run will be created under. | No |  |
| └─ tags | array | A list of tags to be attached to the newly created run. These tags are passed through directly to WandB. Some<br>default tags are generated by OpenAI: "openai/finetune", "openai/{base-model}", "openai/{ftjob-abcdef}". | No |  |

### OpenAI.FineTuningJob

The `fine_tuning.job` object represents a fine-tuning job that has been created through the API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the fine-tuning job was created. | Yes |  |
| error | object | For fine-tuning jobs that have `failed`, this will contain more information on the cause of the failure. | Yes |  |
| └─ code | string | A machine-readable error code. | No |  |
| └─ message | string | A human-readable error message. | No |  |
| └─ param | string | The parameter that was invalid, usually `training_file` or `validation_file`. This field will be null if the failure was not parameter-specific. | No |  |
| estimated_finish | integer | The Unix timestamp (in seconds) for when the fine-tuning job is estimated to finish. The value will be null if the fine-tuning job is not running. | No |  |
| fine_tuned_model | string | The name of the fine-tuned model that is being created. The value will be null if the fine-tuning job is still running. | Yes |  |
| finished_at | integer | The Unix timestamp (in seconds) for when the fine-tuning job was finished. The value will be null if the fine-tuning job is still running. | Yes |  |
| hyperparameters | object | The hyperparameters used for the fine-tuning job. This value will only be returned when running `supervised` jobs. | Yes |  |
| └─ batch_size | enum | <br>Possible values: `auto` | No |  |
| └─ learning_rate_multiplier | enum | <br>Possible values: `auto` | No |  |
| └─ n_epochs | enum | <br>Possible values: `auto` | No |  |
| id | string | The object identifier, which can be referenced in the API endpoints. | Yes |  |
| integrations | array | A list of integrations to enable for this fine-tuning job. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string | The base model that is being fine-tuned. | Yes |  |
| object | enum | The object type, which is always "fine_tuning.job".<br>Possible values: `fine_tuning.job` | Yes |  |
| organization_id | string | The organization that owns the fine-tuning job. | Yes |  |
| result_files | array | The compiled results file ID(s) for the fine-tuning job. You can retrieve the results with the Files API. | Yes |  |
| seed | integer | The seed used for the fine-tuning job. | Yes |  |
| status | enum | The current status of the fine-tuning job, which can be either `validating_files`, `queued`, `running`, `succeeded`, `failed`, or `cancelled`.<br>Possible values: `validating_files`, `queued`, `running`, `succeeded`, `failed`, `cancelled` | Yes |  |
| trained_tokens | integer | The total number of billable tokens processed by this fine-tuning job. The value will be null if the fine-tuning job is still running. | Yes |  |
| training_file | string | The file ID used for training. You can retrieve the training data with the Files API. | Yes |  |
| user_provided_suffix | string | The descriptive suffix applied to the job, as specified in the job creation request. | No |  |
| validation_file | string | The file ID used for validation. You can retrieve the validation results with the Files API. | Yes |  |

### OpenAI.FineTuningJobCheckpoint

The `fine_tuning.job.checkpoint` object represents a model checkpoint for a fine-tuning job that is ready to use.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the checkpoint was created. | Yes |  |
| fine_tuned_model_checkpoint | string | The name of the fine-tuned checkpoint model that is created. | Yes |  |
| fine_tuning_job_id | string | The name of the fine-tuning job that this checkpoint was created from. | Yes |  |
| id | string | The checkpoint identifier, which can be referenced in the API endpoints. | Yes |  |
| metrics | object | Metrics at the step number during the fine-tuning job. | Yes |  |
| └─ full_valid_loss | number |  | No |  |
| └─ full_valid_mean_token_accuracy | number |  | No |  |
| └─ step | number |  | No |  |
| └─ train_loss | number |  | No |  |
| └─ train_mean_token_accuracy | number |  | No |  |
| └─ valid_loss | number |  | No |  |
| └─ valid_mean_token_accuracy | number |  | No |  |
| object | enum | The object type, which is always "fine_tuning.job.checkpoint".<br>Possible values: `fine_tuning.job.checkpoint` | Yes |  |
| step_number | integer | The step number that the checkpoint was created at. | Yes |  |

### OpenAI.FineTuningJobEvent

Fine-tuning job event object

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the fine-tuning job was created. | Yes |  |
| data |  | The data associated with the event. | No |  |
| id | string | The object identifier. | Yes |  |
| level | enum | The log level of the event.<br>Possible values: `info`, `warn`, `error` | Yes |  |
| message | string | The message of the event. | Yes |  |
| object | enum | The object type, which is always "fine_tuning.job.event".<br>Possible values: `fine_tuning.job.event` | Yes |  |
| type | enum | The type of event.<br>Possible values: `message`, `metrics` | No |  |

### OpenAI.FunctionObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| name | string | The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64. | Yes |  |
| parameters |  | The parameters the functions accepts, described as a JSON Schema object.  | No |  |
| strict | boolean | Whether to enable strict schema adherence when generating the function call. If set to true, the model will follow the exact schema defined in the `parameters` field. Only a subset of JSON Schema is supported when `strict` is `true`. | No | False |

### OpenAI.FunctionTool

Defines a function in your own code the model can choose to call. 

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of the function. Used by the model to determine whether or not to call the function. | No |  |
| name | string | The name of the function to call. | Yes |  |
| parameters |  | A JSON schema object describing the parameters of the function. | Yes |  |
| strict | boolean | Whether to enforce strict parameter validation. Default `true`. | Yes |  |
| type | enum | The type of the function tool. Always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.Grader


### Discriminator for OpenAI.Grader

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `label_model` | [OpenAI.GraderLabelModel](#openaigraderlabelmodel) |
| `text_similarity` | [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) |
| `python` | [OpenAI.GraderPython](#openaigraderpython) |
| `score_model` | [OpenAI.GraderScoreModel](#openaigraderscoremodel) |
| `multi` | [OpenAI.GraderMulti](#openaigradermulti) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.GraderType](#openaigradertype) |  | Yes |  |

### OpenAI.GraderLabelModel

A LabelModelGrader object which uses a model to assign labels to each item
in the evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array |  | Yes |  |
| labels | array | The labels to assign to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### OpenAI.GraderMulti

A MultiGrader object combines the output of multiple graders to produce a single score.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| calculate_output | string | A formula to calculate the output based on grader results. | Yes |  |
| graders | object |  | Yes |  |
| name | string | The name of the grader. | Yes |  |
| type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | Yes |  |

### OpenAI.GraderPython

A PythonGrader object that runs a python script on the input.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_tag | string | The image tag to use for the python script. | No |  |
| name | string | The name of the grader. | Yes |  |
| source | string | The source code of the python script. | Yes |  |
| type | enum | The object type, which is always `python`.<br>Possible values: `python` | Yes |  |

### OpenAI.GraderScoreModel

A ScoreModelGrader object that uses a model to assign a score to the input.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array | The input text. This may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params |  | The sampling parameters for the model. | No |  |
| type | enum | The object type, which is always `score_model`.<br>Possible values: `score_model` | Yes |  |

### OpenAI.GraderStringCheck

A StringCheckGrader object that performs a string comparison between input and reference using a specified operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The input text. This may include template strings. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | Yes |  |
| reference | string | The reference text. This may include template strings. | Yes |  |
| type | enum | The object type, which is always `string_check`.<br>Possible values: `string_check` | Yes |  |

### OpenAI.GraderTextSimilarity

A TextSimilarityGrader object which grades text based on similarity metrics.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
| input | string | The text being graded. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| reference | string | The text being graded against. | Yes |  |
| type | enum | The type of grader.<br>Possible values: `text_similarity` | Yes |  |

### OpenAI.GraderType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `string_check`<br>`text_similarity`<br>`score_model`<br>`label_model`<br>`python`<br>`multi` |

### OpenAI.ImageGenTool

A tool that generates images using a model like `gpt-image-1`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Background type for the generated image. One of `transparent`,<br>`opaque`, or `auto`. Default: `auto`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| input_image_mask | object | Optional mask for inpainting. Contains `image_url`<br>(string, optional) and `file_id` (string, optional). | No |  |
| └─ file_id | string | File ID for the mask image. | No |  |
| └─ image_url | string | Base64-encoded mask image. | No |  |
| model | enum | The image generation model to use. Default: `gpt-image-1`.<br>Possible values: `gpt-image-1` | No |  |
| moderation | enum | Moderation level for the generated image. Default: `auto`.<br>Possible values: `auto`, `low` | No |  |
| output_compression | integer | Compression level for the output image. Default: 100. | No | 100 |
| output_format | enum | The output format of the generated image. One of `png`, `webp`, or<br>`jpeg`. Default: `png`.<br>Possible values: `png`, `webp`, `jpeg` | No |  |
| partial_images | integer | Number of partial images to generate in streaming mode, from 0 (default value) to 3. | No | 0 |
| quality | enum | The quality of the generated image. One of `low`, `medium`, `high`,<br>or `auto`. Default: `auto`.<br>Possible values: `low`, `medium`, `high`, `auto` | No |  |
| size | enum | The size of the generated image. One of `1024x1024`, `1024x1536`,<br>`1536x1024`, or `auto`. Default: `auto`.<br>Possible values: `1024x1024`, `1024x1536`, `1536x1024`, `auto` | No |  |
| type | enum | The type of the image generation tool. Always `image_generation`.<br>Possible values: `image_generation` | Yes |  |

### OpenAI.ListFineTuningJobCheckpointsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| first_id | string |  | No |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListFineTuningJobEventsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| has_more | boolean |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListModelsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListPaginatedFineTuningJobsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| has_more | boolean |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.LocalShellTool

A tool that allows the model to execute shell commands in a local environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the local shell tool. Always `local_shell`.<br>Possible values: `local_shell` | Yes |  |

### OpenAI.Location


### Discriminator for OpenAI.Location

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `approximate` | [OpenAI.ApproximateLocation](#openaiapproximatelocation) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.LocationType](#openailocationtype) |  | Yes |  |

### OpenAI.LocationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `approximate` |

### OpenAI.MCPTool

Give the model access to additional tools via remote Model Context Protocol
(MCP) servers. 

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| allowed_tools | object |  | No |  |
| └─ tool_names | array | List of allowed tool names. | No |  |
| headers | object | Optional HTTP headers to send to the MCP server. Use for authentication<br>or other purposes. | No |  |
| require_approval | object (see valid models below) | Specify which of the MCP server's tools require approval. | No |  |
| server_label | string | A label for this MCP server, used to identify it in tool calls. | Yes |  |
| server_url | string | The URL for the MCP server. | Yes |  |
| type | enum | The type of the MCP tool. Always `mcp`.<br>Possible values: `mcp` | Yes |  |

### OpenAI.MetadataPropertyForRequest

Set of 16 key-value pairs that can be attached to an object. This can be
useful for storing additional information about the object in a structured
format, and querying for objects via API or the dashboard.

Keys are strings with a maximum length of 64 characters. Values are strings
with a maximum length of 512 characters.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |

### OpenAI.Model

Describes an OpenAI model offering that can be used with the API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created | integer | The Unix timestamp (in seconds) when the model was created. | Yes |  |
| id | string | The model identifier, which can be referenced in the API endpoints. | Yes |  |
| object | enum | The object type, which is always "model".<br>Possible values: `model` | Yes |  |
| owned_by | string | The organization that owns the model. | Yes |  |

### OpenAI.RankingOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| ranker | enum | The ranker to use for the file search.<br>Possible values: `auto`, `default-2024-11-15` | No |  |
| score_threshold | number | The score threshold for the file search, a number between 0 and 1. Numbers closer to 1 will attempt to return only the most relevant results, but may return fewer results. | No |  |

### OpenAI.ReasoningEffort

**o-series models only**

Constrains effort on reasoning for reasoning models. Currently supported values are `low`, `medium`, and `high`. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.

| Property | Value |
|----------|-------|
| **Description** | **o-series models only**<br><br>Constrains effort on reasoning forreasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. |
| **Type** | string |
| **Values** | `low`<br>`medium`<br>`high` |

### OpenAI.ResponseFormatJsonSchemaSchema

The schema for the response format, described as a JSON Schema object.
Learn how to build JSON schemas [here](https://json-schema.org/).

**Type**: object


### OpenAI.ResponseTextFormatConfiguration


### Discriminator for OpenAI.ResponseTextFormatConfiguration

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `text` | [OpenAI.ResponseTextFormatConfigurationText](#openairesponsetextformatconfigurationtext) |
| `json_object` | [OpenAI.ResponseTextFormatConfigurationJsonObject](#openairesponsetextformatconfigurationjsonobject) |
| `json_schema` | [OpenAI.ResponseTextFormatConfigurationJsonSchema](#openairesponsetextformatconfigurationjsonschema) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ResponseTextFormatConfigurationType](#openairesponsetextformatconfigurationtype) | An object specifying the format that the model must output.<br><br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema.The default format is `{ "type": "text" }` with no additional options.<br><br>**Not recommended for gpt-4o and newer models:**<br><br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | Yes |  |

### OpenAI.ResponseTextFormatConfigurationJsonObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `json_object` | Yes |  |

### OpenAI.ResponseTextFormatConfigurationJsonSchema

JSON Schema response format. Used to generate structured JSON responses.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the response format is for, used by the model to<br>determine how to respond in the format. | No |  |
| name | string | The name of the response format. Must be a-z, A-Z, 0-9, or contain<br>underscores and dashes, with a maximum length of 64. | Yes |  |
| schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| strict | boolean | Whether to enable strict schema adherence when generating the output.<br>If set to true, the model will always follow the exact schema defined<br>in the `schema` field. Only a subset of JSON Schema is supported when<br>`strict` is `true`.  | No | False |
| type | enum | The type of response format being defined. Always `json_schema`.<br>Possible values: `json_schema` | Yes |  |

### OpenAI.ResponseTextFormatConfigurationText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `text` | Yes |  |

### OpenAI.ResponseTextFormatConfigurationType

An object specifying the format that the model must output.

Configuring `{ "type": "json_schema" }` enables Structured Outputs, which ensures the model will match your supplied JSON schema. 

The default format is `{ "type": "text" }` with no additional options.

**Not recommended for gpt-4o and newer models:**

Setting to `{ "type": "json_object" }` enables the older JSON mode, which
ensures the message the model generates is valid JSON. Using `json_schema`
is preferred for models that support it.

| Property | Value |
|----------|-------|
| **Description** | An object specifying the format that the model must output.

Configuring `{ "type": "json_schema" }` enables Structured Outputs,
which ensures the model will match your supplied JSON schema. 

The default format is `{ "type": "text" }` with no additional options.

**Not recommended for gpt-4o and newer models:**

Setting to `{ "type": "json_object" }` enables the older JSON mode, which
ensures the message the model generates is valid JSON. Using `json_schema`
is preferred for models that support it. |
| **Type** | string |
| **Values** | `text`<br>`json_schema`<br>`json_object` |

### OpenAI.RunGraderRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | object | A StringCheckGrader object that performs a string comparison between input and reference using a specified operation. | Yes |  |
| └─ calculate_output | string | A formula to calculate the output based on grader results. | No |  |
| └─ evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | No |  |
| └─ graders | object |  | No |  |
| └─ image_tag | string | The image tag to use for the python script. | No |  |
| └─ input | array | The input text. This may include template strings. | No |  |
| └─ model | string | The model to use for the evaluation. | No |  |
| └─ name | string | The name of the grader. | No |  |
| └─ operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | No |  |
| └─ range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| └─ reference | string | The text being graded against. | No |  |
| └─ sampling_params |  | The sampling parameters for the model. | No |  |
| └─ source | string | The source code of the python script. | No |  |
| └─ type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | No |  |
| item |  | The dataset item provided to the grader. This will be used to populate<br>the `item` namespace.  | No |  |
| model_sample | string | The model sample to be evaluated. This value will be used to populate<br>the `sample` namespace. <br>The `output_json` variable will be populated if the model sample is a<br>valid JSON string. | Yes |  |

### OpenAI.RunGraderResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object |  | Yes |  |
| └─ errors | object |  | No |  |
|   └─ formula_parse_error | boolean |  | No |  |
|   └─ invalid_variable_error | boolean |  | No |  |
|   └─ model_grader_parse_error | boolean |  | No |  |
|   └─ model_grader_refusal_error | boolean |  | No |  |
|   └─ model_grader_server_error | boolean |  | No |  |
|   └─ model_grader_server_error_details | string |  | No |  |
|   └─ other_error | boolean |  | No |  |
|   └─ python_grader_runtime_error | boolean |  | No |  |
|   └─ python_grader_runtime_error_details | string |  | No |  |
|   └─ python_grader_server_error | boolean |  | No |  |
|   └─ python_grader_server_error_type | string |  | No |  |
|   └─ sample_parse_error | boolean |  | No |  |
|   └─ truncated_observation_error | boolean |  | No |  |
|   └─ unresponsive_reward_error | boolean |  | No |  |
| └─ execution_time | number |  | No |  |
| └─ name | string |  | No |  |
| └─ sampled_model_name | string |  | No |  |
| └─ scores |  |  | No |  |
| └─ token_usage | integer |  | No |  |
| └─ type | string |  | No |  |
| model_grader_token_usage_per_model |  |  | Yes |  |
| reward | number |  | Yes |  |
| sub_rewards |  |  | Yes |  |

### OpenAI.Tool


### Discriminator for OpenAI.Tool

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `function` | [OpenAI.FunctionTool](#openaifunctiontool) |
| `file_search` | [OpenAI.FileSearchTool](#openaifilesearchtool) |
| `computer_use_preview` | [OpenAI.ComputerUsePreviewTool](#openaicomputerusepreviewtool) |
| `web_search_preview` | [OpenAI.WebSearchPreviewTool](#openaiwebsearchpreviewtool) |
| `code_interpreter` | [OpenAI.CodeInterpreterTool](#openaicodeinterpretertool) |
| `image_generation` | [OpenAI.ImageGenTool](#openaiimagegentool) |
| `local_shell` | [OpenAI.LocalShellTool](#openailocalshelltool) |
| `mcp` | [OpenAI.MCPTool](#openaimcptool) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ToolType](#openaitooltype) | A tool that can be used to generate a response. | Yes |  |

### OpenAI.ToolType

A tool that can be used to generate a response.

| Property | Value |
|----------|-------|
| **Description** | A tool that can be used to generate a response. |
| **Type** | string |
| **Values** | `file_search`<br>`function`<br>`computer_use_preview`<br>`web_search_preview`<br>`mcp`<br>`code_interpreter`<br>`image_generation`<br>`local_shell` |

### OpenAI.ValidateGraderRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | object | A StringCheckGrader object that performs a string comparison between input and reference using a specified operation. | Yes |  |
| └─ calculate_output | string | A formula to calculate the output based on grader results. | No |  |
| └─ evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | No |  |
| └─ graders | object |  | No |  |
| └─ image_tag | string | The image tag to use for the python script. | No |  |
| └─ input | array | The input text. This may include template strings. | No |  |
| └─ model | string | The model to use for the evaluation. | No |  |
| └─ name | string | The name of the grader. | No |  |
| └─ operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | No |  |
| └─ range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| └─ reference | string | The text being graded against. | No |  |
| └─ sampling_params |  | The sampling parameters for the model. | No |  |
| └─ source | string | The source code of the python script. | No |  |
| └─ type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | No |  |

### OpenAI.ValidateGraderResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | object | A StringCheckGrader object that performs a string comparison between input and reference using a specified operation. | No |  |
| └─ calculate_output | string | A formula to calculate the output based on grader results. | No |  |
| └─ evaluation_metric | enum | The evaluation metric to use. One of `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, or `rouge_l`.<br>Possible values: `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | No |  |
| └─ graders | object |  | No |  |
| └─ image_tag | string | The image tag to use for the python script. | No |  |
| └─ input | array | The input text. This may include template strings. | No |  |
| └─ model | string | The model to use for the evaluation. | No |  |
| └─ name | string | The name of the grader. | No |  |
| └─ operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | No |  |
| └─ range | array | The range of the score. Defaults to `[0, 1]`. | No |  |
| └─ reference | string | The text being graded against. | No |  |
| └─ sampling_params |  | The sampling parameters for the model. | No |  |
| └─ source | string | The source code of the python script. | No |  |
| └─ type | enum | The object type, which is always `multi`.<br>Possible values: `multi` | No |  |

### OpenAI.WebSearchPreviewTool

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| search_context_size | enum | High level guidance for the amount of context window space to use for the search. One of `low`, `medium`, or `high`. `medium` is the default.<br>Possible values: `low`, `medium`, `high` | No |  |
| type | enum | The type of the web search tool. One of `web_search_preview` or `web_search_preview_2025_03_11`.<br>Possible values: `web_search_preview` | Yes |  |
| user_location | object |  | No |  |
| └─ type | [OpenAI.LocationType](#openailocationtype) |  | No |  |

### ResponseFormatJSONSchemaRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| json_schema | object | JSON Schema for the response format | Yes |  |
| type | enum | Type of response format<br>Possible values: `json_schema` | Yes |  |