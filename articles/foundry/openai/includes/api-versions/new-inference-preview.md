---
title: Azure OpenAI new v1 preview inference API documentation
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Latest v1 preview data plane inference documentation generated from OpenAPI 3.0 spec
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 08/04/2025
ai-usage: ai-assisted
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
| api-version | query | No |  | The explicit Microsoft Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| include[] | array | Additional information to include in the transcription response. `logprobs` will return the log probabilities of the tokens in the response to understand the model's confidence in the transcription. `logprobs` only works with response_format set to `json` and only with the models `gpt-4o-transcribe`, `gpt-4o-transcribe-diarize`, `gpt-4o-mini-transcribe`, and `gpt-4o-mini-transcribe-2025-12-15`. | No |  |
| language | string | The language of the input audio. Supplying the input language in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) (e.g. `en`) format will improve accuracy and latency. | No |  |
| model | string | The model to use for this transcription request. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language. | No |  |
| response_format | object |  | No |  |
| stream | boolean | If set to true, the model response data will be streamed to the client as it is generated using [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format). Note: Streaming is not supported for the `whisper-1` model and will be ignored. | No | False |
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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

## Create image edit

```HTTP
POST {endpoint}/openai/v1/images/edits?api-version=preview
```



### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: multipart/form-data

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Allows to set transparency for the background of the generated image(s).<br>This parameter is only supported for `gpt-image-1` models. Must be one of `transparent`, `opaque` or `auto` (default value). When `auto` is used, the model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| image | string or array |  | Yes |  |
| mask | string |  | No |  |
| model | string | The model deployment to use for the image edit operation. | Yes |  |
| n | integer | The number of images to generate. Must be between 1 and 10. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter is only supported for `gpt-image-1`-series models with the `webp` or `jpeg` output formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is only supported for `gpt-image-1`-series models. Must be one of `png`, `jpeg`, or `webp`.<br>The default value is `png`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 1000 characters for `dall-e-2`, and 32000 characters for `gpt-image-1`-series models. | Yes |  |
| quality | enum | The quality of the image that will be generated. `high`, `medium` and `low` are only supported for `gpt-image-1`-series models. `dall-e-2` only supports `standard` quality. Defaults to `auto`.<br>Possible values: `standard`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which the generated images are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter is only supported for `dall-e-2`, as `gpt-image-1`-series models will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`-series models, and one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`.<br>Possible values: `256x256`, `512x512`, `1024x1024`, `1536x1024`, `1024x1536`, `auto` | No |  |
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
| api-key | True | string | Provide Azure OpenAI API key here |
### Request Body

**Content-Type**: application/json

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | Allows to set transparency for the background of the generated image(s).<br>This parameter is only supported for `gpt-image-1` models. Must be one of `transparent`, `opaque` or `auto` (default value). When `auto` is used, the model will automatically determine the best background for the image.<br><br>If `transparent`, the output format needs to support transparency, so it should be set to either `png` (default value) or `webp`.<br>Possible values: `transparent`, `opaque`, `auto` | No |  |
| model | string | The model deployment to use for the image generation. | Yes |  |
| moderation | enum | Control the content-moderation level for images generated by `gpt-image-1`-series models. Must be either `low` for less restrictive filtering or `auto` (default value).<br>Possible values: `low`, `auto` | No |  |
| n | integer | The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only `n=1` is supported. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter is only supported for `gpt-image-1`-series models with the `webp` or `jpeg` output formats, and defaults to 100. | No | 100 |
| output_format | enum | The format in which the generated images are returned. This parameter is only supported for `gpt-image-1`-series models. Must be one of `png`, `jpeg`, or `webp`.<br>Possible values: `png`, `jpeg`, `webp` | No |  |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters for `gpt-image-1`-series models, 1000 characters for `dall-e-2` and 4000 characters for `dall-e-3`. | Yes |  |
| quality | enum | The quality of the image that will be generated.<br><br>- `auto` (default value) will automatically select the best quality for the given model.<br>- `high`, `medium` and `low` are supported for `gpt-image-1`-series models.<br>- `hd` and `standard` are supported for `dall-e-3`.<br>- `standard` is the only option for `dall-e-2`.<br>Possible values: `standard`, `hd`, `low`, `medium`, `high`, `auto` | No |  |
| response_format | enum | The format in which generated images with `dall-e-2` and `dall-e-3` are returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes after the image has been generated. This parameter isn't supported for `gpt-image-1`-series models which will always return base64-encoded images.<br>Possible values: `url`, `b64_json` | No |  |
| size | enum | The size of the generated images. Must be one of `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default value) for `gpt-image-1`-series models, one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`, and one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3`.<br>Possible values: `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `256x256`, `512x512`, `1792x1024`, `1024x1792` | No |  |
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

## Video generation jobs - Create

```HTTP
POST {endpoint}/openai/v1/video/generations/jobs?api-version=preview
```


Creates a new video generation job.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| before | query | No | string |  |
| after | query | No | string |  |
| limit | query | Yes | integer |  |
| statuses | query | No | array |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| job-id | path | Yes | string | The ID of the video generation job to use for the Azure OpenAI request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| job-id | path | Yes | string | The ID of the video generation job to use for the Azure OpenAI request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |
| quality | query | No |  |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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


Retrieves headers for the generated video content.
### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string<br>url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| api-version | query | No |  | The explicit Foundry Models API version to use for this request.<br>`v1` if not otherwise specified. |
| generation-id | path | Yes | string | The ID of the video generation to use for the Azure OpenAI request. |
| quality | query | No |  |  |

### Request Header

**Use either token based authentication or API key. Authenticating with token based authentication is recommended and more secure.**

| Name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | True | string | **Example:** `Authorization: Bearer {Azure_OpenAI_Auth_Token}`<br><br>**To generate an auth token using Azure CLI: `az account get-access-token --resource https://cognitiveservices.azure.com`**<br><br>Type: oauth2<br>Authorization Url: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`<br>scope: `https://ai.azure.com/.default`|
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

For the schema definitions used by chat, completions, embeddings, responses, and other text operations, see the [Azure OpenAI REST API reference](/rest/api/microsoft-foundry/azureopenai/chat?view=rest-microsoft-foundry-v1-preview&preserve-view=true). The following schemas support the image, audio, and video operations on this page.

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

### AzureErrorResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | object | The error details. | No |  |
| └─ code | string | The distinct, machine-generated identifier for the error. | No |  |
| └─ inner_error |  |  | No |  |
| └─ message | string | A human-readable message associated with the error. | No |  |
| └─ param | string | If applicable, the request input parameter associated with the error | No |  |
| └─ type | enum | The object type, always 'error.'<br>Possible values: `error` | No |  |

### AzureImagesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| background | enum | GPT-image-1 only: the background parameter used for the image generation. Either `transparent` or `opaque`.<br>Possible values: `transparent`, `opaque` | No |  |
| created | integer | The Unix timestamp (in seconds) of when the image was created. | Yes |  |
| data | array |  | No |  |
| output_format | enum | The output format of the image generation. Either `png`, `webp`, or `jpeg`.<br>Possible values: `png`, `webp`, `jpeg` | No |  |
| quality | enum | The quality of the image generated. Either `low`, `medium`, or `high`.<br>Possible values: `low`, `medium`, `high` | No |  |
| size | enum | The size of the image generated. Either `1024x1024`, `1024x1536`, or `1536x1024`.<br>Possible values: `1024x1024`, `1024x1536`, `1536x1024` | No |  |
| usage | object | For `gpt-image-1`-series models only, the token usage information for the image generation. | No |  |
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
| └─ error_details |  | The content filter result details associated with the inner error. | No |  |
| └─ revised_prompt | string | If applicable, the modified prompt used for generation. | No |  |
| message | string | A human-readable message associated with the error. | No |  |
| param | string | If applicable, the request input parameter associated with the error | No |  |
| type | string | If applicable, the input line number associated with the error. | No |  |

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
