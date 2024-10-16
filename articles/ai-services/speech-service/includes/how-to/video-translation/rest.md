---
title: include file
description: include file
author: sally-baolian
ms.author: v-baolianzou
ms.service: azure-ai-speech
ms.topic: include
ms.date: 10/11/2024
ms.custom: include
---

The video translation REST API facilitates seamless video translation integration into your applications. It supports uploading, managing, and refining video translations, with multiple iterations for continuous improvement. In this article, you learn how to utilize video translation through the REST API. 

This diagram provides a high-level overview of the workflow.

![Diagram of video translation API workflow.](../../../media/video-translation/video-translation-api-workflow.png)

You can use the following REST API operations for video translation:

| Operation                                             | Method | REST API call                                     |
| ----------------------------------------------------- | ------ | ------------------------------------------------- |
| [Create a translation](/rest/api/aiservices/videotranslation/translation-operations/create-translation) | `PUT`   | `/translations/{translationId}`                  |
| [List translations](/rest/api/aiservices/videotranslation/translation-operations/list-translation)   | `GET`   | `/translations`                                  |
| [Get a translation by translation ID](/rest/api/aiservices/videotranslation/translation-operations/get-translation)   | `GET`   | `/translations/{translationId}`     |
| [Create an iteration](/rest/api/aiservices/videotranslation/iteration-operations/create-iteration) | `PUT`   | `/translations/{translationId}/iterations/{iterationId}` |
| [List iterations](/rest/api/aiservices/videotranslation/iteration-operations/list-iteration)                 | `GET`   | `/translations/{translationId}/iterations`       |
| [Get an iteration by iteration ID](/rest/api/aiservices/videotranslation/iteration-operations/get-iteration) | `GET`   | `/translations/{translationId}/iterations/{iterationId}` |
| [Get operation by operation ID](/rest/api/aiservices/videotranslation/operation-operations/get-operation) | `GET`   | `/operations/{operationId}` |
| [Delete a translation by translation ID](/rest/api/aiservices/videotranslation/translation-operations/delete-translation) | `DELETE`| `/translations/{translationId}`                  |

For code samples, see [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/video-translation/csharp).

This article outlines the primary steps of the API process, including creating a translation, creating an iteration, checking the status of each operation, getting an iteration by iteration ID, and deleting a translation by translation ID. For complete details, refer to the links provided for each API in the table.

## Create a translation

To submit a video translation request, you need to construct an HTTP PUT request path and body according to the following instructions:

- Specify `Operation-Id`: The `Operation-Id` must be unique for each operation. It ensures that each operation is tracked separately. Replace `[operationId]` with an operation ID. 
- Specify `translationId`: The `translationId` must be unique. Replace `[translationId]` with a translation ID. 
- Set the required input: Include details like `sourceLocale`, `targetLocale`, `voiceKind`, and `videoFileUrl`. Ensure that you have the video URL from Azure Blob Storage. For the languages supported for video translation, refer to the [supported source and target languages](../../../language-support.md?tabs=speech-translation#video-translation). You can set `voiceKind` parameter to either `PlatformVoice` or `PersonalVoice`. For `PlatformVoice`, the system automatically selects the most suitable prebuilt voice by matching the speaker's voice in the video with prebuilt voices. For `PersonalVoice`, the system offers a model that generates high-quality voice replication in a few seconds.

   >[!NOTE]
   > To use personal voice, you need to apply for [access](https://aka.ms/customneural). 

- Replace `[YourResourceKey]` with your Speech resource key and replace `[YourSpeechRegion]` with your Speech resource region.
  
Creating a translation doesn't initiate the translation process. You can start translating the video by [creating an iteration](#create-an-iteration). The following example is for Windows shell. Ensure to escape `&` with `^&`  if the URL contains `&`. 

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: [YourResourceKey]" -H "Operation-Id: [operationId]" -H "Content-Type: application/json" -d "{\"displayName\": \"[YourDisplayName]\",\"description\": \"[OptionalYourDescription]\",\"input\": {\"sourceLocale\": \"[VideoSourceLocale]\",\"targetLocale\": \"[TranslationTargetLocale]\",\"voiceKind\": \"[PlatformVoice/PersonalVoice]\",\"speakerCount\": [OptionalVideoSpeakerCount],\"subtitleMaxCharCountPerSegment\": [OptionalYourPreferredSubtitleMaxCharCountPerSegment],\"exportSubtitleInVideo\": [Optional true/false],\"videoFileUrl\": \"[AzureBlobUrlWithSas]\"}}" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/translations/[translationId]?api-version=2024-05-20-preview" 
```

>[!IMPORTANT]
> Data created through the API won't appear in Speech Studio, and the data between the API and Speech Studio isn't synchronized.

You should receive a response body in the following format:

```json
{
  "input": {
    "sourceLocale": "zh-CN",
    "targetLocale": "en-US",
    "voiceKind": "PlatformVoice",
    "speakerCount": 1,
    "subtitleMaxCharCountPerSegment": 30,
    "exportSubtitleInVideo": true
  },
  "status": "NotStarted",
  "lastActionDateTime": "2024-09-20T06:25:05.058Z",
  "id": "mytranslation0920",
  "displayName": "demo",
  "description": "for testing",
  "createdDateTime": "2024-09-20T06:25:05.058Z"
}
```
The status property should progress from `NotStarted` status, to `Running`, and finally to `Succeeded` or `Failed`. You can call the [Get operation by operation ID](#get-operation-by-operation-id) API periodically until the returned status is `Succeeded` or `Failed`. This operation allows you to monitor the progress of your creating translation process.

## Get operation by operation ID

Check the status of a specific operation using its operation ID. The operation ID is unique for each operation, so you can track each operation separately.

Replace `[YourResourceKey]` with your Speech resource key,  `[YourSpeechRegion]` with your Speech resource region, and `[operationId]` with the operation ID you want to check.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key:[YourResourceKey]" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/operations/[operationId]?api-version=2024-05-20-preview" 
```

You should receive a response body in the following format:

```json
{
  "id": "createtranslation0920-1",
  "status": "Running"
}
```

## Create an iteration

To start translating your video or update an iteration for an existing translation, you need to construct an HTTP PUT request path and body according to the following instructions:

- Specify `Operation-Id`: The `Operation-Id` must be unique for each operation, such as creating each iteration. Replace `[operationId]` with a unique ID for this operation.
- Specify `translationId`: If multiple iterations are performed under a single translation, the translation ID remains unchanged.
- Specify `iterationId`: The `iterationId` must be unique for each operation. Replace `[iterationId]` with an iteration ID. 
- Set the required input: Include details like `speakerCount`, `subtitleMaxCharCountPerSegment`,`exportSubtitleInVideo`, or `webvttFile`. No subtitles are embedded in the output video by default. 
- Replace `[YourResourceKey]` with your Speech resource key and replace `[YourSpeechRegion]` with your Speech resource region. 

The following example is for Windows shell. Ensure to escape `&` with `^&`  if the URL contains `&`.

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: [YourResourceKey]" -H "Operation-Id: [operationId]"  -H "Content-Type: application/json" -d "{\"input\": {\"speakerCount\": [OptionalVideoSpeakerCount],\"subtitleMaxCharCountPerSegment\": [OptionalYourPreferredSubtitleMaxCharCountPerSegment],\"exportSubtitleInVideo\": [Optional true/false],\"webvttFile\": {\"Kind\": \"[SourceLocaleSubtitle/TargetLocaleSubtitle/MetadataJson]\", \"url\": \"[AzureBlobUrlWithSas]\"}}}" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/translations/[translationId]/iterations/[iterationId]?api-version=2024-05-20-preview"  
```

> [!NOTE]
> When creating an iteration, if you've already specified the optional parameters `speakerCount`, `subtitleMaxCharCountPerSegment`, and `exportSubtitleInVideo` during the creation of translation, you don’t need to specify them again. The values will inherit from translation settings. Once these parameters are defined when creating an iteration, the new values will override the original settings. 
> 
> The `webvttFile` parameter isn't required when creating the first iteration. However, starting from the second iteration, you must specify the `webvttFile` parameter in the iteration process. You need to download the webvtt file, make necessary edits, and then upload it to your Azure Blob storage. You need to specify the Blob URL in the curl code.
>
> Data created through the API won't appear in Speech Studio, and the data between the API and Speech Studio isn't synchronized.

The subtitle file can be in WebVTT or JSON format. If you're unsure about how to prepare a WebVTT file, refer to the following sample formats. 

#### [WebVTT](#tab/webvtt)

```WebVTT

00:00:01.010 --> 00:00:06.030
Hello this is a sample subtitle.

00:00:07.030 --> 00:00:09.030
Hello this is a sample subtitle.

```

#### [WebVTT with JSON Metadata](#tab/webvttwithjsonmetadata)

```WebVTT with JSON Metadata

00:00:01.010 --> 00:00:02.030
{
  "globalMetadata": {
    "locale": "zh-CN",
    "changeTtsVoiceNameIfConflictWithGender": true,
    "speakers": {
      "PlatformVoice_zh-CN-XiaoxiaoNeural": {
        "defaultSsmlProperties": {
          "voiceKind": "PlatformVoice",
          "voiceName": "zh-CN-XiaoxiaoNeural"
        }
      },
      "PlatformVoice_zh-CN-YunxiNeural": {
        "defaultSsmlProperties": {
          "voiceKind": "PlatformVoice",
          "voiceName": "zh-CN-YunxiNeural"
        }
      },
      "PlatformVoice_ja-JP-NanamiNeural": {
        "defaultSsmlProperties": {
          "voiceKind": "PlatformVoice",
          "voiceName": "ja-JP-NanamiNeural"
        }
      }
    }
  },
  "speakerId": "PlatformVoice_zh-CN-XiaoxiaoNeural",
  "translatedText": "中文晓晓"
}

00:00:02.510 --> 00:00:04.030
{
  "gender": "Female",
  "speakerId": "PlatformVoice_ja-JP-NanamiNeural",
  "translatedText": "こんにちは、これはサンプルの字幕です",
  "comment": "Keep using jaJP voice."
}

00:00:05.010 --> 00:00:07.030
{
  "gender": "Male",
  "speakerId": "PlatformVoice_ja-JP-NanamiNeural",
  "translatedText": "こんにちは、これはサンプルの字幕です",
  "comment": "Not correct gender, will auto be replaced by enUS auto voice selection."
}

```
---

You should receive a response body in the following format:

```json
{
  "input": {
    "speakerCount": 1,
    "subtitleMaxCharCountPerSegment": 30,
    "exportSubtitleInVideo": true
  },
  "status": "Not Started",
  "lastActionDateTime": "2024-09-20T06:31:53.760Z",
  "id": "firstiteration0920",
  "createdDateTime": "2024-09-20T06:31:53.760Z"
}
```

You can use `operationId` you specified and call the [Get operation by operation ID](#get-operation-by-operation-id) API periodically until the returned status is `Succeeded` or `Failed`. This operation allows you to monitor the progress of your creating the iteration process.

## Get an iteration by iteration ID

To retrieve details of a specific iteration by its ID, use the HTTP GET request. Replace `[YourResourceKey]` with your Speech resource key,  `[YourSpeechRegion]` with your Speech resource region, `[translationId]` with the translation ID you want to check,  and `[iterationId]` with the iteration ID you want to check.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: [YourResourceKey]" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/translations/[translationId]/iterations/[iterationId]?api-version=2024-05-20-preview"  
```

You should receive a response body in the following format:

```json
{
  "input": {
    "speaker Count": 1,
    "subtitleMaxCharCountPerSegment": 30,
    "exportSubtitleInVideo": true
  },
  "result": {
    "translatedVideoFileUrl": "https://xxx.blob.core.windows.net/container1/video.mp4?sv=2023-01-03&st=2024-05-20T08%3A27%3A15Z&se=2024-05-21T08%3A27%3A15Z&sr=b&sp=r&sig=xxx",
    "sourceLocaleSubtitleWebvttFileUrl": "https://xxx.blob.core.windows.net/container1/sourceLocale.vtt?sv=2023-01-03&st=2024-05-20T08%3A27%3A15Z&se=2024-05-21T08%3A27%3A15Z&sr=b&sp=r&sig=xxx",
    "targetLocaleSubtitleWebvttFileUrl": "https://xxx.blob.core.windows.net/container1/targetLocale.vtt?sv=2023-01-03&st=2024-05-20T08%3A27%3A15Z&se=2024-05-21T08%3A27%3A15Z&sr=b&sp=r&sig=xxx",
    "metadataJsonWebvttFileUrl": "https://xxx.blob.core.windows.net/container1/metadataJsonLocale.vtt?sv=2023-01-03&st=2024-05-20T08%3A27%3A15Z&se=2024-05-21T08%3A27%3A15Z&sr=b&sp=r&sig=xxx"
  },
  "status": "Succeeded",
  "lastActionDateTime": "2024-09-20T06:32:59.933Z",
  "id": "firstiteration0920",
  "createdDateTime": "2024-09-20T06:31:53.760Z"
}
```

## Delete a translation by translation ID

Remove a specific translation identified by `translationId`. This operation also removes all iterations associated with this translation. Replace `[YourResourceKey]` with your Speech resource key,  `[YourSpeechRegion]` with your Speech resource region, and `[translationId]` with the translation ID you want to delete.

```azurecli-interactive
curl -v -X DELETE -H "Ocp-Apim-Subscription-Key: [YourResourceKey]" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/translations/[translationId]?api-version=2024-05-20-preview" 
```

The response headers include `HTTP/1.1 204 No Content` if the delete request was successful.

## Additional information

This section provides curl commands for other API calls that aren't described in detail above. You can explore each API using the following commands.

### List translations

To list all video translations that have been uploaded and processed in your resource account, make an HTTP GET request as shown in the following example. Replace `YourResourceKey` with your Speech resource key and replace `YourSpeechRegion` with your Speech resource region.   

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: [YourResourceKey]" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/translations?api-version=2024-05-20-preview"
```

### Get a translation by translation ID

This operation retrieves detailed information about a specific translation, identified by its unique `translationId`. Replace `[YourResourceKey]` with your Speech resource key,  `[YourSpeechRegion]` with your Speech resource region, and `[translationId]` with the translation ID you want to check.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: [YourResourceKey]" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/translations/[translationId]?api-version=2024-05-20-preview" 
```

### List iterations

List all iterations for a specific translation. This request lists all iterations without detailed information. Replace `[YourResourceKey]` with your Speech resource key,  `[YourSpeechRegion]` with your Speech resource region, and `[translationId]` with the translation ID you want to check.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: [YourResourceKey]" "https://[YourSpeechRegion].api.cognitive.microsoft.com/videotranslation/translations/[translationId]/iterations?api-version=2024-05-20-preview"  
```

## HTTP status codes

The section details the HTTP response codes and messages from the video translation REST API.

### HTTP 200 OK

HTTP 200 OK indicates that the request was successful.

### HTTP 204 error

An HTTP 204 error indicates that the request was successful, but the resource doesn't exist. For example:

- You tried to get or delete a translation that doesn't exist.
- You successfully deleted a translation. 

### HTTP 400 error

Here are examples that can result in the 400 error:

- The source or target locale you specified isn't among the [supported locales](../../../language-support.md?tabs=speech-translation#video-translation).
- You tried to use a _F0_ Speech resource, but the region only supports the _Standard_ Speech resource pricing tier.

### HTTP 500 error

HTTP 500 Internal Server Error indicates that the request failed. The response body contains the error message.

## Related content

- [Video translation overview](../../../video-translation-overview.md)
