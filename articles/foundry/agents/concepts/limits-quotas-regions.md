---
title: "Quotas and limits for Microsoft Foundry Agent Service"
description: "Review default limits for Foundry Agent Service, including file sizes, vector stores, messages, tools, error handling, supported regions, and compatible models."
manager: mcleans
author: aahill
ms.author: aahi
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 07/20/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026, references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# Foundry Agent Service limits, quotas, and regional support
Foundry Agent Service enforces quotas and limits on agent artifacts, file uploads, messages, and tool registrations. Understanding these limits helps you design applications that scale without hitting service boundaries. This article lists default limits, supported regions, compatible models, and guidance for handling limit errors.

> [!NOTE]
> Foundry Agent Service is generally available (GA). Some sub-features are in public preview and might have different constraints.

## Prerequisites

- An Azure subscription.
- A [Microsoft Foundry project](../../how-to/create-projects.md).
- A deployed model compatible with Agent Service. Model and region availability can vary.

## Supported regions

The following table shows regional support for the [Responses API](../../openai/how-to/responses.md), Agents, and private class A IP address ranges.

| Region | Responses API | Agents | Class A\* |
| --- | --- | --- | --- |
| Australia East | Yes | Yes | Yes |
| Brazil South | Yes | Yes | Yes |
| Canada Central | Yes | Yes | No |
| Canada East | Yes | Yes | Yes |
| Central US | Yes | Yes | Yes |
| East US | Yes | Yes | Yes |
| East US 2 | Yes | Yes | Yes |
| France Central | Yes | Yes | Yes |
| Germany West Central | Yes | Yes | Yes |
| Italy North | Yes | Yes | Yes |
| Japan East | Yes | Yes | Yes |
| Korea Central | Yes | Yes | Yes |
| North Central US | Yes | Yes | Yes |
| Norway East | Yes | Yes | No |
| Poland Central | Yes | Yes | No |
| South Africa North | Yes | Yes | Yes |
| South Central US | Yes | Yes | Yes |
| Southeast Asia | Yes | Yes | Yes |
| South India | Yes | Yes | Yes |
| Spain Central | Yes | Yes | Yes |
| Sweden Central | Yes | Yes | Yes |
| Switzerland North | Yes | Yes | No |
| Switzerland West | Yes | Yes | No |
| UAE North | Yes | Yes | Yes |
| UK South | Yes | Yes | Yes |
| West Central US | Yes | Yes | No |
| West Europe | Yes | Yes | Yes |
| West US | Yes | Yes | Yes |
| West US 3 | Yes | Yes | Yes |

\* Class A refers to support for private Class A IP address ranges (10.x.x.x). For related networking requirements, see [Regional support for private networking](#regional-support-for-private-networking).

Some Azure OpenAI models aren't available in every region. For details, see [Region availability for Foundry Models sold by Azure](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md).

> [!IMPORTANT]
> Not all tools are available in every region. For example, file search isn't available in Italy North and Brazil South. For the full tool-by-region matrix, see [Tool support by region and model](#tool-support-by-region-and-model).

### Regional support for private networking

When you use a private network configuration, such as a network-secured standard agent, the following regional requirements apply:

- **Foundry resource and virtual network region.** You must deploy the Foundry resource in the same region as its virtual network. You can deploy other Azure resources, such as Azure Cosmos DB, Azure AI Search, and Azure Storage, in different regions. Consider the cost implications of cross-region deployments.
- **Grounding with Bing Search.** Only the following regions are supported: West Europe, Canada East, Switzerland North, Spain Central, UAE North, Korea Central, Poland Central, Southeast Asia, West US, West US 2, West US 3, East US, East US 2, Central US, South India, Japan East, UK South, France Central, Norway East, Australia East, Canada Central, Sweden Central, South Africa North, Italy North, Brazil South.

For more information, see [Use a virtual network with Foundry Agent Service](../how-to/virtual-networks.md).

### Supported models

Agent Service supports Azure OpenAI models and several Foundry models sold by Azure. Model availability can change over time and varies by region. To see the full list of models you can deploy for your project and region, use the Foundry portal model experience.

### Sovereign clouds

Foundry Agent Service is also available in Azure Government (US Gov Virginia and US Gov Arizona) with a subset of agent types and tools. For the full list of supported features, see [Foundry Agent Service feature availability in Azure Government](./azure-government.md).

## Tool support by region and model

Region and model determine which tools are available to your agent. In the following tables, **Yes** means fully supported, **No** means not supported, and **Limited** means partial support that varies by tool configuration. Check individual tool documentation for details.

The following table shows which tools are available in each [supported region](#supported-regions). This table only accounts for service availability, so make sure the model you want to use is also available in the same region.

<details>
<summary>Click to expand</summary>

| Region             | Agent2Agent | Azure AI Search | Browser Automation | Code Interpreter | Computer Use | Fabric Data Agent | File Search | Function | Grounding with Bing Custom Search | Grounding with Bing Search | Image Generation | MCP | OpenAPI | SharePoint | Web Search |
|---------------------|-----|-----------------|---------------------|-------------------|--------------|--------------------|-------------|----------|------------------------------------|-----------------------------|-------------------|-----|---------|------------|------------|
| Australia East      | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Brazil South        | yes | yes             | yes                 | yes               | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Canada East         | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| East US             | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| East US 2           | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| France Central      | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Germany West Central | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Italy North         | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Japan East          | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Korea Central       | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| North Central US    | yes | yes             | yes                 | yes               | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Norway East         | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Poland Central      | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| South Africa North  | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| South Central US    | yes | yes             | yes                 | no                | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Southeast Asia      | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| South India         | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Spain Central       | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Sweden Central      | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| Switzerland North   | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| UAE North           | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| UK South            | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| West US             | yes | yes             | yes                 | yes               | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| West US 3           | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |

</details>

The following table shows which tools each model supports. For the image generation tool, you need both the `gpt-image-1` model and a large language model (LLM) as the orchestrator in the same Microsoft Foundry project.

<details>
<summary>Click to expand</summary>

| Model | Agent2Agent | Azure AI Search | Azure Functions | Grounding Bing Custom | Grounding Bing Search | Browser Automation | Code Interpreter | Computer Use | Fabric Data Agent | File Search | Functions | Image Generation | MCP | OpenAPI | SharePoint | Web Search | Work IQ (preview) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cohere-command-r | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| Cohere-command-r-plus | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| DeepSeek-R1-0528 | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| DeepSeek-V3-0324 | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| DeepSeek-V3.1 | No | No | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| FW-DeepSeek-V3.1 | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-DeepSeek-V3.2 | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-GLM-4.7 | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-GLM-5 | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-GLM-5.1 | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-GPT-OSS-120B | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-Kimi-K2-Instruct-0905 | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-Kimi-K2-Thinking | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-Kimi-K2.5 | No | No | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-Kimi-K2.6 | No | No | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-MiniMax-M2.5 | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-Qwen3.5-122B-A10B | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| FW-Qwen3.5-397B-A17B | No | Yes | No | No | No | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | Yes |
| GROK-4-20-REASONING | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| Llama-3.3-70B-Instruct | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| Llama-4-Maverick-17B-128E-Instruct-FP8 | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| Llama-4-Scout-17B-16E-Instruct | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| MAI-DS-R1 | Yes | No | No | No | No | Yes | Yes | No | No | Yes | Yes | No | Yes | No | No | No | No |
| Meta-Llama-3.1-405B-Instruct | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| Mistral-large-2407 | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| claude-haiku-4-5 | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| claude-mythos-preview | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| claude-opus-4-1 | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | No | Yes | Yes | Yes | Yes |
| claude-opus-4-5 | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| claude-opus-4-6 | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| claude-opus-4-7 | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| claude-sonnet-4-5 | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| claude-sonnet-4-6 | Yes | Yes | No | No | No | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| codex-mini | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| computer-use-preview | No | No | No | No | No | No | No | Yes | No | No | No | No | No | No | No | No | No |
| gpt-35-turbo | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| gpt-4 | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | Yes |
| gpt-4.1 | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| gpt-4.1-mini | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| gpt-4.1-nano | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| gpt-4.5-preview | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| gpt-4o | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| gpt-4o-mini | Yes | No | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5 | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-5-chat | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | Yes |
| gpt-5-codex | No | No | No | No | No | No | Yes | No | No | Yes | No | No | Yes | No | No | No | Yes |
| gpt-5-mini | No | No | No | No | No | No | Yes | No | No | Yes | No | No | Yes | No | No | Yes | Yes |
| gpt-5-nano | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | Yes |
| gpt-5-pro | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| gpt-5.1 | No | Yes | Yes | No | Yes | No | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.1-chat | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| gpt-5.1-codex | No | No | No | No | No | No | Yes | No | No | Yes | No | No | Yes | No | No | No | Yes |
| gpt-5.1-codex-max | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| gpt-5.1-codex-mini | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| gpt-5.2 | No | Yes | Yes | No | Yes | No | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.2-chat | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | No | Yes | Yes |
| gpt-5.2-codex | No | No | No | No | No | No | Yes | No | No | Yes | No | No | Yes | No | No | No | Yes |
| gpt-5.3-chat | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.3-codex | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.4 | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.4-mini | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.4-nano | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.4-pro | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-5.5 | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-chat-latest | Yes | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes |
| gpt-oss-120b | No | No | No | No | No | No | Yes | No | No | Yes | Yes | No | Yes | No | No | No | Yes |
| grok-3 | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| grok-3-mini | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| grok-4 | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| grok-4-1-fast-non-reasoning | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| grok-4-1-fast-reasoning | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| grok-4-20-non-reasoning | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| grok-4-20-reasoning | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| grok-4-fast-non-reasoning | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| grok-4-fast-reasoning | No | Yes | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes |
| mistral-small-2503 | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| model-router | No | No | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes |
| o1 | No | Yes | No | Yes | No | Yes | Yes | No | No | Yes | Yes | No | Yes | No | Yes | Yes | Yes |
| o1-mini | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| o1-preview | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| o3 | Yes | Yes | No | Yes | No | Yes | Yes | No | Yes | Yes | Yes | No | Yes | Yes | No | Yes | Yes |
| o3-deep-research | No | No | No | No | No | No | No | No | No | No | No | No | Yes | No | No | Yes | Yes |
| o3-mini | Yes | No | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No | No | No | No | No | No | Yes |
| o3-pro | No | No | No | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No |
| o4-mini | Yes | No | No | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | No | Yes | No | Yes | Yes | Yes |

</details>

## Troubleshooting

### A model or version isn't available in your region

- Confirm you selected the right tab for your deployment type (global standard vs. provisioned).
- Try a different region that supports the [model and Responses API](#supported-regions).
- If you're using gpt-5 models, [registration](https://aka.ms/openai/gpt-5/2025-08-07) is required. Access is granted according to Microsoft's eligibility criteria.

### A tool isn't available in your region

- Not all tools are supported in every region. For example, file search isn't available in Italy North and Brazil South, and code interpreter isn't available in all regions.
- Check the [tool support by region and model](#tool-support-by-region-and-model) table to confirm availability before you deploy.
- If a tool isn't available, choose a supported region or use a different tool.

### Provisioned throughput deployment fails

- Confirm you have enough PTUs available in the region.
- Review [Provisioned throughput](../../openai/concepts/provisioned-throughput.md) and [Spillover traffic management](../../openai/how-to/spillover-traffic-management.md).

### Agent receives rate-limit (429) errors

- Implement exponential backoff with jitter in your application retry logic.
- For sustained high-throughput workloads, consider provisioned throughput deployments.
- Review [Azure OpenAI quotas and limits](../../openai/quotas-limits.md) for your deployment's tokens-per-minute and requests-per-minute caps.

## How Agent Service enforces limits

Foundry Agent Service enforces limits in two places:

- **Agent Service limits.** Limits for agent and thread artifacts, such as file uploads, vector store attachments, message counts, and tool registration.
- **Model limits.** Quotas and rate limits for the model deployments your agents call.

The artifacts these limits govern are stored in either Microsoft-managed storage or your own Azure resources, depending on your setup.

## Where Agent Service stores your data

Where your agent data lives depends on which setup option you choose. The setup option also determines which resources the quotas and limits in this article apply to.

- **Basic setup** stores agent state in secure, Microsoft-managed storage that's logically separated. This is the default when you don't configure your own resources.
- **Standard setup** stores agent state in customer-managed, single-tenant Azure resources in your own subscription, which gives you full control over data residency and access.

| Data type | Basic setup | Standard setup |
| --- | --- | --- |
| Files, uploads, and attachments | Microsoft-managed storage | Azure Storage (Blob Storage) |
| Vector stores, embeddings, and retrieval indexes | Microsoft-managed vector search | Azure AI Search |
| Threads, conversation history, messages, and agent definitions | Microsoft-managed storage | Azure Cosmos DB |

[Capability hosts](capability-hosts.md) tell Agent Service where to store and process file uploads, vector stores, and conversation history. To store agent data in your own resources, see [Standard agent setup](standard-agent-setup.md).

Foundry Agent Service endpoints are regional, and data is stored in the same region as the endpoint. For more information, see the [Azure data residency documentation](https://azure.microsoft.com/explore/global-infrastructure/data-residency/#overview).

## Default service limits

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
| Maximum number of valid agent revisions per agent | 1,000 |

The Agent Service limits in this table are fixed and apply uniformly across all subscription types. Rate limiting for model calls is applied at the model deployment level; see [Azure OpenAI quotas and limits](../../openai/quotas-limits.md) for model-specific rate limits.

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
| Too many valid agent revisions | 400 | `UserError` | Delete older versions before creating new ones |

For example:

- **File exceeds the maximum size.** Uploading the file fails. Split the content into smaller files or reduce file size before you upload.
- **Vector store token limit.** Attaching a file to a vector store fails if the file exceeds the token limit. Reduce the file content or split it into multiple files.
- **Thread message cap.** Adding messages can fail after a thread reaches the message limit. Create a new thread for a new conversation session, or archive and rotate threads as part of your application design.
- **Message content size.** Creating a message can fail if the `text` content is too large. Send smaller messages, or move large content into files and use file search.
- **Tool registration cap.** Creating or updating an agent can fail if you register too many tools. Register only the tools you need, and prefer fewer, reusable tools.
- **Rate limit exceeded.** API calls to the model deployment are throttled. Implement exponential backoff with jitter.
- **Valid agent revision cap.** Creating a version fails once an agent reaches 1,000 valid revisions. Delete versions you no longer need to free capacity immediately, then create new versions.

For file search scenarios, see [Vector stores for file search](vector-stores.md) for guidance on managing vector store growth.

## Best practices to stay within limits

Use the following practices to reduce limit-related failures:

- **Keep files small and focused.** Prefer multiple smaller documents over a single large document.
- **Avoid very large messages.** Put long content in uploaded files and query it by using file search.
- **Plan for long conversations.** Treat threads as session state and rotate to new threads when conversations become very long.
- **Register only required tools.** Remove unused tools from agent definitions.
- **Monitor usage trends.** Track agent activity by using [Foundry Agent Service metrics](../../observability/how-to/how-to-monitor-agents-dashboard.md) to identify growth before you hit limits.

## Model quotas and rate limits

Agents follow the quotas and rate limits for the model deployments they use.

For current model quotas and limits, see:

- [Azure OpenAI quotas and limits](../../openai/quotas-limits.md).
- [Microsoft Foundry Models quotas and limits](../../foundry-models/quotas-limits.md).

To view or request more model quota, see [Manage and increase quotas for resources with Microsoft Foundry (Foundry projects)](../../how-to/quota.md).

## Request a limit increase

The limits in this article are default values for Foundry Agent Service. If your workload requires higher limits:

- **Model quotas.** You can request increases for model deployment quotas. See [Manage and increase quotas for resources with Microsoft Foundry](../../how-to/quota.md).
- **Agent Service limits.** The file, message, and tool limits listed in this article are fixed service limits and can't be increased. Design your application to work within these constraints by using the best practices described earlier.

## Related content

- [Threads, runs, and messages in Foundry Agent Service](./runtime-components.md)
- [Capability hosts](capability-hosts.md)
- [Standard agent setup](standard-agent-setup.md)
- [Tool support by region and model](#tool-support-by-region-and-model)
- [Vector stores for file search](vector-stores.md)
- [Monitor Foundry Agent Service](../../observability/how-to/how-to-monitor-agents-dashboard.md)
- [Azure OpenAI quotas and limits](../../openai/quotas-limits.md)
- [Manage and increase quotas for resources with Microsoft Foundry](../../how-to/quota.md)
