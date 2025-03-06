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

[!INCLUDE [Feature preview](../../../../includes/preview-feature.md)]

In this article, you learn how to use video translation with Azure AI Speech in the [Azure AI Foundry portal](https://ai.azure.com/).

> [!TIP]
> Try out video translation in the [Azure AI Foundry portal](https://ai.azure.com/) before using the API. Use the [video translation REST API](?pivots=rest-api) to integrate video translation into your applications. For more information about the API, see [Video translation REST API](/rest/api/aiservices/videotranslation/translation-operations/create-translation).

## Try out video translation

To try out video translation, follow these steps:

1. Go to the [model catalog in Azure AI Foundry portal](https://ai.azure.com/explore/models). 
   
1. Enter and search for "Azure-AI-Speech" in the catalog search box.

   :::image type="content" source="../../../media/video-translation/search-model-catalog.png" alt-text="Screenshot of the model catalog in Azure AI Foundry portal." lightbox="../../../media/video-translation/search-model-catalog.png":::

1. Select **Azure-AI-Speech** and you're taken to the **Azure-AI-Speech** try out page.
1. Select **Speech capabilities by scenario** > **Video translation**.

   :::image type="content" source="../../../media/video-translation/capabilities-by-scenario.png" alt-text="Screenshot of filtering Speech service capabilities by scenario." lightbox="../../../media/video-translation/capabilities-by-scenario.png":::

1. Under the **Sample option** to the right, select personal or prebuilt voice.

1. Select the **Play** button to hear the translated audio. Select the original video tab to play the original audio.

   :::image type="content" source="../../../media/video-translation/compare-original-translated.png" alt-text="Screenshot of selecting a voice type on the new project page." lightbox="../../../media/video-translation/compare-original-translated.png":::
   
   The voice type options are:
   - **Prebuilt voice**: The service automatically selects the most suitable prebuilt voice by matching the speaker's voice in the video with prebuilt voices.
   - **Personal voice**: Use the personal voice that matches the voice of the speakers in the video. 

   > [!NOTE]
   > To use personal voice via the API, you need to apply for [access](https://aka.ms/customneural). 
  

## Related content

- [Video translation overview](../../../video-translation-overview.md)
