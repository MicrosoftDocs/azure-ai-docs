---
title: 'Tools available in the Azure AI Agent service'
titleSuffix: Azure OpenAI
description: Learn about the various tools available for use by the agents you create. 
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 12/03/2024
author: aahill
ms.author: aahi
recommendations: false
---

# Available tools in Azure AI Agent Service

When you create AI agents, you can specify different tools in order to help ground the model they use, or extend their capabilities. These tools are categorized as *knowledge* or *action* tools. 

* *Knowledge* tools give the agent access to data sources for grounding responses. 
* *Action* tools enhance the agent's capabilities by allowing it to run various tools at runtime.

Agents can access multiple tools in parallel. These can be both Azure OpenAI-hosted tools like code interpreter and file search, or tools you build, host, and access through function calling.

> [!TIP]
> You can use the `tool_choice` parameter which can be used to force the use of a specific tool (like file search, code interpreter, or a function) in a particular run.

## Knowledge tools

|Tool  |Description  |
|---------|---------|
| [Code interpreter](./code-interpreter.md)     | Enables agents to write and run Python code in a sandboxed execution environment.        |
| [Grounding with Bing Search](./bing-grounding.md)     | Allows your agents to incorporate real-time public web data when generating responses.         |
|[File search](./file-search.md)    | Augments agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.        |

## Action tools

|Tool  |Description  |
|---------|---------|
|[Function calling](./function-calling.md)     | Allows you to describe the structure of functions to an agent and then return the functions that need to be called along with their arguments.        |
| [Logic Apps function calling](./agent-logic-apps.md) | Enables agents to call Logic Apps workflows through function calling. |
