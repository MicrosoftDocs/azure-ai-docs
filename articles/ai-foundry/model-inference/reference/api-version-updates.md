---
title: Azure AI Model Inference API releases and lifecycle
titleSuffix: Azure AI Foundry
description: Learn more about API versions in Azure AI Model Inference in Azure AI Services.
manager: scottpolly
ms.service: azure-ai-model-inference
ms.topic: conceptual
ms.date: 03/01/2025
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# Azure AI Model Inference API releases and lifecycle

This article explains Azure AI Model Inference API versions and how you think about them. Whenever possible we recommend using either the latest GA, or preview API releases.

## Latest API releases

The following list contains the latest releases of APIs for Azure AI Model Inference. 

### 2025-04-01

This version expands the previous API version and introduces the following features:

* General availability.
* Reasoning models return reasoning content in the field `reasoning_content` on messages of with role `assistant`. When streaming content, both `content` and `reasoning_content` are included in deltas.
* Route `/info` adds an optional parameter `model` to indicate the model deployment name to get information from when the endpoint is running multiple model deployments.

### 2024-05-01-preview

This version introduces the following features:

* Embeddings models.
* Image embeddings models.
* Chat completions models with images and audio inputs.

## Deprecation

The following API version has been deprecated and marked for retirement:

| API Version        | Status     | Replace with API     | Deprecation date | Retirement date | 
|--------------------|------------|----------------------|------------------|-----------------|
| 2024-05-01-preview | Deprecated | [2025-04-01](/rest/api/aifoundry/model-inference/operation-groups?view=rest-aifoundry-model-inference-2024-04-01&preserve-view=true)       | 04/10/2025       | 04/10/2026      | 