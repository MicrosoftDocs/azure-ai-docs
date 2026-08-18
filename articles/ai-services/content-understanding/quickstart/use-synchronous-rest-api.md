---
title: "Quickstart: Use synchronous Content Understanding operations"
titleSuffix: Foundry Tools
description: Use synchronous Read and Layout operations in the Content Understanding REST API to extract content from small documents and images.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 08/05/2026
ms.service: azure-content-understanding-foundry-tools
ms.topic: quickstart
ms.custom:
  - dev-focus
ai-usage: ai-assisted
---

# Quickstart: Use synchronous Content Understanding operations

Synchronous operations work best for interactive scenarios that need extracted content right away or want to avoid temporary service-side storage during processing. These operations process the input in memory and return structured content directly in the response. You don't send a separate request to check for the result. In this public preview, synchronous operations are available for the `prebuilt-read` and `prebuilt-layout` analyzers.

Synchronous operations support the same document file formats as asynchronous operations. For file size, page, character, and page range limits, see [Content Understanding service limits](../service-limits.md#document-and-text).


[!INCLUDE [Synchronous REST API quickstart](./includes/rest-synchronous-quickstart.md)]
