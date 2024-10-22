---
title: What is Azure AI model inference service in Azure AI Services?
titleSuffix: Azure AI Studio
description: Apply advanced language models to variety of use cases with Azure AI model inference in Azure AI Services
manager: nitinme
author: mrbullwinkle
ms.author: fasantia
ms.service: azure-ai-studio
ms.topic: overview
ms.date: 08/14/2024
ms.custom: ignite-2024, github-universe-2024
recommendations: false
---

# What is Azure AI model inference service in Azure AI Services?

Azure AI models inference service provides access to the most powerful models available in the [Azure AI model catalog](concepts/models.md). Coming from the key model providers in the industry including OpenAI, Microsoft, Meta, Mistral, Cohere, G42, and AI21 Labs; these models can be integrated with software solutions to deliver a wide range of tasks including content generation, summarization, image understanding, semantic search, and code generation.

The Azure AI model inference service in Azure AI Services provides a way to **consume models as APIs without hosting them on your infrastructure**. Models are hosted in a Microsoft-managed infrastructure, which enables API-based access to the model provider's model. API-based access can dramatically reduce the cost of accessing a model and simplify the provisioning experience.

## Models

You can get access to the key model providers in the industry including OpenAI, Microsoft, Meta, Mistral, Cohere, G42, and AI21 Labs. Model providers define the license terms and set the price for use of their models. The following list shows all the models available:

| Model provider | Models                                                                                                                                                                                                                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AI21 Labs      | - AI21-Jamba-1.5-Mini <br/> - AI21-Jamba-1.5-Large </br>                                                                                                                                                                                                                                         |
| Azure OpenAI   | - o1-preview ([Request Access](https://aka.ms/oai/modelaccess)) </br> - o1-mini ([Request Access](https://aka.ms/oai/modelaccess)) </br> - gpt-4o-mini </br> - gpt-4o </br> - text-embedding-3-small </br> - text-embedding-3-large </br>                                                        |
| Cohere         | - Cohere-command-r-plus-08-2024 </br> - Cohere-command-r-08-2024 </br> - Cohere-embed-v3-multilingual </br> - Cohere-embed-v3-english </br> - Cohere-command-r-plus </br> - Cohere-command-r </br>                                                                                               |
| Meta AI        | - Meta-Llama-3-8B-Instruct </br> - Meta-Llama-3-70B-Instruct </br> - Meta-Llama-3.1-8B-Instruct</br> - Meta-Llama-3.1-70B-Instruct </br> - Meta-Llama-3.1-405B-Instruct </br> - Llama-3.2-11B-Vision-Instruct </br> - Llama-3.2-90B-Vision-Instruct                                              |
| Mistral AI     | - Mistral-Small </br> - Mistral-Nemo </br> - Mistral-large </br> - Mistral-large-2407                                                                                                                                                                                                            |
| Microsoft      | - Phi-3-mini-4k-instruct </br> - Phi-3-medium-4k-instruct </br> - Phi-3-mini-128k-instruct </br> - Phi-3-medium-128k-instruct </br> - Phi-3-small-8k-instruct </br> - Phi-3-small-128k-instruct </br> - Phi-3.5-vision-instruct </br> - Phi-3.5-mini-instruct </br> - Phi-3.5-MoE-instruct </br> |

You can [decide and configure which models are available for inference](how-to/create-model-deployments.md) in the created resource. When a given model is configured, you can then generate predictions from it by indicating its model name or deployment name on your requests. No further changes are required in your code to use it.

To learn how to add models to the AI Services resource and use them read [Add and configure models to Azure AI Models in Azure AI Services](how-to/create-model-deployments.md).

## Pricing

Models that are offered by non-Microsoft providers (for example, Meta AI and Mistral models) are billed through the Azure Marketplace. For such models, you're required to subscribe to the particular model offering in accordance with the [Microsoft Commercial Marketplace Terms of Use](/legal/marketplace/marketplace-terms). Users accept license terms for use of the models. Pricing information for consumption is provided during deployment.

Models that are offered by Microsoft (for example, Phi-3 models and Azure OpenAI models) don't have this requirement, and they are billed via Azure meters as First Party Consumption Services. As described in the [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), you purchase First Party Consumption Services by using Azure meters, but they aren't subject to Azure service terms.

## Next steps

* [Create your first model deployment in Azure AI Services](how-to/create-model-deployments.md)