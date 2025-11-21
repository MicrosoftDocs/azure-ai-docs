---
title: Quotas and Limits for Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn about the quotas and limits for when you use Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: conceptual
ms.date: 11/20/2025
ms.custom: azure-ai-agents
monikerRange: 'foundry-classic || foundry'
---

# Foundry Agent Service quotas and limits

This article describes the quotas and limits for Microsoft Foundry Agent Service.

## Default quotas and limits for the service

| Limit name | Limit value |
|--|--|
| Maximum number of files per agent/thread | 10,000 |
| Maximum file size for agents | 512 MB |
| Maximum size for all uploaded files for agents | 300 GB |
| Maximum file size in tokens for attaching to a vector store | 2,000,000 tokens |
| Maximum number of messages per thread | 100,000 |
| Maximum size of `text` content per message | 1,500,000 characters |
| Maximum number of tools registered per agent | 128 |

## Quotas and limits for models

For current quotas and limits for the models that you can use with agents, see the [Azure OpenAI documentation](../openai/quotas-limits.md) and [Microsoft Foundry Models documentation](../foundry-models/quotas-limits.md).

## Related content

- [Supported models in Foundry Agent Service](concepts\model-region-support.md)
