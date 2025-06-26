---
title: 'How to connect to Model Context Protocol Server Endpoint in Azure AI Foundry Agent Service'
titleSuffix: Azure AI Foundry
description: Learn how to add MCP to Foundry Agent service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 06/17/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---
# Connect Model Context Protocol Server with Azure AI Foundry Agent Service (Preview)
You can extend the capabilities of your Foundry Agent by connecting it to tools hosted on remote Model Context Protocol (MCP) servers (bring your own MCP server endpoint). These servers are maintained by developers and organizations and expose tools that can be accessed by MCP-compatible clients, such as the Foundry Agent service.

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is an open standard that defines how applications provide tools and contextual data to large language models (LLMs). It enables consistent, scalable integration of external tools into model workflows.

> [!IMPORTANT]
> * Your use of connected non-Microsoft services is subject to the terms between you and the service provider.  By connecting to a non-Microsoft service, some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service.  You are responsible for your use (and any charges associated with your use) of non-Microsoft services and data.
> * The remote MCP servers you decide to use with this MCP tool were created by third parties, not Microsoft, and have not been tested or verified by Microsoft. Microsoft has no responsibility to you or others in relation to your use of any remote MCP servers. We recommend carefully reviewing and tracking what MCP servers you add to Foundry Agent service and relying on servers hosted by trusted service providers themselves rather than proxies. This MCP tool also allows you to pass custom headers such as authentication keys or schema as might be needed by a remote MCP server. We recommend reviewing all data being shared with remote MCP servers and optionally logging it for auditing purposes.  Be cognizant of third party practices for retention and location of data.

## How it works
You can bring multiple remote MCP servers to Foundry Agent service by adding them as tools. For each tool, you need to provide a unique `server_label` within the same agent and `server_url` that points to the remote MCP server. The MCP tool supports custom headers, allowing you to connect to these servers using the authentication scheme they require or passing other headers required by the MCP server. You can only specify headers by including in `tool_resources` at each run such as API keys, OAuth access tokens, or other credentials directly in your request. The most commonly used header is the authorization header. For more information on using MCP, see:
* [Security best practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
* [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667)

> [!Note]
> * You need to bring a remote MCP server (an existing MCP server endpoint)
> * With current MCP tool in Foundry Agent, explicit approval is not supported yet (only `never` is accepted for `require_approval` parameter). Please review carefully what MCP server(s) you added to Foundry Agent service. We recommend reviewing all data being shared with remote MCP servers and optionally logging it for auditing purposes.
> * Supported regions: `westus`, `westus2` and `uaenorth`

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|---------:|
| - | - | - | - | ✔️ | ✔️ | ✔️ |

## Setup  
1. Create an Azure AI Foundry Agent by following the steps in the [quickstart](../../quickstart.md).

1. Find the remote MCP server you want to connect to, such as GitHub MCP Server. Create or update a Foundry Agent with a `mcp` tool with the following information:
   1. `server_url`: the url of the MCP server, for example, `https://api.githubcopilot.com/mcp/`
   2. `server_label`: a unique identifier of this MCP server to the agent, for example, `github`
   3. `require_approval`: only `never` is supported right now
  
1. Create a run and pass additional information about the `mcp` tool in `tool_resources` with headers
   1. `tool_label`: use the identifier you provided during create/update agent
   2. `headers`: pass a set of headers required by the MCP server

## Next steps

* [How to use the MCP tool](./mcp-samples.md)