---
title: Troubleshoot private endpoint connection
titleSuffix: Azure Machine Learning
description: 'Learn how to troubleshoot connectivity problems to a workspace that is configured with a private endpoint.'
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.topic: troubleshooting
ms.author: scottpolly
author: s-polly
ms.reviewer: shshubhe
ms.date: 09/11/2026
ms.custom: sfi-image-nochange
ai-usage: ai-assisted
# Customer Intent: As an admin, I need to understand how to troubleshoot connectivity problems to a workspace that is configured with a private endpoint.
---

# Troubleshoot private endpoint connection problems

When you connect to an Azure Machine Learning workspace configured with a private endpoint, you might encounter a *403* error or a message saying that access is forbidden. This article explains how you can check for common configuration problems that cause this error.

> [!TIP]
> Before using the steps in this article, try the Azure Machine Learning workspace diagnostic API. It can help identify configuration problems with your workspace. For more information, see [How to use workspace diagnostics](how-to-workspace-diagnostic-api.md).

## DNS configuration

The troubleshooting steps for DNS configuration differ based on whether you use Azure DNS or a custom DNS. Use the following steps to determine which one you're using:

1. In the [Azure portal](https://portal.azure.com), select the private endpoint for your Azure Machine Learning workspace.

1. From the **Overview** page, select the **Network Interface** link.

    :::image type="content" source="media/how-to-troubleshoot-secure-connection-workspace/private-endpoint-overview.png" alt-text="Screenshot of the private endpoint overview with network interface link highlighted." lightbox="media/how-to-troubleshoot-secure-connection-workspace/private-endpoint-overview.png":::

1. Under **Settings**, select **IP Configurations** and then select the **Virtual network** link.

    :::image type="content" source="media/how-to-troubleshoot-secure-connection-workspace/network-interface-ip-configurations.png" alt-text="Screenshot of the IP configuration with virtual network link highlighted." lightbox="media/how-to-troubleshoot-secure-connection-workspace/network-interface-ip-configurations.png":::

1. From the **Settings** section on the left of the page, select the **DNS servers** entry.

    :::image type="content" source="./media/how-to-troubleshoot-secure-connection-workspace/dns-servers.png" alt-text="Screenshot of the DNS servers configuration.":::

    * If this value is **Default (Azure-provided)** or **168.63.129.16**, the virtual network uses Azure-provided DNS. Verify that the affected client's network interface doesn't override this setting, then continue to [Azure DNS troubleshooting](#azure-dns-troubleshooting).
    * If a different IP address is listed, the virtual network uses custom DNS. Verify that the affected client uses that resolver, then continue to [Custom DNS troubleshooting](#custom-dns-troubleshooting).

### Custom DNS troubleshooting

Use the following steps to verify if your custom DNS solution is correctly resolving names to IP addresses:

1. From a virtual machine, laptop, desktop, or other compute resource that has a working connection to the private endpoint, open a web browser. In the browser, use the URL for your Azure region:

    | Azure region | URL |
    | ----- | ----- |
    | Azure Government | <https://portal.azure.us/?feature.privateendpointmanagedns=false> |
    | Microsoft Azure operated by 21Vianet | <https://portal.azure.cn/?feature.privateendpointmanagedns=false> |
    | All other regions | <https://portal.azure.com/?feature.privateendpointmanagedns=false> |

1. In the portal, select the private endpoint for the workspace. Make a list of FQDNs listed for the private endpoint.

    :::image type="content" source="media/how-to-troubleshoot-secure-connection-workspace/custom-dns-settings.png" alt-text="Screenshot of the private endpoint with custom DNS settings highlighted." lightbox="media/how-to-troubleshoot-secure-connection-workspace/custom-dns-settings.png":::

1. Open a command prompt, PowerShell, or other command line and run the following command for each FQDN returned from the previous step. Each time you run the command, verify that the IP address returned matches the IP address listed in the portal for the FQDN:

    `nslookup <fqdn>`

    For example, running the command `nslookup a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1.workspace.eastus.api.azureml.ms` returns a value similar to the following text:

    ```output
    Server: yourdnsserver
    Address: yourdnsserver-IP-address

    Name: a0a0a0a0-bbbb-cccc-dddd-e1e1e1e1e1e1.workspace.eastus.api.azureml.ms
    Address: 10.3.0.5
    ```

1. If the `nslookup` command returns an error, or returns a different IP address than displayed in the portal, the custom DNS solution isn't configured correctly. For more information, see [How to use your workspace with a custom DNS server](how-to-custom-dns.md).

    Verify that your DNS server conditionally forwards the Azure Machine Learning DNS zones required for your scenario. For commercial Azure, these zones include `api.azureml.ms`, `notebooks.azure.net`, `instances.ml.azure.ms`, and `aznbcontent.net`. Include `inference.ml.azure.com` when you use managed online endpoints. Also verify private endpoints and DNS records for the workspace dependencies you use. For cloud-specific zones and managed online endpoint wildcard records, see [How to use your workspace with a custom DNS server](how-to-custom-dns.md).

### Azure DNS troubleshooting

When using Azure DNS for name resolution, use the following steps to verify that the Private DNS integration is configured correctly:

1. On the Private Endpoint, select **DNS configuration**. For each entry in the **Private DNS zone** column, there should also be an entry in the **DNS zone group** column.

    :::image type="content" source="media/how-to-troubleshoot-secure-connection-workspace/dns-zone-group.png" alt-text="Screenshot of the DNS configuration with Private DNS zone and group highlighted." lightbox="media/how-to-troubleshoot-secure-connection-workspace/dns-zone-group.png":::

    * If a **Private DNS zone** entry has no **DNS zone group** entry, verify that the private endpoint connection is approved and that the private DNS zone names, records, and DNS zone group configuration are correct. Add or correct the DNS zone group without deleting the private endpoint when possible.
    * If **DNS zone group** isn't empty, select the link for the **Private DNS zone** entry.

        From the Private DNS zone, select **Virtual network links**. Add links for each client virtual network and applicable peered virtual network that must resolve the private endpoint. Verify that the zone contains the expected private DNS records.

        :::image type="content" source="./media/how-to-troubleshoot-secure-connection-workspace/virtual-network-links.png" alt-text="Screenshot of the virtual network links for the Private DNS zone.":::

1. Repeat the previous steps for the rest of the Private DNS zone entries.

## Browser configuration (DNS over HTTPS)

Check whether DNS over HTTPS is enabled in your web browser. DNS over HTTPS can bypass the operating system or corporate DNS resolver and return public IP addresses instead of the private endpoint address.

* Mozilla Firefox: For more information, see [Disable DNS over HTTPS in Firefox](https://support.mozilla.org/en-US/kb/firefox-dns-over-https).
* Microsoft Edge:
    1. Select **...** in the top right corner, then select **Settings**.
    1. From settings, search for **DNS** and then disable **Use secure DNS to specify how to look up the network address for websites**.

        :::image type="content" source="./media/how-to-troubleshoot-secure-connection-workspace/disable-dns-over-http.png" alt-text="Screenshot of the use secure DNS setting in Microsoft Edge.":::

    For managed devices, set the [DnsOverHttpsMode policy](/deployedge/microsoft-edge-policies#dnsoverhttpsmode) to `off`.

## Proxy configuration

If you use a proxy, it might prevent communication with a secured workspace. To test, use one of the following options:

* Temporarily disable the proxy setting and see if you can connect.
* Create a [Proxy auto-config (PAC)](https://wikipedia.org/wiki/Proxy_auto-config) file that allows direct access to the private endpoint FQDNs and the dependent resource endpoints required by your workspace scenario. Verify the required endpoints by using [Configure inbound and outbound network traffic](how-to-access-azureml-behind-firewall.md).
* Configure conditional forwarding for the required private DNS zones in a DNS forwarder or Azure DNS Private Resolver. For on-premises DNS, forward requests through a DNS forwarder or Azure DNS Private Resolver hosted in a virtual network. Don't configure an HTTP or HTTPS proxy to forward DNS requests to `168.63.129.16`.
