---
title: Self-host OpenAI Responses endpoints
description: Use the Agent Framework Responses helpers in your application-owned server.
zone_pivot_groups: programming-languages
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 09/01/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# Self-host OpenAI Responses endpoints

:::zone pivot="programming-language-csharp"

> [!NOTE]
> Self-hosting helpers for OpenAI Responses endpoints in .NET are coming soon.

:::zone-end

:::zone pivot="programming-language-go"

> [!NOTE]
> Self-hosting helpers for OpenAI Responses endpoints are not currently available for Go.

:::zone-end

:::zone pivot="programming-language-python"

Use `agent-framework-hosting-responses` to convert OpenAI Responses-shaped requests and responses at an endpoint your application owns. Your server chooses the web framework, route, authentication, authorization, request options, and session storage.

```bash
pip install --pre agent-framework agent-framework-foundry agent-framework-hosting agent-framework-hosting-responses azure-identity
```

The FastAPI sample is one implementation. The same helpers work with Django, Flask, Starlette, Azure Functions, or another framework.

## Host an agent endpoint

This sample converts the request to Agent Framework run values, applies an application-defined option allowlist, and persists the updated session under the newly created response ID.

:::code language="python" source="~/../agent-framework-code/python/samples/04-hosting/af-hosting/local_responses/app.py" range="107-179":::

`AgentState` resolves the target and loads or creates a session. Save the session after the run, or after a streaming run finishes, because the run updates it.

For the complete application, including the agent definition and request-option allowlist, see the [local Responses sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/af-hosting/local_responses).

## Understand response usage conversion

For agent and workflow responses, the hosting package preserves an SDK-valid native OpenAI `ResponseUsage` object unchanged when one is available. It doesn't merge native Responses usage with Agent Framework `UsageDetails`.

When native usage isn't available, the package can reconstruct Responses usage from these semantically matching Agent Framework fields:

| Usage value | Agent Framework field |
| --- | --- |
| Input tokens | `input_token_count` |
| Output tokens | `output_token_count` |
| Cache-read input tokens | `cache_read_input_token_count` |
| Cache-write input tokens | `cache_creation_input_token_count` |
| Reasoning output tokens | `reasoning_output_token_count` |

Explicit zero values are preserved. If `total_tokens` is absent while both input and output counts are present, the package derives it as input plus output.

If the available Agent Framework usage is incomplete or semantically inconsistent with the Responses schema, the package omits usage. It doesn't guess, copy one counter into another, or fail an otherwise successful response. A malformed scalar count remains an error.

This reconstruction is intentionally lossy because Agent Framework usage is provider-neutral and OpenAI Responses usage has a richer, provider-specific shape. Provider-specific counters reported by a hosted agent, such as Anthropic-specific usage, therefore might not appear in the response received by the calling application. This conversion doesn't provide interoperability between different versions of the OpenAI SDK running in the same process.

## Host a workflow endpoint

`WorkflowState` resolves the workflow, but your application owns checkpoint storage and the mapping from a response ID to a checkpoint. This sample restores the checkpoint selected by an authorized `previous_response_id`, then saves a cursor for the next response.

:::code language="python" source="~/../agent-framework-code/python/samples/04-hosting/af-hosting/local_responses_workflow/app.py" range="220-272":::

The sample's file-backed storage is for local development. Use durable storage when replicas can restart or scale out.

> [!IMPORTANT]
> Treat `previous_response_id` and `conversation_id` as untrusted input. Authenticate and authorize the caller before using either ID to load or save a session or checkpoint.

For the broader wire format, see [OpenAI-compatible endpoints](openai-endpoints.md).

## Next steps

> [!div class="nextstepaction"]
> [Add Telegram](telegram.md)

**Go deeper:**

- [Self-hosting overview](index.md)
- [A2A](a2a/index.md)
- [MCP](mcp.md)
- [Foundry Hosted Agents](../foundry-hosted-agent.md)

:::zone-end
