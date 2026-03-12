---
title: "Agent tools overview for Microsoft Foundry Agent Service"
description: "Explore the tools available for agents in Foundry Agent Service, including built-in tools, web search, custom options, and the Foundry tool catalog. Get started today."
author: aahill
ms.author: aahi
ms.date: 03/12/2026
ms.manager: nitinme
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# Agent tools overview for Foundry Agent Service

Tools extend what your agents can do in Microsoft Foundry Agent Service. An agent on its own can generate text, but tools let it take action — searching the web, running code, querying your data, or calling your own APIs. This article explains what tools are, the types of tools available, how to use a tool in an agent, and how to manage authentication. It also introduces the Foundry tool catalog where you discover and configure tools. To use tools, you need access to a Foundry project and permission to manage tools in that project.

> [!NOTE]
> The Foundry tool catalog and the core tools framework are generally available. Some individual tools are still in preview, as noted in the tool listings throughout this article. Each tool's own page also indicates its preview status with a banner. Preview tools are subject to [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## What are tools

A *tool* is a capability that an agent can invoke during a conversation to perform a specific task. When an agent receives a user message, the model decides whether to call a tool based on the agent's instructions and the available tool definitions. The agent sends the tool request, your application or the service executes it, and the result flows back into the conversation so the agent can continue with accurate, up-to-date information.

Tools enable agents to go beyond text generation. For example, an agent can:

- Search the web for current information before answering.
- Run Python code to analyze a dataset and generate a chart.
- Query a vector store of your documents to ground its response in your data.
- Call an external API to look up a customer record or create a support ticket.

## Types of tools

Foundry Agent Service provides two categories of tools: built-in tools that are ready to use after basic configuration, and custom tools that let you bring your own capabilities.

### Built-in tools

Built-in tools are preconfigured capabilities provided by Foundry Agent Service. You enable them on your agent and the service handles execution. No external hosting or custom code is required.

The most commonly used built-in tools include:

- **[Web search](../how-to/tools/web-search.md)** — Add web search to your agent. The agent retrieves real-time information from the public web and returns answers with inline citations. This is the recommended way to add web grounding. For advanced scenarios such as market-specific filtering, see [Grounding with Bing tools](../how-to/tools/bing-tools.md) and the [web grounding overview](../how-to/tools/web-overview.md).
- **[Code Interpreter](../how-to/tools/code-interpreter.md)** — Let agents write and run Python code in a sandboxed environment for data analysis, math, and chart generation.
- **[File Search](../how-to/tools/file-search.md)** — Augment agents with knowledge from uploaded files or proprietary documents using vector search.
- **[Function calling](../how-to/tools/function-calling.md)** — Define custom functions that the agent can call. Your application executes the function and returns the result.

For the complete list of built-in tools, see [All built-in tools](#all-built-in-tools).

### Custom tools

Custom tools let you extend your agent with your own APIs, services, or other agents. Use custom tools when built-in tools don't cover your scenario.

The most common custom tool options include:

- **[Model Context Protocol (MCP)](../how-to/tools/model-context-protocol.md)** — Connect your agent to tools hosted on an MCP server endpoint. Best for tools shared across multiple agents or maintained by a different team.
- **[Agent-to-Agent (A2A) (preview)](../how-to/tools/agent-to-agent.md)** — Connect your agent to other agents through A2A-compatible endpoints for cross-agent communication.
- **[OpenAPI tool](../how-to/tools/openapi.md)** — Connect your agent to external HTTP APIs using an OpenAPI 3.0 or 3.1 specification.

For the complete list of custom tool options, see [All custom tools](#all-custom-tools).

## Use a tool in an agent

To add a tool to an agent, include it in the agent's tool list when you create or update the agent definition. The following example creates an agent with the web search tool enabled and sends a query:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, WebSearchTool

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create an agent with web search enabled
agent = project.agents.create_version(
    agent_name="web-search-agent",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_NAME"],
        instructions="You are a helpful assistant that can search the web.",
        tools=[WebSearchTool()],
    ),
)

# Start a conversation and send a query
openai = project.get_openai_client()
response = openai.responses.create(
    input="What are the latest updates to Microsoft Foundry?",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)
print(response.output_text)
```

Each tool type has its own configuration. For detailed setup and code samples in all supported languages, see the individual tool how-to guides linked in the [types of tools](#types-of-tools) section.

### Customize tool behavior at runtime with structured inputs

By default, tool configurations such as file IDs, vector store IDs, and MCP server endpoints are fixed when you create the agent. *Structured inputs* let you use handlebar templates (`{{variable_name}}`) in tool properties so you can override these values at runtime without creating a new agent version.

Structured inputs are useful when:

- Different users need different vector stores or files based on their context.
- You want to reuse the same agent definition across environments (development, staging, production).
- MCP server endpoints or authentication tokens vary per request.

The following tool properties support handlebar templates:

| Tool type | Property | Description |
| --------- | --------- | --------- |
| `file_search` | `vector_store_ids` | Array of vector store IDs. Empty values are stripped at runtime. |
| `code_interpreter` | `container`, `container.file_ids` | Container ID or file IDs within an auto container. Empty values are stripped at runtime. |
| `mcp` | `server_label`, `server_url`, `headers` | MCP server label, URL, and HTTP header values. |

For example, an agent definition with a templated vector store:

```json
{
  "tools": [
    {
      "type": "file_search",
      "vector_store_ids": ["vs_base_kb", "{{customer_kb}}"]
    }
  ],
  "structured_inputs": {
    "customer_kb": {
      "description": "Vector store ID for the customer's knowledge base",
      "required": true,
      "schema": { "type": "string" }
    }
  }
}
```

At runtime, provide the actual value:

```json
{
  "agent": { "type": "agent_reference", "name": "support-agent", "version": "1" },
  "input": [{ "type": "text", "text": "How do I upgrade my account?" }],
  "structured_inputs": {
    "customer_kb": "vs_premium_kb_2024"
  }
}
```

## Manage authentication for tools

Different tools require different authentication approaches. Understanding these options helps you connect tools securely.

**Built-in tools** authenticate through Foundry Agent Service automatically. Most built-in tools such as Code Interpreter and File Search require no extra authentication configuration. Tools that connect to external data sources (for example, Azure AI Search or SharePoint) use the connections configured in your Foundry project.

**MCP servers** support multiple authentication methods depending on the server. Options include key-based authentication (API key or token), Microsoft Entra authentication (managed identity), and OAuth for user-level identity passthrough. When in doubt, start with Microsoft Entra authentication if the MCP server supports it, because it eliminates the need to manage secrets and provides built-in token rotation. For detailed setup steps, see [Set up MCP server authentication](../how-to/mcp-authentication.md).

**OpenAPI tools** support anonymous, API key, and managed identity authentication. Choose the method that matches your API's requirements. For details, see [Connect agents to OpenAPI tools](../how-to/tools/openapi.md).

> [!TIP]
> Treat all credentials as secrets. Only provide the minimum required headers, don't include credentials in prompts, and review the provider's data handling practices. For governance controls such as rate limits and IP restrictions on MCP tools, see [Govern MCP tools by using an AI gateway](../how-to/tools/governance.md).

## All built-in tools

The following table lists all built-in tools available in Foundry Agent Service.

| Tool | Description |
| --------- | --------- |
| [Web search](../how-to/tools/web-search.md) | Retrieve real-time information from the public web and return answers with inline citations. |
| [Code Interpreter](../how-to/tools/code-interpreter.md) | Write and run Python code in a sandboxed environment. |
| [Custom Code Interpreter (preview)](../how-to/tools/custom-code-interpreter.md) | Customize the code interpreter's resources, Python packages, and Container Apps environment. |
| [File Search](../how-to/tools/file-search.md) | Augment agents with knowledge from uploaded files or proprietary documents. |
| [Azure AI Search](../how-to/tools/ai-search.md) | Ground agents with data from an existing Azure AI Search index. |
| [Function calling](../how-to/tools/function-calling.md) | Define custom functions that the agent can call. Your app executes the function and returns the result. |
| [Image Generation (preview)](../how-to/tools/image-generation.md) | Generate images as part of conversations and workflows. |
| [Browser Automation (preview)](../how-to/tools/browser-automation.md) | Perform browser tasks through natural language prompts. |
| [Computer Use (preview)](../how-to/tools/computer-use.md) | Interact with computer systems through their user interfaces. |
| [Microsoft Fabric (preview)](../how-to/tools/fabric.md) | Connect to a [Microsoft Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312815) for data analysis. |
| [SharePoint (preview)](../how-to/tools/sharepoint.md) | Chat with private documents stored in SharePoint. |

> [!TIP]
> For advanced web grounding scenarios, see [Grounding with Bing tools](../how-to/tools/bing-tools.md) and the [web grounding overview](../how-to/tools/web-overview.md).

## All custom tools

The following table lists all custom tool options for connecting your own capabilities to an agent.

| Tool | Description |
| --------- | --------- |
| [Model Context Protocol (MCP)](../how-to/tools/model-context-protocol.md) | Connect your agent to tools hosted on an MCP server endpoint. |
| [OpenAPI tool](../how-to/tools/openapi.md) | Connect your agent to external APIs using an OpenAPI 3.0 or 3.1 specification. |
| [Agent-to-Agent (A2A) (preview)](../how-to/tools/agent-to-agent.md) | Connect your agent to other agents through A2A-compatible endpoints. |

## Key concepts

Use these definitions to keep terminology consistent:

| Term | Meaning |
| --------- | --------- |
| Foundry Tools | The portal experience where you discover, configure, and manage tools for agents and workflows. |
| Tool catalog | The browsable list of available tools, including public and organizational tools. |
| Private tool catalog | An organization-scoped catalog for tools that only users in your organization can discover and configure. |
| MCP server | A server that exposes tools by using the Model Context Protocol (MCP). |
| Remote MCP server | An MCP server hosted by the publisher. You configure it by providing the required settings, such as an endpoint and authentication details. |
| Local MCP server | An MCP server you host yourself, then connect to Foundry by providing its remote endpoint. |
| Custom tool | A tool you add by providing your own endpoint or specification, such as an MCP endpoint, an OpenAPI spec, or Agent-to-Agent (A2A) endpoints. |

> [!NOTE]
> If you're interested in bringing your official, remote MCP servers to all Foundry customers, fill out this [form](https://forms.office.com/r/EEvMNceMRU).

<!-- The verbiage in the following section is required. Do not remove or modify. -->
## Considerations for using non-Microsoft services and servers 

Your use of connected non-Microsoft services and servers ("non-Microsoft services") is subject to the terms between you and the service provider. Non-Microsoft services are non-Microsoft products under your agreement governing use of Microsoft online services. When you connect to non-Microsoft services, some of your data (such as prompt content) is sent to the non-Microsoft service, or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use.

Third parties (not Microsoft) create the non-Microsoft services, including remote MCP servers, that you choose to connect. Microsoft doesn't test or verify these servers. Microsoft has no responsibility to you or others in relation to your use of any non-Microsoft services.

Carefully review and track the MCP servers you add to Foundry Agent Service. Rely on servers hosted by trusted service providers themselves rather than proxies.

The MCP tool can pass custom headers that a remote MCP server might require for authentication. Treat any credentials as secrets:

- Only provide the minimum required headers.
- Don't include credentials in prompts.
- If you log requests for auditing, avoid logging secrets or sensitive prompt content.
- Review the provider's data handling practices, including retention and data location.

## Discover and manage tools in the portal

In the Foundry portal, go to your project and select **Build** > **Tools** to open Foundry Tools. From there, you can browse the tool catalog, configure tools, and add them to agents or workflows. If you need tools that are only visible within your organization, create a [private tool catalog](../how-to/private-tool-catalog.md).

To explore tools while you build, use the Agents playground. For more information, see [Microsoft Foundry Playgrounds](../../concepts/concept-playgrounds.md).

### Tool types in the catalog

The tool catalog includes three types of entries:

**Remote MCP server**: The publisher hosts the server and provides a static or dynamic endpoint. Follow the configuration guidance to provide the required settings, such as an endpoint and authentication details.

**Local MCP server**: You host the server yourself, then connect it to Foundry by providing its endpoint. To build and register your own server, see [Build and register an MCP server](../../mcp/build-your-own-mcp-server.md). To connect an MCP endpoint to an agent, see [Connect to MCP servers](../how-to/tools/model-context-protocol.md).

**Custom**: MCP servers converted from Azure Logic App Connectors. These servers require additional [configuration](https://aka.ms/FoundryCustomTool) to convert to remote MCP servers.

### Filter and search

Foundry Tools provides the following filters to help you find the right tools:

| Filter | Description |
| --------- | --------- |
| Publisher | Microsoft or non-Microsoft publisher |
| Category | Categories such as databases, analytics, web, and more |
| Registry | **Public**: Public remote and local MCP servers in the catalog.<br>**Logic Apps connectors**: Azure Logic Apps connectors that you convert to remote MCP servers for use in a private tool catalog. |
| Supported authentication | Authentication method an MCP server supports. For more information, see [Authentication methods](https://aka.ms/FoundryMCPAuth). |

:::image type="content" source="../media/tool-catalog/tool-example.png" alt-text="Screenshot of a tool details page in the Foundry portal showing configuration and setup information." lightbox="../media/tool-catalog/tool-example.png":::

When you select a tool, Foundry Tools shows the setup details you need to configure it.

### Manage configured tools

In your tools list, you can find the tools you configured, along with details such as endpoints and authentication settings. You can also add tools to agents and workflows.

Before you delete a tool, check which agents or workflows use it. Deleting a tool can break runs that depend on it.

<!--
:::image type="content" source="../media/tool-catalog/tool-view.png" alt-text="A screenshot showing the tools list in the Foundry portal."lightbox="../media/tool-catalog/tool-view.png" :::
-->

## Availability and limitations

Tool availability varies by model and region.

For the latest model and region support details across tools, see [Best practices for using tools in Foundry Agent Service](tool-best-practice.md).

## Troubleshooting

Use these checks to resolve common issues:

- **You can't find the tool catalog**: Confirm you're in the correct project, and then go to **Build** > **Tools**.
- **A tool is visible but you can't configure it**: Review the tool's required authentication and configuration inputs, and verify you have access to any dependent services.
- **Your agent doesn't call a tool**: Use the validation guidance in [Best practices for using tools in Foundry Agent Service](tool-best-practice.md).

## Related content

- [Tool best practices for Foundry Agent Service](tool-best-practice.md)
- [Set up MCP server authentication](../how-to/mcp-authentication.md)
- [Govern MCP tools by using an AI gateway](../how-to/tools/governance.md)
- [Create a private tool catalog](../how-to/private-tool-catalog.md)
- [Build and register an MCP server](../../mcp/build-your-own-mcp-server.md)
- [Foundry MCP Server best practices and security guidance](../../mcp/security-best-practices.md)
