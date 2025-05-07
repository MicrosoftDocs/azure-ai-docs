---
title: What's new in Azure AI Foundry Agent Service?
titleSuffix: Azure AI Foundry
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

## May 2025

### Azure AI Foundry Agent Service GA

The Azure AI Foundry Agent Service is now Generally Available (GA). Along with this milestone, the service offers the following feature updates:

### Agent catalog

The [agent catalog](./how-to/agent-catalog.md) helps streamline your agent deployment with prebuilt, task-specific agent code samples across a variety of domains such as translation, sales prep, computer use, and more.

### AI Foundry Visual Studio Code extension

The [AI Foundry Visual Studio Code extension](../../ai-foundry/how-to/develop/vs-code-agents.md?context=/azure/ai-services/agents/context/context) is now available with the ability to perform a variety of AI Foundry actions, such as deploying and configure agents natively.

### Connected agents

[Connected agents](./how-to/connected-agents.md) allow you to create task-specific agents that can interact seamlessly with a primary agent. This feature enables you to build multi-agent systems without the need for external orchestrators.

### Trace agents

Debug and monitor your agents by [tracing agent threads](./concepts/tracing.md) to clearly see the inputs and outputs of each primitive involved in a particular agent run, in the order in which they were invoked. 

### Trigger agents using Azure Logic Apps 

[Automatically invoke](./how-to/triggers.md) your AI agent when an event occurs, such as receiving a new email, or getting a new customer ticket so that your AI agent can immediately respond to the new event without manual invocation.

### New agent tools

This release brings a number of new tools to extend agents' capabilities:

* **Bing Custom Search tool** - Determine which websites will be used to ground your agents with. 
* **SharePoint tool** - Use your SharePoint sites to ground your agents data, and chat with your data.
* **Morningstar tool** - Leverage Morningstar, a prominent investment research company, as a data source for your agent. 

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
