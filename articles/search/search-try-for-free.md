---
title: 'Try Azure AI Search for free'
titleSuffix: Azure AI Search
description: Learn how to create a trial subscription and use credits for trying advanced features.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: conceptual
ms.date: 11/06/2025
ms.custom: references_regions
---

# Try Azure AI Search for free

If you're new to Azure, you can set up an Azure free account to explore Azure AI Search and other services at no charge. Information retrieval over your own content is useful for many scenarios including AI generative search.

This article explains how to get the most value from your Azure free account so that you can complete your evaluation of Azure AI Search quickly and efficiently.

## Step one: Sign up for an Azure free account

To try Azure AI Search for free, [sign up for an Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). The free account is active for 30 days, and comes with free credits so that you can create billable services at no charge.

Currently, the credit is equivalent to USD 200. The exact amount is subject to change, and you can verify the credit on the Azure sign-up page.

> [!div class="nextstepaction"]
> [Try Azure for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

After you sign up, you can immediately use either of these links to access Azure resources and experiences:

+ [Sign in to Azure portal](https://portal.azure.com/) to view, manage, and create more resources. You can also use the Azure portal to track your credits and projected costs.

+ [Sign in to the Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) for a no-code approach to deploying models on Azure OpenAI and using Azure AI Search for information retrieval. **We recommend you start here first.**

## Step two: "Day One" tasks

In the Foundry (new) portal, you can create an end-to-end solution that integrates Azure AI Search and Foundry Agent Service for knowledge retrieval.

The portal supports creating *knowledge sources* that map to your indexed content in Azure AI Search and *knowledge bases* that orchestrate retrieval operations, including query decomposition, hybrid search, and result reranking. You can then configure a Foundry agent to use this knowledge base as a Model Context Protocol (MCP) tool, allowing the agent to retrieve relevant information and provide grounded, citation-backed responses.

For more information about the programmatic experience, see [Connect a Foundry IQ knowledge base to Foundry Agent Service](/azure/ai-foundry/agents/how-to/tools/knowledge-retrieval).

## Step three: Have a plan for next steps

The trial period can go by quick. Having a plan of action can help you get the most out of your trial subscription. For Azure AI Search, most newer customers and developers are exploring RAG patterns.

For a next step evaluation of [RAG scenarios](retrieval-augmented-generation-overview.md), you should have three or five Azure resources for:

- Storing data
- Deploying embedding and chat models (**Azure OpenAI**)
- Applying Foundry Tools for creating AI-generated content during indexing (optional)
- Adding information retrieval (**Azure AI Search**)
- Adding a frontend app (optional)

Many of our quickstarts and tutorials use Azure Storage, so we recommend creating an Azure Storage account for getting started.

Generative search requires embedding and chat models. The Azure cloud provides Azure OpenAI, but you can also use Azure Vision in Foundry Tools for multimodal embeddings (but not chat). Another model provider is Foundry and deploying chat and embedding models into the model catalog. However, for initial exploration, we recommend Azure OpenAI for its familiarity and mainstream offerings.

Application frontends are useful if you're prototyping a solution for a wider audience. You can use Azure Web apps or build an ASP.NET MVC application for this task. Otherwise, if you're working locally, you can view output in Jupyter notebooks in Visual Studio Code or another IDE. Or view results in console apps or other apps that run on localhost.

## Check regions

Azure AI Search offers integrated operations with applied AI in the Azure cloud. For data residency and efficient operations, integration typically depends on services running within the same region.

> [!NOTE]
> The same-region requirement doesn't apply to Azure OpenAI and Foundry for interoperability with Azure AI Search. However, using the same region can improve performance and reduce latency.

For [AI enrichment](cognitive-search-concept-intro.md), [integrated vectorization](vector-search-integrated-vectorization.md), and [multimodal search](multimodal-search-overview.md) powered by Foundry Tools, you must create Azure AI Search and Foundry in the same region. This is required for [billing purposes](cognitive-search-attach-cognitive-services.md).

Before you create these resources:

+ Check [Azure AI Search regions](search-region-support.md). The **AI enrichment** column indicates whether Azure AI Search and Foundry are in the same region.

+ Check [Azure Vision regions](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability). The **Multimodal embeddings** column indicates regional support for the multimodal APIs that enable text and image vectorization. Azure Vision provides these APIs, which you access through a Foundry resource. Ensure that your search service and Foundry resource are in the same region as the multimodal APIs.

### Create services

1. [Create a search service](search-create-service-portal.md) if you don't have one already. Choose the Basic tier and, if applicable, the same region as Foundry. Most Azure AI Search regions provide higher capacity storage limits. There are just a few that have older and lower limits. For the Basic tier, as you install, confirm that you have a 15-GB partition.

   > [!div class="nextstepaction"]
   > [Create a search service](search-create-service-portal.md)

1. [Create an Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal). Choose a general purpose account and use default settings.

1. [Create an Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource?pivots=web-portal).

1. [Create a Foundry resource](/azure/ai-services/multi-service-resource) to use applied AI in your indexing workloads and Azure Vision multimodal APIs as an embedding model provider. You can create and transform content during indexing if applied AI can be attached. For multimodal APIs, make sure you choose a region that provides those APIs. Look for this tile in Azure Marketplace:

### Try the quickstarts

Try the Azure portal quickstarts for Azure AI Search or quickstarts that use Visual Studio Code with REST or Python extensions.  It's the fastest approach creating searchable content, and you don't need coding skills to complete the tasks.

- [Quickstart: Vector search in the Azure portal](search-get-started-portal-import-vectors.md)
- [Quickstart: Image search in the Azure portal](search-get-started-portal-image-search.md)
- [Quickstart: Keyword in the Azure portal](search-get-started-portal.md)
- [Quickstart: Agentic retrieval](search-get-started-agentic-retrieval.md)
- [Quickstart: Vector search using a REST client](search-get-started-vector.md)

Foundry supports connecting to content in Azure AI Search.

- [Quickstart: Chat using your own data with Azure OpenAI](/azure/ai-services/openai/use-your-data-quickstart)
- [Tutorial: Build a custom chat app with the prompt flow SDK](/azure/ai-foundry/tutorials/copilot-sdk-create-resources)

Developers should review [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repository or the solution accelerators. You can deploy and run any of these samples using the Azure trial subscription. 

Many samples and [accelerators](resource-tools.md) come with bicep scripts that deploy all Azure resources and dependencies, so you can skip installation steps and explore an operational solution as soon as the development completes.

## Step four: Track your credits 

During the trial period, you want to stay under the USD 200 credit allocation. Most services are Standard, so you won't be charged while they're not in use, but an Azure AI Search service on the Basic tier is provisioned on dedicated clusters and it can only be used by you. It's billable during its lifetime. If you provision a basic search service, expect Azure AI Search to consume about one third of your available credits during the trial period.

During the trial period, the Azure portal provides a notification on the top right that tells you how many credits are used up and what remains. 

You can also monitor billing by searching for *subscriptions* in the Azure portal to view subscription information at any time. The Overview page gives you spending rates, forecasts, and cost management. For more information, see [Check usage of free services included with your Azure free account](/azure/cost-management-billing/manage/check-free-service-usage).

## Consider the free tier

You can create a search service that doesn't consume credits. Here are some points about the free tier to keep in mind:

+ You can have one free search service per Azure subscription.
+ You can complete all of the quickstarts and most tutorials, except for those featuring semantic ranking and managed identities for Microsoft Entra ID authentication and authorization.
+ Storage is capped at 50 MB.
+ You can have up to three indexes, indexers, data sources, and skillset at one time.

Review the [service limits](search-limits-quotas-capacity.md) for other constraints that apply to the free tier.

> [!NOTE]
> Free services that remain inactive for an extended period of time might be deleted to free up capacity if the region is under capacity constraints.

## Next steps

Sign up for an Azure free account:

> [!div class="nextstepaction"]
> [Try Azure for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

When you're ready, add Azure AI Search as your first resource:

> [!div class="nextstepaction"]
> [Create a search service](search-create-service-portal.md)
