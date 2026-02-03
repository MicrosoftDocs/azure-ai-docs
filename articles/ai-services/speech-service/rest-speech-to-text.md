---
title: Speech to text REST API - Speech service
titleSuffix: Foundry Tools
description: Get reference documentation for Speech to text REST API.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 11/21/2025
author: PatrickFarley
ms.author: pafarley
# Customer intent: As a developer, I want to learn about the Speech to text REST API.
---

# Speech to text REST API

The speech to text REST API is used for [fast transcription](fast-transcription-create.md), [batch transcription](batch-transcription.md) and [custom speech](custom-speech-overview.md). 

> [!IMPORTANT]
> Speech to text REST API version `2025-10-15` is the latest version that's generally available. 
> - [Speech to text REST API](rest-speech-to-text.md) version `2024-05-15-preview` will be retired on a date to be announced. 
> - Speech to text REST API `v3.0`, `3.2-preview.1`, and `3.2-preview.2` will be retired on March 31st, 2026. 
> 
> For more information about upgrading, see the Speech to text REST API [v3.0 to v3.1](migrate-v3-0-to-v3-1.md), [v3.1 to v3.2](migrate-v3-1-to-v3-2.md), [v3.2 to 2024-11-15](migrate-2024-11-15.md) and [2024-11-15 to 2025-10-15](migrate-2025-10-15.md) migration guides.

> [!div class="nextstepaction"]
> [See the Speech to text REST API 2025-10-15 reference documentation](/rest/api/speechtotext/operation-groups?view=rest-speechtotext-2025-10-15&preserve-view=true)

Use Speech to text REST API to do the following:

- [Fast transcription](fast-transcription-create.md): Transcribe audio files with returning results synchronously and much faster than real-time audio. Use the fast transcription API ([/speechtotext/transcriptions:transcribe](/rest/api/speechtotext/transcriptions/transcribe)) in the scenarios that you need the transcript of an audio recording as quickly as possible with predictable latency, such as quick audio or video transcription or video translation.
- [Batch transcription](batch-transcription.md): Transcribe audio files as a batch from multiple URLs or an Azure container. Use the batch transcription API ([/speechtotext/transcriptions:submit](/rest/api/speechtotext/transcriptions/submit)) in the scenarios that you need to transcribe a large amount of audio in storage, such as a large number of files or a long audio file. 
- [Custom speech](custom-speech-overview.md): Upload your own data, test and train a custom model, compare accuracy between models, and deploy a model to a custom endpoint. Copy models to other subscriptions if you want colleagues to have access to a model that you built, or if you want to deploy a model to more than one region.

Speech to text REST API includes such features as:
- Request logs for each endpoint.
- Request the manifest of the models that you create, to set up on-premises containers.
- Upload data from Azure storage accounts by using a shared access signature (SAS) URI.
- Bring your own storage. Use your own storage accounts for logs, transcription files, and other data.
- Some operations support webhook notifications. You can register your webhooks where notifications are sent.

## Fast transcription

The following operation groups are applicable for [fast transcription](fast-transcription-create.md).

| Operation group | Description |
|---------|---------|
| [Transcriptions](/rest/api/speechtotext/transcriptions) | Use [Transcriptions - Transcribe](/rest/api/speechtotext/transcriptions/transcribe) to transcribe audio files.<br/><br/>When you use [fast transcription](fast-transcription-create.md) you send a single file per request. See [Create a transcription](fast-transcription-create.md?pivots=rest-api) for examples of how to create a transcription from a single audio file. |

## Batch transcription

The following operation groups are applicable for [batch transcription](batch-transcription.md).

| Operation group | Description |
|---------|---------|
| [Models](/rest/api/speechtotext/models) | Use base models or custom models to transcribe audio files.<br/><br/>You can use models with [custom speech](custom-speech-overview.md) and [batch transcription](batch-transcription.md). For example, you can use a model trained with a specific dataset to transcribe audio files. See [Train a model](how-to-custom-speech-train-model.md?pivots=rest-api) and [custom speech model lifecycle](how-to-custom-speech-model-and-endpoint-lifecycle.md?pivots=rest-api) for examples of how to train and manage custom speech models. |
| [Transcriptions](/rest/api/speechtotext/transcriptions) | Use [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit) to transcribe a large amount of audio in storage.<br/><br/>When you use [batch transcription](batch-transcription.md) you send multiple files per request or point to an Azure Blob Storage container with the audio files to transcribe. See [Create a transcription](batch-transcription-create.md?pivots=rest-api) for examples of how to create a transcription from multiple audio files. |
| [Web hooks](/rest/api/speechtotext/web-hooks) | Use web hooks to receive notifications about creation, processing, completion, and deletion events.<br/><br/>You can use web hooks with [custom speech](custom-speech-overview.md) and [batch transcription](batch-transcription.md). Web hooks apply to [datasets](/rest/api/speechtotext/datasets), [endpoints](/rest/api/speechtotext/endpoints), [evaluations](/rest/api/speechtotext/evaluations), [models](/rest/api/speechtotext/models), and [transcriptions](/rest/api/speechtotext/transcriptions). |

## Custom speech

The following operation groups are applicable for [custom speech](custom-speech-overview.md). 

| Operation group | Description |
|---------|---------|
| [Datasets](/rest/api/speechtotext/datasets) | Use datasets to train and test custom speech models.<br/><br/>For example, you can compare the performance of a [custom speech](custom-speech-overview.md) trained with a specific dataset to the performance of a base model or custom speech model trained with a different dataset. See [Upload training and testing datasets](how-to-custom-speech-upload-data.md?pivots=rest-api) for examples of how to upload datasets. |
| [Endpoints](/rest/api/speechtotext/endpoints) | Deploy custom speech models to endpoints.<br/><br/>You must deploy a custom endpoint to use a [custom speech](custom-speech-overview.md) model. See [Deploy a model](how-to-custom-speech-deploy-model.md?pivots=rest-api) for examples of how to manage deployment endpoints.  |
| [Evaluations](/rest/api/speechtotext/evaluations) | Use evaluations to compare the performance of different models.<br/><br/>For example, you can compare the performance of a [custom speech](custom-speech-overview.md) model trained with a specific dataset to the performance of a base model or a custom model trained with a different dataset. See [test recognition quality](how-to-custom-speech-inspect-data.md?pivots=rest-api) and [test accuracy](how-to-custom-speech-evaluate-data.md?pivots=rest-api) for examples of how to test and evaluate custom speech models. |
| [Models](/rest/api/speechtotext/models) | Use base models or custom models to transcribe audio files.<br/><br/>You can use models with [custom speech](custom-speech-overview.md) and [batch transcription](batch-transcription.md). For example, you can use a model trained with a specific dataset to transcribe audio files. See [Train a model](how-to-custom-speech-train-model.md?pivots=rest-api) and [custom speech model lifecycle](how-to-custom-speech-model-and-endpoint-lifecycle.md?pivots=rest-api) for examples of how to train and manage custom speech models. |
| [Projects](/rest/api/speechtotext/projects) | Use projects to manage custom speech models, training and testing datasets, and deployment endpoints.<br/><br/>[Custom speech projects](custom-speech-overview.md) contain models, training and testing datasets, and deployment endpoints. Each project is specific to a [locale](language-support.md?tabs=stt). For example, you might create a project for English in the United States. See [Create a project](how-to-custom-speech-create-project.md?pivots=rest-api) for examples of how to create projects.|
| [Web hooks](/rest/api/speechtotext/web-hooks) | Use web hooks to receive notifications about creation, processing, completion, and deletion events.<br/><br/>You can use web hooks with [custom speech](custom-speech-overview.md) and [batch transcription](batch-transcription.md). Web hooks apply to [datasets](/rest/api/speechtotext/datasets), [endpoints](/rest/api/speechtotext/endpoints), [evaluations](/rest/api/speechtotext/evaluations), [models](/rest/api/speechtotext/models), and [transcriptions](/rest/api/speechtotext/transcriptions). |

## Related content

- [Create a custom speech project](how-to-custom-speech-create-project.md)
- [Get familiar with batch transcription](batch-transcription.md)

