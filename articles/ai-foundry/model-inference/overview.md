---
title: What is AI Foundry Models?
titleSuffix: Azure AI Foundry
description: Apply advanced language models to variety of use cases with Azure AI Foundry Models.
manager: scottpolly
author: msakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: concept-article
ms.date: 01/24/2025
ms.author: mopeak
ms.reviewer: fasantia
ms.custom: generated
recommendations: false
---

# What are Azure AI Foundry Models?

Foundry Models provide access to the most powerful models available in the industry. The models come from key model providers in the AI space, including OpenAI, Microsoft, Meta, Mistral, Cohere, G42, and AI21 Labs. These models can be integrated with software solutions to deliver a wide range of tasks that include content generation, summarization, image understanding, semantic search, and code generation.

AI Foundry Models provides a way to **consume models as APIs without hosting them on your infrastructure**. Models are hosted in a Microsoft-managed infrastructure, which enables API-based access to the model provider's model. API-based access can dramatically reduce the cost of accessing a model and simplify the provisioning experience.

AI Foundry Models is part of Azure AI Foundry, and users can access the service through [REST APIs](./reference/reference-model-inference-api.md), [SDKs in several languages](supported-languages.md) such as Python, C#, JavaScript, and Java. You can also use the AI Foundry Models from [Azure AI Foundry by configuring a connection](how-to/configure-project-connection.md).

## Models

You can get access to the key model providers in the industry. Explore the following model families available:

- [AI21 Labs](concepts/models.md#ai21-labs)
- [Azure OpenAI](concepts/models.md#azure-openai)
- [Cohere](concepts/models.md#cohere)
- [Core42](concepts/models.md#core42)
- [DeepSeek](concepts/models.md#deepseek)
- [Meta](concepts/models.md#meta)
- [Microsoft](concepts/models.md#microsoft)
- [Mistral AI](concepts/models.md#mistral-ai)
- [NTT Data](concepts/models.md#ntt-data)

To see details for each model including language, types, and capabilities, see [Models](concepts/models.md) article.

## Pricing

For models from non-Microsoft providers (for example, Meta AI and Mistral models), billing is through Azure Marketplace. For such models, you're required to subscribe to the particular model offering in accordance with the [Microsoft Commercial Marketplace Terms of Use](/legal/marketplace/marketplace-terms). Users accept license terms for use of the models. Pricing information for consumption is provided during deployment.

For Microsoft models (for example, Phi-3 models and Azure OpenAI models) billing is via Azure meters as First Party Consumption Services. As described in the [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), you purchase First Party Consumption Services by using Azure meters, but they aren't subject to Azure service terms.

> [!TIP]
> Learn how to [monitor and manage cost](how-to/manage-costs.md) in AI Foundry Models.

## Responsible AI

At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Generative models such as the ones available in Azure AI models have significant potential benefits, but without careful design and thoughtful mitigations, such models have the potential to generate incorrect or even harmful content. 

Microsoft helps guard against abuse and unintended harm by taking the following actions:

- Incorporating Microsoft's [principles for responsible AI use](https://www.microsoft.com/ai/responsible-ai)
- Adopting a [code of conduct](/legal/ai-code-of-conduct?context=/azure/ai-services/openai/context/context) for use of the service
- Building [content filters](/azure/ai-services/content-safety/overview) to support customers
- Providing responsible AI [information and guidance](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=image) that customers should consider when using Azure OpenAI.

## Getting started

You can get started with it the same way as any other Azure product where you [create and configure your resource for Azure AI Foundry (formerly known Azure AI Services)](how-to/quickstart-create-resources.md), or instance of the service, in your Azure Subscription. You can create as many resources as needed and configure them independently in case you have multiple teams with different requirements.

Once you create an Azure AI Foundry resource (formerly known Azure AI Services resource), you must deploy a model before you can start making API calls. By default, no models are available on it, so you can control which ones to start from. See the tutorial [Create your first AI Foundry Models deployment](how-to/create-model-deployments.md).

## Next steps

- [Create your first AI Foundry Models deployment](how-to/create-model-deployments.md)
