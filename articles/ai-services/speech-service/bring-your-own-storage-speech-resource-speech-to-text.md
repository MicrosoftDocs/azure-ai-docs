---
title: Use Bring your own storage (BYOS) Speech resource for Speech to text
titleSuffix: Azure AI services
description: Learn how to use Bring your own storage (BYOS) Speech resource with Speech to text.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/12/2024
author: eric-urban
ms.author: eur
ms.reviewer: alexeyo
---

# Use the Bring your own storage (BYOS) Speech resource for speech to text

Bring your own storage (BYOS) can be used in the following speech to text scenarios:

- Batch transcription
- Real-time transcription with audio and transcription results logging enabled
- Custom speech

One pair of a Speech resource and storage account can be used for all scenarios simultaneously.

This article explains in depth how to use a BYOS-enabled Speech resource in all speech to text scenarios. The article implies that you have [a fully configured BYOS-enabled Speech resource and associated Storage account](bring-your-own-storage-speech-resource.md).

## Data storage

When using BYOS, the Speech service doesn't keep any customer artifacts after the data processing (transcription, model training, model testing) is complete. However, some metadata that isn't derived from the user content is stored within Speech service premises. For example, in the custom speech scenario, the Service keeps certain information about the custom endpoints, like which models they use.

BYOS-associated Storage account stores the following data:

> [!NOTE]
> *Optional* in this section means that it's possible, but not required to store the particular artifacts in the BYOS-associated Storage account. If needed, they can be stored elsewhere.

**Batch transcription**
- Source audio (optional)
- Batch transcription results

**Real-time transcription with audio and transcription result logging enabled**
- Audio and transcription result logs

**Custom speech**
- Source files of datasets for model training and testing (optional)
- All data and metadata related to Custom models hosted by the BYOS-enabled Speech resource (including copies of datasets for model training and testing)

## Batch transcription

Batch transcription is used to transcribe a large amount of audio data in storage. If you're unfamiliar with Batch transcription, see [this article](batch-transcription.md) first.

Perform these steps to execute Batch transcription with BYOS-enabled Speech resource:

1. Start Batch transcription as described in [this guide](batch-transcription-create.md).

    > [!IMPORTANT]
    > Don't use `destinationContainerUrl` parameter in your transcription request. If you use BYOS, the transcription results are stored in the BYOS-associated Storage account automatically. 
    >
    > If you use `destinationContainerUrl` parameter, it will work, but provide significantly less security for your data, because of ad hoc SAS usage. See details [here](batch-transcription-create.md#specify-a-destination-container-url).

1. When transcription is complete, get transcription results according to [this guide](batch-transcription-get.md). Consider using `sasValidityInSeconds` parameter (see the following section).  

Speech service uses `customspeech-artifacts` Blob container in the BYOS-associated Storage account for storing intermediate and final transcription results.
 
> [!CAUTION]
> Speech service relies on pre-defined Blob container paths and file names for Batch transcription module to correctly function. Don't move, rename or in any way alter the contents of `customspeech-artifacts` container.
>
> Failure to do so very likely will result in hard to debug 4xx and 5xx Service errors.
>
> Also don't build solutions that directly use files and folders of `customspeech-artifacts` container. Use standard tools to interact with Batch transcription. See details in [Batch transcription section](batch-transcription.md).

### Get Batch transcription results via REST API

[Speech to text REST API](rest-speech-to-text.md) fully supports BYOS-enabled Speech resources. However, because the data is now stored within the BYOS-enabled Storage account, requests like [Get Transcription Files](/rest/api/speechtotext/transcriptions/list-files) interact with the BYOS-associated Storage account Blob storage, instead of Speech service internal resources. It allows using the same REST API based code for both "regular" and BYOS-enabled Speech resources.

For maximum security use the `sasValidityInSeconds` parameter with the value set to `0` in the requests, that return data file URLs, like [Get Transcription Files](/rest/api/speechtotext/transcriptions/list-files) request. Here's an example request URL:

```https
https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions/3b24ca19-2eb1-4a2a-b964-35d89eca486b/files?sasValidityInSeconds=0
```

Such a request returns direct Storage Account URLs to data files (without SAS or other additions). For example:

```json
"links": {
        "contentUrl": "https://<BYOS_storage_account_name>.blob.core.windows.net/customspeech-artifacts/TranscriptionData/3b24ca19-2eb1-4a2a-b964-35d89eca486b_0_0.json"
      }
```

URL of this format ensures that only Microsoft Entra identities (users, service principals, managed identities) with sufficient access rights (like *Storage Blob Data Reader* role) can access the data from the URL.

> [!WARNING]
> If `sasValidityInSeconds` parameter is omitted in [Get Transcription Files](/rest/api/speechtotext/transcriptions/list-files) request or similar ones, then a [User delegation SAS](/azure/storage/common/storage-sas-overview) with the validity of 5 days will be generated for each data file URL returned. This SAS is signed by the system assigned managed identity of your BYOS-enabled Speech resource. Because of it, the SAS allows access to the data, even if storage account key access is disabled. See details [here](/azure/storage/common/shared-key-authorization-prevent#understand-how-disallowing-shared-key-affects-sas-tokens). 

## Real-time transcription with audio and transcription result logging enabled

You can enable logging for both audio input and recognized speech when using speech to text or speech translation. See the complete description [in this article](logging-audio-transcription.md).

If you use BYOS, then you find the logs in `customspeech-audiologs` Blob container in the BYOS-associated Storage account.

> [!WARNING]
> Logging data is kept for 5 days. After this period the logs are automatically deleted. This is valid for BYOS-enabled Speech resources as well. If you want to keep the logs longer, copy the correspondent files and folders from `customspeech-audiologs` Blob container directly or use REST API.

### Get real-time transcription logs via REST API

[Speech to text REST API](rest-speech-to-text.md) fully supports BYOS-enabled Speech resources. However, because the data is now stored within the BYOS-enabled Storage account, requests like [Get Base Model Logs](/rest/api/speechtotext/endpoints/list-base-model-logs) interact with the BYOS-associated Storage account Blob storage, instead of Speech service internal resources. It allows using the same REST API based code for both "regular" and BYOS-enabled Speech resources.

For maximum security use the `sasValidityInSeconds` parameter with the value set to `0` in the requests, that return data file URLs, like [Get Base Model Logs](/rest/api/speechtotext/endpoints/list-base-model-logs) request. Here's an example request URL:

```https
https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/endpoints/base/en-US/files/logs?sasValidityInSeconds=0
```

Such a request returns direct Storage Account URLs to data files (without SAS or other additions). For example:

```json
"links": {
        "contentUrl": "https://<BYOS_storage_account_name>.blob.core.windows.net/customspeech-audiologs/be172190e1334399852185c0addee9d6/en-US/2023-07-06/152339_fcf52189-0d3f-4415-becd-5f639fd7fd6b.v2.json"
      }
```

URL of this format ensures that only Microsoft Entra identities (users, service principals, managed identities) with sufficient access rights (like *Storage Blob Data Reader* role) can access the data from the URL.

> [!WARNING]
> If `sasValidityInSeconds` parameter is omitted in [Get Base Model Logs](/rest/api/speechtotext/endpoints/list-base-model-logs) request or similar ones, then a [User delegation SAS](/azure/storage/common/storage-sas-overview) with the validity of 5 days will be generated for each data file URL returned. This SAS is signed by the system assigned managed identity of your BYOS-enabled Speech resource. Because of it, the SAS allows access to the data, even if storage account key access is disabled. See details [here](/azure/storage/common/shared-key-authorization-prevent#understand-how-disallowing-shared-key-affects-sas-tokens). 

## Custom speech

With custom speech, you can evaluate and improve the accuracy of speech recognition for your applications and products. A custom speech model can be used for real-time speech to text, speech translation, and batch transcription. For more information, see the [custom speech overview](custom-speech-overview.md).

There's nothing specific about how you use custom speech with BYOS-enabled Speech resource. The only difference is where all custom model related data, which Speech service collects and produces for you, is stored. The data is stored in the following Blob containers of BYOS-associated Storage account:

- `customspeech-models` - Location of custom speech models
- `customspeech-artifacts` - Location of all other custom speech related data 

The Blob container structure is provided for your information only and subject to change without a notice.

> [!CAUTION]
> Speech service relies on pre-defined Blob container paths and file names for custom speech module to correctly function. Don't move, rename or in any way alter the contents of `customspeech-models` container and custom speech related folders of `customspeech-artifacts` container.
>
> Failure to do so very likely will result in hard to debug errors and may lead to the necessity of custom model retraining.
>
> Also don't build solutions that directly use files and folders of `customspeech-artifacts` container. Use standard tools, like REST API and Speech Studio to interact with the custom speech related data. See details in [custom speech section](custom-speech-overview.md).

### Use of REST API with custom speech

[Speech to text REST API](rest-speech-to-text.md) fully supports BYOS-enabled Speech resources. However, because the data is now stored within the BYOS-enabled Storage account, requests like [Datasets_ListFiles](/rest/api/speechtotext/datasets/list-files) interact with the BYOS-associated Storage account Blob storage, instead of Speech service internal resources. It allows using the same REST API based code for both "regular" and BYOS-enabled Speech resources.

For maximum security use the `sasValidityInSeconds` parameter with the value set to `0` in the requests, that return data file URLs, like [Get Dataset Files](/rest/api/speechtotext/datasets/list-files) request. Here's an example request URL:

```https
https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/datasets/8427b92a-cb50-4cda-bf04-964ea1b1781b/files?sasValidityInSeconds=0
```

Such a request returns direct Storage Account URLs to data files (without SAS or other additions). For example:

```json
 "links": {
        "contentUrl": "https://<BYOS_storage_account_name>.blob.core.windows.net/customspeech-artifacts/AcousticData/8427b92a-cb50-4cda-bf04-964ea1b1781b/4a61ddac-5b1c-4c21-b87d-22001b0f18ab.zip"
      }
```

URL of this format ensures that only Microsoft Entra identities (users, service principals, managed identities) with sufficient access rights (like *Storage Blob Data Reader* role) can access the data from the URL.

> [!WARNING]
> If `sasValidityInSeconds` parameter is omitted in [Get Dataset Files](/rest/api/speechtotext/datasets/list-files) request or similar ones, then a [User delegation SAS](/azure/storage/common/storage-sas-overview) with the validity of 5 days will be generated for each data file URL returned. This SAS is signed by the system assigned managed identity of your BYOS-enabled Speech resource. Because of it, the SAS allows access to the data, even if storage account key access is disabled. See details [here](/azure/storage/common/shared-key-authorization-prevent#understand-how-disallowing-shared-key-affects-sas-tokens). 

## Next steps

- [Set up the Bring your own storage (BYOS) Speech resource](bring-your-own-storage-speech-resource.md)
- [Batch transcription overview](batch-transcription.md)
- [How to log audio and transcriptions for speech recognition](logging-audio-transcription.md)
- [Custom speech overview](custom-speech-overview.md)
