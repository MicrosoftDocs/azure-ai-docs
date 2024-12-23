---
title: What are agents?
titleSuffix: Azure AI services
description: Learn about using agents in the Azure AI Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 12/11/2024
ms.custom: azure-ai-agents
---

# What are agents?

Azure AI Agent Service is now available in public preview. The service makes it easier for developers to create applications with sophisticated copilot-like experiences that can sift through data, suggest solutions, and automate tasks.

* Agents can call Azure OpenAI and other [models](./model-region-support.md) with specific instructions to tune their personality and capabilities.
* Agents can access **multiple tools in parallel**. These can be both tools like [code interpreter](../how-to/tools/code-interpreter.md) <!--and [file search](../how-to/tools/file-search.md),--> or tools you build, host, and access through [function calling](../how-to/tools/function-calling.md).
* Agents can access **persistent Threads**. Threads simplify AI application development by storing message history and truncating it when the conversation gets too long for the model's context length. You create a thread once, and append messages to it as your users reply.
* Agents can access files in several formats. Either as part of their creation or as part of threads between agents and users. When using tools, agents can also create files (such as images or spreadsheets) and cite files they reference in the messages they create.

## Overview

Previously, building custom AI agents needed heavy lifting even for experienced developers. While many APIs are lightweight and powerful like Azure OpenAI's chat completions API, it's inherently stateless which means that developers had to manage conversation state and chat threads, tool integrations, retrieval documents and indexes, and execute code manually.

Azure AI Agent Service, as the evolution of the chat completion API and Assistants, provides a solution for these challenges. Agents support persistent automatically managed threads. This means that as a developer you no longer need to develop conversation state management systems and work around a model’s context window constraints. Agents will automatically handle the optimizations to keep the thread below the max context window of your chosen model. Once you create a thread, you can append new messages to it as users respond. Agents can also access multiple [tools](../how-to/tools/overview.md) in parallel.

Azure AI Agent Service is built on the same capabilities that power Azure OpenAI's assistants. Some possible use cases range from AI-powered product recommender, sales analyst app, coding assistant, employee Q&A chatbot, and more.

> [!IMPORTANT]
> Retrieving untrusted data using Function Calling, Code Interpreter or File Search with file input, and agent threads functionalities could compromise the security of your agent, or the application that uses the agent.

## Agents components

<!-- :::image type="content" source="../media/agents/agents-overview.png" alt-text="A diagram showing the components of an agent." lightbox="../media/agents/agents-overview.png"::: -->

| **Component** | **Description** |
|---|---|
| **Agent** | Custom AI that uses models in conjunction with tools. |
|**Thread** | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.|
| **Message** | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread. |
|**Run** | Activation of an agent to begin running based on the contents of the Thread. The agent uses its configuration and the Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread.|
|**Run Step** | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during it’s run. Examining Run Steps allows you to understand how the agent is getting to its final results. |

<!--## Agents data access

Currently, agents, threads, messages, and files created for agents are scoped at the resource level. Therefore, anyone with access to the resource or API key access is able to read/write agents, threads, messages, and files.

We strongly recommend the following data access controls:

- Implement authorization. Before performing reads or writes on agents, threads, messages, and files, ensure that the end-user is authorized to do so.
- Restrict resource and API key access. Carefully consider who has access to resources where agents are being used, and the associated API keys.
- Routinely audit which accounts/individuals have access to the resource. API keys and resource level access enable a wide range of operations including reading and modifying messages and files.
- If you're using Azure OpenAI models, enabling [diagnostic settings](../../openai/how-to/monitor-openai.md#configure-diagnostic-settings) to allow long-term tracking of certain aspects of the Azure OpenAI resource's activity log.
-->

## Parameters

The agents API has support for several parameters that let you customize the agents' output. The `tool_choice` parameter lets you force the agent to use a specified tool. You can also create messages with the `assistant` role to create custom conversation histories in Threads. `temperature`, `top_p`, `response_format` let you further tune responses. <!-- For more information, see the [reference](../agents-reference.md#create-an-assistant) documentation. -->

## Context window management

Agents automatically truncate text to ensure it stays within the model's maximum context length. You can customize this behavior by specifying the maximum tokens you'd like a run to utilize and/or the maximum number of recent messages you'd like to include in a run.

### Max completion and max prompt tokens

To control the token usage in a single Run, set `max_prompt_tokens` and `max_completion_tokens` when you create the Run. These limits apply to the total number of tokens used in all completions throughout the Run's lifecycle.

For example, initiating a Run with `max_prompt_tokens` set to 500 and `max_completion_tokens` set to 1000 means the first completion will truncate the thread to 500 tokens and cap the output at 1,000 tokens. If only 200 prompt tokens and 300 completion tokens are used in the first completion, the second completion will have available limits of 300 prompt tokens and 700 completion tokens.

If a completion reaches the `max_completion_tokens` limit, the run will terminate with a status of incomplete, and details will be provided in the `incomplete_details` field of the run object.

When using the File Search tool, we recommend setting the `max_prompt_tokens` to no less than 20,000. For longer conversations or multiple interactions with File Search, consider increasing this limit to 50,000, or ideally, removing the `max_prompt_tokens` limits altogether to get the highest quality results.

## Truncation strategy

You can also specify a truncation strategy to control how your thread should be rendered into the model's context window. Using a truncation strategy of type `auto` will use Azure OpenAI's default truncation strategy. Using a truncation strategy of type `last_messages` will allow you to specify the number of the most recent messages to include in the context window.

## See also
* Learn more about [agents](../overview.md). <!--and [File Search](../how-to/tools/file-search.md)-->