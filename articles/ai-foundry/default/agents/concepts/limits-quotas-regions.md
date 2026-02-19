---
title: Quotas and limits for Microsoft Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Review default limits for Foundry Agent Service, including file sizes, vector stores, messages, tools, error handling, supported regions, and compatible models.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 02/12/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026, references_regions
monikerRange: 'foundry'
ai-usage: ai-assisted
---

# Foundry Agent Service limits, quotas, and regional support

Foundry Agent Service enforces quotas and limits on agent artifacts, file uploads, messages, and tool registrations. Understanding these limits helps you design applications that scale without hitting service boundaries. This article lists default limits, supported regions, compatible models, and guidance for handling limit errors.

> [!NOTE]
> Foundry Agent Service is generally available (GA). Some sub-features, such as [hosted agents](../concepts/hosted-agents.md), are in public preview and might have different constraints.

## Prerequisites

- An Azure subscription.
- A [Microsoft Foundry project](../../../how-to/create-projects.md).
- A [deployed model](../../../agents/concepts/model-region-support.md) compatible with Agent Service. Model and region availability can vary.

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

> [!IMPORTANT]
> Not all tools are available in every region. For example, file search isn't available in Italy North and Brazil South. For the full tool-by-region matrix, see [Tool support by region and model](../concepts/tool-best-practice.md#tool-support-by-region-and-model).

## Azure OpenAI model support

Foundry Agent Service is compatible with current Azure OpenAI models. For a complete list of supported models and their availability by region, see [Foundry Models sold directly by Azure](../../../foundry-models/concepts/models-sold-directly-by-azure.md).

## Other model collections

In addition to Azure OpenAI models, Agent Service supports models from the Foundry model catalog. These models are deployed and managed through Foundry and follow separate quotas. The following models are available for your agents to use.

[!INCLUDE [agent-service-models-support-list](../../../agents/includes/agent-service-models-support-list.md)]

> [!TIP]
> Model availability can change over time. To verify what you can deploy for your project and region, use the Foundry portal model experience.

## Troubleshooting

### A model or version isn't available in your region

- Confirm you selected the right tab for your deployment type (global standard vs. provisioned).
- Try a different region that supports the model and version. See the [model and region support table](../../../agents/concepts/model-region-support.md).
- If you're using gpt-5 models, [registration](https://aka.ms/openai/gpt-5/2025-08-07) is required. Access is granted according to Microsoft's eligibility criteria.

### A tool isn't available in your region

- Not all tools are supported in every region. For example, file search isn't available in Italy North and Brazil South, and code interpreter isn't available in all regions.
- Check the [tool support by region and model](../concepts/tool-best-practice.md#tool-support-by-region-and-model) table to confirm availability before you deploy.
- If a tool isn't available, choose a supported region or use a different tool.

### Provisioned throughput deployment fails

- Confirm you have enough PTUs available in the region.
- Review [Provisioned throughput](../../../openai/concepts/provisioned-throughput.md) and [Spillover traffic management](../../../openai/how-to/spillover-traffic-management.md).

### Agent receives rate-limit (429) errors

- Implement exponential backoff with jitter in your application retry logic.
- For sustained high-throughput workloads, consider provisioned throughput deployments.
- Review [Azure OpenAI quotas and limits](../../../openai/quotas-limits.md) for your deployment's tokens-per-minute and requests-per-minute caps.

## Quotas and limits

Foundry Agent Service enforces limits in two places:

- **Agent Service limits.** Limits for agent and thread artifacts, such as file uploads, vector store attachments, message counts, and tool registration.
- **Model limits.** Quotas and rate limits for the model deployments your agents call.

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

The Agent Service limits in this table are fixed and apply uniformly across all subscription types. Agent Service doesn't impose separate rate limits on API calls. Rate limiting is applied at the model deployment level. See [Azure OpenAI quotas and limits](../../../openai/quotas-limits.md) for model-specific rate limits.

## Limit error reference

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

- **File exceeds the maximum size.** Uploading the file fails. Split the content into smaller files or reduce file size before you upload.
- **Vector store token limit.** Attaching a file to a vector store fails if the file exceeds the token limit. Reduce the file content or split it into multiple files.
- **Thread message cap.** Adding messages can fail after a thread reaches the message limit. Create a new thread for a new conversation session, or archive and rotate threads as part of your application design.
- **Message content size.** Creating a message can fail if the `text` content is too large. Send smaller messages, or move large content into files and use file search.
- **Tool registration cap.** Creating or updating an agent can fail if you register too many tools. Register only the tools you need, and prefer fewer, reusable tools.
- **Rate limit exceeded.** API calls to the model deployment are throttled. Implement exponential backoff with jitter.

For file search scenarios, see [Vector stores for file search](vector-stores.md) for guidance on managing vector store growth.

## Best practices to stay within limits

Use the following practices to reduce limit-related failures:

- **Keep files small and focused.** Prefer multiple smaller documents over a single large document.
- **Avoid very large messages.** Put long content in uploaded files and query it by using file search.
- **Plan for long conversations.** Treat threads as session state and rotate to new threads when conversations become very long.
- **Register only required tools.** Remove unused tools from agent definitions.
- **Monitor usage trends.** Track agent activity by using [Foundry Agent Service metrics](../../../agents/how-to/metrics.md) to identify growth before you hit limits.

## Quotas and limits for models

Agents follow the quotas and rate limits for the model deployments they use.

For current model quotas and limits, see:

- [Azure OpenAI quotas and limits](../../../openai/quotas-limits.md).
- [Microsoft Foundry Models quotas and limits](../../../foundry-models/quotas-limits.md).

To view or request more model quota, see [Manage and increase quotas for resources with Microsoft Foundry (Foundry projects)](../../../how-to/quota.md).

## Request a limit increase

The limits in this article are default values for Foundry Agent Service. If your workload requires higher limits:

- **Model quotas.** You can request increases for model deployment quotas. See [Manage and increase quotas for resources with Microsoft Foundry](../../../how-to/quota.md).
- **Agent Service limits.** The file, message, and tool limits listed in this article are fixed service limits and can't be increased. Design your application to work within these constraints by using the best practices described earlier.

## Related content

- [Threads, runs, and messages in Foundry Agent Service](./runtime-components.md)
- [Model and region support for Foundry Agent Service](../../../agents/concepts/model-region-support.md)
- [Tool support by region and model](../concepts/tool-best-practice.md#tool-support-by-region-and-model)
- [Vector stores for file search](vector-stores.md)
- [Monitor Foundry Agent Service](../../../agents/how-to/metrics.md)
- [Azure OpenAI quotas and limits](../../../openai/quotas-limits.md)
- [Manage and increase quotas for resources with Microsoft Foundry](../../../how-to/quota.md)
