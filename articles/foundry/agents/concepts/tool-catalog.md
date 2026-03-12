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

Microsoft Foundry Agent Service provides a set of tools that extend what your agents can do - from searching the web and running code to calling your own APIs. This article explains the tools available, helps you choose the right one for your scenario, and introduces the Foundry tool catalog where you discover and manage them. To use these tools, you need access to a Foundry project in the portal and permission to manage tools in that project.

## Available tools

The following tools are available for your agents. Some are built in and ready to use after basic configuration. Others let you bring your own endpoints or code.

### Web search

To add web search to your agent, use the web search tool. The agent retrieves real-time information from the public web and returns cited answers.

| Tool | Description |
| --------- | --------- |
| [Web search (preview)](../how-to/tools/web-search.md) | Add web search to your agent. The agent retrieves real-time information from the public web and returns answers with inline citations. This tool is the recommended way to add web grounding. |

> [!TIP]
> For advanced scenarios such as market-specific filtering or custom search indexes, see [Grounding with Bing tools](../how-to/tools/bing-tools.md) and the [web grounding overview](../how-to/tools/web-overview.md).

### Custom tools

When built-in tools aren't enough, add your own custom capabilities to your agent. Two main approaches exist depending on your needs.

**Option 1 (recommended): Define tools in your agent code.** When you use the Microsoft Foundry SDK or frameworks like Agent Framework or LangGraph, you register custom functions directly as tools. The agent calls your function and you return the result. This approach works best for tools tightly coupled to your agent logic.

See [Use function calling with Foundry agents](../how-to/tools/function-calling.md).

**Option 2: Deploy as a Model Context Protocol (MCP) server.** Package your tools in an MCP server and connect the endpoint to your agent. This approach works best for tools shared across multiple agents or maintained by a different team.

See [Connect to MCP servers](../how-to/tools/model-context-protocol.md).

You can also connect agents to external APIs or other agents:

| Tool | Description |
| --------- | --------- |
| [OpenAPI tool](../how-to/tools/openapi.md) | Connect your agent to external APIs using an OpenAPI 3.0 or 3.1 specification. |
| [Agent-to-Agent (A2A) tool (preview)](../how-to/tools/agent-to-agent.md) | Connect your agent to other agents through A2A-compatible endpoints. |

### Other built-in tools

These built-in tools cover common scenarios such as search, retrieval, code execution, and more.

| Tool | Description |
| --------- | --------- |
| [Azure AI Search](../how-to/tools/ai-search.md) | Ground agents with data from an existing Azure AI Search index. |
| [File Search](../how-to/tools/file-search.md) | Augment agents with knowledge from uploaded files or proprietary documents. |
| [Code Interpreter](../how-to/tools/code-interpreter.md) | Let agents write and run Python code in a sandboxed environment. |
| [Custom Code Interpreter (preview)](../how-to/tools/custom-code-interpreter.md) | Customize the code interpreter's resources, Python packages, and Container Apps environment. |
| [Image Generation (preview)](../how-to/tools/image-generation.md) | Generate images as part of conversations and workflows. |
| [Browser Automation (preview)](../how-to/tools/browser-automation.md) | Perform browser tasks through natural language prompts. |
| [Computer Use (preview)](../how-to/tools/computer-use.md) | Interact with computer systems through their user interfaces. |
| [Microsoft Fabric (preview)](../how-to/tools/fabric.md) | Connect to a [Microsoft Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312815) for data analysis. |
| [SharePoint (preview)](../how-to/tools/sharepoint.md) | Chat with private documents stored in SharePoint. |

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
- [Create a private tool catalog](../how-to/private-tool-catalog.md)
- [Build and register an MCP server](../../mcp/build-your-own-mcp-server.md)
- [Foundry MCP Server best practices and security guidance](../../mcp/security-best-practices.md)
