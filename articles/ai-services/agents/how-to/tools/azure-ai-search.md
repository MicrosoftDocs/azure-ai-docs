---
title: 'How to use an existing AI Search index with the Azure AI Search tool'
titleSuffix: Azure OpenAI
description: Learn how to use Agents Azure AI Search tool.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 12/11/2024
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
zone_pivot_groups: selection-azure-ai-search
---

# Use an existing AI Search index with the Azure AI Search tool
::: zone pivot="overview-azure-ai-search"
Use an existing Azure AI Search index with the agent's Azure AI Search tool.

> [!NOTE] 
> Azure AI Search indexes must meet the following requirements:
> - The index must contain at least one searchable & retrievable text field (type Edm.String) 
> - The index must contain at least one searchable vector field (type Collection(Edm.Single)) 
> - The index is assumed to be configured properly

## Search types
You can specify the search type for your index by choosing one of the following
- Simple
- Semantic
- Vector
- Hybrid (Vector + Keyword)
- Hybrid (Vector + Keyword + Semantic)


**Indexes without a specified search type**
- By default, the Azure AI Search tool runs a hybrid search (keyword + vector) on all text fields 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

[!INCLUDE [setup](../../includes/azure-search/setup.md)]

::: zone-end

::: zone pivot="code-examples"

[!INCLUDE [code-examples](../../includes/azure-search/code-examples.md)]

::: zone-end
