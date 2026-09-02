---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/01/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Anthropic's Claude models bring advanced conversational AI capabilities to Microsoft Foundry, providing state-of-the-art language understanding and generation for intelligent applications. Claude models excel at complex reasoning, code generation, and multimodal tasks including image analysis. This article describes the available Claude models, how they're hosted and billed, supported APIs, capabilities, quotas, and best practices.

To deploy and call a Claude model, see [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md).

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]


## How Claude models are hosted and billed

Microsoft Foundry offers Claude models in two versions: 

- Version 1: **Hosted on Anthropic infrastructure**; these models run on Anthropic's infrastructure (outside of Azure). 
- Version 2: **Hosted on Azure**; these models run on Azure infrastructure end-to-end and are all Generally available (GA). 

Not all models are available in both versions. A model's lifecycle stage, such as Preview or Generally available, can differ between the two versions. For per-model availability and lifecycle status, see [Available Claude models](#available-claude-models).

To compare both hosting options across data residency, SLAs, support paths, compliance, and purchasing flow, see [Compare Azure-hosted and Anthropic-hosted Claude models](../concepts/claude-models-hosting-comparison.md).

> [!NOTE]
> You access Claude models in Microsoft Foundry through [Foundry Models from partners and community](../concepts/models-from-partners.md). Models from partners and community that Anthropic sells and operates are Non-Microsoft Products under the Product Terms. 
>
> Claude models in Foundry require an Azure Marketplace subscription and bill through Claude Consumption Units (CCU). Ensure that you have the [permissions required to subscribe to model offerings](../concepts/models-from-partners.md#permissions-required-to-subscribe-to-models-from-partners-and-community) before you deploy. For pricing details, see [Claude Consumption Units (CCU) billing in Microsoft Foundry](../concepts/claude-models-billing.md).

## Available Claude models

[!INCLUDE [claude-eu-ai-compliance](claude-eu-ai-compliance.md)]

The following table compares model availability for both versions of Claude models in Foundry. For details on the features referenced in the table, see the [Capabilities and advanced features](#capabilities-and-advanced-features) section.

For errors you might encounter when you deploy or call Claude models, see [Deploy and use Claude models: Troubleshooting](../how-to/use-foundry-models-claude.md#troubleshooting).

| Model | Availability | Context window / Max output | Key capabilities | Best for |
|---|---|---|---|---|
| `claude-fable-5-1` | <ul><li>Hosted on Anthropic infrastructure: Preview</li></ul> | 1M / 128K | <ul><li>Adaptive thinking</li><li>Long-running work</li><li>Scientific research with self verification</li><li>Knowledge work; handling challenging knowledge work with less hands-on oversight</li><li>Refusal `stop_reason` on dual-use safeguard policies<sup>1</sup> </li><li> See [What's new in Claude Fable 5.1 and Claude Mythos 5.1](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1) | <ul><li>Long-running agents</li><li>Coding and agents, with deeper reasoning for enterprise workflows</li><li>General science and research</li><li>Financial analysis</li><li>Vision</li></ul> |
| `claude-fable-5` | <ul><li>Hosted on Anthropic infrastructure: Preview</li></ul> | 1M / 128K | <ul><li>Adaptive thinking</li><li>Reasoning over entire codebases and multi-day project context</li><li>Longer independent work than any prior Claude model</li><li>Self verification</li><li>Sub-agent orchestration</li><li>Refusal `stop_reason` on dual-use safeguard policies<sup>1</sup> </li><li>See [Migrating to Claude Fable 5.1 and Claude Mythos 5.1](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide) | <ul><li>Cybersecurity</li><li>Autonomous coding</li><li>Long-running agents</li><li>Coding and agents, with deeper reasoning for enterprise workflows</li></ul> |
| `claude-mythos-5-1`<sup>2</sup> | <ul><li>Hosted on Anthropic infrastructure: Gated research preview</li></ul> | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Microsoft Entra ID authentication only </li><li> See [What's new in Claude Fable 5.1 and Claude Mythos 5.1](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)</li></ul> | <ul><li>Biology and life sciences</li><li>Cybersecurity (defensive use cases prioritized): vulnerability discovery, attack-surface auditing, red teaming, threat intelligence</li><li>Autonomous coding</li><li>Long-running agents</li></ul> |
| `claude-mythos-5`<sup>2</sup> | <ul><li>Hosted on Anthropic infrastructure: Gated research preview</li></ul> | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Microsoft Entra ID authentication only </li><li> See [Migrating to Claude Fable 5.1 and Claude Mythos 5.1](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide)</li></ul> | <ul><li>Biology and life sciences</li><li>Cybersecurity (defensive use cases prioritized): vulnerability discovery, attack-surface auditing, red teaming, threat intelligence</li><li>Autonomous coding</li><li>Long-running agents</li></ul> |
| `claude-mythos-preview`<sup>2</sup> |  <ul><li>Hosted on Anthropic infrastructure: Gated research preview</li></ul> | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Microsoft Entra ID authentication only </li><li> See [Migrating to Claude Fable 5.1 and Claude Mythos 5.1](https://platform.claude.com/docs/en/models/fable-5-1/migration-guide)</li></ul> | <ul><li>Cybersecurity (defensive use cases prioritized)</li><li>Autonomous coding</li><li>Long-running agents</li></ul> |
| `claude-opus-5` | <ul><li>Hosted on Azure: GA </li><li>Hosted on Anthropic infrastructure: GA </li></ul> | 1M / 128K |  <ul><li>Adaptive thinking with `xhigh` and `max` effort levels</li><li>Reasoning over entire codebases and multi-day project context</li><li>Per-turn effort controls<sup>3</sup> </li><li>Mid-conversation<sup>3</sup> `role:"system"` </li><li>Token budgets<sup>3</sup> (`task_budget`) </li><li> See [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) </li></ul> | <ul><li>Near-Fable intelligence for long-horizon coding and complex agentic orchestration.</li><li>Long-running agents</li><li>Enterprise workflows</li><li>Financial analysis</li><li>Computer use</li></ul>  |
| `claude-opus-4-8` | <ul><li>Hosted on Azure: GA </li><li>Hosted on Anthropic infrastructure: GA </li></ul> | 1M / 128K | <ul><li>Adaptive thinking with `xhigh` effort level</li><li>Reasoning over entire codebases and multi-day project context</li><li>High-resolution image input (up to 2576px / 3.75MP) </li><li> See [Migrating to Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-5)</li></ul> | <ul><li>Coding</li><li>Long-running agents</li><li>Financial analysis</li><li>Cybersecurity</li><li>Computer use</li></ul> |
| `claude-opus-4-7` | <ul><li>Hosted on Anthropic infrastructure: GA</li></ul>  | 1M / 128K | <ul><li>Adaptive thinking</li><li>Reasoning over entire codebases<li>High-resolution image input (up to 2576px / 3.75MP) </li><li> See [Migrating to Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-5)</li></ul> | <ul><li>Coding</li><li>Enterprise workflows</li><li>Long-running agents</li><li>Multimodal reasoning</li><li>Financial analysis</li><li>Cybersecurity</li></ul> |
| `claude-opus-4-6` | <ul><li>Hosted on Anthropic infrastructure: GA</li></ul> | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples) </li><li> See [Migrating to Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-5)</li></ul> | <ul><li>Coding</li><li>Enterprise agents</li></ul> |
| `claude-opus-4-5` | <ul><li>Hosted on Anthropic infrastructure: GA</li></ul> | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples) </li><li> See [Migrating to Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-5)</li></ul> | <ul><li>Coding</li><li>Agents</li><li>Computer use</li><li>Enterprise workflows</li></ul> |
| `claude-sonnet-5` | <ul><li>Hosted on Azure: GA </li><li>Hosted on Anthropic infrastructure: GA </li></ul> | 1M / 128K | <ul><li>Adaptive thinking </li><li>`xhigh` effort level</li><li>Reasoning over entire codebases and multi-day project context</li><li>High-res image input (up to 2576px / 3.75MP) are on by default</li><li>Mid-conversation<sup>3</sup> `role:"system"` </li><li>Token budgets<sup>3</sup> (`task_budget`) </li><li> See [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5)</li></ul> | <ul><li>Coding</li><li>Long-running agents</li><li>Financial analysis</li><li>Cybersecurity</li><li>Computer use</li></ul> |
| `claude-sonnet-4-6` | <ul><li>Hosted on Anthropic infrastructure: GA</li></ul> | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples) </li><li> See [Migrating to Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-sonnet-5)</li></ul> | <ul><li>Coding</li><li>Agents</li><li>Enterprise workflows</li></ul> |
| `claude-sonnet-4-5` | <ul><li>Hosted on Anthropic infrastructure: GA</li></ul> | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li><li>Computer use </li><li> See [Migrating to Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-sonnet-5) </li></ul> | <ul><li>Agents and complex, long-horizon tasks</li><li>High-volume workloads</li></ul> |
| `claude-haiku-4-5` | <ul><li>Hosted on Azure: GA </li><li>Hosted on Anthropic infrastructure: GA </li></ul> | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input </li></ul> | <ul><li>Coding</li><li>Agents</li></ul> |


<sup>1</sup> **Claude Fable 5** and **Claude Fable 5.1** apply extra input/output classifiers that might refuse requests if the content triggers dual-use safeguard policies. When a refusal happens, the request returns a successful (200) response with a refusal indicator `stop_reason: "refusal"` instead of model-generated content. You aren't billed for input tokens that are refused.

<sup>2</sup> [!INCLUDE [claude-mythos-preview-restriction](claude-mythos-preview-restriction.md)]

<sup>3</sup> Per-turn effort controls, Mid-conversation, and Token budgets are currently in Beta state.

## API overview

The following table lists the APIs that you can use to interact with both the **Hosted on Azure** and **Hosted on Anthropic infrastructure** versions of Claude models in Foundry.

Use the [Anthropic SDKs](https://docs.claude.com/en/api/client-sdks) and the following Claude APIs:

> [!TIP]
> The *Hosted on Anthropic infrastructure version* of Claude models in Foundry supports more APIs than the ones listed in this table. You can see them on the [Claude API docs: API overview](https://platform.claude.com/docs/en/api/overview#available-apis) page.

| API | Description |
|---|---|
| Messages<sup>1</sup> (`POST /v1/messages`) | Core [Messages API](https://docs.claude.com/en/api/messages): Send a structured list of input messages with text or image content, including streaming responses. The model generates the next message in the conversation. |
| Token counting (`POST /v1/messages/count_tokens`) | [Token Count API](https://docs.claude.com/en/api/messages-count-tokens): Count the number of tokens in a message before sending it to Claude. |

<sup>1</sup>You can call the Messages API from the `anthropic` Python package, the `@anthropic-ai/foundry-sdk` JavaScript package, or directly through REST. The deployment endpoint follows the shape `https://<resource-name>.services.ai.azure.com/anthropic/v1/messages`, and REST and JavaScript clients use the `anthropic-version: 2023-06-01` header.

## Capabilities and advanced features

Claude models in Foundry expose *core capabilities* for processing, analyzing, and generating content, and *tools* that let Claude interact with external systems, execute code, and perform automated tasks. Claude's API surface is organized into five areas:

- [Model capabilities](#model-capabilities)
- [Tools](#tools)
- [Tool infrastructure](#tool-infrastructure)
- [Context management](#context-management)
- [Files and assets](#files-and-assets)

The following sections and tables summarize capabilities available across the **Hosted on Azure** and **Hosted on Anthropic infrastructure** versions of Claude models in Foundry. Unless noted, a capability applies to both versions.

> [!TIP]
> The *Hosted on Anthropic infrastructure version* of Claude models in Foundry supports more capabilities than the ones listed in these tables. You can see the full list of capabilities on [Claude Platform Docs: Features overview](https://platform.claude.com/docs/en/build-with-claude/overview).
> 
> For more information about the available capabilities and advanced features for Claude models in Foundry, see the [Microsoft Developer Blog](https://aka.ms/ClaudeGAfeaturesblog).

### Model capabilities

Ways to steer Claude and Claude's direct outputs, including response format, reasoning depth, and input modalities.

| Feature | Description |
|---|---|
| [Streaming messages](https://platform.claude.com/docs/en/build-with-claude/streaming) | When creating a Message, set `"stream": true` to incrementally stream the response using server-sent events (SSE). |
| [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) | Enhanced reasoning capabilities for complex tasks, providing transparency into Claude's step-by-step thought process before delivering its final answer. See [Thinking and effort](#thinking-and-effort) for `thinking` parameter values per model. |
| [Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) | Let Claude dynamically decide when and how much to think. This feature is the only thinking mode on Claude 4.7 and later models. Use the `effort` parameter to control thinking depth. |
| [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) | Control how many tokens Claude uses when responding, trading off between response thoroughness and token efficiency. See [Thinking and effort](#thinking-and-effort) for `effort` parameter values per model. |
| [Citations](https://platform.claude.com/docs/en/build-with-claude/citations) | Ground Claude's responses in sources, including [search results](https://platform.claude.com/docs/en/build-with-claude/search-results) content blocks `search_result`. |
| [Images and vision](https://platform.claude.com/docs/en/build-with-claude/vision) | Process and analyze content from images. **Hosted on Azure** deployments only accept base64 encoded or URL-based images. |
| [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support) | Process and analyze text and visual content from PDF documents. Provide PDFs as base64 or URL. |
| [1M context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) | Up to 1 million tokens for processing large documents, extensive codebases, and long conversations. Support is subject to model eligibility. |
| [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | Constrain Claude's responses to follow a specific JSON schema, using two complementary features: JSON outputs (the `output_config.format` parameter) for structured responses, and strict tool use (`strict: true`) for validated tool inputs. For **Hosted on Azure** deployments, structured outputs also support the legacy parameter for JSON outputs (the `output_format` parameter). |


#### Thinking and effort

The **Thinking** feature allows specific values for the `thinking` parameter type, depending on the model, as described in the following table. The `adaptive` type configures the **adaptive thinking** feature, allowing the model to decide whether to think, based on query complexity and effort level. For example, `thinking={"type": "adaptive"}`.

| Model                   | `adaptive` | `enabled` | `disabled`       |
|-------------------------|:----------:|:---------:|:----------------:|
| `claude-fable-5-1`      | Yes        | No        | No               |
| `claude-fable-5`        | Yes        | No        | No               |
| `claude-mythos-5-1`     | Yes        | No        | No               |
| `claude-mythos-5`       | Yes        | No        | No               |
| `claude-mythos-preview` | Yes        | Yes       | No               |
| `claude-opus-5`         | Yes        | No        | Yes<sup>1</sup>  |
| `claude-opus-4-8`       | Yes        | No        | Yes              |
| `claude-opus-4-7`       | Yes        | No        | Yes              |
| `claude-opus-4-6`       | Yes        | Yes       | Yes              |
| `claude-sonnet-5`       | Yes        | No        | Yes              |
| `claude-sonnet-4-6`     | Yes        | Yes       | Yes              |

<sup>1</sup> Thinking can be `disabled` only at effort `high` or below

The **Effort** feature allows specific `effort` levels for each model, as described in the following table. The `xhigh` level produces the same result as `max`.

| Model               | `low` | `medium` | `high` | `xhigh` | `max` |
|---------------------|:-----:|:--------:|:------:|:-------:|:-----:|
| `claude-fable-5-1`  | Yes   | Yes      | Yes    | Yes     | No    |
| `claude-fable-5`    | Yes   | Yes      | Yes    | Yes     | No    |
| `claude-mythos-5-1` | Yes   | Yes      | Yes    | Yes     | No    |
| `claude-mythos-5`   | Yes   | Yes      | Yes    | Yes     | No    |
| `claude-opus-5`     | Yes   | Yes      | Yes    | Yes     | Yes   |
| `claude-opus-4-8`   | Yes   | Yes      | Yes    | Yes     | Yes   |
| `claude-opus-4-7`   | Yes   | Yes      | Yes    | Yes     | Yes   |
| `claude-opus-4-6`   | Yes   | Yes      | Yes    | No      | Yes   |
| `claude-sonnet-5`   | Yes   | Yes      | Yes    | Yes     | Yes   |
| `claude-sonnet-4-6` | Yes   | Yes      | Yes    | No      | Yes   |

### Tools

Let Claude take actions on the web or in your environment. This feature consists of built-in tools that Claude invokes through `tool_use`. The platform runs server-side tools, and you implement and execute client-side tools.


| Feature | Description |
|---|---|
| Tool use with client-executed tools | Custom tools plus Anthropic-defined `bash`, `text editor`, `computer use`, and `memory`. For more information about these tools, see [Bash](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool), [Text editor](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool), [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), and [Memory](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool). |
| [Web search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) | Discover current real-world data from across the web to use to augment Claude's knowledge. For **Hosted on Azure** deployments, only the `web_search_20250305` tool version is supported. |
| [Web fetch](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool) | Retrieve and perform in-depth analysis of full content from specified web pages and PDF documents, augmenting Claude's context with live web content. On Foundry, web fetch requires a **Hosted on Anthropic infrastructure** deployment. For **Hosted on Azure** deployments, only the `web_fetch_20250910` tool version is supported. |

### Tool infrastructure

Discover, orchestrate, and scale tool use.

| Feature | Description |
|---|---|
| [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming) | Stream tool use parameters without buffering or JSON validation, reducing latency for large parameters. Requires the `anthropic-beta` header `fine-grained-tool-streaming-2025-05-14`. |
| [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector) | Connect to remote MCP servers directly from the Messages API without a separate MCP client. |
| [Tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) | Scale to thousands of tools by dynamically discovering and loading tools on demand using regex- and BM25-based search, optimizing context usage and improving tool selection accuracy. For **Hosted on Azure** deployments, both the `tool_search_tool_bm25_20251119` and `tool_search_tool_regex_20251119` tool versions are supported. The legacy aliases `tool_search_tool_bm25` and `tool_search_tool_regex` are also accepted. |

### Context management

Control and optimize Claude's context window for long-running sessions.

| Feature | Description |
|---|---|
| [Automatic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#automatic-caching) | Simplify prompt caching to a single API parameter. The system automatically caches the last cacheable block in your request, moving the cache point forward as conversations grow. |
| [Prompt caching (5m)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Provide Claude with more background knowledge and example outputs to reduce costs and latency. |
| [Prompt caching (1hr)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration) | Extended 1-hour cache duration for less frequently accessed but important context, complementing the standard 5-minute cache. |
| [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) | Automatically manage conversation context with configurable strategies, including clearing tool results and managing thinking blocks. Requires the anthropic-beta header `context-management-2025-06-27`. |
| [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) | Token counting enables you to determine the number of tokens in a message before sending it to Claude, helping you make informed decisions about your prompts and usage. |

### Files and assets

Manage the documents and data you provide to Claude. 

| Feature | Description |
|---|---|
| [Files API](https://platform.claude.com/docs/en/build-with-claude/files) | Currently available only on **Hosted on Anthropic infrastructure** deployments. Upload and manage files to use with Claude without re-uploading content with each request. Supports PDFs, images, and text files. |

## Agent support

- [Microsoft Agent Framework](/agent-framework/user-guide/agents/agent-types/anthropic-agent) supports creating agents that use Claude models.
- Build custom AI agents with the [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview).

## Deployment types and regions

Claude models in Foundry are available for the following deployment types in specific Azure regions:

- **Global Standard**: All Claude models (Hosted on Azure and Hosted on Anthropic infrastructure).
- **Data Zone Standard (US)**: Hosted on Azure versions of `claude-opus-5`, `claude-opus-4-8`, and `claude-sonnet-5`.

For the exact Azure regions where Claude models are available for deployment, see [Region availability by deployment type](../concepts/models-from-partners.md#region-availability-by-deployment-type).

## Quotas and rate limits

This section explains how deployments share quota and what rate limits apply to them. Subscription-level management handles the deployment quota. Resources and regions share the quota instead of allocating it separately for each resource or region.

- All Global Standard deployments of the same model and version in a subscription draw from one shared quota pool across all regions.
- All Data Zone Standard deployments of the same model and version in a subscription draw from a shared quota pool within each data zone (for example, US).
 
For more information about quota management for Foundry Models, see [Microsoft Foundry Models quotas and limits](../quotas-limits.md#microsoft-foundry-models-quotas-and-limits).

### Cache-aware ITPM

Claude models in Foundry measure rate limits in requests per minute (RPM), _uncached_ input tokens per minute (ITPM), and output tokens per minute (OTPM) for each model.

For most Claude models, **only uncached input tokens count toward your ITPM rate limits**. These tokens include:

- **Input tokens** — tokens in the request after the last cache breakpoint (uncached input).
- **Cache creation input tokens** — tokens being written to cache, which comprises:

    - **Cache write 5m TPM** — tokens being written to the 5-minute prompt cache.
    - **Cache write 1h TPM** — tokens being written to the 1-hour prompt cache.

> [!TIP]
> The _total input tokens_ is the sum of **Input tokens**, **Cache creation input tokens**, and **Cache read input tokens** (the tokens read from cache). However, the _Cache read input tokens_ don't count towards ITPM. **OTPM** also doesn't count towards ITPM.

For more information about rate limits and cache, see [Claude API Docs: Rate limits](https://platform.claude.com/docs/en/api/rate-limits#rate-limits).

### Rate limits by subscription type

Your Azure subscription type determines your rate limits. The **Version 2: Hosted on Azure** and **Version 1: Hosted on Anthropic infrastructure** columns indicate whether quota is available for that model and deployment type combination. **Yes** means quota is available. **N/A** means the model and version combination don't have quota for that deployment type.

The following table lists rate limits. To increase your quota beyond the default limits, submit a request through the [quota increase request form](https://aka.ms/oai/stuquotarequest).

# [Pay-as-you-go](#tab/pay-go)

#### Pay-as-you-go

| Model             | Deployment type         | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | RPM       | ITPM      | OTPM     |
|:------------------|:------------------------|:--------------------------:|:---------------------------------------------:|----------:|----------:|---------:|
| claude-fable-5-1  | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-fable-5    | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-5     | Global Standard         | Yes                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-5     | Data Zone Standard (US) | Yes                        | N/A                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-8   | Global Standard         | Yes                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-8   | Data Zone Standard (US) | Yes                        | N/A                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-7   | Global Standard         | N/A                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-6   | Global Standard         | N/A                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-opus-4-5   | Global Standard         | N/A                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-sonnet-5   | Global Standard         | Yes                        | Yes                                           | 40        | 40,000    | 8,000    |
| claude-sonnet-5   | Data Zone Standard (US) | Yes                        | N/A                                           | 40        | 40,000    | 8,000    |
| claude-sonnet-4-6 | Global Standard         | N/A                        | Yes                                           | 80        | 80,000    | 16,000   |
| claude-sonnet-4-5 | Global Standard         | N/A                        | Yes                                           | 80        | 80,000    | 16,000   |
| claude-haiku-4-5  | Global Standard         | Yes                        | Yes                                           | 80        | 80,000    | 16,000   |

# [Enterprise and MCA-E](#tab/enterprise)

#### Enterprise and MCA-E

| Model             | Deployment type         | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | RPM       | ITPM      | OTPM      |
|:------------------|:------------------------|:--------------------------:|:---------------------------------------------:|----------:|----------:|----------:|
| claude-fable-5-1  | Global Standard         | N/A                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-fable-5    | Global Standard         | N/A                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-opus-5     | Global Standard         | Yes                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-opus-5     | Data Zone Standard (US) | Yes                        | N/A                                           | 2,000     | 2,000,000 | 400,000   |
| claude-opus-4-8   | Global Standard         | Yes                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-opus-4-8   | Data Zone Standard (US) | Yes                        | N/A                                           | 2,000     | 2,000,000 | 400,000   |
| claude-opus-4-7   | Global Standard         | N/A                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-opus-4-6   | Global Standard         | N/A                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-opus-4-5   | Global Standard         | N/A                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-sonnet-5   | Global Standard         | Yes                        | Yes                                           | 2,000     | 2,000,000 | 400,000   |
| claude-sonnet-5   | Data Zone Standard (US) | Yes                        | N/A                                           | 2,000     | 2,000,000 | 400,000   |
| claude-sonnet-4-6 | Global Standard         | N/A                        | Yes                                           | 4,000     | 4,000,000 | 800,000   |
| claude-sonnet-4-5 | Global Standard         | N/A                        | Yes                                           | 4,000     | 4,000,000 | 800,000   |
| claude-haiku-4-5  | Global Standard         | Yes                        | Yes                                           | 4,000     | 4,000,000 | 800,000   |

# [Free Trial](#tab/free)

#### Free Trial

| Model             | Deployment type         | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | RPM       | ITPM      | OTPM     |
|:------------------|:------------------------|:--------------------------:|:---------------------------------------------:|----------:|----------:|---------:|
| claude-fable-5-1  | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-fable-5    | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-5     | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-5     | Data Zone Standard (US) | Yes                        | N/A                                           | 0         | 0         | 0        |
| claude-opus-4-8   | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-4-8   | Data Zone Standard (US) | Yes                        | N/A                                           | 0         | 0         | 0        |
| claude-opus-4-7   | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-4-6   | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-opus-4-5   | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-sonnet-5   | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |
| claude-sonnet-5   | Data Zone Standard (US) | Yes                        | N/A                                           | 0         | 0         | 0        |
| claude-sonnet-4-6 | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-sonnet-4-5 | Global Standard         | N/A                        | Yes                                           | 0         | 0         | 0        |
| claude-haiku-4-5  | Global Standard         | Yes                        | Yes                                           | 0         | 0         | 0        |

---

## Responsible AI considerations

When using Claude models in Foundry, consider these responsible AI practices:

- Review [Data, privacy, and security for Claude models in Microsoft Foundry](../../responsible-ai/claude-models/data-privacy.md) to understand how your data is processed and retained when you deploy Claude models.

- Configure AI content safety during model inference, because Foundry doesn't provide built-in content filtering for Claude models at deployment time.

- Ensure your applications comply with [Anthropic's Acceptable Use Policy](https://www.anthropic.com/legal/aup). Also, see details of safety evaluations for [Claude Fable 5.1 & Claude Mythos 5.1 ](https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card), [Claude Fable 5](https://www.anthropic.com/claude-fable-5-system-card), [Claude Mythos 5](https://www.anthropic.com/claude-mythos-5-system-card), [Claude Mythos Preview](https://www.anthropic.com/claude-mythos-preview-system-card), [Claude Opus 5](https://www.anthropic.com/claude-opus-5-system-card), [Claude Opus 4.8](https://www.anthropic.com/claude-opus-4-8-system-card), [Claude Opus 4.7](https://www.anthropic.com/claude-opus-4-7-system-card), [Claude Opus 4.6](https://www.anthropic.com/claude-opus-4-6-system-card), [Claude Opus 4.5](http://www.anthropic.com/claude-opus-4-5-system-card), [Claude Sonnet 5](https://www.anthropic.com/claude-sonnet-5-system-card), [Claude Sonnet 4.6](https://www.anthropic.com/claude-sonnet-4-6-system-card), [Claude Sonnet 4.5](https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf), and [Claude Haiku 4.5](https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf).
 
## Best practices

Follow these best practices when working with Claude models in Foundry:

### Prompt engineering

- **Clear instructions**: Provide specific and detailed prompts.
- **Context management**: Use the available context window effectively.
- **Role definitions**: Use system messages to define the assistant's role and behavior.
- **Structured prompts**: Use consistent formatting for better results.

### Cost optimization

To optimize your usage and avoid rate limiting:

- **Implement retry logic**: Handle 429 responses with exponential backoff.
- **Batch requests**: Combine multiple prompts when possible.
- **Monitor token usage**: Track your token consumption and request patterns.
- **Use appropriate models**: Use the most cost-effective model for your use case. See [Available Claude models](#available-claude-models).


## Related content

- [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md)
- [Deploy Claude models in Microsoft Foundry using Bicep or Terraform](/azure/developer/ai/how-to/deploy-claude-foundry?context=/azure/foundry/context/context)
- [Foundry Models from partners and community](../concepts/models-from-partners.md)
- [Claude Consumption Units (CCU) billing in Microsoft Foundry](../concepts/claude-models-billing.md)
- [Data, privacy, and security for Claude models in Microsoft Foundry](../../responsible-ai/claude-models/data-privacy.md)
