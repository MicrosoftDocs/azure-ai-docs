---
title: Use custom DNS server
titleSuffix: Azure Machine Learning
description: How to configure a custom DNS server to work with an Azure Machine Learning workspace and private endpoint.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.reviewer: meerakurup 
ms.author: scottpolly
author: s-polly
ms.date: 05/06/2025
ms.topic: how-to
monikerRange: 'azureml-api-2 || azureml-api-1'
ms.custom: sfi-image-nochange
---

# How to use your workspace with a custom DNS server

When using an Azure Machine Learning workspace (including Azure AI hubs) with a private endpoint, there are [several ways to handle DNS name resolution](/azure/private-link/private-endpoint-dns). By default, Azure automatically handles name resolution for your workspace and private endpoint. If you instead __use your own custom DNS server__, you must manually create DNS entries or use conditional forwarders for the workspace.

> [!IMPORTANT]
> This article covers how to find the fully qualified domain names (FQDN) and IP addresses for these entries if you would like to manually register DNS records in your DNS solution. Additionally this article provides architecture recommendations for how to configure your custom DNS solution to automatically resolve FQDNs to the correct IP addresses. This article does NOT provide information on configuring the DNS records for these items. Consult the documentation for your DNS software for information on how to add records.

## Prerequisites

- An Azure Virtual Network that uses [your own DNS server](/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances#name-resolution-that-uses-your-own-dns-server).

:::moniker range="azureml-api-2"
- An Azure Machine Learning workspace with a private endpoint, including hub workspaces such as those used by Azure AI Foundry. For more information, see [Create an Azure Machine Learning workspace](how-to-manage-workspace.md).

- If your workspace dependency resources are secured with an __Azure Virtual network__, familiarity with the [Network isolation during training & inference](./how-to-network-security-overview.md) article.
:::moniker-end
:::moniker range="azureml-api-1"
- An Azure Machine Learning workspace with a private endpoint. For more information, see [Create an Azure Machine Learning workspace](./v1/how-to-manage-workspace.md).
- Familiarity with using [Network isolation during training & inference](./how-to-network-security-overview.md).
:::moniker-end

- Familiarity with [Azure Private Endpoint DNS zone configuration](/azure/private-link/private-endpoint-dns)

- Familiarity with [Azure Private DNS](/azure/dns/private-dns-privatednszone)

- Optionally, [Azure CLI](/cli/azure/install-azure-cli) or [Azure PowerShell](/powershell/azure/install-azure-powershell).

## Automated DNS server integration

### Introduction

There are two common architectures to use automated DNS server integration with Azure Machine Learning:

* A custom [DNS server hosted in an Azure Virtual Network](#dns-vnet).
* A custom [DNS server hosted on-premises](#dns-on-premises), connected to Azure Machine Learning through ExpressRoute.

While your architecture may differ from these examples, you can use them as a reference point. Both example architectures provide troubleshooting steps that can help you identify components that may be misconfigured.

Another option is to modify the `hosts` file on the client that is connecting to the Azure Virtual Network (virtual network) that contains your workspace. For more information, see the [Host file](#hosts) section.
### Workspace DNS resolution path

Access to a given Azure Machine Learning workspace via Private Link is done by communicating with the following Fully Qualified Domains (called the workspace FQDNs):


**Azure Public regions**:
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.azureml.ms```
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.cert.api.azureml.ms```
- ```<compute instance name>.<region the workspace was created in>.instances.azureml.ms```
- `<compute instance name>-22.<region the workspace was created in>.instances.azureml.ms` - Used by the `az ml compute connect-ssh` command to connect to computes in a private virtual network.
- ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.azure.net```
- ```<managed online endpoint name>.<region>.inference.ml.azure.com``` - Used by managed online endpoints

**Microsoft Azure operated by 21Vianet regions**:
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.ml.azure.cn```
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.cert.api.ml.azure.cn```
- ```<compute instance name>.<region the workspace was created in>.instances.azureml.cn```
- `<compute instance name>-22.<region the workspace was created in>.instances.azureml.cn` - Used by the `az ml compute connect-ssh` command to connect to computes in a private virtual network.
- ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.chinacloudapi.cn```
- ```<managed online endpoint name>.<region>.inference.ml.azure.cn``` - Used by managed online endpoints

**Azure US Government regions**:
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.ml.azure.us```
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.cert.api.ml.azure.us```
- ```<compute instance name>.<region the workspace was created in>.instances.azureml.us```
- `<compute instance name>-22.<region the workspace was created in>.instances.azureml.us` - Used by the `az ml compute connect-ssh` command to connect to computes in a private virtual network.
- ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.usgovcloudapi.net```
- ```<managed online endpoint name>.<region>.inference.ml.azure.us``` - Used by managed online endpoints

The Fully Qualified Domains resolve to the following Canonical Names (CNAMEs) called the workspace Private Link FQDNs:

**Azure Public regions**:
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.privatelink.api.azureml.ms```
- ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.privatelink.notebooks.azure.net```
- ```<managed online endpoint name>.<per-workspace globally-unique identifier>.inference.<region>.privatelink.api.azureml.ms``` - Used by managed online endpoints

**Azure operated by 21Vianet regions**:
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.privatelink.api.ml.azure.cn```
- ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.privatelink.notebooks.chinacloudapi.cn```
- ```<managed online endpoint name>.<per-workspace globally-unique identifier>.inference.<region>.privatelink.api.ml.azure.cn``` - Used by managed online endpoints

**Azure US Government regions**:
- ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.privatelink.api.ml.azure.us```
- ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.privatelink.notebooks.usgovcloudapi.net```
- ```<managed online endpoint name>.<per-workspace globally-unique identifier>.inference.<region>.privatelink.api.ml.azure.us``` - Used by managed online endpoints

The FQDNs resolve to the IP addresses of the Azure Machine Learning workspace in that region. However, resolution of the workspace Private Link FQDNs can be overridden by using a custom DNS server hosted in the virtual network. For an example of this architecture, see the [custom DNS server hosted in a virtual network](#example-custom-dns-server-hosted-in-virtual-network) example. For hub and project workspaces, project workspaces inherit the FQDNs from the hub workspace.

[!INCLUDE [machine-learning-add-dns-records](includes/machine-learning-add-dns-records.md)]

## Manual DNS server integration

This section discusses which Fully Qualified Domains to create A records for in a DNS Server, and which IP address to set the value of the A record to.

### Retrieve Private Endpoint FQDNs

#### Azure Public region

The following list contains the fully qualified domain names (FQDNs) used by your workspace if it is in the Azure Public Cloud:

* `<workspace-GUID>.workspace.<region>.cert.api.azureml.ms` 
* `<workspace-GUID>.workspace.<region>.api.azureml.ms`
* `ml-<workspace-name, truncated>-<region>-<workspace-guid>.<region>.notebooks.azure.net`

    > [!NOTE]
    > The workspace name for this FQDN may be truncated. Truncation is done to keep `ml-<workspace-name, truncated>-<region>-<workspace-guid>` at 63 characters or less.
* `<instance-name>.<region>.instances.azureml.ms`

    > [!NOTE]
    > * Compute instances can be accessed only from within the virtual network.
    > * The IP address for this FQDN is **not** the IP of the compute instance. Instead, use the private IP address of the workspace private endpoint (the IP of the `*.api.azureml.ms` entries.)
* `<instance-name>-22.<region>.instances.azureml.ms` - Only used by the `az ml compute connect-ssh` command to connect to computes in a private virtual network. Not needed if you aren't using a managed network or SSH connections.
* `<managed online endpoint name>.<region>.inference.ml.azure.com` - Used by managed online endpoints

#### Microsoft Azure operated by 21Vianet region

The following FQDNs are for Microsoft Azure operated by 21Vianet regions:

* `<workspace-GUID>.workspace.<region>.cert.api.ml.azure.cn`
* `<workspace-GUID>.workspace.<region>.api.ml.azure.cn`
* `ml-<workspace-name, truncated>-<region>-<workspace-guid>.<region>.notebooks.chinacloudapi.cn`

    > [!NOTE]
    > The workspace name for this FQDN may be truncated. Truncation is done to keep `ml-<workspace-name, truncated>-<region>-<workspace-guid>` at 63 characters or less.

* `<instance-name>.<region>.instances.azureml.cn`

   * The IP address for this FQDN is **not** the IP of the compute instance. Instead, use the private IP address of the workspace private endpoint (the IP of the `*.api.azureml.ms` entries.)

* `<instance-name>-22.<region>.instances.azureml.cn` - Only used by the `az ml compute connect-ssh` command to connect to computes in a private virtual network. Not needed if you aren't using a managed network or SSH connections.
* `<managed online endpoint name>.<region>.inference.ml.azure.cn` - Used by managed online endpoints
* `models.ai.azure.com` - Used for standard deployment

#### Azure US Government

The following FQDNs are for Azure US Government regions:

* `<workspace-GUID>.workspace.<region>.cert.api.ml.azure.us`
* `<workspace-GUID>.workspace.<region>.api.ml.azure.us`
* `ml-<workspace-name, truncated>-<region>-<workspace-guid>.<region>.notebooks.usgovcloudapi.net`

    > [!NOTE]
    > The workspace name for this FQDN may be truncated. Truncation is done to keep `ml-<workspace-name, truncated>-<region>-<workspace-guid>` at 63 characters or less.
* `<instance-name>.<region>.instances.azureml.us`
    > * The IP address for this FQDN is **not** the IP of the compute instance. Instead, use the private IP address of the workspace private endpoint (the IP of the `*.api.azureml.ms` entries.)

* `<instance-name>-22.<region>.instances.azureml.us` - Only used by the `az ml compute connect-ssh` command to connect to computes in a private virtual network. Not needed if you aren't using a managed network or SSH connections.

* `<managed online endpoint name>.<region>.inference.ml.azure.us` - Used by managed online endpoints

### Find the IP addresses

To find the internal IP addresses for the FQDNs in the virtual network, use one of the following methods:

> [!NOTE]
> The fully qualified domain names and IP addresses are different based on your configuration. For example, the GUID value in the domain name is specific to your workspace.

# [Azure CLI](#tab/azure-cli)

1. To get the ID of the private endpoint network interface, use the following command:

    ```azurecli
    az network private-endpoint show --name <endpoint> --resource-group <resource-group> --query 'networkInterfaces[*].id' --output table
    ```

1. To get the IP address and FQDN information for the workspace or hub workspace, use the following command. Replace `<resource-id>` with the ID from the previous step:

    ```azurecli
    az network nic show --ids <resource-id> --query 'ipConfigurations[*].{IPAddress: privateIPAddress, FQDNs: privateLinkConnectionProperties.fqdns}'
    ```

    The output is similar to the following text:

    ```json
    [
        {
            "FQDNs": [
            "fb7e20a0-8891-458b-b969-55ddb3382f51.workspace.eastus.api.azureml.ms",
            "fb7e20a0-8891-458b-b969-55ddb3382f51.workspace.eastus.cert.api.azureml.ms"
            ],
            "IPAddress": "10.1.0.5"
        },
        {
            "FQDNs": [
            "ml-myworkspace-eastus-fb7e20a0-8891-458b-b969-55ddb3382f51.eastus.notebooks.azure.net"
            ],
            "IPAddress": "10.1.0.6"
        },
        {
            "FQDNs": [
            "*.eastus.inference.ml.azure.com"
            ],
            "IPAddress": "10.1.0.7"
        }
    ]
    ```
    
# [Azure PowerShell](#tab/azure-powershell)

```azurepowershell
$workspaceDns=Get-AzPrivateEndpoint -Name <endpoint> -resourcegroupname <resource-group>
$workspaceDns.CustomDnsConfigs | format-table
```

# [Azure portal](#tab/azure-portal)

1. In the [Azure portal](https://portal.azure.com), select your Azure Machine Learning __workspace__.
1. From the __Settings__ section, select __Private endpoint connections__.
1. Select the link in the __Private endpoint__ column that is displayed.
1. A list of the fully qualified domain names (FQDN) and IP addresses for the workspace private endpoint are at the bottom of the page.

    :::image type="content" source="./media/how-to-custom-dns/private-endpoint-custom-dns.png" alt-text="List of FQDNs in the portal":::

---

The information returned from all methods is the same; a list of the FQDN and private IP address for the resources. The following example is from the Azure Public Cloud:

| FQDN | IP Address |
| ----- | ----- |
| `fb7e20a0-8891-458b-b969-55ddb3382f51.workspace.eastus.api.azureml.ms` | `10.1.0.5` |
| `fb7e20a0-8891-458b-b969-55ddb3382f51.workspace.eastus.cert.api.azureml.ms` | `10.1.0.5` |
| `ml-myworkspace-eastus-fb7e20a0-8891-458b-b969-55ddb3382f51.eastus.notebooks.azure.net` | `10.1.0.6` |
| `*.eastus.inference.ml.azure.com` | `10.1.0.7` |

The following table shows example IPs from Microsoft Azure operated by 21Vianet regions:

| FQDN | IP Address |
| ----- | ----- |
| `52882c08-ead2-44aa-af65-08a75cf094bd.workspace.chinaeast2.api.ml.azure.cn` | `10.1.0.5` |
| `52882c08-ead2-44aa-af65-08a75cf094bd.workspace.chinaeast2.cert.api.ml.azure.cn` | `10.1.0.5` |
| `ml-mype-pltest-chinaeast2-52882c08-ead2-44aa-af65-08a75cf094bd.chinaeast2.notebooks.chinacloudapi.cn` | `10.1.0.6` |
| `*.chinaeast2.inference.ml.azure.cn` | `10.1.0.7` |

The following table shows example IPs from Azure US Government regions:

| FQDN | IP Address |
| ----- | ----- |
| `52882c08-ead2-44aa-af65-08a75cf094bd.workspace.usgovvirginia.api.ml.azure.us` | `10.1.0.5` |
| `52882c08-ead2-44aa-af65-08a75cf094bd.workspace.usgovvirginia.cert.api.ml.azure.us` | `10.1.0.5` |
| `ml-mype-plt-usgovvirginia-52882c08-ead2-44aa-af65-08a75cf094bd.usgovvirginia.notebooks.usgovcloudapi.net` | `10.1.0.6` |
| `*.usgovvirginia.inference.ml.azure.us` | `10.1.0.7` |

> [!NOTE]
> Managed online endpoints share the workspace private endpoint. If you're manually adding DNS records to the private DNS zone `privatelink.api.azureml.ms`, an A record with wildcard
> `*.<per-workspace globally-unique identifier>.inference.<region>.privatelink.api.azureml.ms` should be added to route all endpoints under the workspace to the private endpoint.

<a id='dns-vnet'></a>

### Create A records in custom DNS server

Once the list of FQDNs and corresponding IP addresses are gathered, proceed to create A records in the configured DNS Server. Refer to the documentation for your DNS server to determine how to create A records. We recommend creating a unique zone for the entire FQDN, and creating the A record in the root of the zone.

## Example: Custom DNS Server hosted in virtual network

This architecture uses the common Hub and Spoke virtual network topology. One virtual network contains the DNS server and one contains the private endpoint to the Azure Machine Learning workspace and associated resources. There must be a valid route between both virtual networks. For example, through a series of peered virtual networks.

:::image type="content" source="./media/how-to-custom-dns/custom-dns-topology.svg" alt-text="Diagram of custom DNS hosted in Azure topology"  lightbox ="./media/how-to-custom-dns/custom-dns-topology-expanded.png":::

The following steps describe how this topology works:

1. **Create Private DNS Zone and link to DNS Server Virtual Network**:

    The first step in ensuring a Custom DNS solution works with your Azure Machine Learning workspace is to create two Private DNS Zones rooted at the following domains:

    **Azure Public regions**:
    - ```privatelink.api.azureml.ms```
    - ```privatelink.notebooks.azure.net```

    **Microsoft Azure operated by 21Vianet regions**:
    - ```privatelink.api.ml.azure.cn```
    - ```privatelink.notebooks.chinacloudapi.cn```

    **Azure US Government regions**:
    - ```privatelink.api.ml.azure.us```
    - ```privatelink.notebooks.usgovcloudapi.net```

    > [!NOTE]
    > Managed online endpoints share the workspace private endpoint. If you're manually adding DNS records to the private DNS zone `privatelink.api.azureml.ms`, an A record with wildcard
    > `*.<per-workspace globally-unique identifier>.inference.<region>.privatelink.api.azureml.ms` should be added to route all endpoints under the workspace to the private endpoint.

    Following creation of the Private DNS Zone, it needs to be linked to the DNS Server Virtual Network. The Virtual Network that contains the DNS Server.

    A Private DNS Zone overrides name resolution for all names within the scope of the root of the zone. This override applies to all Virtual Networks the Private DNS Zone is linked to. For example, if a Private DNS Zone rooted at `privatelink.api.azureml.ms` is linked to Virtual Network foo, all resources in Virtual Network foo that attempt to resolve `bar.workspace.westus2.privatelink.api.azureml.ms` receives any record that is listed in the `privatelink.api.azureml.ms` zone.

    However, records listed in Private DNS Zones are only returned to devices resolving domains using the default Azure DNS Virtual Server IP address. So the custom DNS Server resolves domains for devices spread throughout your network topology. But the custom DNS Server needs to resolve Azure Machine Learning-related domains against the Azure DNS Virtual Server IP address.

2. **Create private endpoint with private DNS integration targeting Private DNS Zone linked to DNS Server Virtual Network**:

    The next step is to create a Private Endpoint to the Azure Machine Learning workspace. The private endpoint targets both Private DNS Zones created in step 1. This step ensures all communication with the workspace is done via the Private Endpoint in the Azure Machine Learning Virtual Network.

    > [!IMPORTANT]
    > The private endpoint must have Private DNS integration enabled for this example to function correctly.

3. **Create conditional forwarder in DNS Server to forward to Azure DNS**:

    Next, create a conditional forwarder to the Azure DNS Virtual Server. The conditional forwarder ensures that the DNS server always queries the Azure DNS Virtual Server IP address for FQDNs related to your workspace. This means that the DNS Server returns the corresponding record from the Private DNS Zone.

    The following list is of zones to conditionally forward. The Azure DNS Virtual Server IP address is 168.63.129.16:

    **Azure Public regions**:
    - ```api.azureml.ms```
    - ```notebooks.azure.net```
    - ```instances.azureml.ms```
    - ```aznbcontent.net```
    - ```inference.ml.azure.com``` - Used by managed online endpoints

    **Microsoft Azure operated by 21Vianet regions**:
    - ```api.ml.azure.cn```
    - ```notebooks.chinacloudapi.cn```
    - ```instances.azureml.cn```
    - ```aznbcontent.net```
    - ```inference.ml.azure.cn``` - Used by managed online endpoints

    **Azure US Government regions**:
    - ```api.ml.azure.us```
    - ```notebooks.usgovcloudapi.net```
    - ```instances.azureml.us```
    - ```aznbcontent.net```
    - ```inference.ml.azure.us``` - Used by managed online endpoints

    > [!IMPORTANT]
    > Configuration steps for the DNS Server aren't included here, as there are many DNS solutions available that can be used as a custom DNS Server. Refer to the documentation for your DNS solution for how to appropriately configure conditional forwarding.

4. **Resolve workspace domain**:

    At this point, all setup is done. Now any client that uses DNS Server for name resolution and has a route to the Azure Machine Learning Private Endpoint can proceed to access the workspace.
    The client starts by querying DNS Server for the address of the following FQDNs:

    **Azure Public regions**:
    - ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.azureml.ms```
    - ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.azure.net```
    - ```<managed online endpoint name>.<region>.inference.ml.azure.com``` - Used by managed online endpoints

    **Microsoft Azure operated by 21Vianet regions**:
    - ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.ml.azure.cn```
    - ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.chinacloudapi.cn```
    - ```<managed online endpoint name>.<region>.inference.ml.azure.cn``` - Used by managed online endpoints

    **Azure US Government regions**:
    - ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.ml.azure.us```
    - ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.usgovcloudapi.net```
    - ```<managed online endpoint name>.<region>.inference.ml.azure.us``` - Used by managed online endpoints

5. **Azure DNS recursively resolves workspace domain to CNAME**:

    The DNS Server resolves the FQDNs from step 4 from Azure DNS. Azure DNS responds with one of the domains listed in step 1.

6. **DNS Server recursively resolves workspace domain CNAME record from Azure DNS**:

    DNS Server proceeds to recursively resolve the CNAME received in step 5. Because there was a conditional forwarder setup in step 3, DNS Server sends the request to the Azure DNS Virtual Server IP address for resolution.

7. **Azure DNS returns records from Private DNS zone**:

    The corresponding records stored in the Private DNS Zones are returned to DNS Server, which means Azure DNS Virtual Server returns the IP addresses of the Private Endpoint.

8. **Custom DNS Server resolves workspace domain name to private endpoint address**:

    Ultimately the Custom DNS Server now returns the IP addresses of the Private Endpoint to the client from step 4. This ensures that all traffic to the Azure Machine Learning workspace is via the Private Endpoint.

#### Troubleshooting

If you can't access the workspace from a virtual machine or jobs fail on compute resources in the virtual network, use the following steps to identify the cause:

1. **Locate the workspace FQDNs on the Private Endpoint**:

    Navigate to the Azure portal using one of the following links:
    - [Azure Public regions](https://portal.azure.com/?feature.privateendpointmanagedns=false)
    - [Microsoft Azure operated by 21Vianet regions](https://portal.azure.cn/?feature.privateendpointmanagedns=false)
    - [Azure US Government regions](https://portal.azure.us/?feature.privateendpointmanagedns=false)

    Navigate to the Private Endpoint to the Azure Machine Learning workspace. The workspace FQDNs is listed on the "Overview" tab.

1. **Access compute resource in Virtual Network topology**:

    Proceed to access a compute resource in the Azure Virtual Network topology. This likely requires accessing a Virtual Machine in a Virtual Network that is peered with the Hub Virtual Network.

1. **Resolve workspace FQDNs**:

    Open a command prompt, shell, or PowerShell. Then for each of the workspace FQDNs, run the following command:

    `nslookup <workspace FQDN>`

    The result of each nslookup should return one of the two private IP addresses on the Private Endpoint to the Azure Machine Learning workspace. If it doesn't, then there's something misconfigured in the custom DNS solution.

    Possible causes:
    - The compute resource running the troubleshooting commands isn't using DNS Server for DNS resolution
    - The Private DNS Zones chosen when creating the Private Endpoint aren't linked to the DNS Server virtual network
    - Conditional forwarders to Azure DNS Virtual Server IP weren't configured correctly

<a id='dns-on-premises'></a>

## Example: Custom DNS Server hosted on-premises

This architecture uses the common Hub and Spoke virtual network topology. ExpressRoute is used to connect from your on-premises network to the Hub virtual network. The Custom DNS server is hosted on-premises. A separate virtual network contains the private endpoint to the Azure Machine Learning workspace and associated resources. With this topology, there needs to be another virtual network hosting a DNS server that can send requests to the Azure DNS Virtual Server IP address.

:::image type="content" source="./media/how-to-custom-dns/custom-dns-express-route.svg" alt-text="Diagram of custom DNS hosted on-premises topology" lightbox ="./media/how-to-custom-dns/custom-dns-express-route-expanded.png" :::

The following steps describe how this topology works:

1. **Create Private DNS Zone and link to DNS Server Virtual Network**:

    The first step in ensuring a Custom DNS solution works with your Azure Machine Learning workspace is to create two Private DNS Zones rooted at the following domains:

    **Azure Public regions**:
    - ```privatelink.api.azureml.ms```
    - ```privatelink.notebooks.azure.net```

    **Microsoft Azure operated by 21Vianet regions**:
    - ```privatelink.api.ml.azure.cn```
    - ```privatelink.notebooks.chinacloudapi.cn```

    **Azure US Government regions**:
    - ```privatelink.api.ml.azure.us```
    - ```privatelink.notebooks.usgovcloudapi.net```

    > [!NOTE]
    > Managed online endpoints share the workspace private endpoint. If you're manually adding DNS records to the private DNS zone `privatelink.api.azureml.ms`, an A record with wildcard
    > `*.<per-workspace globally-unique identifier>.inference.<region>.privatelink.api.azureml.ms` should be added to route all endpoints under the workspace to the private endpoint.

    Following creation of the Private DNS Zone, it needs to be linked to the DNS Server virtual network – the Virtual Network that contains the DNS Server.

    > [!NOTE]
    > The DNS Server in the virtual network is separate from the On-premises DNS Server.

    A Private DNS Zone overrides name resolution for all names within the scope of the root of the zone. This override applies to all Virtual Networks the Private DNS Zone is linked to. For example, if a Private DNS Zone rooted at `privatelink.api.azureml.ms` is linked to Virtual Network foo, all resources in Virtual Network foo that attempt to resolve `bar.workspace.westus2.privatelink.api.azureml.ms` receives any record that is listed in the privatelink.api.azureml.ms zone.

    However, records listed in Private DNS Zones are only returned to devices resolving domains using the default Azure DNS Virtual Server IP address. The Azure DNS Virtual Server IP address is only valid within the context of a Virtual Network. When using an on-premises DNS server, it isn't able to query the Azure DNS Virtual Server IP address to retrieve records.

    To get around this behavior, create an intermediary DNS Server in a virtual network. This DNS server can query the Azure DNS Virtual Server IP address to retrieve records for any Private DNS Zone linked to the virtual network.

    While the On-premises DNS Server resolves domains for devices spread throughout your network topology, it resolves Azure Machine Learning-related domains against the DNS Server. The DNS Server resolves those domains from the Azure DNS Virtual Server IP address.

2. **Create private endpoint with private DNS integration targeting Private DNS Zone linked to DNS Server Virtual Network**:

    The next step is to create a Private Endpoint to the Azure Machine Learning workspace. The private endpoint targets both Private DNS Zones created in step 1. This ensures all communication with the workspace is done via the Private Endpoint in the Azure Machine Learning Virtual Network.

    > [!IMPORTANT]
    > The private endpoint must have Private DNS integration enabled for this example to function correctly.

3. **Create conditional forwarder in DNS Server to forward to Azure DNS**:

    Next, create a conditional forwarder to the Azure DNS Virtual Server. The conditional forwarder ensures that the DNS server always queries the Azure DNS Virtual Server IP address for FQDNs related to your workspace. This means that the DNS Server returns the corresponding record from the Private DNS Zone.

    The following list is of zones to conditionally forward. The Azure DNS Virtual Server IP address is 168.63.129.16.

    **Azure Public regions**:
    - ```api.azureml.ms```
    - ```notebooks.azure.net```
    - ```instances.azureml.ms```
    - ```aznbcontent.net```
    - ```inference.ml.azure.com``` - Used by managed online endpoints

    **Microsoft Azure operated by 21Vianet regions**:
    - ```api.ml.azure.cn```
    - ```notebooks.chinacloudapi.cn```
    - ```instances.azureml.cn```
    - ```aznbcontent.net```
    - ```inference.ml.azure.cn``` - Used by managed online endpoints

    **Azure US Government regions**:
    - ```api.ml.azure.us```
    - ```notebooks.usgovcloudapi.net```
    - ```instances.azureml.us```
    - ```aznbcontent.net```
    - ```inference.ml.azure.us``` - Used by managed online endpoints

    > [!IMPORTANT]
    > Configuration steps for the DNS Server aren't included here, as there are many DNS solutions available that can be used as a custom DNS Server. Refer to the documentation for your DNS solution for how to appropriately configure conditional forwarding.

4. **Create conditional forwarder in On-premises DNS Server to forward to DNS Server**:

    Next, create a conditional forwarder to the DNS Server in the DNS Server Virtual Network. This forwarder is for the zones listed in step 1. This is similar to step 3, but, instead of forwarding to the Azure DNS Virtual Server IP address, the On-premises DNS Server is targeting the IP address of the DNS Server. As the On-premises DNS Server isn't in Azure, it isn't able to directly resolve records in Private DNS Zones. In this case, the DNS Server proxies requests from the On-premises DNS Server to the Azure DNS Virtual Server IP. This allows the On-premises DNS Server to retrieve records in the Private DNS Zones linked to the DNS Server Virtual Network.

    The following list is the zones to conditionally forward. The IP addresses to forward to are the IP addresses of your DNS Servers:

    **Azure Public regions**:
    - ```api.azureml.ms```
    - ```notebooks.azure.net```
    - ```instances.azureml.ms```
    - ```inference.ml.azure.com``` - Used by managed online endpoints

    **Microsoft Azure operated by 21Vianet regions**:
    - ```api.ml.azure.cn```
    - ```notebooks.chinacloudapi.cn```
    - ```instances.azureml.cn```
    - ```inference.ml.azure.cn``` - Used by managed online endpoints

    **Azure US Government regions**:
    - ```api.ml.azure.us```
    - ```notebooks.usgovcloudapi.net```
    - ```instances.azureml.us```
    - ```inference.ml.azure.us``` - Used by managed online endpoints

    > [!IMPORTANT]
    > Configuration steps for the DNS Server aren't included here, as there are many DNS solutions available that can be used as a custom DNS Server. Refer to the documentation for your DNS solution for how to appropriately configure conditional forwarding.

5. **Resolve workspace domain**:

    At this point, all setup is done. Any client that uses on-premises DNS Server for name resolution, and has a route to the Azure Machine Learning Private Endpoint, can proceed to access the workspace.

    The client starts by querying On-premises DNS Server for the address of the following FQDNs:

    **Azure Public regions**:
    - ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.azureml.ms```
    - ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.azure.net```
    - ```<managed online endpoint name>.<region>.inference.ml.azure.com``` - Used by managed online endpoints

    **Microsoft Azure operated by 21Vianet regions**:
    - ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.ml.azure.cn```
    - ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.chinacloudapi.cn```
    - ```<managed online endpoint name>.<region>.inference.ml.azure.cn``` - Used by managed online endpoints

    **Azure US Government regions**:
    - ```<per-workspace globally-unique identifier>.workspace.<region the workspace was created in>.api.ml.azure.us```
    - ```ml-<workspace-name, truncated>-<region>-<per-workspace globally-unique identifier>.<region>.notebooks.usgovcloudapi.net```
    - ```<managed online endpoint name>.<region>.inference.ml.azure.us``` - Used by managed online endpoints

6. **On-premises DNS server recursively resolves workspace domain**:

    The on-premises DNS Server resolves the FQDNs from step 5 from the DNS Server. Because there's a conditional forwarder (step 4), the on-premises DNS Server sends the request to the DNS Server for resolution.

7. **DNS Server resolves workspace domain to CNAME from Azure DNS**:

    The DNS server resolves the FQDNs from step 5 from the Azure DNS. Azure DNS responds with one of the domains listed in step 1.

8. **On-premises DNS Server recursively resolves workspace domain CNAME record from DNS Server**:

    On-premises DNS Server proceeds to recursively resolve the CNAME received in step 7. Because there was a conditional forwarder setup in step 4, On-premises DNS Server sends the request to DNS Server for resolution.

9. **DNS Server recursively resolves workspace domain CNAME record from Azure DNS**:

    DNS Server proceeds to recursively resolve the CNAME received in step 7. Because there was a conditional forwarder setup in step 3, DNS Server sends the request to the Azure DNS Virtual Server IP address for resolution.

10. **Azure DNS returns records from Private DNS zone**:

    The corresponding records stored in the Private DNS Zones are returned to DNS Server, which means the Azure DNS Virtual Server returns the IP addresses of the Private Endpoint.

11. **On-premises DNS Server resolves workspace domain name to private endpoint address**:

    The query from On-premises DNS Server to DNS Server in step 8 ultimately returns the IP addresses associated with the Private Endpoint to the Azure Machine Learning workspace. These IP addresses are returned to the original client, which now communicates with the Azure Machine Learning workspace over the Private Endpoint configured in step 1.

    > [!IMPORTANT]
    > If VPN Gateway is being used in this set up, along with custom DNS Server IPs on the virtual network, then Azure DNS IP (168.63.129.16) needs to be added in the list as well to maintain undisrupted communication.

<a id="hosts"></a>
## Example: Hosts file

The `hosts` file is a text document that Linux, macOS, and Windows all use to override name resolution for the local computer. The file contains a list of IP addresses and the corresponding host name. When the local computer tries to resolve a host name, if the host name is listed in the `hosts` file, the name is resolved to the corresponding IP address.

> [!IMPORTANT]
> The `hosts` file only overrides name resolution for the local computer. If you want to use a `hosts` file with multiple computers, you must modify it individually on each computer.

The following table lists the location of the `hosts` file:

| Operating system | Location |
| ----- | ----- |
| Linux | `/etc/hosts` |
| macOS | `/etc/hosts` |
| Windows | `%SystemRoot%\System32\drivers\etc\hosts` |

> [!TIP]
> The name of the file is `hosts` with no extension. When editing the file, use administrator access. For example, on Linux or macOS you might use `sudo vi`. On Windows, run notepad as an administrator.

The following text is an example of `hosts` file entries for Azure Machine Learning:

```bash
# For core Azure Machine Learning hosts
10.1.0.5    fb7e20a0-8891-458b-b969-55ddb3382f51.workspace.eastus.api.azureml.ms
10.1.0.5    fb7e20a0-8891-458b-b969-55ddb3382f51.workspace.eastus.cert.api.azureml.ms
10.1.0.6    ml-myworkspace-eastus-fb7e20a0-8891-458b-b969-55ddb3382f51.eastus.notebooks.azure.net

# For a managed online/batch endpoint named 'mymanagedendpoint'
10.1.0.7    mymanagedendpoint.eastus.inference.ml.azure.com

# For a compute instance named 'mycomputeinstance'
10.1.0.5    mycomputeinstance.eastus.instances.azureml.ms
```

For more information on the `hosts` file, see [https://wikipedia.org/wiki/Hosts_(file)](https://wikipedia.org/wiki/Hosts_(file)).

## Dependency services DNS resolution

The services that your workspace relies on may also be secured using a private endpoint. If so, then you might need to create a custom DNS record if you need to directly communicate with the service. For example, if you want to directly work with the data in an Azure Storage Account used by your workspace.

> [!NOTE]
> Some services have multiple private-endpoints for subservices or features. For example, an Azure Storage Account may have individual private endpoints for Blob, File, and DFS. If you need to access both Blob and File storage, then you must enable resolution for each specific private endpoint.

For more information on the services and DNS resolution, see [Azure Private Endpoint DNS configuration](/azure/private-link/private-endpoint-dns).

## Troubleshooting

If after running through the above steps you're unable to access the workspace from a virtual machine or jobs fail on compute resources in the Virtual Network containing the Private Endpoint to the Azure Machine Learning workspace, follow the below steps to try to identify the cause.

1. **Locate the workspace FQDNs on the Private Endpoint**:

    Navigate to the Azure portal using one of the following links:
    - [Azure Public regions](https://portal.azure.com/?feature.privateendpointmanagedns=false)
    - [Microsoft Azure operated by 21Vianet regions](https://portal.azure.cn/?feature.privateendpointmanagedns=false)
    - [Azure US Government regions](https://portal.azure.us/?feature.privateendpointmanagedns=false)

    Navigate to the Private Endpoint to the Azure Machine Learning workspace. The workspace FQDNs is listed on the "Overview" tab.

1. **Access compute resource in Virtual Network topology**:

    Proceed to access a compute resource in the Azure Virtual Network topology. This likely requires accessing a Virtual Machine in a Virtual Network that is peered with the Hub Virtual Network.

1. **Resolve workspace FQDNs**:

    Open a command prompt, shell, or PowerShell. Then for each of the workspace FQDNs, run the following command:

    `nslookup <workspace FQDN>`

    The result of each nslookup should yield one of the two private IP addresses on the Private Endpoint to the Azure Machine Learning workspace. If it doesn't, then there's something misconfigured in the custom DNS solution.

    Possible causes:
    - The compute resource running the troubleshooting commands isn't using DNS Server for DNS resolution
    - The Private DNS Zones chosen when creating the Private Endpoint aren't linked to the DNS Server virtual network
    - Conditional forwarders from DNS Server to Azure DNS Virtual Server IP weren't configured correctly
    - Conditional forwarders from On-premises DNS Server to DNS Server weren't configured correctly

## Related content

For information on integrating Private Endpoints into your DNS configuration, see [Azure Private Endpoint DNS configuration](/azure/private-link/private-endpoint-dns).
