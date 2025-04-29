---
title: How to configure a private link for an Azure AI Foundry hub
titleSuffix: Azure AI Foundry
description: Learn how to configure a private link for Azure AI Foundry hubs. A private link is used to secure communication with the Azure AI Foundry hub.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: ignite-2023, devx-track-azurecli, build-2024, ignite-2024
ms.topic: how-to
ms.date: 01/15/2025
ms.reviewer: meerakurup
ms.author: larryfr
author: Blackmist
zone_pivot_groups: azure-portal-and-cli
# Customer intent: As an admin, I want to configure a private link for hub so that I can secure my hubs.
---

# How to configure a private link for Azure AI Foundry hubs

We have two network isolation aspects. One is the network isolation to access an [Azure AI Foundry](https://ai.azure.com) hub. Another is the network isolation of computing resources in your hub and projects such as compute instances, serverless, and managed online endpoints. This article explains the former highlighted in the diagram. You can use private link to establish the private connection to your hub and its default resources. This article is for Azure AI Foundry (hub and projects). For information on Azure AI services, see the [Azure AI services documentation](/azure/ai-services/cognitive-services-virtual-networks).

:::image type="content" source="../media/how-to/network/azure-ai-network-inbound.svg" alt-text="Diagram of Azure AI Foundry hub network isolation." lightbox="../media/how-to/network/azure-ai-network-inbound.png":::

You get several hub default resources in your resource group. You need to configure following network isolation configurations.

- Disable public network access of hub default resources such as Azure Storage, Azure Key Vault, and Azure Container Registry.
- Establish private endpoint connection to hub default resources. You need to have both a blob and file private endpoint for the default storage account.
- If your storage account is private, [assign roles](#private-storage-configuration) to allow access.

## Prerequisites

* You must have an existing Azure Virtual Network to create the private endpoint in. 

    > [!IMPORTANT]
    > We do not recommend using the 172.17.0.0/16 IP address range for your VNet. This is the default subnet range used by the Docker bridge network or on-premises.

* Disable network policies for private endpoints before adding the private endpoint.

## Create a hub that uses a private endpoint

If you are creating a new hub, use the following methods to create the hub (Azure portal or Azure CLI). Each of these methods __requires an existing virtual network__:

:::zone pivot="azure-portal"

> [!NOTE]
> The information in this document is only about configuring a private link. For a walkthrough of creating a secure hub in the portal, see [Create a secure hub in the Azure portal](create-secure-ai-hub.md).

1. From the [Azure portal](https://portal.azure.com), search for __Azure AI Foundry__ and create a new resource by selecting __+ New Azure AI__.
1. After configuring the __Basics__ and __Storage__ tabs, select the __Networking__ tab and pick the __Network isolation__ option that best suits your needs.

    :::image type="content" source="../media/how-to/network/ai-hub-networking.png" alt-text="Screenshot of the Create a hub with the option to set network isolation information." lightbox="../media/how-to/network/ai-hub-networking.png":::

1. Scroll down to __Workspace Inbound access__ and choose __+ Add__.

    :::image type="content" source="../media/how-to/network/workspace-inbound-access.png" alt-text="Screenshot of the workspace inbound access section." lightbox="../media/how-to/network/workspace-inbound-access.png":::

1. Input required fields. When selecting the __Region__, select the same region as your virtual network.

:::zone-end

:::zone pivot="cli"

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

:::zone-end

---

## Add a private endpoint to a hub

Use one of the following methods to add a private endpoint to an existing hub:

:::zone pivot="azure-portal"

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Settings__, __Networking__, and then select the __Private endpoint connections__ tab. Select __+ Private endpoint__.

    :::image type="content" source="../media/how-to/network/add-private-endpoint.png" alt-text="Screenshot of the private endpoint connections tab":::

1. When going through the forms to create a private endpoint, be sure to:

    - From __Basics__, select the same __Region__ as your virtual network.
    - From __Resource__, select `amlworkspace` as the __target sub-resource__.
    - From the __Virtual Network__ form, select the virtual network and subnet that you want to connect to.
 
1. After populating the forms with any additional network configurations you require, use the __Review + create__ tab to review your settings and select __Create__ to create the private endpoint.

:::zone-end

:::zone pivot="cli"

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

:::zone-end

---

## Remove a private endpoint

You can remove one or all private endpoints for a hub. Removing a private endpoint removes the hub from the Azure Virtual Network that the endpoint was associated with. Removing the private endpoint might prevent the hub from accessing resources in that virtual network, or resources in the virtual network from accessing the workspace. For example, if the virtual network doesn't allow access to or from the public internet.

> [!WARNING]
> Removing the private endpoints for a hub __doesn't make it publicly accessible__. To make the hub publicly accessible, use the steps in the [Enable public access](#enable-public-access) section.

To remove a private endpoint, use the following information:

:::zone pivot="azure-portal"

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Settings__, __Networking__, and then select the __Private endpoint connections__ tab.
1. Select the endpoint to remove and then select __Remove__.

    :::image type="content" source="../media/how-to/network/remove-private-endpoint.png" alt-text="Screenshot of a selected private endpoint with the remove option highlighted.":::

:::zone-end

:::zone pivot="cli"

When using the Azure CLI, use the following command to remove the private endpoint:

```azurecli
az network private-endpoint delete \
    --name <private-endpoint-name> \
    --resource-group <resource-group-name>
```

:::zone-end

---

## Enable public access

In some situations, you might want to allow someone to connect to your secured hub over a public endpoint, instead of through the virtual network. Or you might want to remove the workspace from the virtual network and re-enable public access.

> [!IMPORTANT]
> Enabling public access doesn't remove any private endpoints that exist. All communications between components behind the virtual network that the private endpoint(s) connect to are still secured. It enables public access only to the hub, in addition to the private access through any private endpoints.

To enable public access, use the following steps:

:::zone pivot="azure-portal"

1. From the [Azure portal](https://portal.azure.com), select your hub.
1. From the left side of the page, select __Networking__ and then select the __Public access__ tab.
1. Select __Enabled from all networks__, and then select __Save__.

:::zone-end

:::zone pivot="cli"

Use the following Azure CLI command to enable public access:

```azurecli
az ml workspace update --set public_network_access=Enabled -n <workspace-name> -g <resource-group-name>
```

If you receive an error that the `ml` command isn't found, use the following commands to install the Azure Machine Learning CLI extension:

```azurecli
az extension add --name ml
```

:::zone-end

---

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
    > Your storage account may have multiple private endpoints. You need to assign the `Reader` role to each private endpoint for your Azure AI Foundry project managed identity.

1. Assign the `Storage Blob Data reader` role to your developers. This role allows them to read data from the storage account.

1. Verify that the project's connection to the storage account uses Microsoft Entra ID for authentication. To view the connection information, go to the __Management center__, select __Connected resources__, and then select the storage account connections. If the credential type isn't Entra ID, select the pencil icon to update the connection and set the __Authentication method__ to __Microsoft Entra ID__.

For information on securing playground chat, see [Securely use playground chat](secure-data-playground.md).

## Custom DNS configuration

See [Azure Machine Learning custom DNS](/azure/machine-learning/how-to-custom-dns#example-custom-dns-server-hosted-in-vnet) article for the DNS forwarding configurations.

If you need to configure custom DNS server without DNS forwarding, use the following patterns for the required A records.

* `<AI-STUDIO-GUID>.workspace.<region>.cert.api.azureml.ms`
* `<AI-PROJECT-GUID>.workspace.<region>.cert.api.azureml.ms`
* `<AI-STUDIO-GUID>.workspace.<region>.api.azureml.ms`
* `<AI-PROJECT-GUID>.workspace.<region>.api.azureml.ms`
* `ml-<workspace-name, truncated>-<region>-<AI-STUDIO-GUID>.<region>.notebooks.azure.net`
* `ml-<workspace-name, truncated>-<region>-<AI-PROJECT-GUID>.<region>.notebooks.azure.net`

    > [!NOTE]
    > The workspace name for this FQDN might be truncated. Truncation is done to keep `ml-<workspace-name, truncated>-<region>-<workspace-guid>` at 63 characters or less.
* `<instance-name>.<region>.instances.azureml.ms`

    > [!NOTE]
    > * Compute instances can be accessed only from within the virtual network.
    > * The IP address for this FQDN is **not** the IP of the compute instance. Instead, use the private IP address of the workspace private endpoint (the IP of the `*.api.azureml.ms` entries.)

* `<instance-name>.<region>.instances.azureml.ms` - Only used by the `az ml compute connect-ssh` command to connect to computers in a managed virtual network. Not needed if you aren't using a managed network or SSH connections.

* `<managed online endpoint name>.<region>.inference.ml.azure.com` - Used by managed online endpoints
* `models.ai.azure.com` - Used for deploying Models as a Service

To find the private IP addresses for your A records, see the [Azure Machine Learning custom DNS](/azure/machine-learning/how-to-custom-dns#find-the-ip-addresses) article.
To check AI-PROJECT-GUID, go to the Azure portal, select your project, settings, properties, and the workspace ID is displayed.

## Limitations

* You might encounter problems trying to access the private endpoint for your hub if you're using Mozilla Firefox. This problem might be related to DNS over HTTPS in Mozilla Firefox. We recommend using Microsoft Edge or Google Chrome.

## Next steps

- [Create an Azure AI Foundry project](create-projects.md)
- [Learn more about Azure AI Foundry](../what-is-azure-ai-foundry.md)
- [Learn more about Azure AI Foundry hubs](../concepts/ai-resources.md)
- [Troubleshoot secure connectivity to a project](troubleshoot-secure-connection-project.md)
