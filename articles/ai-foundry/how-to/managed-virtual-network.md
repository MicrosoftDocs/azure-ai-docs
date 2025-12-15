---
title: Configure managed virtual network for Microsoft Foundry projects (preview)
ms.service: azure-ai-foundry
ms.date: 12/15/2025
ms.reviewer: meerakurup
ms.author: jburchel
author: jonburchel
description: Secure your Microsoft Foundry projects with managed virtual networks. Learn to enable outbound isolation and private endpoints for enhanced data protection.
#customer intent: As an IT admin, I want to configure a managed virtual network for Microsoft Foundry projects so that I can control outbound traffic securely.
ms.topic: how-to
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
---

# Configure managed virtual network for Microsoft Foundry projects

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

This article shows you how to configure a managed virtual network for a Microsoft Foundry project to control outbound traffic from Agents and Evaluations. This feature is currently in preview. After you enable managed virtual network isolation, you can't disable it. Use this configuration to apply outbound isolation modes, private endpoints, and optional Azure Firewall rules.


## Prerequisites

1. Azure subscription with required permissions to deploy Bicep templates and create network resources (Owner or Contributor + User Access Administrator) [TO VERIFY].
1. Existing Foundry hub and project or plan to create them during the template deployment.
1. CLI environment with Azure CLI installed and signed in (`az login`). Install required extensions for Foundry if applicable [TO VERIFY].
1. Access to the Bicep template: `18-managed-virtual-network-preview` in the `foundry-samples` GitHub repository [TO VERIFY: repository URL].
1. Resource group chosen for the managed virtual network deployment.
1. Confirm required IP address space availability for subnets (minimum /24 for Agent subnet).
1. Decision on outbound isolation mode before deployment.
1. List of any required approved outbound destinations (service tags, fully qualified domain names (FQDNs) limited to ports 80 and 443).
1. Plan for Azure Firewall SKU if FQDN rules are needed (Basic or Standard).
1. No existing private endpoint plus service endpoint combinations on target resources (must use private endpoints only).

## Understand isolation modes

Choose one outbound isolation mode for the managed virtual network. Agents and Evaluations use the managed virtual network automatically once enabled.

| Outbound mode | Description | Scenarios |
| --- | --- | --- |
| Allow internet outbound | Allows all outbound traffic to the internet. | Unrestricted outbound access is acceptable; broad connectivity required. |
| Allow only approved outbound | Restricts outbound using service tags, private endpoints, and optional FQDN rules (ports 80, 443) enforced via Azure Firewall. | Minimize data exfiltration risk; require curated list of destinations. |
| Disabled | Managed virtual network isolation not enabled (unless BYO virtual network used). | Need public inbound/outbound or plan to supply your own virtual network. |

The managed virtual network is pre-configured with required default rules. Private endpoints are automatically created for the hub, its default storage account, container registry, and key vault when resources are private or when isolation mode is set to Allow only approved outbound.

## Review limitations

1. Only deployable via Bicep template (`18-managed-virtual-network-preview`) at this time.
1. FQDN outbound rules require Azure Firewall and increase cost.
1. FQDN outbound rules support only ports 80 and 443.
1. Can't disable managed virtual network isolation after enabling.
1. Private endpoint required; can't mix private endpoint and service endpoint on the same resource.
1. Deleting Foundry deletes the managed virtual network.
1. No upgrade path from BYO virtual network to managed virtual network; redeploy required.
1. End-to-end network isolation for Agent MCP tools not fully supported.
1. Scenarios with MCP tools and certain third-party service integrations not yet supported.

## Plan configuration

Plan these items before deployment:

1. Isolation mode selection (see previous section).
1. Subnet CIDR blocks (ensure private Class A, B, or C; exclude public ranges such as 44.x and carrier-grade NAT 100.64.0.0/10).
1. Required private endpoints (see supported list).
1. Outbound rule set: service tags, private endpoints, and any FQDNs (ports 80, 443).
1. Azure Firewall SKU (Basic or Standard) if FQDN used.
1. Validation strategy: test connectivity from Agent and Evaluations components.
1. Cost review (Private Link + Azure Firewall if applicable).

## Deploy managed virtual network

This section deploys the managed virtual network by using the Bicep template.

1. Clone or download the `foundry-samples` repository containing `18-managed-virtual-network-preview` [TO VERIFY: git clone command].
1. Open the Bicep template parameters file.
1. Set the isolation mode parameter (placeholder name `[TO VERIFY: parameter name]`) to one of:
   - `AllowInternetOutbound`
   - `AllowOnlyApprovedOutbound`
1. Populate required project and hub identifiers (`projectName`, `hubName`, `location`) [TO VERIFY].
1. Add any initial outbound rules (service tags or private endpoints) to parameters as required.
1. Run deployment:
   `az deployment group create --resource-group <rg-name> --template-file main.bicep --parameters @main.parameters.json`
1. Wait for deployment success; review outputs for managed virtual network resource IDs.
1. Confirm private endpoints created for hub, storage account, container registry, and key vault when applicable.

:::image type="content" source="media/managed-virtual-network/managed-virtual-network-architecture.png" alt-text="Architecture diagram showing managed virtual network, hub, storage, container registry, key vault, and private endpoints." lightbox="media/managed-virtual-network/managed-virtual-network-architecture.png":::

## Configure allow internet outbound mode

Use this mode for unrestricted outbound access.

1. In the parameters file, set isolation mode to `AllowInternetOutbound`.
1. Remove or minimize explicit outbound allow lists (unnecessary for full outbound).
1. Deploy the template (see previous task).
1. Validate:
   1. Test DNS resolution and external HTTP access from Agent workload [TO VERIFY].
   1. Confirm required private endpoint outbound rules still present for private resources.

:::image type="content" source="media/managed-virtual-network/allow-internet-outbound-diagram.png" alt-text="Diagram of managed virtual network configured for allow internet outbound mode with broad outbound access." lightbox="media/managed-virtual-network/allow-internet-outbound-diagram.png":::

## Configure allow only approved outbound mode

Use this mode to restrict outbound traffic.

1. Set isolation mode to `AllowOnlyApprovedOutbound` in parameters.
1. Enumerate required service tags (for example: `Storage`, `KeyVault`, `AzureContainerRegistry`) [TO VERIFY: exact tag names].
1. Add FQDN rules only if necessary; note cost impact and port limits (80, 443).
1. Deploy template.
1. Add or update outbound rules post-deployment (see next section).
1. Validate:
   1. Attempt connection to an allowed FQDN.
   1. Confirm blocked access to an unlisted external domain.

:::image type="content" source="media/managed-virtual-network/allow-only-approved-outbound-diagram.png" alt-text="Diagram of managed virtual network in allow only approved outbound mode with Azure Firewall enforcing rules." lightbox="media/managed-virtual-network/allow-only-approved-outbound-diagram.png":::

## Manage outbound rules

Update outbound rules after deployment by using Azure REST or CLI.

1. Install or update Azure CLI: `az upgrade` (optional).
1. Retrieve current outbound rule configuration:
   `az rest --method get --url <managed-network-rules-endpoint>`
1. Prepare JSON payload for PATCH including:
   - Service tags list.
   - Private endpoint resource IDs.
   - FQDN rules (ports 80 or 443 only) if required.
1. Apply update:
   `az rest --method patch --url <managed-network-rules-endpoint> --body @rules.json`
1. Verify response status is 200.
1. Re-test connectivity for new destinations.
1. Document any rule changes for audit.

## Select Azure Firewall version

Azure Firewall is provisioned automatically when you add an outbound FQDN rule in **Allow only approved outbound** mode.

1. Default SKU is Standard; choose Basic for reduced cost if advanced features aren't required.
1. Review SKU differences.
1. Set SKU parameter in template (`firewallSku` placeholder) to `Standard` or `Basic`.
1. Re-deploy if you change SKU later; plan maintenance window.
1. Confirm billing impact after change.

## Review required rules and service tags

Don't remove required default rules. They enable core platform communication.

1. List of required service tags (Source: configure-managed-network article) [TO VERIFY].
1. Preserve tags related to identity, management, storage, and container registry.
1. Confirm private endpoint outbound rules exist for:
   - Hub
   - Storage account
   - Azure Container Registry
   - Key vault

## Supported private endpoints

You can configure private endpoints for these Azure services:

- Foundry Tools
- Azure API Management (Classic without VNet injection; Standard V2 with VNet integration)
- Azure Container Registry
- Azure Cosmos DB (all subresource types)
- Azure Data Factory
- Azure Database for MariaDB
- Azure Database for MySQL
- Azure Database for PostgreSQL Single Server
- Azure Database for PostgreSQL Flexible Server
- Azure Databricks
- Azure Event Hubs
- Azure Key Vault
- Azure Machine Learning
- Azure Machine Learning registries
- Azure Cache for Redis
- Azure SQL Server
- Azure Storage (all subresource types)
- Application Insights (via Private Link scope)

## Apply scenario-specific outbound rules

### Agent service outbound rules

1. Identify required service tags for Agent runtime [TO VERIFY].
1. Add any FQDNs for external APIs used by Agents (ports 80 or 443 only).
1. Update rules via PATCH (see Manage outbound rules).

### Evaluations outbound rules

1. List evaluation data source endpoints (private endpoints preferred).
1. Add service tags for storage and logging services.
1. Apply and validate using test evaluation run.

## Validate configuration

1. List effective outbound rules and confirm expected entries.
1. Run diagnostic:
   1. Attempt allowed destination (should succeed).
   1. Attempt disallowed destination (should fail).
1. Check private endpoint connection states in the portal.
1. Record configuration state for compliance reporting.

## Pricing considerations

You pay for:

- Azure Private Link (private endpoints).
- Azure Firewall (only if you configure FQDN outbound rules; Standard by default).
- Any additional network resources you add (for example, Application Gateway if you use it for on-premises access) [TO VERIFY].

See Azure pricing:

1. Private Link pricing: <https://azure.microsoft.com/pricing/details/private-link/>
1. Azure Firewall SKU comparison (Source: Azure Firewall documentation) [TO VERIFY].

## Compare managed and custom (BYO) network

| Aspect | Managed network | Custom (BYO) network |
| --- | --- | --- |
| Benefits | Microsoft handles subnet range, IP selection, delegation. | Full control: custom firewall, user-defined routes, peering, on-premises connectivity. |
| Limitations | Can't bring your own firewall for Allow only approved outbound; requires Application Gateway for secure on-premises (L7 only); gaps match hub managed network limitations. | More complex setup (subnet delegation to Azure Container Apps; correct CapHost creation; requires private Class A/B/C; needs /24 subnet for Agent). |
| Upgrade path | No upgrade from BYO to managed; redeploy required. | Existing deployment stays as-is. |
| Third-party integration | Limited MCP tool + third-party service networking. | Flexible integration scenarios. |

## Clean up resources

If you need to remove the configuration:

1. Delete the Foundry resource (this action deletes the managed virtual network).
1. Confirm private endpoints are removed.
1. Remove any orphaned firewall resources if you provisioned the SKU.
1. Release IP space for reuse.

## Troubleshooting

1. Deployment failure due to subnet delegation:
   - Verify the subnet is delegated to Azure Container Apps; correct and redeploy.
1. Failure creating CapHost:
   - Delete the faulty CapHost resource; redeploy the template.
1. FQDN rule not enforced:
   - Confirm the firewall SKU is provisioned; verify ports are limited to 80 or 443.
1. Private endpoint conflicts:
   - Remove any service endpoint configuration; use private endpoint only.

