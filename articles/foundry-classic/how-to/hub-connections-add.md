---
title: Create and manage connections (Hubs)
titleSuffix: Microsoft Foundry
description: Learn how to use connections in Microsoft Foundry hubs.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/05/2026
ms.reviewer: scottpolly
reviewer: scottpolly
ms.author: jburchel
author: jonburchel
ai-usage: ai-assisted
ms.custom:
  - hub-only
  - dev-focus
---

# Create and manage connections in Microsoft Foundry hubs

> [!TIP]
> For more information, see [Add a new connection to your project (Foundry projects)](connections-add.md).

By using connections in Microsoft Foundry hubs, you can securely integrate external resources and services, such as Foundry Tools and other Azure data services. This article covers hub-scoped connection tasks.

## Prerequisites

- An Azure subscription.
- A Microsoft Foundry hub.
- Hub permissions: **Owner**, **Contributor**, or **Azure AI Developer** on the hub.
- If the connection uses **Microsoft Entra ID** to access an Azure resource, the hub managed identity must have the required roles on the target resource. For examples, see [Role-based access control for Microsoft Foundry (Hubs and Projects)](../concepts/hub-rbac-foundry.md).

## Add a connection at the hub scope

1. Open the [Foundry portal](https://ai.azure.com/?cid=learnDocs) and navigate to your hub.
1. Select **Management center** > **Connections**.
1. Select **+ New connection** and choose the connection type (for example, Foundry Tools, Azure OpenAI, Azure Storage, Azure SQL, or custom endpoint).
1. Provide the required configuration values (resource selection, endpoint URL, authentication method such as key, managed identity, or service principal).
1. Select **Create** to save the connection. The connection becomes available to all projects within the hub, subject to project-level permissions.

## Validate the connection

1. In **Management center**, select **Connections**.
1. Confirm your connection appears in the list.
1. Select the connection name and confirm the **Scope** is **Hub** and the connection is enabled.

## Manage existing hub connections

From the **Connections** page in **Management center**:

- Select a connection name to view details, including authentication method and scope.
- Use **Edit** to update authentication credentials or rotate keys.
- Use **Disable** to temporarily prevent new usage without deleting the configuration.
- Use **Delete** to remove the connection. Projects depending on the connection stop functioning until you reconfigure them.

## Network isolation considerations

When using private endpoints or VNet-injected resources, ensure the following for hub connections:

- DNS resolution for private endpoints is configured for all project subnets.
- Managed identity or service principal used by the connection has network access to the target resource.
- For storage or database connections, allow firewall rules to include the hub managed identity or necessary outbound IP ranges.

## Authentication options

Hub connections support these authentication methods. Availability varies by connector type:

- Managed identity (system or user-assigned)
- Service principal (client ID/secret or certificate)
- API key (for key-based Foundry Tools / OpenAI)
- SAS token (for specific storage scenarios)

Use managed identity whenever possible for keyless and rotated credential management.

## Rotate credentials

1. Select the connection.
1. Select **Edit**.
1. Update the secret, key, or certificate reference.
1. Save your changes. Rotation is immediate. If running jobs or deployments cached credentials, make sure you restart them.

## Auditing and monitoring

- Use Azure Activity Log to track create, update, and delete events on connection resources.
- Use hub diagnostic settings to export administrative and policy logs for compliance.

## Next steps

- [Create and manage connections in Foundry projects](./connections-add.md).
- [Secure network traffic with private link](./hub-configure-private-link.md).
