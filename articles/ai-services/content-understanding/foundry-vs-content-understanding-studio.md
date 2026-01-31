---
title: Feature comparison for Content Understanding in Foundry and Content Understanding Studio
titleSuffix: Foundry Tools
description: Learn about the available options in Foundry and Content Understanding Studio.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Compare Content Understanding in Foundry and Content Understanding Studio

## Overview

Azure Content Understanding in Foundry Tools transforms unstructured content—documents, images, audio, and video—into structured, searchable data. The Foundry experience is complemented by Content Understanding Studio, which is designed for customers who are transitioning from Azure Document Intelligence in Foundry Tools or need advanced analyzer refinement capabilities. This article describes the capabilities available and planned in each experience.

## Quick comparison

Foundry portal and Content Understanding Studio have parity for most features. See the chart for key differences.

| Feature category | Foundry (new) (coming soon) | Foundry (classic) | Content Understanding Studio |
|------------------|-----------------|-----------------|-----------------|
| **API version support** | 2025-11-01 GA API support | 2025-05-01-preview | 2025-11-01 GA API support |
| **Supports agent building?** |	✅ | ❌	| ❌ |
| **Supports in-context learning (data labeling)?**	| ❌ | ❌	| ✅ | 

## What is offered in Foundry and Content Understanding Studio?

Content Understanding is available in Foundry (classic) and is coming soon to the updated Foundry (new) portal. 

The **Foundry (new) portal** (coming soon) offers the ability to:

* Build advanced, comprehensive agentic workflows with the Content Understanding tool.

> [!NOTE]
> In Foundry (classic), the supported Content Understanding API is 2025-05-01-preview. The updated Foundry (new) platform will soon support all the new features of the Content Understanding GA API 2025-11-01.

**Content Understanding Studio** is a complementary UX experience designed to create a smooth transition path for Document Intelligence customers. It brings familiar studio-based workflows—including testing, model refinement, and labeling—while extending capabilities to new multimodal capabilities and adding the power of generative AI models. Content Understanding Studio offers the following key capabilities:

* Improve custom analyzers by using data labeling techniques to optimize performance.
* Build classification-based custom analyzers for classification scenarios.
* Apply existing Document Intelligence expertise and patterns with familiar core concepts.

**Both experiences** offer the ability to:

* Try out prebuilt analyzers on your own data.
* Develop custom analyzers by using AI-assisted tools for output tailored to your scenario.
* Test custom analyzers on your own data.

## Summary

* **Foundry (new)** is coming soon, and is ideal for users seeking a comprehensive agent-building experience through the Foundry portal.
* **Foundry (classic)** supports the preview API, 2025-05-01-preview. It includes some preview features, like Pro mode, that aren't yet available in the GA API. Migrate to the new GA API when possible to continue getting the best experience from Content Understanding.
* **Content Understanding Studio** is best suited for users focused on building and refining analyzers, with a streamlined interface and guided setup. It's the ideal choice for Document Intelligence customers transitioning to Content Understanding, offering the same studio-based approach you already know while extending to analyze documents, images, audio, and video with enhanced classification and in-context learning capabilities.


## Next steps

* Check out the quickstart to [Get started with Content Understanding Studio](quickstart/content-understanding-studio.md).
