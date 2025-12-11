---
title: Create a batch transcription - Speech service
titleSuffix: Foundry Tools
description: Learn how to use Azure Speech in Foundry Tools for batch transcriptions, where you submit audio and then retrieve transcription results asynchronously.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 10/31/2025
zone_pivot_groups: speech-cli-rest
ms.custom: devx-track-csharp
# Customer intent: As a user who implements audio transcription, I want create transcriptions in bulk so that I don't have to submit audio content repeatedly.
---

# Create a batch transcription

With batch transcriptions, you submit [audio data](batch-transcription-audio-data.md) in a batch. The service transcribes the audio data and stores the results in a storage container. You can then [retrieve the results](batch-transcription-get.md) from the storage container.

Batch transcription completion can take several minutes to hours, depending on the size of the audio data and the number of files submitted. Even the same size of audio data can take different amounts of time to transcribe, depending on service load and other factors. The service doesn't provide a way to estimate the time it takes to transcribe a batch of audio data.

> [!TIP]
> If you need consistent fast speed for audio files less than 2 hours long and less than 300 MB in size, consider using the [fast transcription API](./fast-transcription-create.md) instead. 

## Prerequisites

You need a [Microsoft Foundry resource for Speech](../multi-service-resource.md). 

## Create a transcription job

::: zone pivot="rest-api"

To create a batch transcription job, use the [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit) operation of the [speech to text REST API](rest-speech-to-text.md#batch-transcription). Construct the request body according to the following instructions:

- You must set either the `contentContainerUrl` or `contentUrls` property. For more information about Azure blob storage for batch transcription, see [Locate audio files for batch transcription](batch-transcription-audio-data.md).
- Set the required `locale` property. This value should match the expected locale of the audio data to transcribe. You can't change the locale later.
- Set the required `displayName` property. Choose a transcription name that you can refer to later. The transcription name doesn't have to be unique and can be changed later.
- Set the required `timeToLiveHours` property. This property specifies how long the transcription should be kept in the system after it completed. The shortest supported duration is 6 hours, the longest supported duration is 31 days. The recommended value is 48 hours (two days) when data is consumed directly.
- Optionally, to use a model other than the base model, set the `model` property to the model ID. For more information, see [Use a custom model](#use-a-custom-model) and [Use a Whisper model](#use-a-whisper-model).
- Optionally, set the `wordLevelTimestampsEnabled` property to `true` to enable word-level timestamps in the transcription results. The default value is `false`. For Whisper models, set the `displayFormWordLevelTimestampsEnabled` property instead. Whisper is a display-only model, so the lexical field isn't populated in the transcription.
- Optionally, set the `languageIdentification` property. Language identification is used to identify languages spoken in audio when compared against a list of [supported languages](language-support.md?tabs=language-identification). If you set the `languageIdentification` property, then you must also set `languageIdentification.candidateLocales` with candidate locales.

For more information, see [Request configuration options](#request-configuration-options).

Make an HTTP POST request that uses the URI as shown in the following [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit) example.

- Replace `YourSpeechResoureKey` with your Microsoft Foundry resource key.
- Replace `YourServiceRegion` with your Microsoft Foundry resource region.
- Set the request body properties as previously described.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "contentUrls": [
    "https://crbn.us/hello.wav",
    "https://crbn.us/whatstheweatherlike.wav"
  ],
  "locale": "en-US",
  "displayName": "My Transcription",
  "model": null,
  "properties": {
    "wordLevelTimestampsEnabled": true,
    "languageIdentification": {
      "candidateLocales": [
        "en-US", "de-DE", "es-ES"
      ],
      "mode": "Continuous"
    },
    "timeToLiveHours": 48
  }
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:submit?api-version=2024-11-15"
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions/788a1f24-f980-4809-8978-e5cf41f77b35?api-version=2024-11-15",
  "displayName": "My Transcription 2",
  "locale": "en-US",
  "createdDateTime": "2025-05-24T03:20:39Z",
  "lastActionDateTime": "2025-05-24T03:20:39Z",
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions/788a1f24-f980-4809-8978-e5cf41f77b35/files?api-version=2024-11-15"
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
    }
  },
  "status": "NotStarted"
}
```

The top-level `self` property in the response body is the transcription's URI. Use this URI to [get](/rest/api/speechtotext/transcriptions/get) details such as the URI of the transcriptions and transcription report files. You also use this URI to [update](/rest/api/speechtotext/transcriptions/update) or [delete](/rest/api/speechtotext/transcriptions/delete) a transcription.

You can query the status of your transcriptions with the [Transcriptions - Get](/rest/api/speechtotext/transcriptions/get) operation. 

Call [Transcriptions - Delete](/rest/api/speechtotext/transcriptions/delete)
regularly from the service, after you retrieve the results. Alternatively, set the `timeToLive` property to ensure the eventual deletion of the results.

> [!TIP]
> You can also try the Batch Transcription API using Python, C#, or Node.js on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch).


::: zone-end

::: zone pivot="speech-cli"

To create a transcription, use the `spx batch transcription create` command. Construct the request parameters according to the following instructions:

- Set the required `content` parameter. You can specify a comma delimited list of individual files or the URL for an entire container. For more information about Azure blob storage for batch transcription, see [Locate audio files for batch transcription](batch-transcription-audio-data.md).
- Set the required `language` property. This value should match the expected locale of the audio data to transcribe. You can't change the locale later. The Speech CLI `language` parameter corresponds to the `locale` property in the JSON request and response.
- Set the required `name` property. Choose a transcription name that you can refer to later. The transcription name doesn't have to be unique and can be changed later. The Speech CLI `name` parameter corresponds to the `displayName` property in the JSON request and response.
- Set the required `api-version` parameter to `v3.2`. The Speech CLI doesn't support version `2024-11-15` or later yet, so you must use `v3.2` for now.

Here's an example Speech CLI command that creates a transcription job:

```azurecli
spx batch transcription create --api-version v3.2 --name "My Transcription" --language "en-US" --content https://crbn.us/hello.wav,https://crbn.us/whatstheweatherlike.wav
```

You should receive a response body in the following format:

```json
{
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/bbbbcccc-1111-dddd-2222-eeee3333ffff",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "links": {
    "files": "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/transcriptions/7f4232d5-9873-47a7-a6f7-4a3f00d00dc0/files"
  },
  "properties": {
    "diarizationEnabled": false,
    "wordLevelTimestampsEnabled": false,
    "channels": [
      0,
      1
    ],
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked"
  },
  "lastActionDateTime": "2025-05-24T03:20:39Z",
  "status": "NotStarted",
  "createdDateTime": "2025-05-24T03:20:39Z",
  "locale": "en-US",
  "displayName": "My Transcription",
  "description": ""
}
```

The top-level `self` property in the response body is the transcription's URI. Use this URI to get details such as the URI of the transcriptions and transcription report files. You also use this URI to update or delete a transcription.

For Speech CLI help with transcriptions, run the following command:

```azurecli
spx help batch transcription
```

::: zone-end

## Request configuration options

::: zone pivot="rest-api"

Here are some property options to configure a transcription when you call the [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit) operation. You can find more examples on the same page, such as [creating a transcription with language identification](/rest/api/speechtotext/transcriptions/submit/#create-a-transcription-with-language-identification).

| Property | Description |
|----------|-------------|
|`channels`|An array of channel numbers to process. Channels `0` and `1` are transcribed by default. |
|`contentContainerUrl`| You can submit individual audio files or a whole storage container.<br/><br/>You must specify the audio data location by using either the `contentContainerUrl` or `contentUrls` property. For more information about Azure blob storage for batch transcription, see [Locate audio files for batch transcription](batch-transcription-audio-data.md).<br/><br/>This property isn't returned in the response.|
|`contentUrls`| You can submit individual audio files or a whole storage container.<br/><br/>You must specify the audio data location by using either the `contentContainerUrl` or `contentUrls` property. For more information, see [Locate audio files for batch transcription](batch-transcription-audio-data.md).<br/><br/>This property isn't returned in the response.|
|`destinationContainerUrl`|The result can be stored in an Azure container. If you don't specify a container, the Speech service stores the results in a container managed by Microsoft. When the transcription job is deleted, the transcription result data is also deleted. For more information, such as the supported security scenarios, see [Specify a destination container URL](#specify-a-destination-container-url).|
|`diarization`|Indicates that the Speech service should attempt diarization analysis on the input, which is expected to be a mono channel that contains multiple voices. The feature isn't available with stereo recordings.<br/><br/>Diarization is the process of separating speakers in audio data. The batch pipeline can recognize and separate multiple speakers on mono channel recordings.<br/><br/>Specify the minimum and maximum number of people who might be speaking. You must also set the `diarizationEnabled` property to `true`. The [transcription file](batch-transcription-get.md#transcription-result-file) contains a `speaker` entry for each transcribed phrase.<br/><br/>You need to use this property when you expect three or more speakers. For two speakers, setting `diarizationEnabled` property to `true` is enough. For an example of the property usage, see [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit).<br/><br/>The maximum number of speakers for diarization must be less than 36 and more or equal to the `minCount` property. For an example, see [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit).<br/><br/>When this property is selected, source audio length can't exceed 240 minutes per file.<br/><br/>**Note**: This property is only available with Speech to text REST API version 3.1 and later. If you set this property with any previous version, such as version 3.0, it's ignored and only two speakers are identified.|
|`diarizationEnabled`|Specifies that the Speech service should attempt diarization analysis on the input, which is expected to be a mono channel that contains two voices. The default value is `false`.<br/><br/>For three or more voices you also need to use property `diarization`. Use only with Speech to text REST API version 3.1 and later.<br/><br/>When this property is selected, source audio length can't exceed 240 minutes per file.|
|`displayName`|The name of the batch transcription. Choose a name that you can refer to later. The display name doesn't have to be unique.<br/><br/>This property is required.|
|`displayFormWordLevelTimestampsEnabled`|Specifies whether to include word-level timestamps on the display form of the transcription results. The results are returned in the `displayWords` property of the transcription file. The default value is `false`.<br/><br/>**Note**: This property is only available with Speech to text REST API version 3.1 and later.|
|`languageIdentification`|Language identification is used to identify languages spoken in audio when compared against a list of [supported languages](language-support.md?tabs=language-identification).<br/><br/>If you set the `languageIdentification` property, then you must also set its enclosed `candidateLocales` property.|
|`languageIdentification.candidateLocales`|The candidate locales for language identification, such as `"properties": { "languageIdentification": { "candidateLocales": ["en-US", "de-DE", "es-ES"]}}`. A minimum of two and a maximum of ten candidate locales, including the main locale for the transcription, is supported.|
|`locale`|The locale of the batch transcription. This value should match the expected locale of the audio data to transcribe. The locale can't be changed later.<br/><br/>This property is required.|
|`model`|You can set the `model` property to use a specific base model or [custom speech](how-to-custom-speech-train-model.md) model. If you don't specify the `model`, the default base model for the locale is used. For more information, see [Use a custom model](#use-a-custom-model) and [Use a Whisper model](#use-a-whisper-model).|
|`profanityFilterMode`|Specifies how to handle profanity in recognition results. Accepted values are `None` to disable profanity filtering, `Masked` to replace profanity with asterisks, `Removed` to remove all profanity from the result, or `Tags` to add profanity tags. The default value is `Masked`. |
|`punctuationMode`|Specifies how to handle punctuation in recognition results. Accepted values are `None` to disable punctuation, `Dictated` to imply explicit (spoken) punctuation, `Automatic` to let the decoder deal with punctuation, or `DictatedAndAutomatic` to use dictated and automatic punctuation. The default value is  `DictatedAndAutomatic`.<br/><br/>This property isn't applicable for Whisper models.|
|`timeToLiveHours`|This required property specifies how long the transcription should be kept in the system after it completed.<br/><br/>Once the transcription reaches the time to live after completion (successful or failed) it's automatically deleted.<br/><br/>The shortest supported duration is 6 hours, the longest supported duration is 31 days. The recommended value is 48 hours (two days) when data is consumed directly.<br/><br/>As an alternative, you can call [Transcriptions - Delete](/rest/api/speechtotext/transcriptions/delete) regularly after you retrieve the transcription results.|
|`wordLevelTimestampsEnabled`|Specifies if word level timestamps should be included in the output. The default value is `false`.<br/><br/>This property isn't applicable for Whisper models. Whisper is a display-only model, so the lexical field isn't populated in the transcription.|


::: zone-end

::: zone pivot="speech-cli"

For Speech CLI help with transcription configuration options, run the following command:

```azurecli
spx help batch transcription create advanced
```

::: zone-end

## Use a custom model

Batch transcription uses the default base model for the locale that you specify. You don't need to set any properties to use the default base model.

Optionally, you can modify the previous [create transcription example](#create-a-transcription-job) by setting the `model` property to use a specific base model or [custom speech](how-to-custom-speech-train-model.md) model.

::: zone pivot="rest-api"

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "contentUrls": [
    "https://crbn.us/hello.wav",
    "https://crbn.us/whatstheweatherlike.wav"
  ],
  "locale": "en-US",
  "displayName": "My Transcription",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/models/base/ccccdddd-2222-eeee-3333-ffff4444aaaa"
  },
  "properties": {
    "wordLevelTimestampsEnabled": true,
  }
}'  "https://YourServiceRegion.api.cognitive.microsoft.com/speechtotext/transcriptions:submit?api-version=2024-11-15"
```

::: zone-end

::: zone pivot="speech-cli"

```azurecli
spx batch transcription create --name "My Transcription" --language "en-US" --content https://crbn.us/hello.wav,https://crbn.us/whatstheweatherlike.wav --model "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.2/models/base/ccccdddd-2222-eeee-3333-ffff4444aaaa"
```

::: zone-end

To use a custom speech model for batch transcription, you need the model's URI. The top-level `self` property in the response body is the model's URI. You can retrieve the model location when you create or get a model. For more information, see the JSON response example in [Create a model](how-to-custom-speech-train-model.md?pivots=rest-api#create-a-model).

> [!TIP]
> A [hosted deployment endpoint](how-to-custom-speech-deploy-model.md) isn't required to use custom speech with the batch transcription service. You can conserve resources if you use the [custom speech model](how-to-custom-speech-train-model.md) only for batch transcription.

Batch transcription requests for expired models fail with a 4xx error. Set the `model` property to a base model or custom model that isn't expired. Otherwise don't include the `model` property to always use the latest base model. For more information, see [Choose a model](./custom-speech-overview.md#choose-your-model) and [Custom speech model lifecycle](how-to-custom-speech-model-and-endpoint-lifecycle.md).

## Use a Whisper model

Azure Speech in Foundry Tools supports OpenAI's Whisper model by using the batch transcription API. You can use the Whisper model for batch transcription.

> [!NOTE]
> Azure OpenAI in Microsoft Foundry Models also supports OpenAI's Whisper model for speech to text with a synchronous REST API. To learn more, see [Speech to text with the Azure OpenAI Whisper model](../../ai-foundry/openai/whisper-quickstart.md). For more information about when to use Azure Speech vs. Azure OpenAI in Microsoft Foundry Models, see [What is the Whisper model?](./whisper-overview.md)

To use a Whisper model for batch transcription, you need to set the `model` property. Whisper is a display-only model, so the lexical field isn't populated in the response.

> [!IMPORTANT]
> Batch transcription using Whisper models is available in a subset of regions that support batch transcription. For the current list of supported regions, see the [Speech service regions table](./regions.md?tabs=stt). Note that Whisper model support may be limited to specific regions within those that support batch transcription.

::: zone pivot="rest-api"
You can make a [Models - List Base Models](/rest/api/speechtotext/models/list-base-models) request to get available base models for all locales.

Make an HTTP GET request as shown in the following example for the `eastus` region. Replace `YourSpeechResoureKey` with your Microsoft Foundry resource key. Replace `eastus` if you're using a different region.

```azurecli-interactive
curl -v -X GET "https://eastus.api.cognitive.microsoft.com/speechtotext/models/base?api-version=2024-11-15" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

By default, only the 100 oldest base models are returned. Use the `skip` and `top` query parameters to page through the results. For example, the following request returns the next 100 base models after the first 100.

```azurecli-interactive
curl -v -X GET "https://eastus.api.cognitive.microsoft.com/speechtotext/models/base?api-version=2024-11-15&skip=100&top=100" -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey"
```

::: zone-end

::: zone pivot="speech-cli"
Make sure that you set the [configuration variables](spx-basics.md#create-a-resource-configuration) for a Foundry resource for Speech in one of the supported regions. You can run the `spx csr list --base` command to get available base models for all locales.

Set the required `api-version` parameter to `v3.2`. The Speech CLI doesn't support version `2024-11-15` or later yet, so you must use `v3.2` for now.

```azurecli
spx csr list --base --api-version v3.2
```

::: zone-end

The `displayName` property of a Whisper model contains "Whisper" as shown in this example. Whisper is a display-only model, so the lexical field isn't populated in the transcription.

```json
{
  "links": {
    "manifest": "https://eastus.api.cognitive.microsoft.com/speechtotext/models/base/69adf293-9664-4040-932b-02ed16332e00/manifest?api-version=2024-11-15"
  },
  "properties": {
    "deprecationDates": {
      "adaptationDateTime": "2025-04-15T00:00:00Z",
      "transcriptionDateTime": "2026-04-15T00:00:00Z"
    },
    "features": {
      "supportsAdaptationsWith": [
        "Acoustic"
      ],
      "supportsTranscriptionsSubmit": true,
      "supportsTranscriptionsTranscribe": false,
      "supportsEndpoints": false,
      "supportsTranscriptionsOnSpeechContainers": false,
      "supportedOutputFormats": [
        "Display"
      ]
    },
    "chargeForAdaptation": true
  },
  "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/models/base/69adf293-9664-4040-932b-02ed16332e00?api-version=2024-11-15",
  "displayName": "20240228 Whisper Large V2",
  "description": "OpenAI Whisper Model in Azure Speech (Whisper v2-large)",
  "locale": "en-US",
  "createdDateTime": "2024-02-29T15:46:31Z",
  "lastActionDateTime": "2024-02-29T15:51:53Z",
  "status": "Succeeded"
},
```

::: zone pivot="rest-api"

You set the full model URI as shown in this example for the `eastus` region. Replace `YourSpeechResoureKey` with your Microsoft Foundry resource key. Replace `eastus` if you're using a different region.

```azurecli-interactive
curl -v -X POST -H "Ocp-Apim-Subscription-Key: YourSpeechResoureKey" -H "Content-Type: application/json" -d '{
  "contentUrls": [
    "https://crbn.us/hello.wav",
    "https://crbn.us/whatstheweatherlike.wav"
  ],
  "locale": "en-US",
  "displayName": "My Transcription",
  "model": {
    "self": "https://eastus.api.cognitive.microsoft.com/speechtotext/models/base/69adf293-9664-4040-932b-02ed16332e00?api-version=2024-11-15"
  },
  "properties": {
    "wordLevelTimestampsEnabled": true,
  },
}'  "https://eastus.api.cognitive.microsoft.com/speechtotext/transcriptions:submit?api-version=2024-11-15"
```

::: zone-end

::: zone pivot="speech-cli"

You set the full model URI as shown in this example for the `eastus` region. Replace `eastus` if you're using a different region.

Set the required `api-version` parameter to `v3.2`. The Speech CLI doesn't support version `2024-11-15` or later yet, so you must use `v3.2` for now.

```azurecli
spx batch transcription create --name "My Transcription" --language "en-US" --content https://crbn.us/hello.wav,https://crbn.us/whatstheweatherlike.wav --model "https://eastus.api.cognitive.microsoft.com/speechtotext/models/base/ddddeeee-3333-ffff-4444-aaaa5555bbbb" --api-version v3.2
```

::: zone-end

## Specify a destination container URL

The transcription result can be stored in an Azure container. If you don't specify a container, the Speech service stores the results in a container managed by Microsoft. In that case, when the transcription job is deleted, the transcription result data is also deleted.

You can store the results of a batch transcription to a writable Azure Blob storage container using option `destinationContainerUrl` in the [batch transcription creation request](#create-a-transcription-job). This option uses only an [ad hoc SAS](batch-transcription-audio-data.md#sas-url-for-batch-transcription) URI and doesn't support [Trusted Azure services security mechanism](batch-transcription-audio-data.md#trusted-azure-services-security-mechanism). This option also doesn't support Access policy based SAS. **The Storage account resource of the destination container must allow all external traffic.**

If you want to store the transcription results in an Azure Blob storage container by using the [Trusted Azure services security mechanism](batch-transcription-audio-data.md#trusted-azure-services-security-mechanism), consider using [Bring-your-own-storage (BYOS)](bring-your-own-storage-speech-resource.md). For more information, see [Use the Bring your own storage (BYOS) Microsoft Foundry resource for speech to text](bring-your-own-storage-speech-resource-speech-to-text.md).

## Related content

- [Learn more about batch transcription](batch-transcription.md)
- [Locate audio files for batch transcription](batch-transcription-audio-data.md)
- [Get batch transcription results](batch-transcription-get.md)
- [See batch transcription code samples at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/)
