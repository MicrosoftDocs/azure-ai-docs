---
title: Azure OpenAI latest preview inference API documentation
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Latest preview data plane inference documentation generated from OpenAPI 3.0 spec
manager: mcleans
ms.date: 05/14/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.custom:
  - build-2025
ai-usage: ai-assisted
---

## Transcriptions - Create

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/transcriptions?api-version=2025-04-01-preview
```

Transcribes audio into the input language.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| deployment-id | path | Yes | string |  |
| api-version | query | Yes | string |  |

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
|model | string | ID of the model to use. The options are `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-4o-mini-transcribe-2025-12-15`, `whisper-1`, and `gpt-4o-transcribe-diarize`.| Yes |  |
| file | string | The audio file object to transcribe. | Yes |  |
| language | string | The language of the input audio. Supplying the input language in ISO-639-1 format improves accuracy and latency. | No |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language. | No |  |
| response_format | [audioResponseFormat](#audioresponseformat) | Defines the format of the output. | No |  |
| temperature | number | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model uses log probability to automatically increase the temperature until certain thresholds are hit. | No | 0 |
| timestamp_granularities[] | array | The timestamp granularities to populate for this transcription. `response_format` must be set `verbose_json` to use timestamp granularities. Either or both of these options are supported: `word`, or `segment`. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency. | No | ['segment'] |

### Responses

**Status Code:** 200

**Description**: OK 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |
|text/plain | string | Transcribed text in the output format (when response_format was one of `text`, `vtt` or `srt`).|

### Examples

### Example

Gets transcribed text and associated metadata from provided spoken audio data.

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/transcriptions?api-version=2025-04-01-preview

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
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/transcriptions?api-version=2025-04-01-preview

"---multipart-boundary\nContent-Disposition: form-data; name=\"file\"; filename=\"file.wav\"\nContent-Type: application/octet-stream\n\nRIFF..audio.data.omitted\n---multipart-boundary--"

```

**Responses**:
Status Code: 200

```json
{
  "type": "string",
  "example": "plain text when requesting text, srt, or vtt"
}
```

## Translations - Create

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/translations?api-version=2025-04-01-preview
```

Transcribes and translates input audio into English text.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| deployment-id | path | Yes | string |  |
| api-version | query | Yes | string |  |

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
| file | string | The audio file to translate. | Yes |  |
| prompt | string | An optional text to guide the model's style or continue a previous audio segment. The prompt should be in English. | No |  |
| response_format | [audioResponseFormat](#audioresponseformat) | Defines the format of the output. | No |  |
| temperature | number | The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model uses log probability to automatically increase the temperature until certain thresholds are hit. | No | 0 |

### Responses

**Status Code:** 200

**Description**: OK 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | object | |
|text/plain | string | Transcribed text in the output format (when response_format was one of text, vtt, or srt).|

### Examples

### Example

Gets English language transcribed text and associated metadata from provided spoken audio data.

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/translations?api-version=2025-04-01-preview

"---multipart-boundary\nContent-Disposition: form-data; name=\"file\"; filename=\"file.wav\"\nContent-Type: application/octet-stream\n\nRIFF..audio.data.omitted\n---multipart-boundary--"

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

Gets English language transcribed text and associated metadata from provided spoken audio data.

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/translations?api-version=2025-04-01-preview

"---multipart-boundary\nContent-Disposition: form-data; name=\"file\"; filename=\"file.wav\"\nContent-Type: application/octet-stream\n\nRIFF..audio.data.omitted\n---multipart-boundary--"

```

**Responses**:
Status Code: 200

```json
{
  "type": "string",
  "example": "plain text when requesting text, srt, or vtt"
}
```

## Speech - Create

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/speech?api-version=2025-04-01-preview
```

Generates audio from the input text.

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| deployment-id | path | Yes | string |  |
| api-version | query | Yes | string |  |

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
| input | string | The text to synthesize audio for. The maximum length is 4,096 characters. | Yes |  |
| response_format | enum | The format to synthesize the audio in.<br>Possible values: `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm` | No |  |
| speed | number | The speed of the synthesized audio. Select a value from `0.25` to `4.0`. `1.0` is the default. | No | 1.0 |
| voice | enum | The voice to use for speech synthesis.<br>Possible values: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer` | Yes |  |

### Responses

**Status Code:** 200

**Description**: OK 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/octet-stream | string | |

### Examples

### Example

Synthesizes audio from the provided text.

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/audio/speech?api-version=2025-04-01-preview

{
 "input": "Hi! What are you going to make?",
 "voice": "fable",
 "response_format": "mp3"
}

```

**Responses**:
Status Code: 200

```json
{
  "body": "101010101"
}
```

## Image generations - Create

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/images/generations?api-version=2025-04-01-preview
```

Generates a batch of images from a text caption on a given image generation model deployment

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| deployment-id | path | Yes | string |  |
| api-version | query | Yes | string |  |

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
| background | [imageBackground](#imagebackground) | Allows to set transparency for the background of the generated images. This parameter is only supported for gpt-image-1 series models. | No | auto |
| n | integer | The number of images to generate. For dall-e-3, only n=1 is supported. | No | 1 |
| output_compression | integer | The compression level (0-100%) for the generated images. This parameter is only supported for gpt-image-1 series models with the jpeg output format. | No | 100 |
| output_format | [imagesOutputFormat](#imagesoutputformat) | The file format in which the generated images are returned. Only supported for gpt-image-1 series models. | No | png |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters for gpt-image-1 series and 4000 characters for dall-e-3 | Yes |  |
|partial_images| integer | The number of partial images to generate. This parameter is used for streaming responses that return partial images. Value must be between 0 and 3. When set to 0, the response will be a single image sent in one streaming event. Note that the final image may be sent before the full number of partial images are generated if the full image is generated more quickly. | 0 |
| stream | boolean | Edit the image in streaming mode. | no | `false` |
| quality | [imageQuality](#imagequality) | The quality of the image that will be generated. | No | auto |
| response_format | [imagesResponseFormat](#imagesresponseformat) | The format in which the generated images are returned. This parameter isn't supported for `gpt-image-1`-series models which will always return base64-encoded images.<br>Possible values: `url`, `b64_json`. | No | url |
| size | [imageSize](#imagesize) | The size of the generated images. | No | auto |
| style | [imageStyle](#imagestyle) | The style of the generated images. Only supported for dall-e-3. | No | vivid |
| user | string | A unique identifier representing your end-user, which can help to monitor and detect abuse. | No |  |

### Responses

**Status Code:** 200

**Description**: Ok 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [generateImagesResponse](#generateimagesresponse) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [dalleErrorResponse](#dalleerrorresponse) | |

### Examples

### Example

Creates images given a prompt.

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/images/generations?api-version=2025-04-01-preview

{
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

## Image generations - Edit

```HTTP
POST https://{endpoint}/openai/deployments/{deployment-id}/images/edits?api-version=2025-04-01-preview
```

Edits an image from a text caption on a given gpt-image-1 model deployment

### URI Parameters

| Name | In | Required | Type | Description |
|------|------|----------|------|-----------|
| endpoint | path | Yes | string url | Supported Azure OpenAI endpoints (protocol and hostname, for example: `https://aoairesource.openai.azure.com`. Replace "aoairesource" with your Azure OpenAI resource name). https://{your-resource-name}.openai.azure.com |
| deployment-id | path | Yes | string |  |
| api-version | query | Yes | string |  |

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
| image | string or array | The image(s) to edit. Must be a supported image file or an array of images. Each image should be a png, or jpg file less than 50MB. | Yes |  |
| input_fidelity| string | Control how much effort the model will exert to match the style and features, especially facial features, of input images. This parameter is only supported for gpt-image-1 series models. Supports `high` and `low`. | no |  `low`. | 
| mask | string | An additional image whose fully transparent areas (e.g., where alpha is zero) indicate where the image should be edited. If there are multiple images provided, the mask will be applied to the first image. Must be a valid PNG file, less than 4MB, and have the same dimensions as the image. | No |  |
| n | integer | The number of images to generate.  Must be between 1 and 10. | No | 1 |
| prompt | string | A text description of the desired image(s). The maximum length is 32000 characters. | Yes |  |
| quality | [imageQuality](#imagequality) | The quality of the image that will be generated. | No | auto |
|partial_images| The number of partial images to generate. This parameter is used for streaming responses that return partial images. Value must be between 0 and 3. When set to 0, the response will be a single image sent in one streaming event. Note that the final image may be sent before the full number of partial images are generated if the full image is generated more quickly. |
| stream | boolean | Edit the image in streaming mode. | no | `false` |
| response_format | [imagesResponseFormat](#imagesresponseformat) | The format in which the generated images are returned. | No | url |
| size | [imageSize](#imagesize) | The size of the generated images. | No | auto |
| user | string | A unique identifier representing your end-user, which can help to monitor and detect abuse. | No |  |

### Responses

**Status Code:** 200

**Description**: Ok 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [generateImagesResponse](#generateimagesresponse) | |

**Status Code:** default

**Description**: An error occurred. 

|**Content-Type**|**Type**|**Description**|
|:---|:---|:---|
|application/json | [dalleErrorResponse](#dalleerrorresponse) | |

## Components

For the schema definitions used by chat, completions, embeddings, responses, and other text operations, see the [Azure OpenAI REST API reference](/rest/api/microsoft-foundry/azureopenai/chat?view=rest-microsoft-foundry-v1-preview&preserve-view=true). The following schemas support the image and audio operations on this page.

### innerErrorCode

Error codes for the inner error object.

| Property | Value |
|----------|-------|
| **Description** | Error codes for the inner error object. |
| **Type** | string |
| **Values** | `ResponsibleAIPolicyViolation` |

### dalleErrorResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| error | [dalleError](#dalleerror) |  | No |  |

### dalleError

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| inner_error | [dalleInnerError](#dalleinnererror) | Inner error with additional details. | No |  |
| param | string |  | No |  |
| type | string |  | No |  |

### dalleInnerError

Inner error with additional details.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| code | [innerErrorCode](#innererrorcode) | Error codes for the inner error object. | No |  |
| content_filter_results | [dalleFilterResults](#dallefilterresults) | Information about the content filtering category (hate, sexual, violence, self_harm), if it has been detected, as well as the severity level (very_low, low, medium, high-scale that determines the intensity and risk level of harmful content) and if it has been filtered or not. Information about jailbreak content and profanity, if it has been detected, and if it has been filtered or not. And information about customer block list, if it has been filtered and its id. | No |  |
| revised_prompt | string | The prompt that was used to generate the image, if there was any revision to the prompt. | No |  |

### contentFilterSeverityResult

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| filtered | boolean |  | Yes |  |
| severity | string |  | No |  |

### contentFilterDetectedResult

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| detected | boolean |  | No |  |
| filtered | boolean |  | Yes |  |

### contentFilterDetailedResults

Content filtering results with a detail of content filter ids for the filtered segments.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| details | array |  | No |  |
| filtered | boolean |  | Yes |  |

### dalleFilterResults

Information about the content filtering category (hate, sexual, violence, self_harm), if it has been detected, as well as the severity level (very_low, low, medium, high-scale that determines the intensity and risk level of harmful content) and if it has been filtered or not. Information about jailbreak content and profanity, if it has been detected, and if it has been filtered or not. And information about customer block list, if it has been filtered and its id.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| custom_blocklists | [contentFilterDetailedResults](#contentfilterdetailedresults) | Content filtering results with a detail of content filter ids for the filtered segments. | No |  |
| hate | [contentFilterSeverityResult](#contentfilterseverityresult) |  | No |  |
| jailbreak | [contentFilterDetectedResult](#contentfilterdetectedresult) |  | No |  |
| profanity | [contentFilterDetectedResult](#contentfilterdetectedresult) |  | No |  |
| self_harm | [contentFilterSeverityResult](#contentfilterseverityresult) |  | No |  |
| sexual | [contentFilterSeverityResult](#contentfilterseverityresult) |  | No |  |
| violence | [contentFilterSeverityResult](#contentfilterseverityresult) |  | No |  |

### audioResponseFormat

Defines the format of the output.

| Property | Value |
|----------|-------|
| **Description** | Defines the format of the output. |
| **Type** | string |
| **Values** | `json`<br>`text`<br>`srt`<br>`verbose_json`<br>`vtt` |

### imageQuality

The quality of the image that will be generated.

| Property | Value |
|----------|-------|
| **Description** | The quality of the image that will be generated. |
| **Type** | string |
| **Default** | auto |
| **Values** | `auto`<br>`high`<br>`medium`<br>`low`<br>`hd`<br>`standard` |

### imagesResponseFormat

The format in which the generated images are returned.

| Property | Value |
|----------|-------|
| **Description** | The format in which the generated images are returned. |
| **Type** | string |
| **Default** | url |
| **Values** | `url`<br>`b64_json` |

### imagesOutputFormat

The file format in which the generated images are returned. Only supported for  series models.

| Property | Value |
|----------|-------|
| **Description** | The file format in which the generated images are returned. Only supported for gpt-image-1 series models. |
| **Type** | string |
| **Default** | png |
| **Values** | `png`<br>`jpeg` |

### imageSize

The size of the generated images.

| Property | Value |
|----------|-------|
| **Description** | The size of the generated images. |
| **Type** | string |
| **Default** | auto |
| **Values** | `auto`<br>`1792x1024`<br>`1024x1792`<br>`1024x1024`<br>`1024x1536`<br>`1536x1024` |

### imageStyle

The style of the generated images. Only supported for dall-e-3.

| Property | Value |
|----------|-------|
| **Description** | The style of the generated images. Only supported for dall-e-3. |
| **Type** | string |
| **Default** | vivid |
| **Values** | `vivid`<br>`natural` |

### imageBackground

Allows to set transparency for the background of the generated image(s). This parameter is only supported for gpt-image-1 series models.

| Property | Value |
|----------|-------|
| **Description** | Allows to set transparency for the background of the generated image(s). This parameter is only supported for gpt-image-1 series models. |
| **Type** | string |
| **Default** | auto |
| **Values** | `transparent`<br>`opaque`<br>`auto` |

### generateImagesResponse

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| created | integer | The unix timestamp when the operation was created. | Yes |  |
| data | array | The result data of the operation, if successful | Yes |  |
| usage | [imageGenerationsUsage](#imagegenerationsusage) | Represents token usage details for image generation requests. Only for gpt-image-1 series models. | No |  |

### imageGenerationsUsage

Represents token usage details for image generation requests. Only for gpt-image-1 series models.

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| input_tokens | integer | The number of input tokens. | No |  |
| input_tokens_details | object | A detailed breakdown of the input tokens. | No |  |
| └─ image_tokens | integer | The number of image tokens. | No |  |
| └─ text_tokens | integer | The number of text tokens. | No |  |
| output_tokens | integer | The number of output tokens. | No |  |
| total_tokens | integer | The total number of tokens used. | No |  |

