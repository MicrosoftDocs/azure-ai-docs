---
title: Quotas and limits for Azure AI Agent Service
titleSuffix: Azure AI services
description: Learn about the quotas and limits for when you use Azure AI Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 12/11/2024
ms.custom: azure-ai-agents
---

# Azure AI Agent Service quotas and limits

This article contains a reference and a detailed description of the quotas and limits for Azure AI Agent Service.

## Quotas and limits for the Azure AI Agent Service

The following sections provide you with a guide to the default quotas and limits that apply to Azure AI Agent Service:

| Limit Name | Limit Value |
|--|--|
| Max files per agent/thread | 10,000 when using the API or [Azure AI Foundry portal](https://ai.azure.com/). In Azure OpenAI Studio the limit was 20.|
| Max file size for agents & fine-tuning | 512 MB |
| Max size for all uploaded files for agents |100 GB |  
| agents token limit | 2,000,000 token limit |

The 2,000,000 agent limit refers to the maximum number of distinct Agent resources that can be created within a single Azure subscription per region. It does not apply to threads or token usage.

## Quotas and limits for Azure OpenAI models

See the [Azure OpenAI](../openai/quotas-limits.md) for current quotas and limits for the Azure OpenAI models that you can use with Azure AI Agent Service. 

## Next steps

[Learn about the models available for Azure AI Agent Service](./concepts/model-region-support.md)
