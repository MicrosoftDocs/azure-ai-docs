---
title: Troubleshoot private endpoint connection
titleSuffix: Microsoft Foundry
description: 'Learn how to troubleshoot connectivity problems to a project that is configured with a private endpoint.'
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - hub-only
  - dev-focus
ms.topic: how-to
#CustomerIntent: As a developer, I want to diagnose private endpoint connection issues so that I can securely access my Foundry project.
ms.date: 02/02/2026
ms.reviewer: meerakurup
ms.author: jburchel 
author: jonburchel 
ai-usage: ai-assisted
---

# Troubleshoot connection to a project with a private endpoint

[!INCLUDE [hub-only-alt](../includes/uses-hub-only-alt.md)]

When you create a project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs), you can secure it by using a private endpoint to connect over a private network. If you see an HTTP 403 error or "access forbidden" message when connecting to a project with a private endpoint, use this article to diagnose and fix common configuration problems.

## Prerequisites

- **Azure role-based access control (RBAC)**: You need appropriate RBAC roles to troubleshoot and resolve private endpoint problems:
  - **Reader** role at the subscription level to view Azure Search services and verify DNS configuration
  - **Network Contributor** role on the resource group or virtual network if you need to create or modify private endpoints
  - **Storage Blob Data Reader** or **Storage Blob Data Contributor** role for the storage account associated with your hub (depending on whether you need read-only or read-write access)
  - **Storage File Data Privileged Reader** or **Storage File Data Privileged Contributor** role for the storage account
  
  For more information, see [Azure built-in roles](/azure/role-based-access-control/built-in-roles).
- **Network access**: Connection to the virtual network via Azure VPN Gateway, ExpressRoute, or Azure Bastion

## Verify your private endpoint connectivity

Before you dive into specific troubleshooting sections, run a quick connectivity test from a machine connected to your virtual network:

```powershell
# Replace with your Foundry hub's FQDN from the private endpoint DNS configuration
$fqdn = "<your-workspace-id>.workspace.<region>.api.azureml.ms"

# Test DNS resolution
nslookup $fqdn

# Test network connectivity to the resolved IP (expected: private IP like 10.x.x.x)
Test-NetConnection -ComputerName $fqdn -Port 443
```

**Expected success output**:
- `nslookup` returns a private IP address (for example, `10.0.0.4`)
- `Test-NetConnection` shows `TcpTestSucceeded: True`

**Signs of a problem**:
- `nslookup` returns a public IP address or fails with "Non-existent domain"
- `Test-NetConnection` shows `TcpTestSucceeded: False`

If the test fails, continue with the troubleshooting sections in this article.

Reference: [nslookup command](/windows-server/administration/windows-commands/nslookup) | [Test-NetConnection](/powershell/module/nettcpip/test-netconnection)

## Error loading Foundry hub or project

If you get an error when loading your Foundry hub or project, check these two settings.

- Your hub has public network access set to **Disabled**.
- Your hub has public network access set to **Enable from selected IPs**.

Depending on the public network access setting for your Foundry hub or project, take the matching action:

| Public network access setting | Action |
| ----- | ----- |
| Disabled | Create and approve an inbound private endpoint from your virtual network to your Foundry hub. Connect securely to your hub or project using Azure VPN, ExpressRoute, or Azure Bastion. |
| Enable from selected IPs | Make sure your IP address is listed in the **Firewall IP ranges allowed to access Foundry**. If you can't add your IP address, contact your IT admin. |

## Securely connect to your hub or project

To connect to a hub or project secured by a virtual network, use one of these methods:

* [Azure VPN Gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways)-Connect on-premises networks to the virtual network over a private connection on the public internet. Choose from two VPN gateway types:

    * [Point-to-site](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal): Each client computer uses a VPN client to connect to the virtual network.
    * [Site-to-site](/azure/vpn-gateway/tutorial-site-to-site-portal): A VPN device connects the virtual network to your on-premises network.

* [ExpressRoute](https://azure.microsoft.com/services/expressroute/)-Connect on-premises networks to Azure over a private connection through a connectivity provider.
* [Azure Bastion](/azure/bastion/bastion-overview)-Create an Azure virtual machine (a jump box) in the virtual network, then connect to it through Azure Bastion using RDP or SSH from your browser. Use the VM as your development environment. Because it's in the virtual network, it can access the workspace directly.

## DNS configuration

Proper DNS configuration is essential for resolving private endpoint addresses. The following steps help you identify whether your virtual network uses Azure DNS or a custom DNS solution, then guide you through the appropriate troubleshooting process.

Troubleshooting steps differ based on whether you use Azure DNS or a custom DNS. Follow these steps to see which one you're using:

1. In the [Azure portal](https://portal.azure.com), select the private endpoint resource for your Foundry. If you don't remember the name, select your Foundry resource, **Networking**, **Private endpoint connections**, and then select the **Private endpoint** link.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-connections.png" alt-text="Screenshot of the private endpoint connections for the resource." lightbox="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-connections.png":::

1. From the **Overview** page, select the **Network Interface** link.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-overview.png" alt-text="Screenshot of the private endpoint overview with network interface link highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-overview.png":::

1. Under **Settings**, select **IP Configurations** and then select the **Virtual network** link.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/network-interface-ip-configurations.png" alt-text="Screenshot of the IP configuration with virtual network link highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/network-interface-ip-configurations.png":::

1. In **Settings**, select **DNS servers**.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/dns-servers.png" alt-text="Screenshot of the DNS servers configuration." lightbox="../media/how-to/troubleshoot-secure-connection-project/dns-servers.png":::

    * If this value is **Default (Azure-provided)**, then the virtual network is using Azure DNS. Go to the [Azure DNS troubleshooting](#azure-dns-troubleshooting) section.
    * If there's a different IP address listed, then the virtual network is using a custom DNS solution. Go to the [Custom DNS troubleshooting](#custom-dns-troubleshooting) section.

### Custom DNS troubleshooting

Follow these steps to check whether your custom DNS solution resolves names to IP addresses:

1. On a VM, laptop, desktop, or other compute resource that connects to the private endpoint, open a web browser. In the browser, go to the URL for your Azure region:

    | Azure region | URL |
    | ----- | ----- |
    | Azure Government | https://portal.azure.us/?feature.privateendpointmanageddns=false |
    | Microsoft Azure operated by 21Vianet | https://portal.azure.cn/?feature.privateendpointmanageddns=false |
    | All other regions | https://portal.azure.com/?feature.privateendpointmanageddns=false |

1. In the portal, select the private endpoint for the project. From the __DNS configuration__ section, list the FQDNs for the private endpoint.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/custom-dns-settings.png" alt-text="Screenshot of the private endpoint with custom DNS settings highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/custom-dns-settings.png":::

1. Open a command prompt, PowerShell, or other command line and run the following command for each FQDN returned from the previous step. Each time you run the command, verify that the IP address returned matches the IP address listed in the portal for the FQDN: 

   In the following command, replace the placeholder text *`<fqdn>`* with an FQDN from your list.

   `nslookup <fqdn>`

   For example:

   ```powershell
   nslookup df33e049-7c88-4953-8939-aae374adbef9.workspace.eastus2.api.azureml.ms
   ```

   **Expected success output** (private IP returned):

   ```text
   Server: yourdnsserver
   Address: yourdnsserver-IP-address
  
   Name:   df33e049-7c88-4953-8939-aae374adbef9.workspace.eastus2.api.azureml.ms
   Address: 10.0.0.4
   ```

   **Signs of a problem**:
   - A public IP address is returned instead of a private IP (like `10.x.x.x` or `172.16.x.x`)
   - Error message: "Non-existent domain" or "Server failed"

1. If the `nslookup` command returns an error or a different IP address than the portal shows, your custom DNS solution isn't configured correctly.

   For more information, see [nslookup command](/windows-server/administration/windows-commands/nslookup)

### Azure DNS troubleshooting

When you use Azure DNS for name resolution, follow these steps to check that Private DNS integration is configured correctly:

1. On the private endpoint, select **DNS configuration**.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/dns-zone-group.png" alt-text="Screenshot of the DNS configuration with Private DNS zone and group highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/dns-zone-group.png":::

    * If there's a Private DNS zone entry, but **no DNS zone group entry**, delete and recreate the private endpoint. When recreating the private endpoint, **enable Private DNS zone integration**.
    * If **DNS zone group** isn't empty, select the link for the **Private DNS zone** entry.
    
        From the Private DNS zone, select **Virtual network links**. There should be a link to the virtual network. If there isn't one, then delete and recreate the private endpoint. When recreating it, select a Private DNS zone linked to the virtual network, or create a new one and link it.

        :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/virtual-network-links.png" alt-text="Screenshot of the virtual network links for the Private DNS zone." lightbox="../media/how-to/troubleshoot-secure-connection-project/virtual-network-links.png":::

1. Repeat the previous steps for the rest of the Private DNS zone entries.

## Browser configuration (DNS over HTTPS)

Browser DNS settings can interfere with private endpoint resolution. If you enable DNS over HTTPS, your browser bypasses the network DNS configuration and might fail to resolve private endpoint addresses.

Check if DNS over HTTPS is enabled in your web browser. DNS over HTTPS can prevent Azure DNS from responding with the IP address of the private endpoint.

* Mozilla Firefox: More about [Disable DNS over HTTPS in Firefox](https://support.mozilla.org/en-US/kb/firefox-dns-over-https).
* Microsoft Edge:
    1. In Microsoft Edge, select **...** and then select **Settings**.
    1. In **Settings**, search for *DNS* and then disable **Use secure DNS to specify how to look up the network address for websites**.
    
        :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/disable-dns-over-http.png" alt-text="Screenshot of the Use secure DNS setting in Microsoft Edge." lightbox="../media/how-to/troubleshoot-secure-connection-project/disable-dns-over-http.png":::

## Proxy configuration

Proxy servers can interfere with private endpoint connectivity by blocking or modifying network traffic. The following options help you determine if proxy settings are causing connection problems.

If you're using a proxy, it might block access to a secured project. To test, try one of these options:

* Temporarily disable the proxy setting, then try to connect.
* Create a [Proxy auto-config (PAC)](https://wikipedia.org/wiki/Proxy_auto-config) file that allows direct access to the fully qualified domain names (FQDNs) listed on the private endpoint, and to the FQDN for any compute instances.
* Set up your proxy server to forward DNS requests to Azure DNS.
* Make sure the proxy lets connections to Azure Machine Learning (AML) APIs, such as `*.<region>.api.azureml.ms` and `*.instances.azureml.ms`.

## Troubleshoot storage connection problems

Storage connectivity is critical for Foundry projects. When you disable public network access on the storage account, you need proper private endpoint configuration and managed identity permissions.

When you create a project, Azure Storage creates several connections for data upload and artifact storage, including prompt flow. If you set the public network access on your hub's associated Azure Storage account to **Disabled**, these storage connections can take longer to create. 

Try these steps to troubleshoot:
1. In the Azure portal, check the network settings of the storage account that's associated with your hub.
   * If you set public network access to __Enabled from selected virtual networks and IP addresses__, make sure you add the correct IP address ranges to allow access to your storage account.
   * If you set public network access to __Disabled__, make sure you configure a private endpoint from your Azure virtual network to your storage account with Target sub-resource set to blob. Also, grant the [Reader](/azure/role-based-access-control/built-in-roles#reader) role for the storage account private endpoint to the managed identity.
1. In the Azure portal, go to your Foundry hub. Make sure the managed virtual network is provisioned and the outbound private endpoint to blob storage is Active. For more information, see [How to configure a managed network for Foundry hubs](configure-managed-network.md).
1. Go to Foundry > your project > project settings.
1. Refresh the page. Several connections appear, including `workspaceblobstore`.
