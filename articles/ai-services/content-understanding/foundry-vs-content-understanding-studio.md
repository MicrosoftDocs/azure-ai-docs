---
title: Content Understanding Studio and Microsoft Foundry
titleSuffix: Foundry Tools
description: Compare API versions, prebuilt analyzer availability, and customization features in Content Understanding Studio and Microsoft Foundry.
author: PatrickFarley 
ms.author: pafarley
manager: mcleans
ms.date: 08/06/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
ms.topic: overview
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Content Understanding Studio and Microsoft Foundry

Content Understanding Studio and the Content Understanding playground in Microsoft Foundry (new) are two experiences for working with Azure Content Understanding. Both experiences use the same underlying Content Understanding service, Microsoft Foundry resource, and Azure authentication.

## Quick comparison

Use this comparison to select an experience for your development and testing workflow.

| Feature | Content Understanding Studio | Foundry (new) |
|---------|--------------------------------|---------------|
| **API versions** | `2025-11-01` (GA) and `2026-06-01-preview` | `2026-06-01-preview` |
| **Read and Layout analyzers** | ✓ | ✓ |
| **Prebuilt analyzers** | All | Partial set |
| **Search analyzers** | ✓ | ✓ |
| **Audio, video, and image modality analyzers** | ✓ | ✓ |
| **Create custom analyzers** | ✓ | ❌ |
| **In-context learning with data labeling** | ✓ | ❌ |


> [!NOTE]
> Content Understanding Studio supports the `2025-11-01` GA API and the `2026-06-01-preview` API. The Content Understanding playground in Foundry (new) supports the `2026-06-01-preview` API. Preview APIs are provided without a service-level agreement and aren't recommended for production workloads. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Choose an experience

Use [Content Understanding Studio](https://contentunderstanding.ai.azure.com/) when you need the complete prebuilt analyzer catalog, custom analyzer authoring and building, in-context learning with data labeling, or the `2025-11-01` GA API. If you primarily work in Microsoft Foundry, use the [Content Understanding playground](https://ai.azure.com/) for supported analyzers and switch to Studio when you need these Studio-only capabilities.

The analyzer gallery in each experience shows which analyzers are available for the selected API version. For analyzer descriptions, see [Prebuilt analyzers](concepts/prebuilt-analyzers.md).

## Foundry (classic) deprecation

> [!IMPORTANT]
> Foundry (classic) was deprecated on July 15, 2026, and is no longer available as a Content Understanding experience. Use Content Understanding Studio or Foundry (new).

## Related content

- [Get started with Content Understanding Studio](quickstart/content-understanding-studio.md).
- [Explore prebuilt analyzers](concepts/prebuilt-analyzers.md).
