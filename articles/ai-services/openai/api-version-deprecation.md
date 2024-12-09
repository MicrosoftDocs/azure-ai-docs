---
title: Azure OpenAI Service API version lifecycle
description: Learn more about API version retirement in Azure OpenAI Services.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 11/01/2024
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
ms.custom:
---

# Azure OpenAI API preview lifecycle

This article is to help you understand the support lifecycle for the Azure OpenAI API previews. New preview APIs target a monthly release cadence. Whenever possible we recommend using either the latest GA, or preview API releases.

> [!NOTE]
> The `2023-06-01-preview` API and the `2023-10-01-preview` API remain supported at this time.

## Latest preview API releases

Azure OpenAI API latest release:

- Inference: [2024-10-01-preview](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-10-01-preview/inference.json)
- Authoring: [2024-10-01-preview](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/authoring/preview/2024-10-01-preview/azureopenai.json)

This version contains support for the latest Azure OpenAI features including:

- Assistants V2 [**Added in 2024-05-01-preview**]
- Embeddings `encoding_format` and `dimensions` parameters [**Added in 2024-03-01-preview**]
- [Assistants API](./assistants-reference.md). [**Added in 2024-02-15-preview**]
- [Text to speech](./text-to-speech-quickstart.md). [**Added in 2024-02-15-preview**]
- [DALL-E 3](./dall-e-quickstart.md). [**Added in 2023-12-01-preview**]
- [Fine-tuning](./how-to/fine-tuning.md) `gpt-35-turbo`, `babbage-002`, and `davinci-002` models.[**Added in 2023-10-01-preview**]
- [Whisper](./whisper-quickstart.md). [**Added in 2023-09-01-preview**]
- [Function calling](./how-to/function-calling.md)  [**Added in 2023-07-01-preview**]
- [Retrieval augmented generation with your data feature](./use-your-data-quickstart.md).  [**Added in 2023-06-01-preview**]

## Changes between 2024-09-01-preview and 2024-08-01-preview

- `max_completion_tokens` added to support `o1-preview` and `o1-mini` models. `max_tokens` does not work with the **o1 series** models.
- `parallel_tool_calls` added.
- `completion_tokens_details` & `reasoning_tokens` added.
- `stream_options` & `include_usage` added.

## Changes between 2024-07-01-preview and 2024-08-01-preview API specification

- [Structured outputs support](./how-to/structured-outputs.md).
- Large file upload API added.
- On your data changes:
    * [Mongo DB integration](./reference-preview.md#example-7).
    * `role_information` parameter removed.
    *  [`rerank_score`](https://github.com/Azure/azure-rest-api-specs/blob/2b700e5e84d4a95880d373e6a4bce5d16882e4b5/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-08-01-preview/inference.json#L5532) added to citation object.
    * AML datasource removed.
    * AI Search vectorization integration improvements.

## Changes between 2024-5-01-preview and 2024-07-01-preview API specification

- [Batch API support added](./how-to/batch.md)
- [Vector store chunking strategy parameters](/azure/ai-services/openai/reference-preview?#request-body-17)
- `max_num_results` that the file search tool should output.

## Changes between 2024-04-01-preview and 2024-05-01-preview API specification

- Assistants v2 support - [File search tool and vector storage](https://go.microsoft.com/fwlink/?linkid=2272425)
- Fine-tuning [checkpoints](https://github.com/Azure/azure-rest-api-specs/blob/9583ed6c26ce1f10bbea92346e28a46394a784b4/specification/cognitiveservices/data-plane/AzureOpenAI/authoring/preview/2024-05-01-preview/azureopenai.json#L586), [seed](https://github.com/Azure/azure-rest-api-specs/blob/9583ed6c26ce1f10bbea92346e28a46394a784b4/specification/cognitiveservices/data-plane/AzureOpenAI/authoring/preview/2024-05-01-preview/azureopenai.json#L1574), [events](https://github.com/Azure/azure-rest-api-specs/blob/9583ed6c26ce1f10bbea92346e28a46394a784b4/specification/cognitiveservices/data-plane/AzureOpenAI/authoring/preview/2024-05-01-preview/azureopenai.json#L529)
- On your data updates
- DALL-E 2 now supports model deployment and can be used with the latest preview API.
- Content filtering updates

## Changes between 2024-03-01-preview and 2024-04-01-preview API specification

- **Breaking Change**: Enhancements parameters removed. This impacts the `gpt-4` **Version:** `vision-preview` model.
- [timestamp_granularities](https://github.com/Azure/azure-rest-api-specs/blob/fbc90d63f236986f7eddfffe3dca6d9d734da0b2/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-04-01-preview/inference.json#L5217) parameter added.
- [`audioWord`](https://github.com/Azure/azure-rest-api-specs/blob/fbc90d63f236986f7eddfffe3dca6d9d734da0b2/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-04-01-preview/inference.json#L5286) object added.
- Additional TTS [`response_formats`: wav & pcm](https://github.com/Azure/azure-rest-api-specs/blob/fbc90d63f236986f7eddfffe3dca6d9d734da0b2/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-04-01-preview/inference.json#L5333).

## Latest GA API release

Azure OpenAI API version [2024-10-21](./reference.md) is currently the latest GA API release. This API version is the replacement for the previous `2024-06-01` GA API release.

## Updating API versions

We recommend first testing the upgrade to new API versions to confirm there's no impact to your application from the API update before making the change globally across your environment.

If you're using the OpenAI Python or JavaScript client libraries, or the REST API, you'll need to update your code directly to the latest preview API version.

If you're using one of the Azure OpenAI SDKs for C#, Go, or Java, you'll instead need to update to the latest version of the SDK. Each SDK release is hardcoded to work with specific versions of the Azure OpenAI API.

## Next steps

- [Learn more about Azure OpenAI](overview.md)
- [Learn about working with Azure OpenAI models](./how-to/working-with-models.md)
