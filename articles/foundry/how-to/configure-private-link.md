---

title: "How to configure network isolation for Microsoft Foundry"
description: "Learn how to configure a network isolation end-to-end for Microsoft Foundry. A private link is used to secure communication with the Microsoft Foundry."
manager: mcleans
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023, devx-track-azurecli, build-2024, ignite-2024, dev-focus
  - classic-and-new
ms.topic: how-to
ms.date: 03/12/2026
ms.reviewer: meerakurup
ms.author: jburchel 
author: jonburchel 
ai-usage: ai-assisted
# Customer intent: As an admin, I want to configure a private link for hub so that I can secure Foundry. 
---

# How to configure network isolation for Microsoft Foundry

> [!TIP]
> An alternate hub-focused version of this article is available: [How to configure a private link for a Microsoft Foundry hub](../../foundry-classic/how-to/hub-configure-private-link.md).

When you use a [!INCLUDE [fdp-projects](../includes/fdp-project-name.md)], you can use a private endpoint to secure communication. This article describes how to establish a private connection to your Foundry account and projects using a private endpoint.

## Plan for network isolation in Foundry

### What is network isolation? 

Network isolation is a security strategy that involves dividing a network into separate segments or subnets, each functioning as its own small network. This approach helps to improve security and performance within a larger network structure. Major enterprises require network isolation to secure their resources from unauthorized access, tampering, or leakage of data and models. They also need to adhere to the regulations and standards that apply to their industry and domain.

### Consider network isolation in three areas within Microsoft Foundry

Consider network isolation in the following three areas within Microsoft Foundry:

* **Inbound access** to the Microsoft Foundry resource. For example, for your data scientists to securely access the resource.
* **Outbound access** from the Microsoft Foundry resource. For example, to access other Azure services.
* **Outbound access** from the Microsoft Foundry Agent client to reach required dependencies—such as private data sources, Azure PaaS services, or approved internet endpoints—while keeping all traffic within customer‑defined network boundaries through virtual network injection. 

The following diagram breaks down the inbound and outbound communication.

<!-- :::image type="content" source="../media/how-to/network/plan-network-isolation-diagram.png" alt-text="Diagram of the plan for network isolation in Foundry." lightbox="../media/how-to/network/plan-network-isolation-diagram.png"::: -->

### Inbound access

Set inbound access to a secured Microsoft Foundry project by using the public network access (PNA) flag. The PNA flag setting determines whether your project requires a private endpoint for access. An additional setting between public and private is **Enabled from selected IP addresses**. This setting allows access to your project from the IP addresses you specify. 

### Outbound access

Microsoft Foundry's network isolation spans both Platform as a Service (PaaS) and platform-managed infrastructure components. PaaS resources—such as the Microsoft Foundry project, storage, Key Vault, container registry, and monitoring—are isolated using Private Link. Rather than customers managing IaaS compute resources for training or online endpoints, Foundry uses virtual network (VNet) injection of the Agent client. The Agent client is injected into a customer-managed virtual network subnet, allowing outbound communication to Azure PaaS resources over private endpoints and Private Link while keeping all traffic within customer-defined network boundaries.

In the Agent Service private networking model, customers don't manage separate "compute" resources in Foundry. Instead, the Agent client operates within the delegated Agent subnet and the platform provides container injection to integrate with the customer VNet.

## Prerequisites

Before getting started, ensure you have the following prerequisites set-up.

- An existing Azure virtual network.
- Azure permissions to create and approve private endpoint connections:
    - On the virtual network: **Network Contributor** (or equivalent) to create the private endpoint.
    - On the Foundry project resource: **Contributor** (or **Owner**) to create private endpoint connections. If you don't have approval permissions, the private endpoint connection stays in a **Pending** state until the resource owner approves it.
    - If you manage private DNS zones: **Private DNS Zone Contributor** (or equivalent) for the private DNS zone that you link to the virtual network.

## Setup walkthrough for inbound network isolation

This section guides you through creating a new Foundry resource with inbound network isolation enabled. The public network access can be set to **Disabled** with a private endpoint (private link) enabled, or set to **Selected networks** to grant specific IP addresses and virtual networks the ability to access Foundry securely. 

### Create a new resource and project with private endpoint

When creating a new Foundry resource, follow these steps:

1. From the [Azure portal](https://portal.azure.com), search for **Foundry** and select **Create a resource**.
1. After configuring the **Basics** tab, select the **Networking** tab and then select the **Disabled** option for public access.
1. From the **Private endpoint** section, select **+ Add private endpoint**.
1. When you go through the forms to create a private endpoint, be sure to:

    - From **Basics**, select the same **Region** as your virtual network.
    - From the **Virtual Network** form, select the virtual network and subnet that you want to connect to.
> [!NOTE]
> In the portal UI, the target to which you create the private endpoint should be labeled as an "account". Select your Foundry resource when prompted.

1. Continue through the forms to create the project. When you reach the **Review + create** tab, review your settings and select **Create** to create the project.

### Add a private endpoint to an existing project

If you have an existing Foundry project and want to add network isolation:

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select **Resource Management**, **Networking**, and then select the **Private endpoint connections** tab. Select **+ Private endpoint**.
1. When you go through the forms to create a private endpoint, be sure to:

    - From **Basics**, select the same **Region** as your virtual network.
    - From the **Virtual Network** form, select the virtual network and subnet that you want to connect to.

1. After you populate the forms with any other network configurations you require, use the **Review + create** tab to review your settings and select **Create** to create the private endpoint.

> [!TIP]
> After creating the private endpoint, proceed to the [DNS configuration](#dns-configuration) section to ensure proper name resolution.

### DNS configuration

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

### Validate the configuration

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

References: [Test-NetConnection](/powershell/module/nettcpip/test-netconnection)

### Manage private endpoints

After creating a network-isolated Foundry project, you might need to modify the network configuration. This section covers common management tasks.

### Remove a private endpoint

You can remove one or all private endpoints for a project. Removing a private endpoint removes the project from the Azure Virtual Network that the endpoint was associated with. Removing the private endpoint might prevent the project from accessing resources in that virtual network, or resources in the virtual network from accessing the workspace. For example, if the virtual network doesn't allow access to or from the public internet.

> [!WARNING]
> Removing the private endpoints for a project **doesn't make it publicly accessible**. To make the project publicly accessible, use the steps in the [Enable public access](#enable-public-access) section.

To remove a private endpoint, use the following steps:

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select **Resource Management**, **Networking**, and then select the **Private endpoint connections** tab.
1. Select the endpoint to remove and then select **Remove**.

### Enable public access

In some situations, you might want to allow someone to connect to your secured project over a public endpoint, instead of through the virtual network. Or you might want to remove the project from the virtual network and re-enable public access.

> [!IMPORTANT]
> Enabling public access doesn't remove any private endpoints that exist. All communications between components behind the virtual network that the private endpoints connect to are still secured. It enables public access only to the project, in addition to the private access through any private endpoints.

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select **Resource Management**, **Networking**, and then select the **Firewalls and virtual networks** tab.
1. Select **All networks**, and then select **Save**.

    :::image type="content" source="../media/how-to/network/foundry-portal-firewall.png" alt-text="Screenshot of the firewalls and virtual networks tab with the all networks option selected.":::

### Grant access to trusted Azure services

If your Foundry project restricts network access, grant a subset of trusted Azure services access to Foundry while maintaining network rules for other apps. These trusted services then use managed identity to authenticate. The following table lists the services that can access Foundry if the managed identity of those services has the appropriate role assignment:

| Service | Resource provider name |
| ----- | ----- |
| Foundry Tools | `Microsoft.CognitiveServices` |
| Azure AI Search | `Microsoft.Search` |
| Azure Machine Learning | `Microsoft.MachineLearningServices` |

Grant networking access to trusted Azure services by creating a network rule exception using the REST API or Azure portal.

### Choose a secure connection method to Foundry

To access your Foundry resource that has public network access disabled and is behind a virtual network with a private endpoint, use one of these methods:

* [Azure Virtual Network Gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways) - Connect on-premises networks to the virtual network over a private connection on the public internet. Choose from two VPN gateway types:

    * [Point-to-site](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal): Each client computer uses a VPN client to connect to the virtual network.
    * [Site-to-site](/azure/vpn-gateway/tutorial-site-to-site-portal): A VPN device connects the virtual network to your on-premises network.

* [ExpressRoute](/azure/expressroute/) - Connect on-premises networks to Azure over a private connection through a connectivity provider.
* [Azure Bastion VM](/azure/bastion/bastion-overview) - Create an Azure virtual machine (a jump box) in the virtual network, then connect to it through Azure Bastion using RDP or SSH from your browser. Use the VM as your development environment. Because it's in the virtual network, it can access the resource directly.


## Setup walkthrough for outbound network isolation

This section guides you through creating a new Foundry resource with outbound network isolation enabled. You can choose the best approach to secure outbound access for your Agent and evaluations client: virtual network injection through your own virtual network (BYO VNet) or managed virtual network (preview). For more information on managed networks, see the managed network documentation. This section describes network isolation with a custom (BYO) virtual network. 

### Deep dive into network injection for Agent Service and evaluations

If you're building agents or running evaluations and you want end-to-end network isolation, see [How to use a virtual network with the Azure AI Agent Service](/azure/ai-services/agents/how-to/virtual-networks). That article provides details on required DNS zones, reference architecture, and known limitations.

<!-- :::image type="content" source="../media/how-to/network/agent-eval-network-diagram.png" alt-text="Diagram of the recommended network isolation for Foundry." lightbox="../media/how-to/network/agent-eval-network-diagram.png"::: -->

### Create a new resource and project with virtual network injection

You can create a Foundry resource with virtual network injection using your custom virtual network (BYO VNet) from the Azure portal. Alternatively, you can create a Foundry resource with virtual network injection from a Bicep or Terraform template. 

When creating a new Foundry resource, follow these steps:

1. From the [Azure portal](https://portal.azure.com), search for **Foundry** and select **Create a resource**.
1. After configuring the **Basics** tab, select the **Storage** tab and then select **Select resources** under **Agent service**.
    - Select or create new Storage account, AI Search resource, and Azure Cosmos DB. If you're setting up Foundry with virtual network injection, you must also bring your own Storage, AI Search, and Azure Cosmos DB resources, creating a Standard Agent with end-to-end virtual network isolation.
1. After configuring the **Storage** tab, select the **Network** tab and then select the **Disabled** option for public access. Add your private endpoint using the instructions from the [inbound network isolation section](#setup-walkthrough-for-inbound-network-isolation).
1. After setting your inbound private endpoint, a new dropdown appears for setting **Virtual network injection**. Select your **virtual network** in the first dropdown, then select your **subnet** that is delegated to **Microsoft.App/environments** with a subnet size of /27 or larger. This delegation and subnet size are required for the injection.
1. Continue through the forms to create the project. When you reach the **Review + create** tab, review your settings and select **Create** to create the project.


### Agent tools with network isolation

#### Tool support and traffic flow

Certain Agent tools are supported when Foundry is network isolated, while others are not. The following table shows support status for agent tools in network-isolated environments and how traffic flows. This covers tool support behind a VNet for the new Responses API Agents created through SDK/CLI or in the new Foundry portal only. 

| Tool | Support Status | Traffic Flow |
|------|---------------|--------------|
| MCP Tool (Private MCP) | ✅ Supported | Through your VNet subnet |
| Azure AI Search | ✅ Supported | Through private endpoint |
| Code Interpreter | ✅ Supported | Microsoft backbone network |
| Function Calling | ✅ Supported | Microsoft backbone network |
| Bing Grounding | ✅ Supported | Public endpoint |
| Websearch | ✅ Supported | Public endpoint |
| SharePoint Grounding | ✅ Supported | Public endpoint |
| Foundry IQ (preview) | ✅ Supported | Via MCP |
| Fabric Data Agent | ❌ Not supported |  |
| Logic Apps | ❌ Not supported | |
| File Search | ❌ Not supported | Under development |
| OpenAPI tool | ❌ Not supported | Under development |
| Azure Functions | ❌ Not supported | Under investigation |
| Browser Automation | ❌ Not supported | Under investigation |
| Computer Use | ❌ Not supported | Under investigation |
| Image Generation | ❌ Not supported | Under investigation |
| Agent-to-Agent (A2A) | ❌ Not supported | Under development |

> [!NOTE]
> **Public endpoint tools** (Bing Grounding, Websearch, SharePoint Grounding) work in network-isolated environments but communicate over the public internet. These tools don't require private endpoints or VNet configuration. If your organization requires that all traffic remain within a private network, these tools may not meet your compliance requirements.

#### Configuration requirements by traffic pattern

**Tools using your virtual network subnet** (MCP Tool, Azure AI Search):

For more information on private MCP support and setup, see [19-hybrid-private-resources-agent-setup](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/19-hybrid-private-resources-agent-setup).

**Tools using Microsoft backbone network** (Code Interpreter, Function Calling):

No private endpoints are required and no additional networking configuration is necessary to use these tools. Your traffic stays within Microsoft's backbone network infrastructure, ensuring security.

**Tools using public endpoints** (Bing, Websearch, SharePoint):

No private endpoints are required and no additional networking configuration is necessary to use these tools. However, these tools communicate over public endpoints. If you don't want users in your enterprise to use these tools due to their public endpoint nature, you can block them using Azure policies. 

### Hub-and-spoke and firewall network configuration

To secure egress (outbound) traffic through network injection, configure an Azure Firewall or another firewall solution. This configuration helps inspect and control outbound traffic before it leaves your virtual network.

Additionally, you can use a hub-and-spoke networking architecture where a virtual network is created for a shared firewall (the hub) and a separate virtual network for Foundry networking (a spoke). These virtual networks are then peered together. 

<!-- :::image type="content" source="../media/how-to/network/network-hub-spoke-diagram.png" alt-text="Diagram of the firewall configuration for egress traffic from Foundry projects and agents." lightbox="../media/how-to/network/network-hub-spoke-diagram.png"::: -->

## Limitations and considerations

Understand these limitations before implementing network isolation for Foundry. This section consolidates all known constraints across private endpoints, portal experiences, Agent Service, and tools. 

### Foundry feature limitations

The following features in Foundry don't yet support network isolation.

| Feature | Network Isolation Status | Notes |
|---------|--------------------------|-------|
| Hosted Agents | Not supported | Hosted Agents don't have virtual network support yet. |
| Publish Agent to Teams/M365 | Not supported | Requires public endpoints for Teams/M365 integration. |
| Synthetic Data Gen for Evaluations | Not supported | Bring your own data to run evaluations. |
| Traces | Not supported | Traces don't have virtual network support with a private Application Insights yet. |
| Workflow Agents | Partially supported | Inbound access is supported in the UI, SDK, and CLI. Outbound with virtual network injection isn't currently supported for Workflow Agents. |
| AI Gateway | Partially supported | You can create a new AI Gateway with your private Foundry resource. This gateway is automatically public. To complete any data plane actions with a private Foundry, your AI Gateway must also have network isolation configured. For more information, see [Networking for AI Gateway](/azure/api-management/virtual-network-concepts). |
| Certain Agent Tools | Partially supported | See [Agent tools with network isolation](#agent-tools-with-network-isolation) for detailed tool-by-tool support status. |

For more Agent Service network isolation limitations, see [How to use a virtual network with the Azure AI Agent Service](/azure/ai-services/agents/how-to/virtual-networks).

### Private endpoint limitations

- **Region and subscription**: You must deploy the private endpoint in the same region and subscription as the virtual network.
- **Connection state**: Only private endpoints in an **Approved** state can send traffic to a private-link resource.
- **IP address range**: Don't use the 172.17.0.0/16 IP address range for your virtual network. This range is reserved by Docker bridge networking.
- **Approvals**: If you don't have **Contributor** or **Owner** permissions on the Foundry resource, private endpoint connections remain in **Pending** state until approved.

## Troubleshoot private endpoint issues

If you experience connectivity problems after setting up a private endpoint, try these steps:

### Private endpoint issues

- **Private endpoint stuck in Pending state**: Verify that you have **Contributor** or **Owner** permissions on the Foundry project resource. If you don't, ask the resource owner to approve the connection from the **Networking** > **Private endpoint connections** tab.
- **Private endpoint creation fails**: Ensure you have **Network Contributor** role on the VNET and subnet where you're creating the endpoint. Check that the subnet isn't full (IP addresses available).

### DNS resolution problems

- **DNS resolution returns a public IP address**: Confirm that a private DNS zone exists for the `privatelink` subdomain and is linked to your virtual network. Run `nslookup <your-foundry-endpoint-hostname>` from inside the virtual network to verify it resolves to the private IP.
- **Custom DNS server not resolving**: If you use a custom DNS server, ensure it forwards queries for the `privatelink` subdomain to Azure DNS (168.63.129.16). See [DNS configuration](#dns-configuration) for details.
- **Intermittent DNS failures**: Check that your DNS server (custom or Azure-provided) is reachable from all subnets. Verify DNS server settings on VNET and individual NICs.

### Connectivity issues

- **Connection times out on port 443**: Check that your network security group (NSG) rules allow outbound traffic to the private endpoint IP on port 443. Also verify that no firewall is blocking the connection.
- **Can't reach Foundry from on-premises**: Verify that your VPN or ExpressRoute connection is active and that routing tables include the VNET address space. Test connectivity to the private IP from on-premises.
- **403 Forbidden errors**: This often indicates authentication issues rather than networking. Verify that your credentials have appropriate RBAC roles on the Foundry project.

### Agent-specific troubleshooting

- **Agent fails to start in network-isolated project**: Verify you're using Standard Agent deployment (not Basic). Check that network injection is properly configured and that the subnet has enough available IP addresses.
- **Agent can't access MCP tools**: Ensure private endpoints exist for all Azure services the MCP tools access. Verify managed identity has appropriate RBAC roles. Check firewall rules permit agent → service traffic.
- **Evaluation runs fail with network errors**: Confirm that all required DNS zones are configured. Verify the evaluation compute can reach both Foundry and model endpoints via private links.
- **Agent timeouts on external API calls**: If agents need to call external (non-Azure) APIs, ensure your firewall allows outbound HTTPS to those destinations, or deploy a NAT gateway for controlled egress.

## Next steps

- [Create a Foundry project](create-projects.md)
- [Learn more about Foundry](../what-is-foundry.md)
