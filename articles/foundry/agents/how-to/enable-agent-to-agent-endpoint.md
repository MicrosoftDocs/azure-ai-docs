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
- **Hosted agents** — support incoming A2A only if the hosted agent is built to handle the responses protocol. If your hosted agent doesn't implement the responses protocol, you can't enable incoming A2A for it.

> [!TIP]
> This article covers how to **expose** your agent as an A2A endpoint that other agents can call. If you want your agent to **call** a remote A2A endpoint, see [Connect to an A2A agent endpoint from Foundry Agent Service](tools/agent-to-agent.md).

## Prerequisites

- An Azure subscription with an active Foundry project.
- A deployed agent in Foundry Agent Service that uses the responses protocol (prompt agent or a hosted agent built to support it).
- Required Azure role: **Azure AI User** or higher on the Foundry project.

## Enable incoming A2A

Enabling incoming A2A requires two things: an **agent card** that describes your agent's capabilities, and the **A2A protocol** enabled on the agent endpoint. You can set both in a single PATCH call. This feature isn't available in the Foundry portal yet — use the REST API or Python SDK.

#### [Foundry portal](#tab/portal)

Enabling incoming A2A isn't yet configurable in the Foundry portal. Use the REST API or Python SDK.

#### [REST API (Bash)](#tab/rest-bash)

Set up variables for your project:

```bash
BASE_URL="https://{account}.services.ai.azure.com/api/projects/{project}"
AGENT_NAME="your-agent-name"
TOKEN=$(az account get-access-token --resource https://ai.azure.com \
  --query accessToken -o tsv)
```

Send a `PATCH` request to configure the agent card and enable the A2A protocol:

```bash
curl -X PATCH "$BASE_URL/agents/$AGENT_NAME?api-version=v1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
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

Update the `agent_card` fields to describe your agent's actual capabilities. The agent card is what other agents see when they discover your A2A endpoint.

#### [REST API (PowerShell)](#tab/rest-powershell)

Set up variables for your project:

```powershell
$BASE_URL = "https://{account}.services.ai.azure.com/api/projects/{project}"
$AGENT_NAME = "your-agent-name"
$TOKEN = az account get-access-token --resource https://ai.azure.com `
  --query accessToken -o tsv
```

Send a `PATCH` request to configure the agent card and enable the A2A protocol:

```powershell
$body = @{
    agent_card = @{
        description = "A helpful assistant that answers questions"
        version = "1.0"
        skills = @(
            @{
                id = "general-qa"
                name = "General Q&A"
                description = "Answers general questions"
            }
        )
    }
    agent_endpoint = @{
        protocols = @("responses", "a2a")
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Patch `
  -Uri "$BASE_URL/agents/$AGENT_NAME`?api-version=v1" `
  -Headers @{ Authorization = "Bearer $TOKEN" } `
  -ContentType "application/json" `
  -Body $body
```

Update the `agent_card` fields to describe your agent's actual capabilities. The agent card is what other agents see when they discover your A2A endpoint.

#### [Python SDK](#tab/python)

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

---

## Verify the agent card

After you enable incoming A2A, your agent exposes two URLs that calling agents use:

- **A2A base path** — The root URL for A2A protocol interactions with your agent:

  `https://{account}.services.ai.azure.com/api/projects/{project}/agents/{agent}/endpoint/protocols/a2a`

- **Agent card URL** — The discovery endpoint where calling agents retrieve your agent's capabilities, skills, and metadata:

  `https://{account}.services.ai.azure.com/api/projects/{project}/agents/{agent}/endpoint/protocols/a2a/agentCard/v0.3`

> [!IMPORTANT]
> Both URLs require Microsoft Entra ID authentication. Anonymous access to the agent card isn't supported. The calling agent must present a valid token with the **Azure AI User** role on the Foundry project.

To confirm your agent card is configured correctly, fetch it directly:

#### [Bash](#tab/verify-bash)

```bash
curl -X GET "$BASE_URL/agents/$AGENT_NAME/endpoint/protocols/a2a/agentCard/v0.3" \
  -H "Authorization: Bearer $TOKEN"
```

#### [PowerShell](#tab/verify-powershell)

```powershell
Invoke-RestMethod -Method Get `
  -Uri "$BASE_URL/agents/$AGENT_NAME/endpoint/protocols/a2a/agentCard/v0.3" `
  -Headers @{ Authorization = "Bearer $TOKEN" }
```

---

The response contains the agent card with the description and skills you configured. Verify that the fields match your intended capabilities.

## Configure authentication for incoming requests

Incoming A2A requests require Microsoft Entra ID authentication. Key-based and unauthenticated access aren't supported. The calling agent must present a valid Microsoft Entra token, and the identity behind that token must have the **Azure AI User** role (or higher) on the Foundry project that hosts your agent.

Two authentication patterns are supported:

### On-behalf-of (OBO) the end user

The calling agent passes through the end user's identity. Your agent receives a token that represents the actual user, so you can scope actions to that user's permissions. This pattern is appropriate when your agent needs to enforce per-user access control.

### Service identity (agent identity, service principal, or managed identity)

The calling agent authenticates with its own identity — either the platform-assigned agent identity, a service principal, or a managed identity. Your agent sees the calling service's identity, not an individual user. This pattern is appropriate for backend agent-to-agent workflows where individual user context isn't required.

To grant a calling identity access, assign the **Azure AI User** role on the Foundry project that hosts your agent. For more information about role assignments, see [Role-based access control in the Foundry portal](../../concepts/rbac-foundry.md).

## Supported A2A transports

Foundry Agent Service supports the following A2A transports for incoming requests:

| Transport | Supported |
|-----------|-----------|
| **HTTP+JSON** | ✔️ |
| **JSONRPC** | ✔️ |
| **gRPC** | ❌ |

## Connect to a Foundry A2A agent with the Python A2A SDK

The following example shows how to use the open-source [Python A2A SDK](https://github.com/a2aproject/a2a-python) to connect to a Foundry agent that has incoming A2A enabled. The SDK automatically uses its 0.3 compatibility mode based on the protocol version in the agent card.

Because the Foundry agent card requires authentication and uses a custom path (`agentCard/v0.3` instead of the default `.well-known/agent-card.json`), you configure the `httpx` client with a bearer token and pass the custom agent card path to the resolver.

Install the required packages:

```
pip install a2a-sdk==1.0.2 azure-identity==1.25.3 httpx==0.28.1
```

```python
import asyncio

import httpx

from azure.identity import DefaultAzureCredential
from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import new_text_message
from a2a.types.a2a_pb2 import (
    Role,
    SendMessageRequest,
)

# Your Foundry agent's A2A base path
A2A_BASE_URL = (
    "https://{account}.services.ai.azure.com/api/projects"
    "/{project}/agents/{agent}/endpoint/protocols/a2a"
)
# Agent card path, relative to the A2A base URL
AGENT_CARD_PATH = "agentCard/v0.3"


async def main():
    # Get a Microsoft Entra token
    credential = DefaultAzureCredential()
    token = credential.get_token("https://ai.azure.com/.default").token

    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {token}"},
        timeout=httpx.Timeout(120.0),
    ) as httpx_client:
        # Resolve the agent card from the custom path
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=A2A_BASE_URL,
            agent_card_path=AGENT_CARD_PATH,
        )
        agent_card = await resolver.get_agent_card()

        # Create a non-streaming A2A client
        config = ClientConfig(
            streaming=False,
            httpx_client=httpx_client,
        )
        client = await create_client(
            agent=agent_card, client_config=config
        )

        # Send a message to the Foundry agent
        message = new_text_message(
            "Hello, what can you do?", role=Role.ROLE_USER
        )
        request = SendMessageRequest(message=message)

        async for response in client.send_message(request):
            print(response)

        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Replace `{account}`, `{project}`, and `{agent}` with your Foundry resource name, project name, and agent name. The resolver constructs the full agent card URL by appending the relative `AGENT_CARD_PATH` to `A2A_BASE_URL`.

## Limitations

- Only A2A protocol version 0.3 is supported.
- Only **text** modality is supported. File data and other non-text modalities aren't supported.
- Incoming A2A requires the responses protocol. Agents that don't use the responses protocol can't be exposed as A2A endpoints.
- This feature is in preview and isn't recommended for production workloads.

## Related content

- [Connect to an A2A agent endpoint from Foundry Agent Service](tools/agent-to-agent.md)
- [Agent2Agent (A2A) authentication](../concepts/agent-to-agent-authentication.md)
- [Build with agents, conversations, and responses](../concepts/runtime-components.md)
