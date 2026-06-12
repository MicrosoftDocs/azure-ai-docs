---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/11/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

Anthropic's Claude models bring advanced conversational AI capabilities to Microsoft Foundry, providing state-of-the-art language understanding and generation for intelligent applications. Claude models excel at complex reasoning, code generation, and multimodal tasks including image analysis. This article describes the available Claude models, how they're hosted and billed, their API surface, capabilities, quotas, and best practices.

To deploy and call a Claude model, see [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md).

## Available Claude models

Claude models in Foundry include:

| Model family | Models |
|--|--|
| Claude Mythos | `claude-mythos-5`<sup>1</sup> (gated research preview), `claude-mythos-preview`<sup>1</sup> (gated research preview) |
| Claude Fable | `claude-fable-5` (preview) |
| Claude Opus | `claude-opus-4-8`<sup>2</sup> (preview), `claude-opus-4-7` (preview), `claude-opus-4-6` (preview), `claude-opus-4-5` (preview), `claude-opus-4-1` (preview) |
| Claude Sonnet | `claude-sonnet-4-6` (preview), `claude-sonnet-4-5` (preview) |
| Claude Haiku | `claude-haiku-4-5` (preview) |

<sup>1</sup> [!INCLUDE [claude-mythos-preview-restriction](claude-mythos-preview-restriction.md)]

<sup>2</sup> Follow the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-opus-47) to migrate Messages API code from Claude Opus 4.7 to Claude Opus 4.8.

For more details about the model capabilities, see [capabilities of Claude models](../concepts/models-from-partners.md#anthropic).

## API surface

Use the [Anthropic SDKs](https://docs.claude.com/en/api/client-sdks) and the following Claude APIs:

- [Messages API](https://docs.claude.com/en/api/messages): Send a structured list of input messages with text or image content. The model generates the next message in the conversation.
- [Token Count API](https://docs.claude.com/en/api/messages-count-tokens): Count the number of tokens in a message.
- [Files API](https://docs.claude.com/en/api/files-create): Upload and manage files for use with the Claude API without re-uploading content with each request.
- [Skills API](https://docs.claude.com/en/api/skills/create-skill): Create custom skills for Claude AI.

You can call the Messages API from the `anthropic` Python package, the `@anthropic-ai/foundry-sdk` JavaScript package, or directly through REST. The deployment endpoint follows the shape `https://<resource-name>.services.ai.azure.com/anthropic/v1/messages`, and REST and JavaScript clients use the `anthropic-version: 2023-06-01` header.

## Comparison of Claude models

Foundry supports Claude models through **global standard deployment**. Use the following table to compare models, then see [Capabilities](#capabilities) for details on the features referenced in the table.

> [!WARNING]
> 1M context beta on **Claude Sonnet 4.5** were retired on April 30, 2026.
>
> Starting May 1, 2026:
> - Requests **greater than 200K tokens** that include the `context-1m-2025-08-07` beta header on Sonnet 4.5 return an error.
> - Requests **200K tokens or fewer** remain unaffected, even with the header present.
>
> To migrate, remove the `context-1m-2025-08-07` beta header from your requests. For workloads that require 1M context, migrate to **Claude Sonnet 4.6** (where 1M context is generally available) or to **Claude Opus 4.6** or **Claude Opus 4.7** for higher-intelligence workloads.

| Model | Context window / Max output | Key capabilities | Best for |
|---|---|---|---|
| `claude-mythos-5`<sup>1</sup> (gated research preview) | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Microsoft Entra ID authentication only</li></ul> | <ul><li>Biology and life sciences</li><li>Cybersecurity (defensive use cases prioritized): vulnerability discovery, attack-surface auditing, red teaming, threat intelligence</li><li>Autonomous coding</li><li>Long-running agents</li></ul> |
| `claude-fable-5` (preview) | 1M / 128K | <ul><li>Adaptive thinking</li><li>Reasoning over entire codebases and multi-day project context</li><li>Longer independent work than any prior Claude model</li><li>Self verification</li><li>Sub-agent orchestration</li><li>Refusal `stop_reason` on dual-use safeguard policies<sup>2</sup></li></ul> | <ul><li>Cybersecurity</li><li>Autonomous coding</li><li>Long-running agents</li><li>Coding and agents, with deeper reasoning for enterprise workflows</li></ul> |
| `claude-mythos-preview`<sup>1</sup> (gated research preview) | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Microsoft Entra ID authentication only</li></ul> | <ul><li>Cybersecurity (defensive use cases prioritized)</li><li>Autonomous coding</li><li>Long-running agents</li></ul> |
| `claude-opus-4-8`<sup>3</sup> (preview) | 1M / 128K | <ul><li>Adaptive thinking with `xhigh` effort level</li><li>Reasoning over entire codebases and multi-day project context</li><li>High-resolution image input (up to 2576px / 3.75MP)</li></ul> | <ul><li>Coding</li><li>Long-running agents</li><li>Financial analysis</li><li>Cybersecurity</li><li>Computer use</li></ul> |
| `claude-opus-4-7` (preview) | 1M / 128K | <ul><li>Adaptive thinking</li><li>Reasoning over entire codebases<li>High-resolution image input (up to 2576px / 3.75MP)</li></ul> | <ul><li>Coding</li><li>Enterprise workflows</li><li>Long-running agents</li><li>Multimodal reasoning</li><li>Financial analysis</li><li>Cybersecurity</li></ul> |
| `claude-opus-4-6` (preview) | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples)</li></ul> | <ul><li>Coding</li><li>Enterprise agents</li></ul> |
| `claude-opus-4-5` (preview) | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples)</li></ul> | <ul><li>Coding</li><li>Agents</li><li>Computer use</li><li>Enterprise workflows</li></ul> |
| `claude-opus-4-1` (preview) | 200K / 32K | <ul><li>Extended thinking</li><li>Image and text input</li></ul> | <ul><li>Coding</li><li>Long-running tasks</li></ul> |
| `claude-sonnet-4-6` (preview) | 1M / 128K | <ul><li>Adaptive thinking</li><li>Image and text input</li><li>Computer use</li><li>Advanced tool use (search, programmatic calling, examples)</li></ul> | <ul><li>Coding</li><li>Agents</li><li>Enterprise workflows</li></ul> |
| `claude-sonnet-4-5` (preview) | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li><li>Computer use</li></ul> | <ul><li>Agents and complex, long-horizon tasks</li><li>High-volume workloads</li></ul> |
| `claude-haiku-4-5` (preview) | 200K / 64K | <ul><li>Extended thinking</li><li>Image and text input</li></ul> | <ul><li>Coding</li><li>Agents</li></ul> |

<sup>1</sup> [!INCLUDE [claude-mythos-preview-restriction](claude-mythos-preview-restriction.md)]

<sup>2</sup> Claude Fable 5 applies additional input/output classifiers that may refuse requests whose content triggers dual-use safeguard policies. When a refusal occurs, the request returns a successful (200) response with a refusal indicator `stop_reason: "refusal"` instead of model-generated content. You're not billed for input tokens that are refused.

<sup>3</sup> Follow the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-opus-47) to migrate Messages API code from Claude Opus 4.7 to Claude Opus 4.8.

## Capabilities

Claude models in Foundry expose two kinds of capabilities: core capabilities for processing, analyzing, and generating content, and tools that let Claude interact with external systems.

### Core capabilities

Core capabilities enhance Claude's fundamental abilities for processing, analyzing, and generating content. Foundry supports the following core capabilities for Claude:

- **Large context window:** An extended context window that processes larger documents and longer conversations.
- **Image and text input:** Strong vision for analyzing charts, graphs, technical diagrams, reports, and other visual assets.
- **Code generation:** Advanced code generation, analysis, and debugging.
- **Agent skills:** Extend Claude's capabilities with skills.
- **Citations:** Ground Claude's responses in source documents.
- **PDF support:** Process and analyze text and visual content from PDF documents.
- **Context editing:** Automatically manage conversation context with configurable strategies.
- **Extended thinking:** Enhanced reasoning for complex tasks, available with all Claude models. The following table shows which `thinking` parameter types each model supports. The `adaptive` type allows the model to decide whether to think, based on query complexity and effort level.

    | Model | `adaptive` | `enabled` | `disabled` |
    |---|:---:|:---:|:---:|
    | `claude-mythos-5` | Yes | No | No |
    | `claude-fable-5` | Yes | No | No |
    | `claude-mythos-preview` | Yes | Yes | No |
    | `claude-opus-4-8` | Yes | No | Yes |
    | `claude-opus-4-7` | Yes | No | Yes |
    | `claude-opus-4-6` | Yes | Yes | Yes |
    | `claude-sonnet-4-6` | Yes | Yes | Yes |

- **Effort:** Ability to control the quality/cost tradeoff for responses. Use this parameter with or without enabling thinking. The following table shows which `effort` levels each model supports. The `xhigh` level produces the same result as `max`.

    | Model | `low` | `medium` | `high` | `max` | `xhigh` |
    |---|:---:|:---:|:---:|:---:|:---:|
    | `claude-mythos-5` | Yes | Yes | Yes | No | Yes |
    | `claude-fable-5` | Yes | Yes | Yes | No | Yes |
    | `claude-opus-4-8` | Yes | Yes | Yes | Yes | Yes |
    | `claude-opus-4-7` | Yes | Yes | Yes | Yes | Yes |
    | `claude-opus-4-6` | Yes | Yes | Yes | Yes | No |
    | `claude-sonnet-4-6` | Yes | Yes | Yes | Yes | No |

### Tools

Tools enable Claude to interact with external systems, execute code, and perform automated tasks. Foundry supports the following tools for Claude:

- **MCP connector:** Connect to remote MCP servers directly from the Messages API without a separate MCP client.
- **Memory:** Store and retrieve information across conversations. Build knowledge bases over time, maintain project context, and learn from past interactions.
- **Web fetch:** Retrieve full content from specified web pages and PDF documents for in-depth analysis.

For a full list of supported capabilities and tools, see [Claude's features overview](https://docs.claude.com/en/docs/build-with-claude/overview).

## Agent support

- [Microsoft Agent Framework](/agent-framework/user-guide/agents/agent-types/anthropic-agent) supports creating agents that use Claude models.
- Build custom AI agents with the [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview).

## How Claude models are hosted and billed

Claude is offered through [Foundry Models from partners and community](../concepts/models-from-partners.md). Models from partners and community that aren't sold by Azure are Non-Microsoft Products under the Product Terms.

Deploying a Claude model requires an Azure Marketplace subscription. Ensure that you have the [permissions required to subscribe to model offerings](../how-to/configure-marketplace.md) before you deploy.

## Quotas, rate limits, and regions

Claude models are available for [Global Standard](../concepts/deployment-types.md#global-standard) deployment in the following regions:

- **East US2**
- **Sweden Central**

Rate limits for Claude models in Foundry are measured in Tokens Per Minute (TPM) and Requests Per Minute (RPM). The values are different depending on your subscription type, as listed in the following table. To increase your quota beyond the default limits, submit a request through the [quota increase request form](https://aka.ms/oai/stuquotarequest).

# [Pay-as-yo-go](#tab/pay-go)

#### Pay-as-you-go

| Model             | Deployment type | RPM | TPM    |
|:------------------|:----------------|:---:|:------:|
| claude-fable-5    | Global Standard | 0   | 0      |
| claude-opus-4-8   | Global Standard | 40  | 40,000 |
| claude-opus-4-7   | Global Standard | 40  | 40,000 |
| claude-opus-4-6   | Global Standard | 40  | 40,000 |
| claude-opus-4-5   | Global Standard | 40  | 40,000 |
| claude-opus-4-1   | Global Standard | 40  | 40,000 |
| claude-sonnet-4-6 | Global Standard | 80  | 80,000 |
| claude-sonnet-4-5 | Global Standard | 80  | 80,000 |
| claude-haiku-4-5  | Global Standard | 80  | 80,000 |

# [Enterprise and MCA-E](#tab/enterprise)

#### Enterprise and MCA-E

| Model             | Deployment type | RPM   | TPM       |
|:------------------|:----------------|:-----:|:---------:|
| claude-fable-5    | Global Standard | 2,000 | 2,000,000 |
| claude-opus-4-8   | Global Standard | 2,000 | 2,000,000 |
| claude-opus-4-7   | Global Standard | 2,000 | 2,000,000 |
| claude-opus-4-6   | Global Standard | 2,000 | 2,000,000 |
| claude-opus-4-5   | Global Standard | 2,000 | 2,000,000 |
| claude-opus-4-1   | Global Standard | 2,000 | 2,000,000 |
| claude-sonnet-4-6 | Global Standard | 4,000 | 4,000,000 |
| claude-sonnet-4-5 | Global Standard | 4,000 | 4,000,000 |
| claude-haiku-4-5  | Global Standard | 4,000 | 4,000,000 |

# [Free Trial](#tab/free)

#### Free Trial

| Model             | Deployment type | RPM | TPM |
|:------------------|:----------------|:---:|:---:|
| claude-fable-5    | Global Standard | 0   | 0   |
| claude-opus-4-8   | Global Standard | 0   | 0   |
| claude-opus-4-7   | Global Standard | 0   | 0   |
| claude-opus-4-6   | Global Standard | 0   | 0   |
| claude-opus-4-5   | Global Standard | 0   | 0   |
| claude-opus-4-1   | Global Standard | 0   | 0   |
| claude-sonnet-4-6 | Global Standard | 0   | 0   |
| claude-sonnet-4-5 | Global Standard | 0   | 0   |
| claude-haiku-4-5  | Global Standard | 0   | 0   |

---


## Responsible AI considerations

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
- [Data, privacy, and security for Claude models in Microsoft Foundry (preview)](../../responsible-ai/claude-models/data-privacy.md)