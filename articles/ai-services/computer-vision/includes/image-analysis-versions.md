---
title: "Image Analysis versions"
titleSuffix: "Azure AI services"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: include
ms.date: 01/20/2023
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.author: pafarley
---

## Image Analysis versions

> [!IMPORTANT]
> Select the Image Analysis API version that best fits your requirements.
>
> | Version | Features available | Recommendation&nbsp;|
> |:----------|--------------|-------------------------|
> | version&nbsp;4.0 | Read text, Captions, Dense captions, Tags, Object detection, Custom image classification / object detection, People, Smart crop | Better models; use version 4.0 if it supports your use case. |
> | version&nbsp;3.2 | Tags, Objects, Descriptions, Brands, Faces, Image type, Color scheme, Landmarks, Celebrities, Adult content, Smart crop | Wider range of features; use version 3.2 if your use case is not yet supported in version 4.0 |
> 
> We recommend you use the Image Analysis 4.0 API if it supports your use case. Use version 3.2 if your use case is not yet supported by 4.0.
>
> You'll also need to use version 3.2 if you want to do image captioning and your Vision resource is outside the supported Azure regions. The image captioning feature in Image Analysis 4.0 is only supported in certain Azure regions. Image captioning in version 3.2 is available in all Azure AI Vision regions. See [Region availability](/azure/ai-services/computer-vision/overview-image-analysis#region-availability).
