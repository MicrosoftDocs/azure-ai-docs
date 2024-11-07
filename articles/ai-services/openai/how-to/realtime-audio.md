---
title: 'How to use the GPT-4o Realtime API for speech and audio with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to use the GPT-4o Realtime API for speech and audio with Azure OpenAI Service.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 11/12/2024
author: eric-urban
ms.author: eur
ms.custom: references_regions
zone_pivot_groups: openai-studio-js
recommendations: false
---

# How to use the GPT-4o Realtime API for speech and audio (Preview)

Azure OpenAI GPT-4o Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. The GPT-4o Realtime API is designed to handle real-time, low-latency conversational interactions, making it a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

Most users of the Realtime API need to deliver and receive audio from an end-user in real time, including applications that use WebRTC or a telephony system. The Realtime API isn't designed to connect directly to end user devices and relies on client integrations to terminate end user audio streams. 

## Supported models

Currently only `gpt-4o-realtime-preview` version: `2024-10-01-preview` supports real-time audio.

The `gpt-4o-realtime-preview` model is available for global deployments in [East US 2 and Sweden Central regions](../concepts/models.md#global-standard-model-availability).

> [!IMPORTANT]
> The system stores your prompts and completions as described in the "Data Use and Access for Abuse Monitoring" section of the service-specific Product Terms for Azure OpenAI Service, except that the Limited Exception does not apply. Abuse monitoring will be turned on for use of the `gpt-4o-realtime-preview` API even for customers who otherwise are approved for modified abuse monitoring.

## API support

Support for the Realtime API was first added in API version `2024-10-01-preview`. 

> [!NOTE]
> For more information about the API and architecture, see the [Azure OpenAI GPT-4o real-time audio repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk).

## Prerequisites


## Deploy a model for real-time audio

Before you can use GPT-4o real-time audio, you need:

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).


## Use the GPT-4o real-time audio

You need a deployment of the `gpt-4o-realtime-preview` model in a supported region as described in the [supported models](#supported-models) section. You can deploy the model from the [Azure AI Studio model catalog](../../ai-studio/how-to/model-catalog-overview.md) or from your project in AI Studio. 

For steps to deploy and use the `gpt-4o-realtime-preview` model, see [the real-time audio quickstart](../realtime-audio-quickstart.md).






## Related content

* Learn more about Azure OpenAI [deployment types](deployment-types.md)
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md)
