---
title: Quotas and limits for Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn about the quotas and limits for when you use Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: conceptual
ms.date: 07/03/2025
ms.custom: azure-ai-agents
---

# Azure AI Foundry Agent Service quotas and limits

This article contains a reference and a detailed description of the quotas and limits for Azure AI Foundry Agent Service.

## Quotas and limits for the Azure AI Foundry Agent Service

The following sections provide you with a guide to the default quotas and limits that apply to Azure AI Foundry Agent Service:

| Limit Name | Limit Value |
|--|--|
| Maximum number of files per agent/thread | 10,000 |
| Maximum file size for agents & fine-tuning | 512 MB |
| Maximum size for all uploaded files for agents | 300 GB |
| Maximum file size in tokens for attaching to a vector store | 2,000,000 tokens |
| Maximum number of messages per thread | 100,000 |
| Maximum size of `text` content per message | 1,500,000 characters |
| Maximum number of tools registered per agent | 128 |

## Quotas and limits for Azure OpenAI models

See the [Azure OpenAI](../openai/quotas-limits.md) for current quotas and limits for the Azure OpenAI models that you can use with Azure AI Foundry Agent Service. 

## Next steps

[Learn about the models available for Azure AI Foundry Agent Service](concepts\model-region-support.md)
