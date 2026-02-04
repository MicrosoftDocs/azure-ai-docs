---
title: What's new in Foundry Agent Service?
titleSuffix: Microsoft Foundry
description: Learn about new feature updates and additions for your AI Agents.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: overview
ms.date: 10/08/2025
ms.custom: azure-ai-agents
---

# What's new in Foundry Agent Service

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

This article provides a summary of the latest releases and major documentation updates for Foundry Agent Service.

## October 2025

### Additional model support

The Agent Service supports the following [models](./concepts/model-region-support.md):
* gpt-5
* gpt-5-mini
* gpt-5-nano
* gpt-5-chat


## September 2025

### Computer Use tool

The [Computer Use](how-to/tools-classic/computer-use.md) tool is now available in preview. Computer Use is a specialized AI tool that uses a specialized model that can perform tasks by interacting with computer systems and applications through their user interfaces.

## August 2025

### Java SDK Availability

The public preview of the Azure AI Agent Service Java SDK is available. See the following articles for code samples:

* [quickstart](./quickstart.md?pivots=programming-language-java)
* [Azure AI Search](./how-to/tools-classic/azure-ai-search-samples.md?pivots=java)
* [Azure Functions](./how-to/tools-classic/azure-functions-samples.md?pivots=java) 
* [Code interpreter](./how-to/tools-classic/code-interpreter.md) 
* [File search](./how-to/tools-classic/file-search-upload-files.md?pivots=java)
* [Grounding with Bing Search](./how-to/tools-classic/bing-code-samples.md?pivots=java)
* [OpenAPI based tools](./how-to/tools-classic/openapi-spec-samples.md?pivots=java)

### Browser Automation tool

The [Browser Automation tool](how-to/tools-classic/browser-automation.md) is now available in Public Preview. This tool enables you to perform real-world browser tasks through natural language prompts in an isolated browser session using your own provisioned [Microsoft Playwright Workspaces](/azure/playwright-testing/overview-what-is-microsoft-playwright-testing).

### New regional availability

The Agent Service is now available in the following [regions](./concepts/model-region-support.md#available-models):
* Brazil south
* Germany west central
* Italy north
* South central US
## June 2025

### Deep Research tool

Use the [Deep Research tool](how-to/tools-classic/deep-research.md) to utilize a multi-step research process built on top of the Azure OpenAI `o3-deep-research` model and uses the Grounding with Bing Search as the knowledge source.

### Model Context Protocol (MCP) tool

You can new extend the capabilities of your agents by connecting them to tools hosted on remote [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) servers by using the [MCP tool](how-to/tools-classic/model-context-protocol.md). 

## May 2025

### Agent Service GA

The Agent Service is now Generally Available (GA). Along with this milestone, the service offers the following feature updates:

#### Foundry Visual Studio Code extension

The [Foundry Visual Studio Code extension](../../ai-foundry/how-to/develop/vs-code-agents.md?context=/azure/ai-services/agents/context/context) is now available with the ability to perform a variety of Foundry actions, such as deploying and configure agents natively.

#### Connected agents

[Connected agents](how-to\connected-agents.md) allow you to create task-specific agents that can interact seamlessly with a primary agent. This feature enables you to build multi-agent systems without the need for external orchestrators.

#### Trace agents

Debug and monitor your agents by [tracing agent threads](../how-to/develop/trace-agents-sdk.md) to clearly see the inputs and outputs of each primitive involved in a particular agent run, in the order in which they were invoked. 

#### Trigger agents using Azure Logic Apps 

[Automatically invoke](how-to\triggers.md) your AI agent when an event occurs, such as receiving a new email, or getting a new customer ticket so that your AI agent can immediately respond to the new event without manual invocation.

#### New agent tools

This release brings a number of new tools to extend agents' capabilities:

* **Bing Custom Search tool** - Determine which websites will be used to ground your agents with. 
* **Morningstar tool** - Leverage Morningstar, a prominent investment research company, as a data source for your agent. 

## April 2025

### Azure monitor integration

You can now see metrics related to Agents in Azure monitor
* The number of files indexed for file search.
* The number of runs in a given timeframe.

See the [Azure monitor](./how-to/metrics.md) and [metrics reference](./reference/monitor-service.md) articles for more information.

### BYO thread storage
The Standard Agent Setup now supports **Bring Your Own (BYO) thread storage using an Azure Cosmos DB for NoSQL account**. This feature ensures all thread messages and conversation history are stored in your own resources. See the [Quickstart](quickstart.md) for more information on how to deploy a Standard agent project.


## March 2025

### Microsoft Fabric tool

The Microsoft Fabric tool is now available for the Agent Service, allowing users to interact with data you have in Microsoft Fabric through chat and uncover data-driven and actionable insights. See the [how-to article](how-to\tools\fabric.md) for more information.

## February 2025

### Use Agent Service in the Microsoft Foundry portal

You can now use the Agent Service in the [Foundry](https://ai.azure.com/?cid=learnDocs). Create, debug and modify agents, view threads, add tools and chat with agents without writing code. See the [quickstart](quickstart.md?pivots=ai-foundry) for steps on getting started. 

## December 2024

### Azure AI Service public preview

Azure AI Service is now available in preview. The service builds off of the Assistants API in Azure OpenAI, and offers several additional features, such as:

* Several [additional tools](how-to\tools\overview.md) to enhance your AI agents' functionality, such as the ability to use Bing and as a knowledge source and call functions. 
* The ability to use non Azure OpenAI [models](concepts\model-region-support.md): 
    * Llama 3.1-70B-instruct
    * Mistral-large-2407    
    * Cohere command R+
* Enterprise ready security with secure data handling, keyless authentication, and no public egress.
* The ability to either use Microsoft-managed storage, or bring your own.
* SDK support for:
    * [.NET](quickstart.md?pivots=programming-language-csharp) 
    * [The Azure Python SDK](quickstart.md?pivots=programming-language-python-azure)  
    * [The OpenAI Python SDK](quickstart.md?pivots=programming-language-python-openai)   
* Debugging support using [tracing with Application Insights](../how-to/develop/trace-agents-sdk.md)

## Next steps

Use the [quickstart article](quickstart.md) to get started creating a new AI Agent.
