---
title: "Use on-behalf-of flow with hosted agents in Microsoft Foundry"
description: "Understand delegated access with Microsoft Foundry hosted agents, including the OBO token exchange, x-client-* headers, and end-user identity."
author: ankitbko
ms.author: anksinha
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/26/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Use on-behalf-of flow with hosted agents in Microsoft Foundry

A hosted agent sometimes needs to access data as the signed-in user rather than with its own agent identity. For example, an agent can read a user's Microsoft Graph profile with delegated `User.Read` permission. The downstream API authorizes the operation using the user's access and the application's consented delegated scopes.

In Microsoft Foundry, you can combine a Microsoft Entra on-behalf-of (OBO) token exchange with `x-client-*` header forwarding to enable this access. Your application backend exchanges the user's token for a downstream token, then passes that token to your hosted-agent code. It also sends `x-ms-user-identity` so Foundry associates the request with the represented user.

This is **application-managed OBO and token forwarding**, not a token exchange performed by Foundry. The following sections explain the flow, the three request headers, and the minimal code your agent needs.

## Prerequisites

- A hosted agent that uses container protocol version 2.0.0. The Python example uses the Responses adapter. See [Hosted agent runtime contract](../concepts/hosted-agent-contract.md).
- A trusted application backend that authenticates users and can perform OBO as a confidential client. Its app registration needs the downstream delegated permissions and consent, such as Microsoft Graph `User.Read`. See [Microsoft identity platform OBO flow](/entra/identity-platform/v2-oauth2-on-behalf-of-flow).
- A backend workload identity, such as a managed identity or service principal, with **Foundry Agent Consumer** at the agent or project scope.
- The custom data action `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` assigned to that same workload identity. This permission enables `x-ms-user-identity` and isn't included in built-in roles. An administrator must grant it as described in [Delegate the end-user identity](../concepts/hosted-agent-permissions.md#delegate-the-end-user-identity).

## Understand the delegated access flow

The backend acts as a middle tier: it remains the caller authorized to invoke Foundry, while the agent accesses the downstream API for the user. End users don't need Foundry role assignments in this pattern.

:::image type="content" source="../media/hosted-agents/hosted-agent-obo-flow.svg" alt-text="Sequence diagram showing the OBO exchange, separate Foundry workload authentication, three invocation headers, and the agent's delegated downstream call." lightbox="../media/hosted-agents/hosted-agent-obo-flow.svg":::

The flow has six steps:

1. **Authenticate the user.** The client sends a user access token whose audience is the middle-tier API. The backend validates the token and authorizes the user's request.
1. **Exchange the user token.** The backend authenticates to Microsoft Entra ID as a confidential client and submits the user token as the OBO assertion. Entra ID issues a delegated token for the requested downstream API, subject to consent and policy.
1. **Authenticate to Foundry separately.** The backend obtains a workload token with the `https://ai.azure.com/.default` scope. This token authorizes the backend to invoke the agent; it doesn't represent the user's downstream permissions.
1. **Send tokens and user context.** The backend invokes the hosted agent with its Foundry token in `Authorization`, the downstream token in `x-client-graph-access-token`, and the user's object ID in `x-ms-user-identity`.
1. **Resolve and forward the request.** Foundry authenticates the workload, checks its permission to represent the user, and creates trusted per-request user context. The service forwards the `x-client-*` header to the container, but not the caller's `Authorization` header.
1. **Call the downstream API.** Your agent code reads the delegated token (obtained from the `x-client-*` header) and uses it in `Authorization` on the downstream request. The API applies the user's delegated permissions and returns the authorized data.

The three tokens serve different purposes and aren't interchangeable. The OBO exchange changes the token's audience without changing which user is represented.

A token issued for the middle-tier API can't be used directly against Microsoft Graph. Similarly, an app-only token can't serve as the user assertion for OBO.

Your agent's identity isn't combined with the delegated token. Downstream access reflects the user and the application that performed OBO, not any application permissions assigned to the hosted agent.

## Distinguish the three request headers

The headers solve different problems and aren't interchangeable:

| Header on the Foundry request | Value | What it does |
| --- | --- | --- |
| `Authorization` | `Bearer <foundry-workload-token>` | Authenticates the immediate caller to Foundry. The service doesn't forward it to the container. |
| `x-client-graph-access-token` | The delegated Microsoft Graph access token, without a `Bearer` prefix. | Transports the token to your code. Your agent adds `Bearer` when calling Graph. The name is application-defined; the `x-client-` prefix enables forwarding. |
| `x-ms-user-identity` | The authenticated user's Microsoft Entra object ID, not a token. | Tells Foundry which user the authorized backend represents, enabling per-user conversation isolation. It doesn't grant downstream API access. |

Foundry doesn't exchange or refresh the token in `x-client-*`. Microsoft Graph validates it when your agent calls Graph. Treat downstream tokens as opaque; don't decode or validate tokens for an API you don't own.

Derive `x-ms-user-identity` from the validated user context used for the OBO exchange. Both headers must refer to the same user. Don't copy an object ID or token from untrusted client-supplied headers.

## Pass the tokens and user identity

Use your existing backend's OBO implementation rather than building a separate authentication flow inside the agent.

1. Acquire a delegated token for the downstream API. For Microsoft Graph `/me`, request `https://graph.microsoft.com/User.Read`. Use a supported authentication library, such as MSAL, and obtain consent before the OBO request. For implementation details, see [Acquire tokens with MSAL Node](/entra/msal/javascript/node/acquire-token-requests#on-behalf-of-flow) and the [OBO sample](https://github.com/AzureAD/microsoft-authentication-library-for-js/tree/dev/samples/msal-node-samples/on-behalf-of).
1. Acquire the backend's Foundry workload token, then send all three headers on the same request:

   ```http
   POST <hosted-agent-responses-endpoint> HTTP/1.1
   Authorization: Bearer <foundry-workload-token>
   Content-Type: application/json
   x-client-graph-access-token: <delegated-graph-access-token>
   x-ms-user-identity: <authenticated-user-object-id>

   {
     "input": "Show my profile.",
     "stream": false,
     "background": false,
     "store": false
   }
   ```

   Reference: [Custom header forwarding](../concepts/hosted-agent-contract.md#forward-custom-request-headers-to-your-container), [End-user identity delegation](../concepts/hosted-agent-permissions.md#delegate-the-end-user-identity).

   Replace `<hosted-agent-responses-endpoint>` with your deployed agent's full Responses URL: `https://<account>.services.ai.azure.com/api/projects/<project>/agents/<agent>/endpoint/protocols/openai/responses?api-version=v1`.

1. Check both the HTTP status and the Responses status. A successful invocation has `status: completed`; a handler failure can appear in the Responses lifecycle even when HTTP succeeds.

This example keeps execution in the foreground and doesn't store the response. `x-ms-user-identity` is included even though the request doesn't use conversation history, so Foundry and the downstream API represent the same user.

## Read the token in your agent

The Python Responses adapter exposes forwarded `x-client-*` headers through `ResponseContext.client_headers`, with lowercase keys. The following helper reads the token for the current request and calls a fixed Microsoft Graph endpoint.

- Use an existing Responses handler with `azure-ai-agentserver-responses` and `httpx` installed. For server setup, see the [Python Responses sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/hello-world).
- Call `await read_user_profile(context)` from your handler and use the returned display name in its response.

```python
import httpx
from azure.ai.agentserver.responses import ResponseContext


async def read_user_profile(context: ResponseContext) -> str:
    token = context.client_headers.get("x-client-graph-access-token")
    if not token:
        raise PermissionError("A delegated Graph token is required.")

    async with httpx.AsyncClient(
        timeout=30, follow_redirects=False
    ) as client:
        response = await client.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {token}"},
            params={"$select": "displayName"},
        )
        response.raise_for_status()
        return response.json()["displayName"]
```

Reference: [ResponseContext](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/agentserver/azure-ai-agentserver-responses#key-concepts), [Microsoft Graph get user](/graph/api/user-get?view=graph-rest-1.0&preserve-view=true), [HTTPX AsyncClient](https://www.python-httpx.org/api/#asyncclient).

The helper returns the signed-in user's display name, or raises an error if the token is missing or Graph rejects the request. It doesn't send the token to a model, persist it, or fall back to the agent's own identity.

## Keep user identity and state aligned

Downstream authorization and Foundry user isolation are separate. Forwarding a delegated token doesn't, by itself, identify the user to Foundry. Without `x-ms-user-identity`, Foundry sees the backend workload as the caller, even when each request carries a different user's downstream token.

With authorized end-user delegation on protocol 2.0.0, Foundry exposes the resolved user through `get_request_context().user_id` in the Python AgentServer SDK. Use that trusted context for user-owned state, not an arbitrary `x-client-user-id` value. The platform also supplies a per-request call ID for supported calls to Foundry services; that call ID isn't a Microsoft Graph access token.

Foundry scopes platform-managed conversation history to the resolved user. Your container must separately partition its own files, database rows, and caches by session and resolved user ID. See [Multiplex multiple users in one hosted agent session](multiplex-session-users.md).

## Choose the authentication approach

Use token forwarding only when the backend and hosted-agent container are trusted components of the same application. Passing a bearer token into the container gives its code access to the token's delegated permissions.

| Approach | Use it when |
| --- | --- |
| Application-managed OBO and `x-client-*` forwarding | Your custom agent code must call a downstream API directly with the user's delegated permissions. Your application owns consent, token acquisition, and token handling. |
| [Toolbox authentication](tools/tool-authentication.md) | A supported tool and authentication mode meet your needs. The toolbox handles downstream authentication outside your agent code. |
| Backend calls the downstream API | The agent only needs the resulting data. Passing data instead of a bearer token reduces token exposure. |
| Agent application permissions | The workload is autonomous and doesn't act as a signed-in user. Don't use this approach as a fallback when delegated access fails. |

## Protect tokens and handle expiration

> [!CAUTION]
> Keep tokens out of prompts, model inputs, request bodies, response metadata, conversation history, checkpoints, outputs, exceptions, and logs. Redact both `Authorization` and the custom token header in proxies and telemetry.

A forwarded token remains valid only for its issued lifetime and downstream audience. Header forwarding doesn't extend that lifetime or provide refresh capability.

- Request only the necessary delegated scopes. Use a separate token for each downstream audience, and never send refresh tokens or confidential-client credentials to the agent.
- Keep tokens request-scoped and restrict them to approved HTTPS destinations. Don't let model output choose a URL that receives a token, and don't follow redirects with credentials.
- For longer work, split operations into requests so the backend can obtain fresh tokens. Don't persist token-bearing headers for background execution or crash recovery.
- Return authentication failures to the backend to reacquire a token or challenge the user. If consent or Conditional Access requires interaction, preserve the [OBO claims challenge](/entra/identity-platform/v2-oauth2-on-behalf-of-flow#error-response-example). Never switch silently to app-only access.

## Verify the flow and troubleshoot

Test through your deployed backend and Foundry Service, not just the local container.

1. Sign in as two different users who each consent to the required permissions, and invoke the agent for each user. Confirm that Graph returns each user's own profile.
1. Remove the `x-client-graph-access-token` header in a controlled test. Confirm that the agent fails without calling Graph.
1. Use an expired or invalid Graph token. Confirm that the failure reaches the backend without an app-only retry.
1. If you use conversation history, verify that one user can't continue another user's response chain. Follow [Verify isolation](multiplex-session-users.md#verify-isolation).

Use the failure location to identify which part of the flow needs attention:

| Symptom | Check |
| --- | --- |
| OBO rejects the assertion. | The incoming token must represent a user and be issued for the middle-tier API. Check consent and Conditional Access requirements. |
| Foundry returns HTTP 403. | The backend needs both **Foundry Agent Consumer** and the custom `UserIdentityImpersonation/action` permission for this example. |
| The custom token header is missing in the handler. | Use the `x-client-` prefix and a lowercase lookup key. Check whether a proxy removed the header. |
| Graph returns HTTP 401 or 403. | Check token expiration, the requested resource, delegated scopes, consent, policy, and the user's access. |
| Users see another user's data. | Align the OBO user with `x-ms-user-identity`, then check conversation ownership and container-owned state partitioning. |

## Related content

- [Hosted agent runtime contract](../concepts/hosted-agent-contract.md) describes header forwarding and platform-generated user context.
- [Microsoft identity platform OBO flow](/entra/identity-platform/v2-oauth2-on-behalf-of-flow) explains token audiences, consent, and authentication challenges.
- [Toolbox authentication](tools/tool-authentication.md) describes managed alternatives to application-owned token forwarding.
