---
title: Overview of Memory
titleSuffix: Microsoft Foundry
description: Learn about memory in Foundry Agent Service, a long-term memory solution. Topics include concepts, use cases, best practices, security risks, limitations, and pricing.
author: haileytap
ms.author: haileytapia
ms.reviewer: liulewis
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 12/05/2025
---

# What is memory in Foundry Agent Service?

> [!IMPORTANT]
> Memory (preview) in Foundry Agent Service and the Memory Store API (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all) and the [Microsoft Products and Services Data Protection Addendum](https://aka.ms/DPA), as well as the Microsoft Generative AI Services Previews terms in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Memory in Foundry Agent Service is a managed, long-term memory solution. It enables agent continuity across sessions, devices, and workflows. By creating and managing memory stores, you can build agents that retain user preferences, maintain conversation history, and deliver personalized experiences.

This article provides an overview of agent memory, including its concepts, use cases, best practices, and limitations. For usage instructions, see [Manage memory in Foundry Agent Service](../how-to/memory-usage.md).

## What is memory?

Memory is persistent knowledge retained by an agent across sessions. Generally, agent memory falls into two categories:

- **Short-term memory** tracks the current session's conversation and maintains immediate context for ongoing interactions. Agent orchestration frameworks, such as [Microsoft Agent Framework](/agent-framework/overview/agent-framework-overview), typically manage this memory as part of the session context.

- **Long-term memory** retains distilled knowledge across sessions. The model can recall and build on previous user interactions over time. Long-term memory requires a persistent system that extracts, consolidates, and manages knowledge.

Memory in Foundry Agent Service is designed for long-term memory. It extracts meaningful information from conversations, consolidates it into durable knowledge, and makes it available across sessions.

## How memory works

Behind the scenes, memories are stored as "facts" in a managed memory store. The system applies retention, consolidation, and conflict‑resolution logic to ensure that memories remain accurate and useful over time. It also uses hybrid search techniques (both keyword and vector) to efficiently retrieve relevant memories.

Memory operates in the following phases:

1. **Extraction:** When a user interacts with an agent, the system actively extracts key information from the conversation, such as user preferences, facts, and relevant context. For example, preferences like "allergic to dairy" and facts about recent activities are identified and stored.

1. **Consolidation:** Extracted memories are consolidated to keep the memory store efficient and relevant. The system uses LLMs to merge similar or duplicate topics so that the agent doesn't store redundant information. Conflicting facts, such as a new allergy, are resolved to maintain an accurate memory.

1. **Retrieval:** When the agent needs to recall information, it uses hybrid search techniques to find the most relevant memories. This allows the agent to quickly surface the right context, making conversations feel natural and informed. Core memories, such as allergies, favorite products, and recurring requests, are retrieved at the beginning of a conversation so that the agent is immediately aware of the user's core needs.

Here's an example of how memory can improve and personalize interactions between a recipe agent and a user who previously expressed a food allergy:

:::image type="content" source="../media/agent-memory/agent-memory-diagram.svg" alt-text="A diagram illustrating memory integration." lightbox="../media/agent-memory/agent-memory-diagram.svg":::

> [!TIP]
> Memory isn't designed for general-purpose document ingestion, storage, or retrieval. To provide an agent with grounding data, consider using a [Foundry IQ knowledge base](../how-to/tools/knowledge-retrieval.md).

## Common use cases

The following examples illustrate how memory can enhance various types of agents.

### [Conversational agent](#tab/conversational-agent)

- A customer support agent that remembers your name, previous issues and resolutions, ticket numbers, and your preferred contact method (chat, email, or call back). This memory helps you avoid repeating information, so conversations are more efficient and satisfying.

- A personal shopping assistant that remembers your size in specific brands, preferred colors, past returns, and recent purchases. The agent can suggest relevant items as soon as you start a session and avoid recommending products you already own.

### [Planning agent](#tab/planning-agent)

- A travel agent that knows your flight preferences (window or aisle), seat selections, food choices, nonstop versus connecting flights, loyalty programs, and feedback from past trips. The agent uses this information to quickly build an optimized itinerary.

- An architectural design agent that remembers local building codes, material costs from previous bids, and initial client feedback. The agent refines designs iteratively, ensuring the final plan is feasible and meets all requirements.

### [Research agent](#tab/research-agent)

- A medical research agent that remembers which compounds were previously tested and failed, key findings from different labs, and complex relationships between proteins. The agent uses this knowledge to suggest new, untested research hypotheses.

---

## Best practices

- **Implement per-user access controls:** Avoid giving agents access to memories shared across all users. Use the `scope` property to partition the memory store by user. When sharing `scope` across users, use `user_profile_details` to instruct the memory system not to store personal information.

- **Minimize and protect sensitive data:** Store only what's necessary for your use case. If you must store sensitive data, such as personal data, health data, or confidential business inputs, redact or remove other content that could be used to trace back to an individual.

- **Support privacy and compliance:** Provide users with transparency, including options to access and delete their data. Record all deletions in a tamper-evident audit trail. Ensure the system adheres to local compliance requirements and regulatory standards.

- **Segment data and isolate memory:** In multi-agent systems, segment memory logically and operationally. Allow customers to define, isolate, inspect, and delete their own memory footprint.

- **Monitor memory usage:** Track token usage and memory operations to understand costs and optimize performance.

## Security risks

When you work with memory in Foundry Agent Service, the LLM extracts and consolidates memories based on conversations. Protect memory against threats such as prompt injection and memory corruption. These risks arise when incorrect or harmful data is stored in the agent's memory, potentially influencing agent responses and actions.

To mitigate security risks, consider these actions:

- **Use [Azure AI Content Safety](https://ai.azure.com/explore/contentsafety) and its [prompt injection detection](../../../../ai-services/content-safety/concepts/jailbreak-detection.md):** Validate all prompts entering or leaving the memory system to prevent malicious content.

- **Perform attack and adversarial testing:** Regularly stress-test your agent for injection vulnerabilities through controlled adversarial exercises.

## Limitations and quotas

- You must use Azure OpenAI models. Other model providers aren't currently supported.
- You must set the `scope` value explicitly. Automatic population from the user identity specified in the request isn't currently supported.
- Maximum scopes per memory store: 100
- Maximum memories per scope: 10,000
- Search memories: 1,000 requests per minute
- Update memories: 1,000 requests per minute

## Pricing

During the public preview, memory features are free. You're only billed for usage of the chat and embedding models.

## Related content

- [Python code samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/memories)
- [Manage memory in Foundry Agent Service](agent-memory.md)
- [Build an agent with Microsoft Foundry](../../../agents/quickstart.md)
- [Microsoft Agent Framework overview](/agent-framework/overview/agent-framework-overview)
