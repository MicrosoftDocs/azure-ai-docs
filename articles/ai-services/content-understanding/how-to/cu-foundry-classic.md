---
title: Create Content Understanding Standard and Pro tasks in the Azure AI Foundry Classic portal
titleSuffix: Azure AI services
description: Utilize the Foundry classic portal to create Content Understanding custom tasks
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 10/30/2025
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Create Content Understanding Standard and Pro tasks in the Azure AI Foundry Classic portal

Suppose you have files—such as documents, images, audio, or video—and you want to automatically extract key information from them. With Content Understanding, you can create a task to organize your data processing, define a field schema that specifies the information to extract or generate, and then build an analyzer. The analyzer becomes an API endpoint that you can integrate into your applications or workflows. 

This guide shows you how to utilize  Content Understanding Standard and Pro modes in the Azure AI Foundry Classic portal to build and test a custom analyzer that extracts structured information from your data. 

::: zone pivot="standard-mode"

[!INCLUDE [Content Understanding Standard mode](../includes/use-ai-foundry.md)]

::: zone-end

::: zone pivot="pro-mode"

[!INCLUDE [Content Understanding Pro mode](../includes/use-ai-foundry-pro-mode.md)]

::: zone-end
