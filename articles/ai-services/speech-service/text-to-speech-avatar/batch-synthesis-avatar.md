---
title: How to use batch synthesis for text to speech avatar - Speech service
titleSuffix: Foundry Tools
description: Learn how to create text to speech avatar batch synthesis.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 08/07/2025
ms.author: pafarley
author: PatrickFarley
zone_pivot_groups: programming-languages-text-to-speech-avatar
---

# Use batch synthesis for text to speech avatar

The batch synthesis API for text to speech avatar lets you synthesize text asynchronously into a talking avatar as a video file. Publishers and video content platforms can use this API to create avatar video content in a batch. That approach can be suitable for different use cases like training materials, presentations, or advertisements.

The synthetic avatar video will be generated asynchronously after the system receives text input. The generated video output can be downloaded in batch mode synthesis. You submit text for synthesis, poll for the synthesis status, and download the video output when the status shows success. The text input formats must be plain text or Speech Synthesis Markup Language (SSML) text. 

This diagram provides a high-level overview of the workflow.

:::image type="content" source="./media/batch-synthesis-workflow.png" alt-text="Screenshot that shows a high-level overview of the batch synthesis workflow." lightbox="./media/batch-synthesis-workflow.png":::

::: zone pivot="ai-foundry"
[!INCLUDE [Foundry portal include](../includes/how-to/text-to-speech-avatar/ai-foundry.md)]
::: zone-end

::: zone pivot="programming-language-rest"
[!INCLUDE [REST include](../includes/how-to/text-to-speech-avatar/cli.md)]
::: zone-end

## Next steps

* [Batch synthesis properties](./batch-synthesis-avatar-properties.md)
* [Use batch synthesis for text to speech avatar](./batch-synthesis-avatar.md)
* [What is text to speech avatar](what-is-text-to-speech-avatar.md)
