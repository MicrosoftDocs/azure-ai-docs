---
title: What is Video Retrieval?
titleSuffix: Azure AI services
description: Learn about the basic concepts and features of Azure AI Vision Video Retrieval.
author: PatrickFarley
manager: nitinme
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.update-cycle: 365-days
ms.author: pafarley
ms.service: azure-ai-vision
ms.topic: overview
ms.date: 05/22/2025
ms.custom: contperf-fy22q2, ignite-2022
---

# What is Video Retrieval?

[!INCLUDE [video-retrieval-deprecation](includes/video-retrieval-deprecation.md)]

Video Retrieval is a service that lets you create a search index, add documents (videos and images) to it, and search with natural language. Developers can define metadata schemas for each index and ingest metadata to the service to help with retrieval. Developers can also specify what features to extract from the index (vision, speech) and filter their search based on features.

> [!div class="nextstepaction"]
> [Call the Video Retrieval APIs](./how-to/video-retrieval.md)

## Input requirements

<!--
Spatial Analysis works on videos that meet the following requirements:
* The video must be in RTSP, rawvideo, MP4, FLV, or MKV format.
* The video codec must be H.264, HEVC(H.265), rawvideo, VP9, or MPEG-4.

#### [Video Retrieval](#tab/vr)
-->
[!INCLUDE [video-retrieval-input](./includes/video-retrieval-input.md)]



<!--
## Responsible use of Spatial Analysis technology

To learn how to use Spatial Analysis technology responsibly, see the [Transparency note](/azure/ai-foundry/responsible-ai/computer-vision/transparency-note-spatial-analysis?context=%2fazure%2fcognitive-services%2fComputer-vision%2fcontext%2fcontext). Microsoft's transparency notes help you understand how our AI technology works and the choices system owners can make that influence system performance and behavior. They focus on the importance of thinking about the whole system including the technology, people, and environment.
-->

<!--
## Next step

> [!div class="nextstepaction"]
> [Install and run the Spatial Analysis container](spatial-analysis-container.md)
-->