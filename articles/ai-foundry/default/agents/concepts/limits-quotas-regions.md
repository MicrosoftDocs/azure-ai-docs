---
title: Quotas and limits for the new Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn the quotas and limits for the new Foundry Agent Service, including file sizes, vector stores, threads, messages, tools, and how to handle limit errors.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 02/02/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026, references_regions
monikerRange: 'foundry'
ai-usage: ai-assisted
---

# Quotas, limits, models, and regional support

This article describes the quotas, limits, and regional availability for Foundry Agent Service.

## Supported regions

Foundry Agent Service is available in the following Azure regions:

- Australia East
- Brazil South
- Canada East
- East US
- East US 2
- France Central
- Germany West Central
- Italy North
- Japan East
- Norway East
- South Africa North
- South Central US
- South India
- Sweden Central
- Switzerland North
- UK South
- West Europe
- West US
- West US 3

## Azure OpenAI model support

Foundry Agent Service is compatible with current Azure OpenAI models. For a complete list of supported models and their availability by region, see [Foundry Models sold directly by Azure](../../../foundry-models/concepts/models-sold-directly-by-azure.md).

## Other model collections

The following Foundry models are available for your agents to use.

[!INCLUDE [agent-service-models-support-list](../../../agents/includes/agent-service-models-support-list.md)]
<!--
## Verify model support

Model availability can change over time.

- To verify what you can deploy for your project and region, use the Foundry portal model experience.
- If you use provisioned throughput, make sure you have provisioned throughput units (PTUs) available in the target region. For background, see [Provisioned throughput](../../../openai/concepts/provisioned-throughput.md).
-->

### Troubleshooting

#### A model or version isn't available in your region

- Confirm you selected the right tab for your deployment type.
- Try a different region that supports the model and version.
- If you're using gpt-5 models, make sure your subscription has access. Some models require registration.

#### File search isn't available

- File search isn't available in Italy North and Brazil South. Choose a supported region, or use a different tool.

#### Provisioned throughput deployment fails

- Confirm you have enough PTUs available in the region.
- Review [Provisioned throughput](../../../openai/concepts/provisioned-throughput.md) and [Spillover traffic management](../../../openai/how-to/spillover-traffic-management.md).

## Quotas and limits

Foundry Agent Service enforces limits in two places:

- **Agent Service limits**. Limits for agent and thread artifacts, such as file uploads, vector store attachments, message counts, and tool registration.
- **Model limits**. Quotas and rate limits for the model deployments your agents call.

If you're using threads and messages, see [Threads, runs, and messages in Foundry Agent Service](runtime-components.md). If you're using file search, see [Vector stores for file search](vector-stores.md).

## Default quotas and limits for the service

The following table lists default limits enforced by the Agent Service. These limits apply to all Foundry projects regardless of subscription type or region.

| Limit name | Limit value |
| --- | --- |
| Maximum number of files per agent/thread | 10,000 |
| Maximum file size for agents | 512 MB |
| Maximum size for all uploaded files for agents | 300 GB |
| Maximum file size in tokens for attaching to a vector store | 2,000,000 tokens |
| Maximum number of messages per thread | 100,000 |
| Maximum size of `text` content per message | 1,500,000 characters |
| Maximum number of tools registered per agent | 128 |

Agent Service doesn't impose separate rate limits on API calls. Rate limiting is applied at the model deployment level. See [Azure OpenAI quotas and limits](../../../openai/quotas-limits.md) for model-specific rate limits.

## Handle limit errors

When you exceed a limit, the Agent Service returns an error. Handle these errors gracefully in your application.

| Error scenario | HTTP status | Error code | Recommended action |
| --- | --- | --- | --- |
| File too large | 400 | `file_size_exceeded` | Split content into smaller files |
| Vector store token limit | 400 | `token_limit_exceeded` | Reduce file content or split files |
| Thread message cap | 400 | `message_limit_exceeded` | Create a new thread |
| Message content too large | 400 | `content_size_exceeded` | Use file search for large content |
| Too many tools | 400 | `tool_limit_exceeded` | Remove unused tools |
| Rate limit exceeded | 429 | `rate_limit_exceeded` | Implement exponential backoff |

For example:

- **File exceeds the maximum size**: Uploading the file fails. Split the content into smaller files or reduce file size before you upload.
- **Vector store token limit**: Attaching a file to a vector store fails if the file exceeds the token limit. Reduce the file content or split it into multiple files.
- **Thread message cap**: Adding messages can fail after a thread reaches the message limit. Create a new thread for a new conversation session, or archive and rotate threads as part of your application design.
- **Message content size**: Creating a message can fail if the `text` content is too large. Send smaller messages, or move large content into files and use file search.
- **Tool registration cap**: Creating or updating an agent can fail if you register too many tools. Register only the tools you need, and prefer fewer, reusable tools.

For file search scenarios, see [Vector stores for file search](vector-stores.md) for guidance on managing vector store growth.

## Best practices to stay within limits

Use the following practices to reduce limit-related failures:

- **Keep files small and focused**. Prefer multiple smaller documents over a single large document.
- **Avoid very large messages**. Put long content in uploaded files and query it by using file search.
- **Plan for long conversations**. Treat threads as session state and rotate to new threads when conversations become very long.
- **Register only required tools**. Remove unused tools from agent definitions.
- **Monitor usage trends**. Track agent activity using [Foundry Agent Service metrics](../../../agents/how-to/metrics.md) to identify growth before you hit limits.

## Quotas and limits for models

Agents follow the quotas and rate limits for the model deployments they use.

For current model quotas and limits, see:

- [Azure OpenAI quotas and limits](../../../openai/quotas-limits.md).
- [Microsoft Foundry Models quotas and limits](../../../foundry-models/quotas-limits.md).

To view or request more model quota, see [Manage and increase quotas for resources with Microsoft Foundry (Foundry projects)](../../../how-to/quota.md).

## Request a limit increase

The limits in this article are default values for Foundry Agent Service. If your workload requires higher limits:

- **Model quotas**: You can request increases for model deployment quotas. See [Manage and increase quotas for resources with Microsoft Foundry](../../../how-to/quota.md).
- **Agent Service limits**: The file, message, and tool limits listed in this article are fixed service limits and can't be increased. Design your application to work within these constraints using the best practices described earlier.

## Related content

- [Threads, runs, and messages in Foundry Agent Service](./runtime-components.md)
- [Monitor Foundry Agent Service](../../../agents/how-to/metrics.md)
- [Vector stores for file search](vector-stores.md)
