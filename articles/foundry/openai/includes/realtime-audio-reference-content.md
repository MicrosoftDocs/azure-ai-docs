---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/13/2026
ms.custom: include, classic-and-new, ai-assisted
---

The Azure OpenAI Realtime API follows the OpenAI Realtime API specification. For the full API reference, see the [OpenAI Realtime API reference](https://developers.openai.com/api/reference/resources/realtime).

> [!NOTE]
> **Azure deviation:** The accepted values for the `model` field in `input_audio_transcription` settings differ from the OpenAI reference. Azure OpenAI requires the name of the existing model deployment for the field, like `my-gpt-4o-transcribe-deployment`. See details <link to the correspondent articles> about Model deployment via Foundry Portal and programmatically.