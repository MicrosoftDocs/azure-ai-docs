---

title: How to configure a private link for an Azure AI Foundry hub
titleSuffix: Azure AI Foundry
description: Learn how to configure a private link for Azure AI Foundry hubs. A private link is used to secure communication with the Azure AI Foundry hub.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: ignite-2023, devx-track-azurecli, build-2024, ignite-2024
ms.topic: how-to
ms.date: 05/06/2025
ms.reviewer: meerakurup
ms.author: larryfr
author: Blackmist
zone_pivot_groups: project-type
# Customer intent: As an admin, I want to configure a private link for hub so that I can secure my hubs.

---

# How to configure a private link for Azure AI Foundry

:::zone pivot="fdp-project"

When using a [!INCLUDE [fdp-projects](../includes/fdp-project-name.md)], you can use a private link to secure communication with your project. This article describes how to establish a private connection to your project using a private link.

:::zone-end

:::zone pivot="hub-project"

When using a [!INCLUDE [hub-projects](../includes/hub-project-name.md)], there are two network isolation aspects to consider:

- **Network isolation to access an Azure AI Foundry hub**: This is the focus of this article. It describes how to establish a private connection to your hub and its default resources using a private link.
- **Network isolation of computing resources in your hub and projects**: This includes compute instances, serverless, and managed online endpoints. For more information, see the [Configure managed networks for Azure AI Foundry hubs](configure-managed-network.md) article.

:::image type="content" source="../media/how-to/network/azure-ai-network-inbound.svg" alt-text="Diagram of Azure AI Foundry hub network isolation." lightbox="../media/how-to/network/azure-ai-network-inbound.png":::

You get several hub default resources in your resource group. You need to configure following network isolation configurations:

- Disable public network access of hub default resources such as Azure Storage, Azure Key Vault, and Azure Container Registry.
- Establish private endpoint connection to hub default resources. You need to have both a blob and file private endpoint for the default storage account.
- If your storage account is private, [assign roles](#private-storage-configuration) to allow access.

:::zone-end

## Prerequisites

* You must have an existing Azure Virtual Network to create the private endpoint in. 

    > [!IMPORTANT]
    > We don't recommend using the 172.17.0.0/16 IP address range for your VNet. This is the default subnet range used by the Docker bridge network on-premises.

* Disable network policies for private endpoints before adding the private endpoint.

:::zone pivot="fdp-project"

## Create a Foundry project that uses a private endpoint

When creating a new project, use the following steps to create the project.

1. From the [Azure portal](https://portal.azure.com), search for __Azure AI Foundry__ and select __Create a resource__.
1. After configuring the __Basics__ tab, select the __Networking__ tab and then the __Disabled__ option.
1. From the __Private endpoint__ section, select __+ Add private endpoint__.
1. When going through the forms to create a private endpoint, be sure to:

    - From __Basics__, select the same __Region__ as your virtual network.
    - From the __Virtual Network__ form, select the virtual network and subnet that you want to connect to.

1. Continue through the forms to create the project. When you reach the __Review + create__ tab, review your settings and select __Create__ to create the project.

:::zone-end

:::zone pivot="hub-project"

## Create a hub that uses a private endpoint

If you're creating a new hub, use the following methods to create the hub (Azure portal or Azure CLI). Each of these methods __requires an existing virtual network__:

# [Azure portal](#tab/azure-portal)

> [!NOTE]
> The information in this document is only about configuring a private link. For a walkthrough of creating a secure hub in the portal, see [Create a secure hub in the Azure portal](create-secure-ai-hub.md).

1. From the [Azure portal](https://portal.azure.com), search for __Azure AI Foundry__ and create a new resource by selecting __+ New Azure AI__.
1. After configuring the __Basics__ and __Storage__ tabs, select the __Inbound access__ tab and then select __+ Add__. When prompted, enter the data for the Azure Virtual Network and subnet for the private endpoint. When selecting the __Region__, select the same region as your virtual network.

    :::image type="content" source="../media/how-to/network/inbound-access.png" alt-text="Screenshot of the inbound access tab with public network access disabled." lightbox="../media/how-to/network/inbound-access.png":::

1. Select the __Outbound access__ tab and pick the __Network isolation__ option that best suits your needs.

    :::image type="content" source="../media/how-to/network/outbound-access.png" alt-text="Screenshot of the Create a hub with the option to set network isolation information." lightbox="../media/how-to/network/outbound-access.png":::


# [Azure CLI](#tab/cli)

> [!NOTE]
> The information in this section doesn't cover basic hub configuration. For more information, see [Create a hub using the Azure CLI](./develop/create-hub-project-sdk.md?tabs=azurecli).

After creating the hub, use the [Azure networking CLI commands](/cli/azure/network/private-endpoint#az-network-private-endpoint-create) to create a private link endpoint for the hub.

```azurecli-interactive
az network private-endpoint create \
    --name <private-endpoint-name> \
    --vnet-name <vnet-name> \
    --subnet <subnet-name> \
    --private-connection-resource-id "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>" \
    --group-id amlworkspace \
    --connection-name workspace \
    --location <location> \
    --resource-group <resource-group-name>
```

To create the private DNS zone entries for the workspace, use the following commands:

```azurecli-interactive
# Add privatelink.api.azureml.ms
az network private-dns zone create \
    -g <resource-group-name> \
    --name privatelink.api.azureml.ms

az network private-dns link vnet create \
    -g <resource-group-name> \
    --zone-name privatelink.api.azureml.ms \
    --name <link-name> \
    --virtual-network <vnet-name> \
    --registration-enabled false

az network private-endpoint dns-zone-group create \
    -g <resource-group-name> \
    --endpoint-name <private-endpoint-name> \
    --name myzonegroup \
    --private-dns-zone privatelink.api.azureml.ms \
    --zone-name privatelink.api.azureml.ms
```

---

:::zone-end

:::zone pivot="fdp-project"

## Add a private endpoint to a project

1. From the [Azure portal](https://portal.azure.com), select your project.
1. From the left side of the page, select __Resource Management__, __Networking__, and then select the __Private endpoint connections__ tab. Select __+ Private endpoint__.
1. When going through the forms to create a private endpoint, be sure to:

    - From __Basics__, select the same __Region__ as your virtual network.
    - From the __Virtual Network__ form, select the virtual network and subnet that you want to connect to.

1. After populating the forms with any other network configurations you require, use the __Review + create__ tab to review your settings and select __Create__ to create the private endpoint.

:::zone-end

:::zone pivot="hub-project"

## Add a private endpoint to a hub

Use one of the following methods to add a private endpoint to an existing hub:

# [Azure portal](#tab/azure-portal)

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Settings__, __Networking__, and then select the __Private endpoint connections__ tab. Select __+ Private endpoint__.

    :::image type="content" source="../media/how-to/network/add-private-endpoint.png" alt-text="Screenshot of the private endpoint connections tab":::

1. When going through the forms to create a private endpoint, be sure to:

    - From __Basics__, select the same __Region__ as your virtual network.
    - From __Resource__, select `amlworkspace` as the __target sub-resource__.
    - From the __Virtual Network__ form, select the virtual network and subnet that you want to connect to.
 
1. After populating the forms with any other network configurations you require, use the __Review + create__ tab to review your settings and select __Create__ to create the private endpoint.

# [Azure CLI](#tab/cli)

Use the [Azure networking CLI commands](/cli/azure/network/private-endpoint#az-network-private-endpoint-create) to create a private link endpoint for the hub.

```azurecli-interactive
az network private-endpoint create \
    --name <private-endpoint-name> \
    --vnet-name <vnet-name> \
    --subnet <subnet-name> \
    --private-connection-resource-id "/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>" \
    --group-id amlworkspace \
    --connection-name workspace \
    --location <location> \
    --resource-group <resource-group-name>
```

To create the private DNS zone entries for the workspace, use the following commands:

```azurecli-interactive
# Add privatelink.api.azureml.ms
az network private-dns zone create \
    -g <resource-group-name> \
    --name privatelink.api.azureml.ms

az network private-dns link vnet create \
    -g <resource-group-name> \
    --zone-name privatelink.api.azureml.ms \
    --name <link-name> \
    --virtual-network <vnet-name> \
    --registration-enabled false

az network private-endpoint dns-zone-group create \
    -g <resource-group-name> \
    --endpoint-name <private-endpoint-name> \
    --name myzonegroup \
    --private-dns-zone privatelink.api.azureml.ms \
    --zone-name privatelink.api.azureml.ms

# Add privatelink.notebooks.azure.net
az network private-dns zone create \
    -g <resource-group-name> \
    --name privatelink.notebooks.azure.net

az network private-dns link vnet create \
    -g <resource-group-name> \
    --zone-name privatelink.notebooks.azure.net \
    --name <link-name> \
    --virtual-network <vnet-name> \
    --registration-enabled false

az network private-endpoint dns-zone-group add \
    -g <resource-group-name> \
    --endpoint-name <private-endpoint-name> \
    --name myzonegroup \
    --private-dns-zone privatelink.notebooks.azure.net \
    --zone-name privatelink.notebooks.azure.net
```

---

:::zone-end

:::zone pivot="fdp-project"

## Remove a private endpoint from a project

You can remove one or all private endpoints for a project. Removing a private endpoint removes the project from the Azure Virtual Network that the endpoint was associated with. Removing the private endpoint might prevent the project from accessing resources in that virtual network, or resources in the virtual network from accessing the workspace. For example, if the virtual network doesn't allow access to or from the public internet.

> [!WARNING]
> Removing the private endpoints for a project __doesn't make it publicly accessible__. To make the project publicly accessible, use the steps in the [Enable public access](#enable-public-access) section.

To remove a private endpoint, use the following information:

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Resource Management__, __Networking__, and then select the __Private endpoint connections__ tab.
1. Select the endpoint to remove and then select __Remove__.

:::zone-end

:::zone pivot="hub-project"

## Remove a private endpoint

You can remove one or all private endpoints for a hub. Removing a private endpoint removes the hub from the Azure Virtual Network that the endpoint was associated with. Removing the private endpoint might prevent the hub from accessing resources in that virtual network, or resources in the virtual network from accessing the workspace. For example, if the virtual network doesn't allow access to or from the public internet.

> [!WARNING]
> Removing the private endpoints for a hub __doesn't make it publicly accessible__. To make the hub publicly accessible, use the steps in the [Enable public access](#enable-public-access) section.

To remove a private endpoint, use the following information:

# [Azure portal](#tab/azure-portal)

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Settings__, __Networking__, and then select the __Private endpoint connections__ tab.
1. Select the endpoint to remove and then select __Remove__.

    :::image type="content" source="../media/how-to/network/remove-private-endpoint.png" alt-text="Screenshot of a selected private endpoint with the remove option highlighted.":::

# [Azure CLI](#tab/cli)

When using the Azure CLI, use the following command to remove the private endpoint:

```azurecli
az network private-endpoint delete \
    --name <private-endpoint-name> \
    --resource-group <resource-group-name>
```

---

:::zone-end

:::zone pivot="fdp-project"

## Enable public access

In some situations, you might want to allow someone to connect to your secured project over a public endpoint, instead of through the virtual network. Or you might want to remove the project from the virtual network and re-enable public access.

> [!IMPORTANT]
> Enabling public access doesn't remove any private endpoints that exist. All communications between components behind the virtual network that the private endpoint(s) connect to are still secured. It enables public access only to the project, in addition to the private access through any private endpoints.

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Resource Management__, __Networking__, and then select the __Firewalls and virtual networks__ tab.
1. Select __All networks__, and then select __Save__.

:::zone-end

:::zone pivot="hub-project"

## Enable public access

In some situations, you might want to allow someone to connect to your secured hub over a public endpoint, instead of through the virtual network. Or you might want to remove the workspace from the virtual network and re-enable public access.

> [!IMPORTANT]
> Enabling public access doesn't remove any private endpoints that exist. All communications between components behind the virtual network that the private endpoint(s) connect to are still secured. It enables public access only to the hub, in addition to the private access through any private endpoints.

To enable public access, use the following steps:

# [Azure portal](#tab/azure-portal)

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Networking__ and then select the __Public access__ tab.
1. Select __Enabled from all networks__, and then select __Save__.

# [Azure CLI](#tab/cli)

Use the following Azure CLI command to enable public access:

```azurecli
az ml workspace update --set public_network_access=Enabled -n <workspace-name> -g <resource-group-name>
```

If you receive an error that the `ml` command isn't found, use the following commands to install the Azure Machine Learning CLI extension:

```azurecli
az extension add --name ml
```

---

## Enable Public Access only from internet IP ranges (preview)

You can use IP network rules to allow access to your secured hub from specific public internet IP address ranges by creating IP network rules. Each Azure AI Foundry hub supports up to 200 rules. These rules grant access to specific internet-based services and on-premises networks and block general internet traffic. This feature is currently in preview.

> [!WARNING]
> * Enable your endpoint's public network access flag if you want to allow access to your endpoint from specific public internet IP address ranges.
> * You can only use IPv4 addresses.
> * If the workspace goes from __Enable from selected IPs__ to __Disabled__ or __Enabled__, the IP ranges are reset.

# [Portal](#tab/azure-portal)

1. From the [Azure portal](https://portal.azure.com), select your Azure Machine AI Foundry hub.
1. From the left side of the page, select __Networking__ and then select the __Public access__ tab.
1. Select __Enabled from selected IP addresses__, input address ranges and then select __Save__.


# [Azure CLI](#tab/cli)

Use the `az ml workspace update` Azure CLI command to manage public access from an IP address or address range:

> [!TIP]
> The configurations for the selected IP addresses are stored in the hub's properties, under `network_acls`:
> ```yml
> name: sample_hub
> location: centraluseuap
> display_name: sample hub
> description: desc
> public_network_access: enabled
> network_acls:
>     ip_rules:
>         value: "X.X.X.X/X"
>         value: "X.X.X.X"
>     default_action: Deny
> ```
 
1. Disabled:
`az ml workspace update -n test-ws -g test-rg --public-network-access Disabled`
1. Enabled from selected IP addresses: 
`az ml workspace update -n test-ws -g test-rg --public-network-access Enabled --network-acls "167.220.238.199/32,167.220.238.194/32" `
1. Enabled from all networks: 
`az ml workspace update -n test-ws -g test-rg --public-network-access Enabled --network-acls none`

---

You can also use the [Workspace](/python/api/azure-ai-ml/azure.ai.ml.entities.workspace) class from the Azure Machine Learning [Python SDK](/python/api/azure-ai-ml/azure.ai.ml.entities.networkacls) to define which IP addresses are allowed inbound access:

```python
class Workspace(Resource):
    """Azure ML workspace.
    :param public_network_access: Whether to allow public endpoint connectivity
        when a workspace is private link enabled.
    :type public_network_access: str
    :param network_acls: The network access control list (ACL) settings of the workspace.
    :type network_acls: ~azure.ai.ml.entities.NetworkAcls
 
    def __init__(
        self,
        *,
        public_network_access: Optional[str] = None,
        network_acls: Optional[NetworkAcls] = None,
```

### Restrictions for IP network rules

The following restrictions apply to IP address ranges:

- IP network rules are allowed only for _public internet_ IP addresses.

  [Reserved IP address ranges](https://en.wikipedia.org/wiki/Reserved_IP_addresses) aren't allowed in IP rules such as private addresses that start with 10, 172.16 to 172.31, and 192.168.

- You must provide allowed internet address ranges by using [CIDR notation](https://tools.ietf.org/html/rfc4632) in the form 16.17.18.0/24 or as individual IP addresses like 16.17.18.19.

- Only IPv4 addresses are supported for configuration of storage firewall rules.

- When this feature is enabled, you can test public endpoints using any client tool such as Curl, but the Endpoint Test tool in the portal isn't supported.

- You can only set the IP addresses for the AI Foundry hub after the hub is created.

## Private storage configuration

If your storage account is private (uses a private endpoint to communicate with your project), you perform the following steps:

1. Our services need to read/write data in your private storage account using [Allow Azure services on the trusted services list to access this storage account](/azure/storage/common/storage-network-security#grant-access-to-trusted-azure-services) with following managed identity configurations. Enable the system assigned managed identity of Azure AI Service and Azure AI Search, then configure role-based access control for each managed identity.

    | Role | Managed Identity | Resource | Purpose | Reference |
    |--|--|--|--|--|
    | `Reader` | Azure AI Foundry project | Private endpoint of the storage account | Read data from the private storage account. | 
    | `Storage File Data Privileged Contributor` | Azure AI Foundry project | Storage Account | Read/Write prompt flow data. | [Prompt flow doc](/azure/machine-learning/prompt-flow/how-to-secure-prompt-flow#secure-prompt-flow-with-workspace-managed-virtual-network) |
    | `Storage Blob Data Contributor` | Azure AI Service | Storage Account | Read from input container, write to preprocess result to output container. | [Azure OpenAI Doc](../../ai-services/openai/how-to/managed-identity.md) |
    | `Storage Blob Data Contributor` | Azure AI Search | Storage Account | Read blob and write knowledge store | [Search doc](/azure/search/search-howto-managed-identities-data-sources). |

    > [!TIP]
    > Your storage account might have multiple private endpoints. You need to assign the `Reader` role to each private endpoint for your Azure AI Foundry project managed identity.

1. Assign the `Storage Blob Data reader` role to your developers. This role allows them to read data from the storage account.

1. Verify that the project's connection to the storage account uses Microsoft Entra ID for authentication. To view the connection information, go to the __Management center__, select __Connected resources__, and then select the storage account connections. If the credential type isn't Entra ID, select the pencil icon to update the connection and set the __Authentication method__ to __Microsoft Entra ID__.

For information on securing playground chat, see [Securely use playground chat](secure-data-playground.md).

:::zone-end

::: zone pivot="fdp-project"

## End-to-end secured networking for Agent Service

When creating a Foundry resource and [!INCLUDE [fdp-projects](../includes/fdp-project-name.md)] to build Agents, we recommend the following network architecture for the most secure end-to-end configuration:

:::image type="content" source="../media/how-to/network/network-diagram-agents.png" alt-text="Diagram of the recommended network isolation for AI Foundry projects and agents." lightbox="../media/how-to/network/network-diagram-agents.png":::

1. Set the public network access (PNA) flag of each of your resources to `Disabled`. Disabling public network access locks down inbound access from the public internet to the resources.
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

::: zone-end

## DNS configuration

::: zone pivot="fdp-project"

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

::: zone-end

::: zone pivot="hub-project"

See [Azure Machine Learning custom DNS](/azure/machine-learning/how-to-custom-dns#example-custom-dns-server-hosted-in-vnet) article for the DNS forwarding configurations.

If you need to configure custom DNS server without DNS forwarding, use the following patterns for the required A records.

* `<AI-HUB-GUID>.workspace.<region>.cert.api.azureml.ms`
* `<AI-HUB-GUID>.workspace.<region>.api.azureml.ms`
* `ml-<workspace-name, truncated>-<region>-<AI-HUB-GUID>.<region>.notebooks.azure.net`

    > [!NOTE]
    > The workspace name for this FQDN might be truncated. Truncation is done to keep `ml-<workspace-name, truncated>-<region>-<workspace-guid>` at 63 characters or less.
* `<instance-name>.<region>.instances.azureml.ms`

    > [!NOTE]
    > * Compute instances can be accessed only from within the virtual network.
    > * The IP address for this FQDN is **not** the IP of the compute instance. Instead, use the private IP address of the workspace private endpoint (the IP of the `*.api.azureml.ms` entries.)

* `<instance-name>-22.<region>.instances.azureml.ms` - Only used by the `az ml compute connect-ssh` command to connect to computers in a managed virtual network. Not needed if you aren't using a managed network or SSH connections.

* `<managed online endpoint name>.<region>.inference.ml.azure.com` - Used by managed online endpoints
* `models.ai.azure.com` - Used for deploying Models as a Service

To find the private IP addresses for your A records, see the [Azure Machine Learning custom DNS](/azure/machine-learning/how-to-custom-dns#find-the-ip-addresses) article.

> [!NOTE]
> Project workspaces reuse the FQDNs of the associated hub workspaces. There's no reason to configure separate entries for the project workspace GUIDs.

::: zone-end

## Limitations

:::zone pivot="hub-project"

* You might encounter problems trying to access the private endpoint for your hub if you're using Mozilla Firefox. This problem might be related to DNS over HTTPS in Mozilla Firefox. We recommend using Microsoft Edge or Google Chrome.

:::zone-end

:::zone pivot="fdp-project"

- A network-secured Agent (bring your own virtual network) is only supported through Bicep template deployment. For more information on network-secured Agent deployment, see [How to use a virtual network with the Azure AI Agent Service](/azure/ai-services/agents/how-to/virtual-networks). 
- A network-secured Agent to be deployed is only a Standard Agent, not a Light Agent. 
- There's no managed virtual network support for the Agent Service or [!INCLUDE [FDP](../includes/fdp-project-name.md)].

:::zone-end

## Next steps

- [Create an Azure AI Foundry project](create-projects.md)
- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)
- [Learn more about Azure AI Foundry hubs](../concepts/ai-resources.md)
- [Troubleshoot secure connectivity to a project](troubleshoot-secure-connection-project.md)
