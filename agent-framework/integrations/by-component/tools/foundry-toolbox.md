---
title: Microsoft Foundry Toolbox
description: Consume Microsoft Foundry Toolbox configurations from Agent Framework agents.
zone_pivot_groups: programming-languages
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 10/06/2026
ms.service: agent-framework
ai-usage: ai-assisted
ms.custom: update-code1
---

<!--
  Language parity table - keep in sync when adding/removing sections.

  | Section                  | C# | Python | Go | Notes                         |
  |--------------------------|:--:|:------:|:--:|:------------------------------|
  | Toolbox overview         | ✅ |   ✅   | ✅ | Shared                        |
  | MCP consumption          | ✅ |   ✅   | ❌ | Hosted C# and Python samples  |
  | Managed-agent attachment | ✅ |   ✅   | ❌ | Configured in Foundry         |
  | Language availability    | ✅ |   ✅   | ✅ | Go is status guidance        |
-->

# Microsoft Foundry Toolbox

A Microsoft Foundry Toolbox is a named, versioned server-side bundle of hosted tool configurations, such as code interpreter, file search, image generation, MCP, and web search. Toolboxes let you manage tool configuration once in Foundry and reuse it across agents.

Agent Framework covers Toolbox consumption. Create and update Toolbox versions through the Foundry portal or the `azure-ai-projects` SDK.

> [!IMPORTANT]
> `FoundryToolbox` is provided by the beta `agent-framework-foundry-hosting` package and can change before stable release.

:::zone pivot="programming-language-csharp"

For a service-managed `FoundryAgent`, attach the Toolbox to the agent definition in Foundry.

For a hosted agent built with Microsoft Agent Framework, use `AddFoundryToolboxes` from `Microsoft.Agents.AI.Foundry.Hosting`, as shown in the following example.

Use a .NET 10 web project with implicit usings enabled, matching versions of `Microsoft.Agents.AI.Foundry` and `Microsoft.Agents.AI.Foundry.Hosting`, and `DotNetEnv`. Set `TOOLBOX_NAME` to an existing toolbox and `FOUNDRY_MODEL` to your model deployment. Foundry supplies `FOUNDRY_PROJECT_ENDPOINT` to the deployed host. For local model access, set `FOUNDRY_PROJECT_ENDPOINT` and sign in with Azure CLI. Hosted deployments fall back to the azd-managed `AZURE_AI_MODEL_DEPLOYMENT_NAME`. The hosting integration loads toolbox tools when `FOUNDRY_PROJECT_ENDPOINT` is available.

:::code language="csharp" source="~/../agent-framework-code/dotnet/samples/04-hosting/FoundryHostedAgents/responses/Hosted-Toolbox/Program.cs" range="27-48,54-55,58-68,71-75,80-89":::

The same hosting registration supports tools configured for per-user OAuth consent on their toolbox connections. Users still need the required permissions and consent; no separate host-registration block is needed.

For the project files and deployment instructions, see [Hosted-Toolbox](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/04-hosting/FoundryHostedAgents/responses/Hosted-Toolbox). For per-user consent setup, see [Hosted-Toolbox-AuthPaths](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/04-hosting/FoundryHostedAgents/responses/Hosted-Toolbox-AuthPaths).

:::zone-end

:::zone pivot="programming-language-python"

## Install the packages

```bash
pip install agent-framework-foundry-hosting agent-framework-foundry --pre
```

`FoundryToolbox` is imported from `agent_framework.foundry` and supplied by `agent-framework-foundry-hosting`.

## Configure the Toolbox

Set an explicit Toolbox MCP endpoint:

```bash
TOOLBOX_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<name>/mcp?api-version=v1"
```

Or let `FoundryToolbox` construct the endpoint:

```bash
FOUNDRY_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
TOOLBOX_NAME="<toolbox-name>"
```

The hosted-agent samples prefer `FOUNDRY_MODEL` locally and fall back to the azd-managed `AZURE_AI_MODEL_DEPLOYMENT_NAME` when hosted.

## Use `FoundryToolbox` with a hosted agent

`FoundryToolbox` resolves its endpoint, authenticates every MCP request with the
supplied Azure credential, forwards the Foundry per-request call ID, and
participates in the agent's connection lifecycle. It resolves platform headers
at each operation boundary and reconnects its MCP session when the effective
request identity changes. A long-lived Toolbox therefore doesn't retain an
earlier caller's call ID.

The sample creates the Toolbox, client, and credential inside the
request-scoped agent factory for deterministic ownership and cleanup. Use this
factory pattern when related resources are request-owned, but it isn't required
solely to keep Toolbox call IDs current.

:::code language="python" source="~/../agent-framework-code/python/samples/04-hosting/foundry-hosted-agents/responses/foundry_toolbox/main.py" range="19-71":::

When Toolbox Code Interpreter produces a file and the assistant response names
that file, the hosted Responses adapter emits a native
`container_file_citation` annotation with the container and file IDs. Responses
clients can use those IDs to discover and download the generated file through
the container files API.

## Expose Toolbox skills

A Toolbox can expose Agent Skills over MCP. Set `load_tools=False` when only skills should be model-visible, then add the Toolbox as a tool so its MCP session connects and use `as_skills_provider()` as a context provider.

:::code language="python" source="~/../agent-framework-code/python/samples/04-hosting/foundry-hosted-agents/responses/foundry_toolbox_mcp_skills/main.py" range="19-75":::

Approval remains enabled by default for skill operations. Disable individual approvals only for trusted, unattended scenarios.
Keep the Toolbox and its skills provider together so both use the same MCP
session. For a long-lived Toolbox, the skill discovery cache is replaced when
the effective platform-header identity changes. A custom `header_provider` used
with skills must resolve from ambient state, such as a closure or `ContextVar`,
because skill and resource reads don't receive function runtime arguments.

## Use a Toolbox with `FoundryAgent`

Attach the Toolbox to the Prompt or Hosted Agent definition in Foundry. `FoundryAgent` uses that stored tool configuration; passing a Toolbox client-side doesn't add it to the managed agent.

<a id="connect-through-raw-mcp"></a>

## Connect through MCP with `FoundryToolbox`

Use `FoundryToolbox` with `ResponsesHostServer` to connect a hosted agent to the
Toolbox MCP endpoint. The wrapper authenticates MCP requests and forwards the
current hosted request's caller context for per-user identity passthrough.
The request-scoped `agent` factory remains the simplest option when the client,
credential, and Toolbox need one cleanup boundary. A long-lived Toolbox is also
supported and reconnects before an operation when the platform-header identity
changes.

:::code language="python" source="~/../agent-framework-code/python/samples/04-hosting/foundry-hosted-agents/responses/foundry_toolbox/main.py" range="19-71":::

Set `TOOLBOX_ENDPOINT`, or set both `FOUNDRY_PROJECT_ENDPOINT` and `TOOLBOX_NAME`, as described in [Configure the Toolbox](#configure-the-toolbox). Set `FOUNDRY_MODEL` for local runs; hosted deployments fall back to the azd-managed `AZURE_AI_MODEL_DEPLOYMENT_NAME`.

## Limitations

- MCP tools inside a Toolbox use server-side authentication through a Foundry `project_connection_id`; the Agent Framework client doesn't hold the upstream MCP bearer token.
- Consuming a Toolbox as an MCP server requires client-side Entra ID authentication for the Toolbox endpoint.
- Consent-flow responses such as `CONSENT_REQUIRED` are handled while the agent runs, not while the Toolbox connection is created.

## Samples

| Sample | Description |
|---|---|
| [foundry_toolbox/main.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/04-hosting/foundry-hosted-agents/responses/foundry_toolbox/main.py) | `FoundryToolbox` with a hosted Responses agent |
| [foundry_toolbox_mcp_skills/main.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/04-hosting/foundry-hosted-agents/responses/foundry_toolbox_mcp_skills/main.py) | Toolbox-backed Agent Skills |
| [foundry_chat_client_with_toolbox.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/foundry/foundry_chat_client_with_toolbox.py) | Toolbox MCP consumption with `MCPStreamableHTTPTool` |
| [foundry_chat_client_with_toolbox_skills.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/foundry/foundry_chat_client_with_toolbox_skills.py) | Toolbox-backed skills configuration |
| [invoke_foundry_toolbox_mcp](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/invoke_foundry_toolbox_mcp) | Workflow-side MCP consumption |

:::zone-end

:::zone pivot="programming-language-go"

Go doesn't currently expose a Foundry Toolbox helper. Configure Toolboxes through Foundry and use supported local or hosted tool declarations for Go agents.

:::zone-end

## Related guidance

- [Microsoft Foundry model provider](../model-providers/microsoft-foundry.md)
- [Microsoft Foundry Agent Service](../agent-services/foundry.md)
- [Local MCP tools](../../../agents/tools/local-mcp-tools.md)
