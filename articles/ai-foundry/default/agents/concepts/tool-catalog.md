---
title: "Foundry tool catalog (preview): discover and manage tools"
description: "Learn how to use the Foundry tool catalog to discover, configure, and manage tools for agents, including MCP servers and custom tools."
author: aahill
ms.author: aahi
ms.date: 01/20/2026
ms.manager: nitinme
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Discover and manage tools in the Foundry tool catalog (preview)

Foundry Tools is the place to discover and manage tools you use with agents and workflows in Microsoft Foundry.

[!INCLUDE [preview-feature](../../../openai/includes/preview-feature.md)]

You can use Foundry Tools to:

* Discover tools such as Model Context Protocol (MCP) servers and built-in tools.
* Configure tools once, then add them to agents or workflows.
* Filter, search, and sort tools.

## Prerequisites

To use Foundry Tools, you need:

* Access to a Foundry project in the Foundry portal.
* One of the following roles on the project:
  - **Azure AI User** — View and use configured tools
  - **Azure AI Project Manager** — Configure and manage tools
  - **Azure AI Owner** — Full access including tool deletion
* For tools that connect to external services, you need credentials or access to those services.

**Verification**: To confirm you have access, go to the Foundry portal, open your project, and select **Build** > **Tools**. If you see the tool catalog, you have the required permissions.

## Where to find Foundry Tools

In the Foundry portal, go to your project and then select **Build** > **Tools**.

**Expected result**: The Foundry Tools page opens, showing three tabs: **Configured**, **Catalog**, and **Custom**.

## Key concepts

Use these definitions to keep the terminology consistent:

| Term | Meaning |
|---|---|
| Foundry Tools | The portal experience where you discover, configure, and manage tools for agents and workflows. |
| Tool catalog | The browsable list of available tools (public and organizational). |
| Private tool catalog | An organization-scoped catalog for tools that only users in your organization can discover and configure. |
| MCP server | A server that exposes tools using the Model Context Protocol (MCP). |
| Remote MCP server | An MCP server hosted by the publisher. You configure it by providing the required settings (for example, an endpoint and authentication details). |
| Local MCP server | An MCP server you host yourself, then connect to Foundry by providing its remote endpoint. |
| Custom tool | A tool you add by providing your own endpoint or specification (for example, an MCP endpoint, an OpenAPI spec, or Agent-to-Agent (A2A) endpoints). |

> [!NOTE]
> If you're interested in bringing your official, remote MCP server(s) to all Foundry customers, fill out this [form](https://forms.office.com/r/EEvMNceMRU).

## Considerations for using non-Microsoft services and servers 

Your use of connected non-Microsoft services and servers ("non-Microsoft services") is subject to the terms between you and the service provider. Non-Microsoft services are non-Microsoft products under your agreement governing use of Microsoft online services. When you connect to non-Microsoft services, some of your data (such as prompt content) is sent to the non-Microsoft service, or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use.

Third parties (not Microsoft) create the non-Microsoft services, including remote MCP servers, that you choose to connect. Microsoft doesn't test or verify these servers. Microsoft has no responsibility to you or others in relation to your use of any non-Microsoft services.

Carefully review and track the MCP servers you add to Foundry Agent Service. Rely on servers hosted by trusted service providers themselves rather than proxies.

The MCP tool can pass custom headers that a remote MCP server might require for authentication. Treat any credentials as secrets:

* Only provide the minimum required headers.
* Don't include credentials in prompts.
* If you log requests for auditing, avoid logging secrets or sensitive prompt content.
* Review the provider's data handling practices, including retention and data location.

## Foundry Tools and private tools catalog

Foundry provides both Foundry Tools and private tool catalogs.

Foundry Tools includes a curated list of tools available for building agents. If you need tools that are only visible within your organization, create a [private tool catalog](../how-to/private-tool-catalog.md).

## Find the right tools in Foundry Tools

### Tool types

Foundry Tools includes three types of tool catalog entries:

**Remote MCP server**: The MCP server publisher has already hosted the server and provided a static or dynamic MCP server endpoint. Foundry developers need to follow the configuration guidance to provide the appropriate information to finish the setup. 

**Local MCP server**: The publisher doesn't host the server. You host it, then connect it to Foundry by providing its endpoint. To build and register your own server, see [Build and register a Model Context Protocol (MCP) server](../../mcp/build-your-own-mcp-server.md). To connect an MCP endpoint to an agent, see [Connect to Model Context Protocol servers](../how-to/tools/model-context-protocol.md).

**Custom**: These MCP servers are converted from Azure Logic App Connectors. Foundry developers need additional [configuration](https://aka.ms/FoundryCustomTool) to convert to remote MCP servers.


### Filter and search

Foundry Tools provides the following filters to help you find the right tools for your agents:

| Filter | Description |
|--------|-------------|
| Publisher | Microsoft or non-Microsoft publisher |
| Category | Categories such as databases, analytics, web, and more |
| Registry | **Public**: Public remote and local MCP servers in the catalog<br>**Logic Apps connectors**: Azure Logic Apps connectors that you convert to remote MCP servers for use in a private tool catalog. |
| Supported authentication | Authentication method an MCP server supports. For more information, see [Authentication methods](https://aka.ms/FoundryMCPAuth). |

:::image type="content" source="../media/tool-catalog/tool-example.png" alt-text="Screenshot of a tool details page in the Foundry portal showing configuration and setup information." lightbox="../media/tool-catalog/tool-example.png":::

When you select a tool, Foundry Tools shows the setup details you need to configure it.

## Availability and limitations

Tool availability can vary by model and region. Review the following considerations before configuring tools.

### Model support

Not all models support all tools. The following table shows general tool support by model capability:

| Tool type | Required model capability |
|-----------|---------------------------|
| Code Interpreter | Function calling support |
| File Search | Function calling support |
| MCP servers | Function calling support |
| OpenAPI tools | Function calling support |
| Grounding with Bing | Grounding capability |
| Computer Use | Vision and function calling |

> [!NOTE]
> Check the specific tool documentation for the latest supported models. Model support can change as new capabilities are released.

### Regional availability

Most built-in tools are available in all regions where Foundry Agent Service is available. However, some tools have regional restrictions:

- **Grounding with Bing**: Available in regions where Bing Search is supported.
- **Computer Use**: Check the [Computer Use documentation](../how-to/tools/computer-use.md) for regional availability.
- **Custom Code Interpreter**: Requires Azure Container Apps, which has its own regional availability.

### Preview limitations

Tools marked as **(preview)** have the following limitations:

- No service-level agreement (SLA) for availability or performance.
- Features might change or be removed without notice.
- Not recommended for production workloads.

For the latest model and region support details across tools, see [Best practices for using tools in Microsoft Foundry Agent Service](tool-best-practice.md).

## Manage tools you've configured

In your tools list, you can find the tools you've configured, along with details such as endpoints and authentication settings. You can also add tools to agents and workflows.

### View configured tools

1. In the Foundry portal, go to your project.
1. Select **Build** > **Tools** > **Configured**.

**Expected result**: You see a list of all tools you've configured, including their status, endpoints, and last-used timestamps.

### Add a tool to an agent

1. Open the tool you want to add.
1. Select **Add to agent**.
1. Choose the target agent from the list.

**Verification**: Open the agent and confirm the tool appears in the agent's tool list.

### Delete a configured tool

Before you delete a tool, check which agents or workflows use it. Deleting a tool can break runs that depend on it.

1. In the **Configured** tab, find the tool you want to delete.
1. Check the **Used by** column to see which agents use this tool.
1. Remove the tool from those agents first, or confirm the agents no longer need it.
1. Select the tool, then select **Delete**.

> [!WARNING]
> Deleting a tool immediately removes it from all agents. Active conversations using the tool might fail.

<!--
:::image type="content" source="../media/tool-catalog/tool-view.png" alt-text="A screenshot showing the tools list in the Foundry portal."lightbox="../media/tool-catalog/tool-view.png" :::
-->

To explore tools while you build, use the Agents playground. For more information, see [Microsoft Foundry Playgrounds](../../../concepts/concept-playgrounds.md).

Foundry Tools contains three sections:

- **Configured**: Configured tools are ready to use because you've completed their setup (authentication and required settings). Built-in tools include:

    |Tool  |Description  |
    |---------|---------|
    |[Azure AI Search](../how-to/tools/ai-search.md)     | Use an existing Azure AI Search index to ground agents with data in the index, and chat with your data. |
    |[Browser Automation (preview)](../how-to/tools/browser-automation.md)     | Perform real-world browser tasks through natural language prompts. |
    |[Code Interpreter](../how-to/tools/code-interpreter.md)     | Enable agents to write and run Python code in a sandboxed execution environment. |
    |[Custom Code Interpreter (preview)](../how-to/tools/custom-code-interpreter.md)     | Use a custom code interpreter MCP server to customize resources, available Python packages, and the Container Apps environment the agent uses. |
    |[Computer Use (preview)](../how-to/tools/computer-use.md)     | Specialized tool that uses a model that can perform tasks by interacting with computer systems and applications through their user interfaces. |
    |[File Search](../how-to/tools/file-search.md)     | Augment agents with knowledge from outside its model, such as proprietary product information or documents provided by your users. |
    | [Grounding with Bing tools](../how-to/tools/bing-tools.md) | Enable your agent to use Grounding with Bing Search to access and return information from the internet. |
    | [Image Generation (preview)](../how-to/tools/image-generation.md) | Enable image generation as part of conversations and multi-step workflows. |
    | [Microsoft Fabric (preview)](../how-to/tools/fabric.md) | Integrate your agent with the [Microsoft Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. |
    | [SharePoint (preview)](../how-to/tools/sharepoint.md) | Integrate your agents with Microsoft SharePoint to chat with your private documents securely. |
    |[Web Search (preview)](../how-to/tools/web-search.md)     | Enable models to retrieve and ground responses with real-time information from the public web before generating output. |


- **Catalog**: Available from the public or organizational Foundry Tool Catalog, including remote and local MCP servers and Azure Logic Apps connectors, which may require setup before use.

- **Custom**: These allow you to bring your own APIs using remote MCP server endpoints, A2A endpoints, OpenAPI 3.0 specs, or functions.
    
    |Tool  |Description  |
    |---------|---------|
    | [Model Context Protocol (preview)](../how-to/tools/model-context-protocol.md) | Give the agent access to tools hosted on an existing MCP endpoint. |
    | [OpenAPI 3.0 specified tool](../how-to/tools/openapi.md) | Connect your Foundry agents to external APIs using functions with an OpenAPI 3.0 specification. |
    | [Agent-to-Agent tool (preview)](../how-to/tools/agent-to-agent.md) | Connect your Foundry agents to other agents through A2A-compatible endpoints. |

## Troubleshooting

Use these checks to resolve common issues.

| Issue | Cause | Resolution |
|-------|-------|------------|
| You can't find the tool catalog | Wrong navigation path or missing permissions | Confirm you're in the correct project, then go to **Build** > **Tools**. Verify you have at least **Azure AI User** role on the project. |
| A tool is visible but you can't configure it | Missing authentication or dependent service access | Review the tool's required authentication and configuration inputs. Verify you have access to any dependent services (for example, Azure AI Search index, SharePoint site). |
| Your agent doesn't call a tool | Tool not properly attached, model doesn't support tool, or tool instructions unclear | 1. Verify the tool is attached to the agent. 2. Check that the model supports function calling. 3. Review the tool's description to ensure it clearly states when to use the tool. See [Best practices for using tools](tool-best-practice.md). |
| MCP server connection fails | Invalid endpoint, authentication error, or server unavailable | Verify the MCP server endpoint is correct and accessible. Check authentication credentials. Test the endpoint directly if possible. |
| Tool works in playground but fails in production | Rate limits, authentication expiration, or service changes | Check for rate limit errors in the agent logs. Refresh authentication tokens if using OAuth. Verify the external service hasn't changed its API. |
| Custom tool returns errors | Invalid OpenAPI spec or endpoint mismatch | Validate your OpenAPI 3.0 spec. Ensure all required parameters are defined. Test the endpoint directly to confirm it works. |

### Validate tool configuration

To confirm a tool is configured correctly:

1. In **Foundry Tools**, select the tool to open its details.
1. Check that all required fields show valid values (no error indicators).
1. If available, use the **Test** button to send a sample request.
1. Review the response to confirm the tool works as expected.

### Debug agent tool calls

If an agent isn't calling a tool when expected:

1. Open the agent in the **Agents playground**.
1. Enable **Show tool calls** in the playground settings.
1. Send a message that should trigger the tool.
1. Review the tool call details to see if the agent attempted to call the tool and what response it received.
    
## Next steps

- [Create a private tool catalog](../how-to/private-tool-catalog.md) — Set up organization-specific tools.
- [Connect to Model Context Protocol servers](../how-to/tools/model-context-protocol.md) — Add MCP servers to your agents.
- [Best practices for using tools in Microsoft Foundry Agent Service](tool-best-practice.md) — Optimize tool configuration and usage.

## Related content

* [Create a private tool catalog](../how-to/private-tool-catalog.md)
* [Connect to Model Context Protocol servers](../how-to/tools/model-context-protocol.md)
* [Build and register a Model Context Protocol (MCP) server](../../mcp/build-your-own-mcp-server.md)
* [Foundry MCP Server best practices and security guidance](../../mcp/security-best-practices.md)
* [Get started with Foundry MCP Server (preview) using Visual Studio Code](../../mcp/get-started.md)
* [Bring your remote, official MCP server to all Foundry customers](https://forms.office.com/r/EEvMNceMRU)
