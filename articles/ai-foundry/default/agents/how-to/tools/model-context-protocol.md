---
title: Connect to MCP Server Endpoints for agents (Preview)
titleSuffix: Microsoft Foundry
description: Learn how to connect agents to Model Context Protocol (MCP) servers to extend agent capabilities with external tools and data sources.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/05/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-mcp-code-new
---

# Connect to Model Context Protocol servers (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> When you use a [Network Secured Microsoft Foundry](../../../../agents/how-to/virtual-networks.md), you can't use private MCP servers deployed in the same virtual network. You can only use publicly accessible MCP servers.

Connect your Foundry agents to [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) servers to extend agent capabilities with external tools and data sources. By connecting to remote MCP server endpoints, your agents can access tools hosted by developers and organizations that MCP-compatible clients like Foundry Agent Service can use.

MCP is an open standard that defines how applications provide tools and contextual data to large language models (LLMs). It enables consistent, scalable integration of external tools into model workflows.

## Considerations for using non-Microsoft services and servers

Your use of connected non-Microsoft services is subject to the terms between you and the service provider. When you connect to a non-Microsoft service, some of your data (such as prompt content) is passed to the non-Microsoft service, or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use.

The remote MCP servers that you decide to use with the MCP tool described in this article are created by third parties, not Microsoft. Microsoft doesn't test or verify these servers. Microsoft has no responsibility to you or others in relation to your use of any remote MCP servers.

We recommend that you carefully review and track what MCP servers you add to Foundry Agent Service. We also recommend that you rely on servers hosted by trusted service providers themselves rather than proxies.

The MCP tool allows you to pass custom headers, such as authentication keys or schemas, that a remote MCP server might need. We recommend that you review all data that you share with remote MCP servers and that you log the data for auditing purposes. Be aware of non-Microsoft practices for retention and location of data.

## Code example

:::zone pivot="python"
Use the following code sample to create an agent and call the function. You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool, Tool
from openai.types.responses.response_input_param import McpApprovalResponse, ResponseInputParam


load_dotenv()

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # [START tool_declaration]
    tool = MCPTool(
        server_label="api-specs",
        server_url="https://api.githubcopilot.com/mcp",
        require_approval="always",
        project_connection_id=os.environ["MCP_PROJECT_CONNECTION_ID"],
    )
    # [END tool_declaration]

    # Create a prompt agent with MCP tool capabilities
    agent = project_client.agents.create_version(
        agent_name="MyAgent7",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="Use MCP tools as needed",
            tools=[tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Create a conversation to maintain context across multiple interactions
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # Send initial request that will trigger the MCP tool
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="What is my username in Github profile?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    # Process any MCP approval requests that were generated
    input_list: ResponseInputParam = []
    for item in response.output:
        if item.type == "mcp_approval_request":
            if item.server_label == "api-specs" and item.id:
                # Automatically approve the MCP request to allow the agent to proceed
                # In production, you might want to implement more sophisticated approval logic
                input_list.append(
                    McpApprovalResponse(
                        type="mcp_approval_response",
                        approve=True,
                        approval_request_id=item.id,
                    )
                )

    print("Final input:")
    print(input_list)

    # Send the approval response back to continue the agent's work
    # This allows the MCP tool to access the GitHub repository and complete the original request
    response = openai_client.responses.create(
        input=input_list,
        previous_response_id=response.id,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    print(f"Response: {response.output_text}")

    # Clean up resources by deleting the agent version
    # This prevents accumulation of unused agent versions in your project
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```
:::zone-end

:::zone pivot="csharp"

For C# usage, see the [Sample using Agents with MCP tool in Azure.AI.Projects.OpenAI](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample19_MCP.md) and [Sample using Agents with MCP tool with project connection in Azure.AI.Projects.OpenAI](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample19_MCP_Connection.md) examples in the Azure SDK for .NET repository on GitHub.

:::zone-end

## How it works

You need to bring a remote MCP server (an existing MCP server endpoint) to Foundry Agent Service. You can bring multiple remote MCP servers by adding them as tools. For each tool, you need to provide a unique `server_label` value within the same agent and a `server_url` value that points to the remote MCP server. Be sure to carefully review which MCP servers you add to Foundry Agent Service.

For more information on using MCP, see:

- [Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices) on the Model Context Protocol website.
- [Understanding and mitigating security risks in MCP implementations](https://techcommunity.microsoft.com/blog/microsoft-security-blog/understanding-and-mitigating-security-risks-in-mcp-implementations/4404667) in the Microsoft Security Community Blog.

## Setup

The following steps outline how to connect to a remote MCP server from Foundry Agent Service:

1. Find the remote MCP server that you want to connect to, such as the GitHub MCP server. Create or update a Foundry agent with an `mcp` tool with the following information:
   1. `server_url`: The URL of the MCP server, such as `https://api.githubcopilot.com/mcp/`.
   1. `server_label`: A unique identifier of this MCP server to the agent, such as `github`.
   1. `allowed_tools`: An optional list of tools that this agent can access and use. If you don't provide this value, the default value includes all of the tools in the MCP server.
   1. `require_approval`: Optionally determine whether approval is required. The default value is `always`. Supported values are:
      - `always`: A developer needs to provide approval for every call. If you don't provide a value, this one is the default.
      - `never`: No approval is required.
      - `{"never":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that don't require approval.
      - `{"always":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that require approval.
   1. `project_connection_id`: the name of your project connection
1. If the model tries to invoke a tool in your MCP server with approval required, you get a response output item type as `mcp_approval_request`. In the response output item, you can get more details on which tool in the MCP server is called and arguments to be passed. Review the tool and arguments so that you can make an informed decision for approval.
1. Submit your approval to the agent with `response_id` by setting `approve` to `true`.

## Common questions and errors

The following are common issues that you might encounter when using MCP tools with Foundry Agent Service:

- "Invalid tool schema":

    Invalid tool schema usually happens if you have `anyOf` or `allOf` in your MCP server definition, or if a parameter can take multiple types of values. Update your MCP server definition and try again.

## Host a local MCP server

The Agent Service runtime only accepts a remote MCP server endpoint. If you want to add tools from a local MCP server, you need to self-host it on [Azure Container Apps](/samples/azure-samples/mcp-container-ts/mcp-container-ts/) or [Azure Functions](https://github.com/Azure-Samples/mcp-sdk-functions-hosting-python/tree/main) to get a remote MCP server endpoint. Consider the following factors when hosting local MCP servers in the cloud:

|Local MCP server setup | Hosting in Azure Container Apps | Hosting in Azure Functions |
|:---------:|:---------:|:---------:|
| **Transport** | HTTP POST/GET endpoints required. | HTTP streamable required. | 
| **Code changes** | Container rebuild required. | Azure Functions-specific configuration files required in the root directory. |
| **Authentication** | Custom authentication implementation required. | Key-based only. OAuth needs API Management. |
| **Language** | Any language that runs in Linux containers (Python, Node.js, .NET, TypeScript, Go). | Python, Node.js, Java, .NET only. |
| **Container Requirements** | Linux (linux/amd64) only. No privileged containers.| Containerized servers aren't supported. |
| **Dependencies** | All dependencies must be in container image. | OS-level dependencies (such as Playwright) aren't supported. |
| **State** | Stateless only. | Stateless only. |
| **UVX/NPX** | Supported. | Not supported. `npx` start commands not supported. |
