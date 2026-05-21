---
title: "Troubleshoot Fabric IQ connections (preview)"
description: "Diagnose and resolve common issues when connecting Foundry agents to Microsoft Fabric with Fabric IQ, including authentication, OAuth consent, permissions, and data access errors."
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

# Troubleshoot Fabric IQ connections (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

This article helps you diagnose and resolve common issues when connecting Foundry agents to Microsoft Fabric with [Fabric IQ](tools/fabric-iq.md).

## Connection and authentication issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| `403 Forbidden` on agent calls | User missing Microsoft Fabric license | Assign the Fabric license. Wait 15–30 minutes for provisioning, then retry. |
| `401 Unauthorized` | Token audience mismatch | Ensure the token is issued for the correct Fabric resource. Use `https://ai.azure.com/.default` for Foundry-side calls. |
| `Principal does not have access to API/Operation` | Agent identity missing Foundry User role at project scope | Assign the **Foundry User** role at both account scope and project scope. See [General RBAC reference](#general-rbac-reference). |
| `403 Forbidden` with `Required scopes = [...]` | Admin consent for the required permission not granted | An Entra admin must grant tenant-wide consent. Go to **Entra ID** > **App registrations** > select the app > **API permissions** > **Grant admin consent**. |
| Agent gets no response or empty result | Fabric item index hasn't built, or item isn't published | Wait 15–30 minutes after setup. Confirm the item is published in the Microsoft Fabric portal. |
| OAuth consent page doesn't open or errors out | Redirect URI not registered in the Entra app | After Foundry creates the connection, copy the OAuth redirect URL shown and add it under **Authentication** > **Redirect URIs** in your app registration. |
| Connection fields rejected in Foundry portal | Incorrect scope string format | For ontology connections, use space-separated scopes: `https://analysis.windows.net/powerbi/api/Item.Execute.All https://analysis.windows.net/powerbi/api/Item.Read.All offline_access`. For data agent connections using BYO Entra, use `https://analysis.windows.net/powerbi/api/DataAgent.Execute.All offline_access`. |

> [!NOTE]
> Connection fields can't be edited after creation. If you enter incorrect values, delete the connection and create a new one.

## Tool and data access issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| `server_url` not reachable | Wrong URL format for the Fabric item type | Verify the URL pattern for your item type: **Ontology** — `https://{host}/v1/mcp/dataPlane/workspaces/{workspaceId}/items/{itemId}/ontologyEndpoint`. **Data agent** — `https://{host}/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent`. **Power BI semantic model** — `https://{host}/v1/mcp/powerbi`. |
| Agent doesn't use the Fabric IQ tool | Tool not triggered by the prompt | Add explicit tool guidance in the agent instructions, for example: "For enterprise data questions, use Fabric IQ." You can also set `tool_choice: "required"` to force tool use. |
| Empty results from ontology queries | Query uses table names or SQL syntax instead of business terms | Fabric IQ uses NL2Ontology — phrase questions using business entity names defined in your ontology, for example: "Which customers placed large orders?" |
| Data query returns unexpected or empty results | User lacks access to the Fabric item or underlying data sources | Confirm the signed-in user has at least `Read` access (or `Build` for Power BI semantic models) to the Fabric items and their underlying data sources. |
| `workspace_id` or `item_id` invalid | Incorrect GUID format | Copy both GUIDs from the Fabric item's browser URL, for example: `.../groups/{workspaceId}/items/{itemId}/...`. Don't modify the GUID format. |
| Fabric item not reachable from Foundry | Item not published | A Fabric admin must publish each item (ontology, data agent, or Power BI semantic model) before it can be consumed through Fabric IQ. Confirm the item is published in the Microsoft Fabric portal. |

## General RBAC reference

Most Fabric IQ authorization failures trace back to one of these role assignments:

| Error | Required role | Scope |
|---|---|---|
| `Principal does not have access to API/Operation` | **Foundry User** | Project scope: `.../accounts/{account}/projects/{project}` |
| `lacks required data action '...agents/write'` | **Azure AI User** | Account scope: `.../accounts/{account}` |
| `403 Forbidden` on Fabric IQ calls | **Foundry User** | Project scope |
| OAuth consent errors | Admin consent required | Tenant-wide (Global Administrator action) |

> [!TIP]
> Granting a role only at the account scope is not sufficient for Foundry project-level checks. Always grant the **Foundry User** role at **both** account scope and project scope for agent runtime identities.

## Related content

- [Connect agents to Microsoft Fabric with Fabric IQ](tools/fabric-iq.md)
- [Azure role-based access control in Foundry](../../concepts/rbac-foundry.md)
- [Agent identity](../concepts/agent-identity.md)
- [Troubleshoot connectors and managed MCP servers](TSG%20-%20Connectors.md)
