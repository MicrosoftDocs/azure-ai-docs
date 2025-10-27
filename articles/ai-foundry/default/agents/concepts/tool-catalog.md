---
title: "MCP servers in the Azure AI Foundry tool catalog"
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

# MCP servers in the Azure AI Foundry tool catalog (preview)

The Azure AI Foundry tool catalog is a central hub for discovering MCP servers to extend your AI agents and workflows.

The tool catalog enables you to: 

* Browse and use MCP tool servers created by Microsoft and non-Microsoft services, for various use cases such as data integration, productivity and more. 
* Streamline integration between tool configuration and adding to an agent or workflow. 
* Filter, search, and sort by your desired outcome 

## Public and private tool catalogs

The Azure AI Foundry provides both public and private tool catalogs. The public tool catalog is an enterprise-ready curated list of MCP servers available to all AI Foundry developers for building AI agents. You can also restrict the tools that appear in your organization by creating a [private tool catalog](../how-to/private-tool-catalog.md). 

## Remote MCP server types

There are 3 types of tools in the public tool catalog:

**Remote MCP server**: The MCP server publisher has already hosted the server and provided a static or dynamic MCP server endpoint. AI Foundry developers need to follow the configuration guidance to provide the appropriate information to finish the setup. 

**Local MCP server**: The MCP server publisher doesn't host the server and require AI Foundry developers to self-host and bring the self-hosted remote MCP server endpoint back to AI Foundry to use it with AI agents. For information about self-hosting a local MCP server here, see the [custom MCP Server documentation](https://aka.ms/FoundryCustomMCP)  

**Custom MCP Server**: These MCP servers are converted from Azure Logic App Connectors. AI Foundry developers need additional [configuration](https://aka.ms/FoundryCustomTool) to convert to remote MCP servers.

There are three types of tools in the public tool catalog:

## Next steps

* [Create a private tool catalog](../how-to/private-tool-catalog.md)
* [Build your own MCP server](https://aka.ms/FoundryCustomTool)