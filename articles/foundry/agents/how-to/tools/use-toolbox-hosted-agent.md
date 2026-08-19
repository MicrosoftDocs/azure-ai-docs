---
title: "Use a toolbox with a hosted agent in Microsoft Foundry"
description: "Connect a hosted agent to a Microsoft Foundry toolbox over MCP by using Agent Framework, LangGraph, the Foundry Toolkit, or the Azure Developer CLI."
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
ms.date: 07/29/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-foundry-toolbox
# customer intent: As a developer, I want to connect my hosted agent to a Microsoft Foundry toolbox so that it discovers and calls every tool through a single managed MCP endpoint.
---

# Use a toolbox with a hosted agent

A [hosted agent](../../concepts/hosted-agents.md) runs your code in Foundry Agent Service. In this article, you connect that code to a [toolbox](../../concepts/toolbox-overview.md) so the agent discovers and calls the toolbox tools through one Model Context Protocol (MCP) endpoint.

## Prerequisites

- A [toolbox](toolbox.md) with at least one tool and a default version.
- A Microsoft Foundry project with a deployed model.
- A hosted-agent project. To create the agent and toolbox together, complete the [toolbox quickstart](../../quickstarts/quickstart-toolbox-agent.md).
- A development identity that can access the Foundry project. Sign in locally with `az login` or `azd auth login` before you run a sample.
- Any permissions required by the services behind the toolbox tools. For tools that use OAuth or Microsoft Entra identity passthrough, review [Toolbox authentication](tool-authentication.md) before you deploy the agent.

## Choose the toolbox endpoint

Use the toolbox consumer endpoint for an agent that should follow the toolbox's `default_version`:

```http
https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/mcp?api-version=v1
```

When you promote another toolbox version to default, an agent that uses this endpoint gets the new version without an endpoint change or redeployment.

Use a version-specific developer endpoint only when you need to test an immutable version before promotion:

```http
https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
```

## Authenticate the agent to the toolbox

The agent authenticates to the toolbox endpoint with its Microsoft Entra identity and the `https://ai.azure.com/.default` scope. The connection for each toolbox tool determines which identity or credential reaches the downstream service.

Don't put downstream API keys or OAuth tokens in the agent code. Configure those credentials on the project connection that the toolbox tool references. For details about supported authentication types, consent, and role requirements, see [Toolbox authentication](tool-authentication.md).

## Connect the hosted agent

:::zone pivot="python"

### Use Microsoft Agent Framework

The maintained Python sample uses `FoundryToolbox` from the Agent Framework hosting package. The class resolves the toolbox from `TOOLBOX_ENDPOINT`, or from `FOUNDRY_PROJECT_ENDPOINT` and `TOOLBOX_NAME`. It also authenticates MCP requests and forwards the hosted runtime's per-request call ID.

Install Python 3.12 or later, Azure Developer CLI (`azd`) 1.25 or later, and the `microsoft.foundry` extension before you initialize the sample.

1. Initialize a project from the [hosted-agent toolbox sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox):

   ```bash
   mkdir my-toolbox-agent && cd my-toolbox-agent
   azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox/azure.yaml
   ```

1. Set the toolbox name. The sample constructs the consumer endpoint from the project endpoint and this name:

   ```bash
   azd env set TOOLBOX_NAME <toolbox-name>
   ```

1. Run the agent locally:

   ```bash
   azd ai agent run
   ```

1. In another terminal, verify that the agent discovers the toolbox tools:

   ```bash
   azd ai agent invoke --local "List the tools you can use and briefly describe each one."
   ```

The response lists the tools that the toolbox returns from MCP `tools/list`. If the response contains no toolbox tools, see [Troubleshoot the connection](#troubleshoot-the-connection).

### Use LangGraph

Use `AzureAIProjectToolbox` when your hosted-agent code is built with LangGraph. The integration loads the toolbox tools as LangChain tools and handles authentication to the consumer endpoint.

1. Install the LangChain Azure integration and its hosting dependencies:

   ```bash
   pip install "langchain-azure-ai[hosting]>=1.2.8"
   ```

1. Set `FOUNDRY_PROJECT_ENDPOINT` in the hosted-agent environment. The runtime supplies this value after deployment. Set it yourself for local development.

1. Load the tools by toolbox name:

```python
import asyncio

from langchain_azure_ai.tools import AzureAIProjectToolbox

async def load_tools():
   toolbox = AzureAIProjectToolbox(toolbox_name="<toolbox-name>")
   tools = await toolbox.get_tools()
   print("\n".join(tool.name for tool in tools))

asyncio.run(load_tools())
```

The output contains the names that the toolbox returns from MCP `tools/list`:

```output
<tool-name>
<tool-name>
```

**Reference:** [AzureAIProjectToolbox](https://pypi.org/project/langchain-azure-ai/)

1. Pass the loaded tools to your LangGraph agent and run a prompt that requires one of the toolbox tools. For a complete implementation, see the [LangGraph toolbox sample](https://aka.ms/foundry-toolbox-langgraph).

:::zone-end

:::zone pivot="dotnet"

Use the Agent Framework Foundry hosting integration to register a toolbox by name. `AddFoundryToolboxes` constructs the consumer endpoint from `FOUNDRY_PROJECT_ENDPOINT`, calls MCP `tools/list` during startup, and adds the discovered tools to each agent request.

Install the .NET 10 SDK and Azure CLI before you run the maintained sample.

1. Start from the public [hosted toolbox sample](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/04-hosting/FoundryHostedAgents/responses/Hosted-Toolbox), or add the Foundry hosting package to an existing Agent Framework host.

1. Set these environment variables for local development:

   ```text
   AZURE_AI_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
   AZURE_AI_MODEL_DEPLOYMENT_NAME=<model-deployment-name>
   TOOLBOX_NAME=<toolbox-name>
   ```

   Foundry supplies `FOUNDRY_PROJECT_ENDPOINT` to the deployed container. Keep the toolbox name in `TOOLBOX_NAME`; other `FOUNDRY_*` variable names are reserved by the hosted runtime.

1. In `Program.cs`, register the agent with `AddFoundryResponses`, and then register the toolbox with `AddFoundryToolboxes(credential, toolboxName)`. After you build the web application, call `MapFoundryResponses` before `Run`. The public sample includes the required imports, packages, agent construction, and credential setup.

1. Start the host, and then invoke it with a prompt that requires a toolbox tool. The `/readiness` endpoint returns an unhealthy status when the host can't enumerate the toolbox tools.

:::zone-end

:::zone pivot="rest-api"

The hosted-agent toolbox integrations in this article are available for Python and .NET. To call the MCP endpoint from another runtime, use an MCP Streamable HTTP client, authenticate with a token for `https://ai.azure.com/.default`, and implement the hosted-agent runtime contract.

:::zone-end

:::zone pivot="javascript"

The hosted-agent toolbox integrations in this article are available for Python and .NET. To call the MCP endpoint from another runtime, use an MCP Streamable HTTP client, authenticate with a token for `https://ai.azure.com/.default`, and implement the hosted-agent runtime contract.

:::zone-end

:::zone pivot="vscode"

Use the Microsoft Foundry Toolkit for Visual Studio Code to scaffold a hosted-agent sample that's connected to a toolbox.

Install Visual Studio Code, the Microsoft Foundry Toolkit extension, and the extension pack for your programming language before you scaffold the project.

1. In the Activity Bar, select **Foundry Toolkit**.
1. Under **My Resources**, expand your project, and then expand **Tools**.
1. On the **Toolboxes** tab, find the toolbox, and then select **Scaffold code template**.
1. In the Command Palette, select a project folder.
1. Open the generated `README.md`, and then complete its local run and deployment steps.
1. Run a prompt that requires a toolbox tool and confirm that the agent calls the expected tool.

:::zone-end

:::zone pivot="azd"

Pass the toolbox name to a hosted-agent sample that constructs the consumer endpoint from `FOUNDRY_PROJECT_ENDPOINT`:

Install Azure Developer CLI (`azd`) 1.25 or later and the `microsoft.foundry` extension before you run these commands.

1. Inspect the toolbox and its current default version:

   ```bash
   azd ai toolbox show <toolbox-name> --output json
   ```

   The output uses the `endpoint` property. The endpoint returned by this command identifies the selected version and is useful for testing that version.

1. Store the toolbox name in the `azd` environment:

   ```bash
   azd env set TOOLBOX_NAME <toolbox-name>
   ```

1. To run the hosted agent locally, use:

   ```bash
   azd ai agent run
   ```

   To deploy the hosted agent instead, use:

   ```bash
   azd deploy
   ```

If your application accepts only a complete URL, set `TOOLBOX_ENDPOINT` to the unversioned consumer endpoint from [Choose the toolbox endpoint](#choose-the-toolbox-endpoint).

:::zone-end

## Enforce tool approval

Each entry returned by MCP `tools/list` can contain a `_meta.tool_configuration.require_approval` value:

| Value | Required runtime behavior |
| --- | --- |
| `always` | Show the proposed tool name and arguments to the user, wait for an explicit approval, and invoke the tool only after approval. Repeat this process for every call. |
| `never` | Invoke the tool without an approval prompt. |

The toolbox MCP endpoint doesn't block `tools/call` when `require_approval` is `always`. Your agent runtime must enforce the setting before every invocation. A system-prompt instruction alone doesn't enforce approval.

Use `require_approval: never` unless your runtime can pause the pending tool call, collect the user's decision, and resume or reject that exact call. To configure the value on a toolbox tool, see [Configure tool approval](toolbox.md#configure-require_approval-on-a-tool).

## Troubleshoot the connection

| Symptom | Cause and resolution |
| --- | --- |
| The agent returns no toolbox tools. | Confirm that the toolbox has a default version, the toolbox name matches, and the agent identity can access the Foundry project. |
| Startup or readiness fails. | A toolbox enumerates all its tool sources together. Check agent logs for a failing connection, unavailable MCP server, or invalid allowed-tool name. Fix or remove that source, create a new version, and promote it. |
| A tool returns `401` or `403`. | Verify the agent-to-toolbox identity and the downstream authentication configured on the tool's project connection. These are separate authorization boundaries. |
| A tool requests consent. | Return the consent request to the signed-in user and resume the call after consent. Review the tenant and role requirements in [Toolbox authentication](tool-authentication.md). |
| A version change doesn't appear. | Confirm that the agent uses the unversioned consumer endpoint and that you promoted the intended version to `default_version`. |

## Related content

- [Create and manage a toolbox](toolbox.md)
- [Toolbox authentication](tool-authentication.md)
- [Quickstart: Build a toolbox and use it with a hosted agent](../../quickstarts/quickstart-toolbox-agent.md)
