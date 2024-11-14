---
title: Quotas and limits for Azure Agent Runtime
titleSuffix: Azure AI services
description: Learn about the quotas and limits for when you use Azure Agent Runtime.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: conceptual
ms.date: 11/13/2024
recommendations: false
---

# Azure Agent Runtime quotas and limits

This article contains a reference and a detailed description of the quotas and limits for Azure Agent Runtime.

## Quotas and limits for the Azure Agent Runtime service

The following sections provide you with a guide to the default quotas and limits that apply to Azure Agent Runtime:

| Limit Name | Limit Value |
|--|--|
| Max files per Assistant/thread | 10,000 when using the API or AI Studio. 20 when using Azure OpenAI Studio.|
| Max file size for Assistants & fine-tuning | 512 MB |
| Max size for all uploaded files for Assistants |100 GB |  
| Assistants token limit | 2,000,000 token limit |

## Quotas and limits for Azure OpenAI models

See the [Azure OpenAI](../openai/quotas-limits.md) for current quotas and limits for the Azure OpenAI models that you can use with Azure Agent Runtime. 

## Next steps

[Learn about the models available for Azure Agent Runtime](./concepts/model-region-support.md)