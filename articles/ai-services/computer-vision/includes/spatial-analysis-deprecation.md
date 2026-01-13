---
title: Spatial Analysis deprecation notice
titleSuffix: Foundry Tools
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: include
ms.date: 02/21/2025
ms.author: pafarley
---

> [!CAUTION]
> On 30 March 2025, Azure Vision Spatial Analysis was retired. The Spatial Analysis container is longer supported and will not process new video streams. Please transition to [Azure AI Video Indexer](https://azurearcjumpstart.com/azure_arc_jumpstart/azure_edge_iot_ops/aks_edge_essentials_single_vi) or another open-source solution. In addition to the familiar features you are using, here's a quick comparison between Azure Vision Spatial Analysis and Azure AI Video Indexer.
>
>|Feature |	Azure Vision Spatial Analysis |	Azure AI Video Indexer |
>|---|---|---|
>|Edge support |	Yes 	|Yes |
>|Object Detection |	People & Vehicle detection only |	Detects 1000+ objects |
>|Audio/Speech Processing |	Not supported |	Supported (includes speech transcription, translation and summarization)<br>Supported >(includes speech transcription and sentiment analysis) |
>|Event Detection & Tracking |	Supported (tracking people & vehicles, event detection) |	Not supported at the Edge yet. Is partially supported at the Cloud. |
>|Azure Arc Support|	Not supported |	Native support |
>|Focus Area 	|Visual analysis with specialized tracking |	Comprehensive analysis of both audio and visual content |
