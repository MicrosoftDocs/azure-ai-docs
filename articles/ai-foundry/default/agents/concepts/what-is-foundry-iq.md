---
title: What is Foundry IQ?
titleSuffix: Microsoft Foundry
description: Learn about Foundry IQ, the context engineering platform for agentic RAG that turns enterprise data into reusable, permission-aware knowledge bases for AI agents.
author: haileytap
ms.author: haileytapia
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 01/20/2026
ai-usage: ai-assisted
---

# Foundry IQ (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

Foundry IQ is Microsoft's context engineering platform that provides agents with a single endpoint for enterprise knowledge retrieval. It combines Azure AI Search for agentic retrieval, Azure OpenAI in Foundry Models for reasoning, and Foundry Agent Service for workflow orchestration.

At the heart of Foundry IQ is a *knowledge base*, which is a collection of knowledge sources that aggregate enterprise and web data. When an agent calls the knowledge base, Foundry IQ processes the query, retrieves relevant information, enforces user permissions, and returns a grounded response.

Use Foundry IQ when you want:

+ A single, reusable, configurable knowledge base for multiple agents.
+ Automatic handling of data ingestion, chunking, and vectorization.
+ Agentic retrieval that outperforms traditional retrieval-augmented generation (RAG) in response quality.
+ Permission-aware responses that enforce your organization's access controls.

## Benefits

Foundry IQ addresses three core challenges of building knowledge-equipped AI agents:

### Connect to enterprise knowledge

+ Create a knowledge base once, and then plug the knowledge base into multiple agents and applications.

+ Unify data access across Azure, SharePoint, OneLake, MCP servers, and the web. You can create multiple knowledge sources for a knowledge base.

+ Skip manual preprocessing for index-bound content. The automated indexing pipeline handles chunking and vectorization tuned per data type.

### Deliver quality answers

+ Get better answers without wasting tokens. The agentic retrieval engine plans, selects sources, searches, responds, and iterates automatically.

+ Achieve [36% better response quality](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-boost-response-relevance-by-36-with-agentic-retrieval/4470720) than traditional RAG engines in benchmark testing.

+ Adjust the retrieval reasoning effort to optimize for latency or quality. Let the system adapt automatically or fully customize your RAG stack.

+ Choose between answer synthesis (LLM-generated answers) and extractive data (verbatim content) to match your application requirements. For agent integration, use extractive data.

+ Handle indexed and remote data with multiple retrieval techniques, including keyword, vector, hybrid, and multimodal search.

### Enforce enterprise-grade security

+ Respect user permissions automatically. Document-level ACL synchronization and query-time trimming ensure agents retrieve only what each user is authorized to see.

+ Preserve end-to-end governance. Microsoft Purview sensitivity labels are extracted during indexing, enforced at query time, and preserved across supported knowledge sources.

+ Eliminate credential exposure. All queries run under each user's Microsoft Entra identity using managed identities.

## Architecture and components

Rather than a separate cloud service, Foundry IQ is a workflow that combines existing Azure and Microsoft Foundry resources:

| Resource | Role |
|--|--|
| [Azure AI Search](/azure/search/search-what-is-azure-search) | Provides knowledge bases, knowledge sources, indexing pipelines, and the agentic retrieval engine. The engine on your search service handles data access, scoring, iteration, and grounding. |
| [Azure OpenAI in Foundry Models](/azure/cognitive-services/openai/overview) | GPT-4 and GPT-5-series models perform optional query planning, reasoning, iterative retrieval, and answer synthesis. You can use any supported text embedding model for vectorization. |
| [Foundry Agent Service](/ai-foundry/default/agents/overview) | Hosts agents that call the knowledge base through a single retrieval API. |

Although Foundry IQ's agentic retrieval pipeline has native integrations with Foundry Agent Service, it's also available directly through the Azure AI Search REST APIs and Azure SDKs. This means you can use Foundry IQ knowledge bases with other agent frameworks, such as  LlamaIndex, LangChain, Semantic Kernel, AutoGen, and Haystack.

## Workflow

You can set up Foundry IQ through a portal or programmatically. The following steps outline the typical workflow for both approaches.

### [Portal](#tab/portal)

1. Sign in to the [Microsoft Foundry (new) portal](../../../what-is-foundry.md#microsoft-foundry-portals).

1. Create a project or select an existing project.

1. From the top menu, select **Build**.

1. On the **Knowledge** tab:
    1. Create or connect to an existing Azure AI Search service that supports agentic retrieval.
    1. Create a knowledge base by adding one knowledge source at a time.
    1. Configure knowledge base properties for retrieval behavior.

1. On the **Agents** tab:

   1. Create or select an existing agent.
   1. Connect to your knowledge base.
   1. (Optional) Add memory and guard rails.
   1. Use the playground to send messages and refine your agent.

> [!NOTE]
> + The playground provides a simplified workflow for proof-of-concept testing. When you move to code, configure managed identities and permissions to meet your organization's security requirements.
>
> + You can use the [Azure portal](/azure/search/get-started-portal-agentic-retrieval) to create knowledge bases and knowledge sources, but agent configuration and integration must be done in the Microsoft Foundry (new) portal or programmatically.

### [Programmatic](#tab/programmatic)

1. In Azure AI Search:

   1. Create a service that supports agentic retrieval.
   1. Enable role-based access and configure a managed identity for the service.

1. In Microsoft Foundry:

   1. Deploy a supported LLM (either GPT-4 or GPT-5) for query planning and reasoning during execution. Your agent can also use it for orchestration.
   1. Assign a role for your search service to access the deployed model.

1. In Azure AI Search:

   1. Create one or more knowledge sources.
   1. As part of knowledge source creation, satisfy the connection requirements for knowledge sources. For example, Azure AI Search needs read permissions to retrieve data.
   1. Create a knowledge base.

1. In Microsoft Foundry:

   1. Create an agent.
   1. Connect the agent to your knowledge base.
   1. (Optional) Add memory and guard rails.
   1. Test and refine your agent.

> [!NOTE]
> For centralized guidance on these steps, see [Tutorial: Build an end-to-end agentic retrieval solution using Azure AI Search](/azure/search/agentic-retrieval-how-to-create-pipeline).

---

## Relationship to Fabric IQ and Work IQ

To support enterprises in building agent-native systems, Microsoft provides an intelligence layer composed of three IQ workloads:

+ [Fabric IQ](/fabric/iq/overview) is a semantic intelligence layer for Microsoft Fabric. It models business data (ontologies, semantic models, and graphs) so agents can reason over analytics in OneLake and Power BI.

+ [Work IQ](/copilot/microsoft-365/microsoft-365-copilot-overview) is a contextual intelligence layer for Microsoft 365. It captures collaboration signals from documents, meetings, chats, and workflows, providing agents with insight into how your organization operates.

+ [Foundry IQ](#benefits) is a managed knowledge layer for enterprise data. It connects structured and unstructured data across Azure, SharePoint, OneLake, and the web so agents can access permission-aware knowledge.

Each IQ workload is standalone, but you can use them together to answer virtually any question from an AI agent or application.

## Availability and pricing

The availability of Foundry IQ depends on the availability of its underlying resources:

| Resource | Billing | Regions |
|--|--|--|
| Azure AI Search | Free and billable configurations <sup>1</sup> | [Regions supporting agentic retrieval](/azure/search/search-region-support) |
| Azure OpenAI in Foundry Models | [By usage](https://azure.microsoft.com//pricing/details/azure-ai-agent-service/) | [GPT-4 and GPT-5 regions](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?view=foundry-classic#model-summary-table-and-region-availability&preserve-view=true)  |
| Foundry Agent Service | No charge | [Regions supporting Foundry Agent Service](/azure/ai-foundry/reference/region-support?view=foundry-classic&preserve-view=true) |

<sup>1</sup> You enable [free agentic retrieval](/azure/search/agentic-retrieval-overview?tabs=quickstarts#availability-and-pricing) by using a free search service and the free allocation of tokens for agentic retrieval. A step up uses a [billable tier](/azure/search/search-sku-tier#tier-descriptions), such as Basic or Standard, and the free token allocation. For larger workloads, you need a billable tier and the [standard pricing plan](/azure/search/agentic-retrieval-overview?tabs=quickstarts#availability-and-pricing) for premium features.

## Get started

+ [Watch this session](https://www.youtube.com/watch?v=slDdNIQCJBQ) for an introduction to Foundry IQ, and then [watch this video](https://www.youtube.com/watch?v=uDVkcZwB0EU) for a deep dive.

+ For minimum costs and proof-of-concept testing, start with the Microsoft Foundry (new) portal. You can use the free tier for Azure AI Search and a free allocation of tokens for agentic retrieval. [Watch this video](https://www.youtube.com/watch?v=bHL1jbWjJUc) for a quick demonstration of the portal.

+ Review this tutorial: [Build an end-to-end agentic retrieval solution using Azure AI Search](/azure/search/agentic-retrieval-how-to-create-pipeline)

+ Review this how-to guide: [Connect a Foundry IQ knowledge base to Foundry Agent Service](/azure/ai-foundry/agents/how-to/tools/knowledge-retrieval)

+ Review application code in the [Azure OpenAI demo](/samples/azure-samples/azure-search-openai-demo/azure-search-openai-demo/), which has been updated to agentic retrieval. This programmatic solution includes the Foundry IQ components of Azure AI Search, Azure OpenAI in Foundry Models, and Foundry Agent Service.
