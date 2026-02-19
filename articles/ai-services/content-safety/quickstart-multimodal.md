---
title: "Quickstart: Analyze multimodal content"
titleSuffix: Azure AI services
description: Get started using Azure AI Content Safety to analyze text content in images for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 11/21/2025
ms.author: pafarley
zone_pivot_groups: programming-languages-content-safety-foundry-rest
---

# Quickstart: Analyze multimodal content (preview) 

The Multimodal API analyzes materials containing both image content and text content to help make applications and services safer from harmful user-generated or AI-generated content. Analyzing an image and its associated text content together can preserve context and provide a more comprehensive understanding of the content.

For more information on how content is filtered, see the [Harm categories concept page](./concepts/harm-categories.md#multimodal-image-with-text-content). For API input limits, see the [Input requirements](./overview.md#input-requirements) section of the Overview. 

> [!IMPORTANT]
> This feature is only available in certain Azure regions. See [Region availability](./overview.md#region-availability).

::: zone pivot="programming-language-foundry-portal"

[!INCLUDE [Studio quickstart](./includes/quickstarts/foundry-quickstart-multimodal.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [cURL quickstart](./includes/quickstarts/rest-quickstart-multimodal.md)]

::: zone-end
