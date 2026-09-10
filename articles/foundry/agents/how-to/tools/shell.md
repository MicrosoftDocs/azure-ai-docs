---
title: "Add a shell tool to a toolbox (preview)"
description: "Add ShellToolboxTool to a Microsoft Foundry toolbox so agents can run shell commands in a sandboxed, network-isolated container through the toolbox MCP endpoint."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/08/2026
author: lindazqli
ms.author: zhuoqunli
ms.custom: azure-ai-agents, dev-focus
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to add a shell tool to a Microsoft Foundry toolbox so that my agent can run shell commands in a sandboxed, network-isolated container.
---

# Add a shell tool to a toolbox (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

This article shows how to add a shell tool to a Microsoft Foundry toolbox and make it available to a Microsoft Foundry prompt agent through the toolbox's Model Context Protocol (MCP) endpoint.

The shell toolbox tool provides access to a sandboxed, network-isolated container that Microsoft Foundry provisions and manages for you when you create a toolbox version. You don't need to deploy or manage container infrastructure yourself.

Use the shell toolbox tool when your agent needs to:

- Inspect the container runtime environment, such as the Python version, installed packages, or working directory.
- Run scripts and process files in an isolated execution environment.
- Automate tasks that require shell access without exposing your network.


The shell toolbox tool is a toolbox-level tool. You can add it only when creating a toolbox version by using `toolboxes.create_version(tools=[...])`. You can't add `ShellToolboxTool` directly to `PromptAgentDefinition(tools=[...])`. Instead, the prompt agent accesses the shell tool through an `MCPTool` that's configured to connect to the toolbox's MCP endpoint.

> [!NOTE]
> **Shell toolbox tool and Responses API shell tool are different tools.**
>
> Although they have similar names, they're used in different ways:
>
> - `ShellToolboxTool` is added to a toolbox and accessed by agents through the toolbox's MCP endpoint.
> - The Responses API shell tool is provided directly in a Responses API request and doesn't require a toolbox or MCP endpoint.
>
> Learn more about the [Responses API shell tool](../../../openai/how-to/shells.md).

## Prerequisites

- A [Foundry project](../../../how-to/create-projects.md) with a deployed model.
- Azure CLI installed and authenticated: `az login`
- Python SDK installed at the required minimum version: `pip install "azure-ai-projects>=2.6.0" azure-identity`

## Create a toolbox with the shell tool

Create a toolbox version that includes `ShellToolboxTool`. Foundry provisions the container environment automatically when you use `ToolboxShellContainerAutoEnvironment`. Set `allow_preview=True` on the client because `ShellToolboxTool` is a preview feature. The `tools=[shell_tool]` parameter populates the toolbox's tool list — this list is separate from an agent's `tools` list, which accepts only agent-level tools like `MCPTool`.

`ShellToolboxTool` supports the following parameters:

| Parameter | Required | Description |
| --- | --- | --- |
| `environment` | Yes | The container environment. Use `ToolboxShellContainerAutoEnvironment` or `ToolboxShellContainerReferenceEnvironment`. |
| `name` | No | A name for the tool. |
| `description` | No | A description the model uses to decide when to call the tool. |
| `allowed_callers` | No | Restricts who can invoke the tool. Values: `"direct"` (user-initiated calls) or `"programmatic"` (system-initiated calls). |

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ShellToolboxTool, ToolboxShellContainerAutoEnvironment

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
TOOLBOX_NAME = "shell-toolbox"

# allow_preview=True is required for ShellToolboxTool (preview feature)
credential = DefaultAzureCredential()
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential, allow_preview=True)

# Create a toolbox version with the shell tool in an auto-provisioned container
shell_tool = ShellToolboxTool(
    description="Runs shell commands in a sandboxed container.",
    environment=ToolboxShellContainerAutoEnvironment(),
)
toolbox_version = project.toolboxes.create_version(
    name=TOOLBOX_NAME,
    description="Toolbox with a shell tool running in an auto-provisioned container.",
    tools=[shell_tool],
)
print(f"Toolbox: {toolbox_version.name}, version: {toolbox_version.version}")
```

The output includes the version number. Copy it. You use it in the next step to build the MCP endpoint URL.

```output
Toolbox: shell-toolbox, version: 1
```

## Connect a prompt agent to the toolbox

Create a prompt agent that reaches the shell tool through `MCPTool`. The agent authenticates to the toolbox MCP endpoint by using an Entra token. After you create the agent version, configure the agent endpoint to route traffic to that version. Replace `TOOLBOX_VERSION` with the version printed in the previous step.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpointConfig,
    FixedRatioVersionSelectionRule,
    MCPTool,
    PromptAgentDefinition,
    ProtocolConfiguration,
    ResponsesProtocolConfiguration,
    VersionSelector,
)

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
TOOLBOX_NAME = "shell-toolbox"
TOOLBOX_VERSION = 1  # replace with the version from the previous step
TOOLBOX_MCP_LABEL = "shell-toolbox"
AGENT_NAME = "ShellAgent"

credential = DefaultAzureCredential()
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
    allow_preview=True,
)
token = credential.get_token("https://ai.azure.com/.default").token

# Build the versioned MCP URL and its agent-level MCP tool
toolbox_mcp_url = (
    f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}"
    f"/versions/{TOOLBOX_VERSION}/mcp?api-version=v1"
)
toolbox_mcp_tool = MCPTool(
    server_label=TOOLBOX_MCP_LABEL,
    server_url=toolbox_mcp_url,
    authorization=token,
    require_approval="never",
)

# Create an agent connected to the shell toolbox over MCP
agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions=(
            "You have shell access in a sandboxed container with no network "
            "access. Use the shell tool to answer environment questions."
        ),
        tools=[toolbox_mcp_tool],
    ),
)
print(f"Agent: {agent.name}, version: {agent.version}")

# Route the agent endpoint to the new version
agent_endpoint = AgentEndpointConfig(
    version_selector=VersionSelector(
        version_selection_rules=[
            FixedRatioVersionSelectionRule(
                agent_version=agent.version,
                traffic_percentage=100,
            )
        ]
    ),
    protocol_configuration=ProtocolConfiguration(
        responses=ResponsesProtocolConfiguration()
    ),
)
project.agents.update_details(
    agent_name=AGENT_NAME,
    agent_endpoint=agent_endpoint,
)
print("Agent endpoint configured.")
```

```output
Agent: ShellAgent, version: 1
Agent endpoint configured.
```

## Send a request and read the output

Send a request to the agent and iterate over the response output items. The Responses API returns structured output items as the model interacts with the MCP server. Two item types are relevant for the shell tool:

- **`mcp_list_tools`**: The MCP server sends the list of available tools at the start of the session. Use this item to confirm that the shell tool is reachable.
- **`mcp_call`**: Each call to the shell tool. The item includes the tool name, the arguments the model passed, the command output, and any error.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
AGENT_NAME = "ShellAgent"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)
openai = project.get_openai_client(agent_name=AGENT_NAME)

# Send a request through the agent endpoint
response = openai.responses.create(
    input=(
        "Which Python version is installed, and what is in the working "
        "directory?"
    ),
)

# Inspect the MCP output items before reading the final text response
for item in response.output:
    if item.type == "mcp_list_tools":
        tool_names = [t.name for t in (item.tools or [])]
        print(f"Available tools ({item.server_label}): {tool_names}")
    elif item.type == "mcp_call":
        print(f"Tool call: {item.name} | error: {item.error}")
        print(f"  args:   {item.arguments}")
        print(f"  output: {item.output}")

print(f"\nFinal response: {response.output_text}")
```

```output
Available tools (shell-toolbox): ['<tool-name>']
Tool call: <tool-name> | error: None
  args:   {"command": "python3 --version && ls -la"}
  output: <python-version>\n<directory-listing>

Final response: <model-response>
```

The exact tool name and container runtime depend on the provisioned environment.

## Container environment options

The `environment` parameter on `ShellToolboxTool` controls how the container is provisioned.

### Auto-provisioned container

`ToolboxShellContainerAutoEnvironment` is the default choice. Foundry provisions and manages the container for you — no container image or registry configuration required.

```python
from azure.ai.projects.models import ShellToolboxTool, ToolboxShellContainerAutoEnvironment

# Foundry provisions and manages the container automatically
shell_tool = ShellToolboxTool(
    description="Runs shell commands in a sandboxed container.",
    environment=ToolboxShellContainerAutoEnvironment(),
)
```

`ToolboxShellContainerAutoEnvironment` accepts these optional properties:

| Property | Type | Description |
| --- | --- | --- |
| `file_ids` | List of strings | File IDs to mount into the container at startup. |
| `memory_limit` | `ContainerMemoryLimit` | Container memory cap. Valid values: `"1g"`, `"4g"`, `"16g"`, `"64g"`. |
| `skills` | List | Additional skills to load into the container. |
| `network_policy` | `ToolboxShellNetworkPolicy` | Outbound network policy. When omitted, the service defaults to disabled outbound access. |

The following snippet sets a 4 GB memory limit:

```python
from azure.ai.projects.models import ShellToolboxTool, ToolboxShellContainerAutoEnvironment

# 4 GB memory limit; other optional fields (file_ids, skills, network_policy) are omitted
shell_tool = ShellToolboxTool(
    description="Runs shell commands in a sandboxed container.",
    environment=ToolboxShellContainerAutoEnvironment(memory_limit="4g"),
)
```

### Use an existing container

`ToolboxShellContainerReferenceEnvironment` lets you point the shell tool at a container you already provisioned. Pass the container's ID as `container_id` — that's the only property this class takes.

```python
from azure.ai.projects.models import ShellToolboxTool, ToolboxShellContainerReferenceEnvironment

# Reference an existing container by its ID
shell_tool = ShellToolboxTool(
    description="Runs shell commands in an existing container.",
    environment=ToolboxShellContainerReferenceEnvironment(container_id="<your-container-id>"),
)
```

## Network isolation

The shell tool's container runs without outbound network access by default. This behavior is documented: when you omit `network_policy` on `ToolboxShellContainerAutoEnvironment`, the service defaults to disabled outbound access. This default prevents the shell tool from making outbound calls to arbitrary endpoints and limits the impact of any command the model issues.

The toolbox shell tool currently exposes one network policy class:

- `ToolboxShellNetworkPolicyDisabled` (wire value `"disabled"``): Disables outbound network access from the container. This policy matches the service default.

> [!NOTE]
> Unlike the code-interpreter container policy, the toolbox shell tool doesn't offer an allowlist option. `"disabled"` is the only available network policy.

To set the policy explicitly rather than relying on the default:

```python
from azure.ai.projects.models import (
    ShellToolboxTool,
    ToolboxShellContainerAutoEnvironment,
    ToolboxShellNetworkPolicyDisabled,
)

# Explicitly disable outbound access (same as the service default)
shell_tool = ShellToolboxTool(
    description="Runs shell commands in a sandboxed container.",
    environment=ToolboxShellContainerAutoEnvironment(
        network_policy=ToolboxShellNetworkPolicyDisabled(),
    ),
)
```

For broader toolbox network isolation, including how toolbox traffic flows when your project uses a virtual network and private link, see [Network isolation for a toolbox in Microsoft Foundry](toolbox-network-isolation.md).

## Clean up resources

Delete the agent version and the toolbox when you no longer need them.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
TOOLBOX_NAME = "shell-toolbox"
AGENT_NAME = "ShellAgent"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)

# Delete the agent and its endpoint, then delete the toolbox
project.agents.delete(agent_name=AGENT_NAME, force=True)
project.toolboxes.delete(TOOLBOX_NAME)
print("Resources deleted.")
```

## Related content

- [Toolbox overview](../../concepts/toolbox-overview.md)
- [Create and manage a toolbox](toolbox.md)
- [Network isolation for a toolbox](toolbox-network-isolation.md)
- [Connect to an MCP server](model-context-protocol.md)
- [Use the shell tool with the Responses API](../../../openai/how-to/shells.md)
