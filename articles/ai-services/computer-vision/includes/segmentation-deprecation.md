---
title: Background removal deprecation notice
titleSuffix: Azure AI services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: include
ms.date: 09/10/2024
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.update-cycle: 365-days
ms.author: pafarley
---

> [!IMPORTANT]
> This feature is now deprecated. On March 31, 2025, the Azure AI Image Analysis 4.0 Segment API and background removal service will be retired. All requests to this service will fail after this date.
>
> The segmentation feature of the open-source [Florence 2 model](https://huggingface.co/microsoft/Florence-2-large) might meet your needs. It returns an alpha map marking the difference between foreground and background, but it doesn't edit the original image to remove the background. Install the Florence 2 model and try out its Region to segmentation feature.
>
> For full-featured background removal, consider a third-party utility like [BiRefNet](https://github.com/ZhengPeng7/BiRefNet).