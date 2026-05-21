---
title: "Troubleshoot connectors and managed MCP servers (preview)"
description: "Diagnose and resolve common issues with connectors, managed MCP servers, OAuth consent flows, RBAC, and tool invocation in Microsoft Foundry."
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: troubleshooting
ms.date: 05/20/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Troubleshoot connectors and managed MCP servers (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

This article helps you diagnose and resolve common issues with [connectors and managed MCP servers](tools/connectors.md) in Microsoft Foundry.

## Connection setup issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| Error code `-32006` with a `consent_url` on first MCP call | First-use OAuth consent required | Open the `consent_url` from the error response in a browser and complete the OAuth flow. After consent, `overallStatus` transitions to `Connected` and subsequent calls succeed. |
| `overallStatus` stays `Unauthenticated` after OAuth connection creation | OAuth consent flow not completed | After creating an OAuth2 connection via API, complete the consent flow in the Foundry portal: open the connection, select **Authorize**, and sign in. |
| Credentials returned as `null` in GET connection response | Expected behavior for security | For CustomKeys connections, the API scrubs secrets after write. The connection still works; `null` isn't an error. |
| Can't find the connector in the Tools Catalog | Wrong filter values, or connector isn't in the catalog | The catalog is always served from `eastus` regardless of your project's region. Verify your catalog query uses `entityContainerId: "connectors-registry-prod-bl"`. |
| Connector actions not appearing after connection is created | Connection not yet fully provisioned | Wait a few seconds and retry. The Connector Namespace publishes the MCP server asynchronously after connection creation. |
| `400 Bad Request` when creating a CustomKeys connection | Required credential fields missing or field names wrong | Inspect the connector's `x-ms-connection-parameters` spec. The field `name` values in the spec are the JSON property names to use in `credentials`. |

## Tool invocation issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| `Principal does not have access to API/Operation` | Agent identity missing Azure AI User role at project scope | Grant the **Azure AI User** role to the agent's runtime identity at **both** account scope and project scope. Granting only at account scope is insufficient. See [General RBAC reference](#general-rbac-reference). |
| `lacks required data action 'Microsoft.CognitiveServices/accounts/AIServices/agents/write'` | Agent identity missing RBAC data action at account scope | Grant the **Azure AI User** role to the agent identity at account scope: `/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}`. |
| MCP server URL stale or incorrect | Server URL changes after OAuth re-authorization | After OAuth consent, re-fetch the `target` field from the connection via GET to get the active server URL. |
| Agent calls connector actions that weren't selected during setup | All available actions exposed | Edit the managed MCP server in the **Tools** view of your project to restrict the exposed action set. |
| Trigger-based connector isn't firing routine events | Connector doesn't declare trigger support | Only connectors with `"triggers"` in their `x-ms-capabilities` field can fire event-based routines. Filter on `x-ms-capabilities` in the catalog API to verify trigger support before use. |

> [!IMPORTANT]
> The `Foundry-Features: Toolboxes=V1Preview` header is required on all toolbox API calls during preview. A missing header returns a `404` or unexpected response.

## General RBAC reference

Connector and managed MCP authorization failures typically require one of the following role assignments:

| Error | Required role | Scope |
|---|---|---|
| `Principal does not have access to API/Operation` | **Azure AI User** | Project scope: `.../accounts/{account}/projects/{project}` |
| `lacks required data action '...agents/write'` | **Azure AI User** | Account scope: `.../accounts/{account}` |
| OAuth consent errors | Admin consent required | Tenant-wide (Global Administrator action) |

> [!TIP]
> The agent's runtime identity is a `ServiceIdentity`-type service principal named `{account}-{project}-{agentName}-AgentIdentity`. Grant the **Azure AI User** role at **both** account scope and project scope for this identity.

For full role assignment steps, see [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md).

## Related content

- [Add managed MCP servers powered by connector namespaces](tools/connectors.md)
- [MCP server authentication](mcp-authentication.md)
- [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md)
- [Agent identity](../concepts/agent-identity.md)
- [Troubleshoot routines](TSG%20-%20Routines.md)
