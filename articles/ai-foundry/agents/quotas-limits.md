---
title: Quotas and limits for Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn the quotas and limits for Foundry Agent Service, including file sizes, vector store limits, thread and message limits, and tool limits.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 01/21/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Foundry Agent Service quotas and limits

[!INCLUDE [version-banner](../includes/version-banner.md)]

This article describes the quotas and limits for Foundry Agent Service.

## How quotas and limits apply

Foundry Agent Service enforces limits in two places:

- **Agent Service limits**. Limits for agent and thread artifacts, such as file uploads, vector store attachments, message counts, and tool registration.
- **Model limits**. Quotas and rate limits for the model deployments your agents call.

If you're using threads and messages, see [Threads, runs, and messages in Foundry Agent Service](concepts/threads-runs-messages.md). If you're using file search, see [Vector stores for file search](../default/agents/concepts/vector-stores.md?view=foundry&preserve-view=true).

## Default quotas and limits for the service

The following table lists default limits enforced by the Agent Service.

| Limit name | Limit value |
| --- | --- |
| Maximum number of files per agent/thread | 10,000 |
| Maximum file size for agents | 512 MB |
| Maximum size for all uploaded files for agents | 300 GB |
| Maximum file size in tokens for attaching to a vector store | 2,000,000 tokens |
| Maximum number of messages per thread | 100,000 |
| Maximum size of `text` content per message | 1,500,000 characters |
| Maximum number of tools registered per agent | 128 |

## What happens when you reach a limit

When you exceed one of the limits in this article, the related operation fails. For example:

- **File exceeds the maximum size**: Uploading the file fails. Split the content into smaller files or reduce file size before you upload.
- **Vector store token limit**: Attaching a file to a vector store fails if the file exceeds the token limit. Reduce the file content or split it into multiple files.
- **Thread message cap**: Adding messages can fail after a thread reaches the message limit. Create a new thread for a new conversation session, or archive and rotate threads as part of your application design.
- **Message content size**: Creating a message can fail if the `text` content is too large. Send smaller messages, or move large content into files and use file search.
- **Tool registration cap**: Creating or updating an agent can fail if you register too many tools. Register only the tools you need, and prefer fewer, reusable tools.

For file search scenarios, see [Vector stores for file search](../default/agents/concepts/vector-stores.md?view=foundry&preserve-view=true) for guidance on managing vector store growth.

## Best practices to stay within limits

Use the following practices to reduce limit-related failures:

- **Keep files small and focused**. Prefer multiple smaller documents over a single large document.
- **Avoid very large messages**. Put long content in uploaded files and query it by using file search.
- **Plan for long conversations**. Treat threads as session state and rotate to new threads when conversations become very long.
- **Register only required tools**. Remove unused tools from agent definitions.
- **Monitor usage trends**. Track agent activity and tokens to identify growth early.

## Quotas and limits for models

Agents follow the quotas and rate limits for the model deployments they use.

For current model quotas and limits, see:

- [Azure OpenAI quotas and limits](../openai/quotas-limits.md).
- [Microsoft Foundry Models quotas and limits](../foundry-models/quotas-limits.md).

To view or request more model quota, see [Manage and increase quotas for resources with Microsoft Foundry (Foundry projects)](../how-to/quota.md).

## Related content

- [Supported models in Foundry Agent Service](concepts/model-region-support.md)
- [Threads, runs, and messages in Foundry Agent Service](concepts/threads-runs-messages.md)
- [Monitor Foundry Agent Service](how-to/metrics.md)
- [Vector stores for file search](../default/agents/concepts/vector-stores.md?view=foundry&preserve-view=true)
