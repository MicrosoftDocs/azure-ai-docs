---
title: Get batch transcription results - Speech service
titleSuffix: Foundry Tools
description: With batch transcription, the Speech service transcribes the audio data and stores the results in a storage container. You can then retrieve the results from the storage container.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 12/19/2025
zone_pivot_groups: speech-cli-rest
ms.custom: devx-track-csharp
---

# Get batch transcription results

To get transcription results, first check the [status](#get-transcription-status) of the transcription job. If the job is completed, you can [retrieve](#get-batch-transcription-results) the transcriptions and transcription report. 

## Get transcription status

::: zone pivot="rest-api"

To get the status of the transcription job, call the [Transcriptions - Get](/rest/api/speechtotext/transcriptions/get) operation of the [Speech to text REST API](rest-speech-to-text.md).

> [!IMPORTANT]
> Batch transcription jobs are scheduled on a best-effort basis. At peak hours, it might take up to 30 minutes for a transcription job to start processing and up to 24 hours to complete. Most of the time during the execution the transcription status is `Running`. The reason is because the job has the `Running` status the moment it moves to the batch transcription backend system. When the base model is used, this assignment happens almost immediately; it's slightly slower for custom models. Thus, the amount of time a transcription job spends in the `Running` state doesn't correspond to the actual transcription time but also includes waiting time in the internal queues.

Make an HTTP GET request using the URI as shown in the following example. Replace `YourTranscriptionId` with your transcription ID, replace `YourSpeechResoureKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions/YourTranscriptionId?api-version=2024-11-15" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions/5cff1d03-118f-4c4c-b3ba-e1f1cd88c14d?api-version=2024-11-15",
  "displayName": "My Transcription",
  "locale": "en-US",
  "createdDateTime": "2025-05-24T13:36:57Z",
  "lastActionDateTime": "2025-05-24T13:37:13Z",
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions/5cff1d03-118f-4c4c-b3ba-e1f1cd88c14d/files?api-version=2024-11-15"
  },
  "properties": {
    "wordLevelTimestampsEnabled": true,
    "displayFormWordLevelTimestampsEnabled": false,
    "channels": [
      0,
      1
    ],
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked",
    "timeToLiveHours": 48,
    "languageIdentification": {
      "candidateLocales": [
        "en-US",
        "de-DE",
        "es-ES"
      ],
      "mode": "Continuous"
    },
    "durationMilliseconds": 3000
  },
  "status": "Succeeded"
}
```

The `status` property indicates the current status of the transcriptions. The transcriptions and transcription report are available when the transcription status is `Succeeded`.


::: zone-end

::: zone pivot="speech-cli"

> [!IMPORTANT]
> Batch transcription jobs are scheduled on a best-effort basis. At peak hours, it might take up to 30 minutes or longer for a transcription job to start processing. Most of the time during the execution the transcription status is `Running`. The reason is because the job has the `Running` status the moment it moves to the batch transcription backend system. When the base model is used, this assignment happens almost immediately; it's slightly slower for custom models. Thus, the amount of time a transcription job spends in the `Running` state doesn't correspond to the actual transcription time but also includes waiting time in the internal queues.

To get the status of the transcription job, use the `spx batch transcription status` command. Construct the request parameters according to the following instructions:

- Set the `transcription` parameter to the ID of the transcription that you want to get. 
- Set the required `api-version` parameter to `v3.2`. The Speech CLI doesn't support version `2024-11-15` or later yet, so you must use `v3.2` for now.

Here's an example Speech CLI command to get the transcription status:

```azurecli-interactive
spx batch transcription status --api-version v3.2 --transcription YourTranscriptionId
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/bbbbcccc-1111-dddd-2222-eeee3333ffff",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/637d9333-6559-47a6-b8de-c7d732c1ddf3/files"
  },
  "properties": {
    "diarizationEnabled": false,
    "wordLevelTimestampsEnabled": false,
    "displayFormWordLevelTimestampsEnabled": true,
    "channels": [
      0,
      1
    ],
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked",
    "duration": "PT3S"
  },
  "lastActionDateTime": "2025-05-24T13:37:12Z",
  "status": "Succeeded",
  "createdDateTime": "2024-05-10T18:39:07Z",
  "locale": "en-US",
  "displayName": "My Transcription"
}
```

The `status` property indicates the current status of the transcriptions. The transcriptions and transcription report are available when the transcription status is `Succeeded`.

For Speech CLI help with transcriptions, run the following command:

```azurecli-interactive
spx help batch transcription
```

::: zone-end

## Get transcription results

::: zone pivot="rest-api"

The [Transcriptions - List Files](/rest/api/speechtotext/transcriptions/list-files) operation returns a list of result files for a transcription. A [transcription report](#transcription-report-file) file is provided for each submitted batch transcription job. In addition, one [transcription](#transcription-result-file) file (the end result) is provided for each successfully transcribed audio file.  

Make an HTTP GET request using the "files" URI from the previous response body. Replace `YourTranscriptionId` with your transcription ID, replace `YourSpeechResoureKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

```azurecli-interactive
curl -v -X GET "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions/YourTranscriptionId/files?api-version=2024-11-15" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

You should receive a response body in the following format:

```json
{
  "values": [
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions/5cff1d03-118f-4c4c-b3ba-e1f1cd88c14d/files/ec226a24-d3c7-4ae4-b59e-49d5bdab492e?api-version=2024-11-15",
      "name": "contenturl_0.json",
      "kind": "Transcription",
      "links": {
        "contentUrl": "YourTranscriptionUrl"
      },
      "properties": {
        "size": 1230
      },
      "createdDateTime": "2025-05-24T13:37:12Z"
    },
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions/5cff1d03-118f-4c4c-b3ba-e1f1cd88c14d/files/078cd816-7944-4619-a6a6-bc52fb000f8c?api-version=2024-11-15",
      "name": "contenturl_1.json",
      "kind": "Transcription",
      "links": {
        "contentUrl": "YourTranscriptionUrl"
      },
      "properties": {
        "size": 2413
      },
      "createdDateTime": "2025-05-24T13:37:12Z"
    },
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions/5cff1d03-118f-4c4c-b3ba-e1f1cd88c14d/files/5baff707-8d68-4c69-850e-48775c57c982?api-version=2024-11-15",
      "name": "report.json",
      "kind": "TranscriptionReport",
      "links": {
        "contentUrl": "YourTranscriptionReportUrl"
      },
      "properties": {
        "size": 747
      },
      "createdDateTime": "2025-05-24T13:37:12Z"
    }
  ]
}
```

The location of each transcription and transcription report files with more details are returned in the response body. The `contentUrl` property contains the URL to the [transcription](#transcription-result-file) (`"kind": "Transcription"`) or [transcription report](#transcription-report-file) (`"kind": "TranscriptionReport"`) file.

If you didn't specify a container in the `destinationContainerUrl` property of the transcription request, the results are stored in a container managed by Microsoft. When the transcription job is deleted, the transcription result data is also deleted.

::: zone-end

::: zone pivot="speech-cli"

The `spx batch transcription list` command returns a list of result files for a transcription. A [transcription report](#transcription-report-file) file is provided for each submitted batch transcription job. In addition, one [transcription](#transcription-result-file) file (the end result) is provided for each successfully transcribed audio file. 

- Set the required `files` flag.
- Set the required `transcription` parameter to the ID of the transcription that you want to get logs.
- Set the required `api-version` parameter to `v3.2`. The Speech CLI doesn't support version `2024-11-15` or later yet, so you must use `v3.2` for now.

Here's an example Speech CLI command that gets a list of result files for a transcription:

```azurecli-interactive
spx batch transcription list --api-version v3.2 --files --transcription YourTranscriptionId
```

You should receive a response body in the following format:

```json
{
  "values": [
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/637d9333-6559-47a6-b8de-c7d732c1ddf3/files/aaaabbbb-6666-cccc-7777-dddd8888eeee",
      "name": "contenturl_0.json",
      "kind": "Transcription",
      "properties": {
        "size": 3407
      },
      "createdDateTime": "2025-05-24T13:37:12Z",
      "links": {
        "contentUrl": "YourTranscriptionUrl"
      }
    },
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/637d9333-6559-47a6-b8de-c7d732c1ddf3/files/ffffaaaa-5555-bbbb-6666-cccc7777dddd",
      "name": "contenturl_1.json",
      "kind": "Transcription",
      "properties": {
        "size": 8233
      },
      "createdDateTime": "2025-05-24T13:37:12Z",
      "links": {
        "contentUrl": "YourTranscriptionUrl"
      }
    },
    {
      "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/637d9333-6559-47a6-b8de-c7d732c1ddf3/files/aaaabbbb-6666-cccc-7777-dddd8888eeee",
      "name": "report.json",
      "kind": "TranscriptionReport",
      "properties": {
        "size": 279
      },
      "createdDateTime": "2025-05-24T13:37:12Z",
      "links": {
        "contentUrl": "YourTranscriptionReportUrl"
      }
    }
  ]
}
```

The location of each transcription and transcription report files with more details are returned in the response body. The `contentUrl` property contains the URL to the [transcription](#transcription-result-file) (`"kind": "Transcription"`) or [transcription report](#transcription-report-file) (`"kind": "TranscriptionReport"`) file.

By default, the results are stored in a container managed by Microsoft. When the transcription job is deleted, the transcription result data is also deleted.

::: zone-end

### Transcription report file

One transcription report file is provided for each submitted batch transcription job. The transcription report file is identified by the `"kind": "TranscriptionReport"` property in the response body of the [Transcriptions - List Files](/rest/api/speechtotext/transcriptions/list-files) operation.

The contents of each transcription result file are formatted as JSON, as shown in this example.

```json
{
  "successfulTranscriptionsCount": 2,
  "failedTranscriptionsCount": 0,
  "details": [
    {
      "source": "https://crbn.us/hello.wav",
      "status": "Succeeded"
    },
    {
      "source": "https://crbn.us/whatstheweatherlike.wav",
      "status": "Succeeded"
    }
  ]
}
```

### Transcription result file

One transcription result file is provided for each successfully transcribed audio file. The transcription result file is identified by the `"kind": "Transcription"` property in the response body of the [Transcriptions - List Files](/rest/api/speechtotext/transcriptions/list-files) operation.

The contents of each transcription result file are formatted as JSON, as shown in this example.

```json
{
  "source": "...",
  "timestamp": "2025-05-24T13:37:05Z",
  "durationInTicks": 25800000,
  "durationMilliseconds": 2580,
  "duration": "PT2.58S",
  "combinedRecognizedPhrases": [
    {
      "channel": 0,
      "lexical": "hello world",
      "itn": "hello world",
      "maskedITN": "hello world",
      "display": "Hello world."
    }
  ],
  "recognizedPhrases": [
    {
      "recognitionStatus": "Success",
      "channel": 0,
      "offset": "PT0.76S",
      "duration": "PT1.32S",
      "offsetInTicks": 7600000.0,
      "durationInTicks": 13200000.0,
      "nBest": [
        {
          "confidence": 0.5643338,
          "lexical": "hello world",
          "itn": "hello world",
          "maskedITN": "hello world",
          "display": "Hello world.",
          "displayWords": [
            {
              "displayText": "Hello",
              "offset": "PT0.76S",
              "duration": "PT0.76S",
              "offsetInTicks": 7600000.0,
              "durationInTicks": 7600000.0
            },
            {
              "displayText": "world.",
              "offset": "PT1.52S",
              "duration": "PT0.56S",
              "offsetInTicks": 15200000.0,
              "durationInTicks": 5600000.0
            }
          ]
        },
        {
          "confidence": 0.1769063,
          "lexical": "helloworld",
          "itn": "helloworld",
          "maskedITN": "helloworld",
          "display": "helloworld"
        },
        {
          "confidence": 0.49964225,
          "lexical": "hello worlds",
          "itn": "hello worlds",
          "maskedITN": "hello worlds",
          "display": "hello worlds"
        },
        {
          "confidence": 0.4995761,
          "lexical": "hello worm",
          "itn": "hello worm",
          "maskedITN": "hello worm",
          "display": "hello worm"
        },
        {
          "confidence": 0.49418187,
          "lexical": "hello word",
          "itn": "hello word",
          "maskedITN": "hello word",
          "display": "hello word"
        }
      ]
    }
  ]
}
```

Depending in part on the request parameters set when you created the transcription job, the transcription file can contain the following result properties.

|Property|Description|
|--------|-----------|
|`channel`|The channel number of the results. For stereo audio streams, the left and right channels are split during the transcription. A JSON result file is created for each input audio file.|
|`combinedRecognizedPhrases`|The concatenated results of all phrases for the channel.|
|`confidence`|The confidence value for the recognition.|
|`display`|The display form of the recognized text. Added punctuation and capitalization are included.|
|`displayWords`|The timestamps for each word of the transcription. The `displayFormWordLevelTimestampsEnabled` request property must be set to `true`. Otherwise this property isn't present.|
|`duration`|The audio duration. The value is an ISO 8601 encoded duration.|
|`durationInTicks`|The audio duration in ticks (one tick is 100 nanoseconds).|
|`durationMilliseconds`|The audio duration in milliseconds.|
|`itn`|The inverse text normalized (ITN) form of the recognized text. Abbreviations such as "Doctor Smith" to "Dr Smith," phone numbers, and other transformations are applied.|
|`lexical`|The actual words recognized.|
|`locale`|The locale identified from the input the audio. The `languageIdentification` request property must be set. Otherwise this property isn't present.|
|`maskedITN`|The ITN form with profanity masking applied.|
|`nBest`|A list of possible transcriptions for the current phrase with confidences.|
|`offset`|The offset in audio of this phrase. The value is an ISO 8601 encoded duration.|
|`offsetInTicks`|The offset in audio of this phrase in ticks (one tick is 100 nanoseconds).|
|`recognitionStatus`|The recognition state. For example: "Success" or "Failure."|
|`recognizedPhrases`|The list of results for each phrase.|
|`source`|The URL that was provided as the input audio source. The source corresponds to the `contentUrls` or `contentContainerUrl` request property. The `source` property is the only way to confirm the audio input for a transcription.|
|`speaker`|The identified speaker. The `diarization` and `diarizationEnabled` request properties must be set. Otherwise this property isn't present.|
|`timestamp`|The creation date and time of the transcription. The value is an ISO 8601 encoded timestamp.|
|`words`|A list of results with lexical text for each word of the phrase. The `wordLevelTimestampsEnabled` request property must be set to `true`. Otherwise this property isn't present.|

## Related content

- [Learn more about batch transcription](batch-transcription.md)
- [Locate audio files for batch transcription](batch-transcription-audio-data.md)
- [Create a batch transcription](batch-transcription-create.md)
- [See batch transcription code samples at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/)
