---
title: Azure OpenAI new v1 preview inference API documentation
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Latest v1 preview data plane inference documentation generated from OpenAPI 3.0 spec
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 08/04/2025
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
| input | string | The text to generate audio for. The maximum length is 4096 characters. | Yes |  |
| instructions | string | Control the voice of your generated audio with additional instructions. Does not work with `tts-1` or `tts-1-hd`. | No |  |
| model | string | The model to use for this text-to-speech request. | Yes |  |
| response_format | object | The supported audio output formats for text-to-speech. | No |  |
| speed | number | The speed of speech for generated audio. Values are valid in the range from 0.25 to 4.0, with 1.0 the default and higher values corresponding to faster speech. | No | 1 |
| stream_format | enum | The format to stream the audio in. Supported formats are `sse` and `audio`. `sse` is not supported for `tts-1` or `tts-1-hd`.<br>Possible values: `sse`, `audio` | No |  |
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
| chunking_strategy | object |  | No |  |
| └─ prefix_padding_ms | integer | Amount of audio to include before the VAD detected speech (in<br>milliseconds). | No | 300 |
| └─ silence_duration_ms | integer | Duration of silence to detect speech stop (in milliseconds).<br>With shorter values the model will respond more quickly,<br>but may jump in on short pauses from the user. | No | 200 |
| └─ threshold | number | Sensitivity threshold (0.0 to 1.0) for voice activity detection. A<br>higher threshold will require louder audio to activate the model, and<br>thus might perform better in noisy environments. | No | 0.5 |
| └─ type | enum | Must be set to `server_vad` to enable manual chunking using server side VAD.<br>Possible values: `server_vad` | No |  |
| file | string |  | Yes |  |
| filename | string | The optional filename or descriptive identifier to associate with with the audio data. | No |  |
| include[] | array | Additional information to include in the transcription response.<br>`logprobs` will return the log probabilities of the tokens in the<br>response to understand the model's confidence in the transcription.<br>`logprobs` only works with response_format set to `json` and only with<br>the models `gpt-4o-transcribe`, `gpt-4o-transcribe-diarize`, and `gpt-4o-mini-transcribe`. | No |  |
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

## Create translation

```HTTP
POST {endpoint}/openai/v1/audio/translations?api-version=preview
```

Gets English language transcribed text and associated metadata from provided spoken audio data.

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
| file | string |  | Yes |  |
| filename | string | The optional filename or descriptive identifier to associate with with the audio data | No |  |
| model | string | The model to use for this translation request. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should be in English. | No |  |
| response_format | object |  | No |  |
| temperature | number | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use [log probability](https://en.wikipedia.org/wiki/Log_probability) to automatically increase the temperature until certain thresholds are hit. | No | 0 |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureAudioTranslationResponse](#azureaudiotranslationresponse) | |
|text/plain | string | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

### Example

Gets English language transcribed text and associated metadata from provided spoken audio data.

```HTTP
POST {endpoint}/openai/v1/audio/translations?api-version=preview

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

## Create chatcompletion

```HTTP
POST {endpoint}/openai/v1/chat/completions?api-version=preview
```


Creates a chat completion.
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
| modalities | object | Output types that you would like the model to generate.<br>Most models are capable of generating text, which is the default:<br><br>`["text"]`<br><br>The `gpt-4o-audio-preview` model can also be used to generate audio. To request that this model generate<br>both text and audio responses, you can use:<br><br>`["text", "audio"]` | No |  |
| model | string | The model deployment identifier to use for the chat completion request. | Yes |  |
| n | integer | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs. | No | 1 |
| parallel_tool_calls | object | Whether to enable parallel function calling during tool use. | No |  |
| prediction | object | Base representation of predicted output from a model. | No |  |
| └─ type | [OpenAI.ChatOutputPredictionType](#openaichatoutputpredictiontype) |  | No |  |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>whether they appear in the text so far, increasing the model's likelihood<br>to talk about new topics. | No | 0 |
| reasoning_effort | object | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| response_format | object |  | No |  |
| └─ type | enum | <br>Possible values: `text`, `json_object`, `json_schema` | No |  |
| seed | integer | This feature is in Beta.<br>If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br>Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | object | Not supported with latest reasoning models `o3` and `o4-mini`.<br><br>Up to 4 sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| store | boolean | Whether or not to store the output of this chat completion request for<br>use in model distillation or evals products. | No | False |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using server-sent events. | No | False |
| stream_options | object | Options for streaming response. Only set this when you set `stream: true`. | No |  |
| └─ include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array.<br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| tool_choice | [OpenAI.ChatCompletionToolChoiceOption](#openaichatcompletiontoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tool and instead generates a message.<br>`auto` means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools.<br>Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.<br><br>`none` is the default when no tools are present. `auto` is the default if tools are present. | No |  |
| tools | array | A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
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

## Create embedding

```HTTP
POST {endpoint}/openai/v1/embeddings?api-version=preview
```

Creates an embedding vector representing the input text.

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

## List evals

```HTTP
GET {endpoint}/openai/v1/evals?api-version=preview
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

## Createeval

```HTTP
POST {endpoint}/openai/v1/evals?api-version=preview
```


Create the structure of an evaluation that can be used to test a model's
performance.

An evaluation is a set of testing criteria and a datasource. After
creating an evaluation, you can run it on different models and model
parameters. We support several types of graders and datasources.



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
GET {endpoint}/openai/v1/evals/{eval_id}?api-version=preview
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
POST {endpoint}/openai/v1/evals/{eval_id}?api-version=preview
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
DELETE {endpoint}/openai/v1/evals/{eval_id}?api-version=preview
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
GET {endpoint}/openai/v1/evals/{eval_id}/runs?api-version=preview
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
POST {endpoint}/openai/v1/evals/{eval_id}/runs?api-version=preview
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
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}?api-version=preview
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
POST {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}?api-version=preview
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

## Deleteevalrun

```HTTP
DELETE {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}?api-version=preview
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
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items?api-version=preview
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
GET {endpoint}/openai/v1/evals/{eval_id}/runs/{run_id}/output_items/{output_item_id}?api-version=preview
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
POST {endpoint}/openai/v1/files?api-version=preview
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
POST {endpoint}/openai/v1/files?api-version=preview

```

## List files

```HTTP
GET {endpoint}/openai/v1/files?api-version=preview
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
GET {endpoint}/openai/v1/files/{file_id}?api-version=preview
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
DELETE {endpoint}/openai/v1/files/{file_id}?api-version=preview
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
GET {endpoint}/openai/v1/files/{file_id}/content?api-version=preview
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

## Rungrader

```HTTP
POST {endpoint}/openai/v1/fine_tuning/alpha/graders/run?api-version=preview
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
POST {endpoint}/openai/v1/fine_tuning/alpha/graders/validate?api-version=preview
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
POST {endpoint}/openai/v1/fine_tuning/jobs?api-version=preview
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
| training_file | string | The ID of an uploaded file that contains training data.Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose `fine-tune`.<br><br>The contents of the file should differ depending on if the model uses the chat, completions format, or if the fine-tuning method uses the preference format. | Yes |  |
| validation_file | string | The ID of an uploaded file that contains validation data.<br><br>If you provide this file, the data is used to generate validation<br>metrics periodically during fine-tuning. These metrics can be viewed in<br>the fine-tuning results file.<br>The same data should not be present in both train and validation files.<br><br>Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`. | No |  |

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
GET {endpoint}/openai/v1/fine_tuning/jobs?api-version=preview
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
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}?api-version=preview
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
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel?api-version=preview
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
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints?api-version=preview
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
GET {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/events?api-version=preview
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
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/pause?api-version=preview
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
POST {endpoint}/openai/v1/fine_tuning/jobs/{fine_tuning_job_id}/resume?api-version=preview
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

## Create image edit

```HTTP
POST {endpoint}/openai/v1/images/edits?api-version=preview
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
| background | enum | Allows to set transparency for the background of the generated image(s).<br>This parameter is only supported for `gpt-image-1`. Must be one of<br>`transparent`, `opaque` or `auto` (default value). When `auto` is used, the<br>model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it<br>should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| image | string or array |  | Yes |  |
| mask | string |  | No |  |
| model | string | The model deployment to use for the image edit operation. | Yes |  |
| n | integer | The number of images to generate. Must be between 1 and 10. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter<br>is only supported for `gpt-image-1` with the `webp` or `jpeg` output<br>formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is<br>only supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.<br>The default value is `png`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 1000 characters for `dall-e-2`, and 32000 characters for `gpt-image-1`. | Yes |  |
| quality | enum | The quality of the image that will be generated. `high`, `medium` and `low` are only supported for `gpt-image-1`. `dall-e-2` only supports `standard` quality. Defaults to `auto`.<br>Possible values: `standard`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which the generated images are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter is only supported for `dall-e-2`, as `gpt-image-1` will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`, and one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`.<br>Possible values: `256x256`, `512x512`, `1024x1024`, `1536x1024`, `1024x1536`, `auto` | No |  |
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

## Createimage

```HTTP
POST {endpoint}/openai/v1/images/generations?api-version=preview
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

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Allows to set transparency for the background of the generated image(s).<br>This parameter is only supported for `gpt-image-1`. Must be one of<br>`transparent`, `opaque` or `auto` (default value). When `auto` is used, the<br>model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it<br>should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| model | string | The model deployment to use for the image generation. | Yes |  |
| moderation | enum | Control the content-moderation level for images generated by `gpt-image-1`. Must be either `low` for less restrictive filtering or `auto` (default value).<br>Possible values: `low`, `auto` | No |  |
| n | integer | The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter is only supported for `gpt-image-1` with the `webp` or `jpeg` output formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is only supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters for `gpt-image-1`, 1000 characters for `dall-e-2` and 4000 characters for `dall-e-3`. | Yes |  |
| quality | enum | The quality of the image that will be generated.<br><br>- `auto` (default value) will automatically select the best quality for the given model.<br>- `high`, `medium` and `low` are supported for `gpt-image-1`.<br>- `hd` and `standard` are supported for `dall-e-3`.<br>- `standard` is the only option for `dall-e-2`.<br>Possible values: `standard`, `hd`, `low`, `medium`, `high`, `auto` | No |  |
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

## List models

```HTTP
GET {endpoint}/openai/v1/models?api-version=preview
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
GET {endpoint}/openai/v1/models/{model}?api-version=preview
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

## Create response

```HTTP
POST {endpoint}/openai/v1/responses?api-version=preview
```


Creates a model response.
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
| background | boolean | Whether to run the model response in the background.| No | False |
| include | array | Specify additional output data to include in the model response. Currently<br>supported values are:<br>- `code_interpreter_call.outputs`: Includes the outputs of python code execution<br>  in code interpreter tool call items.<br>- `computer_call_output.output.image_url`: Include image urls from the computer call output.<br>- `file_search_call.results`: Include the search results of<br>  the file search tool call.<br>- `message.input_image.image_url`: Include image urls from the input message.<br>- `message.output_text.logprobs`: Include logprobs with assistant messages.<br>- `reasoning.encrypted_content`: Includes an encrypted version of reasoning<br>  tokens in reasoning item outputs. This enables reasoning items to be used in<br>  multi-turn conversations when using the Responses API statelessly (like<br>  when the `store` parameter is set to `false`, or when an organization is<br>  enrolled in the zero data retention program). | No |  |
| input | string or array |  | No |  |
| instructions | string | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string | The model deployment to use for the creation of this response. | Yes |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| prompt | object | Reference to a prompt template and its variables. | No |  |
| └─ id | string | The unique identifier of the prompt template to use. | No |  |
| └─ variables | [OpenAI.ResponsePromptVariables](#openairesponsepromptvariables) | Optional map of values to substitute in for variables in your<br>prompt. The substitution values can either be strings, or other<br>Response input types like images or files. | No |  |
| └─ version | string | Optional version of the prompt template. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| store | boolean | Whether to store the generated model response for later retrieval via<br>API. | No | True |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). | No | False |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities, like file search.<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>  enabling the model to call your own code. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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

## List input items

```HTTP
GET {endpoint}/openai/v1/responses/{response_id}/input_items?api-version=preview
```


Returns a list of input items for a given response.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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

## List vector stores

```HTTP
GET {endpoint}/openai/v1/vector_stores?api-version=preview
```

Returns a list of vector stores.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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
|application/json | [OpenAI.ListVectorStoresResponse](#openailistvectorstoresresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Create vector store

```HTTP
POST {endpoint}/openai/v1/vector_stores?api-version=preview
```

Creates a vector store.

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
| chunking_strategy | object | The default strategy. This strategy currently uses a `max_chunk_size_tokens` of `800` and `chunk_overlap_tokens` of `400`. | No |  |
| └─ static | [OpenAI.StaticChunkingStrategy](#openaistaticchunkingstrategy) |  | No |  |
| └─ type | enum | Always `static`.<br>Possible values: `static` | No |  |
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| file_ids | array | A list of file IDs that the vector store should use. Useful for tools like `file_search` that can access files. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the vector store. | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreObject](#openaivectorstoreobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

### Examples

Example file not found: ./examples/vector_stores.json

## Get vector store

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}?api-version=preview
```

Retrieves a vector store.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to retrieve. |

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
|application/json | [OpenAI.VectorStoreObject](#openaivectorstoreobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Modify vector store

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}?api-version=preview
```

Modifies a vector store.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to modify. |

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
| expires_after | object | The expiration policy for a vector store. | No |  |
| └─ anchor | enum | Anchor timestamp after which the expiration policy applies. Supported anchors: `last_active_at`.<br>Possible values: `last_active_at` | No |  |
| └─ days | integer | The number of days after the anchor time that the vector store will expire. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the vector store. | No |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreObject](#openaivectorstoreobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Delete vector store

```HTTP
DELETE {endpoint}/openai/v1/vector_stores/{vector_store_id}?api-version=preview
```

Delete a vector store.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store to delete. |

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
|application/json | [OpenAI.DeleteVectorStoreResponse](#openaideletevectorstoreresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Create vector store file batch

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches?api-version=preview
```

Create a vector store file batch.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store for which to create a file batch. |

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
| attributes | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. | No |  |
| file_ids | array | A list of file IDs that the vector store should use. Useful for tools like `file_search` that can access files. | Yes |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileBatchObject](#openaivectorstorefilebatchobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Get vector store file batch

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches/{batch_id}?api-version=preview
```

Retrieves a vector store file batch.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file batch belongs to. |
| batch_id | path | Yes | string | The ID of the file batch being retrieved. |

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
|application/json | [OpenAI.VectorStoreFileBatchObject](#openaivectorstorefilebatchobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Cancel vector store file batch

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/cancel?api-version=preview
```

Cancel a vector store file batch. This attempts to cancel the processing of files in this batch as soon as possible.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file batch belongs to. |
| batch_id | path | Yes | string | The ID of the file batch to cancel. |

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
|application/json | [OpenAI.VectorStoreFileBatchObject](#openaivectorstorefilebatchobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## List files in vector store batch

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/files?api-version=preview
```

Returns a list of vector store files in a batch.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file batch belongs to. |
| batch_id | path | Yes | string | The ID of the file batch that the files belong to. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| filter | query | No |  | Filter by file status. One of `in_progress`, `completed`, `failed`, `cancelled`. |

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
|application/json | [OpenAI.ListVectorStoreFilesResponse](#openailistvectorstorefilesresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## List vector store files

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/files?api-version=preview
```

Returns a list of vector store files.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the files belong to. |
| limit | query | No | integer | A limit on the number of objects to be returned. Limit can range between 1 and 100, and the<br>default is 20. |
| order | query | No | string<br>Possible values: `asc`, `desc` | Sort order by the `created_at` timestamp of the objects. `asc` for ascending order and`desc`<br>for descending order. |
| after | query | No | string | A cursor for use in pagination. `after` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include after=obj_foo in order to fetch the next page of the list. |
| before | query | No | string | A cursor for use in pagination. `before` is an object ID that defines your place in the list.<br>For instance, if you make a list request and receive 100 objects, ending with obj_foo, your<br>subsequent call can include before=obj_foo in order to fetch the previous page of the list. |
| filter | query | No |  | Filter by file status. One of `in_progress`, `completed`, `failed`, `cancelled`. |

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
|application/json | [OpenAI.ListVectorStoreFilesResponse](#openailistvectorstorefilesresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Create vector store file

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/files?api-version=preview
```

Create a vector store file by attaching a file to a vector store.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store for which to create a File. |

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
| attributes | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. | No |  |
| file_id | string | A file ID that the vector store should use. Useful for tools like `file_search` that can access files. | Yes |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileObject](#openaivectorstorefileobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Get vector store file

```HTTP
GET {endpoint}/openai/v1/vector_stores/{vector_store_id}/files/{file_id}?api-version=preview
```

Retrieves a vector store file.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file belongs to. |
| file_id | path | Yes | string | The ID of the file being retrieved. |

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
|application/json | [OpenAI.VectorStoreFileObject](#openaivectorstorefileobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Update vector store file attributes

```HTTP
POST {endpoint}/openai/v1/vector_stores/{vector_store_id}/files/{file_id}?api-version=preview
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string |  |
| file_id | path | Yes | string |  |

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
| attributes | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | Yes |  |

### Responses

**Status Code:** 200

**Description**: The request has succeeded. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [OpenAI.VectorStoreFileObject](#openaivectorstorefileobject) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Delete vector store file

```HTTP
DELETE {endpoint}/openai/v1/vector_stores/{vector_store_id}/files/{file_id}?api-version=preview
```

Delete a vector store file. This will remove the file from the vector store but the file itself will not be deleted. To delete the file, use the delete file endpoint.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| vector_store_id | path | Yes | string | The ID of the vector store that the file belongs to. |
| file_id | path | Yes | string | The ID of the file to delete. |

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
|application/json | [OpenAI.DeleteVectorStoreFileResponse](#openaideletevectorstorefileresponse) | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureErrorResponse](#azureerrorresponse) | |

## Video generation jobs - Create

```HTTP
POST {endpoint}/openai/v1/video/generations/jobs?api-version=preview
```


Creates a new video generation job.
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
| height | integer | The height of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |
| model | string | The name of the deployment to use for this request. | Yes |  |
| n_seconds | integer | The duration of the video generation job. Must be between 1 and 20 seconds. | No | 5 |
| n_variants | integer | The number of videos to create as variants for this job. Must be between 1 and 5. Smaller dimensions allow more variants. | No | 1 |
| prompt | string | The prompt for this video generation job. | Yes |  |
| width | integer | The width of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |
### Request Body

**Content-Type**: multipart/form-data

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| files | array |  | Yes |  |
| height | integer | The height of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |
| inpaint_items | array | Optional inpainting items for this video generation job. | No |  |
| model | string | The name of the deployment to use for this request. | Yes |  |
| n_seconds | integer | The duration of the video generation job. Must be between 1 and 20 seconds. | No | 5 |
| n_variants | integer | The number of videos to create as variants for this job. Must be between 1 and 5. Smaller dimensions allow more variants. | No | 1 |
| prompt | string | The prompt for this video generation job. | Yes |  |
| width | integer | The width of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |

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

Example file not found: ./examples/create_video_generation_job_simple.json

## Video generation jobs - List

```HTTP
GET {endpoint}/openai/v1/video/generations/jobs?api-version=preview
```


Lists video generation jobs.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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

### Examples

Example file not found: ./examples/get_video_generation_job_list.json

## Video generation jobs - Get

```HTTP
GET {endpoint}/openai/v1/video/generations/jobs/{job-id}?api-version=preview
```


Retrieves properties of a video generation job.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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

### Examples

Example file not found: ./examples/get_video_generation_job.json

## Video generation jobs - Delete

```HTTP
DELETE {endpoint}/openai/v1/video/generations/jobs/{job-id}?api-version=preview
```


Deletes a video generation job.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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


Retrieves a video generation by ID.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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

### Examples

Example file not found: ./examples/get_video_generation.json

## Video generations - Retrieve thumbnail

```HTTP
GET {endpoint}/openai/v1/video/generations/{generation-id}/content/thumbnail?api-version=preview
```


Retrieves a thumbnail of the generated video content.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
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
|image/jpg | string | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Video generations - Retrieve video content

```HTTP
GET {endpoint}/openai/v1/video/generations/{generation-id}/content/video?api-version=preview
```


Retrieves the generated video content.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |
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
|video/mp4 | string | |

**Status Code:** default

**Description**: An unexpected error response. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [AzureOpenAIVideoGenerationErrorResponse](#azureopenaivideogenerationerrorresponse) | |

## Video generations - Retrieve videocontent headers only

```HTTP
HEAD {endpoint}/openai/v1/video/generations/{generation-id}/content/video?api-version=preview
```


Retrieves headers for the the generated video content.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Azure AI Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |
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
| tokens | array | The token IDs matching the translated text in this audio segment. | Yes |  |

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
| segments | array | A collection of information about the timing, probabilities, and other detail of each processed audio segment. | No |  |
| task | object | Defines the possible descriptors for available audio operation responses. | No |  |
| text | string | The transcribed text for the provided audio data. | Yes |  |
| words | array | A collection of information about the timing of each processed word. | No |  |

### AzureAudioTranslationResponse

Result information for an operation that translated spoken audio into written text.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| duration | number | The total duration of the audio processed to produce accompanying translation information. | No |  |
| language | string | The spoken language that was detected in the translated audio data.<br>This is expressed as a two-letter ISO-639-1 language code like 'en' or 'fr'. | No |  |
| segments | array | A collection of information about the timing, probabilities, and other detail of each processed audio segment. | No |  |
| task | object | Defines the possible descriptors for available audio operation responses. | No |  |
| text | string | The translated text for the provided audio data. | Yes |  |

### AzureChatCompletionResponseMessage

The extended response model component for chat completion response messages on the Azure OpenAI service.
This model adds support for chat message context, used by the On Your Data feature for intent, citations, and other
information related to retrieval-augmented generation performed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| annotations | array | Annotations for the message, when applicable, as when using the<br> web search tool. | No |  |
| audio | object | If the audio output modality is requested, this object contains data<br>about the audio response from the model.  | No |  |
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

### AzureContentFilterCustomTopicResult

A collection of true/false filtering results for configured custom topics.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| details | array | The pairs of individual topic IDs and whether they are detected. | No |  |
| filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | Yes |  |

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
| custom_topics | object | A collection of true/false filtering results for configured custom topics. | No |  |
| └─ details | array | The pairs of individual topic IDs and whether they are detected. | No |  |
| └─ filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | No |  |
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
| custom_topics | object | A collection of true/false filtering results for configured custom topics. | No |  |
| └─ details | array | The pairs of individual topic IDs and whether they are detected. | No |  |
| └─ filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | No |  |
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
| └─ custom_topics | object | A collection of true/false filtering results for configured custom topics. | No |  |
|   └─ details | array | The pairs of individual topic IDs and whether they are detected. | No |  |
|   └─ filtered | boolean | A value indicating whether any of the detailed topics resulted in a filtering action. | No |  |
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
| modalities | object | Output types that you would like the model to generate.<br>Most models are capable of generating text, which is the default:<br><br>`["text"]`<br><br>The `gpt-4o-audio-preview` model can also be used to generate audio. To request that this model generate<br>both text and audio responses, you can use:<br><br>`["text", "audio"]` | No |  |
| model | string | The model deployment identifier to use for the chat completion request. | Yes |  |
| n | integer | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs. | No | 1 |
| parallel_tool_calls | object | Whether to enable parallel function calling during tool use. | No |  |
| prediction | object | Base representation of predicted output from a model. | No |  |
| └─ type | [OpenAI.ChatOutputPredictionType](#openaichatoutputpredictiontype) |  | No |  |
| presence_penalty | number | Number between -2.0 and 2.0. Positive values penalize new tokens based on<br>whether they appear in the text so far, increasing the model's likelihood<br>to talk about new topics. | No | 0 |
| reasoning_effort | object | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| response_format | object |  | No |  |
| └─ type | enum | <br>Possible values: `text`, `json_object`, `json_schema` | No |  |
| seed | integer | This feature is in Beta.<br>If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.<br>Determinism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend. | No |  |
| stop | object | Not supported with latest reasoning models `o3` and `o4-mini`.<br><br>Up to 4 sequences where the API will stop generating further tokens. The<br>returned text will not contain the stop sequence. | No |  |
| store | boolean | Whether or not to store the output of this chat completion request for<br>use in model distillation or evals products. | No | False |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using server-sent events. | No | False |
| stream_options | object | Options for streaming response. Only set this when you set `stream: true`. | No |  |
| └─ include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array.<br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| tool_choice | [OpenAI.ChatCompletionToolChoiceOption](#openaichatcompletiontoolchoiceoption) | Controls which (if any) tool is called by the model.<br>`none` means the model will not call any tool and instead generates a message.<br>`auto` means the model can pick between generating a message or calling one or more tools.<br>`required` means the model must call one or more tools.<br>Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.<br><br>`none` is the default when no tools are present. `auto` is the default if tools are present. | No |  |
| tools | array | A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for. A max of 128 functions are supported. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
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
| content_filter_results | [AzureContentFilterResultForChoice](#azurecontentfilterresultforchoice) | A content filter result for a single response item produced by a generative AI system. | No |  |
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

### AzureCreateEmbeddingRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| dimensions | integer | The number of dimensions the resulting output embeddings should have. Only supported in `text-embedding-3` and later models. | No |  |
| encoding_format | enum | The format to return the embeddings in. Can be either `float` or [`base64`](https://pypi.org/project/pybase64/).<br>Possible values: `float`, `base64` | No |  |
| input | string or array |  | Yes |  |
| model | string | The model to use for the embedding request. | Yes |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateFileRequestMultiPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | object |  | Yes |  |
| └─ anchor | [AzureFileExpiryAnchor](#azurefileexpiryanchor) |  | No |  |
| └─ seconds | integer |  | No |  |
| file | string |  | Yes |  |
| purpose | enum | The intended purpose of the uploaded file. One of: - `assistants`: Used in the Assistants API - `batch`: Used in the Batch API - `fine-tune`: Used for fine-tuning - `evals`: Used for eval data sets<br>Possible values: `assistants`, `batch`, `fine-tune`, `evals` | Yes |  |

### AzureCreateImageEditRequestMultiPart

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Allows to set transparency for the background of the generated image(s).<br>This parameter is only supported for `gpt-image-1`. Must be one of<br>`transparent`, `opaque` or `auto` (default value). When `auto` is used, the<br>model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it<br>should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| image | string or array |  | Yes |  |
| mask | string |  | No |  |
| model | string | The model deployment to use for the image edit operation. | Yes |  |
| n | integer | The number of images to generate. Must be between 1 and 10. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter<br>is only supported for `gpt-image-1` with the `webp` or `jpeg` output<br>formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is<br>only supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.<br>The default value is `png`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 1000 characters for `dall-e-2`, and 32000 characters for `gpt-image-1`. | Yes |  |
| quality | enum | The quality of the image that will be generated. `high`, `medium` and `low` are only supported for `gpt-image-1`. `dall-e-2` only supports `standard` quality. Defaults to `auto`.<br>Possible values: `standard`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which the generated images are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter is only supported for `dall-e-2`, as `gpt-image-1` will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`, and one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`.<br>Possible values: `256x256`, `512x512`, `1024x1024`, `1536x1024`, `1024x1536`, `auto` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateImageRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Allows to set transparency for the background of the generated image(s).<br>This parameter is only supported for `gpt-image-1`. Must be one of<br>`transparent`, `opaque` or `auto` (default value). When `auto` is used, the<br>model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it<br>should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| model | string | The model deployment to use for the image generation. | Yes |  |
| moderation | enum | Control the content-moderation level for images generated by `gpt-image-1`. Must be either `low` for less restrictive filtering or `auto` (default value).<br>Possible values: `low`, `auto` | No |  |
| n | integer | The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter is only supported for `gpt-image-1` with the `webp` or `jpeg` output formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is only supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters for `gpt-image-1`, 1000 characters for `dall-e-2` and 4000 characters for `dall-e-3`. | Yes |  |
| quality | enum | The quality of the image that will be generated.<br><br>- `auto` (default value) will automatically select the best quality for the given model.<br>- `high`, `medium` and `low` are supported for `gpt-image-1`.<br>- `hd` and `standard` are supported for `dall-e-3`.<br>- `standard` is the only option for `dall-e-2`.<br>Possible values: `standard`, `hd`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which generated images with `dall-e-2` and `dall-e-3` are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter isn't supported for `gpt-image-1` which will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`, one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`, and one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3`.<br>Possible values: `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `256x256`, `512x512`, `1792x1024`, `1024x1792` | No |  |
| style | enum | The style of the generated images. This parameter is only supported for `dall-e-3`. Must be one of `vivid` or `natural`. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the model to produce more natural, less hyper-real looking images.<br>Possible values: `vivid`, `natural` | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |

### AzureCreateResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean | Whether to run the model response in the background.| No | False |
| include | array | Specify additional output data to include in the model response. Currently<br>supported values are:<br>- `code_interpreter_call.outputs`: Includes the outputs of python code execution<br>  in code interpreter tool call items.<br>- `computer_call_output.output.image_url`: Include image urls from the computer call output.<br>- `file_search_call.results`: Include the search results of<br>  the file search tool call.<br>- `message.input_image.image_url`: Include image urls from the input message.<br>- `message.output_text.logprobs`: Include logprobs with assistant messages.<br>- `reasoning.encrypted_content`: Includes an encrypted version of reasoning<br>  tokens in reasoning item outputs. This enables reasoning items to be used in<br>  multi-turn conversations when using the Responses API statelessly (like<br>  when the `store` parameter is set to `false`, or when an organization is<br>  enrolled in the zero data retention program). | No |  |
| input | string or array |  | No |  |
| instructions | string | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| model | string | The model deployment to use for the creation of this response. | Yes |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| prompt | object | Reference to a prompt template and its variables. | No |  |
| └─ id | string | The unique identifier of the prompt template to use. | No |  |
| └─ variables | [OpenAI.ResponsePromptVariables](#openairesponsepromptvariables) | Optional map of values to substitute in for variables in your<br>prompt. The substitution values can either be strings, or other<br>Response input types like images or files. | No |  |
| └─ version | string | Optional version of the prompt template. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| store | boolean | Whether to store the generated model response for later retrieval via<br>API. | No | True |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). | No | False |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No | 1 |
| text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You <br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities, like file search.<br>- **Function calls (custom tools)**: Functions that are defined by you,<br>  enabling the model to call your own code. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No | 1 |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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
| stream_format | enum | The format to stream the audio in. Supported formats are `sse` and `audio`. `sse` is not supported for `tts-1` or `tts-1-hd`.<br>Possible values: `sse`, `audio` | No |  |
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
| include[] | array | Additional information to include in the transcription response.<br>`logprobs` will return the log probabilities of the tokens in the<br>response to understand the model's confidence in the transcription.<br>`logprobs` only works with response_format set to `json` and only with<br>the models `gpt-4o-transcribe`, `gpt-4o-transcribe-diarize`, and `gpt-4o-mini-transcribe`. | No |  |
| language | string | The language of the input audio. Supplying the input language in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format will improve accuracy and latency. | No |  |
| model | string | The model to use for this transcription request. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language. | No |  |
| response_format | object |  | No |  |
| stream | boolean | If set to true, the model response data will be streamed to the client<br>as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). Note: Streaming is not supported for the `whisper-1` model and will be ignored. | No | False |
| temperature | number | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use [log probability](https://en.wikipedia.org/wiki/Log_probability) to automatically increase the temperature until certain thresholds are hit. | No | 0 |
| timestamp_granularities[] | array | The timestamp granularities to populate for this transcription. `response_format` must be set `verbose_json` to use timestamp granularities. Either or both of these options are supported: `word`, or `segment`. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency. | No | ['segment'] |

### AzureCreateTranslationRequestMultiPart

The configuration information for an audio transcription request.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| file | string |  | Yes |  |
| filename | string | The optional filename or descriptive identifier to associate with with the audio data | No |  |
| model | string | The model to use for this translation request. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should be in English. | No |  |
| response_format | object |  | No |  |
| temperature | number | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use [log probability](https://en.wikipedia.org/wiki/Log_probability) to automatically increase the temperature until certain thresholds are hit. | No | 0 |

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

### AzureImage

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| b64_json | string | The base64-encoded JSON of the generated image. Default value for `gpt-image-1`, and only present if `response_format` is set to `b64_json` for `dall-e-2` and `dall-e-3`. | No |  |
| content_filter_results | [AzureContentFilterImageResponseResults](#azurecontentfilterimageresponseresults) | A content filter result for an image generation operation's output response content. | Yes |  |
| prompt_filter_results | [AzureContentFilterImagePromptResults](#azurecontentfilterimagepromptresults) | A content filter result for an image generation operation's input request content. | Yes |  |
| revised_prompt | string | For `dall-e-3` only, the revised prompt that was used to generate the image. | No |  |
| url | string | When using `dall-e-2` or `dall-e-3`, the URL of the generated image if `response_format` is set to `url` (default value). Unsupported for `gpt-image-1`. | No |  |

### AzureImagesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | The background parameter used for the image generation. Either `transparent` or `opaque`.<br>Possible values: `transparent`, `opaque` | No |  |
| created | integer | The Unix timestamp (in seconds) of when the image was created. | Yes |  |
| data | array |  | No |  |
| output_format | enum | The output format of the image generation. Either `png`, `webp`, or `jpeg`.<br>Possible values: `png`, `webp`, `jpeg` | No |  |
| quality | enum | The quality of the image generated. Either `low`, `medium`, or `high`.<br>Possible values: `low`, `medium`, `high` | No |  |
| size | enum | The size of the image generated. Either `1024x1024`, `1024x1536`, or `1536x1024`.<br>Possible values: `1024x1024`, `1024x1536`, `1536x1024` | No |  |
| usage | object | For `gpt-image-1` only, the token usage information for the image generation. | No |  |
| └─ input_tokens | integer | The number of tokens (images and text) in the input prompt. | No |  |
| └─ input_tokens_details | object | The input tokens detailed information for the image generation. | No |  |
|   └─ image_tokens | integer | The number of image tokens in the input prompt. | No |  |
|   └─ text_tokens | integer | The number of text tokens in the input prompt. | No |  |
| └─ output_tokens | integer | The number of image tokens in the output image. | No |  |
| └─ total_tokens | integer | The total number of tokens (images and text) used for the image generation. | No |  |

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

### AzureOpenAIVideoGenerationErrorResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The distinct, machine-generated identifier for the error. | No |  |
| inner_error | object | If applicable, an upstream error that originated this error. | No |  |
| └─ code | enum | The code associated with the inner error.<br>Possible values: `ResponsibleAIPolicyViolation` | No |  |
| └─ error_details |  | The content filter result details associated with the inner error. | No |  |
| └─ revised_prompt | string | If applicable, the modified prompt used for generation. | No |  |
| message | string | A human-readable message associated with the error. | No |  |
| param | string | If applicable, the request input parameter associated with the error | No |  |
| type | string | If applicable, the input line number associated with the error. | No |  |

### AzureResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | boolean | Whether to run the model response in the background.| No | False |
| created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| error | object | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ code | [OpenAI.ResponseErrorCode](#openairesponseerrorcode) | The error code for the response. | No |  |
| └─ message | string | A human-readable description of the error. | No |  |
| id | string | Unique identifier for this Response. | Yes |  |
| incomplete_details | object | Details about why the response is incomplete. | Yes |  |
| └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| instructions | string or array |  | Yes |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| model | string | The model used to generate this response. | Yes |  |
| object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| prompt | object | Reference to a prompt template and its variables. | No |  |
| └─ id | string | The unique identifier of the prompt template to use. | No |  |
| └─ variables | [OpenAI.ResponsePromptVariables](#openairesponsepromptvariables) | Optional map of values to substitute in for variables in your<br>prompt. The substitution values can either be strings, or other<br>Response input types like images or files. | No |  |
| └─ version | string | Optional version of the prompt template. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | Yes |  |
| text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | Yes |  |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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

### ChatCompletionMessageToolCallsItem

The tool calls generated by the model, such as function calls.

**Array of**: [OpenAI.ChatCompletionMessageToolCall](#openaichatcompletionmessagetoolcall)


### CreateVideoGenerationRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| height | integer | The height of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |
| model | string | The name of the deployment to use for this request. | Yes |  |
| n_seconds | integer | The duration of the video generation job. Must be between 1 and 20 seconds. | No | 5 |
| n_variants | integer | The number of videos to create as variants for this job. Must be between 1 and 5. Smaller dimensions allow more variants. | No | 1 |
| prompt | string | The prompt for this video generation job. | Yes |  |
| width | integer | The width of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |

### CreateVideoGenerationWithMediaRequestMultiPart

The properties of a video generation job request with media files.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| files | array |  | Yes |  |
| height | integer | The height of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |
| inpaint_items | array | Optional inpainting items for this video generation job. | No |  |
| model | string | The name of the deployment to use for this request. | Yes |  |
| n_seconds | integer | The duration of the video generation job. Must be between 1 and 20 seconds. | No | 5 |
| n_variants | integer | The number of videos to create as variants for this job. Must be between 1 and 5. Smaller dimensions allow more variants. | No | 1 |
| prompt | string | The prompt for this video generation job. | Yes |  |
| width | integer | The width of the video. The following dimensions are supported: 480x480, 854x480, 720x720, 1280x720, 1080x1080 and 1920x1080 in both landscape and portrait orientations. | Yes |  |

### CropBounds

The crop bounds for an inpainting item.
This specifies the area of the media item that should be used for inpainting.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bottom_fraction | number | The bottom boundary of the crop box specified as fraction of the height of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the height of the original media item. | No | 1 |
| left_fraction | number | The left boundary of the crop box specified as fraction of the width of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the width of the original media item. | No | 0 |
| right_fraction | number | The right boundary of the crop box specified as fraction of the width of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the width of the original media item. | No | 1 |
| top_fraction | number | The top boundary of the crop box specified as fraction of the height of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the height of the original media item. | No | 0 |

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

### InpaintItem

An inpainting item for a video generation job.
This specifies the media item that should be used for inpainting in the video generation.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| crop_bounds | object | The crop bounds for an inpainting item.<br>This specifies the area of the media item that should be used for inpainting. | No |  |
| └─ bottom_fraction | number | The bottom boundary of the crop box specified as fraction of the height of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the height of the original media item. | No | 1 |
| └─ left_fraction | number | The left boundary of the crop box specified as fraction of the width of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the width of the original media item. | No | 0 |
| └─ right_fraction | number | The right boundary of the crop box specified as fraction of the width of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the width of the original media item. | No | 1 |
| └─ top_fraction | number | The top boundary of the crop box specified as fraction of the height of the original media item. Must be between 0.0 and 1.0. Use e.g. 0.5 for half the height of the original media item. | No | 0 |
| file_name | string | The file name of the media item. It must match the file name of a file attachment in this request. | Yes |  |
| frame_index | integer | The frame index for this media item. This specifies the starting frame in the resulting generated video for this inpainting item. | Yes | 0 |
| type | object | The type of the inpainting item. | Yes |  |

### JobStatus

The status of a video generation job.

| Property | Value |
|----------|-------|
| **Description** | The status of a video generation job. |
| **Type** | string |
| **Values** | `preprocessing`<br>`queued`<br>`running`<br>`processing`<br>`cancelled`<br>`succeeded`<br>`failed` |

### MediaItemType

The type of the inpainting item.

| Property | Value |
|----------|-------|
| **Description** | The type of the inpainting item. |
| **Type** | string |
| **Values** | `image` |

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
| filename | string | The filename of the file cited. | Yes |  |
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
| **Values** | `file_citation`<br>`url_citation`<br>`file_path`<br>`container_file_citation` |

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

The format of the output, in one of these options: `json`, `text`, `srt`, `verbose_json`, or `vtt`. For `gpt-4o-transcribe`, `gpt-4o-transcribe-diarize`, and `gpt-4o-mini-transcribe`, the only supported format is `json`.

| Property | Value |
|----------|-------|
| **Description** | The format of the output, in one of these options: `json`, `text`, `srt`, `verbose_json`, or `vtt`. For `gpt-4o-transcribe`, `gpt-4o-transcribe-diarize`, and `gpt-4o-mini-transcribe`, the only supported format is `json`. |
| **Type** | string |
| **Values** | `json`<br>`text`<br>`srt`<br>`verbose_json`<br>`vtt` |

### OpenAI.AutoChunkingStrategyRequestParam

The default strategy. This strategy currently uses a `max_chunk_size_tokens` of `800` and `chunk_overlap_tokens` of `400`.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Always `auto`.<br>Possible values: `auto` | Yes |  |

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
| └─ detail | enum | Specifies the detail level of the image. <br>Possible values: `auto`, `low`, `high` | No |  |
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
| └─ detail | enum | Specifies the detail level of the image. <br>Possible values: `auto`, `low`, `high` | No |  |
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
| include_usage | boolean | If set, an additional chunk will be streamed before the `data: [DONE]`<br>message. The `usage` field on this chunk shows the token usage statistics<br>for the entire request, and the `choices` field will always be an empty<br>array.<br><br>All other chunks will also include a `usage` field, but with a null<br>value. **NOTE:** If the stream is interrupted, you may not receive the<br>final usage chunk which contains the total token usage for the request. | No |  |

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

### OpenAI.ChunkingStrategyRequestParam

The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy.


### Discriminator for OpenAI.ChunkingStrategyRequestParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `static` | [OpenAI.StaticChunkingStrategyRequestParam](#openaistaticchunkingstrategyrequestparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of chunking strategy.<br>Possible values: `auto`, `static` | Yes |  |

### OpenAI.ChunkingStrategyResponseParam


### Discriminator for OpenAI.ChunkingStrategyResponseParam

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `other` | [OpenAI.OtherChunkingStrategyResponseParam](#openaiotherchunkingstrategyresponseparam) |
| `static` | [OpenAI.StaticChunkingStrategyResponseParam](#openaistaticchunkingstrategyresponseparam) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | <br>Possible values: `static`, `other` | Yes |  |

### OpenAI.CodeInterpreterOutput


### Discriminator for OpenAI.CodeInterpreterOutput

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `image` | [OpenAI.CodeInterpreterOutputImage](#openaicodeinterpreteroutputimage) |
| `logs` | [OpenAI.CodeInterpreterOutputLogs](#openaicodeinterpreteroutputlogs) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.CodeInterpreterOutputType](#openaicodeinterpreteroutputtype) |  | Yes |  |

### OpenAI.CodeInterpreterOutputImage

The image output from the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the output. Always 'image'.<br>Possible values: `image` | Yes |  |
| url | string | The URL of the image output from the code interpreter. | Yes |  |

### OpenAI.CodeInterpreterOutputLogs

The logs output from the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| logs | string | The logs output from the code interpreter. | Yes |  |
| type | enum | The type of the output. Always 'logs'.<br>Possible values: `logs` | Yes |  |

### OpenAI.CodeInterpreterOutputType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `logs`<br>`image` |

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
| code | string | The code to run, or null if not available. | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| outputs | array | The outputs generated by the code interpreter, such as logs or images.<br>Can be null if no outputs are available. | Yes |  |
| type | enum | <br>Possible values: `code_interpreter_call` | Yes |  |

### OpenAI.CodeInterpreterToolCallItemResource

A tool call to run code.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The code to run, or null if not available. | Yes |  |
| container_id | string | The ID of the container used to run the code. | Yes |  |
| outputs | array | The outputs generated by the code interpreter, such as logs or images.<br>Can be null if no outputs are available. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `incomplete`, `interpreting`, `failed` | Yes |  |
| type | enum | <br>Possible values: `code_interpreter_call` | Yes |  |

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
| type | enum | Specifies the event type. For a click action, this property is<br>always set to `click`.<br>Possible values: `click` | Yes |  |
| x | integer | The x-coordinate where the click occurred. | Yes |  |
| y | integer | The y-coordinate where the click occurred. | Yes |  |

### OpenAI.ComputerActionDoubleClick

A double click action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a double click action, this property is<br>always set to `double_click`.<br>Possible values: `double_click` | Yes |  |
| x | integer | The x-coordinate where the double click occurred. | Yes |  |
| y | integer | The y-coordinate where the double click occurred. | Yes |  |

### OpenAI.ComputerActionDrag

A drag action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| path | array | An array of coordinates representing the path of the drag action. Coordinates will appear as an array<br>of objects, eg<br>```<br>[<br>  { x: 100, y: 200 },<br>  { x: 200, y: 300 }<br>]<br>``` | Yes |  |
| type | enum | Specifies the event type. For a drag action, this property is<br>always set to `drag`.<br>Possible values: `drag` | Yes |  |

### OpenAI.ComputerActionKeyPress

A collection of keypresses the model would like to perform.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| keys | array | The combination of keys the model is requesting to be pressed. This is an<br>array of strings, each representing a key. | Yes |  |
| type | enum | Specifies the event type. For a keypress action, this property is<br>always set to `keypress`.<br>Possible values: `keypress` | Yes |  |

### OpenAI.ComputerActionMove

A mouse move action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a move action, this property is<br>always set to `move`.<br>Possible values: `move` | Yes |  |
| x | integer | The x-coordinate to move to. | Yes |  |
| y | integer | The y-coordinate to move to. | Yes |  |

### OpenAI.ComputerActionScreenshot

A screenshot action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a screenshot action, this property is<br>always set to `screenshot`.<br>Possible values: `screenshot` | Yes |  |

### OpenAI.ComputerActionScroll

A scroll action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| scroll_x | integer | The horizontal scroll distance. | Yes |  |
| scroll_y | integer | The vertical scroll distance. | Yes |  |
| type | enum | Specifies the event type. For a scroll action, this property is<br>always set to `scroll`.<br>Possible values: `scroll` | Yes |  |
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
| type | enum | Specifies the event type. For a type action, this property is<br>always set to `type`.<br>Possible values: `type` | Yes |  |

### OpenAI.ComputerActionWait

A wait action.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Specifies the event type. For a wait action, this property is<br>always set to `wait`.<br>Possible values: `wait` | Yes |  |

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
| training_file | string | The ID of an uploaded file that contains training data.Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose `fine-tune`.<br><br>The contents of the file should differ depending on if the model uses the chat, completions format, or if the fine-tuning method uses the preference format. | Yes |  |
| validation_file | string | The ID of an uploaded file that contains validation data.<br><br>If you provide this file, the data is used to generate validation<br>metrics periodically during fine-tuning. These metrics can be viewed in<br>the fine-tuning results file.<br>The same data should not be present in both train and validation files.<br><br>Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`. | No |  |

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

### OpenAI.CreateVectorStoreFileBatchRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. | No |  |
| file_ids | array | A list of file IDs that the vector store should use. Useful for tools like `file_search` that can access files. | Yes |  |

### OpenAI.CreateVectorStoreFileRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | No |  |
| chunking_strategy | [OpenAI.ChunkingStrategyRequestParam](#openaichunkingstrategyrequestparam) | The chunking strategy used to chunk the file(s). If not set, will use the `auto` strategy. | No |  |
| file_id | string | A file ID that the vector store should use. Useful for tools like `file_search` that can access files. | Yes |  |

### OpenAI.CreateVectorStoreRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunking_strategy | object | The default strategy. This strategy currently uses a `max_chunk_size_tokens` of `800` and `chunk_overlap_tokens` of `400`. | No |  |
| └─ static | [OpenAI.StaticChunkingStrategy](#openaistaticchunkingstrategy) |  | No |  |
| └─ type | enum | Always `static`.<br>Possible values: `static` | No |  |
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| file_ids | array | A list of file IDs that the vector store should use. Useful for tools like `file_search` that can access files. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the vector store. | No |  |

### OpenAI.DeleteFileResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| deleted | boolean |  | Yes |  |
| id | string |  | Yes |  |
| object | enum | <br>Possible values: `file` | Yes |  |

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

### OpenAI.Embedding

Represents an embedding vector returned by embedding endpoint.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| embedding | array or string |  | Yes |  |
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
| reasoning_effort | object | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
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
| parameters |  | The parameters the functions accepts, described as a JSON Schema object.| No |  |
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
- `code_interpreter_call.outputs`: Includes the outputs of python code execution
  in code interpreter tool call items.
- `computer_call_output.output.image_url`: Include image urls from the computer call output.
- `file_search_call.results`: Include the search results of
  the file search tool call.
- `message.input_image.image_url`: Include image urls from the input message.
- `message.output_text.logprobs`: Include logprobs with assistant messages.
- `reasoning.encrypted_content`: Includes an encrypted version of reasoning
  tokens in reasoning item outputs. This enables reasoning items to be used in
  multi-turn conversations when using the Responses API statelessly (like
  when the `store` parameter is set to `false`, or when an organization is
  enrolled in the zero data retention program).

| Property | Value |
|----------|-------|
| **Description** | Specify additional output data to include in the model response. Currently<br>supported values are:<br>- `code_interpreter_call.outputs`: Includes the outputs of python code execution<br>  in code interpreter tool call items.<br>- `computer_call_output.output.image_url`: Include image urls from the computer call output.<br>- `file_search_call.results`: Include the search results of<br>  the file search tool call.<br>- `message.input_image.image_url`: Include image urls from the input message.<br>- `message.output_text.logprobs`: Include logprobs with assistant messages.<br>- `reasoning.encrypted_content`: Includes an encrypted version of reasoning<br>  tokens in reasoning item outputs. This enables reasoning items to be used in<br>  multi-turn conversations when using the Responses API statelessly (like<br>  when the `store` parameter is set to `false`, or when an organization is<br>  enrolled in the zero data retention program). |
| **Type** | string |
| **Values** | `code_interpreter_call.outputs`<br>`computer_call_output.output.image_url`<br>`file_search_call.results`<br>`message.input_image.image_url`<br>`message.output_text.logprobs`<br>`reasoning.encrypted_content` |

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
| logprobs | array |  | No |  |
| text | string | The text output from the model. | Yes |  |
| type | enum | The type of the output text. Always `output_text`.<br>Possible values: `output_text` | Yes |  |

### OpenAI.ItemContentRefusal

A refusal from the model.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| refusal | string | The refusal explanationfrom the model. | Yes |  |
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
| `file_search_call` | [OpenAI.FileSearchToolCallItemParam](#openaifilesearchtoolcallitemparam) |
| `computer_call` | [OpenAI.ComputerToolCallItemParam](#openaicomputertoolcallitemparam) |
| `computer_call_output` | [OpenAI.ComputerToolCallOutputItemParam](#openaicomputertoolcalloutputitemparam) |
| `web_search_call` | [OpenAI.WebSearchToolCallItemParam](#openaiwebsearchtoolcallitemparam) |
| `function_call` | [OpenAI.FunctionToolCallItemParam](#openaifunctiontoolcallitemparam) |
| `function_call_output` | [OpenAI.FunctionToolCallOutputItemParam](#openaifunctiontoolcalloutputitemparam) |
| `reasoning` | [OpenAI.ReasoningItemParam](#openaireasoningitemparam) |
| `item_reference` | [OpenAI.ItemReferenceItemParam](#openaiitemreferenceitemparam) |
| `image_generation_call` | [OpenAI.ImageGenToolCallItemParam](#openaiimagegentoolcallitemparam) |
| `code_interpreter_call` | [OpenAI.CodeInterpreterToolCallItemParam](#openaicodeinterpretertoolcallitemparam) |
| `local_shell_call` | [OpenAI.LocalShellToolCallItemParam](#openailocalshelltoolcallitemparam) |
| `local_shell_call_output` | [OpenAI.LocalShellToolCallOutputItemParam](#openailocalshelltoolcalloutputitemparam) |
| `mcp_list_tools` | [OpenAI.MCPListToolsItemParam](#openaimcplisttoolsitemparam) |
| `mcp_approval_request` | [OpenAI.MCPApprovalRequestItemParam](#openaimcpapprovalrequestitemparam) |
| `mcp_approval_response` | [OpenAI.MCPApprovalResponseItemParam](#openaimcpapprovalresponseitemparam) |
| `mcp_call` | [OpenAI.MCPCallItemParam](#openaimcpcallitemparam) |
| `message` | [OpenAI.ResponsesMessageItemParam](#openairesponsesmessageitemparam) |

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
| `file_search_call` | [OpenAI.FileSearchToolCallItemResource](#openaifilesearchtoolcallitemresource) |
| `computer_call` | [OpenAI.ComputerToolCallItemResource](#openaicomputertoolcallitemresource) |
| `computer_call_output` | [OpenAI.ComputerToolCallOutputItemResource](#openaicomputertoolcalloutputitemresource) |
| `web_search_call` | [OpenAI.WebSearchToolCallItemResource](#openaiwebsearchtoolcallitemresource) |
| `function_call` | [OpenAI.FunctionToolCallItemResource](#openaifunctiontoolcallitemresource) |
| `function_call_output` | [OpenAI.FunctionToolCallOutputItemResource](#openaifunctiontoolcalloutputitemresource) |
| `reasoning` | [OpenAI.ReasoningItemResource](#openaireasoningitemresource) |
| `image_generation_call` | [OpenAI.ImageGenToolCallItemResource](#openaiimagegentoolcallitemresource) |
| `code_interpreter_call` | [OpenAI.CodeInterpreterToolCallItemResource](#openaicodeinterpretertoolcallitemresource) |
| `local_shell_call` | [OpenAI.LocalShellToolCallItemResource](#openailocalshelltoolcallitemresource) |
| `local_shell_call_output` | [OpenAI.LocalShellToolCallOutputItemResource](#openailocalshelltoolcalloutputitemresource) |
| `mcp_list_tools` | [OpenAI.MCPListToolsItemResource](#openaimcplisttoolsitemresource) |
| `mcp_approval_request` | [OpenAI.MCPApprovalRequestItemResource](#openaimcpapprovalrequestitemresource) |
| `mcp_approval_response` | [OpenAI.MCPApprovalResponseItemResource](#openaimcpapprovalresponseitemresource) |
| `mcp_call` | [OpenAI.MCPCallItemResource](#openaimcpcallitemresource) |
| `message` | [OpenAI.ResponsesMessageItemResource](#openairesponsesmessageitemresource) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string |  | Yes |  |
| type | [OpenAI.ItemType](#openaiitemtype) |  | Yes |  |

### OpenAI.ItemType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `message`<br>`file_search_call`<br>`function_call`<br>`function_call_output`<br>`computer_call`<br>`computer_call_output`<br>`web_search_call`<br>`reasoning`<br>`item_reference`<br>`image_generation_call`<br>`code_interpreter_call`<br>`local_shell_call`<br>`local_shell_call_output`<br>`mcp_list_tools`<br>`mcp_approval_request`<br>`mcp_approval_response`<br>`mcp_call` |

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

### OpenAI.ListVectorStoreFilesFilter

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `in_progress`<br>`completed`<br>`failed`<br>`cancelled` |

### OpenAI.ListVectorStoreFilesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.ListVectorStoresResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array |  | Yes |  |
| first_id | string |  | Yes |  |
| has_more | boolean |  | Yes |  |
| last_id | string |  | Yes |  |
| object | enum | <br>Possible values: `list` | Yes |  |

### OpenAI.LocalShellExecAction

Execute a shell command on the server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| command | array | The command to run. | Yes |  |
| env | object | Environment variables to set for the command. | Yes |  |
| timeout_ms | integer | Optional timeout in milliseconds for the command. | No |  |
| type | enum | The type of the local shell action. Always `exec`.<br>Possible values: `exec` | Yes |  |
| user | string | Optional user to run the command as. | No |  |
| working_directory | string | Optional working directory to run the command in. | No |  |

### OpenAI.LocalShellTool

A tool that allows the model to execute shell commands in a local environment.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | The type of the local shell tool. Always `local_shell`.<br>Possible values: `local_shell` | Yes |  |

### OpenAI.LocalShellToolCallItemParam

A tool call to run a command on the local shell.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| type | enum | <br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.LocalShellToolCallItemResource

A tool call to run a command on the local shell.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | [OpenAI.LocalShellExecAction](#openailocalshellexecaction) | Execute a shell command on the server. | Yes |  |
| call_id | string | The unique ID of the local shell tool call generated by the model. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | <br>Possible values: `local_shell_call` | Yes |  |

### OpenAI.LocalShellToolCallOutputItemParam

The output of a local shell tool call.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| type | enum | <br>Possible values: `local_shell_call_output` | Yes |  |

### OpenAI.LocalShellToolCallOutputItemResource

The output of a local shell tool call.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| output | string | A JSON string of the output of the local shell tool call. | Yes |  |
| status | enum | <br>Possible values: `in_progress`, `completed`, `incomplete` | Yes |  |
| type | enum | <br>Possible values: `local_shell_call_output` | Yes |  |

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

### OpenAI.LogProb

The log probability of a token.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array |  | Yes |  |
| logprob | number |  | Yes |  |
| token | string |  | Yes |  |
| top_logprobs | array |  | Yes |  |

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

### OpenAI.OtherChunkingStrategyResponseParam

This is returned when the chunking strategy is unknown. Typically, this is because the file was indexed before the `chunking_strategy` concept was introduced in the API.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | enum | Always `other`.<br>Possible values: `other` | Yes |  |

### OpenAI.ParallelToolCalls

Whether to enable parallel function calling during tool use.

**Type**: boolean


### OpenAI.Prompt

Reference to a prompt template and its variables.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| id | string | The unique identifier of the prompt template to use. | Yes |  |
| variables | object | Optional map of values to substitute in for variables in your<br>prompt. The substitution values can either be strings, or other<br>Response input types like images or files. | No |  |
| version | string | Optional version of the prompt template. | No |  |

### OpenAI.RankingOptions

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| ranker | enum | The ranker to use for the file search.<br>Possible values: `auto`, `default-2024-11-15` | No |  |
| score_threshold | number | The score threshold for the file search, a number between 0 and 1. Numbers closer to 1 will attempt to return only the most relevant results, but may return fewer results. | No |  |

### OpenAI.Reasoning

**o-series models only**



| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| effort | object | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |

### OpenAI.ReasoningEffort

**o-series models only**

Constrains effort on reasoning for reasoning models. Currently supported values are `low`, `medium`, and `high`. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.

| Property | Value |
|----------|-------|
| **Description** | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. |
| **Type** | string |
| **Values** | `low`<br>`medium`<br>`high` |

### OpenAI.ReasoningItemParam

A description of the chain of thought used by a reasoning model while generating a response. Be sure to include these items in your `input` to the Responses API for subsequent turns of a conversation if you are manually managing context.


| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| encrypted_content | string | The encrypted content of the reasoning item - populated when a response is<br>generated with `reasoning.encrypted_content` in the `include` parameter. | No |  |
| summary | array | Reasoning text contents. | Yes |  |
| type | enum | <br>Possible values: `reasoning` | Yes |  |

### OpenAI.ReasoningItemResource

A description of the chain of thought used by a reasoning model while generating a response. Be sure to include these items in your `input` to the Responses API for subsequent turns of a conversation if you are manually managing context.


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
| background | boolean | Whether to run the model response in the background.| No | False |
| created_at | integer | Unix timestamp (in seconds) of when this Response was created. | Yes |  |
| error | object | An error object returned when the model fails to generate a Response. | Yes |  |
| └─ code | [OpenAI.ResponseErrorCode](#openairesponseerrorcode) | The error code for the response. | No |  |
| └─ message | string | A human-readable description of the error. | No |  |
| id | string | Unique identifier for this Response. | Yes |  |
| incomplete_details | object | Details about why the response is incomplete. | Yes |  |
| └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| instructions | string or array |  | Yes |  |
| max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | Yes |  |
| output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | Yes |  |
| output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | Yes | True |
| previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| prompt | object | Reference to a prompt template and its variables. | No |  |
| └─ id | string | The unique identifier of the prompt template to use. | No |  |
| └─ variables | [OpenAI.ResponsePromptVariables](#openairesponsepromptvariables) | Optional map of values to substitute in for variables in your<br>prompt. The substitution values can either be strings, or other<br>Response input types like images or files. | No |  |
| └─ version | string | Optional version of the prompt template. | No |  |
| reasoning | object | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ effort | [OpenAI.ReasoningEffort](#openaireasoningeffort) | **o-series models only**<br><br>Constrains effort on reasoning for reasoning models.<br>Currently supported values are `low`, `medium`, and `high`. Reducing<br>reasoning effort can result in faster responses and fewer tokens used<br>on reasoning in a response. | No |  |
| └─ generate_summary | enum | **Deprecated:** use `summary` instead.<br><br>A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| └─ summary | enum | A summary of the reasoning performed by the model. This can be<br>useful for debugging and understanding the model's reasoning process.<br>One of `auto`, `concise`, or `detailed`.<br>Possible values: `auto`, `concise`, `detailed` | No |  |
| status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | Yes |  |
| text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
| └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| tool_choice | object | Controls which (if any) tool is called by the model.<br><br>`none` means the model will not call any tool and instead generates a message.<br><br>`auto` means the model can pick between generating a message or calling one or<br>more tools.<br><br>`required` means the model must call one or more tools. | No |  |
| └─ type | [OpenAI.ToolChoiceObjectType](#openaitoolchoiceobjecttype) | Indicates that the model should use a built-in tool to generate a response. | No |  |
| tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | Yes |  |
| truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCodeDeltaEvent

Emitted when a partial code snippet is streamed by the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| delta | string | The partial code snippet being streamed by the code interpreter. | Yes |  |
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code is being streamed. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call_code.delta`.<br>Possible values: `response.code_interpreter_call_code.delta` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCodeDoneEvent

Emitted when the code snippet is finalized by the code interpreter.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | string | The final code snippet output by the code interpreter. | Yes |  |
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code is finalized. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call_code.done`.<br>Possible values: `response.code_interpreter_call_code.done` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallCompletedEvent

Emitted when the code interpreter call is completed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code interpreter call is completed. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.completed`.<br>Possible values: `response.code_interpreter_call.completed` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInProgressEvent

Emitted when a code interpreter call is in progress.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code interpreter call is in progress. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.in_progress`.<br>Possible values: `response.code_interpreter_call.in_progress` | Yes |  |

### OpenAI.ResponseCodeInterpreterCallInterpretingEvent

Emitted when the code interpreter is actively interpreting the code snippet.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| item_id | string | The unique identifier of the code interpreter tool call item. | Yes |  |
| output_index | integer | The index of the output item in the response for which the code interpreter is interpreting code. | Yes |  |
| type | enum | The type of the event. Always `response.code_interpreter_call.interpreting`.<br>Possible values: `response.code_interpreter_call.interpreting` | Yes |  |

### OpenAI.ResponseCompletedEvent

Emitted when the model response is complete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background.| No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string or array | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| └─ max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| └─ top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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
| └─ background | boolean | Whether to run the model response in the background.| No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string or array | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| └─ max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| └─ top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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
| └─ background | boolean | Whether to run the model response in the background.| No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string or array | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| └─ max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| └─ top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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
| └─ strict | boolean | Whether to enable strict schema adherence when generating the output.<br>If set to true, the model will always follow the exact schema defined<br>in the `schema` field. Only a subset of JSON Schema is supported when<br>`strict` is `true`. | No | False |
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
| └─ background | boolean | Whether to run the model response in the background.| No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string or array | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| └─ max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| └─ top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
| └─ usage | [OpenAI.ResponseUsage](#openairesponseusage) | Represents token usage details including input tokens, output tokens,<br>a breakdown of output tokens, and the total tokens used. | No |  |
| └─ user | string | A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.  | No |  |
| type | enum | The type of the event. Always `response.in_progress`.<br>Possible values: `response.in_progress` | Yes |  |

### OpenAI.ResponseIncompleteEvent

An event that is emitted when a response finishes as incomplete.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background.| No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string or array | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| └─ max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| └─ top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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

### OpenAI.ResponsePromptVariables

Optional map of values to substitute in for variables in your
prompt. The substitution values can either be strings, or other
Response input types like images or files.

**Type**: object


### OpenAI.ResponseQueuedEvent

Emitted when a response is queued and waiting to be processed.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| response | object |  | Yes |  |
| └─ background | boolean | Whether to run the model response in the background.| No | False |
| └─ created_at | integer | Unix timestamp (in seconds) of when this Response was created. | No |  |
| └─ error | [OpenAI.ResponseError](#openairesponseerror) | An error object returned when the model fails to generate a Response. | No |  |
| └─ id | string | Unique identifier for this Response. | No |  |
| └─ incomplete_details | object | Details about why the response is incomplete. | No |  |
|   └─ reason | enum | The reason why the response is incomplete.<br>Possible values: `max_output_tokens`, `content_filter` | No |  |
| └─ instructions | string or array | A system (or developer) message inserted into the model's context.<br><br>When using along with `previous_response_id`, the instructions from a previous<br>response will not be carried over to the next response. This makes it simple<br>to swap out system (or developer) messages in new responses. | No |  |
| └─ max_output_tokens | integer | An upper bound for the number of tokens that can be generated for a response, including visible output tokens and reasoning tokens | No |  |
| └─ max_tool_calls | integer | The maximum number of total calls to built-in tools that can be processed in a response. This maximum number applies across all built-in tool calls, not per individual tool. Any further attempts to call a tool by the model will be ignored. | No |  |
| └─ metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| └─ object | enum | The object type of this resource - always set to `response`.<br>Possible values: `response` | No |  |
| └─ output | array | An array of content items generated by the model.<br><br>- The length and order of items in the `output` array is dependent<br>  on the model's response.<br>- Rather than accessing the first item in the `output` array and<br>  assuming it's an `assistant` message with the content generated by<br>  the model, you might consider using the `output_text` property where<br>  supported in SDKs. | No |  |
| └─ output_text | string | SDK-only convenience property that contains the aggregated text output<br>from all `output_text` items in the `output` array, if any are present.<br>Supported in the Python and JavaScript SDKs. | No |  |
| └─ parallel_tool_calls | boolean | Whether to allow the model to run tool calls in parallel. | No | True |
| └─ previous_response_id | string | The unique ID of the previous response to the model. Use this to<br>create multi-turn conversations. | No |  |
| └─ prompt | [OpenAI.Prompt](#openaiprompt) | Reference to a prompt template and its variables. | No |  |
| └─ reasoning | [OpenAI.Reasoning](#openaireasoning) | **o-series models only**<br><br>Configuration options for reasoning models. | No |  |
| └─ status | enum | The status of the response generation. One of `completed`, `failed`,<br>`in_progress`, `cancelled`, `queued`, or `incomplete`.<br>Possible values: `completed`, `failed`, `in_progress`, `cancelled`, `queued`, `incomplete` | No |  |
| └─ temperature | number | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.<br>We generally recommend altering this or `top_p` but not both. | No |  |
| └─ text | object | Configuration options for a text response from the model. Can be plain text or structured JSON data. | No |  |
|   └─ format | [OpenAI.ResponseTextFormatConfiguration](#openairesponsetextformatconfiguration) |  | No |  |
| └─ tool_choice | [OpenAI.ToolChoiceOptions](#openaitoolchoiceoptions) or [OpenAI.ToolChoiceObject](#openaitoolchoiceobject) | How the model should select which tool (or tools) to use when generating<br>a response. See the `tools` parameter to see how to specify which tools<br>the model can call. | No |  |
| └─ tools | array | An array of tools the model may call while generating a response. You<br>can specify which tool to use by setting the `tool_choice` parameter.<br><br>The two categories of tools you can provide the model are:<br><br>- **Built-in tools**: Tools that are provided by OpenAI that extend the<br>  model's capabilities. | No |  |
| └─ top_logprobs | integer | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. | No |  |
| └─ top_p | number | An alternative to sampling with temperature, called nucleus sampling,<br>where the model considers the results of the tokens with top_p probability<br>mass. So 0.1 means only the tokens comprising the top 10% probability mass<br>are considered.<br><br>We generally recommend altering this or `temperature` but not both. | No |  |
| └─ truncation | enum | The truncation strategy to use for the model response.<br>- `auto`: If the context of this response and previous ones exceeds<br>  the model's context window size, the model will truncate the<br>  response to fit the context window by dropping input items in the<br>  middle of the conversation.<br>- `disabled` (default): If a model response will exceed the context window<br>  size for a model, the request will fail with a 400 error.<br>Possible values: `auto`, `disabled` | No |  |
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
| `response.code_interpreter_call_code.delta` | [OpenAI.ResponseCodeInterpreterCallCodeDeltaEvent](#openairesponsecodeinterpretercallcodedeltaevent) |
| `response.code_interpreter_call_code.done` | [OpenAI.ResponseCodeInterpreterCallCodeDoneEvent](#openairesponsecodeinterpretercallcodedoneevent) |
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
| **Values** | `response.audio.delta`<br>`response.audio.done`<br>`response.audio_transcript.delta`<br>`response.audio_transcript.done`<br>`response.code_interpreter_call_code.delta`<br>`response.code_interpreter_call_code.done`<br>`response.code_interpreter_call.completed`<br>`response.code_interpreter_call.in_progress`<br>`response.code_interpreter_call.interpreting`<br>`response.completed`<br>`response.content_part.added`<br>`response.content_part.done`<br>`response.created`<br>`error`<br>`response.file_search_call.completed`<br>`response.file_search_call.in_progress`<br>`response.file_search_call.searching`<br>`response.function_call_arguments.delta`<br>`response.function_call_arguments.done`<br>`response.in_progress`<br>`response.failed`<br>`response.incomplete`<br>`response.output_item.added`<br>`response.output_item.done`<br>`response.refusal.delta`<br>`response.refusal.done`<br>`response.output_text.annotation.added`<br>`response.output_text.delta`<br>`response.output_text.done`<br>`response.reasoning_summary_part.added`<br>`response.reasoning_summary_part.done`<br>`response.reasoning_summary_text.delta`<br>`response.reasoning_summary_text.done`<br>`response.web_search_call.completed`<br>`response.web_search_call.in_progress`<br>`response.web_search_call.searching`<br>`response.image_generation_call.completed`<br>`response.image_generation_call.generating`<br>`response.image_generation_call.in_progress`<br>`response.image_generation_call.partial_image`<br>`response.mcp_call.arguments_delta`<br>`response.mcp_call.arguments_done`<br>`response.mcp_call.completed`<br>`response.mcp_call.failed`<br>`response.mcp_call.in_progress`<br>`response.mcp_list_tools.completed`<br>`response.mcp_list_tools.failed`<br>`response.mcp_list_tools.in_progress`<br>`response.queued`<br>`response.reasoning.delta`<br>`response.reasoning.done`<br>`response.reasoning_summary.delta`<br>`response.reasoning_summary.done` |

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
| type | [OpenAI.ResponseTextFormatConfigurationType](#openairesponsetextformatconfigurationtype) | An object specifying the format that the model must output.<br><br>Configuring `{ "type": "json_schema" }` enables Structured Outputs,<br>which ensures the model will match your supplied JSON schema. The default format is `{ "type": "text" }` with no additional options.<br><br>**Not recommended for gpt-4o and newer models:**<br><br>Setting to `{ "type": "json_object" }` enables the older JSON mode, which<br>ensures the message the model generates is valid JSON. Using `json_schema`<br>is preferred for models that support it. | Yes |  |

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
| strict | boolean | Whether to enable strict schema adherence when generating the output.<br>If set to true, the model will always follow the exact schema defined<br>in the `schema` field. Only a subset of JSON Schema is supported when<br>`strict` is `true`. | No | False |
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

Configuring `{ "type": "json_schema" }` enables Structured Outputs, which ensures the model will match your supplied JSON schema. 

The default format is `{ "type": "text" }` with no additional options.

**Not recommended for gpt-4o and newer models:**

Setting to `{ "type": "json_object" }` enables the older JSON mode, which ensures the message the model generates is valid JSON. Using `json_schema`is preferred for models that support it. 

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

### OpenAI.StaticChunkingStrategy

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| chunk_overlap_tokens | integer | The number of tokens that overlap between chunks. The default value is `400`.<br><br>Note that the overlap must not exceed half of `max_chunk_size_tokens`. | Yes |  |
| max_chunk_size_tokens | integer | The maximum number of tokens in each chunk. The default value is `800`. The minimum value is `100` and the maximum value is `4096`. | Yes |  |

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
| `local_shell` | [OpenAI.LocalShellTool](#openailocalshelltool) |
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
| `function` | [OpenAI.ToolChoiceObjectFunction](#openaitoolchoiceobjectfunction) |
| `mcp` | [OpenAI.ToolChoiceObjectMCP](#openaitoolchoiceobjectmcp) |

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

Use this option to force the model to call a specific tool on a remote MCP server.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| name | string | The name of the tool to call on the server. | No |  |
| server_label | string | The label of the MCP server to use. | Yes |  |
| type | enum | For MCP tools, the type is always `mcp`.<br>Possible values: `mcp` | Yes |  |

### OpenAI.ToolChoiceObjectType

Indicates that the model should use a built-in tool to generate a response.


| Property | Value |
|----------|-------|
| **Description** | Indicates that the model should use a built-in tool to generate a response.
 |
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
| **Values** | `file_search`<br>`function`<br>`computer_use_preview`<br>`web_search_preview`<br>`mcp`<br>`code_interpreter`<br>`image_generation`<br>`local_shell` |

### OpenAI.TopLogProb

The top log probability of a token.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| bytes | array |  | Yes |  |
| logprob | number |  | Yes |  |
| token | string |  | Yes |  |

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

### OpenAI.TranslationAudioResponseFormat

References: [OpenAI.AudioResponseFormat](#openaiaudioresponseformat)

### OpenAI.UpdateVectorStoreFileAttributesRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | Yes |  |

### OpenAI.UpdateVectorStoreRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| expires_after | object | The expiration policy for a vector store. | No |  |
| └─ anchor | enum | Anchor timestamp after which the expiration policy applies. Supported anchors: `last_active_at`.<br>Possible values: `last_active_at` | No |  |
| └─ days | integer | The number of days after the anchor time that the vector store will expire. | No |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | No |  |
| name | string | The name of the vector store. | No |  |

### OpenAI.VadConfig

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| prefix_padding_ms | integer | Amount of audio to include before the VAD detected speech (in<br>milliseconds). | No | 300 |
| silence_duration_ms | integer | Duration of silence to detect speech stop (in milliseconds).<br>With shorter values the model will respond more quickly,<br>but may jump in on short pauses from the user. | No | 200 |
| threshold | number | Sensitivity threshold (0.0 to 1.0) for voice activity detection. A<br>higher threshold will require louder audio to activate the model, and<br>thus might perform better in noisy environments. | No | 0.5 |
| type | enum | Must be set to `server_vad` to enable manual chunking using server side VAD.<br>Possible values: `server_vad` | Yes |  |

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

### OpenAI.VectorStoreExpirationAfter

The expiration policy for a vector store.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| anchor | enum | Anchor timestamp after which the expiration policy applies. Supported anchors: `last_active_at`.<br>Possible values: `last_active_at` | Yes |  |
| days | integer | The number of days after the anchor time that the vector store will expire. | Yes |  |

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
| file_counts | object |  | Yes |  |
| └─ cancelled | integer | The number of files that where cancelled. | No |  |
| └─ completed | integer | The number of files that have been processed. | No |  |
| └─ failed | integer | The number of files that have failed to process. | No |  |
| └─ in_progress | integer | The number of files that are currently being processed. | No |  |
| └─ total | integer | The total number of files. | No |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| object | enum | The object type, which is always `vector_store.file_batch`.<br>Possible values: `vector_store.files_batch` | Yes |  |
| status | enum | The status of the vector store files batch, which can be either `in_progress`, `completed`, `cancelled` or `failed`.<br>Possible values: `in_progress`, `completed`, `cancelled`, `failed` | Yes |  |
| vector_store_id | string | The ID of the vector store that the file is attached to. | Yes |  |

### OpenAI.VectorStoreFileObject

A list of files attached to a vector store.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| attributes | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard. Keys are strings<br>with a maximum length of 64 characters. Values are strings with a maximum<br>length of 512 characters, booleans, or numbers. | No |  |
| chunking_strategy | object |  | No |  |
| └─ type | enum | <br>Possible values: `static`, `other` | No |  |
| created_at | integer | The Unix timestamp (in seconds) for when the vector store file was created. | Yes |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| last_error | object | The last error associated with this vector store file. Will be `null` if there are no errors. | Yes |  |
| └─ code | enum | One of `server_error` or `rate_limit_exceeded`.<br>Possible values: `server_error`, `unsupported_file`, `invalid_file` | No |  |
| └─ message | string | A human-readable description of the error. | No |  |
| object | enum | The object type, which is always `vector_store.file`.<br>Possible values: `vector_store.file` | Yes |  |
| status | enum | The status of the vector store file, which can be either `in_progress`, `completed`, `cancelled`, or `failed`. The status `completed` indicates that the vector store file is ready for use.<br>Possible values: `in_progress`, `completed`, `cancelled`, `failed` | Yes |  |
| usage_bytes | integer | The total vector store usage in bytes. Note that this may be different from the original file size. | Yes |  |
| vector_store_id | string | The ID of the vector store that the file is attached to. | Yes |  |

### OpenAI.VectorStoreObject

A vector store is a collection of processed files can be used by the `file_search` tool.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The Unix timestamp (in seconds) for when the vector store was created. | Yes |  |
| expires_after | [OpenAI.VectorStoreExpirationAfter](#openaivectorstoreexpirationafter) | The expiration policy for a vector store. | No |  |
| expires_at | integer | The Unix timestamp (in seconds) for when the vector store will expire. | No |  |
| file_counts | object |  | Yes |  |
| └─ cancelled | integer | The number of files that were cancelled. | No |  |
| └─ completed | integer | The number of files that have been successfully processed. | No |  |
| └─ failed | integer | The number of files that have failed to process. | No |  |
| └─ in_progress | integer | The number of files that are currently being processed. | No |  |
| └─ total | integer | The total number of files. | No |  |
| id | string | The identifier, which can be referenced in API endpoints. | Yes |  |
| last_active_at | integer | The Unix timestamp (in seconds) for when the vector store was last active. | Yes |  |
| metadata | object | Set of 16 key-value pairs that can be attached to an object. This can be<br>useful for storing additional information about the object in a structured<br>format, and querying for objects via API or the dashboard.<br><br>Keys are strings with a maximum length of 64 characters. Values are strings<br>with a maximum length of 512 characters. | Yes |  |
| name | string | The name of the vector store. | Yes |  |
| object | enum | The object type, which is always `vector_store`.<br>Possible values: `vector_store` | Yes |  |
| status | enum | The status of the vector store, which can be either `expired`, `in_progress`, or `completed`. A status of `completed` indicates that the vector store is ready for use.<br>Possible values: `expired`, `in_progress`, `completed` | Yes |  |
| usage_bytes | integer | The total number of bytes used by the files in the vector store. | Yes |  |

### OpenAI.VoiceIdsShared

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `alloy`<br>`ash`<br>`ballad`<br>`coral`<br>`echo`<br>`fable`<br>`onyx`<br>`nova`<br>`sage`<br>`shimmer`<br>`verse` |

### OpenAI.WebSearchAction


### Discriminator for OpenAI.WebSearchAction

This component uses the property `type` to discriminate between different types:

| Type Value | Schema |
|------------|--------|
| `find` | [OpenAI.WebSearchActionFind](#openaiwebsearchactionfind) |
| `open_page` | [OpenAI.WebSearchActionOpenPage](#openaiwebsearchactionopenpage) |
| `search` | [OpenAI.WebSearchActionSearch](#openaiwebsearchactionsearch) |

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| type | [OpenAI.WebSearchActionType](#openaiwebsearchactiontype) |  | Yes |  |

### OpenAI.WebSearchActionFind

Action type "find": Searches for a pattern within a loaded page.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| pattern | string | The pattern or text to search for within the page. | Yes |  |
| type | enum | The action type.<br>Possible values: `find` | Yes |  |
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
| query | string | The search query. | Yes |  |
| type | enum | The action type.<br>Possible values: `search` | Yes |  |

### OpenAI.WebSearchActionType

| Property | Value |
|----------|-------|
| **Type** | string |
| **Values** | `search`<br>`open_page`<br>`find` |

### OpenAI.WebSearchPreviewTool

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| search_context_size | enum | High level guidance for the amount of context window space to use for the search. One of `low`, `medium`, or `high`. `medium` is the default.<br>Possible values: `low`, `medium`, `high` | No |  |
| type | enum | The type of the web search tool. One of `web_search_preview` or `web_search_preview_2025_03_11`.<br>Possible values: `web_search_preview` | Yes |  |
| user_location | object |  | No |  |
| └─ type | [OpenAI.LocationType](#openailocationtype) |  | No |  |

### OpenAI.WebSearchToolCallItemParam

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | object |  | Yes |  |
| └─ type | [OpenAI.WebSearchActionType](#openaiwebsearchactiontype) |  | No |  |
| type | enum | <br>Possible values: `web_search_call` | Yes |  |

### OpenAI.WebSearchToolCallItemResource

Note: web_search is not yet available via Azure OpenAI.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| action | object |  | Yes |  |
| └─ type | [OpenAI.WebSearchActionType](#openaiwebsearchactiontype) |  | No |  |
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

The quality of the video content to retrieve.
This specifies the quality of the video content that should be returned.

| Property | Value |
|----------|-------|
| **Description** | The quality of the video content to retrieve.<br>This specifies the quality of the video content that should be returned. |
| **Type** | string |
| **Values** | `high`<br>`low` |

### ResponseFormatJSONSchemaRequest

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| json_schema | object | JSON Schema for the response format | Yes |  |
| type | enum | Type of response format<br>Possible values: `json_schema` | Yes |  |

### ResponseModalities

Output types that you would like the model to generate.
Most models are capable of generating text, which is the default:

`["text"]`

The `gpt-4o-audio-preview` model can also be used to generate audio. To request that this model generate both text and audio responses, you can use:

`["text", "audio"]`

**Array of**: string


### SpeechGenerationResponseFormat

The supported audio output formats for text-to-speech.

This component can be one of the following:


### VideoGeneration

A  video generation result.

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

A video generation job.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created_at | integer | The time when the job was created. | Yes |  |
| expires_at | integer | The time when the job gets automatically deleted from the service. The video content and metadata of the job should be stored before this date to avoid data loss. | No |  |
| failure_reason | string (see valid models below) |  | No |  |
| finished_at | integer | The time when the job finished with all video generations. | No |  |
| generations | array | The generated videos for this job. The number depends on the given n_variants and the creation success of the generations. | No |  |
| height | integer | The height of the video. | Yes |  |
| id | string | The id of the job. | Yes |  |
| inpaint_items | array | Optional inpainting items for this video generation job. | No |  |
| model | string | The name of the deployment to use for this video generation job. | Yes |  |
| n_seconds | integer | The duration of the video generation job. | Yes |  |
| n_variants | integer | The number of videos to create as variants for this video generation job. | Yes |  |
| object | enum | <br>Possible values: `video.generation.job` | Yes |  |
| prompt | string | The prompt for this video generation job. | Yes |  |
| status | object | The status of a video generation job. | Yes |  |
| width | integer | The height of the video. | Yes |  |

### VideoGenerationJobList

A list of video generation jobs.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| data | array | The list of video generation jobs. | Yes |  |
| first_id | string | The ID of the first job in the current page, if available. | No |  |
| has_more | boolean | A flag indicating whether there are more jobs available after the list. | Yes |  |
| last_id | string | The ID of the last job in the current page, if available. | No |  |
| object | enum | <br>Possible values: `list` | Yes |  |

