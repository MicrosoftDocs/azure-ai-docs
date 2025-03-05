---
title: include file
description: include file
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: include
ms.date: 3/4/2025
ms.custom: references_regions
---

The video translation REST API facilitates seamless video translation integration into your applications. It supports uploading, managing, and refining video translations, with multiple iterations for continuous improvement. In this article, you learn how to utilize video translation through the REST API. 

## REST API operations

You can use the following REST API operations for video translation:

| Operation | Method | REST API call |
| ----------------------------------------------------- | ------ | ------------------------------------------------- |
| [Create a translation](/rest/api/aiservices/videotranslation/translation-operations/create-translation) | `PUT` | `/translations/{translationId}` |
| [List translations](/rest/api/aiservices/videotranslation/translation-operations/list-translation)   | `GET` | `/translations`|
| [Get a translation by translation ID](/rest/api/aiservices/videotranslation/translation-operations/get-translation)   | `GET` | `/translations/{translationId}` |
| [Create an iteration](/rest/api/aiservices/videotranslation/iteration-operations/create-iteration) | `PUT` | `/translations/{translationId}/iterations/{iterationId}` |
| [List iterations](/rest/api/aiservices/videotranslation/iteration-operations/list-iteration)| `GET` | `/translations/{translationId}/iterations` |
| [Get an iteration by iteration ID](/rest/api/aiservices/videotranslation/iteration-operations/get-iteration) | `GET` | `/translations/{translationId}/iterations/{iterationId}` |
| [Get operation by operation ID](/rest/api/aiservices/videotranslation/operation-operations/get-operation) | `GET` | `/operations/{operationId}` |
| [Delete a translation by translation ID](/rest/api/aiservices/videotranslation/translation-operations/delete-translation) | `DELETE`| `/translations/{translationId}` |

This article outlines the primary steps of the API process:
- Create a translation
- Create an iteration
- Check the status of each operation
- Get an iteration by iteration ID
- Delete a translation by translation ID

For more code samples, see [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/video-translation/csharp).

## Pre-requisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin.
- A Speech resource [in a supported region](../../../video-translation-overview.md#supported-regions-and-languages). If you don't have a Speech resource, create one in the [Azure portal](https://portal.azure.com/).
- You need a video file in .mp4 format, less than 500 MB, and shorter than 60 minutes. For testing purposes, you can use the sample video file provided by Microsoft at [https://speechstudioprodpublicsa.blob.core.windows.net/ttsvoice/VideoTranslation/PublicDoc/SampleData/es-ES-TryOutOriginal.mp4](https://speechstudioprodpublicsa.blob.core.windows.net/ttsvoice/VideoTranslation/PublicDoc/SampleData/es-ES-TryOutOriginal.mp4).
- Make sure video translation supports your [source and target language](../../../language-support.md?tabs=speech-translation#video-translation).

> [!TIP]
> Before you start, see the [video translation overview](../../../video-translation-overview.md#how-it-works) to understand the end-to-end process of video translation.

## Create a translation

> [!IMPORTANT]
> Creating a translation as described in this section doesn't initiate the translation process. You can start translating the video by [creating an iteration](#create-an-iteration). 

To create a video translation, you need to construct an HTTP PUT request path and body according to the following instructions: 

- Specify `displayName`: The display name of the translation. This is a user-friendly name that helps you identify the translation.
- Specify `description`: A brief description of the translation. This is optional but can be helpful for documentation purposes.
- Specify the `sourceLocale`: The language of the original video. This is the language spoken in the video file.
- Specify the `targetLocale`: The language you want to translate the video into. This is the target language for the translation.
- Specify `voiceKind`: The type of voice you want to use for the translation. You can choose between `PlatformVoice` and `PersonalVoice`. For `PlatformVoice`, the system automatically selects the most suitable prebuilt voice by matching the speaker's voice in the video with prebuilt voices. For `PersonalVoice`, the system offers a model that generates high-quality voice replication in a few seconds.

   > [!NOTE]
   > To use personal voice, you need to apply for [access](https://aka.ms/customneural).
- Specify `speakerCount`: The number of speakers in the video. This is an optional parameter, and you can set it to 1 if you're unsure.
- Specify `subtitleMaxCharCountPerSegment`: The maximum number of characters allowed per subtitle segment. This is an optional parameter, and you can set it to 30 if you're unsure.
- Specify `exportSubtitleInVideo`: A boolean value indicating whether to export subtitles in the video. This is an optional parameter, and you can set it to `true` if you want to include subtitles in the video.
- Specify the `videoFileUrl`: The URL of the video file you want to translate. The video must be in .mp4 format, less than 500 MB, and shorter than 60 minutes. You can upload the video to Azure Blob Storage and use the Blob URL. For testing purposes, you can use the sample video file provided by Microsoft at [https://speechstudioprodpublicsa.blob.core.windows.net/ttsvoice/VideoTranslation/PublicDoc/SampleData/es-ES-TryOutOriginal.mp4](https://speechstudioprodpublicsa.blob.core.windows.net/ttsvoice/VideoTranslation/PublicDoc/SampleData/es-ES-TryOutOriginal.mp4).
- Specify `Operation-Id`: The `Operation-Id` must be unique for each operation. It ensures that each operation is tracked separately. In the example, `MyOperationID-1` is used. Replace `MyOperationID-1` with an operation ID of your choice. 
- Specify `translationId`: The `translationId` must be unique. Replace `MyTranslationID` with a translation ID of your choice.
- Replace `YourSpeechResourceKey` with your Speech resource key and replace `YourSpeechResourceRegion` with your Speech resource region.

To create a translation, run the following command with the settings as previously described. 

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" -H "Operation-Id: MyOperationID-1" -H "Content-Type: application/json" -d '{
  "displayName": "My Translation",
  "description": "Create translation via REST API",
  "input": {
    "sourceLocale": "es-ES",
    "targetLocale": "en-US",
    "voiceKind": "PlatformVoice",
    "speakerCount": 1,
    "subtitleMaxCharCountPerSegment": 30,
    "exportSubtitleInVideo": true,
    "videoFileUrl": "https://speechstudioprodpublicsa.blob.core.windows.net/ttsvoice/VideoTranslation/PublicDoc/SampleData/es-ES-TryOutOriginal.mp4"
  }
}' "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/translations/MyTranslationID?api-version=2024-05-20-preview"
```

> [!IMPORTANT]
> Data created through the API won't appear in Speech Studio, and the data between the API and Speech Studio isn't synchronized.

You should receive a response body in the following format:

```json
{
  "input": {
    "sourceLocale": "es-ES",
    "targetLocale": "en-US",
    "voiceKind": "PlatformVoice",
    "speakerCount": 1,
    "subtitleMaxCharCountPerSegment": 30,
    "exportSubtitleInVideo": true
  },
  "status": "NotStarted",
  "lastActionDateTime": "2025-03-02T16:49:46.837Z",
  "id": "MyTranslationID",
  "displayName": "My Translation",
  "description": "Create translation via REST API",
  "createdDateTime": "2025-03-02T16:49:46.837Z"
}
```

The initial status of the translation is `NotStarted`. You can call the [Get operation by operation ID](#get-operation-by-operation-id) API periodically until the returned status is `Succeeded` or `Failed`. This operation allows you to monitor the progress of your creating translation process. The status property should progress from `NotStarted` status, to `Running`, and finally to `Succeeded` or `Failed`. 

## Get operation by operation ID

Check the status of a specific operation using its operation ID. The operation ID is unique for each operation, so you can track each operation separately.

- Specify the same `Operation-Id` that you used when creating the translation. In the example, `MyOperationID-1` is used. Replace `MyOperationID-1` with an operation ID of your choice. 
- Replace `YourSpeechResourceKey` with your Speech resource key and replace `YourSpeechResourceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key:YourSpeechResourceKey" "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/operations/MyOperationID-1?api-version=2024-05-20-preview" 
```

You should receive a response body in the following format:

```json
{
  "id": "MyOperationID-1",
  "status": "Running"
}
```

## Create an iteration

To start translating your video or update an iteration for an existing translation, you need to construct an HTTP PUT request path and body according to the following instructions:

- Specify `Operation-Id`: The `Operation-Id` must be unique for each operation, such as creating each iteration. Replace `YourOperationId` with a unique ID for this operation.
- Specify `translationId`: If multiple iterations are performed under a single translation, the translation ID remains unchanged.
- Specify `iterationId`: The `iterationId` must be unique for each operation. Replace `YourIterationId` with an iteration ID of your choice.
- Set the required input: Include details like `speakerCount`, `subtitleMaxCharCountPerSegment`,`exportSubtitleInVideo`, or `webvttFile`. No subtitles are embedded in the output video by default. 
- Replace `YourSpeechResourceKey` with your Speech resource key and replace `YourSpeechResourceRegion` with your Speech resource region. 

```azurecli-interactive
curl -v -X PUT -H "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" \
-H "Operation-Id: YourOperationId" \
-H "Content-Type: application/json" \
-d '{
  "input": {
    "speakerCount": [OptionalVideoSpeakerCount],
    "subtitleMaxCharCountPerSegment": [OptionalYourPreferredSubtitleMaxCharCountPerSegment],
    "exportSubtitleInVideo": [Optional true/false],
    "webvttFile": {
      "Kind": "[SourceLocaleSubtitle/TargetLocaleSubtitle/MetadataJson]",
      "url": "[AzureBlobUrlWithSas]"
    }
  }
}' "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/translations/YourTranslationId/iterations/YourIterationId?api-version=2024-05-20-preview"
```

When creating an iteration, if you already specified the optional parameters `speakerCount`, `subtitleMaxCharCountPerSegment`, and `exportSubtitleInVideo` during the creation of translation, you don’t need to specify them again. The values inherit from translation settings. Once these parameters are defined when creating an iteration, the new values override the original settings. 

The `webvttFile` parameter isn't required when creating the first iteration. However, starting from the second iteration, you must specify the `webvttFile` parameter in the iteration process. You need to download the webvtt file, make necessary edits, and then upload it to your Azure Blob storage. You need to specify the Blob URL in the curl code.

Data created through the API doesn't appear in Speech Studio, and the data between the API and Speech Studio isn't synchronized.

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
    "subtitleMaxCharCountPerSegment": 50,
    "exportSubtitleInVideo": true
  },
  "status": "NotStarted",
  "lastActionDateTime": "2025-03-03T18:22:01.852Z",
  "id": "MyIterationId-1",
  "description": "Create translation via REST API",
  "createdDateTime": "2025-03-03T18:22:01.852Z"
}
```

You can use `operationId` that you specified and use the [Get operation by operation ID](#get-operation-by-operation-id) API periodically until the returned status is `Succeeded` or `Failed`. This operation allows you to monitor the progress of your creating the iteration process.

## Get an iteration by iteration ID

To retrieve details of a specific iteration by its ID, use the HTTP GET request. Replace `YourSpeechResourceKey` with your Speech resource key,  `YourSpeechResourceRegion` with your Speech resource region, `YourTranslationId` with the translation ID you want to check,  and `YourIterationId` with the iteration ID you want to check.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/translations/YourTranslationId/iterations/YourIterationId?api-version=2024-05-20-preview"  
```

You should receive a response body in the following format:

```json
{
  "input": {
    "speakerCount": 1,
    "subtitleMaxCharCountPerSegment": 50,
    "exportSubtitleInVideo": true
  },
  "result": {
    "translatedVideoFileUrl": "https://cvoiceprodeus.blob.core.windows.net/YourTranlatedVideoFileUrl",
    "sourceLocaleSubtitleWebvttFileUrl": "https://cvoiceprodeus.blob.core.windows.net/YourSourceLocaleSubtitleWebvttFileUrl",
    "targetLocaleSubtitleWebvttFileUrl": "https://cvoiceprodeus.blob.core.windows.net/YourTargetLocaleSubtitleWebvttFileUrl",
    "metadataJsonWebvttFileUrl": "https://cvoiceprodeus.blob.core.windows.net/YourMetadataJsonWebvttFileUrl",
  },
  "status": "Succeeded",
  "lastActionDateTime": "2025-03-03T18:26:37.743Z",
  "id": "MyIterationId-1",
  "description": "Create translation via REST API",
  "createdDateTime": "2025-03-03T18:22:01.853Z"
}
```

## Delete a translation by translation ID

Remove a specific translation identified by `translationId`. This operation also removes all iterations associated with this translation. Replace `YourSpeechResourceKey` with your Speech resource key,  `YourSpeechResourceRegion` with your Speech resource region, and `YourTranslationId` with the translation ID you want to delete. If not deleted manually, the service retains the translation history for up to 31 days.

```azurecli-interactive
curl -v -X DELETE -H "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/translations/YourTranslationId?api-version=2024-05-20-preview" 
```

The response headers include `HTTP/1.1 204 No Content` if the delete request was successful.

## Additional information

This section provides curl commands for other API calls that aren't described in detail previously. You can explore each API using the following commands.

### List translations

To list all video translations that are uploaded and processed in your resource account, make an HTTP GET request as shown in the following example. Replace `YourSpeechResourceKey` with your Speech resource key and replace `YourSpeechResourceRegion` with your Speech resource region.   

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/translations?api-version=2024-05-20-preview"
```

### Get a translation by translation ID

This operation retrieves detailed information about a specific translation, identified by its unique `translationId`. Replace `YourSpeechResourceKey` with your Speech resource key,  `YourSpeechResourceRegion` with your Speech resource region, and `YourTranslationId` with the translation ID you want to check.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/translations/YourTranslationId?api-version=2024-05-20-preview" 
```

### List iterations

List all iterations for a specific translation. This request lists all iterations without detailed information. Replace `YourSpeechResourceKey` with your Speech resource key,  `YourSpeechResourceRegion` with your Speech resource region, and `YourTranslationId` with the translation ID you want to check.

```azurecli-interactive
curl -v -X GET -H "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" "https://YourSpeechResourceRegion.api.cognitive.microsoft.com/videotranslation/translations/YourTranslationId/iterations?api-version=2024-05-20-preview"  
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
