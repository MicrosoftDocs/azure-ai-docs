---
title: Configure a private endpoint
titleSuffix: Azure Machine Learning
description: 'Use a private endpoint to securely access your Azure Machine Learning workspace from a virtual network.'
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.topic: how-to
ms.author: scottpolly
author: s-polly
ms.reviewer: shshubhe
ms.date: 05/22/2025
ms.custom:
  - devx-track-azurecli
  - sdkv2
  - FY25Q1-Linter
  - ignite-2024
  - sfi-image-nochange
# Customer Intent: As an admin, I want to understand how to use private links to secure communications between my Azure Machine Learning workspace and my virtual network.
---

# Configure a private endpoint for an Azure Machine Learning workspace

[!INCLUDE [CLI v2](includes/machine-learning-cli-v2.md)]


In this document, you learn how to configure a private endpoint for your Azure Machine Learning workspace. For information on creating a virtual network for Azure Machine Learning, see [Virtual network isolation and privacy overview](how-to-network-security-overview.md).

Azure Private Link enables you to restrict connections to your workspace to an Azure Virtual Network. You restrict a workspace to only accept connections from a virtual network by creating a private endpoint. The private endpoint is a set of private IP addresses within your virtual network. You can then limit access to your workspace to only occur over the private IP addresses. A private endpoint helps reduce the risk of data exfiltration. To learn more about private endpoints, see the [Azure Private Link](/azure/private-link/private-link-overview) article.

> [!WARNING]
> Securing a workspace with private endpoints doesn't ensure end-to-end security by itself. You must secure all of the individual components of your solution. For example, if you use a private endpoint for the workspace, but your Azure Storage Account isn't behind the VNet, traffic between the workspace and storage doesn't use the VNet for security.
>
> For more information on securing resources used by Azure Machine Learning, see the following articles:
>
> * [Virtual network isolation and privacy overview](how-to-network-security-overview.md).
> * [Secure workspace resources](how-to-secure-workspace-vnet.md).
> * [Secure training environments](how-to-secure-training-vnet.md).
> * [Secure the inference environment](how-to-secure-inferencing-vnet.md).
> * [Use Azure Machine Learning studio in a VNet](how-to-enable-studio-virtual-network.md).
> * [API platform network isolation](how-to-configure-network-isolation-with-v2.md).

## Prerequisites

* You must have an existing virtual network to create the private endpoint in. 

    > [!WARNING]
    > Don't use the 172.17.0.0/16 IP address range for your VNet. This is the default subnet range used by the Docker bridge network, and results in errors if used for your VNet. Other ranges might also conflict depending on what you want to connect to the virtual network. For example, if you plan to connect your on premises network to the VNet, and your on-premises network also uses the 172.16.0.0/16 range. Ultimately, it's up to __you__ to plan your network infrastructure.

* [Disable network policies for private endpoints](/azure/private-link/disable-private-endpoint-network-policy) before adding the private endpoint.

## Limitations

* If you enable public access for a workspace secured with private endpoint and use Azure Machine Learning studio over the public internet, some features such as the designer might fail to access your data. This problem happens when the data is stored on a service that is secured behind the virtual network. For example, an Azure Storage Account.
* If you're using Mozilla Firefox, you might encounter problems trying to access the private endpoint for your workspace. This problem might be related to DNS over HTTPS in Mozilla Firefox. We recommend using Microsoft Edge or Google Chrome.
* Using a private endpoint doesn't affect Azure control plane (management operations) such as deleting the workspace or managing compute resources. For example, creating, updating, or deleting a compute target. These operations are performed over the public Internet as normal. Data plane operations, such as using Azure Machine Learning studio, APIs (including published pipelines), or the SDK use the private endpoint.
* When you create a compute instance or compute cluster in a workspace with a private endpoint, the compute instance and compute cluster must be in the same Azure region as the workspace.
* If you enable or disable Private Link for an Azure Machine Learning workspace after creating compute resources, those existing computes will not automatically update to reflect the new Private Link configuration. To ensure proper connectivity and avoid service disruptions, you must recreate the compute resources after making any changes to the workspace’s private link setting.
* When you attach an Azure Kubernetes Service cluster to a workspace with a private endpoint, the cluster must be in the same region as the workspace.
* When you use a workspace with multiple private endpoints, one of the private endpoints must be in the same virtual network as the following dependency services:

    * Azure Storage Account that provides the default storage for the workspace
    * Azure Key Vault for the workspace
    * Azure Container Registry for the workspace.

    For example, one virtual network ('services') would contain a private endpoint for the dependency services and the workspace. This configuration allows the workspace to communicate with the services. Another virtual network ('clients') might only contain a private endpoint for the workspace, and be used only for communication between client development machines and the workspace.

## Create a workspace that uses a private endpoint

Use one of the following methods to create a workspace with a private endpoint. Each of these methods __requires an existing virtual network__:

> [!TIP]
> If you'd like to create a workspace, private endpoint, and virtual network at the same time, see [Use an Azure Resource Manager template to create a workspace for Azure Machine Learning](how-to-create-workspace-template.md).

# [Azure CLI](#tab/cli)
[!INCLUDE [CLI v2](includes/machine-learning-cli-v2.md)]

When you use the Azure CLI [extension 2.0 CLI for machine learning](how-to-configure-cli.md), a YAML document is used to configure the workspace. The following example demonstrates creating a new workspace using a YAML configuration:

> [!TIP]
> When you use a private link, your workspace can't use Azure Container Registry tasks compute for image building. Instead, the workspace defaults to using a [serverless compute cluster](how-to-use-serverless-compute.md) to build images. This works only when the workspace-deependent resources such as the storage account and container registry aren't under any network restrictions (private endpoint). If your workspace dependencies are under network restrictions, use the `image_build_compute` property to specify a compute cluster to use for image building.
> The `image_build_compute` property in this configuration specifies a CPU compute cluster name to use for Docker image environment building. You can also specify whether the private link workspace should be accessible over the internet using the `public_network_access` property.
>
> In this example, the compute referenced by `image_build_compute` needs to be created before building images.

:::code language="YAML" source="~/azureml-examples-main/cli/resources/workspace/privatelink.yml":::

```azurecli-interactive
az ml workspace create \
    -g <resource-group-name> \
    --file privatelink.yml
```

After creating the workspace, use the [Azure networking CLI commands](/cli/azure/network/private-endpoint#az-network-private-endpoint-create) to create a private link endpoint for the workspace.

```azurecli-interactive
az network private-endpoint create \
    --name <private-endpoint-name> \
    --vnet-name <vnet-name> \
    --subnet <subnet-name> \
    --private-connection-resource-id "/subscriptions/<subscription>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>" \
    --group-id amlworkspace \
    --connection-name workspace -l <location>
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

# [Portal](#tab/azure-portal)

The __Networking__ tab in Azure Machine Learning portal allows you to configure a private endpoint. However, it requires an existing virtual network. For more information, see [Create workspaces in the portal](how-to-manage-workspace.md).

---

## Add a private endpoint to a workspace

Use one of the following methods to add a private endpoint to an existing workspace:

> [!WARNING]
>
> If you have any existing compute targets associated with this workspace, and they aren't behind the same virtual network that the private endpoint is created in, they won't work.

# [Azure CLI](#tab/cli)
[!INCLUDE [CLI v2](includes/machine-learning-cli-v2.md)]

When using the Azure CLI [extension 2.0 CLI for machine learning](how-to-configure-cli.md), use the [Azure networking CLI commands](/cli/azure/network/private-endpoint#az-network-private-endpoint-create) to create a private link endpoint for the workspace.

```azurecli-interactive
az network private-endpoint create \
    --name <private-endpoint-name> \
    --vnet-name <vnet-name> \
    --subnet <subnet-name> \
    --private-connection-resource-id "/subscriptions/<subscription>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>" \
    --group-id amlworkspace \
    --connection-name workspace -l <location>
```

To create the private DNS zone entries for the workspace, use the following commands:

```azurecli-interactive
# Add privatelink.api.azureml.ms
az network private-dns zone create \
    -g <resource-group-name> \
    --name 'privatelink.api.azureml.ms'

az network private-dns link vnet create \
    -g <resource-group-name> \
    --zone-name 'privatelink.api.azureml.ms' \
    --name <link-name> \
    --virtual-network <vnet-name> \
    --registration-enabled false

az network private-endpoint dns-zone-group create \
    -g <resource-group-name> \
    --endpoint-name <private-endpoint-name> \
    --name myzonegroup \
    --private-dns-zone 'privatelink.api.azureml.ms' \
    --zone-name 'privatelink.api.azureml.ms'

# Add privatelink.notebooks.azure.net
az network private-dns zone create \
    -g <resource-group-name> \
    --name 'privatelink.notebooks.azure.net'

az network private-dns link vnet create \
    -g <resource-group-name> \
    --zone-name 'privatelink.notebooks.azure.net' \
    --name <link-name> \
    --virtual-network <vnet-name> \
    --registration-enabled false

az network private-endpoint dns-zone-group add \
    -g <resource-group-name> \
    --endpoint-name <private-endpoint-name> \
    --name myzonegroup \
    --private-dns-zone 'privatelink.notebooks.azure.net' \
    --zone-name 'privatelink.notebooks.azure.net'
```

# [Portal](#tab/azure-portal)

From the Azure Machine Learning workspace in the portal, select __Settings__, __Networking__, __Private endpoint connections__ and then select __+ Private endpoint__. Use the fields to create a new private endpoint.

* When selecting the __Region__, select the same region as your virtual network. 
* When selecting the __Virtual network__, select the virtual network you want to connect to.
* When selecting the __Subnet__, select the subnet in the virtual network that the private endpoint IP addresses are assigned from.

You can leave other fields at the default value or modify as needed for your environment. Finally, select __Create__ to create the private endpoint.

---

## Remove a private endpoint

You can remove one or all private endpoints for a workspace. Removing a private endpoint removes the workspace from the virtual network that the endpoint was associated with. Removing the private endpoint might prevent the workspace from accessing resources in that virtual network, or resources in the virtual network from accessing the workspace. For example, if the virtual network doesn't allow access to or from the public internet.

> [!WARNING]
> Removing the private endpoints for a workspace __doesn't make it publicly accessible__. To make the workspace publicly accessible, use the steps in the [Enable public access](#enable-public-access) section.

To remove a private endpoint, use the following information:

# [Azure CLI](#tab/cli)
[!INCLUDE [CLI v2](includes/machine-learning-cli-v2.md)]


When using the Azure CLI [extension 2.0 CLI for machine learning](how-to-configure-cli.md), use the following command to remove the private endpoint:

```azurecli
az network private-endpoint delete \
    --name <private-endpoint-name> \
    --resource-group <resource-group-name> \
```

# [Portal](#tab/azure-portal)

1. From the [Azure portal](https://portal.azure.com), select your Azure Machine Learning workspace.
1. From the left side of the page, select __Networking__ and then select the __Private endpoint connections__ tab.
1. Select the endpoint to remove and then select __Remove__.

:::image type="content" source="./media/how-to-configure-private-link/remove-private-endpoint.png" alt-text="Screenshot of the UI to remove a private endpoint.":::

---

## Enable public access

In some situations, you might want to allow someone to connect to your secured workspace over a public endpoint, instead of through the virtual network. Or you might want to remove the workspace from the virtual network and re-enable public access.

> [!IMPORTANT]
> Enabling public access doesn't remove any private endpoints that exist. All communications between components behind the VNet that the private endpoint(s) connect to are still secured. It enables public access only to the workspace, in addition to the private access through any private endpoints.

> [!WARNING]
> When connecting over the public endpoint while the workspace uses a private endpoint to communicate with other resources:
> * __Some features of studio will fail to access your data__. This problem happens when the _data is stored on a service that is secured behind the VNet_. For example, an Azure Storage Account. To resolve this problem, add your client device's IP address to the [Azure Storage Account's firewall](/azure/storage/common/storage-network-security?toc=%2fazure%2fstorage%2fblobs%2ftoc.json#grant-access-from-an-internet-ip-range).
> * Using Jupyter, JupyterLab, RStudio, or Posit Workbench (formerly RStudio Workbench) on a compute instance, including running notebooks, __is not supported__.

To enable public access, use the following steps:

> [!TIP]
> There are two possible properties that you can configure:
> * `allow_public_access_when_behind_vnet` - used by the Python SDK v1
> * `public_network_access` - used by the CLI and Python SDK v2
> Each property overrides the other. For example, setting `public_network_access` overrides any previous setting to `allow_public_access_when_behind_vnet`.
>
> Microsoft recommends using `public_network_access` to enable or disable public access to a workspace.

# [Azure CLI](#tab/cli)
[!INCLUDE [CLI v2](includes/machine-learning-cli-v2.md)]


When using the Azure CLI [extension 2.0 CLI for machine learning](how-to-configure-cli.md), use the `az ml update` command to enable `public_network_access` for the workspace:

```azurecli
az ml workspace update \
    --set public_network_access=Enabled \
    -n <workspace-name> \
    -g <resource-group-name>
```

You can also enable public network access by using a YAML file. For more information, see the [workspace YAML reference](reference-yaml-workspace.md).

# [Portal](#tab/azure-portal)

1. From the [Azure portal](https://portal.azure.com), select your Azure Machine Learning workspace.
1. From the left side of the page, select __Networking__ and then select the __Public access__ tab.
1. Select __Enabled from all networks__, and then select __Save__.

:::image type="content" source="./media/how-to-configure-private-link/workspace-public-access.png" alt-text="Screenshot of the UI to enable public endpoint.":::

---

## Enable Public Access only from internet IP ranges

You can use IP network rules to allow access to your workspace and endpoint from specific public internet IP address ranges by creating IP network rules. Each Azure Machine Learning workspace supports up to 200 rules. These rules grant access to specific internet-based services and on-premises networks and block general internet traffic.

> [!IMPORTANT]
> * Before creating a compute instance in an Azure Machine Learning workspace with a selected IP address, ensure that your workspace has network isolation configured using a [workspace-managed virtual network](how-to-managed-network.md) OR [Add a private endpoint to your workspace in your own virtual network](how-to-configure-private-link.md#add-a-private-endpoint-to-a-workspace).
> * Configuring only the selected IP without enabling a managed virtual network or a Private endpoint for the workspace can lead to failures while provisioning the compute instance.

> [!WARNING]
> * Enable your endpoint's [public network access flag](concept-secure-online-endpoint.md#secure-inbound-scoring-requests) if you want to allow access to your endpoint from specific public internet IP address ranges.
> * You can only use IPv4 addresses.
> * To use this feature with Azure Machine Learning managed virtual network, see [Azure Machine Learning managed virtual network](how-to-managed-network.md#scenario-enable-access-from-selected-ip-addresses).

# [Azure CLI](#tab/cli)
[!INCLUDE [CLI v2](includes/machine-learning-cli-v2.md)]

Use the `az ml workspace network-rule` Azure CLI command to manage public access from an IP address or address range:

> [!TIP]
> The configurations for the selected IP addresses are stored in the workspace's properties, under `network_acls`:
> ```yml
> properties:
>   # ...
>   network_acls:
>     description: "The network ACLS for this workspace, enforced when public_network_access is set to Enabled."
>     $ref: "3/defintions/networkAcls"
> ```

- __List IP network rules__: `az ml workspace network-rule list --resource-group "myresourcegroup" --workspace-name "myWS" --query ipRules`
- __Add a rule for a single IP address__: `az ml workspace network-rule add --resource-group "myresourcegroup" --workspace-name "myWS" --ip-address "16.17.18.19"`
- __Add a rule for an IP address range__: `az ml workspace network-rule add --resource-group "myresourcegroup" --workspace-name "myWS" --ip-address "16.17.18.0/24"`
- __Remove a rule for a single IP address__: `az ml workspace network-rule remove --resource-group "myresourcegroup" --workspace-name "myWS" --ip-address "16.17.18.19"`
- __Remove a rule for an IP address range__: `az ml workspace network-rule remove --resource-group "myresourcegroup" --workspace-name "myWS" --ip-address "16.17.18.0/24"`

# [Portal](#tab/azure-portal)

1. From the [Azure portal](https://portal.azure.com), select your Azure Machine Learning workspace.
1. From the left side of the page, select __Networking__ and then select the __Public access__ tab.
1. Select __Enabled from selected IP addresses__, input address ranges and then select __Save__.

:::image type="content" source="./media/how-to-configure-private-link/workspace-public-access-ip-ranges.png" alt-text="Screenshot of the UI to enable access from internet IP ranges.":::

---

You can also use the [Workspace](/python/api/azure-ai-ml/azure.ai.ml.entities.workspace) class from the Azure Machine Learning [Python SDK](/python/api/overview/azure/ai-ml-readme) to define which IP addresses are allowed inbound access:

```python
Workspace( 
  public_network_access = "Enabled", 
  network_rule_set = NetworkRuleSet(default_action = "Allow", bypass = "AzureServices", resource_access_rules = None, ip_rules = yourIPAddress,)
```

### Restrictions for IP network rules

The following restrictions apply to IP address ranges:

- IP network rules are allowed only for _public internet_ IP addresses.

  [Reserved IP address ranges](https://en.wikipedia.org/wiki/Reserved_IP_addresses) aren't allowed in IP rules such as private addresses that start with 10, 172.16 to 172.31, and 192.168.

- You must provide allowed internet address ranges by using [CIDR notation](https://tools.ietf.org/html/rfc4632) in the form 16.17.18.0/24 or as individual IP addresses like 16.17.18.19.

- Only IPv4 addresses are supported for configuration of storage firewall rules.

- When this feature is enabled, you can test public endpoints using any client tool such as Curl, but the Endpoint Test tool in the portal isn't supported.

- You can only set the IP addresses for the workspace after the workspace has been created.

- Managed online endpoint deployments will fail if the workspace managed virtual network is not enabled on the workspace, alongside enable from selected IPs workspace. Training compute targets, including compute clusters, comptue instance, and serverless compute, in the workspace without end-to-end network isolation will not work alongside enable from selected IPs workspace. Network isolated training the previously mentioned computes require a private endpoint from compute network to the workspace with the enable from selected IPs workspace. 

## Securely connect to your workspace

[!INCLUDE [machine-learning-connect-secure-workspace](includes/machine-learning-connect-secure-workspace.md)]

## Multiple private endpoints

Azure Machine Learning supports multiple private endpoints for a workspace. Multiple private endpoints are often used when you want to keep different environments separate. The following are some scenarios that are enabled by using multiple private endpoints:

* Client development environments in a separate virtual network.
* An Azure Kubernetes Service (AKS) cluster in a separate virtual network.
* Other Azure services in a separate virtual network. For example, Azure Synapse and Azure Data Factory can use a Microsoft managed virtual network. In either case, a private endpoint for the workspace can be added to the managed virtual network used by those services. For more information on using a managed virtual network with these services, see the following articles:

    * [Synapse managed private endpoints](/azure/synapse-analytics/security/synapse-workspace-managed-private-endpoints)
    * [Azure Data Factory managed virtual network](/azure/data-factory/managed-virtual-network-private-endpoint).

    > [!IMPORTANT]
    > [Synapse's data exfiltration protection](/azure/synapse-analytics/security/workspace-data-exfiltration-protection) isn't supported with Azure Machine Learning.

> [!IMPORTANT]
> Each VNet that contains a private endpoint for the workspace must also be able to access the Azure Storage Account, Azure Key Vault, and Azure Container Registry used by the workspace. For example, you might create a private endpoint for the services in each VNet.

Adding multiple private endpoints uses the same steps as described in the [Add a private endpoint to a workspace](#add-a-private-endpoint-to-a-workspace) section.

### Scenario: Isolated clients

If you want to isolate the development clients, so they don't have direct access to the compute resources used by Azure Machine Learning, use the following steps:

> [!NOTE]
> These steps assume that you have an existing workspace, Azure Storage Account, Azure Key Vault, and Azure Container Registry. Each of these services has a private endpoints in an existing VNet.

1. Create another virtual network for the clients. This virtual network might contain Azure Virtual Machines that act as your clients, or it might contain a VPN Gateway used by on-premises clients to connect to the virtual network.
1. Add a new private endpoint for the Azure Storage Account, Azure Key Vault, and Azure Container Registry used by your workspace. These private endpoints should exist in the client virtual network.
1. If you have another storage that is used by your workspace, add a new private endpoint for that storage. The private endpoint should exist in the client virtual network and have private DNS zone integration enabled.
1. Add a new private endpoint to your workspace. This private endpoint should exist in the client virtual network and have private DNS zone integration enabled.
1. To enable Azure Machine Learning studio to access the storage accounts, visit the [studio in a virtual network](how-to-enable-studio-virtual-network.md#datastore-azure-storage-account) article.

The following diagram illustrates this configuration. The __Workload__ virtual network contains compute resources created by the workspace for training & deployment. The __Client__ virtual network contains clients or client ExpressRoute/VPN connections. Both VNets contain private endpoints for the workspace, Azure Storage Account, Azure Key Vault, and Azure Container Registry.

:::image type="content" source="./media/how-to-configure-private-link/multiple-private-endpoint-workspace-client.png" alt-text="Diagram of isolated client VNet":::

### Scenario: Isolated Azure Kubernetes Service

If you want to create an isolated Azure Kubernetes Service used by the workspace, use the following steps:

> [!NOTE]
> These steps assume that you have an existing workspace, Azure Storage Account, Azure Key Vault, and Azure Container Registry. Each of these services has a private endpoints in an existing VNet.

1. Create an Azure Kubernetes Service instance. During creation, AKS creates a virtual network that contains the AKS cluster.
1. Add a new private endpoint for the Azure Storage Account, Azure Key Vault, and Azure Container Registry used by your workspace. These private endpoints should exist in the client virtual network.
1. If you have other storage that is used by your workspace, add a new private endpoint for that storage. The private endpoint should exist in the client virtual network and have private DNS zone integration enabled.
1. Add a new private endpoint to your workspace. This private endpoint should exist in the client virtual network and have private DNS zone integration enabled.
1. Attach the AKS cluster to the Azure Machine Learning workspace. For more information, see [Create and attach an Azure Kubernetes Service cluster](how-to-create-attach-kubernetes.md#attach-an-existing-aks-cluster).

:::image type="content" source="./media/how-to-configure-private-link/multiple-private-endpoint-workspace-aks.png" alt-text="Diagram of isolated AKS VNet":::

### Scenario: Managed online endpoints with access from selected IP addresses

Enabling inbound access from selected IP addresses is affected by the ingress setting on your managed online endpoints. The following table shows the possible configurations for your workspace and managed online endpoint network configurations, and how it affects both. For more information, see [Network isolation with managed online endpoints](concept-secure-online-endpoint.md).

| Workspace</br>public network access | Managed online endpoint</br>public network access | Does the workspace</br>respect the selected IPs? | Does the online endpoint</br>respect the selected IPs? |
| --- | --- | --- | --- |
| Disabled | Disabled | No (all public traffic rejected) | No |
| Disabled | Enabled | No (all public traffic rejected) | Not supported |
| Enabled from selected IPs | Disabled | Yes | No |
| Enabled from selected IPs | Enabled | Yes | Yes |

> [!NOTE]
> If the workspace public network access configuration is changed from selected IPs to disabled, the managed online enedpoints continue to respect the selected IPs. If you don't want the selected IPs applied to your online endpoints, remove the addresses before selecting __Disabled__ for the workspace in the Azure portal. The Python SDK and Azure CLI support this change after or before.

### Scenario: Batch endpoints with access from selected IP addresses

The selected IP's configuration isn't supported for batch endpoints. There's no public network access flag on batch endpoints. If the Azure Machine Learning workspace is disabled, and private link enabled, the batch endpoint is private as well. If the workspace's public network access is changed from disabled to enabled, the batch endpoints stay private and don't become public. For more information, see [Securing batch endpoints](/azure/machine-learning/how-to-secure-batch-endpoint#securing-batch-endpoints).

## Related content

* [Virtual network isolation and privacy overview](how-to-network-security-overview.md)

* [How to use a workspace with a custom DNS server](how-to-custom-dns.md)

* [API platform network isolation](how-to-configure-network-isolation-with-v2.md)
