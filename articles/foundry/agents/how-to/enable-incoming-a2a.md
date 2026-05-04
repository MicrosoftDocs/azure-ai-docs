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

[TO VERIFY] — Exact steps for enabling the feature (portal toggle, SDK, or REST) need confirmation.

1. [!INCLUDE [foundry-sign-in](../../../includes/foundry-sign-in.md)]
1. Navigate to your agent in the Foundry portal.
1. [TO VERIFY] — Describe the portal UI for enabling incoming A2A.

## Verify the agent card

After you enable incoming A2A, Foundry Agent Service publishes an agent card at the well-known path for your agent's endpoint. External agents use this card to discover your agent's capabilities and supported interactions.

[TO VERIFY] — Describe how to confirm the agent card is live (for example, `GET <agent-endpoint>/.well-known/agent-card.json`).

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
