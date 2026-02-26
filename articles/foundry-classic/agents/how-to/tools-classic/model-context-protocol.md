---
title: Connect to a Model Context Protocol Server Endpoint in Foundry Agent Service (Preview)
titleSuffix: Microsoft Foundry
description: Learn how to add MCP servers to Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/16/2025
author: alvinashcraft
ms.author: aashcraft
---

# Connect to Model Context Protocol servers (preview)

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new MCP tool documentation](../../../default/agents/how-to/tools/model-context-protocol.md?view=foundry&preserve-view=true).

You can extend the capabilities of your Foundry agent by connecting it to tools hosted on remote [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers (bring your own MCP server endpoint). Developers and organizations maintain these servers. The servers expose tools that MCP-compatible clients, such as Foundry Agent Service, can access.

MCP is an open standard that defines how applications provide tools and contextual data to large language models (LLMs). It enables consistent, scalable integration of external tools into model workflows.

<!-- The verbiage in the following section is required. Do not remove or modify. -->
## Considerations for using non-Microsoft services and servers

Your use of connected non-Microsoft services is subject to the terms between you and the service provider. When you connect to a non-Microsoft service, some of your data (such as prompt content) is passed to the non-Microsoft service, or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use.

The remote MCP servers that you decide to use with the MCP tool described in this article were created by third parties, not Microsoft. Microsoft hasn't tested or verified these servers. Microsoft has no responsibility to you or others in relation to your use of any remote MCP servers.

We recommend that you carefully review and track what MCP servers you add to Foundry Agent Service. We also recommend that you rely on servers hosted by trusted service providers themselves rather than proxies.

The MCP tool allows you to pass custom headers, such as authentication keys or schemas, that a remote MCP server might need. We recommend that you review all data that's shared with remote MCP servers and that you log the data for auditing purposes. Be cognizant of non-Microsoft practices for retention and location of data.

## How it works

You need to bring a remote MCP server (an existing MCP server endpoint) to Foundry Agent Service. You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique `server_label` value within the same agent and a `server_url` value that points to the remote MCP server. Be sure to carefully review which MCP servers you add to Foundry Agent Service.

The MCP tool supports custom headers, so you can connect to the MCP servers by using the authentication schemas that they require or by passing other headers that the MCP servers require. You can specify headers only by including them in `tool_resources` at each run. In this way, you can put API keys, OAuth access tokens, or other credentials directly in your request.

The most commonly used header is the authorization header. Headers that you pass in are available only for the current run and aren't persisted.

For more information on using MCP, see:

* [Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices) on the Model Context Protocol website.
* [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667) in the Microsoft Security Community Blog.

## Usage support

|Azure AI foundry support  | Python SDK |  C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|---------:|
| - | ✔️ | - | - | ✔️ | ✔️ | ✔️ |

## Setup

1. Create a Foundry agent by following the steps in the [quickstart](../../quickstart.md).

1. Find the remote MCP server that you want to connect to, such as the GitHub MCP server. Create or update a Foundry agent with an `mcp` tool with the following information:

   1. `server_url`: The URL of the MCP server; for example, `https://api.githubcopilot.com/mcp/`.
   2. `server_label`: A unique identifier of this MCP server to the agent; for example, `github`.
   3. `allowed_tools`: An optional list of tools that this agent can access and use.
  
1. Create a run and pass additional information about the `mcp` tool in `tool_resources` with headers:

   1. `tool_label`: Use the identifier that you provided when you created the agent.
   2. `headers`: Pass a set of headers that the MCP server requires.
   3. `require_approval`: Optionally determine whether approval is required. Supported values are:
      * `always`: A developer needs to provide approval for every call. If you don't provide a value, this one is the default.
      * `never`: No approval is required.
      * `{"never":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that don't require approval.
      * `{"always":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that require approval.

1. If the model tries to invoke a tool in your MCP server with approval required, you get a run status of `requires_action`. In the `requires_action` field, you can get more details on which tool in the MCP server is called, arguments to be passed, and `call_id` value. Review the tool and arguments so that you can make an informed decision for approval.

1. Submit your approval to the agent with `call_id` by setting `approve` to `true`.

## Host a local MCP server

The Agent Service runtime only accepts a remote MCP server endpoint. If you want to add tools from a local MCP server, you'll have to self-host it on [Azure Container Apps](/samples/azure-samples/mcp-container-ts/mcp-container-ts/) or [Azure Functions](https://github.com/Azure-Samples/mcp-sdk-functions-hosting-python/tree/main) to get a remote MCP server endpoint. Pay attention to the following considerations when attempting to host local MCP servers in the cloud:

|Local MCP server setup | Hosting in Azure Container Apps | Hosting in Azure Functions |
|:---------:|:---------:|:---------:|
| **Transport** | HTTP POST/GET endpoints required. | HTTP streamable required. | 
| **Code changes** | Container rebuild required. | Azure Functions-specific configuration files required in the root directory. |
| **Authentication** | Custom authentication implementation required. | Key-based only. OAuth needs API Management. |
| **Language** | Any language that runs in Linux containers (Python, Node.js, .NET, TypeScript, Go). | Python, Node.js, Java, .NET only. |
| **Container Requirements** | Linux (linux/amd64) only. No privileged containers.| Containerized servers are not supported. |
| **Dependencies** | All dependencies must be in container image. | OS-level dependencies (such as Playwright) are not supported. |
| **State** | Stateless only. | Stateless only. |
| **UVX/NPX** | Supported. | Not supported. `npx` start commands not supported. |

## Known limitations

- **Non-streaming MCP tool call timeout**: Non-streaming MCP tool calls have a timeout of 50 seconds. If your MCP server takes longer than 50 seconds to respond, the call fails. To avoid timeouts, ensure that your MCP server responds within this limit. If your use case requires longer processing times, consider optimizing the server-side logic or breaking the operation into smaller steps.

## Related content

* [Code samples for the Model Context Protocol tool](./model-context-protocol-samples.md)
