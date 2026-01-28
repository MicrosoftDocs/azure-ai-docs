---
title: What is Foundry IQ?
titleSuffix: Microsoft Foundry
description: Learn about Foundry IQ, a context engineering platform for agentic RAG that turns enterprise data into reusable, permission-aware knowledge bases for AI agents.
author: haileytap
ms.author: haileytapia
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 01/28/2026
ai-usage: ai-assisted
---

# Foundry IQ (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Agents need context from scattered enterprise content to accurately answer questions. With Foundry IQ, you can create a configurable, multi-source *knowledge base* that provides agents with permission-aware responses based on your organization's data.

A knowledge base consists of *knowledge sources* (connections to internal and external data stores) and parameters that control retrieval behavior. Multiple agents can share the same knowledge base. When an agent queries the knowledge base, Foundry IQ uses *agentic retrieval* to process the query, retrieve relevant information, enforce user permissions, and return grounded answers with citations.

## Capabilities

+ Connect one knowledge base to multiple agents. Supported knowledge sources include internal data stores (such as Azure Blob Storage, SharePoint, and OneLake) and public web data.

+ Automate document chunking, vector embedding generation, and metadata extraction for indexed knowledge sources. Schedule recurring indexer runs for incremental data refresh.

+ Issue keyword, vector, or hybrid queries across indexed and remote knowledge sources.

+ Use the agentic retrieval engine with a large language model (LLM) to plan queries, select sources, run parallel searches, and aggregate results.

+ Return extractive data with citations so agents can reason over raw content and trace answers to source documents.

+ Synchronize access control lists (ACLs) for supported sources and honor Microsoft Purview sensitivity labels. Enforce permissions at query time so agents return only authorized content.

+ Run queries under the caller's Microsoft Entra identity for end-to-end permission enforcement.

## Components

A Foundry IQ knowledge base contains knowledge sources and uses agentic retrieval to process queries. Azure AI Search provides the underlying indexing and retrieval infrastructure.

| Component | Description |
|--|--|
| [Knowledge base](/azure/search/agentic-retrieval-how-to-create-knowledge-base) | Top-level resource that orchestrates agentic retrieval. Defines which knowledge sources to query and parameters that control retrieval behavior. |
| [Knowledge sources](/azure/search/agentic-knowledge-source-overview) | Connections to indexed or remote content. A knowledge base references one or more knowledge sources. |
| [Agentic retrieval](/azure/search/agentic-retrieval-overview) | Multi-query pipeline that decomposes complex questions into subqueries, executes them in parallel, semantically reranks results, and returns unified responses. Uses an optional LLM for query planning. |

You can call Foundry IQ knowledge bases from Foundry Agent Service, Microsoft Agent Framework, or any application that supports the knowledge base APIs from Azure AI Search.

## Workflow

You can set up Foundry IQ through a portal or programmatically. The following steps outline the typical workflow for both approaches.

### [Portal](#tab/portal)

1. Sign in to the [Microsoft Foundry (new) portal](../../../what-is-foundry.md#microsoft-foundry-portals).

1. Create a project or select an existing project.

1. From the top menu, select **Build**.

1. On the **Knowledge** tab:
    1. Create or connect to an existing search service that supports agentic retrieval.
    1. Create a knowledge base by adding one knowledge source at a time.
    1. Configure knowledge base properties for retrieval behavior.

1. On the **Agents** tab:

   1. Create or select an existing agent.
   1. Connect to your knowledge base.
   1. Use the playground to send messages and refine your agent.

> [!NOTE]
> + The playground provides a simplified workflow for proof-of-concept testing. When you move to code, configure managed identities and permissions to meet your organization's security requirements.
>
> + You can use the [Azure portal](/azure/search/get-started-portal-agentic-retrieval) to create knowledge bases and knowledge sources, but agent configuration and integration must be done in the Microsoft Foundry (new) portal or programmatically.

### [Programmatic](#tab/programmatic)

1. [Create knowledge sources](/azure/search/agentic-knowledge-source-overview).

1. [Create a knowledge base](/azure/search/agentic-retrieval-how-to-create-knowledge-base) that references your knowledge sources.

1. [Connect an agent](/azure/ai-foundry/agents/how-to/tools/knowledge-retrieval) to your knowledge base.

1. Send messages and refine your agent.

> [!NOTE]
> For centralized guidance on these steps, see [Tutorial: Build an end-to-end agentic retrieval solution](/azure/search/agentic-retrieval-how-to-create-pipeline).

---

## Relationship to Fabric IQ and Work IQ

Microsoft provides three IQ workloads that give agents access to different aspects of your organization:

+ [Fabric IQ](/fabric/iq/overview) is a semantic intelligence layer for Microsoft Fabric. It models business data (ontologies, semantic models, and graphs) so agents can reason over analytics in OneLake and Power BI.

+ [Work IQ](/microsoft-365-copilot/extensibility/workiq-overview) is a contextual intelligence layer for Microsoft 365. It captures collaboration signals from documents, meetings, chats, and workflows, providing agents with insight into how your organization operates.

+ [Foundry IQ](#capabilities) is a managed knowledge layer for enterprise data. It connects structured and unstructured data across Azure, SharePoint, OneLake, and the web so agents can access permission-aware knowledge.

Each IQ workload is standalone, but you can use them together to provide comprehensive organizational context for agents.

## Get started

+ [Watch this session](https://www.youtube.com/watch?v=slDdNIQCJBQ) for an introduction to Foundry IQ, and then [watch this video](https://www.youtube.com/watch?v=uDVkcZwB0EU) for a deep dive.

+ For minimum costs and proof-of-concept testing, start with the Microsoft Foundry (new) portal. You can use the free tier for Azure AI Search and a free allocation of tokens for agentic retrieval. [Watch this video](https://www.youtube.com/watch?v=bHL1jbWjJUc) for a quick demonstration of the portal.

+ Review application code in the [Azure OpenAI demo](/samples/azure-samples/azure-search-openai-demo/azure-search-openai-demo/), which uses agentic retrieval.
