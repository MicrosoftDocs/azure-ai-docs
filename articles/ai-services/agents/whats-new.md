---
title: What's new in Azure AI Foundry Agent Service?
titleSuffix: Azure AI services
description: Learn about new feature updates and additions for your AI Agents.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: overview
ms.date: 04/23/2025
ms.custom: azure-ai-agents
---

# What's new in Azure AI Foundry Agent Service

This article provides a summary of the latest releases and major documentation updates for Azure AI Foundry Agent Service.

## April 2025

### Azure monitor integration

You can now see metrics related to Agents in Azure monitor
* The number of files indexed for file search.
* The number of runs in a given timeframe.

See the [Azure monitor](./how-to/metrics.md) and [metrics reference](./reference/monitor-service.md) articles for more information.

### BYO thread storage
The Standard Agent Setup now supports **Bring Your Own (BYO) thread storage using an Azure Cosmos DB for NoSQL account**. This feature ensures all thread messages and conversation history are stored in your own resources. See the [Quickstart](./quickstart.md) for more information on how to deploy a Standard agent project.


## March 2025

### Microsoft Fabric tool

The Microsoft Fabric tool is now available for the Azure AI Foundry Agent Service, allowing users to interact with data you have in Microsoft Fabric through chat and uncover data-driven and actionable insights. See the [how-to article](./how-to/tools/fabric.md) for more information.

## February 2025

### Use Azure AI Foundry Agent Service in the Azure AI Foundry portal

You can now use the Azure AI Foundry Agent Service in the [Azure AI Foundry](https://ai.azure.com/). Create, debug and modify agents, view threads, add tools and chat with agents without writing code. See the [quickstart](./quickstart.md?pivots=ai-foundry) for steps on getting started. 

## December 2024

### Azure AI Service public preview

Azure AI Service is now available in preview. The service builds off of the [Assistants API](../openai/how-to/assistant.md) in Azure OpenAI, and offers several additional features, such as:

* Several [additional tools](./how-to/tools/overview.md) to enhance your AI agents' functionality, such as the ability to use Bing and as a knowledge source and call functions. 
* The ability to use non Azure OpenAI [models](./concepts/model-region-support.md): 
    * Llama 3.1-70B-instruct
    * Mistral-large-2407    
    * Cohere command R+
* Enterprise ready security with secure data handling, keyless authentication, and no public egress.
* The ability to either use Microsoft-managed storage, or bring your own.
* SDK support for:
    * [.NET](./quickstart.md?pivots=programming-language-csharp) 
    * [The Azure Python SDK](./quickstart.md?pivots=programming-language-python-azure)  
    * [The OpenAI Python SDK](./quickstart.md?pivots=programming-language-python-openai)   
* Debugging support using [tracing with Application Insights](./concepts/tracing.md)

## Next steps

Use the [quickstart article](./quickstart.md) to get started creating a new AI Agent.
