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
> Foundry Agent Service doesn't currently support per-user security trimming. This affects knowledge bases that require user-delegated authorization via `x-ms-query-source-authorization`, such as remote SharePoint knowledge sources.
>
> For per-user authorization, use the [Azure OpenAI Responses API](/azure/ai-foundry/openai/how-to/responses) instead.