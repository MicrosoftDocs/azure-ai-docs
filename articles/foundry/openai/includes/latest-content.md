---
title: include file
description: include file
author: scottpolly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include
---

- [v1 OpenAPI 3.0 spec](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/ai/data-plane/OpenAI.v1/azure-v1-v1-generated.json)

**API Version:** v1

**Server Variables:**

| Variable | Default | Description |
| --- | --- | --- |
| endpoint |  | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |

## Authentication

### API key

Pass an API key with the `api-key` header.

### Auth tokens

Pass an auth token with the `authorization` header.

### Oauth2authoauth20

**Flow:** implicit

**Authorization URL:** `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`

**Scopes:**

- `https://ai.azure.com/.default`

## Batch

### Create batch

```HTTP
POST {endpoint}/openai/v1/batches
```

Creates and executes a batch from an uploaded file of requests


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| accept | True | string<br>Possible values: `application/json` |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_window | enum | The time frame within which the batch should be processed. Currently only `24h` is supported.<br>Possible values: `24h` | Yes |  |
| endpoint | enum | The endpoint to be used for all requests in the batch. Currently `/v1/chat/completions` is supported.<br>Possible values: `/v1/chat/completions`, `/v1/embeddings` | Yes |  |
| input_file_id | string | The ID of an uploaded file that contains requests for the new batch.<br><br><br><br>Your input file must be formatted as a JSON file,<br>and must be uploaded with the purpose `batch`. | No |  |

#### Responses

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result.

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List batches

```HTTP
GET {endpoint}/openai/v1/batches
```

List your organization's batches.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| accept | True | string<br>Possible values: `application/json` |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListBatchesResponse](#openailistbatchesresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve batch

```HTTP
GET {endpoint}/openai/v1/batches/{batch_id}
```

Retrieves a batch.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| batch_id | path | Yes | string | The ID of the batch to retrieve. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| accept | True | string<br>Possible values: `application/json` |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Cancel batch

```HTTP
POST {endpoint}/openai/v1/batches/{batch_id}/cancel
```

Cancels an in-progress batch.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| batch_id | path | Yes | string | The ID of the batch to cancel. |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| accept | True | string<br>Possible values: `application/json` |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Chat

### Create chat completion

```HTTP
POST {endpoint}/openai/v1/chat/completions
```


Creates a chat completion.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | [OpenAI.CreateChatCompletionRequestAudio](#openaicreatechatcompletionrequestaudio) or null | Parameters for audio output. Required when audio output is requested with<br>`modalities: ["audio"]`. | No |  |
| frequency_penalty | number or null | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>  their existing frequency in the text so far, decreasing the model's<br>  likelihood to repeat the same line verbatim. | No |  |
| function_call | string or [OpenAI.ChatCompletionFunctionCallOption](#openaichatcompletionfunctioncalloption) | Deprecated in favor of `tool_choice`.<br>  Controls which (if any) function is called by the model.<br>  `none` means the model will not call a function and instead generates a<br>  message.<br>  `auto` means the model can pick between generating a message or calling a<br>  function.<br>  Specifying a particular function via `{"name": "my_function"}` forces the<br>  model to call that function.<br>  `none` is the default when no functions are present. `auto` is the default<br>  if functions are present. | No |  |
| functions | array of [OpenAI.ChatCompletionFunctions](#openaichatcompletionfunctions) | Deprecated in favor of `tools`.<br>  A list of functions the model may generate JSON inputs for. | No |  |
| logit_bias | object or null | Modify the likelihood of specified tokens appearing in the completion.<br>  Accepts a JSON object that maps tokens (specified by their token ID in the<br>  tokenizer) to an associated bias value from -100 to 100. Mathematically,<br>  the bias is added to the logits generated by the model prior to sampling.<br>  The exact effect will vary per model, but values between -1 and 1 should<br>  decrease or increase likelihood of selection; values like -100 or 100<br>  should result in a ban or exclusive selection of the relevant token. | No |  |
| logprobs | boolean or null | Whether to return log probabilities of the output tokens or not. If true,<br>  returns the log probabilities of each output token returned in the<br>  `content` of `message`. | No |  |
| max_completion_tokens | integer or null | An upper bound for the number of tokens that can be generated for a<br>completion, including visible output tokens and reasoning tokens. | No |  |
| max_tokens | integer or null | The maximum number of tokens that can be generated in the chat completion.<br>This value can be used to control costs for text generated via API.<br><br>This value is now deprecated in favor of `max_completion_tokens`, and is<br>not compatible with o1 series models. | No |  |
| messages | array of [OpenAI.ChatCompletionRequestMessage](#openaichatcompletionrequestmessage) | A list of messages comprising the conversation so far. Depending on the<br>model you use, different message types (modalities) are supported,<br>like text, images, and audio. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| modalities | [OpenAI.ResponseModalities](#openairesponsemodalities) | Output types that you would like the model to generate.<br>Most models are capable of generating text, which is the default:<br>`["text"]`<br>The `gpt-4o-audio-preview` model can also be used to<br>[generate audio](https://platform.openai.com/docs/guides/audio). To request that this model generate<br>both text and audio responses, you can use:<br>`["text", "audio"]` | No |  |
| model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | Yes |  |
| n | integer or null | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs. | No |  |
| parallel_tool_calls | [OpenAI.ParallelToolCalls](#openaiparalleltoolcalls) | Whether to enable [parallel function calling](https://platform.openai.com/docs/guides/function-calling#configuring-parallel-function-calling) during tool use. | No |  |
| prediction | [OpenAI.PredictionContent](#openaipredictioncontent) | Static predicted output content, such as the content of a text file that is<br>being regenerated. | No |  |
| └─ content | string or array of [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext) | The content that should be matched when generating a model response.<br>  If generated tokens would match this content, the entire model response<br>  can be returned much more quickly. | Yes |  |
| └─ type | enum | The type of the predicted content you want to provide. This type is<br>  currently always `content`.<br>Possible values: `content` | Yes |  |
| presence_penalty | number or null | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>  whether they appear in the text so far, increasing the model's likelihood<br>  to talk about new topics. | No |  |
| prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| prompt_cache_retention | string or null |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| response_format | [OpenAI.CreateChatCompletionRequestResponseFormat](#openaicreatechatcompletionrequestresponseformat) | An object specifying the format that the model must output.<br>Setting to `{ "type": "json_schema", "json_schema": {...} }` enables<br>Structured Outputs which ensure the model will match your supplied JSON<br>schema. Learn more in the [Structured Outputs<br>guide](https://platform.openai.com/docs/guides/structured-outputs).<br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | No |  |
| └─ type | [OpenAI.CreateChatCompletionRequestResponseFormatType](#openaicreatechatcompletionrequestresponseformattype) |  | Yes |  |
| safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| seed | integer or null | This feature is in Beta.<br>  If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br>  Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | [OpenAI.StopConfiguration](#openaistopconfiguration) | Not supported with latest reasoning models `o3` and `o4-mini`.<br>Up to four sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| store | boolean or null | Whether or not to store the output of this chat completion request for<br>use in model distillation or evals products. | No |  |
| stream | boolean or null | If set to true, the model response data will be streamed to the client<br>as it is generated using server-sent events. | No |  |
| stream_options | [OpenAI.ChatCompletionStreamOptions](#openaichatcompletionstreamoptions) or null |  | No |  |
| temperature | number or null |  | No |  |
| tool_choice | [OpenAI.ChatCompletionToolChoiceOption](#openaichatcompletiontoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tool and instead generates a message.<br>`auto` means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools.<br>Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.<br>`none` is the default when no tools are present. `auto` is the default if tools are present. | No |  |
| tools | array of [OpenAI.ChatCompletionTool](#openaichatcompletiontool) or [OpenAI.CustomToolChatCompletions](#openaicustomtoolchatcompletions) | A list of tools the model may call. You can provide either<br>  [custom tools](https://platform.openai.com/docs/guides/function-calling#custom-tools) or<br>  [function tools](https://platform.openai.com/docs/guides/function-calling). | No |  |
| top_logprobs | integer or null |  | No |  |
| top_p | number or null |  | No |  |
| user | string (deprecated) | A unique identifier representing your end-user, which can help to<br>monitor and detect abuse. | No |  |
| user_security_context | [AzureUserSecurityContext](#azureusersecuritycontext) | User security context contains several parameters that describe the application itself, and the end user that interacts with the application. These fields assist your security operations teams to investigate and mitigate security incidents by providing a comprehensive approach to protecting your AI applications. [Learn more](https://aka.ms/TP4AI/Documentation/EndUserContext) about protecting AI applications using Microsoft Defender for Cloud. | No |  |
| verbosity | [OpenAI.Verbosity](#openaiverbosity) | Constrains the verbosity of the model's response. Lower values will result in<br>more concise responses, while higher values will result in more verbose responses.<br>Currently supported values are `low`, `medium`, and `high`. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object or object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

#### Examples

### Example



```HTTP
POST {endpoint}/openai/v1/chat/completions

```

## Completions

### Create completion

```HTTP
POST {endpoint}/openai/v1/completions
```


Creates a completion.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| best_of | integer or null | Generates `best_of` completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed.<br>  When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.<br>*Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`. | No |  |
| echo | boolean or null | Echo back the prompt in addition to the completion | No |  |
| frequency_penalty | number or null | Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.<br>  [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/text-generation) | No |  |
| logit_bias | object or null | Modify the likelihood of specified tokens appearing in the completion.<br>  Accepts a JSON object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.<br>  As an example, you can pass `{"50256": -100}` to prevent the <&#124;endoftext&#124;> token from being generated. | No |  |
| logprobs | integer or null | Include the log probabilities on the `logprobs` most likely output tokens, as well the chosen tokens. For example, if `logprobs` is 5, the API will return a list of the five most likely tokens. The API will always return the `logprob` of the sampled token, so there may be up to `logprobs+1` elements in the response.<br>  The maximum value for `logprobs` is 5. | No |  |
| max_tokens | integer or null | The maximum number of tokensthat can be generated in the completion.<br>  The token count of your prompt plus `max_tokens` cannot exceed the model's context length. [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens. | No |  |
| model | string | ID of the model to use. You can use the [List models](https://platform.openai.com/docs/api-reference/models/list) API to see all of your available models, or see our [Model overview](https://platform.openai.com/docs/models) for descriptions of them. | Yes |  |
| n | integer or null | How many completions to generate for each prompt.<br>*Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`. | No |  |
| presence_penalty | number or null | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.<br>  [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/text-generation) | No |  |
| prompt | string or array of string or null |  | No |  |
| seed | integer or null | If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br>  Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | [OpenAI.StopConfiguration](#openaistopconfiguration) | Not supported with latest reasoning models `o3` and `o4-mini`.<br>Up to four sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| stream | boolean or null | Whether to stream back partial progress. If set, tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions). | No |  |
| stream_options | [OpenAI.ChatCompletionStreamOptions](#openaichatcompletionstreamoptions) or null |  | No |  |
| suffix | string or null | The suffix that comes after a completion of inserted text.<br>  This parameter is only supported for `gpt-3.5-turbo-instruct`. | No |  |
| temperature | number or null | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>  We generally recommend altering this or `top_p` but not both. | No |  |
| top_p | number or null | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.<br>  We generally recommend altering this or `temperature` but not both. | No |  |
| user | string |  [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#end-user-ids). | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

#### Examples

### Example



```HTTP
POST {endpoint}/openai/v1/completions

```

## Containers

### List containers

```HTTP
GET {endpoint}/openai/v1/containers
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ContainerListResource](#openaicontainerlistresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create container

```HTTP
POST {endpoint}/openai/v1/containers
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | [OpenAI.CreateContainerBodyExpiresAfter](#openaicreatecontainerbodyexpiresafter) |  | No |  |
| └─ anchor | enum | <br>Possible values: `last_active_at` | Yes |  |
| └─ minutes | integer |  | Yes |  |
| file_ids | array of string | IDs of files to copy to the container. | No |  |
| memory_limit | enum | Optional memory limit for the container. Defaults to `1g`.<br>Possible values: `1g`, `4g`, `16g`, `64g` | No |  |
| name | string | Name of the container to create. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ContainerResource](#openaicontainerresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve container

```HTTP
GET {endpoint}/openai/v1/containers/{container_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| container_id | path | Yes | string | The ID of the container to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ContainerResource](#openaicontainerresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete container

```HTTP
DELETE {endpoint}/openai/v1/containers/{container_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| container_id | path | Yes | string | The ID of the container to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List container files

```HTTP
GET {endpoint}/openai/v1/containers/{container_id}/files
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| container_id | path | Yes | string | The ID of the container to list files from. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ContainerFileListResource](#openaicontainerfilelistresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create container file

```HTTP
POST {endpoint}/openai/v1/containers/{container_id}/files
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| container_id | path | Yes | string | The ID of the container to create a file in. |

#### Request Body

**Content-Type**: multipart/form-data

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file |  | The File object (not file name) to be uploaded. | No |  |
| file_id | string | Name of the file to create. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ContainerFileResource](#openaicontainerfileresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve container file

```HTTP
GET {endpoint}/openai/v1/containers/{container_id}/files/{file_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| container_id | path | Yes | string | The ID of the container. |
| file_id | path | Yes | string | The ID of the file to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ContainerFileResource](#openaicontainerfileresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete container file

```HTTP
DELETE {endpoint}/openai/v1/containers/{container_id}/files/{file_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| container_id | path | Yes | string | The ID of the container. |
| file_id | path | Yes | string | The ID of the file to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve container file content

```HTTP
GET {endpoint}/openai/v1/containers/{container_id}/files/{file_id}/content
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| container_id | path | Yes | string | The ID of the container. |
| file_id | path | Yes | string | The ID of the file to retrieve content from. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/octet-stream | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Conversations

### Create conversation

```HTTP
POST {endpoint}/openai/v1/conversations
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve conversation

```HTTP
GET {endpoint}/openai/v1/conversations/{conversation_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| conversation_id | path | Yes | string | The ID of the conversation to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Update conversation

```HTTP
POST {endpoint}/openai/v1/conversations/{conversation_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| conversation_id | path | Yes | string | The ID of the conversation to update. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null | Set of 16 key-value pairs that can be attached to an object. This can be         useful for storing additional information about the object in a structured         format, and querying for objects via API or the dashboard.<br>  Keys are strings with a maximum length of 64 characters. Values are strings         with a maximum length of 512 characters. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete conversation

```HTTP
DELETE {endpoint}/openai/v1/conversations/{conversation_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| conversation_id | path | Yes | string | The ID of the conversation to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeletedConversationResource](#openaideletedconversationresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List conversation items

```HTTP
GET {endpoint}/openai/v1/conversations/{conversation_id}/items
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| conversation_id | path | Yes | string | The ID of the conversation to list items for. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | The order to return the input items in. Default is `desc`. |
| after | query | No | string | An item ID to list items after, used in pagination. |
| include | query | No | array | Specify additional output data to include in the model response. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationItemList](#openaiconversationitemlist) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create conversation items

```HTTP
POST {endpoint}/openai/v1/conversations/{conversation_id}/items
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| conversation_id | path | Yes | string | The ID of the conversation to add the item to. |
| include | query | No | array | Additional fields to include in the response. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) |  | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationItemList](#openaiconversationitemlist) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve conversation item

```HTTP
GET {endpoint}/openai/v1/conversations/{conversation_id}/items/{item_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| conversation_id | path | Yes | string | The ID of the conversation that contains the item. |
| item_id | path | Yes | string | The ID of the item to retrieve. |
| include | query | No | array | Additional fields to include in the response. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationItem](#openaiconversationitem) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete conversation item

```HTTP
DELETE {endpoint}/openai/v1/conversations/{conversation_id}/items/{item_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| conversation_id | path | Yes | string | The ID of the conversation that contains the item. |
| item_id | path | Yes | string | The ID of the item to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ConversationResource](#openaiconversationresource) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Evals

### List evals

```HTTP
GET {endpoint}/openai/v1/evals
```

List evaluations for a project.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| after | query | No | string | Identifier for the last eval from the previous pagination request. |
| limit | query | No | integer | A limit on the number of evals to be returned in a single pagination response. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order for evals by timestamp. Use `asc` for ascending order or<br>`desc` for descending order. |
| order_by | query | No | string<br>Possible values: `created_at`, `updated_at` | Evals can be ordered by creation time or last updated time. Use<br>`created_at` for creation time or `updated_at` for last updated<br>time. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalList](#openaievallist) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create eval

```HTTP
POST {endpoint}/openai/v1/evals
```


Create the structure of an evaluation that can be used to test a model's
performance.

An evaluation is a set of testing criteria and a datasource. After
creating an evaluation, you can run it on different models and model
parameters. We support several types of graders and datasources.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source_config | [OpenAI.CreateEvalCustomDataSourceConfig](#openaicreateevalcustomdatasourceconfig) or [OpenAI.CreateEvalLogsDataSourceConfig](#openaicreateevallogsdatasourceconfig) or [OpenAI.CreateEvalStoredCompletionsDataSourceConfig](#openaicreateevalstoredcompletionsdatasourceconfig) | The configuration for the data source used for the evaluation runs. Dictates the schema of the data used in the evaluation. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| name | string | The name of the evaluation. | No |  |
| statusCode | enum | <br>Possible values: `201` | Yes |  |
| testing_criteria | array of [OpenAI.CreateEvalLabelModelGrader](#openaicreateevallabelmodelgrader) or [OpenAI.EvalGraderStringCheck](#openaievalgraderstringcheck) or [OpenAI.EvalGraderTextSimilarity](#openaievalgradertextsimilarity) or [OpenAI.EvalGraderPython](#openaievalgraderpython) or [OpenAI.EvalGraderScoreModel](#openaievalgraderscoremodel) or [EvalGraderEndpoint](#evalgraderendpoint) | A list of graders for all eval runs in this group. Graders can reference variables in the data source using double curly braces notation, like `{{item.variable_name}}`. To reference the model's output, use the `sample` namespace (ie, `{{sample.output_text}}`). | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Eval](#openaieval) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get eval

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}
```

Retrieve an evaluation by its ID.
Retrieves an evaluation by its ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Eval](#openaieval) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Update eval

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}
```


Update select, mutable properties of a specified evaluation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Eval](#openaieval) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete eval

```HTTP
DELETE {endpoint}/openai/v1/evals/{eval_id}
```


Delete a specified evaluation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get eval runs

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs
```


Retrieve a list of runs for a specified evaluation.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |
| after | query | No | string |  |
| limit | query | No | integer |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |
| status | query | No | string<br>Possible values: `queued`, `in_progress`, `completed`, `canceled`, `failed` |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRunList](#openaievalrunlist) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create eval run

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}/runs
```


Create a new evaluation run, beginning the grading process.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source | [OpenAI.CreateEvalJsonlRunDataSource](#openaicreateevaljsonlrundatasource) or [OpenAI.CreateEvalCompletionsRunDataSource](#openaicreateevalcompletionsrundatasource) or [OpenAI.CreateEvalResponsesRunDataSource](#openaicreateevalresponsesrundatasource) | Details about the run's data source. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| name | string | The name of the run. | No |  |

#### Responses

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRun](#openaievalrun) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get eval run

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}
```


Retrieve a specific evaluation run by its ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRun](#openaievalrun) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Cancel eval run

```HTTP
POST {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}
```


Cancel a specific evaluation run by its ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRun](#openaievalrun) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete eval run

```HTTP
DELETE {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}
```


Delete a specific evaluation run by its ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get eval run output items

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items
```


Get a list of output items for a specified evaluation run.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |
| after | query | No | string |  |
| limit | query | No | integer |  |
| status | query | No | string<br>Possible values: `fail`, `pass` |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRunOutputItemList](#openaievalrunoutputitemlist) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get eval run output item

```HTTP
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items/{output_item_id}
```


Retrieve a specific output item from an evaluation run by its ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| eval_id | path | Yes | string |  |
| run_id | path | Yes | string |  |
| output_item_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.EvalRunOutputItem](#openaievalrunoutputitem) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Files

### Create file

```HTTP
POST {endpoint}/openai/v1/files
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: multipart/form-data

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | object |  | Yes |  |
| └─ anchor | [AzureFileExpiryAnchor](#azurefileexpiryanchor) |  | Yes |  |
| └─ seconds | integer |  | Yes |  |
| file |  | The File object (not file name) to be uploaded. | Yes |  |
| purpose | enum | The intended purpose of the uploaded file. One of: - `assistants`: Used in the Assistants API - `batch`: Used in the Batch API - `fine-tune`: Used for fine-tuning - `evals`: Used for eval data sets<br>Possible values: `assistants`, `batch`, `fine-tune`, `evals` | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

#### Examples

### Example



```HTTP
POST {endpoint}/openai/v1/files

```

### List files

```HTTP
GET {endpoint}/openai/v1/files
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| purpose | query | No | string |  |
| limit | query | No | integer |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |
| after | query | No | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFilesResponse](#openailistfilesresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve file

```HTTP
GET {endpoint}/openai/v1/files/{file_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| file_id | path | Yes | string | The ID of the file to use for this request. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete file

```HTTP
DELETE {endpoint}/openai/v1/files/{file_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| file_id | path | Yes | string | The ID of the file to use for this request. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteFileResponse](#openaideletefileresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Download file

```HTTP
GET {endpoint}/openai/v1/files/{file_id}/content
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| file_id | path | Yes | string | The ID of the file to use for this request. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/octet-stream | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Embeddings

### Create embedding

```HTTP
POST {endpoint}/openai/v1/embeddings
```

Creates an embedding vector representing the input text.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| dimensions | integer | The number of dimensions the resulting output embeddings should have. Only supported in `text-embedding-3` and later models.<br>**Constraints:** min: 1 | No |  |
| encoding_format | enum | The format to return the embeddings in. Can be either `float` or [`base64`](https://pypi.org/project/pybase64/).<br>Possible values: `float`, `base64` | No |  |
| input | string or array of string or array of integer or array of array | Input text to embed, encoded as a string or array of tokens. To embed multiple inputs in a single request, pass an array of strings or array of token arrays. The input must not exceed the max input tokens for the model (8,192 tokens for all embedding models), cannot be an empty string, and any array must be 2,048 dimensions or less. [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens. In addition to the per-input token limit, all embedding  models enforce a maximum of 300,000 tokens summed across all inputs in a  single request. | Yes |  |
| model | string | ID of the model to use. You can use the [List models](https://platform.openai.com/docs/api-reference/models/list) API to see all of your available models, or see our [Model overview](https://platform.openai.com/docs/models) for descriptions of them. | Yes |  |
| user | string |  [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#end-user-ids). | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.CreateEmbeddingResponse](#openaicreateembeddingresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

#### Examples

### Example



```HTTP
POST {endpoint}/openai/v1/embeddings

```

## Fine-tuning

### Run grader

```HTTP
POST {endpoint}/openai/v1/fine_tuning/alpha/graders/run
```

Run a grader.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderPython](#openaigraderpython) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [OpenAI.GraderMulti](#openaigradermulti) or [GraderEndpoint](#graderendpoint) | The grader used for the fine-tuning job. | Yes |  |
| item | [OpenAI.RunGraderRequestItem](#openairungraderrequestitem) |  | No |  |
| model_sample | string | The model sample to be evaluated. This value will be used to populate<br>  the `sample` namespace. See [the guide](https://platform.openai.com/docs/guides/graders) for more details.<br>  The `output_json` variable will be populated if the model sample is a<br>  valid JSON string. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunGraderResponse](#openairungraderresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Validate grader

```HTTP
POST {endpoint}/openai/v1/fine_tuning/alpha/graders/validate
```

Validate a grader.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderPython](#openaigraderpython) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [OpenAI.GraderMulti](#openaigradermulti) or [GraderEndpoint](#graderendpoint) |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ValidateGraderResponse](#openaivalidategraderresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List fine tuning checkpoint permissions

```HTTP
GET {endpoint}/openai/v1/fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions
```

List checkpoint permissions


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuned_model_checkpoint | path | Yes | string | The ID of the fine-tuned model checkpoint to get permissions for. |
| project_id | query | No | string | The ID of the project to get permissions for. |
| after | query | No | string | Identifier for the last permission ID from the previous pagination request. |
| limit | query | No | integer | Number of permissions to retrieve. |
| order | query | No | string<br>Possible values: `ascending`, `descending` | The order in which to retrieve permissions. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningCheckpointPermissionResponse](#openailistfinetuningcheckpointpermissionresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create fine tuning checkpoint permission

```HTTP
POST {endpoint}/openai/v1/fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions
```

Create checkpoint permissions


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuned_model_checkpoint | path | Yes | string | The ID of the fine-tuned model checkpoint to create a permission for. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| project_ids | array of string | The project identifiers to grant access to. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningCheckpointPermissionResponse](#openailistfinetuningcheckpointpermissionresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete fine tuning checkpoint permission

```HTTP
DELETE {endpoint}/openai/v1/fine_tuning/checkpoints/{fine_tuned_model_checkpoint}/permissions/{permission_id}
```

Delete checkpoint permission


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuned_model_checkpoint | path | Yes | string | The ID of the fine-tuned model checkpoint to delete a permission for. |
| permission_id | path | Yes | string | The ID of the fine-tuned model checkpoint permission to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteFineTuningCheckpointPermissionResponse](#openaideletefinetuningcheckpointpermissionresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs
```

Creates a fine-tuning job which begins the process of creating a new model from a given dataset.

Response includes details of the enqueued job including job status and the name of the fine-tuned models once complete.




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.CreateFineTuningJobRequestHyperparameters](#openaicreatefinetuningjobrequesthyperparameters) |  | No |  |
| └─ batch_size | string or integer |  | No | auto |
| └─ learning_rate_multiplier | string or number |  | No |  |
| └─ n_epochs | string or integer |  | No | auto |
| integrations | array of [OpenAI.CreateFineTuningJobRequestIntegrations](#openaicreatefinetuningjobrequestintegrations) or null | A list of integrations to enable for your fine-tuning job. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string (see valid models below) | The name of the model to fine-tune. You can select one of the<br>  [supported models](https://platform.openai.com/docs/guides/fine-tuning#which-models-can-be-fine-tuned). | Yes |  |
| seed | integer or null | The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases.<br>  If a seed is not specified, one will be generated for you. | No |  |
| suffix | string or null | A string of up to 64 characters that will be added to your fine-tuned model name.<br>  For example, a `suffix` of "custom-model-name" would produce a model name like `ft:gpt-4o-mini:openai:custom-model-name:7p4lURel`. | No |  |
| training_file | string | The ID of an uploaded file that contains training data.<br>  See [upload file](https://platform.openai.com/docs/api-reference/files/create) for how to upload a file.<br>  Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose `fine-tune`.<br>  The contents of the file should differ depending on if the model uses the [chat](https://platform.openai.com/docs/api-reference/fine-tuning/chat-input), [completions](https://platform.openai.com/docs/api-reference/fine-tuning/completions-input) format, or if the fine-tuning method uses the [preference](https://platform.openai.com/docs/api-reference/fine-tuning/preference-input) format.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | Yes |  |
| validation_file | string or null | The ID of an uploaded file that contains validation data.<br>  If you provide this file, the data is used to generate validation<br>  metrics periodically during fine-tuning. These metrics can be viewed in<br>  the fine-tuning results file.<br>  The same data should not be present in both train and validation files.<br>  Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List paginated fine tuning jobs

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs
```

List your organization's fine-tuning jobs


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| after | query | No | string | Identifier for the last job from the previous pagination request. |
| limit | query | No | integer | Number of fine-tuning jobs to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListPaginatedFineTuningJobsResponse](#openailistpaginatedfinetuningjobsresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve fine tuning job

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}
```

Get info about a fine-tuning job.




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Cancel fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel
```

Immediately cancel a fine-tune job.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to cancel. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List fine tuning job checkpoints

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints
```

List the checkpoints for a fine-tuning job.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to get checkpoints for. |
| after | query | No | string | Identifier for the last checkpoint ID from the previous pagination request. |
| limit | query | No | integer | Number of checkpoints to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningJobCheckpointsResponse](#openailistfinetuningjobcheckpointsresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Fine tuning - copy checkpoint

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints/{fine_tuning_checkpoint_id}/copy
```


Creates a copy of a fine-tuning checkpoint at the given destination account and region.

NOTE: This Azure OpenAI API is in preview and subject to change.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string |  |
| fine_tuning_checkpoint_id | path | Yes | string |  |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| aoai-copy-ft-checkpoints | True | string<br>Possible values: `preview` | Enables access to checkpoint copy operations for models, an AOAI preview feature.<br>This feature requires the 'aoai-copy-ft-checkpoints' header to be set to 'preview'. |
| accept | True | string<br>Possible values: `application/json` |  |
#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| destinationResourceId | string | The ID of the destination Resource to copy. | Yes |  |
| region | string | The region to copy the model to. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [CopyModelResponse](#copymodelresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Fine tuning - get checkpoint

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints/{fine_tuning_checkpoint_id}/copy
```


Gets the status of a fine-tuning checkpoint copy.

NOTE: This Azure OpenAI API is in preview and subject to change.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string |  |
| fine_tuning_checkpoint_id | path | Yes | string |  |

#### Request Header

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| aoai-copy-ft-checkpoints | True | string<br>Possible values: `preview` | Enables access to checkpoint copy operations for models, an AOAI preview feature.<br>This feature requires the 'aoai-copy-ft-checkpoints' header to be set to 'preview'. |
| accept | True | string<br>Possible values: `application/json` |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [CopyModelResponse](#copymodelresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List fine tuning events

```HTTP
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/events
```

Get status updates for a fine-tuning job.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to get events for. |
| after | query | No | string | Identifier for the last event from the previous pagination request. |
| limit | query | No | integer | Number of events to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListFineTuningJobEventsResponse](#openailistfinetuningjobeventsresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Pause fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/pause
```

Pause a fine-tune job.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to pause. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Resume fine tuning job

```HTTP
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/resume
```

Resume a paused fine-tune job.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| fine_tuning_job_id | path | Yes | string | The ID of the fine-tuning job to resume. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.FineTuningJob](#openaifinetuningjob) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Models

### List models

```HTTP
GET {endpoint}/openai/v1/models
```

Lists the currently available models, and provides basic information about each one such as the
owner and availability.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListModelsResponse](#openailistmodelsresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve model

```HTTP
GET {endpoint}/openai/v1/models/{model}
```

Retrieves a model instance, providing basic information about the model such as the owner and
permissioning.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| model | path | Yes | string | The ID of the model to use for this request. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.Model](#openaimodel) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete model

```HTTP
DELETE {endpoint}/openai/v1/models/{model}
```

Deletes a model instance.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| model | path | Yes | string | The ID of the model to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteModelResponse](#openaideletemodelresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Realtime

### Create real time call

```HTTP
POST {endpoint}/openai/v1/realtime/calls
```

Create a new Realtime API call over WebRTC and receive the SDP answer needed to complete the peer connection.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: multipart/form-data

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| sdp | string | WebRTC Session Description Protocol (SDP) offer generated by the caller. | Yes |  |
| session | [OpenAI.RealtimeSessionCreateRequestGA](#openairealtimesessioncreaterequestga) | Realtime session object configuration. | No |  |
| └─ audio | [OpenAI.RealtimeSessionCreateRequestGAAudio](#openairealtimesessioncreaterequestgaaudio) | Configuration for input and output audio. | No |  |
| └─ include | array of string | Additional fields to include in server outputs.<br>  `item.input_audio_transcription.logprobs`: Include logprobs for input audio transcription. | No |  |
| └─ instructions | string | The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses. The model can be instructed on response content and format, (for example "be extremely succinct", "act friendly", "here are examples of good responses") and on audio behavior (for example "talk quickly", "inject emotion into your voice", "laugh frequently"). The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior.<br>  Note that the server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session. | No |  |
| └─ max_output_tokens | integer (see valid models below) | Maximum number of output tokens for a single assistant response,<br>  inclusive of tool calls. Provide an integer between 1 and 4096 to<br>  limit output tokens, or `inf` for the maximum available tokens for a<br>  given model. Defaults to `inf`. | No |  |
| └─ model | string | The Realtime model used for this session. | No |  |
| └─ output_modalities | array of string | The set of modalities the model can respond with. It defaults to `["audio"]`, indicating<br>  that the model will respond with audio plus a transcript. `["text"]` can be used to make<br>  the model respond with text only. It is not possible to request both `text` and `audio` at the same time. | No | ['audio'] |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceFunction](#openaitoolchoicefunction) or [OpenAI.ToolChoiceMCP](#openaitoolchoicemcp) | How the model chooses tools. Provide one of the string modes or force a specific<br>  function/MCP tool. | No | auto |
| └─ tools | array of [OpenAI.RealtimeFunctionTool](#openairealtimefunctiontool) or [OpenAI.MCPTool](#openaimcptool) | Tools available to the model. | No |  |
| └─ tracing | string or [OpenAI.RealtimeSessionCreateRequestGATracing](#openairealtimesessioncreaterequestgatracing) or null | "" Set to null to disable tracing. Once<br>  tracing is enabled for a session, the configuration cannot be modified.<br>  `auto` will create a trace for the session with default values for the<br>  workflow name, group id, and metadata. | No | auto |
| └─ truncation | [OpenAI.RealtimeTruncation](#openairealtimetruncation) | When the number of tokens in a conversation exceeds the model's input token limit, the conversation be truncated, meaning messages (starting from the oldest) will not be included in the model's context. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.<br>Clients can configure truncation behavior to truncate with a lower max token limit, which is an effective way to control token usage and cost.<br>Truncation will reduce the number of cached tokens on the next turn (busting the cache), since messages are dropped from the beginning of the context. However, clients can also configure truncation to retain messages up to a fraction of the maximum context size, which will reduce the need for future truncations and thus improve the cache rate.<br>Truncation can be disabled entirely, which means the server will never truncate but would instead return an error if the conversation exceeds the model's input token limit. | No |  |
| └─ type | enum | The type of session to create. Always `realtime` for the Realtime API.<br>Possible values: `realtime` | Yes |  |

#### Responses

**Status Code:** 201

**Description**: The request has succeeded and a new resource has been created as a result. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/sdp | string | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| location | string | Relative URL containing the call ID for subsequent control requests. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Accept real time call

```HTTP
POST {endpoint}/openai/v1/realtime/calls/{call_id}/accept
```

Accept an incoming SIP call and configure the realtime session that will handle it.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| call_id | path | Yes | string | The identifier for the call provided in the realtime.call.incoming webhook. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | [OpenAI.RealtimeSessionCreateRequestGAAudio](#openairealtimesessioncreaterequestgaaudio) |  | No |  |
| └─ input | [OpenAI.RealtimeSessionCreateRequestGAAudioInput](#openairealtimesessioncreaterequestgaaudioinput) |  | No |  |
| └─ output | [OpenAI.RealtimeSessionCreateRequestGAAudioOutput](#openairealtimesessioncreaterequestgaaudiooutput) |  | No |  |
| include | array of string | Additional fields to include in server outputs.<br>  `item.input_audio_transcription.logprobs`: Include logprobs for input audio transcription. | No |  |
| instructions | string | The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses. The model can be instructed on response content and format, (for example "be extremely succinct", "act friendly", "here are examples of good responses") and on audio behavior (for example "talk quickly", "inject emotion into your voice", "laugh frequently"). The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior.<br>  Note that the server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session. | No |  |
| max_output_tokens | integer (see valid models below) | Maximum number of output tokens for a single assistant response,<br>  inclusive of tool calls. Provide an integer between 1 and 4096 to<br>  limit output tokens, or `inf` for the maximum available tokens for a<br>  given model. Defaults to `inf`. | No |  |
| model | string | The Realtime model used for this session. | No |  |
| output_modalities | array of string | The set of modalities the model can respond with. It defaults to `["audio"]`, indicating<br>  that the model will respond with audio plus a transcript. `["text"]` can be used to make<br>  the model respond with text only. It is not possible to request both `text` and `audio` at the same time. | No | ['audio'] |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceFunction](#openaitoolchoicefunction) or [OpenAI.ToolChoiceMCP](#openaitoolchoicemcp) | How the model chooses tools. Provide one of the string modes or force a specific<br>  function/MCP tool. | No |  |
| tools | array of [OpenAI.RealtimeFunctionTool](#openairealtimefunctiontool) or [OpenAI.MCPTool](#openaimcptool) | Tools available to the model. | No |  |
| tracing | string or [OpenAI.RealtimeSessionCreateRequestGATracing](#openairealtimesessioncreaterequestgatracing) or null | "" Set to null to disable tracing. Once<br>  tracing is enabled for a session, the configuration cannot be modified.<br>  `auto` will create a trace for the session with default values for the<br>  workflow name, group id, and metadata. | No |  |
| truncation | [OpenAI.RealtimeTruncation](#openairealtimetruncation) | When the number of tokens in a conversation exceeds the model's input token limit, the conversation be truncated, meaning messages (starting from the oldest) will not be included in the model's context. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.<br>Clients can configure truncation behavior to truncate with a lower max token limit, which is an effective way to control token usage and cost.<br>Truncation will reduce the number of cached tokens on the next turn (busting the cache), since messages are dropped from the beginning of the context. However, clients can also configure truncation to retain messages up to a fraction of the maximum context size, which will reduce the need for future truncations and thus improve the cache rate.<br>Truncation can be disabled entirely, which means the server will never truncate but would instead return an error if the conversation exceeds the model's input token limit. | No |  |
| type | enum | The type of session to create. Always `realtime` for the Realtime API.<br>Possible values: `realtime` | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Hang up realtime call

```HTTP
POST {endpoint}/openai/v1/realtime/calls/{call_id}/hangup
```

End an active Realtime API call, whether it was initiated over SIP or WebRTC.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| call_id | path | Yes | string | The identifier for the call. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Refer real time call

```HTTP
POST {endpoint}/openai/v1/realtime/calls/{call_id}/refer
```

Transfer an active SIP call to a new destination using the SIP REFER verb.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| call_id | path | Yes | string | The identifier for the call provided in the realtime.call.incoming webhook. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| target_uri | string | URI that should appear in the SIP Refer-To header. Supports values like<br>  `tel:+14155550123` or `sip:agent\@example.com`. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Reject real time call

```HTTP
POST {endpoint}/openai/v1/realtime/calls/{call_id}/reject
```

Decline an incoming SIP call by returning a SIP status code to the caller.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| call_id | path | Yes | string | The identifier for the call provided in the realtime.call.incoming webhook. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| status_code | integer | SIP response code to send back to the caller. Defaults to `603` (Decline)<br>  when omitted. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create real time client secret

```HTTP
POST {endpoint}/openai/v1/realtime/client_secrets
```

Create a Realtime client secret with an associated session configuration.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | [OpenAI.RealtimeCreateClientSecretRequestExpiresAfter](#openairealtimecreateclientsecretrequestexpiresafter) |  | No |  |
| └─ anchor | enum | <br>Possible values: `created_at` | No |  |
| └─ seconds | integer | **Constraints:** min: 10, max: 7200 | No | 600 |
| session | [OpenAI.RealtimeSessionCreateRequestUnion](#openairealtimesessioncreaterequestunion) |  | No |  |
| └─ type | [OpenAI.RealtimeSessionCreateRequestUnionType](#openairealtimesessioncreaterequestuniontype) |  | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RealtimeCreateClientSecretResponse](#openairealtimecreateclientsecretresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create real time session

```HTTP
POST {endpoint}/openai/v1/realtime/sessions
```

Create an ephemeral API token for use in client-side applications with the Realtime API.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| client_secret | [OpenAI.RealtimeSessionCreateRequestClientSecret](#openairealtimesessioncreaterequestclientsecret) |  | Yes |  |
| └─ expires_at | integer |  | Yes |  |
| └─ value | string |  | Yes |  |
| input_audio_format | string | The format of input audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`. | No |  |
| input_audio_transcription | [OpenAI.RealtimeSessionCreateRequestInputAudioTranscription](#openairealtimesessioncreaterequestinputaudiotranscription) |  | No |  |
| └─ model | string |  | No |  |
| instructions | string | The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses. The model can be instructed on response content and format, (for example "be extremely succinct", "act friendly", "here are examples of good responses") and on audio behavior (for example "talk quickly", "inject emotion into your voice", "laugh frequently"). The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior.<br>  Note that the server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session. | No |  |
| max_response_output_tokens | integer (see valid models below) | Maximum number of output tokens for a single assistant response,<br>  inclusive of tool calls. Provide an integer between 1 and 4096 to<br>  limit output tokens, or `inf` for the maximum available tokens for a<br>  given model. Defaults to `inf`. | No |  |
| modalities | array of string | The set of modalities the model can respond with. To disable audio,<br>  set this to ["text"]. | No | ['text', 'audio'] |
| output_audio_format | string | The format of output audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`. | No |  |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| speed | number | The speed of the model's spoken response. 1.0 is the default speed. 0.25 is<br>  the minimum speed. 1.5 is the maximum speed. This value can only be changed<br>  in between model turns, not while a response is in progress.<br>**Constraints:** min: 0.25, max: 1.5 | No | 1 |
| temperature | number | Sampling temperature for the model, limited to [0.6, 1.2]. Defaults to 0.8. | No |  |
| tool_choice | string | How the model chooses tools. Options are `auto`, `none`, `required`, or<br>  specify a function. | No |  |
| tools | array of [OpenAI.RealtimeSessionCreateRequestTools](#openairealtimesessioncreaterequesttools) | Tools (functions) available to the model. | No |  |
| tracing | string or object | Configuration options for tracing. Set to null to disable tracing. Once<br>  tracing is enabled for a session, the configuration cannot be modified.<br>  `auto` will create a trace for the session with default values for the<br>  workflow name, group id, and metadata. | No |  |
| truncation | [OpenAI.RealtimeTruncation](#openairealtimetruncation) | When the number of tokens in a conversation exceeds the model's input token limit, the conversation be truncated, meaning messages (starting from the oldest) will not be included in the model's context. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.<br>Clients can configure truncation behavior to truncate with a lower max token limit, which is an effective way to control token usage and cost.<br>Truncation will reduce the number of cached tokens on the next turn (busting the cache), since messages are dropped from the beginning of the context. However, clients can also configure truncation to retain messages up to a fraction of the maximum context size, which will reduce the need for future truncations and thus improve the cache rate.<br>Truncation can be disabled entirely, which means the server will never truncate but would instead return an error if the conversation exceeds the model's input token limit. | No |  |
| turn_detection | [OpenAI.RealtimeSessionCreateRequestTurnDetection](#openairealtimesessioncreaterequestturndetection) |  | No |  |
| └─ prefix_padding_ms | integer |  | No |  |
| └─ silence_duration_ms | integer |  | No |  |
| └─ threshold | number |  | No |  |
| └─ type | string |  | No |  |
| type | enum | <br>Possible values: `realtime` | Yes |  |
| voice | [OpenAI.VoiceIdsShared](#openaivoiceidsshared) |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RealtimeSessionCreateResponse](#openairealtimesessioncreateresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create real time transcription session

```HTTP
POST {endpoint}/openai/v1/realtime/transcription_sessions
```

Create an ephemeral API token for use in client-side applications with the Realtime API specifically for realtime transcriptions.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include | array of string | The set of items to include in the transcription. Current available items are:<br>  `item.input_audio_transcription.logprobs` | No |  |
| input_audio_format | enum | The format of input audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`.<br>  For `pcm16`, input audio must be 16-bit PCM at a 24-kHz sample rate,<br>  single channel (mono), and little-endian byte order.<br>Possible values: `pcm16`, `g711_ulaw`, `g711_alaw` | No |  |
| input_audio_noise_reduction | [OpenAI.RealtimeTranscriptionSessionCreateRequestInputAudioNoiseReduction](#openairealtimetranscriptionsessioncreaterequestinputaudionoisereduction) |  | No |  |
| └─ type | [OpenAI.NoiseReductionType](#openainoisereductiontype) | Type of noise reduction. `near_field` is for close-talking microphones such as headphones, `far_field` is for far-field microphones such as laptop or conference room microphones. | No |  |
| input_audio_transcription | [OpenAI.AudioTranscription](#openaiaudiotranscription) |  | No |  |
| └─ language | string | The language of the input audio. Supplying the input language in<br>  [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format<br>  will improve accuracy and latency. | No |  |
| └─ model | string | The model to use for transcription. Current options are `whisper-1`, `gpt-4o-mini-transcribe`, `gpt-4o-mini-transcribe-2025-12-15`, `gpt-4o-transcribe`, and `gpt-4o-transcribe-diarize`. Use `gpt-4o-transcribe-diarize` when you need diarization with speaker labels. | No |  |
| └─ prompt | string | An optional text to guide the model's style or continue a previous audio<br>  segment.<br>  For `whisper-1`, the [prompt is a list of keywords](https://platform.openai.com/docs/guides/speech-to-text#prompting).<br>  For `gpt-4o-transcribe` models (excluding `gpt-4o-transcribe-diarize`), the prompt is a free text string, for example "expect words related to technology". | No |  |
| turn_detection | [OpenAI.RealtimeTranscriptionSessionCreateRequestTurnDetection](#openairealtimetranscriptionsessioncreaterequestturndetection) |  | No |  |
| └─ prefix_padding_ms | integer |  | No |  |
| └─ silence_duration_ms | integer |  | No |  |
| └─ threshold | number |  | No |  |
| └─ type | enum | <br>Possible values: `server_vad` | No |  |
| type | enum | <br>Possible values: `transcription` | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RealtimeTranscriptionSessionCreateResponse](#openairealtimetranscriptionsessioncreateresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Responses

### Create response

```HTTP
POST {endpoint}/openai/v1/responses
```


Creates a model response.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean or null |  | No |  |
| conversation | [OpenAI.ConversationParam](#openaiconversationparam) or null |  | No |  |
| include | array of [OpenAI.IncludeEnum](#openaiincludeenum) or null |  | No |  |
| input | [OpenAI.InputParam](#openaiinputparam) | Text, image, or file inputs to the model, used to generate a response.<br>Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Image inputs](https://platform.openai.com/docs/guides/images)<br>- [File inputs](https://platform.openai.com/docs/guides/pdf-files)<br>- [Conversation state](https://platform.openai.com/docs/guides/conversation-state)<br>- [Function calling](https://platform.openai.com/docs/guides/function-calling) | No |  |
| instructions | string or null |  | No |  |
| max_output_tokens | integer or null |  | No |  |
| max_tool_calls | integer or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| parallel_tool_calls | boolean or null |  | No |  |
| previous_response_id | string or null |  | No |  |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| prompt_cache_retention | string or null |  | No |  |
| reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| store | boolean or null |  | No |  |
| stream | boolean or null |  | No |  |
| stream_options | [OpenAI.ResponseStreamOptions](#openairesponsestreamoptions) or null |  | No |  |
| temperature | number or null |  | No |  |
| text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| top_logprobs | integer or null |  | No |  |
| top_p | number or null |  | No |  |
| truncation | string or null |  | No |  |
| user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |
|text/event-stream | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

#### Examples

### Example



```HTTP
POST {endpoint}/openai/v1/responses

```

### Get response

```HTTP
GET {endpoint}/openai/v1/responses/{response_id}
```


Retrieves a model response with the given ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| response_id | path | Yes | string |  |
| include[] | query | No | array | Additional fields to include in the response. See the include parameter for Response creation above for more information. |
| stream | query | No | boolean | If set to true, the model response data will be streamed to the client as it is generated using server-sent events. |
| starting_after | query | No | integer | The sequence number of the event after which to start streaming. |
| include_obfuscation | query | No | boolean | When true, stream obfuscation will be enabled. Stream obfuscation adds random characters to an `obfuscation` field on streaming delta events to normalize payload sizes as a mitigation to certain side-channel attacks. These obfuscation fields are included by default, but add a small amount of overhead to the data stream. You can set `include_obfuscation` to false to optimize for bandwidth if you trust the network links between your application and the OpenAI API. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete response

```HTTP
DELETE {endpoint}/openai/v1/responses/{response_id}
```


Deletes a response by ID.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| response_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Cancel response

```HTTP
POST {endpoint}/openai/v1/responses/{response_id}/cancel
```


Cancels a model response with the given ID. Only responses created with the background parameter set to true can be cancelled.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| response_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List input items

```HTTP
GET {endpoint}/openai/v1/responses/{response_id}/input_items
```


Returns a list of input items for a given response.

#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| response_id | path | Yes | string |  |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ResponseItemList](#openairesponseitemlist) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Threads

### Create thread

```HTTP
POST {endpoint}/openai/v1/threads
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| messages | array of [OpenAI.CreateMessageRequest](#openaicreatemessagerequest) | A list of [messages](https://platform.openai.com/docs/api-reference/messages) to start the thread with. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| tool_resources | [OpenAI.CreateThreadRequestToolResources](#openaicreatethreadrequesttoolresources) or null |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ThreadObject](#openaithreadobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Createthread and run

```HTTP
POST {endpoint}/openai/v1/threads/runs
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| assistant_id | string | The ID of the [assistant](https://platform.openai.com/docs/api-reference/assistants) to use to execute this run. | Yes |  |
| instructions | string or null | Override the default system message of the assistant. This is useful for modifying the behavior on a per-run basis. | No |  |
| max_completion_tokens | integer or null | The maximum number of completion tokens that may be used over the course of the run. The run will make a best effort to use only the number of completion tokens specified, across multiple turns of the run. If the run exceeds the number of completion tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| max_prompt_tokens | integer or null | The maximum number of prompt tokens that may be used over the course of the run. The run will make a best effort to use only the number of prompt tokens specified, across multiple turns of the run. If the run exceeds the number of prompt tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | The ID of the [Model](https://platform.openai.com/docs/api-reference/models) to be used to execute this run. If a value is provided here, it will override the model associated with the assistant. If not, the model associated with the assistant will be used. | No |  |
| parallel_tool_calls | [OpenAI.ParallelToolCalls](#openaiparalleltoolcalls) | Whether to enable [parallel function calling](https://platform.openai.com/docs/guides/function-calling#configuring-parallel-function-calling) during tool use. | No |  |
| response_format | [OpenAI.AssistantsApiResponseFormatOption](#openaiassistantsapiresponseformatoption) | Specifies the format that the model must output. Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.<br>Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensure the model will match your supplied JSON schema. Learn more in the <br>Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the message the model generates is valid JSON.<br>*Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length. | No |  |
| stream | boolean or null | If `true`, returns a stream of events that happen during the Run as server-sent events, terminating when the Run enters a terminal state with a `data: [DONE]` message. | No |  |
| temperature | number or null | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. | No |  |
| thread | [OpenAI.CreateThreadRequest](#openaicreatethreadrequest) | Options to create a new thread. If no thread is provided when running a<br>request, an empty thread will be created. | No |  |
| tool_choice | [OpenAI.AssistantsApiToolChoiceOption](#openaiassistantsapitoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tools and instead generates a message.<br>`auto` is the default value and means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools before responding to the user.<br>Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool. | No |  |
| tool_resources | [OpenAI.CreateThreadAndRunRequestToolResources](#openaicreatethreadandrunrequesttoolresources) or null | A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For example, the `code_interpreter` tool requires a list of file IDs, while the `file_search` tool requires a list of vector store IDs. | No |  |
| tools | array of [OpenAI.AssistantTool](#openaiassistanttool) | Override the tools the assistant can use for this run. This is useful for modifying the behavior on a per-run basis. | No |  |
| top_p | number or null | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.<br>  We generally recommend altering this or temperature but not both. | No |  |
| truncation_strategy | [OpenAI.TruncationObject](#openaitruncationobject) | Controls for how a thread will be truncated prior to the run. Use this to control the initial context window of the run. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunObject](#openairunobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete thread

```HTTP
DELETE {endpoint}/openai/v1/threads/{thread_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteThreadResponse](#openaideletethreadresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve thread

```HTTP
GET {endpoint}/openai/v1/threads/{thread_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ThreadObject](#openaithreadobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Modify thread

```HTTP
POST {endpoint}/openai/v1/threads/{thread_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| tool_resources | [OpenAI.ModifyThreadRequestToolResources](#openaimodifythreadrequesttoolresources) or null |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ThreadObject](#openaithreadobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List messages

```HTTP
GET {endpoint}/openai/v1/threads/{thread_id}/messages
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| limit | query | No | integer |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |
| after | query | No | string |  |
| before | query | No | string |  |
| run_id | query | No | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListMessagesResponse](#openailistmessagesresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create message

```HTTP
POST {endpoint}/openai/v1/threads/{thread_id}/messages
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attachments | array of [OpenAI.CreateMessageRequestAttachments](#openaicreatemessagerequestattachments) or null |  | No |  |
| content | string or array of [OpenAI.MessageContentImageFileObject](#openaimessagecontentimagefileobject) or [OpenAI.MessageContentImageUrlObject](#openaimessagecontentimageurlobject) or [OpenAI.MessageRequestContentTextObject](#openaimessagerequestcontenttextobject) |  | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| role | enum | The role of the entity that is creating the message. Allowed values include:<br>  - `user`: Indicates the message is sent by an actual user and should be used in most cases to represent user-generated messages.<br>  - `assistant`: Indicates the message is generated by the assistant. Use this value to insert messages from the assistant into the conversation.<br>Possible values: `user`, `assistant` | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.MessageObject](#openaimessageobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete message

```HTTP
DELETE {endpoint}/openai/v1/threads/{thread_id}/messages/{message_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| message_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteMessageResponse](#openaideletemessageresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve message

```HTTP
GET {endpoint}/openai/v1/threads/{thread_id}/messages/{message_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| message_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.MessageObject](#openaimessageobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Modify message

```HTTP
POST {endpoint}/openai/v1/threads/{thread_id}/messages/{message_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| message_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.MessageObject](#openaimessageobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create run

```HTTP
POST {endpoint}/openai/v1/threads/{thread_id}/runs
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| additional_instructions | string or null | Appends additional instructions at the end of the instructions for the run. This is useful for modifying the behavior on a per-run basis without overriding other instructions. | No |  |
| additional_messages | array of [OpenAI.CreateMessageRequest](#openaicreatemessagerequest) or null | Adds additional messages to the thread before creating the run. | No |  |
| assistant_id | string | The ID of the [assistant](https://platform.openai.com/docs/api-reference/assistants) to use to execute this run. | Yes |  |
| instructions | string or null | Overrides the [instructions](https://platform.openai.com/docs/api-reference/assistants/createAssistant) of the assistant. This is useful for modifying the behavior on a per-run basis. | No |  |
| max_completion_tokens | integer or null | The maximum number of completion tokens that may be used over the course of the run. The run will make a best effort to use only the number of completion tokens specified, across multiple turns of the run. If the run exceeds the number of completion tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| max_prompt_tokens | integer or null | The maximum number of prompt tokens that may be used over the course of the run. The run will make a best effort to use only the number of prompt tokens specified, across multiple turns of the run. If the run exceeds the number of prompt tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | The ID of the [Model](https://platform.openai.com/docs/api-reference/models) to be used to execute this run. If a value is provided here, it will override the model associated with the assistant. If not, the model associated with the assistant will be used. | No |  |
| parallel_tool_calls | [OpenAI.ParallelToolCalls](#openaiparalleltoolcalls) | Whether to enable [parallel function calling](https://platform.openai.com/docs/guides/function-calling#configuring-parallel-function-calling) during tool use. | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| response_format | [OpenAI.AssistantsApiResponseFormatOption](#openaiassistantsapiresponseformatoption) | Specifies the format that the model must output. Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.<br>Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensure the model will match your supplied JSON schema. Learn more in the <br>Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the message the model generates is valid JSON.<br>*Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length. | No |  |
| stream | boolean or null | If `true`, returns a stream of events that happen during the Run as server-sent events, terminating when the Run enters a terminal state with a `data: [DONE]` message. | No |  |
| temperature | number or null | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. | No |  |
| tool_choice | [OpenAI.AssistantsApiToolChoiceOption](#openaiassistantsapitoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tools and instead generates a message.<br>`auto` is the default value and means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools before responding to the user.<br>Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool. | No |  |
| tools | array of [OpenAI.AssistantTool](#openaiassistanttool) | Override the tools the assistant can use for this run. This is useful for modifying the behavior on a per-run basis. | No |  |
| top_p | number or null | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.<br>  We generally recommend altering this or temperature but not both. | No |  |
| truncation_strategy | [OpenAI.TruncationObject](#openaitruncationobject) | Controls for how a thread will be truncated prior to the run. Use this to control the initial context window of the run. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunObject](#openairunobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List runs

```HTTP
GET {endpoint}/openai/v1/threads/{thread_id}/runs
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| limit | query | No | integer |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |
| after | query | No | string |  |
| before | query | No | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListRunsResponse](#openailistrunsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve run

```HTTP
GET {endpoint}/openai/v1/threads/{thread_id}/runs/{run_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| run_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunObject](#openairunobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Modify run

```HTTP
POST {endpoint}/openai/v1/threads/{thread_id}/runs/{run_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| run_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunObject](#openairunobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Cancel run

```HTTP
POST {endpoint}/openai/v1/threads/{thread_id}/runs/{run_id}/cancel
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| run_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunObject](#openairunobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List run steps

```HTTP
GET {endpoint}/openai/v1/threads/{thread_id}/runs/{run_id}/steps
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| run_id | path | Yes | string |  |
| limit | query | No | integer |  |
| order | query | No | string<br>Possible values: `asc`, `desc` |  |
| after | query | No | string |  |
| before | query | No | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListRunStepsResponse](#openailistrunstepsresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get run step

```HTTP
GET {endpoint}/openai/v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| run_id | path | Yes | string |  |
| step_id | path | Yes | string |  |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunStepObject](#openairunstepobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Submit tool outputs to run

```HTTP
POST {endpoint}/openai/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| thread_id | path | Yes | string |  |
| run_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| stream | boolean or null |  | No |  |
| tool_outputs | array of [OpenAI.SubmitToolOutputsRunRequestToolOutputs](#openaisubmittooloutputsrunrequesttooloutputs) | A list of tools for which the outputs are being submitted. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.RunObject](#openairunobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Vector Stores

### List vector stores

```HTTP
GET {endpoint}/openai/v1/vector_stores
```

Returns a list of vector stores.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListVectorStoresResponse](#openailistvectorstoresresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create vector store

```HTTP
POST {endpoint}/openai/v1/vector_stores
```

Creates a vector store.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. Only applicable if `file_ids` is non-empty. | No |  |
| description | string | A description for the vector store. Can be used to describe the vector store's purpose. | No |  |
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| file_ids | array of string | A list of [File](https://platform.openai.com/docs/api-reference/files) IDs that the vector store should use. Useful for tools like `file_search` that can access files. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| name | string | The name of the vector store. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreObject](#openaivectorstoreobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

#### Examples

### Example



```HTTP
POST {endpoint}/openai/v1/vector_stores

```

### Get vector store

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}
```

Retrieves a vector store.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to retrieve. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreObject](#openaivectorstoreobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Modify vector store

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}
```

Modifies a vector store.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to modify. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| name | string or null | The name of the vector store. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreObject](#openaivectorstoreobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete vector store

```HTTP
DELETE {endpoint}/openai/v1/vector_stores/{vector_store_id}
```

Delete a vector store.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteVectorStoreResponse](#openaideletevectorstoreresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create vector store file batch

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches
```

Create a vector store file batch.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store for which to create a file batch. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. Only applicable if `file_ids` is non-empty. | No |  |
| file_ids | array of string | A list of [File](https://platform.openai.com/docs/api-reference/files) IDs that the vector store should use. Useful for tools like `file_search` that can access files.  If `attributes` or `chunking_strategy` are provided, they will be  applied to all files in the batch. Mutually exclusive with `files`. | No |  |
| files | array of [OpenAI.CreateVectorStoreFileRequest](#openaicreatevectorstorefilerequest) | A list of objects that each include a `file_id` plus optional `attributes` or `chunking_strategy`. Use this when you need to override metadata for specific files. The global `attributes` or `chunking_strategy` will be ignored and must be specified for each file. Mutually exclusive with `file_ids`. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileBatchObject](#openaivectorstorefilebatchobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get vector store file batch

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches/{batch_id}
```

Retrieves a vector store file batch.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file batch belongs to. |
| batch_id | path | Yes | string | The ID of the file batch being retrieved. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileBatchObject](#openaivectorstorefilebatchobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Cancel vector store file batch

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/cancel
```

Cancel a vector store file batch. This attempts to cancel the processing of files in this batch as soon as possible.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file batch belongs to. |
| batch_id | path | Yes | string | The ID of the file batch to cancel. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileBatchObject](#openaivectorstorefilebatchobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List files in vector store batch

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/files
```

Returns a list of vector store files in a batch.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file batch belongs to. |
| batch_id | path | Yes | string | The ID of the file batch that the files belong to. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| filter | query | No | string<br>Possible values: `in_progress`, `completed`, `failed`, `cancelled` | Filter by file status. One of `in_progress`, `completed`, `failed`, `cancelled`. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListVectorStoreFilesResponse](#openailistvectorstorefilesresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### List vector store files

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/files
```

Returns a list of vector store files.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the files belong to. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| filter | query | No | string<br>Possible values: `in_progress`, `completed`, `failed`, `cancelled` | Filter by file status. One of `in_progress`, `completed`, `failed`, `cancelled`. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.ListVectorStoreFilesResponse](#openailistvectorstorefilesresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Create vector store file

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/files
```

Create a vector store file by attaching a File to a vector store.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store for which to create a File. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. Only applicable if `file_ids` is non-empty. | No |  |
| file_id | string | A [File](https://platform.openai.com/docs/api-reference/files) ID that the vector store should use. Useful for tools like `file_search` that can access files. | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileObject](#openaivectorstorefileobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Get vector store file

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/files/{file_id}
```

Retrieves a vector store file.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file belongs to. |
| file_id | path | Yes | string | The ID of the file being retrieved. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileObject](#openaivectorstorefileobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Update vector store file attributes

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/files/{file_id}
```




#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string |  |
| file_id | path | Yes | string |  |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | Yes |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileObject](#openaivectorstorefileobject) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Delete vector store file

```HTTP
DELETE {endpoint}/openai/v1/vector_stores/{vector_store_id}/files/{file_id}
```

Delete a vector store file. This will remove the file from the vector store but the file itself will not be deleted. To delete the file, use the delete file endpoint endpoint.


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file belongs to. |
| file_id | path | Yes | string | The ID of the file to delete. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.DeleteVectorStoreFileResponse](#openaideletevectorstorefileresponse) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Retrieve vector store file content

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/files/{file_id}/content
```

Retrieve vector store file content


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to search. |
| file_id | path | Yes | string | The ID of the file to retrieve content for. |


#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreSearchResultsPage](#openaivectorstoresearchresultspage) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

### Search vector store

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/search
```

Search vector store


#### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No | string | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to search. |

#### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | [OpenAI.ComparisonFilter](#openaicomparisonfilter) or [OpenAI.CompoundFilter](#openaicompoundfilter) | A filter to apply based on file attributes. | No |  |
| max_num_results | integer | The maximum number of results to return. This number should be between 1 and 50 inclusive.<br>**Constraints:** min: 1, max: 50 | No | 10 |
| query | string or array of string | A query string for a search | Yes |  |
| ranking_options | [OpenAI.VectorStoreSearchRequestRankingOptions](#openaivectorstoresearchrequestrankingoptions) |  | No |  |
| └─ ranker | enum | <br>Possible values: `none`, `auto`, `default-2024-11-15` | No |  |
| └─ score_threshold | number | **Constraints:** min: 0, max: 1 | No |  |
| rewrite_query | boolean | Whether to rewrite the natural language query for vector search. | No |  |

#### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreSearchResultsPage](#openaivectorstoresearchresultspage) | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |

**Response Headers:**

| Header | Type | Description |
| --- | --- | --- |
| apim-request-id | string | A request ID used for troubleshooting purposes. |

## Components

### AudioSegment

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| avg_logprob | number | The average log probability associated with this audio segment. | Yes |  |
| compression_ratio | number | The compression ratio of this audio segment. | Yes |  |
| end | number | The time at which this segment ended relative to the beginning of the translated audio. | Yes |  |
| id | integer | The 0-based index of this segment within a translation. | Yes |  |
| no_speech_prob | number | The probability of no speech detection within this audio segment. | Yes |  |
| seek | integer | The seek position associated with the processing of this audio segment.<br>Seek positions are expressed as hundredths of seconds.<br>The model may process several segments from a single seek position, so while the seek position will never represent<br>a later time than the segment's start, the segment's start may represent a significantly later time than the<br>segment's associated seek position. | Yes |  |
| start | number | The time at which this segment started relative to the beginning of the translated audio. | Yes |  |
| temperature | number | The temperature score associated with this audio segment. | Yes |  |
| text | string | The translated text that was part of this audio segment. | Yes |  |
| tokens | array of integer | The token IDs matching the translated text in this audio segment. | Yes |  |

### AudioTaskLabel

Defines the possible descriptors for available audio operation responses.

| Property | Value |
|----------|-------|
| **Description** | Defines the possible descriptors for available audio operation responses. |
| **Type** | string |
| **Values** | `transcribe`<br>`translate` |

### AudioTranslationSegment

Extended information about a single segment of translated audio data.
Segments generally represent roughly 5-10 seconds of speech. Segment boundaries typically occur between words but not
necessarily sentences.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| avg_logprob | number | The average log probability associated with this audio segment. | Yes |  |
| compression_ratio | number | The compression ratio of this audio segment. | Yes |  |
| end | number | The time at which this segment ended relative to the beginning of the translated audio. | Yes |  |
| id | integer | The 0-based index of this segment within a translation. | Yes |  |
| no_speech_prob | number | The probability of no speech detection within this audio segment. | Yes |  |
| seek | integer | The seek position associated with the processing of this audio segment.<br>Seek positions are expressed as hundredths of seconds.<br>The model may process several segments from a single seek position, so while the seek position will never represent<br>a later time than the segment's start, the segment's start may represent a significantly later time than the<br>segment's associated seek position. | Yes |  |
| start | number | The time at which this segment started relative to the beginning of the translated audio. | Yes |  |
| temperature | number | The temperature score associated with this audio segment. | Yes |  |
| text | string | The translated text that was part of this audio segment. | Yes |  |
| tokens | array of integer | The token IDs matching the translated text in this audio segment. | Yes |  |

### AzureAIFoundryModelsApiVersion

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `v1`<br>`preview` |

### AzureAudioTranscriptionResponse

Result information for an operation that transcribed spoken audio into written text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| duration | number | The total duration of the audio processed to produce accompanying transcription information. | No |  |
| language | string | The spoken language that was detected in the transcribed audio data.<br>This is expressed as a two-letter ISO-639-1 language code like 'en' or 'fr'. | No |  |
| segments | array of [OpenAI.TranscriptionSegment](#openaitranscriptionsegment) | A collection of information about the timing, probabilities, and other detail of each processed audio segment. | No |  |
| task | [AudioTaskLabel](#audiotasklabel) | Defines the possible descriptors for available audio operation responses. | No |  |
| text | string | The transcribed text for the provided audio data. | Yes |  |
| words | array of [OpenAI.TranscriptionWord](#openaitranscriptionword) | A collection of information about the timing of each processed word. | No |  |

### AzureAudioTranslationResponse

Result information for an operation that translated spoken audio into written text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| duration | number | The total duration of the audio processed to produce accompanying translation information. | No |  |
| language | string | The spoken language that was detected in the translated audio data.<br>This is expressed as a two-letter ISO-639-1 language code like 'en' or 'fr'. | No |  |
| segments | array of [AudioTranslationSegment](#audiotranslationsegment) | A collection of information about the timing, probabilities, and other detail of each processed audio segment. | No |  |
| task | [AudioTaskLabel](#audiotasklabel) | Defines the possible descriptors for available audio operation responses. | No |  |
| text | string | The translated text for the provided audio data. | Yes |  |

### AzureCompletionsSamplingParams

Sampling parameters for controlling the behavior of completions.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completion_tokens | integer |  | No |  |
| max_tokens | integer | The maximum number of tokens in the generated output. | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| response_format | [OpenAI.ResponseFormatText](#openairesponseformattext) or [OpenAI.ResponseFormatJsonSchema](#openairesponseformatjsonschema) or [OpenAI.ResponseFormatJsonObject](#openairesponseformatjsonobject) |  | No |  |
| seed | integer | A seed value initializes the randomness during sampling. | No | 42 |
| temperature | number | A higher temperature increases randomness in the outputs. | No | 1 |
| tools | array of [OpenAI.ChatCompletionTool](#openaichatcompletiontool) |  | No |  |
| top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No | 1 |

### AzureContentFilterBlocklistIdResult

A content filter result item that associates an existing custom blocklist ID with a value indicating whether or not
the corresponding blocklist resulted in content being filtered.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filtered | boolean | Whether the associated blocklist resulted in the content being filtered. | Yes |  |
| id | string | The ID of the custom blocklist associated with the filtered status. | Yes |  |

### AzureContentFilterBlocklistResult

A collection of true/false filtering results for configured custom blocklists.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| details | array of object | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
| filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | Yes |  |

### AzureContentFilterCompletionTextSpan

A representation of a span of completion text as used by Azure OpenAI content filter results.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_end_offset | integer | Offset of the first UTF32 code point which is excluded from the span. This field is always equal to completion_start_offset for empty spans. This field is always larger than completion_start_offset for non-empty spans. | Yes |  |
| completion_start_offset | integer | Offset of the UTF32 code point which begins the span. | Yes |  |

### AzureContentFilterCompletionTextSpanDetectionResult

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| details | array of [AzureContentFilterCompletionTextSpan](#azurecontentfiltercompletiontextspan) | Detailed information about the detected completion text spans. | Yes |  |
| detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |

### AzureContentFilterCustomTopicIdResult

A content filter result item that associates an existing custom topic ID with a value indicating whether or not
the corresponding topic resulted in content being detected.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detected | boolean | Whether the associated custom topic resulted in the content being detected. | Yes |  |
| id | string | The ID of the custom topic associated with the detected status. | Yes |  |

### AzureContentFilterCustomTopicResult

A collection of true/false filtering results for configured custom topics.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| details | array of object | The pairs of individual topic IDs and whether they are detected. | No |  |
| filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | Yes |  |

### AzureContentFilterDetectionResult

A labeled content filter result item that indicates whether the content was detected and whether the content was
filtered.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |

### AzureContentFilterForResponsesAPI

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| blocked | boolean | Indicate if the response is blocked. | Yes |  |
| content_filter_offsets | [AzureContentFilterResultOffsets](#azurecontentfilterresultoffsets) |  | Yes |  |
| content_filter_results | [AzureContentFilterResultsForResponsesAPI](#azurecontentfilterresultsforresponsesapi) |  | Yes |  |
| └─ custom_blocklists | [AzureContentFilterBlocklistResult](#azurecontentfilterblocklistresult) | A collection of binary filtering outcomes for configured custom blocklists. | No |  |
| └─ custom_topics | [AzureContentFilterCustomTopicResult](#azurecontentfiltercustomtopicresult) | A collection of binary filtering outcomes for configured custom topics. | No |  |
| └─ error | object | If present, details about an error that prevented content filtering from completing its evaluation. | No |  |
|   └─ code | integer | A distinct, machine-readable code associated with the error. | Yes |  |
|   └─ message | string | A human-readable message associated with the error. | Yes |  |
| └─ hate | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A content filter category that can refer to any content that attacks or uses pejorative or discriminatory<br>language with reference to a person or identity group based on certain differentiating attributes of these groups<br>including but not limited to race, ethnicity, nationality, gender identity and expression, sexual orientation,<br>religion, immigration status, ability status, personal appearance, and body size. | No |  |
| └─ indirect_attack | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A detection result that describes attacks on systems powered by Generative AI models that can happen every time<br>an application processes information that wasn’t directly authored by either the developer of the application or<br>the user. | No |  |
| └─ jailbreak | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A detection result that describes user prompt injection attacks, where malicious users deliberately exploit<br>system vulnerabilities to elicit unauthorized behavior from the LLM. This could lead to inappropriate content<br>generation or violations of system-imposed restrictions. | Yes |  |
| └─ personally_identifiable_information | [AzureContentFilterPersonallyIdentifiableInformationResult](#azurecontentfilterpersonallyidentifiableinformationresult) | A detection result that describes matches against Personal Identifiable Information with configurable subcategories. | No |  |
| └─ profanity | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A detection result that identifies whether crude, vulgar, or otherwise objection language is present in the<br>content. | No |  |
| └─ protected_material_code | object | A detection result that describes a match against licensed code or other protected source material. | No |  |
|   └─ citation | object | If available, the citation details describing the associated license and its location. | No |  |
|     └─ URL | string | The URL associated with the license. | No |  |
|     └─ license | string | The name or identifier of the license associated with the detection. | No |  |
|   └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
|   └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| └─ protected_material_text | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A detection result that describes a match against text protected under copyright or other status. | No |  |
| └─ self_harm | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A content filter category that describes language related to physical actions intended to purposely hurt, injure,<br>damage one's body or kill oneself. | No |  |
| └─ sexual | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A content filter category for language related to anatomical organs and genitals, romantic relationships, acts<br>portrayed in erotic or affectionate terms, pregnancy, physical sexual acts, including those portrayed as an<br>assault or a forced sexual violent act against one's will, prostitution, pornography, and abuse. | No |  |
| └─ task_adherence | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A detection result that indicates if the execution flow still sticks the plan. | Yes |  |
| └─ ungrounded_material | [AzureContentFilterCompletionTextSpanDetectionResult](#azurecontentfiltercompletiontextspandetectionresult) |  | No |  |
| └─ violence | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A content filter category for language related to physical actions intended to hurt, injure, damage, or kill<br>someone or something; describes weapons, guns and related entities, such as manufactures, associations,<br>legislation, and so on. | No |  |
| source_type | string | The name of the source type of the message. | Yes |  |

### AzureContentFilterHarmExtensions

Extensions for harm categories, providing additional configuration options.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| pii_sub_categories | array of [AzurePiiSubCategory](#azurepiisubcategory) | Configuration for PIIHarmSubCategory(s). | No |  |

### AzureContentFilterImagePromptResults

A content filter result for an image generation operation's input request content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom_blocklists | [AzureContentFilterBlocklistResult](#azurecontentfilterblocklistresult) | A collection of true/false filtering results for configured custom blocklists. | No |  |
| └─ details | array of object | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
|   └─ filtered | boolean | A value indicating whether the blocklist produced a filtering action. | Yes |  |
|   └─ id | string | The ID of the custom blocklist evaluated. | Yes |  |
| └─ filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | Yes |  |
| custom_topics | [AzureContentFilterCustomTopicResult](#azurecontentfiltercustomtopicresult) | A collection of true/false filtering results for configured custom topics. | No |  |
| └─ details | array of object | The pairs of individual topic IDs and whether they are detected. | No |  |
|   └─ detected | boolean | A value indicating whether the topic is detected. | Yes |  |
|   └─ id | string | The ID of the custom topic evaluated. | Yes |  |
| └─ filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | Yes |  |
| hate | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| jailbreak | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | Yes |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| profanity | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| self_harm | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| sexual | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| violence | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |

### AzureContentFilterImageResponseResults

A content filter result for an image generation operation's output response content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hate | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| self_harm | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| sexual | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| violence | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |

### AzureContentFilterPersonallyIdentifiableInformationResult

A content filter detection result for Personally Identifiable Information that includes harm extensions.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| redacted_text | string | The redacted text with PII information removed or masked. | No |  |
| sub_categories | array of [AzurePiiSubCategoryResult](#azurepiisubcategoryresult) | Detailed results for individual PIIHarmSubCategory(s). | No |  |

### AzureContentFilterResultForChoice

A content filter result for a single response item produced by a generative AI system.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom_blocklists | [AzureContentFilterBlocklistResult](#azurecontentfilterblocklistresult) | A collection of true/false filtering results for configured custom blocklists. | No |  |
| └─ details | array of object | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
|   └─ filtered | boolean | A value indicating whether the blocklist produced a filtering action. | Yes |  |
|   └─ id | string | The ID of the custom blocklist evaluated. | Yes |  |
| └─ filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | Yes |  |
| custom_topics | [AzureContentFilterCustomTopicResult](#azurecontentfiltercustomtopicresult) | A collection of true/false filtering results for configured custom topics. | No |  |
| └─ details | array of object | The pairs of individual topic IDs and whether they are detected. | No |  |
|   └─ detected | boolean | A value indicating whether the topic is detected. | Yes |  |
|   └─ id | string | The ID of the custom topic evaluated. | Yes |  |
| └─ filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | Yes |  |
| error | object | If present, details about an error that prevented content filtering from completing its evaluation. | No |  |
| └─ code | integer | A distinct, machine-readable code associated with the error. | Yes |  |
| └─ message | string | A human-readable message associated with the error. | Yes |  |
| hate | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| personally_identifiable_information | [AzureContentFilterPersonallyIdentifiableInformationResult](#azurecontentfilterpersonallyidentifiableinformationresult) | A content filter detection result for Personally Identifiable Information that includes harm extensions. | No |  |
| └─ redacted_text | string | The redacted text with PII information removed or masked. | No |  |
| └─ sub_categories | array of [AzurePiiSubCategoryResult](#azurepiisubcategoryresult) | Detailed results for individual PIIHarmSubCategory(s). | No |  |
| profanity | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| protected_material_code | object | A detection result that describes a match against licensed code or other protected source material. | No |  |
| └─ citation | object | If available, the citation details describing the associated license and its location. | No |  |
|   └─ URL | string | The URL associated with the license. | No |  |
|   └─ license | string | The name or identifier of the license associated with the detection. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| protected_material_text | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| self_harm | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| sexual | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| ungrounded_material | [AzureContentFilterCompletionTextSpanDetectionResult](#azurecontentfiltercompletiontextspandetectionresult) |  | No |  |
| violence | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |

### AzureContentFilterResultForPrompt

A content filter result associated with a single input prompt item into a generative AI system.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_filter_results | object | The content filter category details for the result. | No |  |
| └─ custom_blocklists | [AzureContentFilterBlocklistResult](#azurecontentfilterblocklistresult) | A collection of true/false filtering results for configured custom blocklists. | No |  |
|   └─ details | array of object | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
|     └─ filtered | boolean | A value indicating whether the blocklist produced a filtering action. | Yes |  |
|     └─ id | string | The ID of the custom blocklist evaluated. | Yes |  |
|   └─ filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | Yes |  |
| └─ custom_topics | [AzureContentFilterCustomTopicResult](#azurecontentfiltercustomtopicresult) | A collection of true/false filtering results for configured custom topics. | No |  |
|   └─ details | array of object | The pairs of individual topic IDs and whether they are detected. | No |  |
|     └─ detected | boolean | A value indicating whether the topic is detected. | Yes |  |
|     └─ id | string | The ID of the custom topic evaluated. | Yes |  |
|   └─ filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | Yes |  |
| └─ error | object | If present, details about an error that prevented content filtering from completing its evaluation. | No |  |
|   └─ code | integer | A distinct, machine-readable code associated with the error. | Yes |  |
|   └─ message | string | A human-readable message associated with the error. | Yes |  |
| └─ hate | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| └─ indirect_attack | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | Yes |  |
|   └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
|   └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| └─ jailbreak | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | Yes |  |
|   └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
|   └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| └─ profanity | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
|   └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
|   └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| └─ self_harm | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| └─ sexual | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| └─ violence | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| prompt_index | integer | The index of the input prompt associated with the accompanying content filter result categories. | No |  |

### AzureContentFilterResultOffsets

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| check_offset | integer |  | Yes |  |
| end_offset | integer |  | Yes |  |
| start_offset | integer |  | Yes |  |

### AzureContentFilterResultsForResponsesAPI

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom_blocklists | [AzureContentFilterBlocklistResult](#azurecontentfilterblocklistresult) | A collection of true/false filtering results for configured custom blocklists. | No |  |
| └─ details | array of object | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
|   └─ filtered | boolean | A value indicating whether the blocklist produced a filtering action. | Yes |  |
|   └─ id | string | The ID of the custom blocklist evaluated. | Yes |  |
| └─ filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | Yes |  |
| custom_topics | [AzureContentFilterCustomTopicResult](#azurecontentfiltercustomtopicresult) | A collection of true/false filtering results for configured custom topics. | No |  |
| └─ details | array of object | The pairs of individual topic IDs and whether they are detected. | No |  |
|   └─ detected | boolean | A value indicating whether the topic is detected. | Yes |  |
|   └─ id | string | The ID of the custom topic evaluated. | Yes |  |
| └─ filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | Yes |  |
| error | object | If present, details about an error that prevented content filtering from completing its evaluation. | No |  |
| └─ code | integer | A distinct, machine-readable code associated with the error. | Yes |  |
| └─ message | string | A human-readable message associated with the error. | Yes |  |
| hate | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| indirect_attack | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| jailbreak | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | Yes |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| personally_identifiable_information | [AzureContentFilterPersonallyIdentifiableInformationResult](#azurecontentfilterpersonallyidentifiableinformationresult) | A content filter detection result for Personally Identifiable Information that includes harm extensions. | No |  |
| └─ redacted_text | string | The redacted text with PII information removed or masked. | No |  |
| └─ sub_categories | array of [AzurePiiSubCategoryResult](#azurepiisubcategoryresult) | Detailed results for individual PIIHarmSubCategory(s). | No |  |
| profanity | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| protected_material_code | object | A detection result that describes a match against licensed code or other protected source material. | No |  |
| └─ citation | object | If available, the citation details describing the associated license and its location. | No |  |
|   └─ URL | string | The URL associated with the license. | No |  |
|   └─ license | string | The name or identifier of the license associated with the detection. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| protected_material_text | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| self_harm | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| sexual | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |
| task_adherence | [AzureContentFilterDetectionResult](#azurecontentfilterdetectionresult) | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | Yes |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |
| ungrounded_material | [AzureContentFilterCompletionTextSpanDetectionResult](#azurecontentfiltercompletiontextspandetectionresult) |  | No |  |
| violence | [AzureContentFilterSeverityResult](#azurecontentfilterseverityresult) | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |

### AzureContentFilterSeverityResult

A labeled content filter result item that indicates whether the content was filtered and what the qualitative
severity level of the content was, as evaluated against content filter configuration for the category.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |

### AzureFileExpiryAnchor

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `created_at` |

### AzureFineTuneReinforcementMethod

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [OpenAI.GraderMulti](#openaigradermulti) or [GraderEndpoint](#graderendpoint) |  | Yes |  |
| hyperparameters | [OpenAI.FineTuneReinforcementHyperparameters](#openaifinetunereinforcementhyperparameters) | The hyperparameters used for the reinforcement fine-tuning job. | No |  |
| response_format | [ResponseFormatJSONSchemaRequest](#responseformatjsonschemarequest) |  | No |  |
| └─ json_schema | object | JSON Schema for the response format | Yes |  |
| └─ type | enum | Type of response format<br>Possible values: `json_schema` | Yes |  |

### AzurePiiSubCategory

Configuration for individual PIIHarmSubCategory(s) within the harm extensions framework.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detect | boolean | Whether detection is enabled for this subcategory. | Yes |  |
| filter | boolean | Whether content containing this subcategory should be blocked. | Yes |  |
| redact | boolean | Whether content containing this subcategory should be redacted. | Yes |  |
| sub_category | string | The PIIHarmSubCategory being configured. | Yes |  |

### AzurePiiSubCategoryResult

Result details for individual PIIHarmSubCategory(s).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detected | boolean | Whether the labeled content subcategory was detected in the content. | Yes |  |
| filtered | boolean | Whether the content detection resulted in a content filtering action for this subcategory. | Yes |  |
| redacted | boolean | Whether the content was redacted for this subcategory. | Yes |  |
| sub_category | string | The PIIHarmSubCategory that was evaluated. | Yes |  |

### AzureResponsesSamplingParams

Sampling parameters for controlling the behavior of responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_tokens | integer | The maximum number of tokens in the generated output. | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| seed | integer | A seed value initializes the randomness during sampling. | No | 42 |
| temperature | number | A higher temperature increases randomness in the outputs. | No | 1 |
| text | [OpenAI.CreateEvalResponsesRunDataSourceSamplingParamsText](#openaicreateevalresponsesrundatasourcesamplingparamstext) |  | No |  |
| tools | array of [OpenAI.Tool](#openaitool) |  | No |  |
| top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No | 1 |

### AzureUserSecurityContext

User security context contains several parameters that describe the application itself, and the end user that interacts with the application. These fields assist your security operations teams to investigate and mitigate security incidents by providing a comprehensive approach to protecting your AI applications. [Learn more](https://aka.ms/TP4AI/Documentation/EndUserContext) about protecting AI applications using Microsoft Defender for Cloud.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| application_name | string | The name of the application. Sensitive personal information should not be included in this field. | No |  |
| end_user_id | string | This identifier is the Microsoft Entra ID (formerly Azure Active Directory) user object ID used to authenticate end-users within the generative AI application. Sensitive personal information should not be included in this field. | No |  |
| end_user_tenant_id | string | The Microsoft 365 tenant ID the end user belongs to. It's required when the generative AI application is multitenant. | No |  |
| source_ip | string | Captures the original client's IP address. | No |  |

### CopiedAccountDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| destinationResourceId | string | The ID of the destination resource where the model was copied to. | Yes |  |
| region | string | The region where the model was copied to. | Yes |  |
| status | enum | The status of the copy operation.<br>Possible values: `Completed`, `Failed`, `InProgress` | Yes |  |

### CopyModelRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| destinationResourceId | string | The ID of the destination Resource to copy. | Yes |  |
| region | string | The region to copy the model to. | Yes |  |

### CopyModelResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| checkpointedModelName | string | The ID of the copied model. | Yes |  |
| copiedAccountDetails | array of [CopiedAccountDetails](#copiedaccountdetails) | The ID of the destination resource id where it was copied | Yes |  |
| fineTuningJobId | string | The ID of the fine-tuning job that the checkpoint was copied from. | Yes |  |

### CreateVideoBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| model | string | The name of the deployment to use for this request. | Yes |  |
| prompt | string | Text prompt that describes the video to generate.<br>**Constraints:** minLength: 1 | Yes |  |
| seconds | [VideoSeconds](#videoseconds) | Supported clip durations, measured in seconds. | No | 4 |
| size | [VideoSize](#videosize) | Output dimensions formatted as `{width}x{height}`. | No | 720x1280 |

### CreateVideoBodyWithInputReference

The properties of a video generation job request with media files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_reference | object | Optional image reference that guides generation. | Yes |  |
| model | object | The name of the deployment to use for this request. | Yes |  |
| prompt | object | Text prompt that describes the video to generate. | Yes |  |
| seconds | object | Clip duration in seconds. Defaults to 4 seconds. | No |  |
| size | object | Output resolution formatted as width x height. Defaults to 720x1280. | No |  |

### CreateVideoRemixBody

Parameters for remixing an existing generated video.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prompt | string | Updated text prompt that directs the remix generation.<br>**Constraints:** minLength: 1 | Yes |  |

### DeletedVideoResource

Confirmation payload returned after deleting a video.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Indicates that the video resource was deleted. | Yes | True |
| id | string | Identifier of the deleted video. | Yes |  |
| object | string | The object type that signals the deletion response. | Yes | video.deleted |

### Error

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string |  | Yes |  |
| message | string |  | Yes |  |

### EvalGraderEndpoint

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| headers | object or null | Optional HTTP headers to include in requests to the endpoint | No |  |
| name | string | The name of the grader | Yes |  |
| pass_threshold | number or null | Optional threshold score above which the grade is considered passing<br>If not specified, all scores are considered valid | No |  |
| rate_limit | integer or null | Optional rate limit for requests per second to the endpoint<br>Must be a positive integer | No |  |
| type | enum | <br>Possible values: `endpoint` | Yes |  |
| url | string | The HTTPS URL of the endpoint to call for grading<br>**Constraints:** pattern: `^https://` | Yes |  |

### GraderEndpoint

Endpoint grader configuration for external HTTP endpoint evaluation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| headers | object or null | Optional HTTP headers to include in requests to the endpoint | No |  |
| name | string | The name of the grader | Yes |  |
| pass_threshold | number or null | Optional threshold score above which the grade is considered passing<br>If not specified, all scores are considered valid | No |  |
| rate_limit | integer or null | Optional rate limit for requests per second to the endpoint<br>Must be a positive integer | No |  |
| type | enum | <br>Possible values: `endpoint` | Yes |  |
| url | string | The HTTPS URL of the endpoint to call for grading<br>**Constraints:** pattern: `^https://` | Yes |  |

### OpenAI.Annotation

An annotation that applies to a span of output text.


### Discriminator for OpenAI.Annotation

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `file_citation` | [OpenAI.FileCitationBody](#openaifilecitationbody) |
| `url_citation` | [OpenAI.UrlCitationBody](#openaiurlcitationbody) |
| `container_file_citation` | [OpenAI.ContainerFileCitationBody](#openaicontainerfilecitationbody) |
| `file_path` | [OpenAI.FilePath](#openaifilepath) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.AnnotationType](#openaiannotationtype) |  | Yes |  |

### OpenAI.AnnotationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `file_citation`<br>`url_citation`<br>`container_file_citation`<br>`file_path` |

### OpenAI.ApplyPatchCallOutputStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `completed`<br>`failed` |

### OpenAI.ApplyPatchCallStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed` |

### OpenAI.ApplyPatchCreateFileOperation

Instruction describing how to create a file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| diff | string | Diff to apply. | Yes |  |
| path | string | Path of the file to create. | Yes |  |
| type | enum | Create a new file with the provided diff.<br>Possible values: `create_file` | Yes |  |

### OpenAI.ApplyPatchDeleteFileOperation

Instruction describing how to delete a file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| path | string | Path of the file to delete. | Yes |  |
| type | enum | Delete the specified file.<br>Possible values: `delete_file` | Yes |  |

### OpenAI.ApplyPatchFileOperation

One of the create_file, delete_file, or update_file operations applied via apply_patch.


### Discriminator for OpenAI.ApplyPatchFileOperation

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `create_file` | [OpenAI.ApplyPatchCreateFileOperation](#openaiapplypatchcreatefileoperation) |
| `delete_file` | [OpenAI.ApplyPatchDeleteFileOperation](#openaiapplypatchdeletefileoperation) |
| `update_file` | [OpenAI.ApplyPatchUpdateFileOperation](#openaiapplypatchupdatefileoperation) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |

### OpenAI.ApplyPatchFileOperationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `create_file`<br>`delete_file`<br>`update_file` |

### OpenAI.ApplyPatchToolParam

Allows the assistant to create, delete, or update files using unified diffs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the tool. Always `apply_patch`.<br>Possible values: `apply_patch` | Yes |  |

### OpenAI.ApplyPatchUpdateFileOperation

Instruction describing how to update a file via the apply_patch tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| diff | string | Diff to apply. | Yes |  |
| path | string | Path of the file to update. | Yes |  |
| type | enum | Update an existing file with the provided diff.<br>Possible values: `update_file` | Yes |  |

### OpenAI.ApproximateLocation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| city | string or null |  | No |  |
| country | string or null |  | No |  |
| region | string or null |  | No |  |
| timezone | string or null |  | No |  |
| type | enum | The type of location approximation. Always `approximate`.<br>Possible values: `approximate` | Yes |  |

### OpenAI.AssistantTool


### Discriminator for OpenAI.AssistantTool

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `code_interpreter` | [OpenAI.AssistantToolsCode](#openaiassistanttoolscode) |
| `file_search` | [OpenAI.AssistantToolsFileSearch](#openaiassistanttoolsfilesearch) |
| `function` | [OpenAI.AssistantToolsFunction](#openaiassistanttoolsfunction) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.AssistantToolType](#openaiassistanttooltype) |  | Yes |  |

### OpenAI.AssistantToolType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `code_interpreter`<br>`file_search`<br>`function` |

### OpenAI.AssistantToolsCode

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of tool being defined: `code_interpreter`<br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.AssistantToolsFileSearch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_search | [OpenAI.AssistantToolsFileSearchFileSearch](#openaiassistanttoolsfilesearchfilesearch) |  | No |  |
| └─ max_num_results | integer | **Constraints:** min: 1, max: 50 | No |  |
| └─ ranking_options | [OpenAI.FileSearchRankingOptions](#openaifilesearchrankingoptions) | The ranking options for the file search. If not specified, the file search tool will use the `auto` ranker and a score_threshold of 0.<br>See the [file search tool documentation](https://platform.openai.com/docs/assistants/tools/file-search#customizing-file-search-settings) for more information. | No |  |
| type | enum | The type of tool being defined: `file_search`<br>Possible values: `file_search` | Yes |  |

### OpenAI.AssistantToolsFileSearchFileSearch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_num_results | integer | **Constraints:** min: 1, max: 50 | No |  |
| ranking_options | [OpenAI.FileSearchRankingOptions](#openaifilesearchrankingoptions) | The ranking options for the file search. If not specified, the file search tool will use the `auto` ranker and a score_threshold of 0.<br>See the [file search tool documentation](https://platform.openai.com/docs/assistants/tools/file-search#customizing-file-search-settings) for more information. | No |  |

### OpenAI.AssistantToolsFileSearchTypeOnly

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of tool being defined: `file_search`<br>Possible values: `file_search` | Yes |  |

### OpenAI.AssistantToolsFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.FunctionObject](#openaifunctionobject) |  | Yes |  |
| type | enum | The type of tool being defined: `function`<br>Possible values: `function` | Yes |  |

### OpenAI.AssistantsApiResponseFormatOption

Specifies the format that the model must output. Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.
Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensure the model will match your supplied JSON schema. Learn more in the 
Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the message the model generates is valid JSON.
*Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length.

**Type**: string or [OpenAI.ResponseFormatText](#openairesponseformattext) or [OpenAI.ResponseFormatJsonObject](#openairesponseformatjsonobject) or [OpenAI.ResponseFormatJsonSchema](#openairesponseformatjsonschema)

Specifies the format that the model must output. Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.
Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensure the model will match your supplied JSON schema. Learn more in the 
Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the message the model generates is valid JSON.
*Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length.


### OpenAI.AssistantsApiToolChoiceOption

Controls which (if any) tool is called by the model.
`none` means the model will not call any tools and instead generates a message.
`auto` is the default value and means the model can pick between generating a message or calling one or more tools.
`required` means the model must call one or more tools before responding to the user.
Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.

**Type**: string or [OpenAI.AssistantsNamedToolChoice](#openaiassistantsnamedtoolchoice)

Controls which (if any) tool is called by the model.
`none` means the model will not call any tools and instead generates a message.
`auto` is the default value and means the model can pick between generating a message or calling one or more tools.
`required` means the model must call one or more tools before responding to the user.
Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.


### OpenAI.AssistantsNamedToolChoice

Specifies a tool the model should use. Use to force the model to call a specific tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.AssistantsNamedToolChoiceFunction](#openaiassistantsnamedtoolchoicefunction) |  | No |  |
| type | enum | The type of the tool. If type is `function`, the function name must be set<br>Possible values: `function`, `code_interpreter`, `file_search` | Yes |  |

### OpenAI.AssistantsNamedToolChoiceFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string |  | Yes |  |

### OpenAI.AudioTranscription

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| language | string | The language of the input audio. Supplying the input language in<br>  [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format<br>  will improve accuracy and latency. | No |  |
| model | string | The model to use for transcription. Current options are `whisper-1`, `gpt-4o-mini-transcribe`, `gpt-4o-mini-transcribe-2025-12-15`, `gpt-4o-transcribe`, and `gpt-4o-transcribe-diarize`. Use `gpt-4o-transcribe-diarize` when you need diarization with speaker labels. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio<br>  segment.<br>  For `whisper-1`, the [prompt is a list of keywords](https://platform.openai.com/docs/guides/speech-to-text#prompting).<br>  For `gpt-4o-transcribe` models (excluding `gpt-4o-transcribe-diarize`), the prompt is a free text string, for example "expect words related to technology". | No |  |

### OpenAI.AutoChunkingStrategyRequestParam

The default strategy. This strategy currently uses a `max_chunk_size_tokens` of `800` and `chunk_overlap_tokens` of `400`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Always `auto`.<br>Possible values: `auto` | Yes |  |

### OpenAI.Batch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cancelled_at | integer | The Unix timestamp (in seconds) for when the batch was cancelled. | No |  |
| cancelling_at | integer | The Unix timestamp (in seconds) for when the batch started cancelling. | No |  |
| completed_at | integer | The Unix timestamp (in seconds) for when the batch was completed. | No |  |
| completion_window | string | The time frame within which the batch should be processed. | Yes |  |
| created_at | integer | The Unix timestamp (in seconds) for when the batch was created. | Yes |  |
| endpoint | string | The OpenAI API endpoint used by the batch. | Yes |  |
| error_file_id | string | The ID of the file containing the outputs of requests with errors. | No |  |
| errors | [OpenAI.BatchErrors](#openaibatcherrors) |  | No |  |
| expired_at | integer | The Unix timestamp (in seconds) for when the batch expired. | No |  |
| expires_at | integer | The Unix timestamp (in seconds) for when the batch will expire. | No |  |
| failed_at | integer | The Unix timestamp (in seconds) for when the batch failed. | No |  |
| finalizing_at | integer | The Unix timestamp (in seconds) for when the batch started finalizing. | No |  |
| id | string |  | Yes |  |
| in_progress_at | integer | The Unix timestamp (in seconds) for when the batch started processing. | No |  |
| input_file_id | string or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | Model ID used to process the batch, like `gpt-5-2025-08-07`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model<br>  guide](https://platform.openai.com/docs/models) to browse and compare available models. | No |  |
| object | enum | The object type, which is always `batch`.<br>Possible values: `batch` | Yes |  |
| output_file_id | string | The ID of the file containing the outputs of successfully executed requests. | No |  |
| request_counts | [OpenAI.BatchRequestCounts](#openaibatchrequestcounts) | The request counts for different statuses within the batch. | No |  |
| status | enum | The current status of the batch.<br>Possible values: `validating`, `failed`, `in_progress`, `finalizing`, `completed`, `expired`, `cancelling`, `cancelled` | Yes |  |
| usage | [OpenAI.BatchUsage](#openaibatchusage) |  | No |  |
| └─ input_tokens | integer |  | Yes |  |
| └─ input_tokens_details | [OpenAI.BatchUsageInputTokensDetails](#openaibatchusageinputtokensdetails) |  | Yes |  |
| └─ output_tokens | integer |  | Yes |  |
| └─ output_tokens_details | [OpenAI.BatchUsageOutputTokensDetails](#openaibatchusageoutputtokensdetails) |  | Yes |  |
| └─ total_tokens | integer |  | Yes |  |

### OpenAI.BatchError

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | An error code identifying the error type. | No |  |
| line | integer or null |  | No |  |
| message | string | A human-readable message providing more details about the error. | No |  |
| param | string or null |  | No |  |

### OpenAI.BatchErrors

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.BatchError](#openaibatcherror) |  | No |  |
| object | string |  | No |  |

### OpenAI.BatchRequestCounts

The request counts for different statuses within the batch.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completed | integer | Number of requests that have been completed successfully. | Yes |  |
| failed | integer | Number of requests that have failed. | Yes |  |
| total | integer | Total number of requests in the batch. | Yes |  |

### OpenAI.BatchUsage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_tokens | integer |  | Yes |  |
| input_tokens_details | [OpenAI.BatchUsageInputTokensDetails](#openaibatchusageinputtokensdetails) |  | Yes |  |
| output_tokens | integer |  | Yes |  |
| output_tokens_details | [OpenAI.BatchUsageOutputTokensDetails](#openaibatchusageoutputtokensdetails) |  | Yes |  |
| total_tokens | integer |  | Yes |  |

### OpenAI.BatchUsageInputTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cached_tokens | integer |  | Yes |  |

### OpenAI.BatchUsageOutputTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reasoning_tokens | integer |  | Yes |  |

### OpenAI.ChatCompletionAllowedTools

Constrains the tools available to the model to a predefined set.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| mode | enum | Constrains the tools available to the model to a predefined set.<br>  `auto` allows the model to pick from among the allowed tools and generate a<br>  message.<br>  `required` requires the model to call one or more of the allowed tools.<br>Possible values: `auto`, `required` | Yes |  |
| tools | array of object | A list of tool definitions that the model should be allowed to call.<br>  For the Chat Completions API, the list of tool definitions might look like:<br>  ```json<br>  [<br>    { "type": "function", "function": { "name": "get_weather" } },<br>    { "type": "function", "function": { "name": "get_time" } }<br>  ]<br>  ``` | Yes |  |

### OpenAI.ChatCompletionAllowedToolsChoice

Constrains the tools available to the model to a predefined set.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| allowed_tools | [OpenAI.ChatCompletionAllowedTools](#openaichatcompletionallowedtools) | Constrains the tools available to the model to a predefined set. | Yes |  |
| type | enum | Allowed tool configuration type. Always `allowed_tools`.<br>Possible values: `allowed_tools` | Yes |  |

### OpenAI.ChatCompletionFunctionCallOption

Specifying a particular function via `{"name": "my_function"}` forces the model to call that function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the function to call. | Yes |  |

### OpenAI.ChatCompletionFunctions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| name | string | The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64. | Yes |  |
| parameters | [OpenAI.FunctionParameters](#openaifunctionparameters) | The parameters the functions accepts, described as a JSON Schema object. See the [guide](https://platform.openai.com/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.<br>Omitting `parameters` defines a function with an empty parameter list. | No |  |

### OpenAI.ChatCompletionMessageCustomToolCall

A call to a custom tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom | [OpenAI.ChatCompletionMessageCustomToolCallCustom](#openaichatcompletionmessagecustomtoolcallcustom) |  | Yes |  |
| └─ input | string |  | Yes |  |
| └─ name | string |  | Yes |  |
| id | string | The ID of the tool call. | Yes |  |
| type | enum | The type of the tool. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.ChatCompletionMessageCustomToolCallCustom

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string |  | Yes |  |
| name | string |  | Yes |  |

### OpenAI.ChatCompletionMessageToolCall

A call to a function tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.ChatCompletionMessageToolCallFunction](#openaichatcompletionmessagetoolcallfunction) |  | Yes |  |
| └─ arguments | string |  | Yes |  |
| └─ name | string |  | Yes |  |
| id | string | The ID of the tool call. | Yes |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatCompletionMessageToolCallChunk

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.ChatCompletionMessageToolCallChunkFunction](#openaichatcompletionmessagetoolcallchunkfunction) |  | No |  |
| id | string | The ID of the tool call. | No |  |
| index | integer |  | Yes |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | No |  |

### OpenAI.ChatCompletionMessageToolCallChunkFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string |  | No |  |
| name | string |  | No |  |

### OpenAI.ChatCompletionMessageToolCallFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string |  | Yes |  |
| name | string |  | Yes |  |

### OpenAI.ChatCompletionMessageToolCalls

The tool calls generated by the model, such as function calls.


### OpenAI.ChatCompletionMessageToolCallsItem

The tool calls generated by the model, such as function calls.


### OpenAI.ChatCompletionNamedToolChoice

Specifies a tool the model should use. Use to force the model to call a specific function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.ChatCompletionNamedToolChoiceFunction](#openaichatcompletionnamedtoolchoicefunction) |  | Yes |  |
| type | enum | For function calling, the type is always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatCompletionNamedToolChoiceCustom

Specifies a tool the model should use. Use to force the model to call a specific custom tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom | [OpenAI.ChatCompletionNamedToolChoiceCustomCustom](#openaichatcompletionnamedtoolchoicecustomcustom) |  | Yes |  |
| type | enum | For custom tool calling, the type is always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.ChatCompletionNamedToolChoiceCustomCustom

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string |  | Yes |  |

### OpenAI.ChatCompletionNamedToolChoiceFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string |  | Yes |  |

### OpenAI.ChatCompletionRequestAssistantMessage

Messages sent by the model in response to user messages.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | [OpenAI.ChatCompletionRequestAssistantMessageAudio](#openaichatcompletionrequestassistantmessageaudio) or null | Data about a previous audio response from the model. | No |  |
| content | string or array of [OpenAI.ChatCompletionRequestAssistantMessageContentPart](#openaichatcompletionrequestassistantmessagecontentpart) or null |  | No |  |
| function_call | [OpenAI.ChatCompletionRequestAssistantMessageFunctionCall](#openaichatcompletionrequestassistantmessagefunctioncall) or null |  | No |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| refusal | string or null |  | No |  |
| role | enum | The role of the messages author, in this case `assistant`.<br>Possible values: `assistant` | Yes |  |
| tool_calls | [OpenAI.ChatCompletionMessageToolCalls](#openaichatcompletionmessagetoolcalls) | The tool calls generated by the model, such as function calls. | No |  |

### OpenAI.ChatCompletionRequestAssistantMessageAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string |  | Yes |  |

### OpenAI.ChatCompletionRequestAssistantMessageContentPart


### Discriminator for OpenAI.ChatCompletionRequestAssistantMessageContentPart

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `refusal` | [OpenAI.ChatCompletionRequestMessageContentPartRefusal](#openaichatcompletionrequestmessagecontentpartrefusal) |
| `text` | [OpenAI.ChatCompletionRequestAssistantMessageContentPartChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestassistantmessagecontentpartchatcompletionrequestmessagecontentparttext) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ChatCompletionRequestAssistantMessageContentPartType](#openaichatcompletionrequestassistantmessagecontentparttype) |  | Yes |  |

### OpenAI.ChatCompletionRequestAssistantMessageContentPartChatCompletionRequestMessageContentPartText

Learn about [text inputs](https://platform.openai.com/docs/guides/text-generation).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text content. | Yes |  |
| type | enum | The type of the content part.<br>Possible values: `text` | Yes |  |

### OpenAI.ChatCompletionRequestAssistantMessageContentPartType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`refusal` |

### OpenAI.ChatCompletionRequestAssistantMessageFunctionCall

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string |  | Yes |  |
| name | string |  | Yes |  |

### OpenAI.ChatCompletionRequestDeveloperMessage

Developer-provided instructions that the model should follow, regardless of
messages sent by the user. With o1 models and newer, `developer` messages
replace the previous `system` messages.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array of [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext) | The contents of the developer message. | Yes |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| role | enum | The role of the messages author, in this case `developer`.<br>Possible values: `developer` | Yes |  |

### OpenAI.ChatCompletionRequestFunctionMessage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or null |  | Yes |  |
| name | string | The name of the function to call. | Yes |  |
| role | enum | The role of the messages author, in this case `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatCompletionRequestMessage


### Discriminator for OpenAI.ChatCompletionRequestMessage

This component uses the property `role` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `assistant` | [OpenAI.ChatCompletionRequestAssistantMessage](#openaichatcompletionrequestassistantmessage) |
| `developer` | [OpenAI.ChatCompletionRequestDeveloperMessage](#openaichatcompletionrequestdevelopermessage) |
| `function` | [OpenAI.ChatCompletionRequestFunctionMessage](#openaichatcompletionrequestfunctionmessage) |
| `system` | [OpenAI.ChatCompletionRequestSystemMessage](#openaichatcompletionrequestsystemmessage) |
| `user` | [OpenAI.ChatCompletionRequestUserMessage](#openaichatcompletionrequestusermessage) |
| `tool` | [OpenAI.ChatCompletionRequestToolMessage](#openaichatcompletionrequesttoolmessage) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| role | [OpenAI.ChatCompletionRequestMessageType](#openaichatcompletionrequestmessagetype) |  | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_audio | [OpenAI.ChatCompletionRequestMessageContentPartAudioInputAudio](#openaichatcompletionrequestmessagecontentpartaudioinputaudio) |  | Yes |  |
| type | enum | The type of the content part. Always `input_audio`.<br>Possible values: `input_audio` | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartAudioInputAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string |  | Yes |  |
| format | enum | <br>Possible values: `wav`, `mp3` | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartFile

Learn about [file inputs](https://platform.openai.com/docs/guides/text) for text generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file | [OpenAI.ChatCompletionRequestMessageContentPartFileFile](#openaichatcompletionrequestmessagecontentpartfilefile) |  | Yes |  |
| └─ file_data | string |  | No |  |
| └─ file_id | string |  | No |  |
| └─ filename | string |  | No |  |
| type | enum | The type of the content part. Always `file`.<br>Possible values: `file` | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartFileFile

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string |  | No |  |
| file_id | string |  | No |  |
| filename | string |  | No |  |

### OpenAI.ChatCompletionRequestMessageContentPartImage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_url | [OpenAI.ChatCompletionRequestMessageContentPartImageImageUrl](#openaichatcompletionrequestmessagecontentpartimageimageurl) |  | Yes |  |
| type | enum | The type of the content part.<br>Possible values: `image_url` | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartImageImageUrl

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | enum | <br>Possible values: `auto`, `low`, `high` | No |  |
| url | string |  | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartRefusal

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal message generated by the model. | Yes |  |
| type | enum | The type of the content part.<br>Possible values: `refusal` | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text content. | Yes |  |
| type | enum | The type of the content part.<br>Possible values: `text` | Yes |  |

### OpenAI.ChatCompletionRequestMessageType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `developer`<br>`system`<br>`user`<br>`assistant`<br>`tool`<br>`function` |

### OpenAI.ChatCompletionRequestSystemMessage

Developer-provided instructions that the model should follow, regardless of
messages sent by the user. With o1 models and newer, use `developer` messages
for this purpose instead.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array of [OpenAI.ChatCompletionRequestSystemMessageContentPart](#openaichatcompletionrequestsystemmessagecontentpart) | The contents of the system message. | Yes |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| role | enum | The role of the messages author, in this case `system`.<br>Possible values: `system` | Yes |  |

### OpenAI.ChatCompletionRequestSystemMessageContentPart

References: [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext)

### OpenAI.ChatCompletionRequestToolMessage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array of [OpenAI.ChatCompletionRequestToolMessageContentPart](#openaichatcompletionrequesttoolmessagecontentpart) | The contents of the tool message. | Yes |  |
| role | enum | The role of the messages author, in this case `tool`.<br>Possible values: `tool` | Yes |  |
| tool_call_id | string | Tool call that this message is responding to. | Yes |  |

### OpenAI.ChatCompletionRequestToolMessageContentPart

References: [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext)

### OpenAI.ChatCompletionRequestUserMessage

Messages sent by an end user, containing prompts or additional context
information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array of [OpenAI.ChatCompletionRequestUserMessageContentPart](#openaichatcompletionrequestusermessagecontentpart) | The contents of the user message. | Yes |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| role | enum | The role of the messages author, in this case `user`.<br>Possible values: `user` | Yes |  |

### OpenAI.ChatCompletionRequestUserMessageContentPart


### Discriminator for OpenAI.ChatCompletionRequestUserMessageContentPart

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `image_url` | [OpenAI.ChatCompletionRequestMessageContentPartImage](#openaichatcompletionrequestmessagecontentpartimage) |
| `input_audio` | [OpenAI.ChatCompletionRequestMessageContentPartAudio](#openaichatcompletionrequestmessagecontentpartaudio) |
| `file` | [OpenAI.ChatCompletionRequestMessageContentPartFile](#openaichatcompletionrequestmessagecontentpartfile) |
| `text` | [OpenAI.ChatCompletionRequestUserMessageContentPartChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestusermessagecontentpartchatcompletionrequestmessagecontentparttext) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ChatCompletionRequestUserMessageContentPartType](#openaichatcompletionrequestusermessagecontentparttype) |  | Yes |  |

### OpenAI.ChatCompletionRequestUserMessageContentPartChatCompletionRequestMessageContentPartText

Learn about [text inputs](https://platform.openai.com/docs/guides/text-generation).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text content. | Yes |  |
| type | enum | The type of the content part.<br>Possible values: `text` | Yes |  |

### OpenAI.ChatCompletionRequestUserMessageContentPartType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`image_url`<br>`input_audio`<br>`file` |

### OpenAI.ChatCompletionResponseMessage

If the audio output modality is requested, this object contains data
about the audio response from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.ChatCompletionResponseMessageAnnotations](#openaichatcompletionresponsemessageannotations) | Annotations for the message, when applicable, as when using the<br>  [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat). | No |  |
| audio | [OpenAI.ChatCompletionResponseMessageAudio](#openaichatcompletionresponsemessageaudio) or null |  | No |  |
| content | string or null |  | Yes |  |
| function_call | [OpenAI.ChatCompletionResponseMessageFunctionCall](#openaichatcompletionresponsemessagefunctioncall) |  | No |  |
| └─ arguments | string |  | Yes |  |
| └─ name | string |  | Yes |  |
| reasoning_content | string | An Azure-specific extension property containing generated reasoning content from supported models. | No |  |
| refusal | string or null |  | Yes |  |
| role | enum | The role of the author of this message.<br>Possible values: `assistant` | Yes |  |
| tool_calls | [OpenAI.ChatCompletionMessageToolCallsItem](#openaichatcompletionmessagetoolcallsitem) | The tool calls generated by the model, such as function calls. | No |  |

### OpenAI.ChatCompletionResponseMessageAnnotations

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `url_citation` | Yes |  |
| url_citation | [OpenAI.ChatCompletionResponseMessageAnnotationsUrlCitation](#openaichatcompletionresponsemessageannotationsurlcitation) |  | Yes |  |

### OpenAI.ChatCompletionResponseMessageAnnotationsUrlCitation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end_index | integer |  | Yes |  |
| start_index | integer |  | Yes |  |
| title | string |  | Yes |  |
| url | string |  | Yes |  |

### OpenAI.ChatCompletionResponseMessageAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string |  | Yes |  |
| expires_at | integer |  | Yes |  |
| id | string |  | Yes |  |
| transcript | string |  | Yes |  |

### OpenAI.ChatCompletionResponseMessageFunctionCall

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string |  | Yes |  |
| name | string |  | Yes |  |

### OpenAI.ChatCompletionStreamOptions

Options for streaming response. Only set this when you set `stream: true`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_obfuscation | boolean | When true, stream obfuscation will be enabled. Stream obfuscation adds<br>  random characters to an `obfuscation` field on streaming delta events to<br>  normalize payload sizes as a mitigation to certain side-channel attacks.<br>  These obfuscation fields are included by default, but add a small amount<br>  of overhead to the data stream. You can set `include_obfuscation` to<br>  false to optimize for bandwidth if you trust the network links between<br>  your application and the OpenAI API. | No |  |
| include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>  message. The `usage` field on this chunk shows the token usage statistics<br>  for the entire request, and the `choices` field will always be an empty<br>  array.<br>  All other chunks will also include a `usage` field, but with a null<br>  value. **NOTE:** If the stream is interrupted, you may not receive the<br>  final usage chunk which contains the total token usage for the request. | No |  |

### OpenAI.ChatCompletionStreamResponseDelta

A chat completion delta generated by streamed model responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or null |  | No |  |
| function_call | [OpenAI.ChatCompletionStreamResponseDeltaFunctionCall](#openaichatcompletionstreamresponsedeltafunctioncall) |  | No |  |
| └─ arguments | string |  | No |  |
| └─ name | string |  | No |  |
| reasoning_content | string | An Azure-specific extension property containing generated reasoning content from supported models. | No |  |
| refusal | string or null |  | No |  |
| role | enum | The role of the author of this message.<br>Possible values: `developer`, `system`, `user`, `assistant`, `tool` | No |  |
| tool_calls | array of [OpenAI.ChatCompletionMessageToolCallChunk](#openaichatcompletionmessagetoolcallchunk) |  | No |  |

### OpenAI.ChatCompletionStreamResponseDeltaFunctionCall

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string |  | No |  |
| name | string |  | No |  |

### OpenAI.ChatCompletionTokenLogprob

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array of integer or null |  | Yes |  |
| logprob | number | The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely. | Yes |  |
| token | string | The token. | Yes |  |
| top_logprobs | array of [OpenAI.ChatCompletionTokenLogprobTopLogprobs](#openaichatcompletiontokenlogprobtoplogprobs) | List of the most likely tokens and their log probability, at this token position. In rare cases, there may be fewer than the number of requested `top_logprobs` returned. | Yes |  |

### OpenAI.ChatCompletionTokenLogprobTopLogprobs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array of integer or null |  | Yes |  |
| logprob | number |  | Yes |  |
| token | string |  | Yes |  |

### OpenAI.ChatCompletionTool

A function tool that can be used to generate a response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.FunctionObject](#openaifunctionobject) |  | Yes |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatCompletionToolChoiceOption

Controls which (if any) tool is called by the model.
`none` means the model will not call any tool and instead generates a message.
`auto` means the model can pick between generating a message or calling one or more tools.
`required` means the model must call one or more tools.
Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.
`none` is the default when no tools are present. `auto` is the default if tools are present.

**Type**: string or [OpenAI.ChatCompletionAllowedToolsChoice](#openaichatcompletionallowedtoolschoice) or [OpenAI.ChatCompletionNamedToolChoice](#openaichatcompletionnamedtoolchoice) or [OpenAI.ChatCompletionNamedToolChoiceCustom](#openaichatcompletionnamedtoolchoicecustom)

Controls which (if any) tool is called by the model.
`none` means the model will not call any tool and instead generates a message.
`auto` means the model can pick between generating a message or calling one or more tools.
`required` means the model must call one or more tools.
Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.
`none` is the default when no tools are present. `auto` is the default if tools are present.


### OpenAI.ChunkingStrategyRequestParam

The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. Only applicable if `file_ids` is non-empty.


### Discriminator for OpenAI.ChunkingStrategyRequestParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `auto` | [OpenAI.AutoChunkingStrategyRequestParam](#openaiautochunkingstrategyrequestparam) |
| `static` | [OpenAI.StaticChunkingStrategyRequestParam](#openaistaticchunkingstrategyrequestparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ChunkingStrategyRequestParamType](#openaichunkingstrategyrequestparamtype) |  | Yes |  |

### OpenAI.ChunkingStrategyRequestParamType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `auto`<br>`static` |

### OpenAI.ChunkingStrategyResponse

The strategy used to chunk the file.


### Discriminator for OpenAI.ChunkingStrategyResponse

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `static` | [OpenAI.StaticChunkingStrategyResponseParam](#openaistaticchunkingstrategyresponseparam) |
| `other` | [OpenAI.OtherChunkingStrategyResponseParam](#openaiotherchunkingstrategyresponseparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ChunkingStrategyResponseType](#openaichunkingstrategyresponsetype) |  | Yes |  |

### OpenAI.ChunkingStrategyResponseType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `static`<br>`other` |

### OpenAI.ClickButtonType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `left`<br>`right`<br>`wheel`<br>`back`<br>`forward` |

### OpenAI.ClickParam

A click action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| button | [OpenAI.ClickButtonType](#openaiclickbuttontype) |  | Yes |  |
| type | enum | Specifies the event type. For a click action, this property is always `click`.<br>Possible values: `click` | Yes |  |
| x | integer | The x-coordinate where the click occurred. | Yes |  |
| y | integer | The y-coordinate where the click occurred. | Yes |  |

### OpenAI.CodeInterpreterContainerAuto

Configuration for a code interpreter container. Optionally specify the IDs of the files to run the code on.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_ids | array of string | An optional list of uploaded files to make available to your code. | No |  |
| memory_limit | [OpenAI.ContainerMemoryLimit](#openaicontainermemorylimit) or null |  | No |  |
| type | enum | Always `auto`.<br>Possible values: `auto` | Yes |  |

### OpenAI.CodeInterpreterOutputImage

The image output from the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the output. Always `image`.<br>Possible values: `image` | Yes |  |
| url | string | The URL of the image output from the code interpreter. | Yes |  |

### OpenAI.CodeInterpreterOutputLogs

The logs output from the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logs | string | The logs output from the code interpreter. | Yes |  |
| type | enum | The type of the output. Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.CodeInterpreterTool

A tool that runs Python code to help generate a response to a prompt.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container | string or [OpenAI.CodeInterpreterContainerAuto](#openaicodeinterpretercontainerauto) | The code interpreter container. Can be a container ID or an object that<br>  specifies uploaded file IDs to make available to your code, along with an<br>  optional `memory_limit` setting. | Yes |  |
| type | enum | The type of the code interpreter tool. Always `code_interpreter`.<br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.ComparisonFilter

A filter used to compare a specified attribute key to a given value using a defined comparison operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| key | string | The key to compare against the value. | Yes |  |
| type | enum | Specifies the comparison operator: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `nin`.<br>  - `eq`: equals<br>  - `ne`: not equal<br>  - `gt`: greater than<br>  - `gte`: greater than or equal<br>  - `lt`: less than<br>  - `lte`: less than or equal<br>  - `in`: in<br>  - `nin`: not in<br>Possible values: `eq`, `ne`, `gt`, `gte`, `lt`, `lte` | Yes |  |
| value | string or number or boolean or array of [OpenAI.ComparisonFilterValueItems](#openaicomparisonfiltervalueitems) | The value to compare against the attribute key; supports string, number, or boolean types. | Yes |  |

### OpenAI.ComparisonFilterValueItems

This schema accepts one of the following types:

- **string**
- **number**

### OpenAI.CompletionUsage

Usage statistics for the completion request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_tokens | integer | Number of tokens in the generated completion. | Yes |  |
| completion_tokens_details | [OpenAI.CompletionUsageCompletionTokensDetails](#openaicompletionusagecompletiontokensdetails) |  | No |  |
| └─ accepted_prediction_tokens | integer |  | No |  |
| └─ audio_tokens | integer |  | No |  |
| └─ reasoning_tokens | integer |  | No |  |
| └─ rejected_prediction_tokens | integer |  | No |  |
| prompt_tokens | integer | Number of tokens in the prompt. | Yes |  |
| prompt_tokens_details | [OpenAI.CompletionUsagePromptTokensDetails](#openaicompletionusageprompttokensdetails) |  | No |  |
| └─ audio_tokens | integer |  | No |  |
| └─ cached_tokens | integer |  | No |  |
| total_tokens | integer | Total number of tokens used in the request (prompt + completion). | Yes |  |

### OpenAI.CompletionUsageCompletionTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| accepted_prediction_tokens | integer |  | No |  |
| audio_tokens | integer |  | No |  |
| reasoning_tokens | integer |  | No |  |
| rejected_prediction_tokens | integer |  | No |  |

### OpenAI.CompletionUsagePromptTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio_tokens | integer |  | No |  |
| cached_tokens | integer |  | No |  |

### OpenAI.CompoundFilter

Combine multiple filters using `and` or `or`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | array of [OpenAI.ComparisonFilter](#openaicomparisonfilter) or object | Array of filters to combine. Items can be `ComparisonFilter` or `CompoundFilter`. | Yes |  |
| type | enum | Type of operation: `and` or `or`.<br>Possible values: `and`, `or` | Yes |  |

### OpenAI.ComputerAction


### Discriminator for OpenAI.ComputerAction

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `click` | [OpenAI.ClickParam](#openaiclickparam) |
| `double_click` | [OpenAI.DoubleClickAction](#openaidoubleclickaction) |
| `drag` | [OpenAI.Drag](#openaidrag) |
| `keypress` | [OpenAI.KeyPressAction](#openaikeypressaction) |
| `move` | [OpenAI.Move](#openaimove) |
| `screenshot` | [OpenAI.Screenshot](#openaiscreenshot) |
| `scroll` | [OpenAI.Scroll](#openaiscroll) |
| `type` | [OpenAI.Type](#openaitype) |
| `wait` | [OpenAI.Wait](#openaiwait) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ComputerActionType](#openaicomputeractiontype) |  | Yes |  |

### OpenAI.ComputerActionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `click`<br>`double_click`<br>`drag`<br>`keypress`<br>`move`<br>`screenshot`<br>`scroll`<br>`type`<br>`wait` |

### OpenAI.ComputerCallSafetyCheckParam

A pending safety check for the computer call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string or null |  | No |  |
| id | string | The ID of the pending safety check. | Yes |  |
| message | string or null |  | No |  |

### OpenAI.ComputerEnvironment

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `windows`<br>`mac`<br>`linux`<br>`ubuntu`<br>`browser` |

### OpenAI.ComputerScreenshotContent

A screenshot of a computer.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string or null |  | Yes |  |
| image_url | string or null |  | Yes |  |
| type | enum | Specifies the event type. For a computer screenshot, this property is always set to `computer_screenshot`.<br>Possible values: `computer_screenshot` | Yes |  |

### OpenAI.ComputerScreenshotImage

A computer screenshot image used with the computer use tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The identifier of an uploaded file that contains the screenshot. | No |  |
| image_url | string | The URL of the screenshot image. | No |  |
| type | enum | Specifies the event type. For a computer screenshot, this property is<br>  always set to `computer_screenshot`.<br>Possible values: `computer_screenshot` | Yes |  |

### OpenAI.ComputerUsePreviewTool

A tool that controls a virtual computer.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| display_height | integer | The height of the computer display. | Yes |  |
| display_width | integer | The width of the computer display. | Yes |  |
| environment | [OpenAI.ComputerEnvironment](#openaicomputerenvironment) |  | Yes |  |
| type | enum | The type of the computer use tool. Always `computer_use_preview`.<br>Possible values: `computer_use_preview` | Yes |  |

### OpenAI.ContainerFileCitationBody

A citation for a container file used to generate a model response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| container_id | string | The ID of the container file. | Yes |  |
| end_index | integer | The index of the last character of the container file citation in the message. | Yes |  |
| file_id | string | The ID of the file. | Yes |  |
| filename | string | The filename of the container file cited. | Yes |  |
| start_index | integer | The index of the first character of the container file citation in the message. | Yes |  |
| type | enum | The type of the container file citation. Always `container_file_citation`.<br>Possible values: `container_file_citation` | Yes |  |

### OpenAI.ContainerFileListResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.ContainerFileResource](#openaicontainerfileresource) | A list of container files. | Yes |  |
| first_id | string | The ID of the first file in the list. | Yes |  |
| has_more | boolean | Whether there are more files available. | Yes |  |
| last_id | string | The ID of the last file in the list. | Yes |  |
| object | enum | The type of object returned, must be 'list'.<br>Possible values: `list` | Yes |  |

### OpenAI.ContainerFileResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | integer | Size of the file in bytes. | Yes |  |
| container_id | string | The container this file belongs to. | Yes |  |
| created_at | integer | Unix timestamp (in seconds) when the file was created. | Yes |  |
| id | string | Unique identifier for the file. | Yes |  |
| object | enum | The type of this object (`container.file`).<br>Possible values: `container.file` | Yes |  |
| path | string | Path of the file in the container. | Yes |  |
| source | string | Source of the file (for example, `user`, `assistant`). | Yes |  |

### OpenAI.ContainerListResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.ContainerResource](#openaicontainerresource) | A list of containers. | Yes |  |
| first_id | string | The ID of the first container in the list. | Yes |  |
| has_more | boolean | Whether there are more containers available. | Yes |  |
| last_id | string | The ID of the last container in the list. | Yes |  |
| object | enum | The type of object returned, must be 'list'.<br>Possible values: `list` | Yes |  |

### OpenAI.ContainerMemoryLimit

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `1g`<br>`4g`<br>`16g`<br>`64g` |

### OpenAI.ContainerResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the container was created. | Yes |  |
| expires_after | [OpenAI.ContainerResourceExpiresAfter](#openaicontainerresourceexpiresafter) |  | No |  |
| └─ anchor | enum | <br>Possible values: `last_active_at` | No |  |
| └─ minutes | integer |  | No |  |
| id | string | Unique identifier for the container. | Yes |  |
| last_active_at | integer | Unix timestamp (in seconds) when the container was last active. | No |  |
| memory_limit | enum | The memory limit configured for the container.<br>Possible values: `1g`, `4g`, `16g`, `64g` | No |  |
| name | string | Name of the container. | Yes |  |
| object | string | The type of this object. | Yes |  |
| status | string | Status of the container (for example, active, deleted). | Yes |  |

### OpenAI.ContainerResourceExpiresAfter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| anchor | enum | <br>Possible values: `last_active_at` | No |  |
| minutes | integer |  | No |  |

### OpenAI.ConversationItem

A single item within a conversation. The set of possible types are the same as the `output` type of a [Response object](https://platform.openai.com/docs/api-reference/responses/object#responses/object-output).


### Discriminator for OpenAI.ConversationItem

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.ConversationItemMessage](#openaiconversationitemmessage) |
| `function_call` | [OpenAI.ConversationItemFunctionToolCallResource](#openaiconversationitemfunctiontoolcallresource) |
| `function_call_output` | [OpenAI.ConversationItemFunctionToolCallOutputResource](#openaiconversationitemfunctiontoolcalloutputresource) |
| `file_search_call` | [OpenAI.ConversationItemFileSearchToolCall](#openaiconversationitemfilesearchtoolcall) |
| `web_search_call` | [OpenAI.ConversationItemWebSearchToolCall](#openaiconversationitemwebsearchtoolcall) |
| `image_generation_call` | [OpenAI.ConversationItemImageGenToolCall](#openaiconversationitemimagegentoolcall) |
| `computer_call` | [OpenAI.ConversationItemComputerToolCall](#openaiconversationitemcomputertoolcall) |
| `computer_call_output` | [OpenAI.ConversationItemComputerToolCallOutputResource](#openaiconversationitemcomputertoolcalloutputresource) |
| `reasoning` | [OpenAI.ConversationItemReasoningItem](#openaiconversationitemreasoningitem) |
| `code_interpreter_call` | [OpenAI.ConversationItemCodeInterpreterToolCall](#openaiconversationitemcodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.ConversationItemLocalShellToolCall](#openaiconversationitemlocalshelltoolcall) |
| `local_shell_call_output` | [OpenAI.ConversationItemLocalShellToolCallOutput](#openaiconversationitemlocalshelltoolcalloutput) |
| `shell_call` | [OpenAI.ConversationItemFunctionShellCall](#openaiconversationitemfunctionshellcall) |
| `shell_call_output` | [OpenAI.ConversationItemFunctionShellCallOutput](#openaiconversationitemfunctionshellcalloutput) |
| `apply_patch_call` | [OpenAI.ConversationItemApplyPatchToolCall](#openaiconversationitemapplypatchtoolcall) |
| `apply_patch_call_output` | [OpenAI.ConversationItemApplyPatchToolCallOutput](#openaiconversationitemapplypatchtoolcalloutput) |
| `mcp_list_tools` | [OpenAI.ConversationItemMcpListTools](#openaiconversationitemmcplisttools) |
| `mcp_approval_request` | [OpenAI.ConversationItemMcpApprovalRequest](#openaiconversationitemmcpapprovalrequest) |
| `mcp_approval_response` | [OpenAI.ConversationItemMcpApprovalResponseResource](#openaiconversationitemmcpapprovalresponseresource) |
| `mcp_call` | [OpenAI.ConversationItemMcpToolCall](#openaiconversationitemmcptoolcall) |
| `custom_tool_call` | [OpenAI.ConversationItemCustomToolCall](#openaiconversationitemcustomtoolcall) |
| `custom_tool_call_output` | [OpenAI.ConversationItemCustomToolCallOutput](#openaiconversationitemcustomtoolcalloutput) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ConversationItemType](#openaiconversationitemtype) |  | Yes |  |

### OpenAI.ConversationItemApplyPatchToolCall

A tool call that applies file diffs by creating, deleting, or updating files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the apply patch tool call. Populated when this item is returned via API. | Yes |  |
| operation | [OpenAI.ApplyPatchFileOperation](#openaiapplypatchfileoperation) | One of the create_file, delete_file, or update_file operations applied via apply_patch. | Yes |  |
| └─ type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |
| status | [OpenAI.ApplyPatchCallStatus](#openaiapplypatchcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.ConversationItemApplyPatchToolCallOutput

The output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call output. | No |  |
| id | string | The unique ID of the apply patch tool call output. Populated when this item is returned via API. | Yes |  |
| output | string or null |  | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatus](#openaiapplypatchcalloutputstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.ConversationItemCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string or null |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) or null |  | Yes |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.ConversationItemComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.ConversationItemComputerToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The safety checks reported by the API that have been acknowledged by the<br>  developer. | No |  |
| call_id | string | The ID of the computer tool call that produced the output. | Yes |  |
| id | string | The ID of the computer tool call output. | No |  |
| output | [OpenAI.ComputerScreenshotImage](#openaicomputerscreenshotimage) | A computer screenshot image used with the computer use tool. | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the computer tool call output. Always `computer_call_output`.<br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.ConversationItemCustomToolCall

A call to a custom tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | An identifier used to map this custom tool call to a tool call output. | Yes |  |
| id | string | The unique ID of the custom tool call in the OpenAI platform. | No |  |
| input | string | The input for the custom tool call generated by the model. | Yes |  |
| name | string | The name of the custom tool being called. | Yes |  |
| type | enum | The type of the custom tool call. Always `custom_tool_call`.<br>Possible values: `custom_tool_call` | Yes |  |

### OpenAI.ConversationItemCustomToolCallOutput

The output of a custom tool call from your code, being sent back to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The call ID, used to map this custom tool call output to a custom tool call. | Yes |  |
| id | string | The unique ID of the custom tool call output in the OpenAI platform. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the custom tool call generated by your code.<br>  Can be a string or a list of output content. | Yes |  |
| type | enum | The type of the custom tool call output. Always `custom_tool_call_output`.<br>Possible values: `custom_tool_call_output` | Yes |  |

### OpenAI.ConversationItemFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) or null |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.ConversationItemFunctionShellCall

A tool call that executes one or more shell commands in a managed environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellAction](#openaifunctionshellaction) | Execute a shell command. | Yes |  |
| └─ commands | array of string |  | Yes |  |
| └─ max_output_length | integer or null |  | Yes |  |
| └─ timeout_ms | integer or null |  | Yes |  |
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the shell tool call. Populated when this item is returned via API. | Yes |  |
| status | [OpenAI.LocalShellCallStatus](#openailocalshellcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.ConversationItemFunctionShellCallOutput

The output of a shell tool call that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The identifier of the actor that created the item. | No |  |
| id | string | The unique ID of the shell call output. Populated when this item is returned via API. | Yes |  |
| max_output_length | integer or null |  | Yes |  |
| output | array of [OpenAI.FunctionShellCallOutputContent](#openaifunctionshellcalloutputcontent) | An array of shell call output contents | Yes |  |
| type | enum | The type of the shell call output. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.ConversationItemFunctionToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call output. Populated when this item<br>  is returned via API. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the function call generated by your code.<br>  Can be a string or a list of output content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call output. Always `function_call_output`.<br>Possible values: `function_call_output` | Yes |  |

### OpenAI.ConversationItemFunctionToolCallResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.ConversationItemImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the image generation call. | Yes |  |
| result | string or null |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.ConversationItemList

A list of Conversation items.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.ConversationItem](#openaiconversationitem) | A list of conversation items. | Yes |  |
| first_id | string | The ID of the first item in the list. | Yes |  |
| has_more | boolean | Whether there are more items available. | Yes |  |
| last_id | string | The ID of the last item in the list. | Yes |  |
| object | enum | The type of object returned, must be `list`.<br>Possible values: `list` | Yes |  |

### OpenAI.ConversationItemLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.ConversationItemLocalShellToolCallOutput

The output of a local shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| status | string or null |  | No |  |
| type | enum | The type of the local shell tool call output. Always `local_shell_call_output`.<br>Possible values: `local_shell_call_output` | Yes |  |

### OpenAI.ConversationItemMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.ConversationItemMcpApprovalResponseResource

A response to an MCP approval request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| id | string | The unique ID of the approval response | Yes |  |
| reason | string or null |  | No |  |
| type | enum | The type of the item. Always `mcp_approval_response`.<br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.ConversationItemMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string or null |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.ConversationItemMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string or null |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string or null |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string or null |  | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.ConversationItemMessage

A message to or from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.InputTextContent](#openaiinputtextcontent) or [OpenAI.OutputTextContent](#openaioutputtextcontent) or [OpenAI.TextContent](#openaitextcontent) or [OpenAI.SummaryTextContent](#openaisummarytextcontent) or [OpenAI.ReasoningTextContent](#openaireasoningtextcontent) or [OpenAI.RefusalContent](#openairefusalcontent) or [OpenAI.InputImageContent](#openaiinputimagecontent) or [OpenAI.ComputerScreenshotContent](#openaicomputerscreenshotcontent) or [OpenAI.InputFileContent](#openaiinputfilecontent) | The content of the message | Yes |  |
| id | string | The unique ID of the message. | Yes |  |
| role | [OpenAI.MessageRole](#openaimessagerole) |  | Yes |  |
| status | [OpenAI.MessageStatus](#openaimessagestatus) |  | Yes |  |
| type | enum | The type of the message. Always set to `message`.<br>Possible values: `message` | Yes |  |

### OpenAI.ConversationItemReasoningItem

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually
[managing context](https://platform.openai.com/docs/guides/conversation-state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.ReasoningTextContent](#openaireasoningtextcontent) | Reasoning text content. | No |  |
| encrypted_content | string or null |  | No |  |
| id | string | The unique identifier of the reasoning content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| summary | array of [OpenAI.Summary](#openaisummary) | Reasoning summary content. | Yes |  |
| type | enum | The type of the object. Always `reasoning`.<br>Possible values: `reasoning` | Yes |  |

### OpenAI.ConversationItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`function_call`<br>`function_call_output`<br>`file_search_call`<br>`web_search_call`<br>`image_generation_call`<br>`computer_call`<br>`computer_call_output`<br>`reasoning`<br>`code_interpreter_call`<br>`local_shell_call`<br>`local_shell_call_output`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call`<br>`custom_tool_call`<br>`custom_tool_call_output` |

### OpenAI.ConversationItemWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.ConversationParam

The conversation that this response belongs to. Items from this conversation are prepended to `input_items` for this response request.
Input items and output items from this response are automatically added to this conversation after this response completes.

**Type**: string or [OpenAI.ConversationParam-2](#openaiconversationparam-2)

The conversation that this response belongs to. Items from this conversation are prepended to `input_items` for this response request.
Input items and output items from this response are automatically added to this conversation after this response completes.


### OpenAI.ConversationParam-2

The conversation that this response belongs to.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the conversation. | Yes |  |

### OpenAI.ConversationReference

The conversation that this response belonged to. Input items and output items from this response were automatically added to this conversation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the conversation that this response was associated with. | Yes |  |

### OpenAI.ConversationResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The time at which the conversation was created, measured in seconds since the Unix epoch. | Yes |  |
| id | string | The unique ID of the conversation. | Yes |  |
| metadata |  | Set of 16 key-value pairs that can be attached to an object. This can be         useful for storing additional information about the object in a structured         format, and querying for objects via API or the dashboard.<br>  Keys are strings with a maximum length of 64 characters. Values are strings         with a maximum length of 512 characters. | Yes |  |
| object | enum | The object type, which is always `conversation`.<br>Possible values: `conversation` | Yes |  |

### OpenAI.CreateChatCompletionRequestAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | enum | <br>Possible values: `wav`, `aac`, `mp3`, `flac`, `opus`, `pcm16` | Yes |  |
| voice | [OpenAI.VoiceIdsShared](#openaivoiceidsshared) |  | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormat

An object specifying the format that the model must output.
Setting to `{ "type": "json_schema", "json_schema": {...} }` enables
Structured Outputs which ensure the model will match your supplied JSON
schema. Learn more in the [Structured Outputs
guide](https://platform.openai.com/docs/guides/structured-outputs).
Setting to `{ "type": "json_object" }` enables the older JSON mode, which
ensures the message the model generates is valid JSON. Using `json_schema`
is preferred for models that support it.


### Discriminator for OpenAI.CreateChatCompletionRequestResponseFormat

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `json_schema` | [OpenAI.ResponseFormatJsonSchema](#openairesponseformatjsonschema) |
| `text` | [OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatText](#openaicreatechatcompletionrequestresponseformatresponseformattext) |
| `json_object` | [OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatJsonObject](#openaicreatechatcompletionrequestresponseformatresponseformatjsonobject) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.CreateChatCompletionRequestResponseFormatType](#openaicreatechatcompletionrequestresponseformattype) |  | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatJsonObject

JSON object response format. An older method of generating JSON responses.
Using `json_schema` is recommended for models that support it. Note that the
model will not generate JSON without a system or user message instructing it
to do so.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `json_object`.<br>Possible values: `json_object` | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormatResponseFormatText

Default response format. Used to generate text responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.CreateChatCompletionRequestResponseFormatType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`json_schema`<br>`json_object` |

### OpenAI.CreateChatCompletionResponseChoices

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_filter_results | [AzureContentFilterResultForChoice](#azurecontentfilterresultforchoice) | A content filter result for a single response item produced by a generative AI system. | No |  |
| finish_reason | enum | <br>Possible values: `stop`, `length`, `tool_calls`, `content_filter`, `function_call` | Yes |  |
| index | integer |  | Yes |  |
| logprobs | [OpenAI.CreateChatCompletionResponseChoicesLogprobs](#openaicreatechatcompletionresponsechoiceslogprobs) or null |  | Yes |  |
| message | [OpenAI.ChatCompletionResponseMessage](#openaichatcompletionresponsemessage) | If the audio output modality is requested, this object contains data<br>about the audio response from the model. | Yes |  |

### OpenAI.CreateChatCompletionResponseChoicesLogprobs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.ChatCompletionTokenLogprob](#openaichatcompletiontokenlogprob) or null |  | Yes |  |
| refusal | array of [OpenAI.ChatCompletionTokenLogprob](#openaichatcompletiontokenlogprob) or null |  | Yes |  |

### OpenAI.CreateChatCompletionStreamResponseChoices

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | [OpenAI.ChatCompletionStreamResponseDelta](#openaichatcompletionstreamresponsedelta) | A chat completion delta generated by streamed model responses. | Yes |  |
| finish_reason | string or null |  | Yes |  |
| index | integer |  | Yes |  |
| logprobs | [OpenAI.CreateChatCompletionStreamResponseChoicesLogprobs](#openaicreatechatcompletionstreamresponsechoiceslogprobs) or null |  | No |  |

### OpenAI.CreateChatCompletionStreamResponseChoicesLogprobs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.ChatCompletionTokenLogprob](#openaichatcompletiontokenlogprob) or null |  | Yes |  |
| refusal | array of [OpenAI.ChatCompletionTokenLogprob](#openaichatcompletiontokenlogprob) or null |  | Yes |  |

### OpenAI.CreateCompletionResponseChoices

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_filter_results | [AzureContentFilterResultForChoice](#azurecontentfilterresultforchoice) | A content filter result for a single response item produced by a generative AI system. | No |  |
| finish_reason | enum | <br>Possible values: `stop`, `length`, `content_filter` | Yes |  |
| index | integer |  | Yes |  |
| logprobs | [OpenAI.CreateCompletionResponseChoicesLogprobs](#openaicreatecompletionresponsechoiceslogprobs) or null |  | Yes |  |
| text | string |  | Yes |  |

### OpenAI.CreateCompletionResponseChoicesLogprobs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text_offset | array of integer |  | No |  |
| token_logprobs | array of number |  | No |  |
| tokens | array of string |  | No |  |
| top_logprobs | array of object |  | No |  |

### OpenAI.CreateContainerBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | [OpenAI.CreateContainerBodyExpiresAfter](#openaicreatecontainerbodyexpiresafter) |  | No |  |
| └─ anchor | enum | <br>Possible values: `last_active_at` | Yes |  |
| └─ minutes | integer |  | Yes |  |
| file_ids | array of string | IDs of files to copy to the container. | No |  |
| memory_limit | enum | Optional memory limit for the container. Defaults to "1g".<br>Possible values: `1g`, `4g`, `16g`, `64g` | No |  |
| name | string | Name of the container to create. | Yes |  |

### OpenAI.CreateContainerBodyExpiresAfter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| anchor | enum | <br>Possible values: `last_active_at` | Yes |  |
| minutes | integer |  | Yes |  |

### OpenAI.CreateContainerFileBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file |  | The File object (not file name) to be uploaded. | No |  |
| file_id | string | Name of the file to create. | No |  |

### OpenAI.CreateConversationBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |

### OpenAI.CreateConversationItemsParametersBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| items | array of [OpenAI.InputItem](#openaiinputitem) |  | Yes |  |

### OpenAI.CreateEmbeddingRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| dimensions | integer | The number of dimensions the resulting output embeddings should have. Only supported in `text-embedding-3` and later models.<br>**Constraints:** min: 1 | No |  |
| encoding_format | enum | The format to return the embeddings in. Can be either `float` or [`base64`](https://pypi.org/project/pybase64/).<br>Possible values: `float`, `base64` | No |  |
| input | string or array of string or array of integer or array of array | Input text to embed, encoded as a string or array of tokens. To embed multiple inputs in a single request, pass an array of strings or array of token arrays. The input must not exceed the max input tokens for the model (8,192 tokens for all embedding models), cannot be an empty string, and any array must be 2,048 dimensions or less. [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens. In addition to the per-input token limit, all embedding  models enforce a maximum of 300,000 tokens summed across all inputs in a  single request. | Yes |  |
| model | string | ID of the model to use. You can use the [List models](https://platform.openai.com/docs/api-reference/models/list) API to see all of your available models, or see our [Model overview](https://platform.openai.com/docs/models) for descriptions of them. | Yes |  |
| user | string |  [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#end-user-ids). | No |  |

### OpenAI.CreateEmbeddingResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.Embedding](#openaiembedding) | The list of embeddings generated by the model. | Yes |  |
| model | string | The name of the model used to generate the embedding. | Yes |  |
| object | enum | The object type, which is always "list".<br>Possible values: `list` | Yes |  |
| usage | [OpenAI.CreateEmbeddingResponseUsage](#openaicreateembeddingresponseusage) |  | Yes |  |
| └─ prompt_tokens | integer |  | Yes |  |
| └─ total_tokens | integer |  | Yes |  |

### OpenAI.CreateEmbeddingResponseUsage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prompt_tokens | integer |  | Yes |  |
| total_tokens | integer |  | Yes |  |

### OpenAI.CreateEvalCompletionsRunDataSource

A CompletionsRunDataSource object describing a model sampling configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | [OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesTemplate](#openaicreateevalcompletionsrundatasourceinputmessagestemplate) or [OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesItemReference](#openaicreateevalcompletionsrundatasourceinputmessagesitemreference) | Used when sampling from a model. Dictates the structure of the messages passed into the model. Can either be a reference to a prebuilt trajectory (ie, `item.input_trajectory`), or a template with variable references to the `item` namespace. | No |  |
| model | string | The name of the model to use for generating completions (for example "o3-mini"). | No |  |
| sampling_params | [AzureCompletionsSamplingParams](#azurecompletionssamplingparams) | Sampling parameters for controlling the behavior of completions. | No |  |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) or [OpenAI.EvalStoredCompletionsSource](#openaievalstoredcompletionssource) | Determines what populates the `item` namespace in this run's data source. | Yes |  |
| type | enum | The type of run data source. Always `completions`.<br>Possible values: `completions` | Yes |  |

### OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesItemReference

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_reference | string |  | Yes |  |
| type | enum | <br>Possible values: `item_reference` | Yes |  |

### OpenAI.CreateEvalCompletionsRunDataSourceInputMessagesTemplate

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| template | array of [OpenAI.EasyInputMessage](#openaieasyinputmessage) or [OpenAI.EvalItem](#openaievalitem) |  | Yes |  |
| type | enum | <br>Possible values: `template` | Yes |  |

### OpenAI.CreateEvalCompletionsRunDataSourceSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completion_tokens | integer |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| response_format | [OpenAI.ResponseFormatText](#openairesponseformattext) or [OpenAI.ResponseFormatJsonSchema](#openairesponseformatjsonschema) or [OpenAI.ResponseFormatJsonObject](#openairesponseformatjsonobject) |  | No |  |
| seed | integer | A seed value initializes the randomness during sampling. | No | 42 |
| temperature | number | A higher temperature increases randomness in the outputs. | No | 1 |
| tools | array of [OpenAI.ChatCompletionTool](#openaichatcompletiontool) |  | No |  |
| top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No | 1 |

### OpenAI.CreateEvalCustomDataSourceConfig

A CustomDataSourceConfig object that defines the schema for the data source used for the evaluation runs.
This schema is used to define the shape of the data that will be:
- Used to define your testing criteria and
- What data is required when creating a run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_sample_schema | boolean | Whether the eval should expect you to populate the sample namespace (ie, by generating responses off of your data source) | No |  |
| item_schema | object | The json schema for each row in the data source. | Yes |  |
| type | enum | The type of data source. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.CreateEvalItem

A chat message that makes up the prompt or context. May include variable references to the `item` namespace, ie {{item.name}}.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string | The content of the message. | Yes |  |
| role | string | The role of the message (for example "system", "assistant", "user"). | Yes |  |

### OpenAI.CreateEvalJsonlRunDataSource

A JsonlRunDataSource object with that specifies a JSONL file that matches the eval

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) | Determines what populates the `item` namespace in the data source. | Yes |  |
| type | enum | The type of data source. Always `jsonl`.<br>Possible values: `jsonl` | Yes |  |

### OpenAI.CreateEvalLabelModelGrader

A LabelModelGrader object which uses a model to assign labels to each item
in the evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array of [OpenAI.CreateEvalItem](#openaicreateevalitem) | A list of chat messages forming the prompt or context. May include variable references to the `item` namespace, ie {{item.name}}. | Yes |  |
| labels | array of string | The labels to classify to each item in the evaluation. | Yes |  |
| model | string | The model to use for the evaluation. Must support structured outputs. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| passing_labels | array of string | The labels that indicate a passing result. Must be a subset of labels. | Yes |  |
| type | enum | The object type, which is always `label_model`.<br>Possible values: `label_model` | Yes |  |

### OpenAI.CreateEvalLogsDataSourceConfig

A data source config which specifies the metadata property of your logs query.
This is usually metadata like `usecase=chatbot` or `prompt-version=v2`, etc.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Metadata filters for the logs data source. | No |  |
| type | enum | The type of data source. Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSource

A ResponsesRunDataSource object describing a model sampling configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_messages | [OpenAI.CreateEvalResponsesRunDataSourceInputMessagesTemplate](#openaicreateevalresponsesrundatasourceinputmessagestemplate) or [OpenAI.CreateEvalResponsesRunDataSourceInputMessagesItemReference](#openaicreateevalresponsesrundatasourceinputmessagesitemreference) | Used when sampling from a model. Dictates the structure of the messages passed into the model. Can either be a reference to a prebuilt trajectory (ie, `item.input_trajectory`), or a template with variable references to the `item` namespace. | No |  |
| model | string | The name of the model to use for generating completions (for example "o3-mini"). | No |  |
| sampling_params | [AzureResponsesSamplingParams](#azureresponsessamplingparams) | Sampling parameters for controlling the behavior of responses. | No |  |
| source | [OpenAI.EvalJsonlFileContentSource](#openaievaljsonlfilecontentsource) or [OpenAI.EvalJsonlFileIdSource](#openaievaljsonlfileidsource) or [OpenAI.EvalResponsesSource](#openaievalresponsessource) | Determines what populates the `item` namespace in this run's data source. | Yes |  |
| type | enum | The type of run data source. Always `responses`.<br>Possible values: `responses` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSourceInputMessagesItemReference

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_reference | string |  | Yes |  |
| type | enum | <br>Possible values: `item_reference` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSourceInputMessagesTemplate

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| template | array of object or [OpenAI.EvalItem](#openaievalitem) |  | Yes |  |
| type | enum | <br>Possible values: `template` | Yes |  |

### OpenAI.CreateEvalResponsesRunDataSourceSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| seed | integer | A seed value initializes the randomness during sampling. | No | 42 |
| temperature | number | A higher temperature increases randomness in the outputs. | No | 1 |
| text | [OpenAI.CreateEvalResponsesRunDataSourceSamplingParamsText](#openaicreateevalresponsesrundatasourcesamplingparamstext) |  | No |  |
| tools | array of [OpenAI.Tool](#openaitool) |  | No |  |
| top_p | number | An alternative to temperature for nucleus sampling; 1.0 includes all tokens. | No | 1 |

### OpenAI.CreateEvalResponsesRunDataSourceSamplingParamsText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.TextResponseFormatConfiguration](#openaitextresponseformatconfiguration) | An object specifying the format that the model must output.<br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema. Learn more in the<br><br>The default format is `{ "type": "text" }` with no additional options.<br>*Not recommended for gpt-4o and newer models:**<br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | No |  |

### OpenAI.CreateEvalRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data_source | [OpenAI.CreateEvalJsonlRunDataSource](#openaicreateevaljsonlrundatasource) or [OpenAI.CreateEvalCompletionsRunDataSource](#openaicreateevalcompletionsrundatasource) or [OpenAI.CreateEvalResponsesRunDataSource](#openaicreateevalresponsesrundatasource) | Details about the run's data source. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| name | string | The name of the run. | No |  |

### OpenAI.CreateEvalStoredCompletionsDataSourceConfig

Deprecated in favor of LogsDataSourceConfig.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | object | Metadata filters for the stored completions data source. | No |  |
| type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.CreateFileRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | object |  | Yes |  |
| └─ anchor | [AzureFileExpiryAnchor](#azurefileexpiryanchor) |  | Yes |  |
| └─ seconds | integer |  | Yes |  |
| file |  | The File object (not file name) to be uploaded. | Yes |  |
| purpose | enum | The intended purpose of the uploaded file. One of: - `assistants`: Used in the Assistants API - `batch`: Used in the Batch API - `fine-tune`: Used for fine-tuning - `evals`: Used for eval data sets<br>Possible values: `assistants`, `batch`, `fine-tune`, `evals` | Yes |  |

### OpenAI.CreateFineTuningCheckpointPermissionRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| project_ids | array of string | The project identifiers to grant access to. | Yes |  |

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
| hyperparameters | [OpenAI.CreateFineTuningJobRequestHyperparameters](#openaicreatefinetuningjobrequesthyperparameters) |  | No |  |
| └─ batch_size | string or integer |  | No | auto |
| └─ learning_rate_multiplier | string or number |  | No |  |
| └─ n_epochs | string or integer |  | No | auto |
| integrations | array of [OpenAI.CreateFineTuningJobRequestIntegrations](#openaicreatefinetuningjobrequestintegrations) or null | A list of integrations to enable for your fine-tuning job. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string (see valid models below) | The name of the model to fine-tune. You can select one of the<br>  [supported models](https://platform.openai.com/docs/guides/fine-tuning#which-models-can-be-fine-tuned). | Yes |  |
| seed | integer or null | The seed controls the reproducibility of the job. Passing in the same seed and job parameters should produce the same results, but may differ in rare cases.<br>  If a seed is not specified, one will be generated for you. | No |  |
| suffix | string or null | A string of up to 64 characters that will be added to your fine-tuned model name.<br>  For example, a `suffix` of "custom-model-name" would produce a model name like `ft:gpt-4o-mini:openai:custom-model-name:7p4lURel`. | No |  |
| training_file | string | The ID of an uploaded file that contains training data.<br>  See [upload file](https://platform.openai.com/docs/api-reference/files/create) for how to upload a file.<br>  Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose `fine-tune`.<br>  The contents of the file should differ depending on if the model uses the [chat](https://platform.openai.com/docs/api-reference/fine-tuning/chat-input), [completions](https://platform.openai.com/docs/api-reference/fine-tuning/completions-input) format, or if the fine-tuning method uses the [preference](https://platform.openai.com/docs/api-reference/fine-tuning/preference-input) format.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | Yes |  |
| validation_file | string or null | The ID of an uploaded file that contains validation data.<br>  If you provide this file, the data is used to generate validation<br>  metrics periodically during fine-tuning. These metrics can be viewed in<br>  the fine-tuning results file.<br>  The same data should not be present in both train and validation files.<br>  Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`.<br>  See the [fine-tuning guide](https://platform.openai.com/docs/guides/model-optimization) for more details. | No |  |

### OpenAI.CreateFineTuningJobRequestHyperparameters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or integer |  | No |  |
| learning_rate_multiplier | string or number |  | No |  |
| n_epochs | string or integer |  | No |  |

### OpenAI.CreateFineTuningJobRequestIntegrations

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `wandb` | Yes |  |
| wandb | [OpenAI.CreateFineTuningJobRequestIntegrationsWandb](#openaicreatefinetuningjobrequestintegrationswandb) |  | Yes |  |

### OpenAI.CreateFineTuningJobRequestIntegrationsWandb

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| entity | string or null |  | No |  |
| name | string or null |  | No |  |
| project | string |  | Yes |  |
| tags | array of string |  | No |  |

### OpenAI.CreateMessageRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attachments | array of [OpenAI.CreateMessageRequestAttachments](#openaicreatemessagerequestattachments) or null |  | No |  |
| content | string or array of [OpenAI.MessageContentImageFileObject](#openaimessagecontentimagefileobject) or [OpenAI.MessageContentImageUrlObject](#openaimessagecontentimageurlobject) or [OpenAI.MessageRequestContentTextObject](#openaimessagerequestcontenttextobject) |  | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| role | enum | The role of the entity that is creating the message. Allowed values include:<br>  - `user`: Indicates the message is sent by an actual user and should be used in most cases to represent user-generated messages.<br>  - `assistant`: Indicates the message is generated by the assistant. Use this value to insert messages from the assistant into the conversation.<br>Possible values: `user`, `assistant` | Yes |  |

### OpenAI.CreateMessageRequestAttachments

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | No |  |
| tools | array of [OpenAI.AssistantToolsCode](#openaiassistanttoolscode) or [OpenAI.AssistantToolsFileSearchTypeOnly](#openaiassistanttoolsfilesearchtypeonly) |  | No |  |

### OpenAI.CreateResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean or null |  | No |  |
| conversation | [OpenAI.ConversationParam](#openaiconversationparam) or null |  | No |  |
| include | array of [OpenAI.IncludeEnum](#openaiincludeenum) or null |  | No |  |
| input | [OpenAI.InputParam](#openaiinputparam) | Text, image, or file inputs to the model, used to generate a response.<br>Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Image inputs](https://platform.openai.com/docs/guides/images)<br>- [File inputs](https://platform.openai.com/docs/guides/pdf-files)<br>- [Conversation state](https://platform.openai.com/docs/guides/conversation-state)<br>- [Function calling](https://platform.openai.com/docs/guides/function-calling) | No |  |
| instructions | string or null |  | No |  |
| max_output_tokens | integer or null |  | No |  |
| max_tool_calls | integer or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| parallel_tool_calls | boolean or null |  | No |  |
| previous_response_id | string or null |  | No |  |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| prompt_cache_retention | string or null |  | No |  |
| reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| store | boolean or null |  | No |  |
| stream | boolean or null |  | No |  |
| stream_options | [OpenAI.ResponseStreamOptions](#openairesponsestreamoptions) or null |  | No |  |
| temperature | number or null |  | No |  |
| text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| top_logprobs | integer or null |  | No |  |
| top_p | number or null |  | No |  |
| truncation | string or null |  | No |  |
| user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |

### OpenAI.CreateRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| additional_instructions | string or null | Appends additional instructions at the end of the instructions for the run. This is useful for modifying the behavior on a per-run basis without overriding other instructions. | No |  |
| additional_messages | array of [OpenAI.CreateMessageRequest](#openaicreatemessagerequest) or null | Adds additional messages to the thread before creating the run. | No |  |
| assistant_id | string | The ID of the [assistant](https://platform.openai.com/docs/api-reference/assistants) to use to execute this run. | Yes |  |
| instructions | string or null | Overrides the [instructions](https://platform.openai.com/docs/api-reference/assistants/createAssistant) of the assistant. This is useful for modifying the behavior on a per-run basis. | No |  |
| max_completion_tokens | integer or null | The maximum number of completion tokens that may be used over the course of the run. The run will make a best effort to use only the number of completion tokens specified, across multiple turns of the run. If the run exceeds the number of completion tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| max_prompt_tokens | integer or null | The maximum number of prompt tokens that may be used over the course of the run. The run will make a best effort to use only the number of prompt tokens specified, across multiple turns of the run. If the run exceeds the number of prompt tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | The ID of the [Model](https://platform.openai.com/docs/api-reference/models) to be used to execute this run. If a value is provided here, it will override the model associated with the assistant. If not, the model associated with the assistant will be used. | No |  |
| parallel_tool_calls | [OpenAI.ParallelToolCalls](#openaiparalleltoolcalls) | Whether to enable [parallel function calling](https://platform.openai.com/docs/guides/function-calling#configuring-parallel-function-calling) during tool use. | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| response_format | [OpenAI.AssistantsApiResponseFormatOption](#openaiassistantsapiresponseformatoption) | Specifies the format that the model must output. Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.<br>Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensure the model will match your supplied JSON schema. Learn more in the <br>Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the message the model generates is valid JSON.<br>*Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length. | No |  |
| stream | boolean or null | If `true`, returns a stream of events that happen during the Run as server-sent events, terminating when the Run enters a terminal state with a `data: [DONE]` message. | No |  |
| temperature | number or null | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. | No |  |
| tool_choice | [OpenAI.AssistantsApiToolChoiceOption](#openaiassistantsapitoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tools and instead generates a message.<br>`auto` is the default value and means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools before responding to the user.<br>Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool. | No |  |
| tools | array of [OpenAI.AssistantTool](#openaiassistanttool) | Override the tools the assistant can use for this run. This is useful for modifying the behavior on a per-run basis. | No |  |
| top_p | number or null | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.<br>  We generally recommend altering this or temperature but not both. | No |  |
| truncation_strategy | [OpenAI.TruncationObject](#openaitruncationobject) | Controls for how a thread will be truncated prior to the run. Use this to control the initial context window of the run. | No |  |

### OpenAI.CreateThreadAndRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| assistant_id | string | The ID of the [assistant](https://platform.openai.com/docs/api-reference/assistants) to use to execute this run. | Yes |  |
| instructions | string or null | Override the default system message of the assistant. This is useful for modifying the behavior on a per-run basis. | No |  |
| max_completion_tokens | integer or null | The maximum number of completion tokens that may be used over the course of the run. The run will make a best effort to use only the number of completion tokens specified, across multiple turns of the run. If the run exceeds the number of completion tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| max_prompt_tokens | integer or null | The maximum number of prompt tokens that may be used over the course of the run. The run will make a best effort to use only the number of prompt tokens specified, across multiple turns of the run. If the run exceeds the number of prompt tokens specified, the run will end with status `incomplete`. See `incomplete_details` for more info. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | The ID of the [Model](https://platform.openai.com/docs/api-reference/models) to be used to execute this run. If a value is provided here, it will override the model associated with the assistant. If not, the model associated with the assistant will be used. | No |  |
| parallel_tool_calls | [OpenAI.ParallelToolCalls](#openaiparalleltoolcalls) | Whether to enable [parallel function calling](https://platform.openai.com/docs/guides/function-calling#configuring-parallel-function-calling) during tool use. | No |  |
| response_format | [OpenAI.AssistantsApiResponseFormatOption](#openaiassistantsapiresponseformatoption) | Specifies the format that the model must output. Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.<br>Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensure the model will match your supplied JSON schema. Learn more in the <br>Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the message the model generates is valid JSON.<br>*Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length. | No |  |
| stream | boolean or null | If `true`, returns a stream of events that happen during the Run as server-sent events, terminating when the Run enters a terminal state with a `data: [DONE]` message. | No |  |
| temperature | number or null | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. | No |  |
| thread | [OpenAI.CreateThreadRequest](#openaicreatethreadrequest) | Options to create a new thread. If no thread is provided when running a<br>request, an empty thread will be created. | No |  |
| tool_choice | [OpenAI.AssistantsApiToolChoiceOption](#openaiassistantsapitoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tools and instead generates a message.<br>`auto` is the default value and means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools before responding to the user.<br>Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool. | No |  |
| tool_resources | [OpenAI.CreateThreadAndRunRequestToolResources](#openaicreatethreadandrunrequesttoolresources) or null | A set of resources that are used by the assistant's tools. The resources are specific to the type of tool. For example, the `code_interpreter` tool requires a list of file IDs, while the `file_search` tool requires a list of vector store IDs. | No |  |
| tools | array of [OpenAI.AssistantTool](#openaiassistanttool) | Override the tools the assistant can use for this run. This is useful for modifying the behavior on a per-run basis. | No |  |
| top_p | number or null | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.<br>  We generally recommend altering this or temperature but not both. | No |  |
| truncation_strategy | [OpenAI.TruncationObject](#openaitruncationobject) | Controls for how a thread will be truncated prior to the run. Use this to control the initial context window of the run. | No |  |

### OpenAI.CreateThreadAndRunRequestToolResources

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter | [OpenAI.CreateThreadAndRunRequestToolResourcesCodeInterpreter](#openaicreatethreadandrunrequesttoolresourcescodeinterpreter) |  | No |  |
| file_search | [OpenAI.CreateThreadAndRunRequestToolResourcesFileSearch](#openaicreatethreadandrunrequesttoolresourcesfilesearch) |  | No |  |

### OpenAI.CreateThreadAndRunRequestToolResourcesCodeInterpreter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_ids | array of string |  | No | [] |

### OpenAI.CreateThreadAndRunRequestToolResourcesFileSearch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| vector_store_ids | array of string |  | No |  |

### OpenAI.CreateThreadRequest

Options to create a new thread. If no thread is provided when running a
request, an empty thread will be created.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| messages | array of [OpenAI.CreateMessageRequest](#openaicreatemessagerequest) | A list of [messages](https://platform.openai.com/docs/api-reference/messages) to start the thread with. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| tool_resources | [OpenAI.CreateThreadRequestToolResources](#openaicreatethreadrequesttoolresources) or null |  | No |  |

### OpenAI.CreateThreadRequestToolResources

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter | [OpenAI.CreateThreadRequestToolResourcesCodeInterpreter](#openaicreatethreadrequesttoolresourcescodeinterpreter) |  | No |  |
| file_search | object or object |  | No |  |

### OpenAI.CreateThreadRequestToolResourcesCodeInterpreter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_ids | array of string |  | No |  |

### OpenAI.CreateVectorStoreFileBatchRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. Only applicable if `file_ids` is non-empty. | No |  |
| file_ids | array of string | A list of [File](https://platform.openai.com/docs/api-reference/files) IDs that the vector store should use. Useful for tools like `file_search` that can access files.  If `attributes` or `chunking_strategy` are provided, they will be  applied to all files in the batch. Mutually exclusive with `files`. | No |  |
| files | array of [OpenAI.CreateVectorStoreFileRequest](#openaicreatevectorstorefilerequest) | A list of objects that each include a `file_id` plus optional `attributes` or `chunking_strategy`. Use this when you need to override metadata for specific files. The global `attributes` or `chunking_strategy` will be ignored and must be specified for each file. Mutually exclusive with `file_ids`. | No |  |

### OpenAI.CreateVectorStoreFileRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. Only applicable if `file_ids` is non-empty. | No |  |
| file_id | string | A [File](https://platform.openai.com/docs/api-reference/files) ID that the vector store should use. Useful for tools like `file_search` that can access files. | Yes |  |

### OpenAI.CreateVectorStoreRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. Only applicable if `file_ids` is non-empty. | No |  |
| description | string | A description for the vector store. Can be used to describe the vector store's purpose. | No |  |
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| file_ids | array of string | A list of [File](https://platform.openai.com/docs/api-reference/files) IDs that the vector store should use. Useful for tools like `file_search` that can access files. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| name | string | The name of the vector store. | No |  |

### OpenAI.CustomGrammarFormatParam

A grammar defined by the user.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | string | The grammar definition. | Yes |  |
| syntax | [OpenAI.GrammarSyntax1](#openaigrammarsyntax1) |  | Yes |  |
| type | enum | Grammar format. Always `grammar`.<br>Possible values: `grammar` | Yes |  |

### OpenAI.CustomTextFormatParam

Unconstrained free-form text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Unconstrained text format. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.CustomToolChatCompletions

A custom tool that processes input using a specified format.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom | [OpenAI.CustomToolChatCompletionsCustom](#openaicustomtoolchatcompletionscustom) |  | Yes |  |
| └─ description | string |  | No |  |
| └─ format | [OpenAI.CustomToolChatCompletionsCustomFormatText](#openaicustomtoolchatcompletionscustomformattext) or [OpenAI.CustomToolChatCompletionsCustomFormatGrammar](#openaicustomtoolchatcompletionscustomformatgrammar) |  | No |  |
| └─ name | string |  | Yes |  |
| type | enum | The type of the custom tool. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.CustomToolChatCompletionsCustom

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string |  | No |  |
| format | [OpenAI.CustomToolChatCompletionsCustomFormatText](#openaicustomtoolchatcompletionscustomformattext) or [OpenAI.CustomToolChatCompletionsCustomFormatGrammar](#openaicustomtoolchatcompletionscustomformatgrammar) |  | No |  |
| name | string |  | Yes |  |

### OpenAI.CustomToolChatCompletionsCustomFormatGrammar

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grammar | [OpenAI.CustomToolChatCompletionsCustomFormatGrammarGrammar](#openaicustomtoolchatcompletionscustomformatgrammargrammar) |  | Yes |  |
| └─ definition | string |  | Yes |  |
| └─ syntax | enum | <br>Possible values: `lark`, `regex` | Yes |  |
| type | enum | <br>Possible values: `grammar` | Yes |  |

### OpenAI.CustomToolChatCompletionsCustomFormatGrammarGrammar

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| definition | string |  | Yes |  |
| syntax | enum | <br>Possible values: `lark`, `regex` | Yes |  |

### OpenAI.CustomToolChatCompletionsCustomFormatText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `text` | Yes |  |

### OpenAI.CustomToolParam

A custom tool that processes input using a specified format. Learn more about   [custom tools](https://platform.openai.com/docs/guides/function-calling#custom-tools)

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | Optional description of the custom tool, used to provide more context. | No |  |
| format | [OpenAI.CustomToolParamFormat](#openaicustomtoolparamformat) | The input format for the custom tool. Default is unconstrained text. | No |  |
| └─ type | [OpenAI.CustomToolParamFormatType](#openaicustomtoolparamformattype) |  | Yes |  |
| name | string | The name of the custom tool, used to identify it in tool calls. | Yes |  |
| type | enum | The type of the custom tool. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.CustomToolParamFormat

The input format for the custom tool. Default is unconstrained text.


### Discriminator for OpenAI.CustomToolParamFormat

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `text` | [OpenAI.CustomTextFormatParam](#openaicustomtextformatparam) |
| `grammar` | [OpenAI.CustomGrammarFormatParam](#openaicustomgrammarformatparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.CustomToolParamFormatType](#openaicustomtoolparamformattype) |  | Yes |  |

### OpenAI.CustomToolParamFormatType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`grammar` |

### OpenAI.DeleteFileResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `file` | Yes |  |

### OpenAI.DeleteFineTuningCheckpointPermissionResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean | Whether the fine-tuned model checkpoint permission was successfully deleted. | Yes |  |
| id | string | The ID of the fine-tuned model checkpoint permission that was deleted. | Yes |  |
| object | enum | The object type, which is always "checkpoint.permission".<br>Possible values: `checkpoint.permission` | Yes |  |

### OpenAI.DeleteMessageResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `thread.message.deleted` | Yes |  |

### OpenAI.DeleteModelResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | string |  | Yes |  |

### OpenAI.DeleteThreadResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `thread.deleted` | Yes |  |

### OpenAI.DeleteVectorStoreFileResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `vector_store.file.deleted` | Yes |  |

### OpenAI.DeleteVectorStoreResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `vector_store.deleted` | Yes |  |

### OpenAI.DeletedConversationResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `conversation.deleted` | Yes |  |

### OpenAI.DoubleClickAction

A double click action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a double click action, this property is always set to `double_click`.<br>Possible values: `double_click` | Yes |  |
| x | integer | The x-coordinate where the double click occurred. | Yes |  |
| y | integer | The y-coordinate where the double click occurred. | Yes |  |

### OpenAI.Drag

A drag action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| path | array of [OpenAI.DragPoint](#openaidragpoint) | An array of coordinates representing the path of the drag action. Coordinates will appear as an array<br>  of objects, eg<br>  ```<br>  [<br>    { x: 100, y: 200 },<br>    { x: 200, y: 300 }<br>  ]<br>  ``` | Yes |  |
| type | enum | Specifies the event type. For a drag action, this property is<br>  always set to `drag`.<br>Possible values: `drag` | Yes |  |

### OpenAI.DragPoint

An x/y coordinate pair, e.g. `{ x: 100, y: 200 }`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| x | integer | The x-coordinate. | Yes |  |
| y | integer | The y-coordinate. | Yes |  |

### OpenAI.EasyInputMessage

A message input to the model with a role indicating instruction following
hierarchy. Instructions given with the `developer` or `system` role take
precedence over instructions given with the `user` role. Messages with the
`assistant` role are presumed to have been generated by the model in previous
interactions.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or [OpenAI.InputMessageContentList](#openaiinputmessagecontentlist) | Text, image, or audio input to the model, used to generate a response.<br>  Can also contain previous assistant responses. | Yes |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or<br>  `developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | Yes |  |

### OpenAI.Embedding

Represents an embedding vector returned by embedding endpoint.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| embedding | array of number | The embedding vector, which is a list of floats. The length of vector depends on the model as listed in the [embedding guide](https://platform.openai.com/docs/guides/embeddings). | Yes |  |
| index | integer | The index of the embedding in the list of embeddings. | Yes |  |
| object | enum | The object type, which is always "embedding".<br>Possible values: `embedding` | Yes |  |

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
| data_source_config | [OpenAI.EvalCustomDataSourceConfig](#openaievalcustomdatasourceconfig) or [OpenAI.EvalLogsDataSourceConfig](#openaievallogsdatasourceconfig) or [OpenAI.EvalStoredCompletionsDataSourceConfig](#openaievalstoredcompletionsdatasourceconfig) | Configuration of data sources used in runs of the evaluation. | Yes |  |
| id | string | Unique identifier for the evaluation. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | Yes |  |
| name | string | The name of the evaluation. | Yes |  |
| object | enum | The object type.<br>Possible values: `eval` | Yes |  |
| testing_criteria | array of [OpenAI.CreateEvalLabelModelGrader](#openaicreateevallabelmodelgrader) or [OpenAI.EvalGraderStringCheck](#openaievalgraderstringcheck) or [OpenAI.EvalGraderTextSimilarity](#openaievalgradertextsimilarity) or [OpenAI.EvalGraderPython](#openaievalgraderpython) or [OpenAI.EvalGraderScoreModel](#openaievalgraderscoremodel) or [EvalGraderEndpoint](#evalgraderendpoint) | A list of testing criteria. | Yes |  |

### OpenAI.EvalApiError

An object representing an error response from the Eval API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The error code. | Yes |  |
| message | string | The error message. | Yes |  |

### OpenAI.EvalCustomDataSourceConfig

A CustomDataSourceConfig which specifies the schema of your `item` and optionally `sample` namespaces.
The response schema defines the shape of the data that will be:
- Used to define your testing criteria and
- What data is required when creating a run

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| schema | object | The json schema for the run data source items.<br>  Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.EvalGraderPython

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_tag | string | The image tag to use for the python script. | No |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | No |  |
| source | string | The source code of the python script. | Yes |  |
| type | enum | The object type, which is always `python`.<br>Possible values: `python` | Yes |  |

### OpenAI.EvalGraderScoreModel

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | array of [OpenAI.EvalItem](#openaievalitem) | The input messages evaluated by the grader. Supports text, output text, input image, and input audio content blocks, and may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| pass_threshold | number | The threshold for the score. | No |  |
| range | array of number | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params | [OpenAI.EvalGraderScoreModelSamplingParams](#openaievalgraderscoremodelsamplingparams) |  | No |  |
| └─ max_completions_tokens | integer or null |  | No |  |
| └─ reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| └─ seed | integer or null |  | No |  |
| └─ temperature | number or null |  | No |  |
| └─ top_p | number or null |  | No | 1 |
| type | enum | The object type, which is always `score_model`.<br>Possible values: `score_model` | Yes |  |

### OpenAI.EvalGraderScoreModelSamplingParams

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| max_completions_tokens | integer or null |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| seed | integer or null |  | No |  |
| temperature | number or null |  | No |  |
| top_p | number or null |  | No |  |

### OpenAI.EvalGraderStringCheck

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The input text. This may include template strings. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| operation | enum | The string check operation to perform. One of `eq`, `ne`, `like`, or `ilike`.<br>Possible values: `eq`, `ne`, `like`, `ilike` | Yes |  |
| reference | string | The reference text. This may include template strings. | Yes |  |
| type | enum | The object type, which is always `string_check`.<br>Possible values: `string_check` | Yes |  |

### OpenAI.EvalGraderTextSimilarity

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| evaluation_metric | enum | The evaluation metric to use. One of `cosine`, `fuzzy_match`, `bleu`,<br>  `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`,<br>  or `rouge_l`.<br>Possible values: `cosine`, `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
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
| content | [OpenAI.EvalItemContent](#openaievalitemcontent) | Inputs to the model - can contain template strings. Supports text, output text, input images, and input audio, either as a single item or an array of items. | Yes |  |
| role | enum | The role of the message input. One of `user`, `assistant`, `system`, or<br>  `developer`.<br>Possible values: `user`, `assistant`, `system`, `developer` | Yes |  |
| type | enum | The type of the message input. Always `message`.<br>Possible values: `message` | No |  |

### OpenAI.EvalItemContent

Inputs to the model - can contain template strings. Supports text, output text, input images, and input audio, either as a single item or an array of items.

**Type**: [OpenAI.EvalItemContentItem](#openaievalitemcontentitem) or [OpenAI.EvalItemContentArray](#openaievalitemcontentarray)

Inputs to the model - can contain template strings. Supports text, output text, input images, and input audio, either as a single item or an array of items.


### OpenAI.EvalItemContentArray

A list of inputs, each of which may be either an input text, output text, input
image, or input audio object.

**Array of**: [OpenAI.EvalItemContentItem](#openaievalitemcontentitem)


### OpenAI.EvalItemContentItem

A single content item: input text, output text, input image, or input audio.

**Type**: [OpenAI.EvalItemContentText](#openaievalitemcontenttext) or [OpenAI.EvalItemContentItemObject](#openaievalitemcontentitemobject)

A single content item: input text, output text, input image, or input audio.


### OpenAI.EvalItemContentItemObject

A single content item: input text, output text, input image, or input audio.


### Discriminator for OpenAI.EvalItemContentItemObject

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `output_text` | [OpenAI.EvalItemContentOutputText](#openaievalitemcontentoutputtext) |
| `input_image` | [OpenAI.EvalItemInputImage](#openaievaliteminputimage) |
| `input_audio` | [OpenAI.InputAudio](#openaiinputaudio) |
| `input_text` | [OpenAI.EvalItemContentItemObjectInputTextContent](#openaievalitemcontentitemobjectinputtextcontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.EvalItemContentItemObjectType](#openaievalitemcontentitemobjecttype) |  | Yes |  |

### OpenAI.EvalItemContentItemObjectInputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.EvalItemContentItemObjectType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`output_text`<br>`input_image`<br>`input_audio` |

### OpenAI.EvalItemContentOutputText

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.EvalItemContentText

A text input to the model.

**Type**: string


### OpenAI.EvalItemInputImage

An image input block used within EvalItem content arrays.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | string | The detail level of the image to be sent to the model. One of `high`, `low`, or `auto`. Defaults to `auto`. | No |  |
| image_url | string | The URL of the image input. | Yes |  |
| type | enum | The type of the image input. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.EvalJsonlFileContentSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.EvalJsonlFileContentSourceContent](#openaievaljsonlfilecontentsourcecontent) | The content of the jsonl file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_content`.<br>Possible values: `file_content` | Yes |  |

### OpenAI.EvalJsonlFileContentSourceContent

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item | object |  | Yes |  |
| sample | object |  | No |  |

### OpenAI.EvalJsonlFileIdSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The identifier of the file. | Yes |  |
| type | enum | The type of jsonl source. Always `file_id`.<br>Possible values: `file_id` | Yes |  |

### OpenAI.EvalList

An object representing a list of evals.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.Eval](#openaieval) | An array of eval objects. | Yes |  |
| first_id | string | The identifier of the first eval in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more evals available. | Yes |  |
| last_id | string | The identifier of the last eval in the data array. | Yes |  |
| object | enum | The type of this object. It is always set to "list".<br>Possible values: `list` | Yes |  |

### OpenAI.EvalLogsDataSourceConfig

A LogsDataSourceConfig which specifies the metadata property of your logs query.
This is usually metadata like `usecase=chatbot` or `prompt-version=v2`, etc.
The schema returned by this data source config is used to defined what variables are available in your evals.
`item` and `sample` are both defined when using this data source config.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| schema | object | The json schema for the run data source items.<br>  Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.EvalResponsesSource

A EvalResponsesSource object describing a run data source configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | integer or null |  | No |  |
| created_before | integer or null |  | No |  |
| instructions_search | string or null |  | No |  |
| metadata | object or null |  | No |  |
| model | string or null |  | No |  |
| reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) or null |  | No |  |
| temperature | number or null |  | No |  |
| tools | array of string or null |  | No |  |
| top_p | number or null |  | No |  |
| type | enum | The type of run data source. Always `responses`.<br>Possible values: `responses` | Yes |  |
| users | array of string or null |  | No |  |

### OpenAI.EvalRun

A schema representing an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | Unix timestamp (in seconds) when the evaluation run was created. | Yes |  |
| data_source | [OpenAI.CreateEvalJsonlRunDataSource](#openaicreateevaljsonlrundatasource) or [OpenAI.CreateEvalCompletionsRunDataSource](#openaicreateevalcompletionsrundatasource) or [OpenAI.CreateEvalResponsesRunDataSource](#openaicreateevalresponsesrundatasource) | Information about the run's data source. | Yes |  |
| error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | Yes |  |
| eval_id | string | The identifier of the associated evaluation. | Yes |  |
| id | string | Unique identifier for the evaluation run. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | Yes |  |
| model | string | The model that is evaluated, if applicable. | Yes |  |
| name | string | The name of the evaluation run. | Yes |  |
| object | enum | The type of the object. Always "eval.run".<br>Possible values: `eval.run` | Yes |  |
| per_model_usage | array of [OpenAI.EvalRunPerModelUsage](#openaievalrunpermodelusage) | Usage statistics for each model during the evaluation run. | Yes |  |
| per_testing_criteria_results | array of [OpenAI.EvalRunPerTestingCriteriaResults](#openaievalrunpertestingcriteriaresults) | Results per testing criteria applied during the evaluation run. | Yes |  |
| report_url | string | The URL to the rendered evaluation run report on the UI dashboard. | Yes |  |
| result_counts | [OpenAI.EvalRunResultCounts](#openaievalrunresultcounts) |  | Yes |  |
| └─ errored | integer |  | Yes |  |
| └─ failed | integer |  | Yes |  |
| └─ passed | integer |  | Yes |  |
| └─ total | integer |  | Yes |  |
| status | string | The status of the evaluation run. | Yes |  |

### OpenAI.EvalRunList

An object representing a list of runs for an evaluation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.EvalRun](#openaievalrun) | An array of eval run objects. | Yes |  |
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
| results | array of [OpenAI.EvalRunOutputItemResult](#openaievalrunoutputitemresult) | A list of grader results for this output item. | Yes |  |
| run_id | string | The identifier of the evaluation run associated with this output item. | Yes |  |
| sample | [OpenAI.EvalRunOutputItemSample](#openaievalrunoutputitemsample) |  | Yes |  |
| └─ error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | Yes |  |
| └─ finish_reason | string |  | Yes |  |
| └─ input | array of [OpenAI.EvalRunOutputItemSampleInput](#openaievalrunoutputitemsampleinput) |  | Yes |  |
| └─ max_completion_tokens | integer |  | Yes |  |
| └─ model | string |  | Yes |  |
| └─ output | array of [OpenAI.EvalRunOutputItemSampleOutput](#openaievalrunoutputitemsampleoutput) |  | Yes |  |
| └─ seed | integer |  | Yes |  |
| └─ temperature | number |  | Yes |  |
| └─ top_p | number |  | Yes |  |
| └─ usage | [OpenAI.EvalRunOutputItemSampleUsage](#openaievalrunoutputitemsampleusage) |  | Yes |  |
| status | string | The status of the evaluation run. | Yes |  |

### OpenAI.EvalRunOutputItemList

An object representing a list of output items for an evaluation run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.EvalRunOutputItem](#openaievalrunoutputitem) | An array of eval run output item objects. | Yes |  |
| first_id | string | The identifier of the first eval run output item in the data array. | Yes |  |
| has_more | boolean | Indicates whether there are more eval run output items available. | Yes |  |
| last_id | string | The identifier of the last eval run output item in the data array. | Yes |  |
| object | enum | The type of this object. It is always set to "list".<br>Possible values: `list` | Yes |  |

### OpenAI.EvalRunOutputItemResult

A single grader result for an evaluation run output item.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the grader. | Yes |  |
| passed | boolean | Whether the grader considered the output a pass. | Yes |  |
| sample | object or null | Optional sample or intermediate data produced by the grader. | No |  |
| score | number | The numeric score produced by the grader. | Yes |  |
| type | string | The grader type (for example, "string-check-grader"). | No |  |

### OpenAI.EvalRunOutputItemSample

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [OpenAI.EvalApiError](#openaievalapierror) | An object representing an error response from the Eval API. | Yes |  |
| finish_reason | string |  | Yes |  |
| input | array of [OpenAI.EvalRunOutputItemSampleInput](#openaievalrunoutputitemsampleinput) |  | Yes |  |
| max_completion_tokens | integer |  | Yes |  |
| model | string |  | Yes |  |
| output | array of [OpenAI.EvalRunOutputItemSampleOutput](#openaievalrunoutputitemsampleoutput) |  | Yes |  |
| seed | integer |  | Yes |  |
| temperature | number |  | Yes |  |
| top_p | number |  | Yes |  |
| usage | [OpenAI.EvalRunOutputItemSampleUsage](#openaievalrunoutputitemsampleusage) |  | Yes |  |

### OpenAI.EvalRunOutputItemSampleInput

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string |  | Yes |  |
| role | string |  | Yes |  |

### OpenAI.EvalRunOutputItemSampleOutput

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string |  | No |  |
| role | string |  | No |  |

### OpenAI.EvalRunOutputItemSampleUsage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cached_tokens | integer |  | Yes |  |
| completion_tokens | integer |  | Yes |  |
| prompt_tokens | integer |  | Yes |  |
| total_tokens | integer |  | Yes |  |

### OpenAI.EvalRunPerModelUsage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cached_tokens | integer |  | Yes |  |
| completion_tokens | integer |  | Yes |  |
| invocation_count | integer |  | Yes |  |
| model_name | string |  | Yes |  |
| prompt_tokens | integer |  | Yes |  |
| total_tokens | integer |  | Yes |  |

### OpenAI.EvalRunPerTestingCriteriaResults

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| failed | integer |  | Yes |  |
| passed | integer |  | Yes |  |
| testing_criteria | string |  | Yes |  |

### OpenAI.EvalRunResultCounts

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| errored | integer |  | Yes |  |
| failed | integer |  | Yes |  |
| passed | integer |  | Yes |  |
| total | integer |  | Yes |  |

### OpenAI.EvalStoredCompletionsDataSourceConfig

Deprecated in favor of LogsDataSourceConfig.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| schema | object | The json schema for the run data source items.<br>  Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| type | enum | The type of data source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.EvalStoredCompletionsSource

A StoredCompletionsRunDataSource configuration describing a set of filters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_after | integer or null |  | No |  |
| created_before | integer or null |  | No |  |
| limit | integer or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string or null |  | No |  |
| type | enum | The type of source. Always `stored_completions`.<br>Possible values: `stored_completions` | Yes |  |

### OpenAI.FileCitationBody

A citation to a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The ID of the file. | Yes |  |
| filename | string | The filename of the file cited. | Yes |  |
| index | integer | The index of the file in the list of files. | Yes |  |
| type | enum | The type of the file citation. Always `file_citation`.<br>Possible values: `file_citation` | Yes |  |

### OpenAI.FilePath

A path to a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The ID of the file. | Yes |  |
| index | integer | The index of the file in the list of files. | Yes |  |
| type | enum | The type of the file path. Always `file_path`.<br>Possible values: `file_path` | Yes |  |

### OpenAI.FileSearchRanker

The ranker to use for the file search. If not specified will use the `auto` ranker.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `auto`<br>`default_2024_08_21` |

### OpenAI.FileSearchRankingOptions

The ranking options for the file search. If not specified, the file search tool will use the `auto` ranker and a score_threshold of 0.
See the [file search tool documentation](https://platform.openai.com/docs/assistants/tools/file-search#customizing-file-search-settings) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| ranker | [OpenAI.FileSearchRanker](#openaifilesearchranker) | The ranker to use for the file search. If not specified will use the `auto` ranker. | No |  |
| score_threshold | number | The score threshold for the file search. All values must be a floating point number between 0 and 1.<br>**Constraints:** min: 0, max: 1 | Yes |  |

### OpenAI.FileSearchTool

A tool that searches for relevant content from uploaded files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | [OpenAI.Filters](#openaifilters) or null |  | No |  |
| max_num_results | integer | The maximum number of results to return. This number should be between 1 and 50 inclusive. | No |  |
| ranking_options | [OpenAI.RankingOptions](#openairankingoptions) |  | No |  |
| └─ hybrid_search | [OpenAI.HybridSearchOptions](#openaihybridsearchoptions) | Weights that control how reciprocal rank fusion balances semantic embedding matches versus sparse keyword matches when hybrid search is enabled. | No |  |
| └─ ranker | [OpenAI.RankerVersionType](#openairankerversiontype) | The ranker to use for the file search. | No |  |
| └─ score_threshold | number | The score threshold for the file search, a number between 0 and 1. Numbers closer to 1 will attempt to return only the most relevant results, but may return fewer results. | No |  |
| type | enum | The type of the file search tool. Always `file_search`.<br>Possible values: `file_search` | Yes |  |
| vector_store_ids | array of string | The IDs of the vector stores to search. | Yes |  |

### OpenAI.FileSearchToolCallResults

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | No |  |
| file_id | string |  | No |  |
| filename | string |  | No |  |
| score | number |  | No |  |
| text | string |  | No |  |

### OpenAI.Filters

**Type**: [OpenAI.ComparisonFilter](#openaicomparisonfilter) or [OpenAI.CompoundFilter](#openaicompoundfilter)


### OpenAI.FineTuneDPOHyperparameters

The hyperparameters used for the DPO fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or integer | Number of examples in each batch. A larger batch size means that model parameters are updated less frequently, but with lower variance. | No |  |
| beta | string or number | The beta value for the DPO method. A higher beta value will increase the weight of the penalty between the policy and reference model. | No |  |
| learning_rate_multiplier | string or number | Scaling factor for the learning rate. A smaller learning rate may be useful to avoid overfitting. | No |  |
| n_epochs | string or integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |

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
| batch_size | string or integer | Number of examples in each batch. A larger batch size means that model parameters are updated less frequently, but with lower variance. | No |  |
| compute_multiplier | string or number | Multiplier on amount of compute used for exploring search space during training. | No |  |
| eval_interval | string or integer | The number of training steps between evaluation runs. | No |  |
| eval_samples | string or integer | Number of evaluation samples to generate per training step. | No |  |
| learning_rate_multiplier | string or number | Scaling factor for the learning rate. A smaller learning rate may be useful to avoid overfitting. | No |  |
| n_epochs | string or integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |
| reasoning_effort | enum | Level of reasoning effort.<br>Possible values: `default`, `low`, `medium`, `high` | No |  |

### OpenAI.FineTuneSupervisedHyperparameters

The hyperparameters used for the fine-tuning job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or integer | Number of examples in each batch. A larger batch size means that model parameters are updated less frequently, but with lower variance. | No |  |
| learning_rate_multiplier | string or number | Scaling factor for the learning rate. A smaller learning rate may be useful to avoid overfitting. | No |  |
| n_epochs | string or integer | The number of epochs to train the model for. An epoch refers to one full cycle through the training dataset. | No |  |

### OpenAI.FineTuneSupervisedMethod

Configuration for the supervised fine-tuning method.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hyperparameters | [OpenAI.FineTuneSupervisedHyperparameters](#openaifinetunesupervisedhyperparameters) | The hyperparameters used for the fine-tuning job. | No |  |

### OpenAI.FineTuningCheckpointPermission

The `checkpoint.permission` object represents a permission for a fine-tuned model checkpoint.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the permission was created. | Yes |  |
| id | string | The permission identifier, which can be referenced in the API endpoints. | Yes |  |
| object | enum | The object type, which is always "checkpoint.permission".<br>Possible values: `checkpoint.permission` | Yes |  |
| project_id | string | The project identifier that the permission is for. | Yes |  |

### OpenAI.FineTuningIntegration

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the integration being enabled for the fine-tuning job<br>Possible values: `wandb` | Yes |  |
| wandb | [OpenAI.FineTuningIntegrationWandb](#openaifinetuningintegrationwandb) |  | Yes |  |
| └─ entity | string or null |  | No |  |
| └─ name | string or null |  | No |  |
| └─ project | string |  | Yes |  |
| └─ tags | array of string |  | No |  |

### OpenAI.FineTuningIntegrationWandb

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| entity | string or null |  | No |  |
| name | string or null |  | No |  |
| project | string |  | Yes |  |
| tags | array of string |  | No |  |

### OpenAI.FineTuningJob

The `fine_tuning.job` object represents a fine-tuning job that has been created through the API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the fine-tuning job was created. | Yes |  |
| error | [OpenAI.FineTuningJobError](#openaifinetuningjoberror) or null |  | Yes |  |
| estimated_finish | string or null |  | No |  |
| fine_tuned_model | string or null |  | Yes |  |
| finished_at | string or null |  | Yes |  |
| hyperparameters | [OpenAI.FineTuningJobHyperparameters](#openaifinetuningjobhyperparameters) |  | Yes |  |
| └─ batch_size | string or integer or null |  | No | auto |
| └─ learning_rate_multiplier | string or number |  | No |  |
| └─ n_epochs | string or integer |  | No | auto |
| id | string | The object identifier, which can be referenced in the API endpoints. | Yes |  |
| integrations | array of [OpenAI.FineTuningIntegration](#openaifinetuningintegration) or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| method | [OpenAI.FineTuneMethod](#openaifinetunemethod) | The method used for fine-tuning. | No |  |
| model | string | The base model that is being fine-tuned. | Yes |  |
| object | enum | The object type, which is always "fine_tuning.job".<br>Possible values: `fine_tuning.job` | Yes |  |
| organization_id | string | The organization that owns the fine-tuning job. | Yes |  |
| result_files | array of string | The compiled results file ID(s) for the fine-tuning job. You can retrieve the results with the [Files API](https://platform.openai.com/docs/api-reference/files/retrieve-contents). | Yes |  |
| seed | integer | The seed used for the fine-tuning job. | Yes |  |
| status | enum | The current status of the fine-tuning job, which can be either `validating_files`, `queued`, `running`, `succeeded`, `failed`, or `cancelled`.<br>Possible values: `validating_files`, `queued`, `running`, `succeeded`, `failed`, `cancelled` | Yes |  |
| trained_tokens | integer or null |  | Yes |  |
| training_file | string | The file ID used for training. You can retrieve the training data with the [Files API](https://platform.openai.com/docs/api-reference/files/retrieve-contents). | Yes |  |
| validation_file | string or null |  | Yes |  |

### OpenAI.FineTuningJobCheckpoint

The `fine_tuning.job.checkpoint` object represents a model checkpoint for a fine-tuning job that is ready to use.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the checkpoint was created. | Yes |  |
| fine_tuned_model_checkpoint | string | The name of the fine-tuned checkpoint model that is created. | Yes |  |
| fine_tuning_job_id | string | The name of the fine-tuning job that this checkpoint was created from. | Yes |  |
| id | string | The checkpoint identifier, which can be referenced in the API endpoints. | Yes |  |
| metrics | [OpenAI.FineTuningJobCheckpointMetrics](#openaifinetuningjobcheckpointmetrics) |  | Yes |  |
| └─ full_valid_loss | number |  | No |  |
| └─ full_valid_mean_token_accuracy | number |  | No |  |
| └─ step | number |  | No |  |
| └─ train_loss | number |  | No |  |
| └─ train_mean_token_accuracy | number |  | No |  |
| └─ valid_loss | number |  | No |  |
| └─ valid_mean_token_accuracy | number |  | No |  |
| object | enum | The object type, which is always "fine_tuning.job.checkpoint".<br>Possible values: `fine_tuning.job.checkpoint` | Yes |  |
| step_number | integer | The step number that the checkpoint was created at. | Yes |  |

### OpenAI.FineTuningJobCheckpointMetrics

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| full_valid_loss | number |  | No |  |
| full_valid_mean_token_accuracy | number |  | No |  |
| step | number |  | No |  |
| train_loss | number |  | No |  |
| train_mean_token_accuracy | number |  | No |  |
| valid_loss | number |  | No |  |
| valid_mean_token_accuracy | number |  | No |  |

### OpenAI.FineTuningJobError

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string |  | Yes |  |
| message | string |  | Yes |  |
| param | string or null |  | Yes |  |

### OpenAI.FineTuningJobEvent

Fine-tuning job event object

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the fine-tuning job was created. | Yes |  |
| data | [OpenAI.FineTuningJobEventData](#openaifinetuningjobeventdata) |  | No |  |
| id | string | The object identifier. | Yes |  |
| level | enum | The log level of the event.<br>Possible values: `info`, `warn`, `error` | Yes |  |
| message | string | The message of the event. | Yes |  |
| object | enum | The object type, which is always "fine_tuning.job.event".<br>Possible values: `fine_tuning.job.event` | Yes |  |
| type | enum | The type of event.<br>Possible values: `message`, `metrics` | No |  |

### OpenAI.FineTuningJobEventData

**Type**: object


### OpenAI.FineTuningJobHyperparameters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| batch_size | string or integer or null |  | No |  |
| learning_rate_multiplier | string or number |  | No |  |
| n_epochs | string or integer |  | No |  |

### OpenAI.FunctionAndCustomToolCallOutput


### Discriminator for OpenAI.FunctionAndCustomToolCallOutput

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `input_text` | [OpenAI.FunctionAndCustomToolCallOutputInputTextContent](#openaifunctionandcustomtoolcalloutputinputtextcontent) |
| `input_image` | [OpenAI.FunctionAndCustomToolCallOutputInputImageContent](#openaifunctionandcustomtoolcalloutputinputimagecontent) |
| `input_file` | [OpenAI.FunctionAndCustomToolCallOutputInputFileContent](#openaifunctionandcustomtoolcalloutputinputfilecontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.FunctionAndCustomToolCallOutputType](#openaifunctionandcustomtoolcalloutputtype) |  | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputInputFileContent

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string or null |  | No |  |
| file_url | string | The URL of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputInputImageContent

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.ImageDetail](#openaiimagedetail) |  | Yes |  |
| file_id | string or null |  | No |  |
| image_url | string or null |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputInputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.FunctionAndCustomToolCallOutputType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`input_image`<br>`input_file` |

### OpenAI.FunctionObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| name | string | The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64. | Yes |  |
| parameters | [OpenAI.FunctionParameters](#openaifunctionparameters) | The parameters the functions accepts, described as a JSON Schema object. See the [guide](https://platform.openai.com/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.<br>Omitting `parameters` defines a function with an empty parameter list. | No |  |
| strict | boolean or null |  | No |  |

### OpenAI.FunctionParameters

The parameters the functions accepts, described as a JSON Schema object. See the [guide](https://platform.openai.com/docs/guides/function-calling) for examples, and the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.
Omitting `parameters` defines a function with an empty parameter list.

**Type**: object


### OpenAI.FunctionShellAction

Execute a shell command.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| commands | array of string |  | Yes |  |
| max_output_length | integer or null |  | Yes |  |
| timeout_ms | integer or null |  | Yes |  |

### OpenAI.FunctionShellCallOutputContent

The content of a shell tool call output that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_by | string | The identifier of the actor that created the item. | No |  |
| outcome | [OpenAI.FunctionShellCallOutputOutcome](#openaifunctionshellcalloutputoutcome) | Represents either an exit outcome (with an exit code) or a timeout outcome for a shell call output chunk. | Yes |  |
| └─ type | [OpenAI.FunctionShellCallOutputOutcomeType](#openaifunctionshellcalloutputoutcometype) |  | Yes |  |
| stderr | string | The standard error output that was captured. | Yes |  |
| stdout | string | The standard output that was captured. | Yes |  |

### OpenAI.FunctionShellCallOutputExitOutcome

Indicates that the shell commands finished and returned an exit code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| exit_code | integer | Exit code from the shell process. | Yes |  |
| type | enum | The outcome type. Always `exit`.<br>Possible values: `exit` | Yes |  |

### OpenAI.FunctionShellCallOutputOutcome

Represents either an exit outcome (with an exit code) or a timeout outcome for a shell call output chunk.


### Discriminator for OpenAI.FunctionShellCallOutputOutcome

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `timeout` | [OpenAI.FunctionShellCallOutputTimeoutOutcome](#openaifunctionshellcalloutputtimeoutoutcome) |
| `exit` | [OpenAI.FunctionShellCallOutputExitOutcome](#openaifunctionshellcalloutputexitoutcome) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.FunctionShellCallOutputOutcomeType](#openaifunctionshellcalloutputoutcometype) |  | Yes |  |

### OpenAI.FunctionShellCallOutputOutcomeType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `timeout`<br>`exit` |

### OpenAI.FunctionShellCallOutputTimeoutOutcome

Indicates that the shell call exceeded its configured time limit.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The outcome type. Always `timeout`.<br>Possible values: `timeout` | Yes |  |

### OpenAI.FunctionShellToolParam

A tool that allows the model to execute shell commands.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the shell tool. Always `shell`.<br>Possible values: `shell` | Yes |  |

### OpenAI.FunctionTool

Defines a function in your own code the model can choose to call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string or null |  | No |  |
| name | string | The name of the function to call. | Yes |  |
| parameters | object or null |  | Yes |  |
| strict | boolean or null |  | Yes |  |
| type | enum | The type of the function tool. Always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.GraderMulti

A MultiGrader object combines the output of multiple graders to produce a single score.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| calculate_output | string | A formula to calculate the output based on grader results. | Yes |  |
| graders | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [GraderEndpoint](#graderendpoint) |  | Yes |  |
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
| input | array of [OpenAI.EvalItem](#openaievalitem) | The input messages evaluated by the grader. Supports text, output text, input image, and input audio content blocks, and may include template strings. | Yes |  |
| model | string | The model to use for the evaluation. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| range | array of number | The range of the score. Defaults to `[0, 1]`. | No |  |
| sampling_params | [OpenAI.EvalGraderScoreModelSamplingParams](#openaievalgraderscoremodelsamplingparams) |  | No |  |
| └─ max_completions_tokens | integer or null |  | No |  |
| └─ reasoning_effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| └─ seed | integer or null |  | No |  |
| └─ temperature | number or null |  | No |  |
| └─ top_p | number or null |  | No | 1 |
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
| evaluation_metric | enum | The evaluation metric to use. One of `cosine`, `fuzzy_match`, `bleu`,<br>  `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`,<br>  or `rouge_l`.<br>Possible values: `cosine`, `fuzzy_match`, `bleu`, `gleu`, `meteor`, `rouge_1`, `rouge_2`, `rouge_3`, `rouge_4`, `rouge_5`, `rouge_l` | Yes |  |
| input | string | The text being graded. | Yes |  |
| name | string | The name of the grader. | Yes |  |
| reference | string | The text being graded against. | Yes |  |
| type | enum | The type of grader.<br>Possible values: `text_similarity` | Yes |  |

### OpenAI.GrammarSyntax1

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `lark`<br>`regex` |

### OpenAI.HybridSearchOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| embedding_weight | number | The weight of the embedding in the reciprocal ranking fusion. | Yes |  |
| text_weight | number | The weight of the text in the reciprocal ranking fusion. | Yes |  |

### OpenAI.ImageDetail

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `low`<br>`high`<br>`auto` |

### OpenAI.ImageGenTool

A tool that generates images using the GPT image models.


**Valid models:**

```
gpt-image-1
gpt-image-1-mini
```

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Background type for the generated image. One of `transparent`,<br>  `opaque`, or `auto`. Default: `auto`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| input_fidelity | [OpenAI.InputFidelity](#openaiinputfidelity) or null |  | No |  |
| input_image_mask | [OpenAI.ImageGenToolInputImageMask](#openaiimagegentoolinputimagemask) |  | No |  |
| └─ file_id | string |  | No |  |
| └─ image_url | string |  | No |  |
| model | string (see valid models below) |  | No |  |
| moderation | enum | Moderation level for the generated image. Default: `auto`.<br>Possible values: `auto`, `low` | No |  |
| output_compression | integer | Compression level for the output image. Default: 100.<br>**Constraints:** min: 0, max: 100 | No | 100 |
| output_format | enum | The output format of the generated image. One of `png`, `webp`, or<br>  `jpeg`. Default: `png`.<br>Possible values: `png`, `webp`, `jpeg` | No |  |
| partial_images | integer | Number of partial images to generate in streaming mode, from 0 (default value) to 3.<br>**Constraints:** min: 0, max: 3 | No |  |
| quality | enum | The quality of the generated image. One of `low`, `medium`, `high`,<br>  or `auto`. Default: `auto`.<br>Possible values: `low`, `medium`, `high`, `auto` | No |  |
| size | enum | The size of the generated image. One of `1024x1024`, `1024x1536`,<br>  `1536x1024`, or `auto`. Default: `auto`.<br>Possible values: `1024x1024`, `1024x1536`, `1536x1024`, `auto` | No |  |
| type | enum | The type of the image generation tool. Always `image_generation`.<br>Possible values: `image_generation` | Yes |  |

### OpenAI.ImageGenToolInputImageMask

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | No |  |
| image_url | string |  | No |  |

### OpenAI.IncludeEnum

Specify additional output data to include in the model response. Currently supported values are:
- `web_search_call.action.sources`: Include the sources of the web search tool call.
- `code_interpreter_call.outputs`: Includes the outputs of python code execution in code interpreter tool call items.
- `computer_call_output.output.image_url`: Include image urls from the computer call output.
- `file_search_call.results`: Include the search results of the file search tool call.
- `message.input_image.image_url`: Include image urls from the input message.
- `message.output_text.logprobs`: Include logprobs with assistant messages.
- `reasoning.encrypted_content`: Includes an encrypted version of reasoning tokens in reasoning item outputs. This enables reasoning items to be used in multi-turn conversations when using the Responses API statelessly (like when the `store` parameter is set to `false`, or when an organization is enrolled in the zero data retention program).

| Property | Value |
|----------|-------|
| **Description** | Specify additional output data to include in the model response. Currently supported values are:
- `web_search_call.action.sources`: Include the sources of the web search tool call.
- `code_interpreter_call.outputs`: Includes the outputs of python code execution in code interpreter tool call items.
- `computer_call_output.output.image_url`: Include image urls from the computer call output.
- `file_search_call.results`: Include the search results of the file search tool call.
- `message.input_image.image_url`: Include image urls from the input message.
- `message.output_text.logprobs`: Include logprobs with assistant messages.
- `reasoning.encrypted_content`: Includes an encrypted version of reasoning tokens in reasoning item outputs. This enables reasoning items to be used in multi-turn conversations when using the Responses API statelessly (like when the `store` parameter is set to `false`, or when an organization is enrolled in the zero data retention program). |
| **Type** | string |
| **Values** | `file_search_call.results`<br>`web_search_call.results`<br>`web_search_call.action.sources`<br>`message.input_image.image_url`<br>`computer_call_output.output.image_url`<br>`code_interpreter_call.outputs`<br>`reasoning.encrypted_content`<br>`message.output_text.logprobs` |

### OpenAI.InputAudio

An audio input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_audio | [OpenAI.InputAudioInputAudio](#openaiinputaudioinputaudio) |  | Yes |  |
| type | enum | The type of the input item. Always `input_audio`.<br>Possible values: `input_audio` | Yes |  |

### OpenAI.InputAudioInputAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string |  | Yes |  |
| format | enum | <br>Possible values: `mp3`, `wav` | Yes |  |

### OpenAI.InputContent


### Discriminator for OpenAI.InputContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `input_text` | [OpenAI.InputContentInputTextContent](#openaiinputcontentinputtextcontent) |
| `input_image` | [OpenAI.InputContentInputImageContent](#openaiinputcontentinputimagecontent) |
| `input_file` | [OpenAI.InputContentInputFileContent](#openaiinputcontentinputfilecontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.InputContentType](#openaiinputcontenttype) |  | Yes |  |

### OpenAI.InputContentInputFileContent

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string or null |  | No |  |
| file_url | string | The URL of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.InputContentInputImageContent

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.ImageDetail](#openaiimagedetail) |  | Yes |  |
| file_id | string or null |  | No |  |
| image_url | string or null |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.InputContentInputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.InputContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `input_text`<br>`input_image`<br>`input_file` |

### OpenAI.InputFidelity

Control how much effort the model will exert to match the style and features, especially facial features, of input images. This parameter is only supported for `gpt-image-1`. Unsupported for `gpt-image-1-mini`. Supports `high` and `low`. Defaults to `low`.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `high`<br>`low` |

### OpenAI.InputFileContent

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string or null |  | No |  |
| file_url | string | The URL of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.InputImageContent

An image input to the model. Learn about [image inputs](https://platform.openai.com/docs/guides/vision).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | [OpenAI.ImageDetail](#openaiimagedetail) |  | Yes |  |
| file_id | string or null |  | No |  |
| image_url | string or null |  | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.InputItem


### Discriminator for OpenAI.InputItem

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.EasyInputMessage](#openaieasyinputmessage) |
| `item_reference` | [OpenAI.ItemReferenceParam](#openaiitemreferenceparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.InputItemType](#openaiinputitemtype) |  | Yes |  |

### OpenAI.InputItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`item_reference` |

### OpenAI.InputMessageContentList

A list of one or many input items to the model, containing different content
types.

**Array of**: [OpenAI.InputContent](#openaiinputcontent)


### OpenAI.InputMessageResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | [OpenAI.InputMessageContentList](#openaiinputmessagecontentlist) | A list of one or many input items to the model, containing different content<br>types. | Yes |  |
| id | string | The unique ID of the message input. | Yes |  |
| role | enum | The role of the message input. One of `user`, `system`, or `developer`.<br>Possible values: `user`, `system`, `developer` | Yes |  |
| status | enum | The status of item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the message input. Always set to `message`.<br>Possible values: `message` | Yes |  |

### OpenAI.InputParam

Text, image, or file inputs to the model, used to generate a response.
Learn more:
- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
- [Image inputs](https://platform.openai.com/docs/guides/images)
- [File inputs](https://platform.openai.com/docs/guides/pdf-files)
- [Conversation state](https://platform.openai.com/docs/guides/conversation-state)
- [Function calling](https://platform.openai.com/docs/guides/function-calling)

**Type**: string or array of [OpenAI.InputItem](#openaiinputitem)

Text, image, or file inputs to the model, used to generate a response.
Learn more:
- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
- [Image inputs](https://platform.openai.com/docs/guides/images)
- [File inputs](https://platform.openai.com/docs/guides/pdf-files)
- [Conversation state](https://platform.openai.com/docs/guides/conversation-state)
- [Function calling](https://platform.openai.com/docs/guides/function-calling)


### OpenAI.InputTextContent

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.ItemReferenceParam

An internal identifier for an item to reference.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The ID of the item to reference. | Yes |  |
| type | enum | The type of item to reference. Always `item_reference`.<br>Possible values: `item_reference` | Yes |  |

### OpenAI.ItemResource

Content item used to generate a response.


### Discriminator for OpenAI.ItemResource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.InputMessageResource](#openaiinputmessageresource) |
| `output_message` | [OpenAI.ItemResourceOutputMessage](#openaiitemresourceoutputmessage) |
| `file_search_call` | [OpenAI.ItemResourceFileSearchToolCall](#openaiitemresourcefilesearchtoolcall) |
| `computer_call` | [OpenAI.ItemResourceComputerToolCall](#openaiitemresourcecomputertoolcall) |
| `computer_call_output` | [OpenAI.ItemResourceComputerToolCallOutputResource](#openaiitemresourcecomputertoolcalloutputresource) |
| `web_search_call` | [OpenAI.ItemResourceWebSearchToolCall](#openaiitemresourcewebsearchtoolcall) |
| `function_call` | [OpenAI.ItemResourceFunctionToolCallResource](#openaiitemresourcefunctiontoolcallresource) |
| `function_call_output` | [OpenAI.ItemResourceFunctionToolCallOutputResource](#openaiitemresourcefunctiontoolcalloutputresource) |
| `image_generation_call` | [OpenAI.ItemResourceImageGenToolCall](#openaiitemresourceimagegentoolcall) |
| `code_interpreter_call` | [OpenAI.ItemResourceCodeInterpreterToolCall](#openaiitemresourcecodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.ItemResourceLocalShellToolCall](#openaiitemresourcelocalshelltoolcall) |
| `local_shell_call_output` | [OpenAI.ItemResourceLocalShellToolCallOutput](#openaiitemresourcelocalshelltoolcalloutput) |
| `shell_call` | [OpenAI.ItemResourceFunctionShellCall](#openaiitemresourcefunctionshellcall) |
| `shell_call_output` | [OpenAI.ItemResourceFunctionShellCallOutput](#openaiitemresourcefunctionshellcalloutput) |
| `apply_patch_call` | [OpenAI.ItemResourceApplyPatchToolCall](#openaiitemresourceapplypatchtoolcall) |
| `apply_patch_call_output` | [OpenAI.ItemResourceApplyPatchToolCallOutput](#openaiitemresourceapplypatchtoolcalloutput) |
| `mcp_list_tools` | [OpenAI.ItemResourceMcpListTools](#openaiitemresourcemcplisttools) |
| `mcp_approval_request` | [OpenAI.ItemResourceMcpApprovalRequest](#openaiitemresourcemcpapprovalrequest) |
| `mcp_approval_response` | [OpenAI.ItemResourceMcpApprovalResponseResource](#openaiitemresourcemcpapprovalresponseresource) |
| `mcp_call` | [OpenAI.ItemResourceMcpToolCall](#openaiitemresourcemcptoolcall) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ItemResourceType](#openaiitemresourcetype) |  | Yes |  |

### OpenAI.ItemResourceApplyPatchToolCall

A tool call that applies file diffs by creating, deleting, or updating files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the apply patch tool call. Populated when this item is returned via API. | Yes |  |
| operation | [OpenAI.ApplyPatchFileOperation](#openaiapplypatchfileoperation) | One of the create_file, delete_file, or update_file operations applied via apply_patch. | Yes |  |
| └─ type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |
| status | [OpenAI.ApplyPatchCallStatus](#openaiapplypatchcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.ItemResourceApplyPatchToolCallOutput

The output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call output. | No |  |
| id | string | The unique ID of the apply patch tool call output. Populated when this item is returned via API. | Yes |  |
| output | string or null |  | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatus](#openaiapplypatchcalloutputstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.ItemResourceCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string or null |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) or null |  | Yes |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.ItemResourceComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.ItemResourceComputerToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The safety checks reported by the API that have been acknowledged by the<br>  developer. | No |  |
| call_id | string | The ID of the computer tool call that produced the output. | Yes |  |
| id | string | The ID of the computer tool call output. | No |  |
| output | [OpenAI.ComputerScreenshotImage](#openaicomputerscreenshotimage) | A computer screenshot image used with the computer use tool. | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the computer tool call output. Always `computer_call_output`.<br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.ItemResourceFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) or null |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.ItemResourceFunctionShellCall

A tool call that executes one or more shell commands in a managed environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellAction](#openaifunctionshellaction) | Execute a shell command. | Yes |  |
| └─ commands | array of string |  | Yes |  |
| └─ max_output_length | integer or null |  | Yes |  |
| └─ timeout_ms | integer or null |  | Yes |  |
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the shell tool call. Populated when this item is returned via API. | Yes |  |
| status | [OpenAI.LocalShellCallStatus](#openailocalshellcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.ItemResourceFunctionShellCallOutput

The output of a shell tool call that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The identifier of the actor that created the item. | No |  |
| id | string | The unique ID of the shell call output. Populated when this item is returned via API. | Yes |  |
| max_output_length | integer or null |  | Yes |  |
| output | array of [OpenAI.FunctionShellCallOutputContent](#openaifunctionshellcalloutputcontent) | An array of shell call output contents | Yes |  |
| type | enum | The type of the shell call output. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.ItemResourceFunctionToolCallOutputResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call output. Populated when this item<br>  is returned via API. | No |  |
| output | string or array of [OpenAI.FunctionAndCustomToolCallOutput](#openaifunctionandcustomtoolcalloutput) | The output from the function call generated by your code.<br>  Can be a string or a list of output content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call output. Always `function_call_output`.<br>Possible values: `function_call_output` | Yes |  |

### OpenAI.ItemResourceFunctionToolCallResource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.ItemResourceImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the image generation call. | Yes |  |
| result | string or null |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.ItemResourceLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.ItemResourceLocalShellToolCallOutput

The output of a local shell tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| status | string or null |  | No |  |
| type | enum | The type of the local shell tool call output. Always `local_shell_call_output`.<br>Possible values: `local_shell_call_output` | Yes |  |

### OpenAI.ItemResourceMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.ItemResourceMcpApprovalResponseResource

A response to an MCP approval request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| id | string | The unique ID of the approval response | Yes |  |
| reason | string or null |  | No |  |
| type | enum | The type of the item. Always `mcp_approval_response`.<br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.ItemResourceMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string or null |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.ItemResourceMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string or null |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string or null |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string or null |  | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.ItemResourceOutputMessage

An output message from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.OutputMessageContent](#openaioutputmessagecontent) | The content of the output message. | Yes |  |
| id | string | The unique ID of the output message. | Yes |  |
| role | enum | The role of the output message. Always `assistant`.<br>Possible values: `assistant` | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the output message. Always `message`.<br>Possible values: `output_message` | Yes |  |

### OpenAI.ItemResourceType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`output_message`<br>`file_search_call`<br>`computer_call`<br>`computer_call_output`<br>`web_search_call`<br>`function_call`<br>`function_call_output`<br>`image_generation_call`<br>`code_interpreter_call`<br>`local_shell_call`<br>`local_shell_call_output`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call` |

### OpenAI.ItemResourceWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.KeyPressAction

A collection of keypresses the model would like to perform.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| keys | array of string | The combination of keys the model is requesting to be pressed. This is an array of strings, each representing a key. | Yes |  |
| type | enum | Specifies the event type. For a keypress action, this property is always set to `keypress`.<br>Possible values: `keypress` | Yes |  |

### OpenAI.ListBatchesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.Batch](#openaibatch) |  | Yes |  |
| first_id | string |  | No |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListFilesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.OpenAIFile](#openaiopenaifile) |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | string |  | Yes |  |

### OpenAI.ListFineTuningCheckpointPermissionResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.FineTuningCheckpointPermission](#openaifinetuningcheckpointpermission) |  | Yes |  |
| first_id | string or null |  | No |  |
| has_more | boolean |  | Yes |  |
| last_id | string or null |  | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListFineTuningJobCheckpointsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.FineTuningJobCheckpoint](#openaifinetuningjobcheckpoint) |  | Yes |  |
| first_id | string or null |  | No |  |
| has_more | boolean |  | Yes |  |
| last_id | string or null |  | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListFineTuningJobEventsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.FineTuningJobEvent](#openaifinetuningjobevent) |  | Yes |  |
| has_more | boolean |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListMessagesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.MessageObject](#openaimessageobject) |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | string |  | Yes |  |

### OpenAI.ListModelsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.Model](#openaimodel) |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListPaginatedFineTuningJobsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.FineTuningJob](#openaifinetuningjob) |  | Yes |  |
| has_more | boolean |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListRunStepsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.RunStepObject](#openairunstepobject) |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | string |  | Yes |  |

### OpenAI.ListRunsResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.RunObject](#openairunobject) |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | string |  | Yes |  |

### OpenAI.ListVectorStoreFilesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.VectorStoreFileObject](#openaivectorstorefileobject) |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | string |  | Yes |  |

### OpenAI.ListVectorStoresResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.VectorStoreObject](#openaivectorstoreobject) |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | string |  | Yes |  |

### OpenAI.LocalShellCallStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete` |

### OpenAI.LocalShellExecAction

Execute a shell command on the server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| command | array of string | The command to run. | Yes |  |
| env | object | Environment variables to set for the command. | Yes |  |
| timeout_ms | integer or null |  | No |  |
| type | enum | The type of the local shell action. Always `exec`.<br>Possible values: `exec` | Yes |  |
| user | string or null |  | No |  |
| working_directory | string or null |  | No |  |

### OpenAI.LocalShellToolParam

A tool that allows the model to execute shell commands in a local environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the local shell tool. Always `local_shell`.<br>Possible values: `local_shell` | Yes |  |

### OpenAI.LogProb

The log probability of a token.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array of integer |  | Yes |  |
| logprob | number |  | Yes |  |
| token | string |  | Yes |  |
| top_logprobs | array of [OpenAI.TopLogProb](#openaitoplogprob) |  | Yes |  |

### OpenAI.MCPListToolsTool

A tool available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | [OpenAI.MCPListToolsToolAnnotations](#openaimcplisttoolstoolannotations) or null |  | No |  |
| description | string or null |  | No |  |
| input_schema | [OpenAI.MCPListToolsToolInputSchema](#openaimcplisttoolstoolinputschema) |  | Yes |  |
| name | string | The name of the tool. | Yes |  |

### OpenAI.MCPListToolsToolAnnotations

**Type**: object


### OpenAI.MCPListToolsToolInputSchema

**Type**: object


### OpenAI.MCPTool

Give the model access to additional tools via remote Model Context Protocol
(MCP) servers. [Learn more about MCP](https://platform.openai.com/docs/guides/tools-remote-mcp).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| allowed_tools | array of string or [OpenAI.MCPToolFilter](#openaimcptoolfilter) or null |  | No |  |
| authorization | string | An OAuth access token that can be used with a remote MCP server, either<br>  with a custom MCP server URL or a service connector. Your application<br>  must handle the OAuth authorization flow and provide the token here. | No |  |
| connector_id | enum | Identifier for service connectors, like those available in ChatGPT. One of<br>  `server_url` or `connector_id` must be provided. Learn more about service<br>  connectors [here](https://platform.openai.com/docs/guides/tools-remote-mcp#connectors).<br>  Currently supported `connector_id` values are:<br>  - Dropbox: `connector_dropbox`<br>  - Gmail: `connector_gmail`<br>  - Google Calendar: `connector_googlecalendar`<br>  - Google Drive: `connector_googledrive`<br>  - Microsoft Teams: `connector_microsoftteams`<br>  - Outlook Calendar: `connector_outlookcalendar`<br>  - Outlook Email: `connector_outlookemail`<br>  - SharePoint: `connector_sharepoint`<br>Possible values: `connector_dropbox`, `connector_gmail`, `connector_googlecalendar`, `connector_googledrive`, `connector_microsoftteams`, `connector_outlookcalendar`, `connector_outlookemail`, `connector_sharepoint` | No |  |
| headers | object or null |  | No |  |
| require_approval | [OpenAI.MCPToolRequireApproval](#openaimcptoolrequireapproval) or string or null |  | No |  |
| server_description | string | Optional description of the MCP server, used to provide more context. | No |  |
| server_label | string | A label for this MCP server, used to identify it in tool calls. | Yes |  |
| server_url | string | The URL for the MCP server. One of `server_url` or `connector_id` must be<br>  provided. | No |  |
| type | enum | The type of the MCP tool. Always `mcp`.<br>Possible values: `mcp` | Yes |  |

### OpenAI.MCPToolCallStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete`<br>`calling`<br>`failed` |

### OpenAI.MCPToolFilter

A filter object to specify which tools are allowed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| read_only | boolean | Indicates whether or not a tool modifies data or is read-only. If an<br>  MCP server is [annotated with `readOnlyHint`](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations-readonlyhint),<br>  it will match this filter. | No |  |
| tool_names | array of string | List of allowed tool names. | No |  |

### OpenAI.MCPToolRequireApproval

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| always | [OpenAI.MCPToolFilter](#openaimcptoolfilter) | A filter object to specify which tools are allowed. | No |  |
| never | [OpenAI.MCPToolFilter](#openaimcptoolfilter) | A filter object to specify which tools are allowed. | No |  |

### OpenAI.MessageContent


### Discriminator for OpenAI.MessageContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `image_url` | [OpenAI.MessageContentImageUrlObject](#openaimessagecontentimageurlobject) |
| `text` | [OpenAI.MessageContentTextObject](#openaimessagecontenttextobject) |
| `refusal` | [OpenAI.MessageContentRefusalObject](#openaimessagecontentrefusalobject) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.MessageContentType](#openaimessagecontenttype) |  | Yes |  |

### OpenAI.MessageContentImageFileObject

References an image [File](https://platform.openai.com/docs/api-reference/files) in the content of a message.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_file | [OpenAI.MessageContentImageFileObjectImageFile](#openaimessagecontentimagefileobjectimagefile) |  | Yes |  |
| type | enum | Always `image_file`.<br>Possible values: `image_file` | Yes |  |

### OpenAI.MessageContentImageFileObjectImageFile

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | enum | <br>Possible values: `auto`, `low`, `high` | No |  |
| file_id | string |  | Yes |  |

### OpenAI.MessageContentImageUrlObject

References an image URL in the content of a message.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_url | [OpenAI.MessageContentImageUrlObjectImageUrl](#openaimessagecontentimageurlobjectimageurl) |  | Yes |  |
| type | enum | The type of the content part.<br>Possible values: `image_url` | Yes |  |

### OpenAI.MessageContentImageUrlObjectImageUrl

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | enum | <br>Possible values: `auto`, `low`, `high` | No |  |
| url | string |  | Yes |  |

### OpenAI.MessageContentRefusalObject

The refusal content generated by the assistant.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string |  | Yes |  |
| type | enum | Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.MessageContentTextAnnotationsFileCitationObject

A citation within the message that points to a specific quote from a specific File associated with the assistant or the message. Generated when the assistant uses the "file_search" tool to search files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end_index | integer | **Constraints:** min: 0 | Yes |  |
| file_citation | [OpenAI.MessageContentTextAnnotationsFileCitationObjectFileCitation](#openaimessagecontenttextannotationsfilecitationobjectfilecitation) |  | Yes |  |
| start_index | integer | **Constraints:** min: 0 | Yes |  |
| text | string | The text in the message content that needs to be replaced. | Yes |  |
| type | enum | Always `file_citation`.<br>Possible values: `file_citation` | Yes |  |

### OpenAI.MessageContentTextAnnotationsFileCitationObjectFileCitation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | Yes |  |

### OpenAI.MessageContentTextAnnotationsFilePathObject

A URL for the file that's generated when the assistant used the `code_interpreter` tool to generate a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end_index | integer | **Constraints:** min: 0 | Yes |  |
| file_path | [OpenAI.MessageContentTextAnnotationsFilePathObjectFilePath](#openaimessagecontenttextannotationsfilepathobjectfilepath) |  | Yes |  |
| start_index | integer | **Constraints:** min: 0 | Yes |  |
| text | string | The text in the message content that needs to be replaced. | Yes |  |
| type | enum | Always `file_path`.<br>Possible values: `file_path` | Yes |  |

### OpenAI.MessageContentTextAnnotationsFilePathObjectFilePath

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | Yes |  |

### OpenAI.MessageContentTextObject

The text content that is part of a message.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | [OpenAI.MessageContentTextObjectText](#openaimessagecontenttextobjecttext) |  | Yes |  |
| type | enum | Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.MessageContentTextObjectText

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.TextAnnotation](#openaitextannotation) |  | Yes |  |
| value | string |  | Yes |  |

### OpenAI.MessageContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `image_file`<br>`image_url`<br>`text`<br>`refusal` |

### OpenAI.MessageObject

Represents a message within a [thread](https://platform.openai.com/docs/api-reference/threads).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| assistant_id | string or null |  | Yes |  |
| attachments | array of [OpenAI.MessageObjectAttachments](#openaimessageobjectattachments) or null |  | Yes |  |
| completed_at | string or null |  | Yes |  |
| content | array of [OpenAI.MessageContent](#openaimessagecontent) | The content of the message in array of text and/or images. | Yes |  |
| created_at | integer | The Unix timestamp (in seconds) for when the message was created. | Yes |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| incomplete_at | string or null |  | Yes |  |
| incomplete_details | [OpenAI.MessageObjectIncompleteDetails](#openaimessageobjectincompletedetails) or null |  | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | Yes |  |
| object | enum | The object type, which is always `thread.message`.<br>Possible values: `thread.message` | Yes |  |
| role | enum | The entity that produced the message. One of `user` or `assistant`.<br>Possible values: `user`, `assistant` | Yes |  |
| run_id | string or null |  | Yes |  |
| status | enum | The status of the message, which can be either `in_progress`, `incomplete`, or `completed`.<br>Possible values: `in_progress`, `incomplete`, `completed` | Yes |  |
| thread_id | string | The [thread](https://platform.openai.com/docs/api-reference/threads) ID that this message belongs to. | Yes |  |

### OpenAI.MessageObjectAttachments

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | No |  |
| tools | array of [OpenAI.AssistantToolsCode](#openaiassistanttoolscode) or [OpenAI.AssistantToolsFileSearchTypeOnly](#openaiassistanttoolsfilesearchtypeonly) |  | No |  |

### OpenAI.MessageObjectIncompleteDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reason | enum | <br>Possible values: `content_filter`, `max_tokens`, `run_cancelled`, `run_expired`, `run_failed` | Yes |  |

### OpenAI.MessageRequestContentTextObject

The text content that is part of a message.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | Text content to be sent to the model | Yes |  |
| type | enum | Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.MessageRole

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `unknown`<br>`user`<br>`assistant`<br>`system`<br>`critic`<br>`discriminator`<br>`developer`<br>`tool` |

### OpenAI.MessageStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`incomplete` |

### OpenAI.Metadata

Set of 16 key-value pairs that can be attached to an object. This can be
useful for storing additional information about the object in a structured
format, and querying for objects via API or the dashboard.
Keys are strings with a maximum length of 64 characters. Values are strings
with a maximum length of 512 characters.

**Type**: object


### OpenAI.Model

Describes an OpenAI model offering that can be used with the API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created | integer | The Unix timestamp (in seconds) when the model was created. | Yes |  |
| id | string | The model identifier, which can be referenced in the API endpoints. | Yes |  |
| object | enum | The object type, which is always "model".<br>Possible values: `model` | Yes |  |
| owned_by | string | The organization that owns the model. | Yes |  |

### OpenAI.ModifyMessageRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |

### OpenAI.ModifyRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |

### OpenAI.ModifyThreadRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| tool_resources | [OpenAI.ModifyThreadRequestToolResources](#openaimodifythreadrequesttoolresources) or null |  | No |  |

### OpenAI.ModifyThreadRequestToolResources

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter | [OpenAI.ModifyThreadRequestToolResourcesCodeInterpreter](#openaimodifythreadrequesttoolresourcescodeinterpreter) |  | No |  |
| file_search | [OpenAI.ModifyThreadRequestToolResourcesFileSearch](#openaimodifythreadrequesttoolresourcesfilesearch) |  | No |  |

### OpenAI.ModifyThreadRequestToolResourcesCodeInterpreter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_ids | array of string |  | No |  |

### OpenAI.ModifyThreadRequestToolResourcesFileSearch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| vector_store_ids | array of string |  | No |  |

### OpenAI.Move

A mouse move action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a move action, this property is<br>  always set to `move`.<br>Possible values: `move` | Yes |  |
| x | integer | The x-coordinate to move to. | Yes |  |
| y | integer | The y-coordinate to move to. | Yes |  |

### OpenAI.NoiseReductionType

Type of noise reduction. `near_field` is for close-talking microphones such as headphones, `far_field` is for far-field microphones such as laptop or conference room microphones.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `near_field`<br>`far_field` |

### OpenAI.OpenAIFile

The `File` object represents a document that has been uploaded to OpenAI.

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
| status_details | string (deprecated) | Deprecated. For details on why a fine-tuning training file failed validation, see the `error` field on `fine_tuning.job`. | No |  |

### OpenAI.OtherChunkingStrategyResponseParam

This is returned when the chunking strategy is unknown. Typically, this is because the file was indexed before the `chunking_strategy` concept was introduced in the API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Always `other`.<br>Possible values: `other` | Yes |  |

### OpenAI.OutputContent


### Discriminator for OpenAI.OutputContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `output_text` | [OpenAI.OutputContentOutputTextContent](#openaioutputcontentoutputtextcontent) |
| `refusal` | [OpenAI.OutputContentRefusalContent](#openaioutputcontentrefusalcontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.OutputContentType](#openaioutputcontenttype) |  | Yes |  |

### OpenAI.OutputContentOutputTextContent

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.Annotation](#openaiannotation) | The annotations of the text output. | Yes |  |
| logprobs | array of [OpenAI.LogProb](#openailogprob) |  | No |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.OutputContentRefusalContent

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanation from the model. | Yes |  |
| type | enum | The type of the refusal. Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.OutputContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `output_text`<br>`refusal`<br>`reasoning_text` |

### OpenAI.OutputItem


### Discriminator for OpenAI.OutputItem

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `output_message` | [OpenAI.OutputItemOutputMessage](#openaioutputitemoutputmessage) |
| `file_search_call` | [OpenAI.OutputItemFileSearchToolCall](#openaioutputitemfilesearchtoolcall) |
| `function_call` | [OpenAI.OutputItemFunctionToolCall](#openaioutputitemfunctiontoolcall) |
| `web_search_call` | [OpenAI.OutputItemWebSearchToolCall](#openaioutputitemwebsearchtoolcall) |
| `computer_call` | [OpenAI.OutputItemComputerToolCall](#openaioutputitemcomputertoolcall) |
| `reasoning` | [OpenAI.OutputItemReasoningItem](#openaioutputitemreasoningitem) |
| `compaction` | [OpenAI.OutputItemCompactionBody](#openaioutputitemcompactionbody) |
| `image_generation_call` | [OpenAI.OutputItemImageGenToolCall](#openaioutputitemimagegentoolcall) |
| `code_interpreter_call` | [OpenAI.OutputItemCodeInterpreterToolCall](#openaioutputitemcodeinterpretertoolcall) |
| `local_shell_call` | [OpenAI.OutputItemLocalShellToolCall](#openaioutputitemlocalshelltoolcall) |
| `shell_call` | [OpenAI.OutputItemFunctionShellCall](#openaioutputitemfunctionshellcall) |
| `shell_call_output` | [OpenAI.OutputItemFunctionShellCallOutput](#openaioutputitemfunctionshellcalloutput) |
| `apply_patch_call` | [OpenAI.OutputItemApplyPatchToolCall](#openaioutputitemapplypatchtoolcall) |
| `apply_patch_call_output` | [OpenAI.OutputItemApplyPatchToolCallOutput](#openaioutputitemapplypatchtoolcalloutput) |
| `mcp_call` | [OpenAI.OutputItemMcpToolCall](#openaioutputitemmcptoolcall) |
| `mcp_list_tools` | [OpenAI.OutputItemMcpListTools](#openaioutputitemmcplisttools) |
| `mcp_approval_request` | [OpenAI.OutputItemMcpApprovalRequest](#openaioutputitemmcpapprovalrequest) |
| `custom_tool_call` | [OpenAI.OutputItemCustomToolCall](#openaioutputitemcustomtoolcall) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.OutputItemType](#openaioutputitemtype) |  | Yes |  |

### OpenAI.OutputItemApplyPatchToolCall

A tool call that applies file diffs by creating, deleting, or updating files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the apply patch tool call. Populated when this item is returned via API. | Yes |  |
| operation | [OpenAI.ApplyPatchFileOperation](#openaiapplypatchfileoperation) | One of the create_file, delete_file, or update_file operations applied via apply_patch. | Yes |  |
| └─ type | [OpenAI.ApplyPatchFileOperationType](#openaiapplypatchfileoperationtype) |  | Yes |  |
| status | [OpenAI.ApplyPatchCallStatus](#openaiapplypatchcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call`.<br>Possible values: `apply_patch_call` | Yes |  |

### OpenAI.OutputItemApplyPatchToolCallOutput

The output emitted by an apply patch tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the apply patch tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call output. | No |  |
| id | string | The unique ID of the apply patch tool call output. Populated when this item is returned via API. | Yes |  |
| output | string or null |  | No |  |
| status | [OpenAI.ApplyPatchCallOutputStatus](#openaiapplypatchcalloutputstatus) |  | Yes |  |
| type | enum | The type of the item. Always `apply_patch_call_output`.<br>Possible values: `apply_patch_call_output` | Yes |  |

### OpenAI.OutputItemCodeInterpreterToolCall

A tool call to run code.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string or null |  | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| id | string | The unique ID of the code interpreter tool call. | Yes |  |
| outputs | array of [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) or [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) or null |  | Yes |  |
| status | enum | The status of the code interpreter tool call. Valid values are `in_progress`, `completed`, `incomplete`, `interpreting`, and `failed`.<br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | The type of the code interpreter tool call. Always `code_interpreter_call`.<br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.OutputItemCompactionBody

A compaction item generated by the [`v1/responses/compact` API](https://platform.openai.com/docs/api-reference/responses/compact).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_by | string | The identifier of the actor that created the item. | No |  |
| encrypted_content | string | The encrypted content that was produced by compaction. | Yes |  |
| id | string | The unique ID of the compaction item. | Yes |  |
| type | enum | The type of the item. Always `compaction`.<br>Possible values: `compaction` | Yes |  |

### OpenAI.OutputItemComputerToolCall

A tool call to a computer use tool. See the
[computer use guide](https://platform.openai.com/docs/guides/tools-computer-use) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| id | string | The unique ID of the computer call. | Yes |  |
| pending_safety_checks | array of [OpenAI.ComputerCallSafetyCheckParam](#openaicomputercallsafetycheckparam) | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the computer call. Always `computer_call`.<br>Possible values: `computer_call` | Yes |  |

### OpenAI.OutputItemCustomToolCall

A call to a custom tool created by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | An identifier used to map this custom tool call to a tool call output. | Yes |  |
| id | string | The unique ID of the custom tool call in the OpenAI platform. | No |  |
| input | string | The input for the custom tool call generated by the model. | Yes |  |
| name | string | The name of the custom tool being called. | Yes |  |
| type | enum | The type of the custom tool call. Always `custom_tool_call`.<br>Possible values: `custom_tool_call` | Yes |  |

### OpenAI.OutputItemFileSearchToolCall

The results of a file search tool call. See the
[file search guide](https://platform.openai.com/docs/guides/tools-file-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the file search tool call. | Yes |  |
| queries | array of string | The queries used to search for files. | Yes |  |
| results | array of [OpenAI.FileSearchToolCallResults](#openaifilesearchtoolcallresults) or null |  | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`,<br>  `searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | The type of the file search tool call. Always `file_search_call`.<br>Possible values: `file_search_call` | Yes |  |

### OpenAI.OutputItemFunctionShellCall

A tool call that executes one or more shell commands in a managed environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.FunctionShellAction](#openaifunctionshellaction) | Execute a shell command. | Yes |  |
| └─ commands | array of string |  | Yes |  |
| └─ max_output_length | integer or null |  | Yes |  |
| └─ timeout_ms | integer or null |  | Yes |  |
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The ID of the entity that created this tool call. | No |  |
| id | string | The unique ID of the shell tool call. Populated when this item is returned via API. | Yes |  |
| status | [OpenAI.LocalShellCallStatus](#openailocalshellcallstatus) |  | Yes |  |
| type | enum | The type of the item. Always `shell_call`.<br>Possible values: `shell_call` | Yes |  |

### OpenAI.OutputItemFunctionShellCallOutput

The output of a shell tool call that was emitted.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the shell tool call generated by the model. | Yes |  |
| created_by | string | The identifier of the actor that created the item. | No |  |
| id | string | The unique ID of the shell call output. Populated when this item is returned via API. | Yes |  |
| max_output_length | integer or null |  | Yes |  |
| output | array of [OpenAI.FunctionShellCallOutputContent](#openaifunctionshellcalloutputcontent) | An array of shell call output contents | Yes |  |
| type | enum | The type of the shell call output. Always `shell_call_output`.<br>Possible values: `shell_call_output` | Yes |  |

### OpenAI.OutputItemFunctionToolCall

A tool call to run a function. See the
[function calling guide](https://platform.openai.com/docs/guides/function-calling) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| id | string | The unique ID of the function tool call. | No |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| type | enum | The type of the function tool call. Always `function_call`.<br>Possible values: `function_call` | Yes |  |

### OpenAI.OutputItemImageGenToolCall

An image generation request made by the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique ID of the image generation call. | Yes |  |
| result | string or null |  | Yes |  |
| status | enum | The status of the image generation call.<br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | The type of the image generation call. Always `image_generation_call`.<br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.OutputItemLocalShellToolCall

A tool call to run a command on the local shell.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| id | string | The unique ID of the local shell call. | Yes |  |
| status | enum | The status of the local shell call.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the local shell call. Always `local_shell_call`.<br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.OutputItemMcpApprovalRequest

A request for human approval of a tool invocation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| id | string | The unique ID of the approval request. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | The type of the item. Always `mcp_approval_request`.<br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.OutputItemMcpListTools

A list of tools available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string or null |  | No |  |
| id | string | The unique ID of the list. | Yes |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array of [OpenAI.MCPListToolsTool](#openaimcplisttoolstool) | The tools available on the server. | Yes |  |
| type | enum | The type of the item. Always `mcp_list_tools`.<br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.OutputItemMcpToolCall

An invocation of a tool on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string or null |  | No |  |
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string or null |  | No |  |
| id | string | The unique ID of the tool call. | Yes |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string or null |  | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| status | [OpenAI.MCPToolCallStatus](#openaimcptoolcallstatus) |  | No |  |
| type | enum | The type of the item. Always `mcp_call`.<br>Possible values: `mcp_call` | Yes |  |

### OpenAI.OutputItemOutputMessage

An output message from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.OutputMessageContent](#openaioutputmessagecontent) | The content of the output message. | Yes |  |
| id | string | The unique ID of the output message. | Yes |  |
| role | enum | The role of the output message. Always `assistant`.<br>Possible values: `assistant` | Yes |  |
| status | enum | The status of the message input. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when input items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the output message. Always `message`.<br>Possible values: `output_message` | Yes |  |

### OpenAI.OutputItemReasoningItem

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually
[managing context](https://platform.openai.com/docs/guides/conversation-state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.ReasoningTextContent](#openaireasoningtextcontent) | Reasoning text content. | No |  |
| encrypted_content | string or null |  | No |  |
| id | string | The unique identifier of the reasoning content. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>  `incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | No |  |
| summary | array of [OpenAI.Summary](#openaisummary) | Reasoning summary content. | Yes |  |
| type | enum | The type of the object. Always `reasoning`.<br>Possible values: `reasoning` | Yes |  |

### OpenAI.OutputItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `output_message`<br>`file_search_call`<br>`function_call`<br>`web_search_call`<br>`computer_call`<br>`reasoning`<br>`compaction`<br>`image_generation_call`<br>`code_interpreter_call`<br>`local_shell_call`<br>`shell_call`<br>`shell_call_output`<br>`apply_patch_call`<br>`apply_patch_call_output`<br>`mcp_call`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`custom_tool_call` |

### OpenAI.OutputItemWebSearchToolCall

The results of a web search tool call. See the
[web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) or [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) or [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) | An object describing the specific action taken in this web search call.<br>  Includes details on how the model used the web (search, open_page, find). | Yes |  |
| id | string | The unique ID of the web search tool call. | Yes |  |
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | The type of the web search tool call. Always `web_search_call`.<br>Possible values: `web_search_call` | Yes |  |

### OpenAI.OutputMessageContent


### Discriminator for OpenAI.OutputMessageContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `output_text` | [OpenAI.OutputMessageContentOutputTextContent](#openaioutputmessagecontentoutputtextcontent) |
| `refusal` | [OpenAI.OutputMessageContentRefusalContent](#openaioutputmessagecontentrefusalcontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.OutputMessageContentType](#openaioutputmessagecontenttype) |  | Yes |  |

### OpenAI.OutputMessageContentOutputTextContent

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.Annotation](#openaiannotation) | The annotations of the text output. | Yes |  |
| logprobs | array of [OpenAI.LogProb](#openailogprob) |  | No |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.OutputMessageContentRefusalContent

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanation from the model. | Yes |  |
| type | enum | The type of the refusal. Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.OutputMessageContentType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `output_text`<br>`refusal` |

### OpenAI.OutputTextContent

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array of [OpenAI.Annotation](#openaiannotation) | The annotations of the text output. | Yes |  |
| logprobs | array of [OpenAI.LogProb](#openailogprob) |  | No |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.ParallelToolCalls

Whether to enable [parallel function calling](https://platform.openai.com/docs/guides/function-calling#configuring-parallel-function-calling) during tool use.

**Type**: boolean


### OpenAI.PredictionContent

Static predicted output content, such as the content of a text file that is
being regenerated.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array of [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext) | The content that should be matched when generating a model response.<br>  If generated tokens would match this content, the entire model response<br>  can be returned much more quickly. | Yes |  |
| type | enum | The type of the predicted content you want to provide. This type is<br>  currently always `content`.<br>Possible values: `content` | Yes |  |

### OpenAI.Prompt

Reference to a prompt template and its variables.
[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique identifier of the prompt template to use. | Yes |  |
| variables | [OpenAI.ResponsePromptVariables](#openairesponsepromptvariables) or null |  | No |  |
| version | string or null |  | No |  |

### OpenAI.RankerVersionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `auto`<br>`default-2024-11-15` |

### OpenAI.RankingOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hybrid_search | [OpenAI.HybridSearchOptions](#openaihybridsearchoptions) |  | No |  |
| └─ embedding_weight | number | The weight of the embedding in the reciprocal ranking fusion. | Yes |  |
| └─ text_weight | number | The weight of the text in the reciprocal ranking fusion. | Yes |  |
| ranker | [OpenAI.RankerVersionType](#openairankerversiontype) |  | No |  |
| score_threshold | number | The score threshold for the file search, a number between 0 and 1. Numbers closer to 1 will attempt to return only the most relevant results, but may return fewer results. | No |  |

### OpenAI.RealtimeAudioFormats


### Discriminator for OpenAI.RealtimeAudioFormats

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `audio/pcm` | [OpenAI.RealtimeAudioFormatsAudioPcm](#openairealtimeaudioformatsaudiopcm) |
| `audio/pcmu` | [OpenAI.RealtimeAudioFormatsAudioPcmu](#openairealtimeaudioformatsaudiopcmu) |
| `audio/pcma` | [OpenAI.RealtimeAudioFormatsAudioPcma](#openairealtimeaudioformatsaudiopcma) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.RealtimeAudioFormatsType](#openairealtimeaudioformatstype) |  | Yes |  |

### OpenAI.RealtimeAudioFormatsAudioPcm

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| rate | enum | <br>Possible values: `24000` | No |  |
| type | enum | <br>Possible values: `audio/pcm` | Yes |  |

### OpenAI.RealtimeAudioFormatsAudioPcma

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `audio/pcma` | Yes |  |

### OpenAI.RealtimeAudioFormatsAudioPcmu

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `audio/pcmu` | Yes |  |

### OpenAI.RealtimeAudioFormatsType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `audio/pcm`<br>`audio/pcmu`<br>`audio/pcma` |

### OpenAI.RealtimeCallCreateRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| sdp | string | WebRTC Session Description Protocol (SDP) offer generated by the caller. | Yes |  |
| session | [OpenAI.RealtimeSessionCreateRequestGA](#openairealtimesessioncreaterequestga) | Realtime session object configuration. | No |  |
| └─ audio | [OpenAI.RealtimeSessionCreateRequestGAAudio](#openairealtimesessioncreaterequestgaaudio) | Configuration for input and output audio. | No |  |
| └─ include | array of string | Additional fields to include in server outputs.<br>  `item.input_audio_transcription.logprobs`: Include logprobs for input audio transcription. | No |  |
| └─ instructions | string | The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses. The model can be instructed on response content and format, (for example "be extremely succinct", "act friendly", "here are examples of good responses") and on audio behavior (for example "talk quickly", "inject emotion into your voice", "laugh frequently"). The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior.<br>  Note that the server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session. | No |  |
| └─ max_output_tokens | integer (see valid models below) | Maximum number of output tokens for a single assistant response,<br>  inclusive of tool calls. Provide an integer between 1 and 4096 to<br>  limit output tokens, or `inf` for the maximum available tokens for a<br>  given model. Defaults to `inf`. | No |  |
| └─ model | string | The Realtime model used for this session. | No |  |
| └─ output_modalities | array of string | The set of modalities the model can respond with. It defaults to `["audio"]`, indicating<br>  that the model will respond with audio plus a transcript. `["text"]` can be used to make<br>  the model respond with text only. It is not possible to request both `text` and `audio` at the same time. | No | ['audio'] |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceFunction](#openaitoolchoicefunction) or [OpenAI.ToolChoiceMCP](#openaitoolchoicemcp) | How the model chooses tools. Provide one of the string modes or force a specific<br>  function/MCP tool. | No | auto |
| └─ tools | array of [OpenAI.RealtimeFunctionTool](#openairealtimefunctiontool) or [OpenAI.MCPTool](#openaimcptool) | Tools available to the model. | No |  |
| └─ tracing | string or [OpenAI.RealtimeSessionCreateRequestGATracing](#openairealtimesessioncreaterequestgatracing) or null | "" Set to null to disable tracing. Once<br>  tracing is enabled for a session, the configuration cannot be modified.<br>  `auto` will create a trace for the session with default values for the<br>  workflow name, group id, and metadata. | No | auto |
| └─ truncation | [OpenAI.RealtimeTruncation](#openairealtimetruncation) | When the number of tokens in a conversation exceeds the model's input token limit, the conversation be truncated, meaning messages (starting from the oldest) will not be included in the model's context. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.<br>Clients can configure truncation behavior to truncate with a lower max token limit, which is an effective way to control token usage and cost.<br>Truncation will reduce the number of cached tokens on the next turn (busting the cache), since messages are dropped from the beginning of the context. However, clients can also configure truncation to retain messages up to a fraction of the maximum context size, which will reduce the need for future truncations and thus improve the cache rate.<br>Truncation can be disabled entirely, which means the server will never truncate but would instead return an error if the conversation exceeds the model's input token limit. | No |  |
| └─ type | enum | The type of session to create. Always `realtime` for the Realtime API.<br>Possible values: `realtime` | Yes |  |

### OpenAI.RealtimeCallReferRequest

Parameters required to transfer a SIP call to a new destination using the
Realtime API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| target_uri | string | URI that should appear in the SIP Refer-To header. Supports values like<br>  `tel:+14155550123` or `sip:agent\@example.com`. | Yes |  |

### OpenAI.RealtimeCallRejectRequest

Parameters used to decline an incoming SIP call handled by the Realtime API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| status_code | integer | SIP response code to send back to the caller. Defaults to `603` (Decline)<br>  when omitted. | No |  |

### OpenAI.RealtimeCreateClientSecretRequest

Create a session and client secret for the Realtime API. The request can specify
either a realtime or a transcription session configuration.
[Learn more about the Realtime API](https://platform.openai.com/docs/guides/realtime).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | [OpenAI.RealtimeCreateClientSecretRequestExpiresAfter](#openairealtimecreateclientsecretrequestexpiresafter) |  | No |  |
| └─ anchor | enum | <br>Possible values: `created_at` | No |  |
| └─ seconds | integer | **Constraints:** min: 10, max: 7200 | No | 600 |
| session | [OpenAI.RealtimeSessionCreateRequestUnion](#openairealtimesessioncreaterequestunion) |  | No |  |
| └─ type | [OpenAI.RealtimeSessionCreateRequestUnionType](#openairealtimesessioncreaterequestuniontype) |  | Yes |  |

### OpenAI.RealtimeCreateClientSecretRequestExpiresAfter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| anchor | enum | <br>Possible values: `created_at` | No |  |
| seconds | integer | **Constraints:** min: 10, max: 7200 | No | 600 |

### OpenAI.RealtimeCreateClientSecretResponse

Response from creating a session and client secret for the Realtime API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_at | integer | Expiration timestamp for the client secret, in seconds since epoch. | Yes |  |
| session | [OpenAI.RealtimeSessionCreateResponseUnion](#openairealtimesessioncreateresponseunion) |  | Yes |  |
| └─ type | [OpenAI.RealtimeSessionCreateResponseUnionType](#openairealtimesessioncreateresponseuniontype) |  | Yes |  |
| value | string | The generated client secret value. | Yes |  |

### OpenAI.RealtimeFunctionTool

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | The description of the function, including guidance on when and how<br>  to call it, and guidance about what to tell the user when calling<br>  (if anything). | No |  |
| name | string | The name of the function. | No |  |
| parameters | [OpenAI.RealtimeFunctionToolParameters](#openairealtimefunctiontoolparameters) |  | No |  |
| type | enum | The type of the tool, i.e. `function`.<br>Possible values: `function` | No |  |

### OpenAI.RealtimeFunctionToolParameters

**Type**: object


### OpenAI.RealtimeSessionCreateRequest

A new Realtime session configuration, with an ephemeral key. Default TTL
for keys is one minute.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| client_secret | [OpenAI.RealtimeSessionCreateRequestClientSecret](#openairealtimesessioncreaterequestclientsecret) |  | Yes |  |
| └─ expires_at | integer |  | Yes |  |
| └─ value | string |  | Yes |  |
| input_audio_format | string | The format of input audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`. | No |  |
| input_audio_transcription | [OpenAI.RealtimeSessionCreateRequestInputAudioTranscription](#openairealtimesessioncreaterequestinputaudiotranscription) |  | No |  |
| └─ model | string |  | No |  |
| instructions | string | The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses. The model can be instructed on response content and format, (for example "be extremely succinct", "act friendly", "here are examples of good responses") and on audio behavior (for example "talk quickly", "inject emotion into your voice", "laugh frequently"). The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior.<br>  Note that the server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session. | No |  |
| max_response_output_tokens | integer (see valid models below) | Maximum number of output tokens for a single assistant response,<br>  inclusive of tool calls. Provide an integer between 1 and 4096 to<br>  limit output tokens, or `inf` for the maximum available tokens for a<br>  given model. Defaults to `inf`. | No |  |
| modalities | array of string | The set of modalities the model can respond with. To disable audio,<br>  set this to ["text"]. | No | ['text', 'audio'] |
| output_audio_format | string | The format of output audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`. | No |  |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| speed | number | The speed of the model's spoken response. 1.0 is the default speed. 0.25 is<br>  the minimum speed. 1.5 is the maximum speed. This value can only be changed<br>  in between model turns, not while a response is in progress.<br>**Constraints:** min: 0.25, max: 1.5 | No | 1 |
| temperature | number | Sampling temperature for the model, limited to [0.6, 1.2]. Defaults to 0.8. | No |  |
| tool_choice | string | How the model chooses tools. Options are `auto`, `none`, `required`, or<br>  specify a function. | No |  |
| tools | array of [OpenAI.RealtimeSessionCreateRequestTools](#openairealtimesessioncreaterequesttools) | Tools (functions) available to the model. | No |  |
| tracing | string or object | Configuration options for tracing. Set to null to disable tracing. Once<br>  tracing is enabled for a session, the configuration cannot be modified.<br>  `auto` will create a trace for the session with default values for the<br>  workflow name, group id, and metadata. | No |  |
| truncation | [OpenAI.RealtimeTruncation](#openairealtimetruncation) | When the number of tokens in a conversation exceeds the model's input token limit, the conversation be truncated, meaning messages (starting from the oldest) will not be included in the model's context. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.<br>Clients can configure truncation behavior to truncate with a lower max token limit, which is an effective way to control token usage and cost.<br>Truncation will reduce the number of cached tokens on the next turn (busting the cache), since messages are dropped from the beginning of the context. However, clients can also configure truncation to retain messages up to a fraction of the maximum context size, which will reduce the need for future truncations and thus improve the cache rate.<br>Truncation can be disabled entirely, which means the server will never truncate but would instead return an error if the conversation exceeds the model's input token limit. | No |  |
| turn_detection | [OpenAI.RealtimeSessionCreateRequestTurnDetection](#openairealtimesessioncreaterequestturndetection) |  | No |  |
| └─ prefix_padding_ms | integer |  | No |  |
| └─ silence_duration_ms | integer |  | No |  |
| └─ threshold | number |  | No |  |
| └─ type | string |  | No |  |
| type | enum | <br>Possible values: `realtime` | Yes |  |
| voice | [OpenAI.VoiceIdsShared](#openaivoiceidsshared) |  | No |  |

### OpenAI.RealtimeSessionCreateRequestClientSecret

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_at | integer |  | Yes |  |
| value | string |  | Yes |  |

### OpenAI.RealtimeSessionCreateRequestGA

Realtime session object configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | [OpenAI.RealtimeSessionCreateRequestGAAudio](#openairealtimesessioncreaterequestgaaudio) |  | No |  |
| └─ input | [OpenAI.RealtimeSessionCreateRequestGAAudioInput](#openairealtimesessioncreaterequestgaaudioinput) |  | No |  |
| └─ output | [OpenAI.RealtimeSessionCreateRequestGAAudioOutput](#openairealtimesessioncreaterequestgaaudiooutput) |  | No |  |
| include | array of string | Additional fields to include in server outputs.<br>  `item.input_audio_transcription.logprobs`: Include logprobs for input audio transcription. | No |  |
| instructions | string | The default system instructions (i.e. system message) prepended to model calls. This field allows the client to guide the model on desired responses. The model can be instructed on response content and format, (for example "be extremely succinct", "act friendly", "here are examples of good responses") and on audio behavior (for example "talk quickly", "inject emotion into your voice", "laugh frequently"). The instructions are not guaranteed to be followed by the model, but they provide guidance to the model on the desired behavior.<br>  Note that the server sets default instructions which will be used if this field is not set and are visible in the `session.created` event at the start of the session. | No |  |
| max_output_tokens | integer (see valid models below) | Maximum number of output tokens for a single assistant response,<br>  inclusive of tool calls. Provide an integer between 1 and 4096 to<br>  limit output tokens, or `inf` for the maximum available tokens for a<br>  given model. Defaults to `inf`. | No |  |
| model | string | The Realtime model used for this session. | No |  |
| output_modalities | array of string | The set of modalities the model can respond with. It defaults to `["audio"]`, indicating<br>  that the model will respond with audio plus a transcript. `["text"]` can be used to make<br>  the model respond with text only. It is not possible to request both `text` and `audio` at the same time. | No | ['audio'] |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceFunction](#openaitoolchoicefunction) or [OpenAI.ToolChoiceMCP](#openaitoolchoicemcp) | How the model chooses tools. Provide one of the string modes or force a specific<br>  function/MCP tool. | No |  |
| tools | array of [OpenAI.RealtimeFunctionTool](#openairealtimefunctiontool) or [OpenAI.MCPTool](#openaimcptool) | Tools available to the model. | No |  |
| tracing | string or [OpenAI.RealtimeSessionCreateRequestGATracing](#openairealtimesessioncreaterequestgatracing) or null | "" Set to null to disable tracing. Once<br>  tracing is enabled for a session, the configuration cannot be modified.<br>  `auto` will create a trace for the session with default values for the<br>  workflow name, group id, and metadata. | No |  |
| truncation | [OpenAI.RealtimeTruncation](#openairealtimetruncation) | When the number of tokens in a conversation exceeds the model's input token limit, the conversation be truncated, meaning messages (starting from the oldest) will not be included in the model's context. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.<br>Clients can configure truncation behavior to truncate with a lower max token limit, which is an effective way to control token usage and cost.<br>Truncation will reduce the number of cached tokens on the next turn (busting the cache), since messages are dropped from the beginning of the context. However, clients can also configure truncation to retain messages up to a fraction of the maximum context size, which will reduce the need for future truncations and thus improve the cache rate.<br>Truncation can be disabled entirely, which means the server will never truncate but would instead return an error if the conversation exceeds the model's input token limit. | No |  |
| type | enum | The type of session to create. Always `realtime` for the Realtime API.<br>Possible values: `realtime` | Yes |  |

### OpenAI.RealtimeSessionCreateRequestGAAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | [OpenAI.RealtimeSessionCreateRequestGAAudioInput](#openairealtimesessioncreaterequestgaaudioinput) |  | No |  |
| output | [OpenAI.RealtimeSessionCreateRequestGAAudioOutput](#openairealtimesessioncreaterequestgaaudiooutput) |  | No |  |

### OpenAI.RealtimeSessionCreateRequestGAAudioInput

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.RealtimeAudioFormats](#openairealtimeaudioformats) |  | No |  |
| noise_reduction | [OpenAI.RealtimeSessionCreateRequestGAAudioInputNoiseReduction](#openairealtimesessioncreaterequestgaaudioinputnoisereduction) |  | No |  |
| transcription | [OpenAI.AudioTranscription](#openaiaudiotranscription) |  | No |  |
| turn_detection | [OpenAI.RealtimeTurnDetection](#openairealtimeturndetection) |  | No |  |

### OpenAI.RealtimeSessionCreateRequestGAAudioInputNoiseReduction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.NoiseReductionType](#openainoisereductiontype) | Type of noise reduction. `near_field` is for close-talking microphones such as headphones, `far_field` is for far-field microphones such as laptop or conference room microphones. | No |  |

### OpenAI.RealtimeSessionCreateRequestGAAudioOutput

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.RealtimeAudioFormats](#openairealtimeaudioformats) |  | No |  |
| speed | number | **Constraints:** min: 0.25, max: 1.5 | No | 1 |
| voice | [OpenAI.VoiceIdsShared](#openaivoiceidsshared) |  | No |  |

### OpenAI.RealtimeSessionCreateRequestGATracing

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| group_id | string |  | No |  |
| metadata | object |  | No |  |
| workflow_name | string |  | No |  |

### OpenAI.RealtimeSessionCreateRequestInputAudioTranscription

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| model | string |  | No |  |

### OpenAI.RealtimeSessionCreateRequestTools

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string |  | No |  |
| name | string |  | No |  |
| parameters | [OpenAI.RealtimeSessionCreateRequestToolsParameters](#openairealtimesessioncreaterequesttoolsparameters) |  | No |  |
| type | enum | <br>Possible values: `function` | No |  |

### OpenAI.RealtimeSessionCreateRequestToolsParameters

**Type**: object


### OpenAI.RealtimeSessionCreateRequestTurnDetection

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prefix_padding_ms | integer |  | No |  |
| silence_duration_ms | integer |  | No |  |
| threshold | number |  | No |  |
| type | string |  | No |  |

### OpenAI.RealtimeSessionCreateRequestUnion


### Discriminator for OpenAI.RealtimeSessionCreateRequestUnion

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `realtime` | [OpenAI.RealtimeSessionCreateRequest](#openairealtimesessioncreaterequest) |
| `transcription` | [OpenAI.RealtimeTranscriptionSessionCreateRequest](#openairealtimetranscriptionsessioncreaterequest) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.RealtimeSessionCreateRequestUnionType](#openairealtimesessioncreaterequestuniontype) |  | Yes |  |

### OpenAI.RealtimeSessionCreateRequestUnionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `realtime`<br>`transcription` |

### OpenAI.RealtimeSessionCreateResponse

A Realtime session configuration object.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | [OpenAI.RealtimeSessionCreateResponseAudio](#openairealtimesessioncreateresponseaudio) |  | No |  |
| └─ input | [OpenAI.RealtimeSessionCreateResponseAudioInput](#openairealtimesessioncreateresponseaudioinput) |  | No |  |
| └─ output | [OpenAI.RealtimeSessionCreateResponseAudioOutput](#openairealtimesessioncreateresponseaudiooutput) |  | No |  |
| expires_at | integer | Expiration timestamp for the session, in seconds since epoch. | No |  |
| id | string | Unique identifier for the session that looks like `sess_1234567890abcdef`. | No |  |
| include | array of string | Additional fields to include in server outputs.<br>  - `item.input_audio_transcription.logprobs`: Include logprobs for input audio transcription. | No |  |
| instructions | string | The default system instructions (i.e. system message) prepended to model<br>  calls. This field allows the client to guide the model on desired<br>  responses. The model can be instructed on response content and format,<br>  (for example "be extremely succinct", "act friendly", "here are examples of good<br>  responses") and on audio behavior (for example "talk quickly", "inject emotion<br>  into your voice", "laugh frequently"). The instructions are not guaranteed<br>  to be followed by the model, but they provide guidance to the model on the<br>  desired behavior.<br>  Note that the server sets default instructions which will be used if this<br>  field is not set and are visible in the `session.created` event at the<br>  start of the session. | No |  |
| max_output_tokens | integer (see valid models below) | Maximum number of output tokens for a single assistant response,<br>  inclusive of tool calls. Provide an integer between 1 and 4096 to<br>  limit output tokens, or `inf` for the maximum available tokens for a<br>  given model. Defaults to `inf`. | No |  |
| model | string | The Realtime model used for this session. | No |  |
| object | string | The object type. Always `realtime.session`. | No |  |
| output_modalities | array of string | The set of modalities the model can respond with. To disable audio,<br>  set this to ["text"]. | No |  |
| tool_choice | string | How the model chooses tools. Options are `auto`, `none`, `required`, or<br>  specify a function. | No |  |
| tools | array of [OpenAI.RealtimeFunctionTool](#openairealtimefunctiontool) | Tools (functions) available to the model. | No |  |
| tracing | string or object | Configuration options for tracing. Set to null to disable tracing. Once<br>  tracing is enabled for a session, the configuration cannot be modified.<br>  `auto` will create a trace for the session with default values for the<br>  workflow name, group id, and metadata. | No |  |
| turn_detection | [OpenAI.RealtimeSessionCreateResponseTurnDetection](#openairealtimesessioncreateresponseturndetection) |  | No |  |
| └─ prefix_padding_ms | integer |  | No |  |
| └─ silence_duration_ms | integer |  | No |  |
| └─ threshold | number |  | No |  |
| └─ type | string |  | No |  |
| type | enum | <br>Possible values: `realtime` | Yes |  |

### OpenAI.RealtimeSessionCreateResponseAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | [OpenAI.RealtimeSessionCreateResponseAudioInput](#openairealtimesessioncreateresponseaudioinput) |  | No |  |
| output | [OpenAI.RealtimeSessionCreateResponseAudioOutput](#openairealtimesessioncreateresponseaudiooutput) |  | No |  |

### OpenAI.RealtimeSessionCreateResponseAudioInput

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.RealtimeAudioFormats](#openairealtimeaudioformats) |  | No |  |
| noise_reduction | [OpenAI.RealtimeSessionCreateResponseAudioInputNoiseReduction](#openairealtimesessioncreateresponseaudioinputnoisereduction) |  | No |  |
| transcription | [OpenAI.AudioTranscription](#openaiaudiotranscription) |  | No |  |
| turn_detection | [OpenAI.RealtimeSessionCreateResponseAudioInputTurnDetection](#openairealtimesessioncreateresponseaudioinputturndetection) |  | No |  |

### OpenAI.RealtimeSessionCreateResponseAudioInputNoiseReduction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.NoiseReductionType](#openainoisereductiontype) | Type of noise reduction. `near_field` is for close-talking microphones such as headphones, `far_field` is for far-field microphones such as laptop or conference room microphones. | No |  |

### OpenAI.RealtimeSessionCreateResponseAudioInputTurnDetection

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prefix_padding_ms | integer |  | No |  |
| silence_duration_ms | integer |  | No |  |
| threshold | number |  | No |  |
| type | string |  | No |  |

### OpenAI.RealtimeSessionCreateResponseAudioOutput

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.RealtimeAudioFormats](#openairealtimeaudioformats) |  | No |  |
| speed | number |  | No |  |
| voice | [OpenAI.VoiceIdsShared](#openaivoiceidsshared) |  | No |  |

### OpenAI.RealtimeSessionCreateResponseTurnDetection

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prefix_padding_ms | integer |  | No |  |
| silence_duration_ms | integer |  | No |  |
| threshold | number |  | No |  |
| type | string |  | No |  |

### OpenAI.RealtimeSessionCreateResponseUnion


### Discriminator for OpenAI.RealtimeSessionCreateResponseUnion

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `realtime` | [OpenAI.RealtimeSessionCreateResponse](#openairealtimesessioncreateresponse) |
| `transcription` | [OpenAI.RealtimeTranscriptionSessionCreateResponse](#openairealtimetranscriptionsessioncreateresponse) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.RealtimeSessionCreateResponseUnionType](#openairealtimesessioncreateresponseuniontype) |  | Yes |  |

### OpenAI.RealtimeSessionCreateResponseUnionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `realtime`<br>`transcription` |

### OpenAI.RealtimeTranscriptionSessionCreateRequest

Realtime transcription session object configuration.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include | array of string | The set of items to include in the transcription. Current available items are:<br>  `item.input_audio_transcription.logprobs` | No |  |
| input_audio_format | enum | The format of input audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`.<br>  For `pcm16`, input audio must be 16-bit PCM at a 24-kHz sample rate,<br>  single channel (mono), and little-endian byte order.<br>Possible values: `pcm16`, `g711_ulaw`, `g711_alaw` | No |  |
| input_audio_noise_reduction | [OpenAI.RealtimeTranscriptionSessionCreateRequestInputAudioNoiseReduction](#openairealtimetranscriptionsessioncreaterequestinputaudionoisereduction) |  | No |  |
| └─ type | [OpenAI.NoiseReductionType](#openainoisereductiontype) | Type of noise reduction. `near_field` is for close-talking microphones such as headphones, `far_field` is for far-field microphones such as laptop or conference room microphones. | No |  |
| input_audio_transcription | [OpenAI.AudioTranscription](#openaiaudiotranscription) |  | No |  |
| └─ language | string | The language of the input audio. Supplying the input language in<br>  [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format<br>  will improve accuracy and latency. | No |  |
| └─ model | string | The model to use for transcription. Current options are `whisper-1`, `gpt-4o-mini-transcribe`, `gpt-4o-mini-transcribe-2025-12-15`, `gpt-4o-transcribe`, and `gpt-4o-transcribe-diarize`. Use `gpt-4o-transcribe-diarize` when you need diarization with speaker labels. | No |  |
| └─ prompt | string | An optional text to guide the model's style or continue a previous audio<br>  segment.<br>  For `whisper-1`, the [prompt is a list of keywords](https://platform.openai.com/docs/guides/speech-to-text#prompting).<br>  For `gpt-4o-transcribe` models (excluding `gpt-4o-transcribe-diarize`), the prompt is a free text string, for example "expect words related to technology". | No |  |
| turn_detection | [OpenAI.RealtimeTranscriptionSessionCreateRequestTurnDetection](#openairealtimetranscriptionsessioncreaterequestturndetection) |  | No |  |
| └─ prefix_padding_ms | integer |  | No |  |
| └─ silence_duration_ms | integer |  | No |  |
| └─ threshold | number |  | No |  |
| └─ type | enum | <br>Possible values: `server_vad` | No |  |
| type | enum | <br>Possible values: `transcription` | Yes |  |

### OpenAI.RealtimeTranscriptionSessionCreateRequestInputAudioNoiseReduction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.NoiseReductionType](#openainoisereductiontype) | Type of noise reduction. `near_field` is for close-talking microphones such as headphones, `far_field` is for far-field microphones such as laptop or conference room microphones. | No |  |

### OpenAI.RealtimeTranscriptionSessionCreateRequestTurnDetection

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prefix_padding_ms | integer |  | No |  |
| silence_duration_ms | integer |  | No |  |
| threshold | number |  | No |  |
| type | enum | <br>Possible values: `server_vad` | No |  |

### OpenAI.RealtimeTranscriptionSessionCreateResponse

A new Realtime transcription session configuration.
When a session is created on the server via REST API, the session object
also contains an ephemeral key. Default TTL for keys is 10 minutes. This
property is not present when a session is updated via the WebSocket API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| client_secret | [OpenAI.RealtimeTranscriptionSessionCreateResponseClientSecret](#openairealtimetranscriptionsessioncreateresponseclientsecret) |  | Yes |  |
| └─ expires_at | integer |  | Yes |  |
| └─ value | string |  | Yes |  |
| input_audio_format | string | The format of input audio. Options are `pcm16`, `g711_ulaw`, or `g711_alaw`. | No |  |
| input_audio_transcription | [OpenAI.AudioTranscription](#openaiaudiotranscription) |  | No |  |
| └─ language | string | The language of the input audio. Supplying the input language in<br>  [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format<br>  will improve accuracy and latency. | No |  |
| └─ model | string | The model to use for transcription. Current options are `whisper-1`, `gpt-4o-mini-transcribe`, `gpt-4o-mini-transcribe-2025-12-15`, `gpt-4o-transcribe`, and `gpt-4o-transcribe-diarize`. Use `gpt-4o-transcribe-diarize` when you need diarization with speaker labels. | No |  |
| └─ prompt | string | An optional text to guide the model's style or continue a previous audio<br>  segment.<br>  For `whisper-1`, the [prompt is a list of keywords](https://platform.openai.com/docs/guides/speech-to-text#prompting).<br>  For `gpt-4o-transcribe` models (excluding `gpt-4o-transcribe-diarize`), the prompt is a free text string, for example "expect words related to technology". | No |  |
| modalities | array of string | The set of modalities the model can respond with. To disable audio,<br>  set this to ["text"]. | No |  |
| turn_detection | [OpenAI.RealtimeTranscriptionSessionCreateResponseTurnDetection](#openairealtimetranscriptionsessioncreateresponseturndetection) |  | No |  |
| └─ prefix_padding_ms | integer |  | No |  |
| └─ silence_duration_ms | integer |  | No |  |
| └─ threshold | number |  | No |  |
| └─ type | string |  | No |  |
| type | enum | <br>Possible values: `transcription` | Yes |  |

### OpenAI.RealtimeTranscriptionSessionCreateResponseClientSecret

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_at | integer |  | Yes |  |
| value | string |  | Yes |  |

### OpenAI.RealtimeTranscriptionSessionCreateResponseTurnDetection

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prefix_padding_ms | integer |  | No |  |
| silence_duration_ms | integer |  | No |  |
| threshold | number |  | No |  |
| type | string |  | No |  |

### OpenAI.RealtimeTruncation

When the number of tokens in a conversation exceeds the model's input token limit, the conversation be truncated, meaning messages (starting from the oldest) will not be included in the model's context. A 32k context model with 4,096 max output tokens can only include 28,224 tokens in the context before truncation occurs.
Clients can configure truncation behavior to truncate with a lower max token limit, which is an effective way to control token usage and cost.
Truncation will reduce the number of cached tokens on the next turn (busting the cache), since messages are dropped from the beginning of the context. However, clients can also configure truncation to retain messages up to a fraction of the maximum context size, which will reduce the need for future truncations and thus improve the cache rate.
Truncation can be disabled entirely, which means the server will never truncate but would instead return an error if the conversation exceeds the model's input token limit.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `auto`<br>`disabled` |

### OpenAI.RealtimeTurnDetection


### Discriminator for OpenAI.RealtimeTurnDetection

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.RealtimeTurnDetectionType](#openairealtimeturndetectiontype) |  | Yes |  |

### OpenAI.RealtimeTurnDetectionType

**Type**: string


### OpenAI.Reasoning

**gpt-5 and o-series models only**
Configuration options for
reasoning models.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | Constrains effort on reasoning for<br>reasoning models.<br>Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response.<br>- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.<br>- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.<br>- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.<br>- `xhigh` is supported for all models after `gpt-5.1-codex-max`. | No |  |
| generate_summary | string or null |  | No |  |
| summary | string or null |  | No |  |

### OpenAI.ReasoningEffort

Constrains effort on reasoning for
reasoning models.
Currently supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`. Reducing
reasoning effort can result in faster responses and fewer tokens used
on reasoning in a response.
- `gpt-5.1` defaults to `none`, which does not perform reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`, `medium`, and `high`. Tool calls are supported for all reasoning values in gpt-5.1.
- All models before `gpt-5.1` default to `medium` reasoning effort, and do not support `none`.
- The `gpt-5-pro` model defaults to (and only supports) `high` reasoning effort.
- `xhigh` is supported for all models after `gpt-5.1-codex-max`.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `none`<br>`minimal`<br>`low`<br>`medium`<br>`high`<br>`xhigh` |

### OpenAI.ReasoningTextContent

Reasoning text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The reasoning text from the model. | Yes |  |
| type | enum | The type of the reasoning text. Always `reasoning_text`.<br>Possible values: `reasoning_text` | Yes |  |

### OpenAI.RefusalContent

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanation from the model. | Yes |  |
| type | enum | The type of the refusal. Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.Response

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean or null |  | No |  |
| completed_at | string or null |  | No |  |
| content_filters | array of [AzureContentFilterForResponsesAPI](#azurecontentfilterforresponsesapi) | The content filter results from RAI. | Yes |  |
| conversation | [OpenAI.ConversationReference](#openaiconversationreference) or null |  | No |  |
| created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| error | [OpenAI.ResponseError](#openairesponseerror) or null |  | Yes |  |
| id | string | Unique identifier for this Response. | Yes |  |
| incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) or null |  | Yes |  |
| instructions | string or array of [OpenAI.InputItem](#openaiinputitem) or null |  | Yes |  |
| max_output_tokens | integer or null |  | No |  |
| max_tool_calls | integer or null |  | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| output_text | string or null |  | No |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| previous_response_id | string or null |  | No |  |
| prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| prompt_cache_retention | string or null |  | No |  |
| reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| temperature | number or null |  | No |  |
| text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| top_logprobs | integer or null |  | No |  |
| top_p | number or null |  | No |  |
| truncation | string or null |  | No |  |
| usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |

### OpenAI.ResponseAudioDeltaEvent

Emitted when there is a partial audio response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | A chunk of Base64 encoded response audio bytes. | Yes |  |
| sequence_number | integer | A sequence number for this chunk of the stream response. | Yes |  |
| type | enum | The type of the event. Always `response.audio.delta`.<br>Possible values: `response.audio.delta` | Yes |  |

### OpenAI.ResponseAudioTranscriptDeltaEvent

Emitted when there is a partial transcript of audio.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The partial transcript of the audio response. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.audio.transcript.delta`.<br>Possible values: `response.audio.transcript.delta` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCodeDeltaEvent

Emitted when a partial code snippet is streamed by the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The partial code snippet being streamed by the code interpreter. | Yes |  |
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code is being streamed. | Yes |  |
| sequence_number | integer | The sequence number of this event, used to order streaming events. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call_code.delta`.<br>Possible values: `response.code_interpreter_call_code.delta` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInProgressEvent

Emitted when a code interpreter call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code interpreter call is in progress. | Yes |  |
| sequence_number | integer | The sequence number of this event, used to order streaming events. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.in_progress`.<br>Possible values: `response.code_interpreter_call.in_progress` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInterpretingEvent

Emitted when the code interpreter is actively interpreting the code snippet.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code interpreter is interpreting code. | Yes |  |
| sequence_number | integer | The sequence number of this event, used to order streaming events. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.interpreting`.<br>Possible values: `response.code_interpreter_call.interpreting` | Yes |  |

### OpenAI.ResponseContentPartAddedEvent

Emitted when a new content part is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that was added. | Yes |  |
| item_id | string | The ID of the output item that the content part was added to. | Yes |  |
| output_index | integer | The index of the output item that the content part was added to. | Yes |  |
| part | [OpenAI.OutputContent](#openaioutputcontent) |  | Yes |  |
| └─ type | [OpenAI.OutputContentType](#openaioutputcontenttype) |  | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.content_part.added`.<br>Possible values: `response.content_part.added` | Yes |  |

### OpenAI.ResponseCreatedEvent

An event that is emitted when a response is created.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ background | boolean or null |  | No |  |
| └─ completed_at | string or null |  | No |  |
| └─ content_filters | array of [AzureContentFilterForResponsesAPI](#azurecontentfilterforresponsesapi) | The content filter results from RAI. | Yes |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) or null |  | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) or null |  | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) or null |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) or null |  | Yes |  |
| └─ max_output_tokens | integer or null |  | No |  |
| └─ max_tool_calls | integer or null |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| └─ model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string or null |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string or null |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | string or null |  | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number or null |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | integer or null |  | No |  |
| └─ top_p | number or null |  | No | 1 |
| └─ truncation | string or null |  | No | disabled |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | integer | The sequence number for this event. | Yes |  |
| type | enum | The type of the event. Always `response.created`.<br>Possible values: `response.created` | Yes |  |

### OpenAI.ResponseCustomToolCallInputDeltaEvent

Event representing a delta (partial update) to the input of a custom tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The incremental input data (delta) for the custom tool call. | Yes |  |
| item_id | string | Unique identifier for the API item associated with this event. | Yes |  |
| output_index | integer | The index of the output this delta applies to. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The event type identifier.<br>Possible values: `response.custom_tool_call_input.delta` | Yes |  |

### OpenAI.ResponseError

An error object returned when the model fails to generate a Response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | [OpenAI.ResponseErrorCode](#openairesponseerrorcode) | The error code for the response. | Yes |  |
| message | string | A human-readable description of the error. | Yes |  |

### OpenAI.ResponseErrorCode

The error code for the response.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `server_error`<br>`rate_limit_exceeded`<br>`invalid_prompt`<br>`vector_store_timeout`<br>`invalid_image`<br>`invalid_image_format`<br>`invalid_base64_image`<br>`invalid_image_url`<br>`image_too_large`<br>`image_too_small`<br>`image_parse_error`<br>`image_content_policy_violation`<br>`invalid_image_mode`<br>`image_file_too_large`<br>`unsupported_image_media_type`<br>`empty_image_file`<br>`failed_to_download_image`<br>`image_file_not_found` |

### OpenAI.ResponseErrorEvent

Emitted when an error occurs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string or null |  | Yes |  |
| message | string | The error message. | Yes |  |
| param | string or null |  | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `error`.<br>Possible values: `error` | Yes |  |

### OpenAI.ResponseFailedEvent

An event that is emitted when a response fails.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ background | boolean or null |  | No |  |
| └─ completed_at | string or null |  | No |  |
| └─ content_filters | array of [AzureContentFilterForResponsesAPI](#azurecontentfilterforresponsesapi) | The content filter results from RAI. | Yes |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) or null |  | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) or null |  | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) or null |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) or null |  | Yes |  |
| └─ max_output_tokens | integer or null |  | No |  |
| └─ max_tool_calls | integer or null |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| └─ model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string or null |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string or null |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | string or null |  | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number or null |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | integer or null |  | No |  |
| └─ top_p | number or null |  | No | 1 |
| └─ truncation | string or null |  | No | disabled |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.failed`.<br>Possible values: `response.failed` | Yes |  |

### OpenAI.ResponseFileSearchCallInProgressEvent

Emitted when a file search call is initiated.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | integer | The index of the output item that the file search call is initiated. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.in_progress`.<br>Possible values: `response.file_search_call.in_progress` | Yes |  |

### OpenAI.ResponseFileSearchCallSearchingEvent

Emitted when a file search is currently searching.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | integer | The index of the output item that the file search call is searching. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.searching`.<br>Possible values: `response.file_search_call.searching` | Yes |  |

### OpenAI.ResponseFormatJsonObject

JSON object response format. An older method of generating JSON responses.
Using `json_schema` is recommended for models that support it. Note that the
model will not generate JSON without a system or user message instructing it
to do so.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `json_object`.<br>Possible values: `json_object` | Yes |  |

### OpenAI.ResponseFormatJsonSchema

JSON Schema response format. Used to generate structured JSON responses.
Learn more about [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| json_schema | [OpenAI.ResponseFormatJsonSchemaJsonSchema](#openairesponseformatjsonschemajsonschema) |  | Yes |  |
| └─ description | string |  | No |  |
| └─ name | string |  | Yes |  |
| └─ schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | No |  |
| └─ strict | boolean or null |  | No |  |
| type | enum | The type of response format being defined. Always `json_schema`.<br>Possible values: `json_schema` | Yes |  |

### OpenAI.ResponseFormatJsonSchemaJsonSchema

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string |  | No |  |
| name | string |  | Yes |  |
| schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | No |  |
| strict | boolean or null |  | No |  |

### OpenAI.ResponseFormatJsonSchemaSchema

The schema for the response format, described as a JSON Schema object.
Learn how to build JSON schemas [here](https://json-schema.org/).

**Type**: object


### OpenAI.ResponseFormatText

Default response format. Used to generate text responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.ResponseFunctionCallArgumentsDeltaEvent

Emitted when there is a partial function-call arguments delta.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The function-call arguments delta that is added. | Yes |  |
| item_id | string | The ID of the output item that the function-call arguments delta is added to. | Yes |  |
| output_index | integer | The index of the output item that the function-call arguments delta is added to. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.function_call_arguments.delta`.<br>Possible values: `response.function_call_arguments.delta` | Yes |  |

### OpenAI.ResponseImageGenCallGeneratingEvent

Emitted when an image generation tool call is actively generating an image (intermediate state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| sequence_number | integer | The sequence number of the image generation item being processed. | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.generating'.<br>Possible values: `response.image_generation_call.generating` | Yes |  |

### OpenAI.ResponseImageGenCallInProgressEvent

Emitted when an image generation tool call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| sequence_number | integer | The sequence number of the image generation item being processed. | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.in_progress'.<br>Possible values: `response.image_generation_call.in_progress` | Yes |  |

### OpenAI.ResponseImageGenCallPartialImageEvent

Emitted when a partial image is available during image generation streaming.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| partial_image_b64 | string | Base64-encoded partial image data, suitable for rendering as an image. | Yes |  |
| partial_image_index | integer | 0-based index for the partial image (backend is 1-based, but this is 0-based for the user). | Yes |  |
| sequence_number | integer | The sequence number of the image generation item being processed. | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.partial_image'.<br>Possible values: `response.image_generation_call.partial_image` | Yes |  |

### OpenAI.ResponseInProgressEvent

Emitted when the response is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ background | boolean or null |  | No |  |
| └─ completed_at | string or null |  | No |  |
| └─ content_filters | array of [AzureContentFilterForResponsesAPI](#azurecontentfilterforresponsesapi) | The content filter results from RAI. | Yes |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) or null |  | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) or null |  | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) or null |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) or null |  | Yes |  |
| └─ max_output_tokens | integer or null |  | No |  |
| └─ max_tool_calls | integer or null |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| └─ model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string or null |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string or null |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | string or null |  | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number or null |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | integer or null |  | No |  |
| └─ top_p | number or null |  | No | 1 |
| └─ truncation | string or null |  | No | disabled |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.in_progress`.<br>Possible values: `response.in_progress` | Yes |  |

### OpenAI.ResponseIncompleteDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reason | enum | <br>Possible values: `max_output_tokens`, `content_filter` | No |  |

### OpenAI.ResponseIncompleteEvent

An event that is emitted when a response finishes as incomplete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ background | boolean or null |  | No |  |
| └─ completed_at | string or null |  | No |  |
| └─ content_filters | array of [AzureContentFilterForResponsesAPI](#azurecontentfilterforresponsesapi) | The content filter results from RAI. | Yes |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) or null |  | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) or null |  | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) or null |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) or null |  | Yes |  |
| └─ max_output_tokens | integer or null |  | No |  |
| └─ max_tool_calls | integer or null |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| └─ model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string or null |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string or null |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | string or null |  | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number or null |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | integer or null |  | No |  |
| └─ top_p | number or null |  | No | 1 |
| └─ truncation | string or null |  | No | disabled |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.incomplete`.<br>Possible values: `response.incomplete` | Yes |  |

### OpenAI.ResponseItemList

A list of Response items.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.ItemResource](#openaiitemresource) | A list of items used to generate this response. | Yes |  |
| first_id | string | The ID of the first item in the list. | Yes |  |
| has_more | boolean | Whether there are more items available. | Yes |  |
| last_id | string | The ID of the last item in the list. | Yes |  |
| object | enum | The type of object returned, must be `list`.<br>Possible values: `list` | Yes |  |

### OpenAI.ResponseLogProb

A logprob is the logarithmic probability that the model assigns to producing
a particular token at a given position in the sequence. Less-negative (higher)
logprob values indicate greater model confidence in that token choice.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logprob | number | The log probability of this token. | Yes |  |
| token | string | A possible text token. | Yes |  |
| top_logprobs | array of [OpenAI.ResponseLogProbTopLogprobs](#openairesponselogprobtoplogprobs) | The log probability of the top 20 most likely tokens. | No |  |

### OpenAI.ResponseLogProbTopLogprobs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logprob | number |  | No |  |
| token | string |  | No |  |

### OpenAI.ResponseMCPCallArgumentsDeltaEvent

Emitted when there is a delta (partial update) to the arguments of an MCP tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | A JSON string containing the partial update to the arguments for the MCP tool call. | Yes |  |
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call_arguments.delta'.<br>Possible values: `response.mcp_call_arguments.delta` | Yes |  |

### OpenAI.ResponseMCPCallFailedEvent

Emitted when an MCP  tool call has failed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that failed. | Yes |  |
| output_index | integer | The index of the output item that failed. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.failed'.<br>Possible values: `response.mcp_call.failed` | Yes |  |

### OpenAI.ResponseMCPCallInProgressEvent

Emitted when an MCP  tool call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.in_progress'.<br>Possible values: `response.mcp_call.in_progress` | Yes |  |

### OpenAI.ResponseMCPListToolsFailedEvent

Emitted when the attempt to list available MCP tools has failed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that failed. | Yes |  |
| output_index | integer | The index of the output item that failed. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_list_tools.failed'.<br>Possible values: `response.mcp_list_tools.failed` | Yes |  |

### OpenAI.ResponseMCPListToolsInProgressEvent

Emitted when the system is in the process of retrieving the list of available MCP tools.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the MCP tool call item that is being processed. | Yes |  |
| output_index | integer | The index of the output item that is being processed. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_list_tools.in_progress'.<br>Possible values: `response.mcp_list_tools.in_progress` | Yes |  |

### OpenAI.ResponseModalities

Output types that you would like the model to generate.
Most models are capable of generating text, which is the default:
`["text"]`
The `gpt-4o-audio-preview` model can also be used to
[generate audio](https://platform.openai.com/docs/guides/audio). To request that this model generate
both text and audio responses, you can use:
`["text", "audio"]`

This schema accepts one of the following types:

- **array**
- **null**

### OpenAI.ResponseOutputItemAddedEvent

Emitted when a new output item is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item | [OpenAI.OutputItem](#openaioutputitem) |  | Yes |  |
| └─ type | [OpenAI.OutputItemType](#openaioutputitemtype) |  | Yes |  |
| output_index | integer | The index of the output item that was added. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.output_item.added`.<br>Possible values: `response.output_item.added` | Yes |  |

### OpenAI.ResponseOutputTextAnnotationAddedEvent

Emitted when an annotation is added to output text content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotation | [OpenAI.Annotation](#openaiannotation) | An annotation that applies to a span of output text. | Yes |  |
| └─ type | [OpenAI.AnnotationType](#openaiannotationtype) |  | Yes |  |
| annotation_index | integer | The index of the annotation within the content part. | Yes |  |
| content_index | integer | The index of the content part within the output item. | Yes |  |
| item_id | string | The unique identifier of the item to which the annotation is being added. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always 'response.output_text.annotation.added'.<br>Possible values: `response.output_text.annotation.added` | Yes |  |

### OpenAI.ResponsePromptVariables

Optional map of values to substitute in for variables in your
prompt. The substitution values can either be strings, or other
Response input types like images or files.

**Type**: object


### OpenAI.ResponseQueuedEvent

Emitted when a response is queued and waiting to be processed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | [OpenAI.Response](#openairesponse) |  | Yes |  |
| └─ background | boolean or null |  | No |  |
| └─ completed_at | string or null |  | No |  |
| └─ content_filters | array of [AzureContentFilterForResponsesAPI](#azurecontentfilterforresponsesapi) | The content filter results from RAI. | Yes |  |
| └─ conversation | [OpenAI.ConversationReference](#openaiconversationreference) or null |  | No |  |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) or null |  | Yes |  |
| └─ id | string | Unique identifier for this Response. | Yes |  |
| └─ incomplete_details | [OpenAI.ResponseIncompleteDetails](#openairesponseincompletedetails) or null |  | Yes |  |
| └─ instructions | string or array of [OpenAI.InputItem](#openaiinputitem) or null |  | Yes |  |
| └─ max_output_tokens | integer or null |  | No |  |
| └─ max_tool_calls | integer or null |  | No |  |
| └─ metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| └─ model | string | Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI<br>  offers a wide range of models with different capabilities, performance<br>  characteristics, and price points. Refer to the [model guide](https://platform.openai.com/docs/models)<br>  to browse and compare available models. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| └─ output | array of [OpenAI.OutputItem](#openaioutputitem) | An array of content items generated by the model.<br>  - The length and order of items in the `output` array is dependent<br>  on the model's response.<br>  - Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| └─ output_text | string or null |  | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| └─ previous_response_id | string or null |  | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables.<br>[Learn more](https://platform.openai.com/docs/guides/text?api-mode=responses#reusable-prompts). | No |  |
| └─ prompt_cache_key | string | Used by OpenAI to cache responses for similar requests to optimize your cache hit rates. Replaces the `user` field. [Learn more](https://platform.openai.com/docs/guides/prompt-caching). | No |  |
| └─ prompt_cache_retention | string or null |  | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) or null |  | No |  |
| └─ safety_identifier | string | A stable identifier used to help detect users of your application that may be violating OpenAI's usage policies.<br>  The IDs should be a string that uniquely identifies each user. We recommend hashing their username or email address, in order to avoid sending us any identifying information. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>  `in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number or null |  | No | 1 |
| └─ text | [OpenAI.ResponseTextParam](#openairesponsetextparam) | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data. Learn more:<br>- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)<br>- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceParam](#openaitoolchoiceparam) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | [OpenAI.ToolsArray](#openaitoolsarray) | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br>We support the following categories of tools:<br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)<br>or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about<br>[built-in tools](https://platform.openai.com/docs/guides/tools).<br>- **MCP Tools**: Integrations with third-party systems via custom MCP servers<br>or predefined connectors such as Google Drive and SharePoint. Learn more about<br>[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>enabling the model to call your own code with strongly typed arguments<br>and outputs. Learn more about<br>[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use<br>custom tools to call your own code. | No |  |
| └─ top_logprobs | integer or null |  | No |  |
| └─ top_p | number or null |  | No | 1 |
| └─ truncation | string or null |  | No | disabled |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string (deprecated) | This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use `prompt_cache_key` instead to maintain caching optimizations.<br>  A stable identifier for your end-users.<br>  Used to boost cache hit rates by better bucketing similar requests and  to help OpenAI detect and prevent abuse. [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers). | No |  |
| sequence_number | integer | The sequence number for this event. | Yes |  |
| type | enum | The type of the event. Always 'response.queued'.<br>Possible values: `response.queued` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartAddedEvent

Emitted when a new reasoning summary part is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the item this summary part is associated with. | Yes |  |
| output_index | integer | The index of the output item this summary part is associated with. | Yes |  |
| part | [OpenAI.ResponseReasoningSummaryPartAddedEventPart](#openairesponsereasoningsummarypartaddedeventpart) |  | Yes |  |
| └─ text | string |  | Yes |  |
| └─ type | enum | <br>Possible values: `summary_text` | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| summary_index | integer | The index of the summary part within the reasoning summary. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_part.added`.<br>Possible values: `response.reasoning_summary_part.added` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartAddedEventPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `summary_text` | Yes |  |

### OpenAI.ResponseReasoningSummaryTextDeltaEvent

Emitted when a delta is added to a reasoning summary text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The text delta that was added to the summary. | Yes |  |
| item_id | string | The ID of the item this summary text delta is associated with. | Yes |  |
| output_index | integer | The index of the output item this summary text delta is associated with. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| summary_index | integer | The index of the summary part within the reasoning summary. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_text.delta`.<br>Possible values: `response.reasoning_summary_text.delta` | Yes |  |

### OpenAI.ResponseReasoningTextDeltaEvent

Emitted when a delta is added to a reasoning text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the reasoning content part this delta is associated with. | Yes |  |
| delta | string | The text delta that was added to the reasoning content. | Yes |  |
| item_id | string | The ID of the item this reasoning text delta is associated with. | Yes |  |
| output_index | integer | The index of the output item this reasoning text delta is associated with. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_text.delta`.<br>Possible values: `response.reasoning_text.delta` | Yes |  |

### OpenAI.ResponseRefusalDeltaEvent

Emitted when there is a partial refusal text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that the refusal text is added to. | Yes |  |
| delta | string | The refusal text that is added. | Yes |  |
| item_id | string | The ID of the output item that the refusal text is added to. | Yes |  |
| output_index | integer | The index of the output item that the refusal text is added to. | Yes |  |
| sequence_number | integer | The sequence number of this event. | Yes |  |
| type | enum | The type of the event. Always `response.refusal.delta`.<br>Possible values: `response.refusal.delta` | Yes |  |

### OpenAI.ResponseStreamOptions

Options for streaming responses. Only set this when you set `stream: true`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_obfuscation | boolean | When true, stream obfuscation will be enabled. Stream obfuscation adds<br>  random characters to an `obfuscation` field on streaming delta events to<br>  normalize payload sizes as a mitigation to certain side-channel attacks.<br>  These obfuscation fields are included by default, but add a small amount<br>  of overhead to the data stream. You can set `include_obfuscation` to<br>  false to optimize for bandwidth if you trust the network links between<br>  your application and the OpenAI API. | No |  |

### OpenAI.ResponseTextDeltaEvent

Emitted when there is an additional text delta.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that the text delta was added to. | Yes |  |
| delta | string | The text delta that was added. | Yes |  |
| item_id | string | The ID of the output item that the text delta was added to. | Yes |  |
| logprobs | array of [OpenAI.ResponseLogProb](#openairesponselogprob) | The log probabilities of the tokens in the delta. | Yes |  |
| output_index | integer | The index of the output item that the text delta was added to. | Yes |  |
| sequence_number | integer | The sequence number for this event. | Yes |  |
| type | enum | The type of the event. Always `response.output_text.delta`.<br>Possible values: `response.output_text.delta` | Yes |  |

### OpenAI.ResponseTextParam

Configuration options for a text response from the model. Can be plain
text or structured JSON data. Learn more:
- [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| format | [OpenAI.TextResponseFormatConfiguration](#openaitextresponseformatconfiguration) | An object specifying the format that the model must output.<br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema. Learn more in the<br><br>The default format is `{ "type": "text" }` with no additional options.<br>*Not recommended for gpt-4o and newer models:<br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | No |  |
| verbosity | [OpenAI.Verbosity](#openaiverbosity) | Constrains the verbosity of the model's response. Lower values will result in<br>more concise responses, while higher values will result in more verbose responses.<br>Currently supported values are `low`, `medium`, and `high`. | No |  |

### OpenAI.ResponseUsage

Represents token usage details including input tokens, output tokens,
a breakdown of output tokens, and the total tokens used.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_tokens | integer | The number of input tokens. | Yes |  |
| input_tokens_details | [OpenAI.ResponseUsageInputTokensDetails](#openairesponseusageinputtokensdetails) |  | Yes |  |
| └─ cached_tokens | integer |  | Yes |  |
| output_tokens | integer | The number of output tokens. | Yes |  |
| output_tokens_details | [OpenAI.ResponseUsageOutputTokensDetails](#openairesponseusageoutputtokensdetails) |  | Yes |  |
| └─ reasoning_tokens | integer |  | Yes |  |
| total_tokens | integer | The total number of tokens used. | Yes |  |

### OpenAI.ResponseUsageInputTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cached_tokens | integer |  | Yes |  |

### OpenAI.ResponseUsageOutputTokensDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reasoning_tokens | integer |  | Yes |  |

### OpenAI.ResponseWebSearchCallInProgressEvent

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | integer | The index of the output item that the web search call is associated with. | Yes |  |
| sequence_number | integer | The sequence number of the web search call being processed. | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.in_progress`.<br>Possible values: `response.web_search_call.in_progress` | Yes |  |

### OpenAI.ResponseWebSearchCallSearchingEvent

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | integer | The index of the output item that the web search call is associated with. | Yes |  |
| sequence_number | integer | The sequence number of the web search call being processed. | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.searching`.<br>Possible values: `response.web_search_call.searching` | Yes |  |

### OpenAI.RunCompletionUsage

Usage statistics related to the run. This value will be `null` if the run is not in a terminal state (i.e. `in_progress`, `queued`, etc.).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_tokens | integer | Number of completion tokens used over the course of the run. | Yes |  |
| prompt_tokens | integer | Number of prompt tokens used over the course of the run. | Yes |  |
| total_tokens | integer | Total number of tokens used (prompt + completion). | Yes |  |

### OpenAI.RunGraderRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderPython](#openaigraderpython) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [OpenAI.GraderMulti](#openaigradermulti) or [GraderEndpoint](#graderendpoint) | The grader used for the fine-tuning job. | Yes |  |
| item | [OpenAI.RunGraderRequestItem](#openairungraderrequestitem) |  | No |  |
| model_sample | string | The model sample to be evaluated. This value will be used to populate<br>  the `sample` namespace. See [the guide](https://platform.openai.com/docs/guides/graders) for more details.<br>  The `output_json` variable will be populated if the model sample is a<br>  valid JSON string. | Yes |  |

### OpenAI.RunGraderRequestItem

**Type**: object


### OpenAI.RunGraderResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.RunGraderResponseMetadata](#openairungraderresponsemetadata) |  | Yes |  |
| model_grader_token_usage_per_model | object |  | Yes |  |
| reward | number |  | Yes |  |
| sub_rewards | object |  | Yes |  |

### OpenAI.RunGraderResponseMetadata

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| errors | [OpenAI.RunGraderResponseMetadataErrors](#openairungraderresponsemetadataerrors) |  | Yes |  |
| execution_time | number |  | Yes |  |
| name | string |  | Yes |  |
| sampled_model_name | string or null |  | Yes |  |
| scores | object |  | Yes |  |
| token_usage | integer or null |  | Yes |  |
| type | string |  | Yes |  |

### OpenAI.RunGraderResponseMetadataErrors

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| formula_parse_error | boolean |  | Yes |  |
| invalid_variable_error | boolean |  | Yes |  |
| model_grader_parse_error | boolean |  | Yes |  |
| model_grader_refusal_error | boolean |  | Yes |  |
| model_grader_server_error | boolean |  | Yes |  |
| model_grader_server_error_details | string or null |  | Yes |  |
| other_error | boolean |  | Yes |  |
| python_grader_runtime_error | boolean |  | Yes |  |
| python_grader_runtime_error_details | string or null |  | Yes |  |
| python_grader_server_error | boolean |  | Yes |  |
| python_grader_server_error_type | string or null |  | Yes |  |
| sample_parse_error | boolean |  | Yes |  |
| truncated_observation_error | boolean |  | Yes |  |
| unresponsive_reward_error | boolean |  | Yes |  |

### OpenAI.RunObject

Represents an execution run on a [thread](https://platform.openai.com/docs/api-reference/threads).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| assistant_id | string | The ID of the [assistant](https://platform.openai.com/docs/api-reference/assistants) used for execution of this run. | Yes |  |
| cancelled_at | string or null | The Unix timestamp (in seconds) for when the run was cancelled. | Yes |  |
| completed_at | string or null | The Unix timestamp (in seconds) for when the run was completed. | Yes |  |
| created_at | integer | The Unix timestamp (in seconds) for when the run was created. | Yes |  |
| expires_at | string or null | The Unix timestamp (in seconds) for when the run will expire. | Yes |  |
| failed_at | string or null | The Unix timestamp (in seconds) for when the run failed. | Yes |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| incomplete_details | [OpenAI.RunObjectIncompleteDetails](#openairunobjectincompletedetails) or null | Details on why the run is incomplete. Will be `null` if the run is not incomplete. | Yes |  |
| instructions | string | The instructions that the [assistant](https://platform.openai.com/docs/api-reference/assistants) used for this run. | Yes |  |
| last_error | [OpenAI.RunObjectLastError](#openairunobjectlasterror) or null | The last error associated with this run. Will be `null` if there are no errors. | Yes |  |
| max_completion_tokens | integer or null | The maximum number of completion tokens specified to have been used over the course of the run. | Yes |  |
| max_prompt_tokens | integer or null | The maximum number of prompt tokens specified to have been used over the course of the run. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | Yes |  |
| model | string | The model that the [assistant](https://platform.openai.com/docs/api-reference/assistants) used for this run. | Yes |  |
| object | enum | The object type, which is always `thread.run`.<br>Possible values: `thread.run` | Yes |  |
| parallel_tool_calls | [OpenAI.ParallelToolCalls](#openaiparalleltoolcalls) | Whether to enable [parallel function calling](https://platform.openai.com/docs/guides/function-calling#configuring-parallel-function-calling) during tool use. | Yes |  |
| required_action | [OpenAI.RunObjectRequiredAction](#openairunobjectrequiredaction) or null | Details on the action required to continue the run. Will be `null` if no action is required. | Yes |  |
| response_format | [OpenAI.AssistantsApiResponseFormatOption](#openaiassistantsapiresponseformatoption) | Specifies the format that the model must output. Compatible with [GPT-4o](https://platform.openai.com/docs/models#gpt-4o), [GPT-4 Turbo](https://platform.openai.com/docs/models#gpt-4-turbo-and-gpt-4), and all GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.<br>Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensure the model will match your supplied JSON schema. Learn more in the <br>Setting to `{ "type": "json_object" }` enables JSON mode, which ensures the message the model generates is valid JSON.<br>*Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length. | Yes |  |
| started_at | string or null | The Unix timestamp (in seconds) for when the run was started. | Yes |  |
| status | [OpenAI.RunStatus](#openairunstatus) | The status of the run, which can be either `queued`, `in_progress`, `requires_action`, `cancelling`, `cancelled`, `failed`, `completed`, `incomplete`, or `expired`. | Yes |  |
| temperature | number or null | The sampling temperature used for this run. If not set, defaults to 1. | No |  |
| thread_id | string | The ID of the [thread](https://platform.openai.com/docs/api-reference/threads) that was executed on as a part of this run. | Yes |  |
| tool_choice | [OpenAI.AssistantsApiToolChoiceOption](#openaiassistantsapitoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tools and instead generates a message.<br>`auto` is the default value and means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools before responding to the user.<br>Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool. | Yes |  |
| tools | array of [OpenAI.AssistantTool](#openaiassistanttool) | The list of tools that the [assistant](https://platform.openai.com/docs/api-reference/assistants) used for this run. | Yes | [] |
| top_p | number or null | The nucleus sampling value used for this run. If not set, defaults to 1. | No |  |
| truncation_strategy | [OpenAI.TruncationObject](#openaitruncationobject) | Controls for how a thread will be truncated prior to the run. Use this to control the initial context window of the run. | Yes |  |
| usage | [OpenAI.RunCompletionUsage](#openairuncompletionusage) or null |  | Yes |  |

### OpenAI.RunObjectIncompleteDetails

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| reason | enum | <br>Possible values: `max_completion_tokens`, `max_prompt_tokens` | No |  |

### OpenAI.RunObjectLastError

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | enum | <br>Possible values: `server_error`, `rate_limit_exceeded`, `invalid_prompt` | Yes |  |
| message | string |  | Yes |  |

### OpenAI.RunObjectRequiredAction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| submit_tool_outputs | [OpenAI.RunObjectRequiredActionSubmitToolOutputs](#openairunobjectrequiredactionsubmittooloutputs) |  | Yes |  |
| type | enum | <br>Possible values: `submit_tool_outputs` | Yes |  |

### OpenAI.RunObjectRequiredActionSubmitToolOutputs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| tool_calls | array of [OpenAI.RunToolCallObject](#openairuntoolcallobject) |  | Yes |  |

### OpenAI.RunStatus

The status of the run, which can be either `queued`, `in_progress`, `requires_action`, `cancelling`, `cancelled`, `failed`, `completed`, `incomplete`, or `expired`.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `queued`<br>`in_progress`<br>`requires_action`<br>`cancelling`<br>`cancelled`<br>`failed`<br>`completed`<br>`incomplete`<br>`expired` |

### OpenAI.RunStepCompletionUsage

Usage statistics related to the run step. This value will be `null` while the run step's status is `in_progress`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_tokens | integer | Number of completion tokens used over the course of the run step. | Yes |  |
| prompt_tokens | integer | Number of prompt tokens used over the course of the run step. | Yes |  |
| total_tokens | integer | Total number of tokens used (prompt + completion). | Yes |  |

### OpenAI.RunStepDetailsMessageCreationObject

Details of the message creation by the run step.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| message_creation | [OpenAI.RunStepDetailsMessageCreationObjectMessageCreation](#openairunstepdetailsmessagecreationobjectmessagecreation) |  | Yes |  |
| type | enum | Always `message_creation`.<br>Possible values: `message_creation` | Yes |  |

### OpenAI.RunStepDetailsMessageCreationObjectMessageCreation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| message_id | string |  | Yes |  |

### OpenAI.RunStepDetailsToolCall


### Discriminator for OpenAI.RunStepDetailsToolCall

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `code_interpreter` | [OpenAI.RunStepDetailsToolCallsCodeObject](#openairunstepdetailstoolcallscodeobject) |
| `file_search` | [OpenAI.RunStepDetailsToolCallsFileSearchObject](#openairunstepdetailstoolcallsfilesearchobject) |
| `function` | [OpenAI.RunStepDetailsToolCallsFunctionObject](#openairunstepdetailstoolcallsfunctionobject) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.RunStepDetailsToolCallType](#openairunstepdetailstoolcalltype) |  | Yes |  |

### OpenAI.RunStepDetailsToolCallType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `code_interpreter`<br>`file_search`<br>`function` |

### OpenAI.RunStepDetailsToolCallsCodeObject

Details of the Code Interpreter tool call the run step was involved in.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter | [OpenAI.RunStepDetailsToolCallsCodeObjectCodeInterpreter](#openairunstepdetailstoolcallscodeobjectcodeinterpreter) |  | Yes |  |
| └─ input | string |  | Yes |  |
| └─ outputs | array of [OpenAI.RunStepDetailsToolCallsCodeOutputLogsObject](#openairunstepdetailstoolcallscodeoutputlogsobject) or [OpenAI.RunStepDetailsToolCallsCodeOutputImageObject](#openairunstepdetailstoolcallscodeoutputimageobject) |  | Yes |  |
| id | string | The ID of the tool call. | Yes |  |
| type | enum | The type of tool call. This is always going to be `code_interpreter` for this type of tool call.<br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.RunStepDetailsToolCallsCodeObjectCodeInterpreter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string |  | Yes |  |
| outputs | array of [OpenAI.RunStepDetailsToolCallsCodeOutputLogsObject](#openairunstepdetailstoolcallscodeoutputlogsobject) or [OpenAI.RunStepDetailsToolCallsCodeOutputImageObject](#openairunstepdetailstoolcallscodeoutputimageobject) |  | Yes |  |

### OpenAI.RunStepDetailsToolCallsCodeOutputImageObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image | [OpenAI.RunStepDetailsToolCallsCodeOutputImageObjectImage](#openairunstepdetailstoolcallscodeoutputimageobjectimage) |  | Yes |  |
| type | enum | Always `image`.<br>Possible values: `image` | Yes |  |

### OpenAI.RunStepDetailsToolCallsCodeOutputImageObjectImage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | Yes |  |

### OpenAI.RunStepDetailsToolCallsCodeOutputLogsObject

Text output from the Code Interpreter tool call as part of a run step.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logs | string | The text output from the Code Interpreter tool call. | Yes |  |
| type | enum | Always `logs`.<br>Possible values: `logs` | Yes |  |

### OpenAI.RunStepDetailsToolCallsFileSearchObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_search | [OpenAI.RunStepDetailsToolCallsFileSearchObjectFileSearch](#openairunstepdetailstoolcallsfilesearchobjectfilesearch) |  | Yes |  |
| └─ ranking_options | [OpenAI.RunStepDetailsToolCallsFileSearchRankingOptionsObject](#openairunstepdetailstoolcallsfilesearchrankingoptionsobject) | The ranking options for the file search. | No |  |
| └─ results | array of [OpenAI.RunStepDetailsToolCallsFileSearchResultObject](#openairunstepdetailstoolcallsfilesearchresultobject) |  | No |  |
| id | string | The ID of the tool call object. | Yes |  |
| type | enum | The type of tool call. This is always going to be `file_search` for this type of tool call.<br>Possible values: `file_search` | Yes |  |

### OpenAI.RunStepDetailsToolCallsFileSearchObjectFileSearch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| ranking_options | [OpenAI.RunStepDetailsToolCallsFileSearchRankingOptionsObject](#openairunstepdetailstoolcallsfilesearchrankingoptionsobject) | The ranking options for the file search. | No |  |
| results | array of [OpenAI.RunStepDetailsToolCallsFileSearchResultObject](#openairunstepdetailstoolcallsfilesearchresultobject) |  | No |  |

### OpenAI.RunStepDetailsToolCallsFileSearchRankingOptionsObject

The ranking options for the file search.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| ranker | [OpenAI.FileSearchRanker](#openaifilesearchranker) | The ranker to use for the file search. If not specified will use the `auto` ranker. | Yes |  |
| score_threshold | number | The score threshold for the file search. All values must be a floating point number between 0 and 1.<br>**Constraints:** min: 0, max: 1 | Yes |  |

### OpenAI.RunStepDetailsToolCallsFileSearchResultObject

A result instance of the file search.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array of [OpenAI.RunStepDetailsToolCallsFileSearchResultObjectContent](#openairunstepdetailstoolcallsfilesearchresultobjectcontent) | The content of the result that was found. The content is only included if requested via the include query parameter. | No |  |
| file_id | string | The ID of the file that result was found in. | Yes |  |
| file_name | string | The name of the file that result was found in. | Yes |  |
| score | number | The score of the result. All values must be a floating point number between 0 and 1.<br>**Constraints:** min: 0, max: 1 | Yes |  |

### OpenAI.RunStepDetailsToolCallsFileSearchResultObjectContent

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | No |  |
| type | enum | <br>Possible values: `text` | No |  |

### OpenAI.RunStepDetailsToolCallsFunctionObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.RunStepDetailsToolCallsFunctionObjectFunction](#openairunstepdetailstoolcallsfunctionobjectfunction) |  | Yes |  |
| └─ arguments | string |  | Yes |  |
| └─ name | string |  | Yes |  |
| └─ output | string or null |  | Yes |  |
| id | string | The ID of the tool call object. | Yes |  |
| type | enum | The type of tool call. This is always going to be `function` for this type of tool call.<br>Possible values: `function` | Yes |  |

### OpenAI.RunStepDetailsToolCallsFunctionObjectFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string |  | Yes |  |
| name | string |  | Yes |  |
| output | string or null |  | Yes |  |

### OpenAI.RunStepDetailsToolCallsObject

Details of the tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| tool_calls | array of [OpenAI.RunStepDetailsToolCall](#openairunstepdetailstoolcall) | An array of tool calls the run step was involved in. These can be associated with one of three types of tools: `code_interpreter`, `file_search`, or `function`. | Yes |  |
| type | enum | Always `tool_calls`.<br>Possible values: `tool_calls` | Yes |  |

### OpenAI.RunStepObject

Represents a step in execution of a run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| assistant_id | string | The ID of the [assistant](https://platform.openai.com/docs/api-reference/assistants) associated with the run step. | Yes |  |
| cancelled_at | string or null |  | Yes |  |
| completed_at | string or null |  | Yes |  |
| created_at | integer | The Unix timestamp (in seconds) for when the run step was created. | Yes |  |
| expired_at | string or null |  | Yes |  |
| failed_at | string or null |  | Yes |  |
| id | string | The identifier of the run step, which can be referenced in API endpoints. | Yes |  |
| last_error | [OpenAI.RunStepObjectLastError](#openairunstepobjectlasterror) or null |  | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | Yes |  |
| object | enum | The object type, which is always `thread.run.step`.<br>Possible values: `thread.run.step` | Yes |  |
| run_id | string | The ID of the [run](https://platform.openai.com/docs/api-reference/runs) that this run step is a part of. | Yes |  |
| status | enum | The status of the run step, which can be either `in_progress`, `cancelled`, `failed`, `completed`, or `expired`.<br>Possible values: `in_progress`, `cancelled`, `failed`, `completed`, `expired` | Yes |  |
| step_details | [OpenAI.RunStepDetailsMessageCreationObject](#openairunstepdetailsmessagecreationobject) or [OpenAI.RunStepDetailsToolCallsObject](#openairunstepdetailstoolcallsobject) | The details of the run step. | Yes |  |
| thread_id | string | The ID of the [thread](https://platform.openai.com/docs/api-reference/threads) that was run. | Yes |  |
| type | enum | The type of run step, which can be either `message_creation` or `tool_calls`.<br>Possible values: `message_creation`, `tool_calls` | Yes |  |
| usage | [OpenAI.RunStepCompletionUsage](#openairunstepcompletionusage) | Usage statistics related to the run step. This value will be `null` while the run step's status is `in_progress`. | Yes |  |

### OpenAI.RunStepObjectLastError

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | enum | <br>Possible values: `server_error`, `rate_limit_exceeded` | Yes |  |
| message | string |  | Yes |  |

### OpenAI.RunToolCallObject

Tool call objects

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | [OpenAI.RunToolCallObjectFunction](#openairuntoolcallobjectfunction) |  | Yes |  |
| └─ arguments | string |  | Yes |  |
| └─ name | string |  | Yes |  |
| id | string | The ID of the tool call. This ID must be referenced when you submit the tool outputs in using the [Submit tool outputs to run](https://platform.openai.com/docs/api-reference/runs/submitToolOutputs) endpoint. | Yes |  |
| type | enum | The type of tool call the output is required for. For now, this is always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.RunToolCallObjectFunction

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string |  | Yes |  |
| name | string |  | Yes |  |

### OpenAI.Screenshot

A screenshot action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a screenshot action, this property is<br>  always set to `screenshot`.<br>Possible values: `screenshot` | Yes |  |

### OpenAI.Scroll

A scroll action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| scroll_x | integer | The horizontal scroll distance. | Yes |  |
| scroll_y | integer | The vertical scroll distance. | Yes |  |
| type | enum | Specifies the event type. For a scroll action, this property is<br>  always set to `scroll`.<br>Possible values: `scroll` | Yes |  |
| x | integer | The x-coordinate where the scroll occurred. | Yes |  |
| y | integer | The y-coordinate where the scroll occurred. | Yes |  |

### OpenAI.SearchContextSize

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `low`<br>`medium`<br>`high` |

### OpenAI.SpecificApplyPatchParam

Forces the model to call the apply_patch tool when executing a tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The tool to call. Always `apply_patch`.<br>Possible values: `apply_patch` | Yes |  |

### OpenAI.SpecificFunctionShellParam

Forces the model to call the shell tool when a tool call is required.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The tool to call. Always `shell`.<br>Possible values: `shell` | Yes |  |

### OpenAI.StaticChunkingStrategy

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunk_overlap_tokens | integer | The number of tokens that overlap between chunks. The default value is `400`.<br>  Note that the overlap must not exceed half of `max_chunk_size_tokens`. | Yes |  |
| max_chunk_size_tokens | integer | The maximum number of tokens in each chunk. The default value is `800`. The minimum value is `100` and the maximum value is `4096`.<br>**Constraints:** min: 100, max: 4096 | Yes |  |

### OpenAI.StaticChunkingStrategyRequestParam

Customize your own chunking strategy by setting chunk size and chunk overlap.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| static | [OpenAI.StaticChunkingStrategy](#openaistaticchunkingstrategy) |  | Yes |  |
| type | enum | Always `static`.<br>Possible values: `static` | Yes |  |

### OpenAI.StaticChunkingStrategyResponseParam

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| static | [OpenAI.StaticChunkingStrategy](#openaistaticchunkingstrategy) |  | Yes |  |
| type | enum | Always `static`.<br>Possible values: `static` | Yes |  |

### OpenAI.StopConfiguration

Not supported with latest reasoning models `o3` and `o4-mini`.
Up to four sequences where the API will stop generating further tokens. The
returned text will not contain the stop sequence.

This schema accepts one of the following types:

- **array**
- **null**

### OpenAI.SubmitToolOutputsRunRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| stream | boolean or null |  | No |  |
| tool_outputs | array of [OpenAI.SubmitToolOutputsRunRequestToolOutputs](#openaisubmittooloutputsrunrequesttooloutputs) | A list of tools for which the outputs are being submitted. | Yes |  |

### OpenAI.SubmitToolOutputsRunRequestToolOutputs

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| output | string |  | No |  |
| tool_call_id | string |  | No |  |

### OpenAI.Summary

A summary text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | A summary of the reasoning output from the model so far. | Yes |  |
| type | enum | The type of the object. Always `summary_text`.<br>Possible values: `summary_text` | Yes |  |

### OpenAI.SummaryTextContent

A summary text from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | A summary of the reasoning output from the model so far. | Yes |  |
| type | enum | The type of the object. Always `summary_text`.<br>Possible values: `summary_text` | Yes |  |

### OpenAI.TextAnnotation


### Discriminator for OpenAI.TextAnnotation

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `file_citation` | [OpenAI.MessageContentTextAnnotationsFileCitationObject](#openaimessagecontenttextannotationsfilecitationobject) |
| `file_path` | [OpenAI.MessageContentTextAnnotationsFilePathObject](#openaimessagecontenttextannotationsfilepathobject) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.TextAnnotationType](#openaitextannotationtype) |  | Yes |  |

### OpenAI.TextAnnotationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `file_citation`<br>`file_path` |

### OpenAI.TextContent

A text content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `text` | Yes |  |

### OpenAI.TextResponseFormatConfiguration

An object specifying the format that the model must output.
Configuring `{ "type": "json_schema" }` enables Structured Outputs,
which ensures the model will match your supplied JSON schema. Learn more in the

The default format is `{ "type": "text" }` with no additional options.
*Not recommended for gpt-4o and newer models:**
Setting to `{ "type": "json_object" }` enables the older JSON mode, which
ensures the message the model generates is valid JSON. Using `json_schema`
is preferred for models that support it.


### Discriminator for OpenAI.TextResponseFormatConfiguration

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `json_schema` | [OpenAI.TextResponseFormatJsonSchema](#openaitextresponseformatjsonschema) |
| `text` | [OpenAI.TextResponseFormatConfigurationResponseFormatText](#openaitextresponseformatconfigurationresponseformattext) |
| `json_object` | [OpenAI.TextResponseFormatConfigurationResponseFormatJsonObject](#openaitextresponseformatconfigurationresponseformatjsonobject) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.TextResponseFormatConfigurationType](#openaitextresponseformatconfigurationtype) |  | Yes |  |

### OpenAI.TextResponseFormatConfigurationResponseFormatJsonObject

JSON object response format. An older method of generating JSON responses.
Using `json_schema` is recommended for models that support it. Note that the
model will not generate JSON without a system or user message instructing it
to do so.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `json_object`.<br>Possible values: `json_object` | Yes |  |

### OpenAI.TextResponseFormatConfigurationResponseFormatText

Default response format. Used to generate text responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of response format being defined. Always `text`.<br>Possible values: `text` | Yes |  |

### OpenAI.TextResponseFormatConfigurationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`json_schema`<br>`json_object` |

### OpenAI.TextResponseFormatJsonSchema

JSON Schema response format. Used to generate structured JSON responses.
Learn more about [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the response format is for, used by the model to<br>  determine how to respond in the format. | No |  |
| name | string | The name of the response format. Must be a-z, A-Z, 0-9, or contain<br>  underscores and dashes, with a maximum length of 64. | Yes |  |
| schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | Yes |  |
| strict | boolean or null |  | No |  |
| type | enum | The type of response format being defined. Always `json_schema`.<br>Possible values: `json_schema` | Yes |  |

### OpenAI.ThreadObject

Represents a thread that contains [messages](https://platform.openai.com/docs/api-reference/messages).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the thread was created. | Yes |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | Yes |  |
| object | enum | The object type, which is always `thread`.<br>Possible values: `thread` | Yes |  |
| tool_resources | [OpenAI.ThreadObjectToolResources](#openaithreadobjecttoolresources) or null |  | Yes |  |

### OpenAI.ThreadObjectToolResources

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter | [OpenAI.ThreadObjectToolResourcesCodeInterpreter](#openaithreadobjecttoolresourcescodeinterpreter) |  | No |  |
| file_search | [OpenAI.ThreadObjectToolResourcesFileSearch](#openaithreadobjecttoolresourcesfilesearch) |  | No |  |

### OpenAI.ThreadObjectToolResourcesCodeInterpreter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_ids | array of string |  | No |  |

### OpenAI.ThreadObjectToolResourcesFileSearch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| vector_store_ids | array of string |  | No |  |

### OpenAI.TokenLimits

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| post_instructions | integer | **Constraints:** min: 0 | No |  |

### OpenAI.Tool

A tool that can be used to generate a response.


### Discriminator for OpenAI.Tool

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `code_interpreter` | [OpenAI.CodeInterpreterTool](#openaicodeinterpretertool) |
| `function` | [OpenAI.FunctionTool](#openaifunctiontool) |
| `file_search` | [OpenAI.FileSearchTool](#openaifilesearchtool) |
| `computer_use_preview` | [OpenAI.ComputerUsePreviewTool](#openaicomputerusepreviewtool) |
| `web_search` | [OpenAI.WebSearchTool](#openaiwebsearchtool) |
| `mcp` | [OpenAI.MCPTool](#openaimcptool) |
| `image_generation` | [OpenAI.ImageGenTool](#openaiimagegentool) |
| `local_shell` | [OpenAI.LocalShellToolParam](#openailocalshelltoolparam) |
| `shell` | [OpenAI.FunctionShellToolParam](#openaifunctionshelltoolparam) |
| `custom` | [OpenAI.CustomToolParam](#openaicustomtoolparam) |
| `web_search_preview` | [OpenAI.WebSearchPreviewTool](#openaiwebsearchpreviewtool) |
| `apply_patch` | [OpenAI.ApplyPatchToolParam](#openaiapplypatchtoolparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ToolType](#openaitooltype) |  | Yes |  |

### OpenAI.ToolChoiceAllowed

Constrains the tools available to the model to a predefined set.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| mode | enum | Constrains the tools available to the model to a predefined set.<br>  `auto` allows the model to pick from among the allowed tools and generate a<br>  message.<br>  `required` requires the model to call one or more of the allowed tools.<br>Possible values: `auto`, `required` | Yes |  |
| tools | array of object | A list of tool definitions that the model should be allowed to call.<br>  For the Responses API, the list of tool definitions might look like:<br>  ```json<br>  [<br>    { "type": "function", "name": "get_weather" },<br>    { "type": "mcp", "server_label": "deepwiki" },<br>    { "type": "image_generation" }<br>  ]<br>  ``` | Yes |  |
| type | enum | Allowed tool configuration type. Always `allowed_tools`.<br>Possible values: `allowed_tools` | Yes |  |

### OpenAI.ToolChoiceCodeInterpreter

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.ToolChoiceComputerUsePreview

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `computer_use_preview` | Yes |  |

### OpenAI.ToolChoiceCustom

Use this option to force the model to call a specific custom tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the custom tool to call. | Yes |  |
| type | enum | For custom tool calling, the type is always `custom`.<br>Possible values: `custom` | Yes |  |

### OpenAI.ToolChoiceFileSearch

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `file_search` | Yes |  |

### OpenAI.ToolChoiceFunction

Use this option to force the model to call a specific function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the function to call. | Yes |  |
| type | enum | For function calling, the type is always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.ToolChoiceImageGeneration

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `image_generation` | Yes |  |

### OpenAI.ToolChoiceMCP

Use this option to force the model to call a specific tool on a remote MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string or null |  | No |  |
| server_label | string | The label of the MCP server to use. | Yes |  |
| type | enum | For MCP tools, the type is always `mcp`.<br>Possible values: `mcp` | Yes |  |

### OpenAI.ToolChoiceOptions

Controls which (if any) tool is called by the model.
`none` means the model will not call any tool and instead generates a message.
`auto` means the model can pick between generating a message or calling one or
more tools.
`required` means the model must call one or more tools.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `none`<br>`auto`<br>`required` |

### OpenAI.ToolChoiceParam

How the model should select which tool (or tools) to use when generating
a response. See the `tools` parameter to see how to specify which tools
the model can call.


### Discriminator for OpenAI.ToolChoiceParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `allowed_tools` | [OpenAI.ToolChoiceAllowed](#openaitoolchoiceallowed) |
| `mcp` | [OpenAI.ToolChoiceMCP](#openaitoolchoicemcp) |
| `custom` | [OpenAI.ToolChoiceCustom](#openaitoolchoicecustom) |
| `apply_patch` | [OpenAI.SpecificApplyPatchParam](#openaispecificapplypatchparam) |
| `shell` | [OpenAI.SpecificFunctionShellParam](#openaispecificfunctionshellparam) |
| `file_search` | [OpenAI.ToolChoiceFileSearch](#openaitoolchoicefilesearch) |
| `web_search_preview` | [OpenAI.ToolChoiceWebSearchPreview](#openaitoolchoicewebsearchpreview) |
| `computer_use_preview` | [OpenAI.ToolChoiceComputerUsePreview](#openaitoolchoicecomputerusepreview) |
| `web_search_preview_2025_03_11` | [OpenAI.ToolChoiceWebSearchPreview20250311](#openaitoolchoicewebsearchpreview20250311) |
| `image_generation` | [OpenAI.ToolChoiceImageGeneration](#openaitoolchoiceimagegeneration) |
| `code_interpreter` | [OpenAI.ToolChoiceCodeInterpreter](#openaitoolchoicecodeinterpreter) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ToolChoiceParamType](#openaitoolchoiceparamtype) |  | Yes |  |

### OpenAI.ToolChoiceParamType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `allowed_tools`<br>`function`<br>`mcp`<br>`custom`<br>`apply_patch`<br>`shell`<br>`file_search`<br>`web_search_preview`<br>`computer_use_preview`<br>`web_search_preview_2025_03_11`<br>`image_generation`<br>`code_interpreter` |

### OpenAI.ToolChoiceWebSearchPreview

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `web_search_preview` | Yes |  |

### OpenAI.ToolChoiceWebSearchPreview20250311

Indicates that the model should use a built-in tool to generate a response.
[Learn more about built-in tools](https://platform.openai.com/docs/guides/tools).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `web_search_preview_2025_03_11` | Yes |  |

### OpenAI.ToolType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `function`<br>`file_search`<br>`computer_use_preview`<br>`web_search`<br>`mcp`<br>`code_interpreter`<br>`image_generation`<br>`local_shell`<br>`shell`<br>`custom`<br>`web_search_preview`<br>`apply_patch` |

### OpenAI.ToolsArray

An array of tools the model may call while generating a response. You
can specify which tool to use by setting the `tool_choice` parameter.
We support the following categories of tools:
- **Built-in tools**: Tools that are provided by OpenAI that extend the
model's capabilities, like [web search](https://platform.openai.com/docs/guides/tools-web-search)
or [file search](https://platform.openai.com/docs/guides/tools-file-search). Learn more about
[built-in tools](https://platform.openai.com/docs/guides/tools).
- **MCP Tools**: Integrations with third-party systems via custom MCP servers
or predefined connectors such as Google Drive and SharePoint. Learn more about
[MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).
- **Function calls (custom tools)**: Functions that are defined by you,
enabling the model to call your own code with strongly typed arguments
and outputs. Learn more about
[function calling](https://platform.openai.com/docs/guides/function-calling). You can also use
custom tools to call your own code.

**Array of**: [OpenAI.Tool](#openaitool)


### OpenAI.TopLogProb

The top log probability of a token.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array of integer |  | Yes |  |
| logprob | number |  | Yes |  |
| token | string |  | Yes |  |

### OpenAI.TranscriptionSegment

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| avg_logprob | number | Average logprob of the segment. If the value is lower than -1, consider the logprobs failed. | Yes |  |
| compression_ratio | number | Compression ratio of the segment. If the value is greater than 2.4, consider the compression failed. | Yes |  |
| end | number | End time of the segment in seconds. | Yes |  |
| id | integer | Unique identifier of the segment. | Yes |  |
| no_speech_prob | number | Probability of no speech in the segment. If the value is higher than 1.0 and the `avg_logprob` is below -1, consider this segment silent. | Yes |  |
| seek | integer | Seek offset of the segment. | Yes |  |
| start | number | Start time of the segment in seconds. | Yes |  |
| temperature | number | Temperature parameter used for generating the segment. | Yes |  |
| text | string | Text content of the segment. | Yes |  |
| tokens | array of integer | Array of token IDs for the text content. | Yes |  |

### OpenAI.TranscriptionWord

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end | number | End time of the word in seconds. | Yes |  |
| start | number | Start time of the word in seconds. | Yes |  |
| word | string | The text content of the word. | Yes |  |

### OpenAI.TruncationObject

Controls for how a thread will be truncated prior to the run. Use this to control the initial context window of the run.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| last_messages | integer or null |  | No |  |
| type | enum | The truncation strategy to use for the thread. The default is `auto`. If set to `last_messages`, the thread will be truncated to the n most recent messages in the thread. When set to `auto`, messages in the middle of the thread will be dropped to fit the context length of the model, `max_prompt_tokens`.<br>Possible values: `auto`, `last_messages` | Yes |  |

### OpenAI.Type

An action to type in text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text to type. | Yes |  |
| type | enum | Specifies the event type. For a type action, this property is<br>  always set to `type`.<br>Possible values: `type` | Yes |  |

### OpenAI.UpdateConversationBody

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| metadata | [OpenAI.Metadata](#openaimetadata) or null | Set of 16 key-value pairs that can be attached to an object. This can be         useful for storing additional information about the object in a structured         format, and querying for objects via API or the dashboard.<br>  Keys are strings with a maximum length of 64 characters. Values are strings         with a maximum length of 512 characters. | Yes |  |

### OpenAI.UpdateVectorStoreFileAttributesRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | Yes |  |

### OpenAI.UpdateVectorStoreRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | No |  |
| name | string or null | The name of the vector store. | No |  |

### OpenAI.UrlCitationBody

A citation for a web resource used to generate a model response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end_index | integer | The index of the last character of the URL citation in the message. | Yes |  |
| start_index | integer | The index of the first character of the URL citation in the message. | Yes |  |
| title | string | The title of the web resource. | Yes |  |
| type | enum | The type of the URL citation. Always `url_citation`.<br>Possible values: `url_citation` | Yes |  |
| url | string | The URL of the web resource. | Yes |  |

### OpenAI.ValidateGraderResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| grader | [OpenAI.GraderStringCheck](#openaigraderstringcheck) or [OpenAI.GraderTextSimilarity](#openaigradertextsimilarity) or [OpenAI.GraderPython](#openaigraderpython) or [OpenAI.GraderScoreModel](#openaigraderscoremodel) or [OpenAI.GraderMulti](#openaigradermulti) or [GraderEndpoint](#graderendpoint) | The grader used for the fine-tuning job. | No |  |

### OpenAI.VectorStoreExpirationAfter

The expiration policy for a vector store.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| anchor | enum | Anchor timestamp after which the expiration policy applies. Supported anchors: `last_active_at`.<br>Possible values: `last_active_at` | Yes |  |
| days | integer | The number of days after the anchor time that the vector store will expire.<br>**Constraints:** min: 1, max: 365 | Yes |  |

### OpenAI.VectorStoreFileAttributes

Set of 16 key-value pairs that can be attached to an object. This can be
useful for storing additional information about the object in a structured
format, and querying for objects via API or the dashboard. Keys are strings
with a maximum length of 64 characters. Values are strings with a maximum
length of 512 characters, booleans, or numbers.

**Type**: object


### OpenAI.VectorStoreFileBatchObject

A batch of files attached to a vector store.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the vector store files batch was created. | Yes |  |
| file_counts | [OpenAI.VectorStoreFileBatchObjectFileCounts](#openaivectorstorefilebatchobjectfilecounts) |  | Yes |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| object | enum | The object type, which is always `vector_store.file_batch`.<br>Possible values: `vector_store.files_batch` | Yes |  |
| status | enum | The status of the vector store files batch, which can be either `in_progress`, `completed`, `cancelled` or `failed`.<br>Possible values: `in_progress`, `completed`, `cancelled`, `failed` | Yes |  |
| vector_store_id | string | The ID of the [vector store](https://platform.openai.com/docs/api-reference/vector-stores/object) that the [File](https://platform.openai.com/docs/api-reference/files) is attached to. | Yes |  |

### OpenAI.VectorStoreFileBatchObjectFileCounts

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cancelled | integer |  | Yes |  |
| completed | integer |  | Yes |  |
| failed | integer |  | Yes |  |
| in_progress | integer |  | Yes |  |
| total | integer |  | Yes |  |

### OpenAI.VectorStoreFileObject

A list of files attached to a vector store.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyResponse](#openaichunkingstrategyresponse) | The strategy used to chunk the file. | No |  |
| created_at | integer | The Unix timestamp (in seconds) for when the vector store file was created. | Yes |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| last_error | [OpenAI.VectorStoreFileObjectLastError](#openaivectorstorefileobjectlasterror) or null |  | Yes |  |
| object | enum | The object type, which is always `vector_store.file`.<br>Possible values: `vector_store.file` | Yes |  |
| status | enum | The status of the vector store file, which can be either `in_progress`, `completed`, `cancelled`, or `failed`. The status `completed` indicates that the vector store file is ready for use.<br>Possible values: `in_progress`, `completed`, `cancelled`, `failed` | Yes |  |
| usage_bytes | integer | The total vector store usage in bytes. Note that this may be different from the original file size. | Yes |  |
| vector_store_id | string | The ID of the [vector store](https://platform.openai.com/docs/api-reference/vector-stores/object) that the [File](https://platform.openai.com/docs/api-reference/files) is attached to. | Yes |  |

### OpenAI.VectorStoreFileObjectLastError

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | enum | <br>Possible values: `server_error`, `unsupported_file`, `invalid_file` | Yes |  |
| message | string |  | Yes |  |

### OpenAI.VectorStoreObject

A vector store is a collection of processed files can be used by the `file_search` tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the vector store was created. | Yes |  |
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| expires_at | string or null |  | No |  |
| file_counts | [OpenAI.VectorStoreObjectFileCounts](#openaivectorstoreobjectfilecounts) |  | Yes |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| last_active_at | string or null |  | Yes |  |
| metadata | [OpenAI.Metadata](#openaimetadata) or null |  | Yes |  |
| name | string | The name of the vector store. | Yes |  |
| object | enum | The object type, which is always `vector_store`.<br>Possible values: `vector_store` | Yes |  |
| status | enum | The status of the vector store, which can be either `expired`, `in_progress`, or `completed`. A status of `completed` indicates that the vector store is ready for use.<br>Possible values: `expired`, `in_progress`, `completed` | Yes |  |
| usage_bytes | integer | The total number of bytes used by the files in the vector store. | Yes |  |

### OpenAI.VectorStoreObjectFileCounts

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| cancelled | integer |  | Yes |  |
| completed | integer |  | Yes |  |
| failed | integer |  | Yes |  |
| in_progress | integer |  | Yes |  |
| total | integer |  | Yes |  |

### OpenAI.VectorStoreSearchRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | [OpenAI.ComparisonFilter](#openaicomparisonfilter) or [OpenAI.CompoundFilter](#openaicompoundfilter) | A filter to apply based on file attributes. | No |  |
| max_num_results | integer | The maximum number of results to return. This number should be between 1 and 50 inclusive.<br>**Constraints:** min: 1, max: 50 | No | 10 |
| query | string or array of string | A query string for a search | Yes |  |
| ranking_options | [OpenAI.VectorStoreSearchRequestRankingOptions](#openaivectorstoresearchrequestrankingoptions) |  | No |  |
| └─ ranker | enum | <br>Possible values: `none`, `auto`, `default-2024-11-15` | No |  |
| └─ score_threshold | number | **Constraints:** min: 0, max: 1 | No |  |
| rewrite_query | boolean | Whether to rewrite the natural language query for vector search. | No |  |

### OpenAI.VectorStoreSearchRequestRankingOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| ranker | enum | <br>Possible values: `none`, `auto`, `default-2024-11-15` | No |  |
| score_threshold | number | **Constraints:** min: 0, max: 1 | No |  |

### OpenAI.VectorStoreSearchResultContentObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text content returned from search. | Yes |  |
| type | enum | The type of content.<br>Possible values: `text` | Yes |  |

### OpenAI.VectorStoreSearchResultItem

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | [OpenAI.VectorStoreFileAttributes](#openaivectorstorefileattributes) or null |  | Yes |  |
| content | array of [OpenAI.VectorStoreSearchResultContentObject](#openaivectorstoresearchresultcontentobject) | Content chunks from the file. | Yes |  |
| file_id | string | The ID of the vector store file. | Yes |  |
| filename | string | The name of the vector store file. | Yes |  |
| score | number | The similarity score for the result.<br>**Constraints:** min: 0, max: 1 | Yes |  |

### OpenAI.VectorStoreSearchResultsPage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [OpenAI.VectorStoreSearchResultItem](#openaivectorstoresearchresultitem) | The list of search result items. | Yes |  |
| has_more | boolean | Indicates if there are more results to fetch. | Yes |  |
| next_page | string or null |  | Yes |  |
| object | enum | The object type, which is always `vector_store.search_results.page`<br>Possible values: `vector_store.search_results.page` | Yes |  |
| search_query | array of string |  | Yes |  |

### OpenAI.Verbosity

Constrains the verbosity of the model's response. Lower values will result in
more concise responses, while higher values will result in more verbose responses.
Currently supported values are `low`, `medium`, and `high`.

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `low`<br>`medium`<br>`high` |

### OpenAI.VoiceIdsShared

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `alloy`<br>`ash`<br>`ballad`<br>`coral`<br>`echo`<br>`sage`<br>`shimmer`<br>`verse`<br>`marin`<br>`cedar` |

### OpenAI.Wait

A wait action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a wait action, this property is<br>  always set to `wait`.<br>Possible values: `wait` | Yes |  |

### OpenAI.WebSearchActionFind

Action type "find": Searches for a pattern within a loaded page.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| pattern | string | The pattern or text to search for within the page. | Yes |  |
| type | enum | The action type.<br>Possible values: `find_in_page` | Yes |  |
| url | string | The URL of the page searched for the pattern. | Yes |  |

### OpenAI.WebSearchActionOpenPage

Action type "open_page" - Opens a specific URL from search results.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The action type.<br>Possible values: `open_page` | Yes |  |
| url | string | The URL opened by the model. | Yes |  |

### OpenAI.WebSearchActionSearch

Action type "search" - Performs a web search query.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| queries | array of string | The search queries. | No |  |
| query | string (deprecated) | [DEPRECATED] The search query. | Yes |  |
| sources | array of [OpenAI.WebSearchActionSearchSources](#openaiwebsearchactionsearchsources) | The sources used in the search. | No |  |
| type | enum | The action type.<br>Possible values: `search` | Yes |  |

### OpenAI.WebSearchActionSearchSources

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `url` | Yes |  |
| url | string |  | Yes |  |

### OpenAI.WebSearchApproximateLocation

The approximate location of the user.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| city | string or null |  | No |  |
| country | string or null |  | No |  |
| region | string or null |  | No |  |
| timezone | string or null |  | No |  |
| type | enum | The type of location approximation. Always `approximate`.<br>Possible values: `approximate` | No |  |

### OpenAI.WebSearchPreviewTool

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| search_context_size | [OpenAI.SearchContextSize](#openaisearchcontextsize) |  | No |  |
| type | enum | The type of the web search tool. One of `web_search_preview` or `web_search_preview_2025_03_11`.<br>Possible values: `web_search_preview` | Yes |  |
| user_location | [OpenAI.ApproximateLocation](#openaiapproximatelocation) or null |  | No |  |

### OpenAI.WebSearchTool

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | [OpenAI.WebSearchToolFilters](#openaiwebsearchtoolfilters) or null |  | No |  |
| search_context_size | enum | High level guidance for the amount of context window space to use for the search. One of `low`, `medium`, or `high`. `medium` is the default.<br>Possible values: `low`, `medium`, `high` | No |  |
| type | enum | The type of the web search tool. One of `web_search` or `web_search_2025_08_26`.<br>Possible values: `web_search` | Yes |  |
| user_location | [OpenAI.WebSearchApproximateLocation](#openaiwebsearchapproximatelocation) or null |  | No |  |

### OpenAI.WebSearchToolFilters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| allowed_domains | array of string or null |  | No |  |

### Order

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `asc`<br>`desc` |

### ResponseFormatJSONSchemaRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| json_schema | object | JSON Schema for the response format | Yes |  |
| type | enum | Type of response format<br>Possible values: `json_schema` | Yes |  |

### SpeechGenerationResponse

A representation of a response for a text-to-speech operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | string | The generated audio, generated in the requested audio output format. | Yes |  |

### SpeechGenerationResponseFormat

The supported audio output formats for text-to-speech.

This component can be one of the following:

- **string**
- **string**: `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm`

### SpeechVoice

The available voices for text-to-speech.

| Property | Value |
|----------|-------|
| **Description** | The available voices for text-to-speech. |
| **Type** | string |
| **Values** | `alloy`<br>`echo`<br>`fable`<br>`onyx`<br>`nova`<br>`shimmer` |

### VideoContent

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string |  | Yes |  |

### VideoContentVariant

Selectable asset variants for downloaded content.

| Property | Value |
|----------|-------|
| **Description** | Selectable asset variants for downloaded content. |
| **Type** | string |
| **Values** | `video`<br>`thumbnail`<br>`spritesheet` |

### VideoIdParameter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| video-id | string | The ID of the video to use for the Azure OpenAI request. | Yes |  |

### VideoList

A list of video generation jobs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array of [VideoResource](#videoresource) | The list of video generation jobs. | Yes |  |
| first_id | string | The ID of the first video in the current page, if available. | No |  |
| has_more | boolean | A flag indicating whether there are more jobs available after the list. | Yes |  |
| last_id | string | The ID of the last video in the current page, if available. | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### VideoResource

Structured information describing a generated video job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completed_at | integer | Unix timestamp (seconds) for when the job completed, if finished. | No |  |
| created_at | integer | Unix timestamp (seconds) for when the job was created. | Yes |  |
| error | [Error](#error) |  | No |  |
| └─ code | string |  | Yes |  |
| └─ message | string |  | Yes |  |
| expires_at | integer | Unix timestamp (seconds) for when the video generation expires (and will be deleted). | No |  |
| id | string | Unique identifier for the video job. | Yes |  |
| model | string | The video generation model deployment that produced the job. | Yes |  |
| object | string | The object type, which is always `video`. | Yes |  |
| progress | integer | Approximate completion percentage for the generation task. | Yes |  |
| remixed_from_video_id | string | Identifier of the source video if this video is a remix. | No |  |
| seconds | [VideoSeconds](#videoseconds) | Supported clip durations, measured in seconds. | Yes |  |
| size | [VideoSize](#videosize) | Output dimensions formatted as `{width}x{height}`. | Yes |  |
| status | [VideoStatus](#videostatus) | Lifecycle state of a generated video. | Yes |  |

### VideoSeconds

Supported clip durations, measured in seconds.

| Property | Value |
|----------|-------|
| **Description** | Supported clip durations, measured in seconds. |
| **Type** | string |
| **Values** | `4`<br>`8`<br>`12` |

### VideoSize

Output dimensions formatted as `{width}x{height}`.

| Property | Value |
|----------|-------|
| **Description** | Output dimensions formatted as `{width}x{height}`. |
| **Type** | string |
| **Values** | `720x1280`<br>`1280x720`<br>`1024x1792`<br>`1792x1024` |

### VideoStatus

Lifecycle state of a generated video.

| Property | Value |
|----------|-------|
| **Description** | Lifecycle state of a generated video. |
| **Type** | string |
| **Values** | `queued`<br>`in_progress`<br>`completed`<br>`failed` |
