---
title: 'Tools available in the Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn about the various tools available for use by the agents you create. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 12/18/2024
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Available tools in Azure AI Agent Service

When you create AI agents, you can specify different tools in order to help ground the model they use, or extend their capabilities. These tools are categorized as *knowledge* or *action* tools. 

* *Knowledge* tools give the agent access to data sources for grounding responses. 
* *Action* tools enhance the agent's capabilities by allowing it to run various tools at runtime.

Agents can access multiple tools in parallel. These can be both Azure OpenAI-hosted tools like code interpreter and file search, or tools you build, host, and access through function calling.

> [!TIP]
> You can use the `tool_choice` parameter to force the use of a specific tool (like file search, code interpreter, or a function) in a particular run.

## Knowledge tools

|Tool  |Description  | Python SDK |	C# SDK | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|
| [Grounding with Bing Search](./bing-grounding.md)     | Allows your agents to incorporate real-time public web data when generating responses.         | ✔️ | ✔️ | ✔️ | ✔️ |
|[File search](./file-search.md)    | Augments agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.        | ✔️ | ✔️ | File upload only | File upload and using blob storage | 
| [Azure AI Search](./azure-ai-search.md) | Uses an existing Azure AI Search index as a knowledge base. | ✔️ | ✔️ | | ✔️ |

## Action tools

|Tool  |Description  | Python SDK |	C# SDK | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|
| [Code interpreter](./code-interpreter.md)     | Enables agents to write and run Python code in a sandboxed execution environment.        | ✔️ | ✔️ | ✔️ | ✔️ |
|[Function calling](./function-calling.md)     | Allows you to describe the structure of functions to an agent and then return the functions that need to be called along with their arguments.        | ✔️ | ✔️ | ✔️ | ✔️ |
|[OpenAPI Specification](./openapi-spec.md) | Connect to an external API using an OpenAPI 3.0 specified tool, allowing for scalable interoperability with various applications. | ✔️ | ✔️ | ✔️ | ✔️ |
|[Azure functions](./azure-functions.md) | Use Azure functions to leverage the scalability and flexibility of serverless computing. | ✔️ |  | | ✔️ |