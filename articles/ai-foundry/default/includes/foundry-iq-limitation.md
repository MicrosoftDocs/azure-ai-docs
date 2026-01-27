---
title: Foundry Agent Service Limitations for Per-User Trimming 
description: Important box about the limitations of using Foundry Agent Service with Foundry IQ for per-user trimming security trimming.
author: haileytap
ms.author: haileytapia
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/27/2026
ms.custom: include file
---

> [!IMPORTANT]
> In this preview, Foundry Agent Service doesn't support per-request headers for MCP tools. Headers set in agent definitions apply to all invocations and can't vary by user or request.
>
> For per-user authorization, use the [Azure OpenAI Responses API](/azure/ai-foundry/openai/how-to/responses) instead.