---
title: 'What is the tool catelog in Azure AI Agents Service?'
titleSuffix: Azure OpenAI
description: Learn how to use the various tools available in the Azure AI Agents Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 03/12/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# What is the tool catalog in the Azure AI Agent Service? 

The tool catalog in Azure AI Foundry portal is the hub to discover and use a wide range of tools for building AI agents with Azure AI Agent Service. The tool catalog features tools for extending your agents' abilities using hosted tools, and ones offered from partners such as Tripadvisor, and Morningstar. 

## Prerequisites 

* [A created agent](../../quickstart.md) 

## Supported Tools 

The following is a list of tools supported by Azure AI Agent Service. 

|Tool  |Description  |
|---------|---------|
|[Azure AI Search](./azure-ai-search.md)     | Use an existing Azure AI Search index to ground agents with data in the index, and chat with your data.        |
|[Azure Functions](./azure-functions.md)     | Leverage your Azure Functions to create intelligent, event-driven applications.        |
|[Code Interpreter](./code-interpreter.md)     | Enable agents to write and run Python code in a sandboxed execution environment.         |
|[File Search](./file-search.md)     | Augment agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.          |
|[Function calling](./function-calling.md)     |Describe the structure of functions you create to an agent and have them be called when appropriate during the agent's interactions with users.         |
|[Grounding with Bing Search](./bing-grounding.md)     | Enable your agent to use Bing Search to access and return information from the internet.         |
| [Microsoft Fabric](./fabric.md) | Integrate your agent with the [Microsoft Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. |
| [OpenAPI 3.0 Specified tool ](./openapi-spec.md) | C    onnect your Azure AI Agent to external APIs using functions with an OpenAPI 3.0 specification. |

> [!IMPORTANT]
> * Your use of connected non-Microsoft services is subject to the terms between you and the service provider. By connecting to a non-Microsoft service, you acknowledge that some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft data. 
> * Using tools from tool catalog may incur usage with tool providers, review the pricing plan with your selected tool data providers. 

## Licensed data tools

|Tool  |Description  |
|---------|---------|
| [Morningstar](./morningstar.md) | This tool lets you access Morningstar's investment research API that provides comprehensive analysis, ratings, and data on mutual funds, ETFs, stocks, and bonds. |
| [Tripadvisor](./tripadvisor.md) | This tool lets you access Tripadvisor's useful travel platform that can, for example, provide travel guidance and reviews. |
 