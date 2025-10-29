﻿---

title: How to configure a private link for Azure AI Foundry projects
titleSuffix: Azure AI Foundry
description: Learn how to configure a private link for Azure AI Foundry projects. A private link is used to secure communication with the Azure AI Foundry.
manager: mcleans
ms.service: azure-ai-foundry
ms.custom: ignite-2023, devx-track-azurecli, build-2024, ignite-2024
ms.topic: how-to
ms.date: 09/12/2025
ms.reviewer: meerakurup
ms.author: jburchel 
author: jonburchel 
ai-usage: ai-assisted
# Customer intent: As an admin, I want to configure a private link for hub so that I can secure my hubs.

---

# How to configure a private link for Azure AI Foundry (Foundry projects)

> [!NOTE]
> An alternate hub-focused version of this article is available: [How to configure a private link for an Azure AI Foundry hub](hub-configure-private-link.md).

When using a [!INCLUDE [fdp-projects](../includes/fdp-project-name.md)], you can use a private link to secure communication with your project. This article describes how to establish a private connection to your project using a private link. 

## Prerequisites

* You must have an existing Azure Virtual Network to create the private endpoint in. 

    > [!IMPORTANT]
    > We don't recommend using the 172.17.0.0/16 IP address range for your VNet. This is the default subnet range used by the Docker bridge network on-premises.

## Securely connect to Foundry

To connect to Foundry secured by a virtual network, use one of these methods:

* [Azure VPN Gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways)-Connect on-premises networks to the virtual network over a private connection on the public internet. Choose from two VPN gateway types:

    * [Point-to-site](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal): Each client computer uses a VPN client to connect to the virtual network.
    * [Site-to-site](/azure/vpn-gateway/tutorial-site-to-site-portal): A VPN device connects the virtual network to your on-premises network.

* [ExpressRoute](https://azure.microsoft.com/services/expressroute/)-Connect on-premises networks to Azure over a private connection through a connectivity provider.
* [Azure Bastion](/azure/bastion/bastion-overview)-Create an Azure virtual machine (a jump box) in the virtual network, then connect to it through Azure Bastion using RDP or SSH from your browser. Use the VM as your development environment. Because it's in the virtual network, it can access the workspace directly.

## Create a Foundry project that uses a private endpoint

When creating a new project, use the following steps to create the project.

1. From the [Azure portal](https://portal.azure.com), search for __Azure AI Foundry__ and select __Create a resource__.
1. After configuring the __Basics__ tab, select the __Networking__ tab and then the __Disabled__ option.
1. From the __Private endpoint__ section, select __+ Add private endpoint__.
1. When going through the forms to create a private endpoint, be sure to:

    - From __Basics__, select the same __Region__ as your virtual network.
    - From the __Virtual Network__ form, select the virtual network and subnet that you want to connect to.

    > [!NOTE]
    > In the portal UI, the target to which you create the private endpoint may be labeled as an "account" or "resource". Select your Azure AI Foundry project resource when prompted.

1. Continue through the forms to create the project. When you reach the __Review + create__ tab, review your settings and select __Create__ to create the project.

## Add a private endpoint to a project

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select __Resource Management__, __Networking__, and then select the __Private endpoint connections__ tab. Select __+ Private endpoint__.
1. When going through the forms to create a private endpoint, be sure to:

    - From __Basics__, select the same __Region__ as your virtual network.
    - From the __Virtual Network__ form, select the virtual network and subnet that you want to connect to.

    > [!NOTE]
    > The portal refers to the PE target as an "account" or "resource". Choose your Azure AI Foundry project resource as the target.

1. After populating the forms with any other network configurations you require, use the __Review + create__ tab to review your settings and select __Create__ to create the private endpoint.

## Remove a private endpoint from a project

You can remove one or all private endpoints for a project. Removing a private endpoint removes the project from the Azure Virtual Network that the endpoint was associated with. Removing the private endpoint might prevent the project from accessing resources in that virtual network, or resources in the virtual network from accessing the workspace. For example, if the virtual network doesn't allow access to or from the public internet.

> [!WARNING]
> Removing the private endpoints for a project __doesn't make it publicly accessible__. To make the project publicly accessible, use the steps in the [Enable public access](#enable-public-access) section.

To remove a private endpoint, use the following information:

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select __Resource Management__, __Networking__, and then select the __Private endpoint connections__ tab.
1. Select the endpoint to remove and then select __Remove__.

## Enable public access

In some situations, you might want to allow someone to connect to your secured project over a public endpoint, instead of through the virtual network. Or you might want to remove the project from the virtual network and re-enable public access.

> [!IMPORTANT]
> Enabling public access doesn't remove any private endpoints that exist. All communications between components behind the virtual network that the private endpoint(s) connect to are still secured. It enables public access only to the project, in addition to the private access through any private endpoints.

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select __Resource Management__, __Networking__, and then select the __Firewalls and virtual networks__ tab.
1. Select __All networks__, and then select __Save__.

    :::image type="content" source="../media/how-to/network/foundry-portal-firewall.png" alt-text="Screenshot of the firewalls and virtual networks tab with the all networks option selected.":::

## End-to-end secured networking for Agent Service

When creating a Foundry resource and [!INCLUDE [fdp-projects](../includes/fdp-project-name.md)] to build Agents, we recommend the following network architecture for the most secure end-to-end configuration:

:::image type="content" source="../media/how-to/network/network-diagram-agents.png" alt-text="Diagram of the recommended network isolation for AI Foundry projects and agents." lightbox="../media/how-to/network/network-diagram-agents.png":::

1. Set the public network access (PNA) flag of each of your resources to `Disabled`. Disabling public network access locks down inbound access from the public internet to the resources.

   > [!NOTE]
   > When the Foundry resources' public network access (PNA) flag is set to Disabled, actions such as deploying a model is possible for the user from their local machine. Only data actions such as building an Agent or creating a new evaluation is not possible for the user, unless they are securely accessing their Foundry resource using a VPN, VM, or ExpressRoute from their local machine.

1. Create a private endpoint for each of your Azure resources that are required for a Standard Agent:

    - Azure Storage Account
    - Azure AI Search resource
    - Cosmos DB resource
    - Azure AI Foundry resource

1. To access your resources, we recommend using a Bastion VM, ExpressRoute, or VPN connection to your Azure Virtual Network. These options allow you to connect to the isolated network environment.

## Network injection for Agent Service

Network-secured Standard Agents support full network isolation and data exfiltration protection through network injection of the Agent client. To do this, the Agent client is network injected into your Azure virtual network, allowing for strict control over data movement and preventing data exfiltration by keeping traffic within your defined network boundaries. Network injection is supported only for Standard Agent deployment, not Light Agent deployment.

Additionally, a network-secured Standard Agent is only supported through BICEP template deployment, and not through UX, CLI, or SDK. After the Foundry resource and Agent are deployed through the template, you can't update the delegated subnet for the Agent Service. This is visible in the Foundry resource Networking tab, where you can view and copy the subnet, but can't update or remove the subnet delegation. To update the delegated subnet, you must redeploy the network-secured Standard Agent template. 

:::image type="content" source="../media/how-to/network/network-injection.png" alt-text="Diagram of the network injection for Azure AI Foundry projects and agents." lightbox="../media/how-to/network/network-injection.png":::

For more information on secured networking for the Agent Service, see [How to use a virtual network with the Azure AI Agent Service](/azure/ai-services/agents/how-to/virtual-networks) article.

## DNS configuration

Clients on a virtual network that use the private endpoint use the same connection string for the Azure AI Foundry resource and projects as clients connecting to the public endpoint. DNS resolution automatically routes the connections from the virtual network to the Azure AI Foundry resource and projects over a private link.

### Apply DNS changes for private endpoints

When you create a private endpoint, the DNS CNAME resource record for the Azure AI Foundry resource is updated to an alias in a subdomain with the prefix `privatelink`. By default, Azure also creates a private DNS zone that corresponds to the `privatelink` subdomain, with the DNS A resource records for the private endpoints. For more information, see [what is Azure Private DNS](/azure/dns/private-dns-overview).

When you resolve the endpoint URL from outside the virtual network with the private endpoint, it resolves to the public endpoint of the Azure AI Foundry resource. When it's resolved from the virtual network hosting the private endpoint, it resolves to the private IP address of the private endpoint.

This approach enables access to the Azure AI Foundry resource using the same connection string for clients in the virtual network that hosts the private endpoints, and clients outside the virtual network.

If you use a custom DNS server on your network, clients must be able to resolve the fully qualified domain name (FQDN) for the Azure AI services resource endpoint to the private endpoint IP address. Configure your DNS server to delegate your private link subdomain to the private DNS zone for the virtual network.

> [!TIP]
> When you use a custom or on-premises DNS server, you should configure your DNS server to resolve the Azure AI services resource name in the `privatelink` subdomain to the private endpoint IP address. Delegate the `privatelink` subdomain to the private DNS zone of the virtual network. Alternatively, configure the DNS zone of your DNS server and add the DNS A records.
>
> For more information on configuring your own DNS server to support private endpoints, use the following articles:
> - [Name resolution that uses your own DNS server](/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances#name-resolution-that-uses-your-own-dns-server)
> - [DNS configuration](/azure/private-link/private-endpoint-overview#dns-configuration)

## Grant access to trusted Azure services

You can grant a subset of trusted Azure services access to Azure OpenAI, while maintaining network rules for other apps. These trusted services then use managed identity to authenticate your Azure OpenAI resources. The following table lists the services that can access Azure OpenAI if the managed identity of those services has the appropriate role assignment:

| Service | Resource provider name |
| ----- | ----- |
| Azure AI Search | `Microsoft.Search` |

You can grant networking access to trusted Azure services by creating a network rule exception using the REST API or Azure portal.

## Limitations
 
- A network-secured Agent (bring your own virtual network) is only supported through Bicep template deployment. For more information on network-secured Agent deployment, see [How to use a virtual network with the Azure AI Agent Service](/azure/ai-services/agents/how-to/virtual-networks). 
- A network-secured Agent to be deployed is only a Standard Agent, not a Light Agent. 
- There's no managed virtual network support for the Agent Service or [!INCLUDE [FDP](../includes/fdp-project-name.md)].
- Evaluations in AI Foundry are currently not supported with virtual network injection for egress. 

## Next steps

- [Create an Azure AI Foundry project](create-projects.md)
- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)
- [Troubleshoot secure connectivity to a project](troubleshoot-secure-connection-project.md)
