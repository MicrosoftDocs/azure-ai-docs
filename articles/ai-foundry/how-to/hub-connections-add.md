---
title: Create and manage connections (Hubs)
titleSuffix: Azure AI Foundry
description: Learn how to use connections in Azure AI Foundry hubs.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 09/22/2025
ms.reviewer: scottpolly
reviewer: scottpolly
ms.author: jburchel
author: jonburchel
ai-usage: ai-assisted
ms.custom:
  - hub-only
---

# Create and manage connections in Azure AI Foundry hubs

> [!NOTE]
> An alternate Foundry project connections article is available: [Add a new connection to your project (Foundry projects)](connections-add.md).

Connections in Azure AI Foundry hubs allow you to securely integrate external resources and services, such as Azure AI services and other Azure data services. This article covers hub-scoped connection tasks.

## Prerequisites

- An Azure subscription.
- An Azure AI Foundry hub with the required role assignments to create and manage connections.

## Add a connection at the hub scope

1. Open the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and navigate to your hub.
1. Select **Management center** > **Connections**.
1. Select **+ New connection** and choose the connection type (for example, Azure AI services, Azure OpenAI, Azure Storage, Azure SQL, or custom endpoint).
1. Provide the required configuration values (resource selection, endpoint URL, authentication method such as key, managed identity, or service principal).
1. Select **Create** to save the connection. The connection becomes available to all projects within the hub, subject to project-level permissions.

## Manage existing hub connections

From the **Connections** page in **Management center**:

- Select a connection name to view details, including authentication method and scope.
- Use **Edit** to update authentication credentials or rotate keys.
- Use **Disable** to temporarily prevent new usage without deleting the configuration.
- Use **Delete** to remove the connection (projects depending on it will no longer function until reconfigured).

## Network isolation considerations

When using private endpoints or VNet-injected resources, ensure the following for hub connections:

- DNS resolution for private endpoints is configured for all project subnets.
- Managed identity or service principal used by the connection has network access to the target resource.
- For storage or database connections, allow firewall rules to include the hub managed identity or necessary outbound IP ranges.

## Authentication options

Hub connections support these authentication methods (availability varies by connector type):

- Managed identity (system or user-assigned)
- Service principal (client ID/secret or certificate)
- API key (for key-based Azure AI services / OpenAI)
- SAS token (for specific storage scenarios)

Prefer managed identity wherever possible for keyless and rotated credential management.

## Rotate credentials

1. Select the connection.
2. Choose **Edit**.
3. Update the secret, key, or certificate reference.
4. Save changes. Rotation is immediate; ensure running jobs or deployments are restarted if they cached credentials.

## Auditing and monitoring

- Use Azure Activity Log to track create/update/delete events on connection resources.
- Use hub diagnostic settings to export administrative and policy logs for compliance.

## Next steps

- [Create and managed connections in Azure AI Foundry projects](./connections-add.md).
- [Secure network traffic with private link](./hub-configure-private-link.md).
