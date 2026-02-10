---

title: How to configure a private link for Microsoft Foundry projects
titleSuffix: Microsoft Foundry
description: Learn how to configure a private link for Microsoft Foundry projects. A private link is used to secure communication with the Microsoft Foundry.
manager: mcleans
ms.service: azure-ai-foundry
ms.custom: ignite-2023, devx-track-azurecli, build-2024, ignite-2024, dev-focus
ms.topic: how-to
ms.date: 01/06/2026
ms.reviewer: meerakurup
ms.author: jburchel 
author: jonburchel 
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
# Customer intent: As an admin, I want to configure a private link for hub so that I can secure my hubs.
---

# How to configure a private link for Microsoft Foundry (Foundry projects)

> [!TIP]
> An alternate hub-focused version of this article is available: [How to configure a private link for a Microsoft Foundry hub](hub-configure-private-link.md).

When you use a [!INCLUDE [fdp-projects](../includes/fdp-project-name.md)], you can use a private link to secure communication with your project. This article describes how to establish a private connection to your project using a private link. 

> [!NOTE]
> End-to-end network isolation isn't supported in the new Foundry portal experience. Use the classic Foundry portal experience or the SDK or CLI to securely access your Foundry projects when network isolation is enabled. For more on limitations with private networking in Foundry, see [limitations](#limitations).


## Prerequisites

- An existing Azure virtual network and subnet to create the private endpoint in.
- Azure permissions to create and approve private endpoint connections:
    - On the virtual network: **Network Contributor** (or equivalent) to create the private endpoint.
    - On the Foundry project resource: **Contributor** (or **Owner**) to create private endpoint connections. If you don't have approval permissions, the private endpoint connection stays in a **Pending** state until the resource owner approves it.
    - If you manage private DNS zones: **Private DNS Zone Contributor** (or equivalent) for the private DNS zone that you link to the virtual network.

    > [!IMPORTANT]
    > Don't use the 172.17.0.0/16 IP address range for your virtual network. This range is the default subnet range used by the Docker bridge network on-premises.

## Securely connect to Foundry

To connect to Foundry secured by a virtual network, use one of these methods:

* [Azure VPN Gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways) - Connect on-premises networks to the virtual network over a private connection on the public internet. Choose from two VPN gateway types:

    * [Point-to-site](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal): Each client computer uses a VPN client to connect to the virtual network.
    * [Site-to-site](/azure/vpn-gateway/tutorial-site-to-site-portal): A VPN device connects the virtual network to your on-premises network.

* [ExpressRoute](/azure/expressroute/) - Connect on-premises networks to Azure over a private connection through a connectivity provider.
* [Azure Bastion](/azure/bastion/bastion-overview) - Create an Azure virtual machine (a jump box) in the virtual network, then connect to it through Azure Bastion using RDP or SSH from your browser. Use the VM as your development environment. Because it's in the virtual network, it can access the workspace directly.

## Create a Foundry project 

When creating a new project, use the following steps to create the project.

1. From the [Azure portal](https://portal.azure.com), search for **Foundry** and select **Create a resource**.
1. After configuring the **Basics** tab, select the **Networking** tab and then the **Disabled** option.
1. From the **Private endpoint** section, select **+ Add private endpoint**.
1. When you go through the forms to create a private endpoint, be sure to:

    - From **Basics**, select the same **Region** as your virtual network.
    - From the **Virtual Network** form, select the virtual network and subnet that you want to connect to.

    > [!NOTE]
    > In the portal UI, the target to which you create the private endpoint might be labeled as an "account" or "resource". Select your Foundry project resource when prompted.

1. Continue through the forms to create the project. When you reach the **Review + create** tab, review your settings and select **Create** to create the project.

## Add a private endpoint to a resource

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select **Resource Management**, **Networking**, and then select the **Private endpoint connections** tab. Select **+ Private endpoint**.
1. When you go through the forms to create a private endpoint, be sure to:

    - From **Basics**, select the same **Region** as your virtual network.
    - From the **Virtual Network** form, select the virtual network and subnet that you want to connect to.

    > [!NOTE]
    > The portal refers to the private endpoint target as an "account" or "resource". Choose your Foundry resource as the target.

1. After you populate the forms with any other network configurations you require, use the **Review + create** tab to review your settings and select **Create** to create the private endpoint.

## Remove a private endpoint from a project

You can remove one or all private endpoints for a project. Removing a private endpoint removes the project from the Azure Virtual Network that the endpoint was associated with. Removing the private endpoint might prevent the project from accessing resources in that virtual network, or resources in the virtual network from accessing the workspace. For example, if the virtual network doesn't allow access to or from the public internet.

> [!WARNING]
> Removing the private endpoints for a project **doesn't make it publicly accessible**. To make the project publicly accessible, use the steps in the [Enable public access](#enable-public-access) section.

To remove a private endpoint, use the following information:

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select **Resource Management**, **Networking**, and then select the **Private endpoint connections** tab.
1. Select the endpoint to remove and then select **Remove**.

## Enable public access

In some situations, you might want to allow someone to connect to your secured project over a public endpoint, instead of through the virtual network. Or you might want to remove the project from the virtual network and re-enable public access.

> [!IMPORTANT]
> Enabling public access doesn't remove any private endpoints that exist. All communications between components behind the virtual network that the private endpoints connect to are still secured. It enables public access only to the project, in addition to the private access through any private endpoints.

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select **Resource Management**, **Networking**, and then select the **Firewalls and virtual networks** tab.
1. Select **All networks**, and then select **Save**.

    :::image type="content" source="../media/how-to/network/foundry-portal-firewall.png" alt-text="Screenshot of the firewalls and virtual networks tab with the all networks option selected.":::

## DNS configuration

Clients on a virtual network that use the private endpoint use the same connection string for the Foundry resource and projects as clients connecting to the public endpoint. DNS resolution automatically routes the connections from the virtual network to the Foundry resource and projects over a private link.

### Apply DNS changes for private endpoints

When you create a private endpoint, Azure updates the DNS CNAME resource record for the Foundry resource to an alias in a subdomain with the prefix `privatelink`. By default, Azure also creates a private DNS zone that corresponds to the `privatelink` subdomain, with the DNS A resource records for the private endpoints. For more information, see [what is Azure Private DNS](/azure/dns/private-dns-overview).

When you resolve the endpoint URL from outside the virtual network with the private endpoint, it resolves to the public endpoint of the Foundry resource. When you resolve it from the virtual network hosting the private endpoint, it resolves to the private IP address of the private endpoint.

This approach enables access to the Foundry resource using the same connection string for clients in the virtual network that hosts the private endpoints, and clients outside the virtual network.

If you use a custom DNS server on your network, clients must be able to resolve the fully qualified domain name (FQDN) for the Foundry resource endpoint to the private endpoint IP address. Configure your DNS server to delegate your private link subdomain to the private DNS zone for the virtual network.

> [!TIP]
> When you use a custom or on-premises DNS server, configure your DNS server to resolve the Foundry resource name in the `privatelink` subdomain to the private endpoint IP address. Delegate the `privatelink` subdomain to the private DNS zone of the virtual network. Alternatively, configure the DNS zone of your DNS server and add the DNS A records.
>
> For more information on configuring your own DNS server to support private endpoints, use the following articles:
> - [Name resolution that uses your own DNS server](/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances#name-resolution-that-uses-your-own-dns-server)
> - [DNS configuration](/azure/private-link/private-endpoint-overview#dns-configuration)

## Validate the configuration

Use the following steps to validate that your private endpoint is approved and that DNS resolves to the private IP address from inside your virtual network.

1. In the Azure portal, go to your project resource. Under **Networking** > **Private endpoint connections**, confirm the connection status is **Approved**.
1. From a VM connected to the virtual network (or from an on-premises machine connected through VPN/ExpressRoute), resolve your Foundry endpoint and confirm it resolves to the private IP address of the private endpoint.

    ```cmd
    nslookup <your-foundry-endpoint-hostname>
    ```

1. Test connectivity to the private endpoint IP address on port 443.

    ```powershell
    Test-NetConnection <private-endpoint-ip-address> -Port 443
    ```

### References

* [Test-NetConnection](/powershell/module/nettcpip/test-netconnection)

## Grant access to trusted Azure services

If your Foundry project uses Azure OpenAI and you restrict network access, grant a subset of trusted Azure services access to Azure OpenAI while maintaining network rules for other apps. These trusted services then use managed identity to authenticate to Azure OpenAI. The following table lists the services that can access Azure OpenAI if the managed identity of those services has the appropriate role assignment:

| Service | Resource provider name |
| ----- | ----- |
| Foundry Tools | `Microsoft.CognitiveServices` |
| Azure AI Search | `Microsoft.Search` |
| Azure Machine Learning | `Microsoft.MachineLearningServices` |

Grant networking access to trusted Azure services by creating a network rule exception using the REST API or Azure portal.

## Limitations

- You must deploy the private endpoint in the same region and subscription as the virtual network.
- Only private endpoints in an **Approved** state can send traffic to a private-link resource.
- End-to-end network isolation in Foundry is not support in the new Foundry portal experience. End-to-end network isolation in Foundry is not supported for the new version of the Agent service. Use the classic Foundry portal experience with the current version of Agent service to securely access your Foundry projects when network isolation is enabled.
- When you use a network isolated Foundry, you cannot use private MCP servers deployed in the same virtual network. You can only use publicly accessible MCP servers.
- Hosted Agents in Microsoft Foundry are not supported with end-to-end network isolation. 

For Agent Service network isolation scenarios (including network injection, end-to-end isolation, and limitations), see [How to use a virtual network with the Azure AI Agent Service](/azure/ai-services/agents/how-to/virtual-networks). 

## End-to-end secured networking for Foundry Agent Service and evaluations

If you're building agents or running evaluations and you want end-to-end network isolation, use the guidance in [How to use a virtual network with the Azure AI Agent Service](/azure/ai-services/agents/how-to/virtual-networks). That article includes required DNS zones, a reference architecture, and known limitations.

:::image type="content" source="../media/how-to/network/agent-eval-networking.png" alt-text="Diagram of the recommended network isolation for Foundry." lightbox="../media/how-to/network/agent-eval-networking.png":::

## Network injection for Agent Service and evaluations

Network-secured Standard Agents and evaluations support full network isolation and protect against data exfiltration through network injection. Network injection supports only Standard Agent deployment and evaluations, not Light Agent deployment.

## Firewall configuration for agent and evaluations egress

To secure egress (outbound) traffic through network injection, configure an Azure Firewall or another firewall. This configuration helps inspect and control outbound traffic before it leaves your virtual network.

:::image type="content" source="../media/how-to/network/hub-spoke-network.png" alt-text="Diagram of the hub and spoke network isolation for Foundry projects and agents." lightbox="../media/how-to/network/hub-spoke-network.png":::

## Next steps

- [Create a Foundry project](create-projects.md)
- [Learn more about Foundry](../what-is-foundry.md)
