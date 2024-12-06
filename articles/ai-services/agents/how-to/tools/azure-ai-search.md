---
title: 'How to BYO AI Search index with the Azure AI Search tool'
titleSuffix: Azure OpenAI
description: Learn how to use Agents file search.
services: azure-ai-agent service
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 11/20/2024
author: fosteramanda
ms.author: fosteramanda
recommendations: false
zone_pivot_groups: selection-azure-ai-search
---

# BYO AI Search index with the Azure AI Search tool
::: zone pivot="overview"

Use an existing Azure AI Search index with the agent's Azure AI Search tool.

> [!NOTE] Azure AI Search indexes must meet the following requirements:
> - The index must contain at least one searchable & retrievable text field (type Edm.String) 
> - The index must contain at least one searchable vector field (type Collection(Edm.Single)) 
> - The index must use a vector profile/integrated vectorization

## Search types

**Index without semantic configuration**
- By default, the Azure AI Search tool runs a hybrid search (keyword + vector) on all text fields. 
<br>

**Index with semantic configuration**
- By default, the Azure AI Search tool can uses semantic or hybrid + semantic search on all text fields.

## File Types
The Azure AI Search tool currently only supports indexes with unstructured data. 
The Azure AI Search tool supports the following file types:

::: zone-end

::: zone pivot="code-examples"

## Quickstart – Use an existing Azure AI Search index with the Azure AI Search tool

In this quickstart, you'll learn how to use an existing Azure AI Search index with the Azure AI Search tool.

### Prerequisites
1. One prerequite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal or via REST API.
- [Quickstart: Create a vector index using the Azure portal](../../../search/search-get-started-portal-import-vectors.md)
- [Quickstart: Create a vector index using REST API](../../../search/search-get-started-vector.md)

### Setup: Create an agent that can uses an existing Azure AI Search index
You have not completed the agent setup
1. **Option 1: Standard Agent Setup using existing AI Search resource** If you want your agent to uses an existing AI Search resource to create new indexes or bring existing ones you should use the [standard agent setup and add your AI Search resourc ID](../../quickstart.md). 
    - You can provide your Azure AI Search resource ID in the bicep file. Your resource ID should be in the format: `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}`.
2. **Standard Agent Setup** If you want to create a new Azure AI Search resource for you agents to use when creating new indexes follow the [standard agent setup](../../quickstart.md).
3. **Basic Agent Setup** If you don't want

### Setup: Create a project connection to the Azure AI Search resource with the index you want to use
1. In Azure AI Foundry, navigate to the project you created in the agent setup.
1. 


::: zone-end