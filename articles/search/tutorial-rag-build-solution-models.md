---
title: 'RAG tutorial: Set up models'
titleSuffix: Azure AI Search
description: Set up an embedding model and chat model for generative search (RAG).
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: tutorial
ms.custom: references_regions
ms.date: 05/29/2025

---

# Tutorial: Choose embedding and chat models for RAG in Azure AI Search

A RAG solution built on Azure AI Search takes a dependency on embedding models for vectorization, and on chat completion models for conversational search over your data.

In this tutorial, you:

> [!div class="checklist"]
> - Learn about the Azure models supported for built-in vectorization
> - Learn about the Azure models supported for chat completion
> - Deploy models and collect model information for your code
> - Configure search engine access to Azure models
> - Learn about custom skills and vectorizers for attaching non-Azure models

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

## Prerequisites

- The Azure portal, used to deploy models and configure role assignments in the Azure cloud.

- An **Owner** or **User Access Administrator** role on your Azure subscription, necessary for creating role assignments. You use at least three Azure resources in this tutorial. The connections are authenticated using Microsoft Entra ID, which requires the ability to create roles. Role assignments for connecting to models are documented in this article. If you can't create roles, you can use [API keys](search-security-api-keys.md) instead.

- A model provider, such as [Azure OpenAI](/azure/ai-services/openai/how-to/create-resource), Azure AI Vision via an [Azure AI services multi-service resource](/azure/ai-services/multi-service-resource#azure-ai-services-resource-for-azure-ai-search-skills), or [Azure AI Foundry](https://ai.azure.com/).

  We use Azure OpenAI in this tutorial. Other providers are listed so that you know your options for integrated vectorization.

- Azure AI Search, Basic tier or higher provides a [managed identity](search-howto-managed-identities-data-sources.md) used in role assignments. 

- A shared region. To complete all of the tutorials in this series, the region must support both Azure AI Search and the model provider. See supported regions for:

  - [Azure OpenAI regions](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)

  - [Azure AI Vision regions](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability)

  - [Azure AI Foundry regions](/azure/ai-foundry/reference/region-support)

  - [Azure AI Search regions](search-region-support.md)

## Review models supporting built-in vectorization

Vectorized content improves the query results in a RAG solution. Azure AI Search supports a built-in vectorization action in an indexing pipeline. It also supports vectorization at query time, converting text or image inputs into embeddings for a vector search. In this step, identify an embedding model that works for your content and queries. If you're providing raw vector data and raw vector queries, or if your RAG solution doesn't include vector data, skip this step.

Vector queries that include a text-to-vector conversion step must use the same embedding model that was used during indexing. The search engine doesn't throw an error if you use different models, but you get poor results.

To meet the same-model requirement, choose embedding models that can be referenced through *skills* during indexing and through *vectorizers* during query execution. The following table lists the skill and vectorizer pairs. To see how the embedding models are used, skip ahead to [Create an indexing pipeline](tutorial-rag-build-solution-pipeline.md) for code that calls an embedding skill and a matching vectorizer. 

Azure AI Search provides skill and vectorizer support for the following embedding models in the Azure cloud.

| Client | Embedding models | Skill | Vectorizer |
|--------|------------------|-------|------------|
| Azure OpenAI | text-embedding-ada-002, <br>text-embedding-3-large, <br>text-embedding-3-small | [AzureOpenAIEmbedding](cognitive-search-skill-azure-openai-embedding.md) | [AzureOpenAIEmbedding](vector-search-vectorizer-azure-open-ai.md) |
| Azure AI Vision | multimodal 4.0 <sup>1</sup> | [AzureAIVision](cognitive-search-skill-vision-vectorize.md) | [AzureAIVision](vector-search-vectorizer-ai-services-vision.md) |
| Azure AI Foundry model catalog | Facebook-DinoV2-Image-Embeddings-ViT-Base, <br>Facebook-DinoV2-Image-Embeddings-ViT-Giant, <br>Cohere-embed-v3-english, <br>Cohere-embed-v3-multilingual | [AML](cognitive-search-aml-skill.md) <sup>2</sup>  | [Azure AI Foundry model catalog](vector-search-vectorizer-azure-machine-learning-ai-studio-catalog.md) |

<sup>1</sup> Supports image and text vectorization.

<sup>2</sup> Deployed models in the model catalog are accessed over an AML endpoint. We use the existing AML skill for this connection.

You can use other models besides the ones listed here. For more information, see [Use non-Azure models for embeddings](#use-non-azure-models-for-embeddings) in this article.

> [!NOTE]
> Inputs to an embedding models are typically chunked data. In an Azure AI Search RAG pattern, chunking is handled in the indexer pipeline, covered in [another tutorial](tutorial-rag-build-solution-pipeline.md) in this series.

## Review models used for generative AI at query time

Azure AI Search doesn't have integration code for chat models, so you should choose an LLM that you're familiar with and that meets your requirements. You can modify query code to try different models without having to rebuild an index or rerun any part of the indexing pipeline. Review [Search and generate answers](tutorial-rag-build-solution-query.md) for code that calls the chat model.

The following models are commonly used for a chat search experience:

| Client | Chat models |
|--------|------------|
| Azure OpenAI | GPT-35-Turbo, <br>GPT-4, <br>GPT-4o, <br>GPT-4 Turbo |

GPT-35-Turbo and GPT-4 models are optimized to work with inputs formatted as a conversation.

We use GPT-4o in this tutorial. During testing, we found that it's less likely to supplement with its own training data. For example, given the query "how much of the earth is covered by water?", GPT-35-Turbo answered using its built-in knowledge of earth to state that 71% of the earth is covered by water, even though the sample data doesn't provide that fact. In contrast, GPT-4o responded (correctly) with "I don't know".

## Deploy models and collect information

Models must be deployed and accessible through an endpoint. Both embedding-related skills and vectorizers need the number of dimensions and the model name. 

This tutorial series uses the following models and model providers:

- Text-embedding-3-large on Azure OpenAI for embeddings
- GPT-4o on Azure OpenAI for chat completion

You must have [**Cognitive Services OpenAI Contributor**]( /azure/ai-services/openai/how-to/role-based-access-control#cognitive-services-openai-contributor) or higher to deploy models in Azure OpenAI.

1. Go to [Azure AI Foundry](https://ai.azure.com/).

1. Select **Deployments** on the left menu.

1. Select **Deploy model** > **Deploy base model**.

1. Select **text-embedding-3-large** from the dropdown list and confirm the selection.

1. Specify a deployment name. We recommend "text-embedding-3-large".

1. Accept the defaults.

1. Select **Deploy**.

1. Repeat the previous steps for **gpt-4o**.

1. Make a note of the model names and endpoint. Embedding skills and vectorizers assemble the full endpoint internally, so you only need the resource URI. For example, given `https://MY-FAKE-ACCOUNT.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2024-06-01`, the endpoint you should provide in skill and vectorizer definitions is `https://MY-FAKE-ACCOUNT.openai.azure.com`.

## Configure search engine access to Azure models

For pipeline and query execution, this tutorial uses Microsoft Entra ID for authentication and roles for authorization. 

Assign yourself and the search service identity permissions on Azure OpenAI. The code for this tutorial runs locally. Requests to Azure OpenAI originate from your system. Also, search results from the search engine are passed to Azure OpenAI. For these reasons, both you and the search service need permissions on Azure OpenAI.

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. Configure Azure AI Search to [use a system-managed identity](search-howto-managed-identities-data-sources.md).

1. Find your Azure OpenAI resource.

1. Select **Access control (IAM)** on the left menu. 

1. Select **Add role assignment**.

1. Select [**Cognitive Services OpenAI User**](/azure/ai-services/openai/how-to/role-based-access-control#cognitive-services-openai-userpermissions).

1. Select **Managed identity** and then select **Members**. Find the system-managed identity for your search service in the dropdown list.

1. Next, select **User, group, or service principal** and then select **Members**. Search for your user account and then select it from the dropdown list.

1. Make sure you have two security principals assigned to the role.

1. Select **Review and Assign** to create the role assignments.

For access to models on Azure AI Vision, assign **Cognitive Services OpenAI User**. For Azure AI Foundry, assign **Azure AI Developer**.

## Use non-Azure models for embeddings

The pattern for integrating any embedding model is to wrap it in a custom skill and custom vectorizer. This section provides links to reference articles. For a code example that calls a non-Azure model, see [custom-embeddings demo](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/custom-vectorizer/readme.md).

| Client | Embedding models | Skill | Vectorizer |
|--------|------------------|-------|------------|
| Any | Any | [custom skill](cognitive-search-custom-skill-web-api.md) | [custom vectorizer](vector-search-vectorizer-custom-web-api.md) |

<!-- In this tutorial,  Learn how to set up connections so that Azure AI Search can connect securely during indexing, and at query time for generative AI responses and text-to-vector conversions of query strings.

Objective:

- Identify an embedding model and chat model for your RAG workflow.

Key points:

- Built-in integration for models hosted in the Azure cloud.
- For chunking, use the native Text Split skill with overlapping text -- or -- for semantic chunking, use Document Intelligence.
- For embedding during indexing, use a skill that points to Azure OpenAI, Azure AI Vision, or the model catalog. Alternatively, use custom skill with HTTP endpoint to external model.
- For queries, same embedding models as above, but you're wrapping it in a "vectorizer" instead of a "skill".
- Use the same embedding model for indexing and text-to-vector queries. If you want to try a different model, it's a rebuild. An indexer pipeline like the one used in this tutorial makes this step easy.
- For chat, same location requirements and providers, except no Azure AI Vision. You specify a chat model in your query logic. Unlike embedding, you can swap these around at query time to see what they do.

Tasks:

- H2: Identify the models for which we have skills/vectorizers and provide locations (model catalog, Azure OpenAI, etc). Crosslink to model deployment instructions. Include steps for getting endpoints, model version, deployment name, REST API version.
- H2: How to use other models (create a custom skill, create a custom vectorizer).
- H2: How to configure access. Set up an Azure AI Search managed identity, give it permissions on Azure-hosted models. -->

## Next step

> [!div class="nextstepaction"]
> [Design an index](tutorial-rag-build-solution-index-schema.md)