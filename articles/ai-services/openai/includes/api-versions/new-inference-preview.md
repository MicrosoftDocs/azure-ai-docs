---
title: Azure OpenAI new v1 preview inference API documentation
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Latest v1 preview data plane inference documentation generated from OpenAPI 3.0 spec
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 05/23/2025
---

## Create speech

```HTTP
POST {endpoint}/openai/v1/audio/speech?api-version=preview
```

Generates text-to-speech audio from the input text.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| input | string | The text to generate audio for. The maximum length is 4096 characters. | Yes |  |
| instructions | string | Control the voice of your generated audio with additional instructions. Does not work with `tts-1` or `tts-1-hd`. | No |  |
| model | string | The model to use for this text-to-speech request. | Yes |  |
| response_format | object | The supported audio output formats for text-to-speech. | No |  |
| speed | number | The speed of speech for generated audio. Values are valid in the range from 0.25 to 4.0, with 1.0 the default and higher values corresponding to faster speech. | No | 1 |
| voice | object |  | Yes |  |

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

### Examples

### Example

Synthesizes audio from the provided text.

```HTTP
POST {endpoint}/openai/v1/audio/speech?api-version=preview

{
 "input": "Hi! What are you going to make?",
 "voice": "fable",
 "response_format": "mp3",
 "model": "tts-1"
}

```

**Responses**:
Status Code: 200

```json
{
  "body": "101010101"
}
```

## Create transcription

```HTTP
POST {endpoint}/openai/v1/audio/transcriptions?api-version=preview
```

Transcribes audio into the input language.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| chunking_strategy | object |  | No |  |
| └─ prefix_padding_ms | integer | Amount of audio to include before the VAD detected speech (in milliseconds). | No | 300 |
| └─ silence_duration_ms | integer | Duration of silence to detect speech stop (in milliseconds). With shorter values the model will respond more quickly, but may jump in on short pauses from the user. | No | 200 |
| └─ threshold | number | Sensitivity threshold (0.0 to 1.0) for voice activity detection. A higher threshold will require louder audio to activate the model, and thus might perform better in noisy environments. | No | 0.5 |
| └─ type | enum | Must be set to `server_vad` to enable manual chunking using server side VAD.<br>Possible values: `server_vad` | No |  |
| file | string |  | Yes |  |
| filename | string | The optional filename or descriptive identifier to associate with with the audio data. | No |  |
| include[] | array | Additional information to include in the transcription response. <br>`logprobs` will return the log probabilities of the tokens in the <br>response to understand the model's confidence in the transcription. <br>`logprobs` only works with response_format set to `json` and only with <br>the models `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`. | No |  |
| language | string | The language of the input audio. Supplying the input language in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format will improve accuracy and latency. | No |  |
| model | string | The model to use for this transcription request. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language. | No |  |
| response_format | object |  | No |  |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). Note: Streaming is not supported for the `whisper-1` model and will be ignored. | No | False |
| temperature | number | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use [log probability](https://en.wikipedia.org/wiki/Log_probability) to automatically increase the temperature until certain thresholds are hit. | No | 0 |
| timestamp_granularities[] | array | The timestamp granularities to populate for this transcription. `response_format` must be set `verbose_json` to use timestamp granularities. Either or both of these options are supported: `word`, or `segment`. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency. | No | ['segment'] |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureAudioTranscriptionResponse](#azureaudiotranscriptionresponse) | |
|text/plain | string | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example

Gets transcribed text and associated metadata from provided spoken audio data.

```HTTP
POST {endpoint}/openai/v1/audio/transcriptions?api-version=preview

{
 "file": "<binary audio data>",
 "model": "whisper-1",
 "response_format": "verbose_json"
}

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "text": "A structured object when requesting json or verbose_json"
  }
}
```

### Example

Gets transcribed text and associated metadata from provided spoken audio data.

```HTTP
POST {endpoint}/openai/v1/audio/transcriptions?api-version=preview

{
 "file": "<binary audio data>",
 "model": "whisper-1",
 "response_format": "text"
}

```

**Responses**:
Status Code: 200

```json
{
  "body": "plain text when requesting text, srt, or vtt"
}
```

## Create chat completion

```HTTP
POST {endpoint}/openai/v1/chat/completions?api-version=preview
```


Creates a chat completion.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| audio | object | Parameters for audio output. Required when audio output is requested with<br>`modalities: ["audio"]`. | No |  |
| └─ format | enum | Specifies the output audio format. Must be one of `wav`, `mp3`, `flac`,<br>`opus`, or `pcm16`.<br>Possible values: `wav`, `aac`, `mp3`, `flac`, `opus`, `pcm16` | No |  |
| └─ voice | object |  | No |  |
| data_sources | array | The data sources to use for the On Your Data feature, exclusive to Azure OpenAI. | No |  |
| frequency_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>their existing frequency in the text so far, decreasing the model's<br>likelihood to repeat the same line verbatim. | No | 0 |
| function_call | enum | Specifying a particular function via `{"name": "my_function"}` forces the model to call that function.<br>Possible values: `none`, `auto` | No |  |
| functions | array | Deprecated in favor of `tools`.<br><br>A list of functions the model may generate JSON inputs for. | No |  |
| logit_bias | object | Modify the likelihood of specified tokens appearing in the completion.<br><br>Accepts a JSON object that maps tokens (specified by their token ID in the<br>tokenizer) to an associated bias value from -100 to 100. Mathematically,<br>the bias is added to the logits generated by the model prior to sampling.<br>The exact effect will vary per model, but values between -1 and 1 should<br>decrease or increase likelihood of selection; values like -100 or 100<br>should result in a ban or exclusive selection of the relevant token. | No | None |
| logprobs | boolean | Whether to return log probabilities of the output tokens or not. If true,<br>returns the log probabilities of each output token returned in the<br>`content` of `message`. | No | False |
| max_completion_tokens | integer | An upper bound for the number of tokens that can be generated for a<br>completion, including visible output tokens and reasoning tokens. | No |  |
| max_tokens | integer | The maximum number of tokens that can be generated in the chat completion.<br>This value can be used to control costs for text generated via API.<br><br>This value is now deprecated in favor of `max_completion_tokens`, and is<br>not compatible with o1 series models. | No |  |
| messages | array | A list of messages comprising the conversation so far. Depending on the<br>model you use, different message types (modalities) are supported,<br>like text, images, and audio. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| modalities | object | Output types that you would like the model to generate.<br>Most models are capable of generating text, which is the default:<br><br>`["text"]`<br><br>The `gpt-4o-audio-preview` model can also be used to generate audio. To request that this model generate <br>both text and audio responses, you can use:<br><br>`["text", "audio"]` | No |  |
| model | string | The model deployment identifier to use for the chat completion request. | Yes |  |
| n | integer | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs. | No | 1 |
| parallel_tool_calls | object | Whether to enable parallel function calling during tool use. | No |  |
| prediction | object | Base representation of predicted output from a model. | No |  |
| └─ type | [OpenAI.ChatOutputPredictionType](#openaichatoutputpredictiontype) |  | No |  |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>whether they appear in the text so far, increasing the model's likelihood<br>to talk about new topics. | No | 0 |
| reasoning_effort | object | **o-series models only** <br><br>Constrains effort on reasoning for reasoning models. Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| response_format | object |  | No |  |
| └─ type | enum | <br>Possible values: `text`, `json_object`, `json_schema` | No |  |
| seed | integer | This feature is in Beta.<br>If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br>Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | object | Not supported with latest reasoning models `o3` and `o4-mini`.<br><br>Up to 4 sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| store | boolean | Whether or not to store the output of this chat completion request for<br>use in model distillation or evals products. | No | False |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using server-sent events. | No | False |
| stream_options | object | Options for streaming response. Only set this when you set `stream: true`. | No |  |
| └─ include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array. <br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| tool_choice | [OpenAI.ChatCompletionToolChoiceOption](#openaichatcompletiontoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tool and instead generates a message.<br>`auto` means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools.<br>Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.<br><br>`none` is the default when no tools are present. `auto` is the default if tools are present. | No |  |
| tools | array | A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to<br>return at each token position, each with an associated log probability.<br>`logprobs` must be set to `true` if this parameter is used. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| user | string | A unique identifier representing your end-user, which can help to<br>monitor and detect abuse. | No |  |
| user_security_context | [AzureUserSecurityContext](#azureusersecuritycontext) | User security context contains several parameters that describe the application itself, and the end user that interacts with the application. These fields assist your security operations teams to investigate and mitigate security incidents by providing a comprehensive approach to protecting your AI applications. [Learn more](https://aka.ms/TP4AI/Documentation/EndUserContext) about protecting AI applications using Microsoft Defender for Cloud. | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureCreateChatCompletionResponse](#azurecreatechatcompletionresponse) | |
|text/event-stream | [AzureCreateChatCompletionStreamResponse](#azurecreatechatcompletionstreamresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example

Creates a completion for the provided prompt, parameters and chosen model.

```HTTP
POST {endpoint}/openai/v1/chat/completions?api-version=preview

{
 "model": "gpt-4o-mini",
 "messages": [
  {
   "role": "system",
   "content": "you are a helpful assistant that talks like a pirate"
  },
  {
   "role": "user",
   "content": "can you tell me how to care for a parrot?"
  }
 ]
}

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "id": "chatcmpl-7R1nGnsXO8n4oi9UPz2f3UHdgAYMn",
    "created": 1686676106,
    "choices": [
      {
        "index": 0,
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": "Ahoy matey! So ye be wantin' to care for a fine squawkin' parrot, eh?..."
        }
      }
    ],
    "usage": {
      "completion_tokens": 557,
      "prompt_tokens": 33,
      "total_tokens": 590
    }
  }
}
```

## Create completion

```HTTP
POST {endpoint}/openai/v1/completions?api-version=preview
```


Creates a completion.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| best_of | integer | Generates `best_of` completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed.<br><br>When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return `best_of` must be greater than `n`.<br><br>**Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`. | No | 1 |
| echo | boolean | Echo back the prompt in addition to the completion | No | False |
| frequency_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.| No | 0 |
| logit_bias | object | Modify the likelihood of specified tokens appearing in the completion.<br><br>Accepts a JSON object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100.  Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.<br><br>As an example, you can pass `{"50256": -100}` to prevent the <&#124;endoftext&#124;> token from being generated. | No | None |
| logprobs | integer | Include the log probabilities on the `logprobs` most likely output tokens, as well the chosen tokens. For example, if `logprobs` is 5, the API will return a list of the 5 most likely tokens. The API will always return the `logprob` of the sampled token, so there may be up to `logprobs+1` elements in the response.<br><br>The maximum value for `logprobs` is 5. | No | None |
| max_tokens | integer | The maximum number of tokens that can be generated in the completion.<br><br>The token count of your prompt plus `max_tokens` cannot exceed the model's context length. | No | 16 |
| model | string | The model to use for the text completion request. | Yes |  |
| n | integer | How many completions to generate for each prompt.<br><br>**Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`. | No | 1 |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. | No | 0 |
| prompt | string or array | The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.<br>Note that <&#124;endoftext&#124;> is the document separator that the model sees during training, so if a prompt is not specified the model will generate as if from the beginning of a new document. | No |  |
| seed | integer | If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br><br>Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | object | Not supported with latest reasoning models `o3` and `o4-mini`.<br><br>Up to 4 sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| stream | boolean | Whether to stream back partial progress. If set, tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message.  | No | False |
| stream_options | object | Options for streaming response. Only set this when you set `stream: true`. | No |  |
| └─ include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array. <br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |
| suffix | string | The suffix that comes after a completion of inserted text.<br><br>This parameter is only supported for `gpt-3.5-turbo-instruct`. | No | None |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br><br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureCreateCompletionResponse](#azurecreatecompletionresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example

Creates a completion for the provided prompt, parameters and chosen model.

```HTTP
POST {endpoint}/openai/v1/completions?api-version=preview

{
 "model": "gpt-4o-mini",
 "prompt": [
  "tell me a joke about mango"
 ],
 "max_tokens": 32,
 "temperature": 1.0,
 "n": 1
}

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "id": "cmpl-7QmVI15qgYVllxK0FtxVGG6ywfzaq",
    "created": 1686617332,
    "choices": [
      {
        "text": "es\n\nWhat do you call a mango who's in charge?\n\nThe head mango.",
        "index": 0,
        "finish_reason": "stop",
        "logprobs": null
      }
    ],
    "usage": {
      "completion_tokens": 20,
      "prompt_tokens": 6,
      "total_tokens": 26
    }
  }
}
```

## Create embedding

```HTTP
POST {endpoint}/openai/v1/embeddings?api-version=preview
```

Creates an embedding vector representing the input text.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| dimensions | integer | The number of dimensions the resulting output embeddings should have. Only supported in `text-embedding-3` and later models. | No |  |
| encoding_format | enum | The format to return the embeddings in. Can be either `float` or [`base64`](https://pypi.org/project/pybase64/).<br>Possible values: `float`, `base64` | No |  |
| input | string or array |  | Yes |  |
| model | string | The model to use for the embedding request. | Yes |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.CreateEmbeddingResponse](#openaicreateembeddingresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example

Return the embeddings for a given prompt.

```HTTP
POST {endpoint}/openai/v1/embeddings?api-version=preview

{
 "model": "text-embedding-ada-002",
 "input": [
  "this is a test"
 ]
}

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "data": [
      {
        "index": 0,
        "embedding": [
          -0.012838088,
          -0.007421397,
          -0.017617522,
          -0.028278312,
          -0.018666342,
          0.01737855,
          -0.01821495,
          -0.006950092,
          -0.009937238,
          -0.038580645,
          0.010674067,
          0.02412286,
          -0.013647936,
          0.013189907,
          0.0021125758,
          0.012406612,
          0.020790534,
          0.00074595667,
          0.008397198,
          -0.00535031,
          0.008968075,
          0.014351576,
          -0.014086051,
          0.015055214,
          -0.022211088,
          -0.025198232,
          0.0065186154,
          -0.036350243,
          0.009180495,
          -0.009698266,
          0.009446018,
          -0.008463579,
          -0.0040426035,
          -0.03443847,
          -0.00091273896,
          -0.0019217303,
          0.002349888,
          -0.021560553,
          0.016515596,
          -0.015572986,
          0.0038666942,
          -8.432463e-05,
          0.0032178196,
          -0.020365695,
          -0.009631885,
          -0.007647093,
          0.0033837722,
          -0.026764825,
          -0.010501476,
          0.020219658,
          0.024640633,
          -0.0066912062,
          -0.036456455,
          -0.0040923897,
          -0.013966565,
          0.017816665,
          0.005366905,
          0.022835068,
          0.0103488,
          -0.0010811808,
          -0.028942121,
          0.0074280356,
          -0.017033368,
          0.0074877786,
          0.021640211,
          0.002499245,
          0.013316032,
          0.0021524043,
          0.010129742,
          0.0054731146,
          0.03143805,
          0.014856071,
          0.0023366117,
          -0.0008243692,
          0.022781964,
          0.003038591,
          -0.017617522,
          0.0013309394,
          0.0022154662,
          0.00097414135,
          0.012041516,
          -0.027906578,
          -0.023817508,
          0.013302756,
          -0.003003741,
          -0.006890349,
          0.0016744611
        ]
      }
    ],
    "usage": {
      "prompt_tokens": 4,
      "total_tokens": 4
    }
  }
}
```

## Image generations - Edit

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/images/edits?api-version=2025-04-01-preview
```

Edits an image from a text caption on a given gpt-image-1 model deployment

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| deployment-id | path | Yes | string |  |
| api-version | query | Yes | string |  |

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
| image | string or array | The image(s) to edit. Must be a supported image file or an array of images. Each image should be a png, or jpg file less than 25MB. | Yes |  |
| mask | string | An additional image whose fully transparent areas (e.g., where alpha is zero) indicate where the image should be edited. If there are multiple images provided, the mask will be applied to the first image. Must be a valid PNG file, less than 4MB, and have the same dimensions as the image. | No |  |
| n | integer | The number of images to generate. | No | 1 |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters. | Yes |  |
| quality | enum | The quality of the image that will be generated. `high`, `medium` and `low` are only supported for `gpt-image-1`. `dall-e-2` only supports `standard` quality. Defaults to `auto`.<br>Possible values: `standard`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which the generated images are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter is only supported for `dall-e-2`, as `gpt-image-1` will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`, and one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`.<br>Possible values: `256x256`, `512x512`, `1024x1024`, `1536x1024`, `1024x1536`, `auto` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |


### Responses

**Status Code:** 200

**Description**: Ok 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureImagesResponse](#azureimagesresponse) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [azureerrorresponse](#azureerrorresponse) | |


## Create image

```HTTP
POST {endpoint}/openai/v1/images/generations?api-version=preview
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| background | enum | Allows to set transparency for the background of the generated image(s). <br>This parameter is only supported for `gpt-image-1`. Must be one of <br>`transparent`, `opaque` or `auto` (default value). When `auto` is used, the <br>model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it <br>should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| model | string | The model deployment to use for the image generation. | Yes |  |
| moderation | enum | Control the content-moderation level for images generated by `gpt-image-1`. Must be either `low` for less restrictive filtering or `auto` (default value).<br>Possible values: `low`, `auto` | No |  |
| n | integer | The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter is only supported for `gpt-image-1` with the `webp` or `jpeg` output formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is only supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters for `gpt-image-1`, 1000 characters for `dall-e-2` and 4000 characters for `dall-e-3`. | Yes |  |
| quality | enum | The quality of the image that will be generated. <br><br>- `auto` (default value) will automatically select the best quality for the given model.<br>- `high`, `medium` and `low` are supported for `gpt-image-1`.<br>- `hd` and `standard` are supported for `dall-e-3`.<br>- `standard` is the only option for `dall-e-2`.<br>Possible values: `standard`, `hd`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which generated images with `dall-e-2` and `dall-e-3` are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter isn't supported for `gpt-image-1` which will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`, one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`, and one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3`.<br>Possible values: `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `256x256`, `512x512`, `1792x1024`, `1024x1792` | No |  |
| style | enum | The style of the generated images. This parameter is only supported for `dall-e-3`. Must be one of `vivid` or `natural`. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the model to produce more natural, less hyper-real looking images.<br>Possible values: `vivid`, `natural` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureImagesResponse](#azureimagesresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example

Creates images given a prompt.

```HTTP
POST {endpoint}/openai/v1/images/generations?api-version=preview

{
 "model": "dall-e-3",
 "prompt": "In the style of WordArt, Microsoft Clippy wearing a cowboy hat.",
 "n": 1,
 "style": "natural",
 "quality": "standard"
}

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "created": 1698342300,
    "data": [
      {
        "revised_prompt": "A vivid, natural representation of Microsoft Clippy wearing a cowboy hat.",
        "prompt_filter_results": {
          "sexual": {
            "severity": "safe",
            "filtered": false
          },
          "violence": {
            "severity": "safe",
            "filtered": false
          },
          "hate": {
            "severity": "safe",
            "filtered": false
          },
          "self_harm": {
            "severity": "safe",
            "filtered": false
          },
          "profanity": {
            "detected": false,
            "filtered": false
          },
          "custom_blocklists": {
            "filtered": false,
            "details": []
          }
        },
        "url": "https://dalletipusw2.blob.core.windows.net/private/images/e5451cc6-b1ad-4747-bd46-b89a3a3b8bc3/generated_00.png?se=2023-10-27T17%3A45%3A09Z&...",
        "content_filter_results": {
          "sexual": {
            "severity": "safe",
            "filtered": false
          },
          "violence": {
            "severity": "safe",
            "filtered": false
          },
          "hate": {
            "severity": "safe",
            "filtered": false
          },
          "self_harm": {
            "severity": "safe",
            "filtered": false
          }
        }
      }
    ]
  }
}
```

## Create response

```HTTP
POST {endpoint}/openai/v1/responses?api-version=preview
```


Creates a model response.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| background | boolean | Whether to run the model response in the background. | No | False |
| include | array | Specify additional output data to include in the model response. Currently<br>supported values are:<br>- `file_search_call.results`: Include the search results of<br>  the file search tool call.<br>- `message.input_image.image_url`: Include image urls from the input message.<br>- `computer_call_output.output.image_url`: Include image urls from the computer call output.<br>- `reasoning.encrypted_content`: Includes an encrypted version of reasoning <br>  tokens in reasoning item outputs. This enables reasoning items to be used in<br>  multi-turn conversations when using the Responses API statelessly (like<br>  when the `store` parameter is set to `false`, or when an organization is<br>  enrolled in the zero data retention program). | No |  |
| input | string or array |  | Yes |  |
| instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string | The model deployment to use for the creation of this response. | Yes |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only** <br><br>Constrains effort on reasoning for <br>reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| store | boolean | Whether to store the generated model response for later retrieval via<br>API. | No | True |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). | No | False |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities, like file search.<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>  enabling the model to call your own code. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureResponse](#azureresponse) | |
|text/event-stream | [OpenAI.ResponseStreamEvent](#openairesponsestreamevent) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example

Create a model response

```HTTP
POST {endpoint}/openai/v1/responses?api-version=preview

```

## Get response

```HTTP
GET {endpoint}/openai/v1/responses/{response_id}?api-version=preview
```


Retrieves a model response with the given ID.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| response_id | path | Yes | string |  |
| include[] | query | No | array |  |

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
|application/json | [AzureResponse](#azureresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Delete response

```HTTP
DELETE {endpoint}/openai/v1/responses/{response_id}?api-version=preview
```


Deletes a response by ID.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| response_id | path | Yes | string |  |

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

## Listinputitems

```HTTP
GET {endpoint}/openai/v1/responses/{response_id}/input_items?api-version=preview
```

Returns a list of input items for a given response.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| response_id | path | Yes | string |  |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |

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
|application/json | [OpenAI.ResponseItemList](#openairesponseitemlist) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Video generation jobs - Create

```HTTP
POST {endpoint}/openai/v1/video/generations/jobs?api-version=preview
```

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |

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
| height | integer | The height of the video. The following dimensions are supported: 480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080. | Yes |  |
| model | string | The name of the deployment to use for this request. | Yes |  |
| n_seconds | integer | The duration of the video generation job. Must be between 1 and 20 seconds. | No | 5 |
| n_variants | integer | The number of videos to create as variants for this job. Must be between 1 and 5. Smaller dimensions allow more variants. | No | 1 |
| prompt | string | The prompt for this video generation job. | Yes |  |
| width | integer | The width of the video. The following dimensions are supported: 480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080. | Yes |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [VideoGenerationJob](#videogenerationjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

### Examples

### Example

Create a video generation job

```HTTP
POST {endpoint}/openai/v1/video/generations/jobs?api-version=preview

{
 "prompt": "A cat playing piano in a jazz bar.",
 "model": "video-gen-001"
}

```

**Responses**:
Status Code: 200

```json
{
  "body": {
    "id": "vidjob_1234567890",
    "object": "video_generation_job",
    "created": 1680000000,
    "status": "queued",
    "prompt": "A cat playing piano in a jazz bar.",
    "model": "video-gen-001"
  }
}
```

## Video generation jobs - List

```HTTP
GET {endpoint}/openai/v1/video/generations/jobs?api-version=preview
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| before | query | No | string |  |
| after | query | No | string |  |
| limit | query | Yes | integer |  |
| statuses | query | No | array |  |

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
|application/json | [VideoGenerationJobList](#videogenerationjoblist) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Video generation jobs - Get

```HTTP
GET {endpoint}/openai/v1/video/generations/jobs/{job-id}?api-version=preview
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| job-id | path | Yes | string | The ID of the video generation job to use for the Azure OpenAI request. |

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
|application/json | [VideoGenerationJob](#videogenerationjob) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Video generation jobs - Delete

```HTTP
DELETE {endpoint}/openai/v1/video/generations/jobs/{job-id}?api-version=preview
```

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| job-id | path | Yes | string | The ID of the video generation job to use for the Azure OpenAI request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://cognitiveservices.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |

### Responses

**Status Code:** 204

**Description**: There is no content to send for this request, but the headers may be useful.  

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Video generations - Get

```HTTP
GET {endpoint}/openai/v1/video/generations/{generation-id}?api-version=preview
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |

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
|application/json | [VideoGeneration](#videogeneration) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Video generations - Retrieve thumbnail

```HTTP
GET {endpoint}/openai/v1/video/generations/{generation-id}/content/thumbnail?api-version=preview
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |
| If-Modified-Since | header | No | string | Timestamp formatted as GMT time |

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
|application/json | string | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Video generations - Retrieve video

```HTTP
GET {endpoint}/openai/v1/video/generations/{generation-id}/content/video?api-version=preview
```

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Model Inference API version to use for this request.<br>`latest` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |
| If-Modified-Since | header | No | string |  |
| quality | query | No |  |  |

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
|application/json | string | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Components

### AudioTaskLabel

Defines the possible descriptors for available audio operation responses.

| Property | Value |
|----------|-------|
| **Description** | Defines the possible descriptors for available audio operation responses. |
| **Type** | string |
| **Values** | `transcribe`<br>`translate` |

### AzureAIFoundryModelsApiVersion

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `latest`<br>`preview` |

### AzureAudioTranscriptionResponse

Result information for an operation that transcribed spoken audio into written text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| duration | number | The total duration of the audio processed to produce accompanying transcription information. | No |  |
| language | string | The spoken language that was detected in the transcribed audio data.<br>This is expressed as a two-letter ISO-639-1 language code like 'en' or 'fr'. | No |  |
| segments | array | A collection of information about the timing, probabilities, and other detail of each processed audio segment. | No |  |
| task | object | Defines the possible descriptors for available audio operation responses. | No |  |
| text | string | The transcribed text for the provided audio data. | Yes |  |
| words | array | A collection of information about the timing of each processed word. | No |  |

### AzureChatCompletionResponseMessage

The extended response model component for chat completion response messages on the Azure OpenAI service.
This model adds support for chat message context, used by the On Your Data feature for intent, citations, and other
information related to retrieval-augmented generation performed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array | Annotations for the message, when applicable, as when using the<br>web search tool. | No |  |
| audio | object | If the audio output modality is requested, this object contains data<br>about the audio response from the model. | No |  |
| └─ data | string | Base64 encoded audio bytes generated by the model, in the format<br>specified in the request. | No |  |
| └─ expires_at | integer | The Unix timestamp (in seconds) for when this audio response will<br>no longer be accessible on the server for use in multi-turn<br>conversations. | No |  |
| └─ id | string | Unique identifier for this audio response. | No |  |
| └─ transcript | string | Transcript of the audio generated by the model. | No |  |
| content | string | The contents of the message. | Yes |  |
| context | object | An additional property, added to chat completion response messages, produced by the Azure OpenAI service when using<br>extension behavior. This includes intent and citation information from the On Your Data feature. | No |  |
| └─ all_retrieved_documents | object | Summary information about documents retrieved by the data retrieval operation. | No |  |
|   └─ chunk_id | string | The chunk ID for the citation. | No |  |
|   └─ content | string | The content of the citation. | No |  |
|   └─ data_source_index | integer | The index of the data source used for retrieval. | No |  |
|   └─ filepath | string | The file path for the citation. | No |  |
|   └─ filter_reason | enum | If applicable, an indication of why the document was filtered.<br>Possible values: `score`, `rerank` | No |  |
|   └─ original_search_score | number | The original search score for the retrieval. | No |  |
|   └─ rerank_score | number | The rerank score for the retrieval. | No |  |
|   └─ search_queries | array | The search queries executed to retrieve documents. | No |  |
|   └─ title | string | The title for the citation. | No |  |
|   └─ url | string | The URL of the citation. | No |  |
| └─ citations | array | The citations produced by the data retrieval. | No |  |
| └─ intent | string | The detected intent from the chat history, which is used to carry conversation context between interactions | No |  |
| function_call | object | Deprecated and replaced by `tool_calls`. The name and arguments of a function that should be called, as generated by the model. | No |  |
| └─ arguments | string |  | No |  |
| └─ name | string |  | No |  |
| reasoning_content | string | An Azure-specific extension property containing generated reasoning content from supported models. | No |  |
| refusal | string | The refusal message generated by the model. | Yes |  |
| role | enum | The role of the author of this message.<br>Possible values: `assistant` | Yes |  |
| tool_calls | [ChatCompletionMessageToolCallsItem](#chatcompletionmessagetoolcallsitem) | The tool calls generated by the model, such as function calls. | No |  |

### AzureChatCompletionStreamResponseDelta

The extended response model for a streaming chat response message on the Azure OpenAI service.
This model adds support for chat message context, used by the On Your Data feature for intent, citations, and other
information related to retrieval-augmented generation performed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | object |  | No |  |
| └─ data | string |  | No |  |
| └─ expires_at | integer |  | No |  |
| └─ id | string |  | No |  |
| └─ transcript | string |  | No |  |
| content | string | The contents of the chunk message. | No |  |
| context | object | An additional property, added to chat completion response messages, produced by the Azure OpenAI service when using<br>extension behavior. This includes intent and citation information from the On Your Data feature. | No |  |
| └─ all_retrieved_documents | object | Summary information about documents retrieved by the data retrieval operation. | No |  |
|   └─ chunk_id | string | The chunk ID for the citation. | No |  |
|   └─ content | string | The content of the citation. | No |  |
|   └─ data_source_index | integer | The index of the data source used for retrieval. | No |  |
|   └─ filepath | string | The file path for the citation. | No |  |
|   └─ filter_reason | enum | If applicable, an indication of why the document was filtered.<br>Possible values: `score`, `rerank` | No |  |
|   └─ original_search_score | number | The original search score for the retrieval. | No |  |
|   └─ rerank_score | number | The rerank score for the retrieval. | No |  |
|   └─ search_queries | array | The search queries executed to retrieve documents. | No |  |
|   └─ title | string | The title for the citation. | No |  |
|   └─ url | string | The URL of the citation. | No |  |
| └─ citations | array | The citations produced by the data retrieval. | No |  |
| └─ intent | string | The detected intent from the chat history, which is used to carry conversation context between interactions | No |  |
| function_call | object | Deprecated and replaced by `tool_calls`. The name and arguments of a function that should be called, as generated by the model. | No |  |
| └─ arguments | string |  | No |  |
| └─ name | string |  | No |  |
| reasoning_content | string | An Azure-specific extension property containing generated reasoning content from supported models. | No |  |
| refusal | string | The refusal message generated by the model. | No |  |
| role | object | The role of the author of a message | No |  |
| tool_calls | array |  | No |  |

### AzureChatDataSource

A representation of configuration data for a single Azure OpenAI chat data source.
This will be used by a chat completions request that should use Azure OpenAI chat extensions to augment the
response behavior.
The use of this configuration is compatible only with Azure OpenAI.


### Discriminator for AzureChatDataSource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `azure_search` | [AzureSearchChatDataSource](#azuresearchchatdatasource) |
| `azure_cosmos_db` | [AzureCosmosDBChatDataSource](#azurecosmosdbchatdatasource) |
| `elasticsearch` | [ElasticsearchChatDataSource](#elasticsearchchatdatasource) |
| `pinecone` | [PineconeChatDataSource](#pineconechatdatasource) |
| `mongo_db` | [MongoDBChatDataSource](#mongodbchatdatasource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | object |  | Yes |  |

### AzureChatDataSourceAccessTokenAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| access_token | string |  | Yes |  |
| type | enum | <br>Possible values: `access_token` | Yes |  |

### AzureChatDataSourceApiKeyAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| key | string |  | Yes |  |
| type | enum | <br>Possible values: `api_key` | Yes |  |

### AzureChatDataSourceAuthenticationOptions


### Discriminator for AzureChatDataSourceAuthenticationOptions

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `system_assigned_managed_identity` | [AzureChatDataSourceSystemAssignedManagedIdentityAuthenticationOptions](#azurechatdatasourcesystemassignedmanagedidentityauthenticationoptions) |
| `user_assigned_managed_identity` | [AzureChatDataSourceUserAssignedManagedIdentityAuthenticationOptions](#azurechatdatasourceuserassignedmanagedidentityauthenticationoptions) |
| `access_token` | [AzureChatDataSourceAccessTokenAuthenticationOptions](#azurechatdatasourceaccesstokenauthenticationoptions) |
| `connection_string` | [AzureChatDataSourceConnectionStringAuthenticationOptions](#azurechatdatasourceconnectionstringauthenticationoptions) |
| `key_and_key_id` | [AzureChatDataSourceKeyAndKeyIdAuthenticationOptions](#azurechatdatasourcekeyandkeyidauthenticationoptions) |
| `encoded_api_key` | [AzureChatDataSourceEncodedApiKeyAuthenticationOptions](#azurechatdatasourceencodedapikeyauthenticationoptions) |
| `username_and_password` | [AzureChatDataSourceUsernameAndPasswordAuthenticationOptions](#azurechatdatasourceusernameandpasswordauthenticationoptions) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [AzureChatDataSourceAuthenticationOptionsType](#azurechatdatasourceauthenticationoptionstype) |  | Yes |  |

### AzureChatDataSourceAuthenticationOptionsType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `api_key`<br>`username_and_password`<br>`connection_string`<br>`key_and_key_id`<br>`encoded_api_key`<br>`access_token`<br>`system_assigned_managed_identity`<br>`user_assigned_managed_identity` |

### AzureChatDataSourceConnectionStringAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| connection_string | string |  | Yes |  |
| type | enum | <br>Possible values: `connection_string` | Yes |  |

### AzureChatDataSourceDeploymentNameVectorizationSource

Represents a vectorization source that makes internal service calls against an Azure OpenAI embedding model
deployment. In contrast with the endpoint-based vectorization source, a deployment-name-based vectorization source
must be part of the same Azure OpenAI resource but can be used even in private networks.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deployment_name | string | The embedding model deployment to use for vectorization. This deployment must exist within the same Azure OpenAI<br>resource as the model deployment being used for chat completions. | Yes |  |
| dimensions | integer | The number of dimensions to request on embeddings.<br>Only supported in 'text-embedding-3' and later models. | No |  |
| type | enum | The type identifier, always 'deployment_name' for this vectorization source type.<br>Possible values: `deployment_name` | Yes |  |

### AzureChatDataSourceEncodedApiKeyAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| encoded_api_key | string |  | Yes |  |
| type | enum | <br>Possible values: `encoded_api_key` | Yes |  |

### AzureChatDataSourceEndpointVectorizationSource

Represents a vectorization source that makes public service calls against an Azure OpenAI embedding model deployment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| authentication | object |  | Yes |  |
| └─ access_token | string |  | No |  |
| └─ key | string |  | No |  |
| └─ type | enum | <br>Possible values: `access_token` | No |  |
| dimensions | integer | The number of dimensions to request on embeddings.<br>Only supported in 'text-embedding-3' and later models. | No |  |
| endpoint | string | Specifies the resource endpoint URL from which embeddings should be retrieved.<br>It should be in the format of:<br>https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/embeddings.<br>The api-version query parameter is not allowed. | Yes |  |
| type | enum | The type identifier, always 'endpoint' for this vectorization source type.<br>Possible values: `endpoint` | Yes |  |

### AzureChatDataSourceIntegratedVectorizationSource

Represents an integrated vectorization source as defined within the supporting search resource.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type identifier, always 'integrated' for this vectorization source type.<br>Possible values: `integrated` | Yes |  |

### AzureChatDataSourceKeyAndKeyIdAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| key | string |  | Yes |  |
| key_id | string |  | Yes |  |
| type | enum | <br>Possible values: `key_and_key_id` | Yes |  |

### AzureChatDataSourceModelIdVectorizationSource

Represents a vectorization source that makes service calls based on a search service model ID.
This source type is currently only supported by Elasticsearch.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| model_id | string | The embedding model build ID to use for vectorization. | Yes |  |
| type | enum | The type identifier, always 'model_id' for this vectorization source type.<br>Possible values: `model_id` | Yes |  |

### AzureChatDataSourceSystemAssignedManagedIdentityAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `system_assigned_managed_identity` | Yes |  |

### AzureChatDataSourceType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `azure_search`<br>`azure_cosmos_db`<br>`elasticsearch`<br>`pinecone`<br>`mongo_db` |

### AzureChatDataSourceUserAssignedManagedIdentityAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| managed_identity_resource_id | string |  | Yes |  |
| type | enum | <br>Possible values: `user_assigned_managed_identity` | Yes |  |

### AzureChatDataSourceUsernameAndPasswordAuthenticationOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| password | string |  | Yes |  |
| type | enum | <br>Possible values: `username_and_password` | Yes |  |
| username | string |  | Yes |  |

### AzureChatDataSourceVectorizationSource

A representation of a data vectorization source usable as an embedding resource with a data source.


### Discriminator for AzureChatDataSourceVectorizationSource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `deployment_name` | [AzureChatDataSourceDeploymentNameVectorizationSource](#azurechatdatasourcedeploymentnamevectorizationsource) |
| `integrated` | [AzureChatDataSourceIntegratedVectorizationSource](#azurechatdatasourceintegratedvectorizationsource) |
| `model_id` | [AzureChatDataSourceModelIdVectorizationSource](#azurechatdatasourcemodelidvectorizationsource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | object |  | Yes |  |

### AzureChatDataSourceVectorizationSourceType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `endpoint`<br>`deployment_name`<br>`model_id`<br>`integrated` |

### AzureChatMessageContext

An additional property, added to chat completion response messages, produced by the Azure OpenAI service when using
extension behavior. This includes intent and citation information from the On Your Data feature.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| all_retrieved_documents | object | Summary information about documents retrieved by the data retrieval operation. | No |  |
| └─ chunk_id | string | The chunk ID for the citation. | No |  |
| └─ content | string | The content of the citation. | No |  |
| └─ data_source_index | integer | The index of the data source used for retrieval. | No |  |
| └─ filepath | string | The file path for the citation. | No |  |
| └─ filter_reason | enum | If applicable, an indication of why the document was filtered.<br>Possible values: `score`, `rerank` | No |  |
| └─ original_search_score | number | The original search score for the retrieval. | No |  |
| └─ rerank_score | number | The rerank score for the retrieval. | No |  |
| └─ search_queries | array | The search queries executed to retrieve documents. | No |  |
| └─ title | string | The title for the citation. | No |  |
| └─ url | string | The URL of the citation. | No |  |
| citations | array | The citations produced by the data retrieval. | No |  |
| intent | string | The detected intent from the chat history, which is used to carry conversation context between interactions | No |  |

### AzureContentFilterBlocklistResult

A collection of true/false filtering results for configured custom blocklists.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| details | array | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
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
| details | array | Detailed information about the detected completion text spans. | Yes |  |
| detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |

### AzureContentFilterDetectionResult

A labeled content filter result item that indicates whether the content was detected and whether the content was
filtered.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detected | boolean | Whether the labeled content category was detected in the content. | Yes |  |
| filtered | boolean | Whether the content detection resulted in a content filtering action. | Yes |  |

### AzureContentFilterImagePromptResults

A content filter result for an image generation operation's input request content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom_blocklists | object | A collection of true/false filtering results for configured custom blocklists. | No |  |
| └─ details | array | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
| └─ filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | No |  |
| jailbreak | object | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | Yes |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |
| profanity | object | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |

### AzureContentFilterImageResponseResults

A content filter result for an image generation operation's output response content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| hate | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| self_harm | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| sexual | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| violence | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |

### AzureContentFilterResultForChoice

A content filter result for a single response item produced by a generative AI system.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom_blocklists | object | A collection of true/false filtering results for configured custom blocklists. | No |  |
| └─ details | array | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
| └─ filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | No |  |
| error | object | If present, details about an error that prevented content filtering from completing its evaluation. | No |  |
| └─ code | integer | A distinct, machine-readable code associated with the error. | No |  |
| └─ message | string | A human-readable message associated with the error. | No |  |
| hate | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| profanity | object | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |
| protected_material_code | object | A detection result that describes a match against licensed code or other protected source material. | No |  |
| └─ citation | object | If available, the citation details describing the associated license and its location. | No |  |
|   └─ URL | string | The URL associated with the license. | No |  |
|   └─ license | string | The name or identifier of the license associated with the detection. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |
| protected_material_text | object | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
| └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
| └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |
| self_harm | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| sexual | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| ungrounded_material | [AzureContentFilterCompletionTextSpanDetectionResult](#azurecontentfiltercompletiontextspandetectionresult) |  | No |  |
| violence | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
| └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
| └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |

### AzureContentFilterResultForPrompt

A content filter result associated with a single input prompt item into a generative AI system.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_filter_results | object | The content filter category details for the result. | No |  |
| └─ custom_blocklists | object | A collection of true/false filtering results for configured custom blocklists. | No |  |
|   └─ details | array | The pairs of individual blocklist IDs and whether they resulted in a filtering action. | No |  |
|   └─ filtered | boolean | A value indicating whether any of the detailed blocklists resulted in a filtering action. | No |  |
| └─ error | object | If present, details about an error that prevented content filtering from completing its evaluation. | No |  |
|   └─ code | integer | A distinct, machine-readable code associated with the error. | No |  |
|   └─ message | string | A human-readable message associated with the error. | No |  |
| └─ hate | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| └─ indirect_attack | object | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
|   └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
|   └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |
| └─ jailbreak | object | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
|   └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
|   └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |
| └─ profanity | object | A labeled content filter result item that indicates whether the content was detected and whether the content was<br>filtered. | No |  |
|   └─ detected | boolean | Whether the labeled content category was detected in the content. | No |  |
|   └─ filtered | boolean | Whether the content detection resulted in a content filtering action. | No |  |
| └─ self_harm | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| └─ sexual | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| └─ violence | object | A labeled content filter result item that indicates whether the content was filtered and what the qualitative<br>severity level of the content was, as evaluated against content filter configuration for the category. | No |  |
|   └─ filtered | boolean | Whether the content severity resulted in a content filtering action. | No |  |
|   └─ severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | No |  |
| prompt_index | integer | The index of the input prompt associated with the accompanying content filter result categories. | No |  |

### AzureContentFilterSeverityResult

A labeled content filter result item that indicates whether the content was filtered and what the qualitative
severity level of the content was, as evaluated against content filter configuration for the category.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filtered | boolean | Whether the content severity resulted in a content filtering action. | Yes |  |
| severity | enum | The labeled severity of the content.<br>Possible values: `safe`, `low`, `medium`, `high` | Yes |  |

### AzureCosmosDBChatDataSource

Represents a data source configuration that will use an Azure CosmosDB resource.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| parameters | object | The parameter information to control the use of the Azure CosmosDB data source. | Yes |  |
| └─ allow_partial_result | boolean | If set to true, the system will allow partial search results to be used and the request will fail if all<br>partial queries fail. If not specified or specified as false, the request will fail if any search query fails. | No | False |
| └─ authentication | [AzureChatDataSourceConnectionStringAuthenticationOptions](#azurechatdatasourceconnectionstringauthenticationoptions) |  | No |  |
| └─ container_name | string |  | No |  |
| └─ database_name | string |  | No |  |
| └─ embedding_dependency | [AzureChatDataSourceVectorizationSource](#azurechatdatasourcevectorizationsource) | A representation of a data vectorization source usable as an embedding resource with a data source. | No |  |
| └─ fields_mapping | object |  | No |  |
|   └─ content_fields | array |  | No |  |
|   └─ content_fields_separator | string |  | No |  |
|   └─ filepath_field | string |  | No |  |
|   └─ title_field | string |  | No |  |
|   └─ url_field | string |  | No |  |
|   └─ vector_fields | array |  | No |  |
| └─ in_scope | boolean | Whether queries should be restricted to use of the indexed data. | No |  |
| └─ include_contexts | array | The output context properties to include on the response.<br>By default, citations and intent will be requested. | No | ['citations', 'intent'] |
| └─ index_name | string |  | No |  |
| └─ max_search_queries | integer | The maximum number of rewritten queries that should be sent to the search provider for a single user message.<br>By default, the system will make an automatic determination. | No |  |
| └─ strictness | integer | The configured strictness of the search relevance filtering.<br>Higher strictness will increase precision but lower recall of the answer. | No |  |
| └─ top_n_documents | integer | The configured number of documents to feature in the query. | No |  |
| type | enum | The discriminated type identifier, which is always 'azure_cosmos_db'.<br>Possible values: `azure_cosmos_db` | Yes |  |

### AzureCreateChatCompletionRequest

The extended request model for chat completions against the Azure OpenAI service.
This adds the ability to provide data sources for the On Your Data feature.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | object | Parameters for audio output. Required when audio output is requested with<br>`modalities: ["audio"]`. | No |  |
| └─ format | enum | Specifies the output audio format. Must be one of `wav`, `mp3`, `flac`,<br>`opus`, or `pcm16`.<br>Possible values: `wav`, `aac`, `mp3`, `flac`, `opus`, `pcm16` | No |  |
| └─ voice | object |  | No |  |
| data_sources | array | The data sources to use for the On Your Data feature, exclusive to Azure OpenAI. | No |  |
| frequency_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>their existing frequency in the text so far, decreasing the model's<br>likelihood to repeat the same line verbatim. | No | 0 |
| function_call | enum | Specifying a particular function via `{"name": "my_function"}` forces the model to call that function.<br>Possible values: `none`, `auto` | No |  |
| functions | array | Deprecated in favor of `tools`.<br><br>A list of functions the model may generate JSON inputs for. | No |  |
| logit_bias | object | Modify the likelihood of specified tokens appearing in the completion.<br><br>Accepts a JSON object that maps tokens (specified by their token ID in the<br>tokenizer) to an associated bias value from -100 to 100. Mathematically,<br>the bias is added to the logits generated by the model prior to sampling.<br>The exact effect will vary per model, but values between -1 and 1 should<br>decrease or increase likelihood of selection; values like -100 or 100<br>should result in a ban or exclusive selection of the relevant token. | No | None |
| logprobs | boolean | Whether to return log probabilities of the output tokens or not. If true,<br>returns the log probabilities of each output token returned in the<br>`content` of `message`. | No | False |
| max_completion_tokens | integer | An upper bound for the number of tokens that can be generated for a<br>completion, including visible output tokens and reasoning tokens. | No |  |
| max_tokens | integer | The maximum number of tokens that can be generated in the chat completion.<br>This value can be used to control costs for text generated via API.<br><br>This value is now deprecated in favor of `max_completion_tokens`, and is<br>not compatible with o1 series models. | No |  |
| messages | array | A list of messages comprising the conversation so far. Depending on the<br>model you use, different message types (modalities) are supported,<br>like text, images, and audio. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| modalities | object | Output types that you would like the model to generate.<br>Most models are capable of generating text, which is the default:<br><br>`["text"]`<br><br>The `gpt-4o-audio-preview` model can also be used to <br>generate audio. To request that this model generate <br>both text and audio responses, you can use:<br><br>`["text", "audio"]` | No |  |
| model | string | The model deployment identifier to use for the chat completion request. | Yes |  |
| n | integer | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs. | No | 1 |
| parallel_tool_calls | object | Whether to enable parallel function calling during tool use. | No |  |
| prediction | object | Base representation of predicted output from a model. | No |  |
| └─ type | [OpenAI.ChatOutputPredictionType](#openaichatoutputpredictiontype) |  | No |  |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>whether they appear in the text so far, increasing the model's likelihood<br>to talk about new topics. | No | 0 |
| reasoning_effort | object | **o-series models only** <br><br>Constrains effort on reasoning for <br>reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| response_format | object |  | No |  |
| └─ type | enum | <br>Possible values: `text`, `json_object`, `json_schema` | No |  |
| seed | integer | This feature is in Beta.<br>If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br>Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | object | Not supported with latest reasoning models `o3` and `o4-mini`.<br><br>Up to 4 sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| store | boolean | Whether or not to store the output of this chat completion request for<br>use in model distillation or evals products. | No | False |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using server-sent events. | No | False |
| stream_options | object | Options for streaming response. Only set this when you set `stream: true`. | No |  |
| └─ include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array. <br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| tool_choice | [OpenAI.ChatCompletionToolChoiceOption](#openaichatcompletiontoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tool and instead generates a message.<br>`auto` means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools.<br>Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.<br><br>`none` is the default when no tools are present. `auto` is the default if tools are present. | No |  |
| tools | array | A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to<br>return at each token position, each with an associated log probability.<br>`logprobs` must be set to `true` if this parameter is used. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| user | string | A unique identifier representing your end-user, which can help to<br>monitor and detect abuse. | No |  |
| user_security_context | [AzureUserSecurityContext](#azureusersecuritycontext) | User security context contains several parameters that describe the application itself, and the end user that interacts with the application. These fields assist your security operations teams to investigate and mitigate security incidents by providing a comprehensive approach to protecting your AI applications. [Learn more](https://aka.ms/TP4AI/Documentation/EndUserContext) about protecting AI applications using Microsoft Defender for Cloud. | No |  |

### AzureCreateChatCompletionResponse

The extended top-level chat completion response model for the Azure OpenAI service.
This model adds Responsible AI content filter annotations for prompt input.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| choices | array |  | Yes |  |
| created | integer | The Unix timestamp (in seconds) of when the chat completion was created. | Yes |  |
| id | string | A unique identifier for the chat completion. | Yes |  |
| model | string | The model used for the chat completion. | Yes |  |
| object | enum | The object type, which is always `chat.completion`.<br>Possible values: `chat.completion` | Yes |  |
| prompt_filter_results | array | The Responsible AI content filter annotations associated with prompt inputs into chat completions. | No |  |
| system_fingerprint | string | This fingerprint represents the backend configuration that the model runs with.<br><br>Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism. | No |  |
| usage | [OpenAI.CompletionUsage](#openaicompletionusage) | Usage statistics for the completion request. | No |  |

### AzureCreateChatCompletionStreamResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| choices | array | A list of chat completion choices. Can contain more than one elements if `n` is greater than 1. Can also be empty for the<br>last chunk if you set `stream_options: {"include_usage": true}`. | Yes |  |
| created | integer | The Unix timestamp (in seconds) of when the chat completion was created. Each chunk has the same timestamp. | Yes |  |
| delta | [AzureChatCompletionStreamResponseDelta](#azurechatcompletionstreamresponsedelta) | The extended response model for a streaming chat response message on the Azure OpenAI service.<br>This model adds support for chat message context, used by the On Your Data feature for intent, citations, and other<br>information related to retrieval-augmented generation performed. | No |  |
| id | string | A unique identifier for the chat completion. Each chunk has the same ID. | Yes |  |
| model | string | The model to generate the completion. | Yes |  |
| object | enum | The object type, which is always `chat.completion.chunk`.<br>Possible values: `chat.completion.chunk` | Yes |  |
| system_fingerprint | string | This fingerprint represents the backend configuration that the model runs with.<br>Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism. | No |  |
| usage | object | Usage statistics for the completion request. | No |  |
| └─ completion_tokens | integer | Number of tokens in the generated completion. | No | 0 |
| └─ completion_tokens_details | object | Breakdown of tokens used in a completion. | No |  |
|   └─ accepted_prediction_tokens | integer | When using Predicted Outputs, the number of tokens in the<br>prediction that appeared in the completion. | No | 0 |
|   └─ audio_tokens | integer | Audio input tokens generated by the model. | No | 0 |
|   └─ reasoning_tokens | integer | Tokens generated by the model for reasoning. | No | 0 |
|   └─ rejected_prediction_tokens | integer | When using Predicted Outputs, the number of tokens in the<br>prediction that did not appear in the completion. However, like<br>reasoning tokens, these tokens are still counted in the total<br>completion tokens for purposes of billing, output, and context window<br>limits. | No | 0 |
| └─ prompt_tokens | integer | Number of tokens in the prompt. | No | 0 |
| └─ prompt_tokens_details | object | Breakdown of tokens used in the prompt. | No |  |
|   └─ audio_tokens | integer | Audio input tokens present in the prompt. | No | 0 |
|   └─ cached_tokens | integer | Cached tokens present in the prompt. | No | 0 |
| └─ total_tokens | integer | Total number of tokens used in the request (prompt + completion). | No | 0 |

### AzureCreateCompletionRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| best_of | integer | Generates `best_of` completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed.<br><br>When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return â&euro;" `best_of` must be greater than `n`.<br><br>**Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`. | No | 1 |
| echo | boolean | Echo back the prompt in addition to the completion | No | False |
| frequency_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. | No | 0 |
| logit_bias | object | Modify the likelihood of specified tokens appearing in the completion.<br><br>Accepts a JSON object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100.  Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.<br><br>As an example, you can pass `{"50256": -100}` to prevent the <&#124;endoftext&#124;> token from being generated. | No | None |
| logprobs | integer | Include the log probabilities on the `logprobs` most likely output tokens, as well the chosen tokens. For example, if `logprobs` is 5, the API will return a list of the 5 most likely tokens. The API will always return the `logprob` of the sampled token, so there may be up to `logprobs+1` elements in the response.<br><br>The maximum value for `logprobs` is 5. | No | None |
| max_tokens | integer | The maximum number of tokens that can be generated in the completion.<br><br>The token count of your prompt plus `max_tokens` cannot exceed the model's context length. | No | 16 |
| model | string | The model to use for the text completion request. | Yes |  |
| n | integer | How many completions to generate for each prompt.<br><br>**Note:** Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for `max_tokens` and `stop`. | No | 1 |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. | No | 0 |
| prompt | string or array | The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.<br>Note that <&#124;endoftext&#124;> is the document separator that the model sees during training, so if a prompt is not specified the model will generate as if from the beginning of a new document. | No |  |
| seed | integer | If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br><br>Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | object | Not supported with latest reasoning models `o3` and `o4-mini`.<br><br>Up to 4 sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| stream | boolean | Whether to stream back partial progress. If set, tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message.  | No | False |
| stream_options | object | Options for streaming response. Only set this when you set `stream: true`. | No |  |
| └─ include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array. <br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |
| suffix | string | The suffix that comes after a completion of inserted text.<br><br>This parameter is only supported for `gpt-3.5-turbo-instruct`. | No | None |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br><br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateCompletionResponse

Represents a completion response from the API. Note: both the streamed and non-streamed response objects share the same shape (unlike the chat endpoint).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| choices | array | The list of completion choices the model generated for the input prompt. | Yes |  |
| created | integer | The Unix timestamp (in seconds) of when the completion was created. | Yes |  |
| id | string | A unique identifier for the completion. | Yes |  |
| model | string | The model used for completion. | Yes |  |
| object | enum | The object type, which is always "text_completion"<br>Possible values: `text_completion` | Yes |  |
| prompt_filter_results | array |  | No |  |
| system_fingerprint | string | This fingerprint represents the backend configuration that the model runs with.<br><br>Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made that might impact determinism. | No |  |
| usage | [OpenAI.CompletionUsage](#openaicompletionusage) | Usage statistics for the completion request. | No |  |

### AzureCreateEmbeddingRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| dimensions | integer | The number of dimensions the resulting output embeddings should have. Only supported in `text-embedding-3` and later models. | No |  |
| encoding_format | enum | The format to return the embeddings in. Can be either `float` or [`base64`](https://pypi.org/project/pybase64/).<br>Possible values: `float`, `base64` | No |  |
| input | string or array |  | Yes |  |
| model | string | The model to use for the embedding request. | Yes |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateImageEditRequestMultiPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Allows to set transparency for the background of the generated image(s). <br>This parameter is only supported for `gpt-image-1`. Must be one of <br>`transparent`, `opaque` or `auto` (default value). When `auto` is used, the <br>model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it <br>should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| image | string or array |  | Yes |  |
| mask | string |  | No |  |
| model | string | The model deployment to use for the image edit operation. | Yes |  |
| n | integer | The number of images to generate. Must be between 1 and 10. | No | 1 |
| prompt | string | A text description of the desired image(s). The maximum length is 1000 characters for `dall-e-2`, and 32000 characters for `gpt-image-1`. | Yes |  |
| quality | enum | The quality of the image that will be generated. `high`, `medium` and `low` are only supported for `gpt-image-1`. `dall-e-2` only supports `standard` quality. Defaults to `auto`.<br>Possible values: `standard`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which the generated images are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter is only supported for `dall-e-2`, as `gpt-image-1` will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`, and one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`.<br>Possible values: `256x256`, `512x512`, `1024x1024`, `1536x1024`, `1024x1536`, `auto` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateImageRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Allows to set transparency for the background of the generated image(s). <br>This parameter is only supported for `gpt-image-1`. Must be one of <br>`transparent`, `opaque` or `auto` (default value). When `auto` is used, the <br>model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it <br>should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| model | string | The model deployment to use for the image generation. | Yes |  |
| moderation | enum | Control the content-moderation level for images generated by `gpt-image-1`. Must be either `low` for less restrictive filtering or `auto` (default value).<br>Possible values: `low`, `auto` | No |  |
| n | integer | The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter is only supported for `gpt-image-1` with the `webp` or `jpeg` output formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is only supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters for `gpt-image-1`, 1000 characters for `dall-e-2` and 4000 characters for `dall-e-3`. | Yes |  |
| quality | enum | The quality of the image that will be generated. <br><br>- `auto` (default value) will automatically select the best quality for the given model.<br>- `high`, `medium` and `low` are supported for `gpt-image-1`.<br>- `hd` and `standard` are supported for `dall-e-3`.<br>- `standard` is the only option for `dall-e-2`.<br>Possible values: `standard`, `hd`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which generated images with `dall-e-2` and `dall-e-3` are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter isn't supported for `gpt-image-1` which will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`, one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`, and one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3`.<br>Possible values: `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `256x256`, `512x512`, `1792x1024`, `1024x1792` | No |  |
| style | enum | The style of the generated images. This parameter is only supported for `dall-e-3`. Must be one of `vivid` or `natural`. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the model to produce more natural, less hyper-real looking images.<br>Possible values: `vivid`, `natural` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean | Whether to run the model response in the background. | No | False |
| include | array | Specify additional output data to include in the model response. Currently<br>supported values are:<br>- `file_search_call.results`: Include the search results of<br>  the file search tool call.<br>- `message.input_image.image_url`: Include image urls from the input message.<br>- `computer_call_output.output.image_url`: Include image urls from the computer call output.<br>- `reasoning.encrypted_content`: Includes an encrypted version of reasoning <br>  tokens in reasoning item outputs. This enables reasoning items to be used in<br>  multi-turn conversations when using the Responses API statelessly (like<br>  when the `store` parameter is set to `false`, or when an organization is<br>  enrolled in the zero data retention program). | No |  |
| input | string or array |  | Yes |  |
| instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string | The model deployment to use for the creation of this response. | Yes |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only** <br><br>Constrains effort on reasoning for <br>reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| store | boolean | Whether to store the generated model response for later retrieval via<br>API. | No | True |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). | No | False |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities, like file search.<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>  enabling the model to call your own code. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateSpeechRequestMultiPart

A representation of the request options that control the behavior of a text-to-speech operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input | string | The text to generate audio for. The maximum length is 4096 characters. | Yes |  |
| instructions | string | Control the voice of your generated audio with additional instructions. Does not work with `tts-1` or `tts-1-hd`. | No |  |
| model | string | The model to use for this text-to-speech request. | Yes |  |
| response_format | object | The supported audio output formats for text-to-speech. | No |  |
| speed | number | The speed of speech for generated audio. Values are valid in the range from 0.25 to 4.0, with 1.0 the default and higher values corresponding to faster speech. | No | 1 |
| voice | object |  | Yes |  |

### AzureCreateTranscriptionRequestMultiPart

The configuration information for an audio transcription request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking_strategy | object |  | No |  |
| └─ prefix_padding_ms | integer | Amount of audio to include before the VAD detected speech (in<br>milliseconds). | No | 300 |
| └─ silence_duration_ms | integer | Duration of silence to detect speech stop (in milliseconds).<br>With shorter values the model will respond more quickly,<br>but may jump in on short pauses from the user. | No | 200 |
| └─ threshold | number | Sensitivity threshold (0.0 to 1.0) for voice activity detection. A<br>higher threshold will require louder audio to activate the model, and<br>thus might perform better in noisy environments. | No | 0.5 |
| └─ type | enum | Must be set to `server_vad` to enable manual chunking using server side VAD.<br>Possible values: `server_vad` | No |  |
| file | string |  | Yes |  |
| filename | string | The optional filename or descriptive identifier to associate with with the audio data. | No |  |
| include[] | array | Additional information to include in the transcription response. <br>`logprobs` will return the log probabilities of the tokens in the <br>response to understand the model's confidence in the transcription. <br>`logprobs` only works with response_format set to `json` and only with <br>the models `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`. | No |  |
| language | string | The language of the input audio. Supplying the input language in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format will improve accuracy and latency. | No |  |
| model | string | The model to use for this transcription request. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language. | No |  |
| response_format | object |  | No |  |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). <br>Note: Streaming is not supported for the `whisper-1` model and will be ignored. | No | False |
| temperature | number | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use [log probability](https://en.wikipedia.org/wiki/Log_probability) to automatically increase the temperature until certain thresholds are hit. | No | 0 |
| timestamp_granularities[] | array | The timestamp granularities to populate for this transcription. `response_format` must be set `verbose_json` to use timestamp granularities. Either or both of these options are supported: `word`, or `segment`. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency. | No | ['segment'] |

### AzureErrorResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | object | The error details. | No |  |
| └─ code | string | The distinct, machine-generated identifier for the error. | No |  |
| └─ inner_error |  |  | No |  |
| └─ message | string | A human-readable message associated with the error. | No |  |
| └─ param | string | If applicable, the request input parameter associated with the error | No |  |
| └─ type | enum | The object type, always 'error.'<br>Possible values: `error` | No |  |

### AzureImage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_filter_results | [AzureContentFilterImageResponseResults](#azurecontentfilterimageresponseresults) | A content filter result for an image generation operation's output response content. | Yes |  |
| prompt_filter_results | [AzureContentFilterImagePromptResults](#azurecontentfilterimagepromptresults) | A content filter result for an image generation operation's input request content. | Yes |  |

### AzureImagesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created | integer | The Unix timestamp (in seconds) of when the image was created. | Yes |  |
| data | array |  | No |  |
| usage | object | For `gpt-image-1` only, the token usage information for the image generation. | No |  |
| └─ input_tokens | integer | The number of tokens (images and text) in the input prompt. | No |  |
| └─ input_tokens_details | object | The input tokens detailed information for the image generation. | No |  |
|   └─ image_tokens | integer | The number of image tokens in the input prompt. | No |  |
|   └─ text_tokens | integer | The number of text tokens in the input prompt. | No |  |
| └─ output_tokens | integer | The number of image tokens in the output image. | No |  |
| └─ total_tokens | integer | The total number of tokens (images and text) used for the image generation. | No |  |

### AzureOpenAIVideoGenerationErrorResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The distinct, machine-generated identifier for the error. | No |  |
| inner_error | object | If applicable, an upstream error that originated this error. | No |  |
| └─ code | enum | The code associated with the inner error.<br>Possible values: `ResponsibleAIPolicyViolation` | No |  |
| └─ error_details | object |  | No |  |
| └─ revised_prompt | string | If applicable, the modified prompt used for generation. | No |  |
| message | string | A human-readable message associated with the error. | No |  |
| param | string | If applicable, the request input parameter associated with the error | No |  |
| type | string | If applicable, the input line number associated with the error. | No |  |

### AzureResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean | Whether to run the model response in the background. | No | False |
| created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| error | object | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ code | [OpenAI.ResponseErrorCode](#openairesponseerrorcode) | The error code for the response. | No |  |
| └─ message | string | A human-readable description of the error. | No |  |
| id | string | Unique identifier for this Response. | Yes |  |
| incomplete_details | object | Details about why the response is incomplete. | Yes |  |
| └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| model | string | The model used to generate this response. | Yes |  |
| object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only** <br><br>Constrains effort on reasoning for <br>reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | Yes |  |
| text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. **nction calls (custom tools)**: Functions that are defined by you,  enabling the model to call your own code | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | Yes |  |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | Yes |  |

### AzureSearchChatDataSource

Represents a data source configuration that will use an Azure Search resource.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| parameters | object | The parameter information to control the use of the Azure Search data source. | Yes |  |
| └─ allow_partial_result | boolean | If set to true, the system will allow partial search results to be used and the request will fail if all<br>partial queries fail. If not specified or specified as false, the request will fail if any search query fails. | No | False |
| └─ authentication | object |  | No |  |
|   └─ access_token | string |  | No |  |
|   └─ key | string |  | No |  |
|   └─ managed_identity_resource_id | string |  | No |  |
|   └─ type | enum | <br>Possible values: `access_token` | No |  |
| └─ embedding_dependency | object | Represents a vectorization source that makes public service calls against an Azure OpenAI embedding model deployment. | No |  |
|   └─ authentication | [AzureChatDataSourceApiKeyAuthenticationOptions](#azurechatdatasourceapikeyauthenticationoptions) or [AzureChatDataSourceAccessTokenAuthenticationOptions](#azurechatdatasourceaccesstokenauthenticationoptions) | The authentication mechanism to use with the endpoint-based vectorization source.<br>Endpoint authentication supports API key and access token mechanisms. | No |  |
|   └─ deployment_name | string | The embedding model deployment to use for vectorization. This deployment must exist within the same Azure OpenAI<br>resource as the model deployment being used for chat completions. | No |  |
|   └─ dimensions | integer | The number of dimensions to request on embeddings.<br>Only supported in 'text-embedding-3' and later models. | No |  |
|   └─ endpoint | string | Specifies the resource endpoint URL from which embeddings should be retrieved.<br>It should be in the format of:<br>https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/embeddings.<br>The api-version query parameter is not allowed. | No |  |
|   └─ type | enum | The type identifier, always 'integrated' for this vectorization source type.<br>Possible values: `integrated` | No |  |
| └─ endpoint | string | The absolute endpoint path for the Azure Search resource to use. | No |  |
| └─ fields_mapping | object | The field mappings to use with the Azure Search resource. | No |  |
|   └─ content_fields | array | The names of index fields that should be treated as content. | No |  |
|   └─ content_fields_separator | string | The separator pattern that content fields should use. | No |  |
|   └─ filepath_field | string | The name of the index field to use as a filepath. | No |  |
|   └─ image_vector_fields | array | The names of fields that represent image vector data. | No |  |
|   └─ title_field | string | The name of the index field to use as a title. | No |  |
|   └─ url_field | string | The name of the index field to use as a URL. | No |  |
|   └─ vector_fields | array | The names of fields that represent vector data. | No |  |
| └─ filter | string | A filter to apply to the search. | No |  |
| └─ in_scope | boolean | Whether queries should be restricted to use of the indexed data. | No |  |
| └─ include_contexts | array | The output context properties to include on the response.<br>By default, citations and intent will be requested. | No | ['citations', 'intent'] |
| └─ index_name | string | The name of the index to use, as specified in the Azure Search resource. | No |  |
| └─ max_search_queries | integer | The maximum number of rewritten queries that should be sent to the search provider for a single user message.<br>By default, the system will make an automatic determination. | No |  |
| └─ query_type | enum | The query type for the Azure Search resource to use.<br>Possible values: `simple`, `semantic`, `vector`, `vector_simple_hybrid`, `vector_semantic_hybrid` | No |  |
| └─ semantic_configuration | string | Additional semantic configuration for the query. | No |  |
| └─ strictness | integer | The configured strictness of the search relevance filtering.<br>Higher strictness will increase precision but lower recall of the answer. | No |  |
| └─ top_n_documents | integer | The configured number of documents to feature in the query. | No |  |
| type | enum | The discriminated type identifier, which is always 'azure_search'.<br>Possible values: `azure_search` | Yes |  |

### AzureUserSecurityContext

User security context contains several parameters that describe the application itself, and the end user that interacts with the application. These fields assist your security operations teams to investigate and mitigate security incidents by providing a comprehensive approach to protecting your AI applications. [Learn more](https://aka.ms/TP4AI/Documentation/EndUserContext) about protecting AI applications using Microsoft Defender for Cloud.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| application_name | string | The name of the application. Sensitive personal information should not be included in this field. | No |  |
| end_user_id | string | This identifier is the Microsoft Entra ID (formerly Azure Active Directory) user object ID used to authenticate end-users within the generative AI application. Sensitive personal information should not be included in this field. | No |  |
| end_user_tenant_id | string | The Microsoft 365 tenant ID the end user belongs to. It's required when the generative AI application is multitenant. | No |  |
| source_ip | string | Captures the original client's IP address. | No |  |

### AzureVideoGenerationError

**Type**: object


### ChatCompletionMessageToolCallsItem

The tool calls generated by the model, such as function calls.

**Array of**: [OpenAI.ChatCompletionMessageToolCall](#openaichatcompletionmessagetoolcall)


### CompletionChoice

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_filter_results | [AzureContentFilterResultForChoice](#azurecontentfilterresultforchoice) | A content filter result for a single response item produced by a generative AI system. | No |  |
| finish_reason | enum | The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence,<br>`length` if the maximum number of tokens specified in the request was reached,<br>or `content_filter` if content was omitted due to a flag from our content filters.<br>Possible values: `stop`, `length`, `content_filter` | Yes |  |
| index | integer |  | Yes |  |
| logprobs | object |  | Yes |  |
| └─ text_offset | array |  | No |  |
| └─ token_logprobs | array |  | No |  |
| └─ tokens | array |  | No |  |
| └─ top_logprobs | array |  | No |  |
| text | string |  | Yes |  |

### CreateVideoGenerationRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| height | integer | The height of the video. The following dimensions are supported: 480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080. | Yes |  |
| model | string | The name of the deployment to use for this request. | Yes |  |
| n_seconds | integer | The duration of the video generation job. Must be between 1 and 20 seconds. | No | 5 |
| n_variants | integer | The number of videos to create as variants for this job. Must be between 1 and 5. Smaller dimensions allow more variants. | No | 1 |
| prompt | string | The prompt for this video generation job. | Yes |  |
| width | integer | The width of the video. The following dimensions are supported: 480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080. | Yes |  |

### ElasticsearchChatDataSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| parameters | object | The parameter information to control the use of the Elasticsearch data source. | Yes |  |
| └─ allow_partial_result | boolean | If set to true, the system will allow partial search results to be used and the request will fail if all<br>partial queries fail. If not specified or specified as false, the request will fail if any search query fails. | No | False |
| └─ authentication | object |  | No |  |
|   └─ encoded_api_key | string |  | No |  |
|   └─ key | string |  | No |  |
|   └─ key_id | string |  | No |  |
|   └─ type | enum | <br>Possible values: `encoded_api_key` | No |  |
| └─ embedding_dependency | [AzureChatDataSourceVectorizationSource](#azurechatdatasourcevectorizationsource) | A representation of a data vectorization source usable as an embedding resource with a data source. | No |  |
| └─ endpoint | string |  | No |  |
| └─ fields_mapping | object |  | No |  |
|   └─ content_fields | array |  | No |  |
|   └─ content_fields_separator | string |  | No |  |
|   └─ filepath_field | string |  | No |  |
|   └─ title_field | string |  | No |  |
|   └─ url_field | string |  | No |  |
|   └─ vector_fields | array |  | No |  |
| └─ in_scope | boolean | Whether queries should be restricted to use of the indexed data. | No |  |
| └─ include_contexts | array | The output context properties to include on the response.<br>By default, citations and intent will be requested. | No | ['citations', 'intent'] |
| └─ index_name | string |  | No |  |
| └─ max_search_queries | integer | The maximum number of rewritten queries that should be sent to the search provider for a single user message.<br>By default, the system will make an automatic determination. | No |  |
| └─ query_type | enum | <br>Possible values: `simple`, `vector` | No |  |
| └─ strictness | integer | The configured strictness of the search relevance filtering.<br>Higher strictness will increase precision but lower recall of the answer. | No |  |
| └─ top_n_documents | integer | The configured number of documents to feature in the query. | No |  |
| type | enum | The discriminated type identifier, which is always 'elasticsearch'.<br>Possible values: `elasticsearch` | Yes |  |

### JobStatus

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `preprocessing`<br>`queued`<br>`running`<br>`processing`<br>`cancelled`<br>`succeeded`<br>`failed` |

### MongoDBChatDataSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| parameters | object | The parameter information to control the use of the MongoDB data source. | Yes |  |
| └─ allow_partial_result | boolean | If set to true, the system will allow partial search results to be used and the request will fail if all<br>partial queries fail. If not specified or specified as false, the request will fail if any search query fails. | No | False |
| └─ app_name | string | The name of the MongoDB application. | No |  |
| └─ authentication | object |  | No |  |
|   └─ password | string |  | No |  |
|   └─ type | enum | <br>Possible values: `username_and_password` | No |  |
|   └─ username | string |  | No |  |
| └─ collection_name | string | The name of the MongoDB collection. | No |  |
| └─ database_name | string | The name of the MongoDB database. | No |  |
| └─ embedding_dependency | object | Represents a vectorization source that makes public service calls against an Azure OpenAI embedding model deployment. | No |  |
|   └─ authentication | [AzureChatDataSourceApiKeyAuthenticationOptions](#azurechatdatasourceapikeyauthenticationoptions) or [AzureChatDataSourceAccessTokenAuthenticationOptions](#azurechatdatasourceaccesstokenauthenticationoptions) | The authentication mechanism to use with the endpoint-based vectorization source.<br>Endpoint authentication supports API key and access token mechanisms. | No |  |
|   └─ deployment_name | string | The embedding model deployment to use for vectorization. This deployment must exist within the same Azure OpenAI<br>resource as the model deployment being used for chat completions. | No |  |
|   └─ dimensions | integer | The number of dimensions to request on embeddings.<br>Only supported in 'text-embedding-3' and later models. | No |  |
|   └─ endpoint | string | Specifies the resource endpoint URL from which embeddings should be retrieved.<br>It should be in the format of:<br>https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT_NAME/embeddings.<br>The api-version query parameter is not allowed. | No |  |
|   └─ type | enum | The type identifier, always 'deployment_name' for this vectorization source type.<br>Possible values: `deployment_name` | No |  |
| └─ endpoint | string | The name of the MongoDB cluster endpoint. | No |  |
| └─ fields_mapping | object | Field mappings to apply to data used by the MongoDB data source.<br>Note that content and vector field mappings are required for MongoDB. | No |  |
|   └─ content_fields | array |  | No |  |
|   └─ content_fields_separator | string |  | No |  |
|   └─ filepath_field | string |  | No |  |
|   └─ title_field | string |  | No |  |
|   └─ url_field | string |  | No |  |
|   └─ vector_fields | array |  | No |  |
| └─ in_scope | boolean | Whether queries should be restricted to use of the indexed data. | No |  |
| └─ include_contexts | array | The output context properties to include on the response.<br>By default, citations and intent will be requested. | No | ['citations', 'intent'] |
| └─ index_name | string | The name of the MongoDB index. | No |  |
| └─ max_search_queries | integer | The maximum number of rewritten queries that should be sent to the search provider for a single user message.<br>By default, the system will make an automatic determination. | No |  |
| └─ strictness | integer | The configured strictness of the search relevance filtering.<br>Higher strictness will increase precision but lower recall of the answer. | No |  |
| └─ top_n_documents | integer | The configured number of documents to feature in the query. | No |  |
| type | enum | The discriminated type identifier, which is always 'mongo_db'.<br>Possible values: `mongo_db` | Yes |  |

### OpenAI.Annotation


### Discriminator for OpenAI.Annotation

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `file_citation` | [OpenAI.AnnotationFileCitation](#openaiannotationfilecitation) |
| `url_citation` | [OpenAI.AnnotationUrlCitation](#openaiannotationurlcitation) |
| `file_path` | [OpenAI.AnnotationFilePath](#openaiannotationfilepath) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.AnnotationType](#openaiannotationtype) |  | Yes |  |

### OpenAI.AnnotationFileCitation

A citation to a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The ID of the file. | Yes |  |
| index | integer | The index of the file in the list of files. | Yes |  |
| type | enum | The type of the file citation. Always `file_citation`.<br>Possible values: `file_citation` | Yes |  |

### OpenAI.AnnotationFilePath

A path to a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string | The ID of the file. | Yes |  |
| index | integer | The index of the file in the list of files. | Yes |  |
| type | enum | The type of the file path. Always `file_path`.<br>Possible values: `file_path` | Yes |  |

### OpenAI.AnnotationType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `file_citation`<br>`url_citation`<br>`file_path` |

### OpenAI.AnnotationUrlCitation

A citation for a web resource used to generate a model response.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end_index | integer | The index of the last character of the URL citation in the message. | Yes |  |
| start_index | integer | The index of the first character of the URL citation in the message. | Yes |  |
| title | string | The title of the web resource. | Yes |  |
| type | enum | The type of the URL citation. Always `url_citation`.<br>Possible values: `url_citation` | Yes |  |
| url | string | The URL of the web resource. | Yes |  |

### OpenAI.ApproximateLocation

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| city | string |  | No |  |
| country | string |  | No |  |
| region | string |  | No |  |
| timezone | string |  | No |  |
| type | enum | <br>Possible values: `approximate` | Yes |  |

### OpenAI.AudioResponseFormat

The format of the output, in one of these options: `json`, `text`, `srt`, `verbose_json`, or `vtt`. For `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`, the only supported format is `json`.

| Property | Value |
|----------|-------|
| **Description** | The format of the output, in one of these options: `json`, `text`, `srt`, `verbose_json`, or `vtt`. For `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`, the only supported format is `json`. |
| **Type** | string |
| **Values** | `json`<br>`text`<br>`srt`<br>`verbose_json`<br>`vtt` |

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
| parameters |  | The parameters the functions accepts, described as a JSON Schema object.<br>See the [JSON Schema reference](https://json-schema.org/understanding-json-schema/)<br>for documentation about the format.<br><br>Omitting `parameters` defines a function with an empty parameter list. | No |  |

### OpenAI.ChatCompletionMessageAudioChunk

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string |  | No |  |
| expires_at | integer |  | No |  |
| id | string |  | No |  |
| transcript | string |  | No |  |

### OpenAI.ChatCompletionMessageToolCall

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | object | The function that the model called. | Yes |  |
| └─ arguments | string | The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function. | No |  |
| └─ name | string | The name of the function to call. | No |  |
| id | string | The ID of the tool call. | Yes |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatCompletionMessageToolCallChunk

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | object |  | No |  |
| └─ arguments | string | The arguments to call the function with, as generated by the model in JSON format. Note that the model does not always generate valid JSON, and may hallucinate parameters not defined by your function schema. Validate the arguments in your code before calling your function. | No |  |
| └─ name | string | The name of the function to call. | No |  |
| id | string | The ID of the tool call. | No |  |
| index | integer |  | Yes |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | No |  |

### OpenAI.ChatCompletionNamedToolChoice

Specifies a tool the model should use. Use to force the model to call a specific function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | object |  | Yes |  |
| └─ name | string | The name of the function to call. | No |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatCompletionRequestAssistantMessage

Messages sent by the model in response to user messages.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | object | Data about a previous audio response from the model. | No |  |
| └─ id | string | Unique identifier for a previous audio response from the model. | No |  |
| content | string or array |  | No |  |
| function_call | object | Deprecated and replaced by `tool_calls`. The name and arguments of a function that should be called, as generated by the model. | No |  |
| └─ arguments | string |  | No |  |
| └─ name | string |  | No |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| refusal | string | The refusal message by the assistant. | No |  |
| role | enum | The role of the messages author, in this case `assistant`.<br>Possible values: `assistant` | Yes |  |
| tool_calls | [ChatCompletionMessageToolCallsItem](#chatcompletionmessagetoolcallsitem) | The tool calls generated by the model, such as function calls. | No |  |

### OpenAI.ChatCompletionRequestAssistantMessageContentPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal message generated by the model. | Yes |  |
| text | string | The text content. | Yes |  |
| type | enum | The type of the content part.<br>Possible values: `refusal` | Yes |  |

### OpenAI.ChatCompletionRequestDeveloperMessage

Developer-provided instructions that the model should follow, regardless of
messages sent by the user. With o1 models and newer, `developer` messages
replace the previous `system` messages.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array |  | Yes |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| role | enum | The role of the messages author, in this case `developer`.<br>Possible values: `developer` | Yes |  |

### OpenAI.ChatCompletionRequestFunctionMessage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string | The contents of the function message. | Yes |  |
| name | string | The name of the function to call. | Yes |  |
| role | enum | The role of the messages author, in this case `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatCompletionRequestMessage


### Discriminator for OpenAI.ChatCompletionRequestMessage

This component uses the property `role` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `system` | [OpenAI.ChatCompletionRequestSystemMessage](#openaichatcompletionrequestsystemmessage) |
| `developer` | [OpenAI.ChatCompletionRequestDeveloperMessage](#openaichatcompletionrequestdevelopermessage) |
| `user` | [OpenAI.ChatCompletionRequestUserMessage](#openaichatcompletionrequestusermessage) |
| `assistant` | [OpenAI.ChatCompletionRequestAssistantMessage](#openaichatcompletionrequestassistantmessage) |
| `tool` | [OpenAI.ChatCompletionRequestToolMessage](#openaichatcompletionrequesttoolmessage) |
| `function` | [OpenAI.ChatCompletionRequestFunctionMessage](#openaichatcompletionrequestfunctionmessage) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array |  | No |  |
| role | object | The role of the author of a message | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPart


### Discriminator for OpenAI.ChatCompletionRequestMessageContentPart

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `text` | [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext) |
| `image_url` | [OpenAI.ChatCompletionRequestMessageContentPartImage](#openaichatcompletionrequestmessagecontentpartimage) |
| `refusal` | [OpenAI.ChatCompletionRequestMessageContentPartRefusal](#openaichatcompletionrequestmessagecontentpartrefusal) |
| `file` | [OpenAI.ChatCompletionRequestMessageContentPartFile](#openaichatcompletionrequestmessagecontentpartfile) |
| `input_audio` | [OpenAI.ChatCompletionRequestMessageContentPartAudio](#openaichatcompletionrequestmessagecontentpartaudio) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ChatCompletionRequestMessageContentPartType](#openaichatcompletionrequestmessagecontentparttype) |  | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartAudio

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_audio | object |  | Yes |  |
| └─ data | string | Base64 encoded audio data. | No |  |
| └─ format | enum | The format of the encoded audio data. Currently supports "wav" and "mp3".<br>Possible values: `wav`, `mp3` | No |  |
| type | enum | The type of the content part. Always `input_audio`.<br>Possible values: `input_audio` | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartFile



| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file | object |  | Yes |  |
| └─ file_data | string | The base64 encoded file data, used when passing the file to the model<br>as a string. | No |  |
| └─ file_id | string | The ID of an uploaded file to use as input. | No |  |
| └─ filename | string | The name of the file, used when passing the file to the model as a<br>string. | No |  |
| type | enum | The type of the content part. Always `file`.<br>Possible values: `file` | Yes |  |

### OpenAI.ChatCompletionRequestMessageContentPartImage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| image_url | object |  | Yes |  |
| └─ detail | enum | Specifies the detail level of the image. .<br>Possible values: `auto`, `low`, `high` | No |  |
| └─ url | string | Either a URL of the image or the base64 encoded image data. | No |  |
| type | enum | The type of the content part.<br>Possible values: `image_url` | Yes |  |

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

### OpenAI.ChatCompletionRequestMessageContentPartType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `text`<br>`file`<br>`input_audio`<br>`image_url`<br>`refusal` |

### OpenAI.ChatCompletionRequestSystemMessage

Developer-provided instructions that the model should follow, regardless of
messages sent by the user. With o1 models and newer, use `developer` messages
for this purpose instead.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array |  | Yes |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| role | enum | The role of the messages author, in this case `system`.<br>Possible values: `system` | Yes |  |

### OpenAI.ChatCompletionRequestSystemMessageContentPart

References: [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext)

### OpenAI.ChatCompletionRequestToolMessage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array |  | Yes |  |
| role | enum | The role of the messages author, in this case `tool`.<br>Possible values: `tool` | Yes |  |
| tool_call_id | string | Tool call that this message is responding to. | Yes |  |

### OpenAI.ChatCompletionRequestToolMessageContentPart

References: [OpenAI.ChatCompletionRequestMessageContentPartText](#openaichatcompletionrequestmessagecontentparttext)

### OpenAI.ChatCompletionRequestUserMessage

Messages sent by an end user, containing prompts or additional context
information.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array |  | Yes |  |
| name | string | An optional name for the participant. Provides the model information to differentiate between participants of the same role. | No |  |
| role | enum | The role of the messages author, in this case `user`.<br>Possible values: `user` | Yes |  |

### OpenAI.ChatCompletionRequestUserMessageContentPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file | object |  | Yes |  |
| └─ file_data | string | The base64 encoded file data, used when passing the file to the model<br>as a string. | No |  |
| └─ file_id | string | The ID of an uploaded file to use as input. | No |  |
| └─ filename | string | The name of the file, used when passing the file to the model as a<br>string. | No |  |
| image_url | object |  | Yes |  |
| └─ detail | enum | Specifies the detail level of the image. .<br>Possible values: `auto`, `low`, `high` | No |  |
| └─ url | string | Either a URL of the image or the base64 encoded image data. | No |  |
| input_audio | object |  | Yes |  |
| └─ data | string | Base64 encoded audio data. | No |  |
| └─ format | enum | The format of the encoded audio data. Currently supports "wav" and "mp3".<br>Possible values: `wav`, `mp3` | No |  |
| text | string | The text content. | Yes |  |
| type | enum | The type of the content part. Always `file`.<br>Possible values: `file` | Yes |  |

### OpenAI.ChatCompletionRole

The role of the author of a message

| Property | Value |
|----------|-------|
| **Description** | The role of the author of a message |
| **Type** | string |
| **Values** | `system`<br>`developer`<br>`user`<br>`assistant`<br>`tool`<br>`function` |

### OpenAI.ChatCompletionStreamOptions

Options for streaming response. Only set this when you set `stream: true`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array. <br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |

### OpenAI.ChatCompletionStreamResponseDelta

A chat completion delta generated by streamed model responses.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| audio | object |  | No |  |
| └─ data | string |  | No |  |
| └─ expires_at | integer |  | No |  |
| └─ id | string |  | No |  |
| └─ transcript | string |  | No |  |
| content | string | The contents of the chunk message. | No |  |
| function_call | object | Deprecated and replaced by `tool_calls`. The name and arguments of a function that should be called, as generated by the model. | No |  |
| └─ arguments | string |  | No |  |
| └─ name | string |  | No |  |
| refusal | string | The refusal message generated by the model. | No |  |
| role | object | The role of the author of a message | No |  |
| tool_calls | array |  | No |  |

### OpenAI.ChatCompletionTokenLogprob

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array | A list of integers representing the UTF-8 bytes representation of the token. Useful in instances where characters are represented by multiple tokens and their byte representations must be combined to generate the correct text representation. Can be `null` if there is no bytes representation for the token. | Yes |  |
| logprob | number | The log probability of this token, if it is within the top 20 most likely tokens. Otherwise, the value `-9999.0` is used to signify that the token is very unlikely. | Yes |  |
| token | string | The token. | Yes |  |
| top_logprobs | array | List of the most likely tokens and their log probability, at this token position. In rare cases, there may be fewer than the number of requested `top_logprobs` returned. | Yes |  |

### OpenAI.ChatCompletionTool

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

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| function | object |  | Yes |  |
| └─ name | string | The name of the function to call. | No |  |
| type | enum | The type of the tool. Currently, only `function` is supported.<br>Possible values: `function` | Yes |  |

### OpenAI.ChatOutputPrediction

Base representation of predicted output from a model.


### Discriminator for OpenAI.ChatOutputPrediction

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `content` | [OpenAI.ChatOutputPredictionContent](#openaichatoutputpredictioncontent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ChatOutputPredictionType](#openaichatoutputpredictiontype) |  | Yes |  |

### OpenAI.ChatOutputPredictionContent

Static predicted output content, such as the content of a text file that is
being regenerated.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array |  | Yes |  |
| type | enum | The type of the predicted content you want to provide. This type is<br>currently always `content`.<br>Possible values: `content` | Yes |  |

### OpenAI.ChatOutputPredictionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `content` |

### OpenAI.CodeInterpreterFileOutput

The output of a code interpreter tool call that is a file.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| files | array |  | Yes |  |
| type | enum | The type of the code interpreter file output. Always `files`.<br>Possible values: `files` | Yes |  |

### OpenAI.CodeInterpreterTextOutput

The output of a code interpreter tool call that is text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logs | string | The logs of the code interpreter tool call. | Yes |  |
| type | enum | The type of the code interpreter text output. Always `logs`.<br>Possible values: `logs` | Yes |  |

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

### OpenAI.CodeInterpreterToolCallItemParam

A tool call to run code.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The code to run. | Yes |  |
| container_id | string | The ID of the container used to run the code. | No |  |
| results | array | The results of the code interpreter tool call. | Yes |  |
| type | enum | <br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.CodeInterpreterToolCallItemResource

A tool call to run code.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The code to run. | Yes |  |
| container_id | string | The ID of the container used to run the code. | No |  |
| results | array | The results of the code interpreter tool call. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `interpreting`, `completed` | Yes |  |
| type | enum | <br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.CodeInterpreterToolOutput

The output of a code interpreter tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| files | array |  | Yes |  |
| logs | string | The logs of the code interpreter tool call. | Yes |  |
| type | enum | The type of the code interpreter file output. Always `files`.<br>Possible values: `files` | Yes |  |

### OpenAI.ComparisonFilter

A filter used to compare a specified attribute key to a given value using a defined comparison operation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| key | string | The key to compare against the value. | Yes |  |
| type | enum | Specifies the comparison operator: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`.<br>- `eq`: equals<br>- `ne`: not equal<br>- `gt`: greater than<br>- `gte`: greater than or equal<br>- `lt`: less than<br>- `lte`: less than or equal<br>Possible values: `eq`, `ne`, `gt`, `gte`, `lt`, `lte` | Yes |  |
| value | string or number or boolean |  | Yes |  |

### OpenAI.CompletionUsage

Usage statistics for the completion request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| completion_tokens | integer | Number of tokens in the generated completion. | Yes | 0 |
| completion_tokens_details | object | Breakdown of tokens used in a completion. | No |  |
| └─ accepted_prediction_tokens | integer | When using Predicted Outputs, the number of tokens in the<br>prediction that appeared in the completion. | No | 0 |
| └─ audio_tokens | integer | Audio input tokens generated by the model. | No | 0 |
| └─ reasoning_tokens | integer | Tokens generated by the model for reasoning. | No | 0 |
| └─ rejected_prediction_tokens | integer | When using Predicted Outputs, the number of tokens in the<br>prediction that did not appear in the completion. However, like<br>reasoning tokens, these tokens are still counted in the total<br>completion tokens for purposes of billing, output, and context window<br>limits. | No | 0 |
| prompt_tokens | integer | Number of tokens in the prompt. | Yes | 0 |
| prompt_tokens_details | object | Breakdown of tokens used in the prompt. | No |  |
| └─ audio_tokens | integer | Audio input tokens present in the prompt. | No | 0 |
| └─ cached_tokens | integer | Cached tokens present in the prompt. | No | 0 |
| total_tokens | integer | Total number of tokens used in the request (prompt + completion). | Yes | 0 |

### OpenAI.CompoundFilter

Combine multiple filters using `and` or `or`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | array | Array of filters to combine. Items can be `ComparisonFilter` or `CompoundFilter`. | Yes |  |
| type | enum | Type of operation: `and` or `or`.<br>Possible values: `and`, `or` | Yes |  |

### OpenAI.ComputerAction


### Discriminator for OpenAI.ComputerAction

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `click` | [OpenAI.ComputerActionClick](#openaicomputeractionclick) |
| `double_click` | [OpenAI.ComputerActionDoubleClick](#openaicomputeractiondoubleclick) |
| `drag` | [OpenAI.ComputerActionDrag](#openaicomputeractiondrag) |
| `move` | [OpenAI.ComputerActionMove](#openaicomputeractionmove) |
| `screenshot` | [OpenAI.ComputerActionScreenshot](#openaicomputeractionscreenshot) |
| `scroll` | [OpenAI.ComputerActionScroll](#openaicomputeractionscroll) |
| `type` | [OpenAI.ComputerActionTypeKeys](#openaicomputeractiontypekeys) |
| `wait` | [OpenAI.ComputerActionWait](#openaicomputeractionwait) |
| `keypress` | [OpenAI.ComputerActionKeyPress](#openaicomputeractionkeypress) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ComputerActionType](#openaicomputeractiontype) |  | Yes |  |

### OpenAI.ComputerActionClick

A click action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| button | enum | Indicates which mouse button was pressed during the click. One of `left`, `right`, `wheel`, `back`, or `forward`.<br>Possible values: `left`, `right`, `wheel`, `back`, `forward` | Yes |  |
| type | enum | Specifies the event type. For a click action, this property is <br>always set to `click`.<br>Possible values: `click` | Yes |  |
| x | integer | The x-coordinate where the click occurred. | Yes |  |
| y | integer | The y-coordinate where the click occurred. | Yes |  |

### OpenAI.ComputerActionDoubleClick

A double click action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a double click action, this property is <br>always set to `double_click`.<br>Possible values: `double_click` | Yes |  |
| x | integer | The x-coordinate where the double click occurred. | Yes |  |
| y | integer | The y-coordinate where the double click occurred. | Yes |  |

### OpenAI.ComputerActionDrag

A drag action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| path | array | An array of coordinates representing the path of the drag action. Coordinates will appear as an array<br>of objects, eg<br>```<br>[<br>  { x: 100, y: 200 },<br>  { x: 200, y: 300 }<br>]<br>``` | Yes |  |
| type | enum | Specifies the event type. For a drag action, this property is <br>always set to `drag`.<br>Possible values: `drag` | Yes |  |

### OpenAI.ComputerActionKeyPress

A collection of keypresses the model would like to perform.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| keys | array | The combination of keys the model is requesting to be pressed. This is an<br>array of strings, each representing a key. | Yes |  |
| type | enum | Specifies the event type. For a keypress action, this property is <br>always set to `keypress`.<br>Possible values: `keypress` | Yes |  |

### OpenAI.ComputerActionMove

A mouse move action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a move action, this property is <br>always set to `move`.<br>Possible values: `move` | Yes |  |
| x | integer | The x-coordinate to move to. | Yes |  |
| y | integer | The y-coordinate to move to. | Yes |  |

### OpenAI.ComputerActionScreenshot

A screenshot action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a screenshot action, this property is <br>always set to `screenshot`.<br>Possible values: `screenshot` | Yes |  |

### OpenAI.ComputerActionScroll

A scroll action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| scroll_x | integer | The horizontal scroll distance. | Yes |  |
| scroll_y | integer | The vertical scroll distance. | Yes |  |
| type | enum | Specifies the event type. For a scroll action, this property is <br>always set to `scroll`.<br>Possible values: `scroll` | Yes |  |
| x | integer | The x-coordinate where the scroll occurred. | Yes |  |
| y | integer | The y-coordinate where the scroll occurred. | Yes |  |

### OpenAI.ComputerActionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `screenshot`<br>`click`<br>`double_click`<br>`scroll`<br>`type`<br>`wait`<br>`keypress`<br>`drag`<br>`move` |

### OpenAI.ComputerActionTypeKeys

An action to type in text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text to type. | Yes |  |
| type | enum | Specifies the event type. For a type action, this property is <br>always set to `type`.<br>Possible values: `type` | Yes |  |

### OpenAI.ComputerActionWait

A wait action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a wait action, this property is <br>always set to `wait`.<br>Possible values: `wait` | Yes |  |

### OpenAI.ComputerToolCallItemParam

A tool call to a computer use tool. 


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| pending_safety_checks | array | The pending safety checks for the computer call. | Yes |  |
| type | enum | <br>Possible values: `computer_call` | Yes |  |

### OpenAI.ComputerToolCallItemResource

A tool call to a computer use tool. 


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.ComputerAction](#openaicomputeraction) |  | Yes |  |
| call_id | string | An identifier used when responding to the tool call with output. | Yes |  |
| pending_safety_checks | array | The pending safety checks for the computer call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>`incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | <br>Possible values: `computer_call` | Yes |  |

### OpenAI.ComputerToolCallOutputItemOutput


### Discriminator for OpenAI.ComputerToolCallOutputItemOutput

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `computer_screenshot` | [OpenAI.ComputerToolCallOutputItemOutputComputerScreenshot](#openaicomputertoolcalloutputitemoutputcomputerscreenshot) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ComputerToolCallOutputItemOutputType](#openaicomputertoolcalloutputitemoutputtype) | A computer screenshot image used with the computer use tool. | Yes |  |

### OpenAI.ComputerToolCallOutputItemOutputComputerScreenshot

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_id | string |  | No |  |
| image_url | string |  | No |  |
| type | enum | <br>Possible values: `computer_screenshot` | Yes |  |

### OpenAI.ComputerToolCallOutputItemOutputType

A computer screenshot image used with the computer use tool.

| Property | Value |
|----------|-------|
| **Description** | A computer screenshot image used with the computer use tool. |
| **Type** | string |
| **Values** | `computer_screenshot` |

### OpenAI.ComputerToolCallOutputItemParam

The output of a computer tool call.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array | The safety checks reported by the API that have been acknowledged by the<br>developer. | No |  |
| call_id | string | The ID of the computer tool call that produced the output. | Yes |  |
| output | [OpenAI.ComputerToolCallOutputItemOutput](#openaicomputertoolcalloutputitemoutput) |  | Yes |  |
| type | enum | <br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.ComputerToolCallOutputItemResource

The output of a computer tool call.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| acknowledged_safety_checks | array | The safety checks reported by the API that have been acknowledged by the<br>developer. | No |  |
| call_id | string | The ID of the computer tool call that produced the output. | Yes |  |
| output | [OpenAI.ComputerToolCallOutputItemOutput](#openaicomputertoolcalloutputitemoutput) |  | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>`incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | <br>Possible values: `computer_call_output` | Yes |  |

### OpenAI.ComputerToolCallSafetyCheck

A pending safety check for the computer call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The type of the pending safety check. | Yes |  |
| id | string | The ID of the pending safety check. | Yes |  |
| message | string | Details about the pending safety check. | Yes |  |

### OpenAI.ComputerUsePreviewTool

A tool that controls a virtual computer. 

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| display_height | integer | The height of the computer display. | Yes |  |
| display_width | integer | The width of the computer display. | Yes |  |
| environment | enum | The type of computer environment to control.<br>Possible values: `windows`, `mac`, `linux`, `ubuntu`, `browser` | Yes |  |
| type | enum | The type of the computer use tool. Always `computer_use_preview`.<br>Possible values: `computer_use_preview` | Yes |  |

### OpenAI.Coordinate

An x/y coordinate pair, e.g. `{ x: 100, y: 200 }`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| x | integer | The x-coordinate. | Yes |  |
| y | integer | The y-coordinate. | Yes |  |

### OpenAI.CreateEmbeddingResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of embeddings generated by the model. | Yes |  |
| model | string | The name of the model used to generate the embedding. | Yes |  |
| object | enum | The object type, which is always "list".<br>Possible values: `list` | Yes |  |
| usage | object | The usage information for the request. | Yes |  |
| └─ prompt_tokens | integer | The number of tokens used by the prompt. | No |  |
| └─ total_tokens | integer | The total number of tokens used by the request. | No |  |

### OpenAI.Embedding

Represents an embedding vector returned by embedding endpoint.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| embedding | array or string |  | Yes |  |
| index | integer | The index of the embedding in the list of embeddings. | Yes |  |
| object | enum | The object type, which is always "embedding".<br>Possible values: `embedding` | Yes |  |

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

### OpenAI.FileSearchToolCallItemParam

The results of a file search tool call. 


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| queries | array | The queries used to search for files. | Yes |  |
| results | array | The results of the file search tool call. | No |  |
| type | enum | <br>Possible values: `file_search_call` | Yes |  |

### OpenAI.FileSearchToolCallItemResource

The results of a file search tool call. 


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| queries | array | The queries used to search for files. | Yes |  |
| results | array | The results of the file search tool call. | No |  |
| status | enum | The status of the file search tool call. One of `in_progress`, <br>`searching`, `incomplete` or `failed`,<br>Possible values: `in_progress`, `searching`, `completed`, `incomplete`, `failed` | Yes |  |
| type | enum | <br>Possible values: `file_search_call` | Yes |  |

### OpenAI.Filters

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filters | array | Array of filters to combine. Items can be `ComparisonFilter` or `CompoundFilter`. | Yes |  |
| key | string | The key to compare against the value. | Yes |  |
| type | enum | Type of operation: `and` or `or`.<br>Possible values: `and`, `or` | Yes |  |
| value | string or number or boolean | The value to compare against the attribute key; supports string, number, or boolean types. | Yes |  |

### OpenAI.FunctionObject

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of what the function does, used by the model to choose when and how to call the function. | No |  |
| name | string | The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64. | Yes |  |
| parameters |  | The parameters the functions accepts, described as a JSON Schema object.  | No |  |
| strict | boolean | Whether to enable strict schema adherence when generating the function call. If set to true, the model will follow the exact schema defined in the `parameters` field. Only a subset of JSON Schema is supported when `strict` is `true`.  | No | False |

### OpenAI.FunctionTool

Defines a function in your own code the model can choose to call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| description | string | A description of the function. Used by the model to determine whether or not to call the function. | No |  |
| name | string | The name of the function to call. | Yes |  |
| parameters |  | A JSON schema object describing the parameters of the function. | Yes |  |
| strict | boolean | Whether to enforce strict parameter validation. Default `true`. | Yes |  |
| type | enum | The type of the function tool. Always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.FunctionToolCallItemParam

A tool call to run a function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| name | string | The name of the function to run. | Yes |  |
| type | enum | <br>Possible values: `function_call` | Yes |  |

### OpenAI.FunctionToolCallItemResource

A tool call to run a function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments to pass to the function. | Yes |  |
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| name | string | The name of the function to run. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>`incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | <br>Possible values: `function_call` | Yes |  |

### OpenAI.FunctionToolCallOutputItemParam

The output of a function tool call.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the function tool call. | Yes |  |
| type | enum | <br>Possible values: `function_call_output` | Yes |  |

### OpenAI.FunctionToolCallOutputItemResource

The output of a function tool call.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| call_id | string | The unique ID of the function tool call generated by the model. | Yes |  |
| output | string | A JSON string of the output of the function tool call. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>`incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | <br>Possible values: `function_call_output` | Yes |  |

### OpenAI.ImageGenTool

A tool that generates images using a model like `gpt-image-1`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Background type for the generated image. One of `transparent`, <br>`opaque`, or `auto`. Default: `auto`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| input_image_mask | object | Optional mask for inpainting. Contains `image_url` <br>(string, optional) and `file_id` (string, optional). | No |  |
| └─ file_id | string | File ID for the mask image. | No |  |
| └─ image_url | string | Base64-encoded mask image. | No |  |
| model | enum | The image generation model to use. Default: `gpt-image-1`.<br>Possible values: `gpt-image-1` | No |  |
| moderation | enum | Moderation level for the generated image. Default: `auto`.<br>Possible values: `auto`, `low` | No |  |
| output_compression | integer | Compression level for the output image. Default: 100. | No | 100 |
| output_format | enum | The output format of the generated image. One of `png`, `webp`, or <br>`jpeg`. Default: `png`.<br>Possible values: `png`, `webp`, `jpeg` | No |  |
| partial_images | integer | Number of partial images to generate in streaming mode, from 0 (default value) to 3. | No | 0 |
| quality | enum | The quality of the generated image. One of `low`, `medium`, `high`, <br>or `auto`. Default: `auto`.<br>Possible values: `low`, `medium`, `high`, `auto` | No |  |
| size | enum | The size of the generated image. One of `1024x1024`, `1024x1536`, <br>`1536x1024`, or `auto`. Default: `auto`.<br>Possible values: `1024x1024`, `1024x1536`, `1536x1024`, `auto` | No |  |
| type | enum | The type of the image generation tool. Always `image_generation`.<br>Possible values: `image_generation` | Yes |  |

### OpenAI.ImageGenToolCallItemParam

An image generation request made by the model.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| result | string | The generated image encoded in base64. | Yes |  |
| type | enum | <br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.ImageGenToolCallItemResource

An image generation request made by the model.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| result | string | The generated image encoded in base64. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `generating`, `failed` | Yes |  |
| type | enum | <br>Possible values: `image_generation_call` | Yes |  |

### OpenAI.ImplicitUserMessage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | string or array |  | Yes |  |

### OpenAI.Includable

Specify additional output data to include in the model response. Currently
supported values are:
- `file_search_call.results`: Include the search results of
  the file search tool call.
- `message.input_image.image_url`: Include image urls from the input message.
- `computer_call_output.output.image_url`: Include image urls from the computer call output.
- `reasoning.encrypted_content`: Includes an encrypted version of reasoning 
  tokens in reasoning item outputs. This enables reasoning items to be used in
  multi-turn conversations when using the Responses API statelessly (like
  when the `store` parameter is set to `false`, or when an organization is
  enrolled in the zero data retention program).

| Property | Value |
|----------|-------|
| **Description** | Specify additional output data to include in the model response. Currently<br>supported values are:<br>- `file_search_call.results`: Include the search results of<br>  the file search tool call.<br>- `message.input_image.image_url`: Include image urls from the input message.<br>- `computer_call_output.output.image_url`: Include image urls from the computer call output.<br>- `reasoning.encrypted_content`: Includes an encrypted version of reasoning <br>  tokens in reasoning item outputs. This enables reasoning items to be used in<br>  multi-turn conversations when using the Responses API statelessly (like<br>  when the `store` parameter is set to `false`, or when an organization is<br>  enrolled in the zero data retention program). |
| **Type** | string |
| **Values** | `file_search_call.results`<br>`message.input_image.image_url`<br>`computer_call_output.output.image_url`<br>`reasoning.encrypted_content` |

### OpenAI.ItemContent


### Discriminator for OpenAI.ItemContent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `input_audio` | [OpenAI.ItemContentInputAudio](#openaiitemcontentinputaudio) |
| `output_audio` | [OpenAI.ItemContentOutputAudio](#openaiitemcontentoutputaudio) |
| `refusal` | [OpenAI.ItemContentRefusal](#openaiitemcontentrefusal) |
| `input_text` | [OpenAI.ItemContentInputText](#openaiitemcontentinputtext) |
| `input_image` | [OpenAI.ItemContentInputImage](#openaiitemcontentinputimage) |
| `input_file` | [OpenAI.ItemContentInputFile](#openaiitemcontentinputfile) |
| `output_text` | [OpenAI.ItemContentOutputText](#openaiitemcontentoutputtext) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ItemContentType](#openaiitemcontenttype) | Multi-modal input and output contents. | Yes |  |

### OpenAI.ItemContentInputAudio

An audio input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string | Base64-encoded audio data. | Yes |  |
| format | enum | The format of the audio data. Currently supported formats are `mp3` and<br>`wav`.<br>Possible values: `mp3`, `wav` | Yes |  |
| type | enum | The type of the input item. Always `input_audio`.<br>Possible values: `input_audio` | Yes |  |

### OpenAI.ItemContentInputFile

A file input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file_data | string | The content of the file to be sent to the model. | No |  |
| file_id | string | The ID of the file to be sent to the model. | No |  |
| filename | string | The name of the file to be sent to the model. | No |  |
| type | enum | The type of the input item. Always `input_file`.<br>Possible values: `input_file` | Yes |  |

### OpenAI.ItemContentInputImage

An image input to the model. 

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detail | enum | The detail level of the image to be sent to the model. One of `high`, `low`, or `auto`. Defaults to `auto`.<br>Possible values: `low`, `high`, `auto` | No |  |
| file_id | string | The ID of the file to be sent to the model. | No |  |
| image_url | string | The URL of the image to be sent to the model. A fully qualified URL or base64 encoded image in a data URL. | No |  |
| type | enum | The type of the input item. Always `input_image`.<br>Possible values: `input_image` | Yes |  |

### OpenAI.ItemContentInputText

A text input to the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string | The text input to the model. | Yes |  |
| type | enum | The type of the input item. Always `input_text`.<br>Possible values: `input_text` | Yes |  |

### OpenAI.ItemContentOutputAudio

An audio output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | string | Base64-encoded audio data from the model. | Yes |  |
| transcript | string | The transcript of the audio data from the model. | Yes |  |
| type | enum | The type of the output audio. Always `output_audio`.<br>Possible values: `output_audio` | Yes |  |

### OpenAI.ItemContentOutputText

A text output from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array | The annotations of the text output. | Yes |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.ItemContentRefusal

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanation from the model. | Yes |  |
| type | enum | The type of the refusal. Always `refusal`.<br>Possible values: `refusal` | Yes |  |

### OpenAI.ItemContentType

Multi-modal input and output contents.

| Property | Value |
|----------|-------|
| **Description** | Multi-modal input and output contents. |
| **Type** | string |
| **Values** | `input_text`<br>`input_audio`<br>`input_image`<br>`input_file`<br>`output_text`<br>`output_audio`<br>`refusal` |

### OpenAI.ItemParam

Content item used to generate a response.


### Discriminator for OpenAI.ItemParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.ResponsesMessageItemParam](#openairesponsesmessageitemparam) |
| `function_call_output` | [OpenAI.FunctionToolCallOutputItemParam](#openaifunctiontoolcalloutputitemparam) |
| `file_search_call` | [OpenAI.FileSearchToolCallItemParam](#openaifilesearchtoolcallitemparam) |
| `computer_call` | [OpenAI.ComputerToolCallItemParam](#openaicomputertoolcallitemparam) |
| `computer_call_output` | [OpenAI.ComputerToolCallOutputItemParam](#openaicomputertoolcalloutputitemparam) |
| `web_search_call` | [OpenAI.WebSearchToolCallItemParam](#openaiwebsearchtoolcallitemparam) |
| `function_call` | [OpenAI.FunctionToolCallItemParam](#openaifunctiontoolcallitemparam) |
| `reasoning` | [OpenAI.ReasoningItemParam](#openaireasoningitemparam) |
| `item_reference` | [OpenAI.ItemReferenceItemParam](#openaiitemreferenceitemparam) |
| `image_generation_call` | [OpenAI.ImageGenToolCallItemParam](#openaiimagegentoolcallitemparam) |
| `code_interpreter_call` | [OpenAI.CodeInterpreterToolCallItemParam](#openaicodeinterpretertoolcallitemparam) |
| `mcp_list_tools` | [OpenAI.MCPListToolsItemParam](#openaimcplisttoolsitemparam) |
| `mcp_approval_request` | [OpenAI.MCPApprovalRequestItemParam](#openaimcpapprovalrequestitemparam) |
| `mcp_approval_response` | [OpenAI.MCPApprovalResponseItemParam](#openaimcpapprovalresponseitemparam) |
| `mcp_call` | [OpenAI.MCPCallItemParam](#openaimcpcallitemparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ItemType](#openaiitemtype) |  | Yes |  |

### OpenAI.ItemReferenceItemParam

An internal identifier for an item to reference.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The service-originated ID of the previously generated response item being referenced. | Yes |  |
| type | enum | <br>Possible values: `item_reference` | Yes |  |

### OpenAI.ItemResource

Content item used to generate a response.


### Discriminator for OpenAI.ItemResource

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `message` | [OpenAI.ResponsesMessageItemResource](#openairesponsesmessageitemresource) |
| `computer_call_output` | [OpenAI.ComputerToolCallOutputItemResource](#openaicomputertoolcalloutputitemresource) |
| `function_call` | [OpenAI.FunctionToolCallItemResource](#openaifunctiontoolcallitemresource) |
| `function_call_output` | [OpenAI.FunctionToolCallOutputItemResource](#openaifunctiontoolcalloutputitemresource) |
| `mcp_approval_response` | [OpenAI.MCPApprovalResponseItemResource](#openaimcpapprovalresponseitemresource) |
| `code_interpreter_call` | [OpenAI.CodeInterpreterToolCallItemResource](#openaicodeinterpretertoolcallitemresource) |
| `file_search_call` | [OpenAI.FileSearchToolCallItemResource](#openaifilesearchtoolcallitemresource) |
| `computer_call` | [OpenAI.ComputerToolCallItemResource](#openaicomputertoolcallitemresource) |
| `web_search_call` | [OpenAI.WebSearchToolCallItemResource](#openaiwebsearchtoolcallitemresource) |
| `reasoning` | [OpenAI.ReasoningItemResource](#openaireasoningitemresource) |
| `image_generation_call` | [OpenAI.ImageGenToolCallItemResource](#openaiimagegentoolcallitemresource) |
| `mcp_list_tools` | [OpenAI.MCPListToolsItemResource](#openaimcplisttoolsitemresource) |
| `mcp_approval_request` | [OpenAI.MCPApprovalRequestItemResource](#openaimcpapprovalrequestitemresource) |
| `mcp_call` | [OpenAI.MCPCallItemResource](#openaimcpcallitemresource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string |  | Yes |  |
| type | [OpenAI.ItemType](#openaiitemtype) |  | Yes |  |

### OpenAI.ItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`file_search_call`<br>`function_call`<br>`function_call_output`<br>`computer_call`<br>`computer_call_output`<br>`web_search_call`<br>`reasoning`<br>`item_reference`<br>`image_generation_call`<br>`code_interpreter_call`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call` |

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

### OpenAI.MCPApprovalRequestItemParam

A request for human approval of a tool invocation.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | <br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.MCPApprovalRequestItemResource

A request for human approval of a tool invocation.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of arguments for the tool. | Yes |  |
| name | string | The name of the tool to run. | Yes |  |
| server_label | string | The label of the MCP server making the request. | Yes |  |
| type | enum | <br>Possible values: `mcp_approval_request` | Yes |  |

### OpenAI.MCPApprovalResponseItemParam

A response to an MCP approval request.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| reason | string | Optional reason for the decision. | No |  |
| type | enum | <br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.MCPApprovalResponseItemResource

A response to an MCP approval request.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| approval_request_id | string | The ID of the approval request being answered. | Yes |  |
| approve | boolean | Whether the request was approved. | Yes |  |
| reason | string | Optional reason for the decision. | No |  |
| type | enum | <br>Possible values: `mcp_approval_response` | Yes |  |

### OpenAI.MCPCallItemParam

An invocation of a tool on an MCP server.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string | The error from the tool call, if any. | No |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string | The output from the tool call. | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| type | enum | <br>Possible values: `mcp_call` | Yes |  |

### OpenAI.MCPCallItemResource

An invocation of a tool on an MCP server.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | A JSON string of the arguments passed to the tool. | Yes |  |
| error | string | The error from the tool call, if any. | No |  |
| name | string | The name of the tool that was run. | Yes |  |
| output | string | The output from the tool call. | No |  |
| server_label | string | The label of the MCP server running the tool. | Yes |  |
| type | enum | <br>Possible values: `mcp_call` | Yes |  |

### OpenAI.MCPListToolsItemParam

A list of tools available on an MCP server.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string | Error message if the server could not list tools. | No |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array | The tools available on the server. | Yes |  |
| type | enum | <br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.MCPListToolsItemResource

A list of tools available on an MCP server.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | string | Error message if the server could not list tools. | No |  |
| server_label | string | The label of the MCP server. | Yes |  |
| tools | array | The tools available on the server. | Yes |  |
| type | enum | <br>Possible values: `mcp_list_tools` | Yes |  |

### OpenAI.MCPListToolsTool

A tool available on an MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations |  | Additional annotations about the tool. | No |  |
| description | string | The description of the tool. | No |  |
| input_schema |  | The JSON schema describing the tool's input. | Yes |  |
| name | string | The name of the tool. | Yes |  |

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

### OpenAI.ParallelToolCalls

Whether to enable parallel function calling during tool use.

**Type**: boolean


### OpenAI.RankingOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| ranker | enum | The ranker to use for the file search.<br>Possible values: `auto`, `default-2024-11-15` | No |  |
| score_threshold | number | The score threshold for the file search, a number between 0 and 1. Numbers closer to 1 will attempt to return only the most relevant results, but may return fewer results. | No |  |

### OpenAI.Reasoning

**o-series models only**

Configuration options for reasoning models.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| effort | object | **o-series models only** <br><br>Constrains effort on reasoning for <br>reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |

### OpenAI.ReasoningEffort

**o-series models only** 

Constrains effort on reasoning for reasoning models.

Currently supported values are `low`, `medium`, and `high`. Reducing reasoning effort can result in faster responses and fewer tokens used
on reasoning in a response.

| Property | Value |
|----------|-------|
| **Description** | **o-series models only** <br><br>Constrains effort on reasoning for <br>reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. |
| **Type** | string |
| **Values** | `low`<br>`medium`<br>`high` |

### OpenAI.ReasoningItemParam

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually 
managing context.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| encrypted_content | string | The encrypted content of the reasoning item - populated when a response is<br>generated with `reasoning.encrypted_content` in the `include` parameter. | No |  |
| summary | array | Reasoning text contents. | Yes |  |
| type | enum | <br>Possible values: `reasoning` | Yes |  |

### OpenAI.ReasoningItemResource

A description of the chain of thought used by a reasoning model while generating
a response. Be sure to include these items in your `input` to the Responses API
for subsequent turns of a conversation if you are manually 
managing context.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| encrypted_content | string | The encrypted content of the reasoning item - populated when a response is<br>generated with `reasoning.encrypted_content` in the `include` parameter. | No |  |
| summary | array | Reasoning text contents. | Yes |  |
| type | enum | <br>Possible values: `reasoning` | Yes |  |

### OpenAI.ReasoningItemSummaryPart


### Discriminator for OpenAI.ReasoningItemSummaryPart

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `summary_text` | [OpenAI.ReasoningItemSummaryTextPart](#openaireasoningitemsummarytextpart) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ReasoningItemSummaryPartType](#openaireasoningitemsummaryparttype) |  | Yes |  |

### OpenAI.ReasoningItemSummaryPartType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `summary_text` |

### OpenAI.ReasoningItemSummaryTextPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| text | string |  | Yes |  |
| type | enum | <br>Possible values: `summary_text` | Yes |  |

### OpenAI.Response

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean | Whether to run the model response in the background. | No | False |
| created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| error | object | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ code | [OpenAI.ResponseErrorCode](#openairesponseerrorcode) | The error code for the response. | No |  |
| └─ message | string | A human-readable description of the error. | No |  |
| id | string | Unique identifier for this Response. | Yes |  |
| incomplete_details | object | Details about why the response is incomplete. | Yes |  |
| └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only** <br><br>Constrains effort on reasoning for <br>reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | Yes |  |
| text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities **Function calls (custom tools)**: Functions that are defined by you,<br>  enabling the model to call your own code. managing context. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | Yes |  |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCodeDeltaEvent

Emitted when a partial code snippet is added by the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The partial code snippet added by the code interpreter. | Yes |  |
| output_index | integer | The index of the output item that the code interpreter call is in progress. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.code.delta`.<br>Possible values: `response.code_interpreter_call.code.delta` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCodeDoneEvent

Emitted when code snippet output is finalized by the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The final code snippet output by the code interpreter. | Yes |  |
| output_index | integer | The index of the output item that the code interpreter call is in progress. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.code.done`.<br>Possible values: `response.code_interpreter_call.code.done` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCompletedEvent

Emitted when the code interpreter call is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter_call | [OpenAI.CodeInterpreterToolCallItemResource](#openaicodeinterpretertoolcallitemresource) | A tool call to run code.<br> | Yes |  |
| output_index | integer | The index of the output item that the code interpreter call is in progress. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.completed`.<br>Possible values: `response.code_interpreter_call.completed` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInProgressEvent

Emitted when a code interpreter call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter_call | [OpenAI.CodeInterpreterToolCallItemResource](#openaicodeinterpretertoolcallitemresource) | A tool call to run code.<br> | Yes |  |
| output_index | integer | The index of the output item that the code interpreter call is in progress. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.in_progress`.<br>Possible values: `response.code_interpreter_call.in_progress` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInterpretingEvent

Emitted when the code interpreter is actively interpreting the code snippet.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code_interpreter_call | [OpenAI.CodeInterpreterToolCallItemResource](#openaicodeinterpretertoolcallitemresource) | A tool call to run code.<br> | Yes |  |
| output_index | integer | The index of the output item that the code interpreter call is in progress. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.interpreting`.<br>Possible values: `response.code_interpreter_call.interpreting` | Yes |  |

### OpenAI.ResponseCompletedEvent

Emitted when the model response is complete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background. | No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that extend the model's capabilities. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |
| type | enum | The type of the event. Always `response.completed`.<br>Possible values: `response.completed` | Yes |  |

### OpenAI.ResponseContentPartAddedEvent

Emitted when a new content part is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that was added. | Yes |  |
| item_id | string | The ID of the output item that the content part was added to. | Yes |  |
| output_index | integer | The index of the output item that the content part was added to. | Yes |  |
| part | object |  | Yes |  |
| └─ type | [OpenAI.ItemContentType](#openaiitemcontenttype) | Multi-modal input and output contents. | No |  |
| type | enum | The type of the event. Always `response.content_part.added`.<br>Possible values: `response.content_part.added` | Yes |  |

### OpenAI.ResponseContentPartDoneEvent

Emitted when a content part is done.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that is done. | Yes |  |
| item_id | string | The ID of the output item that the content part was added to. | Yes |  |
| output_index | integer | The index of the output item that the content part was added to. | Yes |  |
| part | object |  | Yes |  |
| └─ type | [OpenAI.ItemContentType](#openaiitemcontenttype) | Multi-modal input and output contents. | No |  |
| type | enum | The type of the event. Always `response.content_part.done`.<br>Possible values: `response.content_part.done` | Yes |  |

### OpenAI.ResponseCreatedEvent

An event that is emitted when a response is created.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background. | No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. **Function calls (custom tools)**: Functions that are defined by you,<br>  enabling the model to call your own code. managing context. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |
| type | enum | The type of the event. Always `response.created`.<br>Possible values: `response.created` | Yes |  |

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
| **Description** | The error code for the response. |
| **Type** | string |
| **Values** | `server_error`<br>`rate_limit_exceeded`<br>`invalid_prompt`<br>`vector_store_timeout`<br>`invalid_image`<br>`invalid_image_format`<br>`invalid_base64_image`<br>`invalid_image_url`<br>`image_too_large`<br>`image_too_small`<br>`image_parse_error`<br>`image_content_policy_violation`<br>`invalid_image_mode`<br>`image_file_too_large`<br>`unsupported_image_media_type`<br>`empty_image_file`<br>`failed_to_download_image`<br>`image_file_not_found` |

### OpenAI.ResponseErrorEvent

Emitted when an error occurs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The error code. | Yes |  |
| message | string | The error message. | Yes |  |
| param | string | The error parameter. | Yes |  |
| type | enum | The type of the event. Always `error`.<br>Possible values: `error` | Yes |  |

### OpenAI.ResponseFailedEvent

An event that is emitted when a response fails.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background. | No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. **Function calls (custom tools)**: Functions that are defined by you,<br>  enabling the model to call your own code. managing context. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |
| type | enum | The type of the event. Always `response.failed`.<br>Possible values: `response.failed` | Yes |  |

### OpenAI.ResponseFileSearchCallCompletedEvent

Emitted when a file search call is completed (results found).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | integer | The index of the output item that the file search call is initiated. | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.completed`.<br>Possible values: `response.file_search_call.completed` | Yes |  |

### OpenAI.ResponseFileSearchCallInProgressEvent

Emitted when a file search call is initiated.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | integer | The index of the output item that the file search call is initiated. | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.in_progress`.<br>Possible values: `response.file_search_call.in_progress` | Yes |  |

### OpenAI.ResponseFileSearchCallSearchingEvent

Emitted when a file search is currently searching.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the output item that the file search call is initiated. | Yes |  |
| output_index | integer | The index of the output item that the file search call is searching. | Yes |  |
| type | enum | The type of the event. Always `response.file_search_call.searching`.<br>Possible values: `response.file_search_call.searching` | Yes |  |

### OpenAI.ResponseFormat


### Discriminator for OpenAI.ResponseFormat

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `text` | [OpenAI.ResponseFormatText](#openairesponseformattext) |
| `json_object` | [OpenAI.ResponseFormatJsonObject](#openairesponseformatjsonobject) |
| `json_schema` | [OpenAI.ResponseFormatJsonSchema](#openairesponseformatjsonschema) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `text`, `json_object`, `json_schema` | Yes |  |

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


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| json_schema | object | Structured Outputs configuration options, including a JSON Schema. | Yes |  |
| └─ description | string | A description of what the response format is for, used by the model to<br>determine how to respond in the format. | No |  |
| └─ name | string | The name of the response format. Must be a-z, A-Z, 0-9, or contain<br>underscores and dashes, with a maximum length of 64. | No |  |
| └─ schema | [OpenAI.ResponseFormatJsonSchemaSchema](#openairesponseformatjsonschemaschema) | The schema for the response format, described as a JSON Schema object.<br>Learn how to build JSON schemas [here](https://json-schema.org/). | No |  |
| └─ strict | boolean | Whether to enable strict schema adherence when generating the output.<br>If set to true, the model will always follow the exact schema defined<br>in the `schema` field. Only a subset of JSON Schema is supported when<br>`strict` is `true`. . | No | False |
| type | enum | The type of response format being defined. Always `json_schema`.<br>Possible values: `json_schema` | Yes |  |

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
| type | enum | The type of the event. Always `response.function_call_arguments.delta`.<br>Possible values: `response.function_call_arguments.delta` | Yes |  |

### OpenAI.ResponseFunctionCallArgumentsDoneEvent

Emitted when function-call arguments are finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments | string | The function-call arguments. | Yes |  |
| item_id | string | The ID of the item. | Yes |  |
| output_index | integer | The index of the output item. | Yes |  |
| type | enum | <br>Possible values: `response.function_call_arguments.done` | Yes |  |

### OpenAI.ResponseImageGenCallCompletedEvent

Emitted when an image generation tool call has completed and the final image is available.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.completed'.<br>Possible values: `response.image_generation_call.completed` | Yes |  |

### OpenAI.ResponseImageGenCallGeneratingEvent

Emitted when an image generation tool call is actively generating an image (intermediate state).

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.generating'.<br>Possible values: `response.image_generation_call.generating` | Yes |  |

### OpenAI.ResponseImageGenCallInProgressEvent

Emitted when an image generation tool call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.in_progress'.<br>Possible values: `response.image_generation_call.in_progress` | Yes |  |

### OpenAI.ResponseImageGenCallPartialImageEvent

Emitted when a partial image is available during image generation streaming.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the image generation item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| partial_image_b64 | string | Base64-encoded partial image data, suitable for rendering as an image. | Yes |  |
| partial_image_index | integer | 0-based index for the partial image (backend is 1-based, but this is 0-based for the user). | Yes |  |
| type | enum | The type of the event. Always 'response.image_generation_call.partial_image'.<br>Possible values: `response.image_generation_call.partial_image` | Yes |  |

### OpenAI.ResponseInProgressEvent

Emitted when the response is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background. | No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the model's capabilities. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |
| type | enum | The type of the event. Always `response.in_progress`.<br>Possible values: `response.in_progress` | Yes |  |

### OpenAI.ResponseIncompleteEvent

An event that is emitted when a response finishes as incomplete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background. | No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that that extend the model's capabilities, **Function calls (custom tools)** | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |
| type | enum | The type of the event. Always `response.incomplete`.<br>Possible values: `response.incomplete` | Yes |  |

### OpenAI.ResponseItemList

A list of Response items.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | A list of items used to generate this response. | Yes |  |
| first_id | string | The ID of the first item in the list. | Yes |  |
| has_more | boolean | Whether there are more items available. | Yes |  |
| last_id | string | The ID of the last item in the list. | Yes |  |
| object | enum | The type of object returned, must be `list`.<br>Possible values: `list` | Yes |  |

### OpenAI.ResponseMCPCallArgumentsDeltaEvent

Emitted when there is a delta (partial update) to the arguments of an MCP tool call.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta |  | The partial update to the arguments for the MCP tool call. | Yes |  |
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.arguments_delta'.<br>Possible values: `response.mcp_call.arguments_delta` | Yes |  |

### OpenAI.ResponseMCPCallArgumentsDoneEvent

Emitted when the arguments for an MCP tool call are finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| arguments |  | The finalized arguments for the MCP tool call. | Yes |  |
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.arguments_done'.<br>Possible values: `response.mcp_call.arguments_done` | Yes |  |

### OpenAI.ResponseMCPCallCompletedEvent

Emitted when an MCP  tool call has completed successfully.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the event. Always 'response.mcp_call.completed'.<br>Possible values: `response.mcp_call.completed` | Yes |  |

### OpenAI.ResponseMCPCallFailedEvent

Emitted when an MCP  tool call has failed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the event. Always 'response.mcp_call.failed'.<br>Possible values: `response.mcp_call.failed` | Yes |  |

### OpenAI.ResponseMCPCallInProgressEvent

Emitted when an MCP  tool call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the MCP tool call item being processed. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| type | enum | The type of the event. Always 'response.mcp_call.in_progress'.<br>Possible values: `response.mcp_call.in_progress` | Yes |  |

### OpenAI.ResponseMCPListToolsCompletedEvent

Emitted when the list of available MCP tools has been successfully retrieved.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the event. Always 'response.mcp_list_tools.completed'.<br>Possible values: `response.mcp_list_tools.completed` | Yes |  |

### OpenAI.ResponseMCPListToolsFailedEvent

Emitted when the attempt to list available MCP tools has failed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the event. Always 'response.mcp_list_tools.failed'.<br>Possible values: `response.mcp_list_tools.failed` | Yes |  |

### OpenAI.ResponseMCPListToolsInProgressEvent

Emitted when the system is in the process of retrieving the list of available MCP tools.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the event. Always 'response.mcp_list_tools.in_progress'.<br>Possible values: `response.mcp_list_tools.in_progress` | Yes |  |

### OpenAI.ResponseOutputItemAddedEvent

Emitted when a new output item is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item | object | Content item used to generate a response. | Yes |  |
| └─ id | string |  | No |  |
| └─ type | [OpenAI.ItemType](#openaiitemtype) |  | No |  |
| output_index | integer | The index of the output item that was added. | Yes |  |
| type | enum | The type of the event. Always `response.output_item.added`.<br>Possible values: `response.output_item.added` | Yes |  |

### OpenAI.ResponseOutputItemDoneEvent

Emitted when an output item is marked done.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item | object | Content item used to generate a response. | Yes |  |
| └─ id | string |  | No |  |
| └─ type | [OpenAI.ItemType](#openaiitemtype) |  | No |  |
| output_index | integer | The index of the output item that was marked done. | Yes |  |
| type | enum | The type of the event. Always `response.output_item.done`.<br>Possible values: `response.output_item.done` | Yes |  |

### OpenAI.ResponseQueuedEvent

Emitted when a response is queued and waiting to be processed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background. | No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string | Inserts a system (or developer) message as the first item in the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and . | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and <br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output <br>from all `output_text` items in the `output` array, if any are present. <br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. reasoning models. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for<br>reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`, <br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain<br>text or structured JSON data.  | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>-**Built-in tools**: Tools that that extend the model's capabilities. **Function calls (custom tools)**: Functions that are defined by you, nabling the model to call your own code.  | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the <br>  response to fit the context window by dropping input items in the<br>  middle of the conversation. <br>- `disabled` (default): If a model response will exceed the context window <br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |
| type | enum | The type of the event. Always 'response.queued'.<br>Possible values: `response.queued` | Yes |  |

### OpenAI.ResponseReasoningDeltaEvent

Emitted when there is a delta (partial update) to the reasoning content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the reasoning content part within the output item. | Yes |  |
| delta |  | The partial update to the reasoning content. | Yes |  |
| item_id | string | The unique identifier of the item for which reasoning is being updated. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| type | enum | The type of the event. Always 'response.reasoning.delta'.<br>Possible values: `response.reasoning.delta` | Yes |  |

### OpenAI.ResponseReasoningDoneEvent

Emitted when the reasoning content is finalized for an item.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the reasoning content part within the output item. | Yes |  |
| item_id | string | The unique identifier of the item for which reasoning is finalized. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| text | string | The finalized reasoning text. | Yes |  |
| type | enum | The type of the event. Always 'response.reasoning.done'.<br>Possible values: `response.reasoning.done` | Yes |  |

### OpenAI.ResponseReasoningSummaryDeltaEvent

Emitted when there is a delta (partial update) to the reasoning summary content.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta |  | The partial update to the reasoning summary content. | Yes |  |
| item_id | string | The unique identifier of the item for which the reasoning summary is being updated. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| summary_index | integer | The index of the summary part within the output item. | Yes |  |
| type | enum | The type of the event. Always 'response.reasoning_summary.delta'.<br>Possible values: `response.reasoning_summary.delta` | Yes |  |

### OpenAI.ResponseReasoningSummaryDoneEvent

Emitted when the reasoning summary content is finalized for an item.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the item for which the reasoning summary is finalized. | Yes |  |
| output_index | integer | The index of the output item in the response's output array. | Yes |  |
| summary_index | integer | The index of the summary part within the output item. | Yes |  |
| text | string | The finalized reasoning summary text. | Yes |  |
| type | enum | The type of the event. Always 'response.reasoning_summary.done'.<br>Possible values: `response.reasoning_summary.done` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartAddedEvent

Emitted when a new reasoning summary part is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the item this summary part is associated with. | Yes |  |
| output_index | integer | The index of the output item this summary part is associated with. | Yes |  |
| part | object |  | Yes |  |
| └─ type | [OpenAI.ReasoningItemSummaryPartType](#openaireasoningitemsummaryparttype) |  | No |  |
| summary_index | integer | The index of the summary part within the reasoning summary. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_part.added`.<br>Possible values: `response.reasoning_summary_part.added` | Yes |  |

### OpenAI.ResponseReasoningSummaryPartDoneEvent

Emitted when a reasoning summary part is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the item this summary part is associated with. | Yes |  |
| output_index | integer | The index of the output item this summary part is associated with. | Yes |  |
| part | object |  | Yes |  |
| └─ type | [OpenAI.ReasoningItemSummaryPartType](#openaireasoningitemsummaryparttype) |  | No |  |
| summary_index | integer | The index of the summary part within the reasoning summary. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_part.done`.<br>Possible values: `response.reasoning_summary_part.done` | Yes |  |

### OpenAI.ResponseReasoningSummaryTextDeltaEvent

Emitted when a delta is added to a reasoning summary text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The text delta that was added to the summary. | Yes |  |
| item_id | string | The ID of the item this summary text delta is associated with. | Yes |  |
| output_index | integer | The index of the output item this summary text delta is associated with. | Yes |  |
| summary_index | integer | The index of the summary part within the reasoning summary. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_text.delta`.<br>Possible values: `response.reasoning_summary_text.delta` | Yes |  |

### OpenAI.ResponseReasoningSummaryTextDoneEvent

Emitted when a reasoning summary text is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The ID of the item this summary text is associated with. | Yes |  |
| output_index | integer | The index of the output item this summary text is associated with. | Yes |  |
| summary_index | integer | The index of the summary part within the reasoning summary. | Yes |  |
| text | string | The full text of the completed reasoning summary. | Yes |  |
| type | enum | The type of the event. Always `response.reasoning_summary_text.done`.<br>Possible values: `response.reasoning_summary_text.done` | Yes |  |

### OpenAI.ResponseRefusalDeltaEvent

Emitted when there is a partial refusal text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that the refusal text is added to. | Yes |  |
| delta | string | The refusal text that is added. | Yes |  |
| item_id | string | The ID of the output item that the refusal text is added to. | Yes |  |
| output_index | integer | The index of the output item that the refusal text is added to. | Yes |  |
| type | enum | The type of the event. Always `response.refusal.delta`.<br>Possible values: `response.refusal.delta` | Yes |  |

### OpenAI.ResponseRefusalDoneEvent

Emitted when refusal text is finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that the refusal text is finalized. | Yes |  |
| item_id | string | The ID of the output item that the refusal text is finalized. | Yes |  |
| output_index | integer | The index of the output item that the refusal text is finalized. | Yes |  |
| refusal | string | The refusal text that is finalized. | Yes |  |
| type | enum | The type of the event. Always `response.refusal.done`.<br>Possible values: `response.refusal.done` | Yes |  |

### OpenAI.ResponseStreamEvent


### Discriminator for OpenAI.ResponseStreamEvent

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `response.completed` | [OpenAI.ResponseCompletedEvent](#openairesponsecompletedevent) |
| `response.content_part.added` | [OpenAI.ResponseContentPartAddedEvent](#openairesponsecontentpartaddedevent) |
| `response.content_part.done` | [OpenAI.ResponseContentPartDoneEvent](#openairesponsecontentpartdoneevent) |
| `response.created` | [OpenAI.ResponseCreatedEvent](#openairesponsecreatedevent) |
| `error` | [OpenAI.ResponseErrorEvent](#openairesponseerrorevent) |
| `response.file_search_call.completed` | [OpenAI.ResponseFileSearchCallCompletedEvent](#openairesponsefilesearchcallcompletedevent) |
| `response.file_search_call.in_progress` | [OpenAI.ResponseFileSearchCallInProgressEvent](#openairesponsefilesearchcallinprogressevent) |
| `response.file_search_call.searching` | [OpenAI.ResponseFileSearchCallSearchingEvent](#openairesponsefilesearchcallsearchingevent) |
| `response.function_call_arguments.delta` | [OpenAI.ResponseFunctionCallArgumentsDeltaEvent](#openairesponsefunctioncallargumentsdeltaevent) |
| `response.function_call_arguments.done` | [OpenAI.ResponseFunctionCallArgumentsDoneEvent](#openairesponsefunctioncallargumentsdoneevent) |
| `response.in_progress` | [OpenAI.ResponseInProgressEvent](#openairesponseinprogressevent) |
| `response.failed` | [OpenAI.ResponseFailedEvent](#openairesponsefailedevent) |
| `response.incomplete` | [OpenAI.ResponseIncompleteEvent](#openairesponseincompleteevent) |
| `response.output_item.added` | [OpenAI.ResponseOutputItemAddedEvent](#openairesponseoutputitemaddedevent) |
| `response.output_item.done` | [OpenAI.ResponseOutputItemDoneEvent](#openairesponseoutputitemdoneevent) |
| `response.refusal.delta` | [OpenAI.ResponseRefusalDeltaEvent](#openairesponserefusaldeltaevent) |
| `response.refusal.done` | [OpenAI.ResponseRefusalDoneEvent](#openairesponserefusaldoneevent) |
| `response.output_text.annotation.added` | [OpenAI.ResponseTextAnnotationDeltaEvent](#openairesponsetextannotationdeltaevent) |
| `response.output_text.delta` | [OpenAI.ResponseTextDeltaEvent](#openairesponsetextdeltaevent) |
| `response.output_text.done` | [OpenAI.ResponseTextDoneEvent](#openairesponsetextdoneevent) |
| `response.reasoning_summary_part.added` | [OpenAI.ResponseReasoningSummaryPartAddedEvent](#openairesponsereasoningsummarypartaddedevent) |
| `response.reasoning_summary_part.done` | [OpenAI.ResponseReasoningSummaryPartDoneEvent](#openairesponsereasoningsummarypartdoneevent) |
| `response.reasoning_summary_text.delta` | [OpenAI.ResponseReasoningSummaryTextDeltaEvent](#openairesponsereasoningsummarytextdeltaevent) |
| `response.reasoning_summary_text.done` | [OpenAI.ResponseReasoningSummaryTextDoneEvent](#openairesponsereasoningsummarytextdoneevent) |
| `response.web_search_call.completed` | [OpenAI.ResponseWebSearchCallCompletedEvent](#openairesponsewebsearchcallcompletedevent) |
| `response.web_search_call.in_progress` | [OpenAI.ResponseWebSearchCallInProgressEvent](#openairesponsewebsearchcallinprogressevent) |
| `response.web_search_call.searching` | [OpenAI.ResponseWebSearchCallSearchingEvent](#openairesponsewebsearchcallsearchingevent) |
| `response.image_generation_call.completed` | [OpenAI.ResponseImageGenCallCompletedEvent](#openairesponseimagegencallcompletedevent) |
| `response.image_generation_call.generating` | [OpenAI.ResponseImageGenCallGeneratingEvent](#openairesponseimagegencallgeneratingevent) |
| `response.image_generation_call.in_progress` | [OpenAI.ResponseImageGenCallInProgressEvent](#openairesponseimagegencallinprogressevent) |
| `response.image_generation_call.partial_image` | [OpenAI.ResponseImageGenCallPartialImageEvent](#openairesponseimagegencallpartialimageevent) |
| `response.mcp_call.arguments_delta` | [OpenAI.ResponseMCPCallArgumentsDeltaEvent](#openairesponsemcpcallargumentsdeltaevent) |
| `response.mcp_call.arguments_done` | [OpenAI.ResponseMCPCallArgumentsDoneEvent](#openairesponsemcpcallargumentsdoneevent) |
| `response.mcp_call.completed` | [OpenAI.ResponseMCPCallCompletedEvent](#openairesponsemcpcallcompletedevent) |
| `response.mcp_call.failed` | [OpenAI.ResponseMCPCallFailedEvent](#openairesponsemcpcallfailedevent) |
| `response.mcp_call.in_progress` | [OpenAI.ResponseMCPCallInProgressEvent](#openairesponsemcpcallinprogressevent) |
| `response.mcp_list_tools.completed` | [OpenAI.ResponseMCPListToolsCompletedEvent](#openairesponsemcplisttoolscompletedevent) |
| `response.mcp_list_tools.failed` | [OpenAI.ResponseMCPListToolsFailedEvent](#openairesponsemcplisttoolsfailedevent) |
| `response.mcp_list_tools.in_progress` | [OpenAI.ResponseMCPListToolsInProgressEvent](#openairesponsemcplisttoolsinprogressevent) |
| `response.queued` | [OpenAI.ResponseQueuedEvent](#openairesponsequeuedevent) |
| `response.reasoning.delta` | [OpenAI.ResponseReasoningDeltaEvent](#openairesponsereasoningdeltaevent) |
| `response.reasoning.done` | [OpenAI.ResponseReasoningDoneEvent](#openairesponsereasoningdoneevent) |
| `response.reasoning_summary.delta` | [OpenAI.ResponseReasoningSummaryDeltaEvent](#openairesponsereasoningsummarydeltaevent) |
| `response.reasoning_summary.done` | [OpenAI.ResponseReasoningSummaryDoneEvent](#openairesponsereasoningsummarydoneevent) |
| `response.code_interpreter_call.code.delta` | [OpenAI.ResponseCodeInterpreterCallCodeDeltaEvent](#openairesponsecodeinterpretercallcodedeltaevent) |
| `response.code_interpreter_call.code.done` | [OpenAI.ResponseCodeInterpreterCallCodeDoneEvent](#openairesponsecodeinterpretercallcodedoneevent) |
| `response.code_interpreter_call.completed` | [OpenAI.ResponseCodeInterpreterCallCompletedEvent](#openairesponsecodeinterpretercallcompletedevent) |
| `response.code_interpreter_call.in_progress` | [OpenAI.ResponseCodeInterpreterCallInProgressEvent](#openairesponsecodeinterpretercallinprogressevent) |
| `response.code_interpreter_call.interpreting` | [OpenAI.ResponseCodeInterpreterCallInterpretingEvent](#openairesponsecodeinterpretercallinterpretingevent) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| sequence_number | integer | The sequence number for this event. | Yes |  |
| type | [OpenAI.ResponseStreamEventType](#openairesponsestreameventtype) |  | Yes |  |

### OpenAI.ResponseStreamEventType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `response.audio.delta`<br>`response.audio.done`<br>`response.audio_transcript.delta`<br>`response.audio_transcript.done`<br>`response.code_interpreter_call.code.delta`<br>`response.code_interpreter_call.code.done`<br>`response.code_interpreter_call.completed`<br>`response.code_interpreter_call.in_progress`<br>`response.code_interpreter_call.interpreting`<br>`response.completed`<br>`response.content_part.added`<br>`response.content_part.done`<br>`response.created`<br>`error`<br>`response.file_search_call.completed`<br>`response.file_search_call.in_progress`<br>`response.file_search_call.searching`<br>`response.function_call_arguments.delta`<br>`response.function_call_arguments.done`<br>`response.in_progress`<br>`response.failed`<br>`response.incomplete`<br>`response.output_item.added`<br>`response.output_item.done`<br>`response.refusal.delta`<br>`response.refusal.done`<br>`response.output_text.annotation.added`<br>`response.output_text.delta`<br>`response.output_text.done`<br>`response.reasoning_summary_part.added`<br>`response.reasoning_summary_part.done`<br>`response.reasoning_summary_text.delta`<br>`response.reasoning_summary_text.done`<br>`response.web_search_call.completed`<br>`response.web_search_call.in_progress`<br>`response.web_search_call.searching`<br>`response.image_generation_call.completed`<br>`response.image_generation_call.generating`<br>`response.image_generation_call.in_progress`<br>`response.image_generation_call.partial_image`<br>`response.mcp_call.arguments_delta`<br>`response.mcp_call.arguments_done`<br>`response.mcp_call.completed`<br>`response.mcp_call.failed`<br>`response.mcp_call.in_progress`<br>`response.mcp_list_tools.completed`<br>`response.mcp_list_tools.failed`<br>`response.mcp_list_tools.in_progress`<br>`response.queued`<br>`response.reasoning.delta`<br>`response.reasoning.done`<br>`response.reasoning_summary.delta`<br>`response.reasoning_summary.done` |

### OpenAI.ResponseTextAnnotationDeltaEvent

Emitted when a text annotation is added.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotation | [OpenAI.Annotation](#openaiannotation) |  | Yes |  |
| annotation_index | integer | The index of the annotation that was added. | Yes |  |
| content_index | integer | The index of the content part that the text annotation was added to. | Yes |  |
| item_id | string | The ID of the output item that the text annotation was added to. | Yes |  |
| output_index | integer | The index of the output item that the text annotation was added to. | Yes |  |
| type | enum | The type of the event. Always `response.output_text.annotation.added`.<br>Possible values: `response.output_text.annotation.added` | Yes |  |

### OpenAI.ResponseTextDeltaEvent

Emitted when there is an additional text delta.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that the text delta was added to. | Yes |  |
| delta | string | The text delta that was added. | Yes |  |
| item_id | string | The ID of the output item that the text delta was added to. | Yes |  |
| output_index | integer | The index of the output item that the text delta was added to. | Yes |  |
| type | enum | The type of the event. Always `response.output_text.delta`.<br>Possible values: `response.output_text.delta` | Yes |  |

### OpenAI.ResponseTextDoneEvent

Emitted when text content is finalized.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content_index | integer | The index of the content part that the text content is finalized. | Yes |  |
| item_id | string | The ID of the output item that the text content is finalized. | Yes |  |
| output_index | integer | The index of the output item that the text content is finalized. | Yes |  |
| text | string | The text content that is finalized. | Yes |  |
| type | enum | The type of the event. Always `response.output_text.done`.<br>Possible values: `response.output_text.done` | Yes |  |

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
| type | [OpenAI.ResponseTextFormatConfigurationType](#openairesponsetextformatconfigurationtype) | An object specifying the format that the model must output.<br><br>Configuring `{ "type": "json_schema" }` enables Structured Outputs, <br>which ensures the model will match your supplied JSON schema. <br><br>The default format is `{ "type": "text" }` with no additional options.<br><br>**Not recommended for gpt-4o and newer models:**<br><br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | Yes |  |

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

Configuring `{ "type": "json_schema" }` enables Structured Outputs, 
which ensures the model will match your supplied JSON schema. 

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

### OpenAI.ResponseUsage

Represents token usage details including input tokens, output tokens,
a breakdown of output tokens, and the total tokens used.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_tokens | integer | The number of input tokens. | Yes |  |
| input_tokens_details | object | A detailed breakdown of the input tokens. | Yes |  |
| └─ cached_tokens | integer | The number of tokens that were retrieved from the cache. | No |  |
| output_tokens | integer | The number of output tokens. | Yes |  |
| output_tokens_details | object | A detailed breakdown of the output tokens. | Yes |  |
| └─ reasoning_tokens | integer | The number of reasoning tokens. | No |  |
| total_tokens | integer | The total number of tokens used. | Yes |  |

### OpenAI.ResponseWebSearchCallCompletedEvent

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | integer | The index of the output item that the web search call is associated with. | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.completed`.<br>Possible values: `response.web_search_call.completed` | Yes |  |

### OpenAI.ResponseWebSearchCallInProgressEvent

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | integer | The index of the output item that the web search call is associated with. | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.in_progress`.<br>Possible values: `response.web_search_call.in_progress` | Yes |  |

### OpenAI.ResponseWebSearchCallSearchingEvent

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | Unique ID for the output item associated with the web search call. | Yes |  |
| output_index | integer | The index of the output item that the web search call is associated with. | Yes |  |
| type | enum | The type of the event. Always `response.web_search_call.searching`.<br>Possible values: `response.web_search_call.searching` | Yes |  |

### OpenAI.ResponsesAssistantMessageItemParam

A message parameter item with the `assistant` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `assistant`.<br>Possible values: `assistant` | Yes |  |

### OpenAI.ResponsesAssistantMessageItemResource

A message resource item with the `assistant` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `assistant`.<br>Possible values: `assistant` | Yes |  |

### OpenAI.ResponsesDeveloperMessageItemParam

A message parameter item with the `developer` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `developer`.<br>Possible values: `developer` | Yes |  |

### OpenAI.ResponsesDeveloperMessageItemResource

A message resource item with the `developer` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `developer`.<br>Possible values: `developer` | Yes |  |

### OpenAI.ResponsesMessageItemParam

A response message item, representing a role and content, as provided as client request parameters.


### Discriminator for OpenAI.ResponsesMessageItemParam

This component uses the property `role` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `user` | [OpenAI.ResponsesUserMessageItemParam](#openairesponsesusermessageitemparam) |
| `system` | [OpenAI.ResponsesSystemMessageItemParam](#openairesponsessystemmessageitemparam) |
| `developer` | [OpenAI.ResponsesDeveloperMessageItemParam](#openairesponsesdevelopermessageitemparam) |
| `assistant` | [OpenAI.ResponsesAssistantMessageItemParam](#openairesponsesassistantmessageitemparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| role | object | The collection of valid roles for responses message items. | Yes |  |
| type | enum | The type of the responses item, which is always 'message'.<br>Possible values: `message` | Yes |  |

### OpenAI.ResponsesMessageItemResource

A response message resource item, representing a role and content, as provided on service responses.


### Discriminator for OpenAI.ResponsesMessageItemResource

This component uses the property `role` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `user` | [OpenAI.ResponsesUserMessageItemResource](#openairesponsesusermessageitemresource) |
| `system` | [OpenAI.ResponsesSystemMessageItemResource](#openairesponsessystemmessageitemresource) |
| `developer` | [OpenAI.ResponsesDeveloperMessageItemResource](#openairesponsesdevelopermessageitemresource) |
| `assistant` | [OpenAI.ResponsesAssistantMessageItemResource](#openairesponsesassistantmessageitemresource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| role | object | The collection of valid roles for responses message items. | Yes |  |
| status | enum | The status of the item. One of `in_progress`, `completed`, or<br>`incomplete`. Populated when items are returned via API.<br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | The type of the responses item, which is always 'message'.<br>Possible values: `message` | Yes |  |

### OpenAI.ResponsesMessageRole

The collection of valid roles for responses message items.

| Property | Value |
|----------|-------|
| **Description** | The collection of valid roles for responses message items. |
| **Type** | string |
| **Values** | `system`<br>`developer`<br>`user`<br>`assistant` |

### OpenAI.ResponsesSystemMessageItemParam

A message parameter item with the `system` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `system`.<br>Possible values: `system` | Yes |  |

### OpenAI.ResponsesSystemMessageItemResource

A message resource item with the `system` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `system`.<br>Possible values: `system` | Yes |  |

### OpenAI.ResponsesUserMessageItemParam

A message parameter item with the `user` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `user`.<br>Possible values: `user` | Yes |  |

### OpenAI.ResponsesUserMessageItemResource

A message resource item with the `user` role.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| content | array | The content associated with the message. | Yes |  |
| role | enum | The role of the message, which is always `user`.<br>Possible values: `user` | Yes |  |

### OpenAI.StopConfiguration

Not supported with latest reasoning models `o3` and `o4-mini`.

Up to 4 sequences where the API will stop generating further tokens. The
returned text will not contain the stop sequence.

This schema accepts one of the following types:

- **string**
- **array**

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
| `mcp` | [OpenAI.MCPTool](#openaimcptool) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ToolType](#openaitooltype) | A tool that can be used to generate a response. | Yes |  |

### OpenAI.ToolChoiceObject


### Discriminator for OpenAI.ToolChoiceObject

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `file_search` | [OpenAI.ToolChoiceObjectFileSearch](#openaitoolchoiceobjectfilesearch) |
| `computer_use_preview` | [OpenAI.ToolChoiceObjectComputer](#openaitoolchoiceobjectcomputer) |
| `web_search_preview` | [OpenAI.ToolChoiceObjectWebSearch](#openaitoolchoiceobjectwebsearch) |
| `image_generation` | [OpenAI.ToolChoiceObjectImageGen](#openaitoolchoiceobjectimagegen) |
| `code_interpreter` | [OpenAI.ToolChoiceObjectCodeInterpreter](#openaitoolchoiceobjectcodeinterpreter) |
| `mcp` | [OpenAI.ToolChoiceObjectMCP](#openaitoolchoiceobjectmcp) |
| `function` | [OpenAI.ToolChoiceObjectFunction](#openaitoolchoiceobjectfunction) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | Yes |  |

### OpenAI.ToolChoiceObjectCodeInterpreter

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `code_interpreter` | Yes |  |

### OpenAI.ToolChoiceObjectComputer

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `computer_use_preview` | Yes |  |

### OpenAI.ToolChoiceObjectFileSearch

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `file_search` | Yes |  |

### OpenAI.ToolChoiceObjectFunction

Use this option to force the model to call a specific function.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the function to call. | Yes |  |
| type | enum | For function calling, the type is always `function`.<br>Possible values: `function` | Yes |  |

### OpenAI.ToolChoiceObjectImageGen

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `image_generation` | Yes |  |

### OpenAI.ToolChoiceObjectMCP

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `mcp` | Yes |  |

### OpenAI.ToolChoiceObjectType

Indicates that the model should use a built-in tool to generate a response.

| Property | Value |
|----------|-------|
| **Description** | Indicates that the model should use a built-in tool to generate a response. |
| **Type** | string |
| **Values** | `file_search`<br>`function`<br>`computer_use_preview`<br>`web_search_preview`<br>`image_generation`<br>`code_interpreter`<br>`mcp` |

### OpenAI.ToolChoiceObjectWebSearch

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `web_search_preview` | Yes |  |

### OpenAI.ToolChoiceOptions

Controls which (if any) tool is called by the model.

`none` means the model will not call any tool and instead generates a message.

`auto` means the model can pick between generating a message or calling one or
more tools.

`required` means the model must call one or more tools.

| Property | Value |
|----------|-------|
| **Description** | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. |
| **Type** | string |
| **Values** | `none`<br>`auto`<br>`required` |

### OpenAI.ToolType

A tool that can be used to generate a response.

| Property | Value |
|----------|-------|
| **Description** | A tool that can be used to generate a response. |
| **Type** | string |
| **Values** | `file_search`<br>`function`<br>`computer_use_preview`<br>`web_search_preview`<br>`mcp`<br>`code_interpreter`<br>`image_generation` |

### OpenAI.TranscriptionAudioResponseFormat

References: [OpenAI.AudioResponseFormat](#openaiaudioresponseformat)

### OpenAI.TranscriptionInclude

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `logprobs` |

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
| tokens | array | Array of token IDs for the text content. | Yes |  |

### OpenAI.TranscriptionWord

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| end | number | End time of the word in seconds. | Yes |  |
| start | number | Start time of the word in seconds. | Yes |  |
| word | string | The text content of the word. | Yes |  |

### OpenAI.VadConfig

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prefix_padding_ms | integer | Amount of audio to include before the VAD detected speech (in<br>milliseconds). | No | 300 |
| silence_duration_ms | integer | Duration of silence to detect speech stop (in milliseconds).<br>With shorter values the model will respond more quickly,<br>but may jump in on short pauses from the user. | No | 200 |
| threshold | number | Sensitivity threshold (0.0 to 1.0) for voice activity detection. A<br>higher threshold will require louder audio to activate the model, and<br>thus might perform better in noisy environments. | No | 0.5 |
| type | enum | Must be set to `server_vad` to enable manual chunking using server side VAD.<br>Possible values: `server_vad` | Yes |  |

### OpenAI.VectorStoreFileAttributes

Set of 16 key-value pairs that can be attached to an object. This can be
useful for storing additional information about the object in a structured
format, and querying for objects via API or the dashboard. Keys are strings
with a maximum length of 64 characters. Values are strings with a maximum
length of 512 characters, booleans, or numbers.

**Type**: object


### OpenAI.VoiceIdsShared

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `alloy`<br>`ash`<br>`ballad`<br>`coral`<br>`echo`<br>`fable`<br>`onyx`<br>`nova`<br>`sage`<br>`shimmer`<br>`verse` |

### OpenAI.WebSearchPreviewTool

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| search_context_size | enum | High level guidance for the amount of context window space to use for the search. One of `low`, `medium`, or `high`. `medium` is the default.<br>Possible values: `low`, `medium`, `high` | No |  |
| type | enum | The type of the web search tool. One of `web_search_preview` or `web_search_preview_2025_03_11`.<br>Possible values: `web_search_preview` | Yes |  |
| user_location | object |  | No |  |
| └─ type | [OpenAI.LocationType](#openailocationtype) |  | No |  |

### OpenAI.WebSearchToolCallItemParam

The results of a web search tool call. 


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `web_search_call` | Yes |  |

### OpenAI.WebSearchToolCallItemResource

The results of a web search tool call. 


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| status | enum | The status of the web search tool call.<br>Possible values: `in_progress`, `searching`, `completed`, `failed` | Yes |  |
| type | enum | <br>Possible values: `web_search_call` | Yes |  |

### PineconeChatDataSource

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| parameters | object | The parameter information to control the use of the Pinecone data source. | Yes |  |
| └─ allow_partial_result | boolean | If set to true, the system will allow partial search results to be used and the request will fail if all<br>partial queries fail. If not specified or specified as false, the request will fail if any search query fails. | No | False |
| └─ authentication | object |  | No |  |
|   └─ key | string |  | No |  |
|   └─ type | enum | <br>Possible values: `api_key` | No |  |
| └─ embedding_dependency | object | A representation of a data vectorization source usable as an embedding resource with a data source. | No |  |
|   └─ type | [AzureChatDataSourceVectorizationSourceType](#azurechatdatasourcevectorizationsourcetype) | The differentiating identifier for the concrete vectorization source. | No |  |
| └─ environment | string | The environment name to use with Pinecone. | No |  |
| └─ fields_mapping | object | Field mappings to apply to data used by the Pinecone data source.<br>Note that content field mappings are required for Pinecone. | No |  |
|   └─ content_fields | array |  | No |  |
|   └─ content_fields_separator | string |  | No |  |
|   └─ filepath_field | string |  | No |  |
|   └─ title_field | string |  | No |  |
|   └─ url_field | string |  | No |  |
| └─ in_scope | boolean | Whether queries should be restricted to use of the indexed data. | No |  |
| └─ include_contexts | array | The output context properties to include on the response.<br>By default, citations and intent will be requested. | No | ['citations', 'intent'] |
| └─ index_name | string | The name of the Pinecone database index to use. | No |  |
| └─ max_search_queries | integer | The maximum number of rewritten queries that should be sent to the search provider for a single user message.<br>By default, the system will make an automatic determination. | No |  |
| └─ strictness | integer | The configured strictness of the search relevance filtering.<br>Higher strictness will increase precision but lower recall of the answer. | No |  |
| └─ top_n_documents | integer | The configured number of documents to feature in the query. | No |  |
| type | enum | The discriminated type identifier, which is always 'pinecone'.<br>Possible values: `pinecone` | Yes |  |

### Quality

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `high`<br>`low` |

### ResponseModalities

Output types that you would like the model to generate.
Most models are capable of generating text, which is the default:

`["text"]`

The `gpt-4o-audio-preview` model can also be used to 
generate audio. To request that this model generate 
both text and audio responses, you can use:

`["text", "audio"]`

**Array of**: string


### SpeechGenerationResponseFormat

The supported audio output formats for text-to-speech.

### VideoGeneration

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The time when the video generation was created. | Yes |  |
| height | integer | The height of the video. | Yes |  |
| id | string | The id of the video generation. | Yes |  |
| job_id | string | The id of the video generation job for this video. | Yes |  |
| n_seconds | integer | The duration of the video generation. | Yes |  |
| object | enum | <br>Possible values: `video.generation` | Yes |  |
| prompt | string | The prompt for this video generation. | Yes |  |
| width | integer | The width of the video. | Yes |  |

### VideoGenerationJob

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The time when the job was created. | Yes |  |
| expires_at | integer | The Unix timestamp (in seconds) for when the job gets deleted from the server. The video content and metadata of the job should be stored before this date to avoid data loss. The default and maximum range is 24 hours from the job completion timestamp. | No | |
| failure_reason | string (see valid models below) |  | No |  |
| finished_at | integer | The time when the job finished with all video generations. | No |  |
| generations | array | The generated videos for this job. The number depends on the given n_variants and the creation success of the generations. | No |  |
| height | integer | The height of the video. | Yes |  |
| id | string | The id of the job. | Yes |  |
| model | string | The name of the deployment to use for this video generation job. | Yes |  |
| n_seconds | integer | The duration of the video generation job. | Yes |  |
| n_variants | integer | The number of videos to create as variants for this video generation job. | Yes |  |
| object | enum | <br>Possible values: `video.generation.job` | Yes |  |
| prompt | string | The prompt for this video generation job. | Yes |  |
| status | object |  | Yes |  |
| width | integer | The height of the video. | Yes |  |

### VideoGenerationJobList

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| first_id | string |  | No |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

