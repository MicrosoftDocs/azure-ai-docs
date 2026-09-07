---
title: Google Gemini
description: Use Google Gemini Developer API or Vertex AI models with Agent Framework agents.
zone_pivot_groups: programming-languages
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 09/04/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

<!--
  Language parity table - keep in sync when adding/removing sections.

  | Section              | C# | Python | Go | Notes                       |
  |----------------------|:--:|:------:|:--:|-----------------------------|
  | Gemini client setup  | ✅ |   ✅   | ✅ |                             |
  | Function tools       | ✅ |   ✅   | ✅ |                             |
  | Streaming            | ✅ |   ✅   | ✅ |                             |
  | Request failures     | ❌ |   ✅   | ❌ | Python SDK exception mapping |
  | Gemini hosted tools  | ❌ |   ✅   | ❌ | Python factories documented |
-->

# Google Gemini

Google Gemini can back an Agent Framework agent through the Gemini Developer API or Vertex AI. The provider-specific client handles authentication and Gemini request options while Agent Framework owns the agent definition and orchestration.

> [!IMPORTANT]
> Google Gemini and Vertex AI are third-party systems. Review service terms, data handling, regional boundaries, model access, and usage costs before sending application data.

:::zone pivot="programming-language-csharp"

## Install a Gemini `IChatClient`

The .NET sample demonstrates the official Google GenAI client and the community `Mscc.GenerativeAI.Microsoft` implementation.

```bash
dotnet add package Google.GenAI
dotnet add package Mscc.GenerativeAI.Microsoft
dotnet add package Microsoft.Agents.AI --prerelease
```

## Configuration

```bash
GOOGLE_GENAI_API_KEY="<google-ai-studio-api-key>"
GOOGLE_GENAI_MODEL="gemini-2.5-flash"
```

:::code language="csharp" source="~/../agent-framework-code/dotnet/samples/02-agents/AgentProviders/google-gemini/Agent_With_GoogleGemini/Program.cs" range="10-34":::

Choose one `IChatClient` implementation and configure its Gemini Developer API or Vertex AI authentication.

:::zone-end

:::zone pivot="programming-language-python"

## Install the package

```bash
pip install agent-framework-gemini --pre
```

## Configuration

Use either the Gemini Developer API:

```bash
GEMINI_API_KEY="<api-key>"
GEMINI_MODEL="gemini-2.5-flash"
# GOOGLE_API_KEY and GOOGLE_MODEL are also supported.
```

Or configure Vertex AI:

```bash
GOOGLE_GENAI_USE_VERTEXAI="true"
GOOGLE_CLOUD_PROJECT="<project-id>"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_MODEL="gemini-2.5-flash"
```

`GeminiChatClient` supports streaming, function tools, structured output, extended thinking, and provider-hosted tools.

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/providers/gemini/gemini_basic.py" range="37-75":::

### Handle request failures

For streaming and non-streaming runs, Gemini SDK request failures are exposed through Agent Framework exceptions. HTTP 401 and 403 failures raise `ChatClientInvalidAuthException`, other HTTP 4xx failures raise `ChatClientInvalidRequestException`, and all other provider failures raise `ChatClientException`.

Catch `ChatClientException` when the same error handling should apply across chat providers.

### Include thought summaries

The [extended thinking sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/gemini/gemini_advanced.py) shows how to configure `ThinkingConfig`. To receive Gemini thought summaries, set `include_thoughts=True` in the thinking configuration:

```python
options: GeminiChatOptions = {
    "thinking_config": ThinkingConfig(include_thoughts=True, thinking_budget=2048),
}
```

When Gemini returns a thought summary, `GeminiChatClient` adds it to the response as `Content` with `type == "text_reasoning"`. Read the summary from `content.text`.

For a run without streaming, filter the `contents` of each item in `result.messages`. For a streaming run, filter each `chunk.contents`. Text accessors such as `result.text` and `chunk.text` include only `text` content, so inspect the content collections when your app needs reasoning summaries.

The package includes factories for Google Search grounding, Google Maps grounding, code execution, file search, and MCP.

### Google Search grounding

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/providers/gemini/gemini_with_google_search.py" range="16-48":::

:::zone-end

:::zone pivot="programming-language-go"

The Go SDK provides `geminiprovider` for Gemini inference. Create a standard `*agent.Agent` through the provider-specific constructor.

See the [Gemini provider package](https://github.com/microsoft/agent-framework-go/tree/main/provider/geminiprovider) and [examples](https://github.com/microsoft/agent-framework-go/tree/main/examples/02-agents/providers/gemini).

:::zone-end

## Tools

| Tool | C# | Python | Go | Notes |
|---|:---:|:---:|:---:|---|
| [Function Tools](../../../agents/tools/function-tools.md) | ✅ | ✅ | ✅ | Standard model function calling. |
| [Tool Approval](../../../agents/tools/tool-approval.md) | ✅ | ✅ | ✅ | Applied by the framework tool loop. |
| [Code Interpreter](../../../agents/tools/code-interpreter.md) | ❌ | ✅ | ❌ | `GeminiChatClient.get_code_interpreter_tool()`. |
| [File Search](../../../agents/tools/file-search.md) | ❌ | ✅ | ❌ | `GeminiChatClient.get_file_search_tool()`. |
| [Web Search](../../../agents/tools/web-search.md) | ❌ | ✅ | ❌ | Google Search grounding through `get_web_search_tool()`. |
| Google Maps grounding | ❌ | ✅ | ❌ | `GeminiChatClient.get_maps_grounding_tool()`. |
| [Hosted MCP Tools](../../../agents/tools/hosted-mcp-tools.md) | ❌ | ✅ | ❌ | `GeminiChatClient.get_mcp_tool()`. |
| [Local MCP Tools](../../../agents/tools/local-mcp-tools.md) | ✅ | ✅ | ✅ | Runs in the application process. |

## Next steps

> [!div class="nextstepaction"]
> [ONNX](onnx.md)
