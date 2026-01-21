---
title: Memory in Microsoft Foundry Agent Service (preview)
titleSuffix: Microsoft Foundry
description: Learn what memory is in Microsoft Foundry Agent Service (preview), how it works, and how to use long-term memories safely.
author: haileytap
ms.author: haileytapia
ms.reviewer: liulewis
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 01/20/2026
ms.custom: pilot-ai-workflow-jan-2026 
ai-usage: ai-assisted
---

# Memory in Microsoft Foundry Agent Service (preview)

> [!IMPORTANT]
> Memory (preview) in Foundry Agent Service and the Memory Store API (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all) and the [Microsoft Products and Services Data Protection Addendum](https://aka.ms/DPA), as well as the Microsoft Generative AI Services Previews terms in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Memory in Microsoft Foundry Agent Service is a managed, long-term memory solution. It enables agent continuity across sessions, devices, and workflows. By creating and managing memory stores, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

This article provides an overview of agent memory, including its concepts, use cases, best practices, and limitations. For usage instructions, see [Create and use memory in Foundry Agent Service](../how-to/memory-usage.md).

## Prerequisites

- A [Microsoft Foundry project](../../../how-to/create-projects.md).
- An Azure OpenAI chat model deployment and an embedding model deployment in your project.

For the full list and setup steps, see [Prerequisites](../how-to/memory-usage.md#prerequisites).

## Supported models and regions

Memory requires Azure OpenAI chat and embedding model deployments. Model and region availability varies.

For the supported model list and region availability, see [Supported models in Foundry Agent Service](../../../agents/concepts/model-region-support.md).

## What is memory?

Memory is persistent knowledge retained by an agent across sessions. Generally, agent memory falls into two categories:

- **Short-term memory** tracks the current session's conversation and maintains immediate context for ongoing interactions. Agent orchestration frameworks typically manage this memory as part of the session context.

- **Long-term memory** retains distilled knowledge across sessions. The model can recall and build on previous user interactions over time. Long-term memory requires a persistent system that extracts, consolidates, and manages knowledge.

Memory in Foundry Agent Service is designed for long-term memory. It extracts meaningful information from conversations, consolidates it into durable knowledge, and makes it available across sessions.

## Key concepts

Memory in Foundry Agent Service uses these core concepts:

- **Memory store**: A managed store that holds long-term memories for an agent. You configure what the store can capture (for example, user profile details and chat summaries) and how your agent reads and writes memories.

- **Scope**: A value you provide to partition memories into isolated collections (for example, one scope per user). Choose a stable identifier that your app can reproduce across sessions. For guidance, see [Understand scope](../how-to/memory-usage.md#understand-scope).

## How memory works

Behind the scenes, memories are stored as items in a managed memory store. The system applies consolidation and conflict‑resolution logic where applicable. Currently, consolidation is performed for user profile memories to merge duplicate or overlapping profile information. Chat summary memories aren't consolidated.

Memory operates in the following phases:

1. **Extraction:** When a user interacts with an agent, the system actively extracts key information from the conversation, such as user preferences, facts, and relevant context. For example, preferences like "allergic to dairy" and summaries of recent activities are identified and stored.

1. **Consolidation:** Extracted memories are consolidated to keep the memory store efficient and relevant. The system uses LLMs to merge similar or duplicate topics so that the agent doesn't store redundant information. Conflicting facts, such as a new allergy, are resolved to maintain an accurate memory.

1. **Retrieval:** When the agent needs to recall information, it uses hybrid search techniques to find the most relevant memories. This allows the agent to quickly surface the right context, making conversations feel natural and informed. Core memories, such as user profile and preferences, are retrieved at the beginning of a conversation so that the agent is immediately aware of the user's core needs.

Here's an example of how memory can improve and personalize interactions between a recipe agent and a user who previously expressed a food allergy:

:::image type="content" source="../media/memory/agent-memory-diagram.svg" alt-text="Diagram that shows memory extraction, storage, and retrieval for an agent across sessions." lightbox="../media/memory/agent-memory-diagram.svg":::

## Memory types

Memory in Foundry Agent Service extracts and stores two types of long-term memory:

| Type | Description | Configuration |
|--|--|--|
| User profile memory | Information and preferences about the user, such as preferred name, dietary restrictions, and language preference. These memories are considered "static" with respect to a conversation because they generally don't depend on the current chat context. Retrieve user profile memories once at the beginning of each conversation. | Specify `user_profile_details` in a [memory store](../how-to/memory-usage.md#customize-memory). |
| Chat summary memory | A distilled summary of each topic or thread covered in a chat session. These memories allow users to continue conversations or reference prior sessions without repeating earlier context. Retrieve chat summary memories based on the current conversation to surface relevant threads. | Enable `chat_summaries` in a [memory store](../how-to/memory-usage.md#create-a-memory-store). |

## Working with memory

There are two ways to use memory for agent interactions:

- **Memory search tool:** Attach the memory search tool to a prompt agent to enable reading from and writing to the memory store during conversations. This approach is ideal for most scenarios because it simplifies memory management. For more information, see [Use memories via an agent tool](../how-to/memory-usage.md#use-memories-via-an-agent-tool).

- **Memory store APIs:** Interact directly with the memory store using the low-level APIs. This approach provides more control and flexibility for advanced use cases. For more information, see [Use memories via APIs](../how-to/memory-usage.md#use-memories-via-apis) and the Memory Store API reference operations: [Create memory store](../../../reference/foundry-project-rest-preview.md#create-memory-store), [List memory stores](../../../reference/foundry-project-rest-preview.md#list-memory-stores), [Get memory store](../../../reference/foundry-project-rest-preview.md#get-memory-store), [Update memory store](../../../reference/foundry-project-rest-preview.md#update-memory-store), [Search memories](../../../reference/foundry-project-rest-preview.md#search-memories), [Update memories](../../../reference/foundry-project-rest-preview.md#update-memories), [Delete scope memories](../../../reference/foundry-project-rest-preview.md#delete-scope-memories), and [Delete memory store](../../../reference/foundry-project-rest-preview.md#delete-memory-store).

## Manage and delete memories

Plan for lifecycle operations, including deletion:

- To delete memories by scope or delete a memory store, see [Delete memories](../how-to/memory-usage.md#delete-memories).
- If you build your own management UI or automation, use the Memory Store API operations, such as [Delete scope memories](../../../reference/foundry-project-rest-preview.md#delete-scope-memories) and [Delete memory store](../../../reference/foundry-project-rest-preview.md#delete-memory-store).

## Choose between memory, conversations, and grounding

Use memory when your agent needs to carry forward user-specific context over time, such as preferences, recurring requirements, and conversation continuity.

Use conversations to maintain interaction history across turns and sessions, rather than storing distilled long-term user knowledge. For more information, see [Agent runtime components](runtime-components.md).

Memory isn't designed for general-purpose document ingestion or retrieval. Use these options instead:

- To ground your agent on curated organizational content, use a [Foundry IQ knowledge base](../how-to/tools/knowledge-retrieval.md).
- To search user-provided documents as part of an interaction, use the [file search tool](../how-to/tools/file-search.md).

## Data and privacy considerations

Treat memory as persisted user data:

- Avoid storing secrets, credentials, authentication tokens, or payment information.
- Store only the minimum information your agent needs to be effective.
- Use `scope` to keep memories isolated to the right user boundary.
- Use `user_profile_details` to narrow what the service should extract and store. See [Customize memory](../how-to/memory-usage.md#customize-memory).
- For production deployments, use [role-based access control](../../../concepts/rbac-foundry.md).

## Best practices

- Start with one scope per user and keep the scope value stable across sessions.
- Retrieve user profile memories once at the start of a conversation, and retrieve chat summary memories based on the current thread.
- Reduce the risk of storing incorrect or malicious content by validating inputs and outputs. Use [Azure AI Content Safety](https://ai.azure.com/explore/contentsafety) and the prompt injection detection guidance in [jailbreak detection](../../../../ai-services/content-safety/concepts/jailbreak-detection.md).

## Common issues

- **The agent doesn't remember a user**: Verify you reuse the same `scope` value across sessions and that your agent is configured to retrieve memories.
- **Memories are irrelevant or too broad**: Tighten `user_profile_details` to focus on only what your agent needs.
- **A memory is incorrect**: Use the management steps in [Create and use memory](../how-to/memory-usage.md), including deleting memories by scope when appropriate.

## Use cases

The following examples illustrate how memory can enhance various types of agents.

### Conversational agent

- A customer support agent that remembers your name, previous issues and resolutions, ticket numbers, and your preferred contact method (chat, email, or call back). This memory helps you avoid repeating information, so conversations are more efficient and satisfying.

- A personal shopping assistant that remembers your size in specific brands, preferred colors, past returns, and recent purchases. The agent can suggest relevant items as soon as you start a session and avoid recommending products you already own.

### Planning agent

- A travel agent that knows your flight preferences (window or aisle), seat selections, food choices, nonstop versus connecting flights, loyalty programs, and feedback from past trips. The agent uses this information to quickly build an optimized itinerary.

- An architectural design agent that remembers local building codes, material costs from previous bids, and initial client feedback. The agent refines designs iteratively, ensuring the final plan is feasible and meets all requirements.

### Research agent

- A medical research agent that remembers which compounds were previously tested and failed, key findings from different labs, and complex relationships between proteins. The agent uses this knowledge to suggest new, untested research hypotheses.

## Security risks

When you work with memory in Foundry Agent Service, the large language model (LLM) extracts and consolidates memories based on conversations. Protect memory against threats such as prompt injection and memory corruption. These risks arise when incorrect or harmful data is stored in the agent's memory, potentially influencing agent responses and actions.

To mitigate security risks, consider these actions:

- **Use [Azure AI Content Safety](https://ai.azure.com/explore/contentsafety) and its [prompt injection detection](../../../../ai-services/content-safety/concepts/jailbreak-detection.md):** Validate all prompts entering or leaving the memory system to prevent malicious content.

- **Perform attack and adversarial testing:** Regularly stress-test your agent for injection vulnerabilities through controlled adversarial exercises.

## Limitations and quotas

- You must use Azure OpenAI models. Other model providers aren't currently supported.
- You must set the `scope` value explicitly (for example, a stable user identifier or `{{$userId}}` when you use the memory search tool). For guidance, see [Best practices](../how-to/memory-usage.md#best-practices).
- Maximum scopes per memory store: 100
- Maximum memories per scope: 10,000
- Search memories: 1,000 requests per minute
- Update memories: 1,000 requests per minute

For broader Foundry Agent Service quotas and limits, see [Foundry Agent Service quotas and limits](../../../agents/quotas-limits.md).

## Pricing

During the public preview, memory features are free. You're only billed for usage of the chat and embedding models.

## Related content

- [Python code samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/memories)
- [Create and use memory in Foundry Agent Service](../how-to/memory-usage.md)
- [Supported models in Foundry Agent Service](../../../agents/concepts/model-region-support.md)
- [Agent runtime components](runtime-components.md)
- [Role-based access control for Microsoft Foundry](../../../concepts/rbac-foundry.md)
- [Microsoft Foundry Quickstart](../../../quickstarts/get-started-code.md)
