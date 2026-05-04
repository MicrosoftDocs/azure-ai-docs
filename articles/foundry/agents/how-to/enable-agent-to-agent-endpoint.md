---
title: "Enable incoming A2A on a Foundry agent"
description: "Expose your Foundry Agent Service agent as an A2A endpoint so other agents can discover and call it using the Agent2Agent protocol."
author: aahill
ms.author: aahi
ms.date: 05/04/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Enable incoming A2A on a Foundry agent (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

You can expose your Foundry Agent Service agent as an Agent2Agent (A2A) endpoint so that other agents can discover and call it through the [A2A protocol](https://a2a-protocol.org/latest/). When incoming A2A is enabled, Foundry publishes an agent card for your agent and accepts inbound A2A requests from external callers.

> [!NOTE]
> Foundry Agent Service supports A2A protocol **version 0.3** only.

## Supported agent types

Incoming A2A requires the responses protocol. The following agent types support it:

- **Prompt agents** — support the responses protocol by default. All prompt agents can be exposed as A2A endpoints.
- **Container agents (hosted agents)** — support incoming A2A only if the container is built to handle the responses protocol. If your container agent doesn't implement the responses protocol, you can't enable incoming A2A for it.

> [!TIP]
> This article covers how to **expose** your agent as an A2A endpoint that other agents can call. If you want your agent to **call** a remote A2A endpoint, see [Connect to an A2A agent endpoint from Foundry Agent Service](tools/agent-to-agent.md).

## Prerequisites

- An Azure subscription with an active Foundry project.
- A deployed agent in Foundry Agent Service that uses the responses protocol (prompt agent, or a container agent built to support it).
- Required Azure role: **Azure AI User** or higher on the Foundry project.

## Enable incoming A2A

Enabling incoming A2A requires two things: an **agent card** that describes your agent's capabilities, and the **A2A protocol** enabled on the agent endpoint. You can set both in a single PATCH call. This feature isn't available in the Foundry portal yet — use the REST API or Python SDK.

### REST API

Set up variables for your project:

```bash
BASE_URL="https://{account}.services.ai.azure.com/api/projects/{project}"
API_VERSION="v1"
TOKEN=$(az account get-access-token --resource https://ai.azure.com \
  --query accessToken -o tsv)
```

Send a `PATCH` request to configure the agent card and enable the A2A protocol:

```bash
curl -X PATCH "$BASE_URL/agents/{agent_name}?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: AgentEndpoints=V1Preview" \
  -d '{
    "agent_card": {
      "description": "A helpful assistant that answers questions",
      "version": "1.0",
      "skills": [
        {
          "id": "general-qa",
          "name": "General Q&A",
          "description": "Answers general questions"
        }
      ]
    },
    "agent_endpoint": {
      "protocols": ["responses", "a2a"]
    }
  }'
```

Replace `{agent_name}` with the name of your agent. Update the `agent_card` fields to describe your agent's actual capabilities. The agent card is what other agents see when they discover your A2A endpoint.

### Python SDK

Install the required package:

```bash
pip install "azure-ai-projects>=2.0.0"
```

Use the `patch_agent_details` method to add the A2A protocol to your agent's endpoint:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpoint,
    AgentEndpointProtocol,
)

# Format: "https://{account}.ai.azure.com/api/projects/{project}"
PROJECT_ENDPOINT = "your_project_endpoint"
AGENT_NAME = "your_agent_name"

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

endpoint_config = AgentEndpoint(
    protocols=[
        AgentEndpointProtocol.RESPONSES,
        AgentEndpointProtocol.A2A,
    ],
)

patched_agent = project_client.beta.agents.patch_agent_details(
    agent_name=AGENT_NAME,
    agent_endpoint=endpoint_config,
)
```

> [!NOTE]
> Setting the agent card through the Python SDK isn't supported yet. Use the REST API to configure the agent card.

## Verify the agent card

After you enable incoming A2A, external agents use the agent card to discover your agent's capabilities and supported interactions. Confirm the agent card is set by retrieving your agent's properties:

```bash
curl -X GET "$BASE_URL/agents/{agent_name}?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN"
```

The response includes the `agent_card` and `agent_endpoint` objects. Verify that `protocols` contains `a2a` and that the `agent_card` fields match your intended description and skills.

## Configure authentication for incoming requests

When other agents call your A2A endpoint, you control how those requests are authenticated. Configure authentication to ensure only authorized callers can reach your agent.

[TO VERIFY] — Describe the supported authentication methods for incoming A2A (for example, Microsoft Entra ID, API key, unauthenticated). Include setup steps for each supported method.

### Microsoft Entra ID authentication

[TO VERIFY] — Describe how to require Entra ID tokens for inbound A2A calls. Include any role assignments the calling agent's identity needs.

### Key-based authentication

[TO VERIFY] — Describe how to issue and configure an API key for inbound A2A access, if supported.

### Unauthenticated access

[TO VERIFY] — Describe whether unauthenticated inbound A2A is supported, and any security considerations.

## Limitations

- Only A2A protocol version 0.3 is supported.
- Incoming A2A requires the responses protocol. Agents that don't use the responses protocol can't be exposed as A2A endpoints.
- This feature is in preview and isn't recommended for production workloads.

## Related content

- [Connect to an A2A agent endpoint from Foundry Agent Service](tools/agent-to-agent.md)
- [Agent2Agent (A2A) authentication](../concepts/agent-to-agent-authentication.md)
- [Build with agents, conversations, and responses](../concepts/runtime-components.md)
