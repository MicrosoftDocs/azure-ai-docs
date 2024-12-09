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
The Azure AI Search tool currently only supports indexes with unstructured data. If you have structured data in your index, we cannot make any guarantees on the quality of the search results.

::: zone-end

::: zone pivot="code-examples"

## Quickstart – Use an existing Azure AI Search index with the Azure AI Search tool

In this quickstart, you'll learn how to use an existing Azure AI Search index with the Azure AI Search tool.

### Prerequisites
1. One prerequite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal or via REST API.
- [Quickstart: Create a vector index using the Azure portal](../../../search/search-get-started-portal-import-vectors.md)
- [Quickstart: Create a vector index using REST API](../../../search/search-get-started-vector.md)

### Setup: Create an agent that can uses an existing Azure AI Search index
#### 1. Complete the agent setup
- **Option 1: Standard Agent Setup using existing AI Search resource** If you want your agent to uses an existing AI Search resource to create new indexes or bring existing ones you should use the [standard agent setup and add your AI Search resourc ID](../../quickstart.md). 
        - You can provide your Azure AI Search resource ID in the bicep file. Your resource ID should be in the format: `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}`.
- **Option 2: Standard Agent Setup** If you want to create a new Azure AI Search resource for you agents to use when creating new indexes follow the [standard agent setup](../../quickstart.md).
- **Option 3: Basic Agent Setup** If you want your agent to use multitenant search and storage resources fully managed by Microsoft and connect your AI Search index later use the [basic agent setup](../../quickstart.md).

#### 2. Create a project connection to the Azure AI Search resource with the index you want to use
If you already connected the AI Search resource that contains the index you want to use to your project, skip this step.

1. In the Azure Portal, navigate to the AI Search resource that contains the index you want to use.
2. Make sure your ACS resource is set to “Both” API key and RBAC access control.
    :::image type="content" source="../../media/tools/ai-search/acs-azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/acs-azure-portal.png":::

3. In Azure AI Foundry, navigate to the project you created in the agent setup and Click on **Open in management center**.
    :::image type="content" source="../../media/tools/ai-search/project-studio.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/project-studio.png":::
4. Click on the **Connections** tab.
5. Click on **Add Connection**.
 :::image type="content" source="../../media/tools/ai-search/project-connections-page.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/project-connections-page.png":::
6. Select **Azure AI Search**.
 :::image type="content" source="../../media/tools/ai-search/select-acs.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/select-acs.png":::
1. Select the Azure AI Search resource that has the index you want to use and fill in the required fields. Both Managed Identity and Key-based authentication are supported. Once all the fields are filled in, click **Add connection**.
:::image type="content" source="../../media/tools/ai-search/acs-connection2.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/acs-connection2.png":::
1. Verify that the connection was successfully created.
:::image type="content" source="../../media/tools/ai-search/success-acs-connection.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/success-acs-connection.png":::

::: zone-end