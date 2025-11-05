---
title: "Discover tools in the Azure AI Foundry tool catalog"
description: "Learn about the tool catalog in Azure AI Foundry to extend your AI agents and workflows."
author: aahill
ms.author: aahi
ms.date: 10/27/2025
ms.manager: nitinme
ms.topic: conceptual
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
---

# Discover tools in the Azure AI Foundry tool catalog (preview)

The Azure AI Foundry tool catalog is a central hub for discovering tools to extend your AI agents

The tool catalog enables you to: 

* Browse and use Model Context Protocol (MCP) tool servers created by Microsoft and non-Microsoft services, for various use cases such as data integration, productivity and more. 
* Streamline integration between tool configuration and adding to an agent or workflow. 
* Filter, search, and sort by your desired outcome 

## Considerations for using non-Microsoft services and servers 

Your use of connected non-Microsoft services and servers ("non-Microsoft services") is subject to the terms between you and the service provider. Non-Microsoft services are non-Microsoft products under your agreement governing use of Microsoft online services. When you connect to non-Microsoft services, some of your data (such as prompt content) is passed to the non-Microsoft services, or your application might receive data from the non-Microsoft Services. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use. 

The non-Microsoft services, including remote MCP servers, that you decide to use with the MCP tool described in this article were created by third parties, not Microsoft. Microsoft hasn't tested or verified these servers. Microsoft has no responsibility to you or others in relation to your use of any non-Microsoft services.  

We recommend that you carefully review and track the MCP servers you add to Foundry Agent Service. We also recommend that you rely on servers hosted by trusted service providers themselves rather than proxies. 

The MCP tool allows you to pass custom headers, such as authentication keys or schemas, that a remote MCP server might need. We recommend that you review all data that's shared with Non-Microsoft services, including remote MCP servers, and that you log the data for auditing purposes. Be cognizant of non-Microsoft practices for retention and location of data. 

## Public and private tool catalogs

The Azure AI Foundry provides both public and private tool catalogs. The public tool catalog is an enterprise-ready curated list of MCP servers available to all AI Foundry developers for building AI agents. You can also build an organizational tool catalog with tools that appear only in your organization by creating a [private tool catalog](../how-to/private-tool-catalog.md). 

## Find the right tools from the tool catalog

### Tool types

There are three types of MCP tool servers in the public tool catalog:

**Remote MCP server**: The MCP server publisher has already hosted the server and provided a static or dynamic MCP server endpoint. AI Foundry developers need to follow the configuration guidance to provide the appropriate information to finish the setup. 

**Local MCP server**: The MCP server publisher doesn't host the server and require AI Foundry developers to self-host and bring the self-hosted remote MCP server endpoint back to AI Foundry to use it with AI agents. For information about self-hosting a local MCP server here, see the [custom MCP Server documentation](https://aka.ms/FoundryCustomMCP)  

**Custom**: These MCP servers are converted from Azure Logic App Connectors. AI Foundry developers need additional [configuration](https://aka.ms/FoundryCustomTool) to convert to remote MCP servers.


### Filter and search

The AI Foundry tool catalog provides the following filters to help you find the right tools for your agents:

| Filter | Description |
|--------|-------------|
| Publisher | Microsoft and Partner: non-Microsoft service |
| Category | Categorize tools by different industries and use cases, such as databases, analytics, web, and more |
| Registry | **Public**: This is the registry for all public remote MCP servers and local MCP servers in the catalog<br>**Logic app connectors**: This is the registry for all Azure Logic App Connectors that need to be converted to remote MCP servers to use a private tool catalog you built. You can have multiple private tool catalogs in your Foundry Tool Catalog. |
| Supported Authentication | You can also filter by the authentication method an MCP server supports. For more information see [Authentication methods](https://aka.ms/FoundryMCPAuth). |

When you select a specific tool you are interested, you can see the details page like this one:

:::image type="content" source="../media/tool-catalog/tool-example.png" alt-text="An example tool in the AI Foundry portal." lightbox="../media/tool-catalog/tool-example.png":::

The details page contains the following information: 

- **Basic information**: Name, logo, and description
- **MCP server endpoint**: The endpoint for the tool. Only available for remote MCP servers. Some MCP servers such as Elasticsearch have dynamic endpoint that requires you to provide configurations to complete the endpoint. You will later be prompted to enter more information.
- **Supported authentication**: The [authentication](https://aka.ms/FoundryMCPAuth) method the MCP server supports.
- **Documentation link**: The hyperlink to view the specific documentation for the tool.
- **Use cases**: In addition to category of the tool, you can also see more detailed explanation of use cases, and supported capabilities.
- **Warning and license**: Before using the tool, make sure you have reviewed the warning and license for the tool.
- **Support Contact**: If you have questions about using or setting up the tool, reach out to a support contact.

## Tool catalog in the AI Foundry

In your tools list <!--(https://ai.azure.com/nextgen/build/tools)-->, you can find the list of tools you have configured, along with details such as MCP server endpoints, and authentication information. You can also delete or add your tools to existing agents. If you delete a tool, affect agents currently using them.

<!--
:::image type="content" source="../media/tool-catalog/tool-view.png" alt-text="A screenshot showing the tools list in the AI Foundry portal."lightbox="../media/tool-catalog/tool-view.png" :::
-->

To see a full list of available tools, you can use the Agent playground. You can view recently used tools, and add new ones.

The tool catalog contains three sections:

- **Configured**: Configured tools are ready to use with your configured authentication, configuration or setup. You can also find built-in tools:

    |Tool  |Description  |
    |---------|---------|
    |[Azure AI Search](../../../agents/how-to/tools/azure-ai-search.md)     | Use an existing Azure AI Search index to ground agents with data in the index, and chat with your data.        |
    |[Browser Automation (preview)](../../../agents/how-to/tools/browser-automation.md)     | Perform real-world browser tasks through natural language prompts.         |
    |[Code Interpreter](../../../agents/how-to/tools/code-interpreter.md)     | Enable agents to write and run Python code in a sandboxed execution environment.         |
    |[Computer Use (preview)](../../../agents/how-to/tools/computer-use.md)     | Specialized AI tool that uses a specialized model that can perform tasks by interacting with computer systems and applications through their user interfaces         |
    |[File Search](../../../agents/how-to/tools/file-search.md)     | Augment agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.          |
    |[Grounding with Bing Search](../../../agents/how-to/tools/bing-grounding.md)     | Enable your agent to use Grounding with Bing Search to access and return information from the internet.         |
    | [Grounding with Bing Custom Search (preview)](../../../agents/how-to/tools/bing-custom-search.md) | Enhance your Agent response with selected web domains |
    | [Image Generation (preview)](../how-to/tools/image-generation.md) | Enables image generation as part of conversations and multi-step workflows |
    | [Microsoft Fabric (preview)](../../../agents/how-to/tools/fabric.md) | Integrate your agent with the [Microsoft Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. |
    | [SharePoint (preview)](../../../agents/how-to/tools/sharepoint.md) | Integrate your agents with the Microsoft SharePoint to chat with your private documents securely. |
    |[Web Search (preview)](../how-to/tools/web-search.md)     | Enables models to retrieve and ground responses with real-time information from the public web before generating output.         |


- **Catalog**: Available from the public or organizational Foundry Tool Catalog, including remote and local MCP servers and Azure Logic Apps connectors, which may require setup before use.

- **Custom**: These allow you to bring your own APIs using remote MCP server endpoints, A2A endpoints, OpenAPI 3.0 specs, functions, or Azure Functions.
    
    |Tool  |Description  |
    |---------|---------|
    |[Azure Functions](../../../agents/how-to/tools/azure-functions.md)     | Leverage your Azure Functions to create intelligent, event-driven applications.        |
    |[Function calling](../../../agents/how-to/tools/function-calling.md)     |Describe the structure of functions you create to an agent and have them be called when appropriate during the agent's interactions with users.         |
    | [Model Context Protocol (preview)](../../../agents/how-to/tools/model-context-protocol.md) | Give the agent access to tools hosted on an existing MCP endpoint |
    | [OpenAPI 3.0 Specified tool](../../../agents/how-to/tools/openapi-spec.md) | Connect your Azure AI Agent to external APIs using functions with an OpenAPI 3.0 specification. |
    
## Next steps

* [Create a private tool catalog](../how-to/private-tool-catalog.md)
* [Build your own MCP server](https://aka.ms/FoundryCustomTool)