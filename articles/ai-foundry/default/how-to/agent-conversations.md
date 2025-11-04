---
title: Agent Conversation and Responses
titleSuffix: Azure AI Foundry
description: "Explore how to view and analyze agent conversation results in Azure AI Foundry, including conversation history, response details, and trace insights."
ai-usage: ai-assisted
author: yanchen-ms
ms.author: lagayhar
ms.reviewer: ychen
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: how-to
---
# View conversation results

A **Conversation** is the persistent context of an end-to-end dialogue history between a user and an agent. In the Azure AI Foundry portal, you can view **Conversation** results for your agent run along with traces in **Traces** page.

You can search for a known Conversation ID, or search by a Response ID or Trace ID, which maps to this conversation, then select **Conversation ID** to review the conversation:

- Conversation history details
- Response information and tokens in a run
- Ordered actions, run steps, and tool calls
- Inputs and outputs between a user and an agent
  
:::image type="content" source="../../agents/media/thread-trace.png" alt-text="A screenshot of a trace." lightbox="../../agents/media/thread-trace.png":::

## Related content

- [Tracing integrations](trace-agent-framework.md)