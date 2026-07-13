---
title: "Tutorial: Deploy Private Agentic Retrieval"
titleSuffix: Foundry IQ
description: Review the tutorial scope and end-to-end architecture for private agentic retrieval.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: tutorial
ms.date: 07/13/2026
author: haileytap
ms.author: haileytapia
ms.reviewer: magottei
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#customer intent: As a platform engineer, I want a single private retrieval tutorial sequence so that I can validate networking and retrieval behavior in a predictable order.
---

# Tutorial: Deploy private agentic retrieval for Foundry IQ

> [!IMPORTANT]
> This tutorial series uses the 2026-05-01-preview REST API for agentic retrieval. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

This three-part tutorial series describes how to deploy an end-to-end private agentic retrieval architecture for Foundry IQ by using Microsoft Foundry and Azure AI Search. It explains how inbound connectivity, outbound dependencies, and retrieval runtime fit together across the deployment.

In this tutorial, you:

> [!div class="checklist"]
> * Establish inbound private connectivity between Foundry and Azure AI Search.
> * Configure outbound private dependencies from Azure AI Search.
> * Validate end-to-end retrieval with a knowledge source, knowledge base, project connection, and agent.

## What is private agentic retrieval?

Private agentic retrieval is a pattern where an agent retrieves knowledge over private network paths instead of public endpoints. In this tutorial, the agent-to-Search path and the Search-to-Storage path stay on private endpoints, shared private links, and private DNS zones. The Search-to-Foundry embedding dependency is also configured for private outbound access, but the ingestion-time embedding call currently still relies on the Foundry trusted-service bypass.

> [!TIP]
> This tutorial is the private network version of [Tutorial: Build an end-to-end agentic retrieval solution using Azure AI Search](/azure/search/agentic-retrieval-how-to-create-pipeline). Both tutorials use managed identities and role-based access, but this version emphasizes private connectivity and adds inbound and outbound validation at each step.

## Services in this tutorial

The deployment provisions the following services. You interact with each service differently throughout this tutorial.

| Service | Role |
| --- | --- |
| Foundry (resource and project) | Orchestrates the agent runtime and hosts the project connection, the agent, and a GPT-5 family model that powers the agent. In part three, you also deploy the `text-embedding-3-large` embedding model that Azure AI Search uses to vectorize content. |
| Azure AI Search | Ingests and vectorizes your private blob content into a knowledge source, and then serves agentic retrieval through a knowledge base and its MCP endpoint. Makes a private outbound call to Azure Blob Storage for content access. For the Foundry embedding dependency, this tutorial uses the `openai_account` shared private link for the target resource, and the ingestion-time embedding call currently also relies on the trusted-service bypass. |
| Azure Blob Storage | Stores the source documents that the knowledge source ingests and indexes for agentic retrieval. |
| Azure Cosmos DB | Stores agent state for the standard agent setup, including messages, conversation history, and agent metadata. The deployment provisions it automatically, and you don't configure or use it directly. |

## Parts in this tutorial

The following table shows what you accomplish in each part, the components involved, and how to confirm success before moving to the next part.

| Part | Outcome | Components | Success criteria |
| --- | --- | --- | --- |
| 1 - Inbound | A private request path from Foundry to Azure AI Search. | <ul><li>Virtual network and subnets</li><li>Private endpoints</li><li>Private DNS zones</li><li>Foundry and Azure AI Search private access settings</li></ul> | From your in-VNet client, the Foundry and Azure AI Search endpoints resolve to private IP addresses and accept connections on TCP 443. |
| 2 - Outbound | Private dependency paths from Azure AI Search to Azure Blob Storage and Foundry. | <ul><li>Shared private links</li><li>Target-side approvals</li><li>Managed identities</li><li>Dependency RBAC for Azure Blob Storage and Foundry</li></ul> | The Azure Blob Storage and Foundry shared private links report an `Approved` state, and the Azure AI Search managed identity holds its assigned blob and model roles. |
| 3 - Retrieval validation | An agent that returns grounded answers over the private retrieval path. | <ul><li>Knowledge source</li><li>Knowledge base</li><li>Project connection</li><li>Agent configuration</li></ul> | The validation prompt returns an answer grounded in your blob content, with citations to the source documents. |

## Next step

> [!div class="nextstepaction"]
> [Set up private inbound connectivity](foundry-iq-tutorial-private-inbound.md)
