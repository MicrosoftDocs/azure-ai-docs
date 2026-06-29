---
title: "Isolate hosted agent sessions per user"
description: "Keep each user's Microsoft Foundry hosted agent sessions, conversations, and stored data private, and extend isolation to your own application's users."
author: aahill
ms.author: aahi
ms.reviewer: asultania
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/27/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: hosted-agent-manage-method

#CustomerIntent: As a developer, I want each user's hosted agent sessions to stay isolated so that one user can't see another user's sessions, conversations, or stored data.
---

# Isolate hosted agent sessions per user

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

A single hosted agent serves many users from one endpoint. This article shows you how Microsoft Foundry keeps each user's sessions, conversations, and stored data private, and how to extend that isolation to the users of your own application. By the end, you can invoke an agent and confirm that one caller can't see another caller's sessions, conversations, or stored data.

## Prerequisites

- A deployed hosted agent. To deploy one, see [Deploy a hosted agent](deploy-hosted-agent.md).
- The Azure Developer CLI Foundry extensions, for the CLI steps. See [Install the Azure Developer CLI Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated session. Run `azd auth login`, or sign in with the Microsoft Entra credential your SDK or REST client uses.
- The Foundry User role on the project.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

## Understand per-user isolation

The platform identifies each caller from their Microsoft Entra token and keeps their data private to that identity, even though every caller reaches the same agent through one shared endpoint. For each user, the following stay isolated:

- **Conversations.** Each user's conversation history - the messages, tool calls, and responses they thread through the Responses protocol - is private to that user. One user can't read or list another user's conversations.
- **Sessions.** Each caller gets their own session by default, so the sessions one user can list and manage don't include another user's sessions.
- **Stored data.** Data your agent stores for a user is scoped to that user, so it isn't returned to a different user.

Think of it as one agent serving many private workspaces. Each session also gets a private `$HOME` filesystem in its own sandbox, isolated by default because each user gets their own session. If you instead place several users in one session, that sandbox is shared - see [Multiplex multiple users in one hosted agent session](multiplex-session-users.md). For more about the session model, see [Hosted agents in Foundry Agent Service](../concepts/hosted-agents.md#isolation-model).

Typical scenarios include:

- **Per-user chat.** Each signed-in customer gets their own conversation history, sessions, and stored data.
- **Multi-tenant apps.** Each tenant's users are isolated from every other tenant's users.

You get this isolation by default. The following sections show the default path, then how to extend it to users that you authenticate yourself.

## Invoke an agent with automatic isolation

Invoke the agent as the signed-in identity. The platform creates a session scoped to that identity and returns its `agent_session_id`.

:::zone pivot="azd"

```bash
azd ai agent invoke "Summarize the latest support tickets"
```

The session belongs to the identity from `azd auth login`. A different signed-in user that runs the same command gets a separate, private session.

:::zone-end

:::zone pivot="rest"

Set up the shared variables that the REST examples use:

```bash
BASE_URL="https://my-account.services.ai.azure.com/api/projects/my-project"
API_VERSION="v1"
RESOURCE="https://ai.azure.com"
AGENT_NAME="my-agent"

az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/protocols/openai/responses?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --body '{
        "input": "Summarize the latest support tickets",
        "stream": false
    }'
```

The Microsoft Entra token on the request identifies the caller. The response payload includes the `agent_session_id` that the platform created and scoped to that identity.

:::zone-end

:::zone pivot="python"

```python
openai_client = project.get_openai_client(agent_name="my-agent")

response = openai_client.responses.create(
    input="Summarize the latest support tickets",
)
session_id = response.model_extra.get("agent_session_id")
print(f"Session: {session_id}")
```

The OpenAI client authenticates with the caller's Microsoft Entra credential, so the session is scoped to that identity.

:::zone-end

## Isolate sessions for your own users

If your application authenticates its own end users - for example, through Google, GitHub, or a custom identity provider - a trusted service can tell Foundry which end user a request belongs to, so the platform isolates sessions per end user instead of per calling service.

The service sends the end user's stable identifier in the `x-ms-user-identity` header. The platform treats the value as an opaque string and scopes the session to it. The value must be 1–256 characters and contain only letters, digits, and the characters `. _ : - @`; other values are rejected.

To pass `x-ms-user-identity`, the calling identity must hold the `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` permission on the agent. A caller without it receives a `403`. Grant this permission to your middle-tier service's identity. For more about agent permissions, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

If a service holds this permission but doesn't send the header on a request, the platform scopes that session to the service's own identity instead of an end user. Your service can mix delegated and non-delegated calls, but only requests that include `x-ms-user-identity` are isolated per end user.

> [!WARNING]
> Within delegation, the platform doesn't fence one delegated end user from another. It enforces a hard boundary only between delegated and non-delegated callers - it lets any of your delegated users into a session your app created. Give each user their own session ID; if you route two users to the same session, they can see each other's data. To deliberately share one session, see [Multiplex multiple users in one hosted agent session](multiplex-session-users.md).

:::zone pivot="rest"

```bash
az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/protocols/openai/responses?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" "x-ms-user-identity=<stable-end-user-id>" \
    --body '{
        "input": "Summarize my open tickets",
        "stream": false
    }'
```

Replace `<stable-end-user-id>` with the identifier your service assigns to the signed-in end user, such as a tenant-scoped user ID.

:::zone-end

:::zone pivot="python"

```python
openai_client = project.get_openai_client(agent_name="my-agent")

response = openai_client.responses.create(
    input="Summarize my open tickets",
    extra_headers={"x-ms-user-identity": "<stable-end-user-id>"},
)
```

Replace `<stable-end-user-id>` with the identifier your service assigns to the signed-in end user. The session is scoped to that end user rather than to the calling service.

:::zone-end

:::zone pivot="azd"

The Azure Developer CLI invokes the agent as your own signed-in identity, so it doesn't pass a delegated end-user identity. Use the REST or SDK path from your service to send `x-ms-user-identity`.

:::zone-end

## Secure the end-user identity

When you use delegated isolation, your service is the trust boundary. Choose identifiers that are stable per user, unique, and hard to guess. Reuse the same value for the same user so their sessions resume correctly.

> [!IMPORTANT]
> Derive the `x-ms-user-identity` value from an authenticated, server-side identity - never from a value the browser or client supplies directly. Otherwise, a caller can set the header to another user's identifier and read that user's data. Any service with the delegation permission can act on behalf of any end user, so grant it only to services you trust.

## Verify isolation

Confirm that two identities get two separate sessions:

1. Invoke the agent as one identity and note the returned `agent_session_id`.
1. Invoke the agent as a second identity - a different signed-in user, or a different `x-ms-user-identity` value - and note its `agent_session_id`.
1. Confirm the two IDs differ, and that listing sessions as each identity returns only that identity's sessions.

To see isolation end to end, deploy the [note-taking agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/notetaking-agent), which stores notes per session under `$HOME`: each identity's notes land in a separate session file that only that identity can list or download through the [Session Files API](manage-hosted-sessions.md#session-file-operations).

## View sessions across users

By default, each caller sees only their own sessions. An administrator or automation that holds the **Foundry User** role on the project can list and manage every session on the agent, regardless of which identity created it. To manage sessions, see [Manage hosted agent sessions](manage-hosted-sessions.md).

## Isolation keys on container protocol 1.0.0 (deprecated)

Agents on container protocol version 1.0.0 use the earlier isolation-key model, in which the caller supplies an isolation key to scope sessions instead of the platform deriving identity from the Microsoft Entra token. This model - and protocol 1.0.0 itself - is deprecated. Agents on protocol 1.0.0 continue to work until July 31, 2026; afterward, the platform blocks requests to agents that still run on protocol 1.0.0.

Upgrade to protocol 2.0.0 to get the automatic per-user isolation described earlier in this article. Protocol 2.0.0 requires the AgentServer SDK that supports it - [`azure-ai-agentserver-core`](https://pypi.org/project/azure-ai-agentserver-core/) 2.0.0b7 or later for Python, or [`Azure.AI.AgentServer.Core`](https://www.nuget.org/packages/Azure.AI.AgentServer.Core) 1.0.0-beta.26 or later for .NET. Earlier versions use protocol 1.0.0; update them as part of the upgrade.

- If you remain on protocol 1.0.0 for now, see [Pass isolation keys to a hosted agent](pass-isolation-keys.md) for how isolation keys work.
- To upgrade, see [Migrate hosted agents to the refreshed public preview](migrate-hosted-agent-preview.md).

## Troubleshoot isolation

| Symptom | Likely cause | What to try |
|---------|--------------|-------------|
| `403` with `preview_feature_required` | The preview opt-in header is missing. | Add the `Foundry-Features=HostedAgents=V1Preview` header to the request. |
| `403` or `session_not_accessible` when accessing a session | The session belongs to a different identity. | Use the same identity that created the session, or hold the Foundry User role to see other identities' sessions. |
| `403` on a request that sets `x-ms-user-identity` | The caller lacks the `UserIdentityImpersonation` permission. | Grant the `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` permission to the calling service. |
| Local runs don't isolate sessions | Local runs don't enforce isolation. | Test isolation against a deployed agent. Local mode (`--local`, `azd ai agent run`) targets a single user. |

## Related content

- [Manage hosted agent sessions](manage-hosted-sessions.md) to list, inspect, and delete sessions, including across users.
- [Multiplex multiple users in one hosted agent session](multiplex-session-users.md) when several users intentionally share one session.
- [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md) to understand how agent and user identities work.
- [Invoke a hosted agent with the Azure Developer CLI](invoke-hosted-agent.md) for every invoke variant and option.
- [Note-taking agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/notetaking-agent) for a runnable agent that stores user-owned data per session (Python and C#).
