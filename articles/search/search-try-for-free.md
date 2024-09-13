---
title: 'Try Azure AI Search for free'
titleSuffix: Azure AI Search
description: Learn how to create a trial subscription and use credits for trying advanced features.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: conceptual
ms.date: 09/13/2024
---

# Try Azure AI Search for free

If you're new to Azure, you can set up a free trial subscription to explore the services at no charge. One of the Azure services you might want to try is Azure AI Search. Search is an expected component of any front-end app that's backed by content, and increasingly it's a critical component for generative search over content you own.

This article explains how to get the most value from your Azure trial subscription so that you can complete your evaluation of Azure AI Search quickly and efficiently.

## Sign up for a free subscription

To try Azure AI Search for free, [start a trial subscription](https://azure.microsoft.com/pricing/free-trial/?WT.mc_id=A261C142F). The trial subscription is non-renewable, active for one month, and comes with free credits so that you can create services at no charge. In the United States, the credit amount is $200. Equivalent credits are available in other currencies.

Although you can create a free search service that doesn't use up your credits, we recommend provisioning the **Basic** tier so that you can work with larger indexes, more indexes, and premium features like semantic ranking.

The [Azure portal](https://portal.azure.com/) is the easiest approach for first-time users who want to create and use Azure resources. You can access and manage all of your subscriptions and resources from the portal. For Azure AI Search, you can use the portal to build components for classic search scenarios and generative search (RAG) workloads.

## Start with a plan

Having a plan of action can help you get the most out of your trial subscription. For Azure AI Search, most newer customers and developers are exploring RAG patterns.

To evaluate Azure for [RAG scenarios](retrieval-augmented-generation-overview.md), you should have three or five Azure resources for:

- Storing data
- Deploying embedding and chat models
- Applying AI services for creating AI-generated content during indexing (optional)
- Adding information retrieval (**Azure AI Search**)
- Adding a frontend app (optional)

Many of our quickstarts and tutorials use Azure Storage, so we recommend creating an Azure Storage account for getting started.

Generative search requires embedding and chat models. The Azure cloud provides Azure OpenAI, but you can also use Azure AI Vision for multimodal embeddings (but not chat). Another model provider is Azure AI Studio and deploying chat and embedding models into the model catalog. However, for initial exploration, we recommend Azure OpenAI for its familiarity and mainstream offerings.

Application frontends are useful if you're prototyping a solution for a wider audience. You can use Azure Web apps or build an ASP.NET MVC application for this task. Otherwise, if you're working locally, you can view output in Jupyter notebooks in Visual Studio Code or another IDE. Or view results in console apps or other apps that run on localhost.

## Check regions

Azure AI Search has integrated operations with applied AI in the Azure cloud. Integration depends on services running within the same region. This is a requirement for data residency and for efficient operations.

Verifying region availability can save you time and frustration because you need to choose a region that supports all of the services you want to use.

Start here:

- [Azure AI Search region list](search-region-support.md). This list identifies region support for Azure AI Search, applied AI (Azure AI multiservice), and semantic ranking. You don't need a separate region check for applied AI.

  West Europe and West US 2/3 are currently at capacity for Azure AI Search and aren't accepting new search services.

Continue with the following links to review which regions also provide the model provider that you want to use.

- [Azure OpenAI region list](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)
- [Azure AI Vision region list](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability)
- [Azure AI Studio region list](/azure/ai-studio/reference/region-support)

> [!TIP]
> Currently, these regions provide the most overlap and capacity: **East US**, **East US2**, and **South Central** in the Americas; **France Central** or **Switzerland North** in Europe; **Australia East** in Asia Pacific.
>
> For Azure AI Vision and AI Search interoperability, choose one of these regions: **East US**, **France Central**, **Korea Central**, **North Europe**, **South East Asia**, or **West US**.

## Create services

1. [Create a search service](search-create-service-portal.md), choosing the Basic tier and a region that also offers a model provider. Most Azure AI Search regions provide higher capacity storage limits. There are just a few that have older and lower limits. For the Basic tier, as you install, confirm that you have a 15-GB partition.

1. [Create an Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal), choosing a general purpose account and using default settings.

1. [Create an Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource?pivots=web-portal) as your model provider.

1. [Create an Azure AI multiservice account](/azure/ai-services/multi-service-resource?pivots=azportal) to use applied AI in your indexing workloads and Azure AI Vision multimodal APIs as an embedding model provider. You can create and transform content during indexing if applied AI can be attached. For multimodal APIs, make sure you have chosen a region that provides those APIs. Look for this tile in the Azure Marketplace:

   :::image type="content" source="./media/search-try-for-free/azure-ai-service-marketplace.png" alt-text="Screenshot of the Azure AI Services offering in the Azure Marketplace.":::

## Estimate costs

During the trial period, you want to stay under the $200 credit allocation. Most services are pay-as-you-go, so you won't be charged while they're not in use, but an Azure AI Search service is provisioned on dedicated clusters and it can only be used by you. It's billable during its lifetime. If you provision a basic tier search service, expect Azure AI Search to consume about one third (or $70) of your available credits during the trial period.

During the trial period, the Azure portal provides a notification on the top right that tells you how many credits are used up and what remains. 

You can also monitor billing by searching for *subscriptions* in the Azure portal to view subscription information at any time. The Overview page gives you spending rates, forecasts, and cost management.

## Tips for getting the most value from your subscription

Try the portal quickstarts for Azure AI Search or quickstarts that use Visual Studio Code with REST or Python extensions.  It's the fastest approach creating searchable content, and you don't need coding skills to complete the tasks.

- [Quickstart: Vector search in the Azure portal](search-get-started-portal-import-vectors.md)
- [Quickstart: Image search in the Azure portal](search-get-started-portal-image-search.md)
- [Quickstart: Keyword in the Azure portal](search-get-started-portal.md)
- [Quickstart: Generative search (RAG) using a Python client](search-get-started-rag.md)
- [Quickstart: Vector search using a REST client](search-get-started-vector.md)

Azure AI Studio and Azure OpenAI Studio support connecting to content in Azure AI Search

- [Quickstart: Chat using your own data in Azure OpenAI Studio](/azure/ai-services/openai/use-your-data-quickstart)
- [Tutorial: Build a custom chat app with the prompt flow SDK](/azure/ai-studio/tutorials/copilot-sdk-create-resources)

Developers should review [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repository or the solution accelerators. You can deploy and run any of these samples using the Azure trial subscription. 

Many samples and [accelerators](resource-tools.md) come with bicep scripts that deploy all Azure resources and dependencies, so you can skip installation steps and explore an operational solution as soon as the development completes.

## Use the free tier

You can create a search service that doesn't consume credits. Here are some points about the free tier to keep in mind:

- You can have one free search service per Azure subscription.
- You can complete all of the quickstarts and most tutorials, except for those featuring semantic ranking and managed identities for Microsoft Entra ID authentication and authorization.
- Storage is capped at 50 MB.
- You can have up to three indexes, indexers, data sources, and skillset at one time. 

Review the [service limits](search-limits-quotas-capacity.md) for other constraints that apply to the free tier.

## Next steps

Sign up for an Azure trial subscription:

> [!div class="nextstepaction"]
> [Start your free trial subscription](https://azure.microsoft.com/pricing/free-trial/?WT.mc_id=A261C142F)

When you're ready, add Azure AI Search as your first resource:

> [!div class="nextstepaction"]
> [Create a search service](search-create-service-portal.md)
