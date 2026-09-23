---
title: Configure Microsoft Entra authentication for Foundry Agent trace ingestion (preview)
titleSuffix: Microsoft Foundry
description: Learn how to use Microsoft Entra authentication for Foundry Agent trace ingestion to Application Insights with managed identities and RBAC.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: anksing
ms.date: 08/06/2026
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: how-to
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer building or hosting Foundry Agents, I want to use Microsoft Entra authentication for trace ingestion so that I can avoid key-based ingestion and enforce identity-based access.
---

# Configure Microsoft Entra authentication for Foundry agent trace ingestion (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use Microsoft Entra authentication for trace ingestion when your agents send telemetry to the Application Insights resource connected to your Foundry project. This approach replaces key-based ingestion with identity-based access control.

This article applies to Foundry agents that send traces to the Application Insights resource connected to your Foundry project.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- An [Azure Monitor Application Insights resource](/azure/azure-monitor/app/app-insights-overview) to store traces (create a new one or connect an existing one).
- Access to the Application Insights resource connected to your project.
- Permission to assign Azure roles on the connected Application Insights resource, such as **User Access Administrator** at minimum. See [prerequisites for assigning roles via the Azure portal](/azure/role-based-access-control/role-assignments-portal#prerequisites).
- [Local authentication disabled](/azure/azure-monitor/app/azure-ad-authentication?tabs=python#disable-local-authentication) on the connected Application Insights resource to enforce Microsoft Entra ID-only ingestion.
- To view traces in Foundry, the [Log Analytics Reader role](/azure/azure-monitor/logs/manage-access?tabs=portal#log-analytics-reader) on the connected Application Insights resource. If the underlying Log Analytics tables are [protected](/azure/azure-monitor/logs/protected-tables-configure), also assign [Privileged Monitoring Data Reader](/azure/azure-monitor/logs/manage-access?tabs=portal#privileged-monitoring-data-reader).

## Connect Application Insights to your Foundry project

Foundry stores traces in [Application Insights](/azure/azure-monitor/app/app-insights-overview) by using [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

### Update an existing connection

[!INCLUDE [trace update connection from project details](../../includes/trace-update-connection-from-project-details.md)]

### Create a new connection

[!INCLUDE [trace setup connection from traces](../../includes/trace-setup-connection-from-traces.md)]

   - To connect an existing resource, select the resource, and then select **Connect**. 
   - To create a new resource, select **Create new**, and then complete the wizard.
    
6. In the connection creation experience, set **Auth type** to **Project Managed Identity**.
   
  :::image type="content" source="../../media/observability/tracing/trace-authentication-type-project-managed-identity.png" alt-text="Screenshot of Monitor settings showing Auth type options with Project Managed Identity available." lightbox="../../media/observability/tracing/trace-authentication-type-project-managed-identity.png":::

7. Complete the wizard and select **Create**.

A confirmation message appears when the connection succeeds.

[!INCLUDE [trace setup connection from project details](../../includes/trace-setup-connection-from-project-details.md)]

4. Before you select **Connect**, in the connection creation experience, set **Auth type** to **Project Managed Identity**.
   
    :::image type="content" source="../../media/observability/tracing/trace-authentication-type-project-managed-identity-project-details.png" alt-text="Screenshot of Create a new connection showing Auth Type set to Project Managed Identity." lightbox="../../media/observability/tracing/trace-authentication-type-project-managed-identity-project-details.png":::

After you connect the resource, your project is ready for Entra-authenticated trace ingestion. Foundry uses project Managed Identity to ingest traces to connected Application Insights. 

> [!NOTE]
> When you create the connection from the Foundry portal with **Auth type** set to **Project managed identity**, the Foundry portal assigns the **Monitoring Metrics Publisher** role to the Foundry project managed identity.

## Set up Entra authentication for hosted agent traces

For hosted agents, in addition to setting up the connection by using **Project Managed Identity**, you also need to grant the **Agent Identity** permission on the connected Application Insights resource.

This permission is required because hosted agent traces can come from two identities:

- **Foundry Agent Service** emits server-side traces by using project managed identity.
- **Agent** emits traces from code that runs in the hosted agent sandbox by using **Agent Identity**.

To assign the **Monitoring Metrics Publisher** role to the agent identity, use the Foundry portal or Azure CLI. 

### [Foundry portal](#tab/portal)

1. In the Azure portal, open the Application Insights resource connected to your Foundry project.
1. Select **Access control (IAM)**.
1. Select **Add** > **Add role assignment**.
1. Select **Monitoring Metrics Publisher**, and then select **Next**.
1. In **Members**, select the Agent Identity of hosted agent.
1. Select **Review + assign**.

For detailed portal guidance, see [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

### [Azure CLI](#tab/azure-cli)

Use this option to create the same role assignment by using Azure CLI.

1. Sign in by using Azure CLI:

   ```bash
   az login
   ```

1. Run the following command to assign **Monitoring Metrics Publisher** role:

   ```bash
   az role assignment create \
     --assignee-object-id "$AGENT_IDENTITY_OBJECT_ID" \
     --assignee-principal-type ServicePrincipal \
     --role "Monitoring Metrics Publisher" \
     --scope "$APP_INSIGHTS_RESOURCE_ID"
   ```

   Set these environment variables before running the command:
   - `APP_INSIGHTS_RESOURCE_ID`: Full resource ID of the connected Application Insights resource.
   - `AGENT_IDENTITY_OBJECT_ID`: Microsoft Entra object ID of the Agent Identity.

Reference: [`az login`](/cli/azure/reference-index#az-login), [`az role assignment create`](/cli/azure/role/assignment#az-role-assignment-create)

---


## Troubleshoot common ingestion problems

| Issue | Likely cause | Resolution |
|---|---|---|
| `Error creating connection: Multiple connection with same category (AppInsights) created, we only allow to have 1 connection for category` | A trace connection to Application Insights is already configured for the project | [Update the existing connection](#update-an-existing-connection) instead of creating a new one. |
| `azure.monitor.opentelemetry.exporter.export._base: Retryable server side error: Operation returned an invalid status 'Forbidden'. Your application might be configured with a token credential, but your Application Insights resource might be configured incorrectly.` | Application Insights isn't configured for Microsoft Entra ID authentication, or the ingestion identity is missing **Monitoring Metrics Publisher** on the connected Application Insights resource | [Disable local authentication](/azure/azure-monitor/app/azure-ad-authentication?tabs=python#disable-local-authentication) on the connected Application Insights resource to enforce Microsoft Entra ID-only ingestion, then assign **Monitoring Metrics Publisher** to the identity that sends telemetry (for example, **Project managed identity** or **Agent Identity**). |
| Traces from agent code don't show up | Agent code uses an identity that doesn't have permission to ingest telemetry, or sends data to a different Application Insights resource | [Assign **Monitoring Metrics Publisher** to the Agent Identity](#set-up-entra-authentication-for-hosted-agent-traces) on the connected Application Insights resource, and verify your runtime points to that same resource. |
| Connection is created, but traces still don't show up | Ingestion role assignment or connection settings aren't fully applied yet | [Verify the authentication type](#update-an-existing-connection) is set to **Project managed identity**, confirm role assignments for the required identity, and wait 2-5 minutes before checking the **Traces** page again. |

## Related content

- [Set up tracing in Microsoft Foundry](trace-agent-setup.md)
- [Configure tracing for AI agent frameworks](trace-agent-framework.md)
- [Agent tracing overview](../concepts/trace-agent-concept.md)
- [Microsoft Entra authentication for Application Insights](/azure/azure-monitor/app/azure-ad-authentication)
