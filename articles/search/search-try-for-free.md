---
title: 'Try Azure AI Search for free'
titleSuffix: Azure AI Search
description: Learn how to create a trial subscription and use credits for trying advanced features.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: conceptual
ms.date: 01/15/2025
ms.custom: references_regions
---

# Try Azure AI Search for free

If you're new to Azure, you can set up a free trial subscription to explore Azure AI Search and other services at no charge. Information retrieval over your own content is useful for many scenarios including AI generative search.

This article explains how to get the most value from your Azure trial subscription so that you can complete your evaluation of Azure AI Search quickly and efficiently.

## Step one: Sign up for a free subscription

To try Azure AI Search for free, [start a trial subscription](https://azure.microsoft.com/pricing/free-trial/?WT.mc_id=A261C142F). The trial subscription is nonrenewable, active for one month, and comes with free credits so that you can create billable services at no charge. 

At this point in time, the credit is equivalent to USD 200. As always, the exact amount is subject to change, but you can verify the credit on the trial subscription sign-up page.

> [!div class="nextstepaction"]
> [Start your free trial subscription](https://azure.microsoft.com/pricing/free-trial/?WT.mc_id=A261C142F)

Once you sign up, you can immediately use either of these links to access Azure resources and experiences:

+ [Sign in to Azure portal](https://portal.azure.com/) to view, manage, and create more resources. You can also use the Azure portal to track your credits and projected costs.

+ [Sign in to Azure AI Foundry](https://ai.azure.com) for a no-code approach to deploying models on Azure OpenAI and using Azure AI Search for information retrieval. **We recommend you start here first.**

## Step two: "Day One" tasks

[**How to build and consume vector indexes in Azure AI Foundry portal**](/azure/ai-foundry/how-to/index-add) is a great place to start.

1. [Sign in to Azure AI Foundry](https://ai.azure.com).

1. Create a new hub and project.

1. On the left, under **Components**, select **Indexes**. The Create Index wizard guides you through the remaining tasks.

   + On the **Source Data** page, if you have local files that you want to query using an LLM, upload them. 

   + On the **Index Settings**, you can create a new Azure AI Search service. The wizard selects a matching region automatically, but you choose the pricing tier.

     We recommend Basic for larger data files and more indexes, or Free if your files are less than 50 MB. Basic has more features and storage, but it's billable for the lifetime of the service and it might consume about one third of your available credits if you retain it for the entire trial period.

> [!TIP]
> Azure AI Search and Azure OpenAI must be in the [same region](search-create-service-portal.md#regions-with-the-most-overlap).

## Step three: Have a plan for next steps

The trial period can go by quick. Having a plan of action can help you get the most out of your trial subscription. For Azure AI Search, most newer customers and developers are exploring RAG patterns.

For a next step evaluation of [RAG scenarios](retrieval-augmented-generation-overview.md), you should have three or five Azure resources for:

- Storing data
- Deploying embedding and chat models (**Azure OpenAI**)
- Applying AI services for creating AI-generated content during indexing (optional)
- Adding information retrieval (**Azure AI Search**)
- Adding a frontend app (optional)

Many of our quickstarts and tutorials use Azure Storage, so we recommend creating an Azure Storage account for getting started.

Generative search requires embedding and chat models. The Azure cloud provides Azure OpenAI, but you can also use Azure AI Vision for multimodal embeddings (but not chat). Another model provider is Azure AI Foundry and deploying chat and embedding models into the model catalog. However, for initial exploration, we recommend Azure OpenAI for its familiarity and mainstream offerings.

Application frontends are useful if you're prototyping a solution for a wider audience. You can use Azure Web apps or build an ASP.NET MVC application for this task. Otherwise, if you're working locally, you can view output in Jupyter notebooks in Visual Studio Code or another IDE. Or view results in console apps or other apps that run on localhost.

## Check regions

Azure AI Search has integrated operations with applied AI in the Azure cloud. Integration depends on services running within the same region. This is a requirement for data residency and for efficient operations.

Verifying region availability can save you time and frustration because you need to choose a region that supports all of the services you want to use.

Start here if you want to use built-in vectorization or chat models:

- [Azure OpenAI region list](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)
- [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability)
- [Azure AI Foundry region list](/azure/ai-foundry/reference/region-support)

Continue with the following link to confirm region and tier availability for AI Search:

- [Azure AI Search region list](search-region-support.md). This list identifies region support for Azure AI Search, applied AI (Azure AI services multi-service), and semantic ranking. You don't need a separate region check for applied AI.

> [!TIP]
> Currently, these regions provide the most overlap and capacity: **East US**, **East US2**, **Central US​​**, and **South Central** in the Americas; **UK South** or **Switzerland North** in Europe; **Australia East** in Asia Pacific.
>
> For Azure AI Vision and AI Search interoperability, choose one of these regions: **East US**, **West US**, **Switzerland North**, **Korea Central**, **South East Asia**, or **Australia East**.

### Create services

1. [Create a search service](search-create-service-portal.md) if you don't have one already, choosing the Basic tier and a region that also offers a model provider. Most Azure AI Search regions provide higher capacity storage limits. There are just a few that have older and lower limits. For the Basic tier, as you install, confirm that you have a 15-GB partition.

   > [!div class="nextstepaction"]
   > [Create a search service](search-create-service-portal.md)

1. [Create an Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal), choosing a general purpose account and using default settings.

1. [Create an Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource?pivots=web-portal) as your model provider.

1. [Create an Azure AI services multi-service account](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills?pivots=azportal) to use applied AI in your indexing workloads and Azure AI Vision multimodal APIs as an embedding model provider. You can create and transform content during indexing if applied AI can be attached. For multimodal APIs, make sure you choose a region that provides those APIs. Look for this tile in Azure Marketplace:

   :::image type="content" source="./media/search-try-for-free/azure-ai-service-marketplace.png" alt-text="Screenshot of the Azure AI Services offering in Azure Marketplace.":::

### Try the quickstarts

Try the Azure portal quickstarts for Azure AI Search or quickstarts that use Visual Studio Code with REST or Python extensions.  It's the fastest approach creating searchable content, and you don't need coding skills to complete the tasks.

- [Quickstart: Vector search in the Azure portal](search-get-started-portal-import-vectors.md)
- [Quickstart: Image search in the Azure portal](search-get-started-portal-image-search.md)
- [Quickstart: Keyword in the Azure portal](search-get-started-portal.md)
- [Quickstart: Generative search (RAG) using a Python client](search-get-started-rag.md)
- [Quickstart: Vector search using a REST client](search-get-started-vector.md)

Azure AI Foundry supports connecting to content in Azure AI Search.

- [Quickstart: Chat using your own data with Azure OpenAI](/azure/ai-services/openai/use-your-data-quickstart)
- [Tutorial: Build a custom chat app with the prompt flow SDK](/azure/ai-foundry/tutorials/copilot-sdk-create-resources)

Developers should review [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repository or the solution accelerators. You can deploy and run any of these samples using the Azure trial subscription. 

Many samples and [accelerators](resource-tools.md) come with bicep scripts that deploy all Azure resources and dependencies, so you can skip installation steps and explore an operational solution as soon as the development completes.

## Step four: Track your credits 

During the trial period, you want to stay under the USD 200 credit allocation. Most services are Standard, so you won't be charged while they're not in use, but an Azure AI Search service on the Basic tier is provisioned on dedicated clusters and it can only be used by you. It's billable during its lifetime. If you provision a basic tier search service, expect Azure AI Search to consume about one third of your available credits during the trial period.

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

Sign up for an Azure trial subscription:

> [!div class="nextstepaction"]
> [Start your free trial subscription](https://azure.microsoft.com/pricing/free-trial/?WT.mc_id=A261C142F)

When you're ready, add Azure AI Search as your first resource:

> [!div class="nextstepaction"]
> [Create a search service](search-create-service-portal.md)
