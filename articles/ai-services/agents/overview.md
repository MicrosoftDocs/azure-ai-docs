---
title: What is Azure AI Agent Service?
titleSuffix: Azure AI services
description: Learn how to create agents that leverage advanced language models for workflow automation.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: overview
ms.date: 11/13/2024
recommendations: false
---

# What is Azure AI Agent Service?

Azure AI Agent Service is a fully managed service designed to empower developers to securely build, deploy, and scale high-quality, and extensible AI agents. Leveraging an extensive ecosystem of models tools and capabilities from OpenAI, Microsoft, and other non-Microsoft providers, Azure AI Agent Service enables you to build agents for a wide range of generative AI use cases. Users can access the service through REST APIs, SDKs, or in the [Azure AI Foundry](https://ai.azure.com).

### Features overview

**Use OpenAI models and non-OpenAI models** - Create agents that leverage OpenAI models, or others such as Llama 3, Mistral and Cohere. 

**Extensive data integrations** - Ground your AI agents with relevant, secure enterprise knowledge from various data sources, such as Microsoft Bing, Microsoft SharePoint, Microsoft Fabric, Azure AI Search, and third-party APIs. 

## Responsible AI

At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Generative models such as the ones available in Azure OpenAI have significant potential benefits, but without careful design and thoughtful mitigations, such models have the potential to generate incorrect or even harmful content. Microsoft has made significant investments to help guard against abuse and unintended harm, which includes incorporating Microsoft’s <a href="https://www.microsoft.com/ai/responsible-ai?activetab=pivot1:primaryr6" target="_blank">principles for responsible AI use</a>, adopting a [Code of Conduct](/legal/cognitive-services/openai/code-of-conduct?context=/azure/ai-services/openai/context/context) for use of the service, building [content filters](/azure/ai-services/content-safety/overview) to support customers, and providing responsible AI [information and guidance](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=image) that customers should consider when using Azure AI Agent Service.

## Get started with Azure AI Agent Service

To get started with Azure AI Agent Service, you need to create an Azure AI Foundry hub and an Agent project in your Azure subscription. 

Start with the [quickstart](./quickstart.md) guide if it's your first time using the service.
1. You can create a hub and project with the required resources via Azure portal, or Azure CLI. 
1. After you create a project, you can deploy a compatible model such as GPT-4o.
1. When you have a deployed model, you can:

    - Try out the Azure AI Foundry agents playground to start exploring agents' capabilities. 
    - You can also start making API calls to the service using the REST API or SDKs.


## Comparing Azure agents and Azure OpenAI assistants

Both agents and assistants enable you to build automated workflows that leverage Large Language Models (LLMs), but Azure AI Agent Service provides all the capabilities of assistants and:
* The ability to use non-Azure OpenAI models Such as Llama 3
* An extended toolset that lets you ground the agent with different datasets and access the web using Bing web searches.

## Next steps

Learn more about the [models that power agents](./concepts/model-region-support.md).