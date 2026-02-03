---
title: "Tool best practices for Microsoft Foundry Agent Service"
description: "Learn tool best practices for Foundry Agent Service: configure tool_choice, secure tool usage, and troubleshoot tool-calling issues."
author: aahill
ms.author: aahi
ms.date: 02/03/2026
ms.custom: references_regions, pilot-ai-workflow-jan-2026
ms.manager: nitinme
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
#CustomerIntent: As a developer building agents, I want to understand tool best practices so that I can configure reliable and secure tool usage.
---

# Tool best practices for Microsoft Foundry Agent Service

When you build agents in Microsoft Foundry Agent Service, tools extend what your agent can do—retrieving information, calling APIs, and connecting to external services. This article helps you configure tools effectively, control when the model calls them, and keep your data secure.

> [!TIP]
> In your agent instructions, describe what each tool is for and when to use it. For example:
>
> `When you need information from my indexed documents, use File Search. When you need to call an API, use the OpenAPI tool. When a tool call fails or returns no results, explain what happened and ask a follow-up question.`

## Prerequisites

- Access to a Foundry project in the Foundry portal with the **Azure AI Developer** role or equivalent permissions.
- A model deployed in the same project.
- Any required connections configured for the tools you plan to use (for example, Azure AI Search, SharePoint, or Bing grounding).

## Configure and validate tool usage

- Configure tools and connections in the Foundry tool catalog. See [Discover and manage tools in the Foundry tool catalog (preview)](tool-catalog.md).
- Review run traces to confirm when your agent calls tools and to inspect tool inputs and outputs. For end-to-end tracing setup, see [Trace your application](../../../how-to/develop/trace-application.md).

## Improve tool-calling reliability

### Control tool calling with `tool_choice`

Use `tool_choice` for the most deterministic control over tool calling.

- `auto`: The model decides whether to call tools.
- `required`: The model must call one or more tools.
- `none`: The model doesn't call tools.

For details, see `tool_choice` in [Foundry project REST (preview)](../../../reference/foundry-project-rest-preview.md).

### Write effective tool instructions

- Keep instructions specific and consistent with your tool setup.
- Tell the model what each tool is for.
- If you have multiple tools that overlap, add a decision rule (for example, “Use File Search before Web Search for internal content.”).

## Secure tool usage

Tools send and receive data outside the model. Reduce security and privacy risks with these practices:

- Treat tool outputs as untrusted input and validate critical values before acting on them.
- Send only the information required to complete the task.
- Don’t include keys, tokens, or other credentials in prompts.
- Avoid logging secrets in traces or application logs.
- If you connect to non-Microsoft services (for example, third-party MCP servers), review the considerations in [Discover and manage tools in the Foundry tool catalog (preview)](tool-catalog.md).
- If you need centralized routing and policy enforcement for MCP tools, see [Tools governance with AI Gateway (preview)](../how-to/tools/governance.md).

## Tool support by region and model

Region and model determine which tools are available to your agent.

> [!NOTE]
> In the tables below: **Yes** means fully supported, **No** means not supported, and **Limited** means partial support that varies by tool configuration. Check individual tool documentation for details.

The following table shows tool availability by [region](../../../openai/how-to/responses.md#region-availability).

> [!NOTE]
> This region availability table only accounts for service availability. You need to make sure the model you want to use is also available in the same region.

| Region Name        | Agent2Agent | Azure AI Search | Browser Automation | Code Interpreter | Computer Use | Fabric Data Agent | File Search | Function | Grounding with Bing Custom Search | Grounding with Bing Search | Image Generation | MCP | OpenAPI | SharePoint | Web Search |
|---------------------|-----|-----------------|---------------------|-------------------|--------------|--------------------|-------------|----------|------------------------------------|-----------------------------|-------------------|-----|---------|------------|------------|
| australiaeast       | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| brazilsouth         | yes | yes             | yes                 | yes               | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| canadaeast          | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| eastus              | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| eastus2             | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| francecentral       | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| germanywestcentral  | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| italynorth          | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| japaneast           | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| koreacentral        | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| northcentralus      | yes | yes             | yes                 | yes               | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| norwayeast          | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| polandcentral       | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southafricanorth    | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southcentralus      | yes | yes             | yes                 | no                | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southeastasia       | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southindia          | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| spaincentral        | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| swedencentral       | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| switzerlandnorth    | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| uaenorth            | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| uksouth             | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| westus              | yes | yes             | yes                 | yes               | no           | yes                | yes         | no      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| westus3             | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |

Tools are supported by the following models.

> [!NOTE]
> For the image generation tool, you need both the `gpt-image-1` model and a large language model (LLM) as the orchestrator in the same Microsoft Foundry project.

| Model | agent2agent | Azure AI Search | Browser Automation | Code Interpreter | Computer Use | Fabric Data Agent | File Search | Function | Grounding Bing Custom | Grounding Bing Search | Image Generation | MCP | OpenAPI | SharePoint | Web Search |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-5 | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-5-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-5-nano | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-5-chat | No | No | No | No | No | No | Yes | No | No | No | No | No | No | No | No |
| gpt-5-pro | Yes | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| o4-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| o3 | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| o3-mini | Yes | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes |
| o1 | Yes | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes |
| computer-use-preview | No | No | No | No | Yes | No | No | No | No | No | No | No | No | No | No |
| gpt-4.1 | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4.1-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4.1-nano | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4o | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4o-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-image-1 | No | No | No | No | No | No | No | No | No | No | Yes | No | No | No | No |
| DeepSeek-V3.0324 | No | Limited | No | Yes | No | Limited | Yes | Yes | Limited | Limited | No | Limited | No | Limited | No |
| DeepSeek-V3.1 | No | Limited | No | Yes | No | Limited | No | No | Limited | Limited | No | Limited | No | Limited | No |
| Llama-3.3-70B-Instruct | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No | No |
| Llama-4-Maverick-178-128E-Instr | No | Limited | No | No | No | Limited | Yes | Yes | Limited | Limited | No | Limited | No | Limited | No |
| grok-3-mini | No | Limited | No | No | No | Limited | No | Yes | Limited | Limited | No | Limited | No | Limited | No |
| grok-4-fast-non-reasoning | No | Limited | No | No | No | Limited | No | Yes | Limited | Limited | No | Limited | No | Limited | No |
| grok-4-fast-reasoning | No | Limited | No | No | No | Limited | No | Yes | Limited | Limited | No | Limited | No | Limited | No |

## Troubleshooting

Use these checks to resolve common issues:

- **Your agent doesn’t call a tool**:
    - Confirm the tool is attached to the agent.
    - Confirm the model supports the tool.
    - If you need deterministic behavior, set `tool_choice` to `required`.
    - Review run traces to confirm whether the model produced a tool call.
- **Tool calls return empty or irrelevant results**:
    - Improve tool descriptions and agent instructions.
    - For retrieval tools, ensure your data is ingested and searchable.
- **Tool calls fail**:
    - Verify tool configuration and authentication.
    - For MCP and OpenAPI tools, validate the endpoint is reachable and returns expected responses.

## FAQ

**How do I validate whether a tool was called?**

Review run traces to confirm whether your agent called a tool and to inspect tool inputs and outputs. For end-to-end tracing setup, see [Trace your application](../../../how-to/develop/trace-application.md).

**How do I make tool usage more reliable?**

Start with clear tool instructions. If you need deterministic tool calling, use `tool_choice`. For details, see [Control tool calling with `tool_choice`](#control-tool-calling-with-tool_choice).

## Related content

### Tool management

- [Discover and manage tools in the Foundry tool catalog (preview)](tool-catalog.md)
- [Tools governance with AI Gateway (preview)](../how-to/tools/governance.md)

### Retrieval and search tools

- [Azure AI Search](../how-to/tools/ai-search.md)
- [File search](../how-to/tools/file-search.md)
- [Web search (preview)](../how-to/tools/web-search.md)
- [Grounding with Bing tools](../how-to/tools/bing-tools.md)
- [SharePoint (preview)](../how-to/tools/sharepoint.md)

### Data and integration tools

- [Fabric data agent (preview)](../how-to/tools/fabric.md)
- [Model Context Protocol (MCP) (preview)](../how-to/tools/model-context-protocol.md)
- [OpenAPI tool](../how-to/tools/openapi.md)
- [Function calling](../how-to/tools/function-calling.md)

### Automation and generation tools

- [Code interpreter](../how-to/tools/code-interpreter.md)
- [Browser automation (preview)](../how-to/tools/browser-automation.md)
- [Computer Use (preview)](../how-to/tools/computer-use.md)
- [Image generation (preview)](../how-to/tools/image-generation.md)
- [Agent2Agent (A2A) tool (preview)](../how-to/tools/agent-to-agent.md)
