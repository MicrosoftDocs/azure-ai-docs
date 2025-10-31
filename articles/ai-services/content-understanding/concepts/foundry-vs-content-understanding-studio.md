---
title: Feature comparison Content Understanding in Azure AI Foundry vs Content Understanding Studio
titleSuffix: Azure AI services
description: Learn about the available options in AI Foundry and Content Understanding Studio
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 10/30/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Feature comparison: Content Understanding in Azure AI Foundry vs Content Understanding Studio

## Overview
Azure AI Content Understanding is an Azure AI Foundry service that transforms unstructured content- documents, images, audio and video- into structured, searchable data. The Azure AI Foundry experience is complemented by the Content Understanding Studio for customers that need advanced capabilities. This document describes the capabilities available and planned in each of these experiences.

## What is offered in Azure AI Foundry vs Content Understanding Studio?

Content Understanding is available in AI Foundry Classic and is coming soon to the updated AI Foundry NextGen portal. 

The **Azure AI Foundry NextGen portal** (coming soon) will offer the ability to:
* Build advanced, comprehensive agentic workflows with the Content Understanding Tool

> [!NOTE]
> In AI Foundry Classic, the supported Content Understanding API is 2025-05-01-preview. The updated Foundry NextGen platform will soon support all the great new features of the Content Understanding GA API 2025-11-01.

**Content Understanding Studio** is a complementary UX experience that brings the power of analyzer improvement to your custom analyzer workflows. Content Understanding Studio offers the following key capabilities:
* Improve custom analyzers using data labeling techniques to optimize performance
* Build classification-based custom analyzers to meet the needs of your classification scenarios

**Both experiences** offer the ability to:
* Try out prebuilt analyzers on your own data
* Develop custom analyzers using AI assisted tools for an output tailored to your unique scenario
* Test custom analyzers on your own data

## Quick comparison 
AI Foundry portal and Content Understanding Studio have parity in most all features. See the chart below to understand the key differences.

| Feature Category | Azure AI Foundry NextGen (Coming soon) | Azure AI Foundry Classic |	Content Understanding Studio |
|------------------|-----------------|-----------------|-----------------|
| **API version support** | 2025-11-01 GA API support | 2025-05-01-preview | 2025-11-01 GA API support |
| **Supports agent building?** |	✅ | ❌	| ❌ |
| **Supports in-context learning (data labeling)?**	| ❌ | ❌	| ✅ |
| **Supports classification?** | ❌ |  ❌ | ✅ | 
| **Supported modes**	| Supports Standard mode only | Offers both Standard and Pro modes for extended agentic features (2025-05-01-preview)	| Supports Standard mode| 


## Summary

* **Azure AI Foundry NextGen** is coming soon, and is ideal for users seeking a comprehensive agent-building experience through the AI Foundry portal.
* **Azure AI Foundry Classic** supports the preview API, 2025-05-01-preview. Migrate to the new GA API when possible to continue getting the best experience from Content Understanding.
* **Content Understanding Studio** is best suited for users focused on building and refining analyzers, with a streamlined interface and guided setup.


## Next steps
* Check out the quickstart to [get started with Content Understanding Studio](../quickstart/cu-studio.md)
