---
title: "Quickstart - Get started with Azure OpenAI audio generation (Classic)"
description: "Get started with audio generation using Azure OpenAI. (Classic)"
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/30/2026
author: PatrickFarley
ms.author: pafarley
ms.custom:
  - references_regions
  - classic-and-new
zone_pivot_groups: audio-completions-quickstart
recommendations: false

ROBOTS: NOINDEX, NOFOLLOW
---

# Quickstart: Get started with Azure OpenAI audio generation (Classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/openai/audio-completions-quickstart.md)

[!INCLUDE [audio-completions-quickstart 1](../../foundry/openai/includes/audio-completions-quickstart-1.md)]

## Troubleshooting

> [!NOTE]
> When using `gpt-4o-audio-preview` for chat completions with the audio modality and `stream` is set to true, the only supported audio format is pcm16.

### Audio duration limit for transcription

Maximum duration of input audio for transcription is one hour (3,600 seconds). Service returns an error for longer audio inputs.

### Authentication errors

If you receive a 401 or 403 error:
- **Keyless auth:** Verify you've run `az login` and have the `Cognitive Services User` role assigned to your account.
- **API key:** Check that `AZURE_OPENAI_API_KEY` is set correctly and the key hasn't been regenerated.

### Model not found

If the `gpt-4o-mini-audio-preview` model isn't available:
- Verify the model is deployed in your Azure OpenAI resource.
- Check that you're using a [supported region](../foundry-models/concepts/models-sold-directly-by-azure.md).

### Audio file issues

If the generated audio file doesn't play:
- Ensure the file was written completely (check file size is greater than 0 bytes).
- Verify the format matches what your player supports (wav is widely compatible).
- For streaming responses, remember that only pcm16 format is supported.

### Rate limiting

If you receive a 429 error, you've exceeded the rate limit. Wait and retry, or request a quota increase. For more information about rate limits, see [Azure OpenAI quotas and limits](quotas-limits.md).

[!INCLUDE [audio-completions-quickstart 2](../../foundry/openai/includes/audio-completions-quickstart-2.md)]
