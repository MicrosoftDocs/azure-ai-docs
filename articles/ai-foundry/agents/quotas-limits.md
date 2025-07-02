---
title: Quotas and limits for Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn about the quotas and limits for when you use Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 05/29/2025
ms.custom: azure-ai-agents
---

# Azure AI Foundry Agent Service quotas and limits

This article contains a reference and a detailed description of the quotas and limits for Azure AI Foundry Agent Service.

## Quotas and limits for the Azure AI Foundry Agent Service

The following sections provide you with a guide to the default quotas and limits that apply to Azure AI Foundry Agent Service:

| Limit Name | Limit Value |
|--|--|
| Max files per agent/thread | 10,000 |
| Max file size for agents & fine-tuning | 512 MB |
| Max size for all uploaded files for agents |200 GB |  
| agents token limit | 2,000,000 token limit |

The 2,000,000 agent limit refers to the maximum number of distinct Agent resources that can be created within a single Azure subscription per region. It does not apply to threads or token usage.

## Quotas and limits for Azure OpenAI models

See the [Azure OpenAI](../../ai-services/openai/quotas-limits.md) for current quotas and limits for the Azure OpenAI models that you can use with Azure AI Foundry Agent Service. 

## Next steps

[Learn about the models available for Azure AI Foundry Agent Service](concepts\model-region-support.md)
