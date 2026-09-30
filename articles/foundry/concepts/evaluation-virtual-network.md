---
title: "Configure virtual network support for evaluation in Microsoft Foundry"
description: "Learn how to configure virtual network support for evaluation in Microsoft Foundry and troubleshoot network-related evaluation errors."
author: lgayhardt
ms.author: lagayhar
ms.reviewer: skohlmeier
ms.date: 09/11/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - classic-and-new
---

# Configure virtual network support for evaluation in Microsoft Foundry

Use a virtual network (VNet) to isolate evaluation traffic in Microsoft Foundry. This article helps you choose the appropriate network setup guidance, configure evaluation-specific requirements, and resolve common network-related evaluation errors.

## Prerequisites

- A Foundry project in a [region that supports VNet evaluation](#virtual-network-region-support).
- Permissions to configure network isolation and assign Azure role-based access control (RBAC) roles.
- A VNet and a subnet that you can delegate for network injection, or permission to deploy them by using the evaluation-only setup template.

## Choose network setup guidance

Use the following table to find the networking guidance for your scenario. Return to this article for requirements and troubleshooting that are specific to evaluation.

| Goal | Guidance |
|---|---|
| Understand network isolation options and configure private endpoints, DNS, firewall allow lists, and public network access. | [Configure network isolation for Microsoft Foundry](../how-to/configure-private-link.md) |
| Use the Microsoft-managed VNet solution for outbound network isolation. | [Configure a managed VNet for Foundry projects](../how-to/managed-virtual-network.md) |
| Connect a managed VNet to on-premises or non-Azure resources. | [Access on-premises resources from a Foundry managed network](../how-to/access-on-premises-resources.md) |
| Configure a full private network setup that includes Foundry Agent Service. | [Set up private networking for Foundry Agent Service](../agents/how-to/virtual-networks.md) |
| Understand Agent Service network architecture, traffic flow, subnet sizing, and IP allocation. | [Deep dive into Foundry Agent Service networking](../agents/concepts/agents-networking-deep-dive.md) |
| Use a coding agent to help plan and configure Foundry resources and networking. | [Use the Microsoft Foundry Skill in coding agents](../how-to/develop/use-microsoft-foundry-skill.md) |

## Configure evaluation network requirements

Virtual network support for evaluation requires network injection through subnet delegation. If you only need evaluation capabilities and don't require full agent support, such as Azure Cosmos DB, Azure AI Search, or a project capability host, use the simplified [evaluation-only setup template (15a)](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup). The template deploys a minimal network-secured environment for evaluation scenarios.

> [!IMPORTANT]
> To prevent evaluation and red teaming run failures, assign the **Foundry User** role to the project's managed identity at the Foundry resource scope during initial project setup.

[!INCLUDE [role-rename-note](../includes/role-rename-note.md)]

If you connect Application Insights, evaluation data is sent to it.

## Virtual network region support

You can bring your own VNet for evaluation in the following regions:

| Americas | Europe | Asia Pacific | Middle East & Africa |
|--|--|--|--|
| Brazil South | France Central | Australia East | South Africa North |
| Canada Central | Germany West Central | Japan East | UAE North |
| Canada East | Italy North | Korea Central |  |
| East US | Norway East | South India |  |
| East US 2 | Poland Central | Southeast Asia |  |
| North Central US | Spain Central |  |  |
| South Central US | Sweden Central |  |  |
| West US | Switzerland North |  |  |
| West US 2 | UK South |  |  |
| West US 3 | West Europe |  |  |

## Configure virtual network support for data generation

Synthetic data generation and trace-to-dataset generation use the same network injection through subnet delegation as evaluation. Use the [evaluation-only setup template (15a)](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup) to deploy the required network-secured environment.

For data-generation region availability, see [Supported regions for data generation](evaluation-regions-limits-virtual-network.md#supported-regions-for-data-generation).

## Troubleshoot virtual network evaluation errors

### Diagnose your virtual network configuration

Run the [VNet project setup diagnostic](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup/vnet-project-setup-diagnostic/usage.md) from a machine that has private connectivity to your virtual network. The script inspects an existing Foundry project configuration and its network connectivity without running an evaluation or changing Azure resources.

Follow the usage guide to prepare the prerequisites, run the appropriate diagnostic checks, and review the generated `diagnostics.md` report. The report provides actionable findings, supporting evidence, known limitations, and remediation guidance to help you resolve configuration issues.

### Evaluation run remains in progress until it times out

An evaluation run can remain **In progress** because the network isolation setup is incomplete, required private endpoints aren't configured while public network access is disabled, or the project's managed identity doesn't have permission to update the run status.

To resolve the issue:

1. Verify that network injection and subnet delegation are configured as described in [Configure network isolation for Microsoft Foundry](../how-to/configure-private-link.md). If you only need evaluation capabilities, compare your deployment with the [evaluation-only setup template (15a)](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup).
1. If public network access is disabled, verify that the required private endpoints are configured and approved, and that private DNS resolves the resource endpoints from the network that was injected to Foundry project.
1. Ensure the Foundry project has capability host setup. We do need the capability host both at Foundry account and project level. If you didn't setup Foundry project level capability host use the bicep template [add-project-capability-host](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/15a-private-network-evaluation-only-setup/modules-network-secured/add-project-capability-host.bicep) to setup.
1. Verify that the project's managed identity has the **Foundry User** role at the Foundry resource scope.
1. For a large dataset, run an evaluation against a smaller representative subset. If the smaller run completes, reduce the dataset size or split the dataset across multiple evaluation runs.

### Evaluation run fails to start with a 403 error

The error states that network access is disabled, public network access is disabled but the evaluation service can't reach one or more required resources through the VNet.

`Error: Public access is disabled. Please configure private endpoint.`

To resolve the issue:

1. Identify the resource hostname in the error details or evaluation diagnostics.
1. Verify that network injection and subnet delegation are configured for evaluation.
1. Verify that the private endpoint for the affected resource is configured and approved.
1. Verify that private DNS resolves the hostname and that network rules allow access from within the VNet.
1. Retry the evaluation run after the network configuration changes take effect.

For other `403` errors, verify the RBAC assignments for the user who starts the run and for the project's managed identity. For more evaluation-specific issues, see [Troubleshoot evaluation and observability issues](../observability/how-to/troubleshooting.md).

### Custom DNS doesn't resolve private endpoints

If you define a [custom DNS server](/azure/virtual-network/manage-virtual-network#change-dns-servers) for a virtual network, the system doesn't automatically query private DNS zones linked to that virtual network. The custom DNS settings override the name resolution order.

To enable custom DNS to resolve the private zone, use an [Azure DNS Private Resolver](/azure/dns/dns-private-resolver-overview) in a virtual network linked to the private zone. For configuration guidance, see [Centralized DNS architecture](/azure/dns/private-resolver-architecture#centralized-dns-architecture).

If your custom DNS server runs on an Azure virtual machine, configure a conditional forwarder for the private zone. Set the forwarder's destination to the Azure DNS IP address, `168.63.129.16`.
