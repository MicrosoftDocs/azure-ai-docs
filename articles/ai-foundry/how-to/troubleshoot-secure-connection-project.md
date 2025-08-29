---
title: Troubleshoot private endpoint connection
titleSuffix: Azure AI Foundry
description: 'Learn how to troubleshoot connectivity problems to a project that is configured with a private endpoint.'
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - hub-only
ms.topic: how-to
ms.date: 08/27/2025
ms.reviewer: meerakurup
ms.author: jburchel 
author: jonburchel 
ai.usage: ai-assisted
---

# Troubleshoot connection to a project with a private endpoint

[!INCLUDE [hub-only-alt](../includes/uses-hub-only-alt.md)]

When you create a project in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), secure it with a private endpoint. A private endpoint lets you connect to the project over a private network and protects your data and resources. If you're having trouble connecting to a project that uses a private endpoint, this article lists steps to help you fix the issue.

When you connect to an [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) project that's set up with a private endpoint, you might see an HTTP 403 error or a message that says access is forbidden. Use this article to check for common configuration issues that cause this error.

## Error loading Azure AI Foundry hub or project

If you get an error when loading your Azure AI Foundry hub or project, check these two settings.

1. Your hub has public network access set to __Disabled__.
1. Your hub has public network access set to __Enable from selected IPs__.

Depending on the public network access setting for your Azure AI Foundry hub or project, take the matching action:

| Public network access setting | Action |
| ----- | ----- |
| Disabled | Create and approve an inbound private endpoint from your virtual network to your Azure AI Foundry hub. Connect securely to your hub or project using Azure VPN, ExpressRoute, or Azure Bastion. |
| Enable from selected IPs | Make sure your IP address is listed in the **Firewall IP ranges allowed to access Azure AI Foundry**. If you can't add your IP address, contact your IT admin. |

## Securely connect to your hub or project

To connect to a hub or project secured by a virtual network, use one of these methods:

* [Azure VPN Gateway](/azure/vpn-gateway/vpn-gateway-about-vpngateways)-Connect on-premises networks to the virtual network over a private connection on the public internet. Choose from two VPN gateway types:

    * [Point-to-site](/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal): Each client computer uses a VPN client to connect to the virtual network.
    * [Site-to-site](/azure/vpn-gateway/tutorial-site-to-site-portal): A VPN device connects the virtual network to your on-premises network.

* [ExpressRoute](https://azure.microsoft.com/services/expressroute/)-Connect on-premises networks to Azure over a private connection through a connectivity provider.
* [Azure Bastion](/azure/bastion/bastion-overview)-Create an Azure virtual machine (a jump box) in the virtual network, then connect to it through Azure Bastion using RDP or SSH from your browser. Use the VM as your development environment. Because it's in the virtual network, it can access the workspace directly.

## DNS configuration

Troubleshooting steps differ based on whether you use Azure DNS or a custom DNS. Follow these steps to see which one you're using:

1. In the [Azure portal](https://portal.azure.com), select the private endpoint resource for your Azure AI Foundry. If you don't remember the name, select your Azure AI Foundry resource, __Networking__, __Private endpoint connections__, and then select the __Private endpoint__ link.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-connections.png" alt-text="Screenshot of the private endpoint connections for the resource." lightbox="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-connections.png":::

1. From the __Overview__ page, select the __Network Interface__ link.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-overview.png" alt-text="Screenshot of the private endpoint overview with network interface link highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/private-endpoint-overview.png":::

1. Under __Settings__, select __IP Configurations__ and then select the __Virtual network__ link.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/network-interface-ip-configurations.png" alt-text="Screenshot of the IP configuration with virtual network link highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/network-interface-ip-configurations.png":::

1. In __Settings__, select __DNS servers__.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/dns-servers.png" alt-text="Screenshot of the DNS servers configuration." lightbox="../media/how-to/troubleshoot-secure-connection-project/dns-servers.png":::

    * If this value is __Default (Azure-provided)__, then the virtual network is using Azure DNS. Skip to the [Azure DNS troubleshooting](#azure-dns-troubleshooting) section.
    * If there's a different IP address listed, then the virtual network is using a custom DNS solution. Skip to the [Custom DNS troubleshooting](#custom-dns-troubleshooting) section.

### Custom DNS troubleshooting

Follow these steps to check whether your custom DNS solution resolves names to IP addresses:

1. On a VM, laptop, desktop, or other compute resource that connects to the private endpoint, open a web browser. In the browser, go to the URL for your Azure region:

    | Azure region | URL |
    | ----- | ----- |
    | Azure Government | https://portal.azure.us/?feature.privateendpointmanagedns=false |
    | Microsoft Azure operated by 21Vianet | https://portal.azure.cn/?feature.privateendpointmanagedns=false |
    | All other regions | https://portal.azure.com/?feature.privateendpointmanagedns=false |

1. In the portal, select the private endpoint for the project. From the __DNS configuration__ section, list the FQDNs for the private endpoint.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/custom-dns-settings.png" alt-text="Screenshot of the private endpoint with custom DNS settings highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/custom-dns-settings.png":::

1. Open a command prompt, PowerShell, or other command line and run the following command for each FQDN returned from the previous step. Each time you run the command, verify that the IP address returned matches the IP address listed in the portal for the FQDN: 

    In the following command, replace the placeholder text *`<fqdn>`* with an FQDN from your list.

    `nslookup <fqdn>`

For example:

```powershell
nslookup df33e049-7c88-4953-8939-aae374adbef9.workspace.eastus2.api.azureml.ms
```

Example output:

```text
Server: yourdnsserver
Address: yourdnsserver-IP-address

Name:   df33e049-7c88-4953-8939-aae374adbef9.workspace.eastus2.api.azureml.ms
Address: 10.0.0.4
```

1. If the `nslookup` command returns an error or a different IP address than the portal shows, your custom DNS solution isn't configured correctly.

### Azure DNS troubleshooting

When you use Azure DNS for name resolution, follow these steps to check that Private DNS integration is configured correctly:

1. On the private endpoint, select __DNS configuration__.

    :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/dns-zone-group.png" alt-text="Screenshot of the DNS configuration with Private DNS zone and group highlighted." lightbox="../media/how-to/troubleshoot-secure-connection-project/dns-zone-group.png":::

    * If there's a Private DNS zone entry, but __no DNS zone group entry__, delete and recreate the Private Endpoint. When recreating the private endpoint, __enable Private DNS zone integration__.
    * If __DNS zone group__ isn't empty, select the link for the __Private DNS zone__ entry.
    
        From the Private DNS zone, select __Virtual network links__. There should be a link to the virtual network. If there isn't one, then delete and recreate the private endpoint. When recreating it, select a Private DNS zone linked to the virtual network, or create a new one and link it.

        :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/virtual-network-links.png" alt-text="Screenshot of the virtual network links for the Private DNS zone." lightbox="../media/how-to/troubleshoot-secure-connection-project/virtual-network-links.png":::

1. Repeat the previous steps for the rest of the Private DNS zone entries.

## Browser configuration (DNS over HTTPS)

Check if DNS over HTTPS is enabled in your web browser. DNS over HTTPS can prevent Azure DNS from responding with the IP address of the private endpoint.

* Mozilla Firefox: More about [Disable DNS over HTTPS in Firefox](https://support.mozilla.org/en-US/kb/firefox-dns-over-https).
* Microsoft Edge:
    1. In Microsoft Edge, select __...__ and then select __Settings__.
    1. In **Settings**, search for *DNS* and then disable **Use secure DNS to specify how to look up the network address for websites**.
    
        :::image type="content" source="../media/how-to/troubleshoot-secure-connection-project/disable-dns-over-http.png" alt-text="Screenshot of the Use secure DNS setting in Microsoft Edge." lightbox="../media/how-to/troubleshoot-secure-connection-project/disable-dns-over-http.png":::

## Proxy configuration

If you're using a proxy, it might block access to a secured project. To test, try one of these options:

* Temporarily disable the proxy setting, and then try to connect.
* Create a [Proxy auto-config (PAC)](https://wikipedia.org/wiki/Proxy_auto-config) file that allows direct access to the fully qualified domain names (FQDNs) listed on the private endpoint, and to the FQDN for any compute instances.
* Set up your proxy server to forward DNS requests to Azure DNS.
* Make sure the proxy lets connections to Azure Machine Learning (AML) APIs, such as `*.<region>.api.azureml.ms` and `*.instances.azureml.ms`.

## Troubleshoot storage connection issues

When you create a project, Azure Storage creates several connections for data upload and artifact storage, including prompt flow. If your hub's associated Azure Storage account has public network access set to **Disabled**, these storage connections can take longer to create. 

Try these steps to troubleshoot:
1. In the Azure portal, check the network settings of the storage account that's associated with your hub.
  * If public network access is set to __Enabled from selected virtual networks and IP addresses__, make sure the correct IP address ranges are added to allow access to your storage account.
  * If public network access is set to __Disabled__, make sure a private endpoint from your Azure virtual network to your storage account is configured with Target sub-resource set to blob. Also, grant the [Reader](/azure/role-based-access-control/built-in-roles#reader) role for the storage account private endpoint to the managed identity.
1. In the Azure portal, go to your Azure AI Foundry hub. Make sure the managed virtual network is provisioned and the outbound private endpoint to blob storage is Active. Learn more in [How to configure a managed network for Azure AI Foundry hubs](configure-managed-network.md).
1. Go to Azure AI Foundry > your project > project settings.
1. Refresh the page. Several connections appear, including `workspaceblobstore`.
