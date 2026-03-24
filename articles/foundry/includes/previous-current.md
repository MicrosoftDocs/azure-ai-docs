---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/04/2026
ms.custom: include, classic-and-new

---
## Evolution of Foundry

Foundry consolidates several previous Azure AI services and tools into a unified platform. The following table maps previous concepts to their current equivalents.

| Dimension | Previous | Current |
|-----------|---------|-----|
| Brand | Azure AI Studio / Azure AI Foundry | Microsoft Foundry |
| Brand | Azure AI Services | Foundry Tools |
| Portal | [Foundry (classic)](/azure/foundry-classic/) | [Foundry](/azure/foundry) |
| Agent API | Assistants API (Agents v0.5/v1) | Responses API (Agents v2) |
| API versioning | Monthly `api-version` params | v1 stable routes (`/openai/v1/`) |
| Resource model | Hub + Azure OpenAI + Azure AI Services | Foundry resource (single, with projects) |
| SDKs & endpoints | Multiple packages (`azure-ai-inference`, `azure-ai-generative`, `azure-ai-ml`, `AzureOpenAI()`) against 5+ endpoints | Unified project client (`azure-ai-projects` 2.x) + `OpenAI()` against one project endpoint. |
| Terminology | Threads, Messages, Runs, Assistants | Conversations, Items, Responses, Agent Versions |
