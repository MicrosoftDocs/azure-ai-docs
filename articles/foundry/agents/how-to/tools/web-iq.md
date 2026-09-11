---
title: "Use Microsoft Web IQ in a Foundry prompt agent (preview)"
description: "Learn how to add Microsoft Web IQ to a Foundry Agent Service prompt agent by using the azure-ai-projects Python SDK."
services: cognitive-services
manager: mcleanbyron
author: mattwojo
ms.author: mattwoj
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/03/2026
ms.custom:
 - azure-ai-agents
 - dev-focus
 - doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to add Microsoft Web IQ to a Foundry prompt agent so that the agent can retrieve current web data.
---

# Use Microsoft Web IQ in a Foundry prompt agent (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

[Microsoft Web IQ](https://webiq.microsoft.ai/documentation/) is a limited-access suite of AI-native grounding APIs that gives AI systems and agents access to current information from across the web, including web pages, news, images, and videos. Web IQ builds on the Bing global index and ecosystem. You configure it as a server-side tool on a prompt agent by using the `azure-ai-projects` Python SDK (2.6.0 or later).

For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

> [!WARNING]
> When you connect to Web IQ, you might incur costs and data might be sent outside the Azure compliance boundary and processed according to the applicable service terms and data handling policies. It's your responsibility to manage whether your data flows outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This responsibility includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. See the [Foundry Agent Service transparency note](../../../responsible-ai/agents/transparency-note.md).

## Prerequisites

Before you begin, ensure you have:

- An active [Microsoft Foundry project](../../../how-to/create-projects.md) with a deployed model.
- Access to Web IQ. Web IQ is available in limited access to select Azure customers. If you don't have access, [request access](https://aka.ms/webiq-access).
- A Web IQ project connection in your Foundry project. See [Create a Web IQ project connection](#create-a-web-iq-project-connection).
- The `azure-ai-projects` Python package, version 2.6.0 or later, and the `azure-identity` Python package:

  ```bash
  pip install "azure-ai-projects>=2.6.0" azure-identity
  ```

- The Azure CLI, signed in to the subscription that hosts your Foundry project:

  ```bash
  az login
  ```

## Create a Web IQ project connection

After your access is approved, get your API key from [Web IQ Profile Management](https://webiq.microsoft.ai/profiles). For more information about using the key, see the [Web IQ Quick Start](https://webiq.microsoft.ai/documentation/).

Create a project connection that stores the key and supplies it to the Web IQ MCP endpoint:

1. In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), open your project, and then select **Tools**.
1. Select **Connect tool**, and then select **Catalog**.
1. Search for and select **Web IQ**.
1. Enter a connection name and your Web IQ API key.
1. Create the connection and copy its fully qualified resource ID. Use this value for `WEB_IQ_PROJECT_CONNECTION_ID` in the samples.

For programmatic connection creation, configure a `RemoteTool` connection with `CustomKeys` authentication. Use `https://api.microsoft.ai/v3/mcp` as the target and `x-apikey` as the credential name.

For general guidance about storing shared credentials in a project connection, see [Key-based MCP authentication](../mcp-authentication.md#key-based-authentication).

Set the following environment variables before running the samples:

- `FOUNDRY_PROJECT_ENDPOINT` — your project endpoint, found on the **Overview** page of your Foundry project.
- `WEB_IQ_PROJECT_CONNECTION_ID` — the fully qualified resource ID of your Web IQ project connection.

## Add Web IQ to a prompt agent

Use `WebIQPreviewTool` to add Web IQ directly to a server-side prompt agent. Set `allow_preview=True` on `AIProjectClient` because `WebIQPreviewTool` is a preview feature.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpointConfig,
    FixedRatioVersionSelectionRule,
    PromptAgentDefinition,
    ProtocolConfiguration,
    ResponsesProtocolConfiguration,
    VersionSelector,
    WebIQPreviewTool,
)

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
WEB_IQ_CONNECTION_ID = os.environ["WEB_IQ_PROJECT_CONNECTION_ID"]
AGENT_NAME = "web-iq-agent"

# allow_preview=True is required because WebIQPreviewTool is a preview feature
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)

web_iq_tool = WebIQPreviewTool(
    project_connection_id=WEB_IQ_CONNECTION_ID,
    require_approval="never",
)

# Create a server-side prompt agent with the Web IQ tool
agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="Use the available Web IQ tools to answer questions.",
        tools=[web_iq_tool],
    ),
    description="Prompt agent with Web IQ.",
)

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

# Send a request to the agent
openai = project.get_openai_client(agent_name=AGENT_NAME)
response = openai.responses.create(
    input="What are the latest AI news headlines today?",
)
print(f"Response: {response.output_text}")
```

The snippet creates a prompt agent with the Web IQ tool attached, configures the agent endpoint, sends a question to the endpoint, and prints the response.

## Parameter reference

The following parameters apply to `WebIQPreviewTool`.

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| `project_connection_id` | Required | string | The fully qualified resource ID of the Web IQ project connection. |
| `server_label` | Optional | string | A short label for the Web IQ MCP server. When omitted, the service defaults to the connection name extracted from `project_connection_id`. |
| `require_approval` | Optional | string | Whether the agent requires approval before executing Web IQ actions. Defaults to `"always"`. See [Approval behavior](#approval-behavior). |

## Approval behavior

The `require_approval` setting controls whether the agent pauses for human approval before it executes a Web IQ action.

| Value | Behavior |
| --- | --- |
| `"always"` (default) | The agent always requests approval before executing a Web IQ action. Your application must handle the approval step. |
| `"never"` | The agent executes Web IQ actions automatically, without requesting approval. |

The default is `"always"`. Web IQ actions don't run automatically unless you explicitly set `require_approval="never"`. To allow fully automatic operation, pass `require_approval="never"` when you construct the tool:

```python
WebIQPreviewTool(
    project_connection_id=WEB_IQ_CONNECTION_ID,
    require_approval="never",
)
```

## Related content

- [Microsoft Web IQ documentation](https://webiq.microsoft.ai/documentation/)
- [Best practices for using tools in Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Work IQ (preview)](work-iq.md)
- [Fabric IQ (preview)](fabric-iq.md)
- [Web IQ sample (Python)](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_web_iq.py)
