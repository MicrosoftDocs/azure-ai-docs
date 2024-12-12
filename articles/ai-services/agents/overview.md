---
title: What is Azure AI Agent Service?
titleSuffix: Azure AI services
description: Learn how to create agents that apply advanced language models for workflow automation.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: overview
ms.date: 12/11/2024
ms.custom: azure-ai-agents
---

# What is Azure AI Agent Service?

Azure AI Agent Service is a fully managed service designed to empower developers to securely build, deploy, and scale high-quality, and extensible AI agents without needing to manage the underlying compute and storage resources. What originally took hundreds of lines of code to support [client side function calling](/azure/ai-services/openai/how-to/function-calling) can now be done in just a few lines of code with Azure AI Agent Service.

## What is an AI agent?

Within Azure AI Foundry, an AI Agent acts as a "smart" microservice that can be used to answer questions (RAG), perform actions, or completely automate workflows. It achieves this by combining the power of generative AI models with tools that allow it to access and interact with real-world data sources.

// Add a diagram here

Because Azure AI Agent Service uses the same wire protocol as [Azure OpenAI Assistants](/azure/ai-services/openai/how-to/assistant), you can use either [OpenAI SDKs](./quickstart.md?pivots=programming-language-python-openai) or [Azure AI Foundry SDKs](./quickstart.md?programming-language-python-azure) to create and run an agent in just a few lines of code. For example, to create an AI Agent with Azure AI Foundry SDK, you can simply  define which model the AI uses, the instructions for how it should complete tasks, and the tools it can use to access and interact with other services.

// Add code here

After defining an agent, you can start asking it to perform work by invoking a run on top of an activity thread, which is simply a conversation between multiple agents and users. 

// Add code here

Whenever the run operation is invoked, Azure AI Agent Service will complete the entire tool calling lifecycle for you by 1) running the model with the provided instructions, 2) invoking the tools as the agent calls them, and 3) returning the results back to you.

Once you've gotten the basics, you can start using multiple agents together to automate even more complex workflows with [AutoGen](https://microsoft.github.io/autogen/0.2/docs/Getting-Started/) and [Semantic Kernel](/semantic-kernel). Because Azure AI Agent Service is a fully managed service, you can focus on building workflows and the agents that power them without needing to worry about scaling, security, or management of the underlying infrastructure for individual agents.

## Why use Azure AI Agent Service?

When compared to developing with the [Inference API](/azure/ai-studio/reference/reference-model-inference-api) directly, Azure AI Agent Service provides a more streamlined and secure way to build and deploy AI agents. This includes:
1. Automating the tool calling lifecycle for you – no need to parse a tool call, invoke the tool, and handle the response; all of this is now done server-side
2. Securely managing your data – instead of managing your own conversation state, you can rely on threads to store all the information you need
3. Providing out-of-the-box tools – Azure AI Agent Service comes with a set of tools that you can use to interact with your data sources, such as Bing, Azure AI Search, and Azure Functions.

What originally took hundreds of lines of code can now be done in just a few with Azure AI Agent Service.

### Comparing Azure agents and Azure OpenAI assistants

Both services enable you to build agents using the same API and SDKs, but if you have additional enterprise requirements, you may want to consider using Azure AI Agent Service. Azure AI Agent Service provides all the capabilities of assistants in addition to:
* The ability to use non-Azure OpenAI models Such as Llama-3.
* An extended toolset that lets you ground the agent with different services such as Microsoft Bing, Azure Functions, and services defined with OpenAPI specifications.
* And the ability to bring your own Azure Blog storage and Azure AI Search resources for full control and visibility of your storage resources.

## Features overview

**Flexible model selection** - Create agents that leverage OpenAI models, or others such as Llama 3, Mistral and Cohere. Choose the most suitable model to meet your business needs.

**Extensive data integrations** - Ground your AI agents with relevant, secure enterprise knowledge from various data sources, such as Microsoft Bing, Microsoft SharePoint, Microsoft Fabric, Azure AI Search, and other APIs. 

**Enterprise grade security** - Ensure data privacy and compliance with secure data handling, keyless authentication, and no public egress. 

**Choose your storage solution** - Either bring your own Azure Blob storage for full visibility and control of your storage resources, or use platform-managed storage for secure ease-of-use.  

## Responsible AI

At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Generative models such as the ones available in Azure OpenAI have significant potential benefits, but without careful design and thoughtful mitigations, such models have the potential to generate incorrect or even harmful content. Microsoft has made significant investments to help guard against abuse and unintended harm, which includes incorporating Microsoft’s <a href="https://www.microsoft.com/ai/responsible-ai?activetab=pivot1:primaryr6" target="_blank">principles for responsible AI use</a>, adopting a [Code of Conduct](/legal/cognitive-services/openai/code-of-conduct?context=/azure/ai-services/openai/context/context) for use of the service, building [content filters](/azure/ai-services/content-safety/overview) to support customers, and providing responsible AI [information and guidance](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=image) that customers should consider when using Azure AI Agent Service.

## Get started with Azure AI Agent Service

To get started with Azure AI Agent Service, you need to create an Azure AI Foundry hub and an Agent project in your Azure subscription. 

Start with the [quickstart](./quickstart.md) guide if it's your first time using the service.
1. You can create a AI hub and project with the required resources. 
1. After you create a project, you can deploy a compatible model such as GPT-4o.
1. When you have a deployed model, you can also start making API calls to the service using the SDKs.


## Next steps

Learn more about the [models that power agents](./concepts/model-region-support.md).