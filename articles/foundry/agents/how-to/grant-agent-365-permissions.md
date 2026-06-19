---
title: "Grant Agent 365 observability permissions"
description: "Learn how to grant a Foundry Hosted agent permission to export telemetry to Microsoft Agent 365 by assigning the required app role in Microsoft Entra ID."
author: deeikele
ms.author: deeikele
ms.reviewer: jburchel
ms.date: 06/05/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
#CustomerIntent: As a platform engineer, I want to grant a hosted agent permission to export telemetry to Agent 365 so that observability data can flow correctly.
---

# Grant Agent 365 observability permissions

Grant your Foundry Hosted agent permission to export telemetry to Microsoft Agent 365 by assigning the `Agent365.Observability.OtelWrite` app role to the hosted agent's managed identity.

Use this procedure when your hosted agent is configured to send telemetry to Agent 365 and needs Microsoft Entra permission to write observability data.

## Prerequisites

- Azure CLI 2.x or later, signed in. Run `az --version` to confirm.
- **Global Administrator** or **Application Administrator** role in Microsoft Entra ID to manage app role assignments.
- A Foundry Hosted Agent deployed and configured to send telemetry to Agent 365. See [Configure Agent 365 data collection for Microsoft Foundry](./configure-agent-365-data-collection.md).
- Access to the resource group name and hosted agent resource name so you can retrieve the managed identity object ID.
- A tenant where the `Agent365Observability` service principal exists.

> [!NOTE]
> The hosted agent must have a system-assigned managed identity enabled. If `az resource show` in step 1 returns an empty `principalId`, see [Troubleshooting](#troubleshooting).

## Identify the required IDs

Collect the three values you need before you assign the app role.

| Value | Description | Example |
| --- | --- | --- |
| `principalId` | Hosted agent managed identity service principal object ID | `47bd3468-237c-4542-8e5a-ca37993e9605` |
| `resourceId` | `Agent365Observability` service principal object ID in your tenant | `9918adcd-eb42-4743-a98e-71027476fd7a` |
| `appRoleId` | `Agent365.Observability.OtelWrite` app role ID | `8f71190c-00c8-461d-a63b-f74abde9ba52` |

1. Get the object ID of the hosted agent's managed identity service principal:

   ```bash
   az resource show \
     --resource-group <RESOURCE_GROUP> \
     --name <AGENT_NAME> \
     --resource-type "Microsoft.MachineLearningServices/workspaces" \
     --query "identity.principalId" \
     --output tsv
   ```

   Save this value as `<AGENT_PRINCIPAL_ID>`. If the command returns an empty value, see [Troubleshooting](#troubleshooting).

1. Get the object ID of the `Agent365Observability` service principal:

   ```bash
   az rest --method GET \
     --uri "https://graph.microsoft.com/v1.0/servicePrincipals?\$filter=displayName eq 'Agent365Observability'" \
     --query "value[0].id" \
     --output tsv
   ```

   > [!NOTE]
   > These commands use bash syntax. In PowerShell, escape the dollar sign with a backtick: `` `$filter ``. Alternatively, enclose the entire URI in single quotes, which suppresses variable expansion in PowerShell.

   Save this value as `<AGENT365_OBSERVABILITY_SP_ID>`.

> [!NOTE]
> The `appRoleId` value is fixed and doesn't vary by tenant — it's the well-known identifier for the `Agent365.Observability.OtelWrite` role. Copy it directly from the table above; you don't need to retrieve it with a command.

## Assign the observability app role

Assign the `Agent365.Observability.OtelWrite` app role to the hosted agent's managed identity.

> [!NOTE]
> Replace both occurrences of `<AGENT_PRINCIPAL_ID>` in the following command — one appears in the URI path and one in the request body. Replace `<AGENT365_OBSERVABILITY_SP_ID>` with the `Agent365Observability` service principal object ID. Keep the `appRoleId` value as-is.

1. Run the command:

   ```bash
   az rest --method POST \
     --uri "https://graph.microsoft.com/v1.0/servicePrincipals/<AGENT_PRINCIPAL_ID>/appRoleAssignments" \
     --body '{
       "principalId": "<AGENT_PRINCIPAL_ID>",
       "resourceId": "<AGENT365_OBSERVABILITY_SP_ID>",
       "appRoleId": "8f71190c-00c8-461d-a63b-f74abde9ba52"
     }'
   ```

   A successful request returns HTTP 201 with a JSON object containing the assignment details, including `principalId`, `resourceId`, and `appRoleId`.

   > [!NOTE]
   > The `--body` value uses single-quoted JSON, which is valid in bash. In PowerShell, save the JSON to a file and pass it with `--body @body.json`, or use a here-string with escaped inner double quotes.

## Verify the assignment

Verify that the role assignment exists before you test telemetry export.

1. Run the following command:

   ```bash
   az rest --method GET \
     --uri "https://graph.microsoft.com/v1.0/servicePrincipals/<AGENT_PRINCIPAL_ID>/appRoleAssignments" \
     --query "value[?appRoleId=='8f71190c-00c8-461d-a63b-f74abde9ba52']"
   ```

1. Confirm that the response includes an assignment for the `Agent365.Observability.OtelWrite` app role.
1. After the assignment is present, test your hosted agent telemetry flow by reviewing traces in Microsoft Agent 365. See [Configure Agent 365 data collection for Microsoft Foundry](./configure-agent-365-data-collection.md).

> [!NOTE]
> App role assignments can take a few minutes to propagate. If telemetry export fails immediately after assignment, wait 2–5 minutes and try again.

## Troubleshooting

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `az resource show` returns an empty `principalId` | The hosted agent doesn't have a system-assigned managed identity enabled. | Enable the system-assigned managed identity on the agent resource in the Foundry portal or contact your administrator. |
| `Agent365Observability` service principal not found | The Agent 365 observability service isn't provisioned in your tenant. | Contact your Microsoft 365 administrator to verify the service is enabled for your tenant. |
| `POST` returns HTTP 403 | The signed-in user lacks permission to create app role assignments. | Confirm the signed-in account has **Global Administrator** or **Application Administrator** role in Microsoft Entra ID. |
| `az rest` returns HTTP 401 | The Azure CLI session isn't authorized to call the Microsoft Graph API. | Re-authenticate with a Graph scope: `az login --scope https://graph.microsoft.com/.default`. |
| Duplicate assignment conflict (HTTP 409) | The app role is already assigned to the managed identity. | Verify the existing assignment with the GET command in [Verify the assignment](#verify-the-assignment). No further action is needed. |
| Verification GET returns an empty array | The assignment hasn't propagated yet, or `<AGENT_PRINCIPAL_ID>` doesn't match the value from `az resource show`. | Wait 5 minutes and re-run the GET command. Confirm `<AGENT_PRINCIPAL_ID>` matches the `az resource show` output exactly. |

## Related content

- [Microsoft Agent 365 integration with Foundry](../concepts/agent-365-integration.md)
- [Configure Agent 365 data collection for Microsoft Foundry](./configure-agent-365-data-collection.md)
- [Trace agent overview](../../observability/concepts/trace-agent-concept.md)