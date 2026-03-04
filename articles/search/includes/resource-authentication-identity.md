---
title: Include File
description: Include file for Azure AI Search authentication to Microsoft Foundry.
author: haileytap 
ms.author: haileytapia 
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/11/2026
# Use this file to describe authentication for Foundry-integrated scenarios.
---

Azure AI Search connects to Microsoft Foundry models for certain skills, vectorizers, and agentic retrieval workloads. You can configure this connection to use Microsoft Entra ID authentication and role-based access.

To configure the recommended role-based access:

1. [Create a managed identity](../search-security-enable-roles.md) for your search service.

1. [Assign the following roles](/azure/ai-foundry/concepts/rbac-foundry) in your Azure OpenAI resource or Microsoft Foundry resource.

    | Target Endpoint | Required Role | Scope |
    |-|-|-|
    | GPT-4/5 & text-embedding-3 | Cognitive Services OpenAI User | Azure OpenAI Resource |
    | Azure AI Vision multimodal 4.0 | Cognitive Services User | Azure AI Multi-service Resource |
    | Content Understanding  | Cognitive Services User | Microsoft Foundry Resource |
    | Foundry Model Orchestration | Azure AI User | Foundry Project |

1. Choose **Managed identity** and then assign your [search service managed identity](search-how-to-managed-identities.md).
