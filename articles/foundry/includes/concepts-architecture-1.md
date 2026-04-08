---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## When to use this architecture

Consider the Foundry resource model when your scenario involves:

- **First-time setup**: You're starting a new AI project and want a single resource that bundles model access, agent hosting, and evaluation tooling.
- **Multi-team access**: Multiple teams need isolated projects with shared model deployments and centralized governance.
- **Compliance-driven design**: Your organization requires private networking, customer-managed encryption, or Azure RBAC scoping at both resource and project levels.
- **Azure OpenAI migration**: You're moving from a standalone Azure OpenAI resource and want to keep existing policies and RBAC while adding agent and evaluation capabilities.

For single-developer exploration, a Foundry resource with one project is the recommended default. If your workload only requires Azure OpenAI completions without agent hosting or evaluation, a standalone Azure OpenAI resource might be sufficient.

## Azure AI resource types and providers

Within the Azure AI product family, you can use these [Azure resource providers](/azure/azure-resource-manager/management/resource-providers-and-types) that support user needs at different layers in the stack.

| Resource provider | Purpose | Supported services |
| --- | --- | --- |
| Microsoft.CognitiveServices | Supports Agentic and GenAI application development composing and customizing prebuilt models. | Foundry; Azure OpenAI; Azure Speech in Foundry Tools; Azure Language in Foundry Tools; Azure Vision in Foundry Tools | 
| Microsoft.Search | Supports knowledge retrieval over your data | Azure AI Search | 

For most AI development scenarios—including agent building, model deployment, and evaluation workflows—the Foundry resource is the recommended starting point. Foundry resources share the Microsoft.CognitiveServices provider namespace with services such as Azure OpenAI, Speech, Vision, and Language. This shared provider namespace helps align management APIs, access control patterns, networking, and policy behavior across related AI resources.

Use the following table to identify which resource type matches your workload. It shows the specific resource types and capabilities within the Microsoft.CognitiveServices provider: