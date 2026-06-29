---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/23/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Anthropic's Claude models bring advanced conversational AI capabilities to Microsoft Foundry, providing state-of-the-art language understanding and generation for intelligent applications. Claude models excel at complex reasoning, code generation, and multimodal tasks including image analysis. This article describes the available Claude models, how they're hosted and billed, supported APIs, capabilities, quotas, and best practices.

To deploy and call a Claude model, see [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md).

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]


## How Claude models are hosted and billed

Microsoft Foundry offers Claude models in two versions: **Hosted on Azure** and **Hosted on Anthropic infrastructure (preview)**. Not every model is available in both versions. A model's lifecycle stage, such as Preview or Generally available, can differ between the two versions. For per-model availability and lifecycle status, see [Available Claude models](#available-claude-models).

> [!NOTE]
> You access Claude models in Microsoft Foundry through [Foundry Models from partners and community](../concepts/models-from-partners.md). Models from partners and community that Anthropic sells and operates are Non-Microsoft Products under the Product Terms. Claude models in Foundry require an Azure Marketplace subscription. Ensure that you have the [permissions required to subscribe to model offerings](../how-to/configure-marketplace.md) before you deploy.

Claude models that are **Hosted on Azure** run on Azure infrastructure end-to-end and are Generally available (GA). 

Claude models that are **Hosted on Anthropic infrastructure (preview)** run on Anthropic's infrastructure (outside of Azure) and are in preview. 

To learn how data is processed when you use Claude models in Foundry, see [Data, privacy, and security for Claude models in Microsoft Foundry](../../responsible-ai/claude-models/data-privacy.md).

To learn how Claude consumption units (CCU) bill Claude models in Microsoft Foundry through Azure Marketplace, see [Claude Consumption Units (CCU) billing in Microsoft Foundry](../concepts/claude-models-billing.md).

## Available Claude models

<!-- PLACEHOLDER: When [TO VERIFY: Scarlett] is available, confirm it is also Azure-hosted and update any model-specific warnings, notes, or footnotes that apply. -->

The following table compares model availability for both versions of Claude models in Foundry. For details on the features referenced in the table, see the [Capabilities](#capabilities) section.

> [!WARNING]
> 1M context beta on **Claude Sonnet 4.5** was retired on April 30, 2026.
>
> Starting May 1, 2026:
> - Requests **greater than 200K tokens** that include the `context-1m-2025-08-07` beta header on Sonnet 4.5 return an error.
> - Requests **200K tokens or fewer** remain unaffected, even with the header present.
>
> To migrate, remove the `context-1m-2025-08-07` beta header from your requests. For workloads that require 1M context, migrate to **Claude Sonnet 4.6** (where 1M context is generally available) or to **Claude Opus 4.6** or **Claude Opus 4.7** for higher-intelligence workloads.

| Model | Availability | Context window / Max output | Key capabilities | Best for |
|---|---|---|---|---|
| `claude-mythos-5`<sup>1</sup> | Hosted on Anthropic: Gated research preview | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Microsoft Entra ID authentication only</li></ul> | <ul><li>Biology and life sciences</li><li>Cybersecurity (defensive use cases prioritized): vulnerability discovery, attack-surface auditing, red teaming, threat intelligence</li><li>Autonomous coding</li><li>Long-running agents</li></ul> |
| `claude-fable-5` | Hosted on Anthropic: Preview | 1M / 128K | <ul><li>Adaptive thinking</li><li>Reasoning over entire codebases and multi-day project context</li><li>Longer independent work than any prior Claude model</li><li>Self verification</li><li>Sub-agent orchestration</li><li>Refusal `stop_reason` on dual-use safeguard policies<sup>2</sup></li></ul> | <ul><li>Cybersecurity</li><li>Autonomous coding</li><li>Long-running agents</li><li>Coding and agents, with deeper reasoning for enterprise workflows</li></ul> |
| `claude-mythos-preview`<sup>1</sup> |  Hosted on Anthropic: Gated research preview | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Microsoft Entra ID authentication only</li></ul> | <ul><li>Cybersecurity (defensive use cases prioritized)</li><li>Autonomous coding</li><li>Long-running agents</li></ul> |
| `claude-opus-4-8`<sup>3</sup> | Hosted on Azure: GA | 1M / 128K | <ul><li>Adaptive thinking with `xhigh` effort level</li><li>Reasoning over entire codebases and multi-day project context</li><li>High-resolution image input (up to 2576px / 3.75MP)</li></ul> | <ul><li>Coding</li><li>Long-running agents</li><li>Financial analysis</li><li>Cybersecurity</li><li>Computer use</li></ul> |
| `claude-opus-4-8`<sup>3</sup> | Hosted on Anthropic (Version 1) - GA | 1M / 128K | <ul><li>Adaptive thinking with `xhigh` effort level</li><li>Reasoning over entire codebases and multi-day project context</li><li>High-resolution image input (up to 2576px / 3.75MP)</li></ul> | <ul><li>Coding</li><li>Long-running agents</li><li>Financial analysis</li><li>Cybersecurity</li><li>Computer use</li></ul> |
| `claude-opus-4-7` | Hosted on Anthropic: GA  | 1M / 128K | <ul><li>Adaptive thinking</li><li>Reasoning over entire codebases<li>High-resolution image input (up to 2576px / 3.75MP)</li></ul> | <ul><li>Coding</li><li>Enterprise workflows</li><li>Long-running agents</li><li>Multimodal reasoning</li><li>Financial analysis</li><li>Cybersecurity</li></ul> |
| `claude-opus-4-6` | Hosted on Anthropic: GA | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples)</li></ul> | <ul><li>Coding</li><li>Enterprise agents</li></ul> |
| `claude-opus-4-5` | Hosted on Anthropic (Version 1) - GA | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples)</li></ul> | <ul><li>Coding</li><li>Agents</li><li>Computer use</li><li>Enterprise workflows</li></ul> |
| `claude-opus-4-1` | Hosted on Anthropic: GA | 200K / 32K | <ul><li>Extended thinking</li><li>Image and text input</li></ul> | <ul><li>Coding</li><li>Long-running tasks</li></ul> |
| `claude-sonnet-4-6` | Hosted on Anthropic:  GA | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples)</li></ul> | <ul><li>Coding</li><li>Agents</li><li>Enterprise workflows</li></ul> |
| `claude-sonnet-4-5` | Hosted on Anthropic: GA | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li><li>Computer use</li></ul> | <ul><li>Agents and complex, long-horizon tasks</li><li>High-volume workloads</li></ul> |
| `claude-haiku-4-5` | Hosted on Azure: GA | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li></ul> | <ul><li>Coding</li><li>Agents</li></ul> |
| `claude-haiku-4-5` | Hosted on Anthropic: GA  | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li></ul> | <ul><li>Coding</li><li>Agents</li></ul> |

<sup>1</sup> [!INCLUDE [claude-mythos-preview-restriction](claude-mythos-preview-restriction.md)]

<sup>2</sup> Claude Fable 5 applies additional input/output classifiers that may refuse requests whose content triggers dual-use safeguard policies. When a refusal occurs, the request returns a successful (200) response with a refusal indicator `stop_reason: "refusal"` instead of model-generated content. You're not billed for input tokens that are refused.

<sup>3</sup> Follow the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-opus-47) to migrate Messages API code from Claude Opus 4.7 to Claude Opus 4.8.

<sup>4</sup> Mid-conversation and Token budgets are currently in Beta state.

## API overview

The following table lists the APIs that you can use to interact with both the **Hosted on Azure** and **Hosted on Anthropic infrastructure (preview)** versions of Claude models in Foundry.

Use the [Anthropic SDKs](https://docs.claude.com/en/api/client-sdks) and the following Claude APIs:

> [!TIP]
> The *Hosted on Anthropic infrastructure (preview) version* of Claude models in Foundry supports more APIs than the ones listed in this table. You can see them on the [Claude API docs: API overview](https://platform.claude.com/docs/en/api/overview#available-apis) page.

| API | Description |
|---|---|
| Messages<sup>1</sup> (`POST /v1/messages`) | Core [Messages API](https://docs.claude.com/en/api/messages): Send a structured list of input messages with text or image content, including streaming responses. The model generates the next message in the conversation. |
| Token counting (`POST /v1/messages/count_tokens`) | [Token Count API](https://docs.claude.com/en/api/messages-count-tokens): Count the number of tokens in a message before sending it to Claude. |

<sup>1</sup>You can call the Messages API from the `anthropic` Python package, the `@anthropic-ai/foundry-sdk` JavaScript package, or directly through REST. The deployment endpoint follows the shape `https://<resource-name>.services.ai.azure.com/anthropic/v1/messages`, and REST and JavaScript clients use the `anthropic-version: 2023-06-01` header.

## Capabilities

<!-- PLACEHOLDER: When [TO VERIFY: Scarlett] is available, update the capabilities table and any model-specific parameter tables in this section. -->

Claude models in Foundry expose *core capabilities* for processing, analyzing, and generating content, and *tools* that let Claude interact with external systems, execute code, and perform automated tasks. 

The following table summarizes capabilities available for both the **Hosted on Azure** and **Hosted on Anthropic infrastructure (preview)** versions of Claude models in Foundry, including core capabilities and tools.

> [!TIP]
> The *Hosted on Anthropic infrastructure (preview) version* of Claude models in Foundry supports more capabilities than the ones listed in this table. You can see them on the [Claude API docs: Features overview](https://docs.claude.com/en/docs/build-with-claude/overview) page.

| Feature | Description |
|---|---|
| Streaming responses | Server-sent event streaming. |
| Fine-grained tool streaming | Stream tool use parameters without buffering or JSON validation, reducing latency for large parameters. Requires the anthropic-beta header `fine-grained-tool-streaming-2025-05-14`. |
| Prompt caching | Cache context to reduce cost and latency. |
| Tool use with client-executed tools | Custom tools plus Anthropic-defined `bash`, `text editor`, `computer use`, and `memory`. |
| Context editing | Automatically manage conversation context with configurable strategies, including clearing tool results and managing thinking blocks. Requires the anthropic-beta header `context-management-2025-06-27`. |
| Extended thinking | Step-by-step reasoning for complex tasks. |
| Effort | Control how many tokens Claude uses when responding, trading off between response thoroughness and token efficiency. |
| Citations | Ground Claude's responses in sources, including `search_result` content blocks. |
| Image support | Process and analyze content from images (provided as base64 or URL). |
| PDF support | Process and analyze text and visual content from PDF documents. Provided as base64 or URL. |
| 1M context window | Up to 1M tokens for processing large documents, extensive codebases, and long conversations. Support is subject to model eligibility. |

#### Model-specific parameter values

**Extended thinking**

The **Extended thinking** feature allows specific values for the `thinking` parameter type, depending on the model, as described in the following table. The `adaptive` type allows the model to decide whether to think, based on query complexity and effort level.

| Model                   | `adaptive` | `enabled` | `disabled` |
|-------------------------|:----------:|:---------:|:----------:|
| `claude-mythos-5`       | Yes        | No        | No         |
| `claude-fable-5`        | Yes        | No        | No         |
| `claude-mythos-preview` | Yes        | Yes       | No         |
| `claude-opus-4-8`       | Yes        | No        | Yes        |
| `claude-opus-4-7`       | Yes        | No        | Yes        |
| `claude-opus-4-6`       | Yes        | Yes       | Yes        |
| `claude-sonnet-4-6`     | Yes        | Yes       | Yes        |


**Effort**

The Effort feature allows specific `effort` levels for each model, as described in the following table. The `xhigh` level produces the same result as `max`.

| Model               | `low` | `medium` | `high` | `max` | `xhigh` |
|---------------------|:-----:|:--------:|:------:|:-----:|:-------:|
| `claude-mythos-5`   | Yes   | Yes      | Yes    | No    | Yes     |
| `claude-fable-5`    | Yes   | Yes      | Yes    | No    | Yes     |
| `claude-opus-4-8`   | Yes   | Yes      | Yes    | Yes   | Yes     |
| `claude-opus-4-7`   | Yes   | Yes      | Yes    | Yes   | Yes     |
| `claude-opus-4-6`   | Yes   | Yes      | Yes    | Yes   | No      |
| `claude-sonnet-4-6` | Yes   | Yes      | Yes    | Yes   | No      |

## Agent support

- [Microsoft Agent Framework](/agent-framework/user-guide/agents/agent-types/anthropic-agent) supports creating agents that use Claude models.
- Build custom AI agents with the [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview).


## Quotas, rate limits, and regions

<!-- PLACEHOLDER: When [TO VERIFY: Scarlett] is available, update deployment type availability, quota text, and all three rate-limit tables in this section for both Hosted on Azure and Hosted on Anthropic infrastructure. -->

Use this section to understand where you can deploy Claude models, how quota is shared, and what rate limits apply to your deployments.

### Deployment types

Claude models in Foundry are available for the following deployment types:

- **Global Standard**: All Claude models (Hosted on Azure and Hosted on Anthropic infrastructure) are available in **East US2** and **Sweden Central**.
- **Data Zone Standard (US)**: `claude-opus-4-8`.

For more information on the different deployment types, see [Deployment types for Microsoft Foundry Models](../concepts/deployment-types.md).

### Quotas and rate limits

Subscription-level management handles the deployment quota. Resources and regions share the quota instead of allocating it separately for each resource or region.

- All Global Standard deployments of the same model and version in a subscription draw from one shared quota pool across all regions.
- All Data Zone Standard deployments of the same model and version in a subscription draw from a shared quota pool within each data zone (for example, US).
 
For more information about quota management for Foundry Models, see [Microsoft Foundry Models quotas and limits](../quotas-limits.md#microsoft-foundry-models-quotas-and-limits).

Claude models in Foundry measure rate limits in Requests Per Minute (RPM) and uncached input Tokens Per Minute (ITPM).

**What counts towards ITPM?**

- **Input TPM** — tokens in the request after the last cache breakpoint (uncached input).
- **Cache write 5m TPM** — tokens being written to the 5-minute prompt cache.
- **Cache write 1h TPM** — tokens being written to the 1-hour prompt cache.

**What doesn't count towards ITPM?**

- Output tokens (including tokens read from cache) don't count towards uiTPM. 

For more information about rate limits and cache, see [Claude API Docs: Rate limits](https://platform.claude.com/docs/en/api/rate-limits#rate-limits).

### Rate limits by subscription type

Your Azure subscription type determines your rate limits. The **Version 2: Hosted on Azure** and **Version 1: Hosted on Anthropic infrastructure** columns indicate whether quota is available for that model and deployment type combination. **Yes** means quota is available. **N/A** means the model and version combination don't have quota for that deployment type.

As listed in the following table, to increase your quota beyond the default limits, submit a request through the [quota increase request form](https://aka.ms/oai/stuquotarequest).

# [Pay-as-you-go](#tab/pay-go)

#### Pay-as-you-go

| Model             | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | Deployment type         | RPM | ITPM   |
|:------------------|:--------------------------:|:---------------------------------------------:|:------------------------|:---:|:------:|
| claude-fable-5    | N/A                        | Yes                                           | Global Standard         | 0   | 0      |
| claude-opus-4-8   | Yes                        | Yes                                           | Global Standard         | 40  | 40,000 |
| claude-opus-4-8   | Yes                        | N/A                                           | Data Zone Standard (US) | 40  | 40,000 |
| claude-opus-4-7   | N/A                        | Yes                                           | Global Standard         | 40  | 40,000 |
| claude-opus-4-6   | N/A                        | Yes                                           | Global Standard         | 40  | 40,000 |
| claude-opus-4-5   | N/A                        | Yes                                           | Global Standard         | 40  | 40,000 |
| claude-opus-4-1   | N/A                        | Yes                                           | Global Standard         | 40  | 40,000 |
| claude-sonnet-4-6 | N/A                        | Yes                                           | Global Standard         | 80  | 80,000 |
| claude-sonnet-4-5 | N/A                        | Yes                                           | Global Standard         | 80  | 80,000 |
| claude-haiku-4-5  | N/A                        | Yes                                           | Global Standard         | 80  | 80,000 |

# [Enterprise and MCA-E](#tab/enterprise)

#### Enterprise and MCA-E

| Model             | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | Deployment type         | RPM   | ITPM      |
|:------------------|:--------------------------:|:---------------------------------------------:|:------------------------|:-----:|:---------:|
| claude-fable-5    | N/A                        | Yes                                           | Global Standard         | 2,000 | 2,000,000 |
| claude-opus-4-8   | Yes                        | Yes                                           | Global Standard         | 2,000 | 2,000,000 |
| claude-opus-4-8   | Yes                        | N/A                                           | Data Zone Standard (US) | 2,000 | 2,000,000 |
| claude-opus-4-7   | N/A                        | Yes                                           | Global Standard         | 2,000 | 2,000,000 |
| claude-opus-4-6   | N/A                        | Yes                                           | Global Standard         | 2,000 | 2,000,000 |
| claude-opus-4-5   | N/A                        | Yes                                           | Global Standard         | 2,000 | 2,000,000 |
| claude-opus-4-1   | N/A                        | Yes                                           | Global Standard         | 2,000 | 2,000,000 |
| claude-sonnet-4-6 | N/A                        | Yes                                           | Global Standard         | 4,000 | 4,000,000 |
| claude-sonnet-4-5 | N/A                        | Yes                                           | Global Standard         | 4,000 | 4,000,000 |
| claude-haiku-4-5  | N/A                        | Yes                                           | Global Standard         | 4,000 | 4,000,000 |

# [Free Trial](#tab/free)

#### Free Trial

| Model             | Version 2: Hosted on Azure | Version 1: Hosted on Anthropic infrastructure | Deployment type         | RPM   | ITPM      |
|:------------------|:--------------------------:|:---------------------------------------------:|:------------------------|:---:|:----:|
| claude-fable-5    | N/A                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-opus-4-8   | Yes                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-opus-4-8   | Yes                        | N/A                                           | Data Zone Standard (US) | 0   | 0    |
| claude-opus-4-7   | N/A                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-opus-4-6   | N/A                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-opus-4-5   | N/A                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-opus-4-1   | N/A                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-sonnet-4-6 | N/A                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-sonnet-4-5 | N/A                        | Yes                                           | Global Standard         | 0   | 0    |
| claude-haiku-4-5  | Yes                        | Yes                                           | Global Standard         | 0   | 0    |

---


## Responsible AI considerations

<!-- PLACEHOLDER: Add the safety evaluation, system card, or other Responsible AI references for [TO VERIFY: Scarlett] when they are published. -->

When using Claude models in Foundry, consider these responsible AI practices:

- Configure AI content safety during model inference, because Foundry doesn't provide built-in content filtering for Claude models at deployment time.

- Ensure your applications comply with [Anthropic's Acceptable Use Policy](https://www.anthropic.com/legal/aup). Also, see details of safety evaluations for [Claude Fable 5](https://www.anthropic.com/claude-fable-5-system-card), [Claude Mythos 5](https://www.anthropic.com/claude-mythos-5-system-card), [Claude Mythos Preview](https://www.anthropic.com/claude-mythos-preview-system-card), [Claude Opus 4.8](https://www.anthropic.com/claude-opus-4-8-system-card), [Claude Opus 4.7](https://www.anthropic.com/claude-opus-4-7-system-card), [Claude Opus 4.6](https://www.anthropic.com/claude-opus-4-6-system-card), [Claude Opus 4.5](http://www.anthropic.com/claude-opus-4-5-system-card), [Claude Opus 4.1](https://assets.anthropic.com/m/4c024b86c698d3d4/original/Claude-4-1-System-Card.pdf), [Claude Sonnet 4.6](https://www.anthropic.com/claude-sonnet-4-6-system-card), [Claude Sonnet 4.5](https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf), and [Claude Haiku 4.5](https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf).
 
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
- [Claude on Foundry starter kit](https://github.com/Azure-Samples/claude#readme)
- [Foundry Models from partners and community](../concepts/models-from-partners.md)
- [Claude Consumption Units (CCU) billing in Microsoft Foundry](../concepts/claude-models-billing.md)
- [Data, privacy, and security for Claude models in Microsoft Foundry](../../responsible-ai/claude-models/data-privacy.md)
