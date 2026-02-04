---
title: Try for Free
titleSuffix: Azure AI Search
description: Learn how to start a trial subscription and use credits to try advanced Azure AI Search features.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 01/13/2026
ms.custom: references_regions
---

# Try Azure AI Search for free

If you're new to Azure, you can create an Azure free account to explore Azure AI Search and other services at no charge. The free account provides credits that you can use to create and test services for 30 days.

This article explains how to maximize the value of your Azure free account to quickly and efficiently evaluate Azure AI Search.

## Prerequisites

+ An internet connection and a supported web browser.
+ A phone number, credit or debit card, and Microsoft or GitHub account to create an Azure free account.

## Create an Azure free account

To try Azure AI Search for free, [sign up for an Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

The free account is active for 30 days and includes credits that allow you to create billable services at no charge. Currently, the credits are equivalent to USD200. This amount is subject to change, so verify the credit on the sign-up page.

## Choose a region

You can optionally integrate Azure AI Search with Foundry Tools for [AI enrichment](cognitive-search-concept-intro.md), [integrated vectorization](vector-search-integrated-vectorization.md), and [multimodal search](multimodal-search-overview.md). For billing purposes, you must [attach your Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md) to your search service via a keyless connection (preview) or key-based connection. Key-based connections require both services to be in the same region.

Before you create resources for a key-based connection, confirm regional support:

+ [**Azure AI Search regions**](search-region-support.md): The **AI enrichment** column indicates whether Azure AI Search and Microsoft Foundry are in the same region.

+ [**Azure Vision regions**](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability): The **Multimodal embeddings** column indicates regional support for the multimodal APIs that enable text and image vectorization. Azure Vision provides these APIs, which you access through a Microsoft Foundry resource. Ensure that Azure AI Search and Microsoft Foundry are in the same region as the multimodal APIs.

> [!TIP]
> If you don't need features powered by Foundry Tools, ignore the Azure Vision regions and choose an Azure AI Search region that provides the features and capacity you need.

## Choose a pricing tier

Azure AI Search offers several [pricing tiers](search-sku-tier.md), but only two tiers stay within the free account credit limits:

+ **Free** doesn't consume credits and provides 50 MB of storage. You can have one free search service per Azure subscription. This tier is always free and doesn't expire, even after your 30-day trial ends. However, it doesn't support semantic ranking or managed identities for Microsoft Entra ID authentication and authorization, which are commonly used in quickstarts.

+ **Basic** (recommended) consumes about one-third of your USD200 credits over 30 days and provides 15 GB of storage in most regions. This tier supports all features, including semantic ranking and managed identities, and runs on dedicated infrastructure for consistent performance.

> [!NOTE]
> Free search services that remain inactive for an extended period of time might be deleted to free up capacity, should the region be experiencing capacity constraints.

## Create resources

Most Azure AI Search scenarios require the following resources:

1. [Create an Azure AI Search service](search-create-service-portal.md). Choose the pricing tier that fits your needs and, if applicable, the same region as Microsoft Foundry. Most Azure AI Search regions provide higher-capacity storage limits. Only a few have older, lower limits. For the Basic tier, confirm that you have a 15-GB partition during service creation.

1. [Create an Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal) to index your own files. Choose a general purpose account and use the default settings.

1. [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource) to use AI enrichment in your indexing workloads and the Azure Vision multimodal APIs as an embedding model provider.

## Run a quickstart

To get started with Azure AI Search, try one of the following quickstarts:

+ Quickstart: Agentic retrieval ([portal](get-started-portal-agentic-retrieval.md) or [programmatic](search-get-started-agentic-retrieval.md))
+ Quickstart: Keyword search ([portal](search-get-started-portal.md) or [programmatic](search-get-started-text.md))
+ Quickstart: Vector search ([portal](search-get-started-portal-import-vectors.md) or [programmatic](search-get-started-vector.md))

You can also explore the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) GitHub repository or [solution accelerators](resource-tools.md). Many samples and accelerators include Bicep scripts that deploy all Azure resources and dependencies, allowing you to quickly explore operational solutions.

## Use a portal to explore features

You can access Azure AI Search through two portals, each optimized for different scenarios:

| Portal | Description | What you can do |
|--------|-------------|-----------------|
| [Azure portal](https://portal.azure.com/) | The primary management interface for Azure resources and your Azure AI Search service. **This portal is most useful for classic search scenarios and overall resource management.** | <ul><li>Create and configure your search service.</li><li>Build knowledge bases and knowledge sources for [agentic retrieval](search-what-is-azure-search.md#what-is-agentic-retrieval).</li><li>Build indexes, indexers, data sources, and skillsets for [classic search](search-what-is-azure-search.md#what-is-classic-search).</li><li>Query your knowledge bases and indexes.</li><li>Track credits and monitor costs.</li></ul> |
| [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) | A unified platform for deploying models and building AI applications. **This portal is most useful for agentic retrieval (RAG) scenarios.** | <ul><li>Deploy embedding and chat models.</li><li>Use [Foundry IQ](/azure/ai-foundry/agents/concepts/what-is-foundry-iq.md) to connect your Azure AI Search knowledge base to an AI agent.</li></ul> |

## Track your credit usage

During the trial period, you should stay under the USD200 credit allocation. Most services are on the Standard tier, so you aren't charged while they're not in use. However, an Azure AI Search service on the Basic tier is provisioned on dedicated clusters, so it's billable during its lifetime and can only be used by you. If you create a Basic search service, expect Azure AI Search to consume about one-third of your available credits during the trial period.

In the Azure portal, a notification in the upper-right corner shows how many credits have been used and how many remain. You can also monitor billing by searching for **Subscriptions** in the topmost search bar. The **Overview** page shows spending rates, forecasts, and cost management. For more information, see [Check usage of free services included with your Azure free account](/azure/cost-management-billing/manage/check-free-service-usage).

## Next step

Ready to move beyond exploration? After your free trial ends, learn how to [plan and manage capacity](search-capacity-planning.md) and [plan and manage costs](search-sku-manage-costs.md) for production workloads.
